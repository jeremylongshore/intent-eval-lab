---
title: Prose↔schema reconciliation liveness — the ≤ 5-business-day escalation SLA
date: 2026-06-20
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Blueprint A § 2.3 (DR-010 three-class governance routing)
inherits_from:
  - 033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md (§ 14.16.2 — the SLA this spec normatively expands)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: 9k5h (GH intent-eval-lab#114 — make the kernel the SSoT, continuously spec-compliant)
bead: bd_000-projects-a5l6
filing_standard: Document Filing Standard v4.3
closes_finding: F-LL-005 (prose↔schema reconciliation liveness)
related_docs:
  - 045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md (SSoT declaration + continuity machinery)
  - 054-AT-SPEC-lineage-log-and-derived-coverage-map-2026-06-12.md (lineage log + outstanding-trigger count this SLA reads)
  - 063-AT-SPEC-leading-indicator-watcher-2026-06-12.md (sibling liveness watcher — the bitter-lesson STOP trigger)
  - 072-AT-ARCH-human-review-governance-2026-06-18.md (HR triggers + read-only review surface the day-5 retro consumes)
  - 075-AT-STND-priority-governance-2026-06-18.md (P0 placement of an open reconciliation)
related_drs:
  - 010-AT-DECR (DR-010 — three-class governance routing; ISEDC Class-2 session class)
  - 044-AT-DECR (Session 8 — SAK charter; governance owners the escalation routes to)
---

> **State label: NORMATIVE.** Binding on the Spec Authority Kernel (SAK)
> prose↔schema reconciliation flow per Blueprint A § 2.3. Normatively expands
> the ≤ 5-business-day SLA sketched in plan 033 § 14.16.2 (F-LL-005). The
> machinery it governs (spec-drift watch, prose-anchor parser, lineage log)
> already exists; this spec defines the **liveness contract** layered over it.

# Prose↔schema reconciliation liveness — the ≤ 5-business-day escalation SLA

When the kernel's prose source of truth (the 6767-h master skills spec) and the
machine-readable schema authority disagree — a coverage-map entry cites a 6767-h
section that no longer exists, a `diverge` event's convergence trigger fires
upstream, or a fetch surface goes materially dark — the disagreement is **drift**,
and drift left unreconciled is how a "single source of truth" silently becomes
two. This spec sets the **liveness bound** on closing that gap: a reconciliation
MUST land within **5 business days** of detection, with mechanically-defined
escalation at day 1 (auto-PR) and day 5 (ISEDC Class-2 retrospective).

It is the **prose-side sibling** of the leading-indicator watcher
(`063-AT-SPEC`). Both answer "has the world moved underneath the kernel?" — 063
answers the strategic question (_should the SAK stop investing and cut over to
upstream?_), this spec answers the operational one (_the prose and the schema
disagree right now; how fast must that be reconciled, and what happens if it
isn't?_). They share the same deterministic detection backbone (the four-layer
spec-drift machinery) and the same escalation venue (ISEDC Class-2), but trip on
different conditions and carry different verdicts.

## 1. The hole this closes (F-LL-005)

The four-layer spec-drift watcher (`spec-drift-watch.yml` + `spec-drift-check.sh`

- `spec-projection-diff.py` + `watcher-liveness.py`) and the prose-anchor parser
  (`prose-anchor-validity.yml`, plan 033 § 14.16.1) **detect** prose↔schema drift
  and open a reconciliation issue/PR. The lineage log (`054-AT-SPEC`) **records**
  every adopt/diverge/converge/snapshot/degrade event and derives a coverage map
  carrying a `convergence_triggers_outstanding` count per surface.

What none of them did: bound **how long a detected, recorded drift may remain
open**. Detection without a deadline lets a RED gate become wallpaper — a
permanently-failing check the team learns to ignore, the exact failure mode the
watcher-liveness P0 fixes were written to prevent on the _fetch_ side (Gregg's
"fail silent-green"). F-LL-005 names the symmetric _reconciliation_-side risk:
the gate fires loud, and then nothing makes the loudness expire into action. This
spec is the timer.

## 2. What counts as a reconciliation-clock start (the trigger set)

The 5-business-day clock starts on the **first scheduled-run detection** of any
of the following. Each is already emitted by existing machinery; this spec only
names which ones arm the SLA timer.

| #   | Trigger                                                                                | Detected by                                  | Lineage signal                                                                 |
| --- | -------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------ |
| T1  | A coverage-map entry cites a 6767-h section that no longer exists (prose-anchor break) | `prose-anchor-validity.yml` (§ 14.16.1)      | n/a (parser-side; opens a reconciliation PR directly)                          |
| T2  | A recorded `diverge` event's convergence trigger is observed upstream                  | spec-drift watch field-diff + human append   | a `convergence-trigger-fired` is now **due** (raises `…_outstanding` mismatch) |
| T3  | The normative SHAPE of an adopted surface changed (field added/removed/retyped)        | `spec-projection-diff.py` (field-level diff) | a `snapshot-updated` event lands; coverage map regenerates                     |
| T4  | An adopted surface is **materially** degraded (`fetch_error_streak >= 3`)              | `watcher-liveness.py`                        | a `fetch-degraded` event (the materiality roll-up, 054 event vocabulary)       |

**Not** clock-starters (deliberately, to protect the flake budget): a single
transient fetch error (tolerated by watcher-liveness), a prose change still inside
the 7-day PENDING disposition window (063 § flake budget), or a byte-hash drift
with no field-level SHAPE change. Only a **clean, persistent, materially-relevant**
detection arms the timer — mirroring the "only FETCH_OK feeds disposition" rule
the rest of the SAK machinery already enforces.

## 3. The SLA — ≤ 5 business days, with mechanical escalation

The bound from plan 033 § 14.16.2, made normative and given explicit owners and a
business-day definition. **Business day** = a UTC weekday (Mon–Fri), excluding
Sat/Sun. The clock counts elapsed business days since the detecting scheduled run;
holidays are NOT excluded (a sole-proprietor cadence does not maintain a holiday
calendar — the bound is deliberately conservative, not generous).

| Business day | Stage               | Required action                                                                                                                                   | Owner (per § 14.12 + 044-AT-DECR)                 |
| ------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Day 1**    | Auto-PR             | The detecting workflow opens (or re-surfaces, deduped by title) a `[reconciliation]` PR carrying the drift description + the affected subject.    | machinery (no human in the loop)                  |
| Days 1–3     | Resolve             | The editor resolves: CTO for kernel-schema changes, CCP-editorial for prose/6767-h changes. Resolution = a merged reconciliation commit.          | CTO (kernel) / CCP-editorial (prose)              |
| Day 4        | Escalate            | If unresolved: escalate to GC (when the 6767-h change carries IP implications) **or** the governance triple (otherwise).                          | GC / governance triple                            |
| **Day 5**    | ISEDC Class-2 retro | If still unresolved, an **ISEDC Class-2 retrospective** session is triggered (drift root-cause + process gap, per the Class-2 routing in DR-010). | acting head of board convenes; 7-seat adversarial |
| Day > 5      | Block               | CI is BLOCKED on the affected repository until reconciled — a force-rebase against the affected files fails. (Plan 033 § 14.16.2 final bullet.)   | machinery (no human in the loop)                  |

**Day-1 auto-PR — wiring.** The day-1 step is NOT new machinery. The existing
detectors already open a deduped reconciliation issue/PR on a fresh hit (063
§ "Side effects"; `spec-drift-watch.yml` side-effect #3; the prose-anchor gate's
RED). This spec **names** that side effect as the SLA's day-1 obligation and
requires the PR/issue body to carry: (a) the trigger # from § 2, (b) the affected
`(upstream_identity, subject)` key from the lineage log, and (c) the
`since` timestamp the clock counts from. No detector emits a _new_ artifact for
this SLA — the SLA reads the artifacts that already exist.

**Day-5 retro — what it is.** The ISEDC Class-2 retrospective is the SAME session
class the leading-indicator watcher's `RETRO` verdict routes to (063 disposition
matrix) and that the post-flip-regression rollback path opens (033 § 14.4
rollback). A Class-2 session is process/operational scope (not a Class-1
re-charter): it asks _why did this drift sit 5 business days unreconciled, and
what closes the gap?_ — root cause + a remediation, recorded as an `AT-DECR`. It
does NOT, by itself, change the schema; a schema change still routes through the
normal authoring-amendment path.

## 4. Relationship to the sibling watcher (063-AT-SPEC) — the explicit cross-link

| Axis              | This spec (090 — reconciliation liveness)                                        | 063-AT-SPEC (leading-indicator watcher)                           |
| ----------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Question answered | The prose and the schema disagree NOW — how fast must it be reconciled?          | Has Anthropic shipped a signal the SAK should STOP and cut over?  |
| Trigger condition | prose-anchor break / convergence trigger fired / SHAPE change / degraded surface | one of 12 named bitter-lesson indicators firing                   |
| Cadence           | continuous (every scheduled drift run; SLA clock per detection)                  | daily cron; 7-day prose disposition window                        |
| Verdict surface   | reconcile-within-5-days → block on day > 5                                       | CONTINUE / NOTE / RETRO / PAUSE / STOP disposition matrix         |
| Shared venue      | **ISEDC Class-2 retrospective** (day 5)                                          | **ISEDC Class-2 retrospective** (`RETRO` verdict)                 |
| Shared backbone   | the four-layer deterministic spec-drift machinery; FETCH_OK-only feeds           | the same four-layer machinery + typed fetch-failure posture (052) |

The two are deliberately distinct documents because their **verdicts and
deadlines** differ: a reconciliation has a hard 5-business-day SLA that ends in
_blocking CI_; a leading indicator has a graduated CONTINUE→STOP disposition with
no per-indicator deadline. Conflating them would force one timer onto two
different decision shapes. They cross-reference here so a future reader lands on
both halves of "the kernel's liveness against upstream."

## 5. Stale-reconciliation detector (OPTIONAL — informative, NOT a CI gate)

The closeable deliverable is the SLA above (§ 3). This section specifies an
**optional, advisory** detector that makes the SLA _observable_ between scheduled
drift runs by reading the lineage outstanding-trigger count directly, rather than
waiting for the next detector pass to re-surface a RED gate.

`scripts/reconciliation-liveness.py` (stub shipped with this spec) reads the
DERIVED `specs/lineage/coverage-map.json` (the projection contract from
`054-AT-SPEC` § "Projection contract") and reports, per surface:

- `convergence_triggers_outstanding` — the count of `diverge` events with no
  matching later `convergence-trigger-fired`. A nonzero count is the standing
  reconciliation backlog.
- For each `divergences_outstanding[]` entry, the **business days outstanding**
  since its `since` timestamp, classified against the § 3 SLA bands
  (`OK` ≤ 3 · `ESCALATE` 4 · `RETRO-DUE` ≥ 5).

**Posture (deliberate, per IEP review-gate policy).** The detector is:

- **read-only** — it never edits the lineage log, the coverage map, or any
  kernel/schema file. It reads the derived projection and prints a verdict.
- **advisory** — NOT wired into `ci.yml`'s required `Validate specs and docs`
  job, NOT a branch-protection gate. Wiring a new business-day timer as a
  _required_ check would make CI fail on a calendar boundary unrelated to the
  PR's diff — exactly the path-filtered/time-coupled footgun the doc-quality and
  required-check posture comments warn against. The SLA's _blocking_ obligation
  (day > 5) lives in the existing reconciliation gate, not here.
- **self-contained** — it ships an offline, deterministic `--self-test` (the
  repo-wide convention: every script in `scripts/` proves its behavior on
  fixtures with no network), so it is not dead code under the escape-scan even
  though it is unwired. Promotion from advisory to a gate is a future,
  separately-governed step (it would require its own self-test in CI and a
  governance-routed decision), explicitly out of scope for F-LL-005.

The detector exists to answer "what's my standing reconciliation backlog, and is
any of it past SLA?" on demand — a manual `python3 scripts/reconciliation-liveness.py`
— not to add a new failure surface.

## 6. Tracking checklist (per-reconciliation)

When a § 2 trigger arms the clock, the day-1 auto-PR body SHOULD carry this
checklist so the SLA state is legible in the PR itself (markdown task list — the
PR author or owner checks boxes as stages clear):

```text
- [ ] Day 1 — auto-PR open; trigger #, (upstream_identity, subject), since-timestamp recorded
- [ ] Days 1–3 — editor resolves (CTO=kernel / CCP-editorial=prose) → reconciliation commit merged
- [ ] Day 4 — IF unresolved: escalated to GC (IP) or governance triple
- [ ] Day 5 — IF unresolved: ISEDC Class-2 retrospective convened; AT-DECR opened
- [ ] Reconciled — lineage `convergence-trigger-fired` appended (T2) / snapshot promoted (T3) / surface restored (T4); coverage map regenerated
```

The final box closing is the SLA satisfaction signal: the corresponding
`…_outstanding` count drops, and the next coverage-map regeneration reflects it.

## 7. Non-goals

- **This spec does not introduce a new event type.** The five lineage event
  types (`054-AT-SPEC`) are sufficient; the SLA reads them, it does not extend
  the vocabulary.
- **This spec does not move the day > 5 blocking gate.** That obligation stays
  where plan 033 § 14.16.2 put it (the reconciliation gate blocks CI on the
  affected repo). § 5's detector is advisory and separate.
- **This spec does not change schema-authority routing.** A reconciliation that
  requires a schema change still routes through the normal authoring-amendment
  path; the day-5 retro produces a process Decision Record, not a schema bump.

## 8. Authority chain

Plan 033 § 14.16.2 (the SLA sketch + F-LL-005) → this spec (normative SLA +
owners + business-day definition + advisory detector) → enforced by the existing
reconciliation gate (day > 5 block) + the lineage projection freshness gate
(`054-AT-SPEC`, `ci.yml` "Validate specs and docs") that keeps the
outstanding-trigger count honest. Governance routing for any amendment to this
SLA: Blueprint A § 2.3 (Class-2 operational).
