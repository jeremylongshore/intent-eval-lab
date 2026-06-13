# gbrain Citation-Integrity Eval

**What:** a non-derivative Evidence Bench measurement of whether the `gbrain` memory system's synthesized answers cite sources that actually support their claims — citation / provenance integrity, a dimension the upstream retrieval-eval suite does not measure.

**Why:** Move 2 of the snoopy-fluttering-comet plan, re-scoped 2026-06-01 after the feasibility finding that gbrain is a memory system (not an LLM). Provenance is the lab's differentiated measurement lane.

**Where:** this directory. Epic `bd_000-projects-704w`.

## Status

| Phase       | Bead      | Deliverable                                                                   | State               |
| ----------- | --------- | ----------------------------------------------------------------------------- | ------------------- |
| Design      | `704w.1`  | `DESIGN.md` — pre-registered corpus / questions / ground-truth / scoring rule | DONE (this session) |
| Feasibility | `704w.3`  | `FEASIBILITY.md` — install + offline smoke + confirmed embedding override     | DONE (this session) |
| Harness     | `704w.5`  | `scripts/{capture,run,score}.py` + corpus manifest                            | TBD (run phase)     |
| Run         | `704w.7`  | `RESULTS.md` + per-question verdicts on free NIM                              | TBD (run phase)     |
| Sign        | `704w.9`  | production Rekor blob signature (predicate reserved)                          | TBD                 |
| Publish     | `704w.11` | Evidence Bench scorecard row (dimension stated loudly)                        | TBD                 |

## Entry points

- `DESIGN.md` — pre-registered experimental design (read first).
- `FEASIBILITY.md` — install record + confirmed free-tier embedding wiring + offline smoke.
- `corpus/` — captured pages + `manifest.json` + `ground-truth.json` (run phase).
- `results/` — outputs (gitignored: `results/raw/`; committed: `results/aggregated/`).

## Discipline

Mirrors the Phase A.0 null-hypothesis baseline (`../phase-a-0-baseline/`): pre-register
corpus + question set + ground-truth + scoring rule BEFORE any API call; single pinned
system version; $0 target via free OpenAI-compatible NIM dev tier; honest scope.
