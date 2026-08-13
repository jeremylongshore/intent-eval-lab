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
