# 109 · AT · DECR — ISEDC: the Governed Judgment Layer (living, self-improving governed judgment) for Bob the Intendant

| Field                  | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Date**               | 2026-07-12                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Status**             | **RATIFIED** — Claude, **acting head of board** (delegated by Jeremy Longshore this session), after a 7-seat ISEDC council (CTO · GC · CMO · CFO · CSO · CISO · VP-DevRel)                                                                                                                                                                                                                                                                                                    |
| **Decides**            | Q1 layer positioning · Q2 public-timing supersession · Q3 scope/sequence · Q4 Circle of Life · Q5 category play · Q6 claim discipline · Q7 bandwidth · Q8 first-mover · Q9 naming — and synthesizes a binding **Public-Flip Gate**                                                                                                                                                                                                                                            |
| **Supersedes in part** | intent-os `030-AT-DECR` **D3** ("default dark; stay dark until Slice-0 green + one-command install") and AGP `001-AT-DECR` ("no public surface until defensible") — the **timing** locks only, superseded by Jeremy's build-in-public / OSS-first decision. `030-AT-DECR` **D1** naming (Intendants → **Bob the Intendant**) — amended, not reversed. All other `030` red lines (partner-consent, claim-discipline, `correlationId`-required, Q5-lock) **carry over intact.** |
| **Governing docs**     | AGP `001-AT-DECR` · AGP `050-AT-DECR` (Q5 lock / ACS gated) · intent-os `030-AT-DECR` · AGP `MARKETING_CLAIMS.md` + `scripts/claim-scan.sh` · GSB `013-OD-STND` (commit/PR standard)                                                                                                                                                                                                                                                                                          |
| **Inputs (cited)**     | `107-RA-ANLY-governed-judgment-prior-art-and-method-stack` · `108-AT-ARCH-governed-judgment-layer`                                                                                                                                                                                                                                                                                                                                                                            |
| **Session artifacts**  | `~/.claude/skills/exec-decision-council/sessions/2026-07-12-governed-judgment-layer/` (`session.jsonl`, verbatim seat returns, this record)                                                                                                                                                                                                                                                                                                                                   |
| **Beads**              | epic `iel-25a` · council `iel-25a.3` · **green-lit build bead `iel-25a.4`**                                                                                                                                                                                                                                                                                                                                                                                                   |

---

## 1. Mission of this record

Adjudicate whether — and under exactly what binding constraints — to build **the Governed Judgment
Layer** ("living, self-improving governed judgment"): an agent that judges whether an external event
is _worth a human_, **grounded** in the Governed Second Brain, **cited** to the brain nuggets it used,
**recorded** on a signed cross-chain audit trail, and whose judgment quality is **measured** by a
composed evaluation stack. Home for the ratified build: the **public `jeremylongshore/bob-the-intendant`**
repo, composing owned kernels — **AGP** (the governance plane), **GSB** (the brain), **IEP/JRig**
(measurement) — with a **Circle-of-Life** live self-improvement loop.

Jeremy pre-decided the strategic forks (public/OSS-first · bold whole Layers 1+2 · Circle of Life =
core pillar · category play = yes · naming = Bob the Intendant). The council's charge was to
**pressure-test and sharpen** the bold direction and **ratify the guardrails — not to re-litigate or
shrink.** It did exactly that: **all 7 seats ratified all 9 decisions, zero vetoes**, and each seat
bound minority constraints. The resolution shape is the ISEDC canonical: _accept the direction, stack
the binding constraints._

## 2. Why a council, not a single review

The failure modes here are asymmetric and largely **one-way doors**: a public git commit is
immutable; a schema frozen at the public tag ossifies; personal data written to public history is
unrecoverable; a first-impression category claim, if wrong, transfers authorship to a competitor.
Single-reviewer reasoning cannot price that asymmetry across legal, security, standards, brand,
bandwidth, and developer-adoption value systems at once. Seven adversarial seats can.

## 3. Synthesis lenses (threaded through every seat)

(a) **the three-axis moat** — ① govern actions ② ground + cite judgment ③ measure + self-improve
judgment; (b) **compose-don't-rebuild** — AGP/GSB/IEP already own the parts; (c) the
**deterministic-vs-probabilistic boundary** — "the model proposes; the deterministic system decides
and records"; (d) **frozen contracts + the cross-chain journal↔receipt pointer** as a
design-in-from-day-one invariant.

## 4. The questions (verbatim)

| #   | Question                                                                                                                             | Why costly / immutable                                                              |
| --- | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Q1  | Are we a HARNESS, or a governance plane ABOVE harnesses (complement to the labs' SDKs, not a competitor; we do NOT build a harness)? | Positioning ossifies the whole build's identity; Anthropic-partner posture at stake |
| Q2  | Ratify build-in-public / OSS-first, superseding `030`/`001` dark-until-green; ratify the guardrails.                                 | Public flip is a one-way door                                                       |
| Q3  | Scope: bold whole (Layers 1+2), Layer-1-first, vs Layer-1-only.                                                                      | Public scope = a public promise                                                     |
| Q4  | Circle of Life: CORE PILLAR vs Layer-2 mechanism.                                                                                    | The moat axis; a poisoning surface if built wrong                                   |
| Q5  | Category play: product + paper + Evidence-Bench scorecard. Set the Q5 (paper-not-spec) line.                                         | A published scorecard is a first-impression-with-community event                    |
| Q6  | Claim discipline: what may the public README claim vs the banned terms; `MARKETING_CLAIMS.md`-first.                                 | Overclaim torches the one allowed claim + credibility                               |
| Q7  | Bandwidth: solo operator — right next bet vs shipping Layer 1 quietly.                                                               | Opportunity cost of the runway                                                      |
| Q8  | IP/first-mover: Glean/Fiddler/Notion (~12–18mo window → EU AI Act Aug 2026).                                                         | The window closes when a 2/3 player ships 3/3                                       |
| Q9  | Naming: Intendants → Bob the Intendant; `bob-the-intendant` (public); Bob v3 flagship / v2 archived; AGP unchanged.                  | First public repo name + mark are permanent                                         |

## 5. Council composition

| Seat                          | Value system                                                               | Agent                                     |
| ----------------------------- | -------------------------------------------------------------------------- | ----------------------------------------- |
| CTO / Chief Architect         | technical durability · frozen-contract discipline · immutability awareness | `iep-isedc-cto` (a1beae49d4b5ab6b8)       |
| GC / General Counsel          | IP · partner-consent · trademark · record-must-equal-artifact              | `iep-isedc-gc` (ad5152d6c05de0371)        |
| CMO / Standard Strategist     | positioning · first-mover authorship · category creation                   | `iep-isedc-cmo` (a63ba681a14474bdb)       |
| CFO / Strategic Operator      | sole-prop bandwidth · opportunity cost · defer-until-justified             | `iep-isedc-cfo` (a69f2896523467927)       |
| CSO / Chief Standards Officer | RFC realpolitik · paper-not-spec · community-temperature                   | `iep-isedc-cso` (a298647b334088ba4)       |
| CISO                          | signing integrity · threat model · claim-must-not-outrun-primitive         | `iep-isedc-ciso` (a8824e9b4892e23a3)      |
| VP-DevRel                     | developer signal · friction-to-adopt · Saturday-afternoon-test             | `iep-isedc-vp-devrel` (a3512060491253896) |

---

## 6. Per-question record (vote · tension · verbatim positions · DECISION)

### Q1 — Plane ABOVE harnesses (not a harness)

**Vote:** 7/7 ratify (CTO/GC/CFO/CISO ratify; CMO/CSO/DevRel ratify-with-constraint).
**Primary tension:** CMO (category leads the headline) vs CTO/GC (architecture-accurate wording; "complement" as a controlled phrase).

Verbatim highlights:

- **CTO:** _"The Slice-0 watcher drift is REAL — `daemon.runMediated()` driving the plane is correct; a hand-rolled turn-loop / tool-dispatch / context-manager inside an intendant is the failure mode. The `intendant-adapter` frozen contract IS the boundary that keeps us a plane."_ Binds: **an intendant delegates agent execution to an external harness SDK — no in-tree turn-loop; gate it with a contract test; if Bob grows its own runtime, that is a bead+ADR event.**
- **CISO:** _"The plane-above framing is the correct threat boundary… we govern the actions, we don't vouch for the model's cognition."_ Binds: never harden "complement" into "secures/hardens your harness."
- **DevRel:** _"'Governs YOUR existing agent' lets them keep everything and add a gate… the single most adoptable framing on the board."_ Binds: README H1 says "governs the Claude Code / Codex agent you already run," never "an agent framework."
- **CMO:** _"The offensive frame is category: we are the judgment layer any harness plugs into… Architecture is not positioning."_ Binds: H1 leads with the category; "complement to the labs' SDKs" is the reassurance line beneath it.
- **GC:** Binds "complement to Google ADK / Claude Agent SDK / OpenAI Agents SDK, not a competitor" as a controlled phrase — factual interop reference, never implied endorsement.

**DECISION — RATIFIED.** AGP is **the governance plane**; intendants (like Bob) run **on** it, **above** any harness; we **compose** the labs' SDKs and **do not build a harness**. **Binding:** (a) no in-tree agent turn-loop in any intendant — delegate to an external harness SDK, enforced by a contract test extending the leaf-layers-must-not-import-daemon invariant; growing an in-tree runtime is a bead+ADR event; (b) public copy uses the controlled phrase "complement to the labs' SDKs, not a competitor," never "replaces/secures your harness"; (c) developer H1 = "governs the agent you already run."

### Q2 — Build-in-public / OSS-first (supersession)

**Vote:** 7/7 ratify (all with constraint; GC ratify-with-constraint on the paperwork).
**Primary tension:** CMO/DevRel (publish to realize the moat) vs GC/CISO/CSO (the flip is the maximum-liability instant; discipline must RISE).

Verbatim highlights:

- **GC:** _"I do not contest the decision; I contest any version of it that lands silently… A build agent — or a future reader — encountering 030 (dark) and this DECR (public) with no supersession chain inherits a self-contradicting record, which is a defective instrument."_ Binds: **explicit "Supersedes in part" header naming `030`-D3 + `001`; `030` gets a recorded amendment note (body preserved verbatim); the holstered Rhys reply does NOT auto-fire and its no-endorser bind survives.**
- **CISO:** _"Going public does NOT waive extraction-gate condition #3 (signing trust root provisioned); it makes it a prerequisite."_ Binds: **NEVER commit real GSB brain / personal data to the public repo — synthetic fixtures only, enforced by a PII/secret pre-commit + CI scanner that lands before the first public commit; THREAT-MODEL.md is honest but scrubbed of unpatched-hole detail; signing trust root + npm scope provisioned before flip.**
- **CSO:** _"Build-in-public inverts my only protection… discipline must RISE, not relax."_ Binds: **no empty storefront** (flip only with a runnable Layer-1 slice + populated `MARKETING_CLAIMS.md` + working `claim-scan`); first public contracts immutable-in-community-memory.
- **DevRel:** Binds: **extraction-gate #4 ("one-command install on a clean machine") is extended — install must bootstrap a bundled synthetic brain so a stranger reproduces the demo without any Jeremy data.**
- **CFO:** Binds: README states **no support SLA**; no community-management workstream funded until adoption pulls it.
- **CMO:** Binds: ship a curated public **build-log / devlog** (the narrative), not just a repo; accepts "build-in-public ≠ overclaim-in-public."
- **CTO:** Binds: the **technical** extraction-gate conditions from `030`-D2 are NOT superseded — condition #2 (frozen cross-chain journal↔receipt contract) must be green **before the first judgment loop runs on a public surface.**

**DECISION — RATIFIED (public/OSS-first; timing lock of `030`-D3 + `001` superseded).** OSS/Apache-2.0
is moat pillar #2; building in public **is** the OSS-first play. **This supersession is explicit and
recorded** (per GC), and is gated by the **Public-Flip Gate (§7)** aggregating every seat's
precondition. The `030`-D3 holstered Rhys reply and its no-partner-as-endorser bind are **untouched**.

### Q3 — Scope: bold whole (Layers 1+2), Layer-1-first

**Vote:** 7/7 ratify (CMO ratify; rest ratify-with-constraint).
**Primary tension:** CFO/GC (Layer-2 is net-new cost + implied-capability exposure) vs CTO (reserve Layer-2 substrate now) vs CMO (narrate the whole).

Verbatim highlights:

- **CFO:** _"Layer 2 is NOT cheap and the doc undersells it: weak-signal maps (Yoon/BERTopic) are net-new build, not compose; Brier/U-calibration is a deferred loop whose first real signal is months of calendar away."_ Binds: **zero Layer-2 code, zero forward-looking scoring, until Layer 1 is green on the watcher AND Bob AND passes "would Jeremy keep Bob running?"; Layer 2 is a scope commitment, not a current bead.**
- **CTO:** Binds: **reserve Layer-2 schema slots NOW, present-but-null at Layer 1** (`resolution_horizon`, `forecast_probability`, `resolved_outcome`) — "a null slot costs minutes; retrofitting costs the chain."
- **GC:** Binds: public docs mark Layer 2 **unshipped/experimental**; no present-tense README verb for an unshipped capability.
- **DevRel:** Binds: the first-run demo + README hero is **Layer-1-only** until Layer 2 produces something a stranger observes in one sitting.
- **CSO:** Binds: Layer 2 ships as a **described method / paper contribution**, never a normative spec, until exercised by a real run.
- **CISO:** Binds: the Layer-2 nugget store inherits the **same signing + retention + citation discipline** as the journal — no unsigned parallel memory.

**DECISION — RATIFIED.** Scope = the **bold whole (Layers 1+2)**; **build strictly Layer-1-first.**
**Binding:** reserve Layer-2 schema slots now (present-but-null); zero Layer-2 build until Layer 1 is
green on the watcher **and** Bob and passes the standing gate; public docs label Layer 2
unshipped/experimental; the Layer-2 nugget store is signed from day one.

### Q4 — Circle of Life = CORE PILLAR

**Vote:** 7/7 ratify as core pillar (all with constraint).
**Primary tension:** CISO (a data-poisoning pipeline without a commit gate) + CFO (recurring labeling tax; κ/α with one operator) vs CTO/CMO (maximal automation / market it).

Verbatim highlights:

- **CISO (sharpest security finding on the board):** _"The loop re-feeds production judgments — made on attacker-controlled external events — back into the golden set. If a production judgment auto-promotes into the trusted golden set without a commit gate, anyone who can emit an event can drift the judge and launder a bad label into the ground truth."_ Binds: **golden-set refresh requires a human/deterministic commit gate; no production judgment enters the trusted golden set without an explicit signed label event carrying provenance (source judgment, correlation_id, labeler, time); the golden set is a signed, hash-chained artifact.**
- **CFO:** _"A live golden-set pipeline with κ/α inter-annotator agreement structurally requires ≥2 annotators, and we have one operator."_ Binds: **the loop is sampled and time-boxed (a fixed weekly Jeremy-minutes budget); resolve the κ/α problem explicitly (a cheap free second judge as annotator-2, or drop κ/α and report single-labeler honestly) before any "validated golden set" claim.**
- **CTO:** Binds: resolutions/refreshes write back **through the same cross-chain pointer**; "self-improving" is **not claimable until the loop provably closes at least once.**
- **CMO:** Binds: the loop is the **moat-axis**; judgment is the **story-axis** — lead with felt judgment, let the loop be _why it compounds_; surface eval as "tell me when judgment slips," not a dashboard.
- **CSO:** Binds: the scorecard/loop-output schema is **frozen-on-first-publish.**
- **GC:** Binds: any public "self-improving/judgment-improves-over-time" **efficacy** claim needs a `MARKETING_CLAIMS.md` row backed by **resolved** Circle-of-Life data, not a design promise.

**DECISION — RATIFIED as a CORE PILLAR.** "Living, self-improving governed judgment" is the moat.
**Binding:** (a) the golden-set promotion path has a **human/deterministic commit gate** — no
auto-promotion from attacker-controllable events (the loop is a data-poisoning surface otherwise);
(b) the loop is **sampled + time-boxed** to a fixed weekly labeling budget, and the single-operator
κ/α problem is resolved before any "validated golden set" claim; (c) "self-improving" is not
public-claimable until the loop **provably closes once** through the cross-chain pointer.

### Q5 — Category play: product + paper + Evidence-Bench scorecard

**Vote:** 6 ratify-with-constraint + 1 partial-dissent (CFO: paper deferred as a byproduct).
**Primary tension:** the defining tension of the session — CMO/DevRel (own the category via the benchmark) vs CSO (a canonical benchmark is normative-by-adoption = a de-facto spec) vs GC (a comparative scorecard naming competitors is a Lanham-Act surface) vs CFO (the paper is real solo-founder spend).

Verbatim highlights:

- **CSO (defining bind):** _"The spec risk is NOT a document labeled 'RFC.' It is the scorecard becoming canonical… A benchmark that invites submissions is normative-by-adoption; it is a de-facto spec even with no document labeled 'RFC.'"_ Binds: **scorecard/paper carry zero normative language (no MUST/SHALL/conformant-to-ours); cite upstream benchmarks by their real names — never re-badge RAGAS-faithfulness as "Bob-faithfulness"; "governed judgment" ships as a described category, never a claimed standard name; "Evidence-Bench scorecard" (a result) is fine, "The Governed-Judgment Benchmark" (an institution) crosses the line.**
- **GC:** _"Publishing comparative capability claims about named, well-funded companies is a Lanham Act §43(a) false-advertising / trade-libel surface."_ Binds: **every comparative claim about a named competitor must be factual, dated, and sourced to that party's own public statement/roadmap — never our characterization — and pass a pre-publish GC review; the citation ledger's integrity note is binding (re-verify any specific result/number before it reaches the paper/scorecard).**
- **CISO:** Binds: scorecard signed with the **provisioned trust root**; **predicate URIs at `evals.intentsolutions.io` only — never `labs.`**; reproducible-by-a-stranger; **pin judge provider/model versions** in provenance.
- **CTO:** Binds: **version-pin and freeze the scorecard's metric definitions (Brier/κ/α/ALCE) as internal-unstable, labeled "not a spec"**; a metric-definition change is a contract change (bead+ADR).
- **CMO:** Binds: **own Evidence-Bench as the category's measuring stick** (the way MT-Bench/HELM own theirs); "governed judgment" = descriptor, not an ownable mark; category authorship = paper + scorecard + build-log, **never a spec**.
- **DevRel:** Binds: the scorecard **ships with the synthetic brain + eval harness so a third party regenerates the numbers.**
- **CFO (partial dissent):** _"The paper is the expensive one… its value can't be claimed until Layer-1 production data exists."_ Binds: **paper is a byproduct written from the scorecard once Layer 1 has real data — not a separate research track/bead.**

**DECISION — RATIFIED (product + paper + Evidence-Bench scorecard), Q5-lock STANDS.** The **paper on
the composed method is allowed** (per `050` orthogonality: composing/describing ≠ authoring a rival
spec). **No AGP/Bob spec, RFC, or "conformance profile" at v0.** **Binding — the CSO line:** the
scorecard is **a published result, never a canonical/submissions-inviting benchmark**; zero normative
language; upstream metrics cited by real name, never re-badged; metric definitions version-frozen as
"not a spec." **Binding — the GC line:** any named-competitor comparison is sourced to the
competitor's own public words + GC pre-review. **Binding — the CISO line:** signed with the
provisioned trust root, `evals.` predicate URIs only, pinned judge versions, stranger-reproducible.
**Sequencing (CFO):** the **paper is deferred** — a byproduct of the scorecard once Layer 1 has real
production data, not a concurrent workstream.

### Q6 — Claim discipline

**Vote:** 7/7 ratify (CFO/GC/DevRel/CSO ratify; CMO/CISO/CTO ratify-with-constraint). **CISO holds the veto.**
**Primary tension:** CMO (maximal honest _capability_ copy) vs CISO/GC/CTO (a claim doesn't exist until its enforcing primitive ships).

Verbatim highlights:

- **CISO (sets the exact wording; veto authority):** allowed v0 wording for `bob-the-intendant` public surfaces —
  - carries over: **"signed audit log of every tool call."**
  - allowed (mechanism-only): **"every judgment is cited to the brain context it used and recorded on a signed, hash-chained journal"**; **"judgment quality is measured against a human-labeled golden set"** (process, never a standing accuracy number).
  - **NEW banned terms** (added to the `claim-scan` regex): _reliable/trustworthy/verified/provably-correct/accurate/accuracy-guaranteed judgment, hallucination-free/-proof, unbiased, self-improving-as-a-guarantee_ — plus all inherited AGP bans. _"A judge that tops out ~55% on hard grounded calls cannot wear an accuracy claim."_
  - **`bob-the-intendant` gets its own `MARKETING_CLAIMS.md` + `claim-scan` gate BEFORE the first public commit.**
- **CTO:** Binds: **no "cited" claim until ALCE citation precision/recall ships and verifies; no "measured/self-improving" until κ/α + the closed loop are published.**
- **CMO:** Binds: register "living, self-improving governed judgment" as a scoped **capability** claim that fires **only when the loop is live (not a static golden file)**; "built for the questions the EU AI Act asks" is honest, "compliance-grade" is banned.
- **GC:** "governed/grounded/cited/measured" = safe _mechanism descriptions_; the EU AI Act tailwind must **not** tempt "compliance-grade."
- **DevRel:** the strongest honest promise is the **demonstrable** one — "Bob only pings you when it's genuinely worth it… written to a signed audit log of every tool call" — plus a demo that visibly kills noise.

**DECISION — RATIFIED (CISO wording adopted verbatim; CISO veto stands).** `bob-the-intendant` gets
its **own `MARKETING_CLAIMS.md` + `claim-scan` gate before the first public commit**, extending the
AGP denylist with the new judgment-layer banned terms above. Mechanism descriptions
(governed/grounded/cited/measured) are allowed; no accuracy/assurance/self-improving-as-guarantee
copy; each claim registers in the same PR that ships its enforcing primitive.

### Q7 — Bandwidth

**Vote:** 7/7 ratify-with-constraint (CTO/CISO ratify; GC defers to CFO).
**Primary tension:** CTO/CMO (more surface in flight) vs CFO/CSO (one workstream at a time).

Verbatim highlights:

- **CFO:** _"The minimum that lands the moat in the window is the Layer-1 grounded-judgment loop on the watcher — already the ratified Slice-0 agent, the lowest-net-new-cost path to a demonstrable loop."_ Binds: **one green-lit build bead only (`iel-25a.4`), then Bob; no parallel Layer-2/paper/forward-looking beads open concurrently; no net-new paid dependency on the provable path; keep the free-provider judge panel free.**
- **CTO:** Binds: reversible knobs (panel providers, rubric weights, JRig thresholds) iterate fast; immutable artifacts (journal schema, cross-chain pointer, frozen contracts, scorecard methodology) get deliberation in the free window; frozen-contract + claim-surface changes always get their own PR+ADR+bead.
- **CISO:** Binds: Layer-1 DoD additionally hard-gates PII-scrub, judge-provider egress boundary, golden-set commit gate, **cross-chain pointer signed-in.**
- **DevRel:** Binds: ship exactly **one stranger-PR-able surface** at launch (a trigger source or a golden-set example) with a template + fixture.

**DECISION — RATIFIED.** **One workstream at a time.** The next bet is the **Layer-1 grounded-judgment
loop on the watcher, then Bob** (`iel-25a.4`) — no concurrent Layer-2/paper beads. Reversible knobs
move fast; immutable artifacts get the free-window deliberation and their own PR+ADR+bead.

### Q8 — IP / first-mover

**Vote:** 7/7 ratify-with-constraint (CMO/DevRel ratify).
**Primary tension:** CMO (author the idea NOW; the clock is real) vs CFO (window = ship-fast, not spend-now) vs CTO (first-mover = a provable-lineage artifact, not a rushed claim).

Verbatim highlights:

- **CTO:** _"The EU AI Act ask — lineage-backed auditability + reasoning-trace provenance — IS the cross-chain journal↔receipt pointer."_ Binds: **first build action = freeze the journal↔receipt contract + `correlation_id` + GSB tip-hash before any judgment run.**
- **CMO:** Binds: **author the category idea now** (thesis + Evidence-Bench-in-progress + dated public build-log = the first-mover evidence); no spec, no assurance overclaim, no partner named as endorser.
- **CFO:** Binds: **first-mover is defended by shipping the Layer-1 loop into public view, not by publishing ahead of the primitive**; no dated public promise about Layer 2.
- **CSO:** _"Claiming a category via paper + working scorecard is the correct realpolitik — that is how CNCF/academic categories crystallize."_ Binds: position as "produces the lineage + provenance the Act asks for," never "AI-Act-compliant."
- **CISO:** _"The judgment surface now is an attack surface too… prompt-injection into an event poisons retrieval → poisons the cited rationale → poisons the journal → poisons the golden set."_ Binds: the event→retrieval→judge injection path + provider-egress path named honestly in THREAT-MODEL.md; treat provider egress as untrusted; no EU-compliance claim.
- **DevRel:** _"OSS IS the moat precisely because Glean/Fiddler/Notion cannot be tried on a Saturday."_ Binds: the synthetic brain is moat-load-bearing.
- **GC:** Binds: **trademark clearance on "Bob the Intendant" before the flip; Apache-2.0 + NOTICE/provenance on every composed asset; an explicit "not a compliance product" disclaimer.**

**DECISION — RATIFIED.** The ~12–18-month window (compressing to EU AI Act, Aug 2026) is real; we
**defend the loop, not the gate.** **Binding:** first build action freezes the journal↔receipt
cross-chain contract; category _authorship_ proceeds via **thesis + working scorecard + dated
build-log only** (no spec, no assurance overclaim); EU AI Act framing is "produces the lineage the
Act asks for," never "compliant/grade"; the judgment/provider-egress attack surface is named in
THREAT-MODEL.md.

### Q9 — Naming: Bob the Intendant

**Vote:** 7/7 ratify/confirm (CFO ratify; rest with constraint).
**Primary tension:** GC (personal-data leak + trademark) + CTO (frozen contract IDs must not rename) vs CMO/DevRel (Bob-as-brand).

Verbatim highlights:

- **GC (the costliest item on the board):** _"GSB is a brain of real people, places, things… Putting GSB nuggets into a public repo's examples writes third-party personal data into an immutable public git history — unrecoverable."_ Binds: **(1) trademark clearance + a designated fallback name recorded before the repo flips public; (2) ZERO real GSB personal data in any public surface — synthetic/fixture brains only, no real partner/client name (any person or organization) as nugget/example/endorser without prior written consent; (3) the `030`-D1 naming amendment is recorded, not silent.**
- **CTO:** _"This is the SECOND reinterpretation of 'intendant'… GC's binding condition was 'never a silent reinterpretation.'"_ Binds: **the product rename touches marketing/repo/wordmark ONLY; the frozen contract identifiers `intendant-adapter`, `intendant-manifest`, and the `src/intendants/` layer stay UNCHANGED (renaming a frozen contract is an ADR event); AGP stays untouched.**
- **CMO:** _"Bob is a mascot/hero, not a category."_ Binds: three separated layers — **Bob** = flagship hero product; **"governed judgment"** = category; **Evidence-Bench** = authorship artifact; **do not expose "v3" publicly** — the public repo ships as v0/v1.
- **CSO:** Binds: clear the public slug (`bob-the-intendant` exact-GH + npm scope + visible trademark) before flip; **do NOT publish `bob-the-intendant@3.0.0` as the first tag** — public release train starts at its first signed release (v0.x).
- **DevRel:** _"A lovable named agent LOWERS friction — devs root for a mascot."_ Binds: every public H1 pairs "Bob the Intendant" with the searchable category phrase ("governed judgment for the agent you already run").
- **CFO:** Binds: **this is the last rename — no third flip;** reuse the reserved private repo/scope; no empty-storefront npm publish until the extraction gate is green.

**DECISION — RATIFIED.** **Intendants → Bob the Intendant**; product/repo = **`jeremylongshore/bob-the-intendant`**
(flipped private→public at the Public-Flip Gate); **Bob v3 = the flagship intendant**; **Bob v2 →
archived + design harvested**; **AGP unchanged.** **Binding:** (a) the rename touches
marketing/repo/wordmark ONLY — the frozen `intendant-adapter`/`intendant-manifest` contracts and
`src/intendants/` are unchanged; (b) `030`-D1 gets a **recorded naming amendment** (not silent); (c)
**zero real GSB personal data on any public surface — synthetic fixtures only**; (d) trademark
clearance + a designated fallback recorded before the flip; (e) public release train starts at
**v0.x**, not "v3"; (f) Bob = hero, "governed judgment" = category, Evidence-Bench = authorship
artifact — never conflated; (g) this is the **last rename**.

---

## 7. THE PUBLIC-FLIP GATE (synthesized — binding)

Six of seven "most costly to recover from" picks converge on **the public flip and what becomes
irreversible at that instant.** The council's aggregate output is a **Public-Flip Gate**: an _event,
never a date_ — **`jeremylongshore/bob-the-intendant` flips private→public only when ALL of the
following are green.** This extends `030`-D2's extraction gate for the build-in-public era.

1. **Frozen cross-chain contract, signed-in** (CTO + CISO) — the journal↔receipt contract +
   `correlation_id` + GSB receipt tip-hash is frozen **and covered by the Ed25519 signature over the
   journal entry** (an embedded-but-unsigned pointer has forgery cost zero). No public judgment is
   journaled before this.
2. **Runnable Layer-1 slice + bundled synthetic brain** (DevRel + CSO) — one-command install on a
   clean machine bootstraps a **synthetic brain** so a stranger reproduces the noise-killing demo
   end-to-end **with zero Jeremy data**. No empty storefront.
3. **PII/secret scrub gate live** (CISO + GC) — a pre-commit + CI scanner blocks real GSB/personal
   data before the first public commit; **zero real partner/client names** as nuggets/examples/endorsers.
4. **Claim-control in-repo** (CISO + CSO + DevRel) — `bob-the-intendant` ships its **own
   `MARKETING_CLAIMS.md` + `claim-scan`** (AGP denylist + the new judgment-layer banned terms) from
   commit #1; public copy carries only the allowed mechanism claims.
5. **Signing trust root + npm scope provisioned** (CISO) — before the flip; signed artifacts bind to
   it; predicate URIs at `evals.intentsolutions.io` only.
6. **Trademark clearance + designated fallback recorded** (GC) — on "Bob the Intendant" before the flip.
7. **Supersession recorded** (GC) — this DECR's "Supersedes in part" header + the `030`-D1/D3
   amendment notes are filed; record equals artifact.
8. **Honest THREAT-MODEL.md** (CISO) — names the event→retrieval→judge injection path + provider-egress
   path; honest posture, scrubbed of unpatched-hole detail.

Until all eight are green, public surface is limited to the **category thesis + dated build-log**
(idea authorship — zero retraction risk per CMO), never a capability launch.

## 8. Council memos (verbatim — "most costly to recover from")

- **CTO:** _"Q2 (public-timing). Publishing is the irreversible act that ossifies whatever schema state exists at that tag — a public judgment journaled without the cross-chain pointer is permanently unprovable and witnessed, and no later fix window reopens."_
- **GC:** _"Q9, the personal-data leak into a public immutable repo. Third-party personal data committed to public git history is not [reversible] — it is permanent, discoverable, and a partner-consent + privacy breach the moment it lands… Synthetic fixtures from day one; no exceptions."_
- **CMO:** _"Q6 (category claim shipped before the live loop)… If 'self-improving governed judgment' hits a public surface backed by a static golden file and one HN thread exposes it as eval-theater-with-a-hash-chain, the authorship transfers to whoever's loop is real."_
- **CFO:** _"Publicly scoping the bold whole… while solo bandwidth can only deliver Layer 1 inside the window. Build-in-public converts an over-scoped promise into a public retraction… Second: the cross-chain causal pointer must be born-correct on the first run — the cheapest dollar we'll ever spend; spend it now."_
- **CSO:** _"Q5 — the Evidence-Bench scorecard is a first-impression-with-community event, immutable the instant it publishes… A benchmark that invites submissions is normative-by-adoption. Guard the framing, not just the filename."_
- **CISO:** _"The cross-chain causal pointer being embedded but not covered by the Ed25519 signature… its forgery cost is zero… every run recorded before the field is signed-in is permanently unprovable. (Private-brain leak is the close second — bounded and scrubbable; this is not.)"_
- **VP-DevRel:** _"Launching the public repo without a shipped synthetic brain / demo corpus… structurally forces every stranger to fail the first run… Unrecoverable for 12–18 months — the whole runway."_

## 9. Cross-cutting themes

- **THE PUBLIC FLIP IS THE ONE-WAY DOOR.** Every seat's costliest fear resolves at the flip. The
  Public-Flip Gate (§7) is the council's single most load-bearing output.
- **Separate the IDEA from the CLAIM (CMO's through-line, adopted).** Author the category _idea_ loud,
  dated, now (zero retraction risk); gate every _capability_ claim on a shipped, **live** primitive.
- **Discipline must RISE with exposure (CSO/GC/CISO).** Losing "dark-until-green" as a shock absorber
  means claim-scan, trademark, comparative statements, partner-consent, personal data, and schema
  freezes each become permanent first-impression artifacts — all recorded before the flip.
- **Compose don't rebuild; freeze the immutable before you publish (CTO).** Reversible knobs move fast;
  immutable artifacts (journal schema, cross-chain pointer, frozen contracts, scorecard methodology)
  get the free-window deliberation now.
- **The moat is the LOOP, not the gate — and the loop is a poisoning surface (CISO).** Its power (live
  self-improvement) is its risk; a human/deterministic commit gate on golden-set promotion is
  non-negotiable.
- **Adversarial integrity check:** no consensus theater — CFO carried a lone partial-dissent on Q5
  (paper deferred); CISO introduced the novel data-poisoning finding on Q4 no other seat raised; DevRel
  introduced the synthetic-brain-as-moat finding; CSO introduced the "canonical benchmark = de-facto
  spec" finding. Seven distinct value systems produced seven distinct costliest-risks.

## 10. Implementation directives

1. **Green-lit build bead `iel-25a.4`** — "Build Layer 1 — governed grounded-judgment eval (the
   ratified wedge) in `bob-the-intendant`" — stays **OPEN**, blocked on this DECR (now ratified). Its
   Definition of Done is `108-AT-ARCH` §12 **plus** the CISO hard-gates (PII-scrub, judge-provider
   egress boundary, golden-set commit gate, cross-chain pointer signed-in) and the Public-Flip Gate (§7).
2. **`030-AT-DECR` naming amendment** — file a recorded "Naming amendment (2026-07-12)" note on
   intent-os `030-AT-DECR` (D1): Intendants → **Bob the Intendant**; repo `intendants` →
   `bob-the-intendant`; the vocabulary fix (Bob = an intendant instance; the frozen `intendant-*`
   contracts unchanged; AGP unchanged). Body preserved verbatim (GC's record-equals-artifact bind).
   _Filed as its own bead/PR; executed as a consequence of this ratified DECR, not in the design phase._
3. **Candidate IEP bead (not a blocker)** — JRig upgrade: retrieval-context input + a groundedness
   criterion type + panel support (`108` §9). File under epic `iel-25a` when Layer 1 build starts.
4. **Reserve Layer-2 schema slots now** (CTO) — `resolution_horizon`, `forecast_probability`,
   `resolved_outcome`, present-but-null, in the Layer-1 journal schema.
5. **Claim registration** — before any "governed judgment" public copy: add a scoped row to
   `bob-the-intendant`'s own `MARKETING_CLAIMS.md` (CISO veto), never ahead of the primitive.
6. **Three-layer mirror** — mirror epic `iel-25a` + build bead `iel-25a.4` to a GitHub issue (and
   Plane, if mapped) via `bd-sync` when the build workstream opens.

## 11. Acting head of board declaration

I, **Claude**, as **acting head of board** (delegated by **Jeremy Longshore** this session), ratify
the council's recommendations: **all 9 decisions RATIFIED in line with Jeremy's pre-decided bold
direction, with every seat's binding minority constraint stacked**, and the synthesized **Public-Flip
Gate (§7)** binding the one-way door. No dissent was dismissed; CFO's Q5 partial-dissent is honored as
the paper-deferral binding constraint. This record supersedes the _timing_ locks of `030`-D3 + `001`
as stated; all other red lines carry over intact.

_Delegated authority for this session per Jeremy's directive: "do the right thing" + the north-star
"research-deep, then fast-build; be bold." Final strategic authority remains Jeremy's; this record is
open to his override on the record._

## 12. References + provenance

- Evidence base: `107-RA-ANLY-governed-judgment-prior-art-and-method-stack-2026-07-12.md`
- Design under ratification: `108-AT-ARCH-governed-judgment-layer-2026-07-12.md`
- Superseded-in-part: intent-os `030-AT-DECR` (D3 timing, D1 naming) · AGP `001-AT-DECR` (public-surface timing)
- Carried-over governing: AGP `050-AT-DECR` (Q5 lock) · AGP `MARKETING_CLAIMS.md` + `scripts/claim-scan.sh`
- Reusable pattern: `~/.claude/skills/exec-decision-council/SKILL.md`
- Verbatim seat returns + `session.jsonl`: `~/.claude/skills/exec-decision-council/sessions/2026-07-12-governed-judgment-layer/`
- Beads: epic `iel-25a` · council `iel-25a.3` · build `iel-25a.4`

---

_Filed under Document Filing Standard v4.4. RATIFIED decision record; verbatim seat positions preserved for future readers._
