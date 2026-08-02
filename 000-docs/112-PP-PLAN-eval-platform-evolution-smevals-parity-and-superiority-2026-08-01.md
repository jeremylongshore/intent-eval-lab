# Master Blueprint: Evaluation Platform Evolution

**Plan ID:** IEP-EVAL-EVOLUTION-001
**Status:** ACTIVE — PHASE 1 IN EXECUTION
**Date:** 2026-08-01
**Owner:** Intent Solutions
**Master bead:** `bd_000-projects-htjt`
**Canonical home:** `intent-eval-lab/000-docs/`
**Scope:** `intent-eval-core`, `intent-eval-lab`, `j-rig-binary-eval`, `audit-harness`, `intent-rollout-gate`, and `intent-eval-dashboard`

## 1. Executive decision

The Intent Eval Platform will evolve from a strong, skill-specific evaluation
and evidence system into a general evaluation substrate with a first-class
skill profile.

The platform will adopt the best product primitives demonstrated by `smevals`:

- declarative tasks and configurations;
- an executable, model- and harness-neutral runner contract;
- immutable raw run records;
- separate named graders with grader snapshots;
- regrading without re-running models;
- balanced repeated runs per task/config/model combination;
- uncertainty-aware reports;
- terminal, live, and static report surfaces.

It will retain and strengthen the capabilities that distinguish the Intent Eval
Platform:

- skill package, trigger, functional, adversarial, regression, baseline, and
  rollout-safety evaluation;
- external evaluator separation;
- blocker and sacred-regression semantics;
- coverage honesty and explicit skipped dimensions;
- cost and runtime telemetry;
- content-addressed evidence and kernel validation;
- signed Evidence Bundles and fail-closed rollout decisions;
- verified dashboard ingestion and C3-safe rendering.

### 1.1 Reference basis

The parity baseline is the public [Prime Radiant SMEvals article](https://primeradiant.com/blog/2026/smevals.html) and the [SMEvals README](https://github.com/prime-radiant-inc/smevals/blob/main/README.md), inspected on 2026-08-01. The comparison is capability-based, not a claim that the projects share an implementation or license. Local IEP findings come from the six sibling repositories and their current schemas, CLIs, evidence paths, and documentation; every implementation phase must replace a planning claim with executable acceptance evidence.

The target is not a copy of `smevals`. The target is a composable substrate in
which a generic model benchmark and a governed skill-release evaluation share
the same run/grade/report foundation, while their scoring policies remain
explicitly separate.

## 2. Current diagnosis

The current platform is technically deeper than a small eval CLI, but its
measurement loop is less cohesive.

### 2.1 Current strengths to preserve

- J-Rig already has real provider adapters, external judges, blocker criteria,
  baseline comparison, regression detection, cost accounting, vote evidence,
  SQLite persistence, and Evidence Bundle emission.
- The kernel provides content-addressed contracts, validation, state machines,
  and signed predicate boundaries.
- The rollout gate is fail-closed and delegates decision semantics to the
  published rollout package.
- The dashboard verifies evidence before rendering and protects the public
  surface from unverified or cross-dimension aggregate claims.
- The Skill Refiner already provides eval-set lineage, leakage/coverage checks,
  significance-aware acceptance, and content-addressed proposals.

### 2.2 Current gaps to close

1. J-Rig's public execution model is centered on `SKILL.md`, not an arbitrary
   executable harness.
2. J-Rig's `--samples` primarily samples judge votes; it does not provide a
   balanced target-N workflow for complete task/config/model executions.
3. Raw execution and grading are coupled in the main CLI path. There is no
   complete `grade --regrade` workflow over immutable captured runs.
4. The local report surface is a SQLite run inspector while the richer report
   surface lives in a separate dashboard ingestion/deployment path.
5. The name `EvalSpec` currently refers to two different contracts: the
   platform kernel's canonical entity and J-Rig's skill-specific YAML shape.
6. The local J-Rig checkout pins `@intentsolutions/core` at `0.9.0` while the
   platform's current canonical kernel is `0.10.0`.
7. Existing real-skill dogfood and batch work must be integrated with this
   substrate rather than duplicated.

## 3. Design principles and non-negotiables

### 3.1 Principles

1. **Raw evidence before judgment.** A model/harness execution is captured once
   and can be judged many times.
2. **Configuration is data.** Model, prompt, system instructions, tools,
   harness, provider, sampling parameters, and resource ceilings belong to a
   named Config, not hidden CLI state.
3. **Execution variance and judge variance are different.** The platform must
   record and report both.
4. **Policy is not a score.** Numeric reporting may describe a homogeneous
   population; rollout decisions remain policy-driven and fail-closed.
5. **The kernel owns stable contracts, not every implementation detail.** J-Rig
   owns its local run/grade store; the kernel owns cross-repo wire contracts and
   predicate schemas.
6. **Adapters are explicit.** A skill-specific profile may compile to a
   canonical EvalSpec, but it must not silently pretend to be the same shape.
7. **No silent coverage claims.** Every report and evidence row states what was
   evaluated, what was skipped, and why.
8. **Verified data only reaches public surfaces.** The dashboard continues to
   render only after signature, content, visibility, and policy checks.
9. **Every improvement must be dogfoodable.** A feature is not complete until
   the generic example and a real skill example use it.

### 3.2 Hard anti-goals

- No monorepo conversion.
- No unbounded schema growth in `intent-eval-core` merely to mirror internal
  SQLite tables.
- No aggregate PASS percentage across heterogeneous predicate types or
  unrelated dimensions.
- No model output treated as a harness failure merely because the answer is
  poor; non-zero runner exit is infrastructure evidence, while a real bad
  response remains gradable evidence.
- No regrading that mutates the raw Run.
- No public dashboard path that bypasses verified ingest.
- No production-Rekor or signed-decision claim where the existing contract
  still marks the operation reserved or deferred.

## 4. Target vocabulary

The following names are normative for the new substrate.

| Term            | Meaning                                                                                   | Owner                               |
| --------------- | ----------------------------------------------------------------------------------------- | ----------------------------------- |
| Suite           | A directory or manifest containing one or more Evals                                      | J-Rig                               |
| Eval            | A capability being measured; has tasks and metadata                                       | Core contract + J-Rig               |
| EvalSpec        | Canonical platform contract for an Eval                                                   | `intent-eval-core`                  |
| SkillEvalSpec   | J-Rig profile for `SKILL.md` criteria/test cases                                          | J-Rig                               |
| Task            | One challenge/exercise within an Eval                                                     | J-Rig profile/runtime               |
| Config          | One complete execution setup: model, provider, prompt/context, tools, harness, and limits | J-Rig                               |
| Runner          | Executable adapter that performs one Task under one Config                                | J-Rig                               |
| Run             | Immutable captured execution attempt and artifacts                                        | J-Rig store; kernel-linked identity |
| Checker         | One deterministic or external operation used by a Grader                                  | J-Rig                               |
| Grader          | Ordered checks plus scoring/outcome rules                                                 | J-Rig                               |
| Grade           | Immutable result of applying one named Grader to one Run                                  | J-Rig store                         |
| Evidence Bundle | Signed/validated cross-repo collection of attestations                                    | Core + emitters                     |
| Rollout policy  | Consumer-side allow/block/advisory rules                                                  | Rollout package                     |
| Report          | Human-readable projection of Runs and Grades                                              | J-Rig/dashboard                     |

### 4.1 EvalSpec identity decision

`EvalSpec` remains the canonical kernel term. The existing J-Rig YAML contract
will be explicitly named `SkillEvalSpec` in code and documentation, with a
versioned adapter to the canonical contract. The first adapter may be a
lossless profile mapping rather than a forced one-to-one field translation.

The adapter must preserve:

- the skill snapshot hash;
- criteria and test-case identity;
- model/provider/config identity;
- runtime limits;
- scoring and blocker policy;
- content hash and version;
- skipped/evaluated coverage;
- lineage to the resulting Run and Grade records.

If the canonical kernel must change, that change requires the existing
Class-1/Class-2 governance route and a compatibility fixture in every consumer.

## 5. Target architecture

```text
                         ┌────────────────────────────┐
                         │ Eval/Suite definition      │
                         │ tasks + configs + graders  │
                         └──────────────┬─────────────┘
                                        │
                           scheduler / balanced sampler
                                        │
                         ┌──────────────▼─────────────┐
                         │ Runner contract             │
                         │ skill | llm | agent | custom│
                         └──────────────┬─────────────┘
                                        │
                         ┌──────────────▼─────────────┐
                         │ Immutable Raw Run ledger     │
                         │ output + stderr + artifacts  │
                         │ config + hashes + lifecycle  │
                         └──────────────┬─────────────┘
                                        │ 1..N graders
                         ┌──────────────▼─────────────┐
                         │ Named Grader                 │
                         │ checks + judge + snapshot    │
                         └──────────────┬─────────────┘
                                        │
                         ┌──────────────▼─────────────┐
                         │ Immutable Grade              │
                         │ score + metrics + tags       │
                         │ outcome + artifacts          │
                         └───────┬───────────┬─────────┘
                                 │           │
                    report/serve/build       │ optional policy adapter
                                 │           │
                  ┌──────────────▼───┐  ┌────▼────────────────────┐
                  │ Local/static UI   │  │ Evidence Bundle         │
                  │ leaderboard/task │  │ kernel validation        │
                  │ lineage/artifacts │  │ rollout-gate/dashboard  │
                  └──────────────────┘  └─────────────────────────┘
```

The skill evaluator becomes a first-class Runner + Grader profile. It retains
its seven evaluation layers and rollout semantics; it no longer defines the
only valid shape of an evaluation.

## 6. Proposed on-disk and storage contract

The new suite layout is compatible with the existing skill workflow but can
represent arbitrary evaluations:

```text
my-eval/
├── eval.yaml                 # metadata/profile/version
├── tasks/*.yaml              # one challenge per file
├── configs/*.yaml            # model/prompt/harness configurations
├── graders/*.yaml            # named grading pipelines
├── runners/*                 # executable runner adapters
├── fixtures/                 # inputs and expected resources
└── runs/                     # generated; never edit by hand
    └── <task>/<config>/<model>/<sample>/
        ├── run.yaml          # written last; completion marker
        ├── output.txt
        ├── stderr.txt
        ├── manifest.json     # artifact names, sizes, hashes
        └── artifacts/*
            └── ...
```

The SQLite store remains useful for J-Rig query/report workflows, but the
on-disk Run representation is the portable interchange and recovery format.
SQLite rows must point to the immutable Run and Grade artifacts rather than
become the only copy of the evidence.

### 6.1 Raw Run rules

- The runner receives a resolved Task, Config, model, sample ID, run ID, and
  absolute run directory through a documented contract.
- Standard output is the candidate response; standard error is diagnostic.
- Exit zero means a response was produced, even if it is wrong.
- Non-zero exit means harness/infrastructure failure and is excluded from
  quality statistics but retained for debugging.
- `run.yaml` is written last and includes resolved inputs, timing, exit code,
  runner version, environment-safe metadata, and artifact manifest.
- The raw Run is immutable after completion. Re-execution creates a new sample.

### 6.2 Grade rules

- A Grade names the Run, Grader, Grader version/hash, and grading timestamp.
- The Grader definition is snapshotted beside the Grade.
- A Run can have `default`, `judge`, `security`, or other named Grades.
- `--regrade` deletes/replaces only the selected Grade namespace; it never
  changes the Run.
- Required checks halt later checks and mark them skipped, preserving the
  reason for the short circuit.
- Checkers may emit score, metrics, tags, notes, details, and artifacts.
- The Grade records raw checker output and the normalized result.

## 7. Measurement and statistics protocol

### 7.1 Two sampling layers

**Execution sampling** repeats the complete Task × Config × Model attempt. The
sampler runs balanced passes and tops each combination up to a target N. Failed
runner attempts do not count toward N, but remain in the ledger.

**Judge sampling** repeats only an external judge over the same captured output.
The Grade records each vote, aggregation rule, agreement, and judge identity.

The report must never label judge votes as execution samples.

### 7.2 Reported metrics

For homogeneous populations, reports may show:

- pass rate and sample count;
- mean score and standard error where a numeric score is meaningful;
- per-task and per-config breakdowns;
- failure count and harness-failure count separately;
- tag shares and metric distributions;
- judge agreement and calibration where available;
- execution cost, latency, and token usage;
- skipped coverage and reasons.

The existing binary rollout decision remains a separate policy output. A high
mean cannot override a blocker or sacred regression.

### 7.3 C3 protection

The report model must encode grouping keys explicitly. It must not produce one
rolled score across distinct predicate URIs, meters, tenants, or incompatible
dimensions. Cross-dimension comparison requires an explicit consumer policy and
is never inferred by the renderer.

## 8. Repository ownership and delivery order

### Phase 0 — Blueprint and authority lock

**Canonical repo:** `intent-eval-lab`
**Branch:** `feat/iep-eval-evolution-blueprint`
**Deliverables:** this blueprint, glossary additions, dependency map, bead
umbrella and repo epics.
**Gate:** plan review; no runtime code yet.

### Phase 1 — Contract reconciliation

**Repos:** `intent-eval-core`, `intent-eval-lab`, `j-rig-binary-eval`
**Branches:**

- `feat/iec-E10-eval-substrate-contracts` in `intent-eval-core`;
- `feat/iep-eval-evolution-blueprint` in `intent-eval-lab` for the current
  normative blueprint and any follow-up authority changes;
- `feat/eval-substrate-skill-profile` in `j-rig-binary-eval`.

**Deliverables:** SkillEvalSpec identity, canonical adapter/profile, current
kernel pin, compatibility fixtures, schema/version drift gate.

**Gate:** every consumer validates the same contract version; old J-Rig specs
remain readable through an explicit migration path.

### Phase 2 — Run and Grade substrate

**Primary repo:** `j-rig-binary-eval`
**Branch:** `feat/eval-substrate-run-grade`
**Deliverables:** Runner/Config contract, immutable raw Run ledger, artifact
manifest, named Graders, snapshots, `grade`, `--regrade`, migration tests.

**Gate:** generic non-skill example runs; one Run receives two Grades; regrade
changes only the selected Grade; raw bytes/hashes remain unchanged.

### Phase 3 — Sampling, suites, and reports

**Repos:** `j-rig-binary-eval`, `intent-eval-dashboard`
**Branches:**

- `feat/eval-substrate-sampling` and `feat/eval-substrate-report` in J-Rig;
- `feat/eval-substrate-dashboard-report` in the dashboard.

**Deliverables:** balanced target-N execution sampling, uncertainty metrics,
suite/batch workflow, terminal JSON/Markdown, live serving, static build, and
a unified report model.

**Gate:** three tasks × two configs × target N produces balanced samples and a
static report that exposes per-task results, uncertainty, lineage, and grader
version.

### Phase 4 — Evidence and rollout integration

**Repos:** `audit-harness`, `intent-rollout-gate`, `intent-eval-dashboard`
**Branches:**

- `feat/iep-audit-report-promotion-metadata` in audit-harness;
- `feat/iep-rollout-report-promotion` and stacked
  `feat/iep-rollout-skill-promotion` in intent-rollout-gate;
- `feat/eval-substrate-dashboard-report` and stacked
  `fix/eval-report-cli-separator` in intent-eval-dashboard.

**Deliverables:** contract/drift gates, generic-to-bundle adapter where
appropriate, rollout compatibility tests, verified public/internal rendering,
and no new signing claims beyond the current contract.

**Gate:** a real J-Rig skill Grade produces a kernel-valid bundle, rollout-gate
consumes it, and the dashboard renders only the verified result.

**Status:** implementation slices are delivered on draft PRs and have passed
their local gates. Audit-harness #145 adds the promotion metadata contract;
rollout-gate #57/#59 consumes report and skill-promotion rows with fail-closed
validation; dashboard #68/#70 renders the verified report and fixes the
documented pnpm argument-separator invocation. Merge/review and the separate
human-gated public route remain release controls.

### Phase 5 — Dogfood and release

**Repos:** all affected repos
**Branches:** per-repo `feat/eval-substrate-dogfood` only when a repo needs a
final integration patch; no direct main changes.

**Deliverables:** generic benchmark example, real skill shortlist, DeepSeek
ground truth where available, regression fixtures, migration guide, operator
runbook, release notes, package/version updates, and PRs.

**Gate:** all quality checks pass; evidence artifacts are attached to PRs;
branches are merged through normal CI; each repo is pushed and clean.

**Status:** the generic and real-provider dogfood receipts are complete. The
generic fixture exercised Run → Grade → unified report with idempotent Run
reuse. A pinned MiniMax M3 `audit-tests` run produced a kernel-valid
`j-rig/skill-promotion/v1` bundle; its 3/5 result is intentionally advisory and
the updated rollout consumer blocked promotion. The dashboard rendered the
generic report in an internal destination, refused the public destination, and
the existing signed J-Rig ingest/deploy receipts remain green. The remaining
release controls are PR merge/CI, a broader real-skill shortlist, and the
human-approved tailnet/public route.

## 9. Branch, commit, PR, and note discipline

### 9.1 Branch rules

- Never implement this plan directly on `main`.
- Use one feature branch per sibling repo and one logical concern per branch.
- Do not share a branch across repositories.
- Do not rewrite or delete existing user worktrees, untracked fixtures, or
  unrelated beads state.
- Branch from the repo's current main after a read-only status check. If main
  is behind origin, record that fact and rebase before opening the PR.

### 9.2 Commit rules

Use Conventional Commits with a plan/bead footer:

```text
feat(eval): add immutable raw Run artifact ledger

Implements the raw-run portion of IEP-EVAL-EVOLUTION-001.

Plan: IEP-EVAL-EVOLUTION-001
Bead: bd_000-projects-htjt.6
Repo: j-rig-binary-eval
Depends-on: htjt.2
Evidence: pnpm test; pnpm typecheck; generic-runner e2e
```

Keep commits reviewable and reversible. Separate structural refactors from
behavior changes. Do not mix documentation currency with runtime changes unless
the documentation is the acceptance evidence for that same change.

### 9.3 PR rules

Every PR must include:

- bead and blueprint IDs;
- scope and non-goals;
- dependency PRs/issues;
- migration and compatibility impact;
- tests and exact quality-gate commands;
- sample report/evidence artifacts;
- security/privacy notes;
- explicit statement of any skipped dimensions or deferred signing behavior.

PRs must be opened per repository, linked back to the master umbrella, and
merged in dependency order. The master umbrella is not closed until all child
beads, commits, PRs, documentation, and pushes are complete.

## 10. Documentation update matrix

| Document/surface                                                     | Required update                                               |
| -------------------------------------------------------------------- | ------------------------------------------------------------- |
| This blueprint                                                       | Normative plan, dependencies, gates, delivery record          |
| `intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md`         | Eval/Task/Config/Runner/Run/Grader/Grade terminology          |
| `intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md` | Run/Grade boundary and adapter architecture, if kernel-facing |
| `intent-eval-core` README/CHANGELOG                                  | Canonical schema/profile/version changes                      |
| `j-rig-binary-eval` README/CLI README                                | Generic quickstart, skill profile, migration, commands        |
| `audit-harness` README/CHANGELOG                                     | Drift/contract gate integration                               |
| `intent-rollout-gate` README/CHANGELOG                               | Bundle compatibility only; preserve reserved signing notes    |
| `intent-eval-dashboard` README/runbooks                              | Local/static report vs verified public ingest boundary        |
| umbrella `README.md` / `CLAUDE.md`                                   | Phase status, repo ownership, links to this blueprint         |
| Per-repo `AGENTS.md`/`CLAUDE.md`                                     | Branch, test, release, and cross-repo dependency notes        |

All normative claims must be updated in their owning repo first, then mirrored
into the umbrella. Historical status notes remain historical; do not rewrite
them to make the present look cleaner.

## 11. Acceptance demonstrations

### 11.1 Generic benchmark

Create a small haiku or structured-output Eval with:

- two Tasks;
- at least two Configs, including different model or prompt settings;
- one executable custom Runner;
- one deterministic Grader and one external-judge Grader;
- target-N full-run sampling;
- regrade over existing raw Runs;
- terminal JSON/Markdown plus a self-contained static report.

The demonstration must show that changing a Grader does not spend model tokens
again and that runner failures are not counted as model failures.

### 11.2 Skill benchmark

Run a real `SKILL.md` through the J-Rig profile with:

- package and trigger checks;
- functional and adversarial cases;
- separate judge provider when configured;
- execution and judge sample counts shown separately;
- baseline or regression layer explicitly enabled or explicitly skipped;
- Evidence Bundle emission;
- rollout-gate decision;
- verified dashboard render.

### 11.3 Convergence benchmark

The same report lineage must be traceable across:

```text
EvalSpec/SkillEvalSpec
  → Config + Task
  → Raw Run
  → Grade
  → report
  → optional gate-result/v1 Evidence Bundle
  → rollout decision
  → verified dashboard surface
```

## 12. Risks and mitigations

| Risk                                      | Mitigation                                                                          |
| ----------------------------------------- | ----------------------------------------------------------------------------------- |
| Kernel becomes a dump for J-Rig internals | Keep storage/runtime contracts in J-Rig; add only stable wire contracts to core     |
| Two specs drift again                     | One canonical name, explicit SkillEvalSpec profile, CI adapter fixtures             |
| Statistical reports imply unsafe rollup   | C3-safe grouping model and report tests                                             |
| Regrade leaks stale artifacts             | Grade namespace replacement plus grader snapshot/hash tests                         |
| Generic runner permits credential leakage | scoped environment, audit-harness cred-gate, redacted manifests, fixtures           |
| Batch workflow amplifies provider cost    | target-N caps, cost ceilings, resume semantics, explicit provider selection         |
| Dashboard exposes internal data           | reuse verified ingest and visibility policy; no raw local DB publication            |
| Current user changes are overwritten      | status checks, branch isolation, no destructive commands, explicit conflict handoff |
| Cross-repo release drift                  | dependency beads, version matrix, CI currency gate, PR dependency links             |

## 13. Execution record

This section is append-only. Each phase records branch, PR, commits, bead
closures, quality gates, and pushed revision.

### Phase 0

- Branch: `feat/iep-eval-evolution-blueprint`
- Bead: `bd_000-projects-htjt`
- Artifact: `112-PP-PLAN-eval-platform-evolution-smevals-parity-and-superiority-2026-08-01.md`
- Commits: `0217b32`, `57bc597`
- PR: [intent-eval-lab#258](https://github.com/jeremylongshore/intent-eval-lab/pull/258) (draft)
- Status: blueprint authored; repo-epic decomposition and dependency wiring complete

### Phase 1

- Branches: `feat/iec-E10-eval-substrate-contracts` in `intent-eval-core`; `feat/eval-substrate-skill-profile` in `j-rig-binary-eval`
- Commits: `de41909` (core); `62ae01d` (J-Rig)
- PRs: [intent-eval-core#84](https://github.com/jeremylongshore/intent-eval-core/pull/84); [j-rig-skill-binary-eval#247](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/247) (draft)
- Beads: `bd_000-projects-htjt.1`, `bd_000-projects-htjt.2`
- Status: identity and version-currency slice complete; explicit adapter, compatibility fixtures, and drift gate remain in progress

### Phase 2

- Branch: `feat/eval-substrate-run-grade` in `j-rig-binary-eval`
- Commit: `e9e51ce`
- PR: [j-rig-skill-binary-eval#248](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/248) (draft; stacked on #247)
- Bead: `bd_000-projects-htjt.6`
- Follow-on branch: `feat/eval-substrate-graders` in `j-rig-binary-eval`
- Follow-on commit: `14da36a`
- Follow-on PR: [j-rig-skill-binary-eval#249](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/249) (draft; stacked on #248)
- Follow-on bead: `bd_000-projects-htjt.7`
- Status: raw-run foundation plus deterministic named Graders, immutable snapshots, and explicit regrade are delivered; the full phase gate remains pending review and the later external-judge, sampling, suite, and report slices

### Phase 3

- Branch: `feat/eval-substrate-sampling` in `j-rig-binary-eval`
- Commit: `df5b43e`
- PR: [j-rig-skill-binary-eval#250](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/250) (draft; stacked on #249)
- Bead: `bd_000-projects-htjt.3`
- Follow-on branch: `feat/eval-substrate-report` in `j-rig-binary-eval`
- Follow-on commit: `09adb6e`
- Follow-on PR: [j-rig-skill-binary-eval#251](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/251) (draft; stacked on #250)
- Follow-on bead: `bd_000-projects-htjt.5`
- Dashboard branch: `feat/eval-substrate-dashboard-report` in `intent-eval-dashboard`
- Dashboard commit: `062bfb8` (rebased onto current `origin/main` `9306311`)
- Dashboard PR: [intent-eval-dashboard#68](https://github.com/jeremylongshore/intent-eval-dashboard/pull/68) (draft; consumes the J-Rig report contract from #251)
- Dashboard bead: `bd_000-projects-htjt.5` under epic `bd_000-projects-htjt.14`
- Status: balanced target-N planner, raw-run sampling joins, selected-Grader uncertainty metrics, `sample-plan`, local unified JSON/Markdown report projection, and a tailnet-only dashboard consumer are delivered; suite/batch execution, verified ingest/provenance, live static publication, and human-gated route remain

### Phase 4

- Branches: `feat/iep-audit-report-promotion-metadata` (audit-harness),
  `feat/iep-rollout-report-promotion` plus
  `feat/iep-rollout-skill-promotion` (intent-rollout-gate), and
  `feat/eval-substrate-dashboard-report` plus
  `fix/eval-report-cli-separator` (intent-eval-dashboard)
- PRs: [audit-harness#145](https://github.com/jeremylongshore/intent-audit-harness/pull/145),
  [intent-rollout-gate#57](https://github.com/jeremylongshore/intent-rollout-gate/pull/57),
  [intent-rollout-gate#59](https://github.com/jeremylongshore/intent-rollout-gate/pull/59),
  [intent-eval-dashboard#68](https://github.com/jeremylongshore/intent-eval-dashboard/pull/68),
  [intent-eval-dashboard#70](https://github.com/jeremylongshore/intent-eval-dashboard/pull/70)
- Beads: `bd_000-projects-htjt.13.2`, `bd_000-projects-htjt.13.4`,
  `bd_000-projects-htjt.14.5`, `bd_000-projects-htjt.4.2`
- Status: local quality gates and pushed revisions complete; draft PR review,
  merge order, and the public-route approval are still outstanding.

### Phase 5

- Branch: `feat/iep-eval-evolution-blueprint` in intent-eval-lab
- Bead: `bd_000-projects-htjt.4`; GitHub issue
  [intent-eval-lab#260](https://github.com/jeremylongshore/intent-eval-lab/issues/260);
  Plane `LAB-105`
- Tracking follow-up completed: child bead `bd_000-projects-htjt.4.3`, GitHub issue
  [intent-eval-lab#261](https://github.com/jeremylongshore/intent-eval-lab/issues/261),
  Plane `LAB-107`, for the pre-existing refiner tri-link debt exposed by the
  release-hardening verifier. Lab PR #262 (`1663dda`) fixed the false-positive
  parser; J-Rig PR #267 (`060bb2c`) restored its three headers; the workspace
  verifier now returns zero violations.
- Generic receipt: raw Run
  `raw_14a6b85edcc974734b0fbaeecf7968a58fc47df76ca06f4c1df6720a866b79dd`
  was reused on the repeat invocation; Grade
  `grade_8be8c72bd182c2a1044ea0906ca66e51d5dc7bebdac0346e354a36172b9b070d`
  passed at `1.0` using grader snapshot
  `sha256:5aaacc8f48da3d2728defc5d57f1445f179de1c4d17a34816f0b25a6d6ad2200`.
  The unified report had one attempted/completed/graded cell and no harness
  failures.
- Real-provider receipt: pinned source
  `claude-code-plugins-plus-skills@a9dd5c02a3793412ed35525efd460b399554be13`
  produced `evidence/phase5-dogfood/audit-tests-minimax-m3.bundle.json`
  (SHA-256 `a3b409f7534d2b33c1d21b1df1086c5c2851ca1454a388ceb8ac3cfdbe2e0344`).
  MiniMax-M3 scored `3/5` (`0.6`), with zero provider failures; the bundle is
  advisory, not promotion-eligible, and rollout-gate blocked it for that
  reason. No key, transcript, or local database is committed.
- Dashboard receipt: the internal render consumed the unified report and the
  signed ingest/deploy receipts are workflow runs
  [30734349474](https://github.com/jeremylongshore/intent-eval-dashboard/actions/runs/30734349474)
  and
  [30734361333](https://github.com/jeremylongshore/intent-eval-dashboard/actions/runs/30734361333);
  the public destination remains refused by policy.
- Status: dogfood evidence, release-hardening implementation, and tri-link
  cleanup are complete; the broader shortlist, PR merges/CI, and human-gated
  route remain release work.
