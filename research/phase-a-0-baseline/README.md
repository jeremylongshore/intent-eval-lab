# Phase A.0 — Null-Hypothesis Baseline

**What:** empirical test of whether naive-Opus-in-context beats the proposed Refiner mechanism on `/validate-skillmd`, per DR-028 P0-RATIFY-3.

**Why:** gates Phase A. If H₀ holds (naive ≥ 70% of projected Refiner lift), Phase B mechanism descopes.

**Where:** this directory. Bead `bd_000-projects-214c.8`. GH issue `jeremylongshore/j-rig-skill-binary-eval#81`.

## Status

| Session | Date | Deliverable |
|---|---|---|
| 1 | 2026-05-28 | DESIGN.md + directory scaffold (this session) |
| 2 | TBD | Corpus inventory + pre-registration sha |
| 3 | TBD | Arm A execution |
| 4 | TBD | Arm B execution + RESULTS.md + BLOG-DRAFT.md |

## Entry points

- `DESIGN.md` — experimental design (read first)
- `corpus/inventory.md` — corpus + sampling (Session 2)
- `arms/{naive-opus,proposed-refiner}/` — arm-specific runners (Session 3+)
- `judge/validate-skillmd-judge.md` — scorer spec (Session 2)
- `results/` — outputs (gitignored: `results/raw/`; committed: `results/aggregated/`)

## CTO gates before Session 2 (per DESIGN.md § 9)

5 open items must resolve.
