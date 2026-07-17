# 110 · AT · SPEC — Coordination design: gating marketplace skill PRs on eval results without disturbing the bespoke CCPI CI

**Date:** 2026-07-16
**Status:** DESIGN — coordination proposal only. **This document changes no CI anywhere.**
**Bead:** "Draft the coordination design for gating marketplace skill PRs on eval results without disturbing the bespoke CCPI CI" (umbrella workspace; child of the epic "Give the rollout gate its first real enforcement teeth")
**Refs:** `jeremylongshore/intent-audit-harness#127` (parent issue), `intent-audit-harness#128` (the enforcing-precedent flip), j-rig-skill-binary-eval PR #215/#218/#220 (nightly roster + flap sidecar)
**Related docs:** 080 (eval economics), 106 (CI/CD + j-rig cross-repo remediation), j-rig `ci/emit-evidence/flap-report.ts`

---

## 1. Problem

Skill PRs merge into the marketplace (`claude-code-plugins-plus-skills`, "CCPI") on **static validation only**: the `ci-required` aggregate (schema validators, shellcheck, scan-synced-content, marketplace validation, etc.) plus `gitleaks`. Nothing in the merge path asks _"does this skill behave correctly?"_

Behavioral evidence already exists — the j-rig nightly roster (`j-rig-skill-binary-eval/.github/workflows/nightly-skill-evals.yml`) runs `j-rig eval` over 8 marketplace skills with hand-authored `eval-spec.yaml` files (3 in the coreweave pack, 5 in the databricks pack), 5-sample majority voting on a cheap provider (MiniMax-M3 default since 2026-07-17; DeepSeek before), signs one kernel `gate-result/v1` row per skill, and publishes to the `evidence-latest` rolling prerelease. But that evidence **gates nothing in the marketplace**: it runs against a _pinned_ roster commit on the nightly schedule, after merge, invisible to the PR author. A skill can regress behaviorally, merge green, and the regression only shows up (unsigned-off, unattributed) in the next nightly.

The standing rule for CCPI is **study + coordinate, never bolt on** — its CI is bespoke and load-bearing. This document is the study + the coordination proposal.

## 2. What the CCPI CI actually is (studied 2026-07-16, read-only)

Facts that constrain any design:

1. **The merge gate is exactly two required contexts: `ci-required` + `gitleaks`.** `ci-required` (in `validate-plugins.yml`) is a single aggregate job that `needs:` 19 gated jobs and runs on **every** PR with no path filter — deliberately, to kill the "N Expected forever" stuck-PR class (#778). Its documented invariant: _never add to its `needs:` a job that can skip for an undesigned reason_, or a real gate gets silently bypassed by a green aggregate.
2. **`auto-bump-on-pr.yml`** fires on every PR touching `plugins/**` or `packages/**` and commits a patch-version bump back to the PR head branch. Known gotcha (#985): with `GITHUB_TOKEN` the bump commit becomes head SHA but fires no `pull_request: synchronize`, so required checks never re-run and the PR stalls in `action_required` forever. Escape: `[skip auto-bump]` in the PR title or body. **Any automation-authored PR touching `plugins/**`must carry it.** Also: a lane keyed on the PR head SHA must expect the head to move under it (the minimax lane handles this with per-PR`concurrency`+`cancel-in-progress`).
3. **Supply-chain scanner** (`scan-synced-content` job → `scripts/scan-allowlist.txt`): CHALLENGE/FLAG findings on dual-use patterns are waived by a reviewed, path-scoped `path:rule  reason` line in the allowlist — the sanctioned fix; REFUSE is never waivable. Relevant if the eval lane's docs or fixtures introduce dual-use text.
4. **The advisory-lane pattern already exists and works: `minimax-review.yml`.** Header verbatim: _"ADVISORY ONLY — never a required check, never in `ci-required`'s needs, never blocks a merge."_ It runs on `pull_request` (NOT `pull_request_target`), with a same-repo guard (`github.event.pull_request.head.repo.full_name == github.repository`) so **fork PRs never receive the provider secret**, a repo-variable kill switch (`ENABLE_MINIMAX_REVIEW`), per-PR concurrency, and sticky PR comments. The new eval lane should be a sibling of this shape, not a new invention.
5. **`MINIMAX_API_KEY` already exists as a CCPI repo secret** (the minimax-review lane uses it). The recommended provider therefore needs **zero new secret plumbing**; `DEEPSEEK_API_KEY` would be an addition (note: the DeepSeek account on our key is currently unfunded — roster comment, 2026-07-17 — which is why MiniMax-M3 is the working default).
6. **`emit-evidence.yml`** is the additive-evidence precedent inside CCPI itself: push-to-main only, never a PR status context, kernel-validated `gate-result/v1` rows, cosign-signed, published to `evidence-latest`. Signing lives on `main`, not on PRs.
7. **Eval-spec coverage is 8 skills** at `plugins/saas-packs/{coreweave,databricks}-pack/skills/*/eval-spec.yaml` — hand-authored specs (the roster refuses scaffold-only specs). The other 400+ plugins have no spec. Any design must be honest about that coverage.

## 3. Design options

### Option (a) — advisory-first PR eval lane · **RECOMMENDED**

A new, purely additive workflow in CCPI (working name `skill-eval-advisory.yml`), cloned structurally from `minimax-review.yml`:

- **Trigger:** `pull_request` on `plugins/**` paths. Job-level guards: same-repo only (fork safety, § 5), kill-switch repo variable (e.g. `ENABLE_SKILL_EVAL`), per-PR concurrency with cancel-in-progress.
- **Scope:** detect changed skill directories in the PR diff; run only those that carry a hand-authored `eval-spec.yaml`. No spec-covered skill changed → the job no-ops green (a _designed_ skip).
- **Engine:** `@intentsolutions/jrig-cli` (version-pinned dev install), `j-rig eval <skill> --spec <skill>/eval-spec.yaml --provider minimax --models MiniMax-M3`, 5-sample majority voting — the exact configuration the nightly roster runs.
- **Decision:** feed the resulting `gate-result/v1` row through `@intentsolutions/rollout-gate` (the same published decision library the enforcing audit-harness dogfood lane delegates to) with a committed policy file.
- **Surface:** post/refresh a sticky PR comment via the `@j-rig/pr-comment` renderer (marker-anchored, idempotent). Decision + per-criterion tally + provider + sample count + a "this is advisory" banner.
- **Not required, not signed:** never in `ci-required`'s `needs:`, never a branch-protection context, and **no cosign signing in the PR lane** — PR-lane runs evaluate untrusted-ish, unmerged content and are not roster-pinned provenance; signed evidence stays a `main`-only, nightly concern (matches both `emit-evidence.yml` and the nightly roster's design).

**Cost + latency (real data, not projection):** nightly run 29549429404 (2026-07-17) evaluated the full 8-skill roster — 5 samples each, plus a 22k-file checkout, workspace build, and signing — in ~26 minutes wall-clock, i.e. ~3 min/skill amortized; a PR lane touching 1–2 skills lands in the **~3–8 min** band including setup. Provider spend on MiniMax-M3/DeepSeek-class pricing is **single-digit cents per skill per eval** (5 samples × judge calls on a cheap model). This is noise next to CCPI's existing CI wall-clock and effectively free next to reviewer time.

### Option (b) — graduation criteria to a required check

Mirror the audit-harness precedent exactly (`rollout-gate-dogfood.yml`: started advisory with `continue-on-error` + `fail-on-block: 'false'`; flipped to `fail-on-block: 'true'` + intended-required after a consistently green run history, 2026-07-16/17, `intent-audit-harness#128`). Graduation preconditions — **all** of them, none waivable:

1. **≥ 4 weeks advisory** operation on real PRs with the lane enabled.
2. **Flap rate below threshold on the affected skills:** zero unexplained gate-decision flips for the spec-covered skills over the trailing 14 nightly flap reports (`flap-report.json` sidecar), and no PR-lane verdict that contradicts the same-night nightly verdict for an unchanged skill. A flapping verdict is disqualifying by construction (§ 4).
3. **Operator sign-off: Jeremy approves the flip.** Not the CCPI session, not this platform.

**Mechanics of the flip when (and only when) approved:** the eval lane becomes its **own** branch-protection status context — it is _never_ folded into `ci-required`'s `needs:`, because a path-scoped, provider-dependent job violates `ci-required`'s no-undesigned-skip invariant (a provider outage would read as a skip and green the aggregate). As its own context it must always-report (run on every PR, internally no-op-green when no spec-covered skill changed) — the same lesson `ci-required` itself encodes from #778. **The flip therefore changes the trigger**: option (a)'s `paths: plugins/**` filter is removed at graduation and the spec-covered-skill detection moves inside the job (path filter while advisory = cheap; always-report once required = mandatory — the two shapes are sequential, not contradictory). Escape hatch mirrors the precedent: revert one workflow file + remove one branch-protection context.

### Option (c) — spec-coverage rule

A skill **without** an `eval-spec.yaml` is **exempt** from the lane (nothing to run) but the PR gets a visible label (e.g. `no-eval-spec`) so exemption is observable rather than silent. No block, no nag-comment storm — 8 of 400+ plugins have specs today, so exemption is the overwhelmingly common case and must stay cheap. Growing spec coverage is authoring work (per-pack, hand-authored — the roster's own bar), not CI work, and is out of scope here.

**Recommendation: (a) now, (b) as the pre-agreed graduation path, (c) as the coverage posture.** Advisory-first is the only defensible opening move given the flap record below.

## 4. Judge nondeterminism — why advisory-first is mandatory, not cautious

The empirical record, night one of the roster (2026-07-17), **same pinned skill corpus, same specs, same provider**, runs 29545349026 → 29549429404:

- `databricks-cluster-forensics`: 0/11 advisory → **11/11 pass**
- `coreweave-gpu-cost-leak-hunter`: advisory → **fail (7/10)** — in rollout-gate terms, the verdict swung from would-SHIP-territory to BLOCK with zero input change.

That flip is exactly why the flap sidecar exists (j-rig PR #220): _"a permanent signature must not ride a noisy verdict."_ The same principle transfers verbatim to gating: **never require (and never sign) on a flapping verdict.** Handling, in order:

1. **Multi-sample majority per criterion** (5 samples — already the CLI + roster default) as the first-line de-noising mechanism. Note honestly: the 2026-07-17 flips occurred _with_ 5-sample majority in place, so multi-sampling narrows but does not eliminate flap.
2. **Flap-report data as the graduation instrument**: the nightly `flap-report.json` sidecar is the longitudinal record; the most recent comparison shows 8 compared / 0 flipped, which is encouraging but is one data point, not four weeks.
3. **Advisory comments state their uncertainty**: the PR comment carries the sample count, provider, and criteria tally so a maintainer reads "9/10 on MiniMax-M3, 5-sample majority," not a false-precision verdict.
4. **A required check (option b) inherits all of this**: if the trailing flap window ever regresses after graduation, the correct response is demotion back to advisory (revert the one workflow file), never threshold-loosening.

**Where the deterministic wall sits** (probabilistic-boundary discipline): the LLM judge never authors the gate decision directly. Judge outputs land as per-criterion **binary** verdicts, de-noised by the 5-sample majority; the decision over those verdicts is the deterministic `decideRollout()` contract in `@intentsolutions/rollout-gate` (blocker fails block, sacred regressions block, all-pass ships), and the PR comment is rendered deterministically from that decision. What remains probabilistic is the per-criterion verdict itself — which is exactly what the flap instrument measures and what §§ 3(b).2 gates graduation on. Signing is out of the PR lane entirely; the nightly roster's signing of judge-derived rows is pre-existing platform behavior with its own integrity control (the flap sidecar exists precisely because a signature must not ride a noisy verdict) and is not modified by this design.

## 5. Hard boundaries (non-negotiable in any implementation)

1. **Never weaken `ci-required` or `gitleaks`** — no removals from `needs:`, no threshold changes, no path-filter additions to either. The eval lane is additive alongside them.
2. **Additive workflow only.** One new workflow file; zero edits to `validate-plugins.yml`, `auto-bump-on-pr.yml`, the scanner, or branch protection (until an approved option-b flip, which touches branch protection only to _add_ one context).
3. **`[skip auto-bump]` discipline**: any automation-authored PR that touches `plugins/**` (including eval-spec additions or the lane's own fixtures) carries `[skip auto-bump]` in the body, or the PR wedges in `action_required` (#985). A workflow-only PR doesn't match auto-bump's path filter, but the discipline costs nothing — include it anyway.
4. **Secrets as repo secrets**: `MINIMAX_API_KEY` (already present), `DEEPSEEK_API_KEY` (add only if/when the account is funded). Never echoed, never in logs, never in artifacts.
5. **Fork-PR safety — provider keys must NEVER reach fork PRs.** `pull_request` trigger (never `pull_request_target` with secrets), plus the same-repo guard the minimax-review lane uses: `github.event.pull_request.head.repo.full_name == github.repository`. Fork PRs skip cleanly (no red X on an external contribution); if fork coverage is ever wanted, it is a separate design with a separate threat model — not a follow-up tweak.
6. **No signing in the PR lane** (§ 3a). Signed `gate-result/v1` evidence remains a `main`-ref, nightly-roster concern.
7. **Scanner waivers, if any, go through `scripts/scan-allowlist.txt`** as reviewed, path-scoped lines with reasons — never by weakening a detection pattern.

## 6. Sequencing and decision rights

| Step | What                                                                                                                                                                                                                                                                                            | Who decides / executes                                                                      |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1    | This design doc lands in `intent-eval-lab`; linked from `intent-audit-harness#127`                                                                                                                                                                                                              | This platform session (this PR)                                                             |
| 2    | Coordination handoff: CCPI session/owner reads this doc + confirms or amends the lane shape against current CCPI CI state                                                                                                                                                                       | **CCPI session/owner** — they own the workflow addition; nothing lands in CCPI without them |
| 3    | Prerequisite the platform owes: a consumable PR-comment renderer. `@j-rig/pr-comment` is a **workspace-internal package, not published to npm** — either publish it under `@intentsolutions/*` or bundle the renderer into `@intentsolutions/jrig-cli` before the lane can be built as designed | This platform (j-rig repo)                                                                  |
| 4    | Advisory lane ships in CCPI (option a), kill-switch off by default, enabled by the owner                                                                                                                                                                                                        | CCPI session/owner                                                                          |
| 5    | ≥ 4-week advisory soak; flap window tracked via the nightly sidecar + PR-lane history                                                                                                                                                                                                           | Observed by both; no one "decides" anything here                                            |
| 6    | Required-check graduation (option b)                                                                                                                                                                                                                                                            | **Jeremy, explicitly.** Neither session may flip it                                         |

**Division of labor:** this platform provides the eval CLI (`@intentsolutions/jrig-cli`), the decision library (`@intentsolutions/rollout-gate`), the evidence contract (`gate-result/v1` in `@intentsolutions/core`), the flap instrumentation, and this design. CCPI provides the workflow, the secrets wiring, and the operational judgment about its own repo.

## 7. What this document does NOT authorize

- **No CI changes anywhere** — not in CCPI, not in j-rig, not in audit-harness — on the basis of this doc alone.
- No new workflow file in CCPI until the CCPI session/owner has taken up the coordination handoff (§ 6 step 2).
- No branch-protection change of any kind; no required-check flip without Jeremy's explicit approval (§ 6 step 6).
- No publishing of `@j-rig/pr-comment` without its own PR + review in the j-rig repo.
- No eval-spec authoring campaign across the marketplace; spec coverage grows pack-by-pack on its own merits.
- No fork-PR eval coverage.

This doc is the _study + coordinate_ artifact the CCPI standing rule requires. The next concrete action belongs to the CCPI session, not this one.
