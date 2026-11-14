<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: DEGRADED

Failing condition(s) first:

- **FAIL** `no-fetch-error-streaks` — effectively unmonitored (fetch_error_streak >= 3): anthropic-engineering (streak=12)
- ok `watcher-run-recent` — last successful watcher run 2026-11-14T09:11:39Z was 0.0h ago (max gap 26h)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-11-14T09:11:44Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `bf4137a70201…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 12 | — | 0 |
| claude-code-changelog | version-signal | yes | `162c169ef621…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `b7d63e8799e5…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `a8e9ba49520d…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `bc72fdd5dc45…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `8bc8fae653e4…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `d1c5f24bc137…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `2194e4db0795…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `2828b4387257…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `6220dc0a4ae8…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `f5d88a52b3bf…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `00bda45456b2…` | 0 | yes | 1 |
