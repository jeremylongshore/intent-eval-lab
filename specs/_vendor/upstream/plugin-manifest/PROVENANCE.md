# `specs/_vendor/upstream/plugin-manifest/` — vendored upstream source (the firewall)

The **single vendored source of record** for the `plugin-manifest` authoring contract's
upstream truth — the third contract to get the deep capture (after
`_vendor/upstream/skill-frontmatter/` and `_vendor/upstream/mcp-config/`), and the first
with **no machine-readable upstream at all**: Anthropic publishes no schema for
`.claude-plugin/plugin.json`. The reference page is the spec; real-world sample manifests
corroborate it. Upstream is captured here deterministically; the deterministic extractor
reads only; nothing downstream writes into this directory.

**Do not hand-edit the snapshots to encode IS policy.** IS policy lives in the kernel
overlay (`@intentsolutions/core` `schemas/authoring/v1/is-overlay/plugin-manifest.v1.json`).
This directory holds only what upstream says.

## Contents

| File | What |
|---|---|
| `claude-code-plugins-reference.md` | The Claude Code plugins reference page (`code.claude.com/docs/en/plugins-reference.md`) — § "Plugin manifest schema" is the authority for the `plugin.json` field shape (Required fields + Metadata fields + Component path fields tables, the Complete-schema example, and the unrecognized-fields tolerance rules). Same URL/form the registry's `fetch_plugins_reference` extractor monitors. |
| `sample-*.plugin.json` (5) | Real-world `plugin.json` manifests from `anthropics/claude-plugins-official`, commit-pinned, chosen for structural diversity (per-file `selection_basis` in `vendor-meta.json`). Ground truth: a field used in samples but absent from the doc is recorded `observed-in-samples`, never `documented`. |
| `vendor-meta.json` | Exact source URL + sha256 + bytes + `fetched_at` per file (052-AT-SPEC vendor-meta conventions, contract-keyed), plus per-sample `upstream_commit` + `source_path` + `selection_basis`. |
| `projection.json` | The **normative projection** extracted deterministically by `scripts/extract-plugin-manifest-projection.py` — the field-diff left-hand side for FF#2 on this contract. Regenerate: `python3 scripts/extract-plugin-manifest-projection.py --write`. Never hand-edit (CI `--check` fails on staleness). |

## Authorities (precedence per `specs/upstream-surface-registry.v1.json` + 050-AT-SPEC)

1. `code.claude.com/docs/en/plugins-reference.md` § "Plugin manifest schema" — the spec
   (registered surface `plugins-reference`, contract `plugin-manifest`). Prose + tables +
   JSON examples; there is **no machine-readable upstream schema** — this is the
   documented deviation from the mcp-config capture.
2. `github.com/anthropics/claude-plugins-official` sample manifests — real-world ground
   truth, corroboration only (registry `unmonitored_candidates` row; the samples'
   provenance records live in `vendor-meta.json` until a sampleable surface is registered).

## Refresh mechanism

The fetch happened ONCE at build time (2026-06-12); CI never refetches — offline
determinism. Ongoing freshness signals come from the watcher's daily run over the
registered `plugins-reference` surface. On a material upstream change a human re-captures
here, regenerates `projection.json`, and reconciles the cross-check expectations — the
LLM never authors a kernel schema edit and never closes the deterministic drift signal.
Normative spec for this directory:
`000-docs/058-AT-SPEC-plugin-manifest-deep-capture-2026-06-12.md`.
