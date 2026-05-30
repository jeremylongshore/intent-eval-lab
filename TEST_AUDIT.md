# TEST_AUDIT.md — intent-eval-lab

**Audit date:** 2026-05-29
**Auditor:** /audit-tests v7.2.0 (autonomous, single-pass)
**Branch:** main (protected — handoff requires AskUserQuestion confirmation)
**Harness:** vendored at `.audit-harness/`; `harness-hash --verify` exit 0 ✓
**Harness freshness:** vendored version unknown (no VERSION file); latest npm = 0.1.0

---

## Grade

**C+ (72/100)**

Solid L1 + L2 doc-quality + L3 unit foundation just landed. Three real P0/P1 gaps. L4+ intentionally minimal for a methodology-and-research repo.

---

## Classification

**HYBRID — primarily spec/methodology, with active Python research code.**

| Signal | Value |
|---|---|
| Markdown corpus | 123 .md files |
| Python LOC | 3065 (research/phase-a-0-baseline/scripts/* + .audit-harness vendored) |
| Real test functions | 26 (across 3 files) |
| CI workflows | 7 |
| Branch | main |

Per `references/layer-applicability.md`, this repo's applicable layers are:

- **L1** Git hooks + CI: ✓ required
- **L2** Static analysis + lint (code) + doc-quality: ✓ required
- **L3** Unit + coverage + mutation: ✓ required for the Python research code
- **L4** Integration: REQUIRED ONCE the Phase A.0 arms fire real API calls (currently waived; dry-run smoke is sufficient pre-execution)
- **L5–L7**: WAIVED — research methodology repo with no UI, no UAT, no perf-critical surface

---

## Per-layer presence

| Layer | Concern | Tool/Config | Present? | Configured? | Enforced? |
|---|---|---|---|---|---|
| L1 | Pre-commit hooks | Husky / lefthook / pre-commit.com | ✗ ABSENT | n/a | n/a |
| L1 | Staged-file filter | lint-staged / pre-commit filter | ✗ ABSENT | n/a | n/a |
| L1 | Commit-message policy | commitlint / Conventional Commits | ✗ ABSENT | n/a | n/a |
| L1 | CI pipeline | GitHub Actions | ✓ 7 workflows | ✓ | ✓ |
| L1 | Branch protection | GH branch protection | ✓ main protected | ✓ | ✓ |
| L1 | Hash-pinned policy | `.harness-hash` | ✓ 18 files | ✓ | ✓ (CI gate) |
| L2 | Code lint (Python) | ruff | partial (pyproject [tool.ruff] section exists but minimal) | partial | ✗ NOT in CI |
| L2 | Code format (Python) | ruff format / black | ✗ ABSENT | n/a | n/a |
| L2 | Type checking (Python) | mypy / pyright | ✗ ABSENT (mypy installed locally, not configured) | n/a | n/a |
| L2 | Complexity | radon / `crap-score.py` | ✗ ABSENT | n/a | n/a |
| L2 | Secret scanning | gitleaks / trufflehog | partial (GH push protection works) | n/a | n/a (push-side only) |
| L2 | Dependency vuln scan | pip-audit | ✗ ABSENT | n/a | n/a |
| **L2** | **Doc lint** | **markdownlint-cli2** | ✓ `.markdownlint-cli2.jsonc` | ✓ | advisory (continue-on-error) |
| **L2** | **Prose lint** | **Vale** | ✓ `.vale.ini` + IS Vocab | ✓ | advisory |
| **L2** | **Link integrity** | **lychee** | ✓ `lychee.toml` | ✓ | advisory |
| **L2** | **Doc formatting** | **Prettier (MD)** | ✓ `.prettierrc.json` | ✓ | advisory |
| **L2** | **Frontmatter validator** | custom JSON Schema | ✗ ABSENT | n/a | n/a |
| L3 | Unit framework | pytest | ✓ 62 passing + 1 xfail | ✓ pyproject.toml | ✓ CI workflow |
| L3 | Coverage measurement | coverage.py + pytest-cov | ✓ runs | ✗ no threshold gate | ✗ |
| L3 | Mutation testing | mutmut | ✗ ABSENT | n/a | n/a |
| L3 | Complexity gate | `crap-score.py` | ✗ NOT WIRED on Python code | n/a | n/a |
| L3 | Property-based testing | Hypothesis | ✗ ABSENT | n/a | n/a |
| L4 | Integration fixtures | testcontainers | ✗ ABSENT | n/a | waived pre-arm-execution |
| L4 | Doc-framework build | Astro/Docusaurus | n/a | n/a | n/a (no framework) |
| L5–L7 | — | — | WAIVED (research repo, no UI, no UAT) | n/a | n/a |

---

## P0 gaps (BLOCKERS — would block implement-tests handoff if any present)

**None.** The L1 + L2-doc-quality + L3 foundation is sufficient to unblock Phase A.0 execution. Items below are P1 — quality improvements, not blockers.

---

## P1 gaps (should-fix before Phase A.0 results publish)

### P1-1 — L1 pre-commit hooks absent

CI runs the gates, but engineer-side runs hit failures only after push. Cost: feedback latency, wasted CI minutes. Install lefthook or pre-commit.com framework, wire markdownlint-cli2 + ruff + vale + Prettier MD as pre-commit steps.

**Fix:** `/implement-tests` L1 playbook recipe 1 (pre-commit framework).

### P1-2 — L2 ruff has 8 unfixed errors

`ruff check research/phase-a-0-baseline/scripts/` reports 8 errors (7 auto-fixable; 1 unused-import in `_arm_common.py:130` `from dataclasses import dataclass, field as dc_field` — `dc_field` unused). Plus ruff is NOT wired into CI.

**Fix:**
1. `ruff check --fix` to apply the 7 auto-fixes
2. Manually remove the unused import
3. Add a ruff step to the `Python Tests` workflow (or a new `Python Lint` workflow)
4. Tighten `[tool.ruff]` in `pyproject.toml` to enable more rule families (E, W, F, I, B, UP, SIM)

### P1-3 — L2 mypy not configured for the project

mypy 1.18.2 is installed locally but no `[tool.mypy]` section in pyproject + no CI gate. The 2440 LOC Python suite has rich type annotations already; mypy strict-mode would catch real bugs.

**Fix:** add `[tool.mypy]` section to pyproject.toml with `strict = true` and `python_version = "3.12"`; wire `mypy research/phase-a-0-baseline/scripts/` into CI.

### P1-4 — L3 coverage gate absent + subprocess-coverage gap

Current line coverage: **20%** (vs. an unstated floor). `_arm_common.py` is 54% covered. `run-arm-a.py`, `run-arm-b.py`, `score-fixture.py`, `build-fixtures.py` ALL show 0% because tests invoke them via subprocess — coverage.py doesn't trace into subprocesses by default.

Two-part fix:
1. **Floor:** add `[tool.coverage.report]` with `fail_under = 60` to start; ratchet up.
2. **Subprocess instrumentation:** add `[tool.coverage.run] parallel = true, concurrency = ["multiprocessing"]` + a `sitecustomize.py` or COVERAGE_PROCESS_START env in CI so subprocess invocations are traced.

### P1-5 — L3 mutation testing absent

For a 2440 LOC research suite that gates a real-money decision (Phase A.0 budget approval, DR-028 P0-RATIFY-3 model choice), mutation testing would surface assertion weakness. `mutmut` is the standard Python choice.

**Fix:** `/implement-tests` L3 playbook recipe 4 (mutmut).

### P1-6 — known CostMeter bug (xfail)

Already filed as `bd_000-projects-cost-meter-bug`. Marked `xfail strict=true` so a future fix flips to pass automatically. NOT a blocker; documented.

---

## P2 advisory

- L2 dep-vuln scan (`pip-audit`) absent — research repo, low blast radius
- L2 secret scanning push-side only — GitHub push protection covers it
- L3 property-based testing (Hypothesis) — would shine on the cost-meter / exemplar-sampler / frontmatter parser
- L4 integration tests against live NVIDIA/Groq APIs — wait until Phase A.0 actually fires
- Vendored audit-harness VERSION file absent — surface a meaningful version string

---

## Doc-quality state (NEW L2 row, per taxonomy v7.2.0)

| Tool | Present | CI | Posture |
|---|---|---|---|
| markdownlint-cli2 | ✓ | ✓ | advisory (`continue-on-error: true`) |
| Vale (prose + IS Vocab) | ✓ | ✓ | advisory |
| lychee (link integrity, --offline) | ✓ | ✓ | advisory |
| Prettier (Markdown) | ✓ | ✓ | advisory |
| Frontmatter validator | ✗ | ✗ | gap — doc filing standard expects schema |
| Partner-name guard | ✓ | ✓ | hard-fail (CISO binding, separate workflow) |

**Tightening recommendation:** corpora are now visible. Follow-up PR drops `continue-on-error: true` for markdownlint + Vale + Prettier MD, after fixing existing violations (already known to fail — the gates flag what needs cleanup).

---

## Escape-scan

`bash scripts/audit-harness escape-scan --staged` → REFUSE=0 CHALLENGE=0 FLAG=0 ✓
No staged-diff threshold lowering, no policy weakening, no architectural shifts.

---

## RTM / personas / journeys

**Absent for the lab itself.** The Skill Refiner plan + DR-028 + ADR 034 stand in as the requirements traceability for the research code:

- Requirements live in plan 027 v5 (intent-eval-lab/000-docs/027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md) + DR-028 (P0-RATIFY-1..6) + DR-034 (provider amendment)
- Tests link to plan sections via docstrings (e.g., `test_smoke_runners.py` mentions DESIGN.md § 5.1)
- The 36 v7 audit-remediation beads + the 50 refiner-labeled beads ARE the open requirements list (queryable via `bd list --label refiner`)

**Recommendation:** generate `tests/RTM.md` listing the bead-id → test-file map. Low cost, high audit value when methodology is published.

---

## Decision

**Handoff to implement-tests: RECOMMENDED but not required.**

On `main` (protected), per skill protocol, the handoff prompts for user confirmation. The 6 P1 gaps are real but tractable:

| Gap | Effort | Blocks Phase A.0 execution? |
|---|---|---|
| L1 pre-commit | 30 min | no |
| L2 ruff fixes + CI wire | 20 min | no |
| L2 mypy config + CI wire | 20 min | no |
| L3 coverage gate + subprocess fix | 45 min | no |
| L3 mutation testing | 1 hour | no (low ROI on research code) |
| Bd cost-meter bug fix | 5 min | no |

Total: ~2.5 hours to clean up P1. Phase A.0 arms can fire today regardless.

**Status:** AUDIT CLEAN AT P0. P1 cleanup advisable but not blocking. Suggest implement-tests handoff to land the L1 + L2 (code) + L3 coverage gate triad as one PR.
