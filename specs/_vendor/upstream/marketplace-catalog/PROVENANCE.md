# `specs/_vendor/upstream/marketplace-catalog/` — vendored upstream source (the firewall)

The **single vendored source of record** for the `marketplace-catalog` authoring
contract's upstream truth — the sixth and FINAL contract to get the deep capture
(after `_vendor/upstream/skill-frontmatter/`, `_vendor/upstream/mcp-config/`,
`_vendor/upstream/plugin-manifest/`, `_vendor/upstream/agent-definition/`, and
`_vendor/upstream/hook-config/`), and like plugin-manifest / agent-definition /
hook-config one with **no machine-readable upstream at all**: Anthropic publishes
no load-time schema for `.claude-plugin/marketplace.json` (the `$schema` URL the
official catalog cites is an editor-autocomplete pointer the page says Claude Code
ignores). The plugin-marketplaces reference page is the spec; the official catalog
itself corroborates it. Upstream is captured here deterministically; the
deterministic extractor reads only; nothing downstream writes into this directory.

**Do not hand-edit the snapshots to encode IS policy.** IS policy lives in the kernel
overlay (`@intentsolutions/core` `schemas/authoring/v1/is-overlay/marketplace-catalog.v1.json`).
This directory holds only what upstream says.

## Contents

| File | What |
|---|---|
| `claude-code-plugin-marketplaces.md` | The Claude Code plugin-marketplaces reference page (`code.claude.com/docs/en/plugin-marketplaces.md`) — the authority for the catalog shape: § "Marketplace schema" (the Required-fields, Owner-fields, and Optional-fields tables + the Reserved-names note + the metadata back-compat sentence), § "Plugin entries" (the Required-fields table + the Standard-metadata and Component-configuration tables + the marketplace-specific-fields and manifest-passthrough sentences), § "Plugin sources" (the 5-form summary table, the four per-type `Field/Type/Description` tables, the `source` discriminator examples, the sha-beats-ref rule), and § "Strict mode". Same URL/form the registry's `fetch_plugin_marketplaces` extractor monitors. |
| `sample-claude-plugins-official.marketplace.json` | THE official ground-truth catalog — `anthropics/claude-plugins-official` `.claude-plugin/marketplace.json`, commit-pinned (`eb1510e1`, the same pin 058/059/060 use), 223 plugin entries, vendored whole (126,953 bytes < the 200KB truncation threshold). Ground truth: a field used in the catalog but absent from the doc is recorded `observed-in-samples`, never `documented` — this capture has three such tolerances (`commit` on github sources, `path` on url sources, the non-kebab plugin name `wordpress.com`). |
| `vendor-meta.json` | Exact source URL + sha256 + bytes + `fetched_at` per file (052-AT-SPEC vendor-meta conventions, contract-keyed), plus the sample's `upstream_commit` + `source_path` + `selection_basis`, plus the negative fact that the page documents exactly one catalog file form. |
| `projection.json` | The **normative projection** extracted deterministically by `scripts/extract-marketplace-catalog-projection.py` — the field-diff left-hand side for FF#2 on this contract. Regenerate: `python3 scripts/extract-marketplace-catalog-projection.py --write`. Never hand-edit (CI `--check` fails on staleness). |

## Authorities (precedence per `specs/upstream-surface-registry.v1.json` + 050-AT-SPEC)

1. `code.claude.com/docs/en/plugin-marketplaces.md` — the spec (registered surface
   `plugin-marketplaces`, contract `marketplace-catalog`). Prose + the
   schema/entry/source/strict tables + JSON examples; there is **no machine-readable
   upstream schema** — same deviation class as the plugin-manifest, agent-definition,
   and hook-config captures.
2. `github.com/anthropics/claude-plugins-official` `.claude-plugin/marketplace.json` —
   real-world ground truth, corroboration only (registry `unmonitored_candidates` row;
   the sample's provenance record lives in `vendor-meta.json` until a sampleable
   surface is registered per 050-AT-SPEC change discipline). Unusually strong for this
   contract: the sample IS the official catalog.

## Refresh mechanism

The fetch happened ONCE at build time (2026-06-12); CI never refetches — offline
determinism. Ongoing freshness signals come from the watcher's daily run over the
registered `plugin-marketplaces` surface. On a material upstream change a human
re-captures here, regenerates `projection.json`, and reconciles the cross-check
expectations — the LLM never authors a kernel schema edit and never closes the
deterministic drift signal. Normative spec for this directory:
`000-docs/061-AT-SPEC-marketplace-catalog-deep-capture-2026-06-12.md`.
