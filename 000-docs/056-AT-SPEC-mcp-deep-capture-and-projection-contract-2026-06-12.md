# 056 — MCP deep capture + projection contract (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + tiers), 054-AT-SPEC (lineage log) · **Epic:** 9k5h (GH intent-eval-lab#114)

The `mcp-config` contract gets the deep capture `skill-frontmatter` already has. MCP goes first because it is the one contract whose primary upstream is truly machine-readable: `modelcontextprotocol/modelcontextprotocol` publishes `schema/<version>/schema.json`. Implementation: `specs/_vendor/upstream/mcp-config/` + `scripts/extract-mcp-projection.py`.

## The vendored capture (contract-keyed tier-2)

| File | Authority | What |
|---|---|---|
| `mcp-schema-2025-11-25.json` | official-spec-machine-readable | The official MCP schema for the **CURRENT** spec revision — 2025-11-25 per the spec's versioning page, checked at fetch time. Fetched **commit-pinned** (immutable URL); exact source URL + sha256 + bytes + `fetched_at` in `vendor-meta.json`. |
| `claude-code-mcp.md` | anthropic-doc | `code.claude.com/docs/en/mcp.md` — the authority for the `.mcp.json` per-server config shape (`command`/`args`/`env`/`type`), which the protocol schema deliberately does not define. |
| `vendor-meta.json` | — | Per-file provenance, 052-AT-SPEC vendor-meta conventions. |
| `projection.json` | — | The **normative projection** (below). GENERATED — never hand-edit. |

The fetch happened **once** at build time (2026-06-12). CI never refetches — offline determinism; ongoing freshness comes from the watcher's daily run over the registered surfaces (`mcp-schema-ts` / `mcp-spec-docs` / `mcp-releases`). Note: `claude-code-mcp.md` is **not yet a registered surface**; registering it per 050-AT-SPEC change discipline is a tracked follow-up, and its `vendor-meta.json` entry is its provenance record until then.

## The normative projection (FF#2 left-hand side for mcp-config)

`scripts/extract-mcp-projection.py` extracts `projection.json` deterministically from the vendored bytes alone — sorted keys, **no wall-clock in the output**. Every extracted fact is mechanical (JSON-parsed from the schema; regexed from the doc's standardized-format block, `--transport X` flags, `"type": "X"` examples, alias and deprecation sentences):

- **`machine_schema`** — the schema's `Implementation` identity surface (required `name`/`version`) **and the load-bearing negative fact**: the official machine-readable schema defines **no transport enum and no server-config keys** (`defines_server_config: false`, `transport_defs: []`). Recorded explicitly, never papered over.
- **`server_config`** — from the Claude Code doc: server entries keyed by name in the `mcpServers` map; standardized-format fields `command: string` / `args: array` / `env: object`; transport selector field `type` (absent from the standardized-format example); transport types `{http, sse, stdio, ws}`; alias `streamable-http → http`; `sse` deprecated.

## Cross-check against the kernel (read-only; findings, never fixes)

The self-test cross-checks the committed projection against the kernel's expectations (`intent-eval-core` `schemas/authoring/v1/upstream-base/mcp-config.v1.json`, embedded as fixtures — the kernel is another repo and CI is offline). Both finding sets are exact-matched, so a re-capture that shifts any finding fails loud and a human reconciles:

- **Agreements (6):** kernel transport-enum membership ⊆ upstream types; `command`/`args`/`env` types match; `name` lifted from the map key as the kernel documents; `sse` deprecated on both sides.
- **Divergences (4, reported NOT fixed — tier-3 promotion is human per 052-AT-SPEC):**
  1. `required-set` — the kernel requires `transport`, but upstream's own standardized-format example omits `type` (stdio default); the kernel's flat all-required shape is an IS projection choice.
  2. `selector-name` — upstream calls the field `type`; the kernel calls it `transport`.
  3. `alias` — upstream accepts `streamable-http` (the MCP spec's own name for the transport); the kernel enum omits it.
  4. `provenance` — the machine-readable schema defines neither the transport enum nor the server-config shape; the kernel `$comment` attributes the enum to "the MCP spec", but deterministically it is only fully recoverable from the Claude Code page, and `ws` in particular is Claude-Code-only (the doc states `claude mcp add --transport` does not accept `ws`).

## Enforcement

- **CI** (`ci.yml` "Validate specs and docs", appended step): `extract-mcp-projection.py --check` (committed projection must equal a fresh extraction — staleness fails) + `--self-test` (fixture anchors, missing-anchor exit-2, staleness detection, kernel cross-check exact-match). Offline, deterministic.
- **Lineage** (054-AT-SPEC): the capture appended `snapshot-updated` event 20 (`mcp-schema-ts`, `upstream_version` = the schema sha256, subject `mcp-config`) via the documented CLI; the coverage map regenerated in the same append.
- Workflow files stay harness-hash-pinned; the ci.yml edit re-pinned `.harness-hash` in the same commit.
