# Phase B Scope Refinement — Synthesis of Three Part 2 Landscape Docs

| Field | Value |
|---|---|
| **Date** | 2026-05-10 |
| **Author** | Jeremy Longshore (Intent Solutions LLC) — `jeremy@intentsolutions.io` |
| **Status** | Phase B scope refinement v1.0 — synthesis of three Part 2 landscape docs |
| **Workstream** | D (synthesis) of the Part 2 three-repo convergence research plan |
| **Master plan** | `~/.claude/plans/please-take-your-time-glimmering-stardust.md` § Part 2 |
| **Source landscape docs** | A: `audit-harness/000-docs/002-RR-LAND-upgrade-landscape.md` · B: `j-rig-binary-eval/000-docs/018-RR-LAND-multi-provider-spec-matrix.md` · C: `intent-eval-lab/000-docs/002-RR-LAND-mcp-testing-bridge.md` |
| **Phase A artifacts referenced** | `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/SPEC.md` · `intent-eval-lab/000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` · `audit-harness/000-docs/001-DR-DESIGN-evidence-bundle-envelope-design-notes.md` |
| **Scope** | Phase B scope refinement — NOT implementation, NOT customer-acquisition strategy, NOT packaging |

---

## 1. Mission and ambition — industry-standard substrate, not internal tooling

The three repos — `audit-harness`, `j-rig-skill-binary-eval`, `intent-eval-lab` — are not internal tooling for Intent Solutions partner engagements. They are **candidate substrate for an industry standard** for evaluating the agent-runtime arena. The empirical proving ground is Intent Solutions' multi-vendor partner work (the primary client engagement, an active revenue client, two inbound credibility engagements — MM-1 through MM-6 failure-shapes were *found*, not theorized). The synthesis target for Phase B is the structural reshape that lets every artifact published by the three repos be consumed by an outside party (a partner, an auditor, an OSS contributor, an OTel SIG-GenAI reviewer, an in-toto attestation verifier) without that party having to know anything about Intent Solutions' internal engagements.

Phase A landed three skeletons (`SPEC.md` for the Evidence Bundle, RFC draft for OTel rollout-gate semantic conventions, envelope design notes for gate-result rows). The three Part 2 landscape docs span 15,000 words across three workstreams (A: audit-harness, B: j-rig multi-provider, C: MCP testing bridge), surfacing **17 Phase B candidate work items** and **2 Phase C candidates**.

This document deduplicates, sequences, and prunes those 17 candidates into a coherent Phase B work plan that converges on the industry-standard ambition.

The four synthesis lenses below are USER-PROVIDED ENHANCEMENTS to the original plan (not appearing in the three landscape docs as authored). They thread through every Phase B item annotation in § 5.

---

## 2. The four synthesis lenses

### 2.1 Lens 1 — The arena (5 surfaces)

The convergence operates across five distinct surfaces, each of which can carry conformance claims:

| Surface | What it is | Example |
|---|---|---|
| **API** | Provider-side HTTP/RPC endpoint that returns model output or tool result | Anthropic Messages API, OpenAI Responses API, Gemini API, MCP server `tools/call` JSON-RPC |
| **CLI** | The local binary an operator runs | `claude`, `codex`, `gemini`, `cursor`, `aider`, `cline` |
| **MCP server** | A separately-running protocol surface the agent invokes via JSON-RPC | an enterprise mobile-testing MCP server, custom Plane MCP server, OpenAI MCP servers, gleanwork MCP examples |
| **Agent** | The runtime that composes API + tool calls + memory + hooks | Claude Code, Codex CLI, Gemini CLI, Cline, Cursor, Continue.dev |
| **SKILL.md** | The instruction-shaped artifact that primes the agent for a task | `SKILL.md`, `AGENTS.md`, `.cursor/rules/*.mdc`, `.windsurf/rules/*.md`, `GEMINI.md`, `.continue/checks/*.md`, `CONVENTIONS.md` |

Every Phase B item gets evaluated against which surface(s) it covers. A single repo may ship conformance claims for one surface (an MCP-server-only repo) or for all five (an end-to-end plugin with SKILL.md + agent runtime hints + an MCP server + CLI shape + API shape).

Connection to Phase A: the OTel RFC's `agent.rollout.gate.*` events are *agent-surface* signals. The Evidence Bundle envelope is *cross-surface* (any row can attest to any surface). The gate-result envelope design notes are *agent + MCP-server* surface conformance.

### 2.2 Lens 2 — Both sides (client + server)

Evaluation must cover both:

- **Client side** — what the agent runtime does with credentials, scopes, tool-call permissions, allowlists, `claude_code.tool_decision` decisions, `permission_request`s, hook decisions. This is the side B-doc covers exhaustively (vendor matrix of activation modes, frontmatter, hook firing, OTel emission gating).
- **Server side** — what the MCP server / API endpoint enforces for those credentials, what it emits, what's auditable from outside. This is the side C-doc's bridge-gap map covers (MM-1..MM-6 against server-emitted state).

Most existing tooling collapses one side or the other. A vendor-neutral evaluation standard must explicitly attest **independently** to both, with the Evidence Bundle Statement's `subject` field naming which side a given attestation row covers.

Connection to Phase A: the gate-result envelope's `gate_id` field is the discriminator. Convention: `audit-harness:client:escape-scan` versus `audit-harness:server:mcp-strict-mode` versus `j-rig:agent:skill-activation`. Phase B `gate_id` naming convention is a normative work item (see PB-2 below).

### 2.3 Lens 3 — The transformation pipeline

A capability travels along this hop chain:

```
API  →  CLI wrapper  →  MCP server  →  SKILL.md  →  agent runtime
```

Each hop is its own evaluable + attestable surface, and the in-toto `subject` field can name the **exact transformation point being attested**. Examples:

- An attestation about an **API → CLI** transformation: "the `codex` CLI v0.130.0 binary correctly maps OpenAI Responses-API `tool_calls` shape to its action-log emission."
- An attestation about a **CLI → MCP server** transformation: "the enterprise mobile-testing MCP server's `confirmAppUpload` tool returns a shape consistent with the SKILL.md's `argument-hint` declaration."
- An attestation about an **MCP server → SKILL.md** transformation: "the Plane MCP server's tool list matches the project's `SKILL.md` `allowed-tools` declaration with no orphans."
- An attestation about a **SKILL.md → agent runtime** transformation: "Claude Code v2.1.128 reads the SKILL.md's `effort: high` declaration and emits `claude_code.skill_activated` with `effort=high` in span attributes."

This pipeline lens means Phase B is not "build the conformance harness." It is "name every hop, define what evidence each hop emits, let consumers compose partial coverage into a derived total."

Connection to Phase A: the in-toto Statement `subject` field is exactly the mechanism. Phase A's gate-result envelope design notes mention `repo` + `commit_sha` in metadata but do **not** yet codify the pipeline-hop discriminator. PB-1 below makes this explicit.

### 2.4 Lens 4 — Composable partial attestation

The standard must be **attackable from any component-angle as a valid entry**, with **partial attestation honored, not penalized**. Concretely:

- A repo that ships only audit-harness static-gate rows (escape-scan, CRAP, arch-check) → emits a valid Evidence Bundle.
- A repo that ships only MCP-server conformance rows (mcp-validator transport check + Intentional Mapping MM-3 cooldown verification) → emits a valid Evidence Bundle.
- A repo that ships rows for every hop in the pipeline → emits a valid full-chain Evidence Bundle.
- **Silence about a dimension is "this implementation chose not to cover X," not "this implementation failed X."**
- **Coverage is a derived signal** a consumer computes (e.g., "this bundle covers 4 of 7 pipeline hops, 2 of 5 surfaces, 1 of 6 MM-categories") — it is **not** a required field of the bundle envelope.

This is the single architectural decision that separates an industry standard from internal tooling. An internal tool can require full-chain coverage; a standard CANNOT. If conformance requires coverage of every hop, every surface, every MM-category, no implementation outside the original author will ever ship a conformance report — and the standard will not be a standard.

Connection to Phase A: the Evidence Bundle SPEC.md skeleton's R6 ("tamper evidence via hash chain") works fine under partial attestation — hash-chaining N rows is the same primitive whether N=1 or N=20. The OTel RFC's events fire independently per gate. The gate-result envelope is per-row, not per-bundle. **All Phase A choices already support partial attestation**; Phase B must avoid introducing requirements that break this property. See § 5 PB-3 for the explicit non-requirement.

---

## 3. The cross-doc convergence point — in-toto Statement v1 as the Evidence Bundle envelope

All three landscape docs converge on the same architectural keystone, and getting it right is the single highest-cost decision to defer.

| Doc | Position | Quote / paraphrase |
|---|---|---|
| **A (audit-harness)** | PB-1 (highest ROI): "Wrap the gate-result envelope in an in-toto Statement." | "Single biggest payoff in the landscape — opens GUAC, Cosign, SLSA-tool interop for the price of ~20 lines." |
| **C (mcp-testing-bridge)** | B-5 (Phase B work item): "in-toto attestation envelope for signed conformance reports." | "Each conformance run produces a signed `conformance/v1` predicate (new predicate type)… complements Phase A RFC's `agent.evidence_bundle.*` events." |
| **B (j-rig)** | Implicit — does not address envelope choice. | (Vendor-neutralization is orthogonal to envelope shape; B's silence does not contradict A and C.) |

**Recommendation: adopt in-toto Statement v1 as THE envelope for every Evidence Bundle row.** Every row becomes:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{"name": "<pipeline-hop-id>", "digest": {"sha256": "..."}}],
  "predicateType": "https://evals.intentsolutions.io/gate-result/v1",
  "predicate": { <current envelope contents per AH-4 design notes> }
}
```

**Why this is the keystone:**

1. **It is the smallest envelope change with the largest external interop payoff.** A-doc estimates ~20 lines of wrapping. The payoff: GUAC ingestion for free, Cosign signing compatibility for free, SLSA-toolchain interop for free, in-toto verifier compatibility for free, every downstream attestation consumer interprets the bundle correctly without bespoke integration.
2. **It makes the `subject` field load-bearing as the pipeline-hop discriminator** (Lens 3). The standard doesn't need a new field for "which hop is this attesting"; in-toto Statement's existing `subject` is exactly that field.
3. **It makes partial attestation native** (Lens 4). An in-toto Statement attesting to one subject is *normal*; an in-toto Statement attesting to many subjects is also *normal*; consumers compose multiple Statements into a bundle without any requirement that the bundle be "complete."
4. **It makes signing additive** (Lens 2 client/server independence). Each in-toto Statement signs independently. A bundle can ship 4 server-side rows signed by the server author and 3 client-side rows signed by the agent runtime author — no envelope-level coordination required.
5. **Deferring this decision is the highest-cost path.** If PB-2 (audit-harness `--json` emission) and PB-3 (`emit-evidence` subcommand) ship against the bespoke envelope and the in-toto wrap lands in a later minor, every downstream consumer rewrites its parser. If the wrap lands first, every emitter ships against the final shape.

**Action:** PB-1 lands first in Phase B sequencing. Every other emission work item in Phase B depends on it.

---

## 4. Standards-track artifacts vs Intent Solutions implementation

The industry-standard ambition becomes concrete in this split. Some Phase B work products are published as public standards proposals (filed against external standards bodies / open-spec repos); others stay as Intent Solutions implementation that consume those standards.

| Phase B output | Where it lives | What kind of artifact | Why standards-track |
|---|---|---|---|
| **Evidence Bundle gate-result-row schema (in-toto-wrapped)** | `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/gate-result.json` + filed as an in-toto **predicate type** at `https://github.com/in-toto/attestation` (predicate name: `https://evals.intentsolutions.io/gate-result/v1`) | Public standards-track (in-toto predicate) | Same shape SCAI, SLSA Provenance, VSA use. Standardizing the predicate URI lets non-Intent-Solutions emitters publish compatible rows. |
| **OTel `agent.rollout.gate.*` semantic conventions** | RFC text already drafted at `intent-eval-lab/000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` → filed at `open-telemetry/semantic-conventions` | Public standards-track (OTel SIG-GenAI RFC) | Same scope as the `gen_ai.*` semantic conventions OpenLLMetry upstreamed. Adoption by every CLI vendor (Claude Code, Codex CLI, Gemini CLI) makes cross-vendor observability possible. |
| **Matcher-map signal vocabulary (MM-1..MM-6 categories as OTel semantic conventions)** | Sibling RFC, filed at `open-telemetry/semantic-conventions` SIG-GenAI track | Public standards-track (OTel SIG-GenAI RFC) | C-doc's § 8 cross-cutting gap. Today, MM-1..MM-6 are markdown-table prose; standardizing them as named OTel signals makes every collector + downstream tool able to filter on them by name. |
| **AGENTS.md normative parser shape** | Reference parser at `j-rig-binary-eval/packages/core/src/parsers/agents-md-parser.ts` + filed as a parser-contract reference against `agents.md` open standard | Public standards-track (agents.md ecosystem contribution) | ~20 vendors recognize AGENTS.md. A reference parser shape settles ambiguity (heading conventions, nesting precedence, programmatic-check extraction). |
| **Pact-style MCP plugin contract format** | `intent-eval-lab/specs/mcp-plugin-contract/v0.1.0-draft/` + proposed as Pact v4 extension at `pact-foundation/pact-specification` | Public standards-track (Pact v4 extension) | C-doc B-3. Lets agent-harness authors and plugin authors share contracts via existing Pact broker infrastructure. |
| **MM-1..MM-6 Gherkin scenarios** | `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/scenarios/*.feature` | Public reference content (Apache 2.0 in intent-eval-lab repo) | C-doc B-4. Human-readable expression of the Intentional Mapping spec; not a separate standards body submission, but published under the spec for community reuse. |
| **audit-harness `emit-evidence` subcommand** | `audit-harness/scripts/emit-evidence.{sh,py}` + `bin/audit-harness.js` dispatch | Intent Solutions implementation | Reference emitter against the public schema. Other emitters (e.g., a Stryker-side emitter, a Sonar-side emitter) can ship independently against the same schema. |
| **audit-harness `--json` flag on all subcommands** | `audit-harness/scripts/*.sh` + `crap-score.py` | Intent Solutions implementation | Internal prerequisite for `emit-evidence`. No external party cares whether the harness's text mode coexists with JSON mode. |
| **audit-harness backward-compat regression suite** | `audit-harness/tests/regression/` | Intent Solutions implementation | Internal hygiene. |
| **j-rig vendor-namespaced schema (`ModelTarget` → `{vendor, model, roles}`)** | `j-rig-binary-eval/packages/core/src/schemas/eval-spec.ts` | Intent Solutions implementation | Internal API surface. The schema reshape unblocks multi-provider support but the public face of j-rig is its emitted Evidence Bundle rows, which are standards-track. |
| **j-rig provider adapters (LiteLLM-backed or Vercel-AI-SDK-backed)** | `j-rig-binary-eval/packages/cli/src/providers/` | Intent Solutions implementation | Internal dispatch layer. |
| **j-rig per-vendor reporting layer (Aider-leaderboard format)** | `j-rig-binary-eval/packages/core/src/governance/per-vendor-scoring.ts` | Intent Solutions implementation (with public reporting template) | The output table is consumed by humans; the format mirrors Aider's leaderboard which is itself a community convention. |
| **OTel collector + Tempo + Refinery reference deployment** | `intent-eval-lab/reference-deployment/` (docker-compose + Tempo config + Refinery rules) | Intent Solutions implementation (public reference) | C-doc B-4. Not a standard, but a published reference for adopters who want to reproduce the assertion infrastructure. |

**Summary of the split:** 6 of the Phase B work products are public standards-track (in-toto predicate, two OTel RFCs, AGENTS.md parser, Pact-extension format, Gherkin scenarios under the spec). 6 are Intent Solutions implementation. The standards-track items are where industry-standard ambition becomes concrete; the implementation items demonstrate the standards work in practice (the reference implementation pattern Phase A's OTel RFC already invokes).

---

## 5. Evidence-backed Phase B scope — 12 work items

Synthesized from 17 Phase B candidates across the three landscape docs (A:6 + B:8 + C:3). Deduplicated, sequenced by dependency, clustered by purpose.

**Cluster I — Envelope + emission (PB-1..PB-4):** the foundational shape every other emitter depends on.
**Cluster II — Vendor coverage (PB-5..PB-9):** j-rig becomes vendor-neutral.
**Cluster III — Protocol conformance (PB-10..PB-12):** MCP-testing-bridge primitives lay groundwork for Phase C harness.

Each work item carries: ID, title, source workstream(s), arena-surfaces covered (lens 1), client/server side (lens 2), pipeline-hop (lens 3), partial-attestation effect (lens 4), estimated effort, primary-source links, dependency.

### Cluster I — Envelope + emission

#### PB-1. Wrap gate-result envelope in in-toto Statement v1

- **Source:** A § 8 PB-1 + C § 9 B-5 (convergence point).
- **Surfaces:** all 5 (the envelope is surface-agnostic).
- **Side:** both — the envelope is identical for client-side and server-side rows.
- **Pipeline hop:** carries the hop ID in `subject`.
- **Partial-attestation effect:** **enabling** — in-toto Statement is *the* primitive that makes partial attestation native.
- **Effort:** S (schema edit; ~20 lines of wrapping; updates JSON Schema + AH-4 design notes + the SPEC.md skeleton).
- **Primary sources:** [in-toto Statement v1 spec](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) · [SLSA v1.0 provenance](https://slsa.dev/spec/v1.0/provenance) · [SCAI predicate (arXiv 2210.05813)](https://arxiv.org/abs/2210.05813).
- **Dependency:** none. **Lands first.**

#### PB-2. Codify `gate_id` naming convention (client/server discriminator) + register predicate URI

- **Source:** new — derived from Lens 2 (both-sides). Implicit in A § 7 (gate-result row shape).
- **Surfaces:** all 5.
- **Side:** **the work item exists to make the side dimension explicit** in the schema.
- **Pipeline hop:** orthogonal.
- **Partial-attestation effect:** **enabling** — the discriminator means a bundle with only client-side rows is unambiguously partial-coverage-by-design, not ambiguous-coverage.
- **Effort:** XS (naming convention doc + JSON Schema regex pattern + register `https://evals.intentsolutions.io/gate-result/v1` URI).
- **Primary sources:** § 2.2 of this doc.
- **Dependency:** PB-1.

#### PB-3. Add uniform `--json` flag to all audit-harness subcommands

- **Source:** A § 8 PB-2 (= bead `AH-2`).
- **Surfaces:** primarily SKILL.md + CLI (audit-harness gates static repo content + CLI invocation).
- **Side:** client (the harness analyzes the repo being authored, not the server it talks to).
- **Pipeline hop:** SKILL.md author / CLI wrapper.
- **Partial-attestation effect:** **neutral** — emitters that don't ship `--json` simply don't contribute rows; their silence is not penalty.
- **Effort:** M (6 scripts × ~30 LOC + shared JSON-emitter helper).
- **Primary sources:** `audit-harness/scripts/crap-score.py` (reference implementation).
- **Dependency:** PB-1 (so the emitter ships against the final wrapped shape).

#### PB-4. Implement `audit-harness emit-evidence` subcommand

- **Source:** A § 8 PB-3 (= bead `AH-3`).
- **Surfaces:** SKILL.md + CLI.
- **Side:** client primarily; can emit server-side rows when handed server-evaluation results.
- **Pipeline hop:** any — the subcommand accepts a `--subject` flag naming the hop.
- **Partial-attestation effect:** **enabling** — the emitter produces one row per invocation; bundles are concatenations.
- **Effort:** M.
- **Primary sources:** [in-toto Statement spec](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) · `001-DR-DESIGN-evidence-bundle-envelope-design-notes.md`.
- **Dependency:** PB-1 + PB-3.

### Cluster II — Vendor coverage (j-rig multi-provider)

#### PB-5. Vendor-namespace the j-rig schema

- **Source:** B § 8 item 8.1.
- **Surfaces:** SKILL.md (the schema describes SKILL.md / AGENTS.md / .mdc inputs) + agent runtime (the schema declares which models / vendors execute the eval).
- **Side:** client (j-rig grades client-authored artifacts).
- **Pipeline hop:** SKILL.md → agent runtime.
- **Partial-attestation effect:** **enabling** — vendor-namespacing means a row attesting to a Claude-Code-specific behavior does not pretend to attest to Cursor.
- **Effort:** ~1 day (`packages/core/src/schemas/eval-spec.ts` 52-line edit + tests + ~5 callsite migrations).
- **Primary sources:** B § 3.1 + § 6 item 2 (Vercel AI SDK factory pattern).
- **Dependency:** none (parallel with Cluster I after PB-1).

#### PB-6. Rename `anthropic:` check IDs to `vendor:anthropic:`

- **Source:** B § 8 item 8.3.
- **Surfaces:** SKILL.md.
- **Side:** client.
- **Pipeline hop:** SKILL.md.
- **Partial-attestation effect:** **enabling** (consistent with PB-5: vendor-namespaced check IDs in the schema match vendor-namespaced row emission).
- **Effort:** XS (~½ day, 6 hits in `package-checker.ts` + tests + deprecation alias for one release).
- **Primary sources:** B § 7 item 8.
- **Dependency:** PB-5.

#### PB-7. Add provider adapters (LiteLLM-or-Vercel-AI-SDK decision deferred to prototype)

- **Source:** B § 8 item 8.2.
- **Surfaces:** API + agent runtime.
- **Side:** client (the adapters drive the agent to execute against an API).
- **Pipeline hop:** API → CLI wrapper.
- **Partial-attestation effect:** **enabling** — a row attesting to "OpenAI gpt-5 response had property X" is now expressible.
- **Effort:** M-L (single LiteLLM file ~150 LOC OR N stubs ~80 LOC each). **Decision deferred to in-Phase-B prototype** — landscape doc explicitly does not pre-empt.
- **Primary sources:** [LiteLLM](https://github.com/BerriAI/litellm) · [Vercel AI SDK](https://github.com/vercel/ai) · [Aider polyglot leaderboard](https://aider.chat/docs/leaderboards/) as the LiteLLM-in-production proof point.
- **Dependency:** PB-5.

#### PB-8. Add AGENTS.md parser (cross-vendor baseline)

- **Source:** B § 8 item 8.4.
- **Surfaces:** SKILL.md (across ~20 vendor ecosystems).
- **Side:** client.
- **Pipeline hop:** SKILL.md author.
- **Partial-attestation effect:** **enabling** — one parser covers the lowest-common-denominator surface for all vendors that recognize AGENTS.md (Codex CLI, Gemini CLI, Aider, Cursor, Windsurf, Continue.dev, Cline, Copilot Coding Agent, etc.). A row attesting "this repo's AGENTS.md is heading-conformant" is portable across all those vendors.
- **Effort:** ~1.5 days (`agents-md-parser.ts` ~120 LOC + tests + snapshot in `references/specs/`).
- **Primary sources:** [agents.md](https://agents.md/) · B § 4.2.
- **Dependency:** PB-5 (so the parsed output emits as vendor-namespaced rows when consumed).

#### PB-9. Vendor spec snapshots in `references/specs/`

- **Source:** B § 8 item 8.5.
- **Surfaces:** SKILL.md + CLI + agent runtime (per vendor).
- **Side:** client.
- **Pipeline hop:** SKILL.md.
- **Partial-attestation effect:** **enabling** — each snapshot is independently consumable; j-rig can evaluate a Cursor-shaped skill against the cursor-mdc snapshot without needing the windsurf snapshot loaded.
- **Effort:** ~2 days (six new snapshot files + extend `SpecAuthority` in `governance/spec-sources.ts`).
- **Primary sources:** B § 3 + § 4.
- **Dependency:** PB-5.

### Cluster III — Protocol conformance + observability

#### PB-10. File OTel SIG-GenAI RFC: `agent.rollout.gate.*` semantic conventions

- **Source:** Phase A draft already authored at `intent-eval-lab/000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`; C § 11 Phase B item B-1 calls this out as the multiplier.
- **Surfaces:** agent runtime + API (the events fire from the rollout gate, which is agent-runtime-emitted).
- **Side:** client (the agent runtime is client-side relative to the model provider; relative to the partner consuming the gate decision, "agent runtime" is the observed party).
- **Pipeline hop:** SKILL.md → agent runtime → external CI gate.
- **Partial-attestation effect:** **enabling** — a CI gate firing the events doesn't require any other surface to also fire events; consumers compose what fires.
- **Effort:** ~3 weeks (community review cycle dominates engineering time).
- **Primary sources:** [OTel SIG-GenAI charter](https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md) · existing draft at Phase A.
- **Dependency:** none.

#### PB-11. File OTel SIG-GenAI RFC: Intentional Mapping signal vocabulary (MM-1..MM-6 as named conventions)

- **Source:** C § 8 cross-cutting gap + C § 11 Phase B item B-1 (sibling RFC).
- **Surfaces:** MCP server + agent runtime (signals fire at the hook + tool layer).
- **Side:** **explicitly both** — MM-1 (async race) is observable from the agent emitting `tool_decision` events and from the server emitting reconciled state.
- **Pipeline hop:** MCP server → agent runtime → external assertion.
- **Partial-attestation effect:** **enabling** — codifying MM-1..MM-6 as named signals means a collector + downstream checker can filter on them by name without parsing Intentional Mapping markdown.
- **Effort:** ~3 weeks (RFC drafting + community review).
- **Primary sources:** [OTel semantic-conventions GenAI](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai) · `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/intentional-mapping-template.md`.
- **Dependency:** none (parallel with PB-10).

#### PB-12. Author Gherkin scenarios for MM-1..MM-6 + author Pact-extension format

- **Source:** C § 11 Phase B items B-2 (Pact extension), B-5 (Gherkin scenarios).
- **Surfaces:** MCP server.
- **Side:** **both** — Pact is consumer-driven (client declares, server verifies); Gherkin scenarios are human-readable expressions of either side's expectations.
- **Pipeline hop:** MCP server.
- **Partial-attestation effect:** **enabling** — a plugin author can verify its server against the Pact without the agent-harness side having shipped its consumer pact yet (or vice versa).
- **Effort:** ~3-4 weeks combined (2 weeks Pact-extension spec + 1-2 weeks Gherkin scenarios).
- **Primary sources:** [Pact spec](https://github.com/pact-foundation/pact-specification) · [Cucumber](https://github.com/cucumber).
- **Dependency:** PB-11 (so the Gherkin scenarios reference standardized OTel signal names).

### Sequencing summary

| Sequence | Items | Why |
|---|---|---|
| **Wave 1 (immediate)** | PB-1, PB-10, PB-11 | PB-1 unblocks all emission. PB-10 + PB-11 file in parallel — community-review time is the dominant cost and starts the clock. |
| **Wave 2 (PB-1 lands)** | PB-2, PB-3, PB-5, PB-9 | Schema work everywhere — vendor namespace, gate_id convention, JSON emission, vendor snapshots. Parallelizable across one engineer or two. |
| **Wave 3 (Waves 1-2 land)** | PB-4, PB-6, PB-7, PB-8 | Subcommand emission, check-ID renames, provider adapters, AGENTS.md parser. Depends on schema being settled. |
| **Wave 4 (Waves 1-3 land)** | PB-12 | Gherkin scenarios + Pact extension reference the codified OTel signal names. |

**Items dropped or merged from the original 17:**

- A-doc's PB-4 (backward-compat regression suite, bead `AH-5`) merged into PB-3/PB-4 as a sub-acceptance-criterion ("changes must not break v0.x CLI surface"). Not a separate Phase B item; it is *part of* shipping PB-3/PB-4 responsibly.
- A-doc's PB-5 (mutation-kill-rate dispatcher) **deferred to Phase C or later.** It is a substantial new capability (per-language adapter complexity, performance tuning per Sánchez et al.) that does not block convergence emission. File as a Phase-C+ candidate (see § 6).
- A-doc's PB-6 (reserve signature slot) **folded into PB-1.** Adding the optional `signatures: []` is part of the in-toto Statement wrap, not a separate work item.
- B-doc's PB-6 (Aider-style per-vendor reporting) **deferred to Phase B' (post-Wave-4).** It is a polish item that depends on PB-7 provider adapters and ~2 days; can ship as part of the post-Wave-4 stabilization but is not a Wave 1-4 dependency.
- B-doc's PB-7 (OTel `gen_ai.*` span emission in j-rig) **deferred to Phase C.** Wrapping j-rig's provider calls in `gen_ai.*` spans depends on PB-7 provider adapters being settled and is itself a ~2-day pure-additive item; better landed alongside the Phase C executable conformance harness so the two telemetry streams co-evolve.
- B-doc's PB-8 (MCP-conformance check bundle) **deferred to Phase C.** This overlaps with C-doc's Jepsen-style nemesis harness; consolidating to one Phase C work item avoids fragmenting MCP conformance work.

### Cross-doc conflicts identified + reconciled

1. **CONFLICT: B-doc PB-8 (MCP-conformance check bundle in j-rig) overlaps with C-doc Phase B B-2 (Pact-style MCP plugin contract).**
   - **Reconciliation:** consolidate. PB-12 (Pact-extension + Gherkin) is the canonical Phase B MCP-conformance work. j-rig's role is to *emit rows that reference* the Pact verifier's output, not to embed its own MCP checker. B-doc PB-8 is dropped from Phase B; its semantic content is absorbed by PB-7 (provider adapters can drive an MCP server through the Pact verifier as part of a j-rig eval).
2. **CONFLICT: A-doc's `IEL-CONV-2` reference (PB-1) and C-doc's B-5 (Conformance Provenance predicate) both define new in-toto predicates.**
   - **Reconciliation:** they are **two complementary predicate types**, not one. PB-1 codifies `https://evals.intentsolutions.io/gate-result/v1` (a single gate's row, audit-harness + j-rig emit these). The Conformance Provenance predicate from C-doc B-5 codifies `https://evals.intentsolutions.io/conformance-provenance/v1` (a *run* of a Intentional Mapping harness against a plugin, with aggregated PASS/PARTIAL/FAIL per row). Different scope. **Both are Phase B work**; PB-1 ships the gate-result predicate (Wave 1), and the Conformance Provenance predicate ships as **a sub-task of PB-12** (because it wraps the Pact/Gherkin verifier output). The naming + scope distinction goes in the PB-1 schema docstring + PB-12 spec.
3. **NO CONFLICT (positive confirmation): B-doc's vendor-namespacing (`vendor:anthropic:*`) and PB-1's in-toto-Statement subject naming are orthogonal.** The `gate_id` field in the predicate (PB-2) follows vendor-namespacing convention; the in-toto `subject` field (PB-1) names the pipeline hop being attested. They don't collide.
4. **NO CONFLICT (positive confirmation): A-doc's `policy_hash` + `input_hash` fields and C-doc's MM-1..MM-6 signal vocabulary do not contradict.** `policy_hash` hashes the gate's policy; MM-N names the failure-shape category. Both can appear in one in-toto Statement — `predicate.policy_hash` for the policy artifact, `predicate.matcher_map_category: "MM-1"` for the shape — without ambiguity.
5. **POTENTIAL ASSUMPTION CONFLICT: B-doc Lens-1 silence on vendor priority.** B-doc does not pre-rank vendors beyond the matrix; A-doc assumes "audit-harness must work everywhere" (per `--json` on all subcommands). The composable-partial lens (Lens 4) resolves this: no vendor must be prioritized — partial vendor coverage is fine. **Reconciliation:** PB-9 ships *all six* vendor snapshots as a batch, not gating on a "primary" vendor.

---

## 6. Phase C scope — 4 work items (conditional on first-paying-customer signal)

Phase C is the executable conformance harness layer that consumes the Phase B-codified standards. Each item is conditional on first-paying-customer signal per the master plan; none of them lock until that signal arrives.

| ID | Title | Source | Phase B precondition | Effort |
|---|---|---|---|---|
| **PC-1** | Jepsen-style nemesis-generator-checker harness against the Intentional Mapping | C § 11 Phase C C-1 (B-1 in C-doc § 9) | PB-11 (Intentional Mapping signals codified as OTel conventions) + PB-12 (Pact extension format) | 6-10 weeks |
| **PC-2** | Hypothesis-based `@matcher_map_rule` decorator library | C § 11 Phase C C-2 (B-2 in C-doc § 9) | PB-11 (signal vocabulary) | 4-6 weeks |
| **PC-3** | Mutation-kill-rate dispatcher (audit-harness `audit-harness mutation` subcommand, per-language) | A § 8 PB-5 (deferred from Phase B) | PB-4 (`emit-evidence` ships rows the dispatcher emits to) | L (~3-5 weeks) |
| **PC-4** | OTel `gen_ai.*` span emission across j-rig provider calls + Aider-style per-vendor reporting layer | B § 8 PB-7 + PB-6 (deferred from Phase B) | PB-7 (provider adapters) + PB-10 (rollout-gate conventions in production) | ~1 week |

**Phase B vs Phase C split rationale:** Phase B is **codification** (specs, schemas, conventions, parsers). Phase C is **execution** (harnesses that consume the codifications and produce conformance verdicts). The split lets Phase B ship public standards-track work that is useful to outside parties before the first paying customer signal arrives — and Phase B's outputs **stand alone as deliverables** (an in-toto predicate, two OTel RFCs, a Pact extension, an AGENTS.md parser) even if Phase C never ships under Intent Solutions. This is the maturity-of-standard property: the spec outlives any one implementation.

---

## 7. MM-7 candidate — gleanwork "tool-discoverability"

C-doc § 5 surfaces gleanwork/mcp-server-tester's category of "tool discoverability" assertions (LLM-as-judge: can the agent find the right tool given an ambiguous query?). The doc explicitly flags this as a candidate MM-7.

**Synthesis decision: defer to first observed failure-in-the-wild. Do NOT file MM-7 now.**

Rationale:

1. **Empirical discipline** — MM-1..MM-6 were *found* in Intent Solutions partner engagements (the primary client engagement F-findings F11..F35 directly mapped, plus an active revenue client / two inbound credibility engagements failure-shapes via the engagement structure). MM-7 from a third-party tool's category is **theorized**, not found. Filing MM-7 from a doc rather than from a failure would dilute the credibility property that distinguishes the Intentional Mapping standard from a survey-of-tools.
2. **Coverage overlap** — gleanwork's tool-discoverability is arguably an MM-5 instance (mandatory context the model isn't providing — namely, the right tool ID in its allowlist), not a distinct shape. The C-doc itself flags this ambiguity ("a sibling MM-5 issue that may warrant its own MM-7 category"). Until a real engagement surfaces a failure-shape that **does not fit MM-1..MM-6**, MM-7 stays unallocated.
3. **Standards-track discipline** — published specs that grow categories speculatively get accused of bloat. Six categories shipped as `v0.1.0-draft` with a clear empirical provenance is a stronger position than seven categories where the seventh is "we read about this."

**Action:** add a note to `specs/mcp-plugin-observability/v0.1.0-draft/intentional-mapping-template.md` saying MM-7 is reserved-but-unallocated and citing gleanwork as the prior art that motivates the reservation. When a real partner-engagement failure surfaces that doesn't fit MM-1..MM-6, document the failure and file MM-7 in `v0.2.0`.

---

## 8. Open decisions held for first-paying-customer signal

These do NOT lock during Phase B. Each has a trigger condition that justifies revisiting.

| Decision | What stays open | Trigger condition |
|---|---|---|
| **CLI distribution** | Whether `audit-harness`, `j-rig`, `intent-eval-lab/cli/` ship as separate npm packages, one umbrella package, or per-language packages | First paying customer asks "how do I install this?" — answer drives the packaging shape |
| **Monetization** | Whether the standards work + reference implementations are 100% Apache 2.0 with services-on-top, or whether some surface (e.g., a hosted conformance verifier, a managed Collector deployment) is commercial | First paying-customer engagement spec (M-series for that customer) declares scope |
| **Vendor priority beyond what landscape data justifies** | If a customer wants Cursor / Windsurf / Cline support before AGENTS.md baseline, B-doc's PB-9 batch sequencing might split | A specific vendor request from a paying customer |
| **MM-7 disposition** | See § 7 — held until a real failure-in-the-wild | A partner engagement surfaces a non-MM-1..6 failure-shape |
| **LiteLLM vs Vercel AI SDK adapter choice (PB-7)** | B-doc explicitly punts on the framework choice | First Phase B PR-cycle prototype with both, measured on type-safety + DX |
| **In-toto predicate type URI ownership** | **RESOLVED 2026-05-10 (ISEDC Q1):** namespace is `evals.intentsolutions.io`. Whether the URI also lands in an in-toto-predicate-types-registry entry (in addition to the canonical hosted-spec page) remains open. | When the in-toto community + first external adopter weigh in on registry submission |
| **OTel namespace contention** | RFC open question: `agent.rollout.gate.*` vs `gen-ai.gate.*` vs `ci.gate.*` (per Phase A RFC § "Open questions") | OTel SIG-GenAI community feedback during PB-10 review |
| **Decision-enum tri-state** | Phase A RFC open question 2: `"ship" \| "no-ship"` vs adding `"indeterminate"` | First real "policy cannot conclude" case observed in production reference impl |
| **Reasons cardinality structure** | Phase A RFC open question 3: free-text `reasons[]` vs structured `{reason_id, severity}` | First dashboard / alerting consumer expressing pain on free-text |
| **Reference implementation vs standard-only ambition** | Whether Intent Solutions ships PC-1 / PC-2 Phase C harnesses publicly, or holds them as differentiator | First competitor's reference implementation appears (defensive trigger) OR first paying customer requests the reference (offensive trigger) |

---

## 9. Cross-references from the three landscape docs needing explicit reconciliation

Per Workstream C's unresolved-questions list and surfacing during synthesis:

1. **Phase A RFC `agent.evidence_bundle.*` events vs Phase B-codified `agent.rollout.gate.*` events vs Phase C in-toto Conformance Provenance predicate — where does the boundary go?**
   - **Reconciliation:** the events fire at *evaluation time*; the predicate is the *signed-and-stored result*. Concretely: when a CI gate evaluates, it emits `agent.rollout.gate.evaluated` (event), then `agent.rollout.gate.decision` (event), then `agent.evidence_bundle.signature_verified` (event), then writes an in-toto Statement (predicateType: `https://evals.intentsolutions.io/gate-result/v1` for the row, `https://evals.intentsolutions.io/conformance-provenance/v1` for the run) for durable record. **Events are ephemeral; predicates are durable.** Codify this in PB-1's SPEC.md text.

2. **OTel SIG-GenAI agent-level conventions timing — may need new sub-group.**
   - **Status:** SIG-GenAI's current scope is LLM-internal signals (`gen_ai.*`). The proposed `agent.rollout.gate.*` and `agent.matcher_map.*` are agent-level / CI-level, not LLM-internal. The Phase A RFC's "Open questions" already flag this.
   - **Reconciliation:** file PB-10 + PB-11 as draft PRs against `open-telemetry/semantic-conventions` AND cross-post to SIG-GenAI's mailing list. If the SIG declines the namespace, propose a new sub-group (`SIG-Agents` or similar). The decision is community-driven and out of Intent Solutions' control — but **starting the conversation is Phase B work**, not Phase C.

3. **Doc-rot in vendor specs (Workstream B finding) affecting adapter contract assumptions.**
   - **Status:** B-doc § 3.4 flags Cursor's `.mdc` schema as "partially undocumented; reverse-engineered." B § 3.5 flags Windsurf's MCP integration as "not addressed in current public docs." B § 3.6 flags Copilot CLI as deprecated with no public successor spec.
   - **Reconciliation:** PB-9 snapshots are dated artifacts in `references/specs/`. Drift detection runs quarterly. **Add a Phase B sub-task to PB-9:** drift-detection script (`scripts/refresh-vendor-snapshots.sh`) compares the on-disk snapshot to the live URL; emits a diff for human review. Drift events are not silent failures — they file an issue.

4. **CRAP metric peer-review gap (Workstream A finding) for academic-facing publication.**
   - **Status:** A-doc § 3 surfaces that CRAP's primary citation is Alberto Savoia's 2007 Artima trade-press article — never peer-reviewed.
   - **Reconciliation:** **does not block Phase B.** When the Intentional Mapping methodology + audit-harness Evidence Bundle work eventually reaches a venue submission (post-Phase C, conditional on first-customer signal), the CRAP citation chain will need to be carefully framed: industry-original metric, in-production for ~18 years, no peer-reviewed primary but extensive practitioner adoption. This is a manuscript-prep concern, not a Phase B scope concern. **File as `intent-eval-lab` issue with `manuscript-prep` label** when academic publication track activates.

5. **Composable-partial principle vs verification gates in master plan.**
   - **Status:** master plan § "Verification gates for Part 2 research" lists "Has a 'capability gap matrix'" as required for each landscape doc. This is research-gate language ("must have"). The composable-partial lens (this doc § 2.4) says implementations are valid with partial coverage.
   - **Reconciliation:** **no conflict.** The verification gate applies to *research docs*; the partial-coverage principle applies to *emitted Evidence Bundles*. A landscape doc requires a gap matrix because that's how the research delivers value to Phase B planning. An Evidence Bundle does not require coverage of every gap because that's how the standard stays usable. Same word ("coverage") meaning different things at different layers.

---

## 10. What's NOT in scope here

To prevent scope drift in Phase B / C planning that consumes this synthesis:

- **Not implementation.** No code is being written. The first PR is whichever Phase B work item lands first (PB-1 per § 5 sequencing).
- **Not customer acquisition strategy.** § 8 names the customer-signal trigger conditions for several decisions, but does not propose a go-to-market.
- **Not packaging / distribution decisions.** § 8 leaves CLI distribution open.
- **Not naming.** "intent-eval-lab" / "audit-harness" / "j-rig-skill-binary-eval" repo names are inputs. The predicate URI namespace `https://evals.intentsolutions.io/<predicate-type>/v<version>` was decision-locked by ISEDC Q1 (2026-05-10) — see `004-AT-DECR-isedc-council-record-2026-05-10.md` § 6 Q1. Repo names themselves stay as inputs.
- **Not LAB-6 update.** § "Mission" of the parent task: the parent agent updates LAB-6 after reviewing this synthesis.
- **Not OPS-nfx update.** Same — parent agent handles.
- **Not Plane backlog grooming.** Phase B work items in § 5 are not yet filed as LAB-N children. The parent agent decides which become first-class Plane issues vs which are sub-tasks of existing IEL-CONV-N children.
- **Not changes to the three landscape docs.** They stand as-authored. This document is the *next* layer.

---

## 11. Cross-references

**The three Part 2 landscape docs (sources of this synthesis):**

- Workstream A — `/home/jeremy/000-projects/intent-eval-platform/audit-harness/000-docs/002-RR-LAND-upgrade-landscape.md` (~3,500 words, 6 Phase B candidates)
- Workstream B — `/home/jeremy/000-projects/intent-eval-platform/j-rig-binary-eval/000-docs/018-RR-LAND-multi-provider-spec-matrix.md` (~6,000 words, 8 Phase B candidates)
- Workstream C — `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/000-docs/002-RR-LAND-mcp-testing-bridge.md` (~6,250 words, 3 Phase B + 2 Phase C candidates)

**Phase A artifacts referenced for sequencing:**

- `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/SPEC.md` (skeleton)
- `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` (RFC draft, PB-10 source)
- `/home/jeremy/000-projects/intent-eval-platform/audit-harness/000-docs/001-DR-DESIGN-evidence-bundle-envelope-design-notes.md` (gate-result envelope, PB-1 + PB-2 + PB-4 source)
- `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/SPEC.md` (Intentional Mapping spec, PB-11 + PB-12 source)
- `/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/intentional-mapping-template.md` (MM-1..MM-6 template, PB-11 + PB-12 + § 7 MM-7 source)

**Master plan (research methodology + Part 2 scope):**

- `/home/jeremy/.claude/plans/please-take-your-time-glimmering-stardust.md` § Part 2 (lines 408-760)

**Plane tracking:**

- LAB-6 (parent — convergence umbrella; Phase B section to be updated by parent agent after review)
- OPS-nfx (meta-bead for Part 2 completion; updated by parent agent)

---

*Synthesis authored 2026-05-10 by Jeremy Longshore. The four synthesis lenses are user-provided enhancements over the original Part 2 plan; they thread through every Phase B item annotation.*

— Jeremy Longshore
intentsolutions.io
