---
title: Skill Refiner 3-layer hook architecture — sinker / line / hook (L1 / L2 / L3)
category: AT-ARCH
date: 2026-06-21
authors:
  - Jeremy Longshore (Intent Solutions, acting head of board)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Plan 027 v5 § 4 Phase B (RATIFIED 2026-05-27); DR-028 (ISEDC Session 7)
inherits_from: 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md
filing_standard: Document Filing Standard v4.4
bead: bd_000-projects-rqwk (RC-IEL)
related_drs:
  - 027-PP-PLAN (THE PLAN — § 2 product structure, § 2.5 SkillMD fold-in, § 4 Phase B 3-layer hook table, § 6.5 ASCII catalog D1/D3)
  - 028-AT-DECR (ISEDC Session 7 — Skill Refiner plan ratification; AC-13 RefinerStrategy interface; Phase D anti-goal)
forward_refs:
  - 014-DR-GLOS-canonical-glossary.md (Skill Refiner + 3-layer hooks glossary entries)
  - 083-AT-SPEC-skill-refiner-pass-v1-normative-spec-2026-06-17.md (skill-refiner-pass/v1 predicate)
---

# Skill Refiner 3-layer hook architecture — sinker / line / hook

> **State label: NORMATIVE.** This document faithfully records the **already-decided** 3-layer hook
> design ratified in plan 027 v5 § 4 Phase B (ISEDC Session 7, DR-028, 2026-05-27). It does not
> invent mechanism. Where the plan is precise, this document restates it; where the plan leaves a
> layer's responsibility thin, this document marks the open detail explicitly rather than inventing
> it. When this document and plan 027 § 4 conflict, **the plan wins** — this is a reference rendering
> of the plan's Phase B architecture, not an independent authority.

## 0. Scope and authority

The **Skill Refiner** is the IMPROVE stage of the Intent Solutions 3-product agent-rig stack
(J-Rig Skill Binary Eval → Skill Refiner → Rollout Gate). It is delivered as a Claude Code plugin
whose **delivery mechanism inside Claude Code is three hook layers** named — Intent-Solutions-side —
**sinker / line / hook** (L1 / L2 / L3). The naming is a fishing-rig metaphor: the **sinker** drops
fast and anchors the rig (the cheap deterministic check), the **line** carries the catch
(end-of-turn rollout capture and background refinement), and the **hook** sets the catch (the
commit-time agentic gate that can actually block).

The 3-layer design is lifted in shape from Anthropic's `security-guidance` plugin pattern — "spawn a
separate model call from a hook, feed findings back to the session" — and IS-renamed per plan 027
Architectural Commitment AC-8. Per DR-010 § 13.6 (external-pattern non-borrow), the cited pattern
informed the design space but does not dictate it; the architecture below is IS-native.

This document carries:

- **§ 1** — the 3-product stack context (plan 027 § 6.5 diagram D1).
- **§ 2** — the three layers in detail: hook event, trigger, responsibility, what each gates/emits.
- **§ 3** — the L3 = `PreToolUse:Bash` correction (the v4.1 mechanism fix), stated explicitly so this
  document cannot reintroduce the `PostToolUse:Bash` bug.
- **§ 4** — the end-to-end flow diagram (skill edit → hooks → eval / evidence), plan 027 § 6.5 D3
  corrected to the ratified L3 mechanism.
- **§ 5** — the plugin CLI surface the layers sit alongside.
- **§ 6** — open details the plan does not fully pin (marked, not invented).

**Binding sources** (read these first; this document is downstream of them):

| Source                                                                              | What it binds                                                                 |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` § 4 Phase B    | The 3-layer hook table — the normative per-layer mechanism.                   |
| Plan 027 § 4 revision-history v4.1 entry                                            | The `PostToolUse:Bash` → `PreToolUse:Bash` L3 correction.                     |
| Plan 027 § 6.5 D1 + D3                                                              | The source ASCII diagrams (D3's L3 label is corrected here per the v4.1 fix). |
| `028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md` | ISEDC Session 7 ratification; AC-13 RefinerStrategy; Phase D anti-goal.       |

---

## 1. Where the hooks sit — the 3-product agent-rig stack

The Skill Refiner is the middle product. The hooks are how its refine loop runs inside Claude Code
without the user invoking anything; the explicit CLI (§ 5) is the manual escape hatch.

```text
┌──────────────────────────────────────────────────────────────────────┐
│         INTENT SOLUTIONS — AGENT-RIG STACK (3 products)               │
└──────────────────────────────────────────────────────────────────────┘

   ┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
   │  J-Rig Skill Binary    │    │   Skill Refiner        │    │   Rollout Gate         │
   │  Eval     (shipped)    │───▶│   (this build)         │───▶│   (in flight M5)       │
   │                        │    │                        │    │                        │
   │  TEST                  │    │  IMPROVE               │    │  SHIP                  │
   │  7-layer harness       │    │  bounded SKILL.md      │    │  GitHub Action         │
   │  rollouts → scores     │    │  edits, gated by       │    │  evidence + policy     │
   │                        │    │  score deltas          │    │  → ship / no-ship      │
   └─────────┬──────────────┘    └─────────┬──────────────┘    └─────────┬──────────────┘
             │                              │                             │
             │ ScoreRecord                  │ SkillVersion +              │ verdict +
             │                              │ skill-refiner-pass/v1       │ Evidence Bundle
             ▼                              ▼                             ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │       EVIDENCE BUNDLE  (intent-eval-core canonical schema, 14 entities)  │
    └─────────────────────────────────────────────────────────────────────────┘
```

The three hook layers all live in the one plugin (`claude-code-plugins/plugins/productivity/j-rig/`)
and produce the `SkillVersion` value + the `skill-refiner-pass/v1` row that the stack converges on.

---

## 2. The three layers

The Refiner's hook layers are ordered cheapest-first by escalating cost tier and escalating
authority. The cheap deterministic check fires on every SKILL.md edit; the model-calling layers fire
less often; the only layer that can **block** fires at the latest, most-consequential moment (the
commit/push).

### 2.1 Sinker (L1) — per-edit deterministic gate

| Property                | Value                                                                                                                                                                                                           |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hook event**          | `PostToolUse:Edit/Write` matched on `SKILL.md` files                                                                                                                                                            |
| **Trigger**             | Every Edit/Write tool call whose target path is a `SKILL.md`                                                                                                                                                    |
| **Responsibility**      | Run `/validate-skillmd` Tier 2 — the deterministic frontmatter checks (per AC-11: the agentskills.io open-standard layer + the Claude Code extension layer, each pinned to a local snapshot). No model call.    |
| **What it gates/emits** | Does **not** block. On failure it **appends a warning to the session context** so the author sees the spec violation immediately. It anchors the rig — catches malformed frontmatter the moment the edit lands. |
| **Cost tier**           | `$0` — no model invocation.                                                                                                                                                                                     |
| **Model**               | none (deterministic).                                                                                                                                                                                           |

`PostToolUse` is the correct event for L1 precisely because L1 is **advisory, not blocking**: it runs
after the edit to inspect the result and surface a warning. It has nothing to prevent — the edit is a
file write the author intends. (Contrast L3, § 2.3, where the whole point is to prevent a `git
commit`/`git push` from happening, which forces `PreToolUse` — see § 3.)

### 2.2 Line (L2) — end-of-turn rollout capture + background refine

| Property                | Value                                                                                                                                                                                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hook event**          | `Stop` (end of turn)                                                                                                                                                                                                                                  |
| **Trigger**             | A turn ends in which a skill was invoked AND j-rig has scored its rollouts                                                                                                                                                                            |
| **Responsibility**      | Append the scored rollout to the append-only event log `.j-rig/refiner/log.jsonl`. After N rollouts accumulate on a skill, fire the Refiner loop **in the background** and surface the resulting candidate `SkillVersion` in the next turn's context. |
| **What it gates/emits** | Does **not** block. Emits a candidate edit proposal (the next-turn surfaced candidate) and grows the rollout log. The accept/reject decision uses the multi-dimensional strict-improvement gate (`accept()`) from `@j-rig/refiner-core`.              |
| **Cost tier**           | `$` — Haiku for rollout scoring, Sonnet for the refine pass (per AC-5: Opus is reserved for final validation only, never per-pass scoring or proposing).                                                                                              |
| **Model**               | Haiku (score) + Sonnet (refine).                                                                                                                                                                                                                      |

L2 is the carrier line: it captures behavioral signal as the author works and runs the bounded-edit
propose-and-accept loop out of band, so a refinement candidate is ready by the next turn without
interrupting the author.

### 2.3 Hook (L3) — commit-time agentic gate (the only blocking layer)

| Property                | Value                                                                                                                                                                                                                                                                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hook event**          | **`PreToolUse:Bash`** with matcher `git commit \| git push`                                                                                                                                                                                                                                                                       |
| **Trigger**             | A `git commit` or `git push` Bash command is about to run AND the staged diff modifies a `SKILL.md`                                                                                                                                                                                                                               |
| **Responsibility**      | Run the agentic gate: read the surrounding skills directory, check the proposed edit against the rejected-edit buffer (regression guard), and optionally shadow-validate against the held-out eval set.                                                                                                                           |
| **What it gates/emits** | **CAN BLOCK.** `PreToolUse` is in the Anthropic hooks "Can block" allowlist — it blocks via exit code 2 or `permissionDecision: deny`. On a regression it blocks the commit/push (or annotates the PR); on pass it lets the Bash run and triggers the **Evidence emit** (signed AAR markdown + HTML projection, Rekor log entry). |
| **Cost tier**           | `$$` — Opus for the agentic gate, rate-limited per the security-guidance pattern.                                                                                                                                                                                                                                                 |
| **Model**               | Opus.                                                                                                                                                                                                                                                                                                                             |

L3 sets the catch: it is the single layer with the authority to stop a bad SKILL.md from being
committed or pushed, and it is the layer that emits the signed evidence on a clean pass.

### 2.4 Summary — the three layers at a glance

| Layer           | Event                                        | Blocks?                 | Cost | Model          | One-line role                                               |
| --------------- | -------------------------------------------- | ----------------------- | ---- | -------------- | ----------------------------------------------------------- |
| **Sinker (L1)** | `PostToolUse:Edit/Write` on `SKILL.md`       | No (warns)              | `$0` | none           | Deterministic frontmatter check; anchors the rig.           |
| **Line (L2)**   | `Stop` (end of turn)                         | No                      | `$`  | Haiku + Sonnet | Capture rollouts, run background refine, surface candidate. |
| **Hook (L3)**   | **`PreToolUse:Bash`** `git commit\|git push` | **Yes** (exit-2 / deny) | `$$` | Opus           | Commit-time agentic regression gate; emits signed evidence. |

---

## 3. The L3 = `PreToolUse:Bash` correction (READ THIS)

**L3 fires on `PreToolUse:Bash`, NOT `PostToolUse:Bash`.** This is the v4.1 mechanism fix recorded in
plan 027 § 4 revision history and is binding.

The reason is mechanical, not stylistic:

- A `PostToolUse:Bash` hook fires **after** the Bash command has already executed. By the time it
  runs, the `git commit` (or `git push`) has **already happened**. A `PostToolUse:Bash` hook
  therefore **cannot prevent** the very commit/push that triggered it — the block is impossible
  because the action is already done.
- A `PreToolUse:Bash` hook fires **before** the Bash command runs and is in Anthropic's hooks
  "Can block" allowlist. It blocks via **exit code 2** or `permissionDecision: deny`, which actually
  stops the commit/push from executing.

Because L3's entire purpose is to **gate** the commit/push of a SKILL.md regression, it **must** use
the event that can prevent the action. That event is `PreToolUse:Bash`. The correct mechanisms for an
L3-class gate are, in order of preference:

1. **`PreToolUse:Bash`** matcher on `git commit | git push` (the ratified choice) — blocks via exit-2
   / deny.
2. As a non-blocking fallback where blocking is undesirable: **decision-pattern annotation +
   Evidence emit** — let the action proceed but record the finding into the Evidence Bundle and
   annotate the PR. (This is the degraded mode, not the default.)

> **Anti-pattern — do not reintroduce.** `PostToolUse:Bash` for L3. It looks superficially correct
> ("run after the commit to check it") but it fires too late to block, so the regression ships. Plan
> 027's § 6.5 D3 catalog diagram historically carried a stale `PostToolUse: Bash` label on L3; the
> authoritative source is the § 4 Phase B table (`PreToolUse:Bash`), and the diagram in § 4 below is
> corrected to match.

---

## 4. End-to-end flow — skill edit → hooks → eval / evidence

This is plan 027 § 6.5 diagram D3, **corrected** so the L3 row reads `PreToolUse: Bash` per § 3
above (the plan's catalog rendering of this diagram still showed the pre-fix `PostToolUse: Bash`
label; the binding § 4 Phase B table is `PreToolUse:Bash`, and this is the canonical rendering).

```text
   CLAUDE CODE LIFECYCLE                  REFINER LAYER          COST TIER    MODEL
   ════════════════════════════════════════════════════════════════════════════════

   PostToolUse: Edit/Write on SKILL.md  →  ┌─────────────┐
                                           │  SINKER L1  │       $0          (none)
                                           │  deterministic    drops fast
                                           │  validate-     ─── anchors rig
                                           │  skillmd Tier 2│
                                           └──────┬──────┘
                                                  │ pass?
                                                  ▼ (warning to context if fails; never blocks)

   Stop  (end of turn)                  →   ┌─────────────┐
                                           │  LINE   L2  │       $           Haiku (score)
                                           │  rollout       fires refiner    Sonnet (refine)
                                           │  capture +     after N rollouts
                                           │  bg refiner   │
                                           └──────┬──────┘
                                                  │ proposal accepted? (strict-improvement gate)
                                                  ▼ (candidate surfaced next turn; never blocks)

   PreToolUse: Bash matches             →   ┌─────────────┐
   git commit | git push                    │  HOOK   L3  │       $$          Opus
   on staged SKILL.md diff                  │  agentic gate  rate-limited
   (the v4.1 correction:                    │  + rejected-   sets the catch
    PreToolUse CAN block; PostToolUse        │  edit buffer +
    fires too late to prevent the commit)    │  shadow eval  │
                                            └──────┬──────┘
                                                   │ regression?  ── yes ──▶ BLOCK (exit-2 / deny)
                                                   ▼ no (clean pass)
                                          ┌─────────────────┐
                                          │  Evidence emit  │  signed AAR (md)
                                          │  + Rekor log    │  + HTML projection
                                          └─────────────────┘
                                                   │
                                                   ▼
                                          skill-refiner-pass/v1 Evidence Bundle row
```

Reading the flow: an author edits a SKILL.md → **L1** validates it instantly and warns on spec
violations (no block) → at end of turn **L2** captures scored rollouts, and after enough rollouts
runs the background refine loop and surfaces a candidate → when the author tries to `git commit` /
`git push` a SKILL.md change, **L3** runs the Opus agentic gate; on a regression it **blocks** the
commit, and on a clean pass it emits the signed `skill-refiner-pass/v1` evidence (markdown AAR + HTML
projection + Rekor log entry).

---

## 5. The CLI surface the hooks sit alongside

The hooks make refinement ambient; the explicit plugin CLI is the manual path (the commands users
invoke directly). Both share the same `@j-rig/refiner-core` loop.

| Command                           | Role                                                                                                 |
| --------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `/j-rig refine bootstrap <skill>` | Create the initial held-out eval set for a skill.                                                    |
| `/j-rig refine propose <skill>`   | Run one Refiner pass manually (the L2 loop, on demand).                                              |
| `/j-rig refine shadow <skill>`    | Run a candidate `SkillVersion` in shadow mode against the eval set.                                  |
| `/j-rig refine promote <skill>`   | Promote a candidate → main — **human-gated** (AC-4: the Refiner never auto-writes SKILL.md on main). |
| `/j-rig refine status <skill>`    | Show the trajectory, budget, and rejected-edit buffer.                                               |

The plugin command path is `/j-rig` (the Refiner ships through j-rig's existing engineering home);
the **user-facing brand is "Skill Refiner."** The promotion step is the single-signer audit-trail
control (AC-9): the hooks and CLI **propose**; a human + acting CTO **dispose**.

---

## 6. Open details the plan does not fully pin (marked, not invented)

Per the scope note in the banner, where plan 027 § 4 Phase B leaves a layer's mechanism thin, this
document records the gap rather than inventing a value. These are deferred to the Phase B
implementation PR (`bd_000-projects-jsy3`, RC-IAJ plugin + hooks epic), not resolved here:

1. **L2 rollout threshold `N`.** The plan says "after N rollouts on a skill: fire the refiner in
   background" but does not pin `N`. **OPEN** — a Phase B tuning parameter; the implementation
   chooses a default and exposes it as plugin config.
2. **L3 matcher exact regex.** The plan gives the matcher as `git commit | git push`; the precise
   compiled regex (e.g. handling `git push --force`, aliases, `&&`-chained commands) is **OPEN** and
   belongs to the hooks.json implementation, which `/validate-hook` checks to confirm the regex
   compiles.
3. **L3 shadow-validation: optional vs default.** The plan marks shadow-validation against the
   held-out set as "(optional)". Whether the default L3 gate runs shadow validation, or only the
   rejected-buffer regression check (deferring shadow to the explicit `/j-rig refine shadow`
   command), is **OPEN** — a cost/latency tradeoff for the Phase B PR.
4. **L3 block-vs-annotate policy surface.** § 3 names two L3 mechanisms (block via exit-2, or
   annotate-and-emit). Which one is the default, and whether it is per-repo configurable, is
   **OPEN** for Phase B.

Each open item is a Phase B decision, not an architecture change. The architecture — three layers,
the events (`PostToolUse:Edit/Write` / `Stop` / **`PreToolUse:Bash`**), the cost ladder, the
single-blocking-layer property, and the human-gated promotion — is RATIFIED and binding per plan 027
v5 § 4 and DR-028.

---

## Cross-references

- **Plan 027** (`027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md`) — § 2 product
  structure, § 2.5 SkillMD open-standard fold-in, § 4 Phase B (the normative 3-layer hook table),
  § 6.5 ASCII catalog (D1 stack, D3 hook flow). **THE PLAN; this document is downstream of it.**
- **DR-028** (`028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md`) —
  ISEDC Session 7 ratification, AC-13 RefinerStrategy interface, Phase D anti-goal.
- **DR-010** (`010-AT-DECR-isedc-council-session-4-widened-scope-2026-05-13.md`) — § 13.6
  external-pattern non-borrow (the security-guidance pattern informs, does not dictate).
- **skill-refiner-pass/v1 spec** (`083-AT-SPEC-skill-refiner-pass-v1-normative-spec-2026-06-17.md`) —
  the predicate the L3 Evidence emit produces.
- **Canonical glossary** (`014-DR-GLOS-canonical-glossary.md`) — Skill Refiner, 3-layer hooks
  (sinker/line/hook), SkillVersion, ScoreRecord, EditProposal terminology.
- **Anthropic hooks reference** (`https://code.claude.com/docs/en/hooks`) — the ~30-event allowlist,
  the "Can block" set (`PreToolUse` is in it; `PostToolUse` is not), and exit-code-2 / `deny`
  blocking semantics — the source of the § 3 correction.
