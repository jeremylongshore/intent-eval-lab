# Synthesis — Plan Audit Findings (7 seats)

**Plan under audit:** `000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1, commit `22fc55e`, PR #77)
**Date:** 2026-05-27
**Total findings filed:** ~46 across 7 seats
**Verdict tally:** 7/7 **AMEND**

| Seat       | P0     | P1     | P2     | P3/NIT | Verdict   |
| ---------- | ------ | ------ | ------ | ------ | --------- |
| Hickey     | 3      | 2      | 2      | 0      | AMEND     |
| Beck       | 3      | 3      | 1      | 0      | AMEND     |
| Karpathy   | 3      | 2      | 1      | 0      | AMEND     |
| Huyen      | 2      | 3      | 2      | 0      | AMEND     |
| Lamport    | 2      | 1      | 3      | 1      | AMEND     |
| Cunningham | 1      | 3      | 1      | 0      | AMEND     |
| Kleppmann  | 3      | 1      | 2      | 1      | AMEND     |
| **TOTAL**  | **17** | **15** | **12** | **2**  | **AMEND** |

## Convergent findings (≥2 seats raised the same defect)

These are HIGH-CONFIDENCE remediations — multiple independent seats arrived at the same defect from different lenses.

### CONV-1 — Acceptance gate "strict improvement on all dimensions" is broken (5+ seats convergent)

**Severity: P0**
**Raised by:** Hickey F-RH-007, Beck F-KB-002, Huyen F-CH-002, Lamport F-LL-01, Kleppmann F-MK-6 + Karpathy implicit
**The defect:** Plan AC-3 (multi-dim scores) + the `accept()` predicate that says "strict improvement on all dimensions" is internally inconsistent. (a) ScoreRecord is typed as open record `[dimension: string]: unknown` — `accept()`'s "all dimensions" is undefined for any dimension the authors didn't anticipate (Hickey). (b) Under independence + ≥4 dimensions + SkillsBench's 16/84 (~19%) regression rate, expected acceptance rate is < 30% — the gate will reject nearly all real improvements (Huyen). (c) No tie-breaking rule for Pareto-incomparable cases (Kleppmann). (d) The `accept()` boolean is type-unsound given multi-dim scores per AC-3's "never collapsed to scalar" rule (Lamport). (e) Beck — "If you have to test it later, you don't have it yet." The acceptance gate is the load-bearing AC-7 durable contribution; it has no working specification.
**Action:** Replace strict-on-all with an EXPLICITLY DEFINED partial-order policy (e.g., "Pareto-dominant on the kernel-pinned `behavioral` dimension + non-regressing on all other named dimensions, with statistical-significance threshold T"). Pin the dimension set in the kernel SkillVersion schema. Specify tie-breaking. Until the predicate is formally defined, the Refiner cannot have a meaningful production verdict.

### CONV-2 — Append-only event log + signing has no consistency property (2 seats convergent)

**Severity: P0**
**Raised by:** Lamport F-LL-02, Kleppmann F-MK-2 (Rekor) + F-MK-1 (rollback)
**The defect:** AC-2 claims "append-only event log; never in-place SKILL.md mutation" — but the plan never states the consistency property (linearizable? eventually consistent?). Three components (log + content-addressed store + best-pointer) interact without rules. (a) Local append-only and Rekor append-only are conflated; only the latter is actually one-way-door (Lamport). (b) Sigstore Rekor unavailability has no defined Refiner behavior; CISO invariant `rekor_log_index NOT NULL iff signing_mode='production'` becomes unrepresentable on partial failure (Kleppmann). (c) Rollback (revert) breaks append-only causality — `parent_version_id` cannot semantically distinguish `revert(v_bad)` from "new edit identical to ancestor" (Kleppmann). Signed Rekor row carries `actor` but not `intent`.
**Action:** Specify the consistency model. Add `version_kind: edit | revert | restore` to SkillVersion schema + paired pointer. Add `pending_production` intermediate state for Rekor-unavailable case. Define outbox-and-reconciler pattern.

### CONV-3 — SkillVersion / SkillSnapshot semantic clash (3 seats convergent)

**Severity: P0**
**Raised by:** Hickey F-RH-001 (P0), Lamport F-LL-05 (P2 — no state machine), Kleppmann F-MK-1 (causality)
**The defect:** Plan asserts SkillVersion is the 14th canonical entity, "extends/references" the existing SkillSnapshot. But both entities are immutable, content-addressed, with parent pointers. The plan defends the distinction in parenthetical ("NOT a duplicate") but never derives it. Shipping two entities for one concept in a `@intentsolutions/core@0.3.0` Rekor-signed kernel is a one-way-door defect.
**Action:** EITHER (a) make SkillVersion fully orthogonal — no FK to SkillSnapshot, lineage carried entirely within SkillVersion.parent_version_id (Internal-review architect P1-1 already raised this); OR (b) merge them at the schema level and surface "snapshot" vs "version" as a discriminator field. Decision belongs to an ISEDC ratification.

### CONV-4 — AC-12 tri-link spans 3 writer systems with no consistency model (2 seats convergent)

**Severity: P0**
**Raised by:** Hickey F-RH-002 (place-oriented), Kleppmann F-MK-3 (distributed consistency)
**The defect:** Tri-linkage discipline (AC-12 + § 3.5 PR-1 + verifier + D7 + bd-sync) stores the same `bead ↔ doc ↔ issue` fact in three writable places and runs CI to keep them in sync. (a) Textbook place-oriented programming; bd-sync mirror IS the acknowledgment that drift is expected (Hickey). (b) No consistency model named: at-least-once? linearizable? Out-of-band writers (humans editing GH directly), JSONL throttle interaction, comment dedup — all undefined (Kleppmann).
**Action:** Either (a) specify bd-as-linearizable-writer + idempotent comment UUIDs + write-order policy; OR (b) collapse to one source-of-truth and treat GH/Plane as PROJECTIONS (read-only views).

### CONV-5 — Phase D "deferred indefinitely" is unmanaged debt with wrong re-open triggers (2 seats convergent)

**Severity: P0**
**Raised by:** Karpathy F-AK-003, Cunningham F-WC-003
**The defect:** Plan defers Phase D (creator sub-product) with only two re-open triggers — both demand-signals ("external work demonstrates the bar can be cleared OR a partner explicitly asks"). Missing the UPSTREAM capability signal (frontier model release). "Deferred indefinitely at P3" is also three contradictory framings simultaneously — deferred / indefinitely / P3-priority (Cunningham). Not enumerated as a Blueprint A § 3 anti-goal.
**Action:** Either (a) ADD a quarterly "test the deferred bar" trigger + on-frontier-model-release trigger (Karpathy preference — keeps the option open at low cost); OR (b) UPGRADE to a Blueprint A anti-goal and remove from the plan entirely (Cunningham Path A). Decision belongs to ISEDC.

### CONV-6 — Null-hypothesis baseline missing from Phase A (2 seats convergent)

**Severity: P0**
**Raised by:** Karpathy F-AK-001, Beck F-KB-006
**The defect:** Plan § 12 sample finding F-AK-001 names this as a P1 — and then never inserts it into the Phase A roadmap. Plan budgets weeks to build propose/accept loop WITHOUT measuring "naive Opus one-shot with eval set as in-context examples" first. If the null hypothesis holds, Phase B is wasted engineering (Karpathy's bitter-lesson check). Beck reads this as Three Strikes inverted — the plan refactors on the FIRST hint of mechanism instead of waiting for the third.
**Action:** Insert Phase A.0 "Bitter-lesson baseline" — run eval set against un-refined skill with naive in-context augmentation. If lift > 70% of projected Phase A+B lift, descope. Hard gate Phase A on bitter-lesson result.

## Divergent findings (1 seat raised — kept verbatim, flagged for user judgment)

### F-KB-001 (Beck) — Phase budgets ("~1 week", "~2 weeks") are decoration without a bandwidth model

**P0** — Plan v4.1's revision note acknowledges this gap but doesn't fix it. § 11 punts to a future "actual durations depend on bandwidth." That punt IS the defect (Beck). Same finding was raised in AAR-023 and not addressed.

### F-KB-003 (Beck) — § 13 Step 7 "Hard gate" is honor-system

**P0** — Plan says "no `bd claim` against any Skill Refiner bead until Plan Audit § 12 STATUS.md = RATIFIED." But there is no `bd` enforcement, no CI gate, no hook. Every other gate in the plan has machine enforcement (validate-trilink CI, escape-scan, etc.). Beck: "Make the change easy, then make the easy change."

### F-AK-002 (Karpathy) — AC-7 "mechanism swappable" claim un-operationalized

**P0** — AC-7 explicitly invokes the Karpathy seat ("Karpathy bitter-lesson check") but the plan defines NO `RefinerStrategy` interface, NO second strategy implementation, NO swap exercise. The claim launders the seat's name without earning it.

### F-RH-003 (Hickey) — § 12 contains six pre-written "Sample findings" attributed to six of the seven seats

**P0** — README excluded the internal review from brief pack to avoid biasing seats; the plan defeats that at the source. The sample findings primed our actual findings (Karpathy F-AK-001 matches the sample F-AK-001 verbatim; that's evidence of bias).
**Note: this is METHODOLOGICALLY recursive — it's a defect this audit itself partially demonstrates.** Hickey explicitly notes this.

### F-CH-001 (Huyen) — Eval-set lineage / versioning / refresh cadence absent from Phase A

**P0** — EvalSet value type has `eval_set_hash` but no version, lineage_parent, refresh_due_at, or deprecation policy. Deferred to Phase F (Q3 2026) — meaning the FIRST refiner pass runs against an un-versioned eval set with no drift detection.

### F-WC-003 (Cunningham) — already covered by CONV-5 above

## Cross-seat tensions (require user arbitration)

### TENSION-1 — SkillVersion / SkillSnapshot resolution path

**Hickey** (CONV-3): merge entities OR formally distinguish.
**Kleppmann** (F-MK-1): keep separate but add `version_kind` discriminator + rollback semantics.
**Lamport** (F-LL-05): add state machine.
**Internal-review architect** (P1-1 from 2026-05-27): "make SkillVersion fully orthogonal — no FK."
**Tension:** Hickey wants ONE entity (simpler); Kleppmann wants TWO entities with richer state; architect wants TWO with no relationship. User must arbitrate the schema-design call.

### TENSION-2 — Phase D resolution path

**Karpathy** (CONV-5): keep the option open with quarterly + on-release re-measurement.
**Cunningham** (CONV-5 + F-WC-003): upgrade to anti-goal and remove from the plan.
**Tension:** Karpathy preserves optionality; Cunningham eliminates ambiguity. User must arbitrate the product-axis call.

### TENSION-3 — Process-discipline weight (Cunningham + Hickey)

**Cunningham F-WC-002:** 7 parallel process disciplines without unifying abstraction = accumulating debt.
**Hickey F-RH-002:** the discipline IS the place-oriented complexity.
**Tension:** Cunningham wants the discipline simplified into 1-2 abstractions; Hickey would eliminate AC-12 entirely. Both push toward simplification but with different stopping points.

## Recommendation to user

7/7 seats: **AMEND**. 17 P0 BLOCKERs + 15 P1 CRITICALs. The plan is **architecturally salvageable** — no seat called for RE-DRAFT — but cannot proceed to first `bd claim` without addressing the convergent findings (CONV-1 through CONV-6).

Per § 12 Phase 4 methodology: "If P0 findings or unresolved seat-tensions exist → convene ISEDC session for adversarial ratification, producing an AT-DECR record."

Three cross-seat tensions exist (above). **Recommend convening ISEDC Session 7 (Skill Refiner plan ratification) to arbitrate the three tensions and ratify the CONV-1 through CONV-6 remediations as binding.** Without ratification, the next plan iteration (v5) lands as a one-author decision again — which itself is the F-RH-003 / F-LL-07 / circular-audit defect.

Alternative path: **user directly arbitrates the 3 tensions + authorizes the 6 convergent remediations**, plan v5 lands as an inline amendment, no ISEDC. This is faster but does not address the "single-author / circular-audit" finding.

CTO call deferred to user.

— Claude (acting CTO)
2026-05-27
