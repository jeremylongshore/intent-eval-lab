<!-- GENERATED-DO-NOT-EDIT — SAK dashboard derived from committed state (SAK-STATE.json + leading-indicators registry + lineage coverage map). Regenerate: python3 scripts/render-sak-dashboard.py. Normative spec: 000-docs/033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md § 14.13.1 -->

# SAK Dashboard — generated 2026-07-04T12:00:00Z

State as of 2026-06-20. This file is DERIVED — never hand-edit it.

## Phase status

- **Phase 0 — D4 wedge**: COMPLETE — skill-frontmatter walking skeleton (base + overlay + composition) landed; deep-capture -> base/overlay schema -> drift-watch -> classify -> reconcile pattern exists end-to-end
- **Phase 1 — six contracts + P0 safety spine**: IN PROGRESS — P0 safety spine COMPLETE (8/8 backbone children closed 2026-06-12): typed fetch-failure taxonomy + 3 append-only tiers (doc 052), frozen drift-classification/v1 eval set with recall-floor write gate (doc 053), append-only lineage log + derived coverage map (doc 054), deterministic classifier walls (doc 055), 6767-h prose-anchor validity gate, watcher waves 1+2 + FF#2. P1 siblings (.9-.13) remain
- **Phase 2 — internal-validator canary cutover**: BLOCKED — first of three staged consumer cutovers (.14 internal validators -> .15 j-rig -> .17 CCP, blast-radius ascending); gated behind the Phase 1 P1 siblings
- **Phase 4 — advisory -> blocking flip**: BLOCKED — CCP authority-flip soak window NO-GO as of 2026-06-18 (1.16% deviation); matures ~2026-07-11; requires CTO+CISO+VP-DevRel triple sign-off + ISEDC Class-1 charter (044-AT-DECR)

## State machine

- Machine: SAK advisory -> blocking flip (Phase 4)
- Current state: **ADVISORY** (entered 2026-06-09)
- States: ADVISORY -> ADVISORY-W-A -> ADVISORY-W-AB -> SHADOW-MODE -> HOLDING -> READY-TO-FLIP -> BLOCKING -> ROLLED-BACK
- Next gate: CCP authority-flip soak >= 99.5% / >= 30d / zero-P0 / rollback-rehearsed / triple sign-off / 14d notice (DR-049); soak matures ~2026-07-11

## Leading indicators

- 12 monitored | 0 firing (CRITICAL 0, High 0, Medium 0, Low 0)
- Disposition: **CONTINUE** — Continue per plan

| # | Indicator | Severity | Firing |
|---|---|---|---|
| 1 | Anthropic publishes public roadmap including machine-readable spec | High | — |
| 2 | claude CLI begins ingesting .claude/schema/ directory | High | — |
| 3 | claude doctor adds plugin-format validation | High | — |
| 4 | agentskills.io v2 RFC published | High | — |
| 5 | Anthropic publishes machine-readable agentskills.io v2 schemas | CRITICAL | — |
| 6 | Anthropic ships skill-author-onboarding doc citing field validation | Medium | — |
| 7 | claude-codemod or equivalent field-migration tool ships | Medium | — |
| 8 | Anthropic ships skill-shell-validation | Medium | — |
| 9 | Anthropic ships skill-security-audit | Medium | — |
| 10 | agentskills.io spec adds vendor-namespacing section | Low | — |
| 11 | Vercel skills.sh adopts kernel-schema-compatible format | Low | — |
| 12 | Frontier model demonstrates schema-validator equivalence from prose+examples | CRITICAL | — |

## Cost ledger

- Total budget: 8.8 FTE-week (~3 calendar months (with phase-gating + sync overhead))

| Phase | Budget (FTE-days) | Spent (FTE-days) | Gated on |
|---|---|---|---|
| Phase A.0 null-hypothesis baseline | 3.5 | 0.0 (0.0%) | bandwidth-only |
| Phase A | 11.5 | 0.0 (0.0%) | bandwidth-only |
| Phase B | 9.5 | 0.0 (0.0%) | bandwidth-only |
| Phase C | 15.0 | 0.0 (0.0%) | external blockers uprg + 9pi3 |
| Phase E | 4.5 | 0.0 (0.0%) | bandwidth-only |

## Bead state

SAK / Skill-Refiner bead subtree (epic `9k5h`); captured 2026-06-20.

| Label group | Open | In progress | Deferred | Closed |
|---|---|---|---|---|
| `sak` | 23 | 0 | 1 | 0 |
| `refiner` | 62 | 0 | 1 | 0 |
| `repo:iel` | 15 | 0 | 1 | 0 |

## Coverage map state

- 11/16 upstream surfaces adopted | 12 divergences outstanding | 12 convergence triggers outstanding | 0 convergence triggers fired

| Surface | Contract | Adopted | Divergences outstanding | Convergence triggers outstanding |
|---|---|---|---|---|
| agentskills-spec | skill-frontmatter | yes | 7 | 7 |
| anthropic-engineering | cross-cutting-signal | NO | 0 | 0 |
| claude-code-changelog | version-signal | NO | 0 | 0 |
| claude-code-npm | version-signal | NO | 0 | 0 |
| claude-code-releases | version-signal | NO | 0 | 0 |
| claude-hooks | hook-config | yes | 1 | 1 |
| claude-settings | hook-config | yes | 0 | 0 |
| claude-slash-commands | slash-commands | NO | 0 | 0 |
| mcp-releases | mcp-config | yes | 0 | 0 |
| mcp-schema-ts | mcp-config | yes | 1 | 1 |
| mcp-spec-docs | mcp-config | yes | 0 | 0 |
| platform-skills-overview | skill-frontmatter | yes | 0 | 0 |
| plugin-marketplaces | marketplace-catalog | yes | 1 | 1 |
| plugins-reference | plugin-manifest | yes | 1 | 1 |
| skills-releases | skill-frontmatter | yes | 0 | 0 |
| sub-agents | agent-definition | yes | 1 | 1 |
