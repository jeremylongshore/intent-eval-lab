# PP-PLAN-040 — Make the audit trio comprehensive, on any repo

**Date:** 2026-06-04
**Type:** PP-PLAN (project plan / program plan)
**Status:** RATIFIED (plan-mode approved; this is the durable canonical record)
**Authority:** audit panel (Beck · Thompson · Hickey · Armstrong) + the `/validate-*` reuse finding; IS Testing SOP (`~/000-projects/CLAUDE.md`); DR-010 (unification thesis — every validator emits an Evidence Bundle row)
**Scope:** `audit-harness` (intent-audit-harness) · `audit-tests` skill · `implement-tests` skill · `sync-testing-harness` skill · the org umbrella `intent-solutions-io/intent-eval-platform` · `claude-code-plugins-plus-skills`
**Companion artifacts:** IEP rollback baseline manifest (`041-RR-LAND-iep-rollback-baseline-2026-06-04.md`); bd epic tree (9 epics, labels `audit-harness` `audit-tests` `implement-tests` `conformance` `currency` `ecosystem-sync` `baseline` `kb:iep`)

---

## 0. Executive summary

`/audit-tests` is thin. It only looks for _testing_, and even there it is only deep on one
layer (L3 unit). It misses whole dimensions — schema/protocol conformance, upstream currency,
security/supply-chain, repo hygiene, skill/agent/plugin quality. And the intelligence that
decides _what a repo needs_ lives inside the Claude skills, so `audit-harness` cannot determine
a repo's audit profile or run the full check set in bare CI.

This plan makes the audit trio **comprehensive** and makes the harness **work on any repo**
without Claude in the loop. The resolved relationship is **inspector + provisioner + toolbox**,
not competitors:

- **`/audit-tests`** = inspector — walks a repo, decides _what to look for_, runs checks, writes
  the report. (The "what to look for" checklist lives here, and it is the thin part this plan fattens.)
- **`/implement-tests`** = provisioner — installs the testing setup (frameworks, configs, CI,
  **scaffolded** starter files, `tests/TESTING.md`), staged for review, never committed.
- **`@intentsolutions/audit-harness`** = toolbox — deterministic check-scripts that also install
  into the repo so checks **enforce in the repo's own CI**.

**Terminology lock (the user flagged "scaffold"):** the harness **determines the _audit profile_**
(which gates/dimensions apply to a repo) and **runs the gates** — it never writes repo files.
`/implement-tests` **provisions** the setup. "Scaffold" is reserved only for _generated starter
test files_. So: _harness decides the profile + reports; implement-tests provisions;
scaffolding = generated starters._

---

## 1. Ecosystem model + standalone usage (the shared mental model)

Three independently-usable pieces that **layer** — not competitors:

- **`audit-harness`** = the **no-Claude CLI engine.** The _only_ piece that runs unattended
  (CI, pre-commit, terminal). Install in any repo (npm/pip/cargo/vendored); run
  `audit-harness <gate>`. This is "works on any repo."
- **`/audit-tests`** = Claude **inspector** (standalone-invocable; reports + optionally hands off).
  Uses the harness for the deterministic gates.
- **`/implement-tests`** = Claude **provisioner** (standalone or via handoff; installs the harness
  as L0, stages setup for review).

Layering: harness alone = deterministic gates every commit/CI; `/audit-tests` = Claude diagnoses +
uses the harness; `/implement-tests` = Claude installs the setup so the gates then run in that
repo's CI. **Skills set up + diagnose** (occasional, Claude); **harness enforces** (every build,
deterministic).

---

## 2. Automated auto-update — the CI routine (DECIDED, zero-touch)

Propagation must be an **automated CI routine** with a real **home in the platform** that keeps
the **whole ecosystem** current — explicitly including `claude-code-plugins-plus-skills` (the
validator-tooling source + the largest internal test corpus).

- **The "keep everything current" home = the org umbrella `intent-solutions-io/intent-eval-platform`.**
  It holds:
  - **`ecosystem.json`** — the manifest of every managed repo (the 6 IEP repos +
    `claude-code-plugins-plus-skills` + the broader set), their kind (npm/vendored/python), and
    their pinned harness/schema versions. The single registry of "what is in the ecosystem."
  - **the scheduled `ecosystem-sync` orchestrator workflow** (weekly cron + on-release
    `repository_dispatch`) that iterates the manifest, runs the deterministic drift/currency scan,
    and opens **canary-first** bump PRs across all of them.
- **The drift/conform/currency _logic_ lives in `audit-harness`** (the portable CLI the
  orchestrator calls and that any repo also runs standalone). The umbrella orchestrates; the
  harness computes.
- **Shared validators are packaged INTO audit-harness releases.** `validate-skills-schema.py`,
  `validate-catalog-invariants.py`, the `/validate-*` deterministic checks — currently authored in
  `claude-code-plugins/scripts/` — get bundled into the harness so `conform` is **self-contained on
  any repo** (no requirement that claude-code-plugins be checked out). claude-code-plugins **stays
  their authoring + spec home**; on a validator/spec change, the on-release dispatch repackages +
  propagates them outward via `ecosystem-sync`.
- **`claude-code-plugins-plus-skills` is a first-class manifest member** — synced like every other
  repo, and harvested as the reference implementation (its `scripts/` + CI are the richest existing model).

> **GUARD — `claude-code-plugins` has bespoke, in-flight CI/CD; do not disrupt it (user directive 2026-06-04).**
> That repo runs a large purpose-built plugin-testing pipeline — `validate-plugins.yml`, `pr-prescreen.yml`,
> `e2e-tests.yml`, `cli-test.yml`, `publish-changed-packages.yml` / `publish-all-packages.yml`,
> `secret-scan.yml`, `security-audit.yml`, `deploy-marketplace.yml`, `sync-external.yml`, `plane-sync.yml`,
> and more — and there is active feature work in flight on it. **Any ecosystem-sync work that touches it
> (validator-packaging, manifest membership, Renovate, on-release dispatch) MUST first study the existing
> pipelines and coordinate with the in-flight branch — never bolt generic automation (Renovate auto-merge,
> a sync orchestrator, a `validate-*` extraction) onto it without understanding what its own CI already does.**
> The validators stay _authored_ there; extraction-into-harness is additive and must not regress that repo's
> own gates. Treat claude-code-plugins as the most delicate manifest member, sequenced last in any fan-out.

Mechanics:

- **Package-version bumps** (`@intentsolutions/audit-harness`, `@intentsolutions/core`) →
  **Renovate** configured in every repo: auto-PRs on schedule; green `chore(deps)` bumps
  **auto-merge** once required checks pass. (Industry-standard, zero custom maintenance.)
- **Vendored-harness + schema/currency drift** → a **scheduled `ecosystem-sync` GitHub Actions
  workflow (weekly cron)** — the automated form of `/sync-testing-harness` — runs the deterministic
  drift scan and **opens bump PRs itself**, **canary-first** (bump one repo, confirm green, then fan out).
- **On-release fan-out** → the audit-harness/core release workflow fires a `repository_dispatch`
  that triggers `ecosystem-sync` **immediately** (propagation in minutes, not the weekly wait).
- **Skills** are global (one copy in `~/.claude/skills/`) — nothing to propagate.
- The **Claude `/sync-testing-harness` skill stays** as the manual/interactive path for messy cases
  (the cron handles routine bumps).
- **Currency stays advisory** in this routine — it _reports + opens PRs_, it never reddens a build.

---

## 3. Technical decisions made (for scale + adaptability)

1. **Harness = read-only deterministic classifier + gate-runner + orchestrator of external tools.**
   No filesystem mutation (`apply` stays in `/implement-tests`); no live-fetch in gates.
2. **Reuse, don't reinvent:** conformance shells out to the 7 existing `/validate-*` validators +
   `ajv`/`spectral`; security/hygiene shells out to gitleaks/osv-scanner/syft/markdownlint/Vale/lychee;
   skill-quality consumes j-rig's verdict rows.
3. **Data-first values before verbs:** `audit-profile/v1` (closed, versioned, hashed) + one canonical
   dimension→gate registry (`layer-applicability.md` + `TESTING.md` become projections of it).
4. **Claude only refines the classifier's explicitly-`unresolved` residue** — never co-authors the
   deterministic profile (CI stays reproducible).
5. **New gates ship advisory; blocking promotion is engineer-pinned + FP-rate-gated.**
6. **Safety levers ship before any blocking gate:** `INDETERMINATE` result class, per-gate
   supervision/timeout, `.audit-harness.yml` override + kill-switch, canary propagation, signed
   `install.sh`, IEP rollback baseline first.
7. **Auto-update = Renovate + scheduled `ecosystem-sync` cron + on-release dispatch.**

---

## 4. What the audit panel changed (Beck · Thompson · Hickey · Armstrong) + the `/validate-*` finding

The reviewers converged. The biggest correction: **reuse, don't reinvent, and keep the harness
read-only + deterministic.**

1. **`/validate-*` already exists — reuse it.** 7 validation skills (`/validate-{skillmd,agent,hook,
mcp,marketplace,plugin,consistency}`) plus deterministic CI-runnable validators
   (`claude-code-plugins/scripts/validate-skills-schema.py`, `validate-catalog-invariants.py`,
   `audit-typescript-coverage.py`). `/validate-plugin` already orchestrates the rest.
   **Conformance is mostly wiring these in**, not building schema engines.
2. **Harness stays read-only — no `scaffold --apply`.** A filesystem-mutating gate-runner collides
   with the escape-scan engineer-owned-policy boundary (`escape-scan.sh` REFUSEs AI policy edits).
   _Apply_ stays in `/implement-tests` (already stages-for-review). The deterministic floor =
   `classify` (read-only stdout JSON) + the existing gates.
3. **Don't reinvent scanners — shell out.** secrets→gitleaks, CVE→osv-scanner/pip-audit,
   SBOM→syft+cosign, docs→markdownlint/Vale, links→lychee, JSON-Schema→ajv/check-jsonschema,
   OpenAPI→spectral. The harness _runs the right external tool with the repo's policy and wraps the
   exit code in a `gate-result/v1` row_. Missing tool → `unmeasured`, like today.
4. **Data-first, then verbs.** Specify `audit-profile/v1` as a **closed, versioned, hash-bearing
   value** (exactly like the existing `gate-result/v1` — `additionalProperties:false`, version in
   `$id`) _before_ writing `classify`. Make the **dimension→gate registry the single canonical
   datum**; today the fact "which gates apply to repo-type X" is smeared across
   `layer-applicability.md`, each repo's `TESTING.md`, and `harness-hash.sh` — collapse to one datum
   that the others are _projections_ of.
5. **Test-first the brain.** `classify` + profile-resolution are pure functions → write a **golden
   fixture corpus first** (`tests/fixtures/classify/{mcp-server,skill-only,plugin,openapi-service,
polyglot-monorepo,external-partner-monorepo}/` → expected `audit-profile.json`). No classifier
   code before fixtures. The external partner monorepo is _one fixture among many_, not "the" test.
6. **Currency is an advisory REPORT, never a blocking gate.** It depends on upstream state
   (non-deterministic, network-bound). It lives in `/sync-testing-harness`, has **no exit-code
   authority, no auto-fix, no live-fetch**. Model it as a **per-upstream-identity pin relation**
   (each of MCP-spec / SKILL.md-schema / gate-result-predicate / Anthropic-SDK has its own version +
   `checked_at`), not one opaque `.schema-version.txt` scalar — so the _pin's own staleness_ is detectable.
7. **`conform` stays deterministic + pure-local.** Schemas are **bundled in the pinned harness
   version** (immutable, content-addressed, version-in-`$id`), validated against the bundled copy at
   gate-time — **never live-fetched**. `conform` records the schema-version+hash in the `gate-result`
   `policy_hash`. `currency` _proposes_ new schema versions alongside old ones; **never overwrites**
   (prior signed attestations must stay reproducible).
8. **New gates ship advisory; promotion is earned.** A gate ships `advisory` (exit 0, finding
   logged) until it shows a measured false-positive rate below a stated bar on the IEP corpus; an
   engineer then promotes it to `blocking` via the hash-pinned `tests/TESTING.md` policy. Prevents
   the `|| true` trust-erosion epidemic (already visible in `audit-harness/.github/workflows/ci.yml`).
9. **Failure-class taxonomy + supervision.** Add `INDETERMINATE` (infra failure ≠ policy failure)
   alongside PASS/FAIL/NOT_APPLICABLE. The dispatcher (`bin/audit-harness.js`) supervises each gate
   with a per-gate timeout: a gate hang/crash is isolated; siblings run. Pure-local policy gates fail
   **closed**; network-touching checks fail **open/advisory** → `INDETERMINATE`.
10. **Kill-switch + canary.** Engineer-owned `.audit-harness.yml` (hash-pinnable) pins classification
    - per-gate advisory/disable toggles (the "inside latch" + standing per-gate rollback).
      `AUDIT_HARNESS_ADVISORY=…` / `AUDIT_HARNESS_DISABLE=1` break-glass env.
      `/sync-testing-harness --canary <repo>` bumps one, waits green, then fleet. Sign `install.sh`
      downloads (SHA256SUMS/cosign — cosign already in-house; it already broke once on a rename).
11. **Profiles are a UNION, not a winner.** A repo that is a TS monorepo _and_ ships SKILL.md + MCP
    (j-rig, the external partner monorepo) must get the union of applicable profiles — picking one silently drops the
    other's gates (a false-negative, worse than a false-positive).

---

## 5. Architecture (revised)

- **Harness = read-only classifier + deterministic gate-runner + orchestrator of external tools.**
  Verbs: `classify` (→ `audit-profile/v1` JSON, stdout, no writes), `audit --fast|--deep` (run the
  profile's gates, supervised, emit `gate-result/v1` rows), `conform` (validate artifacts against
  _bundled_ schemas + shell out to the `/validate-*` deterministic validators). No `apply`, no
  live-fetch, no repo mutation.
- **`/audit-tests` (Claude) = refinement on the residue.** Calls `classify` first; operates only on
  what the classifier marks `unresolved` (ambiguous/novel repos), proposes profile patches a human
  pins, and runs the higher-judgment `/validate-consistency` + `/validate-plugin` Tier-3/j-rig evals.
  **Never co-authors the deterministic classification value** (keeps CI reproducible).
- **`/implement-tests` (Claude) = provisioning**, staged for review (unchanged boundary); consumes
  the profile + gaps.
- **`/sync-testing-harness` = currency + propagation**, advisory-only, canary-first.

---

## 6. The comprehensive "what to look for" (every dimension — via reuse/shell-out, advisory-first)

1. **Testing depth (finish the pyramid):** L2 (lint/format/types/secrets/dep-audit/doc-quality),
   L4 (integration/contract/migration), L5 (perf/SAST/DAST/a11y/chaos), + property-based/fuzz/
   flakiness — on top of today's solid L3. Each gate **shells out** to the standard tool.
2. **Conformance:** `conform` validates SKILL.md / agent / hooks / MCP / marketplace / plugin /
   OpenAPI / Evidence-Bundle artifacts — by **calling the existing `/validate-*` deterministic
   validators** + `ajv`/`spectral` for the generic schemas. Wire the already-shipped
   `gate-result.schema.json` (present in fixtures, currently unenforced).
3. **Currency (advisory report only):** per-upstream-identity drift (Anthropic/Codex SDK, MCP spec,
   SKILL.md schema, deprecated APIs) in `/sync-testing-harness`; flags, never blocks, never auto-fixes.
4. **Security/supply-chain:** gitleaks (secrets), osv-scanner/pip-audit (CVEs), license + syft/cosign
   (SBOM/provenance) — shelled out.
5. **Repo hygiene:** README/CONTRIBUTING/SECURITY presence, markdownlint/Vale, lychee link-integrity,
   changelog discipline.
6. **Skill/agent/plugin quality:** consume **j-rig**'s behavioral verdicts (trigger precision,
   tool-allowlist tightness, prompt-injection safety, description quality) as `gate-result` rows —
   **do not** reimplement judgment as deterministic regex; the harness _consumes_ j-rig's Evidence
   Bundle row.

---

## 7. Phasing (re-sequenced: value early, risk contained, test-first)

- **Phase 0 — Data + safety spine (paper + small, reversible):** specify `audit-profile/v1`
  (closed/versioned/hashed); make the dimension→gate registry the canonical datum (generate
  `layer-applicability.md` from it); define the `INDETERMINATE` result + per-gate supervision/timeout
  in the dispatcher; define `.audit-harness.yml` (override + kill-switch) + the advisory/blocking
  promotion rule. **No big-bang re-architecture.**
- **Phase 1 — `classify --json` (read-only) + fixture corpus first.** Golden fixtures before code;
  ship the read-only verb alone; eyeball its profile across every IEP repo. Reversible.
- **Phase 2 — `conform` (highest value, lowest risk).** Wire the existing `/validate-*` validators +
  bundled schemas; pass/fail fixtures (malformed SKILL.md/MCP → fail; valid → pass); record
  schema-version+hash in `policy_hash`. Proves the brain end-to-end on a tiny safe surface.
- **Phase 3 — testing-depth gates (L2/L4/L5 + property/fuzz/flakiness)**, each a shell-out,
  advisory-first, `--fast`/`--deep` split with a per-gate latency budget (fast tier <10s on a
  reference repo).
- **Phase 4 — security/hygiene/skill-quality gates** (shell-outs + j-rig consumption), advisory-first.
- **Phase 5 — currency** as an advisory report in `/sync-testing-harness` (per-identity pins, canary
  propagation) — last, because it's the riskiest and least deterministic.
- Refactor `/audit-tests` + `/implement-tests` to call `classify`/`conform` only after those verbs
  are trusted (not in Phase 0).

**Cross-cutting:** every gate emits a `gate-result/v1` Evidence Bundle row; harness stays polyglot +
version-current via the shipped v1.1.5 + `/sync-testing-harness`; engineer-owned `TESTING.md` policy
boundary preserved (escape-scan still REFUSEs AI policy-weakening, and now also vets
`/implement-tests` output).

---

## 8. Supporting (not the headline)

- **IEP rollback baseline** = safety net established **first** (a `BASELINES` manifest of
  {commit, tag, published-version} + dependency edges across the 6 Tier-1 IEP repos + a rollback
  recipe), so there's a known-good point before any harness surgery.
  See `041-RR-LAND-iep-rollback-baseline-2026-06-04.md`.
- **An external partner mobile-testing monorepo** = a **test candidate / fixture** only (clean,
  IEP-dependency-free: 2 skills + 12-tool MCP + 6 vitest suites + cross-CLI manifests) — one
  validation subject among the fixture corpus, not a plan phase.

---

## 9. Execution tracking (bd epics — file first)

The first execution action is filing this as a bd epic tree (three-layer mirror: bd ↔ GitHub issue ↔
Plane, plain-English titles, `bd-sync` discipline). Epics (one per phase + the cross-cutting ones),
each with child task beads = the concrete deliverables:

1. **Establish the IEP rollback baseline** (safety net, do first): BASELINES manifest, tag snapshot
   across the 6 Tier-1 repos, rollback recipe, coherence check.
2. **Audit-harness data + safety spine (Phase 0):** `audit-profile/v1` schema; canonical
   dimension→gate registry; `INDETERMINATE` result + dispatcher supervision/timeout;
   `.audit-harness.yml` override + kill-switch; advisory→blocking promotion rule.
3. **`classify` (read-only) + golden fixture corpus (Phase 1).**
4. **`conform` via reuse of `/validate-*` + bundled schemas (Phase 2).**
5. **Testing-depth gates L2/L4/L5 + property/fuzz/flakiness, shell-out, advisory-first (Phase 3).**
6. **Security/hygiene/skill-quality gates + j-rig consumption (Phase 4).**
7. **Currency advisory report + per-upstream pin relation (Phase 5).**
8. **Ecosystem-sync home + automation:** `ecosystem.json` manifest + scheduled `ecosystem-sync`
   orchestrator in the org umbrella, Renovate config across repos, on-release dispatch, canary
   propagation, validator-packaging into harness, claude-code-plugins inclusion, signed `install.sh`.
9. **Refactor `/audit-tests` + `/implement-tests`** to call the harness brain (after `classify`/
   `conform` are trusted).

Labels: `audit-harness`, `audit-tests`, `implement-tests`, `conformance`, `currency`,
`ecosystem-sync`, `baseline`, `kb:iep`. First claimable bead = the IEP baseline.

---

## 10. Audit trail & documentation discipline (per `/doc-filing` — every epic lands as a complete unit)

1. **Master plan filed as a durable doc (this file).** Canonical reference the epics + CLAUDE.mds
   point at.
2. **AAR after every epic** (`NNN-AA-AACR-<epic>-<date>.md` in the relevant repo's `000-docs/` —
   audit-harness for harness epics, intent-eval-lab for cross-cutting/methodology, the skills repo
   for skill refactors). No epic closes without its AAR.
3. **CLAUDE.md notes + references:**
   - **Global** `~/.claude/CLAUDE.md` (+ Testing SOP) — note the comprehensive-audit direction +
     ecosystem-sync automation + reference this plan.
   - **Umbrella** `~/000-projects/CLAUDE.md` + `~/000-projects/intent-eval-platform/CLAUDE.md` —
     record the ecosystem-sync home, `ecosystem.json`, the read-only-harness + reuse-validators decisions.
   - **Per-repo** — `audit-harness/CLAUDE.md` (new verbs + read-only + advisory-first + validator
     packaging), `claude-code-plugins/CLAUDE.md` (validator-authoring-home + manifest membership),
     and the `/audit-tests` + `/implement-tests` SKILL.md notes — each referencing this plan.
4. **Memory updated:** auto-memory for the durable architecture decisions (harness read-only,
   conform-reuses-validators, currency-advisory-only, ecosystem-sync automation) + bd memories for
   in-workspace facts. Supersede stale entries rather than duplicate.
5. **Three-layer closure:** every bead closes via `bd-sync` (bd ↔ GH issue ↔ Plane) with evidence;
   PRs carry `Closes`/`Refs` per the convention.

---

## 11. Critical files

- **Harness:** `audit-harness/bin/audit-harness.js` (dispatcher → supervision + `classify`/`conform`),
  `scripts/*.{sh,py}`, `harness-hash.sh` + `escape-scan.sh` (the policy boundary),
  `tests/fixtures/gate-result.schema.json` (the closed/versioned model to mirror for
  `audit-profile/v1`; wire into `conform`), `install.sh` (add SHA256SUMS/cosign verify).
- **Reuse:** `claude-code-plugins/scripts/validate-skills-schema.py` + `validate-catalog-invariants.py`;
  `~/.claude/skills/validate-{skillmd,agent,hook,mcp,marketplace,plugin,consistency}/`.
- **Skills:** `~/.claude/skills/audit-tests/SKILL.md` +
  `references/{taxonomy,layer-applicability,testing-md-spec,rtm-personas-journeys}.md`;
  `~/.claude/skills/implement-tests/SKILL.md` + `references/install-playbook-L{1..7}-*.md`;
  `~/.claude/skills/sync-testing-harness/SKILL.md`.
- **Schema sources:** `@intentsolutions/core` (Evidence Bundle + predicates); upstream MCP/SKILL/SDK
  specs **bundled per harness version** (content-addressed), not live-fetched.

---

## 12. Verification

- **Test-first:** the classify/profile fixture corpus exists and golden-matches _before_ classifier
  code; `conform` pass/fail fixtures (malformed vs valid SKILL.md/MCP) green.
- **Per gate:** unit test + synthetic pass/fail; new gates ship advisory; FP-rate measured on the IEP
  corpus before any blocking promotion.
- **Safety:** simulate network-down → currency/conform-load returns `INDETERMINATE` (advisory), batch
  continues; a hanging gate hits its timeout and siblings still run; `AUDIT_HARNESS_DISABLE=1` no-ops
  with a banner; `.audit-harness.yml` pin overrides a deliberate mis-classification.
- **Reproducibility:** same commit + same harness version → identical `conform` verdict (bundled
  schema, no live-fetch); a signed `gate-result` re-verifies against the recorded `policy_hash` schema
  version.
- **Dogfood:** full audit on the 6 IEP repos (self-host) + the external partner monorepo → evidence
  renders on the dashboard; `classify` produces a correct UNION profile for the
  monorepo-that-also-ships-skills cases (j-rig, the external partner monorepo).
- **Baseline:** rollback recipe restores all 6 IEP repos to the tagged baseline + cross-repo
  installs/imports resolve.
- **Propagation:** `/sync-testing-harness --canary` bumps one repo, confirms green, before any fleet
  bump; `install.sh` rejects a tampered tarball.

---

_Filed per Document Filing Standard v4.3. This plan is the canonical reference; bd is canonical for
task state; DR-010 wins for governance; Blueprint A wins for ecosystem principles; Blueprint B wins
for runtime + the 13-entity domain model + `gate-result/v1` predicate spec._
