---
title: Blueprint C — Repo Blueprint Template
date: 2026-05-14
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
binding_authority: ISEDC Session 4 (DR-010, 2026-05-13)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E04
bead: bd_000-projects-9es
filing_standard: Document Filing Standard v4.3
related_drs:
  - 004-AT-DECR (S1 — provider PASS/FAIL gates, partner-consent, predicate URI namespace)
  - 010-AT-DECR (S4 — three-class governance, hybrid language, provider gates reaffirmed)
related_docs:
  - 014-DR-GLOS-canonical-glossary.md (terminology source of truth)
applies_to:
  - intent-eval-core (iec-E10)
  - intent-eval-lab (iel-E05 — self-application)
  - audit-harness (iah-E01)
  - j-rig-skill-binary-eval (iaj-E01)
  - intent-rollout-gate (iar-E01)
---

# Blueprint C — Repo Blueprint Template

> **This document is a TEMPLATE, not a normative platform doc.** Blueprint A (`011-AT-ARCH-ecosystem-master-blueprint.md`) is the constitution. Blueprint B (`012-AT-ARCH-platform-runtime-blueprint.md`) is the kernel specification. Blueprint C — **this document** — is the reusable scaffold that every repo in the ecosystem applies to produce its **own per-repo blueprint** (`NNN-AT-ARCH-repo-blueprint.md` in that repo's `000-docs/`).
>
> The per-repo blueprint that results from applying this template is the single source of truth for *that* repo's identity, architecture, boundaries, and DoD. It inherits Blueprint A's principles and anti-goals, declares which Blueprint B canonical entities it touches, and links — never redefines — terminology from the canonical glossary (`014-DR-GLOS-canonical-glossary.md`).

## How this document is organized

This document has two halves:

1. **The template-itself** (§§ 1–13). Copy these section headings and placeholder text into your repo's `000-docs/NNN-AT-ARCH-repo-blueprint.md` and replace the `{PLACEHOLDER}` and `<placeholder>` tokens.
2. **Authoring guidance + minimal example + validation checklist** (§ Author's Guide, § Minimal Example, § Validation Checklist). Do **not** copy this half into your per-repo blueprint — it is meta-content for blueprint authors.

Author's Guide callouts inside the template-itself are formatted as block quotes prefixed with **`> Author's Guide:`**. **Delete every such callout** before committing your per-repo blueprint.

---

# PART ONE — The Template (copy this into your repo)

> Author's Guide: Replace `{REPO_NAME}` everywhere it appears with your repo's canonical GitHub name (the name `gh repo view <name>` resolves to). Replace every `<placeholder>` token with repo-specific content. The frontmatter below is the per-repo blueprint's frontmatter, NOT this template's frontmatter — copy it and customize.

```yaml
---
title: Repo Blueprint — {REPO_NAME}
date: <YYYY-MM-DD>
authors:
  - <author-name> (Intent Solutions)
status: NORMATIVE
binding_authority: <epic-id, e.g., iah-E01>
inherits_from:
  - intent-eval-lab/000-docs/011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A)
  - intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B)
  - intent-eval-lab/000-docs/013-AT-SPEC-repo-blueprint-template.md (Blueprint C — this template)
related_drs:
  - <list applicable Decision Records, e.g., 004-AT-DECR (S1Q5 — provider PASS/FAIL gates)>
related_glossary:
  - intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md
filing_standard: Document Filing Standard v4.3
---
```

## § 1 — Repo identity

| Field | Value |
|---|---|
| **Repo name** | `{REPO_NAME}` (matches `gh repo view` and local working-dir name) |
| **Type** | one of: `kernel` / `runtime` / `methodology` / `action-shell` / `spec` |
| **Owner** | per `CODEOWNERS` — `<github-handle-or-team>` |
| **Maturity** | one of: `pre-release` / `v0.x experimental` / `v1.x production` / `archived` |
| **Ecosystem role** | one sentence describing this repo's job in the ecosystem |
| **Bead prefix** | `<prefix>` (e.g., `iec-`, `iah-`, `iaj-`, `iar-`, `iel-`) — must match Blueprint A § 2.1 taxonomy |
| **Plane module** | full module path inside the LAB/JRIG/etc. Plane project |

### 1.1 Dependencies (peer repos consumed)

> Author's Guide: List every other ecosystem repo this repo consumes at runtime, build time, or test time. Cite each by repo name AND its own per-repo blueprint sequence number. Strict SemVer per Blueprint A § 4.2 — pin to a known-good range.

| Peer repo | Consumed at | Pinned range | Cited blueprint |
|---|---|---|---|
| `<peer-repo>` | runtime / build / test | `>=X.Y.Z, <NEXT_MAJOR>` | `<peer-repo>/000-docs/NNN-AT-ARCH-repo-blueprint.md` |

### 1.2 Non-goals (inherited + repo-specific)

This repo inherits every anti-goal locked in Blueprint A § 3 (NOT a generalized autonomous agent platform; NOT a workflow automation competitor; NOT a distributed compute platform; NOT a no-code builder; NOT infinite orchestration; NOT trying to be the union of every adjacent category; AISE 5-domain stack is internal scope-map, NOT separate-brand surface). In addition, this repo specifically does NOT:

- `<repo-specific anti-goal #1>`
- `<repo-specific anti-goal #2>`

Scope-creep into any item above triggers ISEDC re-convene per Blueprint A § 2.3 governance routing.

---

## § 2 — Problem statement

> Author's Guide: One to three paragraphs answering "what problem does this repo solve that no other ecosystem repo solves." Cite Blueprint A § 1.1 mission as upstream context. If this repo's problem could be solved by an existing ecosystem repo, it should NOT exist as a separate repo — surface that observation through Class 2 governance per Blueprint A § 2.3.

`<Author the problem statement here. State the user pain (engineer can't ship a Skill update without manual evidence collection; auditor can't reconstruct a verdict without bespoke tooling; etc.), state how this repo addresses it, and state the boundary at which this repo hands off to a peer repo.>`

---

## § 3 — Scope boundaries

### 3.1 In scope

What this repo ships, end-to-end:

- `<in-scope item #1>`
- `<in-scope item #2>`

### 3.2 Out of scope (permanent, no FUTURE flag)

What this repo refuses to do, full stop:

- `<out-of-scope item #1 — and why>`
- `<out-of-scope item #2 — and why>`

> Author's Guide: "Out of scope" means "this will not be in this repo, ever." If the answer is "not yet, but maybe later," it belongs in § 3.3 (Deferred), not here.

### 3.3 Deferred (FUTURE flag required)

What this repo defers to a later milestone. Each deferred item MUST forward-reference a `FUTURE.md` entry (in `intent-eval-lab/000-docs/FUTURE.md` for ecosystem-wide deferrals; in this repo's own `FUTURE.md` for repo-local deferrals).

| Deferred item | Earliest milestone | FUTURE.md reference |
|---|---|---|
| `<item>` | `<milestone-id>` | `<path-to-FUTURE.md>#<anchor>` |

### 3.4 Anti-goals (binding-scope-control)

The anti-goals here are binding in the same sense as Blueprint A § 3 — scope-creep into any one triggers ISEDC re-convene. Cite every Blueprint A anti-goal that applies, plus any repo-specific anti-goal not already covered.

- **Inherited from Blueprint A § 3.N**: `<short restatement of the relevant Blueprint A anti-goal>` (cite the specific subsection)
- **Repo-specific**: `<repo-specific anti-goal — explain the failure mode prevented, per the pattern in Blueprint A § 3>`

---

## § 4 — Architecture

### 4.1 Module layout

Top-level directory structure and package boundaries:

```
{REPO_NAME}/
├── <top-level-dir>/   — <what lives here>
├── <top-level-dir>/   — <what lives here>
├── ...
└── <top-level-dir>/   — <what lives here>
```

### 4.2 Data flow

> Author's Guide: For a CLI/library repo, document the request → response path or the pipeline stages. For a service repo, document the orchestration model. Include a Mermaid `graph LR` or `sequenceDiagram` when the flow is non-trivial. Inline ASCII is acceptable for simple linear flows.

`<Describe the data flow.>`

### 4.3 Runtime boundaries

| Concern | Specification |
|---|---|
| **Process model** | single-process CLI / long-running daemon / GitHub Action runtime / worker-pool / other |
| **IPC** | stdin-stdout JSON / HTTP / gRPC / file-based / message queue / N/A |
| **External services consumed** | `<list — PostgreSQL? Redis? object storage? Rekor? provider APIs?>` |
| **Process isolation guarantees** | `<what runs in the same memory space; what is sandboxed; what crosses the credential-broker boundary per Blueprint B § 4.1>` |

### 4.4 Storage needs

> Author's Guide: Repos that consume a Blueprint B § 2 canonical entity at rest need to declare their storage commitments here. Methodology and spec repos typically have none. Kernel repos define the schemas but do not themselves persist data.

| Storage class | Backing store | Retention | Reference |
|---|---|---|---|
| `<hot index>` | PostgreSQL / Redis / object storage / other | `<window>` | `Blueprint B § 4.2 cost governance` |
| `<cold archive>` | `<backing store>` | `<window>` | `<reference>` |

### 4.5 External dependencies (cite by version)

Strict SemVer per Blueprint A § 4.2. Pin to a known-good range; MAJOR bumps require a Class-2 pair Decision Record before they land.

| Dependency | Range | Purpose | Notes |
|---|---|---|---|
| `<dep>@<range>` | `>=X.Y.Z, <NEXT_MAJOR>` | `<what it does>` | `<security / license / replaceability notes>` |

### 4.6 Failure boundaries

What fails together; what is isolated; what bounded retries cover. Reference Blueprint B § 2.13 FailureTaxonomy if this repo emits failure categories.

- **Crash boundary**: `<what process-level failures look like and how they recover>`
- **Retry boundary**: `<which operations are bounded-retryable; the policy; the backoff>`
- **Isolation guarantees**: `<what other ecosystem components are protected from a failure here>`
- **Emitted FailureTaxonomy categories**: `<list — or N/A if this repo does not emit FailureTaxonomy rows>`

---

## § 5 — Canonical entities used

> Author's Guide: Blueprint B § 2 enumerates 13 canonical entities (EvalSpec, EvalRun, MatcherMap, EvidenceBundle, JudgeDecision, RuntimeReceipt, RegressionPack, RolloutGate, SkillSnapshot, SessionTrace, ToolInvocation, CostRecord, FailureTaxonomy). For every entity this repo touches, declare whether you **consume**, **produce**, or **both**; cite which Blueprint B § 2.N attributes you implement (e.g., "produces with required-fields and content-hash; defers retention to consumer"); link to the canonical glossary entry. **Do NOT redefine canonical entities locally** — link to `014-DR-GLOS-canonical-glossary.md` § 2.N and let the glossary be the source of truth.

| Entity | Direction | Blueprint B attributes implemented | Glossary ref |
|---|---|---|---|
| `<EntityName>` | consumes / produces / both | `<required fields + UUID + mutability + retention + replayability + provenance + lifecycle + storage + audit — list only the attributes this repo implements>` | `014-DR-GLOS-canonical-glossary.md` § 2.N |

**Entities NOT touched by this repo:** `<list the canonical entities this repo does not interact with — for completeness so a reviewer can spot a gap>`.

---

## § 6 — Interfaces

> Author's Guide: Omit sub-sections that do not apply. A pure-library kernel has no CLI. A methodology repo has no APIs. A GitHub Action has no HTTP server. Be precise; ambiguity in the public-API surface is the source of the most expensive class of bug (silent breakage across SemVer minor bumps).

### 6.1 CLI

Command surface, flag taxonomy, exit codes.

```
{REPO_NAME} <subcommand> [flags] [args]
```

| Subcommand | Purpose | Exit codes |
|---|---|---|
| `<subcommand>` | `<purpose>` | `0` success / `1` user error / `2` blocking violation / `N` repo-specific |

### 6.2 HTTP / gRPC APIs

| Endpoint | Method | Purpose | Authn |
|---|---|---|---|
| `<path>` | `GET` / `POST` / `gRPC method` | `<purpose>` | `<authn scheme — or N/A for unauthenticated>` |

Or link to an OpenAPI / `.proto` file: `<path-to-spec>`.

### 6.3 Config files

| File | Schema | Canonical example |
|---|---|---|
| `<path/to/config>` | `<JSON Schema / TypeScript type / Pydantic model — link>` | `<path-to-example>` |

### 6.4 Output formats

> Author's Guide: If this repo emits Evidence Bundle rows, cite Blueprint B § 7 for the canonical `gate-result/v1` shape (or the relevant predicate URI). Do NOT redefine the predicate body locally. Plain-text fallback formats live here too.

| Output | Shape | Reference |
|---|---|---|
| Evidence Bundle row | in-toto Statement v1 over DSSE; predicate body per Blueprint B § 7.4 | `Blueprint B § 7` |
| JSON envelope | `<schema reference>` | `<path>` |
| Plain-text fallback | `<one-paragraph format description>` | n/a |

### 6.5 Event schemas

OpenTelemetry attribute schema emitted by this repo. Forward-reference `iel-E12` (OTel RFC) until that RFC's `agent.rollout.gate.*` and `agent.evidence_bundle.*` taxonomies are locked.

| Event | Attributes | OTel taxonomy |
|---|---|---|
| `<event.name>` | `<attribute list>` | `agent.rollout.gate.<subkey>` (per iel-E12, forward-ref) |

### 6.6 Public-API stability promise

What this repo guarantees across SemVer minor bumps:

- `<stable surface element #1>` — `<promise>`
- `<stable surface element #2>` — `<promise>`

Breaking changes to anything in the stability promise require MAJOR bump (Blueprint A § 4.2 versioning standard) AND a Class-2 pair Decision Record (Blueprint A § 2.3) before merge.

---

## § 7 — Testing strategy

This section applies the Intent Solutions Testing SOP. Layer applicability is per-repo-type per `~/.claude/skills/audit-tests/references/layer-applicability.md` — not every repo needs all 7 layers, and the per-repo blueprint must declare which layers apply and why.

> Author's Guide: For every layer that applies, declare the framework, the coverage / kill-rate target, and the CI gate that enforces it. Layers that do NOT apply to this repo type get a one-line "N/A — `<reason>`" entry. **Never** reference `~/.claude/` paths in this section's CI gate examples — enforcement travels with the code per Blueprint A § 4.2 CI requirements.

### 7.1 L0 — git hooks (pre-commit)

- **In-scope checks**: `<list — escape-scan, partner-name grep, license-header presence, hash-pin verification, etc.>`
- **Enforcement**: `pnpm exec audit-harness <subcommand>` (Node) or `scripts/audit-harness <subcommand>` (vendored install). NEVER `~/.claude/` paths.

### 7.2 L1–L2 — static analysis (lint + typecheck + escape-scan)

- **Lint**: `<framework — ESLint flat config / Ruff / clippy / shellcheck / yamllint / other>`
- **Typecheck**: `<framework — tsc --noEmit / mypy / cargo check / N/A>`
- **Escape-scan**: `pnpm exec audit-harness escape-scan --staged` (Node) or `scripts/audit-harness escape-scan --staged` (vendored)

### 7.3 L3 — unit tests

| Concern | Target |
|---|---|
| **Framework** | `<vitest / pytest / cargo test / bats / other>` |
| **Coverage floor** | `<NN%>` |
| **Mutation kill rate** | `<NN%>` (or N/A if mutation testing is layer-inapplicable) |
| **CI gate** | `<command>` |

### 7.4 L4 — integration tests

What is exercised end-to-end **inside the repo** (no external services):

- `<integration scenario #1>`
- `<integration scenario #2>`

### 7.5 L5 — system tests

What is exercised against **external services** (Rekor, sigstore staging, provider APIs, the production database, etc.):

- `<system scenario #1 — and which external service it touches>`
- **Provider PASS/FAIL gates**: see § 8.3 below — credential-redaction + env-var spillover tests are NON-NEGOTIABLE for any repo touching LLM providers.

### 7.6 L6 — acceptance tests

| Concern | Specification |
|---|---|
| **Gherkin scope** | `<which user-facing flows are codified as Gherkin features>` |
| **Lint** | `pnpm exec audit-harness gherkin-lint` |
| **RTM** | `<path-to-requirements-traceability-matrix>` |
| **Personas** | `<path-to-personas.md>` |
| **Journeys** | `<path-to-journeys.md>` |

### 7.7 L7 — chaos / property / fuzz

> Author's Guide: Many repos legitimately have no L7. Declare applicability explicitly. If a property-based testing framework is applicable but not yet adopted, file the gap as a bead in this repo's prefix and link the bead ID here.

- **Applicability**: applicable / N/A — `<reason>`
- **Framework**: `<fast-check / hypothesis / proptest / other>`
- **Scope**: `<which invariants are property-checked>`

### 7.8 CI gates

The exact commands a PR runs on merge:

```
<command #1>
<command #2>
...
```

**Hash-pin discipline**: after any policy edit in `tests/TESTING.md`, re-run `pnpm exec audit-harness init` (Node) or `scripts/audit-harness init` (vendored) and commit the updated `.harness-hash` in the same commit. Pre-commit refuses unsigned policy edits by design.

### 7.9 Fixtures

| Concern | Specification |
|---|---|
| **Location** | `<tests/fixtures/ — or repo-specific path>` |
| **Naming convention** | `<NNN-<kind>-<slug>.<ext>>` |
| **Vendor-generic discipline** | All fixtures are scrubbed per DR-004 S1Q2 + DR-010 § 10 reaffirmation. Partner-name grep guard runs on the fixtures directory in CI. |

### 7.10 Golden files (if applicable)

`<framework — snapshot discipline; how regenerations are reviewed; refusal of mass-regenerate via CI>`

---

## § 8 — Security / isolation

### 8.1 Secrets management

Secrets are handled via the **broker pattern** per Blueprint B § 4.1: credentials never cross the subprocess boundary. The broker is the only component that sees plaintext; downstream code receives a redacted handle.

| Secret class | Storage | Broker | Repo-specific |
|---|---|---|---|
| `<class — e.g., provider-api-key>` | `<SOPS-encrypted file / OS keychain / GitHub Actions secret>` | `<broker mechanism>` | `<any repo-specific handling>` |

**SOPS + age standard**: when this repo persists secrets at rest, it uses the SOPS + age pattern per the parent `~/.claude/CLAUDE.md` § "SOPS + age secrets standard". `.env.sops` committed; `.env` plaintext is git-ignored; CI receives the age key via `SOPS_AGE_KEY` GitHub Actions secret. NEVER decrypt to disk.

### 8.2 Sandbox model

> Author's Guide: Repos that execute user-supplied artifacts (skills, prompts, MCP servers, evaluation targets) MUST declare their sandbox model. Repos that only emit signed evidence with no user-code execution may declare "no sandbox required — no user-code execution path."

| Concern | Default per Blueprint B § 4.1 | This repo's override (if any) |
|---|---|---|
| **Filesystem** | per-Run scratch directory; no host-FS access outside scratch | `<override or "default">` |
| **Network egress** | declared egress allowlist per EvalSpec | `<override or "default">` |
| **Wall-clock ceiling** | 30 minutes default; 4 hours hard ceiling | `<override or "default">` |
| **Memory ceiling** | 2 GiB default; 8 GiB hard ceiling | `<override or "default">` |
| **Credential boundary** | broker-pattern; plaintext never crosses subprocess boundary | `<override or "default">` |

### 8.3 Provider PASS/FAIL gates (RESTATE if this repo touches LLM providers)

> Author's Guide: If this repo invokes ANY LLM provider (production or test), restate the gates verbatim below. These gates are NON-NEGOTIABLE per DR-004 S1Q5 (declined reopening at Session 4 per DR-010 § 10). Removing or weakening this section in a per-repo blueprint is itself a Class-1 ISEDC trigger.

The platform's two provider gates are **non-negotiable** and both must PASS before any provider abstraction lands or is bumped in this repo:

1. **Credential-redaction test** — every code path that surfaces an error, log entry, or metric containing a provider response MUST redact the credential. Test asserts the literal credential string is absent from every observable surface.
2. **Env-var spillover test** — provider credentials set in this repo's process environment MUST NOT spill into any spawned subprocess. Test spawns a subprocess and asserts the provider env vars are absent from its environment.

Both tests run in CI on every PR touching provider code. A FAIL on either is a HARD STOP — the PR cannot merge.

Provider adapter library choice (LiteLLM / Vercel AI SDK / custom) is decided per-repo through in-prototype measurement against these gates plus CTO measurement protocol committed BEFORE prototyping plus CMO ≥3 named providers in launch leaderboard plus GC license audit (DR-004 S1Q5 + DR-010 reaffirmation).

### 8.4 Audit logging

| Concern | Specification |
|---|---|
| **What is logged** | `<authn / authz events / verdict emissions / signing events / verification failures / configuration changes>` |
| **Append-only** | yes — log records are never amended in place per Blueprint A § 1.2 principle 3 |
| **Signing** | Evidence Bundle rows are signed per Blueprint B § 7.5; non-Evidence audit log signing per `<repo-specific>` |
| **Retention** | `<window — alignment with Blueprint B § 4.2 hot/warm/cold/archive classes>` |

### 8.5 Threat model

> Author's Guide: One paragraph identifying what an adversary can / cannot do via this repo's surface. Be honest: "an adversary with write access to the npm registry can publish a poisoned version of <peer-dep>; we defend with sigstore + license audit + pinned-range strict-SemVer" is more useful than "we use industry-standard security practices."

`<Author the threat model paragraph here.>`

---

## § 9 — Observability

### 9.1 OpenTelemetry events

> Author's Guide: List the events this repo emits. Forward-reference `iel-E12` (the OTel RFC) until the `agent.rollout.gate.*` and `agent.evidence_bundle.*` taxonomies are locked. Events that emit from this repo BEFORE the RFC is filed use the same names but carry a `taxonomy_status: draft` attribute so they are distinguishable from post-lock emissions.

| Event | Trigger | Attributes |
|---|---|---|
| `agent.rollout.gate.<event>` | `<when this event fires>` | `<attribute list>` |
| `agent.evidence_bundle.<event>` | `<when this event fires>` | `<attribute list>` |

### 9.2 Trace propagation

| Concern | Specification |
|---|---|
| **Incoming trace ID** | how an inbound trace-id is honored (HTTP `traceparent` header / CLI flag / N/A) |
| **Span hierarchy** | how this repo's spans nest under inbound spans |
| **Span attributes** | required attributes per span per the iel-E12 RFC |

### 9.3 Lineage capture

How this repo's outputs map to Blueprint B § 2 canonical entities for lineage purposes:

- **SessionTrace**: `<which session-trace fields this repo populates>`
- **RuntimeReceipt**: `<which receipt fields this repo populates>`
- **ToolInvocation rows**: `<which ToolInvocation rows this repo emits, if any>`

### 9.4 Log levels

Structured logs, log-level taxonomy:

| Level | When |
|---|---|
| `ERROR` | unrecoverable failure — operator action required |
| `WARN` | degraded state — operation continues but signal is reduced |
| `INFO` | high-level lifecycle events — start, end, terminal state transitions |
| `DEBUG` | per-step diagnostics — disabled by default in production |
| `TRACE` | per-operation diagnostics — enabled only in test environments |

### 9.5 Failure taxonomy

Which Blueprint B § 2.13 `FailureTaxonomy` categories this repo can emit:

- `<category #1>` — `<when emitted>`
- `<category #2>` — `<when emitted>`

Or "N/A — this repo does not emit `FailureTaxonomy` rows" if applicable.

---

## § 10 — Cost governance

> Author's Guide: This section applies when the repo touches paid surfaces — provider API calls, paid object-storage tiers, paid Rekor signing, etc. Pure-spec and pure-library repos may declare "N/A — no paid surface touched."

### 10.1 Token ceilings

| Concern | Default | Per-EvalSpec override |
|---|---|---|
| **Per-invocation token ceiling** | `<NN tokens>` | permitted via EvalSpec `runtime_limits.token_ceiling` |
| **Per-run wall-clock ceiling** | `<NN minutes>` | permitted via EvalSpec `runtime_limits.wall_clock_ceiling` |
| **Concurrency** | `<NN concurrent invocations>` | per-deployment |

### 10.2 Cost attribution

Per Blueprint B § 2.12 `CostRecord`:

- **Consumed**: which `CostRecord` fields this repo reads
- **Produced**: which `CostRecord` rows this repo emits (one per invocation / one per Run / N/A)

### 10.3 Retention lifecycle

| Class | Window | Backing store |
|---|---|---|
| Hot | `<NN days>` | `<PostgreSQL primary>` |
| Warm | `<NN days>` | `<compressed PostgreSQL partition>` |
| Cold | `<NN days>` | `<object storage standard tier>` |
| Archive | indefinite | `<object storage archive tier>` |

Aligns with Blueprint B § 4.2 cost-governance retention discipline; deviations require Class-2 pair Decision Record.

### 10.4 Cache strategy

| Cache class | Purpose | Hit/miss accounting |
|---|---|---|
| Prompt cache | `<reduce provider token cost>` | emitted to `CostRecord` as `cache_hits` / `cache_misses` |
| Semantic cache | `<reduce judge invocations>` | emitted to `CostRecord` as `semantic_cache_hits` |

### 10.5 Budget ceilings

| Scope | Daily | Monthly | Per-feature |
|---|---|---|---|
| `<provider api spend>` | `<$NN>` | `<$NN>` | `<$NN>` |

Exceeding any ceiling pauses execution and surfaces an alert. Ceilings are enforced at the runtime sandbox boundary per Blueprint B § 4.1, NOT at the policy layer alone.

---

## § 11 — Release strategy

### 11.1 Versioning

**Strict SemVer** per Blueprint A § 4.2. MAJOR for any breaking change to the public-API stability promise (§ 6.6). No "convenience minor" for things that look like additions but break consumers.

| Bump | When |
|---|---|
| MAJOR | breaking change to § 6.6 stability promise; canonical-contract change in `intent-eval-core`; predicate URI grammar change |
| MINOR | additive feature; new optional field; new event emission; deprecation notice (without removal) |
| PATCH | bug fix; documentation polish; internal refactor with no public-API change |

### 11.2 Changelog

`CHANGELOG.md` discipline per Keep a Changelog format. Sections: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Every PR that merges to main updates `CHANGELOG.md` under the `## [Unreleased]` section; the release commit promotes `[Unreleased]` to the new version + date.

### 11.3 Migration notes

| Concern | Location |
|---|---|
| **Migration guide location** | `<MIGRATING.md / docs/migrations/vX-to-vY.md>` |
| **Migration generator** | `<auto-generated / hand-authored>` |
| **Required for** | every MAJOR bump |

### 11.4 Compatibility guarantees

What downstream consumers can rely on across minor bumps:

- `<guarantee #1>`
- `<guarantee #2>`

Across MAJOR bumps: only the items explicitly preserved in the MAJOR release notes.

### 11.5 Evidence retention discipline

> Author's Guide: Applies to every release that emits Evidence Bundle rows.

Per Blueprint A § 4.2 + DR-010 § 7 Q5 CISO non-negotiable: production-Rekor signing for any predicate URI is gated on that predicate's SPEC.md normative section landing.

- **v0.x releases** anchor to sigstore staging (`rekor.sigstage.dev`) — EXPERIMENTAL mode
- **v0.2+ releases** anchor to production Rekor **per-predicate**, only once the predicate's SPEC.md normative section is merged on `intent-eval-lab` main

This repo's predicate-URI inventory and per-predicate cutover status:

| Predicate URI | Status | SPEC.md ref | Signing mode |
|---|---|---|---|
| `evals.intentsolutions.io/<predicate>/v<N>` | conditional / approved / deferred | `<path>` | `sigstore_staging` / `rekor_production` |

### 11.6 License audit

Every release runs `pip-licenses` (Python) / `npm-license-checker` (Node) / language-equivalent on the resolved dependency tree per DR-010 § 7 Q2 GC non-negotiable. GPL / AGPL dependencies are blocked at CI absent explicit GC waiver. A `LICENSES.md` file in this repo's root enumerates every direct dependency with license name and upstream license-file link.

---

## § 12 — Beads / work breakdown

| Concern | Value |
|---|---|
| **Bead prefix** | `<prefix>` (per Blueprint A § 2.1) |
| **bd workspace** | umbrella `~/000-projects/.beads/` (default) or per-repo `<path>` |
| **Epic naming** | `<prefix>-E<NN>` (e.g., `iah-E01`) |
| **Plane project** | `<LAB / JRIG / IEC / IAH / IAR>` |
| **Plane module** | `<module path inside the project>` |
| **GH ↔ Plane mirror** | via `bd-sync` per global CLAUDE.md three-layer discipline |

### 12.1 Cross-repo bead dependencies

Other ecosystem repos' beads this repo's work depends on (ALL bd-sync-mirrored):

- `<peer-repo-bead-prefix-XX>` — `<what this repo is waiting on>`

### 12.2 In-repo epic inventory

| Epic | Status | Purpose |
|---|---|---|
| `<prefix>-E01` | open / in-progress / closed | `<one-line purpose>` |
| `<prefix>-E02` | open / in-progress / closed | `<one-line purpose>` |

---

## § 13 — Definition of Done

This repo is "complete enough to release" when **every** check below passes:

- [ ] All tests pass at the L0–L7 policy floors declared in § 7 (coverage, mutation kill rate, integration scenarios, system tests).
- [ ] Provider PASS/FAIL gates pass (§ 8.3) — credential-redaction + env-var spillover both green — if this repo touches LLM providers.
- [ ] All canonical entities consumed (§ 5) have their schema versions pinned to a known-good range.
- [ ] License audit clean per § 11.6 (no GPL / AGPL absent explicit GC waiver).
- [ ] Partner-name vendor-generic grep returns 0 against all public-facing directories — use the current partner-name pattern maintained in the ecosystem CLAUDE.md (`~/000-projects/CLAUDE.md` and `~/.claude/CLAUDE.md`) so this blueprint itself stays scrubbable.
- [ ] Evidence Bundle round-trip verified when applicable — emit → DSSE wrap → cosign sign → cosign verify-attestation → consume succeeds end-to-end.
- [ ] `CHANGELOG.md` entry written under `## [Unreleased]` (or promoted to the new version for the release commit).
- [ ] This per-repo blueprint matches reality — `/validate-consistency` clean against this repo's `000-docs/`, `README.md`, and `CHANGELOG.md`.
- [ ] Acting head of board sign-off (or designated approver per `CODEOWNERS`).

---

# PART TWO — Author's Guide (do NOT copy this part into your per-repo blueprint)

## How to apply this template

1. **Choose your sequence number.** Open your repo's `000-docs/000-INDEX.md` and pick the next available `NNN` in the `AT-ARCH` category. The per-repo blueprint filename is `NNN-AT-ARCH-repo-blueprint.md`.

2. **Copy PART ONE (§§ 1–13) into the new file.** Do NOT copy the document-header `> This document is a TEMPLATE` callout, the "How this document is organized" section, or PART TWO. Those are template meta-content.

3. **Replace `{REPO_NAME}` everywhere** with the canonical GitHub repo name (the name `gh repo view <name>` resolves to). It must match the local working-dir name.

4. **Walk every section.** For each section:
   - Replace every `<placeholder>` token with repo-specific content.
   - **Delete every Author's Guide callout** (block quotes prefixed with `> Author's Guide:`).
   - Tables: delete rows that do not apply; do NOT delete the table header.
   - Sections that are entirely N/A for this repo (e.g., § 6.1 CLI for a pure-library repo): replace the section body with a one-line "N/A — `<reason>`" and keep the section heading.

5. **Update `000-docs/000-INDEX.md`** to add a row for the new per-repo blueprint. Pick the correct AT-ARCH sub-type code if your INDEX uses sub-types; otherwise use `AT-ARCH` as both category and sub-type per Doc Filing Standard v4.3.

6. **Run the Validation Checklist** below before raising a PR. Every check must pass.

7. **Raise the PR.** Title: `docs(<epic-id>): land per-repo blueprint`. Example: `docs(iah-E01): land per-repo blueprint`. Body cites Blueprint A + B + C inheritance and lists the canonical entities this repo touches.

8. **Re-apply when the repo's identity shifts.** A per-repo blueprint is not a one-shot document. When this repo's scope, dependencies, or DoD shifts materially, re-walk the template and update the per-repo blueprint in the same commit as the underlying change. Drift between the per-repo blueprint and reality is detectable through `/validate-consistency` and treated as a HIGH-severity finding.

## Minimal Example (INFORMATIVE only)

> The example below is for a **fictional** repo named `intent-example-shim`. It is **not normative** for any real repo in the ecosystem. Its purpose is to demonstrate the shape of a completed per-repo blueprint at 10x compression — a real per-repo blueprint will be 5-10x longer in detail.

```markdown
---
title: Repo Blueprint — intent-example-shim
date: 2026-05-14
authors:
  - Example Author (Intent Solutions)
status: NORMATIVE
binding_authority: iex-E01
inherits_from:
  - intent-eval-lab/000-docs/011-AT-ARCH-ecosystem-master-blueprint.md
  - intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md
  - intent-eval-lab/000-docs/013-AT-SPEC-repo-blueprint-template.md
related_drs:
  - 004-AT-DECR (S1Q5 — provider PASS/FAIL, N/A here, no provider surface)
related_glossary:
  - intent-eval-lab/000-docs/014-DR-GLOS-canonical-glossary.md
filing_standard: Document Filing Standard v4.3
---

# Repo Blueprint — intent-example-shim

## § 1 — Repo identity

| Field | Value |
|---|---|
| Repo name | `intent-example-shim` |
| Type | `spec` |
| Owner | `@example-author` |
| Maturity | `pre-release` |
| Ecosystem role | Reference shim demonstrating the per-repo blueprint shape. |
| Bead prefix | `iex-` |
| Plane module | LAB → Reference Shims |

### 1.2 Non-goals
Inherits Blueprint A § 3 anti-goals in full. Repo-specific: this shim does not
ship runtime code, does not consume provider APIs, does not emit Evidence Bundle
rows; it is documentation-only.

## § 2 — Problem statement

Future blueprint authors need a worked, end-to-end example of a per-repo
blueprint that fits on a single screen, so they can calibrate the level of
specificity expected at each section. No other ecosystem repo carries this role.

## § 3 — Scope boundaries
- In scope: this single per-repo blueprint and its sibling `README.md`.
- Out of scope: any runtime, any CI, any tests beyond markdown-lint.
- Deferred: nothing.
- Anti-goals: NOT a real repo; the example must NEVER be cited as a normative
  source in another blueprint's `inherits_from` field.

## § 4 — Architecture

Module layout: `000-docs/` and `README.md` only. No data flow. No runtime
boundaries beyond "git clone, read markdown."

## § 5 — Canonical entities used

| Entity | Direction | Attributes implemented | Glossary ref |
|---|---|---|---|
| (none) | N/A — methodology-only repo with no entity I/O | N/A | `014-DR-GLOS-canonical-glossary.md` |

## § 6 — Interfaces

N/A — repo ships markdown only. No CLI, no API, no config, no events, no output formats.

Public-API stability promise: the per-repo blueprint URL is stable; the heading
hierarchy is stable across MINOR bumps.

## § 7 — Testing strategy

- L0: markdownlint pre-commit.
- L1: `pnpm exec audit-harness escape-scan --staged` (vendored install).
- L3–L7: N/A — no executable code.

## § 8 — Security / isolation

N/A — no secrets, no sandbox, no provider surface. Threat model: an adversary
with repo write access could publish misleading example content; defended by
CODEOWNERS review.

## § 9 — Observability

N/A — no runtime, no emitted events.

## § 10 — Cost governance

N/A — no paid surfaces.

## § 11 — Release strategy

Strict SemVer; CHANGELOG.md present; no migrations; license audit clean
(MIT, zero dependencies).

## § 12 — Beads / work breakdown

Bead prefix `iex-`; umbrella workspace; epic `iex-E01` (blueprint-itself).

## § 13 — Definition of Done

- [x] No partner-name leakage.
- [x] `/validate-consistency` clean.
- [x] Acting head of board sign-off.
```

Read this example, then forget it. It is intentionally trivial so its shape — section ordering, heading levels, the one-line N/A pattern — is what registers, not its content.

## Validation Checklist (pre-PR gate)

Run every check below before raising the PR for your per-repo blueprint. Every box must be checked.

- [ ] All 13 sections present (no `{PLACEHOLDER}` or `<placeholder>` tokens remain).
- [ ] Frontmatter is YAML-valid (parse: `python3 -c "import yaml,sys; yaml.safe_load(open('<path>').read().split('---')[1])"` — exits 0).
- [ ] Every canonical entity in § 5 is cited via `014-DR-GLOS-canonical-glossary.md` link AND `012-AT-ARCH-platform-runtime-blueprint.md` § 2.N reference, NOT redefined locally.
- [ ] Anti-goals in § 3.4 inherit Blueprint A § 3 explicitly AND add at least one repo-specific anti-goal (or document why none apply).
- [ ] Testing strategy (§ 7) cites the in-repo audit-harness invocation (`pnpm exec audit-harness ...` or `scripts/audit-harness ...`); NEVER `~/.claude/` paths.
- [ ] Provider PASS/FAIL gates (§ 8.3) are restated verbatim if this repo touches LLM providers; the section is present-but-marked-N/A otherwise (NOT silently deleted).
- [ ] Vendor-generic grep guard returns 0 against this file. Use the current partner-name pattern maintained in the ecosystem CLAUDE.md (`~/000-projects/CLAUDE.md`) — the pattern is intentionally NOT inlined here so this blueprint template itself stays scrubbable when new partners are added to or removed from the pattern.
- [ ] OTel events (§ 9.1) listed, with `iel-E12` forward-reference if specific event names aren't locked yet.
- [ ] Bead prefix + Plane module declared in § 12; matches Blueprint A § 2.1 taxonomy.
- [ ] All Decision Record cross-references resolve — target files exist on `main` at `intent-eval-lab/000-docs/`.
- [ ] Author's Guide block-quote callouts have been deleted from the per-repo blueprint.
- [ ] `/validate-consistency` clean against this repo's own docs (drift check between per-repo blueprint, `README.md`, `CHANGELOG.md`, and code reality).

If any check fails, fix it before raising the PR. Maintainers reviewing the PR should re-run every check and refuse merge on the first miss.

---

## Drift handling

When this template document (`013-AT-SPEC-...`) is updated in a backward-incompatible way (a new section is added; an existing section's required content shifts; a Validation Checklist item is added), every per-repo blueprint in the ecosystem becomes out-of-date until updated. Drift handling discipline:

- **MINOR template updates** (new optional sub-section; new Validation Checklist item that does not invalidate existing blueprints): per-repo blueprints update opportunistically at next material change to the repo. No forcing function.
- **MAJOR template updates** (new required section; reshape of an existing required section's contract): triggers a Class-2 pair Decision Record AND a follow-up bead in every affected repo's prefix to re-apply the template. Per-repo blueprints become non-compliant until updated; non-compliance surfaces as a `/validate-consistency` HIGH finding.

This document tracks its own version via the `iel-E04` epic + this file's git history. When this template bumps MAJOR, the bump commit lists every per-repo blueprint that must be re-walked.

---

## License + authority

This template is published under Apache 2.0 as part of `intent-eval-lab`. Per-repo blueprints inherit their containing repo's license — most ecosystem repos are MIT (`audit-harness`, `j-rig-skill-binary-eval`, `intent-rollout-gate`) with `intent-eval-lab` and `intent-eval-core` at Apache 2.0 per Blueprint A § 2.1.

Authority chain for any per-repo blueprint authored from this template: Blueprint A (constitution) → Blueprint B (kernel + canonical entities) → Blueprint C (this template) → the canonical glossary (terminology source of truth) → the binding Decision Records cited in the per-repo blueprint's frontmatter `related_drs` field.

The per-repo blueprint is **NORMATIVE for its own repo**. It is the single source of truth for that repo's identity, architecture, boundaries, and DoD. Drift from the per-repo blueprint within the repo it governs is treated as drift from the constitution itself.
