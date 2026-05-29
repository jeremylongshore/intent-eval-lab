# Ward Cunningham — Plan Audit Findings — 2026-05-27

**Plan under audit:** `intent-eval-lab/000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1)
**Primary axes:** (a) GAPS, (d) SCOPE INTEGRITY
**Cunningham canon invoked:** Technical-debt as the gap between code-you-wrote and code-you-should-have-written; the retrospective is the most important meeting; simplicity is finding the abstractions that give you power without complexity; yes-and beats no-but; wiki/pattern-language thinking (every claim hyperlinks to its rationale).

## Summary — top concerns

1. The plan flags its own missing AAR cadence as P2 (F-WC-001 in § 12 "Sample findings"). That severity is wrong by the plan's own evidence: AAR-023 produced 9+ findings *because* the panel convened, and the plan cites AAR-023 as load-bearing precedent. Self-diagnosing your retrospective gap and then triaging it as a MINOR is the textbook accidental-debt pattern.
2. § 3.5 introduces seven parallel process disciplines (tri-linkage, validate-consistency, sequential execution, bd memories, per-repo CLAUDE.md updates, validate-trilink CI, quarterly spec refresh) without naming the single abstraction that unifies them. Seven disciplines, seven failure modes, seven debt accounts.
3. Phase D ("DEFERRED INDEFINITELY") and the four spec-snapshot quarterlies are both deferrals dressed as decisions. Deferred-vs-abandoned is the most expensive ambiguity a plan can ship; this plan ships it twice without distinguishing them.

## Findings

### F-WC-001 [P1] [GAPS] — The plan self-diagnoses no AAR cadence and triages it as a P2, contradicting the canonical position

**Plan section cited:** § 12 "Sample findings" → `F-WC-001 [P2] [GAPS] — No AAR cadence is built into the plan`, paired with § 6 Operations (which never appears in the plan as a distinct section — § 6 is "Reused infrastructure" and § 6.5 is the ASCII catalog; *there is no § 6 Operations*).

**Plan verbatim:**
> "F-WC-001 [P2] [GAPS] — No AAR cadence is built into the plan … AAR-023 produced 9+ findings *because* a panel was convened. The Skill Refiner plan defines no equivalent retrospective trigger — no 'after first 5 promotions, convene AAR' or 'monthly Refiner review'. Institutional memory will leak."

**Cunningham position invoked:** *"The retrospective is the most important meeting."*

**Defect:** The plan correctly identifies the gap in its own sample-findings section, then triages it at P2 — which the plan's own rubric defines as "Real gap or risk; plan should address but not blocking … New bead filed; addressed in plan v5." A retrospective gap is not "addressed in plan v5"; it is the difference between detecting drift in 5 promotions vs. detecting it 18 months later in a postmortem. The plan also cites a § 6 Operations that does not exist — the plan structurally cannot point at the section the AAR cadence is supposed to live in, because no such section was authored. The remediation ("Add §X 'AAR cadence'") is unanchored.

**Why this matters:** The plan's load-bearing argument for the § 12 Plan Audit itself (line 1452) is *"Lesson of AAR-023 was adversarial review finds things. Not scheduling it means next finding arrives post-incident."* That argument applies recursively to the post-ratification execution phase — the same lesson the plan invokes against pre-code drift applies word-for-word against post-ship drift. Accepting this finding at P2 means the plan agrees AAR matters and refuses to act on it before code is written. That is accidental debt by Cunningham's own definition: *the gap between the plan you wrote and the plan you should have written had you known what you know now* — and the plan demonstrably already knows.

**Proposed remediation:** Up-severity to P1 CRITICAL. Author a new § 6 "Operations" section (currently a phantom reference). That section must define: (a) AAR trigger conditions — first 5 successful promotions, first rollback, first P0 incident, every 90 days regardless; (b) AAR output artifact — `intent-eval-lab/000-docs/NNN-AA-AACR-skill-refiner-operations-<date>.md`; (c) ratification cadence — which AAR findings re-enter the bead backlog vs. which trigger an ISEDC re-convene. No bead may be claimed against Phase B until § 6 exists and the first cadence-trigger is in the calendar.

---

### F-WC-002 [P1] [SCOPE INTEGRITY] — Seven parallel process disciplines without a unifying abstraction

**Plan section cited:** § 3.5 "Process Rigor — non-negotiable workflow gates" (PR-1 tri-linkage; PR-2 validate-consistency; PR-3 sequential execution; PR-4 bd memories; PR-5 per-repo CLAUDE.md updates), plus § 5.5 `validate-trilink.sh` CI integration, plus § 13 Step 0 quarterly spec snapshot refresh.

**Plan verbatim (PR-3 listing seven sub-disciplines):**
> "1. Plan … 2. Beads … 3. GH issues … 4. Validate … 5. Plan Audit … 6. Ratify … 7. THEN code"

And § 3.5 PR-1: tri-linkage doc↔bead↔GH-issue. PR-2: `/validate-consistency` at five trigger points. PR-4: nine `bd remember` trigger events. PR-5: six CLAUDE.md update triggers across five repos. The plan adds **31 enumerated process trigger conditions across the five PR-N disciplines** with no shared mechanism.

**Cunningham position invoked:** *"Simplicity is finding the abstractions that give you power without complexity."*

**Defect:** The plan stacks five PR-N disciplines (PR-1..PR-5), each with its own trigger list, its own verifier script, its own failure mode, and its own remediation path. There is no single abstraction — no "process event log" or "audit-trail entity" — that subsumes the others. Tri-linkage validates doc↔bead↔GH; validate-consistency validates 7 drift categories; bd memories captures operational findings; CLAUDE.md updates document repo state. Each of those is half of the same idea (preserve the connection between an artifact and its rationale), and each is implemented separately. The audit-trail integrity claim of the entire Refiner product (AC-7, AC-9, the Phase E Evidence Report § 6) rests on five-stacked-disciplines whose individual reliabilities multiply.

**Why this matters:** Each new discipline is a new opportunity for accidental debt — the kind that compounds at every Phase exit. By Phase F, the plan will be carrying seven parallel disciplines (the five PR-N plus quarterly spec refresh plus AAR cadence once F-WC-001 is remediated). At that point the cost of *adding* a constraint exceeds the cost of *living with the drift it would catch*. Cunningham's wiki was 200 lines because every page hyperlinked to its rationale and to the patterns that justified it; this plan has no equivalent — the rationale for each PR-N is asserted, not linked. The seven disciplines are seven hand-rolled tools where one well-chosen abstraction (e.g., a single "EvidenceLink" entity on every artifact, mirrored across layers by `bd-sync`, validated by one verifier) would unify all five PR-N + AAR cadence + spec-refresh into one mechanism.

**Proposed remediation:** Before Phase A claims, the plan must add a § 3.6 "Unifying abstraction" identifying one of: (a) a single `EvidenceLink` entity on every Refiner artifact whose validator subsumes PR-1, PR-2, PR-5, and validate-trilink; (b) an explicit acknowledgment that the seven disciplines are intentionally parallel because no single abstraction exists, with a named owner for each and a budget-of-attention argument for why seven is sustainable; OR (c) deletion of the disciplines that don't earn their keep at the bead-throughput level the plan claims (~1 week Phase A). The current "all seven, all simultaneous, all CI-enforced, all without unifying abstraction" position cannot survive contact with Phase F's ≥100 SkillVersion records.

---

### F-WC-003 [P0] [SCOPE INTEGRITY] — "Deferred indefinitely" is unmanaged debt, not a decision

**Plan section cited:** § 2 (Phase D), § 4 Phase D "DEFERRED indefinitely (creator sub-product)", § 11 non-goals (Phase D is named but not enumerated as a non-goal).

**Plan verbatim:**
> "**Creator sub-product (would generate NEW skills from scratch)**: DEFERRED INDEFINITELY at P3. SkillsBench evidence: self-generated skills underperform no-skill baseline. Re-open trigger: (a) external work demonstrates the bar can be cleared OR (b) a partner explicitly asks AND accepts the risk profile. Until then: no code, no design, no marketplace listing. Filed as standalone deferred bead `bd_000-projects-vbqp`."

**Cunningham position invoked:** *"Technical debt is the gap between the code you wrote and the code you should have written had you known what you know now."* Deferral is a debt instrument; indefinite deferral with no compounding clock is unpriced debt.

**Defect:** "Deferred indefinitely at P3" is three contradictory framings:
1. **Deferred** implies a clock — work that will be revisited.
2. **Indefinitely** removes the clock — work that may never be revisited.
3. **P3** is the lowest non-NIT priority in the plan's own rubric, which the rubric defines as "Improvement opportunity; not a defect."

The plan also lists Phase D in § 11 "What this plan does NOT do" implicitly (by omitting it from the do-list) but does NOT list it as a non-goal in Blueprint A § 3 terms (where non-goals are co-equal to goals and trigger ISEDC re-convene on scope creep, per Blueprint A line 140). So Phase D is simultaneously: (a) a deferred phase that might come back, (b) a P3 backlog item, (c) bd_000-projects-vbqp tracking the deferral, and (d) **not** a Blueprint A-level anti-goal. Future readers cannot tell whether this is debt-to-be-paid or work-that-was-abandoned.

Compounding the ambiguity: the plan's "quarterly spec-snapshot refresh" (§ 2.5, § 13 Step 0, AC-11) is a *second* indefinite deferral — drift-detection that the plan promises will happen every 90 days, with no named owner, no calendar mechanism, and no failure mode if the refresh is skipped. That is debt that will silently compound: the agentskills.io spec will move, the snapshot will go stale, and the AC-11 portability claim every SkillVersion record bears will become a lie. Cunningham's canon — *"The wiki only worked because every claim hyperlinked to its rationale"* — says the rationale must be inspectable; an unmaintained snapshot is a claim with a dead hyperlink.

**Why this matters:** This is the single finding most likely to embarrass Cunningham to leave unflagged. The plan is built on top of the SkillsBench finding (-1.3pp for self-generated skills) as the IP-defense argument for `claude-code-plugins`. If the creator sub-product is **abandoned**, that should be said — the plan should add a Blueprint A § 3 anti-goal "NOT a generative skill author" and close `bd_000-projects-vbqp` as `wont-fix` with citation. If it is **deferred**, the re-open trigger must carry a calendar review (every 6 months, did SkillsBench-class evidence change?) — otherwise the plan is asking the next session to remember to check, which is the prototype of institutional memory leak the plan's own AAR-023 lesson warns against. The third framing — "P3" — is incoherent with both: a deferred phase is not an "improvement opportunity," and a P3 finding does not warrant a standalone bead.

**Proposed remediation:** Pick one (binding before Phase A claims):
- **Path A — Abandon.** Add Blueprint A § 3.X anti-goal "NOT a generative skill author." Close `bd_000-projects-vbqp` with `--reason "abandoned per Plan Audit F-WC-003; SkillsBench finding is durable; re-litigate via ISEDC if reopened."` Remove "Phase D" framing from the plan; renumber Phases E→D, F→E. Deferred-indefinitely-at-P3 dies.
- **Path B — Defer with a clock.** Re-severity from P3 to P1, name an owner (Acting CTO), set a calendar review (2026-11-26 — six months out), and define the falsifying evidence that would re-open. Every six months the bead acquires a `bd-sync note` documenting why it stays deferred — that is the AAR-equivalent for non-active work. The deferral becomes managed debt instead of unpriced debt.

Apply the same Path A/B choice to the four spec-snapshot quarterlies (§ 13 Step 0 items 2 + 3): name an owner, schedule the first three refresh dates, define what failure-to-refresh triggers, OR delete the quarterly claim and admit the snapshot is pinned-forever-until-something-breaks.

---

### F-WC-004 [P2] [GAPS] — Every plan claim should hyperlink to its rationale; § 9 verification criteria do not

**Plan section cited:** § 9 "Verification (end-to-end)" — 8 aggregate plan-completion criteria.

**Plan verbatim:**
> "1. § 12 Plan Audit ratified … 2. § 13 Execution Sequence Steps 1-4 complete … 3. Phase A ships: `npm view @j-rig/refiner-core` … returns v0.1.0+ … 4. Phase B ships … 5. Phase C ships (gated on uprg+9pi3) … 6. Phase D: stays DEFERRED until external trigger fires … 7. Phase E ships … 8. Phase F triggers …"

**Cunningham position invoked:** *Wiki/pattern-language thinking — every claim should be a hyperlink to its rationale; opaque claims accumulate as debt.*

**Defect:** Each of the 8 criteria asserts a binary ship/no-ship state. None of them link to the artifact, test, bead, or signed Evidence Bundle that would prove the criterion is met. Criterion 3 says "Phase A ships if `npm view` returns v0.1.0+" — but there is no link to (a) the release ceremony bead that produces the npm publish, (b) the audit-harness emit-evidence row that signs the release, (c) the AAR doc filed per § 13 Step 7 that proves the ceremony completed. Criterion 5 says "Phase C ships (gated on uprg+9pi3)" — but `uprg` and `9pi3` are unlinked bead IDs; a reader cannot click through to see what those beads actually require. Criterion 2 cites `/validate-consistency` reporting zero BLOCKERs — but there's no link to the report file `validate-consistency-report.md` that already lives in this audit directory.

**Why this matters:** § 9 is the contract between the plan and its future executor — the exact place where Cunningham's *"every claim hyperlinks to its rationale"* matters most, because it is the place where slippage will be detected. An unlinked claim becomes interpretive at the moment of verification: "did Phase A really ship?" turns into a re-archaeology session against bd, GH, npm registry, and AAR docs, instead of a click-through. Plans that pass their own verification only by re-archaeology are plans where institutional memory leaks into the verifier — which is the exact failure mode F-WC-001 names.

**Proposed remediation:** Rewrite § 9 so every criterion carries an inline link to the bead, doc, or registry URL that proves it. Pattern: `Phase A ships ← bd_000-projects-pu35 (TL-EPIC) closed with --reason "Phase A AAR filed at NNN-AA-AACR-skill-refiner-phase-a-<date>.md; npm @j-rig/refiner-core@0.1.0 readable from https://www.npmjs.com/package/@j-rig/refiner-core"`. The hyperlink IS the rationale. This also forces § 13's AAR-filing discipline to be load-bearing rather than ceremonial.

---

### F-WC-005 [P1] [SCOPE INTEGRITY] — Yes-and-or-no-but: § 4.5 Ecosystem Fold lists 11 cross-repo dependencies, two of which (uprg, 9pi3) are blockers that were not negotiated with their owners

**Plan section cited:** § 4.5 "Ecosystem Fold integration matrix" — row 1 (`uprg`) and row 2 (`9pi3`).

**Plan verbatim:**
> "**`uprg` — Evidence Bundle compat policy (P0)** | intent-eval-core, intent-eval-lab | Phase C (Tier-1 kernel) | `uprg` → blocks Phase C | Phase C ships predicate URI that violates whatever policy `uprg` lands → must re-key, breaks consumers | Phase C explicitly waits on `uprg` closure; Phases A+B unblocked"

**Cunningham position invoked:** *"Yes-and beats no-but."* Yes-and is additive — you accept the constraint and build on top. No-but is subtractive — you assert a constraint others must accept. Ecosystem-wide coordination that hasn't been negotiated is no-but masquerading as yes-and.

**Defect:** The plan asserts that Phase C is "explicitly gated" on `uprg` and `9pi3` closure. But these are P0 beads in the existing IEP convergence-debt plan whose closure is **not under this plan's control**. The plan does not (a) cite a negotiation with the `uprg`/`9pi3` owners that ratifies the Phase C sequencing, (b) carry an ISEDC DR Session 5/6 binding that orders Phase C behind those beads as a *deliberate* sequencing choice, or (c) acknowledge what happens to Phase D/E/F if `uprg` slips. The "mitigation" in column 6 — *"Phase C explicitly waits on `uprg` closure; Phases A+B unblocked"* — is the plan declaring its own scheduling; it is not evidence the rest of the ecosystem agrees. Eleven such rows in § 4.5 means eleven assumed coordinations. Some are real (`bj5m` is closed, `tyck` is named with a grandfathering note), but at least two (`uprg`, `9pi3`) are still-open P0 beads that block Phase C indefinitely and the plan does not acknowledge that indefinite-block is a possible outcome.

**Why this matters:** This is the "no-but masquerading as yes-and" pattern. The plan presents itself as additive to the IEP ecosystem ("Folds additively into the existing 5-repo IEP ecosystem" — § scope line 26), but Phase C is a no-but: *"we will ship the 14th canonical entity AND the new predicate URI, but you must first close uprg+9pi3 on our timeline."* The plan does not have authority to set that timeline on behalf of the uprg/9pi3 owners. Real yes-and would either (a) ship Phase C against the current Evidence Bundle compat policy (whatever it is today) and accept the re-key cost if uprg changes it, or (b) acknowledge Phase C is structurally optional — Phases A+B are the value-bearing core, and Phase C is a polish layer that may never ship if the kernel work blocks.

**Proposed remediation:** Add to § 4.5 a row-by-row "negotiated with owner: YES/NO" column. For YES rows, cite the DR or bd-sync note that records the negotiation. For NO rows (currently at least uprg, 9pi3, M5 substantive runtime, iah-npm-publish-gap), the plan must either: (a) downgrade the dependency from "blocks" to "preferred-precondition" and define what Phase C looks like if the precondition is never met; (b) escalate to an ISEDC Session that ratifies the cross-plan sequencing; or (c) explicitly admit Phase C may slip indefinitely and document the value of Phases A+B as standalone. Until one of those is done, the plan's "fold additively" claim is rhetorical.

---

## Out-of-scope observations (noted but not panel's job)

- The plan's revision history (v1 → v2 → v3 → v4 → v4.1 over a single day) is itself the kind of churn that produces accidental debt; the next session reading this plan in six months will not easily reconstruct which decisions stick and which were overwritten mid-draft. A wiki-style "decisions log" tied to the doc would help. Not Cunningham's panel-axis (this is article-consistency territory).
- § 2.5's recursive link-following discipline (depth-1 minimum, depth-2 for plugins/skills/hooks) will produce a 40-80-URL artifact at `intent-eval-lab/research/claude-docs-spec-tree-2026-05-27.md`. The plan does not specify what makes that artifact stale, nor what the consumer does when a depth-2 link 404s. This is a sub-issue of F-WC-003 (deferred-vs-abandoned ambiguity applied to spec snapshots), but worth flagging discretely for the Karpathy/Lamport seats.
- § 12 "Sample findings" pre-emptively writes findings the panel "would" produce (F-CH-001, F-AK-001, F-LL-001, F-KB-001, F-MK-001, F-WC-001). This is methodologically suspect — the panel's value is independent generation; sample-findings bias the seats. The internal-review report at `internal-review-2026-05-27.md` was correctly withheld from the brief pack for exactly this reason; the in-plan § 12 samples were not. Not Cunningham's axis to escalate, but flagged.

---

VERDICT: AMEND
