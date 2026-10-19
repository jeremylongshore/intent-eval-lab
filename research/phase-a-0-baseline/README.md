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
