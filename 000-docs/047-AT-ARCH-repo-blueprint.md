---
title: Repo Blueprint — intent-eval-lab
date: 2026-06-10
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
binding_authority: iel-E05
inherits_from:
  - intent-eval-lab/000-docs/011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A)
  - intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B)
  - intent-eval-lab/000-docs/013-AT-SPEC-repo-blueprint-template.md (Blueprint C — this template)
related_drs:
  - 004-AT-DECR (S1Q5 — provider PASS/FAIL gates; N/A here, no provider surface in this repo)
  - 010-AT-DECR (S4 — widened-scope lock; unification thesis BINDING)
  - 018-AT-DECR (S5 — j-rig kernel-adoption reconciliation; schema authority)
related_glossary:
  - intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md
filing_standard: Document Filing Standard v4.3
---

# Repo Blueprint — intent-eval-lab

**Beads:** `bd_000-projects-152`

## § 1 — Repo identity

| Field              | Value                                                                                                                |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **Repo name**      | `intent-eval-lab` (matches `gh repo view` and local working-dir name)                                                |
| **Type**           | `methodology` (with normative `spec` modules under `specs/`)                                                         |
| **Owner**          | per `CODEOWNERS` — `@jeremylongshore`                                                                                 |
| **Maturity**       | `v0.x experimental` (version.txt `0.2.0`; Phase A foundation complete)                                                |
| **Ecosystem role** | The methodology + specs umbrella — authors the Blueprints, the Canonical Glossary, the Decision Records, and the per-class normative spec modules every other ecosystem repo references. |
| **Bead prefix**    | `iel-` (per Blueprint A § 2.1 taxonomy)                                                                               |
| **Plane module**   | LAB → Intent Eval Platform module (LAB-6 / `IEL-CONV-1`)                                                              |

### 1.1 Dependencies (peer repos consumed)

| Peer repo            | Consumed at | Pinned range        | Cited blueprint                                                  |
| -------------------- | ----------- | ------------------- | --------------------------------------------------------------- |
| `intent-eval-core`   | build/test  | `>=0.2.0, <0.3.0`   | `intent-eval-core/000-docs/` (kernel; schema-redirect anchor)   |
| `audit-harness`      | test (CI)   | vendored snapshot   | `audit-harness/000-docs/` (vendored `.audit-harness/` + wrapper) |

The lab does NOT consume `j-rig-skill-binary-eval` or `intent-rollout-gate` at
build/test time — it oversees them methodologically (see § 5). Its lab schema is a
redirect stub (`$ref` to the kernel) per `019-AA-AACR-schema-repoint-iel-link-schemas-2026-05-21.md`.

### 1.2 Non-goals (inherited + repo-specific)

This repo inherits every anti-goal locked in Blueprint A § 3 (NOT a generalized
autonomous agent platform; NOT a workflow automation competitor; NOT a distributed
compute platform; NOT a no-code builder; NOT infinite orchestration; NOT trying to
be the union of every adjacent category; AISE 5-domain stack is internal scope-map,
NOT separate-brand surface). In addition, this repo specifically does NOT:

- Ship runtime/feature code into its spec modules ahead of empirical demonstration in a sandbox (methodology-first discipline; CLAUDE.md § "No premature productization").
- Become a plugin marketplace, a consulting practice page, a blog, or a single product — it is a research umbrella; products spin OUT of it (CLAUDE.md § "What this lab is NOT").

Scope-creep into any item above triggers ISEDC re-convene per Blueprint A § 2.3 governance routing.

---

## § 2 — Problem statement

The agentic-CLI ecosystem is converging on cross-tool conventions (`AGENTS.md`,
MCP, `SKILL.md`), but the empirical question — _does my plugin actually get
discovered and invoked correctly when the agent decides on its own?_ — has no
vendor-neutral answer. Vendors won't publish opinionated cross-CLI
invocation-measurement frameworks because they compete across the stack. That niche
is structurally available to a third party. This repo solves the **methodology**
half: it authors the constitution (Blueprint A), the kernel spec (Blueprint B), the
per-repo template (Blueprint C), the canonical glossary, the Decision Records, and
the per-class normative spec modules that the rest of the ecosystem implements. It
hands off to peer repos at the implementation boundary: deterministic gate code →
`audit-harness`; behavioral eval code → `j-rig-skill-binary-eval`; canonical
contracts → `intent-eval-core`; ship/no-ship Action shell → `intent-rollout-gate`.

---

## § 3 — Scope boundaries

### 3.1 In scope

- The platform constitution (Blueprint A), kernel spec (Blueprint B), per-repo template (Blueprint C), and Canonical Glossary.
- Per-class normative spec modules under `specs/` (Evidence Bundle, MCP-plugin observability, prompt evaluation, plus reserved structural slots).
- Decision Records (ISEDC), research/landscape reports, planning docs, and after-action records under `000-docs/`.
- Reusable test-harness/probe code under `scripts/`; per-experiment sandboxes under `sandboxes/`.

### 3.2 Out of scope (permanent, no FUTURE flag)

- Runtime execution of evaluation targets — that is `j-rig-skill-binary-eval`'s job, not the lab's.
- Canonical contract definitions (TS types / JSON Schemas / Zod validators) — those live in `intent-eval-core`; the lab's schema is a redirect stub, never a fork.
- Becoming a distributable product or marketplace — the lab is a filesystem research umbrella, not a SKU.

### 3.3 Deferred (FUTURE flag required)

| Deferred item                                      | Earliest milestone | FUTURE.md reference                       |
| -------------------------------------------------- | ------------------ | ----------------------------------------- |
| Phase B research-eval methodology normative content | Phase B kickoff    | `000-docs/FUTURE.md` + CHANGELOG Unreleased |
| OTel RFC filing (`agent.rollout.gate.*` taxonomy)  | iel-E12            | `000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` |

### 3.4 Anti-goals (binding-scope-control)

- **Inherited from Blueprint A § 3**: NOT a generalized autonomous agent platform; NOT a workflow-automation competitor; NOT the union of every adjacent category (cite Blueprint A § 3 in full).
- **Repo-specific**: the lab does NOT productize speculatively — publishable content (blogs, SKU pages) flows OUT of empirically-demonstrated experiments, never from a spec written ahead of a sandbox run. The failure mode prevented: shipping a "methodology" that has never been run, then being unable to defend it under expert review.

---

## § 4 — Architecture

### 4.1 Module layout

```text
intent-eval-lab/
├── 000-docs/   — numbered docs: Blueprints, Glossary, Decision Records, research, plans, AARs
├── specs/      — normative methodology output; versioned per-class spec modules + snapshots/ + upstream-surfaces/
├── research/   — literature surveys, paper notes, competitive landscape
├── sandboxes/  — per-experiment dirs (one dated subdir per run)
├── evidence/   — captured telemetry, OTEL traces, JSON evidence (mostly gitignored)
├── scripts/    — reusable test harness, OTEL probes, spec-drift + watcher-liveness + trilink validators
├── ci/         — zero-dep CI helpers
└── projects/   — symlinks to constituent project repos (gitignored)
```

### 4.2 Data flow

The lab is documentation-and-spec-authoring; its "data flow" is the authoring
pipeline: a methodology insight → a sandbox experiment under `sandboxes/` →
captured `evidence/` → a normative spec module under `specs/` → a numbered record
under `000-docs/`. The continuity machinery (spec-drift-watch + projection-diff +
watcher-liveness) is the only automated flow: upstream surface registry
(`specs/upstream-surfaces/registry.v1.json`) → snapshot diff → drift signal.

### 4.3 Runtime boundaries

| Concern                          | Specification                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------ |
| **Process model**                | no long-running runtime; CI jobs + ad-hoc `scripts/` invocations (Python + shell) |
| **IPC**                          | N/A — file-based artifacts only                                                |
| **External services consumed**   | none in normal operation; CI may fetch upstream spec surfaces for drift-watch  |
| **Process isolation guarantees** | no user-code execution path; the lab emits docs + specs, not evaluated artifacts |

### 4.4 Storage needs

N/A — methodology/spec repo. No canonical Blueprint B § 2 entity is persisted by
this repo at rest; artifacts are git-tracked markdown, JSON spec files, and
(gitignored) ephemeral evidence.

### 4.5 External dependencies (cite by version)

| Dependency               | Range             | Purpose                                   | Notes                                       |
| ------------------------ | ----------------- | ----------------------------------------- | ------------------------------------------- |
| `@intentsolutions/core`  | `>=0.2.0, <0.3.0` | schema-redirect anchor (lab schema `$ref`) | Apache-2.0; strict-SemVer pin               |
| `audit-harness` (vendored) | snapshot         | L0–L2 gates (escape-scan, hash-pin)        | vendored at `.audit-harness/` + `scripts/audit-harness` wrapper |
| Python                   | `>=3.11`          | spec-drift + watcher-liveness scripts      | per `pyproject.toml`                         |

### 4.6 Failure boundaries

- **Crash boundary**: a script failure is local to one CI job; no shared runtime state to corrupt.
- **Retry boundary**: drift-watch / projection-diff are idempotent; safe to re-run.
- **Isolation guarantees**: no other ecosystem component depends on this repo's runtime — they depend on its committed docs/specs only.
- **Emitted FailureTaxonomy categories**: N/A — this repo does not emit `FailureTaxonomy` rows.

---

## § 5 — Canonical entities used

The lab AUTHORS the Blueprint B § 2 canonical-entity definitions (it owns the
glossary + Blueprint B) but does not itself consume or produce entity instances at
runtime. It references — never redefines — every entity via the canonical glossary.

| Entity            | Direction | Blueprint B Ref | Attributes implemented                                  | Glossary ref                              |
| ----------------- | --------- | --------------- | ------------------------------------------------------- | ----------------------------------------- |
| `EvidenceBundle`  | defines (spec) | `Blueprint B § 7` | Authors the `gate-result/v1` predicate contract; emits no instances | `014-DR-GLOS-canonical-glossary.md` § 2 |

**Entities NOT touched by this repo (as instances):** All 13 canonical entities
(EvalSpec, EvalRun, MatcherMap, EvidenceBundle, JudgeDecision, RuntimeReceipt,
RegressionPack, RolloutGate, SkillSnapshot, SessionTrace, ToolInvocation,
CostRecord, FailureTaxonomy) — the lab defines them in Blueprint B + the glossary
but produces/consumes no instances; entity I/O happens in the implementation repos.

---

## § 6 — Interfaces

### 6.1 CLI

N/A — no public CLI. Internal `scripts/` (Python + shell) are repo-local tooling
(`spec-drift-check.sh`, `spec-projection-diff.py`, `watcher-liveness.py`,
`validate-trilink.sh`, `bd-claim-precheck.sh`, `build-evidence-bundle.py`), not a
published command surface.

### 6.2 HTTP / gRPC APIs

N/A — no server.

### 6.3 Config files

| File                          | Schema                                                | Canonical example                          |
| ----------------------------- | ----------------------------------------------------- | ------------------------------------------ |
| `specs/upstream-surfaces/registry.v1.json` | upstream-surface registry (spec-drift input) | self (the committed registry)              |
| `.sops.yaml` + `.env.sops`    | SOPS + age secrets (provider keys for sandboxes)      | `secrets.example.yaml`                      |

### 6.4 Output formats

| Output              | Shape                                                                | Reference         |
| ------------------- | -------------------------------------------------------------------- | ----------------- |
| Normative spec module | versioned `SPEC.md` + JSON schema under `specs/<module>/vX.Y.Z-*/`  | `specs/README.md` |
| Evidence Bundle row | in-toto Statement v1 over DSSE; predicate body per Blueprint B § 7.4 (spec only — the lab defines the shape, peer repos emit it) | `Blueprint B § 7` |

### 6.5 Event schemas

| Event                       | Attributes              | OTel taxonomy                                            |
| --------------------------- | ----------------------- | ------------------------------------------------------- |
| `agent.rollout.gate.<event>` | (draft — not locked)   | `agent.rollout.gate.<subkey>` (per iel-E12, forward-ref) |

The OTel attribute taxonomy is drafted (`001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`)
but not filed; forward-reference iel-E12 until the RFC lands.

### 6.6 Public-API stability promise

- The Blueprint A/B/C heading hierarchy and the Canonical Glossary entry IDs are stable across MINOR bumps — downstream per-repo blueprints cite them by section number.
- The `specs/<module>/vX.Y.Z-*/` directory grammar is stable; a new spec version is an additive directory, never an in-place rewrite.

Breaking changes to either require MAJOR bump (Blueprint A § 4.2) AND a Class-2 pair Decision Record before merge.

---

## § 7 — Testing strategy

This repo is documentation + spec; only the L0–L2 layers and a spec-drift gate
apply. The 9 CI workflows under `.github/workflows/` enforce the policy floor.

### 7.1 L0 — git hooks (pre-commit)

- **In-scope checks**: escape-scan, partner-name grep, harness-hash verification, markdownlint, prettier (per `.pre-commit-config.yaml`).
- **Enforcement**: `scripts/audit-harness <subcommand>` (vendored install). NEVER `~/.claude/` paths.

### 7.2 L1–L2 — static analysis (lint + typecheck + escape-scan)

- **Lint**: markdownlint-cli2, Vale (prose), lychee (link integrity), Prettier (markdown) — all advisory on first install per `doc-quality.yml`; Ruff for Python.
- **Typecheck**: mypy for the Python scripts (`.mypy_cache` present).
- **Escape-scan**: `scripts/audit-harness escape-scan --staged` (vendored).

### 7.3 L3 — unit tests

| Concern                | Target                                                            |
| ---------------------- | ---------------------------------------------------------------- |
| **Framework**          | pytest (per `python-tests.yml`) for the `scripts/` drift tooling |
| **Coverage floor**     | tooling-scoped; advisory (research repo, not a product library)  |
| **Mutation kill rate** | N/A — mutation testing is layer-inapplicable for a spec repo     |
| **CI gate**            | `python-tests.yml`                                               |

### 7.4 L4 — integration tests

- Spec-drift round-trip: registry → snapshot → projection-diff produces a stable signal (`spec-drift-watch.yml`).
- Tri-link integrity: `validate-trilink.sh` confirms bead↔doc↔GH-issue cross-refs for refiner-labeled artifacts.

### 7.5 L5 — system tests

N/A — the lab touches no external services in normal operation and has no LLM
provider surface in its committed code (sandbox experiments are ephemeral and live
under `sandboxes/`, not the repo's shipped surface).

### 7.6 L6 — acceptance tests

N/A — no user-facing application flow to codify as Gherkin. Acceptance for the lab
is `/validate-consistency` clean against `000-docs/` + `README.md` + `CHANGELOG.md`.

### 7.7 L7 — chaos / property / fuzz

- **Applicability**: N/A — no executable application surface to fuzz; the drift-watch scripts are deterministic.

### 7.8 CI gates

The workflows a PR runs on merge:

```text
ci.yml                     — top-level orchestration
doc-quality.yml            — markdownlint + Vale + lychee + Prettier (advisory)
partner-name-guard.yml     — partner-name vendor-generic grep (HARD gate)
harness-hash-verify.yml    — scripts/audit-harness verify (HARD gate)
python-tests.yml           — pytest over scripts/ tooling
schema-drift.yml           — lab schema redirect-stub vs kernel drift
spec-drift-watch.yml       — upstream-surface drift detection
sign-evidence-bundle.yml   — evidence-bundle signing harness
release.yml                — tagged release packaging
```

**Hash-pin discipline**: after any policy edit, re-run `scripts/audit-harness init`
(vendored) and commit the updated `.harness-hash` in the same commit. Pre-commit
refuses unsigned policy edits by design.

### 7.9 Fixtures

| Concern                       | Specification                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| **Location**                  | per-experiment `sandboxes/<date>-<id>/fixtures/`                                      |
| **Naming convention**         | `<NNN>-<kind>-<slug>.<ext>`                                                           |
| **Vendor-generic discipline** | All fixtures scrubbed per DR-004 S1Q2 + DR-010 § 10; partner-name grep runs in CI.   |

### 7.10 Golden files (if applicable)

`specs/snapshots/.sha` holds spec-surface snapshot hashes; regenerations are
reviewed via the projection-diff gate, not mass-regenerated.

---

## § 8 — Security / isolation

### 8.1 Secrets management

| Secret class        | Storage                          | Broker            | Repo-specific                                |
| ------------------- | -------------------------------- | ----------------- | -------------------------------------------- |
| provider-api-key (sandbox-only) | SOPS-encrypted `.env.sops` (age) | `scripts/sops-env` wrapper | used only in ephemeral `sandboxes/`, never shipped surface |

**SOPS + age standard**: `.env.sops` committed; `.env` plaintext git-ignored; CI
receives the age key via `SOPS_AGE_KEY` GitHub Actions secret. NEVER decrypt to disk.

### 8.2 Sandbox model

No sandbox required for the repo's shipped surface — no user-code execution path.
Per-experiment work under `sandboxes/` is tear-down-after-run and never shares state
across experiments (CLAUDE.md § "Sandboxes").

### 8.3 Provider PASS/FAIL gates

N/A — this repo's shipped surface does not invoke LLM providers. Section present per
the Class-1 ISEDC requirement that the gate-restatement be visible even when not
exercised. The two non-negotiable provider gates (credential-redaction +
env-var-spillover, DR-004 S1Q5 / DR-010 § 10) bind any repo that DOES touch
providers (`j-rig-skill-binary-eval`); they are not exercised here because the lab's
committed code has no provider call path.

### 8.4 Audit logging

| Concern            | Specification                                                                 |
| ------------------ | ----------------------------------------------------------------------------- |
| **What is logged** | Decision Records (append-only under `000-docs/`); CI run logs                 |
| **Append-only**    | yes — Decision Records are never amended in place (Blueprint A § 1.2 principle 3) |
| **Signing**        | evidence-bundle artifacts signed per `sign-evidence-bundle.yml`               |
| **Retention**      | git history is the permanent record; no time-windowed expiry                  |

### 8.5 Threat model

An adversary with repo write access could publish a misleading spec or Decision
Record, or weaken a CI gate. Defenses: CODEOWNERS review on `/specs/`, `/000-docs/`,
and `/.github/workflows/`; harness-hash verification (tamper of vendored gates
hard-fails CI); partner-name guard (leak of a partner name hard-fails CI); SOPS
keeps sandbox provider keys encrypted at rest. The lab ships no executable product,
so the classic supply-chain-poisoning path through a published package does not
apply to this repo's own artifacts (it applies to `intent-eval-core`, which the lab
pins by strict-SemVer range).

---

## § 9 — Observability

### 9.1 OpenTelemetry events

N/A at runtime — the lab emits no live telemetry. The OTel event taxonomy it
DEFINES (`agent.rollout.gate.*`, `agent.evidence_bundle.*`) is drafted in
`001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`; emitting repos forward-ref
iel-E12 with `taxonomy_status: draft` until the RFC locks.

### 9.2 Trace propagation

N/A — no runtime spans.

### 9.3 Lineage capture

N/A — the lab populates no SessionTrace / RuntimeReceipt / ToolInvocation fields;
it defines their shape in Blueprint B + the glossary.

### 9.4 Log levels

| Level   | When                                                                 |
| ------- | -------------------------------------------------------------------- |
| `ERROR` | unrecoverable failure — operator action required                     |
| `WARN`  | degraded state — operation continues but signal is reduced           |
| `INFO`  | high-level lifecycle events — start, end, terminal state transitions |
| `DEBUG` | per-step diagnostics — disabled by default                           |
| `TRACE` | per-operation diagnostics — enabled only in test environments        |

Applies to the `scripts/` tooling only; the repo has no production daemon.

### 9.5 Failure taxonomy

N/A — this repo does not emit `FailureTaxonomy` rows.

---

## § 10 — Cost governance

N/A — no paid surface in the shipped repo. Sandbox provider spend is ephemeral,
experiment-scoped, and tracked per-experiment under `sandboxes/`, not at the repo
level. Cost-budget enforcement for the Skill Refiner / SAK aggregate is the CFO's
seat per `046-AT-STND-sak-governance-owners.md`, exercised in the implementation
repos, not here.

---

## § 11 — Release strategy

### 11.1 Versioning

**Strict SemVer** per Blueprint A § 4.2 (current: `0.2.0` per `version.txt`). MAJOR
for any breaking change to the Blueprint/Glossary section-ID stability promise
(§ 6.6) or the `specs/` directory grammar.

| Bump  | When                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------- |
| MAJOR | breaking change to § 6.6 stability promise; reshape of a Blueprint required section's contract    |
| MINOR | additive doc/spec module; new Decision Record; new optional spec field                            |
| PATCH | doc polish; typo fix; internal script refactor with no public-surface change                      |

### 11.2 Changelog

`CHANGELOG.md` per Keep a Changelog format (`Added` / `Changed` / `Deprecated` /
`Removed` / `Fixed` / `Security`). Every PR updates `## [Unreleased]`; the release
commit promotes `[Unreleased]` to the new version + date.

### 11.3 Migration notes

| Concern                      | Location                                                  |
| ---------------------------- | -------------------------------------------------------- |
| **Migration guide location** | inline in the affected Blueprint's "Drift handling" section |
| **Migration generator**      | hand-authored                                             |
| **Required for**             | every MAJOR bump (Blueprint reshape)                      |

### 11.4 Compatibility guarantees

- Across MINOR bumps: Blueprint section IDs + Glossary entry IDs + `specs/` version-dir grammar stay stable.
- Across MAJOR bumps: only items explicitly preserved in the MAJOR release notes.

### 11.5 Evidence retention discipline

Per Blueprint A § 4.2 + DR-010 § 7 Q5 CISO non-negotiable: production-Rekor signing
for any predicate URI is gated on that predicate's SPEC.md normative section landing.

| Predicate URI                            | Status      | SPEC.md ref         | Signing mode      |
| ---------------------------------------- | ----------- | ------------------- | ----------------- |
| `evals.intentsolutions.io/gate-result/v1` | conditional | `Blueprint B § 7`   | `sigstore_staging` |

The lab defines predicate shapes; emitting repos own the cutover.

### 11.6 License audit

Apache 2.0 (per `LICENSE`). Releases run a license audit on the resolved dependency
tree per DR-010 § 7 Q2 GC non-negotiable; GPL / AGPL deps are blocked at CI absent
explicit GC waiver.

---

## § 12 — Beads / work breakdown

| Concern               | Value                                                       |
| --------------------- | ----------------------------------------------------------- |
| **Bead prefix**       | `iel-` (per Blueprint A § 2.1)                              |
| **bd workspace**      | umbrella `~/000-projects/.beads/`                          |
| **Epic naming**       | `iel-E<NN>` (e.g., `iel-E05` — this blueprint)             |
| **Plane project**     | LAB                                                         |
| **Plane module**      | Intent Eval Platform (LAB-6 / `IEL-CONV-1`)               |
| **GH ↔ Plane mirror** | via `bd-sync` per global CLAUDE.md three-layer discipline   |

### 12.1 Cross-repo bead dependencies

- `iec-E11-*` — SAK kernel schema work the lab's SAK-INDEX + governance docs reference.
- `iah-self-pin` — the vendored harness-hash mechanism this repo adopted (AAR 020).

### 12.2 In-repo epic inventory

| Epic      | Status      | Purpose                                                              |
| --------- | ----------- | ------------------------------------------------------------------- |
| `iel-E04` | closed      | Blueprint C — repo blueprint template                               |
| `iel-E05` | in-progress | Repo blueprint — Blueprint C self-application (this document)        |
| `iel-E12` | open        | OTel RFC filing (`agent.rollout.gate.*` taxonomy lock)              |

---

## § 13 — Definition of Done

This repo is "complete enough to release" when **every** check below passes:

- [ ] All tests pass at the L0–L2 policy floors declared in § 7 (escape-scan, lint, harness-hash verify, partner-name guard).
- [x] Provider PASS/FAIL gates (§ 8.3) — N/A here (no provider surface in shipped code); section present-and-marked, not deleted.
- [x] All canonical entities referenced (§ 5) cite the glossary + Blueprint B; none redefined locally.
- [ ] License audit clean per § 11.6 (no GPL / AGPL absent explicit GC waiver).
- [ ] Partner-name vendor-generic grep returns 0 against all public-facing directories (current pattern from the ecosystem CLAUDE.md).
- [x] Evidence Bundle round-trip — N/A here; the lab defines the shape, emitting repos verify the round-trip.
- [ ] `CHANGELOG.md` entry written under `## [Unreleased]` (or promoted for the release commit).
- [ ] This per-repo blueprint matches reality — `/validate-consistency` clean against `000-docs/`, `README.md`, and `CHANGELOG.md`.
- [ ] Acting head of board sign-off (or designated approver per `CODEOWNERS`).
