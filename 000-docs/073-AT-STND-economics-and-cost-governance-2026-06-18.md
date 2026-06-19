---
title: Economics and Cost Governance — how the platform attributes, attests, and bounds the cost of running evals
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Blueprint B § 4.2 (budget enforcement) + DR-010 § 7 Q5 (bandwidth gate, primary-engagement off-the-top)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — the constitution)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — CostRecord entity, budget enforcement)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E14
bead: bd_000-projects-wtna
filing_standard: Document Filing Standard v4.3
related_docs:
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — § 2.12 CostRecord, § 4.2 budget enforcement)
  - 014-DR-GLOS-canonical-glossary.md (CostRecord / RuntimeReceipt / replay terminology)
  - 067-AT-SPEC-runtime-event-taxonomy-2026-06-12.md (cost.* event category)
  - 072-AT-ARCH-human-review-governance-2026-06-18.md (HR-5 budget-breach human-ack trigger)
  - 075-AT-STND-priority-governance-2026-06-18.md (priority lattice that orders spend)
related_drs:
  - 010-AT-DECR (DR-010 — § 7 Q5 roadmap sequencing; § 13.5 customer-signal-gate override)
  - 029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27 (FTE-week bandwidth model precedent)
state_element_status: PLANNED
---

> **State label: NORMATIVE.** Binding cost-governance doctrine. The `cost-attribution/v1`
> predicate URI it references is `CONDITIONAL` (PREDICATE-TYPES.md) — production-Rekor
> signing is gated on its own SPEC.md normative section landing. The cost-governance
> _rules_ are in force now for every eval the platform runs; the _signed_ cost-attestation
> surface activates when the predicate's SPEC section lands. "Document now, build later"
> per epic iel-E14.

# Economics and Cost Governance

**Beads:** `bd_000-projects-wtna` (iel-E14b) under epic `bd_000-projects-14j` (iel-E14 —
operational doctrine bundle). GitHub: `jeremylongshore/intent-eval-lab#48`. Plane: LAB-46.

## 0. What this doctrine governs

Running an eval costs money (provider API tokens, judge invocations, replays, cache
misses) and bandwidth (founder-hours per release). An evaluation platform that cannot say
_what an eval cost, who incurred it, and whether it was worth running_ is not a platform —
it is a way to spend money you cannot account for. This doctrine fixes:

1. **Attribution** — every cost is recorded against the dimensions that let it be analyzed
   (§ 1), as immutable `CostRecord` rows (glossary § 2.12).
2. **Attestation** — cost facts are emittable as signed evidence under the
   `cost-attribution/v1` predicate, with tamper-evidence over confidentiality (§ 2).
3. **Bounding** — budgets are enforced at the runtime boundary, with a closed set of
   breach behaviors (§ 4), and the founder-hour bandwidth ceiling is the hard outer
   bound on what the platform itself costs to build (§ 5).

It does **not** set prices, does not pick providers, and does not duplicate the kernel's
`CostRecord` schema (Blueprint B § 2.12 is the schema authority; on conflict, the kernel
wins per Blueprint B § 7.0).

This document **derives from and does not override** Blueprint B or DR-010.

## 1. Cost attribution

### R1 — Every cost is a CostRecord, immutable at creation

Every unit of spend the runtime incurs is recorded as a `CostRecord` (glossary § 2.12).
Cost records are **immutable at creation.** Rollups (per-day, per-user, per-provider) are
**separate rows**, never mutations of leaf rows. This is the same append-only discipline
every domain entity obeys — a corrected cost is a new record referencing the original,
not an edit.

### R2 — The attribution dimensions

A `CostRecord` attributes spend along the dimensions Blueprint B § 2.12 fixes:

| Dimension          | What it answers                                                            |
| ------------------ | -------------------------------------------------------------------------- |
| per `EvalRun`      | "what did this one evaluation cost end to end?"                            |
| per provider       | "how much are we spending against each LLM provider?"                      |
| per judge          | "is this judge worth its token cost relative to its discriminating power?" |
| per replay         | "what does it cost to re-verify an audit claim?"                           |
| per cache decision | "did the cache save or cost us on this call?"                              |
| per user           | "which consumer is driving spend?"                                         |
| per day            | "what is the burn rate?"                                                   |

`ToolInvocation` rows (glossary § 2.11) carry leaf-level attribution; the `RuntimeReceipt`
(§ 2.6) summarizes the run's total cost at terminal-state transition.

### R3 — Cost-basis versioning makes replay honest

Every `CostRecord` carries `cost_basis_version` (Blueprint B § 2.12). When a frozen
`EvalRun` is replayed (glossary § 3, "replay") after provider pricing has changed, the
replay declares **both** the original cost basis and the replay-time basis. A replay that
silently re-prices history is a falsified economic record. The discriminator lets a cost
analysis answer "did this get cheaper, or did the prices change?" — never conflating the
two.

## 2. Cost attestation

### R4 — Cost facts are emittable under `cost-attribution/v1`

A `CostRecord` rollup is emittable as an in-toto Statement v1 row (Evidence Bundle SPEC
§ 4) under the predicate URI:

```text
https://evals.intentsolutions.io/cost-attribution/v1
```

This URI is `CONDITIONAL` per PREDICATE-TYPES.md: it is a legitimate type in the
namespace, but production-Rekor signing is gated on the predicate's own SPEC.md normative
section landing first. Until then, cost attestations run in `sigstore_staging` mode
(DR-010 § 7 Q5; PREDICATE-TYPES.md CONDITIONAL row). This doctrine does **not** author that
SPEC section — reserving/activating the URI is a Class-1 ISEDC act. It fixes the
_discipline_ the section must honor.

### R5 — Tamper-evidence over confidentiality

Per the DR-010 § 7 Q3 CISO assessment of `cost-attribution/v1` ("APPROVE with reservations;
tamper-evidence over confidentiality; signing is appropriate"), a cost attestation's
purpose is **proving the cost number was not altered after the fact**, not hiding it. A
cost attestation therefore carries digests and totals, never the raw prompt/response
bodies whose token counts produced the cost. This is the same PII discipline the runtime
event taxonomy fixes (`067-AT-SPEC` § 5: "event payloads carry IDs, digests, enums, and
version strings — never raw prompt/response bodies"). A cost row that embeds a prompt to
"prove" its token count is a confidentiality leak masquerading as auditability.

### R6 — `cost.*` events fire alongside the row

The runtime emits `cost.*`-category OTel events (the category is locked by Blueprint B
§ 4.3; the per-event names are registered under the runtime-event taxonomy `067-AT-SPEC`
convention). Like every event, a cost event carries `eval.run_id` (the idempotency key)
and is malformed without it (`067-AT-SPEC` § 4.2). Cost telemetry is observability; the
`cost-attribution/v1` row is the signed evidence. They are two views of the same fact and
MUST NOT disagree.

## 3. The cost questions the platform must be able to answer

A conforming deployment can answer, from `CostRecord` rows and rollups alone, without
re-running anything:

1. **Per-feature cost** — what does running gate class X cost per invocation? (Input to
   Uncle Bob borrow #5, "coverage-as-prefilter for expensive gates," DR-010 § 7 Q4 — and
   the explicit reason the CISO bound it: prefilter coverage data feeding a signed
   attestation must come from a tamper-evident source.)
2. **Replay cost vs original cost** — does re-verifying an audit claim cost more than it
   saves? (R3 cost-basis versioning.)
3. **Cache economics** — did the cache decision save or cost on this call? (Per-cache-
   decision attribution, R2; informs the DEFERRED `cache-decision/v1` predicate.)
4. **Judge cost-effectiveness** — is a judge's discriminating power worth its token cost?
   (Per-judge attribution; the input to retiring or down-weighting a judge.)
5. **Burn rate** — what is the per-day spend, and how many days of runway does the current
   budget represent? (Per-day rollup, input to § 4 enforcement.)

## 4. Budget enforcement — the closed set of breach behaviors

### R7 — Budgets are enforced at the runtime boundary, declared in policy

Budget enforcement (Blueprint B § 4.2) happens at the **runtime boundary**, before spend
is incurred, against a budget the **consuming policy** declares. Like the human-review
trigger (`072-AT-ARCH` R2), a budget is _policy_, not predicate: a team's budget change
must never mint a new predicate URI.

### R8 — Exactly three breach behaviors

When a projected spend would breach a declared budget, the runtime applies exactly one of
the following, as the policy specifies. The set is **closed**:

| Behavior            | Effect                                                                                                                                                                        | When a policy chooses it                                                      |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `hard_stop`         | The runtime refuses to incur the spend; the `EvalRun` transitions to a terminal `archived_failed` state with a budget-breach reason. No partial spend leaks past the ceiling. | Production budgets where overspend is never acceptable.                       |
| `require_human_ack` | The runtime pauses and emits an HR-5 human-review trigger (`072-AT-ARCH` § 2). A budget owner named in policy must acknowledge before spend resumes.                          | Budgets where a one-time overage may be acceptable but needs an owner's call. |
| `advisory`          | The runtime proceeds and records a budget-advisory `cost.*` event + a non-blocking advisory row. Useful for soft budgets and trend monitoring.                                | Internal exploration; soft ceilings used as tripwires, not walls.             |

A policy that names no behavior defaults to `hard_stop` — the safe default is to **not
spend money you did not budget.** There is no fourth behavior; "warn and silently
continue forever" is `advisory`, and "block" is `hard_stop`.

### R9 — A breach is never silently absorbed

Every breach — whatever the behavior — emits a `cost.*` event and is attributable. A
budget that is breached without a trace is a governance hole. `advisory` is the _quietest_
behavior, not a _silent_ one.

## 5. The founder-hour bandwidth ceiling (the platform's own cost)

### R10 — Bandwidth is the platform's hardest budget

The platform itself is built under a sole-prop bandwidth reality of ~3–5 hrs/wk (DR-010
§ 4). DR-010 § 7 Q5 fixes the hard outer bound on what _building_ the platform may cost:

- **+50 founder-hr widening cap; +66 founder-hr hard ceiling** over the 6-month journey
  (DR-010 § 7 Q5 CFO non-negotiable).
- **The primary client engagement is off-the-top** — its hours are never drawn from this
  budget, and it is the first priority on its own track (DR-010 § 7 Q5; reinforced as the
  top of the priority lattice in `075-AT-STND`).
- **Each new Python package introduced anywhere in the platform = a minimum 15
  founder-hr/release maintenance cost** (DR-010 § 7 Q2 CFO bandwidth gate). That number is
  the gate on language-widening decisions.

The Skill Refiner bandwidth model (`029-DR-BAND`, FTE-week accounting: 8.8 FTE-weeks ≈ ~3
calendar months bandwidth-gated) is the worked precedent for how a feature's founder-hour
cost is estimated _before_ it is committed. New platform features estimate their
founder-hour cost against the remaining headroom under the +50/+66 cap before claiming a
build bead.

### R11 — Bandwidth-gated, not customer-signal-gated

Per the DR-010 § 13.5 acting-head-of-board override, platform feature work is
**bandwidth-gated, not customer-signal-gated.** The economic question for any new feature
is "do we have the founder-hours under the cap?" — never "does a customer pay for this
first?" The platform is an internal tool the acting head of board builds for himself and
the Intent Solutions practice, shared with the world as OSS by default. Marketing/customer-
acquisition framing is removed from cost-justification reasoning.

## 6. Anti-patterns — refuse on sight

- **Unattributed spend.** Incurring provider cost without a `CostRecord` (violates R1).
  Every token spent is attributable or it is a hole.
- **Mutating a cost record.** Editing a leaf `CostRecord` to "correct" it instead of
  appending a new record (violates R1). Cost history is append-only.
- **Silent re-pricing on replay.** Replaying a frozen run and recording today's prices as
  if they were the original cost (violates R3). Replay declares both bases.
- **Raw payloads in a cost attestation.** Embedding the prompt/response that produced a
  token count into a `cost-attribution/v1` row "for auditability" (violates R5). Carry the
  digest and the total, never the bytes.
- **Budget in the predicate.** Encoding a budget threshold in a predicate URI or body so
  that changing the budget mints a new URI (violates R7).
- **A fourth breach behavior.** Inventing "warn-then-continue-but-track-differently" or any
  behavior outside `hard_stop` / `require_human_ack` / `advisory` (violates R8).
- **Silently absorbed breach.** A budget breach with no event and no attribution (violates
  R9).
- **Drawing primary-engagement hours from the widening cap.** Counting the primary client
  engagement's founder-hours against the +50/+66 platform-build budget (violates R10; the
  engagement is off-the-top).
- **Customer-signal cost gate.** Justifying a feature build on "a customer will pay for
  this" rather than "we have the bandwidth under the cap" (violates R11; DR-010 § 13.5).

## 7. Cross-references

- **Blueprint B** (`012-AT-ARCH`) § 2.12 (CostRecord schema authority), § 2.6
  (RuntimeReceipt cost summary), § 4.2 (budget enforcement), § 4.3 (`cost.*` event
  category lock), § 7.0 (kernel-schema-wins precedence).
- **DR-010** (`010-AT-DECR`) § 7 Q2 (Python-package 15-hr gate), § 7 Q3 (`cost-attribution/v1`
  CISO assessment), § 7 Q4 (coverage-as-prefilter borrow), § 7 Q5 (+50/+66 cap,
  primary-engagement off-the-top), § 13.5 (bandwidth-not-customer gate).
- **DR-029** (`029-DR-BAND`) — FTE-week bandwidth-estimation precedent.
- **Canonical glossary** (`014-DR-GLOS`) § 2.12 (CostRecord), § 2.6 (RuntimeReceipt),
  § 3 (replay, cost-basis).
- **Evidence Bundle SPEC** (`specs/evidence-bundle/v0.1.0-draft/SPEC.md`) § 4 (row shape),
  § 7 (signing), § 8 (policy consumption — budgets ride on the same interface).
- **PREDICATE-TYPES.md** — CONDITIONAL `cost-attribution/v1` row; DEFERRED `cache-decision/v1`.
- **Runtime event taxonomy** (`067-AT-SPEC`) § 3 (event categories), § 4.2 (required
  `eval.run_id`), § 5 (PII anti-pattern).
- **Siblings:** `072-AT-ARCH-human-review-governance` (HR-5 budget-ack trigger),
  `074-AT-STND-optimizer-safety-model`, `075-AT-STND-priority-governance`.

## 8. License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
