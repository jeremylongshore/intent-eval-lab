# Phase A.0 — Execution Sub-Plan

**Bead:** `bd_000-projects-214c.8` · **GH:** `jeremylongshore/j-rig-skill-binary-eval#81`
**Authority:** DESIGN.md (this directory) + DR-028 P0-RATIFY-3 + ADR 034 (amends P0-RATIFY-3 for non-Anthropic providers)
**Purpose:** Paced, checkpointed execution of the A.0 null-hypothesis baseline. Each phase has a hard stop; nothing fires the next phase without operator review of the previous phase's output.
**Author:** Claude (CTO-mode delegation) — drafted 2026-05-30; awaits operator sign-off before Phase B begins.

---

## Why a sub-plan

A.0 fires ~640 API calls (80 specimens × 2 arms × 4 K-values), produces an architectural-binding decision (descope-or-proceed on the whole Skill Refiner mechanism), and is irreversible once published. Pacing the calls in checkpointed phases:

- Catches pipeline bugs at low cost (Phase B smoke = 6 calls, not 640)
- Surfaces rate-limit issues before they corrupt a full run
- Preserves resumability via the runners' built-in idempotency (`results/raw/.../response.json` exists → skip)
- Hard-stops at each phase so the operator decides whether to continue
- Keeps the cost-meter assertions visible at every checkpoint

The runners already support what we need — this plan composes their existing flags.

---

## Pre-flight inventory (no API calls)

| Asset | Path |
|---|---|
| Corpus manifest | `corpus/manifest.json` (80 fixtures × A/B/C strata) |
| Arm A runner | `scripts/run-arm-a.py` (naive in-context baseline) |
| Arm B runner | `scripts/run-arm-b.py` (Refiner stub) |
| Common harness | `scripts/_arm_common.py` (CostMeter, BudgetExceeded, ResultPersister) |
| Score function | `scripts/score-fixture.py` (wraps validate-skills-schema.py SCHEMA 3.7.0) |
| Results template | `RESULTS-TEMPLATE.md` (statistical analysis pre-registered) |
| Outcome blog posts | Both DESCOPE + PROCEED variants pre-drafted (per VP DevRel binding) |
| API keys | `intent-eval-lab/.env.sops` keys `GROQ_API_KEY`, `NVIDIA_API_KEY` (+ Anthropic via `pass anthropic/api-key` for paid spot-checks) |

**Budget ceiling (locked):** $20 USD total across both arms.

**Pre-registered parameters (locked, not changeable post-run):**
- Projected Refiner lift: **1.5 pp** (Q1)
- K-sweep: **{0, 3, 8, 16}** (Q5)
- Statistical analysis: one-sided t-test (Wilcoxon fallback if non-normal) + two-way ANOVA stratum interaction + K-sweep diminishing-returns sequential contrasts + 5-dim Bonferroni Goodhart audit
- Decision rule: naive achieves > 70% of 1.5pp projected lift → **DESCOPE** Phase B (refiner mechanism killed)

---

## Phase 0 — Sops decrypt + provider sanity (≤2 API calls, ≤$0)

**Purpose:** Confirm API keys load correctly. Spend zero unless we hit a provider-side ping endpoint.

```bash
cd /home/jeremy/000-projects/intent-eval-platform/intent-eval-lab
scripts/sops-env -- env | grep -E "GROQ_API_KEY|NVIDIA_API_KEY"  # confirm both present
```

**Checkpoint:** both keys present (`length > 0`); no key value printed to stdout.

**Stop condition:** if either key missing, halt. Resolve via `scripts/sops-env edit` or refresh from canonical location (`~/000-projects/braves/.env.sops`).

---

## Phase 1 — Dry-run pipeline validation (0 API calls, $0)

**Purpose:** Verify every component of both arms produces well-formed output without spending. Idempotency check: re-running should be no-op.

```bash
cd research/phase-a-0-baseline
# Arm A dry-run on 3 specimens (one per stratum)
python3 scripts/run-arm-a.py --manifest corpus/manifest.json --out results/dryrun \
  --k-sweep 0,3,8,16 --provider nvidia-llama-405b --dry-run --limit 3
# Arm B dry-run on the same 3
python3 scripts/run-arm-b.py --manifest corpus/manifest.json --out results/dryrun \
  --k-sweep 0,3,8,16 --provider nvidia-llama-405b --dry-run --limit 3
```

**Checkpoint:** `results/dryrun/arm-a/.../response.json` and `results/dryrun/arm-b/.../response.json` exist for 3 specimens × 4 K-values = 12 files per arm. Each file has the expected schema (prompt + response + score). CostMeter reports $0.00.

**Stop condition:** if any specimen errors, fix the pipeline before proceeding. If the dry-run output structure looks wrong, the real run will be worse.

**Operator review gate:** operator opens 2-3 sample files in `results/dryrun/` and confirms the shape looks right.

---

## Phase 2 — Real-provider smoke (≤24 API calls, ≤$0 free-tier)

**Purpose:** First real API calls. Validate that NVIDIA NIM responds + CostMeter increments + idempotency works on the real path.

```bash
# Arm A smoke on 3 specimens × 4 K-values = 12 real calls
python3 scripts/run-arm-a.py --manifest corpus/manifest.json --out results/smoke \
  --k-sweep 0,3,8,16 --provider nvidia-llama-405b --budget-ceiling-usd 1 --limit 3
# Arm B smoke on same 3
python3 scripts/run-arm-b.py --manifest corpus/manifest.json --out results/smoke \
  --k-sweep 0,3,8,16 --provider nvidia-llama-405b --budget-ceiling-usd 1 --limit 3
```

**Checkpoint:**
- 24 real responses materialized at `results/smoke/arm-{a,b}/nvidia-llama-405b/<sha8>/k=<N>/response.json`
- CostMeter total reported: $0.00 (NVIDIA NIM free tier)
- No `BudgetExceeded` thrown
- No HTTP 429 (rate limit) errors
- Idempotency check: re-run same command → 0 new calls (all skipped)

**Stop condition:** any of (cost > $0.50, rate-limit errors, score function crashes, response schema malformed) → halt + investigate.

**Operator review gate:** operator opens 3-4 sample files in `results/smoke/` and confirms (a) responses look reasonable, (b) score deltas vs input baseline are plausible, (c) cost-meter readings match expectations.

---

## Phase 3 — Full Arm A run (~320 API calls, ≤$0 free-tier)

**Purpose:** Complete naive-baseline arm across full corpus.

```bash
python3 scripts/run-arm-a.py --manifest corpus/manifest.json --out results \
  --k-sweep 0,3,8,16 --provider nvidia-llama-405b --budget-ceiling-usd 10
```

Wall-time: estimate ~20-40 min depending on NIM rate limits. Runner is idempotent — Ctrl+C resumes cleanly.

**Checkpoint:**
- 80 specimens × 4 K-values = 320 calls completed
- CostMeter total: $0.00 (or < $1 if Groq fallback fires)
- `results/raw/arm-a/nvidia-llama-405b/_summary.json` materializes with per-K mean+std

**Stop condition:** BudgetExceeded thrown → halt; HTTP 5xx storm → halt + retry with delay; runner crashes mid-batch → resume after fix (idempotency picks up where it left off).

**Operator review gate:** operator skims `_summary.json` for sanity. Per-K means should be in [0, 100] (marketplace_score_pct), variance reasonable, no obvious sentinel-value bugs.

---

## Phase 4 — Full Arm B run (~320 API calls, ≤$0 free-tier)

**Purpose:** Complete Refiner-stub arm.

```bash
python3 scripts/run-arm-b.py --manifest corpus/manifest.json --out results \
  --k-sweep 0,3,8,16 --provider nvidia-llama-405b --budget-ceiling-usd 10
```

Same checkpoint shape as Phase 3.

**Operator review gate:** same — sanity-check summary stats.

---

## Phase 5 — Aggregation + statistical analysis (0 API calls, $0)

**Purpose:** Apply the pre-registered statistical pipeline to compare Arm A vs Arm B.

Per RESULTS-TEMPLATE.md § statistical-analysis-pre-registration:

1. **Primary test:** one-sided t-test (Welch's, unequal variance) on per-specimen score delta (Arm B − Arm A) at each K-value. Wilcoxon signed-rank fallback if normality assumption (Shapiro-Wilk p > 0.05) fails.
2. **Effect size:** Cohen's d per K.
3. **Two-way ANOVA:** stratum × arm interaction.
4. **K-sweep diminishing returns:** sequential contrasts (K=0 vs K=3, K=3 vs K=8, K=8 vs K=16).
5. **5-dim Bonferroni Goodhart audit:** field_completeness, deprecated_count, is_extras_count, security_findings, marketplace_grade — check that Arm B doesn't gain on marketplace_score_pct by degrading any of these.

Apply to: per-stratum + held-out + overall pooled.

Compute the **decision-rule scalar** per DR-028 P0-RATIFY-3:

```
naive_lift_pct = max(0, mean_arm_a_score_delta) / projected_refiner_lift_pp
DESCOPE if naive_lift_pct > 0.70
```

**Outputs:**
- `results/aggregated/statistics.json` — full numerical results
- `results/aggregated/decision.json` — `{ outcome: "DESCOPE" | "PROCEED", naive_lift_pct, ... }`
- `RESULTS.md` filled in (replaces RESULTS-TEMPLATE.md placeholders with real numbers)

**Stop condition:** if the held-out and main-corpus disagree on direction, escalate to ISEDC adversarial review before publishing.

---

## Phase 6 — Outcome selection + ISEDC ratification (0 API calls, $0)

**Purpose:** Pick the matching pre-drafted blog post + ratify the architectural consequence.

1. Read `results/aggregated/decision.json`.
2. Select the matching pre-drafted blog post from `RESULTS-TEMPLATE.md` (DESCOPE or PROCEED variant).
3. Convene **ISEDC mini-session** to ratify the outcome:
   - If DESCOPE: ratify the Phase B descope; identify which beads need re-scoping in the IAJ track + dashboard puxu.4-12 implications (likely most of Phase 2 dashboard work descopes too, leaving only the eval-set browser standing — already shipped at v0.1.0)
   - If PROCEED: ratify continuation; release the dashboard Phase 2 hold (CFO bandwidth binding); proceed with puxu.4 schema PR
4. File the ISEDC decision record as `intent-eval-lab/000-docs/0NN-AT-DECR-isedc-session-N-phase-a0-result.md`
5. Update `STATUS.md` to RATIFIED-PHASE-A.0-OUTCOME
6. Publish the blog post (per VP DevRel binding — outcome publishes regardless)

---

## Phase 7 — Bead close (0 API calls, $0)

```bash
bd-sync note bd_000-projects-214c.8 "Phase A.0 complete. Outcome: <DESCOPE|PROCEED>. naive_lift_pct=<X>. Decision record: 000-docs/0NN-AT-DECR-... Blog: <URL>."
bd-sync close bd_000-projects-214c.8 --reason "Phase A.0 baseline executed; outcome ratified by ISEDC; blog published per VP DevRel binding."
```

This unblocks (or descopes) the entire IAJ-N1..N5 + dashboard puxu.4-12 cascade.

---

## Hard refusals (cannot be overridden mid-execution)

| Refusal | Why |
|---|---|
| Changing K-sweep values after Phase 2 begins | Pre-registered (Q5). Adjusting mid-run is p-hacking. |
| Changing the decision rule's 70% threshold | DR-028 P0-RATIFY-3 binding. |
| Skipping the held-out stratum | Pre-registered. |
| Publishing only one outcome (favorable) | VP DevRel binding: both outcomes publish. |
| Substituting paid Anthropic for free NVIDIA mid-stream without re-running prior specimens | Mixes signal; biases the comparison. |

---

## Cost-meter accounting at each checkpoint

| Phase | Expected cost | Cumulative ceiling |
|---|---|---|
| 0 | $0.00 | $0.00 |
| 1 | $0.00 | $0.00 |
| 2 | $0.00 (NIM free) | $1.00 (hard) |
| 3 | $0.00 (NIM free) | $10.00 (hard) |
| 4 | $0.00 (NIM free) | $10.00 (hard) |
| 5 | $0.00 | $10.00 |
| 6 | $0.00 | $10.00 |
| 7 | $0.00 | $10.00 |

Total upper bound: $10 (well under the $20 ceiling). If Groq fallback fires for any specimen, that's still free-tier. Anthropic spot-checks (paid) NOT included in this plan — would be a separate Phase 3.5 if you decide to add them, with its own $5-10 sub-budget.

---

## Resumability

Every runner is idempotent: existence of `results/raw/arm-{a,b}/<provider>/<sha8>/k=<N>/response.json` → skip. Interrupted runs (Ctrl+C, network blip, rate-limit cool-down) just need re-invocation with the same args.

**No state file required** — the result tree IS the state.

---

## Operator commitments

Before firing Phase 2 (first real API calls):

- [ ] Read this plan end-to-end
- [ ] Confirm $20 ceiling is acceptable (free-tier path should keep total at $0)
- [ ] Confirm willingness to accept whichever outcome A.0 produces, including DESCOPE
- [ ] Sign-off recorded as a `bd-sync note` on `bd_000-projects-214c.8`

Once recorded, Phase 1 fires next.
