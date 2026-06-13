---
title: Optimizer Safety Model — the autonomy ladder, accept predicate, and blast-radius bounds for automated SKILL.md improvement
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: DR-028 (Skill Refiner ratification) + Blueprint A § 1.2 (one-variable-change, rollback-as-pin)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — the constitution)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — SkillSnapshot / RolloutGate / Evidence Bundle)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E14
bead: bd_000-projects-2bic
filing_standard: Document Filing Standard v4.3
related_docs:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — § 1.2 principles 2/4/6 the optimizer obeys)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — SkillSnapshot, RolloutGate entities)
  - 014-DR-GLOS-canonical-glossary.md (SkillSnapshot / RegressionPack / replay terminology)
  - 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md (Skill Refiner plan v5)
  - 028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md (DR-028 — accept predicate)
  - 072-AT-ARCH-human-review-governance-2026-06-18.md (HR-2 human gate for production-pinned proposals)
related_drs:
  - 028-AT-DECR (DR-028 — strict-improvement-on-Pareto accept predicate; Phase D killed; SkillVersion entity)
  - 034-AT-DECR (DR-028 amendment — Phase A.0 provider choice)
  - 036-AT-DECR (Phase A.0 result — proceed)
state_element_status: EXPERIMENTAL
---

> **State label: NORMATIVE.** Binding safety doctrine for any automated optimizer that
> proposes changes to platform artifacts — concretely, the Skill Refiner. The Refiner
> *mechanism* is `EXPERIMENTAL` (DR-028 Phase A.0 null-hypothesis baseline gates whether
> the mechanism beats naive-in-context at all; the `skill-refiner-pass/v1` predicate is
> `RESERVED`). This doctrine binds the optimizer's behavior the moment any line of it
> runs. "Document now, build later" per epic iel-E14.

# Optimizer Safety Model

**Beads:** `bd_000-projects-2bic` (iel-E14c) under epic `bd_000-projects-14j` (iel-E14 —
operational doctrine bundle). GitHub: `jeremylongshore/intent-eval-lab#48`. Plane: LAB-46.

## 0. What an "optimizer" is here, and why it needs a safety model

An **optimizer** is any automated process that *proposes a change to a platform artifact
on the basis of eval evidence.* The canonical instance is the **Skill Refiner** — the
eval-guided improvement loop that proposes minimal SKILL.md edits (DR-028; plan
`027-PP-PLAN`). The third product in the agent-rig stack: **J-Rig Skill Binary Eval**
(test) → **Skill Refiner** (improve) → **Rollout Gate** (ship).

An optimizer is dangerous in a way a gate is not. A gate *reads* and *verdicts*; an
optimizer *writes.* An unbounded writer that optimizes against a metric will (a) overfit
to the eval set, (b) Goodhart the metric, (c) silently regress on dimensions the eval set
does not cover, and (d) — if it can self-apply — compound those errors across versions
faster than a human can catch them. This doctrine is the set of bounds that keep an
optimizer *additive and reversible*: every proposal is gated, every accepted change is a
new immutable version (never an in-place edit), and rollback is always "switch the pin
back" (Blueprint A § 1.2 principle 4).

This document **derives from and does not override** DR-028 or Blueprint A. On conflict,
DR-028 wins for the accept predicate and entity model; Blueprint A wins for the ecosystem
principles.

## 1. The accept predicate — the line an optimizer cannot cross alone

### R1 — Strict improvement on Pareto-dominant behavioral, non-regressing on others

A Refiner proposal is accepted **only** if it satisfies the DR-028 P0-RATIFY-1 predicate:
**strict improvement on a Pareto-dominant behavioral criterion, with non-regression on
every other criterion.** Restated:

- At least one behavioral criterion **strictly improves** (the proposal must *do
  something* — a no-op is not an improvement); AND
- **No** criterion regresses (not the headline metric, not any other).

A proposal that improves criterion A by regressing criterion B is **rejected**, full stop.
This is the anti-Goodhart firewall: the optimizer cannot buy a win on the measured metric
with a loss anywhere else. "Better on average" is not the bar; "better on something and
worse on nothing" is.

### R2 — The predicate is evaluated against the eval set, which is necessarily partial

The accept predicate is evaluated against the **kernel-pinned eval set.** Per the Evidence
Bundle composability principle (SPEC § 1), partial coverage is explicitly valid — and the
eval set is *always* partial. This is the load-bearing limitation: **R1 proves no
regression on what is measured; it cannot prove safety on what is not measured.** That gap
is exactly where the autonomy ladder (§ 2) and the human gate (§ 3) exist.

### R3 — Accepted proposals emit `skill-refiner-pass/v1`

An accepted proposal is recorded as a signed in-toto Statement v1 row under the predicate
URI `https://evals.intentsolutions.io/skill-refiner-pass/v1` (PREDICATE-TYPES.md RESERVED;
DR-028). The row attests "this SKILL.md edit passed the strict-improvement-on-Pareto
predicate against eval-set version V at commit C." The URI is RESERVED — reserving/
activating it is a Class-1 ISEDC act, and this doctrine does not perform that act; it fixes
what the row must mean.

## 2. The autonomy ladder

An optimizer operates at exactly one of the following autonomy rungs for any given
artifact. The rung is a property of **what the proposal touches**, not the optimizer's
confidence. The ladder is closed.

| Rung | Optimizer may | Without | Applies when the proposal touches |
| --- | --- | --- | --- |
| **A-0 PROPOSE-ONLY** | Generate a proposal + run the accept predicate + emit the result as evidence. | Never applies anything. | The default for any new optimizer or strategy until A-1 is earned. |
| **A-1 AUTO-STAGE** | Stage an accepted proposal as a new `SkillVersion` (a candidate `SkillSnapshot`), pending a `RolloutGate`. | Never promotes a pin. | A `SkillSnapshot` that is **not** referenced by any production rollout pin. |
| **A-2 GATED-AUTO-APPLY** | Submit a staged version through the `RolloutGate` and, on a passing ship verdict, advance the pin. | Never bypasses the gate; never touches a one-way-door surface. | A `SkillSnapshot` whose `RolloutGate` policy explicitly opts into auto-apply for this strategy. |
| **HR-2 HUMAN-GATED** | Nothing automatically. Escalates to a human (`072-AT-ARCH` § 2). | — | A `SkillSnapshot` **referenced by a production rollout pin**, OR an edit that also touches a one-way-door surface (predicate URI, signing identity, brand commitment). |

The optimizer **starts at A-0** and earns higher rungs per strategy, per artifact class —
never globally. Earning a rung is itself an evidence-backed decision (a strategy
demonstrating an acceptance-vs-regression track record), not a flag a developer flips.

### R4 — A production-pinned artifact is always at least HR-2

No optimizer rung above HR-2 exists for an artifact a production rollout depends on. The
accept predicate (R1) proves no regression *on the eval set*; a production pin's blast
radius extends to behavior the eval set does not cover (R2). That residual risk is a
**human judgment** — HR-2 in the human-review governance doctrine. The optimizer never
auto-applies across that line; the human gate *is* the line.

## 3. Blast-radius bounds — every change is additive and reversible

### R5 — Accepted change is a new SkillVersion, never an in-place edit

An accepted Refiner proposal produces a **new** `SkillVersion` (DR-028 T1: the 14th kernel
entity, carrying `version_kind` + `parent_version_id` + `source_snapshot_hash`), which
freezes into a new candidate `SkillSnapshot`. The optimizer **never edits a `SkillSnapshot`
in place** — snapshots are immutable (glossary § 2.9). Rolling forward through a passing
`RolloutGate` produces a new snapshot; it never mutates the old one (glossary § 2.9). This
is what makes every optimizer action reversible: rollback is "switch the pin back to
`parent_version_id`" (Blueprint A § 1.2 principle 4), an O(1) pin flip, never a revert of a
mutation.

### R6 — One variable per proposal

Each proposal changes **one variable** (Blueprint A § 1.2 principle 6). A proposal that
bundles three edits is rejected for un-attributability: if it passes, you cannot tell which
edit earned the win; if it fails, you cannot tell which edit caused the regression.
Comparing `RegressionPack` N to N+1 (glossary § 2.7) must reveal *exactly* which variable
changed and what outcomes shifted. The optimizer proposes atomically or not at all.

### R7 — The optimizer cannot move its own gate

An optimizer MUST NOT propose edits to: the accept predicate (R1), the eval set it is
scored against, the `RolloutGate` policy that governs its own auto-apply, or this safety
model. An optimizer that can lower its own bar is an optimizer optimizing the bar, not the
artifact — the canonical reward-hacking failure. Changes to any of those surfaces are
governance acts (Class-1/Class-2 per DR-010 § 7 Q6), authored by humans, never proposed by
the thing they constrain.

### R8 — Bounded self-generation; Phase D stays killed

Per DR-028 T2 (12 of 14 voices), **Phase D — self-generation of eval targets / training
signal by the optimizer — is an ANTI-GOAL and stays killed.** The optimizer improves
artifacts against a **human-and-evidence-curated** eval set; it does not generate the eval
set it is scored against (that is R7's reward-hacking, at the dataset level). The Karpathy
+ Gregg minority binding fixes the *only* re-open trigger: self-generation lift `> +8pp` on
the kernel-pinned eval set on any frontier release, OR internal acceptance-rate parity.
Absent that signal, the optimizer does not author its own training data.

## 4. The null-hypothesis discipline

### R9 — A mechanism that does not beat naive must not ship

Before the Refiner mechanism is trusted, it must clear the **Phase A.0 null-hypothesis
baseline** (DR-028 P0-RATIFY-3; amended provider choice DR-034; result DR-036): if
naive-Opus-in-context beats the proposed Refiner mechanism by `> 70%` of projected lift,
Phase B descopes. An optimizer is justified only by the lift it produces *over the trivial
baseline.* A mechanism that wraps complexity around a result a one-shot prompt already
achieves is negative value — it adds maintenance cost (the founder-hour gate, `073-AT-STND`
§ 5) and a new blast-radius surface for no behavioral gain. The result publishes as a blog
post regardless of outcome (VP DevRel binding) — a negative result is a legitimate,
publishable finding, not a failure to hide.

## 5. Relationship to the rest of the stack

- **Human-review governance** (`072-AT-ARCH`) — HR-2 is the escalation rung of this
  ladder; § 3 R4 routes production-pinned proposals there.
- **Economics governance** (`073-AT-STND`) — each new optimizer strategy (especially any
  that introduces a Python package) is bounded by the founder-hour cap and the 15-hr/
  release Python gate (`073-AT-STND` § 5). The optimizer's own run cost is a `CostRecord`.
- **Priority governance** (`075-AT-STND`) — optimizer-proposed work sits *below* the
  primary client engagement and below human-authored roadmap items in the priority lattice;
  the optimizer does not get to reorder the queue toward its own proposals.
- **Rollout Gate** — the A-2 rung's promotion path; the gate is the machine that decides
  ship/no-ship on a staged version, exactly as for a human-authored snapshot.

## 6. Anti-patterns — refuse on sight

- **Accepting a trade.** Accepting a proposal that improves one criterion by regressing
  another (violates R1). Better-on-something-worse-on-nothing or reject.
- **Treating eval-set pass as total safety.** Auto-applying to a production-pinned artifact
  because the accept predicate passed, ignoring uncovered behavior (violates R2/R4). The
  eval set is always partial; the human gate covers the gap.
- **In-place snapshot edit.** Mutating an existing `SkillSnapshot` instead of producing a
  new `SkillVersion` (violates R5). Snapshots are immutable; rollback is a pin flip.
- **Bundled proposal.** Changing multiple variables in one proposal (violates R6).
  Un-attributable wins and un-attributable regressions both forbidden.
- **Moving its own gate.** Proposing edits to the accept predicate, eval set, rollout
  policy, or this doctrine (violates R7). The optimizer cannot lower its own bar.
- **Self-generating the eval set.** Reviving Phase D — having the optimizer author the
  targets it is scored against — absent the Karpathy+Gregg re-open trigger (violates R8).
- **Shipping a mechanism that loses to naive.** Building Refiner complexity that does not
  beat naive-in-context by the Phase A.0 margin (violates R9).
- **Global autonomy flag.** Granting an optimizer A-2 across all artifacts via one switch
  instead of per-strategy, per-artifact-class earned rungs (violates § 2).

## 7. Cross-references

- **DR-028** (`028-AT-DECR`) — accept predicate (P0-RATIFY-1), SkillVersion entity (T1),
  Phase D anti-goal (T2), null-hypothesis decision rule (P0-RATIFY-3), `skill-refiner-pass/v1`.
- **DR-034 / DR-036** — Phase A.0 provider choice + proceed result.
- **Skill Refiner plan** (`027-PP-PLAN` v5) — the mechanism this doctrine bounds.
- **Blueprint A** (`011-AT-ARCH`) § 1.2 principles 2 (replay), 4 (rollback-as-pin),
  6 (one-variable-change).
- **Blueprint B** (`012-AT-ARCH`) § 2.7 (RegressionPack), § 2.8 (RolloutGate), § 2.9
  (SkillSnapshot immutability).
- **Canonical glossary** (`014-DR-GLOS`) § 2.7/2.8/2.9 (entities), § 3 (replay).
- **Evidence Bundle SPEC** (`specs/evidence-bundle/v0.1.0-draft/SPEC.md`) § 1
  (composability / partial coverage), § 4 (row shape), § 7 (signing).
- **PREDICATE-TYPES.md** — RESERVED `skill-refiner-pass/v1`.
- **Siblings:** `072-AT-ARCH-human-review-governance` (HR-2 gate),
  `073-AT-STND-economics-and-cost-governance`, `075-AT-STND-priority-governance`.

## 8. License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
