# SAK Index

**Beads:** `bd_000-projects-ho6o`

The single canonical entry point for the Spec Authority Kernel (SAK). Start here,
then follow the read order below. Keep this file ≤ 2 pages — it is a map, not the
territory.

## What

Spec Authority Kernel — kernel-canonical authoring schemas for the agent-native
authoring contracts (skill / plugin / agent / mcp / hook / marketplace). The
kernel (`@intentsolutions/core`, `schemas/authoring/v1/`) is the single internal
source of truth for "what is a valid agent-native artifact." It feeds the CCP
validator, the internal SKILL.md validators, and j-rig, and stays continuously
adherent to upstream (agentskills.io + Claude/Anthropic official surfaces + the
MCP spec).

## Why

Before the SAK, "what is a valid artifact" was duplicated across a hand-rolled CCP
validator, several SKILL.md validators, and j-rig — each drifting independently
from upstream. The SAK collapses those into one kernel schema set that every
consumer reads from, with continuity machinery (drift-watch + field-diff +
watcher-liveness) so the kernel tracks upstream rather than rotting. Rationale:
plan 031 (`031-PP-PLAN-skill-refiner-sak-amendment-v6-2026-05-28.md`) § 14.1.

## Status

Phase: incremental rollout (walking skeleton landed — `skill-frontmatter`
base + overlay + composition). State: ADVISORY (pre Phase 4c flip). The
machine-rendered dashboard `SAK-DASHBOARD.md` (auto-generated, root-level) is the
live phase/state pointer once it lands (bead `iel-sak-dashboard`); until then this
Status line is the manual pointer.

## Where things live

| Concern         | Path                                                                                    |
| --------------- | --------------------------------------------------------------------------------------- |
| Plan amendment  | `031-PP-PLAN-skill-refiner-sak-amendment-v6-2026-05-28.md` (v6 intro) + `033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md` (v7 audit-closure) |
| Charter         | `032-AT-DECR-isedc-class-1-charter-spec-authority-kernel-draft-2026-05-28.md` (DRAFT) → ratified `044-AT-DECR-isedc-council-session-8-sak-charter-2026-06-09.md` |
| Audit synthesis | `audit/2026-05-28-sak-incremental-audit/synthesis.md`                                   |
| SSoT declaration | `045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md`       |
| Governance      | `046-AT-STND-sak-governance-owners.md`                                                   |
| Dashboard       | `SAK-DASHBOARD.md` (auto-generated; planned — bead `iel-sak-dashboard`)                  |
| Kernel schemas  | `../../intent-eval-core/schemas/authoring/v1/`                                           |
| Coverage map    | `intent-eval-core` `schemas/authoring/v1/6767h-coverage-map.json` (planned — bead `iec-E11-coverage-map`) |
| 6767-h prose    | `claude-code-plugins` `000-docs/6767-h-*.md` (planned — coupling to the 6767 standard series) |
| Beads (filter)  | `bd list --label sak --label refiner`                                                   |

## Read order (for engineers)

1. `SAK-INDEX.md` (this file)
2. `SAK-DASHBOARD.md` (current state — once it lands)
3. `045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md` (the SSoT declaration + continuity machinery)
4. `031-PP-PLAN-skill-refiner-sak-amendment-v6-2026-05-28.md` § 14 (architecture)
5. `033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md` (v7 audit-closure — this file's sibling rationale)

## Read order (for ISEDC seats)

1. `SAK-INDEX.md` (this file)
2. `032-AT-DECR-isedc-class-1-charter-spec-authority-kernel-draft-2026-05-28.md` (charter draft) → `044-AT-DECR-isedc-council-session-8-sak-charter-2026-06-09.md` (ratification)
3. `audit/2026-05-28-sak-incremental-audit/synthesis.md` (audit synthesis)
4. `046-AT-STND-sak-governance-owners.md` (seat-bound owner map)
