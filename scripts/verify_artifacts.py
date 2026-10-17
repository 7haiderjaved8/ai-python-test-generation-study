#!/usr/bin/env python3
"""
verify_artifacts.py - Independent Artifact Verification Script.

Verifies the integrity, completeness, and internal consistency of the
preserved experimental artifact package in SoftwareTesting-Submission:
- artifacts/index.json
- artifacts/generated/ (112 test snippets)
- artifacts/reference/ (56 unique test snippets)
- results/experiment_log.csv

Scope & Limitations:
This script verifies the integrity and internal consistency of the submitted
artifact package. It confirms that all 112 experimental targets and 56 reference
baselines are preserved, non-empty, byte-consistent with recorded SHA-256 hashes,
and reproduce the exact-match classifications reported in experiment_log.csv.
It cannot independently prove that the generated files were produced by the
underlying AI model or that they match the original external Git repositories;
those properties depend on the original generation workspace and logs.

Uses only the Python standard library.
"""

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


def resolve_repo_root() -> Path:
    """Locate the SoftwareTesting-Submission repository root directory."""
    if len(sys.argv) > 1:
        custom_path = Path(sys.argv[1]).resolve()
        if (custom_path / "artifacts" / "index.json").is_file():
            return custom_path
        if (custom_path / "results" / "experiment_log.csv").is_file():
            return custom_path
        if (custom_path / "experiment_log.csv").is_file():
            return custom_path.parent

    # 1. Prefer script directory's parent (SoftwareTesting-Submission)
    script_parent = Path(__file__).resolve().parent.parent
    if (script_parent / "artifacts" / "index.json").is_file():
        return script_parent

    # 2. Try current working directory
    cwd = Path.cwd().resolve()
    if (cwd / "artifacts" / "index.json").is_file():
        return cwd

    # 3. Fallback checks
    if (script_parent / "results" / "experiment_log.csv").is_file():
        return script_parent
    if (cwd / "results" / "experiment_log.csv").is_file():
        return cwd

    raise FileNotFoundError(
        "Could not locate SoftwareTesting-Submission repository root. "
        "Please run from repository root or supply root path as argument."
    )


def verify_safe_path(base_dir: Path, rel_path_str: str) -> Path:
    """
    Ensure relative path stays strictly within the repository base_dir.
    Rejects directory traversal attempts or absolute path escapes.
    """
    target = (base_dir / rel_path_str).resolve()
    try:
        target.relative_to(base_dir.resolve())
    except ValueError:
        raise ValueError(
            f"Unsafe path detected: '{rel_path_str}' escapes repository root '{base_dir}'."
        )
    return target


def main() -> int:
    try:
        repo_root = resolve_repo_root()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    artifacts_dir = repo_root / "artifacts"
    generated_dir = artifacts_dir / "generated"
    reference_dir = artifacts_dir / "reference"
    index_path = artifacts_dir / "index.json"
    csv_path = repo_root / "results" / "experiment_log.csv"

    print("=" * 72)
    print(" EXPERIMENTAL ARTIFACT PACKAGE VERIFICATION")
    print(f" Repository Root: {repo_root}")
    print("=" * 72)

    failures = []

    def check(condition: bool, msg: str) -> None:
        if not condition:
            failures.append(msg)
            print(f"  [FAIL] {msg}")
        else:
            print(f"  [PASS] {msg}")

    # -------------------------------------------------------------------------
    # 1. Verify existence of required directories and files
    # -------------------------------------------------------------------------
    print("\n[Step 1] Verifying Artifact Structure & Manifests...")
    check(artifacts_dir.is_dir(), f"Artifacts directory exists: {artifacts_dir.name}")
    check(generated_dir.is_dir(), f"Generated directory exists: {generated_dir.name}")
    check(reference_dir.is_dir(), f"Reference directory exists: {reference_dir.name}")
    check(index_path.is_file(), f"Index file exists: {index_path.name}")
    check(csv_path.is_file(), f"Experiment log CSV exists: {csv_path.name}")

    if failures:
        print(f"\nABORTING: Missing foundational files ({len(failures)} failures).", file=sys.stderr)
        return 1

    # -------------------------------------------------------------------------
    # 2. Verify file counts on disk
    # -------------------------------------------------------------------------
    print("\n[Step 2] Verifying Artifact File Counts on Disk...")
    gen_files = list(generated_dir.glob("*.py"))
    ref_files = list(reference_dir.glob("*.py"))

    check(len(gen_files) == 112, f"Exactly 112 generated .py files on disk (found: {len(gen_files)})")
    check(len(ref_files) == 56, f"Exactly 56 reference .py files on disk (found: {len(ref_files)})")

    # Ensure no unexpected non-py or extraneous files
    all_gen_entries = list(generated_dir.iterdir())
    all_ref_entries = list(reference_dir.iterdir())
    check(len(all_gen_entries) == 112, f"No extraneous files in generated/ (found: {len(all_gen_entries)})")
    check(len(all_ref_entries) == 56, f"No extraneous files in reference/ (found: {len(all_ref_entries)})")

    # -------------------------------------------------------------------------
    # 3. Load & validate index.json and experiment_log.csv
    # -------------------------------------------------------------------------
    print("\n[Step 3] Loading & Validating index.json and CSV Records...")
    try:
        with open(index_path, mode="r", encoding="utf-8") as f:
            index_records = json.load(f)
    except Exception as e:
        check(False, f"Failed to parse index.json: {e}")
        return 1

    check(isinstance(index_records, list), "index.json root is a JSON list")
    check(len(index_records) == 112, f"Exactly 112 index records in index.json (found: {len(index_records)})")

    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
    except Exception as e:
        check(False, f"Failed to parse experiment_log.csv: {e}")
        return 1

    check(len(csv_rows) == 112, f"Exactly 112 experiment rows in experiment_log.csv (found: {len(csv_rows)})")

    csv_by_eid = {}
    for r in csv_rows:
        eid = r["experiment_id"].strip()
        if eid in csv_by_eid:
            check(False, f"Duplicate experiment_id in CSV: {eid}")
        csv_by_eid[eid] = r
    check(len(csv_by_eid) == 112, f"Exactly 112 unique experiment IDs in CSV (found: {len(csv_by_eid)})")

    # -------------------------------------------------------------------------
    # 4. Detailed per-record verification
    # -------------------------------------------------------------------------
    print("\n[Step 4] Verifying Index Records, SHA-256 Integrity & Exact Matches...")
    index_eids = set()
    ref_usage = defaultdict(list)
    
    total_exact_matches = 0
    total_non_exact_matches = 0
    wc_exact_matches = 0
    woc_exact_matches = 0

    required_keys = [
        "experiment_id",
        "project",
        "condition",
        "target_sequence",
        "original_test_file_path",
        "class_name",
        "function_name",
        "generated_artifact_path",
        "reference_artifact_path",
        "exact_match_original",
        "sha256_generated",
        "sha256_reference",
        "source_revision",
    ]

    for idx, record in enumerate(index_records):
        eid = record.get("experiment_id")
        if not eid:
            check(False, f"Record #{idx} missing experiment_id")
            continue

        if eid in index_eids:
            check(False, f"Duplicate experiment_id in index: {eid}")
        index_eids.add(eid)

        # Match against CSV row
        csv_row = csv_by_eid.get(eid)
        if not csv_row:
            check(False, f"Indexed experiment_id '{eid}' has no corresponding row in CSV")
            continue

        # Check required schema keys
        for k in required_keys:
            if k not in record:
                check(False, f"{eid}: missing required field '{k}' in index.json")

        # Verify path safety
        gen_rel = record.get("generated_artifact_path", "")
        ref_rel = record.get("reference_artifact_path", "")

        try:
            gen_path = verify_safe_path(repo_root, gen_rel)
            ref_path = verify_safe_path(repo_root, ref_rel)
        except ValueError as pe:
            check(False, f"{eid}: path safety violation - {pe}")
            continue

        # Verify file existence and nonempty content
        if not gen_path.is_file():
            check(False, f"{eid}: generated file does not exist at '{gen_rel}'")
            continue
        if not ref_path.is_file():
            check(False, f"{eid}: reference file does not exist at '{ref_rel}'")
            continue

        gen_text = gen_path.read_text(encoding="utf-8")
        ref_text = ref_path.read_text(encoding="utf-8")

        if len(gen_text.strip()) == 0:
            check(False, f"{eid}: generated file '{gen_rel}' is empty")
        if len(ref_text.strip()) == 0:
            check(False, f"{eid}: reference file '{ref_rel}' is empty")

        # Recalculate SHA-256
        calc_gen_sha = hashlib.sha256(gen_text.encode("utf-8")).hexdigest()
        calc_ref_sha = hashlib.sha256(ref_text.encode("utf-8")).hexdigest()

        if calc_gen_sha != record.get("sha256_generated"):
            check(False, f"{eid}: generated SHA-256 mismatch (disk: {calc_gen_sha}, index: {record.get('sha256_generated')})")
        if calc_ref_sha != record.get("sha256_reference"):
            check(False, f"{eid}: reference SHA-256 mismatch (disk: {calc_ref_sha}, index: {record.get('sha256_reference')})")

        # Recalculate snippet-level exact match using CRLF/LF normalization only
        gen_norm = gen_text.replace("\r\n", "\n")
        ref_norm = ref_text.replace("\r\n", "\n")
        recalc_em = (gen_norm == ref_norm)

        # Compare with CSV classification
        csv_em = csv_row["exact_match_original"].strip().upper() == "YES"
        index_csv_em = record.get("exact_match_original", "").strip().upper() == "YES"

        if recalc_em != csv_em:
            check(False, f"{eid}: recalculated exact match ({recalc_em}) differs from CSV ({csv_em})")
        if recalc_em != index_csv_em:
            check(False, f"{eid}: recalculated exact match ({recalc_em}) differs from index ({index_csv_em})")

        cond = record.get("condition", "").strip()
        if recalc_em:
            total_exact_matches += 1
            if cond in ("With-Context", "WC"):
                wc_exact_matches += 1
            elif cond in ("Without-Context", "WOC"):
                woc_exact_matches += 1
            else:
                check(False, f"{eid}: unrecognized condition '{cond}'")
        else:
            total_non_exact_matches += 1

        # Track reference usage
        ref_usage[ref_rel].append((eid, cond))

    check(len(index_eids) == 112, f"All 112 experiment IDs uniquely validated (count: {len(index_eids)})")

    # -------------------------------------------------------------------------
    # 5. Verify condition-level exact match counts
    # -------------------------------------------------------------------------
    print("\n[Step 5] Confirming Exact-Match Statistical Benchmarks...")
    check(total_exact_matches == 86, f"Exactly 86 total exact matches (recalculated: {total_exact_matches})")
    check(total_non_exact_matches == 26, f"Exactly 26 total non-exact matches (recalculated: {total_non_exact_matches})")
    check(wc_exact_matches == 44, f"Exactly 44 WC exact matches (recalculated: {wc_exact_matches})")
    check(woc_exact_matches == 42, f"Exactly 42 WOC exact matches (recalculated: {woc_exact_matches})")

    # -------------------------------------------------------------------------
    # 6. Verify reference file sharing (exactly 1 WC and 1 WOC pair)
    # -------------------------------------------------------------------------
    print("\n[Step 6] Verifying Reference Target Pairing (1 WC + 1 WOC per Target)...")
    check(len(ref_usage) == 56, f"Exactly 56 unique reference files referenced (found: {len(ref_usage)})")

    invalid_pairings = 0
    for ref_rel, exp_list in ref_usage.items():
        if len(exp_list) != 2:
            check(False, f"Reference '{ref_rel}' used by {len(exp_list)} experiments instead of 2: {[e[0] for e in exp_list]}")
            invalid_pairings += 1
            continue
        conds = {c for _, c in exp_list}
        is_paired = (conds == {"With-Context", "Without-Context"}) or (conds == {"WC", "WOC"})
        if not is_paired:
            check(False, f"Reference '{ref_rel}' does not pair WC with WOC (found conditions: {conds})")
            invalid_pairings += 1

    check(invalid_pairings == 0, f"All 56 reference files are correctly paired across exactly 1 WC and 1 WOC experiment")

    # -------------------------------------------------------------------------
    # Verification Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print(" ARTIFACT VERIFICATION SUMMARY")
    print("=" * 72)
    print(f" Total Experiments Verified:       {len(index_eids)} / 112")
    print(f" Unique Reference Baselines:       {len(ref_usage)} / 56")
    print(f" Generated Files Verified on Disk: {len(gen_files)} / 112")
    print(f" Reference Files Verified on Disk: {len(ref_files)} / 56")
    print(f" Recalculated Exact Matches:       {total_exact_matches} (WC: {wc_exact_matches}, WOC: {woc_exact_matches})")
    print(f" Recalculated Non-Exact Matches:   {total_non_exact_matches}")
    print(f" Total Verification Checks Failed: {len(failures)}")
    print("=" * 72)

    if failures:
        print(f"\nFAILED: {len(failures)} verification checks failed.", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\nSUCCESS: All artifact integrity and consistency checks passed cleanly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
