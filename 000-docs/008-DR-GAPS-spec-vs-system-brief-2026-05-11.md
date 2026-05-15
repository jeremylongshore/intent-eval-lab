# 008-DR-GAPS — Spec coverage vs system brief gap analysis

| Field | Value |
|---|---|
| **Date** | 2026-05-11 |
| **Author** | Claude (Opus 4.7) for Jeremy Longshore |
| **Source plan** | `~/.claude/plans/se-the-council-bubbly-frog.md` (Milestone 1 — Foundation) |
| **Source brief** | [`007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html`](./007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html) |
| **Spec under analysis** | [`specs/evidence-bundle/v0.1.0-draft/SPEC.md`](../specs/evidence-bundle/v0.1.0-draft/SPEC.md) |
| **Status** | Draft — published alongside the SPEC.md normative draft for Phase B Milestone 1 |
| **Bead** | `iel-slp` (M1 sub-bead) under epic `iel-bbt` |

---

## 1. Purpose

The system brief (`007-DR-BRIEF`) describes the full Intent Eval Platform — a six-month journey
across `audit-harness` emission, `j-rig-skill-binary-eval` emission, an `intent-rollout-gate` consumer,
internal dogfood, and public rollout. The **Evidence Bundle SPEC.md normative draft** ships in
Milestone 1 covers a deliberately narrow slice of that journey: the envelope, predicate URI,
predicate body schema, subject naming, signing, and policy-consumption interface.

This document enumerates what the SPEC.md ships, what the SPEC.md deliberately defers, and where
each deferred item lands.

## 2. The 10 gap areas

Each row indicates whether the area ships in the SPEC.md normative draft, defers to a later
milestone, or stays in `FUTURE.md` until a trigger condition fires.

| # | Gap area | Status | Where it lands |
|---|---|---|---|
| **G1** | In-toto Statement v1 envelope, predicate URI, predicate body schema | **SHIPPED in M1** | SPEC.md § 4-5 + `schema/gate-result.schema.json` |
| **G2** | Subject naming convention with regex pattern | **SHIPPED in M1** | SPEC.md § 6 R8-R9 |
| **G3** | Signing & verification (cosign, DSSE, Rekor) | **SHIPPED in M1 spec text; signing infrastructure pending DNSSEC** | SPEC.md § 7; CISO gate `iel-4zr` (Jeremy manual action) |
| **G4** | Policy consumption interface (`tests/TESTING.md`) | **SHIPPED in M1 as interface only** | SPEC.md § 8 R14-R16 |
| **G5** | Policy as peer spec module (standalone schema independent of any consumer) | **DEFERRED to FUTURE.md** | Trigger: external implementer needs it as standalone spec; ≥2 independent consumers requesting a shared format |
| **G6** | Rollout Gate gateway/federation reference (multi-domain MCP server attestation composition) | **DEFERRED to FUTURE.md** | Existing `FUTURE.md` "Gateway / Universal MCP Server" entry per ISEDC Session 3 Q3 |
| **G7** | MM-7+ admission criteria (community contribution path for new failure-mode categories) | **PARTIAL: criteria SHIPPED via `CONTRIBUTING-failure-shape.md`; MM-7 itself DEFERRED** | `mcp-plugin-observability/v0.1.0-draft/CONTRIBUTING-failure-shape.md` (M1 sub-bead `iel-hol`); MM-7 stays in FUTURE.md per ISEDC v1 Q3 |
| **G8** | OpenTelemetry collector reference deployment | **DEFERRED to M6+ / FUTURE.md** | OTel events fire from emit-evidence, j-rig, Rollout Gate (M2-M5); a reference deployment of an OTel collector configured to ingest `agent.rollout.gate.*` events is a Phase C deliverable |
| **G9** | Pact extension format + Gherkin scenarios (PB-12) | **DEFERRED to FUTURE.md** | Wave 2 work item; specs/methodology subdirectory |
| **G10** | AGENTS.md parser, provider adapter measurement, in-toto subject-naming regex tightening, Rekor anchor verification scripts | **DEFERRED to M3-M5** | AGENTS.md parser is M3 j-rig sub-bead; provider adapters are M4 (PB-7); Rekor anchor verification is M5 dogfood + M6 example repo work |

## 3. What "shipped" means in M1

The Milestone 1 normative draft is the foundation downstream consumers need to begin emission.
"Shipped" means:

- The SPEC.md is normative (RFC 2119 keywords throughout, conformance reporting structure
  defined) — not a Phase A skeleton.
- The JSON Schema validates the example artifacts (verified empirically: 7 example predicates
  pass `Draft202012Validator` without errors).
- The example artifacts (`in-toto-statement.json`, `evidence-bundle.json`, `policy.yaml`)
  illustrate every result enum value and both single-row and multi-row container forms.

It does **not** mean:

- The signing infrastructure is operational. DNSSEC + CAA at Porkbun is required before any
  signed in-toto Statement referencing `evals.intentsolutions.io/gate-result/v1` is pushed to
  Rekor (CISO binding constraint, ISEDC v1 Q1, re-stated here). That is the M1 manual action
  tracked under bead `iel-4zr`.
- Any reference implementation has emitted a row against this URI. M2 (audit-harness emission)
  is the first.
- The URI is frozen. The URI moves from `v0.1.0-draft` → `v0.1.0-rc` → `v0.1.0` per SPEC.md
  § 9 R19 only after a non-Intent-Solutions party emits a row that verifies.

## 4. What deferral does NOT mean

A deferral is not abandonment. Each deferred item carries a trigger condition (FUTURE.md) or a
target milestone (M3-M6). The convergent critique reviewed in plan `se-the-council-bubbly-frog.md`
flagged premature peer-spec scope (G5) and premature gateway scope (G6) as the most expensive
errors to recover from. Both stay deferred in M1 by design.

The convergent finding: **policy is NOT a peer spec module**. It is consumer-facing config in
`tests/TESTING.md`. The interface (R15) is normative; the policy schema is the consumer's
concern. This stays true through Phase B unless and until two independent implementers need a
shared format.

## 5. Cross-references

- ISEDC Session 1 (`004-AT-DECR`) — 5 binding constraints (URI namespace, partner consent,
  MM-7 defer, OTel CSO sequence, provider PASS/FAIL)
- ISEDC Session 2 (`006-AT-DECR`) — Phase B gate re-eval (Q1 lift), Q3 gateway FUTURE.md hybrid
- Phase B scope refinement plan (`003-PP-PLAN`) — PB-1..PB-12 wave sequencing
- System brief (`007-DR-BRIEF`) — full architectural narrative; SPEC.md sections 4-6 extract
  and normativize this brief's §§ 6-8

## 6. Closing

This document accompanies the SPEC.md normative draft for the duration of the v0.1.0-draft
window. When the URI freezes at v0.1.0, this document remains as the historical record of what
M1 chose to ship vs defer and why.
