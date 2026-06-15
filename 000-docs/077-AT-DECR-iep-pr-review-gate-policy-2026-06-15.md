---
title: DR-077 — IEP PR-review-gate policy — required CI checks are the review gate; advisory AI-review bots are reactive-only
date: 2026-06-15
authors:
  - Jeremy Longshore (Intent Solutions)
status: RATIFIED
state_label: NORMATIVE
binding_authority: Standing review-gate policy (review gate = required CI checks, per the workflow-orchestration rule); DR-010 § 7 three-class governance routing (Class-2 internal posture)
acting_head: Jeremy Longshore (CEO-mode delegation; enacted by Claude in autonomous-CTO mode)
epic: bd_000-projects-9kcy (IEP testing + CI/CD posture) + bd_000-projects-969j (per-repo testing + CI/CD audit)
bead: bd_000-projects-wcv8 (iep-gemini-review-policy)
filing_standard: Document Filing Standard v4.3
related_docs:
  - 071-AA-AACR-iep-testing-cicd-audit-matrix-2026-06-18.md (the cross-repo CI/CD posture matrix this DR's review-gate column records the policy for)
  - 072-AT-ARCH-human-review-governance-2026-06-18.md (governs HUMAN adjudication of the evidence chain — distinct from this DR, which governs the automated PR-review gate)
related_drs:
  - 010-AT-DECR (DR-010 — three-class governance routing; Class-2 internal posture)
---

> **State label: NORMATIVE.** This is binding internal CI/CD posture for the five
> IEP repos. It is a **Class-2 internal-posture** record (DR-010 § 7) — it changes
> no external-facing policy, declares no predicate URI, and makes no brand
> commitment — so it is ratified by acting-head record, not an ISEDC convening
> (§ 5). It supersedes the open question carried by bead `bd_000-projects-wcv8`
> ("reactive advisory vs required status check"), which was overtaken by events.

# DR-077 — IEP PR-review-gate policy

**Beads:** `bd_000-projects-wcv8` (iep-gemini-review-policy) under epics
`bd_000-projects-9kcy` (IEP testing + CI/CD posture) and `bd_000-projects-969j`
(per-repo testing + CI/CD audit). This DR is the deliverable the bead asked for:
"file output as AT-DECR at `intent-eval-lab/000-docs/`."

## 0. Executive summary

The bead asked: should an AI PR-review bot (then `gemini-code-assist[bot]`) be left
as a reactive advisory, made a required status check, replaced, or kept-reactive
with a session-end ritual? The question was filed 2026-05-21 after an observed
failure: a round-2 bot review never fired across three re-invocations on an
audit-harness PR, and the merge proceeded on the round-1 record.

**The question was overtaken by events.** `gemini-code-assist[bot]` was retired
ecosystem-wide on 2026-05-28. The standing review-gate policy already moved to
**required CI checks as the review gate** — the AI-review bot is no longer in the
critical path of any IEP merge. This DR records the resulting, already-in-force
posture so the open question is closed against a written decision rather than left
to drift.

## 1. Decision

For all five IEP repos (`intent-eval-core`, `intent-eval-lab`, `audit-harness`,
`j-rig-skill-binary-eval`, `intent-rollout-gate`):

1. **The review gate is the set of required CI status checks**, not any AI-review
   bot. A PR is mergeable when its required checks (lint, typecheck, test, coverage,
   architecture, harness-hash verify, the applicable spec/state-machine drift gates,
   and any repo-specific security gate) are green — full stop. The merge decision
   never waits on, and is never blocked by, an AI-review bot.
2. **Any AI-review bot is reactive advisory only.** If one is wired, it fires on a
   PR-comment trigger, returns review comments for the author to weigh, and is
   **not** a required status check. Its silence, delay, or non-fire is never a merge
   blocker (option **(a)** of the bead's four — chosen because it matches what the
   ecosystem already enforces, and because the observed failure mode was exactly a
   bot dropping silently).
3. **A dropped or non-firing advisory bot is a no-op, not an incident.** The very
   failure that triggered this bead — a review that never fires — is, under this
   policy, harmless: the required checks already carry the gate. No re-invocation
   ritual is mandated (rejecting option **(d)**).
4. **The required-checks set is the lever, not the bot roster.** Strengthening the
   review gate means adding a deterministic required check (a new gate, a coverage
   floor, a security scan), not adopting a different review bot (subsuming option
   **(c)**: bot choice is a convenience, not policy).

## 2. Why this is the right posture (and narrow)

- **Determinism over availability.** A required CI check is reproducible and
  always runs; an LLM-review bot is a best-effort external service that can drop a
  run with no signal. Putting the gate on the deterministic surface removes the
  exact failure mode the bead documented.
- **It matches what already shipped.** The retirement of `gemini-code-assist[bot]`
  (2026-05-28) and the move to required CI checks were ecosystem decisions already
  in force; this DR documents IEP's conformance, it does not invent new policy.
- **It does not forbid advisory bots.** Teams may still wire a reactive AI reviewer
  for extra eyes; this DR only fixes its status as advisory-not-gating, so a future
  contributor cannot quietly promote a flaky bot into the merge path.

## 3. Classification

**Class-2 (internal posture)** per DR-010 § 7. It changes no external-facing review
policy for outside contributors, declares no predicate URI or OTel namespace, and
makes no brand commitment. Had it changed the gate that an external contributor's PR
must pass, it would be Class-1 and would return to ISEDC (§ 5).

## 4. Consequences

- The CI/CD posture matrix (doc 071) records "required CI checks" as the review-gate
  column for every IEP repo; this DR is the authority that column cites.
- No IEP repo wires an AI-review bot as a required status check. If one is observed
  wired as required, that is a posture violation to revert under this DR.
- Bead `bd_000-projects-wcv8` is satisfied by this record (its deliverable was this
  doc). The empirical evidence it carried (the silent round-2 non-fire) is preserved
  here as the motivating failure.

## 5. Process note

ISEDC was **not** convened. This is an acting-head record under CEO-mode delegation
for a Class-2 internal-posture decision whose substance was already settled by the
ecosystem-wide retirement of the prior bot plus the standing required-checks policy.
The seven-seat council remains the instrument for any change that would make an
AI-review bot a gating check for external contributors, alter the required-checks set
in a way that changes external contribution rules, or otherwise acquire a Class-1
external-facing dimension.
