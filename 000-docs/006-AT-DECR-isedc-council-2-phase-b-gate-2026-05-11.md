# ISEDC Council Decision Record — Phase B Gate Re-evaluation + Ecosystem Signal Response

| Field | Value |
|---|---|
| **Date convened** | 2026-05-11 |
| **Date decision-locked** | 2026-05-11 |
| **Acting Head of Board** | Jeremy Longshore (CEO, Intent Solutions LLC) — made final calls including one override |
| **Council size** | 8 seats (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel · Research Expert [NEW]) |
| **Questions adjudicated** | 3 (Q2 closed by user override before synthesis) |
| **Decisions logged** | 4 |
| **Adversarial method** | Each seat argued from a distinct value system; dissent preserved; Research Expert added as factual-grounding seat; final calls made by acting head of board |
| **Status** | Decision-locked. |
| **Predecessor** | ISEDC v1 (`004-AT-DECR-isedc-council-record-2026-05-10.md`) · ISEDC v2 (`005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md`) |
| **Meta-bead** | `OPS-2et` (home `~/.beads/`) |
| **Reusable pattern** | `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0 |
| **Synthesis input** | `003-PP-PLAN-phase-b-scope-refinement.md` · `004-AT-DECR-isedc-council-record-2026-05-10.md` |
| **Audience** | Future Intent Solutions sessions; Phase B implementation; standards-body engagement |

---

## 1. Mission of this Decision Record

This document records WHY each decision landed where it did, not just WHAT. Verbatim seat positions are preserved. Dissents are named. The Research Expert seat's factual corrections are recorded. The acting head of board's user override on Q2 is logged with his exact words.

## 2. Why a council, not a single review

Two external signals arrived on 2026-05-11 that were not present when Phase B was scoped and the original gate was set:

1. **@pvncher (Eric Provencher, RepoPrompt) publicly called for MCP tool calling benchmarks** — a credible builder with production MCP tooling naming exactly the gap j-rig + Evidence Bundle fills.
2. **The "ultimate universal MCP server" architecture conversation** surfaced that the Evidence Bundle's gateway/federation pattern is the missing standards layer for multi-domain MCP servers.

Together these constitute external ecosystem validation that the problem space is real and active. The council was convened to deliberate on whether and how these signals change the Phase B gate calculus, gateway scope, and content timing — with 2026-05-10 ISEDC decisions as binding constraints.

## 3. The 6 synthesis lenses

1. **The arena (5 surfaces):** APIs · CLIs · MCP servers · agents · SKILL.md
2. **Both sides:** client-side eval + server-side eval
3. **The transformation pipeline:** API → CLI → MCP → SKILL.md → agent
4. **Composable partial attestation:** every component is a valid entry; silence ≠ failure
5. **Ecosystem clock:** OTel RFC community-review timelines (~3-4 weeks), competing artifacts, window to file first
6. **Sole-prop bandwidth reality:** Jeremy is the only engineer; every Phase B item is opportunity cost against OPS, the primary client engagement, an active revenue client, claude-code-plugins

## 4. Questions brought to the council

| Q | Topic | Status |
|---|---|---|
| **Q1** | Phase B Gate Re-evaluation — do external signals justify beginning any Phase B groundwork before paying-customer signal? | Deliberated → DECIDED |
| **Q2** | @pvncher engagement strategy — should IS engage Eric Provencher directly? | **CLOSED BY USER OVERRIDE before synthesis** |
| **Q3** | Universal MCP Server as Phase B entry vector — does the gateway/federation pattern warrant a new Phase B module or repo? | Deliberated → DECIDED |
| **Q4** | Content timing — publish @pvncher ecosystem post and/or MCP architecture post now, or hold? | Deliberated → DECIDED |

## 5. Research Expert factual correction (load-bearing)

The Research Expert seat (8th seat, added for this session) flagged a **material factual error in the council brief** that affected several seat arguments:

> **BRIEF CLAIM:** "45,000+ NPM downloads for `@intentsolutions/audit-harness`"
> **VERIFIED FACT:** `@intentsolutions/audit-harness` has approximately **1,140 total downloads** (verified 2026-05-11 from npm registry).
> **SOURCE OF CONFUSION:** The 45,000+ figure belongs to the `claude-code-plugins` npm package, not the audit-harness package.

**Impact:** VP DevRel's "community trust bank" arguments and several CMO and CSO positions that cited the 45k figure are recalibrated against the actual 1,140 number. This does not invalidate those positions — the audit-harness still has real-world usage — but arguments framed as "we have massive community trust to leverage" are weaker than briefed.

This correction is preserved here per Research Expert mandate: the council's decisions must be grounded in what is actually true.

## 6. Council composition — 8 seats

| Seat | Value system | Bias | New tension this session |
|---|---|---|---|
| **CTO / Chief Architect** | Technical durability · schema integrity · immutability | Deliberation > commit · empirical evidence | Whether gateway adds scope creep vs fills real architectural gap |
| **GC / General Counsel** | IP · partner-consent · brand-surface · audit-trail | Written consent before any reference · paper trail | Any engagement = brand commitment before consent |
| **CMO / Industry-Standard Strategist** | Positioning · first-mover · narrative · tagline | Visible > silent · ambitious > conservative | Wants all gates opened; ecosystem signal = launch signal |
| **CFO / Strategic Operator** | Sole-prop bandwidth · customer-signal gating · opportunity cost | Defer until customer evidence justifies | Hard gate should stand; @pvncher ≠ paying customer |
| **CSO / Chief Standards Officer** | OTel SIG-GenAI realpolitik · RFC sequencing | Community-temperature ALWAYS precedes RFC · first-impression is permanent | Community-clock argument supports standards-track items beginning now |
| **CISO / Chief Information Security Officer** | Supply-chain attestation integrity · signing · threat model | Pre-commit gates for any new signing surface | Gateway auth surface needs credential-redaction + env-var + routing-isolation gates |
| **VP DevRel / Head of OSS Community** | Developer-audience · OSS dynamics · friction-to-adopt | Artifact > concept · informal > formal | audit-harness NPM count ~1,140 (not 45k) recalibrates trust-bank argument |
| **Research Expert (NEW)** | Synthesis + factual grounding · evidence over theory | "Show me the data" · prevent speculation from driving decisions | Flagged the 45k→1,140 NPM correction; grounded every Q in bead/Plane/GH state |

---

## 7. Per-question council record

### Q1 — Phase B Gate Re-evaluation

**Question:** The original gate is "first paying-customer signal." Do @pvncher's public MCP benchmark call + the universal MCP server architecture conversation justify beginning any Phase B groundwork before that signal arrives?

**Options:**
- A: Hard gate stands. No Phase B work until first paying-customer signal.
- B: Standards-track items only (PB-10 + PB-11 OTel RFCs, PB-2 predicate URI registration) can begin now — community-review-clock dependencies are bottlenecked on filing, not implementation.
- C: Full Phase B kickoff now. @pvncher's advocacy IS the market signal.

**Seat positions:**

| Seat | Vote | One-line position |
|---|---|---|
| **CTO** | **B** | RFC clock is bottleneck-independent from implementation readiness; every week of delay is pure self-inflicted calendar loss. |
| **GC** | **B** | RFC filing creates no brand commitment or consent risk; the customer gate was written to prevent premature commercial positioning, not block standards drafting. |
| **CMO** | C (→**B** compromise) | @pvncher's statement is category vocabulary validation; the gate is now vestigial. Accepts B as compromise since the RFC clock argument is the most urgent lever. |
| **CFO** | A (→**B informal email only** compromise) | The gate exists to filter exactly this scenario. Accepts only the ISEDC Q4-locked Week 1 informal SIG-GenAI email as minimum — 90 minutes, not a Phase B engineering commitment. |
| **CSO** | **B** | PB-10 is already drafted. Every day it sits unfiled is a day the review window doesn't start. The informal email discipline (already locked Q4 decision) gates it correctly. |
| **CISO** | **B** | Standards-track items carry no credential surface and no signing infrastructure. No attack surface is opened by RFC filing; scope fence must be explicit in writing. |
| **VP DevRel** | **B** | Table-stakes sequencing. Recalibrated to actual audit-harness count (~1,140) — trust-bank argument weaker but standards filing still extends into new domain without requiring paying customer. |
| **Research Expert** | **B** | Engineering cost is near-zero. The customer-signal gate was designed to prevent engineering time against unvalidated demand — it over-applies to a 30-minute informal email and a namespace registration already decision-locked by ISEDC Q1. |

**Vote tally:** B = 7 of 8 · A = 1 (CFO, with compromise accepting ISEDC Q4 informal email as minimum)

**Primary tension:** CFO holds that ecosystem validation ≠ business signal. All other seats accept the CSO argument that the community-review clock is a real constraint independent of the customer-gate logic. CMO's C recommendation has no other supporters; their accepted compromise is B.

**DECISION:** **Option B — standards-track items may begin now, with explicit scope fence.**

Concretely:
- **PB-10** (OTel RFC `agent.rollout.gate.*` semantic conventions): the ISEDC Q4-locked sequence governs — Week 1 informal email to verified SIG-GenAI maintainer (already decision-locked, costs 30 minutes), RFC filing Week 4+ informed by routing feedback. This is the MINIMUM action and it was already locked.
- **PB-11** (OTel RFC Intentional Mapping signal vocabulary MM-1..MM-6): same sequence as PB-10, in parallel.
- **PB-2** (predicate URI registration at `evals.intentsolutions.io`): DNSSEC + CAA records must be verified first per ISEDC Q1 CISO binding constraint. Then file.
- **ALL other Phase B items remain hard-gated on first paying-customer signal.** PB-1 (in-toto wrap), PB-3, PB-4, PB-5..PB-9, PB-12 do not begin.

**Stacked binding constraints (from minority seats):**
- CFO: the scope fence is written and enumerated explicitly in this record. "Standards-track items only" means PB-10, PB-11, PB-2, and the ISEDC Q4 informal email. Not PB-1. Not any implementation.
- CISO: PB-2 URI registration does not execute until DNSSEC + CAA records are verified on `evals.intentsolutions.io` (existing ISEDC Q1 constraint, re-stated here as a Q1 pre-condition).
- GC: RFC drafts for PB-10/PB-11 receive GC review for implied-partner-endorsement language before any community submission.
- CTO: the scope fence must be enumerated in writing — "standards-track exception" language goes in the tracking update to LAB-6, not just in conversation.

**Rationale:** Seven of eight seats. The distinguishing argument — that the community-review clock is a real calendar constraint that is bottlenecked on filing, not on implementation — is supported by the Phase B wave plan document itself (which calls PB-10/PB-11 "Wave 1" with the explicit rationale that "community-review time is the dominant cost"). The customer-signal gate governs engineering capacity; it was not designed to govern a 30-minute mailing-list post.

**Dissent acknowledged:** CFO is on record that the gate was designed to filter exactly this scenario and that softening it sets a precedent. The decision rejects full gate-softening (no Option C) but accepts the CFO's minimal interpretation (the ISEDC Q4 informal email sequence that was already locked). CFO's concern about precedent-setting is absorbed by the explicit scope fence in this record.

---

### Q2 — @pvncher Engagement Strategy

**CLOSED BY USER OVERRIDE (Jeremy Longshore, acting head of board).**

Before synthesis, Jeremy directed: *"i dont need to engage with that dude nor do i want to dont rewrite the plan just drop the engagement part off we ride solo me u and the council"*

**Decision: No engagement with @pvncher now or in the future on this topic. IS operates solo.**

The council deliberated (7 of 8 seats returned before override: CTO = D, GC = D, CMO = B, CFO = D, CSO = B-compromise, CISO = D, VP DevRel = D). Seven of seven returning seats recommended either D (hold until PB-1) or B (lightweight public reply) — no seat recommended C (direct outreach). Jeremy's override is consistent with the D majority position and resolves the B/D debate definitively.

**This decision is permanent** for the scope of this council record. Future councils may revisit if Jeremy explicitly brings it back.

---

### Q3 — Universal MCP Server as Phase B Entry Vector

**Question:** Does the gateway/federation pattern warrant a new Phase B module (inside intent-eval-lab) or a 4th repo? Or is it deferred?

**Options:**
- A: No gateway implementation. Current 5-surface arena is sufficient.
- B: Gateway reference implementation as a new Phase B module inside intent-eval-lab.
- C: Gateway reference implementation as a 4th repo.
- D: Defer to Phase C or a paid engagement deliverable.

**Seat positions:**

| Seat | Vote | One-line position |
|---|---|---|
| **CTO** | **B** (Wave 3+, after PB-1) | Module inside intent-eval-lab is architecturally honest — a demonstration artifact, not an independently distributable tool. 4th repo = schema-integrity error. |
| **GC** | D (→**B** compromise, post-PB-1, no partner-derived code) | Gateway = new IP questions; deferral keeps blast radius contained. Accepts B after PB-1 with GC review of first commit. |
| **CMO** | **B** (Wave 2) | First-mover insight on gateway-as-evaluation-substrate has not been publicly filed. Inside intent-eval-lab contains scope; Phase C deferral = category abandonment. |
| **CFO** | A (→**B spec-only note, 2 hours** compromise) | Gateway before PB-1 ships = scope creep. Accepts a single markdown architecture note in `intent-eval-lab/specs/` with no implementation — costs 2 hours, not weeks. |
| **CSO** | **B** (→D compromise) | Inside intent-eval-lab is architecturally clean for a reference implementation. Accepted D as fallback if sole-prop bandwidth cannot support it. |
| **CISO** | A (→**B with 3 non-negotiable gates** if overruled) | Hard NO without (1) gateway-specific threat model doc, (2) PASS/FAIL gates for credential-redaction + env-var spillover + multi-tenant routing isolation, (3) DNSSEC + CAA verified on `evals.intentsolutions.io` before first gateway-signed attestation to Rekor. |
| **VP DevRel** | **D** | Gateway can't federate what doesn't exist yet. PB-11 + PB-12 must ship before a gateway has anything to demonstrate composable attestation against. A module without the eval substrate it federates is a demo, not a reference. |
| **Research Expert** | **D** + FUTURE.md capture | Zero beads, GH issues, or Plane issues represent this work — not in any tracked backlog. Scope expansion without tracking violates three-layer mirror discipline. File a FUTURE.md entry as the capture mechanism. |

**Vote tally:** B = 3 (CTO, CMO, CSO) · D = 3 (GC, VP DevRel, Research Expert) · A = 2 (CFO, CISO)

**Primary tension:** Genuine 3-way split. The strongest arguments:
- **For B:** CTO's architectural argument (module-in-lab, not 4th repo), CMO's first-mover insight argument
- **For D:** VP DevRel's "gateway can't federate what doesn't exist yet" argument, Research Expert's "zero tracking entries = not a real backlog item"
- **For A:** CISO's non-negotiable pre-commit gates (which themselves are substantial work), CFO's bandwidth reality

**Novel options introduced:** CFO proposed "B as spec-only markdown architecture note, ~2 hours, no implementation." Research Expert proposed "FUTURE.md entry with trigger condition." Neither is a full B or D.

**DECISION:** **Hybrid: FUTURE.md entry + architecture note (CFO/Research Expert synthesis), with explicit trigger condition.**

Concretely:
- File `intent-eval-lab/000-docs/FUTURE.md` (or add to existing if present) with a gateway architecture section documenting: (a) the gateway/federation pattern as production architecture for multi-domain MCP servers, (b) why Evidence Bundle's composable partial attestation is the missing standards layer, (c) the connection to PB-11/PB-12 as prerequisites, (d) trigger condition for revisiting.
- **Trigger condition for revisiting:** "Pursue gateway reference implementation when EITHER (a) a paying customer names it explicitly OR (b) PB-11 + PB-12 have shipped and sole-prop bandwidth allows Wave 3 scope."
- This is **not Option B** (no implementation, no new module, no new CI). This is **lighter than Option D** (not a permanent deferral — captures the insight with a named re-entry condition).
- **Option C is rejected** by all seats except none — creating a 4th repo without a paying-customer signal or implementation precedent is consensus-refused.

**Stacked binding constraints (carry forward even if trigger fires):**
- CISO non-negotiables apply the moment any gateway code is committed: (1) gateway-specific threat model doc in `intent-eval-lab/000-docs/`, (2) PASS/FAIL gates for credential-redaction + env-var spillover + multi-tenant routing isolation, (3) DNSSEC + CAA verified before first signed gateway attestation.
- GC: first gateway module commit receives GC review for implied-endorsement language.
- CTO: any implementation lives in `intent-eval-lab/` as a module, not a 4th repo. Period.
- Research Expert: when trigger fires, create bead + GH issue + Plane issue FIRST per three-layer mirror discipline.

**Rationale:** The 3-way split warrants a synthesis that doesn't sacrifice the insight or the security discipline. CFO's "2-hour spec-only note" and Research Expert's "FUTURE.md + trigger" are the same motion at different granularity. The correct path captures the architectural insight durably (so future sessions don't rediscover it) without committing sole-prop implementation hours to an untracked, unvalidated scope item. The CISO's pre-commit gates are preserved as binding for when the trigger fires — they are not discarded just because implementation is deferred.

**Dissent acknowledged:** CMO is on record that "deferred = category abandonment." The FUTURE.md entry with trigger condition partially satisfies CMO — the insight is captured and publicly committable as an architecture note. CTO is on record that Option B (inside intent-eval-lab) is architecturally correct when the trigger fires — that guidance is preserved as the structural decision when revisited.

---

### Q4 — Content Timing: @pvncher + Universal MCP Server

**Question:** Publish the @pvncher research/ecosystem post and/or the MCP server architecture post now, or hold?

**Note:** Q2 override removes any @pvncher-engagement framing from the ecosystem post. The post becomes: "here is the problem space and the ecosystem signal" with no IS-to-@pvncher engagement implied.

**Options:**
- A: Publish both posts now.
- B: Publish the @pvncher research/ecosystem post now. Hold MCP server architecture post until reference implementation exists.
- C: Hold both until Phase B Wave 1 ships.
- D: Publish neither.

**Seat positions:**

| Seat | Vote | One-line position |
|---|---|---|
| **CTO** | **B** | Ecosystem post is pure research synthesis — requires no platform artifact; MCP architecture post makes implementation capability claims that cannot be supported until reference implementation exists. |
| **GC** | C (→**B with GC review** compromise) | Both posts are brand surface; ecosystem post accepted if GC reviews for implied-endorsement language. |
| **CMO** | **B** | Publish ecosystem post while @pvncher's tweet is live. Holding the MCP architecture post until PB-1 ships makes it stronger. Two sequential content events > two simultaneous. |
| **CFO** | C (→**B with zero-promise framing** compromise) | Content without shipped artifacts is marketing without product. Accepts B only if ecosystem post makes no Phase B timeline commitments. |
| **CSO** | **B** | Ecosystem post is community-temperature positioning before RFC filing — exactly the CSO sequence. Holding MCP architecture post correct. |
| **CISO** | **B** | Ecosystem post has no signing surface, no credential mention, no attestation claim — low-risk. MCP architecture post held until Q3 is resolved (no gateway threat model exists yet). |
| **VP DevRel** | C (→**B with concrete PB-1 date** compromise) | Both posts need artifact anchor. Accepts B only if ecosystem post includes "artifact forthcoming, Phase B Wave 1, target date X." |
| **Research Expert** | **B** | Ecosystem post is grounded in observable facts and is legitimate research content the lab exists to produce. MCP architecture post violates `intent-eval-lab/CLAUDE.md` Operational Rule 4: don't publish if methodology hasn't been demonstrated empirically. |

**Vote tally:** B = 6 of 8 · C = 2 (GC, CFO/VP DevRel with compromise accepting B)

**Primary tension:** GC, CFO, and VP DevRel's compromise positions all accept B under conditions. The conditions are non-conflicting and stack cleanly. Research Expert's invocation of `intent-eval-lab/CLAUDE.md` Operational Rule 4 is the strongest structural argument for holding the MCP architecture post.

**DECISION:** **Option B — publish ecosystem post; hold MCP architecture post.**

Concretely:
- **Ecosystem post (publish):** Frame as "here is the problem space and why it matters" — not "here is what IS has built." Cite observable facts: the MCP tooling landscape, the gap in evaluation standards, the evidence-bundle thesis as a methodology in development. No Phase B timeline commitments, no promises about specific ship dates.
- **MCP server architecture post (hold):** Held until (a) Q3 trigger fires and gateway architecture note exists in FUTURE.md/000-docs AND (b) PB-1 ships. Both conditions required.

**Stacked binding constraints:**
- GC: ecosystem post text receives GC review for implied-endorsement language before publish.
- CFO: zero Phase B timeline commitments in ecosystem post. "Methodology in development" framing, not "shipping soon."
- CISO: MCP architecture post held until Q3 CISO conditions are met (threat model doc exists). Publishing architectural guidance for a gateway before the threat model exists is not acceptable.
- Research Expert: ecosystem post must frame IS as recognizing the problem, not having the solution. "What the space needs" > "what we've built."

**Rationale:** Six of eight seats. The Research Expert's structural argument (CLAUDE.md Operational Rule 4: don't publish what hasn't been demonstrated empirically) provides the clearest line between the two posts. The ecosystem post is empirically grounded in observable signals. The MCP architecture post requires artifacts that do not yet exist. The conditions stack without conflict and are all achievable before publish.

---

## 8. Council memos — cross-question themes per seat (verbatim)

### CTO seat memo

> All three live questions share one axis: the difference between filing a claim and having an artifact that supports it. Option B on Q1 is correct because the OTel RFC filing is a claim about vocabulary, not about implementation — and vocabulary claims can be filed before implementation artifacts exist without credibility damage, as long as the filing is accurate. Option D on Q3 (as decided) is correct because a gateway module that has no eval substrate to federate is not a reference implementation; it is a demo. Option B on Q4 is correct for the same reason as Q3: the ecosystem post cites observable signals; the MCP architecture post cites capability that hasn't shipped. The platform's long-term schema integrity depends on never getting ahead of its own evidence. That is the composable partial attestation principle applied to IS's own positioning.
>
> **Most costly to recover from: Q3** (if the council had chosen to create a 4th repo). A premature 4th repo is a namespace error that compounds over time and cannot be quietly undone. The FUTURE.md + trigger solution avoids this permanently.

### GC seat memo

> The throughline is brand commitment vs brand surface. Every question this session involves some version of "can we reference this capability or this person or this architecture before we have the consent framework or the artifact to support it?" The answer is: the ecosystem post is the only Q4 action that passes the brand-surface test under current conditions. The MCP architecture post fails until the gateway threat model exists. The gateway module fails until PB-1 ships and a GC review occurs. The Phase B gate opening fails unless the scope fence is explicit and enumerated in this record (it is).
>
> **Most costly to recover from: Q4** (if MCP architecture post had been published now). Publishing architectural guidance for a gateway we haven't threat-modeled, before PB-1 ships, creates reader expectations IS cannot meet. An ecosystem post can be followed up with "here is the artifact." An architecture post that is wrong about the security posture of the architecture it describes is a credibility event, not a marketing miss.

### CMO seat memo

> Three of four questions resolved to "begin the thing with constraints" rather than "hold everything." That is the right outcome. The CMO seat's consistent position is that waiting for perfect condition is how category ownership is ceded. Q1 Option B correctly starts the RFC clock. Q4 Option B correctly plants the ecosystem stake. The FUTURE.md capture on Q3 is acceptable as a minimum — it is at least a public note that IS recognized the gateway connection before anyone else filed it. The Q2 override is Jeremy's call and the council respects it.
>
> **Most costly to recover from: Q1** (if Option A had held). Standards-body vocabulary, once established by a first-filed RFC, is nearly impossible to displace. Every week the PB-10/PB-11 RFCs sit unfiled is a week that community familiarity builds around competitor vocabulary. The gate logic was correct when written; it over-applied once external ecosystem pull existed.

### CFO seat memo

> The discipline I insisted on was scope-fencing, not gate-holding. Option B on Q1 is acceptable because the scope fence in this record is explicit — PB-10, PB-11, PB-2, and the ISEDC Q4 email. Nothing else. That fence is load-bearing. If "standards-track only" drifts to "well, PB-1 is kind of standards-track" in the next session, this record is the corrective. The FUTURE.md on Q3 costs 2 hours, not 2 weeks, and it captures the insight without burning bandwidth. The ecosystem post on Q4 is acceptable if it contains zero timeline commitments.
>
> **Most costly to recover from: Q1** (if the scope fence is not honored). The gate was not arbitrary. It was a discipline mechanism. Softening "standards-track items only" to "well, we're already doing some Phase B work, so let's continue" is the compounding failure mode. The scope fence in this record prevents that. If it erodes in a future session, this record is the evidence that it was explicitly set.

### CSO seat memo

> The community-clock argument carried Q1. That argument is grounded in a specific fact: the OTel SIG-GenAI review cycle is 3-4 weeks, it starts on filing, and PB-10 is already drafted. The informal-first discipline from ISEDC Q4 remains intact — the SIG-GenAI maintainer email comes first, RFC follows Week 4. Nothing about Q1 Option B violates the Q4 locked decision; it operationalizes it. The FUTURE.md on Q3 is architecturally conservative but preserves the insight. The ecosystem post on Q4 serves as community-temperature positioning before the RFC lands.
>
> **Most costly to recover from: Q1** (if Option A had held). The RFC community review window is not recoverable once ceded. If competitors file in OTel SIG-GenAI while IS waits for a paying customer, the vocabulary bakes around their framing, not ours. Standards-body first-impression events are permanent.

### CISO seat memo

> The gateway threat model gates (Q3) are the highest-stakes items in this session. I accepted the FUTURE.md synthesis rather than fighting for Option A because the FUTURE.md captures my non-negotiable conditions as binding pre-commit gates rather than discarding them. When the trigger fires — paying customer names gateway explicitly, or PB-11 + PB-12 ship — those three gates activate: gateway threat model doc, PASS/FAIL credential-redaction + env-var spillover + routing-isolation test suite, and DNSSEC + CAA verification on `evals.intentsolutions.io`. None of those are negotiable when implementation begins. They are in this record because the council approved them here. Future implementations are bound by this record.
>
> **Most costly to recover from: Q3** (if implementation had been approved without pre-commit gates). A gateway that routes tool calls and holds credentials, if it signs anything before the threat model is written and the PASS/FAIL gates pass, creates a Rekor entry proving IS shipped a signing system with a known-class vulnerability. That is not a reputational risk — it is a standards-body relationship termination event.

### VP DevRel seat memo

> The audit-harness NPM correction matters. The pre-loaded brief's 45k figure was wrong; the actual count is ~1,140. Arguments built on "we have massive community trust to leverage" are weaker than briefed. The correct framing is: audit-harness has demonstrated production usage, and PB-10/PB-11 extend the methodology's reach to a new domain without requiring the community adoption we thought we had. That is a different — and more honest — argument. The Q2 override is the right call by any OSS-community read: arriving without an artifact is worse than not arriving at all.
>
> **Most costly to recover from: Q2** (if engagement had proceeded without PB-1). An empirical builder who encounters "we're working on this" and then sees silence for 3+ months classifies the sender as vaporware. That classification propagates in a small developer community. The Q2 override avoids that permanently. Hold the relationship for when PB-1 exists and makes the introduction credible.

### Research Expert seat memo

> Three findings to carry forward:
>
> 1. **The NPM correction is load-bearing.** Arguments anchored to community trust as a leverage asset need to be recalibrated against the real number. This doesn't kill the trust argument — it correctly sizes it.
>
> 2. **The gate logic was right for implementation, wrong for filing.** The research evidence (Phase B wave plan, ISEDC Q4 locked sequence, OTel review-cycle timing) supports Option B on Q1. The customer-gate over-applies to a 30-minute informal email.
>
> 3. **The gateway insight has no tracking artifacts.** Zero beads, GH issues, Plane issues represent gateway scope. The three-layer mirror discipline requires tracking before implementation. The FUTURE.md + trigger condition is correct — it creates the written record without violating bandwidth or security discipline.
>
> **Most costly to recover from: Q1** (if the scope fence had not been explicitly enumerated). "Standards-track only" is a judgment call that drifts without written enumeration. The scope fence in §7 Q1 prevents that drift. It is the most important sentence in this document after Jeremy's Q2 override.

---

## 9. Cross-cutting themes

### Theme A — "Most costly to recover from" tally

| Seat | Pick | Why |
|---|---|---|
| CTO | Q3 (4th repo option) | Namespace error that compounds, cannot be undone |
| GC | Q4 (MCP architecture post published early) | Architecture post with wrong security posture = credibility event |
| CMO | Q1 (Option A holding) | Standards vocabulary bakes around competitor framing |
| CFO | Q1 (scope fence erosion) | Gate softening compounds in future sessions |
| CSO | Q1 (Option A holding) | RFC community review window is not recoverable once ceded |
| CISO | Q3 (gateway without pre-commit gates) | Rekor entry proving signed system with known vulnerability = termination event |
| VP DevRel | Q2 (engagement without artifact) | Closed by user override — moot. Nearest active: ecosystem post timing |
| Research Expert | Q1 (scope fence not enumerated) | Unenumerated "standards-track only" = the drift path |

**Distribution:** Q1 = 4 picks · Q3 = 3 picks · Q4 = 1 pick

Q1 and Q3 dominate. Both decisions received the slowest, most-deliberate adjudication. Both resolved with explicit written constraints rather than open-ended approvals.

### Theme B — Adversarial integrity check

Evidence that adversarial integrity held:

- **CMO** carried the strongest dissent on Q1 (pushed C, accepted B) and Q3 (pushed B as Wave 2, accepted FUTURE.md). Position preserved verbatim in §7 and §8.
- **CFO** held the hardest line on the customer gate and was the lone A vote on Q1. Their accepted compromise (ISEDC Q4 informal email only) is the minimum interpretation that is itself load-bearing.
- **CISO** introduced three non-negotiable pre-commit gates on Q3 that no other seat raised. Those gates are now binding in this record even though the implementation is deferred.
- **Research Expert** introduced a novel finding (NPM correction) that recalibrated multiple seat arguments mid-deliberation — the exact function the seat was designed for.
- **Jeremy's Q2 override** was the sharpest adversarial move of all: closed the question before synthesis, with explicit direction, preserving full solo-operating-mode discipline.

### Theme C — How the synthesis lenses landed

- **Lens 1 (5-surface arena):** Gateway discussion (Q3) is the lens 1 question — does IS add a 6th surface or hold at 5? Decision: hold at 5 via FUTURE.md; revisit when evaluation substrate exists for what the gateway would federate.
- **Lens 2 (both-sides eval):** PB-10/PB-11 RFC scope explicitly covers both client-side and server-side (MM-1..MM-6 can fire from either direction). Q1 Option B preserves this correctly.
- **Lens 3 (transformation pipeline):** Gateway is the API→MCP hop. Correctly deferred until PB-11 codifies the MCP server surface signals (which the gateway would attest to).
- **Lens 4 (composable partial attestation):** The ecosystem post (Q4) is itself a partial attestation — it attests to problem-space validity without attesting to implementation existence. This is the lens 4 principle in content form.
- **Lens 5 (ecosystem clock):** The clock argument carried Q1 Option B. It was the decisive factor against CFO's Option A.
- **Lens 6 (sole-prop bandwidth):** CFO's consistent lens 6 application shaped every compromise position. The FUTURE.md synthesis on Q3 is entirely lens 6 — captures the insight at near-zero bandwidth cost.

---

## 10. Implementation directives

| Decision | Action | Where it lands | Timing |
|---|---|---|---|
| Q1: Phase B standards-track items begin | Week 1 informal SIG-GenAI email (ISEDC Q4 sequence, already locked) | Jeremy's email/calendar | Next session |
| Q1: Scope fence enumerated | Update LAB-6 (Plane) with explicit Phase B scope fence: "PB-10, PB-11, PB-2 only; all other Phase B hard-gated on paying-customer signal" | LAB-6 comment via bd-sync | This session |
| Q1: DNSSEC + CAA | Verify `evals.intentsolutions.io` records before PB-2 registration | VPS/registrar config | Before PB-2 files |
| Q2: No engagement (user override) | No action required. Record is the artifact. | This Decision Record § 7 Q2 | Permanent |
| Q3: FUTURE.md entry | Author `intent-eval-lab/000-docs/FUTURE.md` with gateway architecture section + trigger condition | `intent-eval-lab/000-docs/FUTURE.md` | This session |
| Q3: CISO gates on file | Pre-commit gate requirements preserved in this record | This Decision Record § 7 Q3 | Activate when trigger fires |
| Q4: Ecosystem post | Author + GC-review + publish ecosystem post (problem-space framing, no IS solution claims) | startaitools.com | Next session |
| Q4: MCP architecture post | Hold until Q3 trigger fires AND PB-1 ships | Backlog | Phase B Wave 1 + Q3 trigger |

---

## 11. ASCII decision tree

```
ISEDC 2026-05-11 — Phase B Gate + Ecosystem Signal
═══════════════════════════════════════════════════

Q2 CLOSED BY USER OVERRIDE (Jeremy: "we ride solo")
  └── No engagement. Permanent. No revisit needed.

Q1 — Phase B Gate
  7/8 for Option B
  ├── DECISION: Option B — standards-track only
  │   ├── PB-10/PB-11: informal SIG-GenAI email → RFC Week 4+
  │   ├── PB-2: predicate URI registration (DNSSEC/CAA first)
  │   └── ALL other Phase B: hard-gated on paying customer
  └── Scope fence: explicit, enumerated, in this record
      └── CFO accepting this scope fence = their accepted compromise

Q3 — Universal MCP Server / Gateway
  B=3 · D=3 · A=2 → 3-way split → hybrid synthesis
  ├── DECISION: FUTURE.md + trigger condition
  │   ├── Captures architectural insight NOW
  │   ├── No implementation, no new module, no 4th repo
  │   └── Trigger: paying-customer names it OR PB-11+PB-12 ship
  └── CISO gates bind when trigger fires
      ├── Gateway threat model doc
      ├── Credential-redaction + env-var + routing-isolation PASS/FAIL
      └── DNSSEC + CAA verified on evals.intentsolutions.io

Q4 — Content Timing
  6/8 for Option B
  ├── DECISION: Option B
  │   ├── Ecosystem post: publish (problem-space framing, no IS claims)
  │   │   ├── GC review before publish
  │   │   └── CFO constraint: zero timeline commitments
  │   └── MCP architecture post: hold
  │       ├── Until Q3 trigger fires (CISO condition)
  │       └── Until PB-1 ships (Research Expert / CLAUDE.md Rule 4)
  └── Research Expert factual correction in effect
      └── NPM count = ~1,140 (not 45k); trust-bank arguments recalibrated
```

---

## 12. Acting head of board declaration

Jeremy Longshore (CEO, Intent Solutions LLC) served as acting head of board for this session, making final calls on all four questions — including the explicit override on Q2.

**I, Jeremy Longshore, find that:**

- All 8 seats convened and returned structured adversarial assessments; adversarial integrity held;
- The Research Expert seat (8th seat, new to this council) performed its function correctly — identifying the NPM download factual error and grounding every Q in actual bead/Plane/GH state;
- Q2 is closed by user override. No @pvncher engagement. We ride solo;
- Q1 Option B correctly distinguishes standards-track filing from implementation spend; the scope fence is explicit and enumerated in this record;
- Q3 FUTURE.md + trigger condition correctly captures the gateway architectural insight without burning sole-prop bandwidth on an untracked scope item; the CISO pre-commit gates bind when the trigger fires;
- Q4 Option B correctly applies `intent-eval-lab/CLAUDE.md` Operational Rule 4 — publish what has been demonstrated; hold what hasn't;
- Implementation directives in §10 carry the decisions into concrete next-session actions;
- The Research Expert seat is promoted to default-available for future ISEDC sessions when factual grounding is a concern.

The decisions in §7 stand until explicitly overridden by a future ISEDC session or by Jeremy Longshore directly.

**Signed,**
**Jeremy Longshore — Acting Head of Board, ISEDC Session 3, 2026-05-11**

---

## 13. References

- ISEDC v1: `004-AT-DECR-isedc-council-record-2026-05-10.md`
- ISEDC v2 (terminology): `005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md`
- Phase B scope: `003-PP-PLAN-phase-b-scope-refinement.md`
- OTel RFC draft (PB-10): `001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`
- Master plan: `~/.claude/plans/please-take-your-time-glimmering-stardust.md`
- Reusable pattern: `~/.claude/skills/exec-decision-council/SKILL.md`
- Meta-bead: `OPS-2et` (home `~/.beads/`)
- Plane HQ: `LAB-6` (Intent Eval Platform umbrella)
- Intent Solutions tagline: *"We create industries that don't exist — we think outside of the box's box."*
