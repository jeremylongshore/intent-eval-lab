<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: HEALTHY

All composite-predicate conditions pass:

- ok `watcher-run-recent` — last successful watcher run 2026-10-17T09:17:44Z was 0.0h ago (max gap 26h)
- ok `no-fetch-error-streaks` — all 16 tracked surfaces under the streak threshold (3)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-10-17T09:17:47Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `4c649bdf0e0a…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `5d91ddc3f5b6…` | 0 | — | 0 |
| claude-code-changelog | version-signal | yes | `57fde96b3318…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `3eb862d89bf0…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `5599b94537be…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `a8cc395af5e0…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `428fdf2654fa…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `b2d3a00d4094…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `13340f19438b…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `d4ee7be3d550…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `0597250fec9a…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `16b6dafd91d4…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `2ef84ba68898…` | 0 | yes | 1 |
