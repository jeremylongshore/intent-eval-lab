---
title: Canonical Glossary — Intent Eval Platform
date: 2026-05-14
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
binding_authority: ISEDC Session 4 (DR-010, 2026-05-13)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E03
bead: bd_000-projects-471
filing_standard: Document Filing Standard v4.3
related_docs:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — names the load-bearing terms)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — 13-entity domain model + signing terms)
  - 010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md (DR-010 — governance terms)
  - 004-AT-DECR-isedc-council-record-2026-05-10.md (DR-004 — Intentional Mapping + provider PASS/FAIL terms)
  - 005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md (DR-005 — matcher-map → Intentional Mapping rename)
forward_refs:
  - 013-AT-SPEC-repo-blueprint-template.md (Blueprint C template — iel-E04)
  - 016-AT-STND-replay-fidelity-levels.md (iel-E11 — RF-N levels)
  - 020-AT-ARCH-runtime-event-taxonomy.md (iel-E12 — canonical OTel events)
---

# Canonical Glossary — Intent Eval Platform

## 1. Purpose + How to read

This document is the **single source of truth for every platform-grade term used across the Intent Eval Platform ecosystem**. If a term appears in any normative document — Blueprint A (`011-AT-ARCH`), Blueprint B (`012-AT-ARCH`), Blueprint C (forthcoming as `013-AT-SPEC`), per-repo blueprints, or any Decision Record under `NNN-AT-DECR-...` — its canonical definition lives here. Other documents **MUST** cross-reference this glossary rather than redefine. When a downstream definition appears to diverge from this glossary, the glossary wins until the conflict is resolved through a Decision Record per Blueprint A § 2.3 governance routing.

This is itself a **NORMATIVE** document binding on the ecosystem under DR-010 § 7 Q3 unification thesis. Amendments are Class-1 routing (full ISEDC convening) when they alter the meaning of a load-bearing term used in immutable artifacts (predicate URIs, attestation envelopes, in-toto Subject names, signed Decision Records). Lower-impact edits — adding cross-references, fixing prose clarity, adding an entry that does not change any existing one — are Class-2 routing (CTO + VP DevRel pair Decision Record). Bug-fix typo corrections are Class-3 (one-line entry in `SOLO-DECISIONS.md`).

**Reading guide:**

- **§ 2 — The 13 canonical entities.** Entity-level concepts from the canonical domain model. One paragraph each; the full 10-attribute schema for each entity lives in Blueprint B § 2.
- **§ 3 — Operational terms.** The verbs and execution-level nouns: matcher, mapping, routing, intent resolution, replay, eval, harness, trace, receipt, gate, judge.
- **§ 4 — Intentional Mapping vocabulary (MM-1..MM-6).** The canonical failure-shape vocabulary from DR-005 (rename) anchored to DR-004 (binding). MM-7+ deferred per DR-004 S1Q3 community-contribution path.
- **§ 5 — Governance + lifecycle terms.** ISEDC, three-class routing, Decision Records, override, ratification.
- **§ 6 — Signing + attestation terms.** in-toto Statement v1, DSSE, cosign, Rekor, predicate URI, subject naming, DNSSEC + CAA.
- **§ 7 — Sequence + lifecycle terms.** Phase A/B/C, RF-N (forward-ref to iel-E11), sigstore staging vs production Rekor, EXPERIMENTAL mode, `bd-sync`.
- **§ 8 — Anti-patterns + reserved terms.** Reservations and disciplines that cannot be silently violated: `labs.intentsolutions.io` reserved-don't-touch, vendor-generic discipline, external-pattern non-borrow, approximate reproducibility, bd auto-flush JSONL drift.
- **§ 9 — Alphabetical cross-reference index.** Alphabetical pointer from each term to its primary section here and to the 2-4 most relevant documents that use it.

When in doubt about which section a term belongs in, prefer the section that captures the term's **canonical use site**. A term that appears across multiple sections (e.g., "Evidence Bundle" — an entity in § 2, but also the lingua franca cited by signing terms in § 6) lives in its primary section with cross-references from the others.

---

## 2. The 13 canonical entities

The canonical domain model is the 13-entity directed-acyclic reference graph defined in Blueprint B § 2. Each entity below carries a one-paragraph definition for glossary purposes; the **complete 10-attribute schema** (Purpose · Required fields · UUID strategy · Mutability rules · Retention policy · Replayability guarantees · Provenance requirements · Lifecycle states · Storage recommendations · Audit requirements) lives in Blueprint B § 2.N for each entity N. Cross-references in any normative doc that need the full schema **MUST** link to Blueprint B § 2.N — not redefine the schema here.

The order below matches Blueprint B's dependency order. A downstream entity may reference an upstream entity; never the reverse. Reference data (EvalSpec, MatcherMap, SkillSnapshot, FailureTaxonomy) never depends on a runtime entity.

### 2.1 EvalSpec

The declarative input that drives every evaluation. An EvalSpec defines the rules: which matchers run, which assertions hold, how outputs are scored, how the run composes into a multi-step DAG, and which `SkillSnapshot` SHA the spec targets. EvalSpecs are versioned, content-addressed, and treated as first-class artifacts — not configuration. They are mutable while `draft` and immutable once `published`. A revision is a new row with an incremented `version`, never an in-place edit.

- **See Blueprint B § 2.1** for the full attribute schema.
- **Common cross-references:** `EvalRun` (the execution instance of an EvalSpec); `MatcherMap` (composed into the spec's assertion logic); `SkillSnapshot` (the spec declares the target snapshot SHA); `RegressionPack` (packs reference the EvalSpec content_hash to detect mid-flight spec mutation).

### 2.2 EvalRun

A single execution instance of an `EvalSpec` against a specific `SkillSnapshot`. The EvalRun is the unit of work in the runtime. Everything observable about a run — its inputs, its lineage, its outputs, its judge decisions, its evidence, its cost — hangs off the EvalRun row. It is the anchor of the lineage graph: an auditor reading an EvalRun row knows which downstream artifacts (`SessionTrace`, `EvidenceBundle`, `CostRecord`, `RuntimeReceipt`) to fetch to complete the audit picture.

- **See Blueprint B § 2.2** for the full attribute schema and the `queued → running → judged → reported → archived` lifecycle.
- **Common cross-references:** `EvalSpec` (input), `SkillSnapshot` (subject), `SessionTrace` (execution lineage), `EvidenceBundle` (terminal evidence), `RuntimeReceipt` (terminal execution proof), `CostRecord` (cost attribution).

### 2.3 MatcherMap

The data structure carrying the **Intentional Mapping** vocabulary (renamed from "matcher-map" per DR-005, with MM-N category codes preserved per DR-005 Q2). A MatcherMap declares "for inputs that look like X, the expected behavior is Y" — the EvalSpec composes MatcherMaps into the assertion logic that judges evaluate. Each row's `mm_class` field categorizes it into MM-1..MM-6 (§ 4 below); multiple MatcherMap rows may share the same `mm_class` (many different MM-3 cooldown matchers, for example).

- **See Blueprint B § 2.3** for the full attribute schema.
- **Common cross-references:** § 4 of this glossary for the canonical MM-1..MM-6 definitions; `EvalSpec` (composes MatcherMaps into assertions); `JudgeDecision` (references the MatcherMap whose expected behavior was being evaluated); `FailureTaxonomy` (every `FAIL` JudgeDecision classifies against an MM class).

### 2.4 EvidenceBundle

The **lingua franca of the platform** (DR-010 § 7 Q3 unification thesis). An EvidenceBundle is an immutable, append-only collection of in-toto Statement v1 rows wrapped in DSSE envelopes for signing, attesting to the outcomes of an `EvalRun` (or a logical subset). Every validator, gate, judge, and runtime in the ecosystem emits Evidence Bundle rows as architectural primitive. Production-signed bundles anchor to Rekor; experimental bundles anchor to sigstore staging. Bundles are never amended in place — corrections happen by emitting a new bundle that references the prior content_hash and includes a correcting row.

- **See Blueprint B § 2.4** for the full attribute schema; **see Blueprint B § 7** for the normative `gate-result/v1` predicate body.
- **Common cross-references:** `EvalRun` (parent), `JudgeDecision` (a row type carried inside the bundle), `RuntimeReceipt` (a row type carried inside), `RolloutGate` (consumer), § 6 of this glossary for signing terminology.

### 2.5 JudgeDecision

A single judge's verdict on a single matching event during an EvalRun. A judge is either a deterministic validator (an audit-harness static gate that returns PASS or FAIL mechanically) or an LLM-as-judge (probabilistic verdict with confidence). The JudgeDecision row preserves the verdict, the input hash the judge saw, the judge's identity and version, the confidence (if applicable), and any free-form reasoning. JudgeDecisions are immutable at creation; a follow-up second opinion is a new row, not a mutation.

- **See Blueprint B § 2.5** for the full attribute schema.
- **Common cross-references:** `MatcherMap` (the matcher whose expected behavior was being evaluated); `EvalRun` (parent); `SessionTrace` (locates the decision in the execution DAG); `EvidenceBundle` (the bundle carries the JudgeDecision row); `FailureTaxonomy` (every `FAIL` verdict classifies against an MM class).

### 2.6 RuntimeReceipt

Execution proof — the platform's "what actually ran" record. A RuntimeReceipt captures the frozen versions of every input that mattered to a terminal `EvalRun`: the EvalSpec content_hash, the SkillSnapshot SHA, the provider adapter versions, the tool versions, the runtime limits in effect, the actual resource usage, the worker identity, and the worker host fingerprint. Receipts are emitted at every EvalRun terminal-state transition and are themselves signed and attested. The receipt is the **integrity anchor** for the run's execution claims and the **input to replay verification**.

- **See Blueprint B § 2.6** for the full attribute schema.
- **Common cross-references:** `EvalRun` (parent — 1:1 cardinality with terminal-state transitions); `EvidenceBundle` (the bundle carries the receipt row); `SkillSnapshot` (the receipt freezes the snapshot SHA); `CostRecord` (the receipt summarizes actual resource usage).

### 2.7 RegressionPack

A frozen historical benchmark capturing a specific set of EvalRun outcomes against a specific SkillSnapshot at a specific moment for a specific reason. Once committed, a RegressionPack is **immutable**. New regression evidence becomes a new pack referencing its ancestor — analogous to git commits over file edits. This is what makes one-variable-change discipline (Blueprint A § 1.2 principle 6) detectable: comparing pack N to pack N+1 reveals exactly which variable changed and what outcomes shifted.

- **See Blueprint B § 2.7** for the full attribute schema.
- **Common cross-references:** `SkillSnapshot` (the pack's subject); `EvalSpec` (the pack includes references to the specs run); `EvalRun` (the pack includes the run IDs frozen into it); ancestor `RegressionPack` (lineage chain).

### 2.8 RolloutGate

The promotion decision engine. A RolloutGate consumes an `EvidenceBundle` and a `tests/TESTING.md`-shaped policy and emits a ship / no-ship / advisory verdict. The RolloutGate is the platform's **user-facing surface** — the thing engineers actually run as a CI gate. The decision LOGIC lives in `@j-rig/rollout-gate` (the workspace package inside `j-rig-skill-binary-eval`); the GitHub Action SHELL that calls into the logic lives in `intent-rollout-gate` (per Blueprint A § 2.1). Every gate decision is emitted as an in-toto Statement v1 row under the `gate-result/v1` predicate URI — the **first predicate URI with SPEC.md normative content landing**, which is what unlocks production-Rekor signing for this predicate.

- **See Blueprint B § 2.8** for the full attribute schema; **see Blueprint B § 7** for the `gate-result/v1` predicate body.
- **Common cross-references:** `EvidenceBundle` (input); `EvalRun` (the run whose bundle was consumed); § 6 of this glossary for signing terminology; § 4 of this glossary for the MM vocabulary the policy file expresses.

### 2.9 SkillSnapshot

An immutable SHA-pinned skill version. A SkillSnapshot is the freeze of a skill's source tarball, its dependency lock, and its configuration at a specific moment. Production references to a skill go through a SkillSnapshot — never to mutable `main`. Rollback is "switch the pin back" (Blueprint A § 1.2 principle 4); rolling forward through a passing RolloutGate produces a new SkillSnapshot, never an in-place edit. The load-bearing identifier in practice is the `combined_sha` derived from `source_sha || dependency_lock_sha || config_sha`.

- **See Blueprint B § 2.9** for the full attribute schema.
- **Common cross-references:** `EvalRun` (the run's subject); `EvalSpec` (declares the target SHA); `RegressionPack` (frozen against a snapshot SHA); `RuntimeReceipt` (records the snapshot SHA that actually ran).

### 2.10 SessionTrace

Execution lineage. A SessionTrace is the directed-acyclic graph of `ToolInvocation` events, retries, `JudgeDecision` events, and gate evaluations that occurred during the lifetime of a single `EvalRun`. The trace is the platform's surface for replay visualization, disagreement analysis, loop-depth monitoring, and forensic reconstruction. Traces are mutable while the parent EvalRun is in non-terminal state (spans append as execution progresses) and frozen at terminal state, at which point the trace blob is content-addressed and immutable.

- **See Blueprint B § 2.10** for the full attribute schema.
- **Common cross-references:** `EvalRun` (parent — 1:1 cardinality); `ToolInvocation` (leaves of the DAG); `JudgeDecision` (located in the DAG by `parent_span_id`); OpenTelemetry span trees (the trace mirrors the OTel span structure).

### 2.11 ToolInvocation

Tool-level execution record. Every time the runtime invokes a tool — an `audit-harness` subcommand, a `j-rig` judge, a provider API call, an internal validator — a ToolInvocation row records the invocation. Tool invocations are the **leaves** of the SessionTrace DAG. They are immutable at creation; retries are NEW ToolInvocation rows with incremented `retry_attempt`, not mutations. Credential redaction is enforced before persistence: a row containing a credential-shaped string in `args` or `result_summary` causes the runtime to reject persistence and fail the parent EvalRun.

- **See Blueprint B § 2.11** for the full attribute schema.
- **Common cross-references:** `SessionTrace` (parent DAG); `CostRecord` (cost attribution per invocation); `JudgeDecision` (a judge invocation is one species of ToolInvocation); the credential-redaction PASS/FAIL gate from DR-004 S1Q5 + DR-010 § 7 Q5.

### 2.12 CostRecord

Cost attribution along several dimensions: per EvalRun, per provider, per judge, per replay, per cache decision, per user, per day. Cost records are the input to budget enforcement (Blueprint B § 4.2), per-feature cost analysis, and the optimizer's bandwidth-vs-quality tradeoff surfaces. They are immutable at creation; rollups (per-day, per-user, per-provider aggregates) are separate rows, not mutations of leaf rows. Cost records carry `cost_basis_version` so a replay can declare the original cost basis vs the replay-time basis — useful when provider pricing has changed since the original run.

- **See Blueprint B § 2.12** for the full attribute schema.
- **Common cross-references:** `EvalRun` (run-level attribution), `ToolInvocation` (leaf-level attribution), `RuntimeReceipt` (the receipt summarizes the run's total cost), provider-adapter declarations (cost-basis lookup).

### 2.13 FailureTaxonomy

Canonical failure-shape registry. The FailureTaxonomy table holds the MM-1..MM-6 Intentional Mapping vocabulary as the v1 enumeration, with the explicit extension path documented in `intent-eval-lab/specs/CONTRIBUTING-failure-shape.md` per DR-004 S1Q3 (MM-7+ via community contribution path; reaffirmed at DR-010). The registry is **reference data** — every JudgeDecision's `verdict=FAIL` MUST classify against an entry. Drift (a JudgeDecision referencing an `mm_class` that does not exist in the registry) is a system-integrity violation surfaced via the `taxonomy.drift.detected` OTel event.

- **See Blueprint B § 2.13** for the full attribute schema.
- **Common cross-references:** § 4 of this glossary for the canonical MM-1..MM-6 definitions; `JudgeDecision` (every FAIL verdict references an MM class); `MatcherMap` (also categorized by `mm_class`); `CONTRIBUTING-failure-shape.md` (the MM-7+ extension path).

---

## 3. Operational terms

These are the verbs and execution-level nouns the platform's documentation uses constantly. They are not entities — they are concepts, actions, or roles that the entities participate in.

**matcher.** The function or predicate that compares an actual output produced during execution against an expected pattern declared in a `MatcherMap`. A matcher is a piece of evaluative logic; the MatcherMap row is the data structure that carries the matcher's declaration. A matcher executes as part of a `JudgeDecision`. Citation: Blueprint B § 2.3 + § 2.5.

**mapping.** A single input-pattern → expected-behavior pair. Each row in a `MatcherMap` is a mapping. "Mappings" in the plural usually refers to the set of MatcherMap rows that a given `EvalSpec` composes into its assertion logic. Citation: Blueprint B § 2.3.

**routing.** The act of dispatching a decision request to Class-1 / Class-2 / Class-3 governance per DR-010 § 7 Q6 (also Blueprint A § 2.3). Routing is a governance verb, not a runtime verb. Each class produces a different artifact (full Decision Record, pair Decision Record, one-line SOLO-DECISIONS entry). Citation: DR-010 § 7 Q6; Blueprint A § 2.3.

**intent resolution.** The act of mapping a user-stated intent (e.g., "evaluate this skill against the production policy") to a concrete `SkillSnapshot` + `EvalSpec` pairing the runtime can execute. Intent resolution is a workflow surface, not an entity surface — it produces an EvalRun submission, but is not itself recorded as a row. In v0.1, intent resolution is manual (engineers select the snapshot and spec); in v0.2+ it may be partially automated through the optimizer surface. Citation: Blueprint B § 1.2 (queued state); DR-005 (the "Intent Resolution Layer" concept was decision-locked OUT of scope at Session 2 per S2Q4 user override — "nothing changes but the name").

**replay.** Deterministic re-execution of a frozen `EvalRun` against the same `SkillSnapshot` + frozen environment + frozen seeds, intended to reproduce the original verdict. Replay's fidelity is enumerated by **RF-N** levels declared per predicate type in their respective SPEC.md normative sections (forward-ref iel-E11). Replay is the platform's primary surface for verifying audit claims and for detecting drift between recorded evidence and current behavior. Citation: Blueprint A § 1.2 principle 2; Blueprint B § 3.2.

**eval.** Short for "evaluation." In running prose, "an eval" refers to an `EvalRun` against an `EvalSpec`. The toolname `j-rig eval` is the canonical CLI verb for submitting an EvalRun. The plural "evals" or the compound noun "eval suite" usually refers to a collection of EvalSpecs run together. Citation: Blueprint A § 1.1.

**harness.** An execution wrapper. The ecosystem hosts three harnesses by canonical naming: `audit-harness` (deterministic gates, polyglot, emits `gate-result/v1` rows), `j-rig` (behavioral evaluation, TypeScript, emits + consumes Evidence Bundle rows including `eval-verdict/v1` and `runtime-receipt/v1`), and `intent-rollout-gate` (thin GitHub Action shell that delegates to `@j-rig/rollout-gate` for the decision logic). When prose says "the harness" without qualification, context determines which one — usually `audit-harness` for static gates and `j-rig` for behavioral eval. Citation: Blueprint A § 2.1.

**trace.** An OpenTelemetry span tree mirroring the `SessionTrace` lineage DAG. The trace is the OTel-emission representation; the SessionTrace is the persisted-row representation. They are two views of the same lineage. The OTel taxonomy for the platform's traces is locked in the iel-E12 RFC (`agent.rollout.gate.*` for gate execution, `agent.evidence_bundle.*` for bundle emission, plus the standard OTel GenAI semantic conventions). Citation: Blueprint A § 4.2 observability requirements; iel-E12 (forward-ref).

**receipt.** A `RuntimeReceipt` (§ 2.6). The full noun; "the receipt" in prose almost always means the RuntimeReceipt associated with an EvalRun's terminal-state transition. Citation: Blueprint B § 2.6.

**gate.** A deterministic check function that emits a `gate-result/v1` predicate row. Gates are the bread-and-butter of `audit-harness` (escape-scan, CRAP, architecture, harness-hash, bias-count, gherkin-lint, etc.) and are also emitted by the user-facing `RolloutGate` (the promotion decision engine). The verdict grammar is `PASS` / `FAIL` / `ADVISORY` (advisory = informational, does not block). Citation: Blueprint A § 1.2 principle 10; Blueprint B § 7.

**judge.** An LLM-as-judge or deterministic-validator function that emits a `JudgeDecision`. Judges that are deterministic produce verdicts mechanically; LLM-judges produce verdicts probabilistically with a confidence and (usually) a seed. The `verdict_source` field on a JudgeDecision declares which kind — `deterministic`, `llm_with_seed`, `llm_no_seed`, or `hybrid`. The platform discourages `llm_no_seed` because it cannot be replayed beyond statistical reconstruction. Citation: Blueprint B § 2.5.

---

## 4. Intentional Mapping vocabulary (MM-1..MM-6)

The Intentional Mapping vocabulary is the canonical **failure-shape framework** of the Intent Eval Platform. Per DR-005, the methodology is named "Intentional Mapping" (proper-noun cased in spec text; lowercase "intentional mapping" in prose); the **identifier codes MM-1..MM-6 are immutable** per DR-005 Q2 (citation-stability binding — "the #1 OSS-trust violation is renaming identifiers under developers' feet"). MM-7+ is **DEFERRED** per DR-004 S1Q3: admission criteria require ≥2 independent engagements demonstrating the shape, the shape must not type-fit into MM-1..MM-6, and the proposal must include OTel signal vocabulary. Community contributions toward MM-7+ flow through `intent-eval-lab/specs/CONTRIBUTING-failure-shape.md`.

The six canonical categories below are vendor-neutral by construction — they describe **shapes** of failure mode, not bugs in any specific plugin or partner.

### MM-1 — Async write success / stale-read failure

An asynchronous write operation returns success, but a read-after-write observes stale state. The failure shape is a race condition between async completion and the downstream read that depends on the write's effect being visible. The discriminating question: *"did the write's success-return outpace the visibility of the effect on the read side?"* Observable from OTel trace context propagated through the asynchronous boundary (Dapper-style). Citation: DR-004 + DR-005 + Blueprint B § 2.3; `002-RR-LAND-mcp-testing-bridge.md` § 4 for the empirical landscape.

### MM-2 — Response-shape drift across consecutive calls

The read-side response shape drifts across consecutive calls — list-shape vs detail-shape inconsistency, paginated drift, schema variance between calls that should return structurally identical payloads. The discriminating question: *"do two adjacent calls to the same logical endpoint return payloads whose shape differs in a way the caller's parser cannot accommodate?"* Observable on `tool_result` events via response payload structural comparison. Citation: DR-004 + DR-005 + Blueprint B § 2.3.

### MM-3 — Cooldown / debounce window required

The operation requires a cooldown or debouncing window before the next equivalent operation. Rate-limiting, debounce, anti-flood. The discriminating question: *"does the protocol require a minimum interval between equivalent calls that the model's default invocation pattern does not honor?"* Observable as the protocol-emitted `decision: block` signal followed by a retry attempt within the cooldown window. Citation: DR-004 + DR-005 + Blueprint B § 2.3.

### MM-4 — Side-effect verification before reliance

The operation requires verification of side-effect completion before downstream reliance is safe. Poll-until-verified, propagation-aware waits, happens-before discipline. The discriminating question: *"did the caller proceed to a dependent operation before confirming the upstream side-effect was actually visible at the relying surface?"* Observable as the missing-confirmation span in the trace DAG (the dependent tool fired before the verification tool returned). Citation: DR-004 + DR-005 + Blueprint B § 2.3.

### MM-5 — Tool inputs need mandatory context

The tool requires mandatory context that the model is not reliably providing — caller identity, intent string, policy tag injection. The discriminating question: *"is the tool signature requiring a context field the model is omitting or filling with a placeholder?"* Observable on `tool_input` events by checking the presence and shape of the required context field against the tool's declared input schema. Citation: DR-004 + DR-005 + Blueprint B § 2.3.

### MM-6 — Strict-mode protocol compliance

The server-side endpoint requires strict-mode protocol compliance that the model's default input does not enforce — W3C-strict / RFC-strict payload reformatting, schema-tight validation. The discriminating question: *"is the server returning a protocol-conformance error against an input the model considered well-formed?"* Observable on the `tool_result` error class — a `400 schema-violation`-class response against an input that lint at the looser tier accepted. Citation: DR-004 + DR-005 + Blueprint B § 2.3.

### MM-7 — DEFERRED

MM-7 admission is gated. Per DR-004 S1Q3 binding (reaffirmed at DR-010 § 10 reopened-bindings register), the admission criteria are: (1) ≥2 independent engagements have demonstrated the shape as a recurring failure mode, (2) the shape does not type-fit into any existing MM-1..MM-6 category, and (3) the proposal carries explicit OpenTelemetry signal vocabulary so the harness can detect it. Until those three conditions are met, MM-7+ remains in the `proposed` lifecycle state of the `FailureTaxonomy` registry. The community contribution path is documented in `intent-eval-lab/specs/CONTRIBUTING-failure-shape.md`. Citation: DR-004 S1Q3; DR-010 § 10.

---

## 5. Governance + lifecycle terms

**ISEDC.** The **Intent Solutions Executive Decision Council** — a 7-seat adversarial council pattern (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel) used to adjudicate strategic architectural decisions for Intent Solutions. Verbatim seat positions are preserved in every Decision Record per the ISEDC adversarial-integrity protocol — dissent is preserved, not suppressed. The reusable skill lives at `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0 and is invoked via `/exec-decision-council`. Citation: Blueprint A § 1.2 principle 12; the canonical session-4 decision record (DR-010).

**Acting head of board.** Jeremy Longshore (Intent Solutions). Final-call authority over ISEDC outcomes per the ISEDC pattern — when the acting head of board reverses a council position, the reversal is recorded **inline** with the original position so future readers reconstruct the audit trail. The two canonical reversals in DR-010 are documented at § 13.5 (customer-signal gate removed) and § 13.6 (external-pattern non-borrow). Citation: DR-010 § 13.5 + § 13.6.

**Class 1 routing.** Decisions producing immutable artifacts or commitments require **full ISEDC convening (7 seats)**. The trigger list per DR-010 § 7 Q6: new predicate URI subtype reservation; DNS zone change at any predicate-URI subdomain; new Fulcio identity issuance or signing key custody change; DSSE attestation envelope schema change; new brand commitment with public surface; new partner-engagement public reference (the vendor-generic case-study scrub binding stays in force); standards-body submission (OTel SIG-GenAI, in-toto, SLSA, CNCF, OpenSSF); new sub-platform initiation; language-lock changes. **Artifact:** full Decision Record (`NNN-AT-DECR-<title>-<date>.md`) per Document Filing Standard v4.3, with verbatim seat positions preserved. **Public archive within 7 days** of decision-lock on the `intent-eval-lab` main branch (VPDevRel non-negotiable floor). Citation: Blueprint A § 2.3; DR-010 § 7 Q6.

**Class 2 routing.** Operational decisions handled by **CTO + VP DevRel pair (2 seats)**: tooling choices, per-component release timing, CI workflow changes, validator additions or version bumps (when no new emitted-attestation surface is introduced), Saturday-afternoon-dev friction-reduction passes, tooling internal architecture below the predicate-URI line. **Artifact:** short pair Decision Record (`NNN-AT-DECR-pair-<title>-<date>.md`). Public archive within 7 days same as Class 1. Citation: Blueprint A § 2.3; DR-010 § 7 Q6.

**Class 3 routing.** Code-level decisions inside an existing sub-component's scope handled by the **solo maintainer (acting head of board)**: bug fixes, documentation polish, library-internal refactors. **Artifact:** one-line entry in `intent-eval-lab/000-docs/SOLO-DECISIONS.md` (append-only). Citation: Blueprint A § 2.3.

**Decision Record (DR).** The formal record of an ISEDC session at Class 1 or Class 2. Filing convention: `NNN-AT-DECR-<title>-<date>.md` (Document Filing Standard v4.3, category code `AT-DECR`). The record preserves the question asked, every seat's vote, every seat's verbatim position, the primary tensions, the council memos, the final vote tally, and any acting-head-of-board override declarations. Public DRs land on the `intent-eval-lab` main branch within 7 days per the VPDevRel binding (DR-010 § 7 Q6). Citation: Blueprint A § 2.3; ISEDC skill at `~/.claude/skills/exec-decision-council/SKILL.md`.

**Override.** The acting-head-of-board reversal of a council position. Overrides are recorded **inline** with the original council position so the audit trail is preserved — never silently. The two canonical override sections in DR-010 are § 13.5 (Q5 customer-signal-gate override: customer-signal-gate language removed; bandwidth-only gate retained; marketing-customer framing removed; internal-tool-shared-with-the-world framing applied) and § 13.6 (Q4 external-pattern-non-borrow override: forward-deployed work proceeds from first principles, no "informed by" / "inspired by" footers). Citation: DR-010 § 13.5 + § 13.6.

**Ratification.** A subsequent ISEDC session that reaffirms or revises an earlier decision. DR-010 § 10 ratifies the five DR-004 bindings (predicate URI namespace, vendor-generic case-study scrub, MM-7 defer + CONTRIBUTING-failure-shape path, OTel CSO informal-email-first sequence, provider PASS/FAIL gates) by listing them in the reopened-bindings register with explicit "REAFFIRMED" status. A binding may also be **lifted** at ratification — DR-006's Phase B gate was subsequently lifted by user override at the Session 4 mandate framing. Citation: DR-010 § 10.

---

## 6. Signing + attestation terms

**in-toto Statement v1.** The wrapping structure for signed software-supply-chain attestations. Defined at `https://in-toto.io/Statement/v1`, the Statement carries four fields: `_type` (always `https://in-toto.io/Statement/v1`), `predicateType` (a URI identifying the predicate's type — see "predicate URI" below), `subject` (an array of `{name, digest: {sha256: "..."}}` entries identifying the artifacts the predicate attests over), and `predicate` (an object whose schema is defined by the predicate type). Every Evidence Bundle row in the Intent Eval Platform is an in-toto Statement v1. Citation: Blueprint A § 1.2 principle 3 + § 4.2; Blueprint B § 7.1.

**DSSE.** **Dead Simple Signing Envelope** — the signing envelope around in-toto Statements, defined at `https://github.com/secure-systems-lab/dsse`. DSSE wraps the Statement payload as `payloadType: "application/vnd.in-toto+json"` and carries one or more signatures over the canonicalized payload. The platform signs every Evidence Bundle row's Statement under DSSE. Citation: Blueprint A § 4.2 evidence retention; Blueprint B § 7.5.

**cosign.** The signing CLI from the sigstore project (`https://sigstore.dev`). The platform uses **cosign keyless** mode via OIDC for production signing: the signing identity is the OIDC subject + issuer that Fulcio mints a short-lived certificate for. Cosign also anchors the signed envelope to Rekor by default. The platform's CI workflows invoke cosign with `--oidc-provider=github-actions` when signing from GitHub-hosted runners. Citation: Blueprint A § 4.2; Blueprint B § 7.5.

**Rekor.** The sigstore **immutable transparency log** (`https://rekor.sigstore.dev`). Once an entry is anchored to production Rekor, the entry is permanent and globally verifiable. **There is no delete** — this is the fundamental property the platform relies on for audit-grade evidence. Verification is performed via `cosign verify-attestation --rekor-url`. Citation: Blueprint A § 4.2 evidence retention.

**Predicate URI.** The typed identifier for a class of Evidence Bundle row. Canonical grammar per DR-004 Q1 + DR-010 § 7 Q3: `evals.intentsolutions.io/<predicate-type>/v<version>`. The predicate URI is the value of the in-toto Statement v1 `predicateType` field. Predicate URIs are **effectively immutable once signed into Rekor** — the signed Statement carrying a given URI cannot be retracted from the transparency log, so the URI's meaning is fixed at first signing. Citation: DR-004 Q1; DR-010 § 7 Q3 grammar lock.

**Subject naming.** The convention for naming the artifact a predicate attests over. The platform uses content-addressed subject naming: `<fqdn>/<artifact-path>@sha256:<digest>` style. The `name` field carries the fully-qualified path; the `digest.sha256` field carries the digest. For an EvidenceBundle attesting a `gate-result/v1` against a SkillSnapshot, the subject is the SkillSnapshot's `combined_sha`. Citation: Blueprint B § 7.3.

**Reserved-don't-touch (predicate URIs).** The subdomain `labs.intentsolutions.io` is **permanently reserved-don't-touch** for predicate URIs per the DR-004 CISO binding (reaffirmed at DR-010 § 10). Predicate URIs only live at `evals.intentsolutions.io`. The `labs.` subdomain may host blog content, methodology landing pages, RFC published-version pages, or Phase-C content surfaces — but **never** an in-toto predicate URI, OTel attribute namespace, or attestation predicate identifier. The rationale is DNS / brand-surface isolation: once the first in-toto Statement is signed referencing an `evals.` URI, that namespace is permanent in Rekor, and the `labs.` namespace must stay clear of attestation surface to preserve isolation. Citation: DR-004 Q1; DR-010 § 10; Blueprint A § 4.2 naming standards.

**Active predicate types (Phase A approved).** `gate-result/v1` — the **first predicate URI** with SPEC.md normative content landing. Production-Rekor signing is unlocked for `gate-result/v1` as soon as Blueprint B (which carries the normative § 7) merges. Citation: Blueprint B § 7; DR-004 Q1.

**Phase A-conditional predicate types (per DR-010 Q3).** `validation-result/v1`, `eval-verdict/v1`, `cost-attribution/v1` are **conditionally approved** — they enter the predicate URI namespace as legitimate types but production-Rekor signing for each is gated on that predicate's SPEC.md normative section landing first. Until then, attestations carrying these URIs run in `sigstore_staging` mode. Citation: DR-010 § 7 Q3.

**Deferred predicate types (Phase B+).** `harness-experiment/v1` and `cache-decision/v1` are deferred for future Phase B+ admission. Their use cases are recognized but not yet ready for namespace reservation. Citation: DR-010 § 7 Q3.

**Rejected predicate types.** `agent-loop-trace/v1` is **REJECTED for v1** per DR-010 Q3 CISO veto, pending a sanitization specification. The rejection rationale: agent-loop traces carry credential-shaped substrings and tool-output payloads whose redaction discipline is not yet specified — admitting the predicate URI before the sanitization spec lands risks a credential leak into Rekor. Citation: DR-010 § 7 Q3 CISO veto.

**DNSSEC + CAA.** DNS-layer cryptographic hardening required **before any production-Rekor anchor** per DR-004 Q1 + DR-010 § 7 Q5 CISO non-negotiable. DNSSEC signs the DNS zone responses for `evals.intentsolutions.io` and any subdomain hosting predicate URIs; CAA (Certification Authority Authorization) records pin which CAs may issue certificates for those names. Both are pre-requisites because predicate URIs that resolve through an un-hardened DNS path are vulnerable to namespace-hijacking attacks that produce signed-but-attacker-controlled attestations. Citation: DR-004 Q1; DR-010 § 7 Q5.

---

## 7. Sequence + lifecycle terms

**Phase A — Foundations.** The phase that lands the platform's substrate: SPEC.md normative content for the first predicate types, the JSON Schema definitions in `intent-eval-core`, DNSSEC + CAA hardening on `evals.intentsolutions.io`, and the first sigstore-staging signed attestations. Production-Rekor signing remains gated until each predicate's SPEC.md normative section lands. The current ecosystem state at the date of this document is **Phase A in progress**. Citation: DR-010 § 7 Q5; Blueprint A § 4.2.

**Phase B — Build-out.** The phase that retrofits the existing tooling against the unification thesis, lands new predicate types (e.g., `validation-result/v1`, `eval-verdict/v1`, `cost-attribution/v1` per the Phase A-conditional list), and lands the provider PASS/FAIL gates (credential redaction + env-var spillover, per DR-004 S1Q5). **Bandwidth-gated** per DR-010 § 13.5 override — the customer-signal gate was removed by acting-head-of-board override at Session 4; the bandwidth-only gate (3-5 hrs/wk solo-maintainer CFO budget) remains. Phase B can begin in parallel with Phase A close-out work where the work surface does not collide. Citation: DR-010 § 13.5.

**Phase C — Steady-state.** The phase that runs the platform at a sustainable cadence: governance scaling per the Class 1 / Class 2 / Class 3 routing, quarterly standing ISEDC convenings, annual full-review of all active bindings, public Decision Record archive within 7 days of decision-lock. Phase C carries the platform's long-arc reliability work: replay-fidelity test-suite continuous-run, regression-pack curation, partner case-study writeups when written consent lands. **Solo-maintainer for the foreseeable future** per DR-010 § 7 Q5 + § 13.5. Citation: Blueprint A § 2.3 cadence + standing.

**Replay Fidelity N (RF-N).** The 5-level replay-determinism scale that enumerates how exactly a replay reproduces an original execution. The complete normative definition of RF-0..RF-4 is **forward-deferred to iel-E11** (`016-AT-STND-replay-fidelity-levels.md`, forthcoming). Until iel-E11 lands, downstream documentation MUST refer to RF levels by name without redefining them. The two levels named in Blueprint A § 4.2 for orientation: **RF-strict** (re-execution reproduces bitwise from captured evidence + seed) and **RF-best-effort** (re-execution reproduces semantically with documented sources of non-determinism). Citation: Blueprint A § 4.2 replay requirements; iel-E11 (forward-ref).

**sigstore staging.** The sigstore **testing Rekor** at `rekor.sigstage.dev`. Signed entries here are **not** considered permanent and do **not** bind operationally — they exist for development, integration testing, and CI dry-runs. The platform runs in `sigstore_staging` mode for any release at `v0.x` where the relevant predicate's SPEC.md normative section has not yet landed. Citation: Blueprint A § 4.2; DR-010 § 7 Q5 CISO non-negotiable.

**Production Rekor.** The sigstore **public transparency log** at `rekor.sigstore.dev`. Entries here are permanent and globally verifiable. Cutover from staging to production Rekor is gated **per-predicate** on the predicate's SPEC.md normative section landing AND DNSSEC + CAA verification on the predicate-URI subdomain. The first predicate cleared for production-Rekor signing is `gate-result/v1`, unlocked when Blueprint B § 7 merges. Citation: DR-010 § 7 Q5.

**EXPERIMENTAL mode.** The operational state for `v0.x` releases where signatures land on sigstore staging only and the predicate URI binding is provisional (replaceable without breaking attestations). EXPERIMENTAL mode is the **default** for any predicate URI whose SPEC.md normative section has not yet landed. Once SPEC.md lands and DNSSEC + CAA are verified, that predicate exits EXPERIMENTAL mode for that release line. Releases that mix EXPERIMENTAL and production predicates declare the per-predicate mode in the release notes. Citation: DR-010 § 7 Q5.

**`bd-sync`.** The three-layer mirror tool (`~/bin/bd-sync`) maintaining bead ↔ GitHub Issue ↔ Plane Issue synchronization. The **canonical source of truth is the bead**; GitHub and Plane issues are mirrored views. Every state change in any layer fans out to the other layers via `bd-sync note` and `bd-sync close`. Drift is detectable and recoverable because every layer carries the IDs of the other two. Citation: `~/000-projects/CLAUDE.md` § "Bead ↔ GitHub Issue ↔ Plane Issue three-layer mirror"; v2.1 epic plan canonical-SoT discipline.

---

## 8. Anti-patterns + reserved terms

This section catalogues disciplines that **cannot be silently violated**. Each entry describes the constraint, the rationale, and the citation that locks it in normatively.

**`labs.intentsolutions.io` reserved-don't-touch.** Permanent reservation per the DR-004 CISO binding (reaffirmed at DR-010 § 10). Predicate URIs live **only** at `evals.intentsolutions.io`. The `labs.` subdomain may host blog content, methodology landing pages, RFC published-version pages, or Phase-C content surfaces — but **never** an in-toto predicate URI, OTel attribute namespace, or attestation predicate identifier. Rationale: DNS / brand-surface isolation. Once the first in-toto Statement is signed referencing an `evals.` URI, that namespace is permanent in Rekor; the `labs.` namespace must stay clear of attestation surface so the operational identity (signing) and the marketing identity (content) cannot collide. Citation: DR-004 Q1; DR-010 § 10; Blueprint A § 4.2.

**Vendor-generic discipline (no partner names in public artifacts).** Partner names are **never** present in public artifacts of any kind — public specs, public READMEs, public Decision Records, public blog drafts, public commit messages. The active grep pattern enforcing this discipline lives in the **PRIVATE** umbrella `~/000-projects/CLAUDE.md` and is not enumerated in this glossary or in any public document (enumerating the pattern in public would, paradoxically, defeat the discipline). Every commit touching public surfaces runs the grep guard; a non-zero result blocks the commit. Re-instantiation with partner names is permitted only after **per-partner written consent** is on file (DR-004 S1Q2, reaffirmed at DR-010 § 10). Public Decision Records that reference a partner engagement must use generic terms like "an enterprise partner engagement" or "the inaugural case study (engagement-private)" until written consent is on file. Citation: DR-004 S1Q2; DR-010 § 10.

**External-pattern non-borrow.** Per DR-010 § 13.6 acting-head-of-board override, the platform does **not** borrow named patterns from external authors into forward-deployed work. Forward-deployed work proceeds from first principles: no "informed by X" / "inspired by Y" / "after Z's pattern" footers in specs, code comments, design docs, READMEs, blog posts, public Decision Records, or RFC text. The platform conforms to **open standards** (in-toto, DSSE, JSON Schema, OpenTelemetry semantic-conventions, SLSA, OpenSSF, UUIDv7 per RFC 9562) — these are standards, not borrowed patterns. The platform depends on **runtime tools** (cosign, sigstore, npm, pnpm) — these are dependencies, not borrowed patterns. **Internal patterns** from prior Intent Solutions work (Evidence Bundle, predicate URIs, MM-1..MM-6 Intentional Mapping vocabulary, the 7-layer testing taxonomy) may be cross-referenced freely. Citation: DR-010 § 13.6; Blueprint A § 4.2.

**Approximate reproducibility (anti-pattern).** Replay in the Intent Eval Platform is **audit-grade deterministic**, not approximately reproducible. A replay produces the same verdict as the original at the RF level declared by the originating predicate, or it produces a replay-failed verdict — there is no "close enough" zone. Documentation that hedges replay claims with phrases like "approximately reproducible," "broadly deterministic," or "reproducible in most cases" is reframing the discipline downward. The correct framing is RF-N: state the RF level explicitly, and if the predicate's RF level is RF-best-effort, document the sources of non-determinism explicitly. Citation: Blueprint A § 1.2 principle 2; Blueprint B § 3.2.

**bd auto-flush JSONL drift.** Operational anti-pattern observed during the v2.1 epic plan execution. `bd`'s auto-export step fails on `git-add` when `.beads/` is gitignored, silently losing in-memory writes between sessions. The workaround is the `bd export → cp → bd import` cycle, applied atomically when state changes need to be persisted across the auto-flush boundary. The underlying bug is tracked in `bd_000-projects-ufc`. Until the fix lands upstream, any session that mutates bead state (note, close, status change) MUST run the export-cp-import workaround before session-end. Citation: v2.1 epic plan canonical-SoT discipline; `bd_000-projects-ufc`.

**No new platform initiation in next 6 months.** Per DR-010 Q1 reaffirmation, no new sub-platform under the Intent Eval Platform umbrella may be **initiated** in the next 6 months. The bandwidth math (3-5 hrs/wk, ~12 founder-hours/year governance overhead) does not support an additional brand surface. The two **named future** sub-platforms catalogued in `FUTURE.md` — *LLM Harness Lab* and *Agent Runtime Sandbox* — are **design-doc-only, bandwidth-gated**. Initiation of either as an actual build is a Class-1 ISEDC trigger. Citation: Blueprint A § 3.7; DR-010 § 7 Q1 reaffirmation.

**Decoupled distribution from publishing.** Per Blueprint A § 1.2 principle 11, every release artifact confirms successful **publish** through an out-of-band check — not just successful local **write**. CI pipelines treat "the artifact is readable from its public URL by an unauthenticated client" as the definition of done, not "the publish command exited 0." This principle exists because of the observed failure mode where local write succeeded but downstream propagation failed silently, producing drift that looks like success. Citation: Blueprint A § 1.2 principle 11.

---

## 9. Alphabetical cross-reference index

This index points each term to its primary section in this glossary and to the 2-4 most relevant documents that use it. When a term has a "see also" entry in another section here, the index entry lists the primary section only — readers traverse from there.

| Term | Section here | Used in |
|---|---|---|
| Acting head of board | § 5 | Blueprint A § 1.1; DR-010 § 13.5 + § 13.6; ISEDC skill |
| Active predicate types | § 6 | Blueprint A § 4.2; Blueprint B § 7.2; DR-010 § 7 Q3 |
| Anti-goals (binding scope control) | § 8 cross-ref | Blueprint A § 3 |
| Approximate reproducibility (anti-pattern) | § 8 | Blueprint A § 1.2; Blueprint B § 3.2 |
| `bd-sync` | § 7 | `~/000-projects/CLAUDE.md`; v2.1 epic plan |
| bd auto-flush JSONL drift | § 8 | v2.1 epic plan; `bd_000-projects-ufc` |
| Class 1 routing | § 5 | Blueprint A § 2.3; DR-010 § 7 Q6 |
| Class 2 routing | § 5 | Blueprint A § 2.3; DR-010 § 7 Q6 |
| Class 3 routing | § 5 | Blueprint A § 2.3; DR-010 § 7 Q6 |
| cosign | § 6 | Blueprint A § 4.2; Blueprint B § 7.5 |
| CostRecord | § 2.12 | Blueprint B § 2.12; Blueprint B § 4.2 |
| Decision Record | § 5 | Blueprint A § 2.3; all DRs `004`/`005`/`006`/`010` |
| Decoupled distribution from publishing | § 8 | Blueprint A § 1.2 principle 11 |
| Deferred predicate types | § 6 | DR-010 § 7 Q3 |
| DNSSEC + CAA | § 6 | DR-004 Q1; DR-010 § 7 Q5; Blueprint A § 4.2 |
| DSSE | § 6 | Blueprint A § 4.2; Blueprint B § 7.1 + § 7.5 |
| EvalRun | § 2.2 | Blueprint B § 2.2; Blueprint B § 1.2 + § 3.1 |
| EvalSpec | § 2.1 | Blueprint B § 2.1 |
| EvidenceBundle | § 2.4 | Blueprint A § 1.2 principle 10; Blueprint B § 2.4 + § 7 |
| EXPERIMENTAL mode | § 7 | DR-010 § 7 Q5 |
| External-pattern non-borrow | § 8 | DR-010 § 13.6; Blueprint A § 4.2 |
| FailureTaxonomy | § 2.13 | Blueprint B § 2.13; DR-004 S1Q3 |
| gate | § 3 | Blueprint A § 1.2 principle 10; Blueprint B § 7 |
| harness | § 3 | Blueprint A § 2.1 + § 4.2 |
| in-toto Statement v1 | § 6 | Blueprint A § 1.2 principle 3; Blueprint B § 7.1 |
| intent resolution | § 3 | Blueprint B § 1.2; DR-005 S2Q4 |
| ISEDC | § 5 | Blueprint A § 1.2 principle 12; ISEDC skill v1.0.0; all DRs |
| judge | § 3 | Blueprint B § 2.5 |
| JudgeDecision | § 2.5 | Blueprint B § 2.5 |
| `labs.intentsolutions.io` reserved-don't-touch | § 8 | DR-004 Q1; DR-010 § 10; Blueprint A § 4.2 |
| matcher | § 3 | Blueprint B § 2.3 + § 2.5 |
| MatcherMap | § 2.3 | Blueprint B § 2.3; DR-005 |
| mapping | § 3 | Blueprint B § 2.3 |
| MM-1 (async write / stale read) | § 4 | DR-004; DR-005; `002-RR-LAND` § 4 |
| MM-2 (response-shape drift) | § 4 | DR-004; DR-005; `002-RR-LAND` § 4 |
| MM-3 (cooldown / debounce) | § 4 | DR-004; DR-005; `002-RR-LAND` § 4 |
| MM-4 (side-effect verification) | § 4 | DR-004; DR-005; `002-RR-LAND` § 4 |
| MM-5 (mandatory context) | § 4 | DR-004; DR-005; `002-RR-LAND` § 4 |
| MM-6 (strict-mode compliance) | § 4 | DR-004; DR-005; `002-RR-LAND` § 4 |
| MM-7 (DEFERRED) | § 4 | DR-004 S1Q3; DR-010 § 10; CONTRIBUTING-failure-shape |
| No new platform initiation (6mo) | § 8 | Blueprint A § 3.7; DR-010 § 7 Q1 |
| Override | § 5 | DR-010 § 13.5 + § 13.6 |
| Phase A | § 7 | Blueprint A § 4.2; DR-010 § 7 Q5 |
| Phase A-conditional predicate types | § 6 | DR-010 § 7 Q3 |
| Phase B | § 7 | DR-010 § 13.5; Blueprint A § 4.2 |
| Phase C | § 7 | Blueprint A § 2.3 |
| Predicate URI | § 6 | DR-004 Q1; DR-010 § 7 Q3; Blueprint A § 4.2; Blueprint B § 7.2 |
| Production Rekor | § 7 | DR-010 § 7 Q5; Blueprint A § 4.2 |
| Ratification | § 5 | DR-010 § 10 |
| Rejected predicate types | § 6 | DR-010 § 7 Q3 CISO veto |
| Rekor | § 6 | Blueprint A § 4.2; Blueprint B § 7.5 |
| RegressionPack | § 2.7 | Blueprint A § 1.2 principle 5; Blueprint B § 2.7 |
| Replay | § 3 | Blueprint A § 1.2 principle 2; Blueprint B § 3.2 |
| Replay Fidelity N (RF-N) | § 7 | Blueprint A § 4.2; iel-E11 (forward-ref) |
| Receipt | § 3 | Blueprint B § 2.6 |
| RolloutGate | § 2.8 | Blueprint A § 4.1; Blueprint B § 2.8 + § 7 |
| Routing | § 3 | Blueprint A § 2.3; DR-010 § 7 Q6 |
| RuntimeReceipt | § 2.6 | Blueprint B § 2.6 |
| SessionTrace | § 2.10 | Blueprint B § 2.10 |
| sigstore staging | § 7 | Blueprint A § 4.2; DR-010 § 7 Q5 |
| SkillSnapshot | § 2.9 | Blueprint A § 4.1; Blueprint B § 2.9 |
| Subject naming | § 6 | Blueprint B § 7.3 |
| ToolInvocation | § 2.11 | Blueprint B § 2.11 |
| trace | § 3 | Blueprint A § 4.2; iel-E12 (forward-ref) |
| Vendor-generic discipline | § 8 | DR-004 S1Q2; DR-010 § 10; PRIVATE `~/000-projects/CLAUDE.md` |

---

*Acting head of board: Jeremy Longshore (Intent Solutions). Decision date: 2026-05-14. Authority: DR-010 (ISEDC Session 4, 2026-05-13) + Blueprint A (`011-AT-ARCH`) + Blueprint B (`012-AT-ARCH`) + v2.1 epic plan § iel-E03 acceptance criteria.*

- Jeremy Longshore
intentsolutions.io
