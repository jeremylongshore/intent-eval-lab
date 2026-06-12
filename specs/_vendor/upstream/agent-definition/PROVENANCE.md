# `specs/_vendor/upstream/agent-definition/` — vendored upstream source (the firewall)

The **single vendored source of record** for the `agent-definition` authoring contract's
upstream truth — the fourth contract to get the deep capture (after
`_vendor/upstream/skill-frontmatter/`, `_vendor/upstream/mcp-config/`, and
`_vendor/upstream/plugin-manifest/`), and like plugin-manifest one with **no
machine-readable upstream at all**: Anthropic publishes no schema for the YAML
frontmatter of subagent files (`agents/*.md`). The sub-agents reference page is the spec;
real-world sample agent files corroborate it. Upstream is captured here
deterministically; the deterministic extractor reads only; nothing downstream writes
into this directory.

**Do not hand-edit the snapshots to encode IS policy.** IS policy lives in the kernel
overlay (`@intentsolutions/core` `schemas/authoring/v1/is-overlay/agent-definition.v1.json`).
This directory holds only what upstream says.

## Contents

| File | What |
|---|---|
| `claude-code-sub-agents.md` | The Claude Code sub-agents reference page (`code.claude.com/docs/en/sub-agents.md`) — § "Supported frontmatter fields" is the authority for the agent-frontmatter field shape (the Field/Required/Description table, the "Only `name` and `description` are required" sentence, the per-field enum clauses, and the Write-subagent-files YAML example). Same URL/form the registry's `fetch_sub_agents` extractor monitors. |
| `platform-skill-authoring-best-practices.md` | The platform agent-skills best-practices page — supporting authority only (the kernel upstream-base `$comment` cites it). Authoring guidance; defines no frontmatter fields, so the extractor does not consume it. |
| `sample-*.agent.md` (5) | Real-world `agents/*.md` files from `anthropics/claude-plugins-official`, commit-pinned, chosen for structural diversity (per-file `selection_basis` in `vendor-meta.json`). Ground truth: a field used in samples but absent from the doc is recorded `observed-in-samples`, never `documented`. |
| `vendor-meta.json` | Exact source URL + sha256 + bytes + `fetched_at` per file (052-AT-SPEC vendor-meta conventions, contract-keyed), plus per-sample `upstream_commit` + `source_path` + `selection_basis`. |
| `projection.json` | The **normative projection** extracted deterministically by `scripts/extract-agent-definition-projection.py` — the field-diff left-hand side for FF#2 on this contract. Regenerate: `python3 scripts/extract-agent-definition-projection.py --write`. Never hand-edit (CI `--check` fails on staleness). |

## Authorities (precedence per `specs/upstream-surface-registry.v1.json` + 050-AT-SPEC)

1. `code.claude.com/docs/en/sub-agents.md` § "Supported frontmatter fields" — the spec
   (registered surface `sub-agents`, contract `agent-definition`). Prose + one
   Field/Required/Description table + YAML examples; there is **no machine-readable
   upstream schema** — same deviation class as the plugin-manifest capture. Additional
   deviation: the table documents NO per-field types (no Type column, no Example column).
2. `platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md` —
   supporting authority (`anthropic-doc` tier), vendored for provenance completeness.
3. `github.com/anthropics/claude-plugins-official` sample agent files — real-world ground
   truth, corroboration only (registry `unmonitored_candidates` row; the samples'
   provenance records live in `vendor-meta.json` until a sampleable surface is registered).

## Refresh mechanism

The fetch happened ONCE at build time (2026-06-12); CI never refetches — offline
determinism. Ongoing freshness signals come from the watcher's daily run over the
registered `sub-agents` surface. On a material upstream change a human re-captures
here, regenerates `projection.json`, and reconciles the cross-check expectations — the
LLM never authors a kernel schema edit and never closes the deterministic drift signal.
Normative spec for this directory:
`000-docs/059-AT-SPEC-agent-definition-deep-capture-2026-06-12.md`.
