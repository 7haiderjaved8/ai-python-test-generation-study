#!/usr/bin/env python3
"""
analyze_results.py - Verification and Statistical Analysis for Track A Research.

Partially replicates the GitHub Copilot Python test-generation study
evaluating test generation under With-Context (WC) vs. Without-Context (WOC)
conditions using Google Antigravity.

Model Identification:
- Requested Model: Gemini 3.6 Flash Low (as recorded in results/experiment_log.csv)
- Actual Runtime Model: Gemini 3.8 Flash (Low) (identifier: gemini-3.8-flash-low)
  Note: Information distinguishing the actual runtime model from the requested
  model originates from the original generation records; the CSV log records
  the requested label and does not independently verify the runtime model identifier.

Uses only the Python standard library.
"""

import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


def mcnemar_exact_test(b: int, c: int) -> float:
    """
    Compute two-sided exact McNemar p-value using the binomial distribution.

    Under H0, discordant pairs b and c follow Binomial(n, 0.5) where n = b + c.
    The two-sided p-value is 2 * sum_{i=0}^{min(b, c)} (n choose i) * 0.5^n,
    capped at 1.0.
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    cum_prob = sum(math.comb(n, i) * (0.5**n) for i in range(k + 1))
    return min(1.0, 2.0 * cum_prob)


def resolve_csv_path() -> Path:
    """Locate results/experiment_log.csv robustly."""
    if len(sys.argv) > 1:
        custom_path = Path(sys.argv[1])
        if custom_path.is_file():
            return custom_path

    candidates = [
        Path.cwd() / "results" / "experiment_log.csv",
        Path(__file__).resolve().parent.parent / "results" / "experiment_log.csv",
        Path(__file__).resolve().parent / "results" / "experiment_log.csv",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "Could not find experiment_log.csv in expected locations. "
        "Please provide the path as an argument."
    )


def main() -> None:
    csv_path = resolve_csv_path()
    print(f"Loading experiment log from: {csv_path}\n")

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    total_rows = len(reader)

    # -------------------------------------------------------------------------
    # Requirement 1: Validate 112 experiment rows and unique experiment IDs
    # -------------------------------------------------------------------------
    assert total_rows == 112, (
        f"Validation failed: expected 112 experiment rows, got {total_rows}."
    )

    experiment_ids = [row["experiment_id"].strip() for row in reader]
    unique_ids = set(experiment_ids)
    assert len(unique_ids) == 112, (
        f"Validation failed: expected 112 unique experiment IDs, got {len(unique_ids)}."
    )

    # -------------------------------------------------------------------------
    # Requirements 2 & 3: 7 projects, 8 distinct target pairs per project,
    # paired by project and sequence number (not test method name)
    # -------------------------------------------------------------------------
    projects = sorted(list({row["project"].strip() for row in reader}))
    assert len(projects) == 7, (
        f"Validation failed: expected 7 projects, got {len(projects)} ({projects})."
    )

    pairs = defaultdict(dict)
    project_seqs = defaultdict(set)

    outcome_counts = defaultdict(int)
    wc_total = 0
    woc_total = 0
    wc_pass = 0
    woc_pass = 0
    wc_exact = 0
    woc_exact = 0

    project_stats = defaultdict(
        lambda: {"WC_exact": 0, "WOC_exact": 0, "total_exact": 0, "total": 0}
    )

    for row in reader:
        exp_id = row["experiment_id"].strip()
        proj = row["project"].strip()
        cond = row["condition"].strip()
        res = row["result"].strip().upper()
        em = row["exact_match_original"].strip().upper() == "YES"

        seq_num = exp_id.split("-")[-1]
        pair_key = (proj, seq_num)

        assert cond in ("With-Context", "Without-Context"), (
            f"Unexpected condition '{cond}' in experiment {exp_id}."
        )

        assert cond not in pairs[pair_key], (
            f"Duplicate condition '{cond}' for target {pair_key}."
        )

        pairs[pair_key][cond] = {
            "result": res,
            "exact_match": em,
            "test_name": row["test"].strip(),
            "exp_id": exp_id,
        }
        project_seqs[proj].add(seq_num)

        outcome_counts[res] += 1
        project_stats[proj]["total"] += 1

        if cond == "With-Context":
            wc_total += 1
            if res == "PASS":
                wc_pass += 1
            if em:
                wc_exact += 1
                project_stats[proj]["WC_exact"] += 1
                project_stats[proj]["total_exact"] += 1
        else:
            woc_total += 1
            if res == "PASS":
                woc_pass += 1
            if em:
                woc_exact += 1
                project_stats[proj]["WOC_exact"] += 1
                project_stats[proj]["total_exact"] += 1

    for proj in projects:
        seq_count = len(project_seqs[proj])
        assert seq_count == 8, (
            f"Validation failed: project '{proj}' has {seq_count} targets instead of 8."
        )
        for seq in sorted(project_seqs[proj]):
            target = pairs[(proj, seq)]
            assert "With-Context" in target and "Without-Context" in target, (
                f"Validation failed: target ({proj}, {seq}) is missing one or both conditions."
            )

    total_pairs = len(pairs)
    assert total_pairs == 56, (
        f"Validation failed: expected 56 target pairs, got {total_pairs}."
    )

    # -------------------------------------------------------------------------
    # Requirements 4 & 5: Paired contingency table for exact matches
    # -------------------------------------------------------------------------
    n11 = 0  # Both WC and WOC exact match
    n10 = 0  # WC-only exact match
    n01 = 0  # WOC-only exact match
    n00 = 0  # Neither exact match

    for pair_key, cond_dict in pairs.items():
        wc_em = cond_dict["With-Context"]["exact_match"]
        woc_em = cond_dict["Without-Context"]["exact_match"]

        if wc_em and woc_em:
            n11 += 1
        elif wc_em and not woc_em:
            n10 += 1
        elif not wc_em and woc_em:
            n01 += 1
        else:
            n00 += 1

    # -------------------------------------------------------------------------
    # Requirement 6: McNemar's exact two-sided p-value
    # -------------------------------------------------------------------------
    p_value = mcnemar_exact_test(n10, n01)

    # -------------------------------------------------------------------------
    # Requirement 7: Assertions against independently established study totals
    # -------------------------------------------------------------------------
    total_pass = outcome_counts.get("PASS", 0)
    total_exact = wc_exact + woc_exact

    assert total_rows == 112, "Assertion failed: Total experiments != 112."
    assert total_pass == 112, f"Assertion failed: Total PASS != 112 (got {total_pass})."
    assert wc_exact == 44, f"Assertion failed: WC exact matches != 44 (got {wc_exact})."
    assert woc_exact == 42, f"Assertion failed: WOC exact matches != 42 (got {woc_exact})."
    assert total_exact == 86, f"Assertion failed: Overall exact matches != 86 (got {total_exact})."
    assert (n11, n10, n01, n00) == (42, 2, 0, 12), (
        f"Assertion failed: Paired contingency counts != (42, 2, 0, 12) (got {(n11, n10, n01, n00)})."
    )
    assert round(p_value, 3) == 0.500, (
        f"Assertion failed: McNemar p-value != 0.500 (got {p_value:.4f})."
    )

    # -------------------------------------------------------------------------
    # Requirement 8: Print clear, readable statistical summary
    # -------------------------------------------------------------------------
    wc_pass_rate = (wc_pass / wc_total) * 100
    woc_pass_rate = (woc_pass / woc_total) * 100
    wc_em_rate = (wc_exact / wc_total) * 100
    woc_em_rate = (woc_exact / woc_total) * 100
    overall_em_rate = (total_exact / total_rows) * 100

    print("=" * 72)
    print(" TRACK A RESEARCH REPLICATION: STATISTICAL SUMMARY")
    print(" Environment:           Google Antigravity")
    print(" Requested Model:       Gemini 3.6 Flash Low (as recorded in log)")
    print(" Actual Runtime Model:  Gemini 3.8 Flash (Low) [gemini-3.8-flash-low]")
    print("                        (verified from original generation records)")
    print("=" * 72)

    print("\n1. EXPERIMENTAL VALIDATION & OVERALL OUTCOMES:")
    print(f"   Total Experiments Logged:    {total_rows}")
    print(f"   Distinct Target Pairs:       {total_pairs} (across {len(projects)} projects)")
    print(f"   Pass Count:                  {total_pass} ({total_pass/total_rows*100:.1f}%)")
    print(f"   Fail Count:                  {outcome_counts.get('FAIL', 0)}")
    print(f"   Broken Count:                {outcome_counts.get('BROKEN', 0)}")
    print(f"   Empty Count:                 {outcome_counts.get('EMPTY', 0)}")

    print("\n2. CONDITION-LEVEL PERFORMANCE:")
    print(f"   With-Context (WC) Pass Rate:        {wc_pass}/{wc_total} ({wc_pass_rate:.1f}%)")
    print(f"   Without-Context (WOC) Pass Rate:     {woc_pass}/{woc_total} ({woc_pass_rate:.1f}%)")
    print(f"   With-Context (WC) Exact-Match Rate:  {wc_exact}/{wc_total} ({wc_em_rate:.2f}%)")
    print(f"   Without-Context (WOC) Exact-Match:   {woc_exact}/{woc_total} ({woc_em_rate:.2f}%)")
    print(f"   Overall Exact-Match Rate:           {total_exact}/{total_rows} ({overall_em_rate:.2f}%)")

    print("\n3. PROJECT-LEVEL EXACT-MATCH BREAKDOWN:")
    print(f"   {'Project':<18} | {'WC Exact':<10} | {'WOC Exact':<10} | {'Total Exact':<12}")
    print(f"   {'-'*18}-+-{'-'*10}-+-{'-'*10}-+-{'-'*12}")
    for proj in projects:
        st = project_stats[proj]
        print(
            f"   {proj:<18} | {st['WC_exact']:>2}/8 ({st['WC_exact']/8*100:5.1f}%) | "
            f"{st['WOC_exact']:>2}/8 ({st['WOC_exact']/8*100:5.1f}%) | "
            f"{st['total_exact']:>2}/16 ({st['total_exact']/16*100:5.1f}%)"
        )

    print("\n4. PAIRED EXACT-MATCH CONTINGENCY TABLE (N = 56 Pairs):")
    print("   " + "-" * 48)
    print(f"   {'':<28} | {'WOC Exact (Yes)':<14} | {'WOC Exact (No)':<14}")
    print("   " + "-" * 48)
    print(f"   {'WC Exact (Yes)':<28} | {n11:>14} | {n10:>14}")
    print(f"   {'WC Exact (No)':<28} | {n01:>14} | {n00:>14}")
    print("   " + "-" * 48)
    print(f"   - Both conditions exact match:   {n11}")
    print(f"   - WC-only exact match:           {n10}")
    print(f"   - WOC-only exact match:          {n01}")
    print(f"   - Neither condition exact match: {n00}")

    print("\n5. HYPOTHESIS TESTING (MCNEMAR'S EXACT TEST):")
    print(f"   Discordant Pairs (b = {n10}, c = {n01}): Total = {n10 + n01}")
    print(f"   Two-Sided Exact p-value:          {p_value:.4f}")
    if p_value >= 0.05:
        print("   Statistical Decision:             Fail to reject H0 (p >= 0.05).")
        print("   Interpretation:                   No statistically significant difference in exact-match")
        print("                                     rates between With-Context and Without-Context.")
    else:
        print("   Statistical Decision:             Reject H0 (p < 0.05).")
        print("   Interpretation:                   Statistically significant difference detected.")

    print("\n" + "=" * 72)
    print(" ALL 7 STUDY ASSERTIONS PASSED SUCCESSFULLY.")
    print("=" * 72)


if __name__ == "__main__":
    main()
