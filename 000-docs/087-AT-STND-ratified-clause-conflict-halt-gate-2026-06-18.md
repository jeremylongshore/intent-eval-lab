---
title: Ratified-Clause-Conflict Halt Gate — a build agent that detects two contradictory ratified clauses on a one-way-door artifact MUST HALT and escalate
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: DR-085 D1 (Q1, 7-0) — ratified hybrid + halt-on-conflict governance gate
issued_under: ISEDC Corrective Council — IEP Kernel One-Way-Door Correction (DR-085)
filing_standard: Document Filing Standard v4.3
related_docs:
  - 085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md (DR-085 — D1 is the source decision)
  - 028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md (DR-028 — the record whose internal conflict motivated this gate)
  - 086-AT-DECR-dr-082-erratum-skill-refiner-pass-v1-freeze-and-amend-2026-06-18.md (sibling D2 erratum)
related_drs:
  - 028-AT-DECR (DR-028 — T1 line 105 defers signing fields vs P0-RATIFY-2 lines 233-236 adds them now; the internal contradiction)
  - 085-AT-DECR (DR-085 — D1 reconciles DR-028 + establishes this halt gate)
state_element_status: CURRENT
---

> **State label: NORMATIVE.** Binding governance rule for every build agent (human or
> automated) operating on one-way-door artifacts in the IEP kernel. Issued under DR-085 D1.
> The motivating defect is real and named: the PR #57 silent T1-vs-P0-RATIFY-2 resolution,
> reconciled in DR-085 D1.

# Ratified-Clause-Conflict Halt Gate

**Beads:** filed under the refiner/kernel epics per DR-085 § 11.4; the two standing CI gates
(this D1 conflict-marker gate + the D5 unenforced-invariant gate) are added to the kernel
boundary suite. **Issued under:** DR-085 D1 (`085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md`).

## 0. The motivating defect

DR-028 (ISEDC Session 7) contained an **internal contradiction** about the v0.8.0
`SkillVersion` shape:

- **T1 (line 105)** — _defer_ the signing fields (`status` / `signing_mode` /
  `rekor_log_index`); signing fields with no trust root are dead slots.
- **P0-RATIFY-2 (lines 233-236)** — _add them now_.

Both clauses were 20/20-ratified. They are contradictory. When the build agent implemented
the `SkillVersion` entity in kernel PR #57, it **silently resolved** the contradiction in one
direction without recording the conflict or escalating — an unrecorded exercise of authority
the agent does not hold. The corrective ISEDC council (DR-085) flagged this as the **more
serious finding** of the whole session (GC: _"the silent unilateral resolution is the more
serious finding"_; the GC seat named the CTO seat — the PR #57 reviewer — as the
silent-resolver to its face). DR-085 D1 reconciled the conflict (defer-then-add: T1 governs
sequencing, P0-RATIFY-2 governs eventual shape) **and** established the standing gate this
document records.

## 1. (a) The governance rule

> **Any build agent — human or automated — that detects two contradictory _ratified_ clauses
> bearing on a _one-way-door_ artifact MUST HALT and escalate. It must NEVER silently resolve
> the contradiction.**

Definitions, so the rule is operable:

- **Ratified clause** — a decision recorded in an ISEDC Decision Record (or an equivalent
  ratified standard) with a vote tally, e.g. a DR-028 T-tension resolution, a P0-RATIFY-N
  directive, a DR-082 Q-decision. Two clauses _conflict_ when implementing one as written
  makes the other false-as-written for the same artifact.
- **One-way-door artifact** — anything whose shape becomes irreversible once it is
  signed/tagged/published: a predicate URI, an in-toto predicate body, a kernel entity that
  feeds a signed predicate, a `$schemaVersion` lane, an attestation envelope, a
  standards-body filing. (The fix window for #56/#57 existed _only_ because they were
  merged-but-unpublished; once the next `@intentsolutions/core` tag fires the door shuts.)
- **HALT** — stop the implementation of the conflicting region, do not pick a side, and
  surface the conflict to the human decision-maker (or convene a corrective ISEDC) with both
  clauses quoted **verbatim** including their source DR + line numbers.
- **Escalate, not wait-a-week** — the duty is _halt-and-flag_, not _halt-and-block-the-repo_.
  Non-conflicting work proceeds; only the conflicting region is gated until a recorded
  reconciliation (a Class-1 amendment naming the clauses verbatim, as DR-085 D1 did for
  DR-028) resolves it.

The agent that silently resolves a ratified-clause conflict is exercising an authority it
does not hold. The remedy is structural: make the silent resolution _detectable_ and make the
honest path (halt + flag) the path of least resistance.

## 2. (b) The mechanism — and an honest account of what is and isn't auto-detectable

### 2.1 What is enforceable mechanically

Two things are genuinely mechanizable and are mandated here:

1. **A pre-merge checklist line in the PR template.** Every PR that changes a schema, a
   predicate file, or a kernel entity must affirmatively check the box:
   _"I checked the governing Decision Records for contradictory ratified clauses on any
   one-way-door artifact this PR touches; if I found one I HALTED and escalated rather than
   resolving it silently (DR-085 D1)."_ This converts the duty from tribal knowledge into a
   recorded affirmation the reviewer can hold the author to. (Landed in
   `.github/PULL_REQUEST_TEMPLATE.md`.)
2. **A lightweight reminder script** — `scripts/ratified-clause-conflict-check.sh` — that
   greps the PR's changed files for one-way-door surfaces (predicate files, signed-schema
   files, kernel entity definitions) and, when it finds any, emits the checklist reminder to
   the build agent / CI log with pointers to the governing DRs.

### 2.2 What is NOT auto-detectable (stated plainly, no overclaim)

**The script does NOT, and cannot honestly claim to, automatically detect a semantic
contradiction between two ratified clauses.** Determining that DR-028 T1 ("defer signing
fields") and P0-RATIFY-2 ("add them now") contradict each other requires reading both
clauses, understanding that they bear on the _same_ artifact, and reasoning that one makes the
other false — that is a judgment task, not a regex. Any tool that claimed to detect arbitrary
ratified-clause conflicts automatically would be lying.

What the script _can_ do is the honest, bounded thing:

- **Detect that a PR touches a one-way-door surface** (by path/content grep). This is a
  reliable, deterministic signal.
- **Emit the halt-on-conflict reminder + the relevant DR pointers** when it does, so the
  conflict-check duty fires at exactly the moments it matters and is never silently skipped.

In other words: the script automates **"you are in conflict-check territory, here is your
duty"**, not **"here is the conflict."** The conflict-detection itself stays a documented human
(or reasoning-agent) responsibility, backed by the recorded PR-template affirmation. This is
the maximum honest mechanization; claiming more would re-introduce exactly the false-assurance
posture DR-085 exists to correct.

### 2.3 The standing CI gate

Per DR-085 § 11.4, this D1 conflict-marker reminder gate and the D5 unenforced-invariant gate
are added to the kernel boundary suite. The D1 gate is the reminder mechanism above (advisory:
it surfaces the duty and the pointers, it does not — and must not — claim to adjudicate the
conflict). The D5 gate ("no unenforced invariant on a signed row," scoped to predicate/entity
schemas) is a separate, genuinely-blocking gate specified in DR-085 D5 and is not duplicated
here.

## 3. (c) The v0.8.0 SkillVersion signing-fields-deferred gate

This is the concrete reconciliation DR-085 D1 produced for the motivating defect, recorded
here as a binding gate:

> **The v0.8.0 `SkillVersion` MUST NOT carry the signing fields `status` / `signing_mode` /
> `rekor_log_index` (nor the `rekor_log_index`-iff-`production` invariant). They are
> DEFERRED.**

Bindings on the deferral (from DR-085 D1):

1. **Pre-specified, added verbatim later — NO third migration.** The deferred signing fields
   are pre-specified in DR-085 D1 and are added to `SkillVersion` _verbatim_ only after the
   **authoring signing trust root is provisioned** (DR-082 trigger 3). They are not
   re-designed at that point; the shape is fixed now and merely installed later. This avoids a
   third migration of the entity (CSO/CTO binding).
2. **Why deferred, not added-now.** Signing fields with no trust root behind them are dead
   slots — an attestation field that can only lie until a production Rekor exists (CISO). T1
   governs _sequencing_ (defer); P0-RATIFY-2 governs _eventual shape_ (the fields, when added,
   are exactly P0-RATIFY-2's). The two ratified clauses are thereby both honored, in order.
3. **A CI gate asserts the absence.** A standing kernel gate asserts that v0.8.0
   `SkillVersion` does NOT carry the signing fields (CTO binding). This is a real, blocking
   structural check — distinct from the advisory conflict-reminder of § 2 — because "the
   fields must be absent at this tag" _is_ mechanically decidable (unlike "two clauses
   contradict," which is not).
4. **Dated re-open tied to DR-082 trigger 3.** The deferral re-opens when the authoring
   chamber's separate signing trust root is provisioned-and-live (DR-082 Q3 trigger 3 /
   DR-085 reference), at which point the pre-specified fields are installed verbatim (CISO
   dated-re-open binding).

## 4. References

- DR-085: `085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md` — D1 (Q1, 7-0) is the
  source decision; § 11.4 mandates the two standing CI gates.
- DR-028: `028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`
  — the record whose internal T1 (line 105) vs P0-RATIFY-2 (lines 233-236) contradiction
  motivated this gate; reconciled by DR-085 D1.
- Sibling erratum (D2): `086-AT-DECR-dr-082-erratum-skill-refiner-pass-v1-freeze-and-amend-2026-06-18.md`.
- Mechanism: `scripts/ratified-clause-conflict-check.sh` (the reminder script) +
  `.github/PULL_REQUEST_TEMPLATE.md` (the pre-merge affirmation line).
