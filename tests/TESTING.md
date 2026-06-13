# TESTING.md — intent-eval-lab Testing SOP (spec-repo light)

**Repo class:** HYBRID — primarily a spec / methodology / research repo, with a
contained Python research surface (`research/phase-a-0-baseline/`).
**SOP authority:** Intent Solutions Testing SOP (`/audit-tests` + `/implement-tests`
+ `@intentsolutions/audit-harness`). This file is the per-repo policy instance.
**Last audit:** `/audit-tests` v7.2.0 → `TEST_AUDIT.md` (repo root). Grade at audit:
C+ (72/100); P0-clean, P1 cleanup tracked.

This is the spec-repo-_light_ flavor of the SOP. The full 7-layer taxonomy
(git hooks → static → unit → integration → system → E2E → acceptance) is scoped
down here: a methodology repo that ships specs, Decision Records, and a small
research codebase does **not** carry a UI, a UAT surface, or a perf-critical
hot path, so L5–L7 are waived. What remains is enforced for real.

---

## 1. Layer applicability (the 7-layer taxonomy, scoped to this repo)

| Layer | Concern | Applies here? | How it is satisfied |
| --- | --- | --- | --- |
| **L1** | Git hooks + CI | ✅ required | `.pre-commit-config.yaml` (local) + 11 GitHub Actions workflows (CI). `.harness-hash` pins the enforcement surface. |
| **L2** | Static analysis + lint | ✅ required | **Code:** ruff lint/format + mypy (`python-tests.yml`, advisory-tightening). **Docs:** markdownlint-cli2 + Vale + lychee + Prettier-MD (`doc-quality.yml`). **Workflow YAML:** yamllint + actionlint (`lint.yml`). |
| **L3** | Unit + coverage | ✅ required for the Python research code | pytest (62 tests) + subprocess-aware coverage + Codecov (`python-tests.yml`). |
| **L4** | Integration | ⏸ deferred until arms fire real API calls | Phase A.0 arms run dry-run/self-test offline today; live-API integration tests land when the arms actually call NVIDIA/Groq/etc. |
| **L5** | System | ⛔ waived | No deployed system surface — this is a spec + research repo. |
| **L6** | E2E | ⛔ waived | No UI / no end-user flow. The "E2E" of a spec repo is the deterministic CI self-test suite (see § 4). |
| **L7** | Acceptance / UAT | ⛔ waived | Requirements traceability is carried by the Decision Records + bead slate, not a UAT harness (see § 6). |

**Rule of thumb for this repo:** every _normative artifact_ (schema, drift-class
row, projection.json, predicate spec) must have a deterministic, offline CI
check that fails when it drifts from its source. Prose (DRs, Blueprints, glossary,
AARs) is governed by ISEDC + doc-quality, not by a freshness gate.

---

## 2. The vendored-harness rule (non-negotiable)

Enforcement travels _with the code_. This repo does **not** reference any
`~/.claude/` path from a hook or workflow.

- The audit-harness is **vendored** at `.audit-harness/` (snapshot of
  `@intentsolutions/audit-harness` v1.1.5; `PROVENANCE` records the source commit).
- The wrapper `scripts/audit-harness` dispatches to `.audit-harness/scripts/*`.
- `.harness-hash` pins the load-bearing files; `.harness-hash-extra-patterns`
  declares the pin scope (CI workflows, schema redirect stubs, the vendored
  harness scripts + wrapper, the classifier-walls policy surface, this extras
  file itself).
- `harness-hash-verify.yml` runs `scripts/audit-harness verify` on every PR +
  push to main. **Exit 2 (HARNESS_TAMPERED) blocks the PR.**

### When a pinned file legitimately changes

A deliberate edit to any pinned file (e.g., a CI workflow, including adding a new
one — `.github/workflows/*.yml` is a glob) requires re-initializing the manifest
**in the same reviewed commit**:

```bash
scripts/audit-harness init
git add .harness-hash
```

Re-init is what makes policy edits structurally reviewable: a silent change to a
gate (e.g., appending `|| true` to a blocking grep) cannot land without the hash
moving, and the hash move is visible in the diff.

### When re-vendoring a new harness release

Per the Testing SOP propagation path (`/sync-testing-harness`): replace
`.audit-harness/` with the new snapshot, update `PROVENANCE` + `VERSION`, run
`scripts/audit-harness init`, commit the new `.harness-hash` alongside.

---

## 3. Gates and their enforcement posture

| Gate | Workflow | Posture | Required? |
| --- | --- | --- | --- |
| Spec/doc validation (JSON-schema syntax, YAML syntax, drift-eval, surface registry, fetch-capture, lineage, classifier-walls, 6 deep-capture projections, leading-indicator self-test) | `ci.yml` | **hard-fail** | ✅ candidate required check |
| Harness-hash verify | `harness-hash-verify.yml` | **hard-fail** (exit 2 blocks) | ✅ candidate required check |
| Partner-name guard (CISO binding, case-insensitive) | `partner-name-guard.yml` | **hard-fail** | ✅ candidate required check |
| Schema drift (redirect-stub shape) | `schema-drift.yml` | **hard-fail** | ✅ candidate required check |
| Workflow-YAML lint (yamllint + actionlint) | `lint.yml` | **hard-fail** | candidate required check after 3 green days |
| Python tests (pytest) | `python-tests.yml` | pytest runs; lint/typecheck/coverage **advisory** (`continue-on-error`) | advisory → tighten |
| Doc quality (markdownlint, Vale, lychee, Prettier-MD) | `doc-quality.yml` | **advisory** (`continue-on-error`) | advisory → tighten |
| Sign evidence bundle | `sign-evidence-bundle.yml` | hard-fail on signing surface | as applicable |
| Release | `release.yml` | tag-gated | n/a |
| Leading-indicator watch / spec-drift watch | `*-watch.yml` | scheduled cron (not PR gate) | n/a |

**Tidy-First posture (per Kent Beck bd memory):** newly installed lint lanes
start advisory (`continue-on-error: true`) so "install the tool" is separated
from "fix the violations." `lint.yml` is the exception — it ships **hard-fail**
because the existing workflow corpus was verified clean at install (yamllint
exit 0; actionlint exit 0 with the cosmetic SC2129 style nit excluded). Each
advisory lane tightens to hard-fail in a follow-up PR once its corpus is clean.

---

## 4. Deterministic-CI principle (the "E2E" of a spec repo)

Every normative artifact carries an **offline, deterministic** self-test +
freshness check in `ci.yml`. No CI job hits the network — the watchers
(`leading-indicator-watch.yml`, `spec-drift-watch.yml`) own the live polling on
a schedule. The pattern, repeated per contract:

- `<script>.py --self-test` — proves the extractor/scorer/walls logic against
  fixtures (every accept + every reject class).
- `<script>.py --check` — re-derives the committed projection from vendored
  upstream snapshots and **fails if the committed file is stale**. Projections
  are DERIVED, never hand-edited.

This is what stands in for L5/L6 system+E2E testing in a methodology repo: the
contract _is_ the product, so the contract's drift check _is_ the end-to-end test.

---

## 5. What is NOT installed, and why (escape-scan / Gherkin lint / schema validation)

Per `iel-E16e`, three candidate gates were evaluated; here is the disposition:

- **JSON-Schema validation** — **already covered.** `ci.yml` validates every
  `specs/**/schema/*.json` for JSON syntax and every example for schema-validity.
  Adding a second lane would duplicate it. No action.
- **Gherkin lint** — **not applicable.** There are **zero `.feature` files** in
  this repo (`find . -name '*.feature'` → empty). The vendored harness ships
  `gherkin-lint.sh`, available on demand, but there is nothing to lint. Wire a
  Gherkin lane only if/when BDD `.feature` files are added.
- **escape-scan** — covered as a **pre-commit gate** via the vendored harness
  (`scripts/audit-harness escape-scan --staged`), guarding diff-level policy
  weakening. It is not a separate CI workflow because the harness-hash verify +
  the per-artifact freshness checks already cover the post-commit surface.

---

## 6. Requirements traceability (RTM stand-in)

A methodology repo's requirements live in its governance + bead slate, not a UAT
matrix:

- **Requirements:** Decision Records (`000-docs/*-AT-DECR-*.md`), Blueprints
  A/B/C, the canonical glossary, and the bead slate (`bd list`).
- **Tests link back** via docstrings (e.g., a smoke test referencing a DESIGN.md
  section) and via the per-contract `--self-test` fixtures.
- **Open requirements** are queryable: `bd list --label <topic>`.

`TEST_AUDIT.md` § "RTM / personas / journeys" recommends generating a
`tests/RTM.md` (bead-id → test-file map) when the methodology publishes — low
cost, high audit value, tracked but not blocking.

---

## 7. Branch protection (recommended config — DOCUMENTED, not auto-applied)

Per `iel-E16g` / `iel-E16` branch-protection scope: this config is **documented
here, not applied via `gh api` from automation** (applying it mid-run interferes
with concurrent admin merges). An operator with admin rights applies it manually
once the new lane has 3 green days.

**Recommended protection on `main`:**

- Require a pull request before merging (no direct pushes to `main`).
- Require status checks to pass before merging, with these as **required**:
  - `Validate specs and docs` (`ci.yml`)
  - `harness-hash --verify` (`harness-hash-verify.yml`)
  - `partner-name-guard` (`partner-name-guard.yml`)
  - **Add after 3 green days:** `yamllint (workflow + config YAML)` +
    `actionlint (GitHub Actions semantics)` (`lint.yml`)
- Require branches to be up to date before merging.
- Require linear history (the repo's stated git model).
- Do **not** allow force pushes or deletions on `main`.

**Apply (operator, manual, when authorized):**

```bash
gh api -X PUT repos/<owner>/intent-eval-lab/branches/main/protection \
  -f 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=Validate specs and docs' \
  -f 'required_status_checks[contexts][]=harness-hash --verify' \
  -f 'required_status_checks[contexts][]=partner-name-guard' \
  -F 'enforce_admins=false' \
  -F 'required_pull_request_reviews=null' \
  -F 'restrictions=null'
```

The two `lint.yml` contexts are added to `contexts[]` only after the lane has
demonstrated 3 green days, so a flaky new gate never blocks merges during burn-in.

---

## 8. Local fast loop (before push)

```bash
# Install the pre-commit framework once per checkout:
pip install --user pre-commit && pre-commit install

# Run all local gates manually:
pre-commit run --all-files

# Workflow-YAML lint (mirrors lint.yml):
pip install --user yamllint==1.38.0
yamllint -c .yamllint.yml .github/ .yamllint.yml .pre-commit-config.yaml

# Harness integrity (mirrors harness-hash-verify.yml):
scripts/audit-harness verify

# Partner-name guard (mirrors partner-name-guard.yml; must return 0 hits):
#   the grep pattern lives in the private workspace CLAUDE.md, never inlined here.
```

---

## 9. Maintenance

- Editing a gate's policy (coverage floor, lint config, a CI workflow) →
  re-init the hash manifest in the same commit (`scripts/audit-harness init`).
- New harness release → `/sync-testing-harness` (or re-vendor manually, § 2).
- Re-audit on a major test-surface change → `/audit-tests` regenerates
  `TEST_AUDIT.md` and hands off to `/implement-tests` for any new gaps.
