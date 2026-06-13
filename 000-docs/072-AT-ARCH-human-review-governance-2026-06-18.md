---
title: Human-Review Governance — when a human must adjudicate, what the reviewer sees, and how the verdict re-enters the evidence chain
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Blueprint A § 1.2 (binding principles) + DR-010 § 7 Q6 (three-class governance routing)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — the constitution)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — runtime + 13-entity domain model)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E14
bead: bd_000-projects-rtcr
filing_standard: Document Filing Standard v4.3
related_docs:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — governance routing this doc operationalizes)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — SessionTrace / JudgeDecision / RolloutGate entities)
  - 014-DR-GLOS-canonical-glossary.md (terminology source of truth)
  - 067-AT-SPEC-runtime-event-taxonomy-2026-06-12.md (gate.* / judge.* OTel events the review surface observes)
  - 073-AT-STND-economics-and-cost-governance-2026-06-18.md (the cost surface a human reviews against budget)
  - 074-AT-STND-optimizer-safety-model-2026-06-18.md (the optimizer whose proposals are human-gated)
  - 075-AT-STND-priority-governance-2026-06-18.md (the priority lattice a reviewer's queue obeys)
related_drs:
  - 010-AT-DECR (DR-010 — three-class governance routing; § 13.5 customer-signal-gate override)
  - 028-AT-DECR (DR-028 — Skill Refiner accept predicate; human-gated optimizer proposals)
state_element_status: PLANNED
---

> **State label: NORMATIVE.** This document is binding governance doctrine. The
> mechanism it governs (an `intent-review-console` surface) is `PLANNED` per the
> State-Labeling Standard (`069-DR-STND-...`) — no review console is built yet. The
> doctrine is authored now so that the day the console is built it has a contract to
> satisfy, and so that manual human-review-in-the-loop today already obeys the rules.
> "Document now, build later" per epic iel-E14.

# Human-Review Governance

**Beads:** `bd_000-projects-rtcr` (iel-E14a) under epic `bd_000-projects-14j` (iel-E14 —
operational doctrine bundle). GitHub: `jeremylongshore/intent-eval-lab#48`. Plane: LAB-46.

## 0. What this doctrine is and is not

The Intent Eval Platform is **agent-native**: most of what it produces — gate verdicts,
judge decisions, rollout decisions — is machine-generated and machine-verifiable. A
human is **not** in the default path. This is deliberate: a verdict that requires a
human to be trustworthy is not an attestation, it is an opinion. Per Blueprint A § 1.2,
the platform's value proposition is *independent verifiability* — anyone with the public
signing component or a Rekor entry confirms a verdict without trusting Intent Solutions
*or* any reviewer.

This doctrine governs the **bounded exceptions**: the specific, enumerated moments at
which a human must adjudicate before the machine result becomes binding, what that human
is shown, and — critically — how the human's verdict re-enters the evidence chain
**without becoming an unverifiable trust root.** It is *not* a workflow tool spec, *not*
a UI design, and *not* a license to insert human approval as a general-purpose safety
blanket. Inserting a human where the machine result is already verifiable is an
anti-pattern this doctrine names and forbids (§ 7).

This document **derives from and does not override** Blueprint A or DR-010. Where it
conflicts with either, Blueprint A wins (per its § 0), then DR-010.

## 1. The default: no human in the loop

### R1 — Machine verdicts are binding without human review

A `gate-result/v1` row that verifies (DSSE signature valid, schema valid, subject digest
matches `input_hash` per the Evidence Bundle SPEC R13) is **binding without human
review.** A `RolloutGate` (canonical glossary § 2.8) ship/no-ship/advisory decision
consumed from a verified bundle against a `tests/TESTING.md` policy is **binding without
human review.** No reviewer signature is part of the verification chain for either.

This is the load-bearing inversion: the platform does not *add* trust by adding a human;
it *preserves* verifiability by keeping the human out of the cryptographic path. A human
review verdict is therefore never a *substitute* for a machine verdict — it is a
**separate, additionally-attested act** (§ 4) that a *policy* may require, the same way a
policy may require a coverage floor.

### R2 — The human-review trigger lives in policy, never in the predicate

Whether a human must review is a property of the **consuming repository's policy**
(`tests/TESTING.md`), exactly as coverage thresholds and advisory-elevation rules are
(Evidence Bundle SPEC § 8 R14/R15). It is **never** encoded in a predicate URI or a
predicate body. Coupling a human-review requirement to the immutable attestation surface
would force every team's reviewer-policy change to mint a new predicate URI — the same
error the SPEC rejects for policy generally. A policy says "require a `human-review/v1`
row from an authorized reviewer when gate decision is `advisory` on branch `main`"; the
predicate URI knows nothing of reviewers.

## 2. The enumerated human-review triggers (closed set)

A human MUST adjudicate before the machine result becomes binding in exactly the
following cases. The set is **closed**: a new trigger is a Class-1 ISEDC act (DR-010 § 7
Q6) because it changes the attestation surface (it admits a new authorized-reviewer
identity into a signed chain).

| # | Trigger | Why a machine cannot self-adjudicate | Routing class |
| --- | --- | --- | --- |
| HR-1 | **One-way-door governance acts** — reserving a predicate URI, a DNS zone change at a predicate subdomain, a Fulcio identity issuance, a DSSE envelope schema change, a standards-body submission, a new brand commitment, a new partner-engagement public reference. | The artifact is immutable in Rekor / the trademark register / a SIG's institutional memory. No replay un-signs a Rekor entry. | Class 1 (full 7-seat ISEDC) |
| HR-2 | **Optimizer-proposed SKILL.md edits** that pass the Skill Refiner accept predicate (DR-028 P0-RATIFY-1: strict-improvement-on-Pareto-dominant-behavioral-with-non-regressing-others) but touch a `SkillSnapshot` that is referenced by a production rollout pin. | The accept predicate proves *no behavioral regression on the eval set*; it cannot prove the edit is *safe against criteria the eval set does not cover.* See `074-AT-STND-optimizer-safety-model`. | Class 2 (CTO + VP DevRel pair) by default; Class 1 if the edit also touches a one-way-door surface |
| HR-3 | **A judge-disagreement event** (`judge.disagreement`, runtime-event taxonomy § 1.2) where the disagreeing judges include at least one `llm_no_seed` source AND the disagreement straddles a ship/no-ship boundary. | An `llm_no_seed` verdict cannot be replayed beyond statistical reconstruction (glossary § 3, "judge"); the machine cannot deterministically break the tie. | Class 3 (solo maintainer) — adjudication is recorded, not the disagreement re-run |
| HR-4 | **A FailureTaxonomy admission** (a candidate MM-7+ per `CONTRIBUTING-failure-shape.md`). | Admission criteria C1/C2/C3 (≥2 engagements, type-distinct, OTel vocabulary) require human judgment that a shape recurs and does not type-fit an existing category. Adding a category is irreversible (glossary § 4). | Class 1 (vocabulary change) |
| HR-5 | **A budget-ceiling breach** that a policy marks `require_human_ack` rather than `hard_stop` (see `073-AT-STND-economics-and-cost-governance` § 4). | The machine *can* hard-stop; whether a one-time overage is acceptable is an economic judgment the budget owner makes, not the runtime. | Class 3 (or the budget owner named in policy) |

Anything not on this list is **not** a human-review trigger. A reviewer who wishes a new
trigger existed files a Class-1 ISEDC request; they do not insert ad-hoc approval steps.

## 3. What the reviewer is shown (the review surface)

### R3 — The reviewer sees evidence, never raw sensitive payloads

When a human adjudicates any HR-N case, the surface presented to them is composed from
**already-sanitized** evidence:

- The relevant `SessionTrace` (glossary § 2.10) **after** the credential-redaction
  discipline of `ToolInvocation` (glossary § 2.11) has applied — a row containing a
  credential-shaped string in `args` or `result_summary` never persisted, so it never
  reaches the reviewer.
- The Evidence Bundle rows under adjudication, with their verification status (verified /
  failed / not-yet-anchored) shown per row.
- For HR-2 optimizer cases, the diff of the proposed SKILL.md edit and the Pareto
  behavioral comparison (the accept-predicate inputs), per `074-AT-STND`.
- For HR-3 judge-disagreement cases, the `judge.disagreement.verdict_set` and each
  judge's `verdict_source`, so the human knows which verdict is replayable.
- The relevant `CostRecord` rollup (glossary § 2.12) for HR-5.

When (and only when) the `agent-loop-trace/v1` predicate becomes admissible — gated on
the sanitization SPEC at `specs/sanitization/v0.1.0-draft/SPEC.md` passing its CISO
PASS/FAIL fixture (DR-010 § 7 Q3 CISO veto; PREDICATE-TYPES.md REJECTED row) — loop-trace
evidence shown to a reviewer MUST pass that sanitization pipeline first. **Until the
sanitization spec lands and its fixtures are green, no agent-loop-trace content is shown
to a human reviewer through this surface**, because the review console would otherwise be
a second uncontrolled egress for the exact credential-shaped substrings the predicate URI
is rejected over.

### R4 — The reviewer cannot mutate evidence

The review surface is **read-only over the evidence chain.** A reviewer cannot edit a
trace, re-score a judge decision, or alter a gate row. Their adjudication is an
*additional* attested act (§ 4), appended — never a mutation. This mirrors the
append-only discipline every entity in the domain model obeys: retries are new rows, not
edits (glossary § 2.11); regression evidence is a new pack referencing its ancestor
(§ 2.7); superseding is a new event, not a rewrite (`065-AT-SPEC`).

## 4. How the verdict re-enters the evidence chain

### R5 — A human verdict is itself an attested row

A human adjudication is recorded as its own in-toto Statement v1 row (Evidence Bundle
SPEC § 4), with:

- A predicate body carrying the reviewer's authorized identity (the OIDC subject + issuer
  of the reviewer, per the Fulcio keyless identity model — Evidence Bundle SPEC R11), the
  HR-N trigger class, the subject digest(s) of the evidence reviewed, the verdict
  (`approve` / `reject` / `escalate`), and a free-text rationale field.
- The reviewer's signature, the same DSSE-wrapped, optionally-Rekor-anchored way every
  other row is signed (SPEC § 7). A human verdict that is *not* signed is **not** part of
  the evidence chain — it is a comment.

The predicate URI for human-review rows is **not reserved by this document.** Reserving it
is a Class-1 ISEDC act (DR-010 § 7 Q6). This doctrine specifies the *shape and discipline*
of human-review attestation so that when the URI is reserved (candidate name
`human-review/v1`, host `evals.intentsolutions.io` only, never `labs.`), it has a
governing contract. Until reserved, human adjudications are recorded as Class-N Decision
Records (§ 5) and are not yet emitted as signed predicate rows.

### R6 — The human verdict never becomes a trust root

A human-review row is *evidence that a human reviewed*, not *proof that the thing reviewed
is correct.* A consumer that verifies a `human-review/v1` row learns "reviewer R, whose
identity is cryptographically established, approved evidence with digest D at time T" — it
does **not** learn that D is good. The machine verdicts D contains remain independently
verifiable on their own merits. This is the firewall against the platform's worst failure
mode: a reviewer signature becoming a substitute for verifiable evidence, such that
disagreeing with the reviewer requires trusting or distrusting a *person* rather than
re-checking *math.* Per R1, the human is additive, never substitutive.

## 5. Governance routing for human-review acts

Each HR-N trigger routes to a governance class per DR-010 § 7 Q6 and Blueprint A § 2.3,
and produces the matching artifact:

- **Class 1** (HR-1, HR-4): full 7-seat ISEDC convening; artifact is a full Decision
  Record (`NNN-AT-DECR-<title>-<date>.md`) with verbatim seat positions preserved; public
  archive on `intent-eval-lab` main within 7 days (VP DevRel non-negotiable floor).
- **Class 2** (HR-2 default): CTO + VP DevRel pair; artifact is a pair Decision Record.
- **Class 3** (HR-3, HR-5): solo maintainer (acting head of board); artifact is a one-line
  append to `SOLO-DECISIONS.md`.

The routing **class is a property of the trigger, not the reviewer's preference.** A
reviewer cannot downgrade a Class-1 act to a solo decision to move faster; doing so is the
"closed-convening + closed-records = indistinguishable from no-governance" hazard the VP
DevRel seat flagged in DR-010 § 8.

## 6. Relationship to the optimizer safety model and priority governance

Human review is the **escalation tier** of two sibling doctrines:

- The **optimizer safety model** (`074-AT-STND`) defines the autonomy ladder for Skill
  Refiner proposals. HR-2 is the rung where an optimizer proposal that the machine cannot
  fully self-certify (because it touches a production-pinned snapshot, or a surface the
  eval set does not cover) escalates to a human. The optimizer never auto-applies across
  that line; the human gate is the line.
- **Priority governance** (`075-AT-STND`) defines the lattice that orders a reviewer's
  queue. When multiple HR-N items await adjudication, the priority lattice — not
  arrival order, not the loudest stakeholder — decides which the reviewer sees first. The
  primary client engagement's off-the-top priority (DR-010 § 7 Q5) sits above this lattice
  entirely.

## 7. Anti-patterns — refuse on sight

- **Human-as-trust-root.** Treating a reviewer signature as evidence that the reviewed
  thing is *correct* rather than evidence that a *review occurred* (violates R6). The
  machine verdicts stand or fall on their own verification.
- **Review where the machine already verifies.** Inserting a mandatory human approval on a
  gate result that is already signed, schema-valid, and digest-matched. The human adds
  latency and a fallible trust dependency, and removes nothing. If a policy wants a second
  opinion, it requires a second *machine* judge (a `JudgeDecision`), not a human.
- **Unsigned human verdict in the chain.** Recording a human "approval" as a comment, a
  PR review, or a Slack thumbs-up and treating it as part of the evidence. A human verdict
  that matters is a signed row (R5) or it is not in the chain.
- **Reviewer mutating evidence.** Letting the review surface edit a trace, re-score a
  judge, or alter a gate row instead of appending an adjudication row (violates R4).
- **Ad-hoc trigger insertion.** Adding a human-review step outside the closed HR-1..HR-5
  set without a Class-1 ISEDC act (violates § 2).
- **Class downgrade for speed.** Routing a one-way-door act (HR-1, HR-4) as a solo
  decision to avoid convening the council (violates § 5).
- **Raw loop-trace to a human before sanitization.** Showing `agent-loop-trace` content
  to a reviewer before the sanitization SPEC's PASS/FAIL fixtures are green (violates R3;
  the review console must not be a second uncontrolled egress for credential-shaped
  substrings).

## 8. Cross-references

- **Blueprint A** (`011-AT-ARCH`) § 1.2 (binding principles — independent verifiability),
  § 2.3 (three-class governance routing).
- **Blueprint B** (`012-AT-ARCH`) § 2 (the entities a reviewer sees: SessionTrace,
  JudgeDecision, RolloutGate, CostRecord).
- **DR-010** (`010-AT-DECR`) § 7 Q6 (Class-1/2/3 routing trigger list), § 13.5
  (customer-signal-gate override — human review is bandwidth-gated, not customer-gated).
- **DR-028** (`028-AT-DECR`) — Skill Refiner accept predicate; HR-2 escalation boundary.
- **Canonical glossary** (`014-DR-GLOS`) § 2 (entities), § 3 (judge / replay terms), § 5
  (governance terms — ISEDC, routing, Decision Record, override, ratification).
- **Evidence Bundle SPEC** (`specs/evidence-bundle/v0.1.0-draft/SPEC.md`) § 4 (row shape),
  § 7 (signing), § 8 (policy consumption — R14/R15 the human-review trigger rides on),
  R13 (verification a reviewer sees per-row).
- **Sanitization SPEC** (`specs/sanitization/v0.1.0-draft/SPEC.md`) — the gate that admits
  agent-loop-trace evidence into the review surface (R3).
- **PREDICATE-TYPES.md** — REJECTED `agent-loop-trace/v1` row; the registry the future
  `human-review/v1` reservation lands in (Class-1).
- **Runtime event taxonomy** (`067-AT-SPEC`) § 1.2 (`judge.*` events HR-3 keys on),
  § 2.2 (`gate.*` events), § 3.1 (`bundle.*`).
- **Siblings:** `073-AT-STND-economics-and-cost-governance`, `074-AT-STND-optimizer-safety-model`,
  `075-AT-STND-priority-governance`.

## 9. License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
