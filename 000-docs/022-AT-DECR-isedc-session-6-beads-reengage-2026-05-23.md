# ISEDC Decision Record — Re-engage `gastownhall/beads` on residual gitignored-path throttle-bypass gap

| Field                    | Value                                                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **Date**                 | 2026-05-23                                                                                                                   |
| **Acting head of board** | Jeremy Longshore (Claude as designated drafting executor)                                                                    |
| **Council size**         | 7 (default roster: CTO · GC · CMO · CFO · CSO · CISO · VP DevRel)                                                            |
| **Status**               | DECIDED, EXECUTED — INVERTED BY EMPIRICAL FINDING (see § 11)                                                                 |
| **Counterparty**         | `gastownhall/beads` — 23,613★ Steve-Yegge-stewarded bd issue tracker; primary code-review counterparty: maphew (Matt Wilkie) |
| **Session JSONL**        | `~/.claude/skills/exec-decision-council/sessions/2026-05-23-beads-reengage/session.jsonl`                                    |

## 1. Why a council, not a single review

Three factors warranted ISEDC convening rather than direct decision:

1. **Asymmetric reputational stakes** on a 23k★ public repo where every artifact becomes permanent searchable record.
2. **Prior misstep already in the record** — Jeremy's 2026-05-21 #4061 close-comment ("default-off makes the bypass logic moot") was incomplete reasoning; any re-engagement either repairs that withdrawal cleanly or compounds it.
3. **AI-assistance optics asymmetry** — counterparty maphew is himself codex-gpt-5.5-fluent; he will detect AI-spam tone instantly. The cost of a wrong tone calibration here propagates across every future Intent Solutions contribution to this repo (which is permanent: we depend on `bd` as the canonical SoT for the entire IEP convergence).

## 2. Synthesis lenses

1. **Maintainer-trust capital** — finite budget; prior close was a withdrawal
2. **Root-cause vs symptom** — does re-engagement address architecture or just our pain
3. **AI-assistance optics** — quality engineering vs AI-spam read
4. **Long-term repo vision alignment** — fit the explicit-opt-in + JSONL-as-viewer-not-sync direction, don't fight it
5. **Reproducibility-first evidence discipline** — falsifiable test fixture > narrative

## 3. The 5 questions

| #   | Question                                                                                               |
| --- | ------------------------------------------------------------------------------------------------------ |
| Q1  | Re-engage now / accept workaround permanent / wait N weeks                                             |
| Q2  | Re-open #3848 / fresh issue / fresh PR / Design Issue first                                            |
| Q3  | Narrative / reproducer script / failing test fixture / full fixture set / architectural brief          |
| Q4  | Lead with self-correction / acknowledge briefly mid-comment / don't mention / separate lessons-learned |
| Q5  | Design Issue first / comment-on-#3848 first / all-in-one / comment → issue if receptive → PR after     |

## 4. Vote tally + decisions

| Q   | CTO | GC  | CMO | CFO   | CSO   | CISO  | VPDR  | Tally | **DECISION**                                                    |
| --- | --- | --- | --- | ----- | ----- | ----- | ----- | ----- | --------------------------------------------------------------- |
| Q1  | a   | a   | a   | a     | a     | a     | a     | 7-0   | **(a) Re-engage now**                                           |
| Q2  | a   | a   | a   | a     | a     | a     | a     | 7-0   | **(a) Re-open #3848 + comment + failing-test fixture**          |
| Q3  | d   | d   | d   | **c** | **c** | **c** | **c** | 4-3   | **(c) Failing-test fixture (single, surgical)**                 |
| Q4  | a   | a   | a   | **b** | a     | a     | **b** | 5-2   | **(a) Lead with self-correction — ONE sentence max**            |
| Q5  | b   | d   | d   | d     | b     | **c** | d     | 4-2-1 | **(d) Comment → issue if receptive → PR after explicit signal** |

**Most-costly-to-recover-from tally:** Q4=4 (CTO, GC, CMO, CSO) · Q3=2 (CISO, VPDR) · Q5=1 (CFO). The council was most-deliberate on Q4 and Q3.

## 5. Binding constraints carried into execution

### Q3 — failing-test fixture

- Test MUST be deterministic; verify on clean checkout before posting
- Test MUST use maphew's `shouldExport` helper from #4063 (CSO binding — demonstrates we work WITH his refactor, not around it)
- Comment includes 1-2 sentence inline pointer to isolated reproducer steps (CTO binding — salvages the (d)-camp concern that test-only can be dismissed as env-specific)
- NO architectural brief, NO benchmark, NO 3-page anything

### Q4 — lead with self-correction

- ONE sentence maximum at the top of the comment (VPDR + CFO brevity binding)
- Specific phrasing: _"That close was incomplete — default-off addresses new users; it does not address explicit-opt-in users with gitignored target paths."_ (CTO + CSO precision binding)
- Pivot immediately to evidence; no mea-culpa elaboration

### Q5 — cascade sequencing

- Comment carries the failing-test fixture inline so the probe itself is falsifiable, not narrative-only (CISO integrity-incident binding)
- PR held DRAFT-ready locally on existing branch `fix/auto-export-jsonl-write-decouple`; named in the comment so maphew knows the next step is one signal away (CFO bandwidth binding)
- No pre-staged Design Issue or PR; wait for explicit maphew signal between each step (CSO + GC consent-gated binding)

## 6. Council memo cross-cutting themes (verbatim, top of each seat's memo)

| Seat      | Cross-question theme                                                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| CTO       | "maintainer-trust capital is now the rate-limiting resource, not engineering effort"                                                                 |
| GC        | "consent-gated, fixture-backed, lead with unambiguous self-correction; audit-trail integrity in 23k-star public record"                              |
| CMO       | "referendum on the narrative — operational-systems thinker bringing reproducer evidence vs AI-spam drive-by; near-optimal positioning opportunity"   |
| CFO       | "real-options-sequenced re-engagement with 4-hr cap; portfolio decision not identity-expression"                                                     |
| CSO       | "match maphew's tone not volume; tight comment + failing test + self-correction + let HIM decide sequencing; relationship not transaction"           |
| CISO      | "silent data loss on canonical IEP tracker is P1 integrity incident; falsifiable evidence in one round-trip; operator discipline is weakest control" |
| VP DevRel | "Saturday-afternoon-maintainer test: 60-word comment + 20-line failing test; enterprise-contributor cosplay is unrecoverable"                        |

## 7. Adversarial integrity check

PASS. Q3 produced a clean 4-3 split — the maintainer-empathy axis (CFO + CSO + CISO + VPDR) beat the evidence-rigor axis (CTO + GC + CMO). The split is the test that seats argued from value systems, not consensus. Q4 dissent (CFO + VPDR on placement) was substantive disagreement on form, not on substance. CISO solo-dissented on Q5 toward all-in-one for integrity-incident reasons; that minority position is preserved via the "fixture-inline-in-comment" binding constraint, which gives CISO the falsifiable-evidence-per-round-trip property they wanted even within the cascade sequence.

## 8. Implementation directives

1. Verify the bug still reproduces on `gastownhall/beads@main` (post-#4063) before drafting — CFO + CISO binding (don't claim a residual that's actually gone)
2. Author the failing test using `shouldExport` helper; deterministic, no flake
3. Draft the reopen comment per the bindings (lead one-sentence self-correction → 1-line scenario → failing-test fixture link → "PR ready on branch X" close — ~150 words max)
4. User reviews + approves before posting (per `~/000-projects/contributing-clanker/CLAUDE.md` non-negotiable rule)
5. Post comment via `gh issue comment 3848 --repo gastownhall/beads`
6. Wait for maphew signal — DO NOT escalate without it
7. On positive signal: open the existing branch as a PR per maphew's preferred shape
8. After resolution (merge OR maphew-decline): update `~/.contribute-system/candidates/gastownhall__beads__issue3848.md` status and the dossier failure log

## 9. References

- Master plan and JSONL source: `~/.claude/skills/exec-decision-council/sessions/2026-05-23-beads-reengage/session.jsonl`
- Reusable pattern: `~/.claude/skills/exec-decision-council/SKILL.md`
- Canonical prior session: `intent-eval-lab/000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md`
- Counterparty thread: <https://github.com/gastownhall/beads/issues/3848> (CLOSED, invitation to reopen on file)
- Prior PRs: #4061 (Jeremy, CLOSED), #4063 (maphew, MERGED, BASED-ON Jeremy's commit `313e1f82`)
- Local candidate: `~/.contribute-system/candidates/gastownhall__beads__issue3848.md`
- Local tracking bead: `bd_000-projects-ufc`

## 10. Acting head of board declaration

Decisions Q1-Q5 above are ratified for execution. The drafting executor (Claude) will produce the reopen comment per the binding constraints, surface to the user for approval, and POST ONLY after explicit user approval (per repo CLAUDE.md non-negotiable). This Decision Record is durable; the JSONL is source of truth; the markdown is derived.

— Jeremy Longshore (acting head of board), via Claude (drafting executor)
2026-05-23

---

## 11. EMPIRICAL ADDENDUM — verify-before-claim inverted the conclusion (2026-05-23, post-deliberation)

The Q1 unanimous council recommendation was _re-engage now_, gated on the CFO + CISO binding constraint _"verify the bug still reproduces post-#4063 before claiming residual; don't claim a residual that's actually gone."_ That gate fired and inverted the outcome. **No comment was posted upstream.** Here is what the verification produced.

### 11.1 Pre-test recon (gh queries against `gastownhall/beads`)

Reconnaissance found that maphew had shipped 5 separate auto-export hardening PRs between 2026-05-21 and 2026-05-22 — beyond the #4063 we previously knew about:

| PR        | Title                                                                                                                        |
| --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| #4063     | Make JSONL auto-export opt-in                                                                                                |
| #4087     | Guard empty auto-export over populated JSONL                                                                                 |
| #4088     | Guard auto-export against richer JSONL overwrite                                                                             |
| #4090     | Guard auto-export against JSONL-only records                                                                                 |
| #4091     | Guard JSONL auto import/export edge cases                                                                                    |
| **#4092** | **fail on auto-export git add errors (Fixes #3970)** — converts the silent-warn-on-git-add-failure path into a non-zero exit |

`#4092` (merged 2026-05-22T17:49Z, ~12 hours _before_ maphew closed #3848) was specifically expected to address the silent-failure mode we previously documented. The CISO seat's "P1 silent-data-loss" concern was the binding precondition for the test.

### 11.2 Empirical reproducer

Asciinema recording at `outputs/reproducer.cast` (34.4s, 5.4 KB). Reproducer script at `inputs/reproducer.sh`. Run against `gastownhall/beads` upstream/main @ `82020c42f` (post-#4092) AND verified against the installed v1.0.4 release `ce242a879` (same throttle behavior in both).

Reproducer steps: fresh `git init` → `.beads/` gitignored → `bd init` (defaults) → `bd config set export.auto true` + `export.git-add true` → `bd create` → inspect `.beads/issues.jsonl`.

### 11.3 What the test actually showed

| Observable                                 | Expected (our claim)    | Actual                                                                                         |
| ------------------------------------------ | ----------------------- | ---------------------------------------------------------------------------------------------- |
| `bd create` exit code                      | 0 (silent succeed)      | 0 ✓                                                                                            |
| `bd create` writes to Dolt DB              | ✓                       | ✓                                                                                              |
| `.beads/issues.jsonl` updated              | ✗ silently (the bug)    | ✗ within 60s window, ✓ after                                                                   |
| `bd` errors loudly on git-add fail (#4092) | ✓ (post-#4092 expected) | ✗ — `git add` never runs because throttle suppresses the entire `maybeAutoExport` flow first   |
| `bd export` (manual)                       | works                   | works — issues are accessible, just not written to file by default unless throttle has cleared |

`config get export.interval` returned `60s`. Operations within that window write to DB but the throttle's `shouldExport` returns false, so the entire export pipeline is skipped (the `git add` call never happens). When the throttle clears (>60s since last successful export timestamp), the next operation catches everything up — all queued issues land in the JSONL in one batch.

### 11.4 The correct framing

The previously-documented bug **"bd silently drops in-memory writes when `.beads/` is gitignored — because bd export calls git add which exits non-zero on ignored paths"** was empirically wrong. The actual behavior:

- bd's auto-export has a **60s default throttle interval** (`export.interval` config key)
- Operations within that window all exit 0 cleanly; DB persists fine
- The JSONL update is **delayed** until the next post-throttle operation, not dropped
- DB writes are **never lost**; only the JSONL representation lags within the throttle window
- The gitignored-target scenario is **not the discriminator** — same throttle behavior either way
- Maphew's #4092 (fail-on-git-add-error) addresses a **different** code path that our scenario never reaches because the throttle short-circuits before git-add runs

### 11.5 Mitigation verified

`bd config set export.interval 1s` was tested in the same reproducer:

- 3 consecutive `bd create` calls within ~1s each wrote 3 new lines to `.beads/issues.jsonl` (no throttle suppression)
- `.beads/export-state.json` advanced after each operation
- No manual `bd export → cp → bd import → backup sync` dance required

Applied to the umbrella `~/000-projects/.beads/config.yaml` on 2026-05-23. The 60s default is now overridden to 1s. The "JSONL workaround" previously documented in `intent-eval-platform/CLAUDE.md` was over-engineered for the throttle scenario; replaced with the one-line `export.interval=1s` mitigation.

### 11.6 Why the council's deliberation still has value (the durable lesson)

The 7-seat council recommended re-engaging upstream based on a premise that was empirically false. **The CFO + CISO binding constraint "verify before claim" was the gate that prevented us from posting a wrong-premise reopen on a 23k★ public repo.** Without ISEDC's adversarial-integrity discipline, the prior misstep ("default-off makes the bypass logic moot") would have been compounded by a second misstep (reopening to claim a residual that was actually a misunderstood throttle).

The council's deliberation was not wasted. It produced:

1. The **verify-before-claim gate** that caught the wrong premise (CFO + CISO)
2. The **maintainer-empathy framing** that would have shaped a good comment IF the reopen had been justified (CSO + VPDR)
3. The **AI-assistance-optics discipline** that prevented us from drafting an over-evidenced "architectural brief" we'd have regretted (Q3 majority)
4. The **lead-with-self-correction template** for future re-engagements where the residual IS real (Q4 majority)

This is the canonical example of why ISEDC exists: 6 of 7 seats independently flagged that the AI-assistance optics + prior-misstep dynamics were the rate-limiting concerns, not the engineering effort. The empirical test that those concerns demanded turned out to invert the conclusion. Council-driven discipline saved a 23k★ public-record withdrawal.

### 11.7 Post-empirical lifecycle actions taken

- **`bd_000-projects-ufc` CLOSED 2026-05-23** as `mischaracterized-actual-cause-is-throttle-interval`. Close reason references this DR + asciinema reproducer.
- **`~/.contribute-system/candidates/gastownhall__beads__issue3848.md`** status updated to `mischaracterized-by-us`; previous re-engage recommendation rescinded; failure-log lesson appended to dossier.
- **`intent-eval-platform/CLAUDE.md`** § "bd workspace + JSONL workaround" REPLACED with § "bd workspace + JSONL throttle mitigation" (3 in-file references updated).
- **NO comment posted to `gastownhall/beads#3848`.** maphew's repo state is clean; we owe him nothing further at this time.
- **`~/000-projects/.beads/config.yaml`** updated: `export.interval=1s`.

### 11.8 Status revision

- **DR 022 status: DECIDED, EXECUTED — INVERTED BY EMPIRICAL FINDING.** The Q1-Q5 decisions remain on record as the council's deliberation; the Q1-gating-constraint-on-empirical-verification fired and changed the action. This is the intended ISEDC workflow shape, not a failure of it.
- **Lesson encoded for future ISEDC sessions:** the canonical CFO+CISO verify-before-claim gate is the template for any decision cluster that depends on a counterparty's behavior model. Reuse the pattern.

— Empirical addendum authored by Claude as drafting executor, 2026-05-23
