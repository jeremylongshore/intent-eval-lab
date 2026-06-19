# 057 — Detector-health composite dashboard (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + three tiers), 054-AT-SPEC (lineage log + coverage map) · **Epic:** 9k5h (GH intent-eval-lab#114)

This is the normative reference for the composite detector-health document. Implementation: `scripts/detector-health.py`; outputs: `specs/detector-health.json` (machine) + `docs/detector-health.md` (rendering).

## Why health leads (the Gregg correction, 9k5h.13)

A drift table full of green rows is a **vanity metric** when the watcher that produces those rows is dead: a cron that stopped firing, a surface that 404s forever, or a registry row nobody monitors all read as "no drift" while the contract silently goes stale. The dashboard therefore leads with the health of the **detection machinery itself** — the verdict tile is the first thing rendered, and the per-surface drift table renders strictly BELOW it. USE-style: first ask "is the instrument working?", only then read the instrument.

## The composite predicate

`HEALTHY` iff **all** of, evaluated in this fixed order:

| #   | Condition                | Predicate                                                                                                                                                    | Source of the signal                                                                          |
| --- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| 1   | `watcher-run-recent`     | last successful watcher run <= `max_gap_hours` (26 — one daily cron + slack) ago; a **null** last-run (bootstrap) FAILS — an unproven watcher is never green | `specs/snapshots/.state.json` (`last_run_utc`, written by `watcher-liveness.py --record-run`) |
| 2   | `no-fetch-error-streaks` | zero surfaces with `fetch_error_streak >= streak_threshold` (3) — such a surface is effectively unmonitored                                                  | `specs/snapshots/.state.json` (per-surface streaks)                                           |
| 3   | `coverage-at-target`     | monitored surfaces / registered surfaces at the registry-declared target: **100% of registered surfaces monitored**                                          | `specs/upstream-surface-registry.v1.json`                                                     |

Thresholds are read from the state file (the same constants `watcher-liveness.py` enforces), so the dashboard and the liveness guards can never disagree at a boundary.

## The DEGRADED naming rule

Anything short of all-three-pass is `DEGRADED`, and the **failing condition(s) are named first** — `failing_conditions` is the leading array in the JSON, and the markdown tile lists every `FAIL` line before any `ok` line. A reader must never have to scan past green to find red.

## Derived, deterministic, fingerprinted

The document is a pure derivation of existing committed state — the script fetches nothing and owns no state of its own. It additionally folds in read-only context: the lineage coverage map (`specs/lineage/coverage-map.json`, 054-AT-SPEC) for adopt / diverge / outstanding-trigger counts, and the drift baselines (`specs/snapshots/.sha/*.sha`) for the per-surface drift rows. Output is deterministic given the inputs + `--now`; `evaluated_at` records the timestamp the verdict was computed against. The JSON carries an `inputs` map with the **sha256 fingerprint of every source file consumed**.

## Freshness gate

`--check` re-derives the document from the current sources **at the committed `evaluated_at`** (so mere passage of time never trips it — the `project-coverage --check` pattern from 054-AT-SPEC) and fails when either committed output differs byte-for-byte. The dashboard is a derived view — never hand-edit it; after changing the registry, baselines, or liveness state, regenerate with `python3 scripts/detector-health.py`.

## Enforcement + wiring

- `ci.yml` "Validate specs and docs" runs `--self-test` (offline fixtures: healthy, dead-watcher > 26h, streak >= 3, coverage-gap) + `--check` on every PR and push to main.
- The scheduled `spec-drift-watch.yml` run regenerates the dashboard after `watcher-liveness.py --record-run` and commits it back append-only **together with** `specs/snapshots/.state.json` it summarizes (committed output and committed sources must advance in the same commit, or the CI freshness gate would red on the next PR). The regeneration step runs `if: always()` — the dashboard flips to DEGRADED-and-committed on exactly the runs where a watcher gate failed.

## Known limitation

The committed verdict is a snapshot: if the cron dies, the last committed tile keeps its old verdict (typically the one that named the failure). The dead-man heartbeat in `watcher-liveness.py` — not this dashboard — is the alarm for "no runs are happening at all"; the dashboard's job is to make that state impossible to mistake for green once observed.
