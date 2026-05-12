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

*This file is maintained by the ISEDC process. Entries graduate to tracked backlog when their
trigger condition is met. Do not delete entries without ISEDC deliberation or acting-head-of-board
direction.*
