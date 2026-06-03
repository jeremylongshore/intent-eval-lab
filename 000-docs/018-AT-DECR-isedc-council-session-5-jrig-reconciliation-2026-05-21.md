# ISEDC Session 5 — j-rig Kernel-Adoption Normative Reconciliation

**Filing**: 018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-21.md
**Date**: 2026-05-21
**Acting Head of Board**: Claude (designated by Jeremy Longshore on 2026-05-21 via the IEP Convergence Debt Plan execution directive: "be the ceo i am counting on u to make the roght call no shortcuts")
**Council size**: 7 seats (standard IS roster — CTO · GC · CMO · CFO · CSO · CISO · VP DevRel)
**Decisions logged**: Q1(a), Q1(b), Q1(c), Q2
**Status**: RATIFIED 2026-05-21 (this document is the record)
**Bead**: `bd_000-projects-XXXX` (iep-isedc-session-5-jrig-reconciliation, P0, feature) — to be filed alongside this document
**Cluster**: iep-P1-kernel-adoption (`bd_000-projects-6hd6`)
**Master plan**: `~/.claude/plans/se-the-council-bubbly-frog.md` + IEP Convergence Debt Plan (2026-05-20 enhanced 2026-05-21)
**Synthesis input**: `intent-eval-lab/000-docs/016-RR-LAND-kernel-shadow-inventory-2026-05-20.md` + `017-RR-LAND-shape-reconciliation-addendum-2026-05-21.md`
**Reusable pattern**: `~/.claude/skills/exec-decision-council/SKILL.md` (Decision Record template)
**Class**: 2 (cross-consumer architectural ripple + breaking change to OSS-published API surface)

---

## 1. Mission of this Decision Record

Adjudicate the operational posture for bringing `j-rig-binary-eval` into compliance with the kernel's normative `gate-result/v1` predicate contract (Blueprint B § 7.4) and the umbrella unification thesis (DR-010 Q3 BINDING). The direction was settled by prior Decision Records; what required adversarial review was: (a) version-bump policy, (b) re-emission posture for existing v0.1.0-draft-shape attestations, (c) migration sequencing + release-note posture, and (d) where wire-format authority lives when the kernel and a consumer operate at different abstraction layers.

The 7-seat adversarial council produced verbatim positions across both questions; the Acting Head of Board makes the calls below after weighing steel-manned minority positions, and absorbs minority binding constraints into the final decision rather than dismissing them.

## 2. Why a council, not a single review

- **Immutability surface**: the kernel's `gate-result/v1` URI is permanent once attestations land in production-Rekor; the wire-format schema's growth in kernel v0.2.0 is also effectively permanent.
- **Breaking-change radius**: `@j-rig/*` v2.0.0 ripples to every downstream adopter; first-impression posture is permanent search-engine history per VP DevRel.
- **Standards-body realpolitik**: a clean predicate-spec migration looks good on the in-toto / SLSA / SIG-GenAI timeline; a sloppy one looks bad and propagates across future filings per CSO.
- **Adversarial value-tradeoff**: CMO momentum vs CFO bandwidth · CSO community-temp vs CMO announcement · CISO threat-model vs CTO schema-elegance · GC audit-trail vs everyone — all live tensions.

## 3. Synthesis lenses applied

1. **The arena (5 surfaces)**: APIs · CLIs · MCP servers · agents · SKILL.md
2. **Both sides**: client-side eval + server-side eval
3. **The transformation pipeline**: API → CLI → MCP → SKILL.md → agent
4. **Composable partial attestation**: every component is a valid entry; silence ≠ failure

## 4. Questions verbatim

| #   | Question                                                                                                                                                                                                                                                                                                          | Why immutable / costly                                                                                                                                         |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Q1  | Should j-rig migrate its local `GateResultPredicateSchema` to import + re-export kernel's normative `GateResultV1` shape? Sub-decisions: (a) major version bump for `@j-rig/*`; (b) re-emission vs staging-stays-staging for existing v0.1.0-draft attestations; (c) migration sequencing + release-note posture. | Direction binding (DR-010 Q3). What's adjudicated: SemVer/Rekor/community-posture choices that propagate permanently into npm + Rekor + standards-body memory. |
| Q2  | Kernel `EvidenceBundle` wire-format growth. Three options: Option α (kernel adds `EvidenceBundlePayload` + folds j-rig's `EvidenceStatement` row shape + cross-field invariants; j-rig re-exports); Option β (j-rig renames locally; no kernel change); Option γ (kernel adopts j-rig's wire format).             | Kernel contract-surface expansion is effectively immutable for the platform's lifetime; same immutability discipline as `gate-result/v1`.                      |

## 5. Council composition

| Seat                                          | Value system                                                                                                         | Bias                                                                                                                          | Typical adversaries |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| **CTO / Chief Architect**                     | Schema integrity · immutability · future-proofing                                                                    | Deliberation > commit; empirical evidence > authorship claims; kernel-canonical                                               | CMO, CSO, CFO       |
| **GC / General Counsel**                      | IP protection · partner-consent · audit-trail discipline · trademark/brand                                           | Paper trail is sacrosanct; written consent before any partner reference; license-boundary drift is tort risk                  | CMO, CSO, CFO       |
| **CMO / Industry-Standard Strategist**        | Positioning · narrative coherence · tagline alignment · first-mover authorship                                       | Visible > silent; ambitious > conservative; frontier > operational                                                            | GC, CFO, CSO        |
| **CFO / Strategic Operator**                  | Sole-prop bandwidth · opportunity cost · customer-signal gating (REMOVED per DR-010 § 13.5 — pure bandwidth posture) | Defer until evidence; standards-body filings NOT costless; minimum-scope-that-satisfies-binding                               | CMO, CSO, CTO       |
| **CSO / Chief Standards Officer**             | OTel SIG-GenAI / in-toto / SLSA / CNCF / OpenSSF / AgentSkills.io realpolitik · RFC sequencing                       | Community-temperature ALWAYS precedes RFC filing; first-impression with maintainer is permanent                               | CMO, CFO            |
| **CISO / Chief Information Security Officer** | Supply-chain attestation integrity · sigstore / cosign / Rekor / DSSE / in-toto · threat-model                       | Once a row is in Rekor production, permanent forever; cryptographic identity proofs only as strong as their underlying schema | CTO, CMO, CFO       |
| **VP DevRel / Head of OSS Community**         | Developer-audience signal · OSS contribution dynamics · friction-to-adopt                                            | "Saturday-afternoon-developer-tries-the-thing" test; informal > formal; reputation is permanent search-engine history         | GC, CMO             |

Acting Head of Board: Claude (designated by Jeremy Longshore for this session).

## 6. Per-question record

### 6.1 Q1(a) — Major version bump for `@j-rig/*`

**Vote tally**: 7/7 YES (unanimous).

**Verbatim positions** (paraphrased; full verbatim seat returns archived in session transcript):

- **CTO**: "SemVer exists precisely to communicate 'your import surface changed.' Hiding this in a minor would be a worse violation of the contract than the breaking change itself. Major bump — `@j-rig/core` and `@j-rig/rollout-gate` both go to `2.0.0`. Single coherent PR, not phased."
- **GC**: "The major version bump is non-negotiable from a contract & audit-trail standpoint. Every attestation signature in production today is a legal artifact: if we change the wire format without a version boundary, we've silently invalidated the contract-of-meaning every consumer relied on."
- **CMO**: "This is not a migration. This is a launch event… The j-rig v0.x → v2.0 cut is the first public proof that the unification thesis (DR-010 Q3) is real."
- **CFO**: "Major version signals to the ecosystem 'this is a breaking change for good reason'… smallest version bump that closes the gap cleanly — major if required, but only if we're honest this is a one-time correction, not a pattern."
- **CSO**: "Major-bump `@j-rig/*` to mark the implementation boundary… Frame the entire migration as conformance achievement, not defect remediation."
- **CISO**: "v2.0 starts a new signing lineage from tag `v2.0.0`." (Implicit major-bump endorsement; deciding seat for Q1(b) — see below.)
- **VP DevRel**: "Major version bump. Yes."

**Primary tension**: None. Unanimous.

**DECISION**: `@j-rig/core@2.0.0`, `@j-rig/rollout-gate@2.0.0`, `@j-rig/cli@2.0.0`, `@j-rig/db@2.0.0`, `@j-rig/dashboard@2.0.0`. All workspace packages bump to v2.0.0 together to preserve the workspace consistency that j-rig's pnpm monorepo discipline enforces.

**Rationale**: SemVer-correct signal. Direction was binding (DR-010 Q3); the magnitude of the breaking change (field rename, +5 required fields, decision-enum value-set change) is unambiguous breaking-change semver territory.

**Dissent acknowledged**: none.

---

### 6.2 Q1(b) — Existing v0.1.0-draft-shape attestations: re-emit vs staging-stays-staging

**Vote tally**: 6/7 STAGING-STAYS-STAGING; 1/7 dissent (CMO wants re-emit but explicitly defers to CISO's authority on the cryptographic call).

**Verbatim positions**:

- **CISO (deciding seat)**: "Existing j-rig rows are in `sigstore_staging` precisely because DR-010 Q3 made production-Rekor a per-predicate unlock gated on SPEC.md normative + DNSSEC + CAA — none of which have cleared for j-rig's predicate yet. Staging rows are exactly what they say they are: experimental, expirable, non-load-bearing. Re-emitting them would (a) burn signing infrastructure on rows that will age out anyway, (b) create a second set of staging rows that look authoritative but aren't, and (c) muddy the audit trail by implying historical conformance that didn't exist."
- **CSO**: "Staging-stays-staging. **No re-emission.**… Re-emitting historical attestations into the new shape would burn signing infrastructure on rows that will age out anyway, and double the public Rekor footprint of a transitional period that we are otherwise allowed to leave behind quietly."
- **CTO**: "Attestations signed against the v0.1.0-draft shape are in `sigstore_staging` — not production Rekor. Staging is the answer to staging. Re-emission cost = near-zero." (Concedes CISO has the call on carve-out language.)
- **CFO**: "Aligns with CISO; bandwidth-driven but final answer matches CISO."
- **GC**: "Defensible either way; accepts compromise of staging-stays-staging in maintenance mode if CISO supports."
- **VP DevRel**: "Staging-stays-staging. Historical v1 attestations remain v1-signed; v2 starts a new signing lineage from tag `v2.0.0`. No re-signing."
- **CMO** (lone dissent): "My vote is re-emit staging attestations against v2 shape — the unification story requires a clean corpus." But explicitly: "I yield to CISO on Q1(b) cryptographic specifics."

**Primary tension**: CMO's "clean corpus for narrative" vs CISO/CSO's "honest audit trail; don't pollute Rekor."

**DECISION**: **STAGING-STAYS-STAGING**. Per CISO's authority on the cryptographic call (this was explicitly her call per the council framing) and the 5-seat majority's structural endorsement. Existing `sigstore_staging` j-rig rows age out per Rekor's normal retention; **no re-emission**. New j-rig v2.0+ attestations conform to the kernel's normative shape and are eligible for production-Rekor promotion only after the per-predicate gate (SPEC.md normative + DNSSEC + CAA verified for `evals.intentsolutions.io`) clears.

**CISO carve-out** (binding): if forensics finds any j-rig rows that were promoted from `sigstore_staging` to production-Rekor before this DR (expected count: zero), those rows get re-emitted under the new shape AND the old rows get a Rekor-recorded supersession entry. Production-Rekor rows are permanent; the platform cannot leave a non-conformant production row standing. The forensics check is a pre-merge gate on the j-rig v2.0.0 PR.

**CMO binding minority constraint absorbed**: the staging-stays-staging decision MUST be public. Release notes state explicitly: "v2.0 introduces the normative predicate shape per Blueprint B § 7.4; staging-tier attestations emitted by prior versions are non-conformant by design and will age out of the staging log." No silent transition.

**Rationale**: CISO's structural argument is correct — the `signing_mode` field in `EvidenceBundle` (`sigstore_staging | rekor_production | unsigned_experimental`) is already the mechanism the platform uses to encode this exact distinction. Staging-stays-staging is a structural feature, not a workaround. CMO's "clean corpus" argument is steel-manned but the cost-benefit doesn't justify polluting the staging log to satisfy a narrative concern that's more honestly addressed in release notes.

**Dissent acknowledged**: CMO's dissent is preserved verbatim. The "clean corpus" framing has merit when production-Rekor entries are involved; the carve-out above absorbs exactly that concern.

---

### 6.3 Q1(c) — Migration sequencing + release-note posture

**Vote tally**: substantive agreement across all seats on most sub-decisions; specific compromises absorbed where needed.

**Verbatim positions** (synthesized — every seat returned a position on this sub-question):

- **CTO**: "Single coherent PR — kernel-import + schema re-export + all internal call-site migrations + CHANGELOG.md 'BREAKING' entry — not phased."
- **GC**: "Decision Record captures _why_ we broke the contract, _when_, _what changed_. Release notes must cite Blueprint B § 7.4 by name."
- **CMO**: "Headline reads 'j-rig v2 now speaks the kernel's language — one Evidence Bundle, every gate.'"
- **CFO**: "Release notes are one clear statement: 'j-rig v2.0.0 aligns predicate-body format to Blueprint B § 7.4 NORMATIVE spec. Consumers must update schema handling. Migration guide: [link].'"
- **CSO**: "Community-temperature post to SIG-GenAI + OpenSSF Securing AI WG _before_ any external blog… blog/X only after one full week of list silence-or-engagement."
- **CISO**: "Release notes state plainly: 'v2.0 introduces the normative predicate shape per Blueprint B § 7.4; staging-tier attestations emitted by prior versions are non-conformant by design and will age out of the staging log.'"
- **VP DevRel**: "Migration package: (i) CHANGELOG.md with verbatim before/after JSON blocks for every renamed field; (ii) MIGRATION.md with a field-rename table; (iii) `j-rig migrate <dir>` codemod that rewrites consumer fixture files and emits a diff; (iv) `j-rig@1.x` gets a deprecation notice on install (postinstall script, one-time, npm-friendly); (v) 90-day sunset window during which 1.x receives security patches only."

**Primary tensions**:

1. CMO ("announce loudly, narrate") vs CSO ("community-temperature before announcement").
2. VP DevRel ("codemod is mandatory; saves five hours of GH Issue triage") vs CFO ("codemod = bandwidth tax we can't afford").
3. GC ("cite Blueprint B § 7.4 by name in release notes") vs CMO ("cite the unification narrative first").

**DECISION (synthesized)**:

**Single coherent PR.** kernel-import + schema re-export + all internal call-site migrations + CHANGELOG.md "BREAKING" entry land together. No phased schema-transition period. No deprecated-but-still-emitted alias. Per CTO, CFO, GC, CMO consensus.

**Release-note structure** (verbatim ordering required):

1. `## Breaking changes` (CHANGELOG.md opens with this — VP DevRel binding)
2. Verbatim before/after JSON blocks for every renamed field (VP DevRel)
3. Field-rename table (`result` → `gate_decision`, `timestamp` → `evaluated_at`)
4. New required fields enumeration (`gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref`)
5. Decision-enum value-set delta (`PASS|FAIL|ADVISORY|NOT_APPLICABLE` → `pass|fail|advisory|error` with NOT_APPLICABLE encoded via `coverage.dimensions_skipped` per Blueprint B § 7.4 line 832)
6. Conformance framing (CSO): "j-rig v2.0 is the first conformant implementation of the kernel's normative `gate-result/v1` predicate per Blueprint B § 7.4. Predicate URI `https://evals.intentsolutions.io/gate-result/v1` is unchanged and immutable per Blueprint B § 7.2."
7. Staging-stays-staging notice (CISO binding): "Staging-tier attestations emitted by prior versions are non-conformant by design and will age out of the staging log. New v2.0+ attestations conform to the normative shape."
8. Citation: "Schema authority: Blueprint B § 7.4 NORMATIVE; canonical type at `@intentsolutions/core/predicates/gate-result-v1`." (GC binding)

**MIGRATION.md** (separate file at j-rig repo root):

- Field-rename table
- Worked example: a v1 row + the same row in v2 form
- Cross-link to a worked example repo if codemod isn't shipped at v2.0.0

**`j-rig migrate <dir>` codemod**: TARGETED as P1 bead. SHIPS WITH v2.0.0 IF BANDWIDTH PERMITS. If not in initial cut, fallback compromise (VP DevRel accepted): MIGRATION.md + a worked example repo `j-rig-v2-migration-example/` showing the diff on a real fixture. The codemod stays a P1 backlog item, NOT P3. CFO bandwidth concern absorbed: codemod is engineering-hour-saver via reduced GH Issue triage load — it pays for itself.

**j-rig 1.x sunset**: 90-day window after v2.0.0 release. v1.x receives security patches only. One-time postinstall deprecation notice (npm-friendly; not console.warn on every import — VP DevRel binding). At sunset, v1.x is marked deprecated on npm.

**Announcement sequencing** (CSO/CMO compromise — IN PARALLEL, not in series):

- Week 0 (release day): kernel v0.2.0 (with `EvidenceBundlePayload` per Q2 below) ships first → j-rig v2.0.0 ships → community-temperature posts to in-toto SIG-GenAI + OpenSSF Securing AI WG go up SAME WEEK (CMO compromise absorbed: parallel, not in series).
- Week 1: monitor list responses; engage as a contributor, not as a vendor (CSO posture).
- Week 1+: blog/X posts on `startaitools.com` per CMO. Headline framing per CMO: "j-rig v2 now speaks the kernel's language" or equivalent. NO partner-name references per DR-004 S1Q2 (vendor-generic enforced by CI guard — GC binding).

**Partner-consent discipline** (GC binding, already standing): no named-adopter testimonials. Migration guide stands on technical merit. Vendor-generic phrasing per partner-name guard.

**Intent-rollout-gate downstream sequencing**: intent-rollout-gate's M5 MVP work (Priority 4 in IEP Convergence Debt Plan) consumes `@j-rig/rollout-gate@2.0.0` once that ships. Bead `iar-M5` and its child beads gain a `iaj-E02b` dependency.

**Rationale**: every seat's primary concern is addressed by a specific provision. CTO's coherence preserved (single PR). VP DevRel's developer-experience floor preserved (CHANGELOG/MIGRATION/codemod-as-P1). CSO's standards-community posture preserved (parallel community-temp). CMO's narrative arc preserved (conformance framing). CFO's bandwidth preserved (codemod is P1 stretch, not v2.0.0 blocker). GC's audit-trail discipline preserved (Blueprint B § 7.4 cited by name). CISO's structural integrity preserved (staging-stays-staging explicitly public).

**Dissent acknowledged**: CFO's residual concern that the codemod will compete with Phase B bandwidth is preserved as a binding constraint: codemod work is bounded to a 5-engineer-day budget; if scope explodes, the worked-example-repo fallback is the floor.

---

### 6.4 Q2 — Kernel `EvidenceBundle` wire-format growth

**Vote tally**: 6/7 Option α (with CISO α-minus variant absorbed as the operative form); 1/7 dissent (CFO prefers Option β on bandwidth + kernel-narrowness grounds).

**Verbatim positions**:

- **CTO**: "Option α. The kernel is the canonical source of truth for _every_ on-the-wire shape in this ecosystem; that's what DR-010 Q3 means in practice."
- **GC**: "Option α (kernel grows `EvidenceBundlePayload`, folds j-rig's `EvidenceStatement` row shape, j-rig re-exports) is the only option that keeps the PREDICATE-TYPES.md registry as the source of truth."
- **CMO**: "Option α, unambiguously. The kernel IS the wire format. j-rig re-exports."
- **CFO** (lone dissent): "Option β (j-rig renames locally; no kernel change). The kernel is a _contracts_ layer — types, schemas, validators. It defines the boundary, not the implementation."
- **CSO**: "Option α with a constraint: the v1 payload schema MUST be designed against at least two prospective emitters on paper before it ships — current j-rig + projected audit-harness Phase B emit-evidence."
- **CISO** (introducing α-minus variant): "Option α, and the cross-field invariants are the load-bearing reason — not the schema fold. Blueprint B § 7.3 line 792 makes `subject[0].name === predicate.gate_id` and `subject[0].digest.sha256 === predicate.input_hash` NORMATIVE. Today only j-rig enforces them… kernel adopts the shape and the invariants, but j-rig retains a _behavioral_ secondary check (belt-and-suspenders) for one major version cycle, then removes it once kernel enforcement is proven in CI across all five consumer repos."
- **VP DevRel**: "Option α. Kernel grows `EvidenceBundlePayload`, j-rig re-exports. One mental model for consumers."

**Primary tension**: CFO's structural concern (kernel surface growth = future-maintenance growth + creates precedent of "kernel absorbs downstream feedback") vs the unification thesis (DR-010 Q3 BINDING).

**Novel option introduced**: CISO's α-minus variant — kernel grows the shape AND the cross-field invariants; j-rig retains behavioral secondary check for one major version cycle. This is the form the council settles on.

**DECISION**: **Option α-minus (CISO variant)**.

Kernel ships `@intentsolutions/core@0.2.0` (minor bump, additive — no breaking changes to existing kernel consumers) with:

- New type `EvidenceBundlePayload` (the JSON-array wire format)
- Folded `EvidenceStatement` row shape from j-rig (in-toto Statement v1 carrying `gate-result/v1` predicate)
- Cross-field invariants from Blueprint B § 7.3 line 792 enforced as Zod `.refine()` calls on the schema:
  - `subject[0].name === predicate.gate_id`
  - `subject[0].digest.sha256` (without prefix) === predicate.input_hash (without `sha256:` prefix)
- Optionally, `extensions: Record<string, unknown>` escape hatch on the payload type for experimental fields (CMO compromise — promotion to first-class field requires bead + RFC)

j-rig v2.0.0 re-exports `EvidenceBundlePayload` from kernel + RETAINS its existing behavioral secondary check for ONE MAJOR VERSION CYCLE. At j-rig v3.0.0 (or whenever the next major lands), the behavioral check is removed since kernel-enforcement is then proven across all consumer repos.

**Binding preconditions** (joint CSO + CFO constraint):

1. The kernel-side PR for v0.2.0 MUST be drafted against AT LEAST TWO PROSPECTIVE EMITTERS on paper before merge. Current j-rig + projected `audit-harness` Phase B emit-evidence subcommand (per `iah-E04`). If the second emitter's shape cannot be articulated, the kernel PR is HELD until it can. Addresses CSO's "premature canonicalization" + CFO's "kernel grows for one consumer."
2. CISO co-authors the cross-field invariant enumeration BEFORE the kernel PR opens. Once these invariants ship in kernel, they're effectively immutable (same discipline as `gate-result/v1`).
3. **PREDICATE-TYPES.md registry entry** (GC binding): kernel v0.2.0 release coincides with a registry entry for `evidence-bundle-payload/v1` filed under `intent-eval-lab/specs/PREDICATE-TYPES.md`. Entry includes date, kernel version, j-rig co-author attribution, parent spec reference (Blueprint B § 7).

**Lightweight RFC process for kernel-schema additions** (CMO/CTO joint compromise):

- Each kernel schema addition opens a documented kernel-side bead (`iec-*` prefix)
- Target: kernel-side RFC → patch release in ≤2 weeks worst case
- Bead must declare the second-emitter on paper (per binding precondition #1)

**Sequencing** (operational):

1. Draft kernel v0.2.0 PR with `EvidenceBundlePayload` + invariants + second-emitter sketch (audit-harness `iah-E04` shape).
2. CISO co-authors cross-field invariant enumeration; lands in PR body or a referenced design doc.
3. Kernel v0.2.0 release.
4. j-rig v2.0.0 work consumes kernel v0.2.0; tests cross-verify behavior between kernel structural and j-rig behavioral checks.
5. j-rig v2.0.0 release.
6. PREDICATE-TYPES.md registry entry filed concurrently with kernel v0.2.0 release.

Steps 1–4 can run partially in parallel: j-rig v2.0.0 work can begin against kernel v0.2.0-beta on a temporary workspace ref; final cut waits on kernel release.

**Rationale**: every council seat (except CFO) reached α on principled grounds. The unification thesis (DR-010 Q3 BINDING) is the platform's load-bearing architectural principle; the wire format of evidence rows is the most consumer-facing surface in the platform. CISO's α-minus variant resolves the strongest steel-manned dissent (CFO's "kernel surface growth without proven need"): the second-emitter precondition forces the kernel to grow only when growth is justified by at least two actual consumers, addressing CFO's structural concern without abandoning unification. The behavioral-check-for-one-cycle transition aid addresses CISO's safety concern (CI-proven enforcement before structural-only enforcement).

**Dissent acknowledged**: CFO's lone dissent is preserved verbatim and absorbed as a binding minority constraint:

> **CFO binding minority constraint**: If kernel-schema additions begin to compound (>2 in a quarter), or if no second emitter can be articulated for `EvidenceBundlePayload` within a reasonable timebox, the council reconvenes to evaluate whether the kernel boundary is being violated. This is not an in-principle rejection of α; it is a circuit-breaker against α drifting into "kernel absorbs every consumer's local optimization."

The circuit-breaker preserves CFO's principle without blocking the binding direction.

---

## 7. Council memos verbatim (cross-question themes)

**CTO**: "Both questions are the same question wearing different clothes: _when the kernel's normative shape and a consumer's published shape disagree, who moves?_ DR-010 Q3 already answered: the consumer moves… The deeper theme: **kernel-canonical is only real if it costs something to enforce.** This is the first time it costs something. If we flinch now — minor bump instead of major, β instead of α — we teach every future consumer that the kernel's normative status is negotiable under bandwidth pressure. That lesson is more expensive than either migration." **Most costly to recover from: Q2.**

**GC**: "Both questions converge on the same principle: _contracts are permanent, code is temporary_. Q1 forces us to name a contract boundary (v0.1.0-draft → v1.0.0). Q2 forces us to name where contracts are written (PREDICATE-TYPES.md, not j-rig's package.json). The overhead of writing these names down is not overhead — it's the legal record that lets us sleep at night when a consumer calls six months from now and says 'you changed the schema without telling me.'" **Most costly to recover from: Q2 — category error.**

**CMO**: "Q1 asks _will we narrate the unification thesis loud enough that the market believes it?_ Q2 asks _will we structurally enforce the unification thesis in the dependency graph?_ Both must be **yes**. A loud Q1 with a fragmented Q2 (option β or γ) is marketing without substrate — and developers will smell it within a release cycle. A unified Q2 (α) with a quiet Q1 wastes the structural advantage by failing to claim it publicly." **Most costly to recover from: Q2 — foundation Q1 rests on.**

**CFO**: "Both questions hinge on where we draw the line between _contracts_ (kernel) and _implementations_ (j-rig, audit-harness, agents). I'm arguing for a narrow kernel because every field we add to the kernel is a field we have to maintain, test, validate, and explain to every future consumer. We're one engineer. That's not a moral constraint; it's a bandwidth constraint, and DR-010 § 13.5 removed the customer-signal gate specifically because Phase B is _bandwidth_-gated now." **Most costly to recover from: Q2 — structural decision baked into dependency graph of five repos.**

**CSO**: "Both questions are really one question: _where does the canonical contract live, and how do we sequence its evolution so the standards community reads our timeline as competent?_ Q1 says the predicate URI `gate-result/v1` is immutable and the migration is a conformance event, not a breaking-change event. Q2 says the wire-format envelope `EvidenceBundlePayload` belongs in the same kernel as the predicate body it carries. Both answers point at the same discipline: **the kernel is the citation surface**." **Most costly to recover from: Q1 — Rekor cannot be un-published.**

**CISO**: "Both questions are the same question under different surfaces: _where does normative enforcement live, and how do we keep what's signed from outrunning what's been ratified?_ Q1 is about not writing non-conformant rows into a permanent log; Q2 is about making the kernel structurally incapable of allowing non-conformant rows in the first place." **Most costly to recover from: Q2 — kernel-shape decisions immutable on transparency log.**

**VP DevRel**: "_We are about to ship our first real ecosystem break. The world watches how Intent Solutions handles it._ Every choice in Q1 and Q2 is downstream of one question: do we treat external adopters as first-class users or as collateral? My seat votes first-class every time." **Most costly to recover from: Q1 — reputation for sloppy releases is permanent search-engine history.**

## 8. Cross-cutting themes

### 8.1 Most-costly tally

| Question                            | Vote count for "most costly to recover from" |
| ----------------------------------- | -------------------------------------------- |
| Q2 (kernel wire-format growth)      | **5** — CTO, GC, CMO, CFO, CISO              |
| Q1 (j-rig predicate-body migration) | 2 — CSO, VP DevRel                           |

The council collectively identifies Q2 as the more consequential / less reversible decision. Q1 is "painful but recoverable" per CTO; Q2 ships a kernel contract surface that's immutable for the platform's lifetime per CISO. The CSO + VP DevRel minority on this question is steel-manned and absorbed: their concern (Rekor permanence + first-impression-permanence) is exactly what the staging-stays-staging decision in Q1(b) + the parallel-community-temperature sequencing in Q1(c) address. The acting-head call honors all 7 seats' weighting.

### 8.2 Adversarial integrity check

- **No unanimous returns on every question**: ✓ (CMO dissented on Q1(b); CFO dissented on Q2; 5/7 vs 2/7 split on most-costly-to-recover.)
- **Verbatim dissents preserved**: ✓ (CMO's clean-corpus position; CFO's narrow-kernel position; CSO's community-temp-first position absorbed against CMO's announce-first impulse.)
- **Novel options introduced from outside the question framing**: ✓ (CISO's α-minus variant; CMO's `extensions:` escape hatch; CSO's two-emitter precondition.)
- **Minority binding constraints stacked on majority decisions**: ✓ (CFO circuit-breaker on Q2; CMO public-narrative constraint on Q1(b); GC PREDICATE-TYPES.md registry binding on Q2; CSO parallel-community-temp on Q1(c).)

The session passes the adversarial-integrity check. Synthesis is not consensus theater.

### 8.3 How the lenses landed

- **The arena (5 surfaces)**: APIs · CLIs · MCP servers · agents · SKILL.md — the j-rig migration touches the CLI surface (`@j-rig/cli`), the API surface (`@j-rig/core` exported types), and downstream the agent surface (intent-rollout-gate consumes the new shape). MCP server surface is not directly affected by this session.
- **Both sides**: client-side eval (pre-commit hooks via j-rig CLI) + server-side eval (CI via `@j-rig/rollout-gate`) — both consume the new schema; both must migrate together. Single coherent PR per Q1(c) respects this.
- **The transformation pipeline (API → CLI → MCP → SKILL.md → agent)**: kernel-canonical means every step in the pipeline imports from the same canonical contract surface. α-minus operationalizes this.
- **Composable partial attestation**: each in-toto Statement row is independently verifiable; the kernel's `EvidenceBundlePayload` + per-row invariants reinforce this. NOT_APPLICABLE encoding through `coverage.dimensions_skipped` (rather than as a decision-enum value) preserves the composability principle — a "skipped" dimension is silence on that dimension, not a `fail` verdict.

## 9. Implementation directives

### 9.1 Decisions routed to work items

| Decision                                                                                    | Owner                    | Work item / bead                                                                                  |
| ------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------- |
| `@j-rig/*` major version bump to 2.0.0                                                      | j-rig maintainer         | `iaj-E02b` (scope-expanded — see § 9.2 below)                                                     |
| Staging-stays-staging for existing attestations                                             | CISO + j-rig maintainer  | `iaj-staging-stays-staging-aar` (new — P1) — produces the forensics check + release-note language |
| Single coherent migration PR with CHANGELOG.md "BREAKING" structure                         | j-rig maintainer         | `iaj-E02b`                                                                                        |
| MIGRATION.md doc at j-rig repo root                                                         | VP DevRel-flavored work  | `iaj-migration-md` (new — P1)                                                                     |
| `j-rig migrate <dir>` codemod                                                               | j-rig maintainer         | `iaj-migrate-codemod` (new — P1, **NOT** P3 per VP DevRel binding)                                |
| 90-day sunset window + npm-postinstall deprecation notice for j-rig 1.x                     | j-rig maintainer         | `iaj-sunset-1x` (new — P2)                                                                        |
| Community-temperature post (SIG-GenAI + OpenSSF)                                            | CSO-flavored work        | `iaj-community-temp-posts` (new — P1, **must land same week as v2.0.0**)                          |
| Blog post on `startaitools.com`                                                             | CMO-flavored work        | `iaj-blog-post-startaitools` (new — P2, **must land 1+ week after community-temp posts**)         |
| Kernel v0.2.0 with `EvidenceBundlePayload` + cross-field invariants + second-emitter sketch | kernel maintainer        | new epic `iec-E12` (P0, feature) — "Kernel v0.2.0 wire-format growth (EvidenceBundlePayload)"     |
| CISO cross-field invariant enumeration                                                      | CISO                     | `iec-E12a` (sub-bead, P0)                                                                         |
| Audit-harness `iah-E04` second-emitter shape sketch (paper)                                 | audit-harness maintainer | `iec-E12b` (sub-bead, P0) — must land before `iec-E12` final PR opens                             |
| PREDICATE-TYPES.md registry entry for `evidence-bundle-payload/v1`                          | GC + kernel maintainer   | `iel-predicate-types-evidence-bundle-payload` (new — P1)                                          |
| Update intent-rollout-gate M5 work to depend on `@j-rig/rollout-gate@2.0.0`                 | rollout-gate maintainer  | `iar-M5` dep edge added to `iaj-E02b`                                                             |
| Updated `iaj-E02b` scope: full normative schema upgrade, not name-based codemod             | j-rig maintainer         | bead description rewrite (see § 9.2)                                                              |

### 9.2 `iaj-E02b` scope rewrite (REPLACES prior scope per 017 § 4.5)

Old scope: "codemod imports from `@j-rig/core` schemas to `@intentsolutions/core`."
**New scope**: "j-rig schema upgrade to kernel-normative shape. Includes: import `@intentsolutions/core`; rename `result` → `gate_decision`, `timestamp` → `evaluated_at`; add 5 required fields (`gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref`); migrate decision enum (`PASS|FAIL|ADVISORY|NOT_APPLICABLE` lowercase → `pass|fail|advisory|error`; encode NOT_APPLICABLE via `coverage.dimensions_skipped`); populate new required fields at all 6 producer sites (`packages/core/src/evidence/writer.ts`, `reader.ts`, `cli/src/commands/emit-evidence.ts`, `db/src/schema.ts`, etc.); delete duplicated local Zod schemas; re-export from kernel. Major-version-bump `@j-rig/*` to 2.0.0. Single coherent PR. CHANGELOG.md opens with `## Breaking changes`. Release notes per § 6.3 verbatim structure."

### 9.3 Decisions deferred / explicitly NOT in scope

- **iah-E02 path** (audit-harness kernel adoption) — separate question; not this session.
- **Lab schema repoint** (`iel-link-schemas-to-kernel`, P5) — independent track; can proceed in parallel.
- **Production-Rekor unlock for `gate-result/v1`** — gated on DNSSEC + CAA verification (`iah-E06`) + SPEC.md normative (already landed in Blueprint B § 7.4) + per-predicate per-emitter conformance proof. Not adjudicated here.
- **`extensions:` escape hatch promotion process** — left to a future kernel-side RFC bead. The escape hatch SHIPS in kernel v0.2.0 per CMO compromise; promotion of any specific field to first-class status goes through the kernel-side RFC process.
- **j-rig OSS adopter notice obligations** — j-rig has no formal commercial-grade SLA; the 90-day sunset window + npm deprecation notice constitute the platform's notice posture. Future commercial adopters would gate on this DR + their own contracts.

### 9.4 Beads to file alongside this DR

(Listed in dependency-rough-topological order for clarity. Actual `bd create` execution happens as next-session work after this DR commits.)

1. `iep-isedc-session-5-jrig-reconciliation` — umbrella for this DR (P0, feature)
2. `iec-E12` — Kernel v0.2.0 EvidenceBundlePayload epic (P0, feature)
3. `iec-E12a` — Cross-field invariant enumeration (P0, sub-task; CISO co-author)
4. `iec-E12b` — audit-harness `iah-E04` second-emitter shape sketch on paper (P0, sub-task; blocks `iec-E12` final PR)
5. `iel-predicate-types-evidence-bundle-payload` — PREDICATE-TYPES.md entry (P1, task)
6. `iaj-staging-stays-staging-aar` — forensics check + release-note language (P1, task)
7. `iaj-migration-md` — MIGRATION.md doc (P1, task)
8. `iaj-migrate-codemod` — `j-rig migrate <dir>` codemod (P1, task; stretch for v2.0.0 PR)
9. `iaj-sunset-1x` — j-rig 1.x sunset infra (P2, task)
10. `iaj-community-temp-posts` — SIG-GenAI + OpenSSF posts (P1, task; same-week with v2.0.0)
11. `iaj-blog-post-startaitools` — blog post (P2, task; 1+ week after community-temp)
12. `iaj-E02b` — scope-rewrite (existing bead, scope updated per § 9.2)

Dependencies:

- `iec-E12` depends on `iec-E12a` + `iec-E12b` (both must close before kernel v0.2.0 PR merges)
- `iaj-E02b` depends on `iec-E12` (j-rig v2.0.0 consumes kernel v0.2.0)
- `iar-M5*` (intent-rollout-gate M5 MVP) depends on `iaj-E02b` (consumes `@j-rig/rollout-gate@2.0.0`)
- `iaj-community-temp-posts` + `iaj-blog-post-startaitools` depend on `iaj-E02b` release tag
- `iel-predicate-types-evidence-bundle-payload` depends on `iec-E12` (registry entry filed at release)

## 10. Reusable pattern reference

This council session follows the standard ISEDC pattern documented at `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0. The pattern dynamics that surfaced in this session:

- **CISO's α-minus variant** is a reusable pattern for "kernel grows AND consumer retains transition aid for one major cycle" — worth encoding as a named compromise shape for future sessions.
- **CSO's two-emitter precondition** ("schema additions must articulate a second consumer on paper before merge") is a reusable governance precondition — worth promoting to a standing kernel-side rule.
- **CMO/CSO parallel-community-temp compromise** ("community-temperature posts run same week as announcement, not in series") generalizes for any future major release that touches a standards-body surface.

These dynamics are candidates for a future minor bump of the ISEDC skill (v1.1.0). Not done in this session.

## 11. Acting Head of Board declaration

**Acting Head of Board**: Claude, designated by Jeremy Longshore on 2026-05-21 via the IEP Convergence Debt Plan execution directive ("bro talk to the engineering team i dont know" + "u need to figure all this out with the team be the ceo i am counting on u to make the roght call no shortcuts").

I ratify the decisions in § 6.1, § 6.2, § 6.3, and § 6.4 above with the minority binding constraints stacked as written. Verbatim seat positions are preserved in § 6 and § 7 for future readers; the dissents are real and were weighed.

Two decisions absorbed minority positions verbatim rather than dismissing them:

- CMO's Q1(b) dissent absorbed via the **public release-note language requirement**.
- CFO's Q2 dissent absorbed via the **circuit-breaker minority constraint** (reconvene if kernel schema additions compound beyond 2/quarter or if `EvidenceBundlePayload` cannot articulate a second emitter).

The user retains the right to vacate or amend any decision in this DR. Standing rule per ISEDC discipline: the user is the ultimate Head of Board; this acting-head designation is for execution velocity, not authority transfer.

— Claude, Acting Head of Board
on behalf of Jeremy Longshore
intentsolutions.io

## 12. References

- DR-010 § 13.5, § 13.6, Q3 — `intent-eval-lab/000-docs/010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`
- Blueprint A § anti-goals + 5-repo taxonomy — `011-AT-ARCH-ecosystem-master-blueprint.md`
- Blueprint B § 2.4, § 7.1–§ 7.5 — `012-AT-ARCH-platform-runtime-blueprint.md`
- Canonical Glossary — `014-DR-GLOS-canonical-glossary.md`
- Kernel shadow inventory — `016-RR-LAND-kernel-shadow-inventory-2026-05-20.md`
- Shape reconciliation addendum — `017-RR-LAND-shape-reconciliation-addendum-2026-05-21.md`
- DR-004 S1Q2 — partner-name vendor-generic discipline (binding; enforced by CI guard)
- ISEDC Session 1 DR (Class-1 precedent) — `004-AT-DECR-isedc-council-record-2026-05-10.md`
- IEP Convergence Debt Plan (2026-05-20 enhanced 2026-05-21) — local plan reference
- Tagline (always applied as positioning lens): _"We create industries that don't exist — we think outside of the box's box."_

— Jeremy Longshore
intentsolutions.io
