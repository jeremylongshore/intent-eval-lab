<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: DEGRADED

Failing condition(s) first:

- **FAIL** `no-fetch-error-streaks` — effectively unmonitored (fetch_error_streak >= 3): anthropic-engineering (streak=4)
- ok `watcher-run-recent` — last successful watcher run 2026-10-24T13:14:09Z was 0.0h ago (max gap 26h)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-10-24T13:14:13Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `9a67de891329…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 4 | — | 0 |
| claude-code-changelog | version-signal | yes | `27d7a0e1d5c1…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `c7bd3bb68246…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `47ffc7990703…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `0b062367ed54…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `acb1f1388ee9…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `b2d3a00d4094…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `0a674a6a3442…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `3bfadf3faa98…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `8375e712c31d…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `3b72923e29d9…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `d66f847bed2c…` | 0 | yes | 1 |
