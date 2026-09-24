---
title: SAK Phase-4 advisory→blocking flip state machine — schema + transition emit/validation
category: AT-SPEC
status: NORMATIVE
date: 2026-06-20
authority: plan 033 v7 § 14.4.shadow + § 14.4c; plan 048 v8 Delta 3 + § 14.31
---

# SAK Phase-4 advisory→blocking flip state machine

**Status: NORMATIVE.** Formalizes the Phase-4 advisory→blocking flip lifecycle (plan 033 v7
§ 14.4.shadow, § 14.4c; plan 048 v8 Delta 3, § 14.31) into a machine-checkable artifact: a JSON
Schema for `SAK-STATE.json` plus a transition emit/validation module that enforces the legal
transitions and the per-flip precondition gates. This is **distinct** from the 13-entity runtime
state machine at `specs/state-machines/transition-table.v1.json` (Blueprint B) — that one is the
per-entity runtime lifecycle, gated by `statemachine-drift.yml`. This one is the SAK Phase-4
**flip lifecycle**, gated by the new `sak-state-machine.py --self-test --validate` CI step.

## Artifacts

| Artifact                                            | Role                                                                                                      |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `specs/state-machines/schema/sak-state.schema.json` | JSON Schema (draft-07) validating `SAK-STATE.json` — state enum, per-state preconditions, transition log. |
| `scripts/sak-state-machine.py`                      | Transition emit/validation module + `--self-test` + `--validate` + `--show` CLI. Import-safe, offline.    |
| `SAK-STATE.json` (root)                             | The hand-maintained state record the renderer + this machine both consume.                                |
| `scripts/tests/test_sak_state_machine.py`           | pytest unit suite (35 cases) for the module.                                                              |

Both the schema and the module are hash-pinned in `.harness-hash` (policy-enforcement surface,
same rationale as `classifier-walls.py`): a silent edit to the flip's hard gates or the
legal-transition graph is structurally blocked until a fresh `scripts/audit-harness init`.

## States (plan 033 § 14.4.shadow)

The eight lifecycle states, forward order:

`ADVISORY → ADVISORY-W-A → ADVISORY-W-AB → SHADOW-MODE → READY-TO-FLIP → BLOCKING`, with
`HOLDING` (audit branch off `SHADOW-MODE`) and `ROLLED-BACK` (reachable from the gated states).

- **ADVISORY** — default state; kernel schema runs advisory-only, never blocking.
- **ADVISORY-W-A** — wave A (deterministic `batch-remediate`) merged.
- **ADVISORY-W-AB** — wave B (Refiner eval-loop) done; both waves complete.
- **SHADOW-MODE** — dual-validator shadow (CCP validator + kernel-schema validator) running; deviations measured.
- **HOLDING** — audit branch: open-P0 deviations route here from `SHADOW-MODE`; its only exit is back to `SHADOW-MODE`. It can **never** flip directly to `BLOCKING`.
- **READY-TO-FLIP** — all dispositions resolved, no open P0; awaiting governance sign-off.
- **BLOCKING** — flip complete; PR-blocking starts.
- **ROLLED-BACK** — a gated-state failure was hit; returns to `SHADOW-MODE` for re-attempt.

## Legal transitions

| From            | Event                     | To              | Gate                                               |
| --------------- | ------------------------- | --------------- | -------------------------------------------------- |
| `ADVISORY`      | `wave-a-merged`           | `ADVISORY-W-A`  | —                                                  |
| `ADVISORY-W-A`  | `wave-b-done`             | `ADVISORY-W-AB` | —                                                  |
| `ADVISORY-W-A`  | `wave-a-failure`          | `ROLLED-BACK`   | rollback (§ 14.4.rollback class 1)                 |
| `ADVISORY-W-AB` | `enable-shadow`           | `SHADOW-MODE`   | —                                                  |
| `ADVISORY-W-AB` | `wave-b-failure`          | `ROLLED-BACK`   | rollback (§ 14.4.rollback class 2)                 |
| `SHADOW-MODE`   | `dispositions-resolved`   | `READY-TO-FLIP` | requires `open_p0_count == 0`                      |
| `SHADOW-MODE`   | `deviations-open-p0`      | `HOLDING`       | open-P0 deviations route to audit, not to the flip |
| `HOLDING`       | `audit-cleared`           | `SHADOW-MODE`   | —                                                  |
| `READY-TO-FLIP` | `governance-triple-signs` | `BLOCKING`      | **HARD-GATED** — see flip preconditions            |
| `BLOCKING`      | `regression-detected`     | `ROLLED-BACK`   | rollback (§ 14.4.rollback class 3)                 |
| `ROLLED-BACK`   | `back-to-shadow`          | `SHADOW-MODE`   | —                                                  |

Any `(from, event)` pair not in this table is an **illegal transition** and is rejected with a
reason listing the legal events from the current state.

## Flip precondition gates (plan 048 v8 Delta 3)

The `READY-TO-FLIP → BLOCKING` transition is the highest-blast-radius event in SAK. Its
preconditions are **not equal in override-ability**:

- **(a) coverage ≥ 99.5% corpus pass** — the ONLY precondition the 30-day calendar ceiling can
  disposition. A flip below the floor is permitted **only** when the caller passes
  `allow_calendar_ceiling=True`, which quarantines the remaining < 0.5% of files (advisory-only,
  never blocking).
- **(c) zero open P0** — **HARD gate.** The flip cannot fire with any open P0 in the
  schema-revision-candidates queue (§ 14.A.3). The calendar ceiling **never** overrides this.
- **(d) governance triple sign-off** — **HARD gate.** All three of CTO + CISO + VP DevRel
  (§ 14.12) must be present. The calendar ceiling **never** overrides this.
- **(b) shadow window ≥ 7 days at deviation < 0.5%** (§ 14.4b.5) — surfaced as a rejection reason
  when clearly unmet; advisory relative to (c)/(d).

The module enforces (c) and (d) as absolute and (a) as calendar-dispositionable, exactly matching
Delta 3's "governance + correctness gates are absolute; the calendar ceiling only caps
coverage-quorum stall."

## Rollback semantics (plan 033 § 14.4.rollback)

`ROLLED-BACK` is reachable from each of the three gated states (`ADVISORY-W-A`, `ADVISORY-W-AB`,
`BLOCKING`) and returns to `SHADOW-MODE` ("back to SHADOW" in the § 14.4.shadow diagram). The
`emit()` API records a `reason` and an optional `decision_record_ref` on each transition so a
rollback carries its AT-DECR pointer in the append-only `transition_history`. (Evidence-Bundle
snapshot semantics during rollback — the `signing_mode: rolled-back-superseded` superseding event,
never Rekor mutation — are out of scope for this state machine and remain owned by the
kernel-side emitter per § 14.4.rollback class 3.)

## Bounded design choices (where the plan is under-specified)

1. **`HOLDING` is modeled** even though the prompt brief names only a 5-state subset. The
   canonical § 14.4.shadow diagram has it as the audit branch off `SHADOW-MODE`; modeling it keeps
   the machine faithful to the diagram. Its only exit is `audit-cleared → SHADOW-MODE`.
2. **`SHADOW-MODE → READY-TO-FLIP` requires `open_p0_count == 0`.** The diagram routes open-P0
   deviations to `HOLDING`; the machine enforces that an open P0 blocks `dispositions-resolved`.
3. **Governance sign-off source is STUBBED behind one seam** (`load_signoff_from_state()`). Until a
   live governance-signoff source exists (an ISEDC AT-DECR ledger / signing service), the three
   booleans are read from `SAK-STATE.json`'s `state_machine.preconditions.governance_signoff`,
   defaulting to all-false. Replacing that single function is the only change a real source needs.

## CI gate

`ci.yml` "Validate specs and docs" runs:

```bash
python3 scripts/sak-state-machine.py --self-test    # legal/illegal/precondition/rollback/emit
python3 scripts/sak-state-machine.py --validate     # committed SAK-STATE.json satisfies the schema
```

The pytest suite at `scripts/tests/test_sak_state_machine.py` (collected via the `scripts/tests`
testpath) covers the same matrix at unit granularity.

— Jeremy Longshore
intentsolutions.io
