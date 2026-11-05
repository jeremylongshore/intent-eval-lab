<!-- GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state (watcher-liveness state + surface registry + lineage coverage map + drift baselines). Regenerate: python3 scripts/detector-health.py. Normative spec: 000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md -->

# Detector health

## Verdict: DEGRADED

Failing condition(s) first:

- **FAIL** `no-fetch-error-streaks` — effectively unmonitored (fetch_error_streak >= 3): anthropic-engineering (streak=7)
- ok `watcher-run-recent` — last successful watcher run 2026-11-05T17:17:02Z was 0.0h ago (max gap 26h)
- ok `coverage-at-target` — 16/16 registered surfaces monitored (100.0% of target 100%)

Lineage: 11 surfaces adopted, 12 divergences outstanding, 0 convergence triggers fired. Evaluated at 2026-11-05T17:17:06Z.

## Drift table (per registered surface)

| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |
|---|---|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | `bf4137a70201…` | 0 | yes | 7 |
| anthropic-engineering | cross-cutting-signal | yes | `f99507064aeb…` | 7 | — | 0 |
| claude-code-changelog | version-signal | yes | `cd5d1dc88811…` | 0 | — | 0 |
| claude-code-npm | version-signal | yes | `81bfdf038582…` | 0 | — | 0 |
| claude-code-releases | version-signal | yes | `556b4faba702…` | 0 | — | 0 |
| claude-hooks | hook-config | yes | `54d66bf143d8…` | 0 | yes | 1 |
| claude-settings | hook-config | yes | `448f49ae3a98…` | 0 | yes | 0 |
| claude-slash-commands | skill-frontmatter | yes | `977bb9f8d6a0…` | 0 | — | 0 |
| mcp-releases | mcp-config | yes | `1b180712c47f…` | 0 | yes | 0 |
| mcp-schema-ts | mcp-config | yes | `b2d3a00d4094…` | 0 | yes | 1 |
| mcp-spec-docs | mcp-config | yes | `ed815353d1d3…` | 0 | yes | 0 |
| platform-skills-overview | skill-frontmatter | yes | `72e111d404c2…` | 0 | yes | 0 |
| plugin-marketplaces | marketplace-catalog | yes | `2b353a0f227f…` | 0 | yes | 1 |
| plugins-reference | plugin-manifest | yes | `b0f8e2f9c1e5…` | 0 | yes | 1 |
| skills-releases | skill-frontmatter | yes | `8ab0fc2a54fa…` | 0 | yes | 0 |
| sub-agents | agent-definition | yes | `db8a532d4c04…` | 0 | yes | 1 |
