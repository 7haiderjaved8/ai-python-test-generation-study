# Evaluating Agentic AI for Python Test Generation: An Empirical Extension of a GitHub Copilot Study

**Course:** Software Testing (A.Y. 2025–2026)  
**Instructor:** Prof. Vincenzo Riccio  
**Track:** Track A – Research  
**Project Type:** Individual Final Project  

---

## 1. Project Overview

This repository contains the empirical data, verification artifacts, and statistical analysis scripts for an individual research project evaluating modern agentic Large Language Models (LLMs) on unit test generation for Python software. 

The study partially replicates and extends the experimental framework established by **El Haji, Brandt, and Zaidman (AST 2024)** in their empirical evaluation of GitHub Copilot. While the original study evaluated commercial code-completion models, this research assesses **Google Antigravity** backed by Google DeepMind's Gemini Flash family under two experimental conditions:
1. **With-Context (WC):** The agent receives the target test signature alongside the implementation source code of the module under test.
2. **Without-Context (WOC):** The agent receives only the test signature and docstring without access to implementation files.

A total of **112 test generation experiments** (56 target pairs across 7 open-source projects) were executed and evaluated using isolated Docker-based test environments.

---

## 2. Original Research Paper

This empirical study builds upon and extends the following baseline publication:

* **Title:** *Using GitHub Copilot for Test Generation in Python: An Empirical Study*
* **Authors:** Khalid El Haji, Carolin Brandt, Andy Zaidman
* **Venue:** *Proceedings of the 5th ACM/IEEE International Conference on Automation of Software Test (AST 2024)*, Lisbon, Portugal
* **DOI:** [10.1145/3644032.3644443](https://doi.org/10.1145/3644032.3644443)

### Comparison with the Original Study
* **Original Work (El Haji et al., AST 2024):** Evaluated GitHub Copilot on Python repositories, analyzing pass rates, test smells, and coverage across broad test suites.
* **Our Extension:** Evaluates Google Antigravity (Gemini 3.8 Flash Low) across 7 selected open-source projects, analyzing pass rates and exact textual convergence against human-written ground truth tests under With-Context and Without-Context conditions.

---

## 3. Research Objectives

The research investigates three primary questions:

* **RQ1 (Executable Correctness):** Can modern agentic models generate syntactically valid and passing unit tests without human intervention?
* **RQ2 (Ground-Truth Convergence):** How frequently does the generated test logic converge textually to the original human developer's implementation?
* **RQ3 (Context Sensitivity):** Does providing full implementation context (With-Context) yield a statistically significant advantage over prompt-only generation (Without-Context) in exact-match convergence?

---

## 4. Experimental Methodology

### Experimental Pipeline
1. **Target Selection:** 8 distinct unit test targets were selected from each of the 7 subject repositories ($7 \times 8 = 56$ paired targets).
2. **Generation Protocol:**
   * One generation attempt per target per condition ($k = 1$), yielding 56 With-Context runs and 56 Without-Context runs (**112 total experiments**).
   * Generative prompts followed standardized templates specifying test function names, parameters, and expected behaviors.
3. **Execution & Evaluation:**
   * Each generated test was placed in its respective repository checkout and executed inside an isolated Docker container matching the target project's runtime dependencies.
   * Execution outcomes and string equality against the human baseline were recorded.

### Model Identification & Telemetry
* **Requested Model Setting:** `Gemini 3.6 Flash Low` (recorded in [`results/experiment_log.csv`](results/experiment_log.csv))
* **Actual Runtime Model Engine:** `Gemini 3.8 Flash (Low)` (runtime identifier: `gemini-3.8-flash-low`)
* **Note on Model Designation:** The experiment log preserves the user-requested model setting. Telemetry from the original execution logs confirms that the underlying API served the `gemini-3.8-flash-low` model. The CSV records the requested configuration label and does not independently authenticate the runtime model identifier.

---

## 5. Subject Projects

Seven diverse open-source Python projects spanning multiple application domains and Python runtime versions were examined:

| Project | Domain | Python Version | Test Framework | Selected Targets |
| :--- | :--- | :---: | :---: | :---: |
| **`click`** | CLI parsing framework | 3.11.17 | `pytest` | 8 |
| **`django-multiurl`** | URL routing library | 3.6.15 / Django 2.2.28 | `unittest` | 8 |
| **`exif`** | Image metadata parser/editor | 3.11.17 | `pytest` | 8 |
| **`pyexperiment`** | Experiment framework | 3.6.15 | `unittest` | 8 |
| **`pyspread`** | Python spreadsheet GUI | 3.10.22 | `pytest` | 8 |
| **`python-crontab`** | Cron schedule parser | 3.11.17 | `unittest` | 8 |
| **`python-lottie`** | Vector animation library | 3.11.17 | `unittest` | 8 |
| **Total** | — | — | — | **56 Targets (112 runs)** |

*Note on Sample Size:* The uniform sample size of $N=8$ targets per project was established by `django-multiurl`, whose complete test suite contains exactly 8 test methods in [`artifacts/index.json`](artifacts/index.json).

---

## 6. Evaluation Metrics

1. **Execution Outcome:**
   * **PASS:** The generated test executed without errors and passed all assertions within the project's native test runner (`pytest` or `unittest`).
   * **FAIL:** The test executed but raised an assertion error.
   * **BROKEN:** The test raised an unhandled exception or runtime/syntax error.
   * **EMPTY:** The model returned empty code or non-code output.
2. **Exact Textual Match:**
   * Evaluated as a binary indicator (`YES` / `NO`).
   * Compares the generated test function body against the human-written reference test.
   * Normalization is strictly limited to line endings (converting `\r\n` to `\n`) without AST restructuring, variable renaming, or comment deletion.

---

## 7. Results

### 1. Overall Execution Outcomes
Across all 112 generation attempts, the model achieved a **100% Pass Rate**:
* **PASS:** 112 / 112 (100.0%)
* **FAIL / BROKEN / EMPTY:** 0 / 112 (0.0%)

### 2. Condition-Level Exact-Match Rates
* **With-Context (WC):** 44 / 56 exact matches (**78.57%**)
* **Without-Context (WOC):** 42 / 56 exact matches (**75.00%**)
* **Overall Exact Match:** 86 / 112 (**76.79%**)

### 3. Project-Level Breakdown

| Project | With-Context (WC) | Without-Context (WOC) | Total Exact Match |
| :--- | :---: | :---: | :---: |
| `click` | 0 / 8 (0.0%) | 0 / 8 (0.0%) | 0 / 16 (0.0%) |
| `django-multiurl` | 8 / 8 (100.0%) | 8 / 8 (100.0%) | 16 / 16 (100.0%) |
| `exif` | 7 / 8 (87.5%) | 7 / 8 (87.5%) | 14 / 16 (87.5%) |
| `pyexperiment` | 8 / 8 (100.0%) | 7 / 8 (87.5%) | 15 / 16 (93.8%) |
| `pyspread` | 8 / 8 (100.0%) | 8 / 8 (100.0%) | 16 / 16 (100.0%) |
| `python-crontab` | 5 / 8 (62.5%) | 5 / 8 (62.5%) | 10 / 16 (62.5%) |
| `python-lottie` | 8 / 8 (100.0%) | 7 / 8 (87.5%) | 15 / 16 (93.8%) |
| **All Projects** | **44 / 56 (78.57%)** | **42 / 56 (75.00%)** | **86 / 112 (76.79%)** |

### 4. Paired Contingency Table (N = 56 Pairs)

| | WOC Exact (Yes) | WOC Exact (No) | Total |
| :--- | :---: | :---: | :---: |
| **WC Exact (Yes)** | 42 | 2 | 44 |
| **WC Exact (No)** | 0 | 12 | 12 |
| **Total** | 42 | 14 | **56** |

* Both conditions matched original: **42 pairs**
* With-Context only matched original: **2 pairs** (`pyexperiment-001`, `python-lottie-003`)
* Without-Context only matched original: **0 pairs**
* Neither condition matched original: **12 pairs** (all 8 `click` tests, 3 `python-crontab` tests, 1 `exif` test)

### 5. Statistical Significance (McNemar's Exact Test)
* Discordant pairs: $b = 2$, $c = 0$ ($n = 2$)
* Null Hypothesis ($H_0$): Marginal probabilities of exact match under WC and WOC are identical ($p_{10} = p_{01}$).
* **Two-Sided Exact $p$-value:** **$0.5000$**
* **Conclusion:** We fail to reject $H_0$ ($p \ge 0.05$). There is no statistically significant difference in exact-match rates between With-Context and Without-Context generation for this benchmark.

---

## 8. Repository Structure

This repository is organized as a lightweight, reproducible submission package:

```text
SoftwareTesting-Submission/
├── README.md                 # Project documentation and study overview
├── results/
│   └── experiment_log.csv    # Complete CSV log of all 112 experimental runs
├── scripts/
│   ├── analyze_results.py    # Self-contained statistical reproduction script
│   └── verify_artifacts.py   # Artifact package integrity & consistency verification script
├── artifacts/
│   ├── index.json            # Structured manifest and SHA-256 hash index (112 records)
│   ├── generated/            # 112 extracted AI-generated test snippets (.py)
│   └── reference/            # 56 unique human-written reference test snippets (.py)
└── docs/                     # Reserved directory for supplementary reports
```

### Purpose of Preserved Snippets
The extracted Python test snippets in `artifacts/generated/` and `artifacts/reference/` serve as granular **evidence for inspection, direct textual comparison, and hash verification**. 

> [!NOTE]
> These extracted snippets are function- and method-level test definitions; they are **not necessarily standalone executable test modules** on their own. Running them directly as independent Python scripts is not expected, as full project modules, package imports, test harness fixtures, and external runtime dependencies are intentionally not bundled into this compact package.

---

## 9. Reproducing the Statistical Analysis

The statistical analysis, contingency tables, hypothesis tests, and study assertions are fully automated and use **only the Python standard library** (no `pandas`, `scipy`, or `numpy` required).

### Execution Command
From the root of this repository:

```bash
python scripts/analyze_results.py
```

Alternatively, specify an explicit path to the CSV:

```bash
python scripts/analyze_results.py results/experiment_log.csv
```

### What the Script Verifies
1. **Row & ID Integrity:** Confirms exactly 112 rows and 112 unique experiment IDs.
2. **Pairing Integrity:** Validates 7 projects, 8 targets per project, paired strictly by project and sequence number.
3. **Outcome Metrics:** Computes pass rates and exact-match rates per condition and per project.
4. **Contingency Table:** Constructs the $2 \times 2$ paired exact-match matrix.
5. **Exact McNemar Test:** Calculates the binomial two-sided exact $p$-value.
6. **Self-Verifying Assertions:** Programmatically asserts that all calculated metrics match the reported study figures.

---

## 10. Artifact Integrity and Verification

To allow independent verification of the preserved experimental artifact package without access to the original full-scale research workspace, a dedicated validation tool is provided.

### Execution Command
From the root of this repository:

```bash
python scripts/verify_artifacts.py
```

### What the Script Verifies
1. **File Inventory on Disk:** Confirms exactly 112 generated `.py` snippets and 56 reference `.py` snippets with no extraneous files.
2. **Manifest Integrity:** Validates that `artifacts/index.json` contains exactly 112 structured records matching the 112 unique experiment IDs in `results/experiment_log.csv`.
3. **Artifact Existence & Non-Emptiness:** Ensures every indexed generated and reference file exists and contains a non-empty code body.
4. **Cryptographic SHA-256 Hashes:** Recalculates the SHA-256 hash for every file on disk and verifies an exact match against the manifest index.
5. **Target Pairing:** Verifies that each of the 56 unique reference files is associated with exactly two experiments: one With-Context (WC) and one Without-Context (WOC).
6. **Normalized Exact-Match Convergence:** Independently recomputes snippet-level exact matches using strictly CRLF/LF line-ending normalization, confirming:
   * **86 Total Exact Matches**
   * **26 Total Non-Exact Matches**
   * **44 With-Context (WC) Exact Matches**
   * **42 Without-Context (WOC) Exact Matches**
   * **Zero discrepancies** with `results/experiment_log.csv` and `artifacts/index.json`.
7. **Path Safety:** Verifies that all artifact paths are relative and strictly confined within the repository root.

---

## 11. Reproducing the AI Experiments

### Transparency Note on Generative Reproduction
* **Interactive Environment:** The original test generation runs were conducted interactively using the **Google Antigravity** development environment connected to Google's model API.
* **Environment Dependencies:** Each project evaluation required isolated container environments matching legacy Python versions (e.g., Python 3.6 for `django-multiurl` and `pyexperiment`).
* **Generation Pipeline Scope:** A batch, automated generation runner is **not** included in this repository. Running `python scripts/analyze_results.py` **only analyzes and validates** the recorded results from [`results/experiment_log.csv`](results/experiment_log.csv); it **does not** re-query the model API, execute Docker containers, or regenerate test files.

---

## 12. Limitations and Threats to Validity

1. **Construct Validity (Exact Match vs. Semantic Equivalence):**
   * The exact-match metric measures literal convergence to developer-written tests. A test that fails the exact-match criterion can still be functionally valid and achieve 100% branch coverage (as observed in `click`, where tests passed at 100% despite 0 exact matches).
2. **Internal Validity (Pre-Generation Validation):**
   * While all target tests originate from active upstream test suites, pre-generation baseline execution was not logged individually per target in this workspace.
3. **External Validity (Sample Size & Scope):**
   * The benchmark is restricted to 7 open-source Python repositories and 8 targets per repository ($N = 56$ pairs). Findings may not generalize to larger commercial codebases or other languages.
4. **Model Evolution & Non-Determinism:**
   * Commercial LLM APIs evolve continuously. While low-temperature settings were used, minor output variations may occur across different platform revisions.
5. **Cross-Study Comparability (Non-Causal Inference):**
   * Direct performance comparisons between this study and the results reported by El Haji et al. cannot be interpreted as demonstrating a causal improvement of Gemini/Antigravity over GitHub Copilot. The studies differ across multiple non-isolated dimensions, including prompting strategies, model scales, evaluation subsets ($N=8$ targets vs. repository-wide sweeps), and upstream dependency versions.
6. **Provenance and Verification Scope:**
   * The verification script validates the cryptographic integrity, internal consistency, and statistical alignment of the preserved artifacts and log files. It cannot independently authenticate that the snippets were generated by the remote model API or verify upstream external repositories; those claims rely on the original development environment logs.
7. **Packaging Scope:**
   * Complete multi-gigabyte Docker images, container runtime caches, full upstream repository Git clones, and automated generation harnesses are omitted from this submission repository to maintain a clean, lightweight, and auditable distribution.

---

## 13. AI-Use Disclosure

In accordance with academic integrity guidelines:
* **Generative AI Role in Study:** The subject of this research is the empirical evaluation of agentic AI test generation (Google Antigravity / Gemini).
* **AI Assistance in Artifact Preparation:** AI assistance (Antigravity) was utilized for pair-programming assistance, structuring the statistical analysis script, and formatting documentation. All experimental data, statistical calculations, and assertions were independently audited and validated.

---

## 14. References

1. **El Haji, K., Brandt, C., & Zaidman, A.** (2024). Using GitHub Copilot for Test Generation in Python: An Empirical Study. In *Proceedings of the 5th ACM/IEEE International Conference on Automation of Software Test (AST 2024)*. DOI: [10.1145/3644032.3644443](https://doi.org/10.1145/3644032.3644443).
2. **McNemar, Q.** (1947). Note on the sampling error of the difference between correlated proportions or percentages. *Psychometrika*, 12(2), 153–157. DOI: [10.1007/BF02295996](https://doi.org/10.1007/BF02295996).
3. **Google DeepMind.** (2024). Gemini: A Family of Highly Capable Multimodal Models. *arXiv preprint arXiv:2312.11805*.
