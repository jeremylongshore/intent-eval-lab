# Gregg Seat — Tension Arbitration (Skill Refiner Plan Audit)

**Plan under audit:** `027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1)
**Seat:** Brendan Gregg (channeled) — observability / production-debuggability lens
**Date:** 2026-05-27

Brief pack: 00, 05 (Blueprint B), 09 (SkillsBench), synthesis. Lens: *"If you can't measure it, you can't manage it."* One question per tension — **what's the metric, what's the span, what's the failure surface?** Architectural elegance with no observability is theater.

---

## TENSION-1 — SkillVersion / SkillSnapshot shape

Other seats argued semantics. None asked: *which shape produces the cleanest OTel span tree under `9pi3` semconv pin?* Blueprint B § 1.1 mandates OTel-native observability; every state transition emits an event. USE-method on the alternatives:

- **Merge** — one entity, one attribute namespace. Lowest cardinality, **Saturation**, **Error** surface.
- **Orthogonal-no-FK** — two entities, no relation. Lineage reconstructed at query time. **Error** explodes — missing pointer is silent (no constraint fires).
- **Discriminator (Kleppmann)** — single entity, `version_kind` field. Same surface as Merge plus `version_kind=revert` becomes queryable → trivial "rollback rate per skill per week" dashboard. Directly addresses CONV-2 rollback causality.
- **State machine (Lamport)** — a state attribute on the merged entity gives you the same.

**Verdict:** **discriminator**. Merge-shape with the lineage attribute CONV-2 demands.

---

## TENSION-2 — Phase D defer-vs-anti-goal

Karpathy wants quarterly + on-release re-test. Cunningham wants anti-goal. Both argued *trigger shape*. Neither named the **trigger metric**. Falsifiable triggers need observable signals:

1. **SkillsBench reproduction lift on self-generated skills crosses threshold** — re-run held-out equivalent on each frontier release; open Phase D when self-gen lift > `+8pp` (half the curated +16.2pp).
2. **Internal `skill-refiner-pass/v1` acceptance rate, from-scratch vs from-curated, exceeds parity** — self-instrumenting via Refiner evidence log.

Karpathy's cadence is right *shape*; without a metric it's a calendar reminder. Cunningham's anti-goal is right *only if* no measurable signal exists — but it does. SkillsBench gives unit and benchmark; eval-set lineage is already Phase A.

**Verdict:** **quarterly-trigger** with metric: "Phase D opens when self-gen lift > +8pp on the kernel-pinned eval set on any frontier release, OR internal acceptance rate exceeds parity, whichever fires first."

---

## TENSION-3 — Process discipline (simplify vs eliminate AC-12)

Quantify. AC-12 tri-link validation ~30s per PR × 7 disciplines = 3.5 min/PR. Across ~283 child beads = ~16 hours CI time before any code lands. That's the **Utilization** number nobody computed.

Worse: when AC-12 fires red, the root cause spans 3 writers (bd, GH, Plane). Flame-graph that — you can't, no shared trace context. Debugging takes 10× the CI minutes.

Hickey's eliminate is right *for the wrong reason* (place-oriented). I say untraceable. Cunningham's simplify-to-1 is a half-measure — the abstraction still writes to 3 places.

**Verdict:** **eliminate-AC-12**. Make bd the linearizable writer (CONV-4 path b: GH/Plane as read-only projections). One writer = one span = one debuggable failure mode.

---

## TENSION-4 — Mechanism-is-product vs swappable

Karpathy F-AK-002 nailed the missing interface. My addition: *what customer-observable metric does the Refiner move?* If it's "SKILL.md quality score," that's the Refiner marking its own homework — not customer-observable.

The only customer-observable metric is **downstream eval-set pass-rate when the refined SKILL.md is consumed by a real workflow**. Identical whether mechanism is multi-pass propose/apply or one-shot in-context. The mechanism is invisible to the metric that matters.

Dispositive. If the mechanism is invisible to the customer-observable signal, the mechanism is not the product — the **eval+gate** is. Ship Karpathy's `RefinerStrategy` interface; expose `refiner.strategy.id` as a span attribute; A/B in production; let the metric pick the winner.

**Verdict:** **mechanism-swappable-eval-is-product**.

---

## One-line verdict block

```
T1: discriminator
T2: quarterly-trigger
T3: eliminate-AC-12
T4: mechanism-swappable-eval-is-product
```

— Brendan Gregg (channeled)
2026-05-27
