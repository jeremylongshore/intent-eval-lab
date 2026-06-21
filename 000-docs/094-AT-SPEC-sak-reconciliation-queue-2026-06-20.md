---
title: SAK reconciliation queue — Wave A residue + Wave B parked, 4 dispositions + real-time enforcement
category: AT-SPEC
status: NORMATIVE
date: 2026-06-20
authority: plan 033 v7 § 14.17.3; plan 048 v8 Delta 1.1
---

# SAK reconciliation queue

**Status: NORMATIVE.** Implements the SINGLE reconciliation queue shared between **Wave A residue**
(files with WARN-level open issues after the mechanical `batch-remediate`) and the **Wave B parked
queue** (files the Refiner could not migrate after the § 14.17.2 3-retry ladder). It composes two
normative authorities: plan 033 v7 § 14.17.3 (the original **monthly-review disposition** queue with
the four dispositions) and plan 048 v8 Delta 1.1 (which **extends — does not replace** — § 14.17.3
with a **real-time enforcement** capability). The monthly-review disposition function is unchanged
and runs **alongside** the real-time enforcement.

This is **distinct** from `scripts/reconciliation-liveness.py` — that is the advisory
≤5-business-day reconciliation **liveness SLA timer** (090-AT-SPEC § 5 / plan 033 § 14.16.2). This
spec is the reconciliation **queue data structure + disposition logic + the two real-time
enforcement predicates**. Different artifact.

## Artifacts

| Artifact                                                           | Role                                                                                                                                                                              |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `specs/state-machines/schema/sak-reconciliation-queue.schema.json` | JSON Schema (draft-07) validating `SAK-RECONCILIATION-QUEUE.json` — source enum, per-file state record, the four dispositions.                                                    |
| `scripts/sak-reconciliation-queue.py`                              | The queue data structure + enqueue/dequeue + disposition assignment + the merge-gate / wave-B-park predicates. `--self-test` + `--validate` + `--show` CLI. Import-safe, offline. |
| `SAK-RECONCILIATION-QUEUE.json` (root)                             | The committed queue record (illustrative seed rows). Hand-maintained / generated upstream; the module reads + reasons, never mutates it.                                          |
| `scripts/tests/test_sak_reconciliation_queue.py`                   | pytest unit suite (28 cases) for the module.                                                                                                                                      |

Both the schema and the module are hash-pinned in `.harness-hash` (policy-enforcement surface, same
rationale as `sak-state-machine.py` + `classifier-walls.py`): a silent edit to the merge-gate
predicate, the wave-B-park predicate, or the four-disposition vocabulary is structurally blocked
until a fresh `scripts/audit-harness init`.

## The shared queue (plan 033 § 14.17.3)

Wave A residue + Wave B parked share **one** queue, keyed on file path (at most one item per path),
preserving enqueue order. Each item carries:

- **`source`** — `wave-a-residue` or `wave-b-parked` (the two streams that share the one queue).
- **`file_state`** — the per-file real-time state record (below).
- **`disposition`** — `pending` (default) or one of the four real dispositions (below).

## The four dispositions (the monthly-review function, plan 033 § 14.17.3)

Reviewed at SAK AAR cadence (§ 14.13.2). `assign_disposition()` moves an item **off** `pending`
into one of:

| Disposition                 | Action                                                                                                      |
| --------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `keep-as-is`                | File stays valid at a lower tier (e.g. open-standard but not IS-marketplace); recorded in the coverage map. |
| `manual-migrate`            | Engineer manually edits; file lands in the next batch.                                                      |
| `deprecate-skill`           | Skill marked for removal in the next CCP minor; consumers warned.                                           |
| `schema-revision-candidate` | Routed to the § 14.A.3 schema-revision-candidates queue; the schema may need revision.                      |

`pending` is a sentinel, not a real disposition — `assign_disposition()` refuses it (the review
moves items off pending, never back onto it).

## The per-file state record (plan 048 v8 Delta 1.1)

Each tracked file carries `{ open_pr_state, wave_a_pending, wave_b_parked, target_version }`:

- **`open_pr_state`** (`open` | `none`) — refreshed from `gh pr list --search "<path>"` on every
  queue tick + the GitHub `pull_request` opened/closed webhook. The GitHub-state source is isolated
  behind a single **stub seam** (`GitHubPrStateSource`) a real `gh` adapter replaces.
- **`wave_a_pending`** (bool) — a queued, un-landed wave-A op exists for the file.
- **`wave_b_parked`** (bool) — the wave-B dispatcher skipped + parked the file (it had an open PR).
- **`target_version`** — the pinned `LATEST_PHASE_4_VERSION` (plan 048 v8 Delta 1); authors never
  chase a moving schema.

## The two real-time enforcement predicates

Both are **pure predicates over the queue state**. The actual GitHub/CI wiring is downstream.

### Merge-gate — `blocks_pr_merge(path)` (rule-2 mechanism)

A file with `wave_a_pending == True` **blocks its own PR merge**. This is the `sak-wave-a-precedence`
required CI check: RED iff this predicate is True. A contributor PR touching the file cannot merge
until wave A lands and `clear_wave_a_pending(path)` flips the gate GREEN. An un-queued path never
blocks (no wave-A op is pending for it).

**Wave-B PR exemption (stated invariant, plan 048 v8 Delta 1.1).** Wave-B Refiner PRs are
exempt-by-construction: wave A always precedes wave B for a given file, so a wave-B-eligible file
never has `wave_a_pending` set. The gate keys on that flag, so the invariant holds with no carve-out.

### Wave-B park — `is_wave_b_park_eligible(path)` (rule-3 mechanism)

The wave-B (Refiner) dispatcher must **skip — park** — any file with `open_pr_state == open`, set
`wave_b_parked = True`, and emit no Refiner op. The `pull_request:closed` webhook (merged **or**
closed) clears the park flag and re-enqueues the file. **Parked ≠ failed** (composes with § 14.17
durability). `refresh_open_pr_state(source)` composes the full park lifecycle: it sets the park flag
for a newly-open file and clears it for a newly-closed one. It deliberately does **not** touch
`wave_a_pending` — only wave A landing clears that flag. The two orderings are independent.

## Queries

`parked()`, `pending_disposition()`, `dispositioned()`, `blocking_pr_merge()`, `by_source()`,
`by_disposition()` — the brief's "what's parked", "what's pending disposition", "what blocks PR
merge".

## CI wiring + test matrix

Wired into `ci.yml`'s required **"Validate specs and docs"** job:

```bash
python3 scripts/sak-reconciliation-queue.py --self-test   # offline, deterministic
python3 scripts/sak-reconciliation-queue.py --validate    # committed queue ⊨ schema
```

The 28-case pytest suite at `scripts/tests/test_sak_reconciliation_queue.py` covers: enqueue from
both sources into the one queue; each of the four dispositions assignable + queryable; the merge-gate
predicate RED for `wave_a_pending` and GREEN otherwise (+ the cleared transition); the wave-B-park
predicate for an open-PR file (+ the refresh lifecycle); pending-vs-dispositioned filtering; the JSON
round-trip + schema validation (and a negative case proving the schema rejects an out-of-enum
disposition).

— Jeremy Longshore
intentsolutions.io
