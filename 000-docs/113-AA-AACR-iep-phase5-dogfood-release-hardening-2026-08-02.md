# After-Action / Acceptance Record — IEP Phase 5 Dogfood and Release Hardening

**Date:** 2026-08-02
**Plan:** `IEP-EVAL-EVOLUTION-001`
**Parent bead:** `bd_000-projects-htjt.4`
**GitHub issue:** [intent-eval-lab#260](https://github.com/jeremylongshore/intent-eval-lab/issues/260)
**Plane:** `LAB-105`
**Lab branch:** `feat/iep-eval-evolution-blueprint`

## Outcome

The cross-repo dogfood path is exercised end to end. A deterministic generic
fixture ran through J-Rig's immutable Run, named Grade, and unified-report
path. A real MiniMax-M3 evaluation of the pinned `audit-tests` skill produced
the new `j-rig/skill-promotion/v1` metadata. The rollout consumer accepted the
bundle as structurally valid and blocked promotion because the result was
advisory and regression comparison was not run. The dashboard rendered the
generic report internally and continued to refuse the public destination.

This is a release-hardening acceptance, not a claim that the sample skill is
promotion-ready.

## Generic substrate receipt

The tracked reproduction is
[`sandboxes/2026-08-02-iep-phase5-dogfood`](../sandboxes/2026-08-02-iep-phase5-dogfood).
It uses a shell-free Node harness and deterministic `answer-checker@1.0.0`.

- Raw Run: `raw_14a6b85edcc974734b0fbaeecf7968a58fc47df76ca06f4c1df6720a866b79dd`
- Repeat Run: same sealed ID, `reused: true`
- Grade: `grade_8be8c72bd182c2a1044ea0906ca66e51d5dc7bebdac0346e354a36172b9b070d`
- Grade verdict: `pass`, score `1.0`
- Grader snapshot: `sha256:5aaacc8f48da3d2728defc5d57f1445f179de1c4d17a34816f0b25a6d6ad2200`
- Unified report: one cell attempted, completed, and graded; one pass; zero
  harness failures; zero ungraded cells.

The report is a local projection, not a signed evidence bundle.

## Real-provider promotion receipt

The source roster was pinned to
`claude-code-plugins-plus-skills@a9dd5c02a3793412ed35525efd460b399554be13`.
The provider key was supplied process-only from the encrypted local provider
store; it was not written to the repository, output bundle, or report.

Durable evidence:
[`evidence/phase5-dogfood/audit-tests-minimax-m3.bundle.json`](../evidence/phase5-dogfood/audit-tests-minimax-m3.bundle.json)

- Bundle SHA-256:
  `a3b409f7534d2b33c1d21b1df1086c5c2851ca1454a388ceb8ac3cfdbe2e0344`
- Skill: `audit-tests` version `7.2.0`
- Skill snapshot:
  `sha256:aeb76ce683432ff44c6718db23a75afca65fd5bbd843615788203a98395c2eef`
- Eval run: `019fc1a1-845b-7077-8d63-fba909b7579b`
- Provider/judge: `minimax` / `MiniMax-M3`
- Selected grader: `j-rig-binary-criteria@0.2.0`
- Grader snapshot:
  `sha256:53f396c7e29b4898a1c0f70baf214fceeac3927728f72ecb52ce6b70ebca6089`
- Result: `3/5`, pass rate `0.6`, decision `warn`
- Provider failures: `0`
- Promotion metadata: `j-rig/skill-promotion/v1`
- Thresholds: `fail` (`required_pass_rate: 1`, `observed_pass_rate: 0.6`)
- Regression: required, disabled, `not-run`
- Promotion eligible: `false`

The live rollout action consumed this bundle and returned a non-failing block
because `fail-on-block=false`:

```text
decision=block
skill promotion row at index 0: predicate gate_decision must be pass (got advisory)
```

That block is the expected fail-closed boundary. The sample is not represented
as a passing promotion.

## Dashboard and workflow receipts

- Dashboard report consumer: [PR #68](https://github.com/jeremylongshore/intent-eval-dashboard/pull/68)
- CLI separator hardening: [PR #70](https://github.com/jeremylongshore/intent-eval-dashboard/pull/70),
  tracked by child bead `bd_000-projects-htjt.4.2`, GitHub issue #69, and
  Plane `LAB-106`
- Verified signed ingest: [workflow run 30734349474](https://github.com/jeremylongshore/intent-eval-dashboard/actions/runs/30734349474)
- Deploy: [workflow run 30734361333](https://github.com/jeremylongshore/intent-eval-dashboard/actions/runs/30734361333)

The dashboard's documented `pnpm run generate:eval-report -- ...` invocation
now works, the direct Node invocation remains compatible, and a `site`
destination is still refused. The existing signed ingest rendered 14 J-Rig
rows and deployed successfully; the generic dogfood report also rendered in a
temporary internal destination.

## Related implementation receipts

- J-Rig producer evidence contract: [PR #266](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/266)
- Rollout consumer compatibility: [PR #59](https://github.com/jeremylongshore/intent-rollout-gate/pull/59)
- Audit-harness promotion metadata: [PR #145](https://github.com/jeremylongshore/intent-audit-harness/pull/145)
- MiniMax provider documentation and prior real-run record: [J-Rig PR #262](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/262)

Each implementation branch was kept isolated, committed with a conventional
message and plan/bead/repo/evidence footer, pushed, and opened as a draft PR.

## Tri-link cleanup receipt

The initial release-hardening run printed 76 tri-link findings. Investigation
showed that 54 of those were false positives caused by the verifier grepping
the wrapped human `bd show` display; three open bead descriptions were
genuinely missing the required fields. The cleanup completed the actual debt:

- lab verifier fix: [PR #262](https://github.com/jeremylongshore/intent-eval-lab/pull/262),
  commit `1663ddae2ab317efbab8943cd87665917135bc55`;
- J-Rig document headers: [PR #267](https://github.com/jeremylongshore/j-rig-skill-binary-eval/pull/267),
  commit `060bb2ce465836f72e07cf1801b06afe09c523af`;
- three genuinely incomplete bead descriptions received Doc/GitHub fields
  and were pushed to Dolt;
- eight open spec-drift issues (#250–#257) received Bead/Doc footers and
  comments, while the older tri-link umbrella issue #79 was read first and
  left intact;
- six legacy Skill-Refiner documents received the required `Beads:` headers;
- the workspace-level `scripts/validate-trilink.sh` run with both feature
  worktrees mounted at their canonical sibling paths returned `PASS — zero
tri-linkage violations`.

The cleanup child is `bd_000-projects-htjt.4.3`, GitHub [#261](https://github.com/jeremylongshore/intent-eval-lab/issues/261),
and Plane `LAB-107`.

## Acceptance and remaining release controls

Accepted for the cross-repo hardening bead:

- generic Run → Grade → report lineage is reproducible;
- real provider output is represented by a kernel-valid promotion bundle;
- rollout consumes and fails closed on non-promotion evidence;
- dashboard rendering and public-destination policy are verified;
- raw credentials, transcripts, and local databases remain uncommitted.

Validation notes:

- `python3 -m pytest -q`: 322 passed, 1 expected failure.
- `scripts/audit-harness verify`: pass.
- JSON/YAML syntax checks and the vendor-generic partner-name guard: pass.
- CI-scoped Ruff check/format for `research/phase-a-0-baseline`: pass. A
  broader optional scan of untouched `scripts/` files still exposes 35
  pre-existing findings; no unrelated lint cleanup was folded into this
  slice.
- `scripts/validate-trilink.sh`: workspace-level pass after the parser fix and
  cross-repo header/footer repairs; zero violations.

Still release-gated:

- merge order and CI for the stacked draft PRs;
- a broader real-skill shortlist and regression baselines;
- human approval for the tailnet/public route;
- review of the intentionally preserved dirty dashboard artifacts and the
  unrelated lab seed fixture.
