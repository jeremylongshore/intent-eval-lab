<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: DEGRADED

Failing condition(s) first:

- **FAIL** `no-fetch-error-streaks` — effectively unmonitored (fetch_error_streak >= 3): anthropic-engineering (streak=25)
- ok `watcher-run-recent` — last successful watcher run 2026-11-27T18:49:24Z was 0.0h ago (max gap 26h)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-11-27T18:49:27Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `bf4137a70201…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 25 | — | 0 |
| claude-code-changelog | version-signal | yes | `4192cfdae7e1…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `f0443805839e…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `d16003851f60…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `7587a3251756…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `3de6c6acc4b9…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `8cf7e2b82126…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `f572759aa8b6…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `dce8b5351ae0…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `7b17c2956657…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `bcd6278cef41…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `9e223cb6656a…` | 0 | yes | 1 |
