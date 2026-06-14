# 7-Layer Testing Taxonomy Spec — v0.1.0-draft

> **Status: NORMATIVE DRAFT.** This specification is the single source of truth for the
> **7-layer testing taxonomy** — the authoritative map of what a repository's testing system
> can include, ordered cheapest→most-expensive and closest-to-developer→closest-to-user. The
> `audit-tests` (diagnostic) and `implement-tests` (installer) skills reference THIS document
> for the canonical layer set, the per-layer concerns, and the walls that sit inside layers.
> Where a skill's own copy and this spec disagree about the taxonomy, this spec wins.
>
> **Why a central spec.** The taxonomy was previously embedded in each skill's reference
> material, which let the two skills' copies silently drift from each other. Promoting it to a
> versioned spec under `specs/` gives both skills one referent: the diagnostic skill maps a
> repo against THIS layer set; the installer skill installs missing layers from THIS layer set;
> a change to the taxonomy is one reviewed edit here, not an N-way reconciliation across skill
> copies.
>
> **Scope of authority.** This spec defines the _layers, their concerns, and the walls_. It
> does **not** mandate specific tools (tools are illustrative, not normative — § 3 R2), nor
> which layers apply to a given repo (that is a classification concern the diagnostic skill
> owns), nor the install order (the installer skill owns that). It defines _what the layers
> are_, so "layer 4" means the same thing in every repo that adopts the platform's testing SOP.
>
> **Authority precedence.** Where this spec touches ecosystem taxonomy or repo roles,
> [Blueprint A](../../../000-docs/011-AT-ARCH-ecosystem-master-blueprint.md) wins. The 7-layer
> testing taxonomy is an internal Intent Solutions pattern that may be cross-referenced freely
> (canonical glossary, "External-pattern non-borrow" → internal patterns).

## 1. Purpose

A repository's testing system is a stack of layers, each catching a distinct class of defect at
a distinct cost. Without a shared map, "we have tests" is unfalsifiable: it could mean a single
smoke test or a full pyramid. This taxonomy is that shared map. It lets a diagnostic tool
classify a repo, identify which layers are present / configured / enforced, and name the gaps
precisely — and lets an installer tool fill those gaps against the same layer definitions.

The taxonomy is ordered along two correlated axes:

- **Cost** — cheapest (a git hook firing in milliseconds) to most expensive (a stakeholder-run
  acceptance test taking days).
- **Proximity** — closest to the developer (a pre-commit hook) to closest to the user (business
  validation that the delivered thing solves the stated problem).

Layers are not a strict pyramid of _counts_ (a repo need not have more L3 tests than L6); they
are a stack of _concerns_, each with distinct failure modes. The **walls** (acceptance, unit,
coverage, mutation, CRAP, architecture) are _invariants enforced inside specific layers_, not a
parallel structure (§ 5).

## 2. Scope

### 2.1 In scope (v0.1.0-draft)

| Concern                                                                   | Where |
| ------------------------------------------------------------------------- | ----- |
| The seven layers + each layer's purpose and concern set                   | § 4   |
| The walls + which layer each wall lives inside                            | § 5   |
| Conformance obligations a repo's testing system has against this taxonomy | § 6   |
| The orthogonality between this taxonomy and the behavioral-eval tiers     | § 4.8 |

### 2.2 Out of scope (v0.1.0-draft)

- **Layer applicability per repo type.** Which layers a given repo _must_ implement (a library
  vs a web app vs a spec repo) is a classification concern owned by the diagnostic skill, not
  this taxonomy. This spec defines the layers; it does not decide which apply where.
- **Specific tool mandates.** Tools named in § 4 are illustrative of each concern, not
  normative requirements. A repo conforms by covering the _concern_, regardless of tool (R2).
- **Threshold values.** Concrete floors (coverage %, mutation kill-rate %, CRAP ceilings) are
  per-repo policy declared in the repo's `tests/TESTING.md`, not fixed by this taxonomy. This
  spec names the _wall_; the repo names its _threshold_.
- **Install order + scaffolding.** How missing layers are installed is the installer skill's
  concern.

## 3. Conformance keywords

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY** are used per
[RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) /
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174).

### R1 — The layer set is fixed at seven

The taxonomy has exactly seven layers, L1 through L7, in the order below. A conformant testing
system MUST classify each of its tests/gates as belonging to one of these layers. A test that
fits no layer indicates either a misclassification or a gap in this taxonomy (reported via § 7
RFC), not a new ad-hoc layer.

### R2 — Layers are defined by concern, not by tool

Each layer is defined by the _class of concern_ it covers, not by a specific tool. Tools listed
per layer are illustrative examples. A repo conforms to a layer by covering that layer's
concerns with _some_ tool; substituting an equivalent tool does not change conformance.

## 4. The seven layers

### 4.1 Layer 1 — Git Hooks & CI Enforcement

Stops bad changes before they land in the repo or propagate to CI.

| Concern               | Gate it provides                                |
| --------------------- | ----------------------------------------------- |
| Pre-commit hooks      | Installed; runs on `pre-commit`                 |
| Staged-file filters   | Only touches staged paths                       |
| Commit-message policy | `commit-msg` hook; CI lint                      |
| Pre-push hooks        | Runs unit + lint before push                    |
| CI pipeline           | On PR + merge; required checks enforced         |
| Branch protection     | Required reviews, status checks, signed commits |

### 4.2 Layer 2 — Static Analysis & Linting

No code execution — reads source and config. Fastest feedback; highest signal-to-noise on
style and common defects.

| Concern                                                        |
| -------------------------------------------------------------- |
| Linting                                                        |
| Formatting                                                     |
| Type checking                                                  |
| Complexity measurement (feeds the CRAP wall)                   |
| Secret scanning                                                |
| Dependency vulnerability scan                                  |
| Container image scan (distinct ecosystem from dependency scan) |
| IaC scan (distinct ecosystem)                                  |
| Doc lint (markdown structure)                                  |
| Prose lint (banned terms, anti-slop, house style)              |
| Link integrity                                                 |
| Doc formatting (Markdown table + code-fence)                   |
| Frontmatter / schema validation                                |

**Doc & prose quality is a first-class L2 concern**, not below-the-line. A broken link in a
deliverable or a banned-term leak in a public spec is as material as a lint error in source. A
repo that ships documentation (a `000-docs/` tree, a large markdown corpus, a SKILL.md corpus)
SHOULD gate doc quality at L2.

### 4.3 Layer 3 — Unit & Function

The core TDD cycle. **Walls 2–7 live here** (§ 5).

| Concern                                                       |
| ------------------------------------------------------------- |
| Unit test framework                                           |
| Architecture / fitness functions                              |
| Property-based testing (proves invariants)                    |
| Fuzzing (finds crashers — distinct from property-based)       |
| Mutation testing                                              |
| Coverage                                                      |
| CRAP / complexity gate                                        |
| Memory safety                                                 |
| Flakiness gate (an explicit measurable threshold, not a note) |

Property-based testing and fuzzing are separate concerns: the former proves invariants, the
latter finds crashers; an adversarial repo needs both.

### 4.4 Layer 4 — Integration & Regression

Unit interactions with real external systems (DB, queue, storage) and cross-version stability.

| Concern                                                                     |
| --------------------------------------------------------------------------- |
| Integration fixtures (containerized dependencies)                           |
| API / service contract testing                                              |
| Consumer-driven contracts (bidirectional — distinct from plain API testing) |
| Migration testing (a broken prod migration is unrecoverable)                |
| Database integration                                                        |
| Fake services                                                               |
| Message-queue integration                                                   |
| Regression snapshot                                                         |
| IaC integration tests                                                       |
| Kubernetes manifest tests                                                   |
| Doc-framework build (gates that docs _render_, not just lint)               |

Migration testing and contract testing are separated out from generic "integration": a broken
migration in prod is unrecoverable, and contract testing is a distinct bidirectional discipline
with its own artifacts.

### 4.5 Layer 5 — System Quality

Non-functional requirements: performance, security, accessibility, compatibility, resilience.

| Concern                                                                         |
| ------------------------------------------------------------------------------- |
| Performance / load                                                              |
| Security — SAST                                                                 |
| Security — DAST                                                                 |
| Accessibility                                                                   |
| Browser compatibility                                                           |
| Mobile compatibility                                                            |
| Chaos engineering (a service can survive load and still fail under a partition) |

### 4.6 Layer 6 — E2E & BDD / Gherkin

User-facing, through the full stack.

| Concern                                                                                       |
| --------------------------------------------------------------------------------------------- |
| End-to-end web                                                                                |
| End-to-end API                                                                                |
| Smoke / critical-path                                                                         |
| Visual regression (diffs rendered pixels — distinct from L4 snapshot, which diffs data shape) |
| BDD runners (the glue for Wall 1)                                                             |

### 4.7 Layer 7 — Acceptance & Business Validation

Does the delivered thing solve the stated problem?

| Concern                                                            |
| ------------------------------------------------------------------ |
| UAT (stakeholder-run)                                              |
| Automated acceptance (ties `.feature` files to real user journeys) |
| Business-rules validation                                          |

### 4.8 Orthogonality — this taxonomy vs the behavioral-eval tiers

This 7-layer _testing_ taxonomy classifies **a repository's testing system**. It is distinct
from the **3-tier validation bridge** (static grading / static production gate / behavioral
eval) specified in [`../../tier-bridge/v0.1.0-draft/SPEC.md`](../../tier-bridge/v0.1.0-draft/SPEC.md),
and distinct from the behavioral harness's own internal eval layers (trigger / functional /
regression / baseline / model-variance / rollout-safety / cost), which classify **one artifact's
runtime behavior**. A conformant tool MUST NOT conflate "the repo covers taxonomy layer N" with
"the artifact passed behavioral-eval layer N" — they measure different things on different
subjects.

## 5. Walls inside layers

The walls are _invariants_ enforced at specific layers, not a parallel structure:

| Wall                          | Layer                 | Invariant                                                 |
| ----------------------------- | --------------------- | --------------------------------------------------------- |
| Wall 1 — Acceptance (Gherkin) | L7 (spec) + L6 (glue) | Hash-pinned `.feature`; lint passes; BDD runner returns 0 |
| Wall 2 — Unit tests           | L3                    | 0 failing, 0 unauthorized skips                           |
| Wall 3 — Coverage floor       | L3                    | Line/branch ≥ the repo's `TESTING.md` floor               |
| Wall 4 — Mutation kill-rate   | L3                    | ≥ the repo's floor (or per-module floor)                  |
| Wall 5 — CRAP on prod code    | L3                    | No method over the prod ceiling; avg ≤ the prod avg       |
| Wall 6 — CRAP on test code    | L3                    | No test method over the test ceiling                      |
| Wall 7 — Architecture rules   | L3 (fitness fns)      | 0 violations; rule configs hash-pinned                    |

### R3 — Walls live inside layers, not alongside them

A conformant testing system MUST treat each wall as an invariant of its host layer, not as a
separate structure. Wall 1 is an L7/L6 invariant; Walls 2–7 are L3 invariants. The taxonomy
adds the other layers (L1, L2, L4, L5, and the E2E-specific part of L6) that the walls do not
individually cover.

### R4 — Wall thresholds are repo policy, not taxonomy constants

The _existence_ of a wall is normative here; its _threshold_ (coverage %, kill-rate %, CRAP
ceiling) is declared per-repo in `tests/TESTING.md`. A repo MUST declare its thresholds; this
taxonomy MUST NOT be read as fixing them.

## 6. Conformance obligations

### R5 — Classification before assertion

A repo claiming taxonomy conformance MUST first classify itself (its applicable layers per its
type) and record that classification (canonically in `tests/TESTING.md`). A blanket "we test"
claim without a layer classification is non-conformant.

### R6 — Per-layer presence / configuration / enforcement

For each _applicable_ layer, a conformant repo MUST demonstrate, in this order: (a) **presence**
(the layer's concern is covered by some tool), (b) **configuration** (the tool is configured,
not stub-installed), and (c) **enforcement** (the gate actually blocks — a CI check, a hook,
a required status). A layer that is present but not enforced is a partial gap, not conformance.

### R7 — Gaps are named, not hidden

A repo with a missing applicable layer is non-conformant _for that layer_ and MUST name the gap
(the diagnostic skill's `TEST_AUDIT.md` is the canonical place). Naming the gap is itself part
of conformance discipline — an unstated gap is the failure mode this taxonomy exists to prevent.

## 7. RFC

Layer-boundary challenges, proposed new concerns within a layer, and counter-proposals to the
fixed-seven structure welcome via GitHub issues on
[`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab). A
test/gate that fits no layer is the strongest signal for an RFC.

## 8. Anchors

- **The 7-layer testing taxonomy is an internal Intent Solutions pattern (free to
  cross-reference):** canonical glossary, "External-pattern non-borrow".
- **The diagnostic + installer skills that consume this taxonomy:** `audit-tests` (maps a repo
  against these layers, writes `TEST_AUDIT.md`) and `implement-tests` (installs missing
  layers). This spec is their shared referent.
- **The orthogonal 3-tier validation bridge:**
  [`../../tier-bridge/v0.1.0-draft/SPEC.md`](../../tier-bridge/v0.1.0-draft/SPEC.md) (§ 4.8).
- **Repo roles + ecosystem taxonomy:**
  [Blueprint A](../../../000-docs/011-AT-ARCH-ecosystem-master-blueprint.md).

## License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
