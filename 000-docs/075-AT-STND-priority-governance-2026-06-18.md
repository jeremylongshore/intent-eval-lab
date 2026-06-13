---
title: Priority Governance — the lattice that orders what gets built, evaluated, and shipped under a fixed bandwidth budget
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: DR-010 § 7 Q5 (primary-engagement off-the-top; bandwidth sequencing) + Blueprint A § 2.3 (governance routing)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — the constitution)
  - 010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md (DR-010 — sequencing + bandwidth gate)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E14
bead: bd_000-projects-ecpj
filing_standard: Document Filing Standard v4.3
related_docs:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — governance routing)
  - 014-DR-GLOS-canonical-glossary.md (routing / phase-lifecycle terminology)
  - 069-DR-STND-state-labeling-standard-2026-06-18.md (CURRENT/PLANNED/EXPERIMENTAL/DEFERRED/REJECTED scope labels)
  - 072-AT-ARCH-human-review-governance-2026-06-18.md (the review queue this lattice orders)
  - 073-AT-STND-economics-and-cost-governance-2026-06-18.md (the founder-hour budget priority spends against)
  - 074-AT-STND-optimizer-safety-model-2026-06-18.md (optimizer proposals sit low in the lattice)
related_drs:
  - 010-AT-DECR (DR-010 — § 7 Q5 sequencing; § 13.5 customer-signal-gate override)
  - 038-AT-DECR (bead naming standard — plain-English priority titles)
state_element_status: CURRENT
---

> **State label: NORMATIVE.** Binding priority doctrine. Unlike its three sibling
> doctrines, the mechanism here is `CURRENT`, not `PLANNED`: priority governance is
> *already* how work is ordered today (via beads + the three-layer mirror). This document
> writes down the lattice that the bead workspace already enforces in practice, so the
> ordering is legible and not re-derived per session.

# Priority Governance

**Beads:** `bd_000-projects-ecpj` (iel-E14d) under epic `bd_000-projects-14j` (iel-E14 —
operational doctrine bundle). GitHub: `jeremylongshore/intent-eval-lab#48`. Plane: LAB-46.

## 0. The scarce resource is founder-hours, and priority is how it is allocated

The Intent Eval Platform is built under a fixed, small bandwidth budget — ~3–5 hrs/wk
sole-prop, capped at +50/+66 founder-hours of widening over the 6-month journey (DR-010
§ 4, § 7 Q5; the cost side is `073-AT-STND` § 5). When the budget is fixed and the backlog
is not, *priority is the only lever that matters.* Every "yes" to one item is a "no,
later" to another. This doctrine fixes the **lattice** — the partial order — that decides
which "yes" comes first, so that the decision is principled and auditable rather than
driven by recency, by whoever asked last, or by which feature is most fun to build.

This is **not** a project-management tool spec. It is the *ordering policy* that the bead
workspace (the canonical source of truth, `~/000-projects/.beads/`) and its GitHub/Plane
mirrors enforce. It binds *how* priorities are assigned and *who* may reorder them.

This document **derives from and does not override** DR-010 or Blueprint A.

## 1. The priority lattice (top to bottom)

Work is ordered by the following lattice. Higher tiers are *absolutely* prior to lower
tiers — a lower-tier item never preempts a higher-tier item, no matter how loud, how
nearly-done, or how cheap.

| Tier | Class of work | Authority |
| --- | --- | --- |
| **P-TOP** | **The primary client engagement.** Off-the-top, on its own track, never drawn from the platform budget, never displaced by platform work. | DR-010 § 7 Q5 ("primary client engagement first priority preserved — runs on its own track, not displaced"); § 13.5 |
| **P0** | **Irreversible-surface unblockers + active revenue-client commitments.** One-way-door governance acts whose absence blocks signed evidence (predicate-URI/SPEC normative landings, kernel releases that gate consumers), plus the active revenue client's committed deliverables. | DR-010 § 7 Q3/Q5; Blueprint A § 2.1 (Evidence Bundle is the invariant everything federates around) |
| **P1** | **Foundation + cross-repo unblockers.** Work that multiple downstream beads depend on (kernel entities, the SAK schema pipeline, normative SPEC sections, the audit-harness supply-chain hardening that gates emission). | DR-010 § 7 Q5 sequencing; the dependency DAG in the bead workspace |
| **P2** | **Standalone deliverables + doctrine.** Self-contained docs, single-repo features, this doctrine bundle (iel-E14) — valuable but not blocking other work. | epic-level priority in the bead workspace |
| **P3** | **Deferred-until-signal work.** Items correctly waiting on a trigger condition (FUTURE.md entries, governance-scaling work deferred until a contributor-growth signal, Phase C deliverables). | FUTURE.md trigger conditions; DR-010 phase lifecycle |
| **P-LOW** | **Optimizer-proposed work.** Skill Refiner proposals (`074-AT-STND`) — admitted to the queue only after passing the accept predicate, and never above human-authored roadmap items. | DR-028; `074-AT-STND` § 5 |

### R1 — P-TOP is sacrosanct

The primary client engagement is **off-the-top.** Its founder-hours are never counted
against the +50/+66 platform-build cap (`073-AT-STND` R10), and platform work *never*
preempts it. This is the single hardest rule in the lattice: a P0 platform unblocker waits
behind a P-TOP engagement commitment, never the reverse. Per DR-010 § 13.5, this is true
regardless of customer-vs-internal framing — the engagement's priority is structural.

### R2 — Tiers are absolute, not weighted

The lattice is a **strict priority order across tiers**, not a weighted score. A nearly-
finished P2 doc does not jump ahead of a barely-started P1 unblocker because it is "almost
done." Sunk effort is not a priority input — that is the sunk-cost trap the CFO seat
flagged in DR-010 § 8. Within a tier, the dependency DAG and the trigger conditions order
items (§ 2).

## 2. Ordering *within* a tier

### R3 — Within a tier, dependencies and triggers decide

Inside a single tier, two rules order work:

1. **Dependency order** — a bead is not "ready" until its blockers close (the bead
   workspace's `bd ready` is the mechanical expression of this). An item whose dependencies
   are unmet is **not** preemptively prioritized just because it is desirable; it is
   *blocked*, which is a distinct state from *deprioritized.*
2. **Trigger satisfaction** — a P3 item whose FUTURE.md trigger has fired graduates into a
   tracked bead at its true tier; an item whose trigger has *not* fired stays in P3 no
   matter how interesting it is. Naming a deferred item does not reserve, prioritize, or
   schedule it (the same discipline PREDICATE-TYPES.md applies to DEFERRED/PROPOSED URIs).

### R4 — Scope-element labels track an item's readiness, not its priority

Per the State-Labeling Standard (`069-DR-STND`) and core-repo-boundaries
(`068-AT-STND`), an item carries a scope-element label — `CURRENT` / `PLANNED` /
`EXPERIMENTAL` / `DEFERRED` / `REJECTED`. These describe *maturity*, not *priority*: a
`PLANNED` item can be P1 (high priority, not yet built) and a `CURRENT` item can be P3 (in
production, low remaining work). The two vocabularies never collide (they label different
things — `069-DR-STND` § 1). A reader resolves "how important" from the lattice tier and
"how ready" from the scope label.

## 3. Who may assign and reorder priority

### R5 — Priority assignment routes through governance class

Changing the *lattice itself* (adding a tier, redefining P-TOP, changing the absolute-
ordering rule) is a **Class-1 ISEDC act** — it changes how the platform allocates its
scarcest resource. Assigning an *individual bead's* priority within the existing lattice is
a **Class-3 solo-maintainer act** (the acting head of board), recorded as the bead's
priority field and mirrored via `bd-sync`. Re-sequencing a *cross-repo wave* (deciding P1
foundation work order across repos) is a **Class-2 pair act** when it changes a published
roadmap commitment. Routing follows DR-010 § 7 Q6 and Blueprint A § 2.3.

### R6 — No stakeholder-volume override

Priority is **not** set by who asks most insistently or most recently. The lattice is the
authority; a request to jump the queue is evaluated against the lattice, not against the
requester's urgency. The "loudest stakeholder wins" failure mode is precisely what a
written lattice exists to prevent. The one structural exception is P-TOP, which is high not
because it is loud but because DR-010 made it structurally off-the-top.

## 4. Bandwidth-gated, not customer-signal-gated

### R7 — Priority spends bandwidth, and the gate is bandwidth

Per the DR-010 § 13.5 acting-head-of-board override, platform feature work is
**bandwidth-gated, not customer-signal-gated.** A P1/P2 platform item is sequenced by *do
we have the founder-hours under the cap* (`073-AT-STND` § 5), not by *will a customer pay
for it.* The platform is an internal tool built for the Intent Solutions practice and
shared as OSS by default; the 45k+ NPM following on `claude-code-plugins` is natural
distribution, not a priority input. The only paying-work tiers are P-TOP (the primary
engagement) and the active-revenue-client portion of P0 — and those are prioritized because
they are *commitments*, not because customer-signal gates the platform.

## 5. Relationship to the sibling doctrines

- **Human-review governance** (`072-AT-ARCH`) — when multiple HR-N items await
  adjudication, this lattice orders the reviewer's queue (`072-AT-ARCH` § 6). A production-
  pin optimizer escalation (HR-2) is ordered by the tier of the artifact it touches, not by
  the optimizer's eagerness.
- **Economics governance** (`073-AT-STND`) — the founder-hour budget is the resource this
  lattice allocates; the +50/+66 cap is the outer bound, and per-item founder-hour
  estimates (the `029-DR-BAND` precedent) feed the within-tier sequencing.
- **Optimizer safety model** (`074-AT-STND`) — optimizer-proposed work is P-LOW and never
  reorders the queue toward itself (`074-AT-STND` § 5; the optimizer cannot move its own
  gate, R7 there).

## 6. Anti-patterns — refuse on sight

- **Displacing P-TOP.** Letting any platform item — even a P0 irreversible-surface
  unblocker — preempt the primary client engagement (violates R1).
- **Weighted-score priority.** Treating the lattice as a weighted average where a high P2
  beats a low P1 (violates R2). Tiers are absolute.
- **Sunk-cost prioritization.** Jumping a nearly-finished item ahead of a higher-tier
  not-yet-started item because effort is already spent (violates R2; DR-010 § 8 sunk-cost
  trap).
- **Blocked-as-deprioritized confusion.** Treating a blocked item as low priority and
  filling its slot, when the right action is to close its blocker (violates R3). Blocked ≠
  deprioritized.
- **Triggering an untriggered defer.** Promoting a P3/FUTURE.md item before its trigger
  condition fires because it is interesting (violates R3).
- **Confusing maturity with priority.** Reading a `PLANNED` label as "low priority" or a
  `CURRENT` label as "high priority" (violates R4). Different vocabularies.
- **Loudest-stakeholder override.** Reordering the queue toward the most insistent
  requester instead of the lattice (violates R6).
- **Customer-signal priority gate.** Sequencing a platform item by "a customer will pay"
  rather than "we have bandwidth under the cap" (violates R7; DR-010 § 13.5).
- **Lattice change as a solo act.** Adding a tier or redefining P-TOP without a Class-1
  ISEDC act (violates R5).

## 7. Cross-references

- **DR-010** (`010-AT-DECR`) § 4 (bandwidth reality), § 7 Q5 (sequencing,
  primary-engagement off-the-top, +50/+66 cap), § 8 (sunk-cost trap), § 13.5
  (bandwidth-not-customer gate).
- **DR-038** (`038-AT-DECR`) — bead-naming standard (plain-English priority titles; the
  system ID is a command handle only).
- **Blueprint A** (`011-AT-ARCH`) § 2.1 (Evidence Bundle invariant; why P0/P1 unblockers
  exist), § 2.3 (governance routing).
- **Canonical glossary** (`014-DR-GLOS`) § 3 (routing), § 5 (Class-1/2/3, phase lifecycle).
- **State-Labeling Standard** (`069-DR-STND`) / **Core Repo Boundaries** (`068-AT-STND`) —
  scope-element labels (R4).
- **Siblings:** `072-AT-ARCH-human-review-governance` (queue ordering),
  `073-AT-STND-economics-and-cost-governance` (the budget), `074-AT-STND-optimizer-safety-model`
  (P-LOW optimizer work).

## 8. License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
