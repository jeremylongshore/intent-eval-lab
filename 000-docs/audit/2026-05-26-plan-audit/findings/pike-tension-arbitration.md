# Pike — Tension Arbitration

**Channeling:** Rob Pike (Go, Plan 9, UTF-8) — thinker-canon seat
**Scope:** 4 cross-seat tensions from synthesis.md
**Date:** 2026-05-27
**Verdict (preview):** AMEND. Cut features, not specifications.

---

## T1 — SkillVersion / SkillSnapshot

> *"Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident."* — Rule 5

> *"Don't communicate by sharing memory; share memory by communicating."*

Two types. Orthogonal. No FK.

- `SkillSnapshot` — pinned bytes at moment T. Content-addressed. No lineage.
- `SkillVersion` — node in a refinement DAG. Carries `parent_version_id`, `version_kind`, score delta. No snapshot pointer.

Compose at use-site. A run that needs both holds both; the kernel does not entangle them.

Hickey's "merge them" loses the DAG semantic. Kleppmann's "shared parent + discriminator" turns two clean types into one cluttered one with a mode field — the union-type trap. The internal architect's P1-1 ("fully orthogonal, no FK") is the right answer.

Errors are values: add `version_kind: edit | revert | restore` as a typed enum on `SkillVersion` only. Don't document the failure modes — encode them.

**Arbitration:** internal-architect P1-1. Two orthogonal types. No FK either direction.

## T2 — Phase D resolution

> *"Clear is better than clever."*

"Deferred indefinitely at P3" is three hedges in one phrase. Pick the sentence:

> Intent Solutions does not build a creator product. SkillsBench evidence shows self-generated skills underperform human-authored ones. If frontier-model evidence inverts this, re-open.

That's it. One sentence. Goes in Blueprint A § 3 as anti-goal. The bead and the P3 row in the plan delete.

Karpathy's "quarterly re-measurement" is well-intentioned but adds a recurring process where a Blueprint anti-goal does the job for free. The re-open trigger is a frontier-model release — that's an external event, not a calendar event. Don't schedule what the world will tell you.

**Arbitration:** Cunningham. Anti-goal. Delete the row.

## T3 — Process discipline weight

> *"A little copying is better than a little dependency."*

AC-12 tri-link couples bd ↔ GH ↔ Plane through `bd-sync` + a verifier + a CI gate + § 3.5 PR-1 + D7. Five mechanisms enforcing one invariant across three writable stores. That's the dependency. The copy is cheaper.

Pick ONE writer: **bd is the source of truth.** GH issues and Plane issues are projections — read-only mirrors generated FROM bd, never written back into. Comments on GH that need to round-trip become explicit `bd-sync pull` operations, not implicit consistency.

Seven disciplines collapse to one: bd writes; everything else reads. The verifier becomes a one-liner ("does bd know about every linked artifact?"). AC-12 deletes. § 3.5 PR-1 deletes. D7 stays only as the read-side check.

Cunningham wants 7 → 1-2 abstractions. Hickey wants AC-12 gone. Both correct; this collapse satisfies both.

**Arbitration:** bd is the writer. GH/Plane are projections. Six disciplines delete.

## T4 — Mechanism vs product

Intent Solutions sells the **eval discipline**, not the refiner.

> *"Show me your eval set and I'll tell you what you sell."*

The refiner is an implementation of one strategy against the discipline. Karpathy's RefinerStrategy interface (F-AK-002) is the giveaway: if it's swappable, it's not the product. The eval set + the acceptance predicate + the signed evidence — that's the product.

The plan currently treats Skill Refiner as the second product in a three-product stack. Reframe: J-Rig is product 1 (the eval surface). Rollout Gate is product 2 (the decision surface). The refiner is a feature of product 1.

**Arbitration:** demote Skill Refiner to a feature of J-Rig Skill Binary Eval. Three-product framing collapses to two.

---

## Verdict

**AMEND.**

| Tension | Resolution |
|---|---|
| T1 | Two orthogonal types, no FK (architect P1-1) |
| T2 | Cunningham — anti-goal sentence, delete the row |
| T3 | bd-as-writer; GH/Plane as projections; six disciplines delete |
| T4 | Demote refiner to a J-Rig feature; two products, not three |

Five things removed. Zero added. Data structures do the work the prose was trying to do.

— Pike (channeled)
2026-05-27

