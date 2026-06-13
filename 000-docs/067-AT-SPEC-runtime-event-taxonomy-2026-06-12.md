# Canonical runtime event taxonomy — categories, names, payloads, lineage rules

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** Blueprint B
(`012-AT-ARCH-platform-runtime-blueprint.md`) § 4.3 (event categories + must-emit) +
§ 7.2 (predicate-kind `must emit` binding) — this doc is the iel-E12 spec those sections
forward-reference for the per-event names · **Epic:** iel-E12 (runtime event taxonomy) ·
**Beads:** blr7, sms2, va7a, z1a3, nzua, 14z

This spec is the canonical registry of runtime OTel **event names** that Blueprint B § 4.3
deferred. Blueprint B locks the event CATEGORIES (`runtime.*`, `replay.*`, `bundle.*`,
`gate.*`, `judge.*`, `agent.*`, `cost.*`, `sandbox.*`, `taxonomy.*`) and names four discrete
emitting events; the kernel YAML pins those four events' attribute names; **this doc DEFINES
the remaining event categories, their per-event names, and their payload field schemas**,
extending the kernel's dotted-lowercase convention to the categories the YAML explicitly
deferred to iel-E12.

**Relation block.** This doc + the kernel YAML
(`intent-eval-core/schemas/v1/otel-attributes.yaml`, repo-relative) together form the COMPLETE
OTel taxonomy. The kernel YAML is the **naming AUTHORITY** for the four already-pinned events
(`runtime.dedup`, `replay.verdict`, `replay.input.drift`, `bundle.emission.refused`) and for
the shared attributes (`eval.run_id`, `eval.session_trace_id`, `trace.id`); this doc cites
those names and MUST NOT contradict them. This doc is the authority for the event names it
introduces here. A future kernel-YAML extension MAY pin the names this doc introduces; until
then the kernel YAML's pinned set + the categories defined here = the full event set.
Relates to: Blueprint B § 4.3 + § 7.2; the kernel YAML; the replay-fidelity spec
(`066-AT-SPEC-replay-fidelity-levels-2026-06-12.md`) for the `replay.*` events; the lineage log
(`054-AT-SPEC-lineage-log-and-derived-coverage-map-2026-06-12.md`); the Rekor superseding-event
protocol (`065-AT-SPEC-rekor-superseding-event-protocol-2026-06-12.md`); the canonical glossary
(`014-DR-GLOS-canonical-glossary.md`); the audit-harness emitter (iah-E07) and the j-rig
emitter (iaj-E08).

## 1. Execution + judge event categories

### 1.1 EXECUTION events (`runtime.*`)

Execution events mark EvalRun lifecycle transitions and criterion evaluation. `runtime.dedup`
is the kernel-pinned anchor (kernel YAML, `category: runtime`); the rest extend the category
under the same dotted-lowercase convention.

| Event | When emitted | Payload (attributes beyond the shared metadata of § 4) |
| --- | --- | --- |
| `runtime.run.started` | a worker leases an EvalRun and transitions it to `running` | `runtime.run.spec_content_hash` (string), `runtime.run.skill_snapshot_sha` (string) |
| `runtime.run.finished` | the EvalRun reaches a terminal state | `runtime.run.terminal_state` (enum `judged`/`archived_success`/`archived_failed`), `runtime.run.duration_ms` (int) |
| `runtime.criterion.evaluated` | one matcher/criterion is scored within a SessionTrace | `runtime.criterion.matcher_class` (string), `runtime.criterion.outcome` (enum `pass`/`fail`/`skip`) |
| `runtime.dedup` | **(kernel-pinned)** a worker skips a duplicate EvalRun whose idempotency key is already terminal-or-later | `runtime.dedup.cache_hit` (bool), `runtime.dedup.terminal_state` (string) — names per kernel YAML |

`runtime.dedup` attribute names are owned by the kernel YAML and reproduced here for category
completeness only; the others are minted by this doc per § 4.

### 1.2 JUDGE events (`judge.*`)

Judge events capture LLM-judge invocation, disagreement, and verdict. Blueprint B § 4.3 already
names `judge.disagreement.count` and `judge.disagreement.verdict_set` as **attributes** on the
parent JudgeDecision span; this doc promotes them to a coherent event+attribute taxonomy.

| Event | When emitted | Payload |
| --- | --- | --- |
| `judge.invoked` | an LLM judge is dialed for a matching event | `judge.id` (string), `judge.model_id` (string), `judge.model_version` (string) |
| `judge.disagreement` | multiple judges scoring the same matching event return different verdicts | `judge.disagreement.count` (int), `judge.disagreement.verdict_set` (string[]) — names per Blueprint B § 4.3 |
| `judge.verdict` | a JudgeDecision is finalized for a matching event | `judge.verdict` (string), `judge.verdict_source` (enum `llm_with_seed`/`llm_no_seed`/`deterministic`), `judge.seed` (int / null) |

`judge.verdict_source` aligns with the kernel RuntimeReceipt `verdict_source` contract (iec-E06)
and is the discriminator the replay spec uses to bound RF level (`066-AT-SPEC` § 1: an
`llm_no_seed` verdict cannot reach RF-2).

## 2. Replay + governance event categories

### 2.1 REPLAY events (`replay.*`)

Two replay events are kernel-pinned; their attribute names are OWNED by the kernel YAML and
MUST NOT be redefined here. This doc places them in the taxonomy and adds the replay events
`066-AT-SPEC` implies.

| Event | Authority for attribute names | Payload |
| --- | --- | --- |
| `replay.verdict` | **kernel YAML** (deferred from this doc) | `replay.verdict` (enum `match`/`semantic_match`/`drift`/`failed`), `replay.is_replay` (bool), `replay.original_trace_id` (string), `replay.fidelity_level` (enum `RF-0..RF-4`) |
| `replay.input.drift` | **kernel YAML** (deferred from this doc) | `replay.original_trace_id` (string), `replay.input.drifted_field` (enum over the five frozen-input dimensions) |
| `replay.started` | this doc | `replay.original_trace_id` (string), `replay.fidelity_level` (enum `RF-0..RF-4`) — marks the re-execution span before a verdict exists |

The `replay.verdict` enum (`match`/`semantic_match`/`drift`/`failed`) and the
`replay.fidelity_level` enum (`RF-0..RF-4`, iel-E11) are pinned in the kernel YAML; the
divergence-handling table that maps them per RF level lives in `066-AT-SPEC` § 3. This doc does
NOT re-pin those attribute names — it defers them to the kernel YAML, which already carries them.

### 2.2 GOVERNANCE events (`gate.*`)

Governance events capture gate decisions, rollback/superseding, and ratification markers. The
`gate.decision.drift` event is already named in Blueprint B (§ 2 RolloutGate replayability) and
`gate.decision.emitted` in the § 6.2 mermaid; this doc registers the category coherently.

| Event | When emitted | Payload |
| --- | --- | --- |
| `gate.decision.emitted` | a RolloutGate decision row is emitted under `gate-result/v1` | `gate.name` (string), `gate.decision` (enum `pass`/`fail`/`advisory`/`error`), `gate.policy_ref` (string) |
| `gate.decision.drift` | re-execution of gate logic against the same bundle+policy+version yields a different decision | `gate.decision.expected` (string), `gate.decision.observed` (string) |
| `gate.superseded` | a superseding event marks a production-Rekor-anchored row advisory-not-binding (`065-AT-SPEC` § 5) | `gate.superseded.subject_digest` (string), `gate.superseded.signing_mode` (const `rolled-back-superseded`), `gate.superseded.rollback_decision_ref` (string) |
| `gate.ratification.recorded` | an ISEDC/acting-head ratification of a one-way-door gate is logged | `gate.ratification.decision_record` (string AT-DECR ref), `gate.ratification.class` (string) |

`gate.superseded` carries the `rolled-back-superseded` marker on the superseding event's
reference per `065-AT-SPEC` § 4 — never as a mutation of the original anchored row.

## 3. Storage + observability + optimization event categories

### 3.1 STORAGE events (`bundle.*`)

`bundle.emission.refused` is kernel-pinned; the persistence events extend the category.

| Event | Authority | Payload |
| --- | --- | --- |
| `bundle.emission.refused` | **kernel YAML** | `bundle.predicate_uri` (string), `bundle.emission.refused_contract` (enum `subject`/`predicate_type`/`predicate_body`/`signature`), `bundle.emission.refused_reason` (string) |
| `bundle.signed` | an Evidence Bundle row is signed and pushed to a transparency log (Blueprint B § 6.2 mermaid) | `bundle.predicate_uri` (string), `bundle.signing_mode` (enum `sigstore_staging`/`rekor_production`/`unsigned_experimental`) |
| `bundle.persisted` | the content-addressed bundle blob lands in object storage with its index row written | `bundle.blob_digest` (`sha256:`), `bundle.lifecycle_class` (enum `hot`/`cold`/`archive`) |

`bundle.emission.refused` attribute names are owned by the kernel YAML and reproduced for
category completeness; `bundle.signing_mode` aligns with the kernel SigningMode space
(Blueprint B § 2.4), to which `rolled-back-superseded` is added only on superseding-event
references, never on an emission row (`065-AT-SPEC` § 4).

### 3.2 OBSERVABILITY events + metrics (`agent.*`)

Observability covers the first-class metrics Blueprint B § 4.3 names. These are OTel **metrics**,
not discrete events; their names are fixed by Blueprint B § 4.3 and registered here.

| Metric / attribute | Kind | Authority | Brief |
| --- | --- | --- | --- |
| `agent.eval.judge_disagreement_rate` | metric (gauge) | Blueprint B § 4.3 | aggregate judge-disagreement rate per matcher class |
| `agent.loop.depth` | span attribute | Blueprint B § 4.3 | tool-call recursion depth on every ToolInvocation span (bounded agentic recursion, Blueprint A § 3.5) |

Per DR-010 Q3, loop depth is observable but the `agent-loop-trace/v1` predicate URI is REJECTED
for v1 — these surfaces capture observability WITHOUT committing to an attestation predicate.

### 3.3 OPTIMIZATION events (`taxonomy.*` reserved; refiner reference only)

Skill Refiner emits attempt/accept/reject events. The refiner internals are unbuilt (DR-028
Phase A.0 null-hypothesis baseline gates the mechanism); this doc RESERVES the category and
names the events at the boundary, aligned with the `skill-refiner-pass/v1` predicate, but does
**not** front-run refiner-internal payload shape.

| Event | When emitted | Payload (boundary-only, refiner-internal fields deferred) |
| --- | --- | --- |
| `optimization.refiner.attempted` | the Refiner proposes a SKILL.md edit | `optimization.skill_version_id` (string), `optimization.strategy` (string) |
| `optimization.refiner.accepted` | a proposal passes the strict-improvement-on-Pareto-dominant predicate | `optimization.predicate_uri` (const `skill-refiner-pass/v1`), `optimization.parent_version_id` (string) |
| `optimization.refiner.rejected` | a proposal fails the acceptance predicate (regression on any behavioral) | `optimization.reject_reason` (string) |

These names are provisional registrations; the refiner spec (forthcoming, `@j-rig/refiner-core`)
is the authority for the refiner-internal payload once built. This doc reserves the names so two
emitters cannot diverge on spelling before the refiner lands (the Gregg finding #2 hazard).

## 4. Naming standard, required metadata, lineage rules

### 4.1 Naming standard (dotted-lowercase)

- **Convention:** dotted-lowercase with snake_case leaf segments, OTel-idiomatic
  (`eval.run_id`, `gate.decision`, `judge.disagreement.count`) — identical to the kernel YAML's.
- **Authority:** the kernel YAML (`intent-eval-core/schemas/v1/otel-attributes.yaml`) is the
  single naming AUTHORITY for every name it pins. This doc is the authority for the names it
  introduces. On any disagreement the kernel YAML wins (Blueprint B § 7.0 schema-authority
  precedence: machine-readable kernel source is canonical, prose is amended to match).
- **Minting a new event name:** add it to the appropriate category here first, then — once an
  emitter needs the attribute pinned for cross-emitter agreement — promote the attribute names
  into the kernel YAML and export the TypeScript constants at `@intentsolutions/core/otel/v1`.
  A name is RESERVED the moment it appears in a NORMATIVE section of this doc; an emitter MUST
  NOT mint an ad-hoc synonym for a reserved name.
- **Categories are closed.** The nine categories (`runtime.*`, `replay.*`, `bundle.*`, `gate.*`,
  `judge.*`, `agent.*`, `cost.*`, `sandbox.*`, `taxonomy.*`) are locked by Blueprint B § 4.3; a
  new event MUST land under an existing category, never a tenth.

### 4.2 Required metadata every event MUST carry

Every event in every category MUST carry the shared correlation metadata, so any event pivots
back to its EvalRun and its lineage chain:

| Field | Authority | Requirement |
| --- | --- | --- |
| `eval.run_id` | kernel YAML (shared) | **required** — UUIDv7 (RFC 9562) of the owning EvalRun; the idempotency key |
| `eval.session_trace_id` | kernel YAML (shared) | recommended — UUIDv7 of the SessionTrace span the event hangs under |
| `trace.id` | kernel YAML (shared) | recommended — W3C Trace Context trace-id propagated from API ingress |
| timestamp | OTel span/event time | **required** — RFC 3339 UTC; the OTel event timestamp, never a wall-clock re-read |

An event missing `eval.run_id` is malformed and is rejected at the emission boundary the same
way Blueprint B § 3.3 rejects a predicate-contract violation — there is no "anonymous" event.

### 4.3 Lineage rules

- Events link to the **run-lineage DAG** (`EvalRun → SessionTrace → ToolInvocation → JudgeDecision`)
  through `eval.run_id` + `eval.session_trace_id`; the span hierarchy mirrors the DAG
  (Blueprint B § 4.3 lineage capture).
- Replay events additionally carry `replay.original_trace_id` linking the re-execution to the
  original, and reference the replay metadata in `066-AT-SPEC` § 2 (the `eval_run_id`-keyed
  replayable record) — never a mutable position.
- Governance/superseding events link to the **append-only lineage log**
  (`054-AT-SPEC`): a `gate.superseded` event references the superseded row by content-addressed
  subject digest, and the binding-state resolution walks the log alone (`065-AT-SPEC` § 5). The
  lineage log only ever grows — the same append-only discipline replay divergence obeys
  (`066-AT-SPEC` § 3).

## 5. Anti-patterns + cross-references

**Event anti-patterns — refuse on sight.**

- **Unpinned ad-hoc names.** Emitting `evalRunId` / `run.id` / `eval_run_id` instead of the
  pinned `eval.run_id`, or minting a synonym for any name reserved in § 1–§ 3. This is exactly
  the Gregg finding #2 hazard the kernel YAML exists to prevent: five independent emitters
  (j-rig, audit-harness, intent-rollout-gate, lab tests, the kernel) WILL diverge on spelling
  the moment two emit the same event independently. One canonical form per name, no exceptions.
- **Missing correlation id.** An event without `eval.run_id` (or a governance event without the
  superseded subject digest) is unjoinable to its lineage and is malformed, not "partial."
- **PII in payloads.** Event payloads carry IDs, digests, enums, and version strings — never
  raw prompt/response bodies, user identifiers, or secrets. Large or sensitive content is
  content-addressed in object storage (Blueprint B § 5.1) and referenced by digest; the event
  carries the digest, not the bytes. The credential broker redacts provider responses
  (Blueprint B § 4.1) before any telemetry is emitted.
- **Inventing a new category.** Adding a tenth top-level category instead of placing the event
  under one of the nine Blueprint B § 4.3 locks.
- **Re-pinning a kernel-owned name.** Redefining `replay.verdict`, `replay.input.drift`,
  `runtime.dedup`, or `bundle.emission.refused` attribute names here instead of deferring to the
  kernel YAML.

**Cross-references.**

- **Kernel YAML** (`intent-eval-core/schemas/v1/otel-attributes.yaml`, repo-relative) — the
  naming authority for the four pinned events + the shared attributes; this doc extends its
  convention to the remaining categories. Together they are the complete taxonomy.
- **Blueprint B § 4.3** (`012-AT-ARCH-platform-runtime-blueprint.md`) — the category lock + the
  observability metrics (`agent.eval.judge_disagreement_rate`, `agent.loop.depth`) + the
  disagreement attributes this doc registers.
- **Blueprint B § 7.2** — the predicate-kind `must emit` binding (which span emits which
  predicate kind's attribute set); this doc supplies the event names that binding's spans emit.
- **`066-AT-SPEC` (replay fidelity levels)** — the RF-0..RF-4 scale, the replayable-record
  metadata, and the divergence-handling table the `replay.*` events surface.
- **`054-AT-SPEC` (lineage log)** — the append-only event log governance/superseding events
  link to; the grow-only discipline § 4.3 lineage rules inherit.
- **`065-AT-SPEC` (Rekor superseding-event protocol)** — the `rolled-back-superseded` marker and
  superseding-event shape the `gate.superseded` event carries.
- **`014-DR-GLOS` (canonical glossary)** — platform terminology every term here resolves to.
- **iah-E07** (audit-harness emit-evidence) — the audit-harness-side emitter that MUST emit
  these names; the deterministic gates' `gate.decision.emitted` / `bundle.signed` events.
- **iaj-E08** (j-rig emitter) — the j-rig behavioral-eval emitter that MUST emit the
  `judge.*` and `replay.*` names; the second independent emitter the cross-emitter pin
  (Gregg finding #2) guards against drift between.
