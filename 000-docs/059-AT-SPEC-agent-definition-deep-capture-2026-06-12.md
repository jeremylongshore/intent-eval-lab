# 059 — Agent-definition deep capture + projection contract (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + tiers), 054-AT-SPEC (lineage log), 058-AT-SPEC (the plugin-manifest analog this capture stamps) · **Epic:** 9k5h (GH intent-eval-lab#114)

The `agent-definition` contract gets the deep capture `skill-frontmatter`, `mcp-config`, and `plugin-manifest` already have. Like plugin-manifest (058): there is **no machine-readable upstream schema** for the YAML frontmatter of subagent files (`agents/*.md`) and no upstream spec versioning — the `code.claude.com/docs/en/sub-agents` page IS the spec (the "Supported frontmatter fields" table + YAML examples + the "Choose a model" bullets) and sample agent files from `anthropics/claude-plugins-official` are real-world corroboration (authority precedence per 050-AT-SPEC: the reference page is the spec; samples corroborate). **Additional deviation from 058:** the frontmatter table carries `Field|Required|Description` columns only — **no Type and no Example column** — so per-field types are not documented tabularly; value-shape facts come from the page's YAML example instead. `spec_version` is the capture date (`unversioned-2026-06-12`). Implementation: `specs/_vendor/upstream/agent-definition/` + `scripts/extract-agent-definition-projection.py`.

## The vendored capture (contract-keyed tier-2)

| File | Authority | What |
|---|---|---|
| `claude-code-sub-agents.md` | reference (registered surface `sub-agents`) | The sub-agents page, `.md` form — the same URL/form the registry's `fetch_sub_agents` extractor monitors. § "Supported frontmatter fields" carries the 16-field table; the Write-subagent-files example and Choose-a-model bullets supply value shapes. |
| `platform-skill-authoring-best-practices.md` | supporting (`anthropic-doc` tier) | Cited by the kernel upstream-base `$comment`; defines NO frontmatter fields, so the extractor does not consume it — vendored for provenance completeness. |
| `sample-*.agent.md` (5) | sample-corroboration | Commit-pinned (`eb1510e1`) `agents/*.md` files from the official plugins repo, chosen for structural diversity (per-file `selection_basis` in `vendor-meta.json`). Ground truth: `tools` appears in BOTH wire forms; one official sample uses `color: magenta`, outside the documented 8-value enum. |
| `vendor-meta.json` | — | Per-file provenance (source URL + ref SHA + sha256 + bytes + `fetched_at`), 052-AT-SPEC conventions. |
| `projection.json` | — | The **normative projection** (below). GENERATED — never hand-edit. |

The fetch happened **once** at build time (2026-06-12). CI never refetches — offline determinism; ongoing freshness comes from the watcher's daily run over the registered `sub-agents` surface. `claude-plugins-official` is an `unmonitored_candidates` registry row, not a registered surface; the samples' `vendor-meta.json` entries are their provenance records until one is registered per 050-AT-SPEC change discipline.

## The normative projection (FF#2 left-hand side for agent-definition)

`scripts/extract-agent-definition-projection.py` extracts `projection.json` deterministically from the vendored bytes alone — sorted keys, **no wall-clock in the output**. Every fact is mechanical: the 16 table rows (`required` from the Required column; the `Only `name` and `description` are required.` sentence is a hard anchor — exit 2 if missing), closed-set enum clauses (`permissionMode`/`memory`/`effort`/`color`) under a residue rule that keeps the open `model` clause enum-free (`model_full_id_latitude` recorded instead, aliases from the Choose-a-model bullet), `Set to`-single-value facts (`background`, `isolation`), the YAML example's comma-separated `tools` wire form, and the sample frontmatter cross-corroborated.

**The documented-vs-observed field provenance rule (conservative by construction):** a field the page documents is `source: "documented"` with `required` known; a field used in samples but absent from the page is `source: "observed-in-samples"` with `required: "unknown"` — **never promoted to documented**. Current capture: **16 documented fields** (2 required + 14 optional), **zero observed-only fields** — every field the official samples use is page-documented, recorded as the `samples-corroborate` agreement below.

## Cross-check against the kernel (read-only; findings, never fixes)

The self-test cross-checks the committed projection against the kernel's expectations (`intent-eval-core` `schemas/authoring/v1/upstream-base/agent-definition.v1.json`, embedded as fixtures — the kernel is another repo and CI is offline). Both finding sets are exact-matched, so a re-capture that shifts any finding fails loud and a human reconciles:

- **Agreements (5):** `name`+`description`-only-required on both sides; the doc's lowercase-letters-and-hyphens prose is what the kernel's `name` pattern encodes; `color` enum matches exactly (8 values); the kernel's `model` enum equals the documented aliases plus `inherit`; no observed-only sample fields.
- **Divergences (6, reported NOT fixed — tier-3 promotion is human per 052-AT-SPEC):**
  1. `doc-fields-not-in-kernel` — the kernel models 6 of the 16 documented fields (`background`, `disallowedTools`, `effort`, `hooks`, `initialPrompt`, `isolation`, `maxTurns`, `mcpServers`, `memory`, `permissionMode`, `skills` are unmodeled).
  2. `kernel-only` — the kernel's `metadata` extension object is not a documented upstream field (it encodes Claude Code's unrecognized-fields tolerance structurally).
  3. `tools-wire-form` — the page's example shows the comma-separated string; the kernel narrows to array-only (a documented IS projection choice); samples also use a YAML flow array.
  4. `model-full-id-latitude` — the doc admits a full model ID; the kernel's closed alias enum does not model it.
  5. `name-maxlength` — the kernel's 64-char cap on `name` is not documented upstream.
  6. `samples:color-outside-documented-enum` — one official sample uses `magenta` (upstream tolerance observed; the doc and kernel both enumerate 8).

## Enforcement

- **CI** (`ci.yml` "Validate specs and docs", appended step): `extract-agent-definition-projection.py --check` (committed projection must equal a fresh extraction — staleness fails) + `--self-test` (fixture anchors, missing-anchor exit-2, staleness detection, kernel cross-check exact-match). Offline, deterministic.
- **Lineage** (054-AT-SPEC): the capture appended `snapshot-updated` event 22 (`sub-agents`, `upstream_version` = the doc sha256, subject `agent-definition`) via the documented CLI; the coverage map regenerated in the same append, and the detector-health composite (057-AT-SPEC, whose inputs include the coverage map) regenerated in the same commit.
- Workflow files stay harness-hash-pinned; the ci.yml edit re-pinned `.harness-hash` in the same commit.
