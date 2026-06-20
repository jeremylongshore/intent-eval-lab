# Evaluating a real Claude Code plugin with the Intent Eval Platform

**Doc:** 088-RR-LAND · **Date:** 2026-06-20 · **Status:** LANDED
**Subject:** the first end-to-end external-adopter run of the Intent Eval Platform convergence — a real, independently-published Claude Code plugin evaluated by the platform, start to ship/no-ship decision.

---

## TL;DR

We took a real, independently-useful Claude Code plugin — [`beads-dolt`](https://github.com/jeremylongshore/beads-dolt), a Dolt/DoltHub-aware workflow for the [beads](https://github.com/gastownhall/beads) (`bd`) task tracker — and ran it through the Intent Eval Platform end to end:

> **audit-harness** (deterministic gates) → **j-rig** (behavioral eval, real model) → **kernel** (`gate-result/v1` Evidence Bundle validation) → **intent-rollout-gate** (ship / no-ship).

This is the first time both the deterministic *and* behavioral halves of the platform emitted Evidence Bundles that a single rollout gate consumed, on one shared external artifact. It worked — and, more usefully, **the eval found a real bug in the platform itself**: the deterministic gate's CLI evidence emitter produced predicate bodies that were *not* valid against the platform's own kernel schema, so the rollout gate (correctly) refused the bundle. We fixed it, the rollout gate flipped from `block` to `allow`, and the fix is merged.

A platform that can only validate things it was built to bless is a rubber stamp. A platform that runs on a real external artifact and catches a flaw in its own seams is doing its job.

---

## 1. What was evaluated

[`beads-dolt`](https://github.com/jeremylongshore/beads-dolt) (Apache-2.0) is a Claude Code plugin that upgrades the `bd` task-tracker workflow with awareness of its [Dolt](https://github.com/dolthub/dolt) / [DoltHub](https://www.dolthub.com) storage backend. It packages a skill, five expert agents, and a wired [`dolthub/dolt-mcp`](https://github.com/dolthub/dolt-mcp) server. It was built independently of this platform and is genuinely useful on its own — which is exactly what makes it a fair test subject rather than a staged demo.

It builds on, and credits, two open-source projects: **beads** (the `bd` task tracker) and **Dolt / DoltHub** (the version-controlled SQL database that is `bd`'s backend). This case study evaluates the plugin with our own tooling; it does not modify either upstream.

## 2. The methodology

The platform is four repositories that converge on a shared **Evidence Bundle** schema — every validator, deterministic or behavioral, emits a kernel-defined `gate-result/v1` row, and a thin rollout gate turns the accumulated rows plus a policy into a ship/no-ship decision.

| Stage | Tool | Role |
|---|---|---|
| 1 | `audit-harness` | Deterministic gates: classify the artifact, conform it against bundled schemas, scan for secrets/hygiene. Emits `gate-result/v1` rows. |
| 2 | `j-rig` | Behavioral eval: run the skill against a spec of binary criteria with a **real model provider**, judge each criterion, emit a rollout decision row. |
| 3 | kernel (`@intentsolutions/core`) | The single source of truth for what a valid `gate-result/v1` predicate body *is*. Every emitted row must validate against `GateResultV1Schema`. |
| 4 | `intent-rollout-gate` | Consume the combined bundle + a policy (`required_gates`, `forbid_decisions`) → **ship / no-ship**. |

The convergence claim is only real if a bundle emitted by stage 1 and stage 2 actually validates at stage 3 and is consumable at stage 4. Nobody had run that full loop on a real external artifact before.

## 3. The run

**Stage 1 — deterministic gates.** `audit-harness classify` detected the plugin's composite nature (agent + marketplace + mcp + skill). `conform` validated the skill frontmatter, the five agents, the MCP config, and the plugin manifest against bundled schemas — **8 PASS / 1 ADVISORY**, zero failures. `scan` confirmed **no secrets** (gitleaks) and clean links/readme.

**Stage 2 — behavioral eval (real model).** We authored an `eval.yaml` for the skill — binary criteria like *"does the response identify a missing Dolt remote as the no-visibility root cause"*, *"does it recommend the `bd dolt remote add` + push fix"*, *"does it correct the rapid-write-race misconception rather than confirm it"*, and an adversarial prompt-injection case. `j-rig eval` ran it against a real provider (DeepSeek), not a stub — genuine behavioral ground truth.

**Stage 3 — kernel validation.** Every emitted row was checked against the kernel's `GateResultV1Schema`.

**Stage 4 — rollout decision.** The bundle plus a policy went to `intent-rollout-gate`, which returned a decision.

## 4. The findings

The run produced three findings. Reporting all three honestly — including the one that was our own fault — is the point.

### Finding 1 — a real bug in the platform (the headline)

When we assembled the deterministic Evidence Bundle and handed it to the rollout gate, the gate returned **`block`** — and the reason was not the plugin. It was that **every row in the bundle failed the kernel's `gate-result/v1` schema.**

The deterministic gate's CLI evidence emitter wrapped each gate row in an in-toto Statement whose `predicateType` declared `gate-result/v1` — but the predicate *body* was an older, partial shape (`result`, `timestamp`, …) rather than the kernel's canonical body (`gate_decision`, `gate_name`, `gate_version`, `gate_reasons`, `coverage`, `policy_ref`, `evaluated_at`, …). The kernel schema forbids extra keys, so it rejected the legacy fields outright. The two ends of the convergence were not speaking the same row shape.

This had stayed invisible because the gate's own regression suite validated its post-emit output against a *stale local fixture* that matched the legacy shape — a fixture that had drifted from the kernel schema it claimed to mirror. The suite was green against the wrong oracle. Only an end-to-end run against the *real* kernel surfaced it.

### Finding 2 — a fixable gap in the plugin

The behavioral eval caught the skill front-loading *diagnosis* without delivering the *fix*: for the canonical "my beads aren't showing in DoltHub" prompt, a one-shot response ran the diagnostic commands and stopped before recommending the remote-add + push. We fixed the skill to lead with the root cause **and** the two-command fix.

### Finding 3 — an eval-authoring lesson

`j-rig` applies every criterion to every test case as a full matrix; per-case criteria scoping is not subtractive. Dolt-specific criteria judged against an off-topic control prompt naturally failed, inflating the raw failure count. A real lesson for anyone authoring eval specs: criteria must be globally applicable, or the matrix noise must be expected and read accordingly.

## 5. The platform bug, fixed — the seam closed

The fix brought the deterministic gate's CLI emitter to parity with the platform's *internal* self-gate emitter, which already produced kernel-valid rows: map the legacy verdict to `gate_decision`, the timestamp to `evaluated_at`, and synthesize the remaining canonical fields. Crucially, we also split the test fixtures — a partial input-envelope schema for the gate emitters' raw rows (which are partial by design, before augmentation) and a full-kernel schema for the *post-emit* predicate — and repointed the regression so it now validates against the real kernel shape. The suite went from masking the drift to gating against it.

**The result, on the exact same chain that returned `block`:**

| | Before | After |
|---|---|---|
| Emitted rows valid against `GateResultV1Schema` | 0 / 9 | **9 / 9** |
| `intent-rollout-gate` decision | `block` | **`allow`** |
| Deterministic gate suites | green against a stale fixture | green against the kernel schema |

The fix is merged ([`intent-audit-harness#103`](https://github.com/jeremylongshore/intent-audit-harness/pull/103)) with full CI green and independent AI review addressed.

## 6. Honest maturity notes

- The deterministic gates, the **real-provider** behavioral eval, kernel validation, and the rollout decision all run today, locally.
- The behavioral stage used a real model (DeepSeek), not a stub. Stub mode exists for first-plumbing; the numbers here are genuine.
- The **signed-to-production-transparency-log** path is intentionally *not* exercised here. It is gated on a DNS pre-condition and is irrelevant to a local quality gate. Evidence here is unsigned; the decision logic is identical.

## 7. What this proves

1. **The convergence is real, not aspirational.** Deterministic *and* behavioral validators emitted Evidence Bundles that the same rollout gate consumed, on one shared external artifact, end to end.
2. **The kernel is load-bearing.** It is the thing that caught the seam — the rollout gate refused a bundle precisely because the rows did not match the canonical contract. A weaker design would have shipped the drift.
3. **The platform survives contact with a real artifact.** It found a flaw in its own plumbing and a gap in the subject, and the fixes were concrete and verifiable.

## 8. Reproduce

The plugin, its eval spec, and the full evidence-and-decision record are public in the [`beads-dolt`](https://github.com/jeremylongshore/beads-dolt) repository (`DOGFOOD.md`). The deterministic gates, the `j-rig` eval, kernel validation, and the rollout decision all run locally; the only external dependency is a model-provider key for the behavioral stage.

## Credits

Built on and grateful to two open-source projects: **[beads](https://github.com/gastownhall/beads)** (the `bd` task tracker) and **[Dolt](https://github.com/dolthub/dolt) / [DoltHub](https://www.dolthub.com)** (the version-controlled SQL database), with the **[`dolthub/dolt-mcp`](https://github.com/dolthub/dolt-mcp)** server for SQL access. The plugin builds on their public work; this evaluation is our own.
