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
| 010 | [`010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`](./010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md) | AT-DECR (decision record) | 2026-05-13 | **ISEDC Session 4 — widened-scope architectural lock.** Full architectural lock for the widened-scope Intent Eval Platform (AISE 5-domain stack). Q1=A ONE BIG. Q2=per-artifact hybrid (TS-primary signing/CI surfaces; Python permitted ML internals behind subprocess boundaries). Q3=unification thesis BINDING; URI namespace incremental (4 predicates approved conditional on SPEC.md normative, 2 deferred, `agent-loop-trace/v1` REJECTED pending sanitization spec); new Plane "Tooling Drift Prevention" sub-module. Q4=Uncle Bob pattern adoption REVERSED per § 13.6 override (no external-pattern borrowing in forward-deployed work). Q5=parallel-track with EXPERIMENTAL-mode gate (M5.1 v0.1 ships sigstore staging; v0.2 production after SPEC.md normative); +50hr widening cap, +66hr ceiling; no new platform-build implementation in 6 months. Q6=three-class governance (Full ISEDC / CTO+VPDevRel pair / solo) + quarterly standing + public DR archive within 7d. S3Q2 narrowly reopened for informal community-temperature email only. S1Q5 (provider PASS/FAIL) explicitly declined reopening. Verbatim seat positions preserved per ISEDC adversarial-integrity protocol. Per-artifact fold-in plan for every in-flight artifact. |
| 011 | [`011-AT-ARCH-ecosystem-master-blueprint.md`](./011-AT-ARCH-ecosystem-master-blueprint.md) | AT-ARCH (architectural blueprint) | 2026-05-14 | Blueprint A — Ecosystem Master Blueprint (the constitution). Mission, 12 binding principles, 5-repo taxonomy, governance routing, and binding anti-goals for the Intent Eval Platform ecosystem. Authority chain: DR-004 → DR-006 (lifted) → DR-010 (NORMATIVE). |
| 012 | [`012-AT-ARCH-platform-runtime-blueprint.md`](./012-AT-ARCH-platform-runtime-blueprint.md) | AT-ARCH (architectural blueprint) | 2026-05-14 | Blueprint B — Platform Runtime Blueprint (the kernel specification). Inherits from Blueprint A (011). Defines the runtime architecture (modular monolith), 13-entity canonical domain model, state machines, isolation/cost/observability pillars, and Evidence Bundle predicate contracts for gate-result/v1. |
| 013 | [`013-AT-SPEC-repo-blueprint-template.md`](./013-AT-SPEC-repo-blueprint-template.md) | AT-SPEC (architectural specification template) | 2026-05-14 | Blueprint C — Repo Blueprint Template. The reusable template every IEP repo applies to produce its own per-repo blueprint (`NNN-AT-ARCH-repo-blueprint.md`). 13-section structure: repo identity · problem statement · scope boundaries (in/out/deferred/anti-goals) · architecture · canonical entities used · interfaces · testing strategy (7-layer SOP) · security + isolation (broker pattern, provider PASS/FAIL gates) · observability · cost governance · release strategy (strict SemVer, license audit) · beads / work breakdown · Definition of Done. Plus Author's Guide, Minimal Example (fictional intent-example-shim, INFORMATIVE only), and Validation Checklist. Unblocks: iec-E10, iel-E05 (self-application), iah-E01, iaj-E01, iar-E01. Epic iel-E04. |
| 014 | [`014-DR-GLOS-canonical-glossary.md`](./014-DR-GLOS-canonical-glossary.md) | DR-GLOS (definitions reference / glossary) | 2026-05-14 | Canonical Glossary — single source of truth for IEP platform terminology. 9 sections: purpose + reading guide; 13 canonical entities (point to Blueprint B § 2 for full attribute schemas); operational terms (matcher, mapping, routing, intent resolution, replay, eval, harness, trace, receipt, gate, judge); Intentional Mapping MM-1..MM-6 (MM-7 deferred); governance + lifecycle (ISEDC, three-class routing, Decision Record, override, ratification); signing + attestation (in-toto, DSSE, cosign, Rekor, predicate URI, subject naming, DNSSEC + CAA); sequence + lifecycle (Phase A/B/C, RF-N forward-ref, sigstore staging vs production Rekor, EXPERIMENTAL mode, bd-sync); anti-patterns + reserved terms; alphabetical cross-reference index. Authority chain: Blueprint A (011) names → Blueprint B (012) entity model → DR-004 / DR-005 / DR-010 terminology bindings. Epic iel-E03. |

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
