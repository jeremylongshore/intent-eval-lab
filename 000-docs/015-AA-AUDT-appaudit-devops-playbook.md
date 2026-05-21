---
title: intent-eval-lab — Operator-Grade System Analysis
date: 2026-05-20
authors:
  - Jeremy Longshore (Intent Solutions)
status: AUDIT (informational)
audit_kind: capstone (5th of 5 in the Intent Eval Platform ecosystem)
related_audits:
  - intent-rollout-gate/000-docs/002-AA-AUDT-appaudit-devops-playbook.md
  - audit-harness/000-docs/003-AA-AUDT-appaudit-devops-playbook.md
  - intent-eval-core/000-docs/005-AA-AUDT-appaudit-devops-playbook.md
  - j-rig-binary-eval/000-docs/019-AA-AUDT-appaudit-devops-playbook.md
binding_authority: none (informational audit; does not amend any binding decision)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
filing_standard: Document Filing Standard v4.3
---

# intent-eval-lab: Operator-Grade System Analysis

*Generated: 2026-05-20*
*Version: HEAD on `feat/epic8-adversarial-bz3.2-bz3.6` (most recent merged work at `da1185a` — partner-name scrub + repo-name canonicalize + fact citations + CI guard, PR #56)*
*Capstone audit — fifth and final in the Intent Eval Platform ecosystem*

---

## 1. This System in 5 Minutes

`intent-eval-lab` is the **constitution-and-kernel-spec repository** of the Intent Eval Platform. It contains no executable runtime, no judges, no validators, no signing pipeline. What it contains is the binding text that every other repo in the ecosystem inherits: the ISEDC Decision Records, the three Blueprints (A = ecosystem constitution; B = kernel specification; C = per-repo blueprint template), the canonical glossary, the methodology specs under `specs/`, and the research artifacts under `research/`. When `audit-harness` decides whether a CRAP score row gets emitted as a `gate-result/v1` Evidence Bundle row, the *shape* of that row was decided here. When `intent-rollout-gate` decides whether a Skill Snapshot ships, the *semantics* of "ship" were decided here. When `intent-eval-core` publishes `@intentsolutions/core@0.1.0` with its Zod validators, the JSON Schemas the validators enforce trace their authority back to Blueprint B § 7 in this repository.

The repo is roughly 6,100 lines of normative markdown across 15 documents in `000-docs/`, plus the SPEC.md draft module at `specs/evidence-bundle/v0.1.0-draft/SPEC.md` (the only spec module with substantive content; the other four module slots — `cross-cli-discovery/`, `validator-contract-reliability/`, `forecasting-drift-detection/`, `decentralized-crypto-evaluation/` — are placeholder READMEs reserving structural slots for future engagements). The single CI surface (`.github/workflows/partner-name-guard.yml`) is a 78-line case-insensitive grep enforcing the DR-004 S1Q2 vendor-generic partner-name discipline. There is no build system, no test runner, no package manifest, no Docker image. The audience-facing artifact is the markdown itself, served via the GitHub repository UI and (in the future) optionally through the partner-portal Hugo pipeline.

The system is operated by a single maintainer (Jeremy Longshore) on a 3-5 hour weekly bandwidth budget. The Phase A foundation closed on 2026-05-15 with five PRs (`#50`, `#52`, `#53`, `#54`, `#55`) landing DR-010, Blueprint A, Blueprint B, the canonical glossary, and Blueprint C in that order. PR `#56` (`da1185a`, 2026-05-15+) followed with an audit-cleanup cycle: partner-name vendor-generic scrub, canonical repo-name fixes (`j-rig-binary-eval` -> `j-rig-skill-binary-eval` where it referred to the GitHub-canonical name), two fact-citation corrections, and the `partner-name-guard.yml` CI workflow that turns the scrub discipline into a machine-checked gate.

What makes this repo unusual is that **it governs four sibling repos that do execute code**. The four sibling audits (`intent-rollout-gate` `002-AA-AUDT`, `audit-harness` `003-AA-AUDT`, `intent-eval-core` `005-AA-AUDT`, `j-rig-binary-eval` `019-AA-AUDT`) each cover an executable surface with builds, tests, CI, npm releases, and runtime concerns. This audit covers the *meta-surface*: how an immutable architectural decision flows from voice-dictated user directive, through an ISEDC adversarial-council session, through a Decision Record at `NNN-AT-DECR`, through Blueprint amendments, through per-repo CLAUDE.md updates, into source code in four sibling repos, into npm package versions, into in-toto Statement v1 predicate URIs anchored to sigstore (eventually production Rekor) — *and how that flow is auditable*. The repo's product is *audit-grade governance evidence*, and the audit-grade-ness is verifiable from the artifacts themselves: every Decision Record preserves verbatim seat positions per ISEDC adversarial-integrity protocol; every binding cites prior bindings explicitly; every override addendum (DR-010 § 13.5, § 13.6) preserves both the council's good-faith position AND the acting-head-of-board reversal so future readers reconstruct both halves.

The biggest single risk is **drift between this repo and its four siblings**. The Phase A foundation is on `main` and the four sibling repos have begun adopting it (`intent-eval-core` published `@intentsolutions/core@0.1.0` with the 13-entity domain model from Blueprint B § 2 baked into Zod validators), but consumer-side adoption is partial: `audit-harness` and `j-rig-binary-eval` have not yet imported the kernel; `intent-rollout-gate` is mid-M5.1 TypeScript runtime work; the lab's own `specs/evidence-bundle/v0.1.0-draft/schema/` JSON Schema duplicates content that should now point to the kernel (open bead `iel-link-schemas-to-kernel`). The drift is not catastrophic — it is the normal lag between authoring a constitution and adopting it. It becomes dangerous if a downstream consumer ships a release referencing a Blueprint clause that has since been amended, or if a Decision Record amendment lands without the corresponding sibling-repo update. The mitigation is the `bd-sync` three-layer mirror discipline (bead ↔ GitHub Issue ↔ Plane Issue) and the CODEOWNERS lock on `/000-docs/` requiring owner review of every Decision Record edit; both are in place. The unmitigated residual is *time-of-check vs time-of-use*: a sibling repo's CI doesn't currently verify that the Blueprint clause it depends on still says what it did at depend-time. That is open as future work (Architect C1/C2 deferrals).

If you read nothing else: this repo is where the platform's binding text lives, every binding is traceable back to a verbatim-preserved adversarial council session, the enforcement primitive that lets the binding text actually shape downstream behavior is the partner-name guard CI workflow plus the CODEOWNERS gate plus the ISEDC discipline of capturing dissent. The repo has no build, no tests in the conventional sense, and no runtime — the *artifact under audit* and the *audit trail* are the same set of markdown files, which is itself a structural feature, not a gap.

---

## 2. Executive Summary

### What It Does

`intent-eval-lab` authors and publishes the binding normative artifacts of the Intent Eval Platform: Decision Records that lock immutable architectural choices, Blueprints (A: ecosystem constitution; B: kernel specification; C: per-repo template) that translate those Decision Records into prescriptive guidance, the canonical glossary that pins terminology, the SPEC.md modules under `specs/` that codify per-class-of-system methodology, and the research-track artifacts under `research/` that surface candidate ideas before they ascend into binding status. It is the only repository in the Intent Eval Platform with the authority to amend platform-wide commitments; all other repos consume the artifacts produced here.

Implementation status is *capstone-stable* for the Phase A foundation: five normative documents landed in five sequential PRs between 2026-05-13 and 2026-05-15, followed by a sixth audit-cleanup PR. The repository is operationally complete for its current scope. What is *not* complete is the downstream consumer adoption of the Phase A foundation: only one of the four sibling repos (`intent-eval-core`) has shipped a release that imports the Blueprint B 13-entity domain model into executable types. The lab's own `specs/evidence-bundle/v0.1.0-draft/SPEC.md` was authored before the kernel-extraction decision (Addendum #3 in the master plan), so it duplicates schema content that should now reference the kernel; that work is tracked at the open bead `iel-link-schemas-to-kernel`.

The technical foundation is intentionally minimal: a plain Apache 2.0 license, a single GitHub Actions workflow enforcing partner-name vendor-generic discipline, CODEOWNERS gating `/000-docs/` and `/.github/workflows/` to a single reviewer, the Document Filing Standard v4.3 naming convention applied uniformly across `000-docs/`, and a `bd-sync` three-layer mirror discipline tracking every artifact at bead ↔ GitHub Issue ↔ Plane Issue parity. There are no language runtimes, no compilers, no test frameworks, no databases, no deployment targets, no Dockerfiles. The repository's *product* is its set of markdown files; the repository's *quality gate* is the CI workflow plus the CODEOWNERS reviewer-lock plus the human discipline of capturing adversarial council dissent verbatim.

The key risks are five: (1) drift between Blueprints and sibling-repo implementations (currently moderate and tracked); (2) NNN- filename collision on parallel work (the Document Filing Standard v4.3 sequence-counter is global per-directory, and two simultaneous PRs both proposing `000-docs/016-...` would collide); (3) normative-spec mutation after ratification (Decision Records are intended to be immutable, but git makes mutation trivially easy — discipline is the only barrier); (4) the upstream `bd` auto-flush JSONL drift bug (documented at `KNOWN-ISSUES.md`; affects audit trail completeness across sessions); and (5) the lab's own `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` duplicating content that should be a pointer to the kernel package (causes downstream consumers to choose-the-wrong-source ambiguously).

### Operational Status

| Environment | Status | Uptime Target | Release Cadence | Last Deploy |
|-------------|--------|---------------|-----------------|-------------|
| Production (the `main` branch on GitHub) | Active | GitHub's; not separately tracked | Ad-hoc per ISEDC convening or audit-cleanup cycle | `da1185a` (PR #56), 2026-05-15+ |
| Staging | None | n/a — feature branches serve as staging | n/a | n/a |
| Local Dev | The repository itself; no runtime | n/a | n/a | n/a |

### Technology Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| Language | Markdown (GitHub-Flavored) | n/a | Primary authoring surface for all 15 normative docs in `000-docs/` and the SPEC.md draft |
| Filing convention | Document Filing Standard v4.3 | v4.3 | `NNN-CC-ABCD-<title>-<date>.md` naming for all `000-docs/` entries; categories AT-DECR, AT-ARCH, AT-SPEC, DR-GLOS, DR-RFC, RR-LAND, RR-INTL, RR-BIBL, RR-COMP, PP-PLAN, AA-AACR, DR-BRIEF, DR-GAPS, DR-FIND |
| CI/CD | GitHub Actions | `actions/checkout@v4` | One workflow: `partner-name-guard.yml` (case-insensitive grep against `000-docs/`, `specs/`, `README.md`, `CLAUDE.md`, `KNOWN-ISSUES.md`) |
| Task tracking | `bd` (beads) | 1.0.3 (host install); workspace at `~/000-projects/.beads/` | Source of truth for all IEP task state; prefix `iel-` for this repo; mirrored to GitHub Issues and Plane via `bd-sync` |
| Governance | ISEDC pattern + Doc Filing Standard v4.3 | n/a | Adversarial 7-seat council captured in `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0; outputs are AT-DECR Decision Records archived in `000-docs/` within 7 days of decision-lock per DR-010 § 7 Q6 VPDevRel binding |
| License | Apache 2.0 | n/a | `LICENSE` at repo root; matches all four siblings (`intent-eval-core` Apache 2.0, `audit-harness` Apache 2.0 since v1.0.0, `j-rig-skill-binary-eval` Apache 2.0 since v1.0.0, `intent-rollout-gate` Apache 2.0) |
| Three-layer mirror | bead ↔ GitHub Issue ↔ Plane Issue | `bd-sync` 1.x | Required discipline per `~/000-projects/CLAUDE.md` — every IEP work item exists in all three layers, each carrying the other two IDs |
| File system | flat `000-docs/` | n/a | All normative + research-finding artifacts at one directory depth; sub-tree under `specs/` per module |

---

## 3. Architecture

### Stack (Detailed)

| Layer | Technology | Version | Purpose | Why This |
|-------|------------|---------|---------|----------|
| Authoring | Markdown | GFM | The medium for every Decision Record, Blueprint, glossary, SPEC.md, RFC draft, and research artifact | Markdown is the only authoring surface that is simultaneously readable in raw form, renderable on GitHub, parseable by any LLM-assisted tooling, and diff-able as plain text. The IEP cannot afford a heavy authoring stack (3-5 hrs/wk bandwidth, per DR-010 Q5 CFO binding). Anything more complex would dominate the maintenance budget. |
| Filing | Document Filing Standard v4.3 | v4.3 | Naming convention: `NNN-CC-ABCD-<title>-<date>.md` | The flat layout under `000-docs/` is intentional. Hierarchical filing produces ambiguity about which directory a doc belongs in; the flat layout with category-coded prefixes (`AT-DECR` for Decision Records, `AT-ARCH` for architectural blueprints, `AT-SPEC` for spec templates, `DR-GLOS` for definitions reference, `DR-RFC` for RFC drafts, etc.) makes every doc's role legible from its filename alone. |
| CI | GitHub Actions | `runs-on: ubuntu-latest`, `actions/checkout@v4` | Enforces DR-004 S1Q2 vendor-generic discipline via case-insensitive grep | One workflow, one gate, one purpose. The CI surface should match the repo's actual concerns — and the only enforcement concern in a spec-only repo is the partner-name vendor-generic binding (since partner identity in public spec content would be a permanent IP / consent violation). |
| Governance | ISEDC | skill v1.0.0 | Adversarial 7-seat council for Class-1 decisions; CTO+VPDevRel pair for Class-2; solo maintainer for Class-3 | Three-class routing is the load-bearing governance abstraction. Class-1 decisions (immutable artifacts, brand commitments, predicate URI reservations, standards-body submissions, language locks) demand full ISEDC; Class-2 decisions (operational, CI workflow changes, validator version bumps) demand CTO+VPDevRel pair; Class-3 decisions (code-level inside an existing scope) are solo. The classes correspond to *recoverability*: Class-1 is hardest to undo, Class-3 easiest. |
| Three-layer mirror | bd-sync | 1.x | Every artifact has a bead + GH issue + Plane issue, each carrying the other two IDs | The mirror is the cross-system redundancy. If the bead workspace corrupts, GH and Plane carry the same IDs and most of the same comments. If Plane is unavailable, the bead and GH carry it. The synchronization substrate IS the IDs themselves — every layer carries the other two, so drift is detectable and recoverable. |
| Authority | DR-010 § 13.5 + § 13.6 override addenda | n/a | Two acting-head-of-board reversals: customer-signal gate removed (§ 13.5); external-pattern non-borrow (§ 13.6) | Captured *inline* with the original council position, never silently. Future readers reconstruct both the council's good-faith work AND the acting-head-of-board reversal. This is the platform's strongest expression of the "preserve dissent" principle from Blueprint A § 1.2 principle 12. |

### System Diagram

```
+-----------------------------------------------------------------------------+
|                        intent-eval-lab (this repo)                          |
|                                                                             |
|  +------------------+  +------------------+  +-----------------+            |
|  |  000-docs/       |  |  specs/          |  |  research/      |            |
|  |  - 15 normative  |  |  - evidence-     |  |  - findings     |            |
|  |    docs (AT-DECR,|  |    bundle/       |  |  - bibliography |            |
|  |    AT-ARCH,      |  |    v0.1.0-draft/ |  |  - ecosystem    |            |
|  |    AT-SPEC,      |  |    SPEC.md       |  |    landscape    |            |
|  |    DR-GLOS,      |  |  - 4 placeholder |  |  - PDF + MD     |            |
|  |    DR-RFC,       |  |    modules       |  |    pairs        |            |
|  |    DR-BRIEF,     |  |    (RFC welcome) |  +-----------------+            |
|  |    DR-GAPS,      |  +------------------+                                 |
|  |    DR-FIND,      |                                                       |
|  |    RR-LAND,      |  +------------------+  +-----------------+            |
|  |    RR-INTL,      |  |  KNOWN-ISSUES.md |  |  .github/       |            |
|  |    PP-PLAN,      |  |  - bd auto-flush |  |  workflows/     |            |
|  |    AA-AACR)      |  |    JSONL drift   |  |  partner-name-  |            |
|  |  - FUTURE.md     |  +------------------+  |  guard.yml      |            |
|  +------------------+                        +-----------------+            |
|         |                                            |                      |
|  +------+--------------------------------------------+-----------+          |
|  |   CODEOWNERS: /000-docs/, /.github/workflows/, /specs/         |         |
|  |   gated to @jeremylongshore (solo maintainer + acting head     |         |
|  |   of board)                                                    |         |
|  +---------------------------------------------------------------+          |
+-----------------------------------------------------------------------------+
                  |                            |
                  | normative artifacts        | task-state mirror
                  v                            v
+-----------------+-----------------+   +------+------+   +------+------+
| Four sibling repos (executable)   |   |  bd-sync    |   |  Plane      |
|                                   |   |             |   |  workspace  |
| 1. intent-eval-core               |   |  bead       |   |  LAB        |
|    - @intentsolutions/core@0.1.0  |   |  workspace  |   |  project    |
|    - 13-entity domain model       |   |  ~/000-     |   |  module     |
|    - Zod + JSON Schema codegen    |   |  projects/  |   |  IEL-CONV-1 |
|    - SIGNED via sigstore          |   |  .beads/    |   +-------------+
|                                   |   +-------------+
| 2. audit-harness                  |
|    - deterministic gates          |
|    - polyglot CLI                 |
|    - emits gate-result/v1 rows    |
|                                   |
| 3. j-rig-skill-binary-eval        |
|    - behavioral judge + rollout-  |
|      gate decision logic          |
|    - TS pnpm monorepo             |
|                                   |
| 4. intent-rollout-gate            |
|    - thin GH Action shell         |
|    - delegates to @j-rig/         |
|      rollout-gate                 |
+-----------------------------------+
```

### The Critical Path

The critical path through this repository is not a request path (the repo has no runtime). It is the **decision-to-binding-to-implementation path** that produces the platform's immutable governance evidence. Step-by-step:

1. **Trigger.** A decision-worthy event surfaces. Examples from the actual audit trail: the user issues a "widening directive" (DR-010, voice-dictated 2026-05-13); an external standards body responds to an informal-temperature email (the pending S3Q2 follow-up tracked at `009-RR-INTL-otel-sig-genai-temperature.md`); an audit cleanup identifies vendor-name leaks (PR #56). Failure point: the trigger is not captured (a conversation closes without the idea reaching a bead). Mitigation: per umbrella CLAUDE.md § "Content / blog topic ideation," capture ideas in Plane CONTENT or the relevant project's bead workspace *immediately* — two minutes of `mcp__plane__create_issue` saves a 30-minute "what was that idea" excavation later.

2. **Class routing.** The decision is classified per DR-010 § 7 Q6: Class-1 (full ISEDC; immutable artifacts), Class-2 (CTO+VPDevRel pair; operational), Class-3 (solo maintainer; code-level). Failure point: a Class-1 decision is mis-routed as Class-3 and lands in `SOLO-DECISIONS.md` as a one-line entry without preserved seat positions — *unrecoverable*, because the dissent that would have surfaced was never captured. Mitigation: the auto-trigger list in Blueprint A § 2.3 is the deterministic routing rule; deviations from it require explicit reasoning.

3. **ISEDC session (Class-1 only).** The 7-seat council convenes; each seat argues from a distinct value system (CTO durability + immutability; GC IP + paper-trail; CMO positioning + category authorship; CFO bandwidth + customer-signal — now overridden; CSO standards-body realpolitik; CISO supply-chain attestation integrity; VP DevRel developer-audience signal). Failure point: a seat's position is summarized rather than preserved verbatim, and the audit trail loses the substance of the dissent. Mitigation: the ISEDC discipline ("verbatim seat positions preserved per ISEDC adversarial-integrity protocol") is in DR-010 § 8 explicitly, with the full session-4 council memos captured at length in § 7.

4. **Decision Record drafted.** The session produces an `NNN-AT-DECR-<title>-<date>.md` per Doc Filing Standard v4.3. Failure point: the Decision Record drifts from the actual session content (paraphrasing creep, hindsight reframing). Mitigation: the verbatim-preservation discipline + the CODEOWNERS gate on `/000-docs/` + the 7-day public-archive binding (DR-010 § 7 Q6 VPDevRel non-negotiable floor).

5. **Acting-head-of-board override** (if applicable). The acting head of board may reverse a council position. The reversal is recorded **inline** with the original council position, never silently. The two canonical examples in DR-010 are § 13.5 (Q5 customer-signal gate removed; bandwidth-only gate retained; marketing-customer framing removed; internal-tool-shared-with-the-world framing applied) and § 13.6 (Q4 external-pattern non-borrow into forward-deployed work). Failure point: an override is recorded as the *new* consensus rather than as the *reversal*, and the council's good-faith original position is lost. Mitigation: the inline-recording discipline is normative per ISEDC pattern v1.0.0; the DR-010 § 13.5 and § 13.6 sections are the canonical example.

6. **Blueprint amendment** (when an existing Blueprint needs adjustment). A new Decision Record can cause downstream amendments to Blueprint A, B, or C. The CODEOWNERS gate ensures every Blueprint edit goes through the acting head of board. Failure point: a Blueprint is edited *without* a corresponding Decision Record — the lineage of *why* the blueprint changed is lost. Mitigation: every PR touching `000-docs/0NN-AT-ARCH-*.md` must cite the Decision Record authorizing the edit.

7. **Sibling repo adoption.** The four sibling repos (`intent-eval-core`, `audit-harness`, `j-rig-skill-binary-eval`, `intent-rollout-gate`) pick up the new binding and reflect it in code, package metadata, CLAUDE.md, or downstream Decision Records of their own. Failure point: a sibling repo *doesn't* adopt the new binding, and its release ships against an outdated Blueprint clause. **This is the open drift risk**, tracked at deferrals Architect C1 (gate-result/v1 spec location, resolved by kernel publication) and Architect C2 (intent-rollout-gate role). Mitigation: per-repo CLAUDE.md cross-references; in the future, a CI gate that asserts "this repo references Blueprint X's Decision Record N — and Decision Record N has not been superseded."

8. **bd-sync three-layer mirror.** Every step's bead is mirrored to a GitHub Issue and a Plane Issue via `bd-sync`. The synchronization substrate is the IDs themselves: every layer carries the other two, so drift is detectable. Failure point: the upstream `bd auto-flush JSONL drift` bug (documented in `KNOWN-ISSUES.md`) silently loses bead state mutations between sessions. Mitigation: the documented `bd-safe` workaround that wraps mutations in an EXIT-trap subshell to atomically export → cp → import → backup-sync.

### Dependency Graph

This repo has **no software dependencies** in the conventional sense — no `package.json`, no `requirements.txt`, no `go.mod`, no `Cargo.toml`. The dependencies are *governance* and *cross-repo schema*, not language runtimes:

- **Upstream (this repo depends on):**
  - The `bd` (beads) tool 1.0.3, installed via the home directory toolchain, for task tracking
  - `bd-sync` at `~/bin/bd-sync` for the three-layer mirror
  - GitHub Actions runners (`ubuntu-latest`, `actions/checkout@v4`) for CI
  - The PRIVATE umbrella `~/000-projects/CLAUDE.md` for the canonical partner-name grep pattern (a defense-in-depth invariant: the public `partner-name-guard.yml` has a pinned inline backstop pattern, but the human-driven scrub is sourced from the private umbrella)
  - The ISEDC skill at `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0 for the adversarial-council pattern (not bundled in this repo; lives in the user's home `.claude/skills/`)
- **Downstream (depends on this repo):**
  - `intent-eval-core` — imports Blueprint B § 2 13-entity domain model into JSON Schemas + Zod codegen; published as `@intentsolutions/core@0.1.0` on 2026-05-17 with sigstore provenance
  - `audit-harness` — its `--emit-evidence` retrofit (Phase B) will consume the Blueprint B § 7 `gate-result/v1` predicate body; not yet implemented (consumer-side adoption gap)
  - `j-rig-skill-binary-eval` — its `@j-rig/rollout-gate` decision-engine consumes the Blueprint A § 4.1 `RolloutGate` semantics + Blueprint B § 2.8 RolloutGate entity schema; partial adoption (the entity schema is referenced but the kernel migration `iaj-E02` is not yet landed)
  - `intent-rollout-gate` — depends transitively via `@j-rig/rollout-gate`; M5.1 runtime work in progress on a feature branch

What happens if each dependency is unavailable:
- *`bd` unavailable:* no new task tracking can happen; existing tasks captured at last successful `bd export` cycle are recoverable from `~/000-projects/.beads/issues.jsonl`. GitHub Issues and Plane carry redundant state via the three-layer mirror.
- *PRIVATE umbrella unavailable:* the inline backstop pattern in `.github/workflows/partner-name-guard.yml` (line 53: `PATTERN='<REDACTED — see ~/000-projects/CLAUDE.md private umbrella for canonical pattern>'`) still runs in CI; the human-driven scrub during authoring is the at-risk surface. The intentional discipline is that the inline backstop *must stay in sync with* the private canonical pattern — mismatch is an audit-trail concern, not an enforcement gap. *(Pattern redacted from this public artifact 2026-05-20 per DR-004 S1Q2; the unredacted `.pdf` companion at sha 1e7ba423 retains canonical content for audit-trail purposes; pattern itself lives in private `~/000-projects/CLAUDE.md`.)*
- *ISEDC skill unavailable:* Class-1 sessions cannot follow the canonical adversarial-council pattern; ad-hoc deliberation is the fallback, with a corresponding loss of audit-trail rigor.
- *Downstream consumer unavailable:* the lab's normative artifacts are unaffected (this repo is upstream-of, not downstream-of, the executable siblings).

---

## 4. Design Decisions & Tradeoffs

### Decision Log

This section captures the eight load-bearing tradeoff decisions visible in the repository, plus a capstone integration subsection that places this repo in the context of the four-sibling ecosystem.

#### Decision 1: ONE BIG converged platform over family-of-platforms or platform-of-platforms (DR-010 Q1)

- **Chosen:** A single converged "Intent Eval Platform" (Q1=A) with the AISE 5-domain stack (Inference, Reliability, Eval Science, Agent Systems, LLMOps) absorbed as an **internal scope map**, not as separate-brand sub-platforms. Single umbrella, single identity in standards-body and developer-funnel surfaces, single Plane module HQ at LAB-6 (IEL-CONV-1).
- **Over:** Option B (family of products under coordinating thesis, no new umbrella brand — preferred by GC seat on trademark-clearance grounds); Option C (platform-of-platforms / schema-bearing constellation — preferred by CTO + CMO seats on architectural-honesty + category-authorship grounds).
- **Because:** The supply-chain attack surface cost of multi-brand identity (CISO position: each additional platform root multiplies DNSSEC zones to monitor, CAA records to audit, signing key custodies, Rekor anchoring pipelines), the standards-body identity cost (CSO position: OTel SIG-GenAI maintainers do not have bandwidth to track three peer "Intent" platforms and will conflate them anyway, badly, on terms we don't control), and the developer adoption friction cost (VP DevRel position: three platform-brands at 3-5 hrs/wk is a guarantee of three half-maintained docs sites — the loudest negative developer signal in OSS) are all permanent in their own ways. The brand-narrative cost CMO + CTO flag is recoverable via internal scope-map naming + reserved-name defensive registrations.
- **Cost:** CTO + CMO dissent on Option C is preserved verbatim in DR-010 § 7 Q1 with minority bindings stacked into the implementation: defensive name registration (domain + npm scope + GitHub org alias), schema-stability SLA separate from code SLA, documented 12-month exit-ramp option. The platform forfeits the multi-brand narrative surface permanently; defensive registrations preserve the option but never use it.
- **Revisit when:** Internal package boundaries enforced by lint rules show release-cadence pain within 18 months (CTO 12-month exit-ramp trigger). Single-brand collapse under platform weight (the "five domains, five release cadences, five toolchains, five threat models" CTO failure-mode prediction). A trademark conflict at USPTO TESS clearance forces a forced rebrand (GC trigger).

#### Decision 2: Per-artifact hybrid language with TS-primary at signing + dev-facing surfaces (DR-010 Q2)

- **Chosen:** A per-artifact hybrid: TypeScript at every signing-adjacent and dev-facing surface (`intent-eval-core` kernel, `j-rig-skill-binary-eval` monorepo, `intent-rollout-gate` Action shell, lab tooling); polyglot retained at `audit-harness` (Node CLI + shell + Python); Python permitted only at ML internals behind subprocess boundaries with sigstore-python signed wheels, when/if those internals ever materialize.
- **Over:** A hard TS lock (CFO + CISO + VP DevRel positions — no Python widening anywhere); a Python-heavy widening (rejected unanimously); a true per-artifact polyglot with no signing-layer constraint (rejected on CISO supply-chain grounds).
- **Because:** All seven seats converged on "signing/dev-facing/CI = TS; ML internals may be Python behind a boundary." The CISO non-negotiable on Python paths that construct or sign Evidence Bundle rows requiring sigstore-python + signed wheels for 100% of the dependency tree is the load-bearing constraint. The GC non-negotiable on every new Python dependency declared in `LICENSES.md` with `pip-licenses` / `licensecheck` CI scan blocking GPL/AGPL at CI level absent explicit GC waiver is the IP discipline. The CFO bandwidth gate of 15 founder-hrs/release per new Python package introduced is the budget gate. The VP DevRel discipline that the headline quickstart uses `npx` or `pnpm dlx` (not `pip install`) for the 45,000+ NPM `claude-code-plugins` audience's muscle memory is the developer-friction gate. The CTO schema-codegen discipline (JSON Schema canonical; Zod + Pydantic codegen enforced by CI gate; no drift tolerated) is the type-system gate.
- **Cost:** The lab itself escapes most of this — it has no executable code surface — but the cost is real for the four sibling repos. The TS-first lock forecloses certain ML-tooling integrations (e.g., a native Python sigstore-policy-controller integration would be straightforwardly Python-first elsewhere). The `audit-harness` polyglot precedent is preserved by exception, not generalized.
- **Revisit when:** A specific ML-tooling integration would benefit from being Python-primary at a signing-adjacent surface; or when the sigstore-python sign-wheels ecosystem reaches the maturity that makes Python-signing equivalent in supply-chain audit posture to npm-signing (which it currently is not).

#### Decision 3: Unification thesis BINDING — every validator emits Evidence Bundle (DR-010 Q3)

- **Chosen:** A 7/7 unanimous council vote making the unification thesis (every validator, gate, judge, and runtime in the ecosystem emits Evidence Bundle rows as architectural primitive) BINDING. The thesis is referenced from `intent-eval-lab/specs/UNIFICATION.md` (to be authored within 30 days of DR-010) and from every constituent repo's CLAUDE.md.
- **Over:** A weaker "Evidence Bundle as recommended pattern" framing (would have permitted incremental adoption without architectural force); a "per-validator opt-in" framing (would have permitted permanent fragmentation).
- **Because:** The schema is the only invariant that survives the widened scope (CTO position: "Evidence Bundle as lingua franca is the right invariant; everything else federates around it"). Validators that don't emit Evidence Bundle rows can't be composed into the Rollout Gate's decision logic; they become dead-end gates that produce information no downstream consumer can use. The unification thesis is what makes the four-sibling ecosystem composable at all.
- **Cost:** Every existing validator (11 inventoried across `claude-code-plugins`: validate-skillmd, validate-plugin, validate-agent, validate-mcp, validate-hook, validate-consistency, validate-marketplace, audit-tests, implement-tests, sync-testing-harness, audit-harness) must retrofit an `--emit-evidence` mode in Phase B. This is multi-person-week of work across the ecosystem and is sequenced after `intent-rollout-gate` M5.1 v0.2 cuts to production Rekor. Until that retrofit lands, the lab carries an open commitment that downstream validators currently don't fulfill.
- **Revisit when:** A class of validator emerges whose verdict is so trivial that emitting an Evidence Bundle row is genuinely overkill (e.g., a pure local-file-existence check). Even then, the cost of inconsistency outweighs the cost of overkill; the discipline is to emit a row with a low-signal predicate type rather than to opt out.

#### Decision 4: Customer-signal gate REMOVED (DR-010 § 13.5 acting-head-of-board override)

- **Chosen:** The customer-signal gate on platform-build implementation, reconstituted by the Session 4 council across CFO + GC + CMO + VP DevRel positions, was overridden by the acting head of board. Platform-builds are gated on **bandwidth only**, not customer-signal. New platform-builds (LLM Harness Lab, Agent Runtime Sandbox, both currently design-doc-only in `FUTURE.md`) initiate when bandwidth permits, with no customer-signal precondition.
- **Over:** Retaining the customer-signal gate as the council had constituted it ("no new platform-build implementation in next 6 months without second paying-customer signal").
- **Because:** The acting head of board had explicitly removed the paying-customer gate at ISEDC Session 3 (DR-006 Q1) with the directive *"if we build it the people will come focus on building dont worry about distribution right now"*. The Session 4 council, deliberating in good faith, partially reconstituted that gate through CFO bandwidth math + GC paper-trail + CMO category-authorship + VP DevRel adoption-funnel framings. The override re-asserts the build-mode directive: internal tool, build it for the acting head of board's own engineering practice (which is *itself* the validation), distribute naturally through the existing 45,000+ NPM `claude-code-plugins` audience, no customer-acquisition or marketing-customer architecture.
- **Cost:** The IP / security / standards-body / bandwidth-math disciplines from the council positions are preserved (the GC license-audit gate, the CISO sigstore-staging-before-production-Rekor gate, the CSO informal-email-first sequence, the CFO bandwidth math + 50hr widening cap remain in force). Only the *customer-signal trigger* is removed. The marketing-customer framing (M5.1 PR-comment template carrying umbrella tagline + link to umbrella site; M6 framing as customer-acquisition funnel; CMO "category-authorship velocity" framing; VP DevRel "convert 45k+ NPM warm market into adopters") is removed. The platform's product positioning *"Reliability infrastructure for agentic systems. Not chatbots. Not wrappers. Infrastructure."* (user-named at DR-010) lives at the umbrella.
- **Revisit when:** A bandwidth windfall arrives (a second consistent revenue source freeing additional founder-hours); or the natural-distribution thesis empirically fails (the platform has been in `main` for a multi-quarter period and the existing 45,000+ NPM audience has not produced any discoverable engagement); or a partner with explicit written consent emerges who wants to commission a platform-build at sufficient scope to justify the implementation cost.

#### Decision 5: External-pattern non-borrow in forward-deployed work (DR-010 § 13.6 acting-head-of-board override)

- **Chosen:** The acting head of board reversed Q4 in its entirety. Patterns borrowed from external authors (the six candidate "Uncle Bob" patterns: two-mode pipeline IR, type-detection mutation rule table, 0/1/2/3 exit-code grammar, Killed/Survived/Error trichotomy, coverage-as-prefilter, spec-as-portable-doc) are NOT to be included in forward-deployed work as named-pattern borrows. The platform conforms to open standards (in-toto, DSSE, JSON Schema, OpenTelemetry semantic-conventions, SLSA, OpenSSF, UUIDv7 per RFC 9562) and depends on runtime tools (cosign, sigstore, npm, pnpm) — these are standards and dependencies, not borrowed patterns. Internal patterns from prior Intent Solutions work (Evidence Bundle, predicate URIs, MM-1..MM-6 Intentional Mapping vocabulary, the 7-layer testing taxonomy) may be cross-referenced freely.
- **Over:** The council's near-unanimous "borrow all 6 patterns with GC attribution discipline + CISO security bindings" position (#3, #4, #6 unanimous; #1, #2, #5 6-of-7).
- **Because:** The acting head of board's directive: forward-deployed work reflects the platform's own thinking — not a pattern-library remix. The reversal removes "informed by X" / "inspired by Y" / "after Z's pattern" footers from specs, code comments, design docs, READMEs, blog posts, public Decision Records, and RFC text. Designs land as our own with our own naming derived from our own use cases.
- **Cost:** The ~14 founder-hours allocated in DR-010 § 7 Q4 to "borrow all 6 patterns" is reclaimed. Some of that work was load-bearing (SPEC.md normative authoring overlaps with what Q4#6 "spec-as-portable-doc" would have covered) — that work still happens, but as our own engineering discipline, not as a borrowed pattern. The cost is reputational-rhetorical: external readers may notice that the platform's exit-code grammar or trichotomy verdict naming resembles familiar patterns from mutation testing or test-driven development literature, but the platform does not cite the resemblance.
- **Revisit when:** Never expected. The override is a stylistic/positioning binding that the acting head of board has explicit standing to assert; revisiting would require a new acting-head-of-board declaration reversing the reversal.

#### Decision 6: Partner-name vendor-generic discipline (DR-004 S1Q2, reaffirmed at DR-010 § 10)

- **Chosen:** Partner names (specific company names of in-flight or prior partner engagements) are **never** present in public artifacts of any kind — public specs, public READMEs, public Decision Records, public blog drafts, public commit messages. The active grep pattern enforcing this discipline lives in the PRIVATE umbrella `~/000-projects/CLAUDE.md` and is not enumerated in this glossary or any public document. Every commit touching public surfaces runs the grep guard via `.github/workflows/partner-name-guard.yml`; a non-zero result blocks the commit. Re-instantiation with partner names is permitted only after per-partner written consent is on file.
- **Over:** Partner-named case-study writeups in public artifacts as a marketing-credibility surface; no enforcement (relying on author memory).
- **Because:** The "we don't mention X, Y, Z" framing (negative-affirmation) is itself a violation — listing partners-not-to-name still names them. Per DR-004 S1Q2 binding language: *"This rule applies even to negative-affirmation phrasings."* Public Decision Records that reference a partner engagement must use generic terms like "an enterprise partner engagement," "an active revenue client," "the primary client engagement," or "the inaugural case study (engagement-private)" until written consent is on file.
- **Cost:** The pattern in the PRIVATE umbrella is the canonical source; the pinned inline pattern in `.github/workflows/partner-name-guard.yml` line 53 is a CI-only backstop. Mismatch between the two is an audit-trail concern, not an enforcement gap (the human-driven scrub uses the private umbrella; the CI uses the inline backstop). Maintenance burden: when a new partner name needs adding to the discipline, both the private umbrella and the public CI backstop must be updated in lockstep. The PR #56 audit cleanup (`da1185a`) is the canonical example of catching a backstop-vs-pattern drift via the CI gate.
- **Revisit when:** A partner provides explicit written consent for public reference (DR-004 S1Q2 escape clause). Even then, the discipline is to amend the inline backstop + the private umbrella + file an `AT-DECR` documenting the consent, not to silently drop the partner from the pattern.

#### Decision 7: Governance-as-spec-repo (no executable code in this repo)

- **Chosen:** The `intent-eval-lab` repository contains no executable code beyond the single CI workflow. There is no build system, no test runner, no package manifest, no Docker image, no runtime, no judges, no validators. The repository's *product* is its set of markdown files.
- **Over:** Bundling the Evidence Bundle JSON Schema validators here (rejected when the kernel-extraction decision in master plan Addendum #3 promoted `intent-eval-core` to a separate repo); bundling reference implementations here (rejected per CTO + GC binding in DR-006 Q3 — "any gateway reference implementation lives as a module inside `intent-eval-lab/`, not a new repo" was originally the binding, but the kernel-extraction supersedes by routing canonical contracts to `intent-eval-core`).
- **Because:** The repository's *role* is to be the authority surface for the platform's normative artifacts — Decision Records, Blueprints, glossary, SPEC.md modules. Adding executable code to this repository would tangle the authoring surface with the execution surface and dilute the CODEOWNERS gate's specificity (a single reviewer-lock makes sense for spec content; it does not make sense for runtime code).
- **Cost:** The lab's own `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` JSON Schema currently *duplicates* content that should now reference the `@intentsolutions/core@0.1.0` kernel package. The duplication is a transitional artifact (the lab schema was authored before the kernel-extraction decision); the open bead `iel-link-schemas-to-kernel` tracks the cleanup. Until that lands, downstream consumers face an ambiguity about which schema is canonical — and the canonical answer (the kernel) is not yet reflected in the lab's spec.
- **Revisit when:** A reference implementation becomes necessary that genuinely belongs in the lab's scope (e.g., a methodology-only demonstration artifact that has no other natural home). The reference implementation would live under `intent-eval-lab/reference-implementations/<name>/` per the DR-006 Q3 binding, not at the repository root.

#### Decision 8: Document Filing Standard v4.3 with flat 000-docs/ + NNN sequencing

- **Chosen:** Every doc lives at `000-docs/NNN-CC-ABCD-<title>-<date>.md` at one directory depth. Categories AT-DECR, AT-ARCH, AT-SPEC, DR-GLOS, DR-RFC, DR-BRIEF, DR-GAPS, DR-FIND, RR-LAND, RR-INTL, RR-BIBL, RR-COMP, PP-PLAN, AA-AACR are enumerated in CLAUDE.md.
- **Over:** Hierarchical filing (`decisions/2026-05-13-isedc-session-4.md`); flat without sequence (date-only; ambiguous co-located docs); per-category subdirectories (`decisions/`, `blueprints/`, `glossary/`).
- **Because:** Flat layout with category-coded prefixes makes every doc's role legible from its filename alone. Hierarchical filing produces ambiguity about which directory a doc belongs in (is a "decision record about a blueprint" filed under `decisions/` or `blueprints/`?). Sequence-counter prefixes give every doc a stable global ordering that survives `ls -1`, which is important for diff-friendliness.
- **Cost:** The NNN sequence-counter is global per-directory. Two parallel PRs both proposing `000-docs/016-...` will collide at merge time. The mitigation is human discipline (check the latest `LAST_NUM` before authoring); the residual is that simultaneous PR authoring without coordination is rare in a single-maintainer context but would surface as a merge conflict in a multi-author context.
- **Revisit when:** The `000-docs/` directory grows past ~200 entries (sub-categorization becomes more legible than a flat 200-line `ls`); or when a multi-author workflow becomes routine and the sequence-counter collision becomes a regular merge-conflict source (the discipline would shift to date-prefix + ULID).

### Capstone integration — how this repo sits inside the 5-repo ecosystem

This audit is the fifth and final in the Intent Eval Platform series. The other four are:

- `intent-rollout-gate/000-docs/002-AA-AUDT-appaudit-devops-playbook.md` (17,138 words; the thin GitHub Action shell)
- `audit-harness/000-docs/003-AA-AUDT-appaudit-devops-playbook.md` (12,750 words; deterministic-gates polyglot CLI)
- `intent-eval-core/000-docs/005-AA-AUDT-appaudit-devops-playbook.md` (15,417 words; canonical contracts kernel, published as `@intentsolutions/core@0.1.0`)
- `j-rig-binary-eval/000-docs/019-AA-AUDT-appaudit-devops-playbook.md` (12,583 words; behavioral judge + rollout-gate decision logic)

The integration thesis: **the lab is the head, intent-eval-core is the spine, audit-harness + j-rig-binary-eval are the organs, intent-rollout-gate is the limb.** The lab decides; the kernel codifies the decisions as types and schemas; the gate-emitting organs produce Evidence Bundle rows against the kernel; the Action-shell limb consumes those rows via the decision-engine and produces a ship/no-ship verdict.

**What's still broken in the convergence (Phase B work):**

1. **Kernel migration not landed in audit-harness or j-rig-binary-eval.** `intent-eval-core@0.1.0` was published 2026-05-17 with the 13-entity domain model in Zod validators (`iec-E02`). The downstream beads `iah-E02` (audit-harness imports kernel) and `iaj-E02` (j-rig migrates `@j-rig/core` schemas to the kernel) are open and queued. Until they land, each sibling carries its own local-schema definitions that *should* be replaced with kernel imports. Drift between local schema and kernel schema is detectable but not enforced.

2. **Customer-signal gate removal reframes positioning across all four siblings.** DR-010 § 13.5 was authored in the lab, but its operational effect cascades: `intent-rollout-gate` M5.1 PR-comment templates that the council had constituted as marketing surface (umbrella tagline + link to umbrella site) are reframed as honest engineering output (decision, summary, reasons, coverage); `audit-harness` README framing that the council had constituted as adoption-funnel content is reframed as build-notes; the M6 framing across the ecosystem shifts from "public rollout to convert warm market" to "public availability shipped." The implementation lag here is documentation, not code — the four siblings' READMEs still carry some marketing-customer language that pre-dates the § 13.5 override and has not been swept.

3. **M5 intent-rollout-gate runtime not started.** The Action-shell limb is still on a feature branch (`feat/m5-typescript-runtime-lock-and-mvp` per the local clone; canonical branch name will be `feat/m5.1-ts-runtime-experimental-v0.1.0` per DR-010 § 11 fold-in). Until M5.1 v0.1.0-experimental ships, no Evidence Bundle row produced by `audit-harness` or `j-rig-binary-eval` flows through a real consumer; the unification thesis is unverified end-to-end.

4. **Production-Rekor signing remains gated.** Per DR-010 § 7 Q5 CISO non-negotiable, no predicate URI gets signed against production Rekor until that predicate's SPEC.md normative section lands. For `gate-result/v1`, the normative section lives in Blueprint B § 7 (folded per master plan M1 reconciliation), and the JSON Schema lives in the kernel — so `gate-result/v1` IS now cleared for production-Rekor signing in principle. The kernel does NOT yet sign attestations against production Rekor in its release flow; it uses sigstore provenance for its npm package (which is a different surface). The full production-Rekor signing flow is end-to-end-unverified.

5. **Lab schema duplication unresolved.** Tracked at `iel-link-schemas-to-kernel`. Until the lab's `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` is replaced with a pointer to the kernel package, downstream consumers face an ambiguity about which schema is canonical.

The convergence is structurally sound but operationally lagging. The lab is correctly positioned as the head; the four siblings are correctly positioned as the spine + organs + limb; the schema is correctly chosen as the lingua franca. The work that remains is mechanical adoption — each sibling pulling the kernel in, sweeping marketing-customer language, replacing duplicated schemas with pointers — not architectural.

### What Was Deliberately Not Built

- **No executable code in this repo.** The lab is governance-as-spec-repo (Decision 7 above). Reference implementations live as modules under `intent-eval-lab/reference-implementations/<name>/` per the DR-006 Q3 binding; none currently exist.
- **No multi-author workflow.** The CODEOWNERS gate routes every PR to a single reviewer (`@jeremylongshore`). The repo accepts external PRs per `CONTRIBUTING.md`, but the cadence is set by single-maintainer bandwidth. Multi-maintainer governance is deferred until the platform has scaled past the solo-maintainer phase (DR-010 § 7 Q5: "Solo-maintainer for the foreseeable future").
- **No automated Blueprint-to-sibling-repo verification.** No CI gate in any sibling repo currently asserts "this repo references Blueprint X's Decision Record N, and Decision Record N has not been superseded." This is tracked at Architect C1/C2 deferrals.
- **No tier-2 (independent lab research) projects co-located.** The `projects/` directory holds symlinks (gitignored) to tier-2 projects living at `~/000-projects/<name>/`. Patent-sensitive projects (e.g., semantic-flux / QCSS, patent provisional clock 2026-06-12) are deliberately isolated from this umbrella per the tier-1-vs-tier-2 binding in `~/000-projects/intent-eval-platform/CLAUDE.md`.
- **No build system, no `package.json`, no tests in the conventional sense.** The repo's quality gate is the CI workflow + the CODEOWNERS reviewer-lock + the ISEDC discipline.
- **No `agent-loop-trace/v1` predicate URI for v1.** Per DR-010 § 7 Q3 CISO veto, the predicate is REJECTED for v1 pending a sanitization specification. The rejection is preserved verbatim in DR-010 and not silently relaxable.
- **No `harness-experiment/v1` or `cache-decision/v1` predicates for v1.** Deferred to Phase B+ per the same CISO per-predicate assessment.
- **No customer-acquisition framing in any artifact.** Per DR-010 § 13.5 acting-head-of-board override.
- **No "informed by X" / "inspired by Y" external-pattern attribution.** Per DR-010 § 13.6.

### Assumptions the Architecture Rests On

- **The single-maintainer bandwidth budget (3-5 hrs/wk) holds.** If it drops to <2 hrs/wk, the +50 founder-hour widening cap from DR-010 § 7 Q5 becomes binding tight rather than budgeted; if it rises past 8 hrs/wk consistently, the customer-signal gate removal (§ 13.5) was correct ex-post.
- **The `bd` + `bd-sync` toolchain remains operational.** The upstream `bd auto-flush JSONL drift` bug is the known weakness; the documented workaround is in `KNOWN-ISSUES.md`. If `bd` becomes structurally broken (the upstream project archived; the binary stops working on a future glibc), the task-tracking substrate would need replacement.
- **The ISEDC discipline scales.** The pattern was designed for solo-maintainer + acting-head-of-board governance. Multi-maintainer extension is feasible (additional seats; reviewer rotation; quarterly cross-maintainer convening) but not yet exercised.
- **GitHub remains the canonical hosting surface.** The repository depends on GitHub Actions for the partner-name-guard CI, GitHub Issues for the bd-sync mirror, and GitHub Pages-equivalent surface for public DR archival. A migration to a different hosting surface would require updating the three-layer-mirror discipline.
- **The PRIVATE umbrella `~/000-projects/CLAUDE.md` stays maintained.** The canonical partner-name grep pattern lives there; the CI workflow's inline backstop is a defense-in-depth pinning, not a replacement.
- **The four sibling repos remain Apache 2.0 (or compatible).** License divergence in the ecosystem would require revisiting the Blueprint A § 4.2 license-audit standard.

---

## 5. Directory Structure

### Layout

```
intent-eval-lab/
+-- .beads/                          # bd workspace (gitignored)
|   |-- config.yaml                  # workspace config; prefix `iel-`
|   |-- issues.jsonl                 # bead state (out-of-tree; sync via bd-sync)
|   |-- export-state.json
|   |-- last-touched
|   |-- metadata.json
|   |-- interactions.jsonl
|   |-- README.md
|   `-- .gitignore
+-- .claude/                         # Claude Code session settings (gitignored mostly)
|   `-- settings.json
+-- .github/
|   |-- workflows/
|   |   `-- partner-name-guard.yml   # the ONE CI gate; case-insensitive grep
|   |-- CODEOWNERS                   # @jeremylongshore on /000-docs/, /.github/workflows/, /specs/
|   |-- FUNDING.yml
|   |-- PULL_REQUEST_TEMPLATE.md
|   `-- dependabot.yml
+-- .private/
|   `-- CLAUDE-private.md            # gitignored — patent-sensitive cross-refs
+-- 000-docs/                        # the canonical home for every normative artifact
|   |-- 000-INDEX.md                 # human-readable directory of every doc
|   |-- 001-DR-RFC-otel-agent-rollout-gate-signals-draft.md       # iel-E12 forward
|   |-- 002-RR-LAND-mcp-testing-bridge.md
|   |-- 003-PP-PLAN-phase-b-scope-refinement.md
|   |-- 004-AT-DECR-isedc-council-record-2026-05-10.md            # DR-004 (5 bindings)
|   |-- 005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md     # DR-005 (Intentional Mapping)
|   |-- 006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md    # DR-006 (Phase B gate, lifted)
|   |-- 007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html  # 6k-word system brief
|   |-- 008-DR-GAPS-spec-vs-system-brief-2026-05-11.md
|   |-- 009-RR-INTL-otel-sig-genai-temperature.md                 # OTel paper-trail file
|   |-- 010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md  # DR-010 (widened-scope lock)
|   |-- 011-AT-ARCH-ecosystem-master-blueprint.md                 # Blueprint A (constitution)
|   |-- 012-AT-ARCH-platform-runtime-blueprint.md                 # Blueprint B (kernel spec)
|   |-- 013-AT-SPEC-repo-blueprint-template.md                    # Blueprint C (per-repo template)
|   |-- 014-DR-GLOS-canonical-glossary.md                         # canonical glossary
|   `-- FUTURE.md                                                 # deferred insights catalog
+-- specs/                           # normative methodology output, per class of system
|   |-- README.md                    # module index + authoring conventions
|   |-- evidence-bundle/             # ONLY module with substantive content
|   |   `-- v0.1.0-draft/
|   |       |-- SPEC.md              # ~17k bytes; Evidence Bundle predicate body draft
|   |       |-- schema/              # JSON Schemas (DUPLICATES kernel content; iel-link-schemas-to-kernel)
|   |       |-- examples/
|   |       |-- case-studies/
|   |       `-- conformance-test-suite/
|   |-- cross-cli-discovery/         # placeholder; RFC welcome
|   |-- mcp-plugin-observability/    # placeholder; RFC welcome
|   |-- validator-contract-reliability/  # placeholder
|   |-- forecasting-drift-detection/     # placeholder
|   |-- decentralized-crypto-evaluation/ # placeholder
|   `-- methodology/                 # placeholder
+-- research/                        # research-track artifacts
|   |-- README.md
|   |-- 000-DR-FIND-iep-phase-b-gap-analysis-and-research-framework-2026-05-20.md
|   |-- 000-DR-FIND-iep-phase-b-gap-analysis-and-research-framework-2026-05-20.pdf  # 289k binary
|   |-- 000-RR-BIBL-shared-bibliography-2026-05-20.md
|   `-- 000-RR-COMP-ecosystem-landscape-2026-05-20.md
+-- sandboxes/                       # per-experiment dirs; YYYY-MM-DD-<name>/
|   `-- .gitkeep                     # empty; experiments add subdirs as needed
+-- evidence/                        # captured telemetry; mostly gitignored
|   `-- .gitkeep
+-- scripts/                         # reusable scripts; currently empty
|   `-- .gitkeep
+-- projects/                        # gitignored symlinks to constituent projects (tier-1 + tier-2)
|                                    #   (tier-1: audit-harness, j-rig-binary-eval, intent-rollout-gate)
|                                    #   (tier-2: semantic-flux, others as added)
+-- AGENTS.md                        # bd workflow Quick Reference for AI agents
+-- CHANGELOG.md
+-- CLAUDE.md                        # Claude Code session guidance
+-- CODE_OF_CONDUCT.md
+-- CONTRIBUTING.md
+-- KNOWN-ISSUES.md                  # operational footnotes (bd auto-flush JSONL drift)
+-- LICENSE                          # Apache 2.0
+-- README.md
+-- SECURITY.md
+-- SUPPORT.md
+-- .editorconfig
+-- .gitattributes
+-- .gitignore
`-- version.txt
```

### Load-Bearing Files

| Path | Role | Why it matters |
|---|---|---|
| `000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md` | DR-010 — widened-scope architectural lock | 675 lines of normative governance text. Contains Q1=A (ONE BIG), Q2 (per-artifact hybrid), Q3 (unification thesis BINDING), Q4 (overridden in § 13.6), Q5 (parallel-track with experimental-mode gate), Q6 (three-class governance), § 13.5 (customer-signal gate removed), § 13.6 (external-pattern non-borrow), § 11 per-artifact fold-in plan. Every Blueprint cites this as binding authority. Editing it requires preserving the verbatim seat positions; silent edits violate ISEDC adversarial-integrity protocol. |
| `000-docs/011-AT-ARCH-ecosystem-master-blueprint.md` | Blueprint A — constitution | 12 binding principles, 5-repo taxonomy, anti-goals (§ 3), governance routing (§ 2.3), engineering standards (§ 4.2). Every per-repo blueprint inherits from this. |
| `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` | Blueprint B — kernel spec | 13-entity canonical domain model (§ 2); state machines + replay semantics + evidence contracts (§ 3); runtime isolation + cost governance + observability (§ 4); deployment philosophy modular-monolith (§ 5); the **NORMATIVE `gate-result/v1` predicate body fold** (§ 7) that unlocks production-Rekor signing for that predicate. |
| `000-docs/014-DR-GLOS-canonical-glossary.md` | Single source of truth for platform terminology | 9 sections + alphabetical cross-reference index. Every other doc references this rather than redefining terms. Amendments are Class-1 routing when they alter the meaning of a load-bearing term used in immutable artifacts. |
| `.github/workflows/partner-name-guard.yml` | The ONE CI gate | Enforces DR-004 S1Q2 binding. Case-insensitive grep against `000-docs/`, `specs/`, `README.md`, `CLAUDE.md`, `KNOWN-ISSUES.md`. Inline pinned pattern (line 53) is the defense-in-depth backstop; PRIVATE umbrella `~/000-projects/CLAUDE.md` carries the canonical pattern. |
| `.github/CODEOWNERS` | Reviewer-lock | Routes every PR to `@jeremylongshore` for `/000-docs/`, `/.github/workflows/`, `/specs/`. Prevents drift on normative content via single-reviewer gate. |
| `CLAUDE.md` | Session guidance for Claude Code | Documents four-repo convergence (now five-repo per master plan Addendum #3); tier-1 vs tier-2 distinction; partner-consent discipline; lab-level conventions. |
| `KNOWN-ISSUES.md` | Operational footnotes | Documents the upstream `bd auto-flush JSONL drift` bug + the `bd-safe` workaround. Pulled out of the canonical glossary to keep the glossary surface focused on platform terminology. |

---

## 6. Getting Started

A first-week engineer onboarding to the Intent Eval Platform should read this repository in a specific order — *not* alphabetically, *not* by file size, *not* by recency. The order is built to teach the platform's architectural reasoning, not just its file contents.

### Prerequisites

| Tool | Version | Install | Verify |
|------|---------|---------|--------|
| `git` | 2.34+ | `apt install git` / `brew install git` | `git --version` |
| `bd` (beads) | 1.0.3+ | per `~/000-projects/BEADS-SETUP-PROMPT.md` | `bd --version` |
| `bd-sync` | 1.x | install at `~/bin/bd-sync` per umbrella CLAUDE.md | `bd-sync status` |
| Markdown reader | any | most editors (`bat`, `glow`, GitHub renders inline) | n/a |
| `gh` (GitHub CLI) | 2.40+ | `apt install gh` / `brew install gh` | `gh auth status` |
| `pass` (optional) | 1.7+ | `apt install pass` / `brew install pass` | `pass intentsolutions/plane/api-key` |

No language runtime required. No Docker required. No package manager required.

### Zero to Reading

1. `git clone https://github.com/jeremylongshore/intent-eval-lab && cd intent-eval-lab`
2. `cat README.md` — get the one-paragraph context: research umbrella for measuring AI plugin / agent / MCP server quality across CLI runtimes. Note the four-repo convergence framing (now five-repo with the kernel addition).
3. `cat CLAUDE.md` — get the session-level conventions: four-repo convergence, tier-1 vs tier-2 distinction, partner-consent discipline, lab-level conventions (doc filing, sandboxes, evidence, scripts).

### Then read the binding documents in this order (the foundation)

4. **`000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`** — read this **first** among the foundation docs. It is the binding ISEDC widened-scope architectural lock. Pay attention to: Q1 (ONE BIG, with stacked CTO + GC + CMO minority bindings); Q2 (per-artifact hybrid; TS-primary at signing surfaces); Q3 (unification thesis BINDING + incremental URI namespace + CISO per-predicate gates); Q5 (parallel-track sequencing with experimental-mode gate); Q6 (three-class governance routing); § 13.5 (acting-head-of-board override removing the customer-signal gate); § 13.6 (acting-head-of-board override removing external-pattern borrowing); § 11 (per-artifact fold-in plan). The verbatim seat positions in § 8 are the audit trail — read them at least once even if you don't need them daily.

5. **`000-docs/011-AT-ARCH-ecosystem-master-blueprint.md`** — Blueprint A. This is the *constitution*. § 1.2 contains the 12 binding principles every repo in the ecosystem inherits. § 2.1 contains the 5-repo taxonomy (the kernel was added in master plan Addendum #3, so the original four-repo framing here is forward-superseded). § 2.3 contains the three-class governance routing. § 3 contains the **anti-goals** (binding scope control — these are co-equal to the goals). § 4.2 contains the engineering standards every repo must honor.

6. **`000-docs/012-AT-ARCH-platform-runtime-blueprint.md` § 7** — Blueprint B's NORMATIVE Evidence Bundle Predicate Contracts section. This is the canonical `gate-result/v1` predicate body. The full Blueprint B is ~964 lines including the 13-entity domain model (§ 2); read it in full if you'll be implementing against the kernel, otherwise § 7 plus § 2 entity summaries are enough.

7. **`000-docs/014-DR-GLOS-canonical-glossary.md`** — the canonical glossary. The alphabetical cross-reference index at § 9 is the lookup table you'll use most often. Every term in every other doc traces back here.

### Then understand how the 4 sibling repos consume these specs

8. `cat ../intent-eval-core/000-docs/005-AA-AUDT-appaudit-devops-playbook.md` — the kernel audit. Shows how the 13-entity domain model from Blueprint B § 2 is materialized as Zod validators + JSON Schemas + lifecycle state machines in `@intentsolutions/core@0.1.0`. Published 2026-05-17 with sigstore provenance.

9. `cat ../audit-harness/000-docs/003-AA-AUDT-appaudit-devops-playbook.md` — the deterministic-gates audit. Shows how the polyglot CLI (Node + shell + Python) consumes the kernel's `gate-result/v1` predicate body to emit Evidence Bundle rows.

10. `cat ../j-rig-binary-eval/000-docs/019-AA-AUDT-appaudit-devops-playbook.md` — the behavioral-judge + rollout-gate-logic audit. Shows how `@j-rig/rollout-gate` consumes Evidence Bundle rows + a `tests/TESTING.md`-shaped policy to produce ship/no-ship verdicts.

11. `cat ../intent-rollout-gate/000-docs/002-AA-AUDT-appaudit-devops-playbook.md` — the GitHub Action shell audit. Shows how the thin Action shell delegates all decision logic to `@j-rig/rollout-gate`.

### Then optional secondary reading

12. **`000-docs/013-AT-SPEC-repo-blueprint-template.md`** — Blueprint C. The per-repo blueprint template. Authoring guidance + minimal example + validation checklist. Useful when applying Blueprint C to a new repo (or to one of the existing sibling repos that hasn't yet adopted it: `iah-E01`, `iaj-E01`, `iar-E01`, `iec-E10`, `iel-E05` self-application).
13. **`000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md`** — DR-004. The Session 1 5 binding constraints (predicate URI namespace, partner-consent vendor-generic, MM-7 defer, OTel CSO sequence, provider PASS/FAIL gates). Read for the foundational bindings that DR-010 § 10 reaffirms.
14. **`000-docs/FUTURE.md`** — deferred insights catalog. Shows what is recognized-but-not-yet-ready and the trigger conditions for graduation to active work.
15. **`KNOWN-ISSUES.md`** — operational footnotes. Read once for the `bd auto-flush JSONL drift` workaround; the workaround is mandatory for any session that mutates bead state.

### Common Setup Problems

| Symptom | Cause | Fix |
|---------|-------|-----|
| `partner-name-guard.yml` CI fails on a PR | Partner-name leak in `000-docs/`, `specs/`, `README.md`, `CLAUDE.md`, or `KNOWN-ISSUES.md` | Replace partner names with vendor-generic phrasing per DR-004 S1Q2 allowed terms (e.g., "the primary client engagement," "an active revenue client," "an enterprise partner engagement"). See `000-docs/014-DR-GLOS-canonical-glossary.md` § 8 "Vendor-generic discipline" for canonical phrasing. The `da1185a` audit-cleanup PR is the canonical example. |
| `bd update` appears to succeed but state is gone next session | Upstream `bd auto-flush JSONL drift` bug (KNOWN-ISSUES.md) | Apply the `bd-safe` wrapper: `bd export 2>/dev/null > /tmp/bd-snapshot.jsonl && \cp -f /tmp/bd-snapshot.jsonl .beads/issues.jsonl && bd import .beads/issues.jsonl && bd backup sync`. The bug is tracked upstream at the linked beads issue tracker; until it's fixed, the workaround is operator-dependent. |
| Two parallel PRs both propose `000-docs/0NN-...md` for the same NNN | NNN sequence-counter collision (Decision 8) | The losing PR (later merge time) renames its file to the next available NNN. Check `ls -1 000-docs/ | grep -E "^[0-9]{3}-" \| tail -1` before authoring. |
| `bd-sync link` fails because Plane credentials are absent | The Plane API key isn't in `pass intentsolutions/plane/api-key` or the env var `PLANE_API_KEY` | `pass insert -e intentsolutions/plane/api-key`; same for `workspace-slug` and `api-host-url`. The umbrella CLAUDE.md § "Bead ↔ GitHub Issue ↔ Plane Issue three-layer mirror" has the canonical credential path. |
| A normative Decision Record edit lands without the corresponding sibling-repo update | Drift between authoring (here) and adoption (the four sibling repos) | Verify each sibling repo's CLAUDE.md cross-reference is up to date; file a bead for the missing adoption work; mirror via `bd-sync`. Architect C1/C2 deferrals track the longer-term CI-gate solution. |

---

## 7. Operations

### Command Map

| Task | Command | Notes |
|------|---------|-------|
| Read the foundation | `cat 000-docs/010-AT-DECR-*.md \| less` | DR-010 first; then 011 (Blueprint A), 012 (Blueprint B), 014 (glossary). |
| Find the right Decision Record | `ls 000-docs/*AT-DECR* \| less` | Filing convention is `NNN-AT-DECR-<title>-<date>.md`; index at `000-docs/000-INDEX.md`. |
| Verify the partner-name guard locally | `grep -rEni --include='*.md' --include='*.html' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.txt' "<REDACTED — pattern in ~/000-projects/CLAUDE.md private umbrella>" 000-docs/ specs/ README.md CLAUDE.md KNOWN-ISSUES.md` | Must return 0 hits. Mirrors the CI workflow at `.github/workflows/partner-name-guard.yml` line 60. Pattern redacted from this public artifact 2026-05-20 per DR-004 S1Q2. |
| Compute the next NNN for a new doc | `LAST_NUM=$(ls -1 000-docs/ \| grep -E "^[0-9]{3}-" \| tail -1 \| cut -d'-' -f1); NEXT_NUM=$(printf "%03d" $((10#${LAST_NUM:-0} + 1))); echo "$NEXT_NUM"` | Adapted from the appaudit numbering algorithm. |
| List beads ready to claim | `cd ~/000-projects && bd ready` | bd workspace is at the umbrella level, not in this repo. |
| Mirror a bead to GitHub + Plane | `bd-sync link <bead> --gh OWNER/REPO#N --plane LAB-N` | Three-layer mirror; the IDs are the synchronization substrate. |
| Apply the bd auto-flush workaround | (the `bd-safe` wrapper from `KNOWN-ISSUES.md`) | Required for any session mutating bead state. |
| Create a new ISEDC Decision Record | (manual; invoke `/exec-decision-council` skill, then file at `000-docs/NNN-AT-DECR-<title>-<date>.md`) | Per Doc Filing Standard v4.3; verbatim seat positions per ISEDC discipline. |
| Push to main (after PR + review) | `git push origin <feature-branch>` then merge via `gh pr merge` | Auto-deploys per `partner-name-guard.yml`; no separate deploy step. |
| View latest commit | `git log -1 --stat` | n/a |

### Deployment

The repository has no separate deployment surface. "Deploy" means "merge to `main`":

- **Pre-flight checklist:** PR is open; CI (the partner-name-guard workflow) is green; CODEOWNERS reviewer has approved; the new document is correctly numbered per Doc Filing Standard v4.3; any new Decision Record preserves verbatim seat positions per ISEDC adversarial-integrity protocol.
- **Execution:** `gh pr merge <N> --squash` (or `--merge` for atomic Decision Record landings where preserving commit-level history is useful). The 7-day public archive binding from DR-010 § 7 Q6 VPDevRel non-negotiable floor means the merged content is publicly visible on `main` immediately.
- **Verification:** GitHub's commit-level UI confirms the merge; the partner-name-guard workflow runs on push-to-main as a backstop; the bd-sync three-layer mirror updates via `bd-sync close <bead> --also-close-gh --also-close-plane`.
- **Rollback:** Per the Blueprint A § 1.2 principle 4 ("Rollbacks always possible"). Since normative artifacts are intended to be immutable once ratified, "rollback" means filing a *new* Decision Record that amends or supersedes the prior one — not git-reverting the prior PR. Git revert is permitted for typo corrections and pre-merge mistakes; never for substantive normative amendments. Example: a hypothetical DR-010 amendment would land as DR-NNN that explicitly amends DR-010 § X, not as a force-push rewriting DR-010 directly.

### Monitoring & Alerting

- **Dashboards:** None. GitHub's commit history is the only operational surface. The bd-sync `status` command is the cross-system drift detector.
- **SLIs/SLOs:** Not formally defined. The implicit availability target is "GitHub's" (whatever GitHub's uptime is). The implicit time-to-public-DR-archive target is the DR-010 § 7 Q6 VPDevRel non-negotiable floor of 7 days.
- **On-call:** None. Solo maintainer; bandwidth-budgeted at 3-5 hrs/wk.

### Incident Response

| Severity | Definition | Response Time | Playbook |
|----------|------------|---------------|----------|
| P0 | A merged Decision Record contains a verbatim-discipline violation (paraphrased seat position, missing dissent, etc.) | Within 24 hours | File a new Decision Record (NNN-AT-DECR) amending the violating record; preserve the original's verbatim content; explicitly cite the amendment in both records. Never silently edit the violating record. |
| P0 | Partner name leaked into a public artifact (CI gate failed open, or the inline backstop pattern diverged from the private umbrella pattern) | Immediate | Revert the offending commit if pre-merge; if merged, file an audit-cleanup PR (PR #56 is the canonical example) sweeping the leak and updating the inline backstop pattern in `.github/workflows/partner-name-guard.yml` to match the private umbrella. Notify any affected partner. |
| P1 | A Blueprint citation is broken (a sibling repo cites Blueprint X § Y but § Y no longer exists or has different content) | Within 1 week | File a bead under `iel-` prefix; mirror via bd-sync; cite the broken citation in the bead description. Fix forward by amending the citation in the consuming repo, not by rewinding the Blueprint amendment. |
| P1 | The bd auto-flush JSONL drift causes a bead-state-loss incident across multiple sessions | Within 1 week | Apply the `bd-safe` workaround documented in `KNOWN-ISSUES.md`. Manually verify the most recent bead state changes since the last successful `bd export → cp → bd import` cycle. Reconstruct state from the GH-issue + Plane-issue mirrors if needed. |
| P2 | NNN sequence-counter collision at PR-merge time | Within 24 hours | The later-merging PR renames its file to the next available NNN. Update any inbound cross-references. |

---

## 8. Things That Will Bite You

Ordered by likelihood × impact, drawing from real sharp edges in the repository.

### 8.1 Decision Record mutation discipline

- **Symptom:** A merged `NNN-AT-DECR-<title>-<date>.md` gets edited in place to "fix wording" or "smooth out an inconsistency."
- **Cause:** Git makes mutation trivially easy. The ISEDC adversarial-integrity protocol requires preservation of verbatim seat positions, but the protocol is human discipline, not a CI enforcement.
- **Fix:** **Don't.** Once a Decision Record is merged to `main`, treat it as immutable. Amendments happen by filing a *new* Decision Record (next NNN) that cites the prior record and explicitly amends section X. The two canonical override examples in DR-010 (§ 13.5 customer-signal gate removal; § 13.6 external-pattern non-borrow) are recorded *inline* with the original council position so the audit trail preserves both halves. Future overrides follow the same inline-recording discipline within the same DR, or land as a new DR if the override happens after-the-fact.
- **Prevention:** The CODEOWNERS gate on `/000-docs/` (`@jeremylongshore`) catches most accidental edits at PR-review time. A stronger automated gate would be a CI check that diffs any `000-docs/*AT-DECR*.md` modification against the previous merge and refuses to merge if section headers or seat-position content changed — currently not implemented; would require deferral resolution at Architect C1.

### 8.2 Partner-name vendor-generic enforcement: inline backstop vs private umbrella drift

- **Symptom:** The CI workflow `partner-name-guard.yml` passes locally and in CI, but a partner name appears in a public artifact that was caught by neither the CI scan nor the human-driven review.
- **Cause:** The CI workflow uses an inline pinned pattern at `.github/workflows/partner-name-guard.yml` line 53. The canonical pattern lives in the PRIVATE umbrella `~/000-projects/CLAUDE.md`. If a new partner name is added to the canonical pattern but *not* propagated to the inline backstop (or vice versa), the CI catches a smaller set of partner names than the human-driven scrub catches. PR #56 (`da1185a`) was the audit-cleanup that identified this drift the first time.
- **Fix:** Maintain lockstep updates: any change to the canonical pattern in the private umbrella requires a corresponding PR to update the inline backstop in this workflow file. The PRIVATE umbrella is the source of truth; the inline backstop is the CI-only defense-in-depth.
- **Prevention:** The PR template (`.github/PULL_REQUEST_TEMPLATE.md`) could include a checkbox: "Did this PR touch the partner-name discipline? If yes, are both the private canonical pattern and the public inline backstop updated?" Currently not implemented.

### 8.3 NNN sequence-counter collision on parallel work

- **Symptom:** Two PRs both propose `000-docs/0NN-...md` for the same NNN; the second PR fails to merge with a git conflict, or worse, the merge succeeds and one PR silently overwrites the other.
- **Cause:** The Document Filing Standard v4.3 NNN counter is global per-directory. Two simultaneous PRs both checking "what's the latest NNN?" at the same moment will both compute the same next NNN. PR review cadence is typically slow enough that this doesn't happen in a single-maintainer context, but it could happen in a multi-author workflow.
- **Fix:** The later-merging PR renames its file to the next available NNN and updates any inbound cross-references. Update the 000-INDEX.md.
- **Prevention:** A PR template checkbox: "Confirm the NNN is unique against `main`." A stronger guard would be a CI check that asserts no NNN collision against the latest `main`. Currently not implemented.

### 8.4 Schema duplication temptation

- **Symptom:** A new spec module under `specs/<class>/v0.1.0-draft/schema/` defines a JSON Schema that *should* reference the kernel's canonical schema in `@intentsolutions/core@0.1.0`, but instead duplicates the content inline.
- **Cause:** Convenience. Authoring a self-contained `schema/` directory is faster than navigating the kernel's published package layout to construct a pointer.
- **Fix:** Per the open bead `iel-link-schemas-to-kernel`, the lab's own `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` is the canonical example of this drift; it duplicates content that should now point to `@intentsolutions/core/schemas/v1/gate-result.schema.json`. The cleanup is to replace the duplicated content with a JSON `$ref` to the kernel package's published URL, or with a markdown pointer if the schema isn't being consumed programmatically from the spec.
- **Prevention:** Blueprint C § 5 (Canonical entities used) should be applied to every per-repo blueprint to document which kernel schemas the repo's specs reference; any non-pointer schema duplication surfaces in the application of the template.

### 8.5 `labs.intentsolutions.io` reserved-don't-touch binding

- **Symptom:** A new blog post, RFC published-version page, or methodology landing page accidentally references an `evals.intentsolutions.io`-style predicate URI in the `labs.` subdomain space, or vice versa.
- **Cause:** The two subdomains are *philosophically* close — both relate to the Intent Eval Platform — but operationally *isolated*. `evals.intentsolutions.io` is for predicate URIs (DNSSEC + CAA pinned before first signed Rekor anchor). `labs.intentsolutions.io` is reserved-don't-touch for predicate URIs (it may host blog content, methodology landing pages, RFC published-version pages, or Phase-C content surfaces — but **never** an in-toto predicate URI, OTel attribute namespace, or attestation predicate identifier).
- **Fix:** Never sign a Statement v1 with a predicate URI under the `labs.` namespace. Never publish an OTel attribute that uses the `labs.` namespace as its root. If a draft document accidentally uses the `labs.` namespace for an attestation surface, file a Decision Record correcting the namespace choice before any signed artifact lands.
- **Prevention:** Blueprint A § 4.2 naming standards + `000-docs/014-DR-GLOS-canonical-glossary.md` § 8 anti-patterns explicitly call out the binding. A CI gate could scan for `labs.intentsolutions.io` appearances near `predicateType` / `predicate-uri` / `attestation` / `OTel` keywords; currently not implemented.

### 8.6 bd auto-flush JSONL drift

- **Symptom:** `bd update` and `bd note` commands appear to succeed during a session, but next session the bead state has reverted to an earlier export.
- **Cause:** Upstream `bd`'s auto-export step fails on `git-add` when `.beads/` is gitignored (which it is in this repo and the umbrella), silently losing in-memory writes between sessions. Documented at `KNOWN-ISSUES.md`.
- **Fix:** The `bd-safe` wrapper function in `KNOWN-ISSUES.md` is the documented workaround. Wrap state mutations in `(...)` subshell with EXIT trap to atomically `bd export → cp → bd import → backup sync` after the mutation completes.
- **Prevention:** Operator-dependent until the upstream fix lands. The audit-trail caveat: a session that crashes after a bead state mutation but before the EXIT trap fires will leave the canonical bd state behind the GH/Plane mirrors. For audit-grade reconstruction, treat any bead state change made after the most recent successful `bd export → cp → bd import` cycle as provisional until manually verified.

### 8.7 Trying to add executable code to this repo

- **Symptom:** A contributor proposes adding TypeScript / Python / Go code to this repository — a validator, a judge implementation, a CLI tool, a Docker image.
- **Cause:** The lab's role as governance-as-spec-repo (Decision 7 above) is not always intuitive. A new contributor may expect that since the lab *defines* the platform, it should also *implement* it.
- **Fix:** Refuse the PR. Direct the contributor to the appropriate sibling repo: `intent-eval-core` for canonical contracts; `audit-harness` for deterministic gates; `j-rig-skill-binary-eval` for behavioral judges + rollout-gate decision logic; `intent-rollout-gate` for the thin Action shell. A reference implementation that genuinely belongs in the lab (a methodology-only demonstration with no other natural home) lives under `intent-eval-lab/reference-implementations/<name>/` per the DR-006 Q3 binding; the bar for that placement is high.
- **Prevention:** `CONTRIBUTING.md` documents what the repo accepts and what it explicitly does not accept. The `/specs/` directory is the place to add new methodology specs; `/000-docs/` for new Decision Records; `/research/` for new research-track artifacts.

### 8.8 ISEDC overhead — using the full council for Class-2 or Class-3 decisions

- **Symptom:** A relatively small change — a CI workflow tweak, a typo correction, a validator version bump — triggers a full ISEDC convening, burning ~3 founder-hours that the CFO bandwidth gate (DR-010 § 7 Q6: ~12 founder-hours/year governance overhead) cannot afford.
- **Cause:** Mis-routing. The auto-trigger list in Blueprint A § 2.3 is the deterministic routing rule, but a contributor unfamiliar with the routing may default to the most-thorough class.
- **Fix:** Re-route. Class-2 decisions (operational, CI workflow changes, validator version bumps when no new emitted-attestation surface is introduced) produce a *pair Decision Record* (`NNN-AT-DECR-pair-<title>-<date>.md`) authored by CTO + VP DevRel together. Class-3 decisions (code-level inside an existing sub-component's scope) produce a one-line entry in `000-docs/SOLO-DECISIONS.md`. The 7-day public-archive binding applies to Class 1 and Class 2; Class 3 may optionally be public.
- **Prevention:** The routing flowchart in Blueprint A § 5.3 (Mermaid diagram) is the visual aid; reading it before convening helps. The CFO bandwidth gate is itself the cost-control mechanism (over-budget governance triggers a re-scope, not silent over-budget).

---

## 9. Security & Access

### Access Control

| Role | Purpose | Permissions | MFA |
|------|---------|-------------|-----|
| `@jeremylongshore` (acting head of board, solo maintainer) | All authoring, review, merge, release | Owner on the GitHub repo; `pass` access to `intentsolutions/plane/*` credentials | Yes (GitHub) |
| External contributor | Open issues; submit PRs against `/specs/`, `/research/`, `/000-docs/` (within the allowed-change rules in `CONTRIBUTING.md`) | Read-only on the repo; PR submission via fork | Per contributor's own GitHub account |

### Secrets

- **Where:** No secrets in this repo. The PRIVATE umbrella `~/000-projects/CLAUDE.md` is gitignored and lives only on the maintainer's machine. The `pass` store at `intentsolutions/plane/{api-key, workspace-slug, api-host-url}` (and the env var fallbacks) is used by `bd-sync` for the Plane mirror; not invoked from CI.
- **Rotation:** Not applicable for this repo (no secrets). The umbrella's Plane API key rotation is per umbrella CLAUDE.md policy.
- **Emergency access:** Single maintainer; emergency access = the maintainer. No break-glass procedure is formally documented; for the repository's archival role this is acceptable since GitHub's own access-recovery suffices.

### Honest Security Assessment

What is **implemented**:

- CODEOWNERS reviewer-lock on `/000-docs/`, `/.github/workflows/`, `/specs/`. Effective for preventing accidental overwrites of normative content by external PRs that might otherwise auto-merge under a different policy.
- Partner-name guard CI workflow. Effective as a backstop against the partner-name vendor-generic discipline violation, with the caveat about inline-backstop-vs-private-umbrella drift (§ 8.2 above).
- Dependabot config at `.github/dependabot.yml` for GitHub Actions ecosystem (the only "dependency" surface this repo has).
- bd-sync three-layer mirror — provides cross-system redundancy: a corruption of any one layer (bd workspace, GitHub Issues, Plane) leaves the other two as recovery substrate.
- Apache 2.0 license at repo root; matches all four siblings.

What is **aspirational** or **not implemented**:

- No automated diff-against-previous-merge check on `000-docs/*AT-DECR*.md` to enforce immutability. § 8.1 documents the human-discipline approach; a CI gate would be stronger.
- No automated cross-repo Blueprint-citation verification. § 8.4 + Architect C1/C2 deferrals.
- No threat model for the case of a maintainer-account compromise. The single-maintainer + GitHub-owned model has a single-point-of-failure dimension.
- No signed commits requirement (`commit.gpgsign`). External contributors do sign via DCO (`git commit -s`) per `CONTRIBUTING.md`, but in-repo commits from the maintainer are not GPG-signed by default. The settings file (`~/.claude/settings.json`) configures attribution but not signing.
- No automated check that the bd-sync three-layer mirror is up to date at PR-merge time. Drift detection is via the operator running `bd-sync status` periodically.
- The `KNOWN-ISSUES.md` upstream `bd auto-flush JSONL drift` bug is a real audit-trail integrity hazard that has no automated mitigation; the documented workaround is operator-dependent.
- No formal SECURITY.md scope for "Decision Record mutation after ratification" as a security concern, even though it is the highest-impact integrity risk for the repository's product.

---

## 10. Cost & Performance

### Monthly Costs

| Resource | Cost | Notes |
|----------|------|-------|
| GitHub repo hosting (public) | $0 | Free tier; public repo. |
| GitHub Actions minutes (partner-name-guard workflow) | <$0.10 | One workflow, runs on PR + push-to-main; <5 seconds per run; well within free-tier minutes for public repos (Actions usage for public repos is free). |
| Domain (`labs.intentsolutions.io`, `evals.intentsolutions.io`) | shared with the parent Intent Solutions infrastructure | Allocated under the parent umbrella's DNS budget, not separately billed to this repo. |
| Storage of `research/000-DR-FIND-*.pdf` (289 KiB) | $0 | Within Git LFS-free zone (no LFS configured); regular Git tracking. |
| Maintainer time | 0-2 hrs/wk (during active phases like Phase A foundation); near-zero during steady-state | The 3-5 hrs/wk umbrella bandwidth from DR-010 § 7 Q5 covers all five sibling repos plus this one combined. |

### Performance

- **Latency:** N/A — no request path. The repository is read by humans via the GitHub UI and by Claude Code sessions; both are interactive surfaces with sub-second cold-read latency.
- **Throughput:** N/A — no throughput dimension. The maximum cadence at which Decision Records land is roughly one per ISEDC convening; convenings happen roughly quarterly (DR-010 § 7 Q6 standing) plus ad-hoc.
- **Error budget:** Not formally defined. The implicit error budget on the partner-name-guard CI workflow is "zero false negatives on the inline pattern; false positives are catchable in review."

### Scaling Limits

- **The 000-docs/ flat layout breaks down at ~200 entries.** Beyond that, an `ls -1 000-docs/` becomes a 200-line scroll; sub-categorization becomes more legible than the flat layout. Current count: 15 entries; the breakdown point is years away at the current ISEDC cadence.
- **The NNN sequence-counter is 3 digits; rolls at 999 docs.** Not a practical concern.
- **The single-maintainer governance model breaks down past 1-2 hrs/wk total commitment.** If platform demand grows past the maintainer's bandwidth budget, the model needs multi-maintainer extension (additional ISEDC seats; reviewer rotation). DR-010 § 7 Q5 explicitly assumes solo-maintainer for the foreseeable future.
- **The bd-sync three-layer mirror breaks down past ~5 simultaneous active beads per mirror operation.** Larger fan-outs become operator-tedious; the underlying bd-sync command is fine, but the human-driven cross-checking after `bd-sync status` is the practical bottleneck.

---

## 11. Current State

### What's Working

- **The Phase A foundation is on `main`.** Five PRs landed between 2026-05-13 and 2026-05-15: `#50` (DR-010), `#52` (Blueprint A), `#53` (Blueprint B), `#54` (Canonical Glossary), `#55` (Blueprint C). Plus `#56` (`da1185a`, 2026-05-15+) — audit cleanup with partner-name vendor-generic scrub + canonical repo-name fixes + 2 fact-citation corrections + the `partner-name-guard.yml` CI workflow. Evidence: `git log --oneline -50` shows the merge commit sequence; `ls 000-docs/` shows the 15 normative artifacts plus `000-INDEX.md` and `FUTURE.md`.
- **Doc Filing Standard v4.3 applied uniformly.** Every doc in `000-docs/` follows the `NNN-CC-ABCD-<title>-<date>.md` convention. Evidence: `ls -1 000-docs/` lists the 15 docs in canonical sequence.
- **ISEDC discipline preserved verbatim.** DR-010 § 7 contains the per-question vote tallies + verbatim seat positions + decision-with-stacked-minority-bindings; DR-010 § 8 contains the council memos verbatim. Evidence: lines 71-390 of `000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`.
- **The two acting-head-of-board override addenda are captured inline.** DR-010 § 13.5 (Q5 customer-signal gate removal) and § 13.6 (Q4 external-pattern non-borrow) are recorded with the original council positions preserved alongside the reversals. Evidence: lines 518-636 of DR-010.
- **The partner-name-guard CI is operational.** `.github/workflows/partner-name-guard.yml` enforces case-insensitive grep against `000-docs/`, `specs/`, `README.md`, `CLAUDE.md`, `KNOWN-ISSUES.md`. Evidence: PR #56 is the canonical example of the workflow catching and fixing a leak.
- **The CODEOWNERS reviewer-lock is operational.** `/000-docs/`, `/.github/workflows/`, `/specs/` are gated to `@jeremylongshore`. Evidence: `.github/CODEOWNERS` lines 1-15.
- **The bd-sync three-layer mirror is established for all 525 IEP beads** per the umbrella CLAUDE.md current state.
- **The kernel publication unblocked downstream adoption.** `@intentsolutions/core@0.1.0` published 2026-05-17 with sigstore provenance per the umbrella CLAUDE.md; the lab's Blueprint B § 2 13-entity domain model is now materialized as TypeScript types + JSON Schemas in a published package.

### What Needs Attention

- **[HIGH]** Lab's own `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` duplicates content that should reference `@intentsolutions/core@0.1.0`. -> Impact: downstream consumers face an ambiguity about which schema is canonical (the kernel is, but the lab's spec doesn't yet point to it). -> Fix: replace the duplicated content with a `$ref` or markdown pointer; tracked at the open bead `iel-link-schemas-to-kernel`. Estimated effort: 1-2 hours.
- **[HIGH]** Architect C1 (gate-result/v1 spec location) was tagged as RESOLVED via the kernel's `gate-result.schema.json`, but the resolution implicitly requires the previous bullet to land (the lab schema pointing to the kernel). Until that lands, the C1 resolution is partial. -> Impact: same as above. -> Fix: same as above.
- **[HIGH]** Consumer-side adoption beads (`iah-E02` audit-harness imports kernel; `iaj-E02` j-rig migrates @j-rig/core schemas to the kernel; intent-rollout-gate consumer migration) are open and queued. -> Impact: until they land, each sibling carries its own local-schema definitions; drift between local schema and kernel schema is detectable but not enforced. -> Fix: per the umbrella CLAUDE.md's "Next-ready" list, claim each bead in order (`iah-E02` first as the simplest consumer; then `iaj-E02`; then intent-rollout-gate). Estimated effort: 1-2 founder-days per sibling.
- **[MEDIUM]** Architect C2 (intent-rollout-gate role) — open. -> Impact: the intent-rollout-gate's role as "thin Action shell delegating to `@j-rig/rollout-gate`" is documented in Blueprint A § 2.1 but the M5.1 runtime implementation is still on a feature branch. -> Fix: M5.1 v0.1.0-experimental ships per DR-010 § 7 Q5 parallel-track sequencing; the lab carries no direct work here, but the lab's role as authority surface is paused on this open deferral. Estimated effort: external to this repo.
- **[MEDIUM]** Security C-2 (Rekor pre-flight) — open. -> Impact: DNSSEC + CAA hardening on `evals.intentsolutions.io` is a CISO non-negotiable before first production-Rekor anchor (DR-010 § 7 Q5). Until verified, all signing happens on sigstore staging. -> Fix: external infrastructure work; the lab carries the binding (Blueprint A § 4.2 naming standards) but not the implementation. Estimated effort: hours of DNS work + verification.
- **[MEDIUM]** Security C-3 (signing_mode in DSSE — covered by SigningMode enum in kernel) — partially addressed. The kernel materializes the enum; the lab's Blueprint B § 7 references it normatively. -> Impact: the lab's role is binding-text; the kernel's role is materialization; the integration is consistent. -> Fix: no lab-side action needed; verify the kernel's enum stays in sync with the Blueprint B § 7 language across future amendments.
- **[MEDIUM]** Architect W1 (tenant_id reservation) — open at `bd_000-projects-k0fj`. -> Impact: multi-tenant boundaries are forward-deferred to `021-AT-ARCH-multi-tenant-boundaries.md` (iel-E13c, not yet authored). Reserving `tenant_id` in current schemas now would prevent a future-breaking change; not reserving it requires a SemVer-MAJOR bump when multi-tenancy is added. -> Fix: a small Decision Record adding `tenant_id` as an optional field across the canonical-domain-model schemas in Blueprint B § 2 with the explicit "reserved-for-iel-E13c" annotation. Estimated effort: 2-4 hours including ISEDC Class-2 routing.
- **[MEDIUM]** DR-011 ratification record — open. -> Impact: per the umbrella CLAUDE.md "Audit deferrals open" list. Likely a follow-up Decision Record formalizing post-Phase-A ratification of choices that were provisional during Phase A. -> Fix: file as Class-1 ISEDC at the next standing quarterly convening. Estimated effort: ~3 founder-hours.
- **[LOW]** Customer-signal gate removal (DR-010 § 13.5) hasn't been swept across sibling-repo READMEs. -> Impact: residual marketing-customer language in `audit-harness`, `j-rig-skill-binary-eval`, `intent-rollout-gate` READMEs that pre-dates the override and contradicts the lab's current positioning. -> Fix: a sweep PR per sibling repo, swapping out customer-acquisition framing for honest engineering output framing. Estimated effort: 1-2 hours per sibling.
- **[LOW]** Upstream `bd auto-flush JSONL drift` bug — open at `bd_000-projects-ufc` + upstream `gastownhall/beads#3848` + `#3970`. -> Impact: audit-trail integrity hazard documented in `KNOWN-ISSUES.md`. -> Fix: external to this repo; until upstream lands a fix, the `bd-safe` workaround is mandatory. Estimated effort: zero on the lab side.
- **[LOW]** No automated immutability gate on `000-docs/*AT-DECR*.md`. -> Impact: § 8.1 documents the human-discipline approach; a CI gate would be stronger. -> Fix: a GitHub Action that compares each PR's `000-docs/*AT-DECR*` modifications against `origin/main` and fails if section headers or seat-position content changed without a corresponding new amendment record being filed. Estimated effort: 4-6 hours.

### Implementation Status

| Component | Status | Evidence |
|-----------|--------|----------|
| Phase A foundation (5 PRs) | Complete | `git log --oneline` shows merge commits for #50, #52, #53, #54, #55, #56 |
| Doc Filing Standard v4.3 application | Complete (15 docs in `000-docs/`) | `ls -1 000-docs/` |
| ISEDC discipline (verbatim preservation) | Complete | `000-docs/010-AT-DECR-...md:71-390` (council positions); `:518-636` (override addenda) |
| Partner-name guard CI | Operational | `.github/workflows/partner-name-guard.yml` (78 lines); PR #56 is the canonical sweep example |
| CODEOWNERS reviewer-lock | Operational | `.github/CODEOWNERS` lines 1-15 |
| Canonical Glossary cross-referenced from Blueprints A + B | Complete | `000-docs/014-DR-GLOS-canonical-glossary.md`; `011-AT-ARCH-...md:200-214` references it; `012-AT-ARCH-...md` references it throughout |
| `gate-result/v1` predicate normative body | Folded into Blueprint B § 7 | `000-docs/012-AT-ARCH-platform-runtime-blueprint.md:33` documents the fold |
| `specs/evidence-bundle/v0.1.0-draft/schema/` kernel-pointer cleanup | **Open** (drift bead `iel-link-schemas-to-kernel`) | The duplicated JSON Schema content exists at `specs/evidence-bundle/v0.1.0-draft/schema/` |
| Per-repo blueprint application (`iah-E01`, `iaj-E01`, `iar-E01`, `iec-E10`, `iel-E05`) | **Open** | These are per-sibling beads; the lab's role is providing Blueprint C as the template |
| iel-E11 (replay fidelity levels RF-0..RF-4) | **Deferred** | Forward-referenced from Blueprint B § 4.2 + Glossary § 7; not yet authored |
| iel-E12 (runtime event taxonomy / canonical OTel events) | **Deferred** | Draft exists at `001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`; normative authoring deferred |
| iel-E13c (multi-tenant boundaries / tenant_id reservation) | **Open** (`bd_000-projects-k0fj`) | Architect W1 deferral |
| iel-E14b (economics / cost governance) | **Deferred** | Forward-referenced from Blueprint B § 2.2 + § 4.2 |
| Customer-signal gate removal sweep across sibling READMEs | **Open** | Sibling-repo READMEs have residual marketing-customer language |
| Bd auto-flush JSONL drift upstream fix | **Open** (external) | `bd_000-projects-ufc`; KNOWN-ISSUES.md |

---

## 12. Roadmap

### Week 1 — Stabilization

- Close the schema-duplication drift: file `iel-link-schemas-to-kernel` PR replacing the lab's duplicated `gate-result.schema.json` content with a pointer to `@intentsolutions/core/schemas/v1/gate-result.schema.json`. **Outcome:** downstream consumers have one unambiguous canonical source for the schema; Architect C1 is fully resolved.
- File `tenant_id` reservation as a Class-2 (or Class-1 if it materially alters the kernel's published schema surface) ISEDC pair Decision Record. **Outcome:** future multi-tenancy work (iel-E13c) does not require a SemVer-MAJOR break on the published kernel.
- Sweep the four sibling READMEs for residual marketing-customer language per DR-010 § 13.5 override. **Outcome:** the four siblings present consistent honest-engineering framing matching the lab's positioning.

### Month 1 — Foundation

- Author `intent-eval-lab/specs/UNIFICATION.md` per DR-010 § 7 Q3 unification thesis discipline. Reference from every constituent repo's CLAUDE.md. **Outcome:** the unification thesis has a single canonical citation point; every constituent repo's link surface is bound to the same text.
- Author `intent-eval-lab/specs/PREDICATE-TYPES.md` registry per DR-010 § 7 Q3 GC discipline. List every URI subtype, first-signed-attestation date, Decision Record link. **Outcome:** the predicate-URI namespace is publicly registered in lockstep with first-signed events; namespace audit is a one-stop lookup.
- Apply Blueprint C to each sibling repo: `iah-E01` (audit-harness), `iaj-E01` (j-rig-binary-eval), `iar-E01` (intent-rollout-gate), `iec-E10` (intent-eval-core), `iel-E05` (lab self-application). **Outcome:** every sibling has a per-repo blueprint matching the template; cross-repo consistency is enforceable by review.
- Author the iel-E11 normative SPEC for replay-fidelity levels RF-0..RF-4. **Outcome:** the forward-references from Blueprint A § 4.2, Blueprint B § 3.2, Glossary § 7 all resolve.

### Quarter 1 — Strategic

- Author the iel-E12 normative SPEC for runtime event taxonomy (canonical OTel events: `agent.rollout.gate.*`, `agent.evidence_bundle.*`). Land the iel-E12 RFC at OTel SIG-GenAI per the S1Q4 CSO sequencing binding (informal-email-first; RFC filing Week 4+ informed by routing feedback). **Outcome:** the OTel surface is a normative interoperability contract, not a draft.
- Author iel-E13c multi-tenant boundaries SPEC. Apply the `tenant_id` reservation from Week 1 to the full canonical-domain-model. **Outcome:** the platform is multi-tenancy-capable on paper; implementation remains future-bandwidth-gated.
- Author iel-E14b economics + cost governance SPEC. Forward-referenced from Blueprint B § 2.2 + § 4.2. **Outcome:** cost-attribution is a normative contract, not an implementation choice.
- File DR-011 ratification Decision Record at the next standing quarterly ISEDC convening. **Outcome:** Phase A provisional choices are formally ratified.
- Begin Phase B work on the 11 validators' `--emit-evidence` retrofit per DR-010 § 7 Q3 unification thesis. Sequenced after intent-rollout-gate M5.1 v0.2 cuts to production Rekor. **Outcome:** every validator in the claude-code-plugins ecosystem emits Evidence Bundle rows; the unification thesis is realized end-to-end.

---

## 13. Quick Reference

### URLs

| Resource | URL |
|----------|-----|
| Public repo | https://github.com/jeremylongshore/intent-eval-lab |
| Public DR archive | (this repo's `main` branch `000-docs/` directory) |
| Plane HQ | https://projects.intentsolutions.io (LAB project, LAB-6 / IEL-CONV-1 in the Intent Eval Platform module) |
| Sibling: intent-eval-core | https://github.com/jeremylongshore/intent-eval-core |
| Sibling: audit-harness | https://github.com/jeremylongshore/audit-harness |
| Sibling: j-rig-skill-binary-eval | https://github.com/jeremylongshore/j-rig-skill-binary-eval |
| Sibling: intent-rollout-gate | https://github.com/jeremylongshore/intent-rollout-gate |
| Published kernel | https://www.npmjs.com/package/@intentsolutions/core (v0.1.0 with sigstore provenance) |
| Reserved-don't-touch domain | `labs.intentsolutions.io` (blog / methodology landing only — NEVER predicate URIs) |
| Predicate URI namespace | `evals.intentsolutions.io/<predicate-type>/v<version>` (DR-004 Q1 + DR-010 § 7 Q3 grammar lock) |
| ISEDC reusable skill | `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0 |

### First-Week Checklist

- [ ] Access granted (GitHub repo read; `bd` workspace at `~/000-projects/.beads/`; `pass intentsolutions/plane/*` for the bd-sync mirror)
- [ ] Local clone in place (`git clone https://github.com/jeremylongshore/intent-eval-lab && cd intent-eval-lab`)
- [ ] Foundation read in order: DR-010, Blueprint A, Blueprint B § 7 + § 2 summaries, Canonical Glossary § 9 alphabetical index
- [ ] Sibling-repo audits skimmed: intent-eval-core 005, audit-harness 003, j-rig-binary-eval 019, intent-rollout-gate 002
- [ ] `bd ready` from `~/000-projects` shows the next-ready beads
- [ ] `bd-sync status` shows no drift between bead / GH / Plane mirrors
- [ ] KNOWN-ISSUES.md read; `bd-safe` wrapper either sourced into shell or aliased
- [ ] Run the partner-name guard locally against the working tree (see § 7 Command Map) before any PR
- [ ] Met with system owner (in this case: the acting head of board) to confirm next-priority claim ordering

---

## Appendices

### A. Glossary

This audit defers terminology to the canonical glossary at `000-docs/014-DR-GLOS-canonical-glossary.md`. Per Blueprint A § 4.1, every other doc cross-references the glossary rather than redefining. The terms used heavily in this audit that the glossary covers in depth:

- **ISEDC** (§ 5 of the glossary) — Intent Solutions Executive Decision Council
- **Acting head of board** (§ 5) — Jeremy Longshore; final-call authority
- **Class 1 / Class 2 / Class 3 routing** (§ 5) — the three-class governance routing
- **Decision Record** (§ 5) — `NNN-AT-DECR-<title>-<date>.md`
- **Override** (§ 5) — the acting-head-of-board reversal pattern (DR-010 § 13.5 and § 13.6 are canonical)
- **Ratification** (§ 5) — subsequent ISEDC session reaffirming or revising an earlier decision
- **Predicate URI** (§ 6) — typed identifier for an Evidence Bundle row class
- **in-toto Statement v1** (§ 6) — the wrapping structure for signed software-supply-chain attestations
- **DSSE** (§ 6) — Dead Simple Signing Envelope
- **cosign** (§ 6) — the signing CLI from sigstore
- **Rekor** (§ 6) — the sigstore immutable transparency log
- **EXPERIMENTAL mode** (§ 7) — the operational state for `v0.x` releases on sigstore staging
- **Phase A / Phase B / Phase C** (§ 7) — the platform's three-phase sequence
- **`labs.intentsolutions.io` reserved-don't-touch** (§ 8) — predicate URIs live only at `evals.intentsolutions.io`
- **Vendor-generic discipline** (§ 8) — DR-004 S1Q2 partner-name binding
- **External-pattern non-borrow** (§ 8) — DR-010 § 13.6 override

### B. Reference Links

| Reference | Path |
|---|---|
| DR-004 (Session 1, 5 binding constraints) | `000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md` |
| DR-005 (terminology rename matcher-map -> Intentional Mapping) | `000-docs/005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md` |
| DR-006 (Session 3, Phase B gate, lifted by user override) | `000-docs/006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md` |
| DR-010 (Session 4, widened-scope architectural lock) | `000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md` |
| Blueprint A (ecosystem master / constitution) | `000-docs/011-AT-ARCH-ecosystem-master-blueprint.md` |
| Blueprint B (kernel specification) | `000-docs/012-AT-ARCH-platform-runtime-blueprint.md` |
| Blueprint C (per-repo template) | `000-docs/013-AT-SPEC-repo-blueprint-template.md` |
| Canonical Glossary | `000-docs/014-DR-GLOS-canonical-glossary.md` |
| FUTURE.md (deferred insights catalog) | `000-docs/FUTURE.md` |
| OTel paper-trail file | `000-docs/009-RR-INTL-otel-sig-genai-temperature.md` |
| System brief (HTML, ~6k words) | `000-docs/007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html` |
| M1 Foundation gap analysis | `000-docs/008-DR-GAPS-spec-vs-system-brief-2026-05-11.md` |
| Phase B scope refinement | `000-docs/003-PP-PLAN-phase-b-scope-refinement.md` |
| MCP testing bridge landscape (~6,257w) | `000-docs/002-RR-LAND-mcp-testing-bridge.md` |
| OTel agent rollout-gate signals RFC draft | `000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` |
| Operational footnotes | `KNOWN-ISSUES.md` |
| Partner-name guard CI workflow | `.github/workflows/partner-name-guard.yml` |
| CODEOWNERS | `.github/CODEOWNERS` |
| Sibling: intent-rollout-gate audit | `../intent-rollout-gate/000-docs/002-AA-AUDT-appaudit-devops-playbook.md` |
| Sibling: audit-harness audit | `../audit-harness/000-docs/003-AA-AUDT-appaudit-devops-playbook.md` |
| Sibling: intent-eval-core audit | `../intent-eval-core/000-docs/005-AA-AUDT-appaudit-devops-playbook.md` |
| Sibling: j-rig-binary-eval audit | `../j-rig-binary-eval/000-docs/019-AA-AUDT-appaudit-devops-playbook.md` |
| ISEDC reusable skill | `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0 |
| Master plan | `~/.claude/plans/se-the-council-bubbly-frog.md` |
| Epic + bead plan v2.1 | `~/.claude/plans/se-the-council-bubbly-frog-epics-and-beads-for-review-v2.1.md` |

### C. Troubleshooting Playbooks

**Playbook: Partner-name leak detected in a public artifact (CI fails or audit identifies a leak)**

1. Identify the offending file(s) from CI output or the audit findings.
2. Replace each partner-name occurrence with the appropriate vendor-generic phrasing per the Canonical Glossary § 8 (e.g., "the primary client engagement," "an active revenue client," "an enterprise partner engagement," "the inaugural case study (engagement-private)").
3. Verify the replacement does not use negative-affirmation phrasing ("we don't mention X") — that itself violates DR-004 S1Q2.
4. Run the local partner-name grep against the working tree before committing.
5. If the leak revealed drift between the private umbrella's canonical pattern and the public inline backstop at `.github/workflows/partner-name-guard.yml` line 53, update both in the same PR.
6. PR title convention from the canonical PR #56 example: `fix(audit): partner-name scrub + repo-name canonicalize + fact citations + CI guard (#NN)`.

**Playbook: A merged Decision Record is found to contain a non-verbatim seat position or paraphrased dissent**

1. Do NOT edit the existing Decision Record in place. The git-revertable nature of markdown is the temptation; the ISEDC adversarial-integrity protocol is the discipline.
2. File a new Decision Record (next NNN) titled `NNN-AT-DECR-amendment-to-DR-NNN-<title>-<date>.md`.
3. Quote the violating paraphrase from the prior record verbatim. Reconstruct the seat position from session notes, conversation transcripts, or — if the original verbatim is lost — declare it lost and document the loss explicitly.
4. The new Decision Record is itself Class-1 routing (full ISEDC) if it materially alters the prior decision's binding force; Class-2 (CTO + VP DevRel pair) if it is a verbatim-discipline correction only.
5. Update `000-docs/000-INDEX.md` to cross-reference both records.
6. Mirror via bd-sync to GitHub Issue + Plane Issue per the three-layer mirror discipline.

**Playbook: A sibling repo's CI references a Blueprint § Y that no longer exists**

1. Identify the affected sibling repo and the broken citation.
2. File a bead under `iel-` prefix (lab-side) describing the broken citation, with sibling-repo issue references.
3. Determine whether the Blueprint amendment was correct (in which case the sibling repo's citation needs updating to point to the amended section) or whether the amendment broke something it shouldn't have (in which case a corrective amendment may be needed, with proper ISEDC routing).
4. Update the consuming repo's citation. Cross-reference the corrective bead in the PR.
5. Consider whether this incident justifies the Architect C1 / C2 deferral resolution: a CI gate that asserts "this repo's references to Blueprint X § Y are still valid against the current `main` of intent-eval-lab."

**Playbook: NNN sequence-counter collision at merge time**

1. The later-merging PR is the loser. Identify the next available NNN via `LAST_NUM=$(ls -1 000-docs/ | grep -E "^[0-9]{3}-" | tail -1 | cut -d'-' -f1); NEXT_NUM=$(printf "%03d" $((10#${LAST_NUM:-0} + 1)))`.
2. Rename the losing PR's file from `000-docs/NNN-...md` to `000-docs/NEW_NNN-...md`.
3. Update any cross-references in: the file's own frontmatter (if it self-references by NNN), `000-docs/000-INDEX.md`, any other doc citing the file by NNN.
4. Force-push the rename to the PR branch. Re-request review.
5. Update the consuming bead's notes via `bd-sync note <bead> "Renamed from NNN to NEW_NNN due to merge-time collision with PR #X"`.

**Playbook: Bd auto-flush JSONL drift causes state loss**

1. Verify the issue: compare `bd list --status in_progress` output against the GitHub Issue and Plane Issue mirrors. If the bead workspace shows fewer or older entries than the mirrors, drift is confirmed.
2. Reconstruct from mirrors: each linked GitHub Issue and Plane Issue should carry the bead ID in its description plus any mirrored comments. Use these to reconstruct the missing bead state.
3. Apply the canonical workaround: `bd export 2>/dev/null > /tmp/bd-snapshot.jsonl && \cp -f /tmp/bd-snapshot.jsonl .beads/issues.jsonl && bd import .beads/issues.jsonl && bd backup sync`.
4. Permanent mitigation: source the `bd-safe` wrapper function from `KNOWN-ISSUES.md` into the shell environment; use it for all bead-mutating commands.
5. Track the upstream fix at `gastownhall/beads#3848` + `#3970` (per the umbrella CLAUDE.md current state).

### D. Open Questions

1. **Should the lab carry a CI gate that diffs `000-docs/*AT-DECR*.md` modifications against the previous merge and fails if section headers or seat-position content changed without an explicit amendment record?** Current answer: not implemented; the human-discipline + CODEOWNERS approach is the live mitigation. The CI gate would strengthen the ISEDC adversarial-integrity protocol from "discipline" to "enforced." Estimated effort: 4-6 hours. Open for next quarterly ISEDC review.

2. **What's the right cadence for sweeping the four sibling repos' READMEs for residual marketing-customer language?** The DR-010 § 13.5 override is on `main` and binding; the sibling READMEs have not been swept. A single sweep PR per sibling is straightforward (1-2 hours each); the open question is whether to wait until each sibling's next natural touch cycle, or to schedule a coordinated sweep across all four simultaneously.

3. **Should the `specs/` placeholder modules (`cross-cli-discovery/`, `validator-contract-reliability/`, `forecasting-drift-detection/`, `decentralized-crypto-evaluation/`, `methodology/`) carry "RFC welcome" READMEs more explicitly, or should they be removed until an actual engagement justifies the structural slot?** Current state: the placeholder READMEs exist and document the "RFC welcome" stance. Argument for removal: they create the appearance of more substance than exists. Argument for retention: they signal intent and reserve the structural slot for a future engagement, consistent with the platform's wedge-then-expand strategy.

4. **Should the `tenant_id` reservation (Architect W1 deferral) land as a Class-2 (CTO + VP DevRel pair) or Class-1 (full ISEDC) Decision Record?** It materially affects the published kernel's schema surface, so Class-1 is the safe answer. The cost is governance overhead; the benefit is full adversarial review of a future-breaking-change-prevention mechanism. Recommendation: file as Class-1 at the next standing quarterly convening.

5. **What's the right archival surface for older Decision Records as the `000-docs/` flat layout grows?** The breakdown point (~200 entries) is years away at the current cadence, but the long-term question is whether to retain the flat layout, introduce sub-categorization (`000-docs/decisions/`, `000-docs/blueprints/`, `000-docs/research-findings/`), or adopt date-prefix + ULID sequencing. Recommendation: defer until ~100 entries (currently 15); the flat layout's advantages compound below that threshold.

6. **Should the lab carry a reference implementation of any kind under `intent-eval-lab/reference-implementations/<name>/`?** Per the DR-006 Q3 binding, reference implementations are permitted in the lab when they have no other natural home. Currently none exist. The open question is whether any specific class of demonstration artifact (e.g., a methodology-only end-to-end example showing Evidence Bundle row construction without depending on any sibling repo) would benefit from being co-located. Recommendation: defer until a specific need surfaces.

---

*Audit author: Claude Code as the `/appaudit` skill (model: opus); reviewed against the appaudit v2.0.0 template + writing guidelines at `~/.claude/skills/appaudit/`. Cross-references to the four sibling audits are pinned by file path; recent git log + repository state captured at HEAD on `feat/epic8-adversarial-bz3.2-bz3.6` (most recent merged commit `da1185a`, PR #56, 2026-05-15+).*

— Jeremy Longshore
intentsolutions.io
