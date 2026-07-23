# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Post-0.3.0 work: continuous-spec-compliance / Spec Authority Kernel (SAK) skeleton, the 6-contract upstream deep-capture program, the spec-drift upstream-surface registry, governance hash-chaining, the IEP PR-review-gate policy, CI-integrity false-green fixes, the tag-triggered release evidence lane, and the end-to-end 5-repo integration test framework.

### Added

#### Spec-currency loop repair (2026-07-22/23) — residual closed

Platform epics intent-solutions-io/intent-eval-platform#10 / #17 closed after:

- Freshness-mode extractors, fail-closed surface contracts, baseline stale-streak
  alert ([#237](https://github.com/jeremylongshore/intent-eval-lab/pull/237)–[#244](https://github.com/jeremylongshore/intent-eval-lab/pull/244)).
- Wave-1 kernel fold disposition: agent-definition `tools_inherit` phrasing =
  extractor fix only ([#243](https://github.com/jeremylongshore/intent-eval-lab/pull/243));
  no bulk authoring/v1 re-vendor (platform #16 closed as process established).
- Reviewer posture: both AI reviewers dark; CI is the only merge gate
  ([#233](https://github.com/jeremylongshore/intent-eval-lab/pull/233)).
- Kernel skew documented as by design for the shadow detector
  ([#231](https://github.com/jeremylongshore/intent-eval-lab/pull/231)).

Downstream: CCPI required `skill-conform` (#1118); j-rig roster 14 (#234).

#### Cross-repo CI/CD remediation — the stranded j-rig-cli release + gate hygiene

Executes `000-docs/106-PP-PLAN-cicd-jrig-cross-repo-remediation-2026-07-01.md`
(full send A+B+C+D). The session's hardening work + four merged j-rig fixes
(#172–#175) were stranded in `main`, unpublished, so `claude-code-plugins`
skill evals still hit the judge-truncation (#175) + reasoning-model
`max_tokens` (#173) bugs that inflate false NO-SHIP (the Xquik dogfood,
`693-AA-AACR`).

- **The core fix.** Cut `@intentsolutions/jrig-cli@0.1.2` (j-rig #176; sigstore
  provenance) carrying #172–#175, and bumped the `claude-code-plugins` exact
  pin `0.1.1 → 0.1.2` (cc-plugins #928) so the fix reaches skill evals. j-rig is
  a build-time enrichment step there, not a PR merge gate.
- **cc-plugins CI hygiene.** `enrich-jrig-data.mjs` now warns loudly (GitHub
  Actions `::warning::`) instead of silently blanking every JRig-Verified badge
  when `forge_proofs` is missing/empty (#929). Report-only deadline gates
  (`# REPORT-ONLY-UNTIL:`) added to the frontmatter `--strict` relaxation (live
  count corrected 182→**317**) and the `npm-audit` policy (#930). A generator,
  `scripts/sync-lint-ignores.mjs`, replaces the check-only sync-lint gate so a
  newly-synced source self-registers its markdownlint/ruff exclusion (#931),
  unblocking beads-dolt re-sync.
- **Eval instrumentation.** `j-rig eval` now characterizes the empty-output
  execution boundary (text length, tool_calls, status, timed_out) per test case
  (`--trace-boundary`), so a completion-only eval no longer silently grades a
  tool-dependent skill's degenerate empty response (j-rig #178).
- **Coverage-gate honesty (phase-a-0 research suite).** Documented the real
  reason the `pytest + coverage` job's CI coverage (~40%) trails local
  (~66-68%): the subprocess arm-runner scripts short-circuit in CI because the
  cross-repo IS validator + fixtures and real model-provider keys are absent —
  an environment limit, not the earlier "process-init timing" hypothesis and
  not a coverage bug. Coverage stays advisory-by-design (`continue-on-error`, no
  `--fail-under`); the 62 unit tests are the required signal. No threshold
  lowered, no exclusion added.

#### Spec Authority Kernel (SAK) + continuous-spec-compliance

- ISEDC Session 8 Class-1 Charter for the Spec Authority Kernel (DR-044) (#112)
- SAK governance owners + `SAK-INDEX` + repo-blueprint self-application (#115)
- DR-049 — ISEDC Class-1 charter RATIFIED (6 D-SAK decisions, 7-seat convening, acting head per CEO-mode delegation); flips SAK disposition to claimable (#117)
- SAK plan v8 amendment — re-audit-closure deltas (#116)
- Continuous-spec-compliance skeleton — FF#2 field-diff + 2 P0 watcher-liveness fixes + SSoT declaration (#113)
- Anthropic leading-indicator bitter-lesson watcher (#138)

#### Upstream deep-capture program (6-contract SSoT)

- MCP deep capture — vendored 2025-11-25 schema + deterministic projection (#129)
- Plugin-manifest deep capture — vendored reference + 5 official samples + projection (#132)
- Agent-definition deep capture — sub-agents reference + 5 official samples + projection (#133)
- Hook-config deep capture — hooks reference + settings + 4 official samples + projection (#134)
- Marketplace-catalog deep capture — closes the 6-contract deep-capture program (#135)
- Deterministic walls bracketing the future LLM drift classifier (#128)
- Frozen `drift-classification/v1` eval set (15 labeled cases + recall-floor scorer) (#126)
- Typed fetch-failure taxonomy + three-tier append-only archive (#125)
- Append-only lineage log + derived coverage-map projection (#127)
- DR-062 convergence lineage — 5 adopt + 5 diverge events (#137)

#### Spec-drift upstream-surface registry

- Wave-1 surfaces (MCP, hooks, settings, slash-commands) (#118)
- Wave-2 surfaces (plugins, sub-agents, marketplace, releases) (#119)
- Versioned upstream-surface registry + consistency gate (#120)
- `gate-result/v1` Evidence Bundle row for snapshot-currency (iel-E07 residual) (#162)

#### Governance + decision records

- Hash-chain Decision Records into an append-only ledger (#147)
- Ratify pre-Rekor one-way-door gates + OTel must-emit list (#139)
- DR-062 — tier-3 reconciliation adjudicated; authoring/v2 bases mirror the captured projections (#136)
- DR-077 — IEP PR-review-gate policy: required CI checks are the gate, AI-review bots reactive-only (#161)
- Architecture boundary standards + predicate-type registry (iel-E13) (#143)
- Replay fidelity levels (iel-E11) + canonical runtime event taxonomy (iel-E12) (#140)
- Operational-doctrine bundle + agent-loop-trace sanitization spec (iel-E14, iel-E10) (#150)
- Pre-register citation-integrity eval design + feasibility (gbrain 704w.1, 704w.3) (#149)
- IEP testing + CI/CD posture audit matrix (5 repos) (#144)

#### Cross-repo + ecosystem

- End-to-end integration test framework for the 5-repo unification thesis (#164)
- Tier 1-2 + Tier 3 normative pointers + conformance fixture suite (#156)
- Tier-bridge + taxonomy specs + snapshot-still-current emit row (#153)
- `ecosystem.json` manifest + coherence-check (CCP-fenced) (#151)
- Composite detector-health dashboard that leads with detector health (#130)
- Tombstone superseded upstream-spec captures (#131)
- Record public gist id for sweep/release tooling (#124)

#### CI lanes

- Tag-triggered release + signed spec-integrity evidence (nr75.13) (#110 landed in 0.3.0; extended here)
- ntfy CI-failure alert over tailnet (#146)
- Workflow-YAML lint lane + spec-repo Testing SOP policy (#142)
- Advisory typos spell-check lane (#154)
- `lefthook.yml` git-hooks config (#155)

### Changed

- Blueprint B § 7 — add Parallel Change discipline (expand-contract for kernel schema additions) (#148)
- Scope advisory doc-lint to exclude machine-generated research results (#157)

### Removed

- Stop dependabot github-actions updates (harness-hash pin friction) (#111)

### Fixed

- Close three false-green gates in CI-integrity scripts (#159)
- Watcher hardening from the 2026-06-11 umbrella review (#121)

### Security

- `PYPI_TOKEN` added to the SOPS-encrypted `.env.sops` (#145)

## [0.3.0] - 2026-06-08

**Phase A.0 empirically validated + labs dashboard ratified.** This release lands the multi-provider Phase A.0 null-hypothesis baseline (DR-036 PROCEED), the first production-Rekor-signed Evidence Bundle from this repo, the ISEDC Session 8 labs-dashboard architecture (DR-035), L2 doc-quality + testing gates, and the audit-trio comprehensive master plan (PP-PLAN-040). Vendored audit-harness re-vendored to v1.1.5; renamed-repo link fixes throughout.

### Added

#### Phase A.0 multi-provider baseline (Skill Refiner null-hypothesis gate)

- **Multi-provider runners + pytest suite (free-tier baseline)** — Phase A.0 multi-provider eval harness (#84)
- **Paced execution sub-plan for the A.0 baseline** (#87)
- **Phase A.0 PROCEED** — Refiner empirically validated; ratified as DR-036 (#89)
- **DR-036 PROCEED frontmatter-only scope caveat** added to `RESULTS.md` + DR-036 to match the public page (#95)

#### Evidence signing (first production-Rekor attestation from this repo)

- **Sign Phase A.0 Evidence Bundle to production Rekor** (blob, predicate reserved) (#92)
- **Commit signed Phase A.0 bundle** — Rekor log index 1689291334 (#94)

#### ISEDC governance corpus

- **DR-035** — ISEDC Session 8 ratification of the labs dashboard architecture (#86)
- **DR-037 + DR-038** — research-decision pair: SkillSpector INTEGRATE + bead-naming HYBRID standard (#90)
- **DR-039** — ratify the Evidence Bench public-scorecard direction (#96)
- **DR-040** — basicauth override of DR-035 § 8 for the internal testing dashboard (#109)

#### Planning + positioning docs

- **SkillOpt-pattern plugin ecosystem plan** — 5-phase roadmap (#77)
- **Audit-trio comprehensive master plan + IEP rollback baseline** (PP-PLAN-040) (#102)
- **Prompt + context-engineering eval positioning** — intent-bearing-artifact reframe (#104)
- **Cross-repo release sweep final summary** (2026-05-25/26) AAR (#76)

#### CI

- **Tag-triggered release + signed spec-integrity evidence** (nr75.13) (#110)

### Changed

- **L2 doc-quality gates** installed (advisory first run) (#82)
- **Testing harness** — implement P1-1,2,3,4 from `TEST_AUDIT.md` (L1 pre-commit + L2 ruff/mypy + L3 coverage) (#85)
- **`Scorer.score_text`** — temp file must be named `SKILL.md` so the scorer's frontmatter detection fires (#88)
- Gitignore raw per-run eval outputs, keep `aggregated/` (#107)
- Link back to the Intent Eval Platform umbrella (#97)
- Bump the GitHub Actions group across 1 directory with 5 updates (#91)
- Bump vendored audit-harness to v1.1.5 (#99)

### Fixed

- **Drift-guard self-reference** — make the signed bundle commit-independent (the drift check caught a self-reference) (#93)
- Fix audit-harness link to the renamed `intent-audit-harness` repo (#98)

### Security

- **`ANTHROPIC_API_KEY`** filled from the intentsolutions-vps-runbook SOPS source into `.env.sops` (#83)
- **`NVIDIA_API_KEY`** added to `.env.sops` (#81)
- **`DEEPSEEK_API_KEY`** committed SOPS-encrypted to `.env.sops` (#106)

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
- GitHub Actions group bump (#33)

### Fixed

- **Audit cleanup PR #56** — partner-name vendor-generic scrub + canonical repo-name fixes (`j-rig-binary-eval` → `j-rig-skill-binary-eval` in GH-public refs) + 2 fact-citation corrections + `KNOWN-ISSUES.md` for operational footnotes that don't belong in the normative glossary

### Security

- Partner-name CI guard ratchets DR-004 S1Q2 BINDING into enforcement: case-insensitive grep against the private partner-name pattern returns 0 hits or CI fails. Pattern enumerated in PRIVATE umbrella CLAUDE.md only.
- Schema-drift CI gate prevents structural drift between lab's redirect-stub schema and kernel canonical
- Harness-hash discipline lands in lab via vendored `.audit-harness/v1.1.4` (escape-scan + arch + harness-hash via hooks + GitHub Actions)

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

[Unreleased]: https://github.com/jeremylongshore/intent-eval-lab/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/jeremylongshore/intent-eval-lab/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/jeremylongshore/intent-eval-lab/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.1.0
