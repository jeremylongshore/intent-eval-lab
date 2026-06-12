# 050 — Upstream-surface registry (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-11 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 030-AT-DECR § 6 · **Epic:** 9k5h (continuous-spec-compliance SSoT, GH intent-eval-lab#114)

## Purpose

The single registry of **upstream spec surfaces** the spec-drift watcher monitors for the kernel authoring family (`@intentsolutions/core` `schemas/authoring/v1`). It is the left-hand side of the coverage map: every contract the kernel governs must have its primary upstream surface watched, so a stale or restructured upstream cannot silently desync the kernel from the spec it claims to encode.

Machine-readable copy: [`specs/upstream-surface-registry.v1.json`](../specs/upstream-surface-registry.v1.json). The executable extractors live in [`scripts/spec-drift-check.sh`](../scripts/spec-drift-check.sh) (the `SOURCES` array). A consistency check — [`scripts/check-surface-registry.py`](../scripts/check-surface-registry.py) — asserts registry ≡ script `SOURCES` and that every registered extractor function exists. Wiring that check into the (harness-hash-pinned) drift-watch CI workflow, and having the script read this JSON directly rather than its DRY-duplicated `SOURCES`, are tracked follow-ups.

## Authority precedence (when surfaces conflict)

1. **official-spec-machine-readable** — e.g. the MCP `schema.ts`. Exact field-level diffing possible (the FF#2 proving ground).
2. **official-spec** — the normative source (`agentskills.io` for skills; `modelcontextprotocol.io` for MCP).
3. **anthropic-doc** — a Claude/Anthropic page *about* a spec; beaten by the official spec it describes.
4. **reference** — a Claude Code reference page; the spec itself for Claude-Code-only contracts (hooks, settings, slash-commands, sub-agents, plugin-manifest, marketplace) that have no separate open standard.
5. **release-feed** — a GH `releases.atom`; the earliest material-change signal, ahead of any page edit.
6. **changelog** — a CHANGELOG / npm version; detects *that* change happened, while the reference page is the spec.

## The 16 monitored surfaces

| Surface | Contract | Wave | Authority tier | Machine-readable |
|---|---|---|---|---|
| `agentskills-spec` | skill-frontmatter | 0 | official-spec | — |
| `platform-skills-overview` | skill-frontmatter | 0 | anthropic-doc | — |
| `skills-releases` | skill-frontmatter | 0 | release-feed | — |
| `mcp-schema-ts` | mcp-config | 1 | **official-spec-machine-readable** | ✅ |
| `mcp-spec-docs` | mcp-config | 1 | official-spec | — |
| `mcp-releases` | mcp-config | 2 | release-feed | — |
| `claude-hooks` | hook-config | 1 | reference | — |
| `claude-settings` | hook-config | 1 | reference | — |
| `claude-slash-commands` | slash-commands | 1 | reference | — |
| `plugins-reference` | plugin-manifest | 2 | reference | — |
| `sub-agents` | agent-definition | 2 | reference | — |
| `plugin-marketplaces` | marketplace-catalog | 2 | reference | — |
| `claude-code-changelog` | version-signal | 0 | changelog | — |
| `claude-code-npm` | version-signal | 0 | changelog | ✅ |
| `claude-code-releases` | version-signal | 2 | release-feed | — |
| `anthropic-engineering` | cross-cutting-signal | 0 | release-feed | — |

Every one of the 6 kernel authoring contracts (skill-frontmatter, plugin-manifest, agent-definition, mcp-config, hook-config, marketplace-catalog) has its primary upstream surface covered, plus slash-commands/settings and the version/release signals.

## Unmonitored candidates (Wave 3)

- **`claude-plugins-official`** (`github.com/anthropics/claude-plugins-official`) — marketplace.json manifests. The `plugin-marketplaces.md` reference page is the spec and IS monitored; add the repo's marketplace manifest if a sampleable raw file is identified.

## Change discipline

Adding/removing a surface = edit `spec-drift-check.sh` `SOURCES` **and** this registry + its JSON in the same change (`scripts/check-surface-registry.py` fails otherwise). Authority-tier or URL changes are normative and follow the same observance gate as any kernel-adjacent change.
