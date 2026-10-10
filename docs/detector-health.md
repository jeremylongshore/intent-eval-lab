<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: HEALTHY

All composite-predicate conditions pass:

- ok `watcher-run-recent` — last successful watcher run 2026-10-10T09:20:34Z was 0.0h ago (max gap 26h)
- ok `no-fetch-error-streaks` — all 16 tracked surfaces under the streak threshold (3)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-10-10T09:20:40Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `4c649bdf0e0a…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 0 | — | 0 |
| claude-code-changelog | version-signal | yes | `0383b383e05c…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `e25db9bddfe9…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `ad56e03ba949…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `0da9be3c724c…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `3a4428d15e82…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `b2d3a00d4094…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `cb1b14a93603…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `d4ee7be3d550…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `0597250fec9a…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `16b6dafd91d4…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `8f2fd54755e3…` | 0 | yes | 1 |
