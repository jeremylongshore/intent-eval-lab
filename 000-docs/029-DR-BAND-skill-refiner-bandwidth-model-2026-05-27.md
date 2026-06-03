# Skill Refiner — Bandwidth Model (closes Beck F-KB-001 P0)

| Field      | Value                                                                                                                                                               |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Status     | RATIFIED 2026-05-27 per DR-028 implementation directive #1                                                                                                          |
| Owner      | Jeremy Longshore (solo operator) + Claude (delegated executor)                                                                                                      |
| Purpose    | Replace plan 027 v4.1's aspirational "~1 week" / "~2 weeks" phase budgets with an FTE-week budget model + critical-path bead callouts, per Beck F-KB-001 P0 finding |
| Beads      | RC-IEL (bd_000-projects-rqwk), RC-IAJ (bd_000-projects-214c), RC-IEC (bd_000-projects-brij), RC-IAH (bd_000-projects-aon3), RC-IAR (bd_000-projects-r8ir)           |
| GitHub     | jeremylongshore/intent-eval-lab#78 (RC-IEL)                                                                                                                         |
| Supersedes | Plan 027 § 4 "~N weeks" phase budgets (inline placeholders); plan v5 references this doc                                                                            |

## 1. Operating constraint

Intent Solutions is a sole-proprietor operation. The unit of bandwidth is **FTE-day** (one engineer-day; the engineer is the user OR Claude executing on the user's behalf with user review gating). Concurrent work IS possible (e.g., Claude executes Phase A.0 baseline while user handles partner work) but synchronization points consume both heads.

**Bandwidth caps observed in practice (per Beck F-KB-001 + AAR-023):**

- Continuous focus block: ~6 FTE-hours/day (0.75 FTE-day) sustainable
- Synchronization overhead between Claude + user: ~0.25 FTE-day per non-trivial review cycle
- Context-switching tax across the 5 IEP repos + claude-code-plugins + tier-2 work: ~10% drag
- External-dependency wait (Gemini quotas, GH Actions, sigstore Rekor): bursty 0-2 hours/day, NOT bandwidth but wall-clock

## 2. FTE-week budget per phase (DR-028-amended)

Each row shows: FTE-days for in-scope work · critical-path bead (the bead that gates the rest) · external blockers (NOT bandwidth, but gate phase exit).

### Phase A.0 — Null-hypothesis baseline (NEW per P0-RATIFY-3)

| Item                                                            | FTE-days         | Owner       | Notes                                     |
| --------------------------------------------------------------- | ---------------- | ----------- | ----------------------------------------- |
| Eval-set bootstrap for `/validate-skillmd` (Phase B demo skill) | 1.5              | Claude      | Synthetic + human-nominated golden traces |
| Naive-Opus-in-context baseline run                              | 0.5              | Claude      | Single-pass, no refinement                |
| Result analysis + decision (Refiner mechanism YES/DESCOPE)      | 0.5              | User+Claude | Sync point; gates Phase A                 |
| Blog-post publication (per VP DevRel binding)                   | 1.0              | Claude+User | Transparency artifact                     |
| **Subtotal**                                                    | **3.5 FTE-days** |             | Bandwidth-gated; no external blockers     |

### Phase A — Skill Refiner discipline library

| Item                                                                                       | FTE-days                              | Owner       | Notes                                                                                                     |
| ------------------------------------------------------------------------------------------ | ------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------- |
| `@j-rig/refiner-core` package scaffold + value types (IAJ-N1)                              | 1.0                                   | Claude      | Pure types; no I/O                                                                                        |
| `apply()` + `accept()` PURE FN impl (per AC-7 durable contribution)                        | 1.5                                   | Claude      | The durable contribution per DR-028 P0-RATIFY-1 binding (Pareto-dominant + non-regressing + tie-breaking) |
| `bootstrap()` impl (synth + harvest + golden, AC-6)                                        | 1.5                                   | Claude      | + EvalSet versioning per P0-RATIFY-6                                                                      |
| Event log + content-addressed store + best-pointer (per CTO P1 finding)                    | 1.0                                   | Claude      | Append-only at FS-level per P0-RATIFY-2                                                                   |
| `score()` delegator to j-rig CLI                                                           | 0.5                                   | Claude      | Adapter only                                                                                              |
| `propose()` impl + tiered routing (Haiku/Sonnet per AC-5; NO Opus)                         | 1.5                                   | Claude      | DR-028 type-sig fix already landed in v4.1                                                                |
| `RefinerStrategy` interface + NaiveInContext + SkillOptStyle reference impls (P0-RATIFY-5) | 1.5                                   | Claude      | One interface, two impls; first impl is the Phase A.0 baseline upgraded                                   |
| CLI surface (5 commands)                                                                   | 1.0                                   | Claude      | bootstrap/score/propose/apply/status                                                                      |
| Vitest coverage gate ≥ 80% (IAJ-N4)                                                        | 0.5                                   | Claude      |                                                                                                           |
| 021-AT-SPEC refiner-core API doc + D4/D8 diagrams (IAJ-N5)                                 | 0.5                                   | Claude      |                                                                                                           |
| Release ceremony + sigstore provenance (synchronized refiner-core@0.1.0 + refiner@0.1.0)   | 1.0                                   | User+Claude | Sync point; uses canonical IEC release.yml pattern                                                        |
| **Subtotal**                                                                               | **11.5 FTE-days** ≈ **2.3 FTE-weeks** |             | Bandwidth-gated; companion to `iep-P2` j-rig hardening                                                    |

**Phase A v4.1 budget said "~1 week"; revised actual = 2.3 FTE-weeks.** The bandwidth gap is +130%.

### Phase B — `/j-rig` plugin v0.1.0 (Refiner + 3-layer hooks)

| Item                                                                                     | FTE-days                             | Owner       | Notes                                                             |
| ---------------------------------------------------------------------------------------- | ------------------------------------ | ----------- | ----------------------------------------------------------------- |
| Plugin scaffold + plugin.json + hooks/hooks.json                                         | 0.5                                  | Claude      |                                                                   |
| L1 Sinker hook (`PostToolUse:Edit/Write` on SKILL.md → `validate-skillmd` Tier 2)        | 1.0                                  | Claude      | $0 — no model call                                                |
| L2 Line hook (`Stop` → rollout capture + background refiner)                             | 2.0                                  | Claude      | Most complex; coordinates with @j-rig/refiner                     |
| L3 Hook (`PreToolUse:Bash` matcher `git commit\|git push` — DR-028 v4.1 mechanism fix)   | 1.5                                  | Claude      | $$ Opus agentic gate; rate-limited                                |
| Plugin CLI bindings (5 user-invokable commands)                                          | 0.5                                  | Claude      |                                                                   |
| `claude-code-plugins` marketplace publish + plugin.json registration                     | 0.5                                  | User+Claude | Outside IEP umbrella; lives in separate repo                      |
| Phase B demo end-to-end (`/validate-skillmd` refined; Evidence Report generated locally) | 2.0                                  | Claude+User | Sync point; the proof artifact                                    |
| Blog post on Phase B demo (per CMO + VP DevRel bindings)                                 | 1.5                                  | Claude+User | Same blog as Phase A.0 baseline publication OR separate follow-up |
| **Subtotal**                                                                             | **9.5 FTE-days** ≈ **1.9 FTE-weeks** |             | Bandwidth-gated; companion to claude-code-plugins repo work       |

**Phase B v4.1 budget said "~2 weeks"; revised actual = 1.9 FTE-weeks** — close to estimate, slight over.

### Phase C — Tier-1 IEP integration (SkillVersion in `@intentsolutions/core@0.3.0`)

| Item                                                                                                                           | FTE-days                              | Owner        | Notes                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------- | ------------ | ---------------------------------------------------------------------------------- |
| SkillVersion schema (DR-028 T1 DISCRIMINATOR — separate entity, `version_kind` + `parent_version_id` + `source_snapshot_hash`) | 2.0                                   | Claude       |                                                                                    |
| Zod validator regen                                                                                                            | 0.5                                   | Claude       | Via `pnpm run codegen:validators`                                                  |
| Skill-refiner-pass/v1 predicate schema                                                                                         | 1.0                                   | Claude       | Pareto + significance + tie-breaking NORMATIVELY per P0-RATIFY-1 + CSO binding     |
| Cross-field invariants + `pending_production` state + outbox+reconciler (P0-RATIFY-2)                                          | 2.5                                   | Claude       | The CISO hard-line binding; the most-load-bearing work in Phase C                  |
| `j-rig emit-refiner-pass` CLI                                                                                                  | 1.0                                   | Claude       | Parallel to `emit-evidence`                                                        |
| Sigstore Rekor outbox + reconciler (P0-RATIFY-2 binding)                                                                       | 2.0                                   | Claude       | Bounded retry (max_retries=5), `retry_after` timestamp, `signing_failed` surfacing |
| intent-rollout-gate M5 consumer wiring (IAR-N1)                                                                                | 1.0                                   | Claude       | Advisory enrichment, NOT blocking per AC-4                                         |
| audit-harness envelope schema + baseline updates (IAH-N1/N2)                                                                   | 1.5                                   | Claude       |                                                                                    |
| Blueprint B § 7 extension + canonical-glossary update (IEL-N1, IEL-N3, 0r8m.4, 0r8m.5)                                         | 2.0                                   | Claude       |                                                                                    |
| ISEDC Session 8 (URI namespace ratification — `evals.intentsolutions.io/skill-refiner-pass/v1`)                                | 0.5                                   | User+Council | Sync point                                                                         |
| `@intentsolutions/core@0.3.0` release ceremony                                                                                 | 1.0                                   | User+Claude  | Tag-trigger pattern per bd memory                                                  |
| **Subtotal**                                                                                                                   | **15.0 FTE-days** ≈ **3.0 FTE-weeks** |              | **GATED on `uprg` + `9pi3`** — see external blockers below                         |

**Phase C v4.1 budget said "~3-4 weeks"; revised actual = 3.0 FTE-weeks bandwidth + external wait.**

### Phase D — KILLED (anti-goal per DR-028 T2)

**0 FTE-days.** Blueprint A § 3.X amendment is ~0.5 FTE-day, folded into Phase C's Blueprint B work.

### Phase E — Evidence report production (ongoing)

| Item                                   | FTE-days                             | Owner  | Notes                                         |
| -------------------------------------- | ------------------------------------ | ------ | --------------------------------------------- |
| SPEC.md template authoring (0r8m.9)    | 1.5                                  | Claude | 10 required sections per plan § E.1           |
| Hugo HTML renderer (0r8m.10)           | 2.0                                  | Claude | ~200 LOC; lives in partner-portal repo        |
| First end-to-end report (Phase B demo) | 1.0                                  | Claude | Sync with Phase B exit                        |
| **Subtotal**                           | **4.5 FTE-days** ≈ **0.9 FTE-weeks** |        | Bandwidth-gated; concurrent with Phase B exit |

### Phase F — DEFERRED until triggers fire (no commitment)

Per plan § 4 Phase F triggers (5+ partners / 100+ SkillVersions / first rollback). 0 FTE-days budgeted in this model.

## 3. Aggregate budget (DR-028-amended)

| Phase     | FTE-weeks                                  | Wall-clock floor      | Gated on                                            |
| --------- | ------------------------------------------ | --------------------- | --------------------------------------------------- |
| Phase A.0 | 0.7                                        | ~1 calendar week      | nothing                                             |
| Phase A   | 2.3                                        | ~3 calendar weeks     | nothing                                             |
| Phase B   | 1.9                                        | ~3 calendar weeks     | Phase A ship                                        |
| Phase C   | 3.0                                        | ~5+ calendar weeks    | `uprg` close + `9pi3` close + `iec-E12` v0.2.0 ship |
| Phase E   | 0.9                                        | concurrent w/ Phase B | —                                                   |
| **TOTAL** | **8.8 FTE-weeks** ≈ **~3 calendar months** |                       | with phase-gating + sync overhead                   |

**Plan 027 v4.1 said "MVP through full-scale" implied ~6-8 weeks.** Revised actual: **~12-14 weeks (~3 calendar months) bandwidth-gated.** The estimate was ~50% under.

## 4. Critical-path beads (single-bead-blocks-phase)

| Phase     | Critical-path bead                                                                                 | Why it gates                                                                           |
| --------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Phase A.0 | NEW bead: Phase A.0 null-hypothesis baseline (filed via DR-028 directive #5)                       | Gates Phase A — if naive beats Refiner, Phase B is descoped                            |
| Phase A   | IAJ-N1 (refiner-core scaffold)                                                                     | Everything else depends on the value-types                                             |
| Phase A   | NEW bead: RefinerStrategy interface (filed via DR-028 directive #4)                                | Enables 2 reference impls per P0-RATIFY-5                                              |
| Phase B   | NEW bead: bd-claim-precheck.sh script (filed via DR-028 directive #7) — already-built this session | Gates first `bd claim` per P0-RATIFY-4                                                 |
| Phase C   | `iec-E12` (bd_000-projects-33tc) v0.2.0                                                            | SkillVersion lands in v0.3.0 only after E12 ships                                      |
| Phase C   | NEW bead: sigstore Rekor outbox+reconciler (filed via DR-028 directive #8)                         | CISO P0-RATIFY-2 binding for `pending_production` state                                |
| Phase C   | `uprg` (bd_000-projects-uprg)                                                                      | Evidence Bundle compat policy MUST land before predicate URI is signed into prod Rekor |
| Phase C   | `9pi3` (bd_000-projects-9pi3)                                                                      | OTel semconv MUST be pinned before kernel v0.3.0                                       |

## 5. External blockers (NOT bandwidth, but gate phase exit)

| Blocker                                                            | Status                                       | Negotiation owner                                                              | Plan-level fallback if not closed                                                      |
| ------------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| `uprg` — Evidence Bundle compat policy                             | OPEN P0                                      | Jeremy (sole-prop; no external counterparty)                                   | Phase C deferred indefinitely; Phases A+B can ship without it                          |
| `9pi3` — OTel semconv pin                                          | OPEN P0                                      | Jeremy + OTel SIG-GenAI (community-temperature reconnaissance per CSO binding) | Same as above                                                                          |
| `iec-E12` v0.2.0 — EvidenceBundlePayload + cross-field invariants  | OPEN P0 (depends on `iec-E12a` + `iec-E12b`) | Jeremy                                                                         | Phase C blocked                                                                        |
| Sigstore Rekor production availability                             | Depends on rekor.sigstore.dev SLA            | n/a                                                                            | `pending_production` state + outbox handles transient outages per P0-RATIFY-2          |
| Claude Code v2.1.152 `disallowed-tools` adoption rate              | Depends on Anthropic                         | n/a                                                                            | AC-11 spec-pinning is locally-forked snapshot; not gated on Anthropic                  |
| Gemini Code Assist daily quota                                     | Bursty unavailability                        | n/a                                                                            | 4-reviewer internal pre-flight pass per this session's pattern; Gemini is nice-to-have |
| `iah-npm-publish-gap` (audit-harness v1.1.4 git tag vs v0.1.0 npm) | OPEN P1                                      | Jeremy                                                                         | Phase C explicitly notes shell-out fallback                                            |

## 6. Dependency-direction-honesty (Cunningham F-WC-005 binding)

Per DR-028 implementation, cross-repo dependencies (`uprg`, `9pi3`) ARE owner-negotiated by Jeremy as sole-prop. The previous concern was that the plan unilaterally scheduled work behind beads that hadn't been negotiated. In the sole-prop case, "negotiation with owner" = "Jeremy decides what order to do his own work in." This document IS that negotiation, made explicit.

`bd update` notes added to `uprg` + `9pi3` + `iec-E12` referencing this bandwidth model + DR-028.

## 7. Re-validation cadence

This bandwidth model is the FIRST FTE-week budget shipped. Per Cunningham F-WC-001 AAR-cadence binding (folded into DR-028 implementation), this doc is re-validated:

- After Phase A.0 ships — does actual baseline FTE-day burn match estimate?
- After Phase A ships — same check on Phase A
- After each phase exit — adjust subsequent phases based on observed velocity
- Quarterly during long phases — drift detection

Re-validation outputs land as **DR-NNN-DR-BAND** amendments (next number: 030 if revalidated; bumped per Doc Filing Standard v4.3).

## 8. Pre-mortem (Cunningham + Beck binding)

**Most likely overrun:** Phase C cross-field invariant + outbox+reconciler work (CISO P0-RATIFY-2 binding). Estimated 4.5 FTE-days; first-time-doing-it tax suggests +50-100%. Mitigation: if Phase C work overruns by > 1 FTE-week, defer the outbox to v0.4.0 per CISO compromise position.

**Most likely under-run:** Phase A.0 baseline. The eval-set bootstrap for `/validate-skillmd` may be quicker than estimated because the skill IS a validator (deterministic outputs). If A.0 finishes in 2 FTE-days instead of 3.5, bank the slack toward Phase A's IAJ-N1 scaffold.

**External-dep tail risk:** `uprg` + `9pi3` are P0 but have NO ESTIMATED CLOSE DATE in their bead descriptions. The bandwidth model assumes they close before Phase C kickoff. If they don't, Phase C slips indefinitely (plan-level: ship Phases A+B without Phase C, treat A+B as v0.1.0 milestone).

— Jeremy Longshore
intentsolutions.io
