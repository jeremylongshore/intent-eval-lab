---
date: 2026-06-10
status: RATIFIED-WITH-DELTAS and CLOSED. Re-audit closure merged via PR #116 on 2026-06-11 with 0 residual P0. ISEDC Class-1 SAK charter RATIFIED via DR-049 (2026-06-10), re-ratified DR-081 (2026-06-17). Hard gate LIFTED; SAK-labeled beads claimable. Original v8 status was PROPOSED-FOR-REAUDIT (v8), closing the 4 blocking findings from the 2026-06-10 incremental re-audit of v7 and gating the ISEDC Class-1 charter.
class: plan amendment (audit-closure deltas)
supersedes_relationship: REVISES + EXTENDS plan 033 v7. Lands 4 re-audit-closure deltas. Does NOT supersede v7 — preserves all v7 section numbers; REVISES § 14.4c, § 14.18, § 14.27 and ADDS § 14.4.migration-concurrency, § 14.A.policy-eval, § 14.31 lifecycle-states.
parent_audit: 2026-06-10 incremental re-audit (workflow sak-v7-incremental-reaudit; 11 P0 closed, 2 still-open, 2 new = NEEDS-AMENDMENT-V8 by § 14.30 new-P0 count).
author: Jeremy Longshore (drafter — Claude as acting CTO under CEO-mode delegation, 2026-06-10)
beads: bd_000-projects-3kye (SAK epic), bd_000-projects-8vq0 (charter)
---

# Skill Refiner Plan v8 Amendment — Spec Authority Kernel (SAK) — re-audit-closure deltas

## Tri-link block

```text
Beads: bd_000-projects-3kye, bd_000-projects-8vq0
GitHub: jeremylongshore/intent-eval-lab#<TBA>
```

**Read order:** plan 027 v5 (ratified body) → plan 031 v6 (SAK introduction) → plan 033 v7 (audit-closure) → **THIS doc (v8 re-audit-closure)** → 032 charter draft (deferred convening).

## Status

**State: RATIFIED-WITH-DELTAS and CLOSED.** The re-audit of v8's deltas closed with 0 new P0 and merged via PR #116 (2026-06-11). The ISEDC Class-1 SAK charter is RATIFIED (DR-049 2026-06-10, re-ratified DR-081 2026-06-17); the hard gate is LIFTED and SAK-labeled beads are claimable. _Original v8 status (for history):_ PROPOSED-FOR-REAUDIT — v8 existed solely to close the 4 blocking findings the 2026-06-10 incremental re-audit surfaced in v7; the gate (§ 14.30) was 0 new P0 → RATIFIED-WITH-DELTAS → the ISEDC Class-1 charter (032) convenes.

## Why v8 (the re-audit finding)

The 2026-06-10 incremental re-audit confirmed v7 closes 11 of the 13 P0 sub-findings, but found 4 blockers — all **specification gaps, not design rejections**:

| #   | Finding                                                                                        | Defect in v7                                                                                                                                                                                                                              |
| --- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **F-MK-002** still open (Kleppmann, "most costly to recover from")                             | § 14.4 header _claims_ it closed, but the earmarked bead was retargeted to F-MK-005 (a different rollback-window concern); the 3 concrete migration-concurrency rules appear nowhere.                                                     |
| 2   | **F-AK-002** still open (Karpathy, "schemas are prompts; we don't ship prompts without evals") | The schema-POLICY eval (does isMarketplace correlate with downstream _quality_?) is unspecified; its bead is the only P0 bead naming no § section. § 14.21 measures schema-vs-fixture self-consistency, a different thing.                |
| 3   | **NEW-P0-1** (v7-introduced)                                                                   | § 14.4c's 30-day calendar ceiling forces the advisory→blocking flip while staying silent on preconditions (c) zero-open-P0 and (d) governance sign-off — permitting the highest-blast-radius flip with open P0s and no human in the loop. |
| 4   | **NEW-P0-2** (v7-introduced)                                                                   | § 14.18 (decompose-then-test: restructure the v1 schemas after they "ship") directly contradicts § 14.27 (read-only-immutable: never mutate authoring/v1 after publication).                                                              |

The 4 deltas below close them. Each is an acting-CTO resolution under CEO-mode delegation.

## Delta 1 — § 14.4.migration-concurrency (NEW) — closes F-MK-002

The Phase-4 corpus migration runs over a multi-week window against a **live, concurrently-edited** corpus (~3,543 files that are themselves being authored/PR'd during the migration). Three binding concurrency rules:

1. **Pinned target version.** SKILL.md authored _during_ the migration window target `LATEST_PHASE_4_VERSION` — a single kernel `authoring/v1` version frozen at migration start and recorded in `migration-manifest.json`. Authors never chase a moving schema; the manifest is the one source of "what do I target right now."
2. **Wave A precedes in-flight-PR merge.** Wave A (mechanical `batch-remediate`) for a file runs **before** any in-flight contributor PR touching that file is merged. On conflict, **wave-A-wins**; the contributor rebases onto the post-wave-A state. The reconciliation queue (**§ 14.17.3**, extended with the real-time enforcement capabilities specified in Delta 1.1 below) enforces the ordering: a file with a queued wave-A op blocks its own PR merge until wave A lands.
3. **Wave B never on open-PR files.** Wave B (Refiner) **never** runs on a file with an OPEN PR. The reconciliation queue (§ 14.17.3 / Delta 1.1) checks per-file open-PR state; open-PR files are **parked** and re-enqueued only after the PR merges or closes (composes with § 14.17 wave-B durability — parked ≠ failed).

Write-write conflict resolution is therefore deterministic and one-directional (wave-A-wins, wave-B-defers), eliminating the concurrent-author-vs-migration races MK flagged.

## Delta 1.1 — § 14.17.3 reconciliation-queue REVISED (real-time enforcement) — closes the v8 host-mechanism gap

The v8 re-audit correctly found that Delta 1's rules 2–3 named the wrong section (§ 14.20 is Phase-5 risk-acknowledgement) and leaned on the v7 reconciliation queue (§ 14.17.3) for capabilities it did not have — that queue was a **monthly-review disposition** queue (4 dispositions: keep-as-is / manual-migrate / deprecate-skill / schema-revision-candidate) with no per-file PR state and no merge-gating. Delta 1's guarantee is only real if the queue is built to enforce it. So § 14.17.3 is **extended** (not replaced — the monthly-review disposition function is unchanged and runs alongside) with a **real-time enforcement** capability:

- **Per-file state record** — each file tracked by the migration carries `{ open_pr_state: open|none, wave_a_pending: bool, wave_b_parked: bool, target_version: LATEST_PHASE_4_VERSION }`. `open_pr_state` is refreshed from `gh pr list --search "<path>"` on every queue tick (and on the GitHub `pull_request` opened/closed webhook).
- **Merge-gate (rule 2 mechanism)** — a **required CI check** `sak-wave-a-precedence` reads the queue and is RED for any file with `wave_a_pending=true`. Branch protection on the corpus repo treats it as required, so a contributor PR touching that file **cannot merge** until wave A lands and clears the flag. This is the concrete "blocks its own PR merge" hook.
- **Wave-B park (rule 3 mechanism)** — the wave-B dispatcher SKIPS any file with `open_pr_state=open`, sets `wave_b_parked=true`, and emits no Refiner op. The `pull_request:closed` webhook (merged or closed) clears `wave_b_parked` and re-enqueues the file on the next tick. Parked ≠ failed (composes with § 14.17 durability).
- **Determinism** — the only write-orderings the queue permits are wave-A-before-PR-merge (gate) and wave-B-after-PR-close (park). No path lets wave B and a contributor edit the same file concurrently, and no path lets a PR merge over an un-applied wave A. That is the F-MK-002 split-brain guarantee, now resting on a specified mechanism rather than an attributed one.
- **Wave-B PR exemption (stated invariant).** Wave-B Refiner PRs (auto-merged per § 14.17.1) are exempt from the `sak-wave-a-precedence` required check. This is safe-by-construction, not a carve-out: wave A always precedes wave B for any given file, so `wave_a_pending` is already `false` by the time a wave-B PR exists for that file. The implementer MUST preserve this ordering invariant; the gate keys on `wave_a_pending`, which a wave-B-eligible file never has set.

## Delta 2 — § 14.A.policy-eval (NEW) — closes F-AK-002

A schema is a policy; a policy shipped to a 3,000+-file corpus without an empirical check of the policy is the decision that compounds for years. A **Phase-1.5 schema-policy eval** gates promotion of any authoring contract's `$defs.isMarketplace` tier to canonical (D-SAK-2):

- **Corpus:** N ≥ 200 historical SKILL.md, each pre-scored with a quality label from `/validate-skillmd --thorough` OR human rating. The label is frozen + model-pinned ground truth (same discipline as the `drift-classification/v1` eval set).
- **Measure:** does `$defs.isMarketplace` accept/reject correlate with the quality label? Two named failure modes:
  - **false-reject** — a high-quality SKILL.md the schema REJECTS (over-strict policy);
  - **false-accept** — a low-quality SKILL.md the schema ACCEPTS (under-strict policy).
- **Pinned floor:** recall ≥ 0.95 on the high-quality class (≤ 5% false-reject) AND precision ≥ 0.90 (≤ 10% false-accept) before the contract's isMarketplace tier is declared canonical. Below floor → the policy is revised, not shipped.
- **Distinct from § 14.21:** § 14.21 = schema agrees with its own fixtures (internal consistency); § 14.A.policy-eval = the policy agrees with downstream quality (external validity). **Both are required** before canonical promotion.

## Delta 3 — § 14.4c REVISED — closes NEW-P0-1 (flip-gate contradiction)

The advisory→blocking flip is the highest-blast-radius event in SAK. Its four exit preconditions are **not equal in override-ability**:

- **(a) coverage (≥ 99.5% corpus pass)** is the ONLY precondition the 30-day calendar ceiling dispositions: at day 30, if coverage < 99.5%, the gate MAY flip with the remaining < 0.5% of files **quarantined** (advisory-only, never blocking; tracked in the quarantine-queue) — preventing indefinite stall on long-tail files.
- **(c) zero-open-P0** (no open P0 in the schema-revision-candidates queue, § 14.A.3) and **(d) governance-triple sign-off** (CTO + CISO + VP DevRel, § 14.12) are **HARD gates the ceiling does NOT override.** The flip CANNOT fire without both — ever.
- **Stall resolution:** if (c) or (d) is unmet at day 30, the flip is **BLOCKED** and **auto-escalates to an ISEDC convening.** The calendar stall triggers a human DECISION, never an automatic flip. This closes both C1 ("no auto-flip without governance") and the v6 "indefinite stall" concern (the stall is bounded by escalation, not by auto-firing).

**Precedence, stated once:** governance + correctness gates are absolute; the calendar ceiling only caps coverage-quorum stall, and only by quarantining the long tail.

## Delta 4 — § 14.31 lifecycle-states (NEW) + § 14.18 / § 14.27 reconciliation — closes NEW-P0-2

`authoring/v1` schemas have three explicit lifecycle states:

1. **DRAFT** — pre-ship; freely mutable.
2. **SHIPPED-INTERNAL** — passes lint + exists in the repo, but **read-only to CONSUMERS** (no consumer has cut over) and **not yet "published."** Still mutable by the kernel team. This is the **decompose-via-failure working state**: § 14.18 Phase 1.5 restructures the single-`$defs.isMarketplace` schema into the 4-fold composition (§ 14.10) in response to test failures _while in SHIPPED-INTERNAL_.
3. **PUBLISHED** — first npm release of `authoring/v1` OR first consumer cutover, whichever comes first. **§ 14.27 read-only-immutable binds here, and only here:** after PUBLISHED, `authoring/v1` is NEVER mutated; bumps create `authoring/v2/`.

§ 14.18 (decompose-then-test) operates exclusively in DRAFT → SHIPPED-INTERNAL. § 14.27's "never mutated after publication" is scoped to PUBLISHED. The `LATEST_PHASE_4_VERSION` pin (Delta 1) names the first PUBLISHED version. No contradiction: structural mutation happens **before** publication; immutability binds **at and after** it.

## Re-audit gate (§ 14.30, restated for v8)

Re-audit v8's 4 deltas only (not §§ 1–13, not v6/v7 content already cleared). Per § 14.30: **0 new P0 → RATIFIED-WITH-DELTAS → ISEDC Class-1 charter (032) convenes; 1–3 new P0 → v9; > 3 → structural escalation to the user.**

— Jeremy Longshore
intentsolutions.io
