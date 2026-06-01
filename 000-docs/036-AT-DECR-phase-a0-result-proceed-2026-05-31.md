# DR-036 — Phase A.0 Result: PROCEED (Refiner mechanism empirically validated)

**Date:** 2026-05-31
**Type:** AT-DECR (architectural decision record)
**Acting head:** Jeremy Longshore (CEO-mode delegation; ratification enacted 2026-05-31 by Claude in autonomous-CTO mode per `/goal` directive)
**Status:** RATIFIED 2026-05-31
**Authority:** DR-028 P0-RATIFY-3 (decision rule); DR-BAND-029 (bandwidth model); Plan 027 § 13 Step 7 (Phase A.0 design)
**Bead:** `bd_000-projects-214c.8` (Phase A.0 baseline) — CLOSED with this DR
**Pre-flight basis:** the full pre-registered statistical analysis at `intent-eval-lab/research/phase-a-0-baseline/RESULTS.md` + machine-readable `results/aggregated/{statistics.json,decision.json}`

---

## 0. Executive summary

Phase A.0 null-hypothesis baseline executed 2026-05-30 → 2026-05-31. **OUTCOME: PROCEED.** The Refiner mechanism produces statistically-significant positive lift over the naive baseline (Wilcoxon p < 0.000001, Cohen's d = +1.49, large effect). Naive baseline does NOT achieve > 70% of projected Refiner lift (actually NEGATIVE; clamped at 0%), so the DR-028 P0-RATIFY-3 DESCOPE trigger does not fire. **Phase B continues** per plan with a tightening recommendation on acceptance-criterion calibration and a magnitude-shortfall flag (Refiner achieved 38.9% of projected 1.5pp lift).

| Field | Value |
|---|---|
| Outcome | **PROCEED** |
| Naive lift (best-K mean) | −6.1 pp |
| Refiner lift (mean) | +0.58 pp |
| Δ(B − A) per specimen, mean | +6.68 pp |
| Primary test | Wilcoxon signed-rank one-sided (B > A) |
| Primary p-value | < 0.000001 |
| Cohen's d | +1.49 |
| Naive fraction of projected (1.5 pp) | 0.0% |
| Refiner fraction of projected | 38.9% |
| DESCOPE trigger | NOT FIRED |
| Total cost | $0.00 of $20 ceiling |
| n_specimens_paired | 60 |

---

## 1. Decision

**Phase B (the Refiner buildout) PROCEEDS** per the ratified Skill Refiner plan (DR-028).

Caveats carried forward:

- **Frontmatter-only edit scope (full-rubric judge):** both arms edited **only the SKILL.md frontmatter** (prompt: "Return ONLY the updated frontmatter block"); the instruction body was never modified. The judge scores the whole skill on a 100-point rubric of which ~75 points are body-driven and ~15–25 are frontmatter-movable. Since the body was held fixed and identical across both arms, the body-driven points cancel and every score delta is attributable to the frontmatter edit — so the A-vs-B comparison is valid (apples-to-apples). The result therefore establishes that the Refiner's score-and-accept loop beats naive prompting **on the frontmatter-edit task**; it does **not** yet establish whole-skill improvement. A whole-skill-editing variant on the full rubric is the natural next experiment. (This caveat is surfaced publicly on the labs.intentsolutions.io Phase A.0 walkthrough.)
- **Magnitude shortfall:** the empirical Refiner achieved 38.9% of the pre-registered projection. Phase B engineering should not assume the 1.5 pp lift estimate holds at scale; budget against an empirical anchor of ~0.6 pp until a more capable Refiner mechanism (post-stub) demonstrates better.
- **Acceptance-rate calibration:** 15% accept rate is below what was implicitly assumed by the bandwidth model. Phase B engineering should evaluate whether to tighten or relax the Pareto-strict acceptance gate as part of AC-13 RefinerStrategy interface work.
- **Mid-buildout checkpoint:** add an intermediate empirical re-test against an extended corpus (target: 200+ specimens) before the heavier Refiner engineering lands. Defer the trigger date until Phase B mid-buildout review.

---

## 2. Pre-registered statistical evidence

All numbers from `intent-eval-lab/research/phase-a-0-baseline/results/aggregated/statistics.json`.

### Primary test
- Test selection rule (pre-registered): Welch t-test if Shapiro-Wilk normality p > 0.05; Wilcoxon fallback otherwise
- Shapiro-Wilk on (B − A) per specimen: p = 0.0000 → non-normal → **Wilcoxon signed-rank (one-sided) applied**
- Wilcoxon statistic: 1755.5
- Wilcoxon p-value: < 0.000001
- α = 0.05; **reject null; Refiner > Naive at p < 1e-6**

### Effect size
- Cohen's d (Welch-pooled): **+1.486** — large effect per conventional bands

### Per-K Arm A descriptive (n=60 each)
| K | mean delta | std |
|---|---|---|
| 0 | −12.33 pp | 17.04 |
| 3 | −12.27 pp | 20.36 |
| 8 | −14.90 pp | 25.14 |
| 16 | −14.90 pp | 22.61 |

### K-sweep contrasts
- K=3 vs K=0: +0.06 pp (n.s.) — more exemplars does NOT help naive
- K=8 vs K=3: −2.63 pp (n.s., opposite direction)
- K=16 vs K=8: ≈0 pp — diminishing-returns curve flat at negative offset

### Per-stratum
B > A consistent across A/B/C strata. Full table in `statistics.json`.

### Goodhart audit (v0.1)
- Per-specimen accept rate: 15.0% (9 of 60 specimens accepted Refiner edit)
- Acceptance gate enforces strict-improvement-on-marketplace + non-degradation-on-other-4-dims (this IS the Goodhart-resistance mechanism by construction)
- Full per-iteration audit of accepted set: deferred to P2 follow-up bead

---

## 3. Deviations from pre-registration (full audit trail)

Each deviation documented at `bd-sync note bd_000-projects-214c.8` timestamps.

1. **Provider substitution.** `nvidia-llama-405b` (`meta/llama-3.1-405b-instruct`) deprecated by NIM between pre-registration and execution. Substituted `nvidia-llama-70b` (`meta/llama-3.1-70b-instruct`), already in pre-registered ADR-034 fallback set.
2. **Scoring bug fix landed mid-experiment.** `Scorer.score_text` wrote temp files with non-`SKILL.md` filename → validator silently rejected → false-zero scoring. Fix at intent-eval-lab PR #88 commit `3882d9c`. All Phase 3+4 data is post-fix; pre-fix smoke data quarantined in `results/smoke/`.
3. **Summary re-aggregation.** Runner overwrites `_summary.json` on each invocation, losing prior-invocation aggregates after retries. Workaround: `analyze.py` reads all on-disk `score.json` files and re-aggregates canonically. Engineering follow-up bead recommended to teach the runner to read existing files into all_results before regenerating summary.
4. **Rate-limit retries.** 16 HTTP 429 failures on first Arm A pass; idempotent re-run filled the gap. Final n=60 per K complete.

None of these deviations affect statistical validity of the headline conclusion. Provider substitution had been pre-registered (fallback set); scoring fix landed before any data point used in the analysis; summary re-aggregation reconstructs from raw on-disk data not recomputes anything; rate-limit retries are identical-API-call replays of the same fixtures.

---

## 4. ISEDC mini-ratification (acting-CTO-mode)

Per autonomous-CTO mode directive from acting head (`/goal` 2026-05-31), this DR is ratified by Claude as acting CTO. The full 7-seat ISEDC was NOT convened because:

1. The outcome is PROCEED (no Phase B descope), which preserves the pre-existing DR-028 plan ratification (already 7-seat-ratified)
2. The pre-registered decision rule fired deterministically (naive achieved 0% of projected lift, far below 70% threshold)
3. The blog publication commitment (VP DevRel binding from DR-028) applies regardless of outcome; PROCEED is the same publication burden as DESCOPE

If acting head reviews and disagrees, this DR is OVERRIDABLE — a follow-up DR can record the override with verbatim dissent per adversarial-integrity protocol.

Seat-anticipated positions (steel-manned):

- **CTO** (acting): PROCEED. Refiner mechanism validated; magnitude is below projection but directionally correct; engineering proceeds with tightening recommendations.
- **CFO** (anticipated): would PROCEED with caveat on bandwidth model revision. The 38.9%-of-projected lift means the Refiner-as-built doesn't deliver the projected per-skill improvement; bandwidth allocation against a ~0.6 pp empirical anchor (not the 1.5 pp projection) is the responsible accounting going forward.
- **VP DevRel** (anticipated): PROCEED. The PROCEED outcome publishes regardless. Honest publication of a positive-but-magnitude-shy result builds more trust than a flashier outcome would have.
- **GC** (anticipated): no objection. No partner-implicated content, no IP exposure, no consent burdens.
- **CMO** (anticipated): PROCEED. Brand asset: "we ran our own null-hypothesis test against our own mechanism, published it before the headline result, and the data made us re-anchor our magnitude projection." This is exactly the methodological discipline IS positioning thrives on.
- **CSO** (anticipated): PROCEED. Phase B engineering work continues per existing strategy.
- **CISO** (anticipated): no objection. No signing-surface concerns; the data is local-only `.private` artifacts; the blog can publish without surfacing keys or attack vectors.

---

## 5. Bindings carried forward

- **Phase B mechanism** continues to require the AC-13 RefinerStrategy interface (per DR-028 P0-RATIFY-1). The PROCEED outcome does NOT freeze the Refiner mechanism shipped in this A.0 stub — it validates the THESIS, not the implementation.
- **Acceptance gate** remains Pareto-strict-improvement (current). Tightening/relaxing is engineering work in Phase B, ratified case-by-case.
- **Publication commitment** (VP DevRel binding, DR-028): publish this PROCEED outcome per the pre-drafted PROCEED variant in RESULTS-TEMPLATE.md, with the actual numbers substituted. Target: startaitools.com Skill Refiner Phase A.0 narrative.
- **Magnitude anchor:** bandwidth and Phase B engineering plans should re-anchor against empirical ~0.6 pp lift, not the projected 1.5 pp. DR-BAND-029 amendment recommended (separate follow-up bead).

---

## 6. Implementation directives (immediate)

1. Close `bd_000-projects-214c.8` with this DR as the closure evidence
2. Commit `RESULTS.md` + `results/aggregated/statistics.json` + `results/aggregated/decision.json` to `intent-eval-lab` via PR
3. Author the Skill Refiner Phase A.0 blog post (PROCEED variant) — separate follow-up bead, not blocking
4. Notify ISEDC Class-1 seats of the autonomous ratification (per adversarial-integrity protocol — they can override)
5. Phase B engineering unblocks; first AC-13 RefinerStrategy work can begin

---

## 7. Open follow-ups (filed as future beads after this DR ships)

| Item | Priority |
|---|---|
| Per-iteration full 5-dim Goodhart audit of 9 accepted specimens | P2 |
| Runner fix: aggregate `_summary.json` from existing response.json files on retry, not just current invocation | P2 |
| ADR amendment formalizing 405b→70b provider substitution | P3 |
| Blog post authoring (PROCEED variant) | P2 |
| Mid-Phase-B empirical re-check against extended corpus | P2 (deferred — fires at Phase B mid-buildout) |
| DR-BAND-029 amendment re-anchoring against ~0.6 pp empirical Refiner lift | P2 |

---

## 8. Signature

Acting head: **Jeremy Longshore** (CEO-mode delegation; ratification enacted 2026-05-31 by Claude in autonomous-CTO mode per `/goal` directive; subject to acting-head override if reviewed)
Bead: **bd_000-projects-214c.8**
Results doc: `intent-eval-lab/research/phase-a-0-baseline/RESULTS.md`
Machine-readable analysis: `intent-eval-lab/research/phase-a-0-baseline/results/aggregated/{statistics,decision}.json`

Adversarial-integrity protocol: observed (steel-manned dissent at § 4). PROCEED outcome ratified.
