# Phase A.0 — Null-Hypothesis Baseline

**What:** empirical test of whether naive-Opus-in-context beats the proposed Refiner mechanism on `/validate-skillmd`, per DR-028 P0-RATIFY-3.

**Why:** gates Phase A. If H₀ holds (naive ≥ 70% of projected Refiner lift), Phase B mechanism descopes.

**Where:** this directory. Bead `bd_000-projects-214c.8`. GH issue `jeremylongshore/j-rig-skill-binary-eval#81`.

## Status

| Session | Date       | Deliverable                                   |
| ------- | ---------- | --------------------------------------------- |
| 1       | 2026-05-28 | DESIGN.md + directory scaffold (this session) |
| 2       | TBD        | Corpus inventory + pre-registration sha       |
| 3       | TBD        | Arm A execution                               |
| 4       | TBD        | Arm B execution + RESULTS.md + BLOG-DRAFT.md  |

## Entry points

- `DESIGN.md` — experimental design (read first)
- `corpus/inventory.md` — corpus + sampling (Session 2)
- `arms/{naive-opus,proposed-refiner}/` — arm-specific runners (Session 3+)
- `judge/validate-skillmd-judge.md` — scorer spec (Session 2)
- `results/` — outputs (gitignored: `results/raw/`; committed: `results/aggregated/`)

## CTO gates before Session 2 (per DESIGN.md § 9)

5 open items must resolve.

## Offline test coverage

From the repository root, install the test dependencies declared in
`.github/workflows/python-tests.yml`, then run:

```bash
COVERAGE_PROCESS_START="$PWD/pyproject.toml" PYTHONPATH="$PWD" coverage run -m pytest research/phase-a-0-baseline/tests/
coverage combine
coverage report
```

The same 60% floor applies locally and in the advisory CI job. Analysis tests
use synthetic on-disk measurements and the real NumPy/SciPy calculations;
scorer-adapter tests use an explicitly synthetic validator process to verify
routing, parsing and provenance. They do not prove marketplace integration,
statistical validity, live provider behavior or experiment outcomes. The four
separate real-validator tests still require the marketplace checkout.

The coverage repair was verified with networking disabled and the developer's
home directory hidden: 43.1% before the new contracts, 61.2% after. No coverage
exclusions, research results, analysis rules or provider behavior changed.
Refs bead `bd_000-projects-js4x`.

Analysis input sufficiency and statistical-claim corrections are tracked
separately in `bd_000-projects-1j6k`; coverage does not settle those findings.

## Analysis input and methodology limits (2026-10-19)

The analyzer now refuses a decision unless both arms contain exactly the
manifest's 60 specimens (20 per stratum), Arm A has all four registered K values,
and every pair has the same baseline score. Missing measurements, duplicate IDs,
invalid JSON, non-finite values and inconsistent score deltas fail with exit 2.
Partial cohorts may be reported descriptively under DESIGN section 6; this
command does not turn those exclusions into a complete-experiment decision.

Each Arm A slot must include `response.json` with a boolean `dry_run: false`.
Each Arm B specimen must include `proposal-0.json`, and every saved proposal
must declare `dry_run: false`. Missing or ambiguous response provenance is
refused. This check catches simulations retained when a later real invocation
resumes a run; the latest summary's flag cannot establish earlier records.

Use a fresh output directory. Existing statistics or decisions are never
replaced, and non-finite calculated statistics are refused before either output
is written. For example, from this research directory:

```bash
python scripts/analyze.py --arm-a results/arm-a/nvidia-llama-70b --arm-b results/arm-b/nvidia-llama-70b --out /tmp/phase-a0-analysis-new
```

The implemented estimators are retained and labeled explicitly:

| Surface                   | Implemented behavior                                        | Unresolved difference from RESULTS-TEMPLATE                 |
| ------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| Normal primary branch     | Paired one-sided t-test after Shapiro on paired differences | Template uses independent samples and normality of each arm |
| Non-normal primary branch | One-sided Wilcoxon signed-rank                              | Historical run selected this branch                         |
| Strata                    | Independent Welch tests within each stratum                 | Does not implement the two-way ANOVA interaction test       |
| K contrasts               | Unadjusted one-sided tests                                  | Does not implement the template's Bonferroni correction     |
| Goodhart                  | Accepted-flag counts only, marked `not_performed`           | Does not implement the five-dimension audit                 |

The strict DR-028 scalar threshold uses exact decimal arithmetic so equality at
1.05 pp does not become DESCOPE through binary rounding. This preserves the
specified strict comparison; it does not select a different estimator. New
outputs identify their methodology as unreconciled and are not authorization
for Phase B or a replacement for a ratified decision.

A read-only audit of the retained historical inputs found different baseline
scores in **all 60 pairs**: Arm A uses cached corpus-manifest scores, while Arm B
re-scores its input. The mean baseline difference is 7.5667 pp. The cause and
impact on DR-036 require provenance review; no corrected scores or reversed
conclusion are inferred here. The new guard refuses to reanalyze those inputs.
Historical raw files, aggregate outputs, RESULTS, DESIGN and decision records
remain unchanged. `bd_000-projects-436s` owns the historical and methodology
reconciliation; `bd_000-projects-1j6k` remains open until that review is settled.
