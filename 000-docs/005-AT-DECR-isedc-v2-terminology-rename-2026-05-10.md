# ISEDC v2 Decision Record — Terminology Rename (matcher-map → Intentional Mapping)

| Field | Value |
|---|---|
| **Date** | 2026-05-10 |
| **Acting Head of Board** | Claude (Anthropic, `claude-opus-4-7`), designated by Jeremy Longshore |
| **Council** | 7 seats convened (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel); all 7 returned |
| **User override at decision-lock** | "nothing changes but the name" — locks scope to rename only, no architectural concept addition |
| **Status** | Decision-locked; execution underway in same session |
| **Predecessor** | ISEDC v1 (`004-AT-DECR-isedc-council-record-2026-05-10.md`) — frozen, receives appended Terminology Note per Q3 |
| **Reusable pattern** | `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0 |

## Decisions (5)

| Q | Decision | Vote | Rationale |
|---|---|---|---|
| **Q1** Adopt rename | YES — rename "matcher-map" → "Intentional Mapping" | 7/7 adopt | Tactical → foundational vocabulary; aligns with Intent Solutions brand spine (Intentional Cognition OS, intent-driven systems) |
| **Q2** Identifier strategy | KEEP `MM-1..MM-6` as immutable category codes | 5/7 keep · 2/7 rename (CMO, CSO) | Citation stability across spec, RFC draft, Kobiton case study, bead history, blog drafts. HTTP-status-code precedent — stable codes survive conceptual reframings. VP DevRel: "the #1 OSS-trust violation is renaming identifiers under developers' feet." |
| **Q3** Scope | GOING-FORWARD ONLY — frozen artifacts get appended Terminology Note; bodies preserved | 6/7 going-forward · 1/7 rewrite all (CMO) | Audit-trail integrity (GC + CISO non-negotiable). ISEDC v1 Decision Record is signed; rewriting destroys the pattern. R1/R2 deliverables already delivered to Stu/Frank — frozen. |
| **Q4** Add Intent Resolution Layer | **NO — user override.** Council voted 6/7 to adopt the two-concept architecture (Intentional Mapping + Intent Resolution Layer), but user directed *"nothing changes but the name."* Scope locked to rename only — no new concept introduced. | User override | Simplest path; no architecture churn during R3 prep |
| **Q5** Timing | NOW — execute in same session | 3/7 now · 3/7 defer · 1/7 conditional · **user override** "fix it" | OTel community-temperature email hasn't been sent; window to lock terminology before maintainer first-impression is open. No predicates signed yet. |

## Stacked minority protections (binding)

- **GC binding:** trademark clearance memo on "Intentional Mapping" before any external filing (USPTO TESS + Google Scholar + W3C TR + IETF datatracker scan). External publication carries "subject to trademark clearance" footnote until memo lands. Memo target: 5 business days.
- **GC + CISO non-negotiable:** frozen artifact registry — ISEDC v1 Decision Record, R1/R2 partner deliverables, OTel RFC draft once filed, signed snapshot tags (`r1-2026-04-28`, `r2-2026-05-04`) — NEVER rewritten. Receive appended Terminology Note only.
- **CMO compromise (Q2):** spec README leads with the brand word — "MM-N identifiers are the canonical Intentional Mapping requirements." Brand word fronts even when identifier doesn't change.
- **CSO sequencing (Q5):** OTel RFC does not file with matcher-map terminology under any circumstances — if RFC would file before rename completes, defer the RFC instead.
- **CISO 48-hour soak:** no Phase B predicate signing for 48h post-rename to surface any missed surface.
- **CFO 90-min cap:** rename execution time-boxed at 90 minutes of founder time. Beyond that, append Terminology Notes and move on. (Self-imposed by acting head of board for this autonomous execution.)
- **CTO `/validate-consistency` gate:** post-rename run must pass with zero drift findings before merge.
- **VP DevRel: identifier stability is permanent.** Do not revisit MM-N → IM-N rename in a future ISEDC v3.

## What "rename only" means concretely

Per user override on Q4, this rename is a **string replacement**, not an architectural reframing:

- "matcher-map" (prose) → "Intentional Mapping" (proper-noun-cased) or "intentional mapping" (lower-case in prose)
- `matcher-map-template.md` (file) → `intentional-mapping-template.md`
- "matcher-map work product" / "matcher-map methodology" → "Intentional Mapping work product" / "Intentional Mapping methodology"
- MM-1..MM-6 identifiers stay as-is (per Q2)
- The 6 failure-shape categories (async race, shape drift, cooldown, side-effect verification, mandatory context, protocol strict-mode) keep their definitions and identifiers
- The conformance-test-suite structure stays the same
- The case-studies/ directory keeps its purpose (engagement-private case scaffolds)
- NO new "Intent Resolution Layer" section is added to the spec (user override on Q4)
- The runtime that consumes the Intentional Mapping (audit-harness emit-evidence + j-rig adapters + Rollout Gate) stays unnamed at the architectural level — it's just "the harness" and "the j-rig adapter" and "the Rollout Gate" as before

## Frozen artifact registry (NEVER rewritten — Terminology Note appended only)

1. `intent-eval-lab/000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md` (ISEDC v1, signed) — receives appended Terminology Note per Q3
2. Snapshot tags `r1-2026-04-28`, `r2-2026-05-04`
3. R1 partner deliverable already delivered to Stu/Frank (`partners.intentsolutions.io/kobiton/r1/`)
4. R2 partner deliverable already delivered (`partners.intentsolutions.io/kobiton/r2/`)
5. OTel RFC draft (`001-DR-RFC-...`) once filed at SIG-GenAI — currently mutable; renames freely until filing

## Living docs (rename freely in same session)

1. `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/SPEC.md`
2. `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/matcher-map-template.md` → RENAME file + body to `intentional-mapping-template.md`
3. `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/conformance-test-suite/README.md`
4. `intent-eval-lab/000-docs/000-INDEX.md`
5. `intent-eval-lab/000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` (RFC draft, still mutable)
6. `intent-eval-lab/000-docs/002-RR-LAND-mcp-testing-bridge.md` (research landscape, not partner-signed; treat as living per acting-head-of-board call)
7. `intent-eval-lab/000-docs/003-PP-PLAN-phase-b-scope-refinement.md` (synthesis, internal)
8. `audit-harness/000-docs/002-RR-LAND-upgrade-landscape.md`
9. `kobiton/CLAUDE.md`
10. `kobiton/000-docs/034-RR-OPEN-things-to-think-about.md`
11. `intent-eval-platform/CLAUDE.md` (umbrella)
12. Memory entries under `~/.claude/projects/-home-jeremy-000-projects-kobiton/memory/`

## Acting Head of Board declaration

I, **Claude (Anthropic, `claude-opus-4-7`)**, find that:
- All 7 ISEDC seats convened and returned adversarial structured assessments
- The user issued two direct overrides: Q5 timing ("fix it" → NOW) and Q4 scope ("nothing changes but the name" → rename only, no architectural concept addition)
- Decisions Q1, Q2, Q3 reflect council majority with stacked minority protections honored
- Decisions Q4 and Q5 reflect user override — council deliberation preserved in seat memos at `/tmp/claude-1000/-home-jeremy-000-projects-kobiton/40b51df0-3e65-4871-b87f-60c926aa6a00/tasks/`
- Execution proceeds in the same session per Q5 user override

Signed,
**Claude (Anthropic) — Acting Head of Board, ISEDC v2 2026-05-10**

## References

- ISEDC v1: `004-AT-DECR-isedc-council-record-2026-05-10.md` (predecessor; frozen)
- Reusable pattern: `~/.claude/skills/exec-decision-council/SKILL.md`
- Seat memos: `/tmp/claude-1000/-home-jeremy-000-projects-kobiton/40b51df0-3e65-4871-b87f-60c926aa6a00/tasks/` (CTO `ab3f8cb`, GC `a6112d25`, CMO `a96817e1`, CFO `aecb22e4`, CSO `a801764f`, CISO `a4617e81`, VP DevRel `a6ad7e33`)
