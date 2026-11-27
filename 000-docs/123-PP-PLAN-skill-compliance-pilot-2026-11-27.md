---
title: Skill compliance pilot — evidence before enforcement
date: 2026-11-27
status: INFORMATIVE
state_label: INFORMATIVE
bead: bd_000-projects-4jc7x
---

> **State label: INFORMATIVE.** Bounded implementation plan and evaluation method; no new binding platform policy.

# Skill compliance pilot: evidence before enforcement

Implementation scope: pilot. Task authority: `bd_000-projects-4jc7x`, mirrored
in [lab issue 421](https://github.com/jeremylongshore/intent-eval-lab/issues/421).
This document records the bounded implementation plan and evaluation method;
Beads owns delivery state and verification receipts.

## Purpose and ownership

Measure whether a skill's required reads, checks and report actually occurred,
then apply host-specific workflow decisions to those measurements. Evaluate
agent adherence, detector quality and output correctness separately. A passing
process receipt cannot establish that a skill produced a correct answer.

| Repository                        | Implementation responsibility                                                                                        |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| intent-eval-lab                   | Evidence semantics, evaluation design, rollout criteria and limitations.                                             |
| intent-audit-harness              | Read-only deterministic verifier of versioned operational policy and local receipts; existing gate-result/v1 output. |
| j-rig-skill-binary-eval           | Opt-in Claude Code collector/hooks, one explicit pilot skill, actual subprocess replay and recovery tests.           |
| intent-eval-core                  | Existing canonical contracts remain authoritative; no contract adoption or new assertion kind in this pilot.         |
| intent-rollout-gate and dashboard | Existing evidence boundaries remain applicable; no gate enrollment, report publication or policy promotion.          |

The harness's `audit-harness/skill-gates/v1` and
`audit-harness/skill-gate-receipt/v1` are experimental operational protocols.
They do not replace EvalSpec, SkillEvalSpec, Requirements, Evidence Bundles, or
the pending kernel adoption work tracked by core issues 90 and 113. There is no
new predicate URI, signed envelope, canonical entity or automatic release.

## Execution sequence and acceptance

First implement and test the deterministic verifier in audit-harness. It checks
strict policy shape, explicit file inventory, session and workspace identity,
required reads, command completion/counts and current checklist reporting.
Exercise actual emitted rows through the existing bundle append boundary.

Then pin the reviewed verifier commit and exact source digest in J-Rig's CI.
The collector imports that implementation instead of duplicating policy
semantics. It executes only explicitly authored argv, records evidence privately,
and connects UserPromptSubmit, PreToolUse, PostToolUse and Stop to one pilot.
The pilot is activated only by its explicit slash prompt or manual begin action;
skill matching and tool-driven invocation are not silently inferred.

Deliver each repository through feature branches and required CI. Keep the
source-only pilot opt-in, with observe mode as the committed default. Runtime
tests use local fixtures and real subprocesses without model/API spend. Execute
the documented manual workflow as a smoke test. Record source commits, test
commands, CI, PRs, Git and Dolt synchronization on the bead. No global hook
installation or enforce-mode rollout is part of completion.

## What each observation establishes

| Requirement | Evidence accepted                                                                                                                                                  | Limit                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Read        | Collector emits all bytes of each required file and records its current digest.                                                                                    | Access is observable; comprehension is not.                                          |
| Run         | Collector launches the declared argv without a shell and observes completion, zero exit, positive minimum passing-test count, zero failed tests and output digest. | Authored commands/count reporters must be reviewed; exit zero alone is insufficient. |
| Report      | Structured checklist receipt and an emitted current gate-result row.                                                                                               | The assistant's final prose is not inspected or certified.                           |
| Freshness   | Session/root, policy bytes, declared inputs, existing file arguments, resolved executables, Python and collector/verifier bytes match.                             | Environment values, undeclared inputs and external services remain unbound.          |

Every rerun revokes prior success durably before process launch. Timeout,
interruption, output overflow, nonzero exit, missing tools, missing/zero test
counts, malformed JSON and changed inputs cannot become a clean result. A
policy/source/tool change requires new reads, checks and reporting. The default
verifier is advisory; its `--strict` mode is independent of host policy mode.

State is scoped to workspace, policy path and session, locked and atomically
written. Files are private to the user. Logs contain event names, findings and
block decisions, excluding prompts, file bodies and command output. Retention
is bounded and operator-managed. Same-user alteration remains possible: these
are trusted local receipts, not independent execution attestations.

## Failure and detector evaluation

The verifier corpus exercises missing, malformed, duplicate-key and stale
evidence; invalid counts and command statuses; path traversal and symlinks;
every identity component; unavailable executables; advisory/strict results;
and pass/advisory/fail compatibility with the existing bundle boundary.

J-Rig replay exercises the complete observe and enforce paths, exact tool
denial in both modes, unrelated sessions, source/policy changes, failed reruns,
nonzero/zero-test/malformed output, timeout, overflow, interrupted subprocess
cleanup, missing or altered provider/configuration/state, repeated Stop and
recovery. A PostToolUse success claim alone cannot satisfy a command gate.
Fixture success validates these cases; it is not an estimate of production
false-positive or false-negative rates.

Review actual logs using evaluated Stop events as the opportunity denominator,
with session and skill as cohort dimensions. Count unmet opportunities, blocked
opportunities and explicit activations separately. Follow each session's
sequence to measure retry recovery; repeated stops are correlated observations.
Obtain false-block and missed-violation labels through independent review and
counterexample replay. Measure hook latency alongside these rates. Raw weekly
skip counts without opportunity counts are not comparable.

Before enforcement promotion, review representative successful tasks, omitted
steps, tool failures, edits after testing and recovery attempts. Confirm that
expected denial and positive-requirement decisions agree with independent
labels, and that ordinary tasks incur no gate. Document unresolved cases and
observed latency. No arbitrary number of quiet days or synthetic test passes
automatically authorizes promotion. Review the policy diff explicitly and keep
an exact rollback procedure.

## Host decisions and rollback

Observe mode records unmet positive requirements without blocking Stop.
Enforce mode returns exit 2 until evidence is complete. Explicit denied tool
names block PreToolUse in both modes while the pilot is active. This is a
workflow restriction; equivalent shell/network capabilities are not sandboxed.
PostToolUse is observational and cannot undo effects. Configuration/runtime
errors return exit 2 visibly; host-specific failure semantics still apply.

Repeated Stop invocations with incomplete evidence remain blocked, including
`stop_hook_active`; the host owns its retry limit. A user interruption may skip
Stop entirely. Disabled/missing hooks, host timeouts and alternate execution
surfaces limit coverage. Do not describe hooks as impossible to bypass.

Rollback removes only these pilot handlers and the installed pilot skill,
preserving existing project hook arrays and private receipts. Returning an
enforce policy to observe is a reviewed policy change and invalidates old
evidence. No global settings, production service or release must be changed.

## Upstream grounding

The [Agent Skills specification](https://agentskills.io/specification) defines
skill packaging and progressive disclosure; it does not standardize this gate
policy. The [Claude Code hook reference](https://code.claude.com/docs/en/hooks)
defines event payloads, exit-code decisions and failure semantics. The collector
is a host adapter over the local verifier, not a claim of portable hook behavior.

The motivating article's reported skipped-step count and implementation files
were supplied as a user summary. They are not independently reproduced results
of this pilot. Existing platform requirements and tests remain authoritative.
