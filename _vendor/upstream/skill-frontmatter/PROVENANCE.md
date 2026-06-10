# `_vendor/upstream/skill-frontmatter/` — vendored upstream source (the firewall)

This directory is the **single vendored source of record** for the `skill-frontmatter`
authoring contract's upstream truth. It is the deterministic firewall in the
deterministic/probabilistic boundary (DR-044 + the 7-thinker panel, 2026-06-09): upstream is
captured here deterministically; the LLM classifier reads only; the deterministic differ is the
sole admission path toward the kernel.

**Do not hand-edit the snapshot to encode IS policy.** IS policy lives in the kernel overlay
(`@intentsolutions/core` `schemas/authoring/v1/is-overlay/skill-frontmatter.v1.json`). This
directory holds only what the upstream standard says.

## Contents

| File | What |
|---|---|
| `agentskills-spec-v1.0.md` | Vendored snapshot of the agentskills.io v1.0 open standard (captured 2026-05-28). The raw-fetch firewall copy. |
| `projection.v1.json` | The **normative projection** extracted from the snapshot — the field set + required/optional + types + deprecations. This is the extract-then-diff anchor (Kleppmann): the differ diffs *projections* field-by-field, not raw page bytes. The byte-hash in `specs/snapshots/.sha/agentskills-spec.sha` is demoted to a cheap "should we re-extract" tripwire. |

## Authorities (precedence: official spec > Anthropic's doc-about-it)

1. `https://agentskills.io/specification` — the open standard Claude Code follows (PRIMARY for skills).
2. `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` + `/best-practices`.
3. `https://code.claude.com/docs/en/skills` — Claude Code extension fields.
4. Deep prose capture: `claude-code-plugins/000-docs/6767-b-SPEC-DR-STND-claude-skills-standard.md` §4.

## Refresh mechanism

`scripts/spec-drift-check.sh` (byte-hash tripwire) + `scripts/spec-projection-diff.py` (field-level
extract-then-diff against `projection.v1.json`). On semantic drift the differ opens a reconciliation
issue; a human promotes the change into the kernel (the LLM never authors a kernel schema edit and
never closes the deterministic drift signal). Next quarterly refresh due 2026-08-26.

## Scattered-copy collapse (tracked bead)

Four agentskills.io copies + two anthropic-skills copies exist across repos and have already
diverged (`intent-eval-lab/research` 2026-05-28 vs the `claude-code-plugins` copies 2026-05-07).
This `_vendor/` is the designated single source they collapse into — tracked by the "collapse
scattered shadow copies" bead under the Continuous Spec-Compliance epic.
