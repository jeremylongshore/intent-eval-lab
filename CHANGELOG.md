# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Pending

- Phase B research-eval methodology work (gated on Phase B bandwidth-only kickoff per DR-010 § 13.5)
- ISEDC Session 7 (cadence TBD; agenda to include thinker-panel findings synthesis per AAR 023)
- bd memories backfill from 22 DRs + 4 AACRs — `bd_000-projects-tyck` (P1, Cunningham finding)
- DR status-banding + post-decision-learnings appendix convention rollout — `bd-` queued (P2, Cunningham findings)

## [0.2.0] - 2026-05-26

**Phase A foundation complete.** This release packages the constitutional documents (Blueprints A/B/C + Canonical Glossary), six ISEDC Decision Records establishing widened-scope governance, the IEP Convergence Debt Plan execution chain, partner-name CI hardening, the first cross-repo /appaudit baseline, four Phase B research artifacts, and the IEP thinker-canon adversarial panel review.

### Added

#### Phase A foundation (NORMATIVE — every downstream consumer references these)

- **Blueprint A** — `000-docs/011-AT-ARCH-ecosystem-master-blueprint.md` — the constitution; 12 binding principles, 5-repo taxonomy, anti-goals, governance routing (`iel-E01`, #52)
- **Blueprint B** — `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` — runtime architecture, 13-entity canonical domain model, `gate-result/v1` NORMATIVE predicate spec at § 7 (`iel-E02`, #53)
- **Blueprint C** — `000-docs/013-AT-SPEC-repo-blueprint-template.md` — reusable per-repo blueprint template (`iel-E04`, #55)
- **Canonical Glossary** — `000-docs/014-DR-GLOS-canonical-glossary.md` — single source of truth for platform terminology (`iel-E03`, #54)

#### ISEDC governance corpus

- **DR-010** Session 4 widened-scope architectural lock (`000-docs/010-AT-DECR-...`, #50) — Q1 ONE BIG; Q2 hybrid (TS-primary signing surfaces, Python permitted ML internals); Q3 unification thesis BINDING; § 13.5 customer-signal gate REMOVED; § 13.6 external-pattern non-borrow
- **DR-018** Session 5 j-rig reconciliation (`000-docs/018-AT-DECR-...`) — 7-seat adversarial council, acting head Claude per CEO-mode delegation, 4 ratified decisions including `@j-rig/*` v2.0.0 major bump + STAGING-STAYS-STAGING for v0.1.0-draft attestations + kernel `EvidenceBundlePayload` Option α-minus
- **DR-021** `iah-E02` scope clarified, deferred to `iah-E04` (`000-docs/021-AT-DECR-...`, #68) — "a codemod with nothing to mod is not a task"
- **DR-022** Session 6 beads re-engage — DECIDED + EXECUTED + INVERTED-BY-EMPIRICAL-FINDING (`000-docs/022-AT-DECR-...`, #69) — verify-before-claim discipline born from this session
- ISEDC Session 3 — Phase B gate re-eval + ecosystem signal response (filed pre-DR-numbering)

#### IEP Convergence Debt Plan execution

- **Kernel shadow inventory** (`000-docs/016-RR-LAND-kernel-shadow-inventory-2026-05-20.md`, #64)
- **Shape reconciliation addendum** (`000-docs/017-RR-LAND-shape-reconciliation-addendum-2026-05-21.md`)
- **Schema repoint to kernel canonical** per DR-018 § 6.4 Option α-minus (`000-docs/019-AA-AACR-schema-repoint-iel-link-schemas-2026-05-21.md`, #65) — lab schema replaced with redirect stub (`$ref` to kernel + `x-redirect` marker); Blueprint B § 7.0 "Schema authority" added; `.github/workflows/schema-drift.yml` CI gate enforces structurally
- **Harness-hash self-pin rollout** with audit-harness v1.1.1 re-vendor (`000-docs/020-AA-AACR-harness-hash-rollout-lab-2026-05-22.md`, #67)
- audit-harness re-vendors: v1.1.1→v1.1.2 Phase A1 shellcheck hard-fail + bonus awk counter fix (#70); v1.1.2→v1.1.3 Phase A2 ruff CI gate (#71); v1.1.3→v1.1.4 cleanup bundle of 4 deferred fixes (#72)

#### Phase B research deliverables (NEW IN THIS RELEASE)

- **Phase B gap analysis + research framework** — `research/000-DR-FIND-iep-phase-b-gap-analysis-and-research-framework-2026-05-20.md` + `.pdf` (60-100pg findings, 172 KB markdown, 282 KB PDF). Audits 20 strategic AI-infrastructure areas surfaced in two advisory rounds, plus one uniquely accessible area (evaluator-disagreement dataset), against current state of IEP. Craft-and-contribution-focused: where the field stands, where we technically fall short, where an obsessive operator with infrastructure expertise can contribute upstream or push the field forward.
- **Shared bibliography** — `research/000-RR-BIBL-shared-bibliography-2026-05-20.md` — ≈148 Semantic Scholar papers across 16 seed queries spanning the 21 advisory gap areas. Tier-1 (≥100 citations), Tier-2 (30-99), Tier-3 (10-29); cluster tags map to the 5-team research framework.
- **Ecosystem landscape audit** — `research/000-RR-COMP-ecosystem-landscape-2026-05-20.md` — verbatim project-state capture (WebFetch 2026-05-20) of 12 OSS projects + 7 frontier labs. Craft-contribution audit, not competitive scan: where to **contribute upstream** vs **build in our repos** vs **skip because well-covered**.

#### Spec foundation

- **Evidence Bundle SPEC normative** — `specs/evidence-bundle/v0.1.0-draft/` (M1 spec work, full schema + examples + M1 docs, #M1)
- IEP system brief — full architecture journey HTML
- `research/README.md` — Master Reading List (clickable index of 150+ sources)

#### Cross-cutting

- **First IEP /appaudit baseline** (`000-docs/015-AA-AUDT-appaudit-devops-playbook.md` + `.pdf`, #63) — operator-grade devops playbook
- **IEP thinker-canon adversarial panel review AAR** — `000-docs/023-AA-AACR-thinker-panel-review-2026-05-25.md` (#73) — 6-seat panel (Kleppmann, Hickey, Fowler, Beck, Gregg, Cunningham), ~28 findings preserved verbatim, synthesis matrix, 9+ new beads filed including 3 P0s (Evidence Bundle compat policy, OTel semconv pin, Release CI alerting)
- **Cross-references for intent-rollout-gate** as 4th repo (M4) added across lab artifacts (#31)
- **Terminology rename**: matcher-map → Intentional Mapping per ISEDC v2 (commit `0ba4f76`)

### Changed

- **CI**: Node-based CI replaced with docs-validation; CodeQL dropped — lab is doc-only, not code (#32)
- **CI**: `release.yml` cleanup — `workflow_dispatch` only, removed push-to-main trigger; subsequently removed redundant workflow entirely (/release skill is canonical for this repo)
- **Partner-name vendor-generic CI guard** — `.github/workflows/partner-name-guard.yml` fires on every PR + push to main with case-insensitive grep (per DR-004 S1Q2 BINDING)
- `CHANGELOG.md` — restructured to Keep-a-Changelog 1.1.0 format (#74, Tidy First per Beck thinker-panel finding #5)

### Fixed

- **Audit cleanup PR #56** — partner-name vendor-generic scrub + canonical repo-name fixes (`j-rig-binary-eval` → `j-rig-skill-binary-eval` in GH-public refs) + 2 fact-citation corrections + `KNOWN-ISSUES.md` for operational footnotes that don't belong in the normative glossary

### Security

- Partner-name CI guard ratchets DR-004 S1Q2 BINDING into enforcement: case-insensitive grep against `Kobiton|Polygon|Nixtla|Lit Protocol|Mudit Gupta|Mudit` returns 0 hits or CI fails. Pattern enumerated in PRIVATE umbrella CLAUDE.md only.
- Schema-drift CI gate prevents structural drift between lab's redirect-stub schema and kernel canonical
- Harness-hash discipline lands in lab via vendored `.audit-harness/v1.1.4` (escape-scan + arch + harness-hash via hooks + GitHub Actions)

### Architectural bindings

- [DR-010](./000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md) — ISEDC Session 4 widened-scope lock (BINDING)
- [Blueprint A](./000-docs/011-AT-ARCH-ecosystem-master-blueprint.md) — 12 binding principles
- [Blueprint B](./000-docs/012-AT-ARCH-platform-runtime-blueprint.md) — runtime architecture + 13-entity domain model + `gate-result/v1` NORMATIVE spec
- [Blueprint C](./000-docs/013-AT-SPEC-repo-blueprint-template.md) — repo template (applied to all 5 IEP sub-repos)
- [Canonical Glossary](./000-docs/014-DR-GLOS-canonical-glossary.md) — single source of truth for terminology

### Dependencies

- GitHub Actions group bump (#33)

## [0.1.0] - 2026-05-10

First public release of the Intent Eval Lab repository — the methodology + specs umbrella for the Intent Eval Platform.

### Added

- Initial repository scaffold (`/repo-dress` 21-file canon, 8 governance files)
- Enterprise documentation set (6-doc planning suite)
- `README.md`, `LICENSE` (Apache 2.0), `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`
- CI/CD workflows (`lint.yml`, `test.yml`, release automation)
- GitHub issue templates + PR template
- Dependabot configuration
- `.editorconfig` + `.gitattributes`
- Beads issue tracking initialized at repo scope
- `specs/` Phase A convergence skeleton — Evidence Bundle skeleton + OpenTelemetry RFC draft (`000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`)
- `specs/mcp-plugin-observability/` reference module (Go as planned reference runner)
- Normative methodology output tree under `specs/`

### Changed

- `CLAUDE.md` — added three-repo convergence section + partner-name vendor-generic discipline (per DR-004 S1Q2)
- `CLAUDE.md` — clarified tier-1 (Evidence-Bundle-composing platform) vs tier-2 (independent lab research) constituent project distinction
- `CLAUDE.md` — updated absolute paths after move into `intent-eval-platform/` umbrella
- Part 2 ecosystem landscape report + Workstream-D synthesis + first ISEDC Decision Record

### Fixed

- `/validate-consistency` audit fixes — INDEX stale entries, README j-rig claim drift, PB-12 DR mapping

[Unreleased]: https://github.com/jeremylongshore/intent-eval-lab/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.1.0
