<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: DEGRADED

Failing condition(s) first:

- **FAIL** `watcher-run-recent` — last successful watcher run 2026-10-01T09:24:18Z was 59.5h ago (max gap 26h)
- ok `no-fetch-error-streaks` — all 16 tracked surfaces under the streak threshold (3)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-10-03T20:55:04Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `4c649bdf0e0a…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 0 | — | 0 |
| claude-code-changelog | version-signal | yes | `c2073a2eb811…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `5fef7bd6468e…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `755e30355fb8…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `41ea72eb3294…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `efdc415213d8…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `b2d3a00d4094…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `82e9c63ce6ba…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `acc3a81d482f…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `0597250fec9a…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `45289e551da9…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `436c792e8739…` | 0 | yes | 1 |
