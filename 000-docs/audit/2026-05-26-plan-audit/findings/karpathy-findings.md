# Karpathy Seat — Plan Audit Findings

**Plan under audit:** `027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1)
**Seat:** Andrej Karpathy (channeled)
**Primary axes:** GAPS, SCOPE INTEGRITY
**Date:** 2026-05-27

I have read brief-pack docs 00, 09, 10. My job here is not to make this plan better — it is to find what is wrong with it. Six findings, ordered by how badly they would embarrass the seat to leave unflagged.

---

## F-AK-001 [P0] [GAPS] — The null-hypothesis baseline is named in the plan's own sample-finding section but never inserted into the Phase A roadmap

**Plan section quoted (verbatim):** § 12 "Sample findings (illustrative)" line 1429:

> "Proposed remediation: Insert Phase A.7 'Bitter-lesson baseline' — run eval set against un-refined skill with naive in-context augmentation. If lift > 70% of projected Phase B lift, descope Phase B's iterative engine."

This appears as an illustrative finding the plan _anticipates_ the panel will produce. It is **not** in § 4 Phase A's deliverables, build order (steps 1-8), or exit criteria. There is no Phase A.7. There is no naive-baseline run. The plan budgets ~1 week for Phase A and ~2 weeks for Phase B and proceeds straight to building the bounded-edit propose/accept loop without ever asking whether the loop beats the trivial alternative.

**Invoked Karpathy position (verbatim where canonical):** _"Evals are everything."_ The eval set is the product. Before you build a multi-stage refinement scaffold, you run the eval set against the cheapest possible mechanism and measure. The cheapest mechanism here is: take the SKILL.md, paste it into Opus 4.7 with the held-out eval items as in-context examples, ask for one improved SKILL.md, score it. One model call. No `propose()`, no `apply()`, no rejected-edit buffer, no 3-layer hooks, no `@j-rig/refiner-core` package split. If that single call captures the bulk of the available lift, every line of Phase B code is dead on arrival.

**Why this is P0 and not P1 (as the plan's own preview tagged it):** the entire Phase A build order (§ 4 lines 362-372) and Phase B plugin shape (§ 4 lines 387-422) is downstream of the assumption that the multi-pass mechanism beats one-shot in-context. With the null hypothesis untested, Phases A+B are speculative engineering against an unmeasured baseline. That is the textbook bitter-lesson trap.

**Remediation (operational, not aspirational):**

1. Move the sample-finding F-AK-001 remediation into Phase A as a **first deliverable, not a seventh**: `Phase A.0 — null-hypothesis baseline`. Owner: same as `bootstrap()`. Output: a ScoreRecord for `(SKILL.md, naive-Opus-one-shot-in-context, held-out-eval-set)` for the demo skill, committed to the event log before any propose/accept code is written.
2. Add a **descope gate** to Phase B exit criteria: "If Phase A.0 baseline captures ≥ 70% of Phase B's measured lift on the demo skill, Phase B's iterative engine is descoped and the plan revises before continuing."
3. The descope gate is a hard fork in the plan, not a soft note. v5 must show what the alternative path looks like.

---

## F-AK-002 [P0] [SCOPE INTEGRITY] — AC-7 asserts "the mechanism is swappable" but the plan defines no swap interface, no second mechanism, and no swap exercise

**Plan section quoted (verbatim):** § 3 AC-7:

> "The acceptance gate is the durable contribution; the refiner mechanism is swappable (Karpathy bitter-lesson check). When frontier-native skill refinement arrives, you keep the harness + gate; throw away the propose() internals."

**Invoked Karpathy position:** _"Pre-training is the new compiling."_ If the seat's name is going to be invoked to launder the architectural claim that the mechanism is swappable, the plan owes the seat a swap interface. There is none. § 4 Phase A's type signature (lines 348-352) hard-codes `propose(skillDoc, scoredRollouts, refinerModel?)` as the sole entry point. There is no `RefinerStrategy` interface. There is no second strategy (e.g., a `OneShotInContextStrategy` to serve as both the null-hypothesis baseline from F-AK-001 _and_ the swap proof-of-concept). The "swap" is a marketing promise, not a contract.

**Why "swappable" without an interface is worse than not claiming swappability at all:** the claim creates a false sense of bitter-lesson safety. When the frontier model release lands, the team will discover the propose/apply/accept call graph has assumptions baked in — score-shape, edit-grammar coupling, rejected-buffer semantics — that prevent a clean swap. The work-to-swap will be a rewrite, not a swap. The honest version of AC-7 either ships the interface now or admits the mechanism is the contract.

**Remediation:**

1. Phase A ships a `RefinerStrategy` interface (or whatever the IS naming is) with the propose+accept contract behind it. The default strategy is `BoundedEditStrategy` (current plan). Mandatory second strategy: `NaiveInContextStrategy` — same interface, one model call, no edit ops. This second strategy is the F-AK-001 null-hypothesis baseline _and_ the AC-7 swap proof.
2. Phase A exit criteria add: "Both `BoundedEditStrategy` and `NaiveInContextStrategy` implementations pass the same Phase A acceptance test against the demo skill, demonstrating the interface is actually swappable, not nominally swappable."
3. The plan's marketing line in AC-7 stops being a forward-looking promise and starts being a present-tense fact.

---

## F-AK-003 [P0] [GAPS] — Phase D is "deferred indefinitely" with no quarterly bitter-lesson re-evaluation trigger; this is exactly the wrong shape for the risk

**Plan section quoted (verbatim):** § 4 Phase D and § 2 line 100:

> "Creator sub-product (would generate NEW skills from scratch): DEFERRED INDEFINITELY at P3. SkillsBench evidence: self-generated skills underperform no-skill baseline. Re-open trigger: (a) external work demonstrates the bar can be cleared OR (b) a partner explicitly asks AND accepts the risk profile."

Brief-pack doc 09 § "Action items for Plan Audit panel" — assigned-to-this-seat:

> "Karpathy seat — the 'self-generated provides no benefit' finding is a bitter-lesson alarm for Phase D timing. Phase D deferral should be re-evaluated each frontier-model release."

**Invoked Karpathy position:** the SkillsBench finding (`+16.2pp curated, −1.3pp / "no benefit" self-generated`) is a **2026-02-13 measurement against then-current models**. The bitter lesson says: that delta is the variable most likely to shrink toward zero, and the most likely event to shrink it is the next frontier model release — not "external work demonstrates the bar can be cleared" and certainly not "a partner explicitly asks." Both of the plan's stated re-open triggers are downstream signals; the upstream signal is _model capability bump_, and the plan is silent on it.

"Deferred indefinitely" is the correct status; "deferred indefinitely with no scheduled re-measurement" is not. The framing implicitly bets that nothing changes upstream — exactly the bet the bitter lesson tells you not to take.

**Why this is P0 and not P1:** it is the cheapest possible fix (a calendar entry + a tiny re-measurement run) and the highest-leverage hedge in the plan. If you ratify the plan as written, you will not look at Phase D again until a partner asks for it, which is a _demand signal_ selecting for whether someone wants this — not a _capability signal_ telling you whether the bitter-lesson surface has shifted.

**Remediation:**

1. Add a **quarterly re-measurement** of the SkillsBench self-generated delta against the then-current frontier model from each major lab (Anthropic, OpenAI, Google). Owner: acting CTO. Output: bd memory per the trigger schedule already drafted in § 3.5 PR-4 line 271 ("Frontier model release shifts the bitter-lesson surface (Karpathy concern)") — that memory trigger exists in the plan but is reactive (fires when the seat sees the effect), not proactive (fires on a clock).
2. Make the trigger event-driven AND time-driven: re-measure on (a) each frontier release from a major lab, AND (b) quarterly regardless. The OR-with-clock disjunction is doing the load-bearing work — pure event-driven leaks because Claude may not notice a release for weeks.
3. Phase D's "Re-open trigger" list grows from 2 to 3: (a) external work, (b) partner asks, **(c) quarterly re-measurement shows self-generated delta has narrowed by ≥ X pp**.

---

## F-AK-004 [P1] [SCOPE INTEGRITY] — "Skill Refiner mechanism is what we sell" framing contradicts AC-7's "mechanism is swappable" framing; the plan does not pick

**Plan section quoted (verbatim):** § 2 Product structure lines 80-88 positions the Skill Refiner as the middle product in a "3-product Intent Solutions agent-rig stack" — i.e. the mechanism _is_ the product. AC-7 (§ 3) says the mechanism is throwaway. § 13 line 1257 lists Phase F triggers in terms of "active SkillVersion records" — i.e. the mechanism's output is the success metric.

**Invoked Karpathy position:** _"Evals are everything. The mechanism is swappable."_ You can sell the eval set, or you can sell the mechanism, but you cannot sell both with internal consistency. If the eval set is the durable contribution (AC-7) then the product positioning should be the eval set + the harness + the predicate URI — not the propose/accept loop. The current positioning treats "Skill Refiner" as a productized loop, which means a frontier-native replacement obviates the product, not just the internals.

**Why this matters now (P1 not P0):** this contradiction is recoverable through positioning copy and does not block Phase A code. But Phase E (Evidence report production) and Phase F (cross-vendor distribution) inherit the contradiction. The Hugo template and the report's hero-section design (§ 4 Phase E.2 lines 565-572) lean on "look at the score delta" — which is mechanism output, not eval-set value. When the mechanism becomes obsolete the report's value framing dies with it.

**Remediation:**

1. Decide before Phase E ships: is the durable product the **eval-set + harness + predicate URI** (Karpathy-consistent), or the **propose/accept loop with branded "Skill Refiner" wrapper** (mechanism-centric)?
2. If the former: rewrite the Phase E.2 HTML projection to lead with the held-out eval set's properties (size, diversity, hash, refresh cadence) and treat the score delta as a footnote. Marketing copy follows.
3. If the latter: drop AC-7 and stop invoking the bitter-lesson check in the plan. The seat will not lend its name to both framings.

---

## F-AK-005 [P1] [GAPS] — "Evals are everything" but the eval set's own quality has no eval

**Plan section quoted (verbatim):** § 4 Phase A line 346:

> "declare function bootstrap(skillDoc: SkillDoc): EvalSet;"

§ 4 Phase E.1 line 510:

> "Eval set composition — source: synthetic / harvested / golden / hybrid; size: N items; diversity: stratified by ...; eval_set_hash + storage location"

**Invoked Karpathy position:** the eval set IS the product (per AC-7 and the seat's canonical position). The plan treats the eval set as plumbing — bootstrap produces an EvalSet, score consumes one, the Evidence Report cites a hash. **There is no eval of the eval set.** No coverage check (does this set exercise the SKILL.md surface area), no adversarial robustness check (do near-paraphrases of eval items produce the same verdict), no leakage check (are eval items downstream-distinguishable from synthetic ones), no calibration check (does a known-broken skill score worse than a known-good one).

Brief-pack doc 09 already flags the risk-corner: SkillsBench measured **16/84 tasks regressing even with curated skills** — a ~19% per-task failure rate. If the eval set selects for the wrong 81 tasks, the strict-improvement gate will accept refinements that regress on the 3 tasks that actually matter to the partner. The plan does not address this.

**Remediation:**

1. Add an `eval()` operation in `@j-rig/refiner-core` alongside `bootstrap()`: takes an EvalSet, returns an EvalSetQualityRecord with coverage / adversarial / leakage / calibration dimensions. This is the SkillsBench-aware quality gate **on the eval set itself**.
2. Phase A.0 (the F-AK-001 null-hypothesis baseline) and every subsequent score-delta claim is conditioned on the EvalSetQualityRecord meeting a published floor. Sets below the floor produce a `confidence_tier: alpha` SkillVersion record at most.
3. The Evidence Report (§ 4 Phase E.1) adds an "Eval-set quality" section before the "Score trajectory" section. Score trajectory without eval-set quality is theater.

---

## F-AK-006 [P2] [SCOPE INTEGRITY] — The "load-bearing" −1.3pp figure is over-specific to the abstract and the plan's IP-defense rests on it

**Plan section quoted (verbatim):** § Context line 58 quotes:

> "Self-generated Skills provide negligible or negative benefit … models achieve −1.3pp on average compared to the no-Skills baseline"

Brief-pack doc 09 § "Discrepancy with Plan 027":

> "Self-generated Skills provide no benefit on average … the plan's load-bearing framing should soften to 'no benefit on average' if the −1.3pp cannot be substantiated post-full-PDF-fetch."

**Invoked Karpathy position:** _"Test the null hypothesis."_ The plan's IP-defense for `claude-code-plugins`'s 30+ human-curated skills is built on a number that the brief-pack itself flags as not-found-in-abstract. That is a cite-to-vibe pattern. Either the −1.3pp is in the paper body (in which case § 13 Step 0 must surface and pin it before Phase A claim) or it is not (in which case the plan's framing is over-specific and brittle to a fact-check).

This is P2 not P0 because the higher-order argument (self-generated < curated) does survive even on the abstract's softer "no benefit on average" framing. But it is exactly the kind of detail a frontier model release announcement could cite-and-disprove in a way that costs Intent Solutions credibility on a public surface.

**Remediation:**

1. § 13 Step 0 must produce a verbatim pin of either the −1.3pp number or the actual paper-body language, with page citation, before Phase A claim. Lamport seat's tracking item from doc 09 line 62 covers this; the Karpathy seat agrees and treats it as a hard pre-claim gate.
2. If the −1.3pp does not survive the full-PDF fetch, every place the plan cites it (§ Context line 58 + 60, AC-7 reasoning, Phase D rationale, § 8 Risk row line 1231) gets a one-line edit to "no benefit on average per SkillsBench abstract."

---

VERDICT: AMEND
