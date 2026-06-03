# agentskills.io Specification — Snapshot

**Source URL:** <https://agentskills.io/specification>
**Snapshot date:** 2026-05-27 (UTC; date provided by session metadata)
**Snapshot purpose:** Pin spec generation for Skill Refiner AC-11 + SkillVersion entity `skill_md_spec_version` field
**Refresh due:** 2026-08-27 (90 days)

## Frontmatter fields (canonical — verbatim from spec)

| Field           | Required | Constraints                                                                                                               |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 chars. Lowercase letters, numbers, hyphens only. Must not start/end with hyphen. Must match parent directory name. |
| `description`   | Yes      | Max 1024 chars. Non-empty. Describes what skill does and when to use.                                                     |
| `license`       | No       | License name or reference to bundled license file.                                                                        |
| `compatibility` | No       | Max 500 chars. Indicates environment requirements.                                                                        |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                                      |
| `allowed-tools` | No       | Space-separated string of pre-approved tools. **Experimental** — support varies between agent implementations.            |

**Total: 6 fields. 2 required, 4 optional.**

## Directory structure

```text
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files/directories
```

## Progressive disclosure model (3 levels)

1. **Metadata** (~100 tokens) — `name` + `description` loaded at startup for ALL skills
2. **Instructions** (< 5000 tokens recommended) — Full SKILL.md body loaded on activation
3. **Resources** — `scripts/` / `references/` / `assets/` loaded on demand

Recommended: SKILL.md body under 500 lines.

## Validation tool

Reference library: `skills-ref` at `github.com/agentskills/agentskills/tree/main/skills-ref`
Command: `skills-ref validate ./my-skill`
Checks: frontmatter validity, naming conventions.

## ★ Plan defect surfaced — AC-11 over-states the spec

The plan's AC-11 (§ 3, this doc's parent plan 027) lists 9 fields:

> "name, description, allowed-tools, disallowed-tools, model, version, author, license, compatibility, tags"

Of those 9:

- **6 are in the open standard**: `name`, `description`, `allowed-tools`, `license`, `compatibility`, plus `metadata` (which the plan omitted)
- **3 are Claude Code extensions, NOT open-standard**: `disallowed-tools`, `model`, plus `version`/`author`/`tags` which are properly placed _inside_ the `metadata` field, not as top-level keys

**Implication for Refiner:** the Refiner's edit grammar can produce + validate the 6 open-standard fields against this snapshot. For Claude Code extensions (`disallowed-tools`, `model`, frontmatter-extensions from `code.claude.com/docs/en/skills`), validate against the Claude Code snapshot separately. Plan AC-11 needs amendment in Step 5 of § 13 (remediation) — fold into Plan Audit (§ 12) as a Lamport-seat finding pre-emptively.

**Spec version identifier to use in SkillVersion records:**

- `skill_md_spec_version: "agentskills.io/v1.0-2026-05-27-snapshot"` (until the spec publishes a formal version string; the spec body does not currently declare a `v1.0.0` literal)

## Body content

No format restrictions. Recommended sections:

- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases

## Documentation index pointer

Full spec index: `https://agentskills.io/llms.txt`

## Plan AC-11 amendment proposal (pre-Plan-Audit)

Replace:

> "name + description, optional allowed-tools, disallowed-tools, model, version, author, license, compatibility, tags"

With:

> "name + description (REQUIRED per agentskills.io v1.0); optional license, compatibility, metadata (arbitrary kv), allowed-tools (EXPERIMENTAL per agentskills.io v1.0). Claude Code extensions (disallowed-tools, model, frontmatter-extensions) validated against the Claude Code skills snapshot at `claude-code-plugins/000-docs/anthropic-skills-spec-snapshot.md` separately."

— Snapshot author: Claude (acting CTO)
