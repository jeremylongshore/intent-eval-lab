# AgentSkills.io Open Standard Spec — Snapshot

**Fetched:** 2026-05-28
**Authority:** WebFetch against https://agentskills.io/specification
**Spec version (canonical citation):** `agentskills.io/v1.0` (no embedded version field; date-anchored)
**Plan reference:** AC-11 (agentskills.io spec compliance); SkillVersion `skill_md_spec_version` field; § 2.5 SkillMD Avenue
**Local-canonical mirror:** also written to `~/000-projects/claude-code-plugins/000-docs/agentskills-spec-snapshot.md` per § 2.5 canonical URL inventory

## Directory structure (normative)

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional executable code
├── references/       # Optional documentation
├── assets/           # Optional templates, resources
└── ...               # Any additional files
```

## Frontmatter — complete field table

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | 1-64 chars; `[a-z0-9-]+` only; no leading/trailing hyphen; no consecutive hyphens (`--`); must match parent directory name |
| `description` | Yes | 1-1024 chars; non-empty; describes what + when |
| `license` | No | License name or reference to bundled license file |
| `compatibility` | No | 1-500 chars; environment/product/system-package requirements |
| `metadata` | No | Map from string keys to string values; vendor-namespaced recommended |
| `allowed-tools` | No | Space-separated string; **marked EXPERIMENTAL** in spec |

**Total open-standard surface: 6 fields (2 required + 4 optional).**

## Fields NOT in the open standard (Claude Code / Anthropic extensions)

These are NOT in agentskills.io v1.0; they are Claude Code / Anthropic spec extensions:

- `disallowed-tools` — Claude Code only (per code.claude.com/docs/en/skills)
- `argument-hint` — Claude Code only
- `disable-model-invocation` — Claude Code only
- `model` — Claude Code only
- `context` — Claude Code only
- `agent` — Claude Code only
- `effort` — Claude Code only
- `hooks` — Claude Code only

**Critical implication for SAK § 14:** the D4 patch adds `disallowed-tools` at the **Claude Code extension tier**, NOT at the open-standard tier. Kernel `authoring/v1/skill-frontmatter.schema.json` § 14.10 tier model must position it accordingly:

- Standard tier: `name` + `description` only
- agentskills.io open-standard tier: 6 fields above
- Claude Code tier: open standard + Claude Code extensions (including `disallowed-tools`)
- IS marketplace tier: Claude Code tier + IS-only extensions (`version`, `author`, `tags`, visibility fields, env-vars, `metadata.intent-solutions.config`, etc.)

## Progressive disclosure (3-tier)

| Tier | Token cost | When loaded |
|---|---|---|
| Metadata (`name` + `description`) | ~100 | At startup |
| Instructions (SKILL.md body) | <5000 recommended | When skill activated |
| Resources (`scripts/`, `references/`, `assets/`) | Effectively unlimited | As needed |

## Validation reference

Open-standard validator: https://github.com/agentskills/agentskills/tree/main/skills-ref — `skills-ref validate ./my-skill`

## Plan-binding implications

| Plan citation | What it claims | Verification |
|---|---|---|
| § 2.5 fold-in #1 (AC-11) | "respect `agentskills.io/specification` frontmatter requirements: required `name` + `description`, optional `allowed-tools`, `disallowed-tools`, `model`, `version`, `author`, `license`, `compatibility`, `tags`" | ⚠️ NEEDS CORRECTION: `disallowed-tools`, `model`, `version`, `author`, `tags` are NOT in agentskills.io v1.0. Only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are. The plan conflated open-standard + Claude-Code-extension + IS-marketplace tiers. Step 5 remediation needed. |
| § 2.5 spec version pinning | "`skill_md_spec_version: \"agentskills.io/v1.0.0\"`" | ✅ DEFENSIBLE — citing as `agentskills.io/v1.0` (no patch version in spec itself; date-anchored snapshot at 2026-05-28) |
| § 14.10 tier model | "Standard floor 2 fields; agentskills.io 2 req + 4 opt = 6 total" | ✅ VERIFIED — fully matches spec |
| § 14.10 anti-realignment guard | "kernel encodes the IS enterprise position, not the upstream floor" | ✅ VERIFIED as compatible — open-standard surface is strict subset of IS marketplace tier |

## Snapshot freshness

Quarterly refresh per § 13 Step 9. Next refresh due: **2026-08-26**. Drift triggers a bd memory + new SkillVersion records carry refreshed version.

## Disposition

Step 0 directive 2 ("Refresh agentskills.io spec snapshot") — COMPLETE.

— Jeremy Longshore
intentsolutions.io
