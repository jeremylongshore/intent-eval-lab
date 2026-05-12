# 000-INDEX — Intent Eval Lab Docs

Index of numbered docs in this directory. Add new docs as they land.

## Current docs

| # | File | Type | Date | Status |
|---|------|------|------|--------|
| 001 | [`001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`](./001-DR-RFC-otel-agent-rollout-gate-signals-draft.md) | DR-RFC (draft RFC) | 2026-05-10 | Phase A draft — files at OTel SIG-GenAI Phase B Week 4+ informed by community-temperature email (per ISEDC Q4) |
| 002 | [`002-RR-LAND-mcp-testing-bridge.md`](./002-RR-LAND-mcp-testing-bridge.md) | RR-LAND (landscape) | 2026-05-10 | Part 2 Workstream C deliverable — 6,257w landscape mapping bridge from static repo analysis to protocol-level runtime conformance (Intentional Mapping MM-1..MM-6 ↔ existing tooling gap map) |
| 003 | [`003-PP-PLAN-phase-b-scope-refinement.md`](./003-PP-PLAN-phase-b-scope-refinement.md) | PP-PLAN (plan) | 2026-05-10 | Part 2 Workstream D synthesis — 6,100w, 12 Phase B work items in 3 clusters, 4 Phase C items, standards-track vs IS-implementation split, four user-supplied lenses applied |
| 004 | [`004-AT-DECR-isedc-council-record-2026-05-10.md`](./004-AT-DECR-isedc-council-record-2026-05-10.md) | AT-DECR (decision record) | 2026-05-10 | ISEDC 7-seat adversarial council Decision Record — 5 Phase B open questions decision-locked with stacked minority protections. Verbatim seat positions preserved for future readers. |
| 005 | [`005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md`](./005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md) | AT-DECR (decision record) | 2026-05-10 | ISEDC v2 — matcher-map → Intentional Mapping terminology rename |
| 006 | [`006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md`](./006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md) | AT-DECR (decision record) | 2026-05-11 | ISEDC Session 3 — Phase B gate re-evaluation (Q1 standards-track lifted with explicit scope fence), Q3 gateway FUTURE.md hybrid synthesis, Q4 ecosystem post + MCP architecture hold. NPM count correction logged. |
| 007 | [`007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html`](./007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html) | DR-BRIEF (draft system brief) | 2026-05-11 | Full system brief — architecture, six-month journey, Evidence Bundle thesis. SPEC.md normative content extracts from §§ 6-8. |
| 008 | [`008-DR-GAPS-spec-vs-system-brief-2026-05-11.md`](./008-DR-GAPS-spec-vs-system-brief-2026-05-11.md) | DR-GAPS (gap analysis) | 2026-05-11 | M1 Foundation gap analysis — what SPEC.md normative draft ships, what defers to M2-M5, what stays in FUTURE.md. 10 gap areas enumerated. |
| 009 | [`009-RR-INTL-otel-sig-genai-temperature.md`](./009-RR-INTL-otel-sig-genai-temperature.md) | RR-INTL (external engagement research) | 2026-05-11 | ISEDC v1 Q4 CSO sequence paper-trail file. OTel SIG-GenAI informal community-temperature email DRAFTED; send is a Jeremy manual action. Response classification + Week 4+ RFC routing-decision criteria documented. |

## Filing convention

```
NNN-CC-ABCD-short-description.md
```

Where:
- `NNN` — three-digit sequence (start at 001)
- `CC` — category code:
  - `AA` — after-action report
  - `RR` — research / recon
  - `PP` — plan / planning
  - `DR` — draft (in-progress, not yet ready)
  - `RA` — ready-to-publish
  - `BL` — baseline / contract / formal record
- `ABCD` — sub-type code (free-form, 3-5 chars):
  - `LAND` — landscape
  - `LITS` — literature survey
  - `PLAN` — plan
  - `AACR` — after-action change-record
  - `EXPS` — experiment
  - `BRIEF` — system brief / executive overview
  - `GAPS` — gap analysis / coverage delta
  - `INTL` — international / external standards-body / community engagement
  - `DECR` — decision record (paired with `AT` category)
  - `RFC` — request-for-comments draft

Examples:
- `001-RR-LAND-cross-cli-eval-landscape-2026-05-07.md`
- `002-RR-LITS-skill-discovery-methodology-2026-05-08.md`
- `003-PP-PLAN-jrig-extension-architecture-2026-05-09.md`
- `004-AA-AACR-first-experimental-run-2026-05-15.md`

Date suffix is recommended for documents that capture a specific moment in time. Methodology / reference docs can omit the date.
