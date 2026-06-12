# `specs/_vendor/upstream/mcp-config/` — vendored upstream source (the firewall)

The **single vendored source of record** for the `mcp-config` authoring contract's
upstream truth — the second contract to get the deep capture skill-frontmatter has
(`_vendor/upstream/skill-frontmatter/`), and the first whose primary upstream is truly
machine-readable (the MCP `schema.json`). Upstream is captured here deterministically;
the deterministic extractor reads only; nothing downstream writes into this directory.

**Do not hand-edit the snapshots to encode IS policy.** IS policy lives in the kernel
overlay (`@intentsolutions/core` `schemas/authoring/v1/is-overlay/mcp-config.v1.json`).
This directory holds only what upstream says.

## Contents

| File | What |
|---|---|
| `mcp-schema-2025-11-25.json` | The official MCP JSON schema for the CURRENT spec revision (2025-11-25, per the spec's versioning page), fetched commit-pinned from the `modelcontextprotocol/modelcontextprotocol` repo. The machine-readable anchor. |
| `claude-code-mcp.md` | The Claude Code MCP doc page (`code.claude.com/docs/en/mcp.md`) — the authority for the `.mcp.json` per-server config shape (`command`/`args`/`env`/`type`), which the protocol schema deliberately does not define. |
| `vendor-meta.json` | Exact source URL + sha256 + bytes + `fetched_at` per file (052-AT-SPEC vendor-meta conventions, contract-keyed). |
| `projection.json` | The **normative projection** extracted deterministically by `scripts/extract-mcp-projection.py` — the field-diff left-hand side for FF#2 on this contract. Regenerate: `python3 scripts/extract-mcp-projection.py --write`. Never hand-edit (CI `--check` fails on staleness). |

## Authorities (precedence per `specs/upstream-surface-registry.v1.json`)

1. `schema/2025-11-25/schema.json` (modelcontextprotocol repo) — official-spec-machine-readable.
2. `modelcontextprotocol.io/specification/2025-11-25` — the normative prose spec (transports live here, not in the schema).
3. `code.claude.com/docs/en/mcp.md` — Anthropic doc; the spec for the `.mcp.json` server-config keys.

## Refresh mechanism

The fetch happened ONCE at build time (2026-06-12); CI never refetches — offline
determinism. Ongoing freshness signals come from the watcher's daily run over the
registered surfaces (`mcp-schema-ts`, `mcp-spec-docs`, `mcp-releases`). On a material
upstream change a human re-captures here, regenerates `projection.json`, and reconciles
the cross-check expectations — the LLM never authors a kernel schema edit and never
closes the deterministic drift signal. Normative spec for this directory:
`000-docs/056-AT-SPEC-mcp-deep-capture-and-projection-contract-2026-06-12.md`.
