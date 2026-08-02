# Reusable lab scripts

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
