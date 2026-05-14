---
title: ISEDC Session 4 — Widened-Scope Architectural Lock
date: 2026-05-13
acting_head_of_board: Jeremy Longshore (Intent Solutions)
council_size: 7 seats (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel)
decisions_logged: 6 questions, 7 reopened-binding determinations, per-artifact fold-in plan
status: LOCKED — foundation for the next 6 months of Intent Eval Platform work
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
synthesis_input: tracking bead iel-5eo (intent-eval-lab); user widening directive verbatim 2026-05-13
reusable_pattern: ~/.claude/skills/exec-decision-council/SKILL.md v1.0.0
prior_decisions: 004-AT-DECR (DR-004), 005-AT-DECR (DR-005), 006-AT-DECR (DR-006)
filing_standard: Document Filing Standard v4.3
---

# ISEDC Session 4 — Widened-Scope Architectural Lock for the Intent Eval Platform

## 1. Mission of this Decision Record

This Decision Record locks the architectural foundation for the widened-scope Intent Eval Platform — Jeremy Longshore's directive (2026-05-13, as acting head of board) was to absorb the **modern AI Systems Engineer (AISE) 5-domain stack** into the platform without abandoning any in-flight work. The council's mandate was full architectural lock + a per-artifact fold-in plan that maps every in-flight artifact onto the locked architecture. All prior ISEDC bindings (Session 1 Q1–Q5, Session 3 Q2–Q3, 2026-05-13 ad-hoc TS lock) were declared reopenable at session open.

The output is a single Decision Record that will govern the platform's next 6 months. Every downstream bead, Plane issue, workstream, and PR derives from the decisions recorded here.

## 2. Why a council, not a single review

The widening crosses multiple value-system axes simultaneously: brand identity (CMO), trademark exposure (GC), bandwidth math (CFO), standards-body diplomacy (CSO), supply-chain attestation surface (CISO), schema-versioning blast radius (CTO), and developer adoption friction (VP DevRel). Single-reviewer reasoning fails this kind of asymmetric-cost cluster. The ISEDC adversarial pattern (each seat from a distinct value system; dissent preserved, not suppressed; minority binding constraints stack on majority recommendations) is the response.

## 3. The user's verbatim widening directive (binding framing for this session)

> *"Everything that is in the works right now needs to be intervened with the large plan we made. The large plan needs to incorporate filling the gaps of the work that we already started. The work that we started in this plan needs to fold into the new plan. If it needs to be rearranged and restructured, that is fine. We do not just stop what we are working on. We figure out a way to incorporate it into the new plan and adapt and overcome after you convene with the board. But we want the whole foundation for the whole thing figured out."*

> *"i want the executive council to discuss this with the board... mcp, universal skills md etc the same path we were in before harnesses etc etc anything agentic related things like this get with the council."*

> *"all these systems should work together basically i am widening the scope to become not only agentic mcp specific but agentic testing in general with focus on mcp agentic etc etc."*

The directive: fold-in, not stop. Adapt + restructure where needed. Foundation locked in one session.

## 4. Synthesis lenses (applied to every seat's analysis)

1. **The arena (5 surfaces):** APIs · CLIs · MCP servers · agents · SKILL.md
2. **Both sides:** client-side eval + server-side eval
3. **The transformation pipeline:** API → CLI → MCP → SKILL.md → agent
4. **Composable partial attestation:** every component is a valid entry; silence ≠ failure
5. **The AISE 5-domain stack:** Inference · Reliability · Eval Science · Agent Systems · LLMOps
6. **Sole-prop bandwidth reality:** ~3-5 hrs/wk sustainable, baseline split across Kobiton M2 (first priority), Nixtla, claude-code-plugins, trucking, VPS-as-the-home, Anthropic Enterprise cohort

## 5. The six questions verbatim

| # | Question | Why immutable / costly |
|---|---|---|
| Q1 | Architectural fork: ONE BIG platform / FAMILY of platforms / REFRAME as platform-of-platforms | Category permanence; URI namespace identity; brand surface multiplication |
| Q2 | Language reconciliation: TS-primary lock vs Python-heavy widening; hybrid; per-artifact fold | Supply-chain audit surface; ecosystem alignment; in-flight rewrite cost |
| Q3 | Drift-prevention architecture: unification thesis binding; widen predicate URI namespace; new Plane module | URI permanence in Rekor (one-way door); schema-versioning blast radius |
| Q4 | Uncle Bob borrowable patterns #1–#6: which to borrow, with what bindings | Spec-vocabulary lock-in; attribution discipline; tamper-evidence in derived patterns |
| Q5 | Roadmap sequencing: M5 first vs pause-to-converge; per-artifact fold; founder-hour budget; Kobiton M2 first priority | Bandwidth math; OTel maintainer warm-context; M5.1 dev-trust decay; SPEC.md drift |
| Q6 | Governance loop: decision routing classes; cadence; convening standing | Future-decision routing; @pvncher engagement S3Q2 reopen request |

## 6. Council composition

| Seat | Value system | Bias | Primary adversaries |
|---|---|---|---|
| **CTO / Chief Architect** | Technical durability · schema integrity · immutability awareness · future-proofing | Deliberation > commit · empirical evidence > authorship claims | CMO (filing tempo), CSO (RFC tempo) |
| **GC / General Counsel** | IP protection · partner-consent · trademark · audit-trail discipline | Written consent before any partner reference · paper trail sacrosanct | CMO (case studies), CSO (RFCs citing partner work) |
| **CMO / Industry-Standard Strategist** | Positioning · narrative coherence · tagline alignment · first-mover authorship | Visible > silent · ambitious > conservative · frontier > operational | GC, CFO, CSO, CTO (on schema-vs-brand primacy) |
| **CFO / Strategic Operator** | Sole-prop bandwidth · customer-signal gating · opportunity cost | Defer until customer evidence justifies · standards-body filings not costless | CMO, CSO (premature standards work) |
| **CSO / Chief Standards Officer** | OTel SIG-GenAI / in-toto / SLSA / CNCF / OpenSSF realpolitik · RFC sequencing | Community-temperature ALWAYS precedes RFC filing · first-impression permanent | CMO (RFC-as-marketing) |
| **CISO / Chief Information Security Officer** | Supply-chain attestation integrity · signing infrastructure · threat model · Rekor discipline | Reserve schema slots for signing fields NOW · scoped subdomain > broad subdomain | CMO (threat-model underweighting), CTO (slot tempo) |
| **VP DevRel / Head of OSS Community** | Developer-audience signal · OSS contribution dynamics · friction-to-adopt | "Saturday-afternoon-developer-tries-the-thing" test · informal > formal | GC (consent gates), CMO (enterprise framing) |

## 7. Per-question record

### Q1 — ARCHITECTURAL FORK

**Vote tally:**

| Seat | Vote |
|---|---|
| CTO | C — platform-of-platforms (schema-bearing constellation) |
| GC | B — family of products under coordinating thesis, no new umbrella brand |
| CMO | C — reframe as "Intent AI Reliability Stack" |
| CFO | C-as-deferral — defer the fork, ship single converged spine first (de-facto A in execution) |
| CSO | A — ONE BIG (single SIG-GenAI / in-toto / SLSA identity) |
| CISO | A — single platform, plug-in domains as subpath-scoped predicate types, NOT subdomains |
| VP DevRel | A — ONE BIG, branded as a developer product |

**Tally (de-facto):** A=4 (CSO, CISO, VPDevRel, CFO-execution), B=1 (GC), C=2 (CTO, CMO).

**Primary tension:** CTO + CMO push C for schema/category-authorship reasons; CSO + CISO + VPDevRel push A for standards-body identity + supply-chain attack-surface + developer adoption-friction reasons. GC dissents toward B on trademark clearance grounds.

**Verbatim seat positions (key excerpts; full positions preserved in appendix to the underlying bead `iel-5eo` for posterity):**

- **CTO:** *"'ONE BIG platform' is a technical lie that will collapse under its own weight within 18 months — five domains, five release cadences, five toolchains, five threat models cannot share a single binary or repo without becoming the worst kind of monolith. Option C — `intent-eval-platform` as the schema-bearing constellation, with sub-platforms (Reliability, Evaluation, Inference, Agent, LLMOps) federating via Evidence Bundle predicates — preserves architectural honesty AND the unifying invariant."*
- **GC:** *"Option C requires USPTO TESS clearance search + common-law search + domain availability check across `.io/.com/.dev/.ai` — minimum 2–4 weeks of GC time I do not have budgeted. Option B preserves four already-public marks; no new clearance spend... Option A creates trademark single-point-of-failure."*
- **CMO:** *"C — REFRAME as 'Intent AI Reliability Stack' (working name; test 'Reliability Fabric' and 'Reliability Plane' in parallel before lock). Five constituent platforms aligned to the 5-domain AISE map. Single tagline at umbrella. Schema (Evidence Bundle + predicate URIs) is the umbrella's technical spine — CTO gets schema primacy at the architecture layer; CMO gets category primacy at the narrative layer."*
- **CFO:** *"Option C (defer the fork, ship one converged spine first) is the only choice that survives bandwidth math. A/B both presume the founder has 3x the hours he actually has."*
- **CSO:** *"A — ONE BIG. OTel SIG-GenAI maintainers do not have bandwidth to track three peer 'Intent' platforms — they will conflate them anyway, badly, and the conflation will be on terms we don't control. One platform, one identity, one URI namespace authority, one voice in committee."*
- **CISO:** *"A — single platform `evals.intentsolutions.io`, plug-in domains as subpath-scoped predicate types, NOT subdomains. Each additional platform root multiplies the attestation attack surface linearly: more DNSSEC zones to monitor, more CAA records to audit, more signing key custodies, more Rekor anchoring pipelines."*
- **VP DevRel:** *"A — ONE BIG, branded as a developer product, not an enterprise platform. Three platform-brands at 3-5 hrs/wk is a guarantee of three half-maintained docs sites, which is the loudest negative developer signal in OSS."*

**DECISION — Q1: A (ONE BIG) with stacked minority binding constraints.**

The platform is **Intent Eval Platform** — single umbrella, single identity in standards-body and developer-funnel surfaces, single Plane module HQ at LAB-6 (IEL-CONV-1). The AISE 5-domain stack (Inference / Reliability / Eval Science / Agent Systems / LLMOps) is the **internal scope map**, not a separate-brand surface. The user's product positioning *"Reliability infrastructure for agentic systems. Not chatbots. Not wrappers. Infrastructure."* lives at the umbrella.

**Stacked minority binding constraints (from dissenters):**
1. **(CTO binding)** Hard internal package boundaries enforced by lint rules from day one. Per-domain CODEOWNERS. Explicit schema-stability SLA separate from code SLA. Documented exit-ramp to split back to family/constellation within 12 months if release-cadence pain emerges.
2. **(CMO binding)** Reserve umbrella name as domain + npm scope + GitHub org alias defensively even though A wins — first-mover authorship of the *phrase* "AI Reliability infrastructure" is non-negotiable. CMO's dissent on Option C preserved verbatim in this DR per adversarial-integrity protocol.
3. **(GC binding)** No new trademark filings until USPTO TESS clearance search completed. "Intent Eval Platform" as existing mark is grandfathered; any future rebrand triggers full clearance Decision Record first. Vendor-generic case-study scrub binding (S1Q2 2026-05-10) stays in force across the widened scope.

**Rationale:** A wins because the supply-chain attack surface (CISO), standards-body identity (CSO), and developer adoption friction (VP DevRel) costs of multi-brand are all permanent in their own ways, while the brand-narrative cost CMO and CTO flag is recoverable via internal scope-map naming + reserved-name defensive registrations. The 3-5 hr/wk bandwidth reality (CFO) makes A the only choice that can be maintained at developer-quality level.

---

### Q2 — LANGUAGE RECONCILIATION

**Vote tally:**

| Seat | Vote |
|---|---|
| CTO | Per-artifact / surface-dictates — TS for current TS, Python for new ML builds |
| GC | Per-artifact + TS lock for rollout-gate preserved + license audit required for any new Python |
| CMO | Per-artifact polyglot-by-domain explicitly framed externally |
| CFO | Hard TS lock — no Python widening; polyglot only in audit-harness (already polyglot) |
| CSO | TS-primary at signing/attestation-producer layer; Python permitted at consumer/eval layer |
| CISO | TS-first lock holds; Python only subprocess-isolated, non-signing-adjacent, credential-redacted |
| VP DevRel | TS-first at dev-facing surface; Python behind clean subprocess boundaries |

**Tally:** Pragmatic per-artifact / hybrid = 4 (CTO, GC, CMO, CSO with signing-layer caveat); hard TS lock = 3 (CFO, CISO, VPDevRel with strong subprocess-boundary). All seats converge on **"signing/dev-facing/CI = TS; ML internals may be Python behind a boundary."**

**DECISION — Q2: PER-ARTIFACT HYBRID, signing-layer + dev-facing surface stays TS.**

- **intent-rollout-gate, j-rig, intent-eval-lab tooling:** TS. The 2026-05-13 ad-hoc TS lock for `intent-rollout-gate` is **upheld** and **generalized** to "TS at every signing-adjacent and dev-facing surface."
- **audit-harness:** stays polyglot (Node CLI + shell + Python) — the polyglot precedent lives here.
- **7 validate-* skills:** stay Python in claude-code-plugins (no rewrite). When emit-evidence retrofit lands (Phase B per Q3), the emit-evidence path must use **sigstore-python** with signed wheels.
- **New ML internals (if/when LLM Harness Lab or Agent Runtime Sandbox land — see Q5 deferral):** Python permitted **only** behind subprocess boundaries. Credentials never cross the boundary. Evidence Bundle rows constructed by Python are re-validated against the canonical TS schema (`@j-rig/core` Zod) before signing.

**Stacked binding constraints:**
1. **(CISO non-negotiable)** Any Python code path that constructs or signs an Evidence Bundle row requires sigstore-python + signed wheels for 100% of its dependency tree. No `pip install` of unsigned packages. Dedicated CVE-monitoring SLA: 48hr critical, 7d high. Python code is **forbidden** from handling provider credentials directly — must receive scoped, short-lived tokens from a TS-side broker.
2. **(GC non-negotiable)** Every new Python dependency declared in a `LICENSES.md` file in the repo root with the license name and a link to upstream license file. Copyleft scan (`pip-licenses` or `licensecheck`) in CI on every PR. GPL/AGPL dependencies blocked at CI level absent explicit GC waiver.
3. **(CFO bandwidth gate)** Any new Python package introduced anywhere in the platform = minimum 15 founder-hrs/release maintenance cost. That number is the gate.
4. **(VPDevRel dev-surface protection)** Headline quickstart on the docs site uses `npx` or `pnpm dlx` — the 45,000+ NPM `claude-code-plugins` audience's muscle memory. `pip install` is **never** the headline command for the umbrella platform.
5. **(CTO schema-codegen discipline)** JSON Schema is canonical; codegen to Pydantic (Python) and Zod (TS) enforced by CI gate. No drift between language bindings tolerated.

---

### Q3 — DRIFT-PREVENTION SYSTEM ARCHITECTURE

**Vote tally on unification thesis ("every validator emits Evidence Bundle as binding principle"):** **7/7 — UNANIMOUS BINDING.**

**Vote tally on URI namespace widening tempo:**

| Seat | Vote |
|---|---|
| CTO | Widen via sub-paths `evals.intentsolutions.io/<platform>/<predicate-type>/v<version>` — lock grammar before first signed attestation |
| GC | Widen under `evals.intentsolutions.io/<predicate-type>/v<version>` with GC sign-off per type filed as Decision Record |
| CMO | DO NOT widen — preserve CISO 2026-05-10 binding; unification at internal naming layer only |
| CFO | DO NOT widen beyond `gate-result/v1`; one Plane module only |
| CSO | Widen conceptually, reserve URI slots **incrementally** — only as working signed attestations back them |
| CISO | Per-predicate assessment — APPROVE 4 / DEFER 2 / REJECT 1 (see breakdown) |
| VP DevRel | Defer URI widening until first paying customer; unify external dev surface (one docs, one CLI) first |

**CISO per-predicate assessment (load-bearing on this question):**

| Predicate URI candidate | CISO call |
|---|---|
| `gate-result/v1` | **APPROVED** (already bound S1Q1) |
| `validation-result/v1` | **APPROVE conditional on SPEC.md normative section first**; risk of confusion with `gate-result` if both exist — SPEC.md must draw the line |
| `eval-verdict/v1` | **APPROVE conditional on SPEC.md normative section first**; verdict (judgment) ≠ gate (mechanical pass/fail) |
| `harness-experiment/v1` | **DEFER to Phase B+**; experimental output is the LAST thing to anchor in Rekor permanently |
| `agent-loop-trace/v1` | **REJECT for v1** — loop traces contain prompts, tool calls, credential-shaped strings, agent reasoning; permanent Rekor record of potentially sensitive trace data is unacceptable without a separate sanitization spec |
| `cost-attribution/v1` | **APPROVE with reservations**; tamper-evidence over confidentiality; signing is appropriate |
| `cache-decision/v1` | **DEFER to Phase B+**; cache decisions leak prompt-shape and access-pattern data — sanitization spec required first |

**DECISION — Q3:**

1. **Unification thesis = BINDING.** Every validator (the 11-validator inventory + audit-harness + j-rig) emits Evidence Bundle rows as architectural primitive. Authored as `intent-eval-lab/specs/UNIFICATION.md` referenced from every constituent repo's CLAUDE.md within 30 days.

2. **URI namespace widening = INCREMENTAL** with CISO per-predicate gates:
   - **v0.1 (Phase A through M1):** `gate-result/v1` only (already bound).
   - **v0.2 (after SPEC.md normative content lands):** add `validation-result/v1` + `eval-verdict/v1` + `cost-attribution/v1`.
   - **v0.3+ (Phase B):** add `harness-experiment/v1` and `cache-decision/v1` after sanitization specs land.
   - **REJECTED for v1:** `agent-loop-trace/v1` — gated on trace-sanitization spec authored in `intent-eval-lab/specs/sanitization/v0.1.0-draft/SPEC.md`. CISO veto preserved.
   - **URI grammar locked in writing BEFORE first signed attestation against any new predicate**, per CTO non-negotiable and CISO immutability discipline.

3. **New Plane module = YES** — "Tooling Drift Prevention" sub-module under LAB project, child of LAB-6 HQ (IEL-CONV-1). Single Plane module, NOT one per platform — CFO + VPDevRel bandwidth concern preserved.

4. **CRITICAL drift risk (SPEC.md skeleton-only):** beads `iel-ni9` (SPEC.md normative) and `iel-f28` (JSON Schema) re-prioritized to **P0** and bumped to the front of M1 work. SPEC.md normative content + JSON Schema for `gate-result/v1` must land before any new predicate URI gets approved or any production-Rekor signing happens.

5. **HIGH drift risks (3):** Anthropic snapshot auto-update CI gate (new bead, Phase B), j-rig Tier 3 ↔ validate-skillmd Tier 1-2 spec bridge (new bead, Phase B), audit-harness SemVer regression test suite (new bead, M2 scope).

6. **MEDIUM drift risks (3):** 7-layer taxonomy extracted to `intent-eval-lab/specs/taxonomy/v0.1.0-draft/SPEC.md` (Phase B); SCHEMA_CHANGELOG pre-commit hook (Phase B); validate-consistency rules extracted to standalone Drift Detection Specification (Phase B).

7. **`labs.intentsolutions.io` is preserved-reserved-don't-touch** per ISEDC v1 CISO binding — the widening does NOT touch it.

**Stacked binding constraints:**
1. **(CISO non-negotiable)** No predicate URI gets signed against production Rekor until SPEC.md normative section for that predicate lands. Until then, signing happens in **sigstore staging** (`rekor.sigstage.dev`) — experimental, not production.
2. **(CTO non-negotiable)** URI grammar `evals.intentsolutions.io/<predicate-type>/v<version>` locked in writing in SPEC.md before first production-Rekor attestation against any predicate.
3. **(GC discipline)** Predicate-type registry at `intent-eval-lab/specs/PREDICATE-TYPES.md` listing every URI subtype, first-signed-attestation date, and Decision Record link — updated within 7 days of any new subtype going live. Drift here is unrecoverable.
4. **(CSO discipline)** Reservations land in internal architecture docs ONLY until working attestations back them. No SIG-GenAI maintainer ever sees a "we've reserved seven URIs" — they see "we're emitting attestations against these N URIs today."
5. **(VPDevRel friction protection)** External dev surface (docs site, CLI namespace, quickstart) unifies BEFORE internal Plane/URI work consumes founder-hours.

---

### Q4 — UNCLE BOB BORROWABLE PATTERNS

**Vote tally per pattern:**

| Pattern | Yes | Conditional/Defer | Binding constraints from minority |
|---|---|---|---|
| **#1 Two-mode pipeline IR** (acceptance + mutation from shared IR) | 6 | 1 (VPDevRel: only if dev-facing) | CISO: IR must have stable canonical-form serialization (JCS or equivalent) for reproducible signatures |
| **#2 Type-detection mutation rule table** (deterministic per-cell, seeded RNG) | 6 | 1 (CFO: bandwidth concern, sequence late) | CISO: seeds for adversarial/security-relevant mutation MUST come from CSPRNG and be treated as low-sensitivity-but-not-public; document seed-handling policy |
| **#3 0/1/2/3 exit-code grammar** (errored/result-failing/held-wrong/survivors) | **7 (UNANIMOUS)** | — | CTO: documented in SPEC.md and CI-enforced |
| **#4 Killed/Survived/Error trichotomy** with structured JSON | **7 (UNANIMOUS)** | — | CISO: schema-validate AND length-cap every string field server-side (log-injection / oversized-payload defense). Forbid raw stderr/stdout passthrough |
| **#5 Coverage-as-prefilter** for expensive gates | 6 | 1 (CFO: defer; premature optimization) | CISO: in CI contexts where prefilter affects a signed attestation, coverage data must be from a tamper-evident source (coverage instrumentation hashed and included in attestation predicate). VPDevRel: highest dev-signal — prioritize |
| **#6 Spec-as-portable-doc** separated from reference impl | **7 (UNANIMOUS)** | — | GC: spec license = CC-BY-4.0 or Apache 2.0; impl license preserves per-repo current license. CISO: institutionalizes spec/impl auditor separation needed for SOC2 |

**DECISION — Q4: ALL 6 BORROWS APPROVED with stacked CISO security bindings + GC attribution discipline.**

**Sequencing (CTO + CFO + VPDevRel synthesis):**
1. **#6 (spec-as-portable-doc) FIRST** — unblocks SPEC.md normative authoring per CTO + Q3 CRITICAL drift fix. ~2 founder-hrs (CFO estimate).
2. **#3 + #4 (exit-code grammar + trichotomy)** — second wave. ~3 founder-hrs total. Unblocks rollout-gate v0.2 production-signing contract.
3. **#1 (two-mode pipeline IR)** — third wave. ~2 founder-hrs. Aligns with Evidence Bundle reproducibility.
4. **#2 (mutation rule table)** — fourth wave. ~3 founder-hrs. Phase B scope.
5. **#5 (coverage-as-prefilter)** — fifth wave but VPDevRel-prioritized for dev signal. ~4 founder-hrs. Phase B scope.

**Total founder-hour cost:** ~14 founder-hrs across 6 borrows (CFO estimate). Aligns with bandwidth budget.

**Non-borrows (preserved per user direction, not relitigated):** FitNesse wiki-tables, swarm-forge tmux orchestration, CRAP formula (already adopted in audit-harness).

**Stacked binding constraints:**
1. **(GC attribution non-negotiable)** Attribution footer in SPEC.md: "Patterns informed by Robert C. Martin's *Clean Code* and the mutation testing literature; specific compositions are Intent Solutions originals." Any borrow that touches a predicate URI or DSSE envelope contents carries inline attribution in the published spec page.
2. **(CISO security bindings)** All bindings listed above are non-negotiable. If overruled, documented as known-deferred threat-model gaps in SPEC.md security considerations section.
3. **(CTO portability discipline)** Spec-as-portable-doc (#6) means SPEC.md is authored as portable spec (no implementation references); reference impl in separate doc; CI gate enforces no impl-leakage into spec.

---

### Q5 — ROADMAP SEQUENCING

**Vote tally:**

| Seat | Position |
|---|---|
| CTO | Pause M5 for ~2 weeks foundation lock (SPEC.md + URI grammar + Plane module + schema codegen), THEN resume M5 |
| GC | M5 substantive completion BEFORE widening artifact ships; per-artifact fold; no new platform-builds public until license audit |
| CMO | Re-sequence (not pause): SPEC.md + M5.1 interface lock parallel weeks 1–2; M5.1 impl weeks 3–4; new platform-builds scaffolded as stub-repos only |
| CFO | Pause-and-converge; **+50hr widening cap, +66hr hard ceiling**; no new platform-build implementation in 6 months without 2nd paying customer |
| CSO | DO NOT pause M5; ship M5 with widened-scope framing in first signed attestation's predicate metadata; OTel informal-email Week 1 proceeds regardless |
| CISO | Pause-and-converge; SPEC.md normative content BEFORE M5 production; M5 may scaffold (CI/manifest/smoke) but **no production-key signing** until SPEC.md lands |
| VP DevRel | M5.1 ships FIRST; parallel track; SPEC.md normative in 2 weeks unblocks M5.1; mark v0.1 EXPERIMENTAL to preserve API-break right |

**Tally:** Pause-and-converge = 3 (CTO, CFO, CISO). Parallel track = 3 (CMO, CSO, VPDevRel). GC bridges (M5 substantive ships, but new platform-builds gated).

**Primary tension:** CISO + CTO + CFO want SPEC.md normative content locked BEFORE any M5 production signing happens, because signing against an under-specified predicate is permanent in Rekor. CSO + VPDevRel + CMO want M5.1 shipping NOT delayed because OTel maintainer warm-context decays, developer warm-market decays, and category-authorship clock runs out.

**SYNTHESIS — both sides correct on different axes. The decision threads the needle:**

**DECISION — Q5: PARALLEL TRACK with EXPERIMENTAL-MODE GATE.**

- **Weeks 1–2 (12–18 founder-hrs total across both tracks):**
  - **Track A — Foundation (CTO/CISO/CFO win):** SPEC.md normative content for `gate-result/v1` authored (Uncle Bob #6 pattern first). JSON Schema lands. URI grammar locked in writing. Plane "Tooling Drift Prevention" sub-module created. Uncle Bob #6 + #3 + #4 patterns spec'd.
  - **Track B — M5.1 implementation (CSO/VPDevRel/CMO win):** TS pnpm skeleton + policy parser + bundle loader + decision engine + PR-comment renderer + dist build + CI per the existing M5.1 plan. Marked `v0.1.0-experimental` in README.
  - **Track C — OTel informal email Week 1 (CSO non-negotiable):** sent regardless of pause/no-pause majority. Includes "architectural-widening in flight, follow-up in 2 weeks with revised vocabulary" honest in-flight signal.

- **Weeks 3–4:** M5.1 ships v0.1.0-experimental publicly. **Signing happens in sigstore staging only** (`rekor.sigstage.dev`) — **NOT production Rekor.** CISO non-negotiable: zero production-key signing until SPEC.md normative section for `gate-result/v1` is locked.

- **Weeks 5–8:** SPEC.md normative lands → v0.2.0 cuts. Production-Rekor signing enabled. `validation-result/v1` + `eval-verdict/v1` + `cost-attribution/v1` predicates added per Q3.

- **Weeks 9–16:** M5 internal dogfood (claude-code-plugins, audit-harness, j-rig themselves run the chain). Bug fixes. v0.3.0 published.

- **Weeks 17–26 (months 5–6):** Public rollout per master plan M6. Quickstart, example repo, blog content, OTel RFC filing (Week 4+ informed by routing feedback per S1Q4 sequence).

**Kobiton M2 first priority preserved — runs on its own track, not displaced.**

**Founder-hour budget (CFO-grade, locked):**

| Item | Hours | Notes |
|---|---|---|
| M1–M6 baseline (from master plan) | 73–118 | Existing plan |
| Drift-debt paydown (Q3 fixes) | 16 | SPEC.md, snapshots, SEMVER, taxonomy |
| Uncle Bob borrows #1–#4 + #6 | 10 | Per Q4; #5 may move to Phase B |
| Convergence-fold (in-flight → new plan) | 12–18 | M1 partial, M4 stub, M5.1 branch fold-in |
| Widening spec surface (5-domain framing in SPEC.md) | 6–10 | Documentation only, not implementation |
| ISEDC governance overhead (Q6) | 8–12 | Quarterly council + ad-hoc Decision Records |
| **Subtotal widening cost** | **+52–66 hrs** | Over 6 months |
| **NEW TOTAL** | **125–184 hrs** | 6-month budget |
| **Available at 3–5 hrs/wk × 26 wks** | **78–130 hrs** | |

**Gap: 54+ hours of work that doesn't exist at the high end.** This is the CFO bandwidth-math reality. Resolution:

- **+50 founder-hour widening cap is BINDING.** +66 is the absolute ceiling. Any work pushing above triggers automatic ISEDC re-convene.
- **No new platform-build implementation in next 6 months.** LLM Harness Lab + Agent Runtime Sandbox stay as **design-doc-only** state in `intent-eval-lab/specs/FUTURE-platforms/`. README, scope, unlock triggers — no code. Gated on second paying-customer signal (Kobiton M2 is signal #1; signal #2 unlocks first platform-build).
- **Eval Control Plane positioning** (user-named: "GitHub Actions for AI reliability") becomes the umbrella positioning at M6 rollout — it's NOT a separate build, it IS the platform.

**Stacked binding constraints:**
1. **(CISO non-negotiable)** M5.1 v0.1 ships in `experimental` mode on sigstore staging. Zero production-key signing until SPEC.md normative lands. Any attestations produced in this window are explicitly enumerated and re-signed against the final spec before production cutover. Documented spec-vs-implementation diff published with every M5 release in this window.
2. **(CFO non-negotiable)** +50 hr widening cap; +66 hr hard ceiling. Kobiton M2 priority off-the-top, never from this budget.
3. **(CSO non-negotiable)** OTel informal-email Week 1 ships in some form (honest in-flight signal if needed) — silence with a warm maintainer is worse than honest in-flight signal.
4. **(GC non-negotiable)** No new public repo for LLM Harness Lab or Agent Runtime Sandbox before (a) license audit complete, (b) name cleared by GC, (c) Decision Record filed. Until those gates: design-doc only.
5. **(VPDevRel discipline)** M5.1 README is honest about what's experimental. Action.yml stub gets replaced with v0.1.0-experimental real-mode (not silent exit-0). Saturday-afternoon dev test must pass: clone → quickstart → working experimental Rollout Gate within 10 minutes.

---

### Q6 — GOVERNANCE LOOP

**Vote tally:** Strong convergence on three-class routing structure with minor cadence and standing variations.

**DECISION — Q6: THREE-CLASS ROUTING + QUARTERLY STANDING + AD-HOC + PUBLIC DECISION RECORDS.**

**Class 1 — Full ISEDC (7 seats):** decisions producing immutable artifacts. Auto-trigger list:
- New predicate URI subtype reservation
- DNS zone change at any predicate-URI subdomain
- New Fulcio identity issuance / signing key custody change
- DSSE attestation envelope schema change
- New brand commitment with public surface (repo rename, npm scope rename, new domain registration)
- New partner-engagement public reference (vendor-generic case-study scrub binding S1Q2 stays binding)
- Standards-body submission (OTel SIG-GenAI / in-toto / SLSA / CNCF / OpenSSF)
- New sub-platform initiation (Q1 reaffirmation: NO new platform initiation in next 6 months per Q5)
- Language-lock changes (Q2 reaffirmation)

**Class 2 — CTO + VP DevRel pair (2 seats, short Decision Record `NNN-AT-DECR-pair-<title>-<date>.md`):**
- Per-component release timing
- CI workflow changes
- Validator additions / version bumps (when no new emitted-attestation surface introduced)
- Saturday-afternoon-dev test reviews and friction-reduction passes
- Tooling internal-architecture below the predicate-URI line

**Class 3 — Solo (acting head of board / maintainer):**
- Code-level decisions inside an existing sub-component's scope
- Bug fixes
- Documentation polish
- Logged append-only in `intent-eval-lab/000-docs/SOLO-DECISIONS.md` (one-line entry per decision with date + rationale)

**Cadence:**
- **Standing quarterly ISEDC** — default-preserve review of prior bindings; reopening any binding requires justification.
- **Ad-hoc Class 1 convening** — triggered by the auto-trigger list above.
- **Annual full review** of all active bindings — GC binding (minimum cadence below quarterly is unacceptable).

**Convening standing:**
- **Acting head of board (Jeremy)** has unilateral standing to convene.
- **Any 2 seats acting jointly** may call ad-hoc Class 1 convening (CFO-CISO ally pattern, CSO-CMO tempo dispute pattern, etc.).
- **VP DevRel** has unilateral standing to call community-temperature Class 1 convenings (DevRel seat compromise).

**S3Q2 (no @pvncher) — REOPENED narrowly:**

- **REOPEN** for informal community-temperature check ONLY (CSO Week 1 informal-email pattern). NO RFC, NO formal ask, NO public engagement beyond an honest email asking whether the agent-tooling community sees a fit for the Intent Eval Platform's positioning.
- **Reopener:** VP DevRel seat (proper standing per "community-temperature is DevRel seat territory").
- **Constraint:** If response is positive, escalate to full ISEDC before any next step.
- **Constraint:** If response is negative or non-response, S3Q2 reverts to closed-binding; no further reopening until next quarterly review.

**Public Decision Records (VPDevRel non-negotiable floor):**
- Every Class 1 Decision Record published to a public archive within 7 days of decision-lock.
- Public archive location: `intent-eval-lab/000-docs/` on the `main` branch of the public OSS repo (`jeremylongshore/intent-eval-lab`).
- Verbatim seat positions preserved per ISEDC discipline.

**Stacked binding constraints:**
1. **(VPDevRel non-negotiable)** Closed convening + closed records is indistinguishable from no-governance from the OSS-community lens. Public archive within 7 days is the floor.
2. **(GC non-negotiable)** Annual full review of all active bindings is the minimum cadence. Default-preserve becomes default-forgotten without periodic re-touch.
3. **(CFO bandwidth gate)** Quarterly + ad-hoc convening capped at ~12 founder-hrs/yr governance overhead. Exceed = re-scope.
4. **(CISO non-negotiable)** Any change to DNSSEC / CAA at predicate-URI subdomains, any new Fulcio identity, any new predicate URI type — REQUIRES CISO-seat sign-off before the change lands, regardless of whether full ISEDC convenes.
5. **(CSO non-negotiable)** Any externally-visible artifact addressed to a named SIG-GenAI / in-toto / SLSA / CNCF / OpenSSF maintainer requires CSO sign-off before send. No exceptions, no tempo overrides.

---

## 8. Council memos (verbatim, condensed)

### CTO

*"The widening is real and the schema is the only invariant that survives it. **Evidence Bundle as lingua franca is the right invariant; everything else federates around it.** Q3 (URI namespace) and Q4#6 (spec-as-portable-doc) are most-costly-to-recover. Q3 is literal one-way door; Q4#6 is opposite — if we DON'T separate spec from impl now, SPEC.md will accrete implementation references until extraction is impossible. Holding firm on Q3 grammar-lock-before-first-attestation and Q5 pause-to-converge against expected CFO + CMO pressure; cost asymmetry is real."*

### GC

*"The widening multiplies the surface area on which Intent Solutions makes permanent commitments. My job across all six questions: slow down the irreversible decisions, speed up the reversible ones. Q1 (architectural fork) and Q3 (URI namespace widening) are most-costly. Trademark misstep in Q1 = USPTO C&D exposure, five-figures minimum. URI namespace misstep in Q3 = **literally unrecoverable** — Rekor is immutable. Holding firm against CMO Option-C push on Q1, against 'unification thesis' as marketing language before binding spec in Q3, against any new public repo before license audit + name clearance in Q5."*

### CMO

*"The widening is not a scope expansion — it's a **category-authorship moment**. Most-costly: Q1 and Q3. Q1=A surrenders multi-platform narrative surface permanently. Q3 widening locks brand+namespace coupling we can never untangle. Holding firm against CTO push to delay Q1 architectural lock for schema-first reasons; against CFO push to defer umbrella brand work on bandwidth grounds; with CISO on URI namespace non-widening (the one place I trade brand for safety, bound publicly). Dissenting from implicit 'TS lock was platform decision' framing — it was a j-rig decision, never platform-wide."*

### CFO

*"The widening is a positioning opportunity disguised as a build mandate. 3-5 hr/wk sole-prop with one revenue signal cannot execute three platforms. Available 78–130 hrs over 6 months; widened plan as-pitched needs 125–184. Gap is 54+ hours that doesn't exist. Either cut scope, secure 2nd paying customer to expand bandwidth, or accept shipping none of it well. Folding-in is CONVERGENCE (reduces surface), NOT ADDITION (multiplies surface). My recommendations preserve fold-in while refusing addition. Most-costly: Q1 (sunk-cost trap) and Q3 (URIs are permanent in Rekor). Holding firm on TS lock, +50 hr cap, no URI expansion, pause-and-converge, no platform-builds without 2nd paying customer. Kobiton M2 protection non-negotiable."*

### CSO

*"Standards-body realpolitik is a first-impression-permanent domain. Every question has a 'looks like marketing, is actually standards-body' dimension. **Community-temperature ALWAYS precedes RFC filing; named-maintainer first-impressions permanent; URI slots reserved only when working attestations back them.** Most-costly: Q1=C (reopens S1Q1 URI namespace; once we float 'platform-of-platforms' to a SIG-GenAI maintainer, that's our identity in their head forever) and Q3 pre-reservation (gets us labeled 'namespace squatter' by in-toto reviewers on first scan). On Q5, OTel informal-email Week 1 ships in some form even under pause-to-converge majority — silence with warm maintainer is worse than honest in-flight signal. Non-negotiable from this seat."*

### CISO

*"The widening proposal is dressed as architecture but reads as attack-surface expansion under deadline pressure. **Immutable artifacts deserve normative specifications written BEFORE the artifact is signed.** Predicate URIs, DNSSEC apices, Fulcio identities, Rekor entries are all 'write-once' in threat-model sense. Most-costly: Q3 (predicate URI widening) and Q5 (M5-before-SPEC sequencing). Both failure modes look fine for weeks then become structurally unfixable. Holding firm against approving `agent-loop-trace/v1` for v1, against shipping M5 production attestations before SPEC.md normative, against dropping S1Q5 provider PASS/FAIL gates — those remain non-negotiable, I explicitly DECLINE TO REOPEN despite the mandate's invitation. Failure mode is permanent credential leakage to provider training corpus; not recoverable."*

### VP DevRel

*"The widening is strategically correct AND operationally hazardous. **Does the Saturday-afternoon dev who clones a repo today have a working thing in front of them, or do they have a stub and a promise?** Today they have a stub and a promise. Recoverable if M5.1 ships in weeks not quarters; unrecoverable if 60 days spent unifying predicate URI namespaces while action.yml still says 'decision=not-implemented'. ONE BIG platform, TS-first surface, M5.1-leads sequencing, dev-visible Uncle Bob borrows (#3, #4, #5, #6) convert the 45k+ NPM warm market into adopters. Most-costly: Q5 (sequencing) and Q2 (language). Reopening S3Q2 (@pvncher) explicitly within DevRel territory. Closed-convening + closed-records = indistinguishable from no-governance from OSS-community lens — public archive within 7 days is my floor."*

## 9. Cross-cutting themes

### Most-costly-to-recover-from tallies

| Question | Seats naming it most-costly |
|---|---|
| **Q1 (Architectural Fork)** | CTO, GC, CMO, CSO, CISO (5 of 7) |
| **Q3 (URI namespace + drift-prevention)** | CTO, GC, CSO, CISO, CFO (5 of 7) |
| **Q5 (Sequencing)** | CFO, VPDevRel, CISO (3 of 7) |
| **Q2 (Language)** | VPDevRel (1 of 7) |
| Q4 (Uncle Bob) | None |
| Q6 (Governance) | None |

**Q1 and Q3 are the irreversibles. The decisions taken in §7 above stack minority binding constraints into both.**

### Adversarial integrity check

Verbatim dissent is preserved in §7 and §8. Key dissent surfaces:

1. **CTO + CMO dissent on Q1** (preferred C; majority chose A) — minority bindings inscribed: defensive name registration, schema-stability SLA, 12-month exit-ramp option.
2. **CFO dissent on Q5 widening cap** — majority accepted CFO bandwidth math; CFO's +50hr cap is binding, not advisory.
3. **CISO dissent on `agent-loop-trace/v1`** — REJECTED for v1; sanitization spec gate preserved.
4. **GC dissent on Q1 trademark clearance velocity** — minority binding inscribed: clearance Decision Record before any rename; vendor-generic scrub binding stays in force.
5. **VPDevRel dissent on Q6 closed-records** — minority binding inscribed as floor: public archive within 7 days.

All dissents stack as binding constraints on the majority recommendation rather than being suppressed.

### How synthesis lenses landed

1. **Arena (5 surfaces):** all 5 surfaces remain in scope; Evidence Bundle is the cross-surface lingua franca per Q3 unification thesis.
2. **Both sides:** client + server eval both covered; rollout-gate is client-side, j-rig is both.
3. **Transformation pipeline:** preserved as scope-map; no surface added or removed.
4. **Composable partial attestation:** elevated to binding architectural principle (Q3 unification). Coverage-as-prefilter (Q4#5) must respect "silence ≠ failure" — emit "skipped-by-prefilter" predicate, never silently skip.
5. **AISE 5-domain stack:** becomes internal scope map under Q1=A. Not a separate-brand surface. New platform-builds (LLM Harness Lab, Agent Runtime Sandbox) stay as design-doc-only per Q5 bandwidth gate.
6. **Sole-prop bandwidth reality:** CFO bandwidth math became load-bearing on Q5 + Q6; +50hr widening cap and 12 founder-hrs/yr governance overhead are binding.

## 10. Prior bindings — reopened, preserved, or reaffirmed

| Binding | Status |
|---|---|
| **S1Q1** — `evals.intentsolutions.io` URI namespace + DNSSEC + CAA pinning | **REAFFIRMED**; widened incrementally per Q3 (sub-paths approved, not new subdomains) |
| **S1Q2** — partner-consent (vendor-generic only through Phase B+1) | **REAFFIRMED** + extended to widened scope; case-study scrub binding stays in force across all AISE 5 domains |
| **S1Q3** — MM-7 defer + CONTRIBUTING-failure-shape path | **REAFFIRMED** |
| **S1Q4** — OTel CSO sequence (informal email FIRST, RFC Week 4+) | **REAFFIRMED**; Week 1 informal email ships regardless of pause-or-parallel majority per Q5 stacked CSO non-negotiable |
| **S1Q5** — provider PASS/FAIL gates (credential-redaction + env-var spillover) | **REAFFIRMED** — CISO explicitly DECLINED reopening despite mandate's invitation. Non-negotiable for any provider abstraction. |
| **S3Q2** — no @pvncher engagement | **REOPENED NARROWLY** — informal community-temperature email only per CSO Week 1 pattern; VPDevRel reopener standing; no RFC, no formal ask, no public engagement beyond the email; positive response escalates to full ISEDC |
| **S3Q3** — FUTURE.md gateway federation deferral | **REAFFIRMED** |
| **2026-05-13 ad-hoc** — TS-primary lock for `intent-rollout-gate` | **REAFFIRMED AND GENERALIZED** — TS-primary at every signing-adjacent + dev-facing surface across the platform; Python permitted at ML internals behind subprocess boundaries (Q2 stacked constraints) |
| **2026-05-10 (DR-004)** — `labs.intentsolutions.io` reserved-don't-touch for predicate URIs | **REAFFIRMED** — widening does NOT touch it |

## 11. Per-artifact fold-in plan (the unique mandate from this session)

User directive: *"The work that we started in this plan needs to fold into the new plan. If it needs to be rearranged and restructured, that is fine. We do not just stop what we are working on."*

| In-flight artifact | Current state | Fold-in destination | Rearrangement / restructure |
|---|---|---|---|
| **`008-DR-GAPS-spec-vs-system-brief-2026-05-11.md`** | Landed in `intent-eval-lab/000-docs/` | Keep as-is. Reference from Q3 binding. | None — gap analysis still informs Phase B work. |
| **`FUTURE.md`** | Landed | Keep + add new entries: design-doc-only LLM Harness Lab; design-doc-only Agent Runtime Sandbox; deferred predicate URIs (`harness-experiment/v1`, `cache-decision/v1`); rejected predicate URI `agent-loop-trace/v1` (gated on sanitization spec) | Append per this DR's outcomes; no rewrites. |
| **`009-RR-INTL-otel-sig-genai-temperature.md`** | Landed (paper trail file per S1Q4) | Keep. Week 1 informal email + response/timeout still in scope. | If pause-and-parallel-majority adds an "in-flight signal" note to the email per CSO stacked non-negotiable, that note gets appended to this file. |
| **`intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/SPEC.md`** | NOT yet authored (bead `iel-ni9` P0) | **PROMOTED to absolute-top-priority** per Q3 CRITICAL drift fix + Q4#6 spec-as-portable-doc binding. Phase A weeks 1–2. | Authored as portable spec (no impl refs). Includes URI grammar lock + signing/verification section + policy consumption section pointing to `tests/TESTING.md` consumer config (NOT a peer policy spec module — per prior plan critique). |
| **`intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json`** | NOT yet authored (bead `iel-f28` P0) | Phase A weeks 1–2 alongside SPEC.md. Codegen to Pydantic + Zod enforced by CI (Q2 stacked binding). | None — JSON Schema as canonical, language bindings derived. |
| **`intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/examples/{policy.yaml, evidence-bundle.json, in-toto-statement.json}`** | NOT yet authored | Phase A weeks 1–2 as informative examples. Policy example is `tests/TESTING.md` shape (NOT normative). | None. |
| **`intent-eval-lab/specs/UNIFICATION.md`** | Does not exist | NEW — created within 30 days per Q3 unification-thesis binding. Referenced from every constituent repo's CLAUDE.md. | New artifact. |
| **`intent-eval-lab/specs/PREDICATE-TYPES.md`** | Does not exist | NEW — registry per Q3 GC discipline. Updated within 7d of any new subtype going live. | New artifact. |
| **`intent-eval-lab/specs/sanitization/v0.1.0-draft/SPEC.md`** | Does not exist | NEW — gates `agent-loop-trace/v1` predicate URI. Phase B scope. | New artifact. |
| **`intent-eval-lab/specs/taxonomy/v0.1.0-draft/SPEC.md`** | Does not exist | NEW — central 7-layer taxonomy doc extracted from audit-tests + implement-tests SKILL.md (MEDIUM drift fix). Phase B scope. Both skills symlink. | New artifact + skill SKILL.md updates. |
| **`intent-eval-lab/specs/FUTURE-platforms/llm-harness-lab/README.md`** | Does not exist | NEW — design-doc-only state per Q5 bandwidth gate. Scope, unlock triggers, recommended Python stack noted. NO code. | New artifact. |
| **`intent-eval-lab/specs/FUTURE-platforms/agent-runtime-sandbox/README.md`** | Does not exist | NEW — design-doc-only state per Q5. NO code. | New artifact. |
| **`intent-rollout-gate` repo (M4 bootstrap commit `87de651`)** | Public, action.yml composite stub returning `decision=not-implemented` exit 0 | KEEP repo public. M4 substantive-stub contract preserved (early-adopter exit-0 promise still honored). | None. M5.1 superseded action.yml replaces the composite stub. |
| **`intent-rollout-gate/000-docs/001-DR-DESIGN-rollout-gate-architecture-...md`** | Landed | KEEP as-is. Reference from Q5 sequencing. | None. |
| **`intent-rollout-gate` branch `feat/m5-typescript-runtime-lock-and-mvp`** | Checked out, zero commits | RESUMED. M5.1 PR proceeds per the master plan's TS skeleton + policy parser + bundle loader + decision engine + PR-comment renderer + dist build + CI. **Branch renamed: `feat/m5.1-ts-runtime-experimental-v0.1.0`** to make the experimental-mode-gate explicit. | New Decision Record `intent-rollout-gate/000-docs/002-AT-DECR-runtime-language-typescript-2026-05-13.md` (referenced from this DR) lands first; cites this DR's Q2 stacked constraints. M5.1 v0.1 ships EXPERIMENTAL on sigstore staging; v0.2 (after SPEC.md normative lands) cuts to production Rekor. |
| **11 existing validators** (validate-skillmd v5.0.1, validate-plugin v2.1.0, validate-agent v1.0.0, validate-mcp v1.0.0, validate-hook v1.0.0, validate-consistency v1.0.0, validate-marketplace v1.0.0, audit-tests v7.1.0, implement-tests v1.1.0, sync-testing-harness v0.1.0, audit-harness v0.3.0) | Working; inconsistent emit-Evidence-Bundle posture | KEEP all where they are. Phase B retrofit: each gets an `--emit-evidence` mode per Q3 unification thesis. Sequenced after M5.1 v0.2 cuts to production. No language migration. | New beads filed per validator under the new "Tooling Drift Prevention" Plane sub-module. |
| **`j-rig-binary-eval` v0.23.0** | Working; already emits Evidence Bundle (M3-equivalent complete per master plan) | KEEP as reference implementation. Phase B: Zod validator bridge to incoming Evidence Bundle rows; AGENTS.md parser; provider abstraction with CISO PASS/FAIL gates. | Already aligned with Q1=A platform identity. |
| **`audit-harness` v0.3.0** | Working; already emits Evidence Bundle (M2-equivalent complete) | KEEP as polyglot reference. Phase B: SEMVER regression test suite (HIGH drift fix). | None. |
| **CRITICAL drift risk (SPEC.md skeleton-only)** | Open | **PROMOTED to absolute-top-priority** per Q3. Beads `iel-ni9` + `iel-f28` re-prioritized P0. | First work item out of this DR. |
| **HIGH × 3 drift risks** (Anthropic snapshots manual-freeze, j-rig Tier 3 no spec, audit-harness SEMVER hand-written) | Open | Phase B per Q3. New beads filed. | None. |
| **MEDIUM × 3 drift risks** (7-layer taxonomy embedded, SCHEMA_CHANGELOG manual sync, validate-consistency rules embedded) | Open | Phase B per Q3. | None. |
| **Plane LAB-6 (IEL-CONV-1)** | HQ | REAFFIRMED as HQ. NEW sub-module "Tooling Drift Prevention" created underneath. | Add cross-reference to this DR. |
| **Sister module in JRIG project** | Exists | REAFFIRMED. | None. |
| **Existing beads `iel-uj0`, `iel-71s`, etc.** | Open in `iel-` prefix | KEEP open. Re-prioritize per Phase A / Phase B sequencing above. | Bead-level updates per the locked sequence; no bead deletions. |
| **Meta-bead `OPS-nfx`** (execution-tracking bead in home `~/.beads/`) | Open | KEEP. Add comment linking to this DR. | None. |
| **Master plan `~/.claude/plans/se-the-council-bubbly-frog.md`** | Authored | REFRESH with this DR's outcomes folded into Phase A / Phase B / FUTURE sections. | Light edits + appendix pointing to this DR. |
| **Kobiton M2 work (kobiton repo)** | Active, first priority | UNTOUCHED. Runs on its own track. Off-the-top from founder-hour budget. | None. |
| **Nixtla / claude-code-plugins / trucking / VPS-as-the-home / Anthropic Enterprise cohort** | Active | UNTOUCHED. | None — eval-platform widening fits in residual capacity per CFO bandwidth gate. |

## 12. Implementation directives

| Workstream | Phase | Owner | Beads to file |
|---|---|---|---|
| SPEC.md normative content for `gate-result/v1` | Phase A, weeks 1–2 | Solo (Jeremy) | Re-prioritize `iel-ni9` to P0; add child beads for §URI grammar, §Signing, §Policy consumption, §Subject naming |
| JSON Schema for `gate-result/v1` | Phase A, weeks 1–2 | Solo (Jeremy) | Re-prioritize `iel-f28` to P0 |
| Uncle Bob #6 (spec-as-portable-doc) authoring discipline | Phase A, weeks 1–2 | Solo (Jeremy) | New bead `iel-???` "Adopt Uncle Bob #6 spec-as-portable-doc" |
| Examples (policy.yaml, evidence-bundle.json, in-toto-statement.json) | Phase A, weeks 1–2 | Solo (Jeremy) | Sub-bead of `iel-ni9` |
| UNIFICATION.md authoring | Phase A, within 30 days | Solo (Jeremy) | New bead |
| PREDICATE-TYPES.md registry | Phase A, within 30 days | Solo (Jeremy) | New bead |
| M5.1 v0.1.0-experimental TS implementation | Phase A, weeks 1–4 (PARALLEL with SPEC.md track) | Solo (Jeremy) | Existing M5.1 bead cluster; rename branch to `feat/m5.1-ts-runtime-experimental-v0.1.0`; new DR `intent-rollout-gate/000-docs/002-AT-DECR-runtime-language-typescript-2026-05-13.md` |
| OTel informal email Week 1 (CSO non-negotiable) | Phase A, week 1 | Solo (Jeremy) | Existing bead per S1Q4 paper trail |
| M5.1 v0.2.0 production cut (after SPEC.md normative lands) | Phase A, weeks 5–8 | Solo (Jeremy) | New bead "M5.1 v0.2 production-Rekor signing enabled" |
| Add `validation-result/v1` + `eval-verdict/v1` + `cost-attribution/v1` predicate URIs | Phase A, weeks 5–8 | Solo (Jeremy) | New beads per predicate type |
| Plane "Tooling Drift Prevention" sub-module creation | Phase A, week 1 | Solo (Jeremy) via Plane MCP | New Plane sub-module under LAB-6 |
| New DR `002-AT-DECR-runtime-language-typescript` in intent-rollout-gate | Phase A, week 1 | Solo (Jeremy) | Self-contained Decision Record citing this DR's Q2 |
| Anthropic snapshot auto-update CI gate | Phase B | Solo (Jeremy) | New bead — HIGH drift fix |
| j-rig Tier 3 ↔ validate-skillmd Tier 1-2 spec bridge | Phase B | Solo (Jeremy) | New bead — HIGH drift fix |
| audit-harness SEMVER regression test suite | Phase B | Solo (Jeremy) | New bead — HIGH drift fix |
| 7-layer taxonomy extraction to central spec | Phase B | Solo (Jeremy) | New bead — MEDIUM drift fix |
| SCHEMA_CHANGELOG pre-commit hook | Phase B | Solo (Jeremy) | New bead — MEDIUM drift fix |
| validate-consistency Drift Detection Spec extraction | Phase B | Solo (Jeremy) | New bead — MEDIUM drift fix |
| sanitization spec for `agent-loop-trace/v1` (gates the v1 predicate) | Phase B | Solo (Jeremy) | New bead — CISO REJECTED gate |
| LLM Harness Lab design-doc-only README in `specs/FUTURE-platforms/` | Phase A, any time | Solo (Jeremy) | New bead |
| Agent Runtime Sandbox design-doc-only README | Phase A, any time | Solo (Jeremy) | New bead |
| 11-validator `--emit-evidence` retrofits | Phase B, sequenced after M5.1 v0.2 | Solo (Jeremy) | New beads per validator (clustered under new GH umbrella issue per CLAUDE.md sub-bead pattern) |
| @pvncher informal community-temperature email (S3Q2 narrow reopen) | Phase B opportunistically | Solo (Jeremy) | New bead under VPDevRel-tagged convening |
| Quarterly ISEDC review cadence | Standing | Acting head of board | Calendar reminder + new bead at start of each quarter |
| Public Decision Record archive (`intent-eval-lab` public on main) | Standing | Solo (Jeremy) | Push this DR + DR-004/005/006 to public main within 7 days |
| Master plan file refresh (`se-the-council-bubbly-frog.md`) | Phase A, week 1 | Solo (Jeremy) | Append section "Phase B — locked by ISEDC Session 4 2026-05-13" referencing this DR |
| Bead `iel-5eo` (this council session tracking bead) | Phase A, immediate | Solo (Jeremy) | Close with evidence (this DR + Plane updates) |

## 13. Reusable pattern reference

This council session is the second canonical invocation of the ISEDC pattern (`~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0). The first was 2026-05-10 (DR-004). Two novel dynamics surfaced in this session worth encoding for future invocations:

1. **The "fold-in mandate" extension to the workflow** — when the user directs the council to absorb in-flight work into a widened scope rather than starting fresh, the Decision Record must include an explicit per-artifact fold-in plan (§11 above) as an additional structural section. The reusable pattern's Workflow Step 9 should reference this section type for future fold-in sessions.
2. **The "reopened bindings" §10 section pattern** — when the mandate declares prior bindings reopenable, the DR must explicitly list each prior binding with status (REAFFIRMED / REOPENED / RELITIGATED) so future readers reconstruct what was preserved versus revisited.

Both extensions are candidates for a v1.1.0 bump of the `exec-decision-council` skill.

## 13.5. Acting Head of Board Override Addendum — 2026-05-13 (post-synthesis)

**Issued by:** Jeremy Longshore, acting head of board.
**Timing:** Issued after the council synthesis (§ 7–§ 13) was drafted, BEFORE the Decision Record was signed into final form. Per ISEDC discipline ("(Per-question overrides) Accept majority on N questions, override on others"), the acting head of board has standing to override seat positions, including stacked minority bindings, when the framing of those bindings drifts from acting-head directive.

**Verbatim user directive (three-part, captured verbatim per ISEDC adversarial-integrity protocol):**

> *"we r not waitinf for paying custonsrs this is internal tool i am creating"*
>
> *"we r not o concerned with marketing customers etc anything like that i have a following"*

(Voice-dictation artifacts preserved verbatim; the substance is unambiguous.)

**Substance of the override:**

The acting head of board observes that several seat positions — particularly CFO's "no new platform-build implementation in 6 months without second paying-customer signal" gate, GC's "no public repo before license audit + name clearance" (when read through a customer-signal lens), CMO's "category-authorship before competitors" framing, and VP DevRel's "convert 45k+ NPM warm market" framing — collectively rebuilt a customer-acquisition / marketing-customer / paying-signal architecture that the same acting head of board explicitly lifted at ISEDC Session 3 (DR-006 Q1) and reaffirmed at the start of Session 4.

The acting head of board re-asserts: **this is an internal tool the acting head of board is creating for his own use, distributed naturally through the existing following (claude-code-plugins audience, OSS reputation, Anthropic Enterprise cohort proximity).** Distribution is a consequence of building the right thing, not an acquisition campaign. The customer-signal gate on platform-build implementation is REMOVED. The marketing-customer framing across CMO + VPDevRel positions is REMOVED.

**What changes (specific stacked-binding revisions):**

| Original stacked binding | Override status | Replacement |
|---|---|---|
| **Q5 CFO** "No new platform-build implementation in next 6 months. LLM Harness Lab + Agent Runtime Sandbox stay as design-doc-only state. Gated on second paying-customer signal (signal #2 unlocks first platform-build)." | **OVERRIDDEN — customer-signal clause removed.** | New platform-builds (LLM Harness Lab, Agent Runtime Sandbox) are gated on **bandwidth only**, not customer-signal. Default sequence: SPEC.md normative (Phase A) → M5 production (Phase A weeks 5-8) → internal dogfood (Phase A weeks 9-16) → new platform-build implementation begins as bandwidth permits, no customer-signal precondition. CFO bandwidth math (+50hr cap, +66hr ceiling, 3-5 hrs/wk reality) **stands intact** — the only change is the GATE TRIGGER. |
| **Q5 GC** "No new public repo for LLM Harness Lab or Agent Runtime Sandbox before (a) license audit complete, (b) name cleared by GC, (c) Decision Record filed. Until those gates: design-doc only." | **PRESERVED — these are IP/legal gates, not customer gates.** | License audit + name clearance + DR filing remain non-negotiable for any new public repo. Customer-signal language stripped where it appeared. |
| **Q1 CMO** "Category-define before competitors do" + "first-mover authorship of the phrase 'AI Reliability infrastructure'" | **OVERRIDDEN — marketing-customer framing removed.** | Defensive name registration (domain + npm scope + GitHub org alias) is PRESERVED as IP discipline. The "category-authorship velocity" framing is removed — the platform is named "Intent Eval Platform" per Q1=A; the acting head of board's existing following is the distribution channel; no first-mover-vs-competitor framing applies. |
| **Q5 VPDevRel** "Convert 45k+ NPM warm market into actual adopters" / "Saturday-afternoon dev test" | **REFRAMED — same test, different purpose.** | The Saturday-afternoon-dev friction test is PRESERVED as an internal-quality discipline (the acting head of board IS a dev, the tool must work for him on a Saturday afternoon). The "convert warm market" / "adoption funnel" framing is removed — the following will find the tool naturally; no conversion campaign. |
| **Q5 CMO** "M5.1's PR comment template must include the umbrella tagline + link to umbrella site" | **OVERRIDDEN — marketing surface removed.** | PR comment template carries technical content only (decision, summary, reasons, coverage). No tagline, no umbrella-site link. Honest engineering output, not marketing surface. |
| **M6 framing (master plan + DR-010)** "Public rollout shipped — quickstart, example repo, blog post(s), Plane CONTENT-tagged ideas filed. Platform discoverable to the existing 45k+ NPM audience." | **REFRAMED.** | Public availability shipped — quickstart, example repo, technical post-mortem / build-notes on startaitools.com. The following discovers the tool through normal channels (claude-code-plugins README cross-link, organic blog readership, OSS dependency graph). No customer-acquisition campaign, no funnel content, no "convert" framing. |
| **Q6 CMO** "Quarterly category-positioning standing convening" | **OVERRIDDEN — category-positioning convening removed.** | Quarterly ISEDC standing remains for binding-review discipline. The CMO-chaired "category-positioning review" is removed — there is no category-positioning campaign to review. |

**What is explicitly NOT overridden (all technical/security/IP/standards-body discipline preserved):**

- **All CISO bindings stand**: zero production-Rekor signing before SPEC.md normative; URI grammar lock before first attestation; per-predicate gates (`agent-loop-trace/v1` REJECTED); sigstore staging discipline; provider PASS/FAIL gates (S1Q5 explicitly declined reopening — stays binding).
- **All CTO bindings stand**: hard internal package boundaries, per-domain CODEOWNERS, schema-stability SLA, JSON Schema → Pydantic + Zod codegen CI gate, URI grammar `evals.intentsolutions.io/<predicate-type>/v<version>`.
- **All GC IP discipline stands**: vendor-generic scrub binding extends across AISE 5 domains, license audit for any Python dependency tree, LICENSES.md + pip-licenses CI gate, PREDICATE-TYPES.md registry. **The IP gates are NOT customer-signal gates and remain in force regardless of internal-vs-external framing.**
- **All CSO standards-body discipline stands**: OTel informal-email Week 1 ships, community-temperature before RFC, named-maintainer sign-off, S1Q4 sequence.
- **CFO bandwidth math stands**: +50hr widening cap, +66hr hard ceiling, 3-5 hrs/wk reality, Kobiton M2 first priority off-the-top. Only the customer-signal GATE TRIGGER is overridden — the bandwidth math itself is untouched.
- **Q1=A (single converged Intent Eval Platform), Q2 (per-artifact hybrid), Q3 (unification thesis binding + incremental URI namespace), Q4 (all 6 Uncle Bob borrows approved with security bindings), Q5 sequencing (parallel-track with experimental-mode gate), Q6 three-class governance + public DR archive within 7d**: ALL STAND.

**Why the override:**

The acting head of board explicitly removed the paying-customer gate at ISEDC Session 3 (DR-006 Q1) with the directive *"if we build it the people will come focus on building dont worry about distribution right now"*. The Session 4 council, deliberating in good faith, partially reconstituted that gate through CFO bandwidth math + GC paper-trail + CMO category-authorship + VPDevRel adoption-funnel framings. This was honest adversarial work from each seat's value system — the framings were not bad-faith. But they collectively reproduced an architecture the acting head of board had already removed.

The override re-asserts the build-mode directive: **internal tool, build it for myself, distribute naturally through the following I already have, no customer-acquisition or marketing-customer framing**. Adversarial integrity is preserved by capturing the seat positions verbatim in § 7–§ 8 AND capturing this override verbatim here. Future readers see both: the council's good-faith work + the acting head of board's framing call.

**Verbatim acting-head-of-board declaration on this override:**

> Per ISEDC discipline, the acting head of board makes final calls after weighing steel-manned minority positions. The customer-signal framing the council reconstituted is overridden. The IP / security / standards-body / bandwidth-math disciplines stand. The platform is built as an internal tool, distributed naturally through the acting head of board's existing following. — Jeremy Longshore, 2026-05-13.

---

## 13.6. Acting Head of Board Override Addendum #2 — 2026-05-13 (post-§ 13.5)

**Issued by:** Jeremy Longshore, acting head of board.
**Timing:** Issued after § 13.5 (post-synthesis), BEFORE the Decision Record was signed into final form.

**Verbatim user directives (two-part):**

> *"internal tool we are building for internals to share with the world also"*
>
> *"patterns we borrow from other people are not to be i cluded in forward deployed work"*

**Substance of the override:**

### Part A — Internal-tool framing clarified

The first override addendum (§ 13.5) established "internal tool, distributed naturally via existing following." The acting head of board clarifies the framing: this is **an internal tool built for internal use (by the acting head of board and Intent Solutions practice), simultaneously shared with the world** as an OSS artifact. It is not "internal use only" — public availability remains in scope (M6 public-rollout deliverables stand). It is not "primarily a public product for sale" — the framing is built-for-use, shared-because-OSS-default, distributed-naturally-via-following. Both halves of the framing are load-bearing:

- **Built for internals**: the design priority is "does this work for the acting head of board on a Saturday afternoon when he opens an internal project that uses it" — NOT "does this convert an external prospect."
- **Shared with the world**: M6 public-rollout deliverables (quickstart, example repo, technical posts, OSS license, public DRs) all ship. The 7-day public-DR-archive binding (Q6 VPDevRel) stands. The Apache 2.0 / MIT license per repo stands.

No further structural change from § 13.5 — this is a clarification rider that prevents future readers from misreading § 13.5 as "private/internal only."

### Part B — Q4 Uncle Bob pattern adoption REVERSED

The Q4 council position was: **borrow all 6 Uncle Bob patterns** (#1 two-mode pipeline IR, #2 type-detection mutation rule table, #3 0/1/2/3 exit-code grammar, #4 Killed/Survived/Error trichotomy, #5 coverage-as-prefilter, #6 spec-as-portable-doc) with GC attribution discipline + CISO security bindings. This position was near-unanimous (#3, #4, #6 unanimous; #1, #2, #5 6-of-7).

The acting head of board **REVERSES Q4 in its entirety.** Patterns borrowed from external authors (Uncle Bob / `unclebob/Acceptance-Pipeline-Specification` / `mutate4java` / `crap4java` / `swarm-forge` / any other named external source) are NOT to be included in forward-deployed work.

**Concrete revisions:**

| Original Q4 position | Override status |
|---|---|
| #1 Two-mode pipeline IR — BORROW | **NOT BORROWED.** Evidence Bundle row design for j-rig's acceptance/mutation modes is derived independently if/when the requirement surfaces in our own work. No `unclebob/Acceptance-Pipeline-Specification` reference in SPEC.md, code, or design docs. |
| #2 Type-detection mutation rule table — BORROW with CISO bindings | **NOT BORROWED.** No `mutate4java` reference. If j-rig mutation-style input fuzzing is ever scoped, design from first principles based on our own needs. |
| #3 0/1/2/3 exit-code grammar — UNANIMOUS BORROW | **NOT BORROWED as a named pattern.** Exit codes in our tooling are designed from first principles for our specific use cases. We may end up with 0/1/2/3 or 0/1/2 or 0/1 — whatever the contract requires — but it is NOT documented as "borrowed from Uncle Bob's exit-code grammar." No external citation. No "informed by" footer. |
| #4 Killed/Survived/Error trichotomy — UNANIMOUS BORROW | **NOT BORROWED as a named pattern.** j-rig verdict states (judge-passed / judge-failed / judge-errored or whatever naming we choose) are designed from our own use cases, not from mutation-testing literature. No external citation. |
| #5 Coverage-as-prefilter — BORROW with CISO bindings | **NOT BORROWED.** Coverage-prefilter optimization, if/when scoped, is derived from our own performance needs. No `mutate4java` or JaCoCo-style attribution. |
| #6 Spec-as-portable-doc separated from reference impl — UNANIMOUS BORROW (called out as "highest leverage" by CTO + GC) | **NOT BORROWED as a named pattern.** SPEC.md will be authored as a portable spec (no implementation references in the spec; reference impl in separate doc) — this is good engineering discipline — but it is NOT documented or cited as "borrowed from Uncle Bob / standards-body separation-of-concerns pattern." We do it because it's correct for our work, not because someone else did it first. |

**Forward-deployed work governance (new rule):**

In specs, code comments, design docs, READMEs, blog posts, public DRs, RFC text, OTel proposals, and any other forward-deployed artifact:

- **No "Patterns informed by X" footers.** GC attribution discipline from Q4 is overridden — there is nothing to attribute because we are not borrowing.
- **No "inspired by" / "based on" / "drawing from" external-author references.** We design from first principles for our specific needs.
- **No external-pattern names** (no "two-mode pipeline IR," no "Killed/Survived/Error trichotomy," no "coverage-as-prefilter," no "spec-as-portable-doc") as named-pattern citations. If the underlying design lands in our work, it lands as our own design with our own naming, derived from our own use cases.

**What is still permitted:**

- **Citing standards** (in-toto Statement v1, DSSE envelope, JSON Schema, OpenTelemetry semantic-conventions, SLSA, OpenSSF) — these are open standards we conform to, not patterns we borrow. Conforming to a standard ≠ borrowing a pattern.
- **Citing tools we depend on** (cosign, sigstore, npm, pnpm, vitest) — runtime dependencies, not pattern borrowing.
- **Internal patterns from prior Intent Solutions work** — Evidence Bundle, predicate URIs, the audit-harness `--json` reference pattern, MM-1..MM-6 intentional-mapping vocabulary, the 7-layer testing taxonomy — these are our own work and may be cross-referenced freely.
- **Common-vocabulary terms** (exit code, JSON output, structured logging, semantic versioning, schema validation) — these are vocabulary, not borrowed patterns.

**Implementation effect on the locked sequencing:**

- The ~14 founder-hours allocated in § 7 Q4 to "borrow all 6 patterns" is **reclaimed**. Some of that work was load-bearing (SPEC.md normative authoring overlaps with what Q4#6 "spec-as-portable-doc" would have covered) — that work still happens, but as our own engineering discipline, not as a borrowed pattern. The remaining hours fold back into bandwidth headroom or accelerate Phase A.
- Master plan + DR-010 §10 (per-artifact fold-in) references to Uncle Bob borrows are nullified by this override.

**What stays from Q4:**

- The "explicit non-borrows" (FitNesse wiki-tables, swarm-forge tmux orchestration, CRAP formula) remain non-borrows — they were already user-locked.
- GC attribution discipline as a general principle (cite external standards we conform to; do not silently appropriate) is broadened: not just "attribute carefully" but "do not borrow at all from named external authors into forward-deployed work."

**Verbatim acting-head-of-board declaration on this second override:**

> The platform is the acting head of board's own engineering practice made shareable. Forward-deployed work reflects our own thinking — not a pattern-library remix. Standards and dependencies are cited as standards and dependencies; external-author patterns are not borrowed into our specs or code. Internal use comes first; public sharing is a default OSS posture, not a marketing-customer architecture. — Jeremy Longshore, 2026-05-13.

---

## 14. Acting head of board declaration

| Field | Value |
|---|---|
| **Acting head of board** | Jeremy Longshore (Intent Solutions) |
| **Decision date** | 2026-05-13 |
| **Mandate scope** | Full architectural lock (user-confirmed in this session) |
| **Prior-bindings scope** | Everything reopenable (user-confirmed in this session) |
| **Signature** | Decisions in §7 reflect the council's majority recommendations with stacked minority binding constraints. The acting head of board accepts the majority position on each question and binds the stacked minority constraints into the implementation directives (§12). Dissenting positions preserved verbatim in §7 and §8 per ISEDC adversarial-integrity protocol. |

— Jeremy Longshore
intentsolutions.io

## 15. References

- **Plan file (input brief):** `~/.claude/plans/se-the-council-bubbly-frog.md`
- **Uncle Bob candidate report:** `~/.claude/plans/se-the-council-bubbly-frog-agent-a99fbfa551607a51b.md`
- **Prior Decision Records:**
  - `intent-eval-lab/000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md` (Session 1, DR-004)
  - `intent-eval-lab/000-docs/005-AT-DECR-isedc-v2-terminology-rename-2026-05-10.md` (DR-005)
  - `intent-eval-lab/000-docs/006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md` (Session 3, DR-006)
- **System brief:** `intent-eval-lab/000-docs/007-DR-BRIEF-intent-eval-platform-system-brief-2026-05-11.html`
- **Gap analysis:** `intent-eval-lab/000-docs/008-DR-GAPS-spec-vs-system-brief-2026-05-11.md`
- **FUTURE.md:** `intent-eval-lab/000-docs/FUTURE.md`
- **OTel temperature record:** `intent-eval-lab/000-docs/009-RR-INTL-otel-sig-genai-temperature.md`
- **intent-rollout-gate design doc:** `intent-rollout-gate/000-docs/001-DR-DESIGN-rollout-gate-architecture-...md`
- **Reusable ISEDC pattern:** `~/.claude/skills/exec-decision-council/SKILL.md` v1.0.0
- **Document Filing Standard v4.3:** `~/000-projects/002-command-bible/DOCUMENT-FILING-STANDARD-v3.0.md` (and successors)
- **Tracking bead:** `iel-5eo` (close with this DR as evidence)
- **Plane HQ:** LAB-6 (IEL-CONV-1) — update with comment linking to this DR
- **Tagline:** *"We create industries that don't exist — we think outside of the box's box."*
- **User-named product positioning:** *"Reliability infrastructure for agentic systems. Not chatbots. Not wrappers. Infrastructure."*

— Jeremy Longshore
intentsolutions.io
