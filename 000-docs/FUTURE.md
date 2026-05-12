# FUTURE.md — Intent Eval Lab Deferred Insights

Insights recognized but not yet ready for implementation. Each entry carries a trigger condition
that specifies when it graduates from this file into a tracked bead + GH issue + Plane issue.

---

## Gateway / Universal MCP Server Reference Implementation

**Insight recognized:** 2026-05-11 (ISEDC Session 3)
**ISEDC reference:** `006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md` § Q3

### What the insight is

The gateway/federation pattern is the production architecture for multi-domain MCP servers. An
"ultimate universal MCP server" is not a monolith — it is a gateway/router that federates
multiple domain-specific MCP servers. Evidence Bundle's composable partial attestation is the
missing standards layer that makes such a gateway evaluable: each federated server can attest to
its own conformance surface independently, and the gateway composes those partial attestations
without requiring total coverage.

No external party has publicly filed this connection as of 2026-05-11.

### Why it is not being implemented now

- Zero beads, GH issues, or Plane issues track this work — it is not in any active backlog.
- PB-11 (Intentional Mapping signal vocabulary) + PB-12 (Pact extension + Gherkin) are the
  prerequisite substrate the gateway would federate. Building the gateway before those items land
  creates architectural debt: the gateway has nothing to evaluate.
- Sole-prop bandwidth is fully committed to active client engagements and Phase B Wave 1 items.
- ISEDC voted 3-3-2 (B vs D vs A) with no majority — the hybrid FUTURE.md capture was the
  correct synthesis per ISEDC acting head of board (Jeremy Longshore 2026-05-11).

### Architecture (when trigger fires, build inside intent-eval-lab, not a 4th repo)

Per ISEDC Q3 CTO/GC binding: any gateway reference implementation lives as a module inside
`intent-eval-lab/` — not a new repo. 4th repo = schema-integrity error (independent release
lifecycle would be misleading since this is a demonstration artifact, not a distributable tool).

Recommended location when trigger fires: `intent-eval-lab/reference-implementations/mcp-gateway/`

### CISO pre-commit gates (activate the moment any gateway code is committed)

ALL THREE REQUIRED before first commit merges. Non-negotiable.

1. **Gateway-specific threat model document** filed at
   `intent-eval-lab/000-docs/NNN-AT-SPEC-gateway-threat-model-<date>.md`. Must cover:
   credential surface, multi-tenant routing isolation model, tool-call permission surface,
   cross-namespace attestation signing surface.

2. **PASS/FAIL test gates** in the reference implementation's test suite:
   - Credential-redaction test: gateway must NOT leak API keys into OTel spans, log events, or
     Evidence Bundle rows. Test: run at debug verbosity, grep emitted telemetry for any substring
     of the API key. Pass = zero substring matches.
   - Env-var spillover test: gateway must NOT expose secrets in subprocess environments. Test:
     invoke gateway, observe child-process environment via `/proc/<pid>/environ`, confirm no
     secret env-vars leak across process boundary.
   - Multi-tenant routing isolation test: attestation rows emitted for Namespace A must not
     appear in the Evidence Bundle for Namespace B when operating in the same gateway process.

3. **DNSSEC + CAA verified on `evals.intentsolutions.io`** before any gateway-signed attestation
   is pushed to Rekor. This is a re-statement of the ISEDC Q1 binding constraint (2026-05-10)
   which already requires DNSSEC + CAA — re-stated here as a gateway-specific gate because the
   gateway introduces a new signing key management surface.

### Trigger condition

Revisit and create bead + GH issue + Plane issue when EITHER:

- **Customer trigger:** A paying customer explicitly names "MCP gateway evaluation" or "federated
  MCP server conformance" as a deliverable requirement.
- **Substrate trigger:** PB-11 (OTel MM-1..MM-6 signal vocabulary) + PB-12 (Pact extension
  format + Gherkin scenarios) have shipped AND sole-prop bandwidth is available for Wave 3 scope.

When the trigger fires, the first action is creating the three tracking artifacts (bead + GH issue
+ Plane issue) before writing any code.

---

## Policy as Peer Spec Module

**Insight recognized:** 2026-05-11 (Milestone 1 of build journey `se-the-council-bubbly-frog.md`)
**Plan reference:** convergent critique of pre-M1 plan; SPEC.md § 8 R14

### What the insight is

The `tests/TESTING.md` policy that consuming repositories author (coverage thresholds, required
gates, advisory elevation rules) could plausibly become its own peer spec module — a standalone
JSON Schema or YAML schema published alongside `evidence-bundle/` describing the policy shape
that any Evidence Bundle consumer reads.

The convergent critique that informed the M1 plan rejected this for v0.1.0-draft on architectural
honesty grounds: per the system brief § 8, policy is **consumer-facing config**, not a peer of
the in-toto envelope. Coupling policy to the attestation surface (under the same predicate URI
namespace, with the same immutability constraints) would force every threshold adjustment to
mint a new URI.

### Why it is not being implemented now

- M1 ships the interface (SPEC.md § 8 R15) — how a consumer reads a policy file alongside a
  bundle. That interface is enough for `intent-rollout-gate` (M5) to implement against without
  a separate spec module.
- Zero independent implementers have requested a shared policy schema. Codifying one before
  there is demand is the same scope-sprawl error the critique flagged.
- The example at `specs/evidence-bundle/v0.1.0-draft/examples/policy.yaml` is explicitly
  informative-only and may serve as a de facto reference shape for multiple consumers before any
  peer-spec module is warranted.

### Architecture (when trigger fires)

If the trigger fires, the peer spec module lands at `specs/policy/v0.1.0-draft/` alongside the
existing spec modules. It would:

- Define a JSON Schema for policy.yaml-shaped documents (coverage thresholds, required vs
  applicable-only vs advisory partitions, branch-specific override rules).
- Reference `evidence-bundle/v0.1.0-draft/SPEC.md` § 8 R15 as the consumer-interface contract
  it satisfies.
- Stay at a different URI namespace from the gate-result predicate URI to preserve
  attestation-URI immutability discipline.

The new module ships as its own `v0.1.0-draft` and goes through the same draft → RC → stable
arc as the gate-result predicate.

### Trigger condition

Revisit and create a tracking bead + GH issue + Plane issue when:

- **External implementer trigger:** A non-Intent-Solutions party building a consumer of the
  Evidence Bundle (a competing Rollout Gate, a CI service, an attestation aggregator) requests
  a shared policy schema citing concrete interop friction.
- **Multi-consumer trigger:** Intent Solutions ships **at least two distinct consumers** of
  the Evidence Bundle that each have their own policy schema. The duplication is the signal
  that a shared module is warranted.

When the trigger fires, the first action is filing a tracking bead and adding the policy
peer-spec module skeleton.

---

## MM-7+ Admission Criteria (DEFERRED — but CONTRIBUTING path SHIPPED)

**Insight recognized:** 2026-05-10 (ISEDC v1 Q3)
**ISEDC reference:** `004-AT-DECR-isedc-council-record-2026-05-10.md` § Q3

### What the insight is

The MM-1..MM-6 failure-mode vocabulary in `specs/mcp-plugin-observability/` is intentionally
finite at v0.1.0-draft. MM-7+ admission is deferred — but the admission *path* is shipped in
Milestone 1 at `specs/mcp-plugin-observability/v0.1.0-draft/CONTRIBUTING-failure-shape.md`.

A new MM-N can only enter the spec via the three admission criteria (C1: ≥2 independent
engagements observed; C2: type-distinct from MM-1..MM-6; C3: OTel signal vocabulary draft
attached). The CONTRIBUTING file is the gate.

### Why MM-7 itself is not being implemented now

- No engagement has reported a failure shape that distinctly type-fits an MM-7 candidate against
  C1/C2/C3 as of 2026-05-11.
- ISEDC v1 Q3 binding constraint: vocabulary inflation under engineering or external pressure
  is the failure mode to avoid. Adding categories is irreversible.

### Trigger condition

A proposal lands per `CONTRIBUTING-failure-shape.md` and the reviewing maintainer adjudicates it
positively against C1, C2, C3. At that point, MM-7 (or whatever the proposer named) becomes a
tracked work item in the next minor version of `mcp-plugin-observability/`.

---

## OpenTelemetry Collector Reference Deployment

**Insight recognized:** 2026-05-11 (Milestone 1 of build journey `se-the-council-bubbly-frog.md`)
**Plan reference:** M6 deferral; system brief § 7

### What the insight is

The Evidence Bundle emitters (`audit-harness` M2, `j-rig-binary-eval` M3, `intent-rollout-gate`
M5) all fire `agent.rollout.gate.*` OTel events alongside their signed-row emission. A reference
deployment of an OTel collector configured to ingest and route those events (to a dashboard, an
alerting backend, or a long-term store) is the natural next step in operator usability — but it
is not foundational to the signing chain.

### Why it is not being implemented now

- M1-M5 deliverables fire OTel events as best-effort no-ops if a collector is absent. The
  signing chain works without a collector deployed.
- A reference deployment is a downstream operator-experience deliverable, not a standards-track
  prerequisite.
- Sole-prop bandwidth in M1-M5 is committed to the signing chain. Adding a collector deployment
  earlier compounds the time-to-public-rollout risk.

### Architecture (when trigger fires)

Land in M6+ (public rollout) or as a Phase C deliverable. Likely candidates:

- A `docker-compose.yml` packaged in the `intent-eval-platform-example/` repo (M6) wiring an
  OTel collector + a viewer (Grafana, SigNoz, or similar).
- A `helm` chart for Kubernetes deployments.
- A blog post on `startaitools.com` walking through the deployment.

### Trigger condition

The trigger is two-part:

- **(a) M6 rollout has shipped** — the platform is publicly discoverable.
- **(b) An external user requests** a reference deployment (issue filed on the example repo or
  on `intent-eval-lab`) OR Jeremy decides operator-experience polish is the next bandwidth slot.

When (a) is satisfied and (b) fires, file a tracking bead in `intent-eval-platform-example/`
(or wherever the reference deployment lands) and begin work.

---

## Pact Extension Format + Gherkin Scenarios (PB-12)

**Insight recognized:** 2026-05-10 (Phase B scope refinement plan `003-PP-PLAN`)
**Plan reference:** PB-12 wave-2 item

### What the insight is

The Pact contract-testing format (the well-known consumer-driven contract testing schema) could
be extended with conventions that align it with the Intent Eval Platform's Evidence Bundle
semantics — specifically the MM-1..MM-6 failure-mode vocabulary, the `agent.rollout.gate.*`
OTel events, and Gherkin scenario bindings.

Practitioners who use Pact for HTTP/microservice contract testing today could compose Pact
verification runs with j-rig behavioral evaluation runs into a single Evidence Bundle, with
Gherkin scenarios authored once and consumed by both.

### Why it is not being implemented now

- The cross-tool composition is downstream of PB-11 (Intentional Mapping OTel signal vocabulary)
  shipping. PB-11 is M6 RFC-filing work in the build journey. Pact integration before PB-11 is
  premature.
- No engagement has requested Pact integration as of 2026-05-11.
- Sole-prop bandwidth gates this behind M1-M6 completion.

### Architecture (when trigger fires)

Land as a new spec module at `specs/methodology/pact-extension/v0.1.0-draft/` describing the
Pact-extension conventions, plus example Pact verifier ↔ Evidence Bundle integration code (most
likely a small adapter library in `j-rig-binary-eval/packages/cli/src/adapters/`).

### Trigger condition

- **(a)** PB-11 has shipped (OTel SIG-GenAI accepts the Intentional Mapping vocabulary RFC, or
  Intent Solutions ships the vocabulary as an independent extension if the SIG declines).
- **(b)** An external user or a paying customer names Pact integration as a deliverable, OR
  internal dogfood (M5) surfaces Pact integration as natural for one of the dogfood repos.

When (a) AND (b), file a tracking bead and begin.

---

*This file is maintained by the ISEDC process. Entries graduate to tracked backlog when their
trigger condition is met. Do not delete entries without ISEDC deliberation or acting-head-of-board
direction.*
