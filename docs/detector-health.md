<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: DEGRADED

Failing condition(s) first:

- **FAIL** `no-fetch-error-streaks` — effectively unmonitored (fetch_error_streak >= 3): anthropic-engineering (streak=19)
- ok `watcher-run-recent` — last successful watcher run 2026-11-21T09:12:04Z was 0.0h ago (max gap 26h)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-11-21T09:12:06Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `bf4137a70201…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 19 | — | 0 |
| claude-code-changelog | version-signal | yes | `5469fbb7031b…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `865a5d6594f0…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `f5e1117b35f0…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `d94a7f2f3ef9…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `12bb7fba1386…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `c32f196e7a84…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `c9edf8b0e772…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `dce8b5351ae0…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `e4549a3fb8c2…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `6d2d7ad4b87c…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `0391a8fbdc9d…` | 0 | yes | 1 |
