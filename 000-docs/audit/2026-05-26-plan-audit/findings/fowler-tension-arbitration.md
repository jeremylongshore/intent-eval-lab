# Martin Fowler — Tension Arbitration — 2026-05-27

Channeled as a thinker-canon seat. The lenses here are **Refactoring** (small reversible steps), **PoEAA** (layer ownership), **Microservices** (boundaries = team + cadence), **YAGNI / one-way door**, and **two-pizza process discipline**.

## TENSION-1 — SkillVersion / SkillSnapshot

**Fowler-canon invoked:** _"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."_ And from PoEAA: **be explicit about which layer owns what** — a Domain Model entity exists when it has identity, behavior, _and a lifecycle distinct from anything else_.

**Trade-off analysis:** Hickey's merge is the simplest legible thing. Architect's orthogonal-no-FK is the most refactorable thing (the FK is the irreversible commitment — once `@intentsolutions/core@0.3.0` ships with that FK signed into Rekor envelopes, you have walked through a one-way door per principle 4 of YAGNI). Kleppmann's discriminator is a _Refactoring_ move — same row shape, one field carries the variant, future split is cheap. Lamport's state machine is correct but premature; you can always _add_ a state machine to a discriminator field, you cannot easily _remove_ an FK from a signed kernel.

**Preferred resolution:** **discriminator** (Kleppmann's `version_kind: edit | revert | restore`), with SkillVersion as a logically separate entity but **no FK** to SkillSnapshot in the v0.3 kernel schema. Carry lineage entirely on `SkillVersion.parent_version_id`. If the cross-reference proves load-bearing in Phase B operational use, _then_ add the FK in v0.4 — that's a small reversible step. Adding an FK is a refactoring; removing one from a signed kernel is a migration.

**Why:** Avoids the one-way door. Preserves Hickey's spirit (one logical lineage chain) without forcing a premature merge. Honors PoEAA layer separation: the kernel owns identity + invariants; relational joins are a query-layer concern, not a schema-layer commitment.

## TENSION-2 — Phase D

**Fowler-canon invoked:** _"YAGNI"_ — but also _"the most expensive feature is the one you said yes to but didn't build, because it sits in the backlog accumulating context-switch tax forever."_

**Trade-off analysis:** Karpathy's quarterly + on-frontier-release trigger keeps optionality at the cost of permanent low-grade backlog noise. Cunningham's anti-goal upgrade is honest — it tells future readers "we considered this and chose not." "Deferred indefinitely at P3" is the worst of three worlds (Cunningham is right).

**Preferred resolution:** **anti-goal** (Cunningham's path). Move to Blueprint A § 3 as anti-goal § 3.8: "NOT a skill _creation_ sub-product." If frontier capability changes the math, that triggers a Class-1 ISEDC reopen per § 2.3 — same mechanism that handles every other anti-goal reversal. You don't need a separate quarterly bead for that; the standing quarterly ISEDC review (§ 2.3 cadence) already covers it.

**Why:** Anti-goals are reversible via DR. Quarterly re-eval triggers are process debt that compounds. The anti-goal IS the trigger mechanism — Karpathy's concern is already covered by the existing governance.

## TENSION-3 — Process discipline weight

**Fowler-canon invoked:** _"If it hurts, do it more often"_ — but the corollary is **"if it hurts and you're doing it manually seven times, automate or eliminate."** And from microservices: **process discipline boundaries should match the team that operates it** (two-pizza rule).

**Trade-off analysis:** Cunningham is correct that 7 parallel disciplines without a unifying abstraction is debt. Hickey is correct that AC-12 tri-link is place-oriented complexity. They're not in tension — they're the _same finding_ at different layers. The unifying observation: **three of the seven disciplines (PR-1 trilink, validate-trilink, bd-sync) are all enforcing the same invariant — "bead, GH issue, Plane issue carry each other's IDs."** That is ONE discipline operationalized three times.

**Preferred resolution:** **eliminate AC-12 as a separate AC; collapse the three trilink-related disciplines into one tool boundary (`bd-sync` is already that tool — make it the only writer).** Treat GH and Plane as projections (read-only views derived from bd state) per Hickey/CONV-4 remediation. The remaining 4 disciplines (escape-scan, partner-name-guard, spec-refresh, doc-filing) are independent and each has a clean automation home — keep them.

**Why:** One-pizza team running seven parallel manual disciplines is the failure mode. The two-pizza rule says: collapse the redundant ones, automate the rest, eliminate AC-12 as a load-bearing checkpoint. The discipline becomes invisible (good) rather than ceremonial (bad).

## TENSION-4 — Mechanism vs product

**Fowler-canon invoked:** _"The interface is the contract; the implementation is an implementation detail."_ And from microservices: **what you sell is the boundary, not the binary.**

**Trade-off analysis:** Brand framing ("Test → Improve → Ship") implies the mechanism IS the product, which is what marketers naturally do. AC-7 says the acceptance gate (the predicate, the evidence, the signed verdict) is the durable contribution. These are reconcilable _if you are precise about what "product" means at which layer_. The mechanism is the _current implementation_ of the eval-guided improvement contract. The contract is what gets attested, versioned, and shipped via predicate URI `skill-refiner-pass/v1`.

**Preferred resolution:** **mechanism-swappable, eval-is-product.** What IS sells (and what enters the kernel) is the **`skill-refiner-pass/v1` predicate contract** — the durable, signed, replayable statement "this skill improved on the pinned dimensions per this acceptance gate." The "Skill Refiner" brand can stay as the _reference implementation_ in the 3-product framing, but Blueprint A § 1.2 principle 10 (schema-is-canon) already says the contract is canonical, not the implementation. AC-7 wins; the brand framing needs a footnote: "Refiner is one implementation of the eval-guided-improvement contract; the contract is the durable artifact."

**Why:** This is the platform's deepest principle (deterministic-evidence-as-product, mechanism interchangeable) applied recursively to the Refiner itself. If you sell the mechanism, you've bound IS to maintain that specific mechanism forever. If you sell the contract, mechanisms compete and the best one wins — which is the bitter-lesson-resistant posture Karpathy is pointing at.

## One-line verdict per tension

- **T1:** discriminator
- **T2:** anti-goal
- **T3:** eliminate-AC-12
- **T4:** mechanism-swappable-eval-is-product

— Martin Fowler (channeled), 2026-05-27
