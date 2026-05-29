# Spec drift snapshots

Committed baseline hashes for the 6 upstream spec sources monitored by `.github/workflows/spec-drift-watch.yml`. Each `.sha/<source>.sha` file is the SHA-256 of the extractor output defined in `scripts/spec-drift-check.sh` at the moment the baseline was sealed.

**Authority**: `000-docs/030-AT-DECR-eval-set-bootstrap-decisions-2026-05-28.md` § 6.

## Why this exists

Per DR-029 § 6 and Agent 5's finding during the eval-set bootstrap scope research: the Skill Refiner Phase A.0 baseline measurement is only interpretable if upstream spec sources are pinned. Without a drift anchor, any Refiner score delta is indistinguishable from upstream spec change. These `.sha` files + the daily-cron workflow are the anchor.

## Sources monitored

| Snapshot file | Source | Extractor logic |
|---|---|---|
| `.sha/claude-code-changelog.sha` | `raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md` | Hash of raw GitHub CHANGELOG.md (upstream source of the published `code.claude.com/docs/en/changelog` page) |
| `.sha/claude-code-npm.sha` | `npm view @anthropic-ai/claude-code version` | Raw version string |
| `.sha/platform-skills-overview.sha` | `platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md` | Mintlify `.md` shim (raw markdown — deterministic) |
| `.sha/anthropic-engineering.sha` | `anthropic.com/engineering` | First `<a href="/engineering/<slug>">` (top article sentinel) |
| `.sha/skills-releases.sha` | `github.com/anthropics/skills/{releases,commits/main}.atom` | Concatenation of latest `<id>` from both feeds |
| `.sha/agentskills-spec.sha` | `agentskills.io/specification.md` | Mintlify `.md` shim |

## How to use

```bash
# Check current state vs committed baselines (exit 1 on drift)
scripts/spec-drift-check.sh

# Seed a missing baseline (won't overwrite existing)
scripts/spec-drift-check.sh --init

# Overwrite ALL baselines with current state (use after acknowledging drift)
scripts/spec-drift-check.sh --refresh

# Emit JSON report (for CI consumption)
scripts/spec-drift-check.sh --json
```

## When drift fires

The workflow opens a GitHub issue labeled `spec-drift` + `refiner` and (if `NTFY_URL` secret is configured) fires a push notification to the `prod-alerts` topic. The acting CTO triages per DR-029 § 6:

1. **Material drift** (spec semantics changed) — update local snapshot at `claude-code-plugins/000-docs/*-snapshot.md`, update eval-set `manifest.json` `skill_md_spec_version` pin, refresh baseline.
2. **Extractor flake** (cookie banner / build ID / etc.) — tighten extractor in `scripts/spec-drift-check.sh`, refresh baseline.
3. **Fetch error** (upstream 404 / network) — not counted as drift; logged for inspection.

## Refresh policy

- **Routine drift** (e.g., new Claude Code minor release): refresh in the same PR that updates downstream snapshots + manifests.
- **No standalone "refresh the baseline" PRs** — every refresh must cite the upstream change being acknowledged.
- **`anthropic-engineering` sentinel** rotates fastest (new blog post → drift). Treat as low-severity unless the post touches skill/plugin/MCP/agent-skills surface.

## CI side effects (not in extractor — workflow-only)

| Event | Effect |
|---|---|
| Scheduled run + drift | ntfy push (if `NTFY_URL` secret set) + GH issue + workflow fails red |
| Manual `workflow_dispatch` + drift | Workflow fails red; no issue / no ntfy (manual run is a check, not an alert) |
| PR touching the script or `.sha/` files + clean check | Workflow green; self-test passes |
| PR or run + drift | Workflow fails; surfaces in PR status checks |
