---
title: bd-sync Cross-Reference Generator — Projection Contract
date: 2026-08-01
status: NORMATIVE
authority: DR-028 T3 — bd is the canonical writer; GitHub and documents are projections
---

<!-- BEGIN BD-SYNC:cross-ref:v1 -->

Beads: `bd_000-projects-rqwk.8.1`
GitHub: `jeremylongshore/intent-eval-lab#266`
Projection-SHA256: 4f70d7d94a90f4307e8b5454a5f7243690a2c7e98c3c9f825b71135708cfd639

<!-- END BD-SYNC:cross-ref:v1 -->

# bd-sync Cross-Reference Generator

This document specifies the guarded cross-reference projection emitted by the
versioned `project` command in `bd-sync`. The bead is the source of truth. The
generated block is deliberately narrow so the surrounding document remains
human-owned and reviewable.

## Authority and correction

The binding decision is DR-028 T3 in
`000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`.
The parent coordination bead contains an older path for a tri-link standard
that is absent from the current lab history. That path is recorded as stale
metadata; this document is the current operational contract.

## Projection contract

`bd-sync project <bead>` reads the bead's explicit `Doc:` and `GitHub:` fields.
It renders a versioned block between the `BD-SYNC:cross-ref:v1` markers into
each linked GitHub issue body and document front-matter. On a first run the
block is additive. Later runs replace nothing unless the existing block is
byte-for-byte equal to the deterministic renderer; a partial or edited block
is an anomaly and the command exits without writing either surface.

The command preflights every linked issue and document before performing a
remote or local write. GitHub bodies retain their human-owned context. Local
document writes are atomic, and a failed local write triggers a best-effort
rollback of any GitHub projection written in the same invocation.

## Operational rules

1. Edit cross-reference facts in the bead, then run `bd-sync project <bead>`.
2. Do not hand-edit text between the generated markers. A correction belongs
   in the bead and must be re-projected.
3. Use `--dry-run` and `--repo-root` when reviewing a worktree before install.
4. The tri-link verifier keeps bead-side presence blocking; GitHub/document
   presence is an advisory observation of this generator's output.

## Test contract

The deterministic fixture suite lives under
`/scripts/tests/fixtures/bd-sync/` and runs without GitHub, Plane, or provider
credentials:

```bash
scripts/bd-sync.sh projection-self-test
```
