# Thompson Tension Arbitration — Skill Refiner Plan Audit

**Seat:** Ken Thompson (thinker canon, tension arbitration)
**Date:** 2026-05-27
**Scope:** 4 cross-seat tensions surfaced in synthesis.md

---

## Bias declaration

I build things that work, then I make them simple. When in doubt, I use brute
force. I trust what I sign myself and very little else (see _Reflections on
Trusting Trust_). Do one thing well. Measure before you optimize. These are the
lenses I bring to all four tensions.

---

## T1 — SkillVersion / SkillSnapshot resolution

**Verdict: MERGE. One entity. Discriminator field.**

Two immutable, content-addressed, parent-pointered entities for one concept is
not a design — it's a backlog item that already shipped. Hickey is right; the
parenthetical "NOT a duplicate" in the plan is the smell.

Brute force: one entity, `kind: snapshot | refinement | revert | restore`.
Consumers query the discriminator. Lineage carried in `parent_version_id`.
Kleppmann's `version_kind` and Lamport's state machine fold into the
discriminator naturally — the state machine becomes a single switch over
`kind`, not two interacting types. The architect's "fully orthogonal" path
preserves the duplicate; reject it.

A kernel ships v0.3.0 in days, not weeks. If a real second concept emerges
later, split then — you'll know what to split on because you'll have data.
Splitting later is cheap; un-splitting two signed Rekor-anchored entities is
not.

## T2 — Phase D resolution

**Verdict: ANTI-GOAL until somebody writes the test.**

Premature optimization is the root of all evil — but the inverse is also true:
you can't defer what you haven't measured. "Frontier-model release triggers
re-open" is not a trigger; it's a vibe. What's the _test_ that says
"self-generated skills now clear the bar"? Eval set, threshold, sample size,
runtime. Until that test exists, Phase D is not deferred work — it's
unspecified work pretending to be deferred work.

Cunningham's Path A (Blueprint A anti-goal) is correct as the _current_ state.
Karpathy's quarterly re-measurement becomes operationally meaningful only once
someone writes the eval that the re-measurement runs against. Make writing
that eval the precondition for re-opening Phase D from anti-goal status. No
eval, no debate.

## T3 — Process discipline weight

**Verdict: Do one thing well — bd carries the link. Drop the other six.**

Seven parallel disciplines to keep three writable stores in sync (CONV-4) is
the same architectural error as T1: shipping more mechanism instead of less.
Unix philosophy: one tool, one job. Pick "every bead carries its own GH
issue URL in its notes; nothing else." Drop the doc-front-matter rule. Drop
the GH-body back-link rule. Drop the AC-12 tri-link verifier CI.

bd IS the source of truth. GH and Plane are projections. If they drift, fix
the projection, not the source. Cunningham wants the discipline simplified;
Hickey would eliminate AC-12 entirely. Both are right and they collapse to
the same answer once you commit to a single writer.

## T4 — Mechanism vs product

**Verdict: The eval IS the product. Sign your own snapshots or you don't
own the verdict.**

Trusting Trust applies cleanly here. If the eval set you grade against is
fetched, mirrored, or vendored from outside your trust boundary at refinement
time, the verdict is laundered through a chain you didn't author. The
Refiner library, the gate, the predicate URI — those are mechanism. The eval
set, signed by IS, anchored in IS-controlled Rekor, refreshed on an
IS-documented cadence — that's the product.

Implication for Huyen's F-CH-001 (eval-set lineage absent until Phase F):
F-CH-001 is not a Phase F item. It is the _first_ Phase A item. Without
signed, versioned, lineage-tracked eval sets, the rest of the platform signs
verdicts against an unauthenticated oracle.

---

## Verdict block

**T1:** MERGE — one entity, discriminator field, ship v0.3.0 fast.
**T2:** ANTI-GOAL — re-open gated on a written, runnable eval, not on vibes.
**T3:** ONE WRITER — bd is the source; GH/Plane are projections; drop the
other six disciplines.
**T4:** OWN THE EVAL SET — sign it, version it, refresh it; promote
F-CH-001 to Phase A.0 alongside the bitter-lesson baseline.

Bias toward simplicity-and-trust. Brute-force the schema. Measure before you
defer. One tool, one job. Sign what you grade against.

— Ken Thompson (channeled)
2026-05-27
