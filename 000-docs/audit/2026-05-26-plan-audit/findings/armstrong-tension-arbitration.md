# Tension Arbitration — Joe Armstrong (thinker-canon seat)

**Date:** 2026-05-27
**Channeling:** Joe Armstrong
**Scope:** 4 cross-seat tensions from synthesis.md
**Lens:** Erlang/OTP — supervised concurrent processes; let it crash; the world is concurrent; make it work, make it work right, make it work fast.

---

## TENSION-1 — SkillVersion / SkillSnapshot

> "Things that are concurrent in the real world should be concurrent in the system."

A SkillSnapshot is a **value** — immutable, content-addressed, dead data on disk. A SkillVersion is a **process** — it has a lifecycle: proposed → evaluated → accepted → promoted → (possibly) rolled-back. These are categorically different things. Hickey wants them merged because their shape rhymes; Lamport wants a state machine bolted on; Torvalds wants one entity with a `kind` discriminator.

They're all partially right and all missing the OTP frame. The discriminator collapses the shape; the state machine names the lifecycle; but neither asks the load-bearing question: **what supervises a SkillVersion's lifecycle?** Who restarts a stuck `evaluating` version? Who reaps a `proposed` version that never got picked up? Who handles the `rolled_back → restored` transition when the previous version is itself in a degraded state?

**Arbitration:** KEEP THEM SEPARATE. SkillSnapshot is a value (no supervisor needed — it's just bytes). SkillVersion is a supervised process with an explicit state machine per Lamport. Add the supervisor (`RefinerSupervisor`?) as a first-class entity in the kernel. The architect's "no FK" is correct: lineage lives on SkillVersion, snapshot is referenced by content hash. If you can't name the supervisor, you don't understand the entity yet.

## TENSION-2 — Phase D

> "Let it crash."

Phase D as currently written is the worst possible posture. It's neither shipped (so we can't observe failure) nor killed (so we can't focus). "Deferred indefinitely at P3" is the anti-pattern: a process that's neither supervised nor terminated. In OTP terms, it's a zombie.

Two honest paths:

1. **Ship it and let it crash.** Define the failure boundary: "if the creator under-performs the bitter-lesson baseline by N%, auto-rollback to 'no skill emitted' and emit a loud signal." If you can articulate that boundary cleanly, ship it; if you can't, you don't have a product yet.
2. **Anti-goal it.** Kill the process. If a frontier model later changes the math, restart the process — restarting is cheap in OTP.

**Arbitration:** Cunningham's path. Convert to Blueprint A § 3 anti-goal until the let-it-crash boundary is acceptable to ship. Karpathy's quarterly re-measurement is a polling loop with no supervisor — it will be skipped. Process you won't run is decoration.

## TENSION-3 — Process discipline

> Seven concurrent processes with no observable failure signal and no recovery action are not disciplines. They are hopes.

The world is concurrent: the bd workspace, 5 sub-repos, 3 sync targets (bead/GH/Plane), CI, human writers — all writing concurrently. AC-12 tri-link doesn't fail; it _silently degrades_. That's the worst failure mode in any distributed system. Cunningham sees the accumulation; Hickey sees the place-orientation; both are right.

**Arbitration:** every discipline must answer two questions or be deleted: (1) what is the observable failure signal? (2) what is the automatic recovery action? Disciplines that can answer both stay and get supervised properly (CI gate that fails loudly + idempotent recovery). Disciplines that can't answer both get deleted from the plan and re-labeled "advisory." No middle ground. My guess: 2 of 7 survive. That's fine — 2 supervised processes beat 7 hopeful ones.

## TENSION-4 — Mechanism vs product

> Concurrent things should be concurrent in the system.

The eval set and the refiner mechanism are **independently evolving concurrent concerns**. The eval set is frozen at a kernel version; the refiner proposes against it. That decoupling is the product. IS sells THE GUARANTEE that the eval set is independent of whatever mechanism proposed the change being evaluated.

If AC-7 means what it says — mechanism swappable — then the eval-set guarantee IS the product and the mechanism is implementation detail. Define `RefinerStrategy` as the interface, ship two implementations, prove the swap works. Until then AC-7 is unearned.

**Arbitration:** the eval-set decoupling is the durable product surface. The mechanism is a swappable subordinate process. Make-it-work first (one strategy, end-to-end), make-it-work-right second (define interface + second strategy), make-it-work-fast never matters at this scale. Phase B owes the second strategy; until it lands, AC-7 stays in the plan as a TODO, not as a citation.

---

## VERDICT

| Tension                         | Arbitration                                                                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T1 — SkillVersion/SkillSnapshot | **KEEP SEPARATE.** SkillSnapshot is a value; SkillVersion is a supervised process with explicit state machine + named supervisor entity. No FK.         |
| T2 — Phase D                    | **KILL (anti-goal).** Let-it-crash boundary not articulable today; zombie process worse than terminated one. Restart cheap if reality changes.          |
| T3 — Process discipline         | **OBSERVABILITY-GATE.** Every discipline must name its failure signal + recovery action or be deleted. Likely 2 of 7 survive.                           |
| T4 — Mechanism/product          | **Eval-set decoupling IS the product.** Mechanism is swappable subordinate; define `RefinerStrategy` + ship second impl before AC-7 earns its citation. |

— Joe Armstrong (channeled)
2026-05-27
