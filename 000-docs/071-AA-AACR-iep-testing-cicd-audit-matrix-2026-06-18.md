# IEP Testing + CI/CD Posture Audit Matrix (5 repos)

> Repo × layer testing/CI-CD posture audit across the five Intent Eval Platform repos, with per-repo grades, a severity-ranked cross-repo gap list, and a trust → enforcement → coverage remediation sequence.

## Repo × Layer Testing Matrix — Intent Eval Platform (5 repos)

| Repo                    | L1 hooks/CI | L2 static | L3 unit | L4 integration | L5 system | L6 e2e/accept | L7 RTM/personas |
| ----------------------- | ----------- | --------- | ------- | -------------- | --------- | ------------- | --------------- |
| **intent-eval-core**    | present     | present   | present | present        | waived    | waived        | waived          |
| **intent-eval-lab**     | present     | partial   | partial | partial\*      | waived    | waived        | absent          |
| **audit-harness**       | partial     | present   | partial | present        | present   | partial       | absent          |
| **j-rig-binary-eval**   | present     | partial   | present | present        | partial   | absent        | absent          |
| **intent-rollout-gate** | partial     | present   | present | present        | present   | absent        | absent          |

\* intent-eval-lab L4 = strong offline-deterministic self-test backbone (ci.yml 45 hard-fail `--check`/`--self-test` invocations), but real provider integration deferred until Phase A.0 arms fire. Waivers in core (L5/L6/L7) are documented + correct for a pure-type contracts library.

## Per-Repo Grade + Verdict

| Repo                    | Grade  | One-line verdict                                                                                                                                                                                                                                              |
| ----------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **intent-eval-core**    | **A-** | Best-in-class for a pure-type kernel (1040 tests, live 100% coverage, sigstore-signed releases); held off A only by stale TEST_AUDIT.md and 3 load-bearing CI workflows left advisory (non-required).                                                         |
| **audit-harness**       | **A-** | Eats its own dogfood well (17-job CI, self-pinned hash, signed evidence emit), but two iah-\* beads were closed with **fabricated/future-dated evidence** that doesn't match the tree, plus no self-coverage and no self tests/TESTING.md.                    |
| **intent-rollout-gate** | **B+** | Solid L2-L5 for a thin-shell action (17 green tests, 3 required CI gates); real gaps are governance hygiene — **materially stale SECURITY.md** (over-claims signature verification) and a **vacuous empty-`.harness-hash` gate** that enforces nothing.       |
| **j-rig-binary-eval**   | **B**  | Production-grade L1-L4 (451 tests, earned + hash-pinned coverage floor) but thin at the top — **no TEST_AUDIT.md, no e2e self-eval** of the very CLI it ships, vendored arch/crap/bias gates unwired.                                                         |
| **intent-eval-lab**     | **B-** | Strong deterministic spec-self-test backbone, but **enforcement is broken**: only 2 required checks; all of lint/mypy/coverage-floor/partner-name-guard/schema-drift run `continue-on-error` or non-required, so nothing code- or doc-quality blocks a merge. |

## Cross-Repo Prioritized Gap List (severity-ranked, highest-value first)

**P0 — Audit-trail integrity & enforcement holes (fix first):**

1. **[audit-harness · HIGH · process]** Two beads (`iah-dependabot-polyglot`, `iah-bash-floor`) closed with **fabricated, future-dated evidence** ("PR #69 merged 2026-06-18") that contradicts the working tree (no pip/cargo in dependabot.yml; no `BASH_VERSINFO` guard anywhere). **Reopen both beads or land the real changes** — a tool that mandates evidence-based closure cannot itself carry false closures.
2. **[intent-eval-lab · HIGH · L1]** Only 2 required status checks on `main`; **partner-name-guard + schema-drift — both enforcing binding ISEDC decisions (DR-004, DR-018) — are NOT required** and `enforce_admins:false`. Add both to required checks + enable enforce_admins.
3. **[intent-eval-lab · HIGH · L2/L3]** Entire code-quality layer (`ruff`/`mypy`/`pytest` with `fail_under=60`) runs `continue-on-error:true` and is non-required — **CI coverage is ~40% below the declared floor with zero consequence**. Promote pytest to a blocking required check; drop `continue-on-error` on ruff+mypy after a one-time cleanup.
4. **[intent-rollout-gate · HIGH · L1]** The required `audit-harness verify` gate is **vacuous**: `.harness-hash` is 0 bytes, nothing is pinned, verify returns OK against an empty manifest. Run `audit-harness init` to pin the real policy surface (action.yml, ci.yml, vitest.config.ts, fail-closed source).
5. **[intent-rollout-gate · HIGH · L7/security-doc]** `SECURITY.md` is **materially stale and over-claims** — describes signature verification + Stage-1 row verification as _implemented_ when `src/run.ts` does none of it (deferred per DR-002 §6.3); still calls shipped v0.1.0 "pending." Rewrite to describe actual v0.1.0 behavior; mark signing/Rekor as deferred.

**P1 — Missing top-of-taxonomy coverage on the eval engines:**

6. **[j-rig-binary-eval · HIGH · L6]** **No e2e/acceptance test drives the `j-rig` CLI against a real fixture SKILL.md** and asserts a binary pass/fail verdict (`cli/index.test.ts` is export-existence; smoke is `1+1`). The tool that evaluates skills has no test proving it evaluates a skill — highest-value missing layer for the product.
7. **[j-rig-binary-eval · HIGH · L7]** **No `TEST_AUDIT.md` exists** despite the 2026-05-01 baseline doc explicitly committing to produce one via `/audit-tests`. The mandated diagnostic artifact was never generated (this very bead was created to do so).

**P2 — Dark/unwired gates + supply-chain breadth:**

8. **[j-rig-binary-eval · MEDIUM · L2]** Vendored `arch`/`crap`/`bias`/`gherkin` harness scripts are installed but **never invoked** by any CI/hook/script — present-but-dark, catching nothing. Wire them into CI.
9. **[intent-eval-core · MEDIUM · L1]** Four PR-triggering workflows (changelog-observance, coverage-map-gates, doc-quality, prose-anchor-validity) are **non-required** — a red result doesn't block merge. Add the load-bearing ones (coverage-map-gates, prose-anchor-validity, changelog-observance) to required checks.
10. **[intent-eval-core · MEDIUM · documentation]** Committed `TEST_AUDIT.md` is **two versions stale** (claims v0.1.0/8 files/154 tests vs actual v0.6.0/37 files/1040 tests). Re-run `/audit-tests`, refresh TEST_AUDIT.md + tests/TESTING.md.
11. **[audit-harness · MEDIUM · L2]** `dependabot.yml` covers only github-actions + npm; the **python/ (PyPI) + rust/ (crates) polyglot wrappers get no dep-update/vuln coverage**. Add pip + cargo ecosystems. _(Same root cause as P0 #1.)_
12. **[intent-rollout-gate · MEDIUM · L2]** **No dependabot.yml and no CodeQL** — despite SECURITY.md promising weekly dependabot once a runtime locked (now locked), and this repo sitting at the highest-leverage supply-chain position (every adopter's deployment-decision tier). Add both.
13. **[audit-harness · MEDIUM · L7]** **No self-coverage instrumentation and no self `tests/TESTING.md`** — the tool enforces a coverage floor + TESTING.md on every consumer but holds itself to neither. Dogfooding gap.

**P3 — Hardening + DX polish (low severity):**

14. **[j-rig-binary-eval · MEDIUM · L3]** **No mutation testing** (no Stryker) — coverage proves lines execute, not that assertions catch faults; for a binary-verdict engine, mutation is the natural next gate.
15. **[audit-harness · MEDIUM · L2]** **No bash version-floor guard** — scripts use bash-4+ features (`mapfile`/assoc arrays) but no `BASH_VERSINFO` check; macOS bash-3.2 users get cryptic failures. _(Same root cause as P0 #1.)_
16. **[intent-rollout-gate · MEDIUM · L2]** **No coverage tooling/floor** on a ~2-file fully-testable surface — cheap, high-value gate to add (`vitest --coverage` v8 + TESTING.md floor).
17. **[intent-eval-lab · MEDIUM · L3/L1]** 15 load-bearing `scripts/*.py` spec-projection tools have **no pytest** (only embedded `--self-test` mixing test logic into prod code); vendored harness is **3 patches behind** (v1.1.5 vs npm 1.1.8). Extract tests to a real suite; re-vendor + re-pin.
18. **[intent-eval-core · LOW · L4/L1]** SemVer api-extractor gate relies on a fragile two-step `continue-on-error`+re-fail pattern; escape-scan is **pre-commit-only (bypassable via `--no-verify`)**, never CI-enforced. Make `api:check` blocking; add a CI escape-scan range step.
19. **[cross-repo · LOW · docs]** Pervasive **CLAUDE.md / doc drift** — j-rig CLAUDE.md still says MIT (actually Apache-2.0) + version.txt-canonical + auto-bump-releases (all wrong); intent-rollout-gate has `v0.2.0` code comments on a v0.1.0 release. Reconcile in each repo's next touch.

## What to Fix First

Sequence the work by **trust → enforcement → coverage**:

1. **Restore audit-trail trust (today).** Reopen the two audit-harness beads closed on fabricated future-dated evidence (P0 #1), and land the real dependabot-polyglot + bash-floor changes. A false closure in the _enforcement tooling itself_ poisons every downstream audit claim — fix this before anything else.
2. **Close the "green CI that enforces nothing" holes (this sprint).** intent-eval-lab's non-required guards (P0 #2/#3) and intent-rollout-gate's vacuous empty-`.harness-hash` gate (P0 #4) are the most dangerous class of gap: they signal safety while blocking nothing. Make the binding-decision guards (partner-name, schema-drift) and the harness-hash pin actually required.
3. **Fix the security-doc-vs-behavior lie (this sprint).** intent-rollout-gate's SECURITY.md over-claiming signature verification (P0 #5) is a deployment-decision-tier misrepresentation — cheap to fix, high blast radius if a downstream adopter trusts it.
4. **Then add the one test that matters most for the product (next).** j-rig's missing CLI e2e self-eval (P1 #6) — the eval engine has no test proving it evaluates a skill. Pair it with generating the overdue TEST_AUDIT.md (P1 #7).
5. **Sweep the cheap doc/version drift (rolling).** TEST_AUDIT refreshes (core, j-rig, lab) and CLAUDE.md license/version corrections ride along on each repo's next touch.

**One-line takeaway:** the platform's _test logic_ is strong (core A-, harness A-); the systemic weakness is **enforcement and audit-trail integrity** — non-required guards, a vacuous hash gate, an over-claiming security doc, and two beads closed on fabricated evidence — so the first wave should harden what's already written before adding new tests.
