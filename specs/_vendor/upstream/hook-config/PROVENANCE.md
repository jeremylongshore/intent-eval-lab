# `specs/_vendor/upstream/hook-config/` — vendored upstream source (the firewall)

The **single vendored source of record** for the `hook-config` authoring contract's
upstream truth — the fifth contract to get the deep capture (after
`_vendor/upstream/skill-frontmatter/`, `_vendor/upstream/mcp-config/`,
`_vendor/upstream/plugin-manifest/`, and `_vendor/upstream/agent-definition/`), and
like plugin-manifest and agent-definition one with **no machine-readable upstream at
all**: Anthropic publishes no schema for the hooks block of `hooks.json` /
`settings.json`. The hooks reference page is the spec; real-world `hooks/hooks.json`
files corroborate it. Upstream is captured here deterministically; the deterministic
extractor reads only; nothing downstream writes into this directory.

**Do not hand-edit the snapshots to encode IS policy.** IS policy lives in the kernel
overlay (`@intentsolutions/core` `schemas/authoring/v1/is-overlay/hook-config.v1.json`).
This directory holds only what upstream says.

## Contents

| File | What |
|---|---|
| `claude-code-hooks.md` | The Claude Code hooks reference page (`code.claude.com/docs/en/hooks.md`) — the authority for the hook-config shape: the § "Hook lifecycle" 30-event table, § "Configuration" (the three-levels-of-nesting statement: hook event → matcher group → hook handler), § "Matcher patterns" (match-all / exact-or-pipe-list / JS-regex evaluation + the per-event no-matcher-support rows), and § "Hook handler fields" (the five handler types and the five `Field/Required/Description` tables: common, command, HTTP, MCP tool, prompt-and-agent). Same URL/form the registry's `fetch_claude_hooks` extractor monitors. |
| `claude-code-settings.md` | The Claude Code settings page — supporting authority: the hooks page's § "Hook locations" points at `/en/settings#hook-configuration` for hooks-block placement inside settings files and the `allowManagedHooksOnly` gate. Defines no handler fields, so the extractor does not consume it — vendored because the hooks page references it for the config-shape placement. Unlike 059's supporting doc this one IS a registered surface (`claude-settings`, same `hook-config` contract). |
| `sample-*.hooks.json` (4) | Real-world plugin `hooks/hooks.json` files from `anthropics/claude-plugins-official`, commit-pinned, chosen for structural diversity (per-file `selection_basis` in `vendor-meta.json`). Ground truth: a field used in samples but absent from the doc is recorded `observed-in-samples`, never `documented` — this capture has two such fields (`rewakeMessage`, `rewakeSummary`). |
| `vendor-meta.json` | Exact source URL + sha256 + bytes + `fetched_at` per file (052-AT-SPEC vendor-meta conventions, contract-keyed), plus per-sample `upstream_commit` + `source_path` + `selection_basis`, plus the negative fact that no public settings-file-form hook sample exists in `anthropics/claude-code`. |
| `projection.json` | The **normative projection** extracted deterministically by `scripts/extract-hook-config-projection.py` — the field-diff left-hand side for FF#2 on this contract. Regenerate: `python3 scripts/extract-hook-config-projection.py --write`. Never hand-edit (CI `--check` fails on staleness). |

## Authorities (precedence per `specs/upstream-surface-registry.v1.json` + 050-AT-SPEC)

1. `code.claude.com/docs/en/hooks.md` — the spec (registered surface `claude-hooks`,
   contract `hook-config`). Prose + the lifecycle/matcher/handler-field tables + JSON
   examples; there is **no machine-readable upstream schema** — same deviation class
   as the plugin-manifest and agent-definition captures.
2. `code.claude.com/docs/en/settings.md` — supporting authority for this capture
   (registered surface `claude-settings`, same contract): hooks-block placement +
   `allowManagedHooksOnly`. The hooks page defines every handler field; the settings
   page defines none.
3. `github.com/anthropics/claude-plugins-official` sample `hooks/hooks.json` files —
   real-world ground truth, corroboration only (registry `unmonitored_candidates` row;
   the samples' provenance records live in `vendor-meta.json` until a sampleable
   surface is registered per 050-AT-SPEC change discipline).

## Refresh mechanism

The fetch happened ONCE at build time (2026-06-12); CI never refetches — offline
determinism. Ongoing freshness signals come from the watcher's daily run over the
registered `claude-hooks` + `claude-settings` surfaces. On a material upstream change
a human re-captures here, regenerates `projection.json`, and reconciles the
cross-check expectations — the LLM never authors a kernel schema edit and never
closes the deterministic drift signal. Normative spec for this directory:
`000-docs/060-AT-SPEC-hook-config-deep-capture-2026-06-12.md`.
