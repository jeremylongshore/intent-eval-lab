---
title: SAK Wave-B durability protocol — per-file branch + atomic commit + 3-retry-with-escalation + parked-queue integration
category: AT-SPEC
status: NORMATIVE
date: 2026-06-20
authority: plan 033 v7 § 14.17.1 + § 14.17.2; plan 048 v8 Delta 1 + § 14.17
---

# SAK Wave-B durability protocol

**Status: NORMATIVE.** The **durability half** of the Wave-B (Refiner / eval-loop) wave of the
Phase-4 SAK corpus migration — the "side-branch + atomic + 3-retry + parked-queue" mechanism of
**F-MK-004**. Wave B refines one SKILL.md file at a time; this protocol makes each file's
refinement **durable and recoverable** so a failure **parks** the file (re-enqueueable) instead of
silently dropping it. It composes two normative authorities: plan 033 v7 § 14.17.1 (per-file branch
plus atomic commit) and § 14.17.2 (the 3-retry ladder, then escalate), together with plan 048 v8
Delta 1 ("Wave B never on open-PR files") and § 14.17 ("parked ≠ failed").

This is **distinct** from `scripts/sak-reconciliation-queue.py` — that is the **single parked
queue** (Wave A residue + Wave B parked, four monthly-review dispositions, the merge-gate /
wave-B-park predicates). This protocol **routes into** that one queue; it does **not** build a
second one. It is also distinct from the SAK Phase-4 flip state machine (`sak-state/v1`,
092-AT-SPEC) and its rollback protocol (093-AT-SPEC).

## Artifacts

| Artifact                                                        | Role                                                                                                                                                                                                                                     |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `specs/state-machines/schema/sak-wave-b-durability.schema.json` | JSON Schema (draft-07) validating `SAK-WAVE-B-DURABILITY.json` — the per-file record, the lifecycle states, the branch-name pattern, the attempt counter, the atomic-commit flag.                                                        |
| `scripts/sak-wave-b-durability.py`                              | The durability protocol: deterministic branch model, the atomic-commit lifecycle, the 3-retry-with-escalation ladder, the open-PR park, and the parked-queue routing. `--self-test` + `--validate` + `--show` CLI. Import-safe, offline. |
| `SAK-WAVE-B-DURABILITY.json` (root)                             | The committed durability record (illustrative seed rows — one per terminal outcome). Hand-maintained / generated upstream; the module reads + reasons, never mutates it.                                                                 |
| `scripts/tests/test_sak_wave_b_durability.py`                   | pytest unit suite (31 cases) for the module.                                                                                                                                                                                             |

Both the schema and the module are hash-pinned in `.harness-hash` (policy-enforcement surface, same
rationale as `sak-reconciliation-queue.py` + `sak-state-machine.py`): a silent edit to the
atomic-commit invariant, the escalation rule, the branch derivation, or the parked-queue routing is
structurally blocked until a fresh `scripts/audit-harness init`.

## What this models vs. what it does not do

This script models the durability-protocol **decisions** as state — exactly as the sibling scripts
model decisions, not side effects. The actual git/GitHub operations (checkout, commit, open PR,
working-tree rollback) are downstream and isolated behind a **single stub seam**
(`RefinerAttemptSource`), mirroring how the reconciliation queue isolates the GitHub open-PR state
(`GitHubPrStateSource`) and the flip state machine isolates the governance sign-off
(`load_signoff_from_state`). **This module decides; it does not execute.**

## The per-file branch model (plan 033 § 14.17.1)

Each file is refined on its own branch, named **deterministically from the path**:

```text
refiner/wave-b/<sha256(path)[:12]>
```

Path-derivation (not content-derivation) is load-bearing for **recoverability**: the dispatcher can
address a file's branch without reading its content, and two runs over the same path produce the
**same** branch. `branch_name(path)` is the single source of the name; `from_state()` re-derives and
**rejects** any record whose stored branch does not match.

## The atomic-commit invariant (the load-bearing durability guarantee)

A Wave-B result for a file is **either fully committed** (exactly one commit on the per-file branch)
**or not at all** (no commit, working tree rolled back) — **never a partial state**. The lifecycle
makes `IN-FLIGHT` a distinct, non-terminal state, and every terminal state asserts the invariant:

| State              | Commits | Meaning                                                                              |
| ------------------ | ------- | ------------------------------------------------------------------------------------ |
| `PENDING`          | 0       | Registered, awaiting (or between) attempts.                                          |
| `IN-FLIGHT`        | 0       | An attempt is being applied (transient).                                             |
| `COMMITTED`        | **1**   | Accepted edit landed as exactly one atomic commit (records run-ID + cost + score-Δ). |
| `PARKED-OPEN-PR`   | 0       | Parked before any attempt — the file has an open PR (plan 048 Delta 1).              |
| `ESCALATED-PARKED` | 0       | The 3-retry ladder was exhausted; escalated to manual review.                        |

`assert_atomic()` enforces it in code (`COMMITTED ⇔ committed is True ⇔ commit_count() == 1`;
otherwise both False/0). A failed attempt never commits; only an accepted attempt commits, exactly
once. The schema documents the cross-field rule, and `from_state()` enforces it on load — a tampered
partial state (`COMMITTED` with `committed: false`, or `PENDING` with a commit) is rejected.

## The 3-retry-with-escalation ladder (plan 033 § 14.17.2)

For each file, the attempt counter walks the ladder; a failure rolls the working tree back to
`PENDING` (no commit) for the next attempt:

| Attempt | Refiner config           | On failure                                            |
| ------- | ------------------------ | ----------------------------------------------------- |
| 1       | `sonnet-default`         | retry (counter → 1)                                   |
| 2       | `sonnet-adjusted-prompt` | retry with a prompt clarifying the failure mode (→ 2) |
| 3       | `opus`                   | **ESCALATE** → `ESCALATED-PARKED` (counter = 3)       |

The 3rd failure **escalates** — the file is routed to the parked queue with an escalation reason
(the last failure mode) **rather than silently dropped**. An accepted attempt at any rung lands
`COMMITTED` immediately.

## The open-PR park (plan 048 v8 Delta 1)

Wave B **never runs on a file with an open PR**. Such a file is parked **before any attempt**
(`park_open_pr`, legal only from `PENDING`) → `PARKED-OPEN-PR`, with no attempt made and no commit
produced. It is re-enqueued by the reconciliation queue when the PR merges or closes.

## Parked-queue integration — the ONE reconciliation queue ("parked ≠ failed")

Both terminal park states (`PARKED-OPEN-PR` + `ESCALATED-PARKED`) route into the **single**
reconciliation queue, **reusing that module's own structures** — `FileState`, `QueueItem`,
`is_wave_b_park_eligible`, `wave_b_parked` — rather than re-implementing a second queue:

- `to_reconciliation_items(srq, target_version=...)` builds a `wave-b-parked` `QueueItem` per parked
  file, with `wave_b_parked=True` (the rule-3 park flag) so the queue's own predicates see it.
  Open-PR-parked files set `open_pr_state=open` (the queue can clear them on PR close); escalated
  files set `open_pr_state=none` (no PR — they wait for manual review). The escalation/park reason
  becomes the item note (audit trail).
- `route_parked_to_queue(srq, queue, target_version=...)` enqueues each parked file into the given
  queue, **skipping any path already present** — re-routing is idempotent. **Parked ≠ failed:** a
  parked item is re-enqueued, not lost; the reconciliation queue's `refresh_open_pr_state` clears
  the park flag when the PR closes (the re-enqueue path).

`PARKED_SOURCE` is asserted to be a real reconciliation-queue source in the self-test, so the two
modules stay in lock-step (no divergent vocabulary).

## CI wiring + test matrix

Wired into `ci.yml`'s required **"Validate specs and docs"** job:

```bash
python3 scripts/sak-wave-b-durability.py --self-test   # offline, deterministic
python3 scripts/sak-wave-b-durability.py --validate    # committed state ⊨ schema
```

The 31-case pytest suite at `scripts/tests/test_sak_wave_b_durability.py` covers: branch-name
determinism (same path → same branch; different → different); the retry counter incrementing +
escalating on the 3rd failure to the parked queue with a reason; the atomic-commit invariant (no
partial state — including the reject-then-accept-on-a-later-rung path); a parked item recoverable /
re-enqueued (not failed); an open-PR file parked, not attempted; the parked-queue routing into the
real reconciliation queue (with idempotence); and the JSON round-trip + schema validation (plus a
negative case proving the schema rejects an out-of-enum state).

— Jeremy Longshore
intentsolutions.io
