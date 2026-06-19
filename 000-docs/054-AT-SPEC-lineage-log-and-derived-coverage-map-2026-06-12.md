# 054 — Append-only lineage log + derived coverage map (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + three tiers) · **Epic:** 9k5h (GH intent-eval-lab#114)

The Kleppmann correction (045-RR-LAND § 4): the kernel's relationship to upstream is an **append-only event log**; the coverage map is a **derived projection** of that log — never a hand-maintained file. Implementation: `scripts/lineage-log.py` (append/verify/project), log at `specs/lineage/log.jsonl`, projection at `specs/lineage/coverage-map.json`.

## The key

Every event is keyed on **(upstream_identity, upstream_version)**: `upstream_identity` is a surface name from `specs/upstream-surface-registry.v1.json`; `upstream_version` is the snapshot sha256 (when a captured body exists) or the registry-declared version (`upstream-surface-registry/v1`) for adoption facts recorded before any tier-2 snapshot. `subject` names the kernel contract (or `contract/field`) the event is about.

## Event vocabulary (the decision)

Exactly **five** event types. The bead's core three plus the two the 052 foundation makes necessary for the log to be complete — without them, a snapshot advancing (the version key changing) or a surface going dark would be invisible to the lineage history:

| Type                        | Meaning                                                                                                                                                                             | Emitted by                                                                                                                                                                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adopt`                     | a kernel contract adopts an upstream surface as a source of truth (kernel `upstream-base/*`)                                                                                        | human (via `append`)                                                                                                                                                                                                                   |
| `diverge`                   | the kernel intentionally departs from upstream (is-overlay extras); `details.convergence_trigger` is **REQUIRED** — a divergence without a documented way home is drift, not policy | human (via `append`)                                                                                                                                                                                                                   |
| `convergence-trigger-fired` | a recorded divergence's trigger condition was observed upstream; the mechanical overlay→base move is now due                                                                        | human (via `append`)                                                                                                                                                                                                                   |
| `snapshot-updated`          | the tier-2 vendored snapshot advanced from a `FETCH_OK` raw record (052-AT-SPEC); `upstream_version` = the new body sha256                                                          | `fetch-capture.py` at promotion time — **the capture stage emits; the differ writes nothing**                                                                                                                                          |
| `fetch-degraded`            | a surface's capture is **materially** degraded (`details.status` = one non-`FETCH_OK` taxonomy status)                                                                              | defined now; per-attempt failures already land append-only in tier 1 (`archive/raw/` meta) — this event is the materiality roll-up (e.g. `fetch_error_streak >= 3` per watcher-liveness), whose emission wiring is a tracked follow-up |

Deliberately **excluded** from the seed: surfaces whose registry contract is not one of the 6 kernel authoring contracts (`claude-slash-commands`, the three `version-signal` surfaces, `anthropic-engineering`) — they enter the log when a kernel contract starts depending on them.

## Event shape

One JSON object per line: `{event_id, at, event_type, upstream_identity, upstream_version, subject, details{}}`. `event_id` is a monotonic integer (sequential from 1); `at` is UTC ISO (`YYYY-MM-DDTHH:MM:SSZ`), non-decreasing across the log. `append` auto-assigns `event_id` and refuses unknown event types, identities not in the current registry (write-time typo guard only — `verify` does not re-check membership, since historical events outlive registry rows), `diverge` without a trigger, and any timestamp earlier than the last event's.

## Append-only enforcement

Kept deliberately simple: `append` snapshots the existing bytes, writes exactly one line, re-reads, and **refuses unless the new content is the old content + one line** (prefix unchanged, line count grew by exactly one). `verify` re-validates every line (shape, sequential `event_id`s, monotonic timestamps), so a rewrite, reorder, or deletion fails loud. The log is additionally covered by the same append-only discipline as the 052 tiers: no deletions or rewrites, in CI or by hand.

## Projection contract (the derived coverage map)

`project-coverage` derives `specs/lineage/coverage-map.json` from the log alone (no wall clock — regeneration is deterministic). Per upstream surface:

- `contract` + `adopted` (latest `adopt`)
- `divergences_outstanding` — `diverge` events with no later `convergence-trigger-fired` matching the same `(upstream_identity, subject)`, each carrying its `convergence_trigger`
- `convergence_triggers_outstanding` (count) + `convergence_fired` (history)
- `last_snapshot_updated` (latest tier-2 promotion: `upstream_version` + when)
- `last_fetch_degraded` (latest material degradation, or null)

Header fields: `_generated` (GENERATED-DO-NOT-EDIT) + `derived_from.line_count` / `last_event_id` (the source-log line count). `append` regenerates the projection after every successful append, so the committed copy can only go stale through a hand edit — which CI catches.

## Enforcement (CI)

In `ci.yml` "Validate specs and docs" (offline, deterministic): `lineage-log.py verify` + `project-coverage --check` (**fails when the committed projection is stale vs the log**) + `--self-test` (fixtures prove append/verify/project plus the staleness and tamper failure modes). The capture self-test (`fetch-capture.py --self-test`) additionally proves a tier-2 promotion emits exactly one `snapshot-updated` event and that dedup/bad-fetch runs emit nothing. The daily `spec-drift-watch.yml` run commits `specs/lineage/` back append-only alongside the archive tiers.

## Seeded history (verifiable only)

The initial 19 events record what can be sourced from committed artifacts: the 2026-05-28 vendored capture of the agentskills spec (sha256 of `_vendor/upstream/skill-frontmatter/agentskills-spec-v1.0.md`); the 045-RR-LAND walking-skeleton adoption of the three skill-frontmatter surfaces (2026-06-09); the seven is-overlay divergences with their convergence triggers, sourced verbatim from the kernel `$comment`s (`intent-eval-core` `schemas/authoring/v1/is-overlay/skill-frontmatter.v1.json`); and the 050-AT-SPEC registry adoption of the remaining eight kernel-contract surfaces (2026-06-11). Known limitation (tracked follow-up): a promotion whose lineage append fails (loud stderr warning in the capture log) is not yet cross-checked against `vendor-meta.json`.
