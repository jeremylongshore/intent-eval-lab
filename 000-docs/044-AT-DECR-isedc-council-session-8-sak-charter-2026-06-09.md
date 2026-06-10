---
date: 2026-06-09
acting_head_of_board: "Claude (acting, designated by Jeremy Longshore via CTO-mode delegation 2026-06-09)"
council_size: 7
seats: [CTO, GC, CMO, CFO, CSO, CISO, "VP DevRel"]
decisions_logged: 8
status: RATIFIED
bead: bd_000-projects-8vq0
session_dir: "~/.claude/skills/exec-decision-council/sessions/2026-06-09-sak-charter-session-8/"
pre_charter_audit: "workflow werie2zsv (37 agents) — GO-WITH-NOTES"
supersedes: none
reusable_pattern: "~/.claude/skills/exec-decision-council/SKILL.md"
---

# ISEDC Session 8 — Class-1 Charter for the Spec Authority Kernel (SAK)

## 1. Mission of this Decision Record

This DR ratifies the **kernel v0.4.0 authoring/v1 expansion** — the Spec Authority Kernel (SAK).
It is a Class-1 charter because it expands the NORMATIVE boundary of `@intentsolutions/core`,
sets a public marketplace-policy floor consumed by the CCP ecosystem (2000+ stars, 45k+ NPM),
and gates the six per-contract authoring schemas (`skill-frontmatter`, `plugin-manifest`,
`agent-definition`, `mcp-config`, `hook-config`, `marketplace-catalog`) plus Phases 1–5 of SAK.
Bead: `bd_000-projects-8vq0`.

## 2. Why a council, not a single review

The charter locks artifacts that are effectively permanent (published kernel schemas under
sigstore provenance; an immutable `authoring/v1` namespace; a public strict-tier policy). The
failure modes are asymmetric — a silently-realigned floor or a non-reproducible signed
attestation costs years of trust, not a revert. Seven seats argued from distinct value systems;
dissent was preserved; the acting head stacked minority constraints into the majority.

## 3. Pre-charter due diligence (audit-informed)

A cross-repo audit (workflow `werie2zsv`, 37 agents: per-repo consistency + code review +
adversarial blocker verification) returned **GO-WITH-NOTES**. The charter's locked surface — the
shipped marketplace-tier 4-fold `isMarketplace` foundation — was found **sound**: three
independent reviewers confirmed **zero** Zod↔JSON-Schema divergence across every boundary and
**zero** kernel P0/P1 correctness bugs; the 240-fixture corpus, scorecard, and integrity tests
reconcile. The notes (documentation drift + two audit-harness evidence-pipeline bugs) sit
**outside** the charter surface and are recorded below as binding follow-ups, not blockers.

## 4. Synthesis lenses

(1) the arena — APIs · CLIs · MCP servers · agents · SKILL.md; (2) both sides — client + server
eval; (3) the transformation pipeline — API → CLI → MCP → SKILL.md → agent; (4) composable
partial attestation — every component a valid entry, silence ≠ failure.

## 5. The questions

| #   | Question                                                                             | Why immutable / costly                                                                          |
| --- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| Q1  | Ratify the bicameral kernel (`schemas/authoring/v1/`) as permanent?                  | Expands the NORMATIVE boundary; hard to unwind once published as `@intentsolutions/core@0.4.0`. |
| Q2  | Ratify the IS marketplace tier (8-field set + IS extras) as canonical?               | Sets the public policy floor the CCP ecosystem validates against.                               |
| Q3  | Ratify a binding anti-realignment guard (`kernel-rubric-floor-guard.yml`)?           | Governs whether the strict tier survives drift; the 2026-04-28 debacle already happened once.   |
| Q4  | Ratify 6767-h as the upstream citation source?                                       | Couples schema evolution to a prose spec; load-bearing for coherence CI.                        |
| Q5  | Ratify Phase 0 sequencing (D4 wedge) as satisfied, unblocking Phases 1–5?            | Sequencing error cascades into validator cutover.                                               |
| Q6  | Ratify the Phase 4 advisory→blocking quorum-pin (99.5% + 30-day shadow)?             | Determines when the gate becomes blocking on the 3,044-file corpus.                             |
| Q7  | How does per-contract `requiredFields` specialization compose with the shared folds? | The modeling decision all 6 contracts inherit; wrong = re-author all 6.                         |
| Q8  | Single-source codegen vs hand-maintained parallel (design note #13)?                 | A divergent validator the agreement test misses ships a wire-contract mismatch.                 |

## 6. Council composition

| Seat      | Value system                                                                            |
| --------- | --------------------------------------------------------------------------------------- |
| CTO       | technical durability · schema integrity · immutability · future-proofing                |
| GC        | IP · partner-consent · license/brand-surface · audit-trail discipline                   |
| CMO       | positioning · narrative · first-mover authorship                                        |
| CFO       | sole-prop bandwidth · opportunity cost · scope discipline                               |
| CSO       | standards-body realpolitik (agentskills.io / in-toto / SLSA / OpenSSF) · RFC sequencing |
| CISO      | supply-chain attestation · signing · threat model · Rekor discipline                    |
| VP DevRel | developer-adoption · friction-to-adopt · the Saturday-afternoon-developer test          |

## 7. Per-question record (verbatim positions + decision)

### Q1 — Bicameral kernel permanent

**Vote: 7 RATIFY** (CMO + VP DevRel clean; CTO/GC/CFO/CSO/CISO with constraints).

| Seat      | Position (verbatim key)                                                                                                                                                      |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | "A kernel that lets authoring contracts live in an ad-hoc validator repo is a kernel with a leak." Bind read-only-immutable v1; `v2`-never-edit-`v1`; name the freeze event. |
| GC        | Better IP posture than scattered convention; bind **per-directory LICENSE + NOTICE** in `schemas/authoring/v1/` (external adopters `$ref`/vendor it).                        |
| CMO       | "Bicameral = we govern both what runs and how it's built — the sentence a category gets named after." Permanent chamber, not a fixed contract schedule.                      |
| CFO       | Don't pay twice for sunk cost; "permanent" = the **structure**, not a roadmap commitment to author all six on a clock.                                                       |
| CSO       | Permanent IFF the `6767h-coverage-map.json` ships and each chamber carries its own `$schemaVersion` lane; drop the "shadow of 6767-h" framing (it already collapsed).        |
| CISO      | Distinct **predicate-URI namespaces per chamber + no shared signing trust root**; shared code OK, shared trust root not.                                                     |
| VP DevRel | Best thing in the charter for developers: 16 partial validators → 1 canonical surface; bind a docs-parity gate.                                                              |

**DECISION (D1): RATIFY** the bicameral kernel as a permanent **structure**. Bind: (a) `authoring/v1`
is read-only-immutable — breaking change creates `authoring/v2`, never edits v1; the
draft→frozen event is named at first non-draft publish; (b) independent `$schemaVersion` lanes
per chamber; (c) distinct predicate-URI namespaces per chamber, no shared signing trust root;
(d) per-directory LICENSE + NOTICE; (e) "permanent" governs the structure, not a six-contract
schedule (authoring sequenced per D7); (f) the "machine-readable shadow of 6767-h" framing is
retired (the IS-extras have no upstream anchor).

### Q2 — IS marketplace tier canonical

**Vote: 7 RATIFY** (GC + VP DevRel with constraints).

| Seat      | Position (verbatim key)                                                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CTO       | The 8-field set is shipped + eval-proven; **version/author/license must stay required** — they are the attestation substrate (an unauthored artifact can't be signed).         |
| GC        | `license` is one of the eight required fields → **fix the glass house first**: don't enforce a required `license:` while consumer docs misstate our own licenses. (Gating.)    |
| CMO       | "The strict tier IS the whole brand; the delta from Anthropic's 2-field floor is the product; the differentiator must be the default."                                         |
| CFO       | Canonicalizes enforcement we already pay for over 3,543 files; the 4-fold split is **cost reduction** (independent changelogs).                                                |
| CSO       | Ratify — additive strictness, "a strict PROFILE of an open standard, the way SLSA L3 sits on in-toto without forking it."                                                      |
| CISO      | `allowed-tools` and `license` are **security fields, not metadata**; securityChecks must scan the **populated** `allowed-tools` value, not just assert presence.               |
| VP DevRel | Strictness must **teach**: every required-field rejection emits a one-line "why" + a copy-pasteable fix; keep lower tiers (`openStandardCompliant`/`standardFloor`) reachable. |

**DECISION (D2): RATIFY** the IS marketplace tier as canonical. Bind: (a) `version`/`author`/
`license` stay required; (b) **gating precondition** — reconcile consumer-doc license drift
(standing condition) before the kernel enforces a required `license:` field; (c) error messages
teach (why + fix); lower tiers remain reachable; (d) securityChecks evaluates the populated
`allowed-tools` value; (e) external adopters may `$ref` `requiredFields` alone.

### Q3 — Binding anti-realignment guard ⟵ TOP most-costly (3 seats)

**Vote: 7 RATIFY** (CSO + VP DevRel with framing constraints).

| Seat      | Position (verbatim key)                                                                                                                                                                      |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | "A floor that lives only in docs is not a floor." At minimum the guard fails on any shrink of the 8-field set or removal of a fold.                                                          |
| GC        | "Every silent realignment is a silent breach of the representation we made." Failure message must cite the governing ADR. Ratify first, hardest.                                             |
| CMO       | "A promise that can be silently weakened is not a promise, it's a vibe." Won't trade; additive = lightweight, subtractive = Class-1.                                                         |
| CFO       | "One YAML file, ~0.25 FTE-day — the cheapest insurance in the charter against the most expensive failure on record."                                                                         |
| CSO       | **Framing veto**: the guard locks "the IS-profile floor," it cites the IS rubric and **zero adversaries** — never "resist Anthropic." "The first impression with a maintainer is permanent." |
| CISO      | **Self-pin the guard** in `.harness-hash` so it can't be weakened in the same PR that weakens the floor.                                                                                     |
| VP DevRel | Frame as **stability** — "this floor doesn't move under you between releases" — not "we're stricter than Anthropic" (that reads as ego).                                                     |

**DECISION (D3): RATIFY** the anti-realignment guard. Bind: (a) the guard self-pins in
`.harness-hash`; (b) subtractive changes to the required-set or error-vs-warning semantics =
Class-1 ADR, additive = lightweight; (c) the failure message cites the governing ADR **and** the
developer harm. **Framing resolution (CMO ↔ CSO/VP DevRel): the guard, its CI, and all
developer-facing copy use neutral "lock the IS-profile floor / this floor does not move under
you" language and NEVER name Anthropic as an adversary — CSO holds phrasing veto. CMO may
celebrate strictness in the marketing site/deck only, never in CI or error strings.**

### Q4 — 6767-h as upstream citation source

**Vote: 7 RATIFY** (5 with constraints).

| Seat      | Position (verbatim key)                                                                                                                                                                                        |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | 6767-h cites fields that **have** an upstream analog; IS-extras cite the IS-extras catalog, never 6767-h; add a citation-currency CI check.                                                                    |
| GC        | **On the record:** 6767-h ships `license: "MIT"` as its frontmatter example (line 140), contradicting the Apache-2.0 standard it anchors — **fix before citing it as canonical**; scope 6767-h to floors only. |
| CMO       | Provenance story makes us a standards author not a schema scraper — but mirror the `schema-drift.yml` pattern so provenance is verifiable, not asserted.                                                       |
| CFO       | The `6767h-coverage-map.json` (field → section OR IS-extra rationale) is a **blocking precondition** to any "6767-h is canonical" claim.                                                                       |
| CSO       | Textbook provenance hygiene; the deterministic `prose-anchor-validity.yml` (pinned markdown-it, no LLM) makes citation trustworthy not decorative.                                                             |
| CISO      | A citation is **prose, never a runtime resolution** — no validator/`$ref`/CI may live-fetch 6767-h (same discipline as the `labs.*` predicate-URI binding).                                                    |
| VP DevRel | Schema `$comment` must be **self-sufficient** without the 6767-h clone; the citation is a deeper-dive pointer.                                                                                                 |

**DECISION (D4): RATIFY** 6767-h as the citation source, scoped. Bind: (a) 6767-h authors the
**floors only**; IS-extras are first-party-authored with no upstream anchor claimed; (b) ship
`6767h-coverage-map.json` (blocking precondition to any canonical claim); (c) `prose-anchor-
validity.yml` deterministic CI fails on dangling citations; (d) citation is by stable heading,
never reproduced content, never a runtime/network resolution; (e) `$comment` self-sufficient.
**Correction directive: fix 6767-h's `license: "MIT"` example (line 140) → `Apache-2.0`/placeholder.**

### Q5 — Phase 0 sequencing satisfied

**Vote: 7 RATIFY** (CISO with constraints).

| Seat      | Position (verbatim key)                                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CTO       | The foundation shipped + passed a clean eval; "empirical evidence > authorship claims, and the evidence is on the board." Phase 1 doesn't start until the standing-condition doc drift is fixed. |
| GC        | Record "satisfied" with the evidencing commit/bead so the unblock is auditable.                                                                                                                  |
| CMO       | "The foundation already shipped" is the strongest launch posture; gate the **public announcement** on the doc-drift fix.                                                                         |
| CFO       | Conditional on D4 wedge (CCP PR #788) merging clean.                                                                                                                                             |
| CSO       | Nothing in Phase 0 commits an immutable artifact; low-risk to unblock.                                                                                                                           |
| CISO      | **No signed evidence may be published from any phase until both audit-harness evidence bugs are fixed and re-verified** — a separate publication gate; STAGING-STAYS-STAGING.                    |
| VP DevRel | Procedurally sound; no developer-facing surface change.                                                                                                                                          |

**DECISION (D5): RATIFY** Phase 0 satisfied; unblock Phases 1–5. Bind: (a) record satisfaction
with the evidencing commit/bead; (b) the D4 wedge (CCP PR #788) merges clean (reopens if it
surfaces problems); (c) reconcile the doc-drift standing condition before public announcement /
Phase 1 consumer-facing work; (d) **no `rekor_production` signed-evidence publication until the
two audit-harness evidence bugs are fixed + re-verified — STAGING-STAYS-STAGING.**

### Q6 — Phase 4 advisory→blocking quorum-pin ⟵ 2nd most-costly (CFO, VP DevRel, + CISO/Rekor)

**Vote: 7 RATIFY-WITH-CONSTRAINTS.**

| Seat      | Position (verbatim key)                                                                                                                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | **Deterministic fold agreement must be 100%** — a 0.5% band on deterministic schema checks is a future incident; the band covers only non-deterministic surfaces; the shadow ceiling is a ceiling, not a floor. |
| GC        | Archive the agreement metric + shadow log as DR artifacts; the flip is a liability-posture change; make it overrideable via a one-line ADR.                                                                     |
| CMO       | Publish the false-reject rate before flip; add a **fast-path appeal lane** for the residual ~0.5% so a false-block is a 1-hour annoyance, not a 1-tweet incident.                                               |
| CFO       | **Convert the 30-day ceiling from "flip anyway" to a governance-triple (CFO+CISO+VP DevRel) re-evaluation trigger** — on a one-engineer shop a calendar ceiling manufactures urgency.                           |
| CSO       | **Rekor rollback = append-only SUPERSESSION (`signing_mode: rolled-back-superseded`), never mutation**; shadow ends on **disposition-completeness**, not the calendar.                                          |
| CISO      | **securityChecks blocks DAY-0**, exempt from the shadow — "a `$(...)` in a name field is RCE-adjacent"; quality folds shadow, security folds block on arrival.                                                  |
| VP DevRel | **Deprecation warnings at 30-day-out and 7-day-out in the advisory output itself** + a changelog/blog on flip day — "the flip is fine; the surprise is the enemy."                                              |

**DECISION (D6): RATIFY-WITH-CONSTRAINTS.** Bind the full stack: (a) deterministic fold agreement
= 100%; the 0.5% tolerance applies only to non-deterministic predicate surfaces; (b) the
`securityChecks` fold blocks day-0, exempt from the shadow period; (c) the 30-day ceiling is a
governance-triple re-evaluation trigger (flip / extend / park), not an auto-flip; shadow exits on
disposition-completeness; (d) Rekor rollback via append-only supersession, never mutation;
(e) deprecation warnings at 30/7-day-out in advisory output + flip-day changelog + a published
fast-path appeal lane; (f) archive the agreement metric, shadow log, and false-reject rate as DR
artifacts, published before the flip.

### Q7 — Per-contract requiredFields specialization (RATIFY-BEFORE-AUTHORING)

**Vote: 7 converge** on: override `requiredFields` per-contract; inherit the three universal folds.

| Seat      | Position (verbatim key)                                                                                                                                                                                                                                                                                                             |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | "The shipped `isMarketplace` $def is **skill-frontmatter's** composition, not the universal one." Refactor: foundation exposes the 3 universal folds + a parameterizable composition; skill-frontmatter applies skill `requiredFields`. REJECTS "every contract inherits skill-requiredFields" (provably wrong vs plugin-manifest). |
| GC        | Override requiredFields; **universal folds uniform across all 6 — contracts may ADD, never SUBTRACT**; guard pins each profile + asserts universal-fold presence.                                                                                                                                                                   |
| CMO       | Override + inherit; floor-guard carries a **per-artifact canonical registry**; no-subtraction-of-universal-folds is non-negotiable.                                                                                                                                                                                                 |
| CFO       | Override + inherit AND **sequence**: author skill-frontmatter now, the other 5 on-demand behind a one-line CFO sign-off (not a new convening); composition binding for all 6.                                                                                                                                                       |
| CSO       | `allOf` is **monotonic-additive** — a profile can only ADD to the upstream base, never loosen it; add a per-contract `upstream-shape-conformance.yml` test.                                                                                                                                                                         |
| CISO      | **`securityChecks` is UNIVERSAL-IMMUTABLE** — never overridable; CI meta-test asserts its `$ref` is present (by reference, not copied) in all 6.                                                                                                                                                                                    |
| VP DevRel | Inline human-readable `$comment` effective-required manifest per contract ("REQUIRED HERE / INHERITED"), **generated not hand-typed** — answer "what does this require?" from one file.                                                                                                                                             |

**DECISION (D7): RATIFY** the composition model — each per-contract schema **overrides
`requiredFields`** and **inherits the three universal folds** (`deprecationRegistry`,
`securityChecks`, `disclosureMarkers`) via `allOf` `$ref` to a single shared `$defs`. Bind:
(a) refactor the foundation to expose the 3 universal folds independently + give skill-frontmatter
its own `requiredFields` (a draft-window edit, before contract #2); (b) **`securityChecks` is
universal-immutable** — add-only, never subtract; (c) a structural/meta CI test asserts every
contract `$ref`s the 3 shared folds (by reference, not inline copy) + defines its own
`requiredFields`; (d) a per-contract upstream-shape-conformance test (monotonic-additive proof);
(e) an inline generated `$comment` effective-required manifest per contract. **Sequencing: the
composition spec is binding for all six; authoring is sequenced — skill-frontmatter first, the
remaining five on-demand behind a lightweight CFO bandwidth sign-off (not a new ISEDC convening).**

### Q8 — Single-source codegen vs hand-maintained parallel

**Vote: 6 MANDATE codegen / 1 defer (CFO).**

| Seat      | Position (verbatim key)                                                                                                                                                               |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | Mandate codegen — "zero divergence today is not evidence the parallel approach scales; it's evidence we haven't hit the 6× multiply yet." Hard tripwire at contract #3 if not before. |
| GC        | Mandate as a precondition to contracts 2–6; contract #1 grandfathered behind the fold-agreement test.                                                                                 |
| CMO       | Mandate; gate on contract #2 — "the product promise (Q3) and the maintenance model (Q8) must agree."                                                                                  |
| CFO       | **Dissent: keep parallel, defer codegen to contract #3** (the amortization crossover); "you don't build the factory to produce one unit."                                             |
| CSO       | Mandate; **JSON Schema is the single source** (standards-native, citable); reuse the existing `codegen:validators` pattern.                                                           |
| CISO      | Mandate — "a divergent validator is a confused-deputy attack surface; prevention beats detection for a security boundary."                                                            |
| VP DevRel | Mandate as steady state; codegen keeps the Q7 inline manifest + docs honest; parallel is never "forever."                                                                             |

**DECISION (D8): RATIFY — MANDATE single-source codegen** (majority 6–1). **JSON Schema is the
single source of truth**; Zod validators + the D7 inline `$comment` manifests are generated from
it; the fold-agreement test + a doc-parity test are retained as the regression backstop, not the
primary control. **Trigger (resolving CSO/CISO "now" vs CFO "#3"): codegen is a hard precondition
of authoring contract #2.** Contract #1 (skill-frontmatter, the already-shipped hand-authored
foundation refactor) is grandfathered behind the existing fold-agreement test. No second authoring
contract ships dual-maintained. (CFO's "don't build the factory for one unit" is honored — #1
grandfathered; the 6-seat mandate is honored — codegen lands before the multiply, which begins at #2.)

## 8. Council memos — cross-question themes (verbatim "most costly to recover from")

- **CTO → Q8:** "A silent Zod↔JSON-Schema divergence shipped under sigstore provenance across six immutable `authoring/v1` contracts is the one failure that is unrecoverable in place."
- **GC → Q3:** "A silent realignment of the strict tier is invisible by construction — that is the breach you discover in discovery."
- **CMO → Q3:** "Q3's worst case is the quiet death of the thing that made us a category instead of a redistributor."
- **CFO → Q6:** "Unbuilt codegen costs us nothing to recover from. A bad signed attestation on the append-only Rekor log costs us forever."
- **CSO → Q3 (framing):** "The technical artifacts are append-only-recoverable. The relationship is not."
- **CISO → evidence-bugs/Rekor:** "A signed attestation written to the public Rekor log is, by design, immutable — once we publish an entry whose `input_hash` is the empty-string SHA, that false-assurance record is permanent. That is the one decision with no undo."
- **VP DevRel → Q6:** "You only get one first impression of 'the vendor broke my build' — bind the deprecation-warnings constraint or record my dissent: the flip ships with a countdown, not a surprise."

## 9. Cross-cutting themes

**Most-costly tally:** Q3 ×3 (GC, CMO, CSO) · Q6 ×2 (CFO, VP DevRel) · Q8 ×1 (CTO) · evidence-bugs/
Rekor ×1 (CISO, ≈ the Q5/Q6 publication-immutability gate). The two slowest-adjudicated decisions —
**Q3 (the anti-realignment guard, especially its framing)** and **Q6 (the flip + Rekor
immutability)** — carry the heaviest stacked constraints.

**Adversarial integrity — PRESERVED.** Live, unpapered clashes: CMO (strict-tier-as-brand-flex)
vs CSO + VP DevRel (neutral-stability framing) on Q3 — resolved by venue-splitting the copy.
CFO (sequence + defer) vs CMO/CSO (complete standard now) on Q7/Q8 — resolved as specified-for-six,
built-incrementally, codegen-before-#2. CISO vs CTO on shared trust root (Q1) and uniform fold
treatment (Q6/Q7) — resolved toward CISO (distinct namespaces; securityChecks day-0 +
universal-immutable). CISO introduced a novel binding (securityChecks UNIVERSAL-IMMUTABLE) no
other seat raised.

**How the lenses landed:** CSO grounded the `allOf` monotonic-additivity property as the
_structural_ proof of the "strict profile ON TOP of agentskills.io, never a fork" posture (lens 1:
each arena surface gets its own base+profile pair; lens 4: each contract validates independently,
silence ≠ failure).

## 10. Implementation directives

| #    | Directive                                                                                                                                                                                                                                                         | Owner seat                      | Where                                  |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | -------------------------------------- |
| ID-1 | Refactor the foundation: expose the 3 universal folds independently; skill-frontmatter gets its own `requiredFields`; `securityChecks` marked universal-immutable (D7)                                                                                            | CTO + CISO                      | intent-eval-core                       |
| ID-2 | Build single-source codegen (JSON Schema → Zod + `$comment` manifests); hard precondition of contract #2 (D8)                                                                                                                                                     | CTO                             | intent-eval-core                       |
| ID-3 | Author `kernel-rubric-floor-guard.yml` — self-pinned, ADR-citing, neutral framing (D3)                                                                                                                                                                            | CTO + CISO + CSO (framing veto) | intent-eval-core                       |
| ID-4 | Ship `6767h-coverage-map.json` + `prose-anchor-validity.yml`; fix 6767-h `license: MIT` example (D4)                                                                                                                                                              | GC + CSO                        | claude-code-plugins + intent-eval-core |
| ID-5 | Phase 4 flip mechanics: deterministic-100% / securityChecks-day-0 / 30-day-governance-triple-trigger / Rekor-supersession / deprecation-warnings / archived shadow log (D6)                                                                                       | CISO + CFO + VP DevRel          | audit-harness + intent-eval-core       |
| ID-6 | **Binding follow-up:** fix the two audit-harness evidence bugs (escape-scan stdin triple-read; emit-evidence `policy_hash` newline-trim) + regression tests; **rekor_production gated on the fix — STAGING until re-verified**                                    | CISO                            | audit-harness                          |
| ID-7 | **Standing condition:** reconcile the 4 charter-premise facts (kernel 0.3.1→0.4.0; Apache-2.0 ecosystem-wide; 5-repo taxonomy incl. the kernel; canonical repo names) in consumer README/CLAUDE.md across all 5 repos, before public announcement (D2 gating, D5) | CMO + GC                        | all 5 repos                            |
| ID-8 | Author the 6 per-contract schemas — skill-frontmatter first; the other 5 on-demand behind a lightweight CFO sign-off (D7)                                                                                                                                         | CTO + CFO                       | intent-eval-core                       |

## 11. Reusable pattern reference

ISEDC pattern: `~/.claude/skills/exec-decision-council/SKILL.md`. This session paired the council
with a **pre-charter cross-repo audit workflow** (37 agents, GO-WITH-NOTES) whose findings seeded
three of the eight questions (Q7 from the schema-policy eval; Q8 from design note #13; the
evidence-bug + doc-drift directives from the audit). That audit-then-charter sequence — validate
the foundation empirically, then convene the council with evidence in hand — is reusable for any
Class-1 charter over already-shipped architecture.

## 12. Acting head of board declaration

All 8 decisions are **RATIFIED** as recorded, with every minority constraint stacked into the
majority (no dissent dismissed; VP DevRel's Q6 countdown constraint and CFO's Q6 governance-trigger
constraint are both binding; CFO's lone Q8 defer-dissent is recorded and overridden in favor of the
6-seat codegen mandate, softened by grandfathering contract #1 and triggering only at contract #2).

The charter (`bd_000-projects-8vq0`) is convened and closed; the six per-contract schema beads are
unblocked **for sequencing** per D7 (skill-frontmatter first), not for simultaneous authoring.

_Signed: Claude, Acting Head of Board, designated by Jeremy Longshore via CTO-mode delegation, 2026-06-09._

## 13. References + provenance

- Session JSONL (source of truth): `~/.claude/skills/exec-decision-council/sessions/2026-06-09-sak-charter-session-8/session.jsonl`
- Pre-charter audit: workflow `werie2zsv` (37 agents, GO-WITH-NOTES)
- SAK plan: `000-docs/033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md` §14
- Schema-policy eval (surfaced Q7): `intent-eval-core/000-docs/008-AA-EVAL-schema-policy-marketplace-tier-2026-06-09.md`
- Shipped foundation: `intent-eval-core/schemas/authoring/v1/marketplace-tier.schema.json` + `src/validators/v1/authoring/marketplace-tier.ts` (PRs #23/#24/#25)
- Prior DRs: DR-010 (Session 4), DR-018 (Session 5), DR-028 (Session 7)
