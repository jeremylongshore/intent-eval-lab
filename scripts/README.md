# Reusable scripts

This directory contains deterministic checks used by the lab and its sibling
repositories. The checks are intentionally offline-first so a CI runner does
not need the umbrella beads database.

## `bd-claim-precheck.sh`

The script is the machine-enforced P0-RATIFY-4 gate for Skill Refiner beads.
It reads the plan-audit `STATUS.md`, validates the bead identifier, looks up
the bead through `bd show`, and fails closed when the plan state or lookup is
unsafe.

Local use from the lab checkout:

```bash
bash scripts/bd-claim-precheck.sh bd_000-projects-xxxx
bash scripts/bd-claim-precheck.sh --self-test
```

The `--self-test` path is hermetic and covers RATIFIED, OPEN,
RATIFIED-WITH-DELTAS, non-refiner, missing-status, lookup-failure, and
injection cases. A real local claim wrapper must run the bead-id path before
`bd update <id> --claim`; CI cannot replace that local hard gate.

## Cross-repo CI contract

`.github/workflows/claim-precheck-reusable.yml` is the canonical CI adapter.
The five convergence repositories call it from their own workflow files and
pin both the reusable workflow ref and the `gate_ref` input to full commit
SHAs. Update those pins together when this script or reusable workflow changes.

Internal pull requests and pushes run the self-test as a hard check. A pull
request whose head repository differs from the base repository is an external
contributor PR: the same self-test runs in advisory mode, emits a warning on
failure, and asks for this exact line in the PR body:

```text
contributor-acknowledgment: bd-claim-precheck
```

The acknowledgment is a maintainer-facing requirement and is intentionally a
warning rather than a merge block, per DR-028's VP DevRel binding. The
workflow uses `pull_request`, never `pull_request_target`, and grants only
read access so fork code cannot receive write credentials.

## `bd-sync`

The canonical, reviewed source for the cross-repository synchronizer is
[`bd-sync.sh`](./bd-sync.sh). The installed operator command is
`~/bin/bd-sync`; after reviewing a change, install the exact tracked script
with:

```bash
install -m 0755 intent-eval-platform/intent-eval-lab/scripts/bd-sync.sh ~/bin/bd-sync
```

Run it from the umbrella beads workspace (`~/000-projects`) so the command
resolves the shared bead database. Plane remains a projection for comments and
state; cross-reference facts are written in beads and projected outward.

### Guarded cross-reference projection

```bash
bd-sync project bd_000-projects-xxxx
bd-sync project bd_000-projects-xxxx --dry-run
bd-sync project bd_000-projects-xxxx --repo-root /path/to/worktree
```

The command reads explicit `Doc:` and `GitHub:` fields from the bead. It
renders only the versioned block between:

```text
<!-- BEGIN BD-SYNC:cross-ref:v1 -->
<!-- END BD-SYNC:cross-ref:v1 -->
```

The first run appends the GitHub block or inserts the document block after
YAML front matter. Later runs are idempotent. When several beads share one
document, the guarded document block aggregates their `Beads:` and `GitHub:`
refs instead of replacing an earlier receipt. If either marker is partial,
duplicated, reordered, or the block content differs from the deterministic
renderer, `bd-sync project` reports an `ANOMALY` and writes neither surface.
Human-owned prose outside the markers is preserved.

The authority is DR-028 T3, recorded in
`000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`.
The historical parent-bead path for `030-AT-STND-tri-linkage-discipline.md`
is stale and absent from the current lab history; it is not recreated or used
as authority.

### Offline self-test

The projection fixtures do not use GitHub, Plane, or provider credentials:

```bash
scripts/bd-sync.sh projection-self-test
scripts/tests/test-bd-sync-project.sh
shellcheck scripts/bd-sync.sh
```

The verifier keeps bead-side presence blocking and reports GitHub/document
projection observations as advisory because `bd-sync project` is the guarded
writer for those surfaces:

```bash
scripts/validate-trilink.sh
```
