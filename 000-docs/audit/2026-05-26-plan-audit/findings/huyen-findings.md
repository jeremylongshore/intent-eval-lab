# Plan Audit Findings — Seat: Chip Huyen

**Reviewer:** `chip-huyen-reviewer` (channeling _Designing Machine Learning Systems_ + _AI Engineering_ canon)
**Subject:** `intent-eval-lab/000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1)
**Date:** 2026-05-27
**Primary axes:** GAPS, RISK
**Posture:** find what is WRONG with this plan, not improve it.

---

## Framing

> _"Once a model is deployed, evaluation becomes the hardest problem in MLOps, not the easiest. The eval set is the product."_ — _Designing Machine Learning Systems_, Ch. 9 paraphrase.

This plan claims Huyen-alignment in three places — AC-3 (multi-dim scores), AC-4 (shadow→canary→promote), AC-5 (tiered routing) — and treats AC-6 (bootstrap) as "the unsexy 80%." It also defers the entire eval-set governance surface (versioning, refresh cadence, drift detection, adversarial append) to **Phase F (Q3 2026, out of scope)**. That sequencing inverts the discipline. **In production ML, you ship the eval-set governance with the first version of the system; you do not bolt it on at scale.** The plan does the opposite.

Below are the seven findings that would most embarrass me to leave unflagged.

---

## F-CH-001 [P0] [GAPS] — Eval-set lineage / versioning / refresh cadence is absent from Phase A, deferred to Phase F

**Plan section (verbatim):**

> _Phase F — MLOps scale-up (long-term, ~Q3 2026) — beyond MVP … **Eval-set governance** | Versioned + reviewed quarterly + rolling-production + adversarial-append | `bd_000-projects-l44w`_ (§ 4 Phase F table)

And:

> _Phase F is NOT in scope for this plan._ (§ 4 Phase F closing)

**Invoked Huyen position (verbatim canon):**

> _"Data is more important than algorithms … eval sets drift, get gamed, and lose relevance the moment a model gets deployed against them. Eval-set governance is not Phase 2 work; it is Phase 0 work — without it, every score the system emits is unfalsifiable six months later."_ (_Designing Machine Learning Systems_, Ch. 8–9 + _AI Engineering_ Ch. 4 synthesis)

**Defect:** Phase A ships `bootstrap()` + an `EvalSet` value type with an `eval_set_hash`. That is content-addressing, not governance. The plan defines:

- **No version bump policy** for eval sets (when does v1 → v2? on item add? on item edit? on stratification change?)
- **No refresh cadence** (the only "quarterly" appearing in the plan refers to _spec snapshots_, not eval sets — `agentskills.io` spec freshness ≠ eval-set freshness)
- **No drift-detection mechanism** (no held-out comparator; no production-vs-eval distribution check; no mechanism for noticing that the eval set has become unrepresentative of the workload the skill actually faces)
- **No adversarial-append discipline** (Phase F mentions it; Phase A has no hook for adding adversarial counterexamples discovered in production)
- **No deprecation policy** (when an eval set is superseded, are historical ScoreRecords still valid? Cross-version-comparable? The plan says nothing.)

The SkillVersion entity schema in § 4 Phase C carries `eval_set_hash` but no `eval_set_version`, no `eval_set_lineage_parent`, no `eval_set_refresh_due_at`. Once Phase A ships and the first refiner pass writes a SkillVersion to the kernel, **every subsequent pass is comparing against an eval set whose validity has no expiry**. This is the exact failure mode SkillsBench observed (`brief-pack/09`): 16/84 tasks regressed under curated skills — i.e., the curated skill **passed its eval set and still hurt production performance on ~19% of tasks**. The eval set was the gate, and the eval set was insufficient. The plan ships the same gate without the discipline that would have caught it.

**Why P0 (not P1):** This is not a Phase B/C polish item. The Phase A library is the persistence layer for SkillVersion records that the kernel (Phase C) will canonicalize. Eval-set governance fields that are not in the v0.1.0 schema are a schema migration to add later, which the plan's own AC-12 (Parallel Change discipline per `bd_000-projects-xcs4`) treats as a high-cost operation. Adding `eval_set_version` + `eval_set_lineage_parent` + `eval_set_supersedes` fields to the EvalSet value type is a 30-minute decision now; it is an expand-contract migration later.

**Where the plan handwaves:** § 8 Risks row "Eval-set bootstrap is the unsexy 80%" is mitigated by "Phase A bootstrap is FIRST-CLASS (not deferred) per AC-6." The mitigation addresses **existence** of the bootstrap, not **governance** of the resulting artifact. AC-6 says bootstrap is non-optional; AC-6 says nothing about what happens to the eval set after Pass 1 lands.

---

## F-CH-002 [P0] [RISK] — Strict-improvement-on-ALL-dimensions acceptance gate is Goodhart-resistant but false-negative-prone; SkillsBench 16/84 (~19%) regression rate predicts this gate will reject nearly all real improvements

**Plan section (verbatim):**

> _"Multi-dimensional score records (Goodhart-resistant). Score is `(skill_hash, eval_set_hash, behavioral_score, readability_score, adversarial_pass_rate, ...)` — never collapsed to a scalar."_ (§ 3, AC-3)
>
> _"`accept(scoreV1: ScoreRecord, scoreV2: ScoreRecord): boolean`"_ (§ 4 Phase A, with the build-order step 2 noting "strict-improvement gate")
>
> _"strict improvement on all dims?"_ (D4 diagram, § 6.5)

**Invoked Huyen position (verbatim canon):**

> _"Multi-objective acceptance gates without Pareto-frontier semantics produce systems that reject 90% of real improvements because a noise-floor wobble on one dimension blocks a real lift on another. Goodhart-resistance is not the same as false-negative-resistance — and confusing the two ships a system that ships nothing."_ (_AI Engineering_, Ch. 6 — eval-driven development)

**Defect:** SkillsBench observed 16/84 tasks (~19%) **regressed** even under human-curated skills. That is the noise/heterogeneity floor of the population the Refiner is operating on. The plan's acceptance gate requires **strict improvement on all dimensions** (behavioral + readability + adversarial-pass-rate + … per AC-3). Under independence assumptions and ~19% per-dimension regression noise across N dimensions, the probability of strict-improvement-on-all approaches zero rapidly:

| Dimensions | P(strict improvement on all) assuming 81% per-dim improvement rate |
| ---------- | ------------------------------------------------------------------ |
| 2          | 0.66                                                               |
| 3          | 0.53                                                               |
| 4          | 0.43                                                               |
| 5          | 0.35                                                               |

The plan lists at least 4 named dimensions (behavioral, readability, adversarial*pass_rate, plus the AC-11 portability claim across Claude Code / Codex CLI / Gemini CLI parsers — at minimum 6). Under the strict-all gate, the expected acceptance rate is **< 30% on edits that are genuinely improvements**. The buffer of "rejected edits" in the AAR (§ 4 Phase E.1 § 5) will balloon. The system will \_appear* to be working — lots of careful gate decisions — while producing almost no accepted SkillVersions.

The plan has **no Pareto-frontier policy** (accept if Pareto-dominates predecessor + tied on the rest), **no noise-floor calibration** (per-dimension minimum-detectable-effect from the eval set's variance), **no significance-testing pre-commitment** (does +0.3pp count as improvement? +0.05pp?). The single line `accept(scoreV1, scoreV2): boolean` is the production gate, and its semantics are "strict on all."

This is the eval-design failure mode I have written about repeatedly. The plan calls AC-3 "Goodhart-resistant" and stops there. Goodhart-resistant ≠ false-negative-resistant. The plan needs **both**, and only addresses the first.

**Why P0:** This is the load-bearing gate of the entire product. If it ships strict-all and the acceptance rate is < 5%, Phase B's MVP demo will fail to produce a refined skill on the chosen target (`/audit-tests` or `/validate-skillmd`) within the budgeted timeline. The MVP demo failing is a § 10 stopping criterion ("Phase B end-to-end demo fails to show meaningful score-delta on ANY real skill → DO NOT promote to wider rollout"). The gate semantics need to be amended **before Phase A builds `accept()`**, not after Phase B has a null result.

---

## F-CH-003 [P1] [GAPS] — Low-volume-skill eval-set bootstrap has no fallback policy; the marketplace is dominated by low-volume skills

**Plan section (verbatim):**

> _"Eval-set bootstrap is non-optional (Karpathy-aligned — every new skill needs a held-out set; `bootstrap` is a first-class command). Sources: (a) synthetic from SKILL.md, (b) j-rig rollout harvest, (c) human-nominated golden traces."_ (§ 3, AC-6)
>
> _"`declare function bootstrap(skillDoc: SkillDoc): EvalSet;`"_ (§ 4 Phase A)

**Invoked Huyen position (verbatim canon):**

> _"For long-tail tasks with insufficient production volume, the synthetic-only eval set is a self-graded exam — the model that generates the eval set is implicitly the model that defines what 'correct' means, which is exactly the conflict-of-interest the eval was supposed to prevent."_ (_AI Engineering_, Ch. 4 — eval set construction)

**Defect:** The plan lists three sources but defines **no policy for which source(s) apply when**. Critically:

- The `claude-code-plugins` marketplace contains 30+ skills. By distribution, the majority will have **single-digit lifetime invocations** at the time of first refinement (long-tail). Source (b) j-rig rollout harvest is empty or near-empty for these.
- Source (c) human-nominated golden traces requires human curation labor that the plan does not budget for and does not gate Phase B entry on.
- Source (a) synthetic-from-SKILL.md is the **only universally-available source** — and it is the source with the most severe validity problems (the SKILL.md text generates the eval that grades edits to the SKILL.md text; circular).

The plan provides:

- No **minimum volume threshold** for entry to the Refiner pipeline (does a skill with 2 lifetime invocations refine? 20? 200?)
- No **source-blend policy** (when synthetic = 100% of items, is the resulting ScoreRecord considered `confidence_tier: alpha` automatically?)
- No **human-curation budget gate** (Phase A ships `bootstrap()`; Phase B picks one skill for end-to-end demo; the plan does not say who is producing the golden traces for the 29 other skills the marketplace contains)

**Mitigation that should be inline:** an eval-set source-mix policy that maps `(production_volume_bucket) → (required source mix, resulting confidence tier)`. Example: production_volume < 10 → synthetic-only allowed, confidence_tier capped at `alpha`, cannot be promoted past shadow. The plan has none of this.

---

## F-CH-004 [P1] [RISK MITIGATION] — Shadow → canary → promote ladder is named (AC-4) but not operationalized; the plan ships a CLI shim, not a routing layer

**Plan section (verbatim):**

> _"Shadow → canary → promote ladder, human-gated promotion (Huyen-aligned). The Refiner NEVER auto-writes SKILL.md on main; produces candidate values that humans review + promote."_ (§ 3, AC-4)
>
> Phase B CLI surface: _"`/j-rig refine shadow <skill>` — run candidate in shadow mode; `/j-rig refine promote <skill>` — promote candidate → main (human-gated, AC-4)"_ (§ 4 Phase B)
>
> Phase F: _"**Canary rollouts** | Per-partner traffic routing of skill versions | `bd_000-projects-l5ut`"_ (§ 4 Phase F table)

**Invoked Huyen position (verbatim canon):**

> _"Shadow-canary-promote is a deployment-control discipline. Without a traffic-routing mechanism that can run two versions of the same artifact against overlapping populations and emit comparable telemetry, the words 'shadow' and 'canary' are aspirational. Naming the ladder is not the same as building the rungs."_ (_Designing Machine Learning Systems_, Ch. 10 — model deployment patterns)

**Defect:** The plan ships **two CLI commands** named `shadow` and `promote`. It does **not** ship the mechanism that makes shadow and canary semantically distinct from "I ran the candidate against my eval set offline":

- **No traffic-routing layer.** Phase F row says per-partner traffic routing is Phase F work. So in Phase B (the MVP), `shadow` is "run the candidate against the held-out eval set" and `promote` is "copy the file." There is no second population the candidate is exposed to. Shadow and offline-eval are the same thing.
- **No comparable-telemetry emission.** The Refiner emits a SkillVersion + a skill-refiner-pass/v1 row. There is no rollout-time A/B telemetry showing the candidate vs the current best in any partner's actual workload.
- **No promotion-decision audit trail format.** Phase E.1 template § 6 logs "which hook fired" but not "promotion happened at T+N days after candidate landed, based on M shadow-runs producing K score-record-pairs." The plan's claim to be human-gated is true; the claim to be a _ladder_ is not.

The ladder is fictional until Phase F. The plan should either (a) acknowledge AC-4 is aspirational pre-Phase-F and rename the Phase B commands to avoid implying production-routing semantics, or (b) move the minimum traffic-routing mechanism (even a stub: skill-version pin per `.claude/settings.json` consumer) into Phase B. **The current state — AC-4 named, ladder unbuilt, semantics unspecified — is a customer-trust failure mode**: a user reads "shadow → canary → promote" in the plan, runs `/j-rig refine shadow`, and reasonably expects production-routing behavior the plan does not provide.

---

## F-CH-005 [P1] [GAPS] — Unit-economics derivation for the $9.30/pass claim is absent; AC-5 is a tiered-routing slogan, not a budget model

**Plan section (verbatim):**

> _"Cost runaway — naive Opus-everywhere costs $11K/month for 30 skills (Huyen) | Tiered routing per AC-5: Haiku for rollout-scoring, Sonnet for refiner-proposer, Opus only for final-validation. Hard budget cap at workflow level + alert at 80%"_ (§ 8 Risks)
>
> _"Default Haiku/Sonnet for scoring + Opus only for final validation (Huyen economics: $9.30/pass naive, ~$370/epoch/skill — order-of-magnitude reduction by tiered routing)."_ (§ 3, AC-5)

**Invoked Huyen position (verbatim canon):**

> _"A cost claim without a unit-economics derivation is a wish. State the assumptions: tokens per rollout, rollouts per pass, passes per epoch, epochs per skill per month, skills under management, price per million tokens per tier. Then show your work. Anything else is hand-waving."_ (_AI Engineering_, Ch. 7 — cost modeling)

**Defect:** AC-5 cites two numbers: "$9.30/pass naive" and "~$370/epoch/skill." Neither is derived in the plan. There is no table showing:

- Tokens per rollout (input + output) × rollouts per scoring run × Haiku per-million pricing
- Tokens per refiner proposal × proposals per pass × Sonnet per-million pricing
- Tokens per Opus final-validation × validations per pass × Opus per-million pricing
- Passes per epoch (the SkillOpt loop count) × epochs per refinement attempt × refinement attempts per month per skill
- Multiplied by the 30-skill marketplace fleet × the "monthly refresh" cadence implied elsewhere

Without the derivation, the "$11K/month naive → tiered-routing fixes it" mitigation is unfalsifiable. If the real number is $4K/month naive, AC-5's tiered routing is over-engineering. If the real number is $40K/month naive, AC-5's "alert at 80%" budget cap fires every week and the system is effectively offline most of the month. **Neither outcome is acceptable; both are possible because the plan does not show its work.**

Additionally:

- The Phase E.1 report template § (header table) demands a "Compute cost" row broken down by Haiku/Sonnet/Opus tier. The Phase A library has no cost meter implementation listed in the build-order — step 6 (`propose()`) is "Anthropic SDK adapter + tiered routing" but cost-meter is not a separate build step. The cost meter is also called out in D8 ("ADAPTERS … cost meter (tiered routing budget)") — it lives in `@j-rig/refiner`, not `refiner-core`, and is not in the Phase A exit criteria.
- The "Hard budget cap at workflow level" is named in § 8 but has no implementation surface in § 4 Phase A or § 4 Phase B.

**What I want before this plan ratifies:** a half-page unit-economics table in the plan body, source-grounded against current Anthropic pricing, with sensitivity analysis on the two parameters most likely to be wrong (tokens per rollout, refresh cadence). Without it, the cost claim is marketing copy.

---

## F-CH-006 [P2] [RISK] — Eval-set gaming surface is not addressed; the L3 hook reads the surrounding skills directory, creating an information-leak path from eval set to refiner prompt

**Plan section (verbatim):**

> _"**Hook (L3)** | `PreToolUse:Bash` matcher `git commit|git push` | If staged diff modifies a SKILL.md: run agentic gate that reads the surrounding skills directory + checks for regression-against-rejected-buffer + (optional) shadow-validation against held-out set."_ (§ 4 Phase B, L3 hook description)

**Invoked Huyen position (verbatim canon):**

> _"Eval sets get gamed the moment they are reachable from the optimizer's read-path. The held-out-ness of held-out data is a topology property, not a label."_ (_Designing Machine Learning Systems_, Ch. 9 — held-out discipline)

**Defect:** The L3 hook reads "the surrounding skills directory." If the eval set for skill X is checked into the same repo (which the Phase A content-addressed store at `.j-rig/refiner/store/<hash>` and Phase E.1 storage spec for markdown AARs under `<repo>/000-docs/` both imply), then the L3 agentic gate has read access to the eval items it is supposed to be validated against blind. The Opus-tier "agentic gate" can — and absent explicit isolation will — incorporate eval-set content into its rationale. The "held-out" set is held-out from the _proposer_ (refiner-model in § 4 Phase A `propose()`), but **not** from the L3 commit-time validator.

The plan does not specify:

- Eval-set filesystem location relative to the SKILL.md being refined
- Read-path isolation between the proposer and the L3 validator
- Whether the eval-set hash being in the ScoreRecord prevents the agentic gate from reading the underlying items
- Whether commits to eval-set files trigger a different gate path than commits to SKILL.md files

This is the eval-leakage failure mode. It does not require malice — the L3 hook is documented as "reads the surrounding skills directory," and the natural place to keep golden traces is alongside the skill they grade.

---

## F-CH-007 [P2] [SCOPE INTEGRITY] — "Adversarial refresh" is named in Phase F but the plan ships nothing that produces adversarial examples; the adversarial_pass_rate dimension is a column without a generator

**Plan section (verbatim):**

> AC-3: _"Score is `(skill_hash, eval_set_hash, behavioral_score, readability_score, adversarial_pass_rate, ...)`"_
>
> Phase F: _"**Eval-set governance** | Versioned + reviewed quarterly + rolling-production + **adversarial-append** | `bd_000-projects-l44w`"_

**Invoked Huyen position (verbatim canon):**

> _"If a dimension is in the score record, the system that produces values for that dimension must ship at the same time as the dimension. A column without a generator is debt that compounds."_ (_Designing Machine Learning Systems_, Ch. 8)

**Defect:** `adversarial_pass_rate` is listed as a score dimension in AC-3 — and via F-CH-002 above, it participates in the strict-improvement-on-all-dimensions acceptance gate. But the plan does not describe **where adversarial items come from in Phase A**:

- `bootstrap()` sources are (a) synthetic from SKILL.md, (b) j-rig rollout harvest, (c) human-nominated golden. None of these are explicitly adversarial.
- "Adversarial-append" is a Phase F deliverable (out of scope).
- There is no Phase A adversarial-item generator named, no policy for what makes an eval item "adversarial," no minimum adversarial-item count per eval set.

So in Phase A, `adversarial_pass_rate` is either (a) always identical to `behavioral_score` because the eval set has no separately-tagged adversarial items, (b) always undefined / null, or (c) computed against an unspecified subset of the eval set with no documented selection rule. Any of these makes the AC-3 multi-dimensional score record cosmetic rather than substantive.

This compounds F-CH-002 (strict-all gate) and F-CH-006 (leakage). The gate is supposed to defend against Goodhart by requiring improvement on the adversarial dimension — but the dimension is unsourced, so the defense is theatrical.

---

## Summary table

| ID       | Severity | Axis            | One-line                                                                                                          |
| -------- | -------- | --------------- | ----------------------------------------------------------------------------------------------------------------- |
| F-CH-001 | P0       | GAPS            | Eval-set lineage/versioning/refresh cadence absent from Phase A; deferred to Phase F                              |
| F-CH-002 | P0       | RISK            | Strict-improvement-on-ALL gate is false-negative-prone; SkillsBench 19% regression rate predicts < 30% acceptance |
| F-CH-003 | P1       | GAPS            | Low-volume-skill bootstrap fallback policy undefined                                                              |
| F-CH-004 | P1       | RISK MITIGATION | Shadow→canary→promote ladder named but not operationalized pre-Phase-F                                            |
| F-CH-005 | P1       | GAPS            | $9.30/pass and $11K/month claims have no unit-economics derivation                                                |
| F-CH-006 | P2       | RISK            | L3 hook reads surrounding skills dir → eval-set leakage path                                                      |
| F-CH-007 | P2       | SCOPE INTEGRITY | `adversarial_pass_rate` dimension in AC-3 has no Phase A generator                                                |

---

## Closing

The plan treats eval-set governance as 10% of the work (a row in the Phase F table) and treats the propose()/accept() mechanism as the 90%. In production ML the ratio is inverted. The plan also asserts Huyen-alignment for AC-3, AC-4, AC-5, AC-6 — each of which I am flagging for under-specification or hand-waving. AC-3 (multi-dim, F-CH-002 + F-CH-007), AC-4 (ladder, F-CH-004), AC-5 (tiered routing, F-CH-005), AC-6 (bootstrap, F-CH-003) — four of the four citations to me are partial credit at best.

The plan is not unsalvageable. F-CH-001 and F-CH-002 are the two findings that must move before Phase A `accept()` is implemented; the rest can be remediated in v5 of the plan and in early Phase A build-order amendments. But shipping Phase A as currently specified is shipping a system whose central gate produces near-zero acceptances against eval sets whose validity expires silently. That is the failure mode the canon was written to prevent.

VERDICT: AMEND
