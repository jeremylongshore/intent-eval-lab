<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: HEALTHY

All composite-predicate conditions pass:

- ok `watcher-run-recent` — last successful watcher run 2026-07-23T09:54:05Z was 0.0h ago (max gap 26h)
- ok `no-fetch-error-streaks` — all 16 tracked surfaces under the streak threshold (3)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-07-23T09:54:06Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `9d770de8f1b0…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 0 | — | 0 |
| claude-code-changelog | version-signal | yes | `1ef5cb06ed90…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `8c12dd45ecf0…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `0b644e2208f8…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `491b623ae274…` | 0 | yes | 0 |
| claude-slash-commands | slash-commands | yes | `d7d367c7d004…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `1bf94a601817…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `9afb71b14f68…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `0bd9758afca5…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `1f37e87ff344…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `bbb4618ec8b1…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `824162201ae4…` | 0 | yes | 1 |

<!-- CI re-run kick after rebase onto main (lab#243) -->
