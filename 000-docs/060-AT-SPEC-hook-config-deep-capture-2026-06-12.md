# 060 — Hook-config deep capture + projection contract (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + tiers), 054-AT-SPEC (lineage log), 058/059-AT-SPEC (the plugin-manifest + agent-definition analogs this capture stamps) · **Epic:** 9k5h (GH intent-eval-lab#114)

The `hook-config` contract gets the deep capture `skill-frontmatter`, `mcp-config`, `plugin-manifest`, and `agent-definition` already have. Like 058/059: there is **no machine-readable upstream schema** for the hooks block and no upstream spec versioning — the `code.claude.com/docs/en/hooks` page IS the spec (the 30-event Hook-lifecycle table, the three-levels-of-nesting Configuration statement, the Matcher-patterns tables, and the five `Field|Required|Description` handler-field tables) and `hooks/hooks.json` files from `anthropics/claude-plugins-official` are real-world corroboration (precedence per 050-AT-SPEC: the reference page is the spec; samples corroborate). **Deviation from 059:** the registry registers TWO monitored surfaces for this contract (`claude-hooks` + `claude-settings`); the hooks page is primary — it defines every handler field — and references `/en/settings#hook-configuration` only for hooks-block placement + `allowManagedHooksOnly`, so the settings page is vendored as **supporting-doc** (the 059 best-practices arrangement) despite being a registered surface. The handler tables carry lowercase `yes`/`no` in the Required column (059's used `Yes`/`No`). `spec_version` is the capture date (`unversioned-2026-06-12`). Implementation: `specs/_vendor/upstream/hook-config/` + `scripts/extract-hook-config-projection.py`.

## The vendored capture (contract-keyed tier-2)

| File | Authority | What |
|---|---|---|
| `claude-code-hooks.md` | reference (registered surface `claude-hooks`) | The hooks reference page, `.md` form — the same URL/form the registry's `fetch_claude_hooks` extractor monitors. Carries the 30-event lifecycle table, the nesting statement (hook event → matcher group → hook handler), the 6-row Hook-locations table, matcher evaluation forms + 10 no-matcher-support events, and the 18 documented handler fields across 5 tables. |
| `claude-code-settings.md` | supporting (registered surface `claude-settings`) | Referenced by the hooks page for hooks-block placement inside settings files + the `allowManagedHooksOnly` gate; defines NO handler fields, so the extractor does not consume it — vendored for provenance completeness. |
| `sample-*.hooks.json` (4) | sample-corroboration | Commit-pinned (`eb1510e1` — the same pin 058/059 use) plugin `hooks/hooks.json` files, chosen for structural diversity (per-file `selection_basis` in `vendor-meta.json`). Ground truth: matcher omission, pipe-list matchers, `if`, `asyncRewake`, explicit timeouts all appear; one official sample uses `rewakeMessage` + `rewakeSummary`, absent from every documented table. Negative fact recorded: `anthropics/claude-code` mirrors the same files and its `examples/settings/*.json` carry no hooks block — no public settings-file-form sample exists. |
| `vendor-meta.json` | — | Per-file provenance (source URL + ref SHA + sha256 + bytes + `fetched_at`), 052-AT-SPEC conventions. |
| `projection.json` | — | The **normative projection** (below). GENERATED — never hand-edit. |

The fetch happened **once** at build time (2026-06-12). CI never refetches — offline determinism; ongoing freshness comes from the watcher's daily run over the registered `claude-hooks` + `claude-settings` surfaces. `claude-plugins-official` is an `unmonitored_candidates` registry row; the samples' `vendor-meta.json` entries are their provenance records until a sampleable surface is registered per 050-AT-SPEC change discipline.

## The normative projection (FF#2 left-hand side for hook-config)

`scripts/extract-hook-config-projection.py` extracts `projection.json` deterministically from the vendored bytes alone — sorted keys, **no wall-clock in the output**. Every fact is mechanical: the 30 lifecycle-table events in doc order, the `The configuration has three levels of nesting:` sentence as a hard anchor (exit 2 if missing), the 6 hook locations (markup-stripped), the matcher match-all forms (`"*"`/`""`/omitted) + JS-regex fallback + the 10 no-matcher-support events, the five handler types from the `type: "X"` bullets, the 18 documented handler fields (6 required) with per-table scope (`common`/`command`/`http`/`mcp_tool`/`prompt-agent`), closed-set enums (`type`, `shell` — the residue rule additionally tolerates the literal `(default)` marker and strips JSON-literal quotes), per-type timeout defaults (600/600/600/30/60), and the 4 sample `hooks.json` files cross-corroborated. The section slicer is fence-aware — the page embeds bash/json fences whose `#` comment lines would fake headings.

**The documented-vs-observed field provenance rule (conservative by construction):** a handler field the page documents is `source: "documented"` with `required` known; a field used in samples but absent from the page lands in `fields_observed_not_documented` — **never promoted to documented**. Current capture: **18 documented handler fields** (6 required), **two observed-only fields** (`rewakeMessage`, `rewakeSummary` — used by one official plugin, on no documented table), recorded as the divergence below.

## Cross-check against the kernel (read-only; findings, never fixes)

The self-test cross-checks the committed projection against the kernel's expectations (`intent-eval-core` `schemas/authoring/v1/upstream-base/hook-config.v1.json`, embedded as fixtures — the kernel is another repo and CI is offline). Both finding sets are exact-matched, so a re-capture that shifts any finding fails loud and a human reconciles:

- **Agreements (4):** the 30-event enum matches the kernel exactly, in lifecycle-table order; the 5-value `type` enum matches exactly; `command` is required for command handlers on both sides; samples stay within the documented event + type enums.
- **Divergences (6, reported NOT fixed — tier-3 promotion is human per 052-AT-SPEC):**
  1. `shape` — the kernel flattens the documented 3-level nesting to a single-hook entry carrying `event` + `matcher` (the kernel `$comment` documents this projection choice; still reported).
  2. `matcher` — the doc allows omit/`""`/`"*"` match-all; the kernel requires an explicit non-empty matcher (IS narrowing).
  3. `doc-handler-fields-not-in-kernel` — 16 of the 18 documented fields are unmodeled (`allowedEnvVars`, `args`, `async`, `asyncRewake`, `headers`, `if`, `input`, `model`, `once`, `prompt`, `server`, `shell`, `statusMessage`, `timeout`, `tool`, `url`).
  4. `kernel-only` — the kernel's `metadata` extension object is not a documented upstream field.
  5. `per-type-required-fields` — the kernel models the command handler only; the required fields of the other four types (`url`, `server`, `tool`, `prompt`) are unmodeled.
  6. `samples:handler-fields-outside-documented-set` — `rewakeMessage`, `rewakeSummary` (upstream tolerance observed in one official sample).

## Enforcement

- **CI** (`ci.yml` "Validate specs and docs", appended step): `extract-hook-config-projection.py --check` (committed projection must equal a fresh extraction — staleness fails) + `--self-test` (fixture anchors, missing-anchor exit-2, staleness detection, kernel cross-check exact-match). Offline, deterministic.
- **Lineage** (054-AT-SPEC): the capture appended `snapshot-updated` event 23 (`claude-hooks`, `upstream_version` = the doc sha256, subject `hook-config`) via the documented CLI; the coverage map regenerated in the same append, and the detector-health composite (057-AT-SPEC, whose inputs include the coverage map) regenerated in the same commit.
- Workflow files stay harness-hash-pinned; the ci.yml edit re-pinned `.harness-hash` in the same commit.
