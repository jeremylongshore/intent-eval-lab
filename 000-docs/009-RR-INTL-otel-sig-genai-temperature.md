# 009-RR-INTL — OTel SIG-GenAI community-temperature engagement

| Field | Value |
|---|---|
| **Date opened** | 2026-05-11 |
| **Author** | Claude (Opus 4.7) drafting for Jeremy Longshore |
| **Authority** | ISEDC v1 Q4 CSO sequence binding constraint (`000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md`) re-affirmed by ISEDC v2 Q1 Option B decision (`000-docs/006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md`) |
| **Plan reference** | Milestone 1 of `~/.claude/plans/se-the-council-bubbly-frog.md` |
| **Bead** | `iel-p4a` (M1 sub-bead) under epic `iel-bbt` |
| **Status** | Email DRAFTED. **Send is a Jeremy manual action.** This file is the GC-mandated paper-trail record. |

---

## 1. Purpose

The CSO seat's binding sequence for OTel SIG-GenAI engagement is:

> Week 1: informal community-temperature email to a verified SIG-GenAI maintainer, with a
> vocabulary draft attached as an enclosure for context — **NO RFC enclosed, no formal proposal,
> no commitment ask**. The purpose is to learn how the maintainer routes new vocabulary
> proposals before filing one.
>
> Week 4+: file the formal RFC (`agent.rollout.gate.*` per `001-DR-RFC-...md`) informed by
> the routing feedback received.

This document records:

1. The verified maintainer-identification approach (§ 2)
2. The 2-paragraph email draft staged for Jeremy to send (§ 3)
3. The criteria for what counts as response / timeout / triage signal (§ 4)
4. The Week 4+ RFC routing-decision criteria (§ 5)

GC mandate: every action against an external standards body is paper-trailed against the
council decision that authorized it. This file is that paper trail for the M1 informal email.

## 2. Verified maintainer identification

The OpenTelemetry SIG-GenAI working group is the relevant group for AI-agent semantic conventions.
Verifying the current maintainer requires reading **fresh** OTel community sources (the maintainer
roster rotates):

1. Visit https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md (the SIG charter
   page) to confirm the current named maintainers and the SIG's current active focus.
2. Cross-check by reading the most recent SIG-GenAI meeting notes (the OTel community calendar
   links the meeting series).
3. Identify a maintainer who has personally landed PRs on the `semantic-conventions` repository
   for AI-agent attributes within the last 90 days. Name + GitHub handle + verified email
   (typically @<employer>.com or the maintainer's personal email listed in their GitHub profile).

**Why verification matters:** a CSO realpolitik concern is that a community-temperature email to
a stale or sidelined maintainer is silently filed as low-signal. The first impression is permanent.
The maintainer must be currently active in the relevant area.

**Action for Jeremy before sending:** complete the verification above and update § 3 below with
the verified `<MAINTAINER NAME>` and `<MAINTAINER HANDLE>` placeholders. Do not send to a
generic mailing-list address — the CSO sequence calls for a personal, named recipient.

## 3. Email draft (TO BE SENT BY JEREMY)

**Subject:** `Quick sanity-check on agent-rollout-gate vocabulary before any RFC`

**To:** `<MAINTAINER NAME> <maintainer@email>`

**From:** `Jeremy Longshore <jeremy@intentsolutions.io>`

---

Hi `<MAINTAINER FIRST NAME>`,

I run Intent Solutions, a small AI-tooling shop. Over the last several months I've been building
out an evaluation platform for agent-native CLIs, and the static-gate + behavioral-eval signals
are starting to look like they want a shared OTel vocabulary — specifically an
`agent.rollout.gate.*` event family fired at evaluation moments (gate-evaluated, gate-decision,
verdict-emitted). I've drafted internal-only RFC text for it, and I'd like to file it formally
with SIG-GenAI in a few weeks once I've got real reference-implementation traffic against the
shape.

Before I file anything, I'd really value 5 minutes of your read on whether this lands in
SIG-GenAI's scope, in another SIG (OTel-MCP if that ends up existing, or a sub-group), or
whether it should sit at the application-level until the underlying primitives stabilize. I'm
not asking for a commitment or a review cycle yet — just routing guidance so I file in the right
place. Happy to share the draft RFC text if it's useful, but I don't want to drop a 4-page
proposal in your inbox uninvited.

Thanks for any time you can give this — and apologies in advance if I've routed to the wrong
person; happy to be re-routed.

Jeremy
Intent Solutions LLC
intentsolutions.io

---

**Notes for Jeremy on the draft:**

- The email contains no RFC enclosure, no commitment ask, and no Phase B timeline assertions
  (CFO Q1 binding constraint).
- It explicitly invites re-routing — preserving the SIG-GenAI maintainer's ability to redirect
  without it feeling like a friction point (CMO seat: "first-impression is permanent").
- It does NOT name @pvncher or any specific external party as a motivation (Q2 user override:
  IS rides solo on this).
- The "shared OTel vocabulary" framing positions IS as recognizing a community-shaped problem
  rather than promoting an IS-built solution (Research Expert seat: "what the space needs" >
  "what we've built").
- The "internal-only RFC text" reference is honest: the RFC exists at
  `001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` but has not been filed publicly anywhere.
- Word count: ~250 words. Reads as a 30-second open and a 2-minute reply.

## 4. Response classification

Once sent, classify the response within 14 calendar days. Update this section with the actual
outcome.

| Outcome | What it means | Next action |
|---|---|---|
| **Routing-accept** — maintainer confirms SIG-GenAI scope and offers a follow-up channel (issue, meeting slot, sub-group thread) | Optimal outcome. M6 RFC filing follows the offered channel. | Schedule the offered channel. Update `001-DR-RFC` doc with maintainer's routing guidance. Plan M6 RFC filing for ~Week 4+ from email send. |
| **Routing-redirect** — maintainer redirects to a different SIG / sub-group / approach | Useful outcome. The CSO sequence's whole point is to learn this BEFORE filing. | Re-do § 2 verification for the new SIG. Re-draft email. Send to new SIG. Restart the 14-day clock. |
| **Routing-defer** — maintainer says "the underlying primitives aren't stable yet, come back when X" | Acceptable outcome. Records that the OTel community sees this work as premature; absorbs the feedback into the Phase B sequence. | Document X. Re-evaluate at the milestone X requires. Do NOT file the RFC against this maintainer's stated guidance. |
| **No response within 14 days** | Triage signal, not failure. The maintainer may be busy, traveling, or simply not interested. | Re-verify maintainer is still active in the SIG. If yes, send a single 1-paragraph follow-up at day 14. If no response by day 28, document the silence and route to a different SIG-GenAI maintainer (re-do § 2). |
| **Hostile / dismissive response** | Rare but possible. CSO seat: "first-impression is permanent" cuts both ways — a dismissive reply IS the first impression of IS. | Do NOT reply defensively. Document the response verbatim. Wait for next ISEDC convening before re-engaging. Consider a different SIG entirely. |

## 5. Week 4+ RFC routing-decision criteria

When the response is classified, the RFC filing decision (M6 work item) carries forward the
routing guidance:

1. **Filing channel:** the channel the maintainer guided toward (most often a GitHub issue on
   `open-telemetry/semantic-conventions` with the SIG-GenAI label).
2. **RFC framing language:** the RFC's opening paragraph should reference the prior conversation
   ("per discussion with `<MAINTAINER HANDLE>` 2026-MM-DD on routing for agent-rollout-gate
   semantics"). This signals to subsequent maintainers that the routing was vetted.
3. **Vocabulary scope adjustment:** if the routing guidance suggested narrowing or widening the
   vocabulary scope, apply the suggestion BEFORE filing. Filing the original draft against
   guidance that asked for adjustment is a credibility event.
4. **Timing:** no earlier than 4 weeks after the informal email send. The 4-week buffer absorbs
   maintainer-vacation gaps and gives the community-clock argument (CSO Q1 rationale) honest
   pacing — not a rush.

## 6. Cross-references

- `001-DR-RFC-otel-agent-rollout-gate-signals-draft.md` — the RFC text that will eventually be
  filed (M6 deliverable per `se-the-council-bubbly-frog.md`)
- `004-AT-DECR-isedc-council-record-2026-05-10.md` § Q4 — original CSO sequence decision
- `006-AT-DECR-isedc-council-2-phase-b-gate-2026-05-11.md` § Q1 — Option B re-affirms the CSO
  sequence as the minimum standards-track action allowed during the Q1-lifted period
- ISEDC v1 GC binding: paper trail every external standards-body action against its authorizing
  council decision. This file is that paper trail.

## 7. Update log

| Date | Update |
|---|---|
| 2026-05-11 | File opened; email drafted; § 2 verification + actual send pending Jeremy manual action |
