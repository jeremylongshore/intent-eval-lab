---
title: SAK Phase-4c rollback protocol — kernel-gate-revert + governance-triple sign-off + 7-day retrospective
category: AT-SPEC
status: NORMATIVE
date: 2026-06-20
authority: plan 033 v7 § 14.4.rollback class 3; plan 048 v8 § 14.4c / Delta 3
---

# SAK Phase-4c rollback protocol

**Status: NORMATIVE.** Formalizes the rollback half of the SAK advisory→blocking flip lifecycle
(plan 033 v7 § 14.4.rollback class 3; plan 048 v8 § 14.4c / Delta 3) into a machine-checkable
command: `kernel-gate-revert`. It reverts a SAK gate from a gated/`BLOCKING` state back toward
advisory by driving the Phase-4 state machine (092-AT-SPEC) to `ROLLED-BACK`, gated by the
governance triple (CTO + CISO + VP-DevRel) and stamping the ISEDC Class-2 retrospective deadline
(revert + 7 calendar days). This is the rollback counterpart to the flip the state machine already
gates — it does **not** reimplement any state/transition logic; the state machine remains the single
source of the legal-transition graph and the hard gates.

## Artifacts

| Artifact                                            | Role                                                                                                                                                                                                  |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/sak-kernel-gate-revert.py`                 | The `kernel-gate-revert` command: governance-triple gate + drive-to-`ROLLED-BACK` + 7-day retrospective stamp. `--self-test`, `--dry-run`, `--revert`, `--check-retrospective`. Import-safe, offline. |
| `scripts/sak-state-machine.py` (092-AT-SPEC)        | The engine. `kernel-gate-revert` reuses its `evaluate()` / `emit()` and its `load_signoff_from_state` sign-off seam.                                                                                  |
| `specs/state-machines/schema/sak-state.schema.json` | Extended with a `stateMachine.rollback` record (`$defs/rollbackRecord`) the revert command stamps; an emitted `ROLLED-BACK` state still schema-validates.                                             |
| `scripts/tests/test_sak_kernel_gate_revert.py`      | pytest unit suite (35 cases) for the command.                                                                                                                                                         |

## The revert flow (plan 033 § 14.4.rollback class 3)

Class 3 is the **post-flip regression** path: `BLOCKING` mode is breaking real PRs at high rate.
The governance triple authorizes a single `kernel-gate-revert <reason>` command, which:

1. **(a) Flips the gate back to advisory** — modeled here as driving the state machine to
   `ROLLED-BACK` via the existing `regression-detected` edge (`BLOCKING → ROLLED-BACK`). The
   command never re-declares that edge; it calls the engine's `emit()`, which deep-copies the
   state (input never mutated) and appends one `transition_history` entry.
2. **(b) Records a Decision Record** — the `AT-DECR-phase-4c-rollback-NNN` pointer is carried on
   both the transition record and the stamped `rollback.decision_record_ref`.
3. **(c) Marks the BLOCKING-window attestations `rolled-back-superseded`** — **out of scope for
   this command.** Per F-MK-005, Rekor is append-only; the superseding-envelope event is owned by
   the kernel-side emitter. This command records only the **intent** (`rollback.affected_window` +
   `rollback.superseding_signing_mode = "rolled-back-superseded"`) so the kernel emitter can act on
   it. It never touches Rekor.
4. **(d) Opens an ISEDC Class-2 retrospective within 7 calendar days** — stamped here as
   `rollback.retrospective_due_at = reverted_at + 7 calendar days`, tagged
   `retrospective_class = "ISEDC-Class-2"`.

`ROLLED-BACK` returns to `SHADOW-MODE` (`back-to-shadow`) for a re-attempt — that onward edge is the
state machine's, not this command's.

## The sign-off gate (plan 048 § 14.4c)

The revert is refused unless **all three** of CTO + CISO + VP-DevRel have signed off — the same
triple that authorizes the forward flip. A revert with any seat absent is rejected, and the rejection
**names the missing seats** (e.g. "missing: VP-DevRel"). Two independent gates must both pass:

1. **Governance triple** — read via the state machine's `load_signoff_from_state` seam (the same seam
   the flip uses), from `SAK-STATE.json`'s `state_machine.preconditions.governance_signoff`.
2. **Legal-transition check** — delegated to `ssm.evaluate(..., "regression-detected")`. A revert from
   a source state with no rollback edge (e.g. `ADVISORY`, `SHADOW-MODE`, `READY-TO-FLIP`, `HOLDING`,
   `ROLLED-BACK`) is rejected with the engine's own "illegal transition" reason — even with the full
   triple.

**Sign-off source is stubbed behind one seam** (the same seam the vyng Phase-4 work stubbed). A real
governance-signoff source — an ISEDC AT-DECR ledger or a signing service — replaces
`load_signoff_from_state` and nothing else. An optional `--signoff cto,ciso,vp_devrel` CLI flag is an
**offline override** for self-test / dry-run and for operators who carry the sign-off out of band;
absent it, the seam is the sole source.

## The retrospective deadline (plan 033 § 14.4.rollback class 3 (d))

On a successful revert the command stamps `rollback.retrospective_due_at = reverted_at + 7 calendar
days` (calendar-day arithmetic; a date-time `reverted_at` is truncated to its date). A companion
read-only check — `kernel-gate-revert --check-retrospective` — surfaces whether that deadline is past,
symmetric to how the detector-health (057-AT-SPEC) and reconciliation-liveness (090-AT-SPEC) scripts
surface overdue items:

- `OVERDUE` (exit 1) — `as_of` is strictly past `retrospective_due_at`; open the ISEDC Class-2
  retrospective now.
- `PENDING` (exit 0) — before or exactly on the deadline; `days_remaining` reported.
- `NONE` (exit 0) — no rollback recorded (the steady state; the committed `SAK-STATE.json` is in
  `ADVISORY` with no `rollback` block).

## Test matrix

| Case                                                                  | Expectation                                                         |
| --------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Revert with the full triple from `BLOCKING`                           | ALLOWED → `ROLLED-BACK`; `retrospective_due_at` = +7d; Class-2.     |
| Revert with CTO / CISO / VP-DevRel absent (each tested independently) | REJECTED; the missing seat named in the reason + `missing_signoff`. |
| Revert with zero sign-off                                             | REJECTED; all three named.                                          |
| Revert from an illegal source state (5 states, full triple)           | REJECTED with the engine's "illegal transition" reason.             |
| Retrospective overdue / pending / on-deadline / none                  | `OVERDUE` / `PENDING` (days remaining) / not overdue / `NONE`.      |
| Emitted `ROLLED-BACK` state (incl. the `rollback` block)              | Validates against `sak-state.schema.json`.                          |
| `perform_revert` non-mutating; empty reason refused                   | Input untouched; empty reason raises `RevertError`.                 |

## CI gate

`ci.yml` "Validate specs and docs" runs (alongside the 092 state-machine gate):

```bash
python3 scripts/sak-kernel-gate-revert.py --self-test            # governance gate + emit reuse + retrospective + schema
python3 scripts/sak-kernel-gate-revert.py --check-retrospective  # NONE in steady state -> exit 0
```

The pytest suite at `scripts/tests/test_sak_kernel_gate_revert.py` (collected via the `scripts/tests`
testpath) covers the same matrix at unit granularity.

— Jeremy Longshore
intentsolutions.io
