# ISEDC Council Decision Record — 7-Seat Adversarial Review of 5 Phase B Open Questions

| Field | Value |
|---|---|
| **Date convened** | 2026-05-10 |
| **Date decision-locked** | 2026-05-10 |
| **Acting Head of Board** | Claude (Anthropic, claude-opus-4-7), designated by Jeremy Longshore (CEO, Intent Solutions LLC) |
| **Council size** | 7 seats (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel) |
| **Questions adjudicated** | 5 |
| **Decisions logged** | 5 |
| **Adversarial method** | Each seat argued from a distinct value system; dissent preserved; final calls made after weighing steel-manned minority positions |
| **Status** | Decision-locked. Implementation underway via LAB-6 update + PB-N work items. |
| **Master plan** | `~/.claude/plans/please-take-your-time-glimmering-stardust.md` |
| **Synthesis input** | `~/000-projects/intent-eval-platform/intent-eval-lab/000-docs/003-PP-PLAN-phase-b-scope-refinement.md` |
| **Reusable pattern** | `~/.claude/skills/exec-decision-council/SKILL.md` (saved in this same execution batch) |
| **Audience** | Future Intent Solutions sessions returning to Phase B; partners requesting decision provenance; academic / standards-body reviewers of Phase B published artifacts |

---

## 1. Mission of this Decision Record

This document exists so future readers can reconstruct **WHY each decision landed where it did**, not just WHAT the decision was. Verbatim seat positions are preserved. Dissents are named. The acting head of board's rationale is explicit. Five years from now, when somebody asks "why is the predicate URI rooted at `evals.intentsolutions.io` and not `labs.`?", this document is the authoritative answer.

## 2. Why a council, not a single review

The five questions concern artifacts that — once filed in public standards bodies, transparency logs, or partner-visible specs — are **effectively immutable**. The cost of a wrong call is measured in years of brand repositioning or damaged standards-body relationships. Single-reviewer reasoning is insufficient when the failure modes carry that kind of asymmetry.

The council was structured as **7 adversarial seats** rather than a consensus body. Each seat's prompt explicitly told it to argue from its value system and flag where it expected to disagree with named other seats. Consensus theater was rejected by design. Final synthesis weighs the steel-manned minority dissents rather than averaging them away.

**Intent Solutions tagline framing (the why behind the why):** *"We create industries that don't exist — we think outside of the box's box."* The council's job is to keep that ambition intact while making decisions that survive standards-body, partner-consent, and developer-community scrutiny.

## 3. The four synthesis lenses (user-supplied enhancements)

The original Part 2 plan covered three workstreams (audit-harness landscape · j-rig multi-provider · MCP testing bridge) and a synthesis. Mid-execution, Jeremy supplied four enhancement lenses that thread through every decision below:

1. **The arena (5 surfaces)** — APIs · CLIs · MCP servers · agents · SKILL.md. Every Phase B work item is evaluated against which surface(s) it covers.
2. **Both sides** — client-side eval (agent runtime: what it does with credentials, scopes, tool-call permissions) + server-side eval (MCP server / API endpoint: what's enforced, what's emitted, what's auditable).
3. **The transformation pipeline** — API → CLI → MCP server → SKILL.md → agent runtime. Each hop is an evaluable + attestable surface.
4. **Composable partial attestation** — attackable from any component-angle as a valid entry; partial attestation honored, not penalized; silence about a dimension means "this implementation chose not to cover X," not "this implementation failed X."

The five questions test the standard's ability to survive these four lenses. Council positions thread through them.

## 4. The 5 questions verbatim

| Q | Topic | Why immutable / costly |
|---|---|---|
| **Q1** | Predicate URI domain (`labs.` vs `evals.` vs subpath) | URI lives forever in Rekor transparency logs once first in-toto Statement is signed. Recovery = predicate version migration + every downstream verifier reconfigures. |
| **Q2** | Case-study scaffold public vs private during Phase B | Partner-name leak in public spec is unpublishable (internet permanence + partner trust). The 2026-05-10 brand-scrub set the binding policy. |
| **Q3** | MM-7 disposition (defer / file now / fold into MM-2) | Speculative category dilutes the matcher-map's strongest defensibility argument ("found, not theorized"). Once shipped, retraction is a credibility event. |
| **Q4** | OTel SIG-GenAI early community-temperature (informal email first vs RFC-first) | Cold RFC drops into a SIG with no roadmap slot for the scope = first-impression event that propagates across every future filing. Years of damage. |
| **Q5** | LiteLLM vs Vercel AI SDK for j-rig provider adapters | Library choice ties Jeremy to maintenance/community-relationship burden he hasn't validated. Less catastrophic than Q1/Q4 but locks engineering velocity. |

## 5. Council composition — 7 seats, distinct value systems

| Seat | Value system | Bias |
|---|---|---|
| **CTO / Chief Architect** | Technical durability · schema integrity · immutability awareness · future-proofing | Deliberation > commit · empirical evidence > authorship claims · schema durability > schema elegance |
| **GC / General Counsel** | IP protection · partner-consent compliance · trademark/brand-surface management · audit-trail discipline | Written consent before any partner reference · conservative interpretation of "implied consent" · paper trail is sacrosanct |
| **CMO / Industry-Standard Strategist** | Positioning · narrative coherence · tagline alignment · "creating industries that don't exist" · first-mover authorship | Visible > silent · ambitious > conservative · frontier framing > operational framing · partner co-author credit BEATS silent generic anonymization |
| **CFO / Strategic Operator** | Sole-prop bandwidth · customer-signal gating · opportunity cost · "small bets that compound" | Defer until customer evidence justifies · measure before committing · standards-body filings are NOT costless |
| **CSO / Chief Standards Officer** | OTel SIG-GenAI / in-toto / SLSA / CNCF / OpenSSF realpolitik · RFC sequencing strategy · standards-body relationship management | Community-temperature ALWAYS precedes RFC filing · URI signals fit-for-purpose to reviewers · "first-impression with a maintainer is permanent" |
| **CISO / Chief Information Security Officer** | Supply-chain attestation integrity · signing infrastructure · key management · threat model · Rekor transparency-log discipline | Reserve schema slots for signing fields NOW · scoped subdomain reads cleaner in transparency logs · threat model = first-class design constraint |
| **VP DevRel / Head of OSS Community** | Developer-audience signal · OSS contribution dynamics · friction-to-adopt · community-temperature timing | "Saturday-afternoon-developer-tries-the-thing" test · informal channels > formal · public examples developers can read and copy > scrubbed abstractions |

Adversarial dynamics by design: CMO vs (CFO, GC) on visibility; CSO vs CMO on RFC sequencing; CISO vs CTO on signing-slot priority; VP DevRel vs GC on case-study examples; CFO vs all on bandwidth gating.

---

## 6. Per-question council record

Each question shows: (a) the question, (b) each seat's recommended answer + 1-line position summary, (c) vote tally, (d) primary tension, (e) **DECISION** (acting head of board), (f) rationale, (g) dissent acknowledged.

### Q1 — Predicate URI domain

**Question:** USER PRE-DECISION: subdomain on `intentsolutions.io` (fits existing pattern `crm.` `projects.` `demos.` `partners.` `analytics.`). Council narrows to `labs.intentsolutions.io` vs `evals.intentsolutions.io` vs subpath form (e.g., `intentsolutions.io/evals/predicates/...`). URI is effectively immutable once filed in OTel RFC / in-toto attestation.

**Seat positions:**

| Seat | Recommended answer | One-line position |
|---|---|---|
| **CTO** | `evals.intentsolutions.io/<predicate-type>/v<version>` | `labs.` is too generic; subpath form ties predicate's lifetime to marketing-site URL routing forever. `evals.` mirrors schema purpose. |
| **GC** | `evals.intentsolutions.io/gate-result/v1` + sibling `conformance-provenance/v1` | Bounded brand surface = bounded litigation exposure. `labs.` invites brand-stretch litigation with existing "Labs" trademark holders. |
| **CMO** | `labs.intentsolutions.io` | `evals.` brands Intent Solutions as test-tooling vendor for the life of the platform. Tagline isn't "we run evals" — it's "we create industries that don't exist." |
| **CFO** | Subpath form `intentsolutions.io/evals/predicates/...` (zero new infra) OR reuse existing `labs.` if already standing. Refuse net-new `evals.` subdomain in Phase B. | URI text matters less than ongoing operational footprint. Subpath = zero new DNS / SSL / Caddy / cert-rotation pathway. |
| **CSO** | `evals.intentsolutions.io/gate-result/v1` + sibling `conformance-provenance/v1`. Reserve `labs.intentsolutions.io` for research/blog/Phase-C content. | When in-toto reviewers parse predicate URI, subdomain IS the fit-for-purpose signal. `labs.` reads research-may-move; `evals.` reads stable schema authority. |
| **CISO** | `predicates.intentsolutions.io` (novel option) > `evals.` > hard NO on `labs.` | Predicate URI is forever in Rekor — narrow subdomain = narrow blast radius if DNS takeover. `predicates.` self-documents in cosign verify output. |
| **VP DevRel** | `evals.intentsolutions.io/predicates/{ns}/{name}/v{N}` | Developers parse subdomain semantics as scope contracts. `evals.` reads "bounded, depend-on-it-safely"; `labs.` reads "research, expect breakage." |

**Vote tally:** `evals.` = 5 · `predicates.` (CISO novel) = 1 · `labs.` (CMO) = 1 · subpath/reuse-labs (CFO) = 1 conditional (CFO accepts `evals.` if op-footprint hardened).

**Primary tension:** CMO is the lone strong dissent — they argue tagline alignment demands `labs.`. Other seats argue brand-arc belongs on a different surface (blog, methodology landing) than predicate URI. CISO's `predicates.` is more precise than `evals.` but adds a third subdomain (CFO concern).

**DECISION (acting head of board):** **`evals.intentsolutions.io`** as the predicate URI namespace. Concretely:
- `evals.intentsolutions.io/gate-result/v1` (audit-harness gate-result predicate)
- `evals.intentsolutions.io/conformance-provenance/v1` (j-rig + MCP-bridge conformance predicate)
- Versioning policy: `/v{major}` only. Minor revisions = same URI; breaking changes = new `/v{N+1}`.

`labs.intentsolutions.io` is **reserved for blog / methodology landing / RFC published-version pages / Phase-C content surface** — gives CMO partial win without putting brand on the permanent predicate URI.

**Stacked binding constraints (from minority seats):**
- CISO: DNSSEC enabled at registrar BEFORE first attestation is signed.
- CISO: CAA record pinning issuance to a single CA.
- CISO: `labs.intentsolutions.io` explicitly NOT used for any predicate URI ever — documented in CLAUDE.md as reserved-don't-touch.
- CTO: predicate-versioning policy doc ships with PB-1 SPEC.md.
- CSO: never rename URI even if spec moves repos (URI immutability post-Rekor is non-negotiable).
- CFO: provisioning lives in same Caddy block + cert-renewal pathway as existing IS subdomain (no new monitoring entry).

**Rationale:** Five of seven seats voted `evals.`. The two non-`evals.` votes (CMO `labs.`, CISO `predicates.`) raise legitimate concerns the decision absorbs: CMO's brand-arc lands on the reserved `labs.` subdomain (just not on the predicate URI itself); CISO's precision concern is absorbed by stacking DNSSEC + CAA + reserved-don't-touch discipline on `evals.`. CFO's operational-footprint concern is absorbed by colocating in existing Caddy block.

**Dissent acknowledged:** CMO is on record that `evals.` brands Intent Solutions as test-tooling vendor for the life of the platform. The decision rejects that frame on grounds that predicate URIs are developer infrastructure (read by tooling, not humans), not brand surface. CMO's "single ask: if Jeremy reads only one council seat, read mine on Q1" is recorded here and overruled. CISO's `predicates.` proposal stays in the option-space as a future migration target if `evals.` proves too broad in scope (separate decision; not this one).

---

### Q2 — Case-study scaffold public vs private during Phase B

**Question:** PB-12 (Gherkin scenarios for MM-1..MM-6) wants example cases. Synthesize from vendor-generic shapes only, or seek partner consent for case-study publication? Current stance: scrubbed-clean per 2026-05-10 brand-scrub.

**Seat positions:**

| Seat | Recommended answer | One-line position |
|---|---|---|
| **CTO** | Generic shapes in PB-12 Gherkin; separate empty `case-studies/` dir under `specs/mcp-plugin-observability/` to land partner-consented cases later. | Decouple spec velocity from consent timelines. Generic Gherkin is more reusable as normative spec anyway. |
| **GC** | STRONGLY generic-only. Public PB-12 cites ZERO real partners by name, by URL, by repo, by F-finding ID, or by recognizable scenario. | 2026-05-10 brand-scrub is binding policy. Deviating without written consent = partner-relationship malpractice with zero upside in Phase B. |
| **CMO** | Tiered ask. Phase B Wave 1 = vendor-generic ONLY; in parallel pursue consent for ONE attributed case study each (the primary client engagement post-milestone, an active revenue client, one of two inbound credibility engagements), target published-real example in Phase B+1. | Named case studies = 10x credibility of "anonymous Fortune 500 customer." Worst case: partner says no, fall back to generic. |
| **CFO** | Generic shapes only through Phase B close. Case-study consent only after first-paying-customer signal + partners in stable post-deliverable state. | Pursuing partner consent in Phase B = sole-prop bandwidth Jeremy doesn't have. Case-study is a Phase C asset, not a Phase B asset. |
| **CSO** | Phase B ships pseudonymized empirical-anchor scaffolds (Partner-A / Partner-B / Partner-C). Phase C re-publishes with consent. | Standards-track credibility rests on "empirical anchor exists" claim, not on "publicly attributable." |
| **CISO** | Vendor-generic Gherkin public; partner-named behind consent gates; schema slot `case_study.partner_id` reserved null in public corpus. | Public scenarios enable independent red-teaming. But cannot override GC consent paper trail. |
| **VP DevRel** | Hybrid: vendor-generic Gherkin baseline (Phase B closes on time regardless) + parallel consent pursuit for Phase B+1. Scaffolds written from REAL shapes with internal docstrings ("based on real engagement, scrubbed per IS-consent-policy") so consent-later = swap names not rewrite. | Developers do not adopt empty scaffolds. They adopt methodologies they can read a worked example of. Empty-scaffold-of-abstractions is unacceptable. |

**Vote tally:** Generic-only-for-Phase-B = 7 of 7. Tension is on emphasis: should generic scaffolds be derived from REAL shapes (VP DevRel) or wholly abstract (potential GC reading)? Should partner-consent ask commence in parallel (CMO) or be deferred entirely (CFO/GC)?

**Primary tension:** VP DevRel and CMO push hard for at least one real worked example with attribution (developer adoption argument + credibility argument). GC and CFO push for the cleanest possible defer (consent process = bandwidth + paper-trail risk).

**DECISION (acting head of board):** **Vendor-generic Gherkin scaffolds derived from real engagements** (per VP DevRel's hybrid path). Specifically:
- PB-12 Phase B ships generic Gherkin with internal docstrings noting "based on real engagement, scrubbed per IS-consent-policy 2026-05-10" — so future consent enables drop-in attribution, not rewrite.
- An empty `case-studies/` directory is created under `specs/mcp-plugin-observability/v0.1.0-draft/` to reserve the structural slot.
- A `CONTRIBUTING-case-study.md` is authored in that directory documenting the consent + co-credit pattern for Phase B+1.
- Partner-consent ask commences in **Phase B+1** (not Phase B), aligned with engagement-close windows (the primary client engagement post-milestone (~2026-05-25+), an active revenue client, one of two inbound credibility engagements). CMO's tiered ask is preserved as Phase B+1 work.
- Schema slot `case_study.partner_id` reserved null in public corpus (CISO requirement).
- CISO's revocation-procedure requirement applies: if any partner-named publication is later authorized pre-consent (edge case), Rekor-anchored revocation procedure must be documented BEFORE first publication.

**Rationale:** All seven seats voted generic-only for Phase B. The synthesis converges on VP DevRel's "real-shape-derived but scrubbed" framing — this satisfies GC's binding policy (no partner names in public Phase B), CFO's bandwidth concern (consent ask deferred), CMO's credibility concern (scaffolds are real-shape-derived, not invented), VP DevRel's adoption concern (docstrings make scaffolds reflect actual engagement work), and CISO's threat model (public scenarios enable red-teaming once consent lands later).

**Dissent acknowledged:** None on the Phase B decision itself. CMO's preferred timing (parallel consent ask during Phase B) is rejected on CFO bandwidth grounds but preserved as the Phase B+1 work plan.

---

### Q3 — MM-7 disposition

**Question:** Workstream C flagged gleanwork/mcp-server-tester's "tool-discoverability" as candidate seventh failure-shape. Defer until first observed failure, file MM-7 now, or fold into MM-2 shape-drift?

**Seat positions:**

| Seat | Recommended answer | One-line position |
|---|---|---|
| **CTO** | Defer hard. Reserved-but-unallocated note in `matcher-map-template.md`. Trigger criterion: "MM-7 filing requires a partner-engagement finding that does not type-fit MM-1..6 plus 30-day MM-5 differential review." | Filing MM-7 from a third-party tool's category dilutes the matcher-map's strongest schema property: every category was FOUND, not theorized. |
| **GC** | Defer. Add prior-art citation to gleanwork in `matcher-map-template.md` as reservation note. File MM-7 in `v0.2.0` when real partner-engagement failure surfaces. | Codifying MM-7 from third-party tool's category without clean attribution chain creates downstream attribution-dispute risk. |
| **CMO** | File a public MM-7 *slot* with status "RESERVED — awaiting first observed failure." Do NOT fold into MM-2 (destroys option value). | Public placeholder claims the namespace without claiming false provenance. Forces honesty about what's observed vs. predicted. |
| **CFO** | Defer hard. Document the candidate in `specs/.../FUTURE.md` so the idea is captured without consuming spec real-estate. | Adding scope to a spec before customer signal validates existing scope = textbook sole-prop trap. |
| **CSO** | Defer. Per § 7 of synthesis doc — reservation note + gleanwork prior-art citation in `matcher-map-template.md`. File MM-7 in `v0.2.0` when real engagement surfaces non-MM-1..6 failure-shape. | Filing speculative categories is the most common way published specs get accused of bloat by standards reviewers. |
| **CISO** | Defer. Open tracking issue with trigger condition: "file MM-7 only when ≥2 empirical instances observed across distinct engagements." | Adding an unanchored shape to the matcher-map pollutes the attestation namespace with a category that has no empirical attack pattern. |
| **VP DevRel** | Defer MM-7 AND open public contribution path. Ship `specs/CONTRIBUTING-failure-shape.md` in Phase B with proposal template + acceptance criteria (must be observed in ≥2 independent engagements, must not fold into MM-1..MM-6) + curator = Jeremy. | "Community proposes MM-N, we curate" is the Kubernetes/CNCF/IETF pattern. Converts methodology from product to standard. |

**Vote tally:** Defer = 7 of 7. CMO adds "public reservation slot"; VP DevRel adds "public contribution path."

**Primary tension:** Minimal. Universal defer. The texture is whether to (a) silently defer, (b) publicly reserve a slot, or (c) actively invite community proposals via a contribution path.

**DECISION (acting head of board):** **Defer MM-7** with VP DevRel's community contribution path:
- Add gleanwork prior-art citation to `matcher-map-template.md` as a reservation note (GC/CSO).
- Ship `specs/CONTRIBUTING-failure-shape.md` in Phase B (VP DevRel). Acceptance criteria: must be observed in ≥2 independent engagements (CISO threshold); must not type-fit MM-1..MM-6; must include OTel signal vocabulary; must be backwards-compatible with v0.1.0-draft. Curator: Jeremy Longshore until standards body forms.
- Do NOT fold into MM-2 (CMO's specific guard — preserves shape-drift's clean signature).
- Document the candidate in a public `specs/mcp-plugin-observability/v0.1.0-draft/FUTURE.md` (CFO's framing) so the idea is captured without consuming spec real-estate.

**Rationale:** Unanimous defer is the cleanest signal. VP DevRel's community-contribution-path proposal is the value-add that converts the deferral from passive ("we don't know yet") to active ("we invite community to propose") — strongest industry-standard signal available. Empirical-anchor discipline ("found, not theorized") is preserved.

**Dissent acknowledged:** None. All seven seats agree on defer. CMO's preferred "public reservation slot" is partially satisfied by `FUTURE.md` + the gleanwork citation in `matcher-map-template.md`.

---

### Q4 — OTel SIG-GenAI early community-temperature

**Question:** PB-10 + PB-11 file two RFCs into agent-level conventions; SIG-GenAI charter (https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md) says agent-level is "long-term, no current roadmap target." Worth low-stakes informal Slack/email to SIG maintainers before Phase B Wave 1 commits to RFC filing, or proceed RFC-first?

**Seat positions:**

| Seat | Recommended answer | One-line position |
|---|---|---|
| **CTO** | Informal first, before Wave 1. Email/Slack-DM one SIG-GenAI maintainer with a 2-paragraph description of `agent.rollout.gate.*` + `agent.matcher_map.*` namespaces. Wait up to 2 weeks; file RFCs informed by response regardless. | A 30-minute Slack conversation surfaces the actual scoping objection before ~3 weeks of RFC drafting time is burned. |
| **GC** | STRONGLY informal first. Documents responses in `intent-eval-lab/000-docs/0NN-RR-INTL-otel-sig-genai-temperature.md`. Later RFC opens with "per discussion with @maintainer 2026-MM-DD." | Informal contact creates relationship paper trail (defensive value if accused of "drive-by RFC spam") without contractual commitment. |
| **CMO** | RFC-first. Intent Solutions claims authorship by FILING, not by quietly asking permission. If informal heads-up prevents procedural-rejection landmine, fine — but substance lives in RFC, not backchannel. | Standards-body realpolitik rewards visible concrete artifacts over backchannel relationship-building (which favors incumbent vendors). |
| **CFO** | Informal community-temperature email first, full stop. Single informal email; time-box response window to 4 weeks. RFC consideration ONLY after positive-signal reply AND first-paying-customer signal. | RFCs are MASSIVE founder-time commitments. Email costs 30 minutes; RFC costs weeks + ongoing community-stewardship burden. |
| **CSO** | Informal email first. Sequence: Week 1 informal email to a SIG-GenAI maintainer (likely Drew Robbins or `gen-ai.md` charter-doc primary author per GitHub blame log; verify before sending) with matcher-map vocabulary as public draft link, asking "Is SIG-GenAI scope receptive to agent-level conventions, or should we file against a different sub-group / propose a new one?" Do NOT include RFC draft in first email. Week 2-3 incorporate routing feedback. Week 4+ file RFC. | Cold-RFC-dropping into a SIG with no roadmap slot for your scope is how proposals get ignored, deflected, or politely-but-firmly rejected with a "thanks, we're focused on `gen_ai.*` right now" that becomes the public record citation against your work for years. |
| **CISO** | Informal email first. Bad-faith RFC perception is a reputational supply-chain attack on the methodology itself. | Standards bodies are an attack vector when mishandled — a premature RFC reads as land-grab and damages future legitimacy permanently. Reputation in standards work is a one-way ratchet. |
| **VP DevRel** | Informal email first. Always. Standard OSS norm: lurk → contribute small → propose. We have ZERO prior contribution credit in SIG-GenAI; RFC-first reads as vendor-pushing. | Walking into a standards SIG cold with an RFC reads as "we've decided, we're here to tell you" — that burns community-temperature on day one. |

**Vote tally:** Informal first = 6 of 7. RFC-first (CMO) = 1.

**Primary tension:** CMO carries the lone dissent — argues "authorship claimed by filing." Five seats explicitly named Q4 (or tied for it) as the single most-costly-to-recover-from decision in the council. CSO stated they would "fight harder for Q4 than any other Q" — they have the most standards-body domain knowledge on the council.

**DECISION (acting head of board):** **Informal community-temperature email first** per CSO's full sequence:
- **Week 1** — informal email to a verified SIG-GenAI maintainer (CSO's named candidate: Drew Robbins, or `gen-ai.md` charter-doc primary author per GitHub blame log — verify before sending). Email content: 2-paragraph description of agent-level signal needs surfaced by Intent Solutions' multi-vendor partner work, link to public matcher-map vocabulary draft at `intent-eval-lab/specs/mcp-plugin-observability/v0.1.0-draft/`, ask "Is SIG-GenAI scope receptive to agent-level conventions, or should we file against a different sub-group / propose a new one?" **Do NOT include RFC draft in first email** (sharing vocabulary = "here's what we found"; sharing RFC = "here's what we want you to accept" — different social register per CSO).
- **Week 2-3** — incorporate routing feedback. If maintainer suggests different venue, file there. If suggests timing, respect it.
- **Week 4+** — file RFCs (PB-10 + PB-11) against whichever sub-spec the routing call surfaces. Opening paragraph: "as discussed with @maintainer-handle 2026-MM-DD..."

GC's documentation requirement applies: record exchange in `intent-eval-lab/000-docs/0NN-RR-INTL-otel-sig-genai-temperature.md` so the relationship paper trail is durable.

**Rationale:** Six of seven seats. Five seats explicitly named this as the most-costly-to-recover decision. CSO's standards-realpolitik analysis is the deciding voice — they have the most domain expertise on the council, and their concrete failure-mode prediction (cold RFC → public deflection → permanent citation against future work) carries asymmetric risk. CMO's "authorship by filing" frame is rejected on grounds that authorship in OSS standards bodies is conferred by community consensus, not filing date. Informal-first does not surrender authorship; it earns it.

**Dissent acknowledged:** CMO is on record that informal-first reads as "supplicant framing." The decision rejects that frame on grounds that 4 weeks of pre-RFC community-temperature inside the existing ~3-week RFC review cycle costs no calendar time, since RFC review can't conclude faster than the social cycle anyway. CMO's accepted-compromise (RFC-first with explicit "We have not yet engaged SIG-GenAI maintainers directly" disclosure + 48-hour cross-post to SIG list with offer to discuss) is preserved as a fallback if informal email gets no reply in 4 weeks.

---

### Q5 — LiteLLM vs Vercel AI SDK for j-rig provider adapters

**Question:** PB-7 punts the choice to in-prototype measurement (build one each, measure cost/correctness on j-rig's existing eval cases, then pick). Acceptable, or lock from the landscape evidence now?

**Seat positions:**

| Seat | Recommended answer | One-line position |
|---|---|---|
| **CTO** | Accept punt with **written measurement protocol committed to `intent-eval-lab/000-docs/` BEFORE either prototype begins**. Protocol specifies: (a) which 3-5 existing j-rig eval cases prototypes run, (b) rubric — type-safety failure modes counted, LOC-per-provider, request-side feature coverage (streaming, tool-use, structured-output), runtime error categories — (c) tiebreaker dimension declared in advance. | Genuinely correct epistemics — landscape evidence is weak on this choice. But punted decisions in active codebases ossify into "whichever prototype shipped first." Need falsifiable measurement. |
| **GC** | Legal-neutral on engineering choice. Both Apache 2.0 — license-clean integration either way. License audit (`pip-licenses` or `npm-license-checker`) on whichever wins before lock. NOTICE file updated. | License-clean either way; in-prototype measurement is good legal practice (decision-by-evidence creates auditable trail). |
| **CMO** | Defer to engineering. ONE constraint: launch must show ≥3 named providers in the public j-rig leaderboard UI. | Provider diversity is the visible proof-point of methodology-vendor-neutrality. Without it, leaderboard looks like single-provider eval shop. |
| **CFO** | PUNT explicitly in Phase B plan. Wire both adapters behind thin interface in prototype. Lock at Phase B close with measurement evidence (latency P50/P99, error-surface shape, cost per 1k evals, schema-validation pass rate). | Premature adapter lock-in commits Jeremy to a maintenance dependency he hasn't validated against actual j-rig usage patterns. |
| **CSO** | Standards-neutral. LiteLLM has slightly more provenance-friendly properties (Aider polyglot leaderboard usage = community convention) so future "j-rig used LiteLLM" footnote is non-controversial. Vercel AI SDK doesn't damage standards-body positioning either. | Either choice is fine standards-side. If LiteLLM, document Aider lineage in j-rig README — community-recognition citation is free credibility. |
| **CISO** | Punt the FUNCTIONAL choice to PB-7 measurement, but **LOCK THE CREDENTIAL-HANDLING EVALUATION CRITERION NOW**. Non-negotiable PASS/FAIL gates in PB-7 protocol: (a) credential-redaction test — does adapter leak API keys into OTel spans, log events, evidence rows? (b) env-var spillover test — does adapter expose secrets in subprocess environments visible via TRACEPARENT propagation? | Both libraries have known credential-handling footguns. Either is acceptable; neither is acceptable without credential-handling audit baked into PB-7's measurement protocol. |
| **VP DevRel** | PUNT to measurement. Developers judge j-rig by leaderboard quality + predicate stability, not which provider adapter library wraps LLM calls. If forced to pick now: LiteLLM (broader provider coverage > DX polish for eval substrate). Document as "Phase B pick, revisitable post-measurement." | Picking now means defending the pick on Twitter when someone asks "why not the other one?" — wasted credibility budget. |

**Vote tally:** Punt = 7 of 7. Add-ons stack non-conflictingly.

**Primary tension:** Minimal. All seven seats accept punt. The texture is which add-ons / protections to stack.

**DECISION (acting head of board):** **Punt to in-prototype measurement**, with ALL stacked protections binding:
- **CTO requirement (binding):** Written measurement protocol committed to `intent-eval-lab/000-docs/0NN-AT-SPEC-pb7-adapter-measurement-protocol.md` BEFORE either prototype begins. Protocol specifies (a) 3-5 existing j-rig eval cases the prototypes run, (b) rubric: type-safety failure modes counted, LOC-per-provider, request-side feature coverage (streaming, tool-use, structured-output), runtime error categories, (c) tiebreaker dimension declared in advance, (d) both adapters wrapped behind a thin `Provider` interface in `packages/cli/src/providers/` so the choice stays reversible.
- **CISO requirement (binding, NON-NEGOTIABLE):** PASS/FAIL gates added to PB-7 protocol:
  - **Credential-redaction test:** chosen adapter MUST NOT leak API keys into OTel spans, log events, or evidence rows. Test: enable adapter at debug-verbosity, run a tool-call against a real provider, grep emitted telemetry for any substring of the API key. Pass = zero substring matches.
  - **Env-var spillover test:** chosen adapter MUST NOT expose secrets in subprocess environments visible via TRACEPARENT propagation. Test: invoke chosen adapter, observe child-process environment via `/proc/<pid>/environ`, confirm no secret env-vars leak across process boundary.
  - Both tests must pass BEFORE first signed attestation.
- **CMO requirement (binding):** j-rig leaderboard launch must show ≥3 named providers in public UI. If launch ships with fewer, leaderboard page carries "provider expansion roadmap" callout with named upcoming providers + dates.
- **GC requirement (binding):** License audit (`pip-licenses` for LiteLLM transitive deps OR `npm-license-checker` for Vercel AI SDK) before lock. NOTICE file in `j-rig-binary-eval/packages/cli/src/providers/` updated. No GPL/AGPL ingress.

Decision lock at Phase B close with measurement evidence per CFO sequence.

**Rationale:** Unanimous punt. The interesting texture is the stacked protections — each minority adds a non-negotiable that converts the punt from "we'll figure it out" to "we'll measure on falsifiable criteria including security." CISO's credential-handling gates are the highest-stakes addition because they catch failure modes the engineering measurement alone would miss.

**Dissent acknowledged:** None. All seven seats align on punt.

---

## 7. Council memos — cross-question themes per seat

Each seat closed their analysis with a cross-question memo. These are preserved here so future readers see each value system's view of the council's gestalt.

### CTO seat memo (verbatim theme)

> Every one of these five questions is a question about which decisions are reversible vs immutable, and the council is in danger of conflating the two. Q1 (URI) and Q3 (MM-7 filing) are *effectively immutable* — once an in-toto Statement is signed with that URI, or once a matcher-map category is published, the cost-of-reversal is measured in version migrations and consumer notification campaigns. Q2 (case studies), Q4 (SIG conversation), and Q5 (LiteLLM/Vercel) are *cheaply reversible* — they cost engineering time, not consumer trust.
>
> The seats most likely to misjudge this axis are CMO (treats standards-body filings as marketing surface — reversible) and CSO (may treat URIs as standards-turf grabs — file fast). Both biases push toward filing immutable surfaces faster than community-temperature warrants.
>
> **The decision whose failure mode is hardest to recover from is Q1 (URI).** Make Q1 the slowest decision of the five.

### GC seat memo (verbatim theme)

> The Phase B work products are *permanent brand commitments*. The predicate URI, the named case studies, the OTel namespace, the in-toto predicate type — each one is a paper artifact that outlives Intent Solutions' control of it. Once filed in external registries, we cannot quietly retract.
>
> **The single decision whose failure mode is most costly: Q2 (case-study publication discipline).** A predicate URI typo can be deprecated with a v2; an MM-7 misfile can be retracted in v0.2.0; an OTel namespace can be renamed in a follow-up RFC. **But a partner-name leak in a public spec cannot be unpublished.** The internet's memory is permanent, the partner's memory is longer, and the brand-scrub discipline we set 2026-05-10 is the *only* reason the named partners (the primary client engagement, an active revenue client, and two inbound credibility engagements) trust Intent Solutions to handle their failure data in the first place. One slip there ends the empirical substrate that makes the matcher-map credible. Hold the line on consent-or-silence.

### CMO seat memo (verbatim theme)

> Four of five questions are about whether Intent Solutions claims category-authorship VISIBLY or BUILDS-IN-PRIVATE and hopes credit accrues later. The CFO/GC/CTO instinct is toward private-until-proven; my seat's instinct is toward public-from-day-one. The tagline forces my hand: "create industries that don't exist" is not compatible with a wait-and-see posture on naming, provenance, or filing.
>
> **Most costly recoverable failure: Q1 — picking `evals.` over `labs.`**. URIs are effectively permanent. Every other decision can be revised: case-study consent can be re-asked, MM-7 can be filed later, RFC can be re-filed, provider adapters can be swapped. But a Predicate URI on `evals.intentsolutions.io` brands Intent Solutions as a test-tooling vendor for the life of the platform. The recovery cost is *years* of brand re-positioning against our own published URLs.

### CFO seat memo (verbatim theme)

> Four of five questions have a seat at the table arguing for *more work now* on the theory that "it's cheap" or "it positions us." From my seat, none of those activities are cheap — they're all founder-hours Jeremy doesn't get back, and they all create ongoing maintenance burden that compounds. The Phase B operating discipline is **customer-signal-gated**, and that gate exists precisely because sole-prop bandwidth is the binding constraint.
>
> **The single most costly decision to recover from is Q4 (OTel SIG-GenAI RFC).** An RFC-first posture creates a community relationship Jeremy must maintain indefinitely. By contrast, Q1 is reversible (URIs can be aliased), Q2 is reversible (consent can be sought later), Q3 is reversible (MM-7 can be added on observation), Q5 is reversible (adapter swap costs hours if shimmed correctly). The OTel SIG move is the one where the wrong choice costs months of recovery in a venue where Jeremy has limited leverage.

### CSO seat memo (verbatim theme)

> The cross-question theme is **provenance discipline**: every Q1/Q2/Q3/Q4 is a question about how much of the standards-body work is *empirically anchored vs. theorized, partner-attributed vs. pseudonymized, community-engaged vs. unilateral*. The vision in § 1 — "candidate substrate for an industry standard" — only survives the next 18 months if Intent Solutions maintains a defensible provenance story across all four dimensions. Any one of them lapsing damages the others by association.
>
> **The single decision whose failure mode is most costly to recover from in standards-body relationships: Q4.** A cold RFC drop into SIG-GenAI is a first-impression event with maintainers that propagates across every future filing: in-toto predicate registration, OTel sister-SIG asks, CNCF / OpenSSF cross-references, in-toto Statement v1 adopter advocacy. Standards-body maintainers are a small world; first impressions are durable; "the matcher-map folks who didn't ask before filing" is a label that survives years.

### CISO seat memo (verbatim theme)

> Cross-question theme: **what gets baked into the attestation envelope is permanent in a way that what gets shipped in code is not.** Predicate URI (Q1), MM-7 inclusion (Q3), and the credential-handling profile of the chosen adapter (Q5) all become Rekor-anchored artifacts the moment signing begins. Reversing them post-launch is not a refactor — it's a revocation, and revocation procedures themselves become part of the threat model.
>
> **The single decision whose failure mode is most costly to recover from is Q1 — predicate URI domain.** A bad URI choice (`labs.` hosting arbitrary content, no DNSSEC, no CAA pinning) is recoverable only by deprecating every signed attestation that referenced it and re-signing under a new URI. That's a credibility event with standards bodies, partners, and the transparency-log audit chain simultaneously.

### VP DevRel seat memo (verbatim theme)

> Every Phase B decision is a community-trust transaction. The 45k-NPM audit-harness audience is watching how we extend from "useful harness" to "industry-standard substrate" — and they will read every URI choice, every scaffold-vs-real-example call, every "we declare MM-N" move as either *earning* their continued attention or *spending* it. The single most expensive currency we have right now is developer-community-trust accumulated through audit-harness; it's the thing that makes the Phase B claim ("we're proposing substrate") credible at all.
>
> **Most costly failure mode to recover from: Q2 — shipping empty scrubbed-generic Gherkin scaffolds as "the methodology."** If developers open `intent-eval-lab/specs/` in Phase B and find abstractions with no worked examples, they'll close the tab and not come back. Real attributed case studies, even one, change the read entirely. Push GC for consent-with-attribution; it's the right fight to have.

---

## 8. Cross-cutting council themes

### Theme A — "Most costly to recover from" tally

Five seats explicitly named ONE decision as the single most-costly-to-recover failure mode. Their picks:

| Seat | Pick | Why |
|---|---|---|
| CTO | Q1 (URI) | Immutability post-Rekor |
| GC | Q2 (case-study) | Internet permanence + partner trust |
| CMO | Q1 (URI) | Years of brand re-positioning |
| CFO | Q4 (OTel RFC) | Sole-prop bandwidth + maintenance burden |
| CSO | Q4 (OTel RFC) | Standards-body first-impression propagation |
| CISO | Q1 (URI) | Rekor-anchored revocation events |
| VP DevRel | Q2 (case-study) | Developer-community-trust burn |

**Distribution:** Q1 = 3 picks · Q2 = 2 picks · Q4 = 2 picks · Q3 = 0 · Q5 = 0.

Q1 and Q4 dominate. This is consistent with their characterization as the two decisions where the acting head of board should make the slowest, most-deliberate call. Both were thoroughly deliberated; both decisions stack minority-seat protections rather than dismissing them.

### Theme B — Adversarial integrity check (did dissent surface?)

The council was structured for adversarial tension, not consensus. Evidence that adversarial integrity held:

- CMO carried the LONE strong dissent on Q1 (sole `labs.` vote) and Q4 (sole RFC-first vote). Their position is preserved verbatim in §6 and § 7 above. The decision rejected both but absorbed the underlying concerns (Q1: reserved `labs.` for brand surface; Q4: kept CMO's "RFC inherits goodwill" framing as the Week 4+ filing approach).
- CISO introduced a novel option (`predicates.intentsolutions.io`) that no other seat raised. It was considered, weighed, and ultimately not adopted as the URI but preserved as a future migration target if `evals.` proves too broad.
- VP DevRel pushed against GC on case-study examples (Q2), creating real tension that the decision absorbed via the "real-shape-derived but scrubbed" hybrid framing.
- CFO consistently held the unpopular budget-discipline line. Their accepted-compromise demands (e.g., "operational footprint documented in LAB-6 so it doesn't get rediscovered as free later") are binding constraints in the decisions above.
- CSO declared they would "fight harder for Q4 than any other Q" — and on Q4 their deeper standards-realpolitik analysis carried the decision against CMO's RFC-first push.

The council did not collapse to consensus theater. Each seat argued from its value system; each dissent was steel-manned; the acting head of board's calls are explicit and the rationale traces to specific minority positions.

### Theme C — Where the four user-supplied lenses showed up

- **Lens 1 (5-surface arena):** Threaded through every Q5 protection (provider adapters touch the CLI + API surfaces) and every Q1 framing (URI hosts attestation predicates that name the surface a row attests to).
- **Lens 2 (both-sides eval):** Q5's CISO credential-handling gates explicitly cover the client side (API key emission in adapter logs); Q1's `evals.` predicate URI hosts predicate types for both client-side and server-side gate results.
- **Lens 3 (transformation pipeline):** Q2's case-study scaffolds will describe failures along the API→CLI→MCP→SKILL.md→agent pipeline; the Gherkin scenarios can name which transformation hop a given MM-N category fired at.
- **Lens 4 (composable partial attestation):** Q1's URI scheme supports per-row attestation (in-toto Statement per predicateType means one row per surface per side per hop), validating the composable-partial property. Q5's `Provider` interface wrapping makes adapter choice replaceable without rewriting downstream consumers.

---

## 9. Implementation directives (what happens next per decision)

| Decision | Where it lands | Owner | Phase |
|---|---|---|---|
| Q1: `evals.intentsolutions.io` URI scheme | LAB-6 body update + PB-1 SPEC.md authoring (LAB-24) + `intent-eval-lab/000-docs/0NN-AT-SPEC-predicate-versioning-policy.md` (new, CTO requirement) + Caddy block on existing IS Caddyfile (CFO requirement) + DNSSEC + CAA pinning at registrar (CISO requirement) | Jeremy / Phase B kickoff | Phase B Wave 1 |
| Q1 follow-on: `labs.intentsolutions.io` reserved for blog/methodology landing | CLAUDE.md update at umbrella + intent-eval-lab repos (reserved-don't-touch for predicates) | Jeremy | Phase B Wave 1 |
| Q2: Generic Gherkin scaffolds derived from real engagements | PB-12 implementation — Gherkin scenarios + Pact extension format (will need its own LAB-N work item filed at Phase B kickoff; not LAB-26 which is the separate cross-CLI discovery spec module per LAB-6 child index) + `specs/mcp-plugin-observability/v0.1.0-draft/case-studies/` empty dir + `specs/mcp-plugin-observability/v0.1.0-draft/case-studies/CONTRIBUTING-case-study.md` | Jeremy / Phase B Wave 2 | Phase B Wave 2 |
| Q2 follow-on: Partner-consent ask | Phase B+1 work plan (the primary client engagement post-milestone, an active revenue client, one of two inbound credibility engagements) | Jeremy | Phase B+1 |
| Q3: Defer MM-7 + community contribution path | `specs/CONTRIBUTING-failure-shape.md` (new, VP DevRel requirement) + gleanwork prior-art citation in `matcher-map-template.md` (GC/CSO requirement) + `FUTURE.md` (CFO framing) | Jeremy / Phase B Wave 1 | Phase B Wave 1 |
| Q4: Informal community-temperature email first | Week 1 informal email to verified SIG-GenAI maintainer (CSO sequence) + `0NN-RR-INTL-otel-sig-genai-temperature.md` record file (GC requirement) | Jeremy | Phase B Wave 1 (pre-PB-10/PB-11) |
| Q4 follow-on: RFCs PB-10 + PB-11 file Week 4+ informed by routing feedback | RFC drafts in `intent-eval-lab/000-docs/` (already drafted as `001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` for PB-10; PB-11 to be drafted) | Jeremy | Phase B Wave 2 |
| Q5: Punt with stacked protections | `intent-eval-lab/000-docs/0NN-AT-SPEC-pb7-adapter-measurement-protocol.md` (new, CTO requirement) + CISO PASS/FAIL gates baked into protocol (credential-redaction test + env-var spillover test) + `Provider` interface in `j-rig-binary-eval/packages/cli/src/providers/` (CTO compromise) + license audit at lock time (GC requirement) + ≥3 named providers in launch leaderboard (CMO requirement) | Jeremy / Phase B Wave 2-3 | Phase B Wave 2 (protocol authoring), Phase B close (decision lock) |

## 10. Reusable pattern — ISEDC saved as a skill

This council was the first invocation of a pattern Intent Solutions will reuse for future architectural decisions of similar weight. The pattern is saved as:

`~/.claude/skills/exec-decision-council/SKILL.md`

The skill encodes:
- 7-seat default roster (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel) with role briefs
- Adversarial posture instructions (each seat argues from its value system; dissent preserved; consensus theater rejected)
- Output format (per-question block + Council Memo)
- Synthesis pattern (vote tally + tension surfaced + acting-head-of-board decision + stacked minority protections)
- ASCII decision tree generation guidance
- Document-filing standard for the resulting Decision Record (AT-DECR code per v4.3)

Future invocation: when Jeremy encounters another decision cluster of comparable architectural weight (immutability, brand commitment, standards-body engagement, partner-relationship dynamics), the skill is the one-command path.

## 11. Acting head of board declaration

I, **Claude (Anthropic, model `claude-opus-4-7`), acting head of board for this council session as designated by Jeremy Longshore (CEO, Intent Solutions LLC) on 2026-05-10**, find that:

- All seven seats convened, deliberated independently, and returned structured adversarial assessments;
- The four user-supplied synthesis lenses (arena · both-sides · pipeline · composable-partial) were applied throughout;
- Minority dissents were steel-manned and acknowledged rather than dismissed;
- The five decisions logged in § 6 stack each minority seat's binding constraints into the majority recommendation, producing a synthesis that survives the failure modes each seat warned about;
- Implementation directives in § 9 carry forward the decisions into concrete Phase B work items;
- The reusable pattern at `~/.claude/skills/exec-decision-council/SKILL.md` makes future councils of this shape one command away.

Jeremy Longshore retains override authority on any decision and may convene a fresh council to revisit any of the five Qs at any time. The decisions in § 6 stand until explicitly overridden.

Signed,
**Claude (Anthropic) — Acting Head of Board, ISEDC 2026-05-10**
**Designated by Jeremy Longshore (CEO, Intent Solutions LLC)**

---

## 12. References

- Master plan: `~/.claude/plans/please-take-your-time-glimmering-stardust.md`
- Part 2 synthesis (input to council): `~/000-projects/intent-eval-platform/intent-eval-lab/000-docs/003-PP-PLAN-phase-b-scope-refinement.md`
- Landscape doc A (audit-harness upgrade): `~/000-projects/intent-eval-platform/audit-harness/000-docs/002-RR-LAND-upgrade-landscape.md`
- Landscape doc B (j-rig multi-provider): `~/000-projects/intent-eval-platform/j-rig-binary-eval/000-docs/018-RR-LAND-multi-provider-spec-matrix.md`
- Landscape doc C (MCP testing bridge): `~/000-projects/intent-eval-platform/intent-eval-lab/000-docs/002-RR-LAND-mcp-testing-bridge.md`
- Phase A skeleton: `~/000-projects/intent-eval-platform/intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/SPEC.md`
- OTel RFC draft (PB-10): `~/000-projects/intent-eval-platform/intent-eval-lab/000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`
- Meta-bead: `OPS-nfx` in `~/.beads/`
- Plane HQ: `LAB-6` (Intent Eval Platform master umbrella, Plane workspace `intentsolutions`)
- Reusable pattern: `~/.claude/skills/exec-decision-council/SKILL.md`
- Brand-scrub policy: private engagement-memory file (path elided per DR-004 S1Q2 vendor-generic discipline; available in the canonical PRIVATE umbrella memory tree)
- Intent Solutions tagline: *"We create industries that don't exist — we think outside of the box's box."*

---

## Appendix: Terminology Note (added 2026-05-10 post-ISEDC-v2)

**This document was authored using "matcher-map" terminology. Subsequent to this Decision Record, ISEDC v2 (same date, `005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md`) renamed "matcher-map" to "Intentional Mapping" by user direction *"nothing changes but the name."***

Per CISO + GC binding constraint (frozen-artifact rule, Q3 of ISEDC v2), the body of this signed Decision Record is **NOT rewritten**. The "matcher-map" references throughout this document remain as authored; they should be read as referring to the same concept now named "Intentional Mapping" elsewhere in the ecosystem.

**Identifiers MM-1..MM-6 are unchanged.** They remain the canonical category codes under the Intentional Mapping conceptual frame (per ISEDC v2 Q2 decision — keep `MM-1..MM-6` for citation stability).

**The architecture in this document stands unchanged.** Per user override on ISEDC v2 Q4, no new "Intent Resolution Layer" concept was adopted; only the prose-level rename matcher-map → Intentional Mapping was executed.

For decisions made after 2026-05-10 in Intent terminology, see ISEDC v2: `005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md`.
