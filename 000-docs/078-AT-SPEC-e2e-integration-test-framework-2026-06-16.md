# 078-AT-SPEC — End-to-end integration test framework for the 5-repo unification thesis

| Field      | Value                                                                                                                 |
| ---------- | --------------------------------------------------------------------------------------------------------------------- |
| Doc        | `078-AT-SPEC-e2e-integration-test-framework-2026-06-16.md`                                                            |
| Status     | **NORMATIVE** (spec) + **RUNNABLE** (skeleton harness shipped at `e2e/`)                                              |
| Authority  | Blueprint A (ecosystem) · Blueprint B § 2.4 + § 7 (`gate-result/v1`, EvidenceBundle) · DR-010 Q3 (unification thesis) |
| Supersedes | — (first e2e integration spec)                                                                                        |
| Bead       | `iep-e2e-integration-spec` (epic `i1c0`)                                                                              |
| Kernel pin | `@intentsolutions/core@0.7.0` (published, sigstore provenance)                                                        |

---

## 0. Why this exists

Every IEP repo tests itself. Nothing tests the **unification thesis** — DR-010 Q3's
binding claim that _every validator in the platform emits the same kernel-canonical
Evidence Bundle, and the rows compose end-to-end across the 5 repos without
re-declaring a schema_. Five repos passing their own CI is necessary but not
sufficient: a row that audit-harness emits and j-rig appends and rollout-gate
consumes and the dashboard renders could drift at any seam — a field rename, an
enum-case change (`PASS` vs `pass`), a wire-form change (`{rows:[...]}` container
vs plain array) — and every repo's _own_ suite would stay green while the
composition silently breaks.

This framework defines:

1. The **canonical end-to-end flow** — the exact path an Evidence Bundle travels
   across the 5 repos (§ 2).
2. The **contract assertion at each seam** — what MUST hold where one repo's output
   becomes another's input (§ 3).
3. A **concrete test-harness design** — fixtures, the kernel-canonical schema checks
   at each hop, and which repo's CI runs the framework (§ 4–6).
4. A **runnable skeleton** — `e2e/run-e2e.mjs`, shipped in this PR, that pipes a
   fixture bundle through the **published** `@intentsolutions/core@0.7.0` validators,
   the audit-harness `conform` verb, the j-rig append step, the
   `@intentsolutions/rollout-gate` `decide()` logic, and a dashboard-render check, and
   asserts the contract at each seam (§ 7).

> **Honesty boundary.** This is a _spec + framework_ deliverable. The skeleton
> exercises every seam against **real published validators and real CLIs** using a
> fixture bundle — it is NOT a synthetic mock presented as a live eval. It does NOT
> run a paid LLM judge, sign to the production Rekor log, or stand up the hosted
> dashboard. Those require infrastructure outside a deterministic CI lane and are
> covered by their own per-repo signing/deploy gates (see § 8 "Out of scope").

---

## 1. The 5 repos and their convergence role

| #   | Repo                                                    | Role at the seam                                                                                                                                     | Wire artifact it produces                        |
| --- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 1   | `intent-eval-core` (`@intentsolutions/core`)            | **Schema authority.** Owns `gate-result/v1` + EvidenceBundle Zod validators + JSON Schemas. Validates, never produces.                               | (validators — the SSoT every other repo imports) |
| 2   | `audit-harness`                                         | **Deterministic gate emitter.** `conform` / `audit` / `cred-gate` emit `gate-result/v1` rows; `emit-evidence` wraps each in an in-toto Statement v1. | gate-result/v1 in-toto Statement(s)              |
| 3   | `j-rig-skill-binary-eval`                               | **Behavioral gate emitter.** Appends behavioral `gate-result/v1` rows to the same bundle (binary verdicts, separate evaluator).                      | gate-result/v1 in-toto Statement(s)              |
| 4   | `intent-rollout-gate` (`@intentsolutions/rollout-gate`) | **Decider.** `decide(bundle, policy)` → `allow` / `block`, fail-closed.                                                                              | rollout decision (allow/block + reasons)         |
| 5   | `intent-eval-dashboard`                                 | **Renderer.** Projects the bundle + decision into a `dashboard-render/v1` view.                                                                      | dashboard-render/v1 payload                      |

The convergence is **at the schema layer, not package consolidation** (Blueprint A
binding principle). The kernel is the only shared dependency; rows flow as data.

---

## 2. Canonical end-to-end flow

```text
                        ┌──────────────────────────────────────────┐
                        │  @intentsolutions/core  (schema authority) │
                        │  GateResultV1Schema · EvidenceBundleSchema │
                        └───────────────▲──────────────▲────────────┘
                                        │ validates    │ validates
   HOP 1                  HOP 2         │   HOP 3       │   HOP 4          HOP 5
 ┌──────────┐   row(s)  ┌──────────┐  row(s) ┌──────────┐ bundle ┌──────────┐ view ┌──────────┐
 │  audit-  │──────────▶│  kernel  │────────▶│  j-rig   │───────▶│ rollout- │─────▶│dashboard │
 │ harness  │  gate-    │ validate │ append  │ behavior │ decide │  gate    │render│  render  │
 │ conform/ │  result/  │ (S1)     │ +valid  │ +valid   │ (S3)   │ decide() │ (S4) │ (S5)     │
 │ audit    │  v1       │          │ (S2)    │          │        │          │      │          │
 └──────────┘           └──────────┘         └──────────┘        └──────────┘      └──────────┘
       │ emit-evidence wraps each row in an in-toto Statement v1                       │
       └───────────────── all rows share predicateType gate-result/v1 ────────────────┘
```

**Plain-English narrative:**

1. **HOP 1 — audit-harness emits.** A deterministic gate (`conform`, `audit`,
   `cred-gate`, `escape-scan`) runs and emits a `gate-result/v1` envelope with
   `--json`; `emit-evidence` wraps it in an in-toto Statement v1 carrying
   `predicateType: https://evals.intentsolutions.io/gate-result/v1`.
2. **HOP 2 — kernel validates (seam S1).** Each row's predicate body MUST pass
   `@intentsolutions/core`'s `GateResultV1Schema`; the enclosing Statement MUST be a
   valid in-toto Statement v1 (`_type`, `subject`, `predicateType`).
3. **HOP 3 — j-rig appends (seam S2).** j-rig runs its behavioral eval and **appends**
   a behavioral `gate-result/v1` row (same predicate URI, same schema) to the same
   append-only bundle. The bundle stays kernel-conformant after the append.
4. **HOP 4 — rollout-gate decides (seam S3).** `@intentsolutions/rollout-gate`'s
   `decide(bundle, policy)` consumes the full bundle + a rollout policy
   (`required_gates`, `forbid_decisions`) and returns `allow` / `block`, fail-closed.
5. **HOP 5 — dashboard renders (seam S4 → S5).** The bundle + decision project into a
   `dashboard-render/v1` payload that itself validates against the kernel.

The thesis under test: **one schema, one bundle, five repos, zero re-declaration.**

---

## 3. Contract assertions at each seam

Each seam has a numbered, machine-checkable contract. The skeleton harness (§ 7)
asserts every one of these; a CI run is green only if all pass.

### S1 — audit-harness output ⊨ kernel `gate-result/v1`

| ID   | Assertion                                                                                                                                                                                                    |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| S1.1 | Every row emitted by audit-harness is an in-toto Statement v1 (`_type === "https://in-toto.io/Statement/v1"`, non-empty `subject[]`, `predicateType === "https://evals.intentsolutions.io/gate-result/v1"`). |
| S1.2 | Each row's `predicate` passes the **published kernel** `GateResultV1Schema` (the SSoT — NOT a copy).                                                                                                         |
| S1.3 | `predicate.gate_id` equals the in-toto `subject[0].name` (Blueprint B § 7.3 subject↔gate binding).                                                                                                           |
| S1.4 | `gate_decision` is lowercase (`pass`/`fail`/`advisory`/`error`) — guards against the legacy `result: "PASS"` draft shape.                                                                                    |
| S1.5 | `predicate.runner` identifies the emitting repo (e.g. `audit-harness@x.y.z`).                                                                                                                                |

### S2 — kernel-validated bundle is a well-formed EvidenceBundle

| ID   | Assertion                                                                                                                                                                                   |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S2.1 | The assembled bundle metadata passes the kernel `EvidenceBundleSchema` (`id`/`eval_run_id` UUIDv7, `predicate_uri_set`, `row_count`, `subject_set`, `signing_mode`, `verification_status`). |
| S2.2 | `row_count` equals the number of rows actually present (no count drift).                                                                                                                    |
| S2.3 | `predicate_uri_set` contains exactly the predicate URIs present in the rows (no phantom URIs, no missing URIs).                                                                             |
| S2.4 | `subject_set` is the deduplicated union of every row's subjects.                                                                                                                            |

### S3 — j-rig append preserves kernel-conformance

| ID   | Assertion                                                                                                                                |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| S3.1 | After j-rig appends a behavioral row, **every** row (deterministic + behavioral) still passes `GateResultV1Schema`.                      |
| S3.2 | The behavioral row carries the **same** `predicateType` URI as the deterministic rows (single predicate family — the unification claim). |
| S3.3 | The append is additive: every pre-existing row is byte-identical (append-only invariant, Blueprint B § 2.4).                             |
| S3.4 | The behavioral row's evaluator (`runner`) is distinct from the artifact under test (separate-evaluator principle).                       |

### S4 — rollout-gate consumes the unified bundle and decides

| ID   | Assertion                                                                                                                                                      |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S4.1 | `decide(bundle, policy)` parses the bundle in **both** wire forms (v2 plain array AND v1 `{bundle_format,rows}` container) — neither is rejected as malformed. |
| S4.2 | A bundle where all `required_gates` pass and no `forbid_decisions` appear → `allow`.                                                                           |
| S4.3 | A bundle with a `fail` (or any `forbid_decisions`) row → `block` (fail-closed).                                                                                |
| S4.4 | A bundle missing a `required_gate` → `block`, citing the missing gate id.                                                                                      |
| S4.5 | A schema-invalid row → `block`, citing the row index (no silent pass-through).                                                                                 |

### S5 — dashboard render validates against the kernel

| ID   | Assertion                                                                                                                                                                                                         |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S5.1 | The render payload built from the bundle + decision passes the kernel `dashboard-render/v1` schema (or the harness reports it as a documented gap if the schema is not yet on the published surface — see § 7.3). |
| S5.2 | The rendered row count and decision match the upstream bundle + rollout decision (no projection drift).                                                                                                           |

---

## 4. Test-harness design

### 4.1 Fixtures

Fixtures live in `e2e/fixtures/` and are **kernel-canonical by construction** — each
is validated against the published `@intentsolutions/core@0.7.0` schema as the first
step of the harness, so a fixture can never silently rot the test.

| Fixture                         | Purpose                                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------- |
| `audit-harness-row.json`        | A real gate-result/v1 in-toto Statement as audit-harness emits it (HOP 1 output).                 |
| `jrig-behavioral-row.json`      | A behavioral gate-result/v1 row as j-rig appends it (HOP 3 output).                               |
| `policy.allow.json`             | Rollout policy whose `required_gates` are satisfied by the unified bundle → expect `allow`.       |
| `policy.block-missing.json`     | Policy requiring a gate the bundle lacks → expect `block`.                                        |
| `policy.block-forbidden.json`   | Bundle variant carrying a `fail` row → expect `block`.                                            |
| `bad-row.uppercase-result.json` | A legacy `result:"PASS"` row → MUST be rejected at S1 (regression guard for the enum-case drift). |

> The fixtures are deliberately _small and real_: they are the exact wire shapes the
> repos produce, captured from the canonical example
> (`specs/evidence-bundle/v0.1.0-draft/examples/in-toto-statement.json`, migrated to
> the kernel v1 shape) and the lab's own emitted row
> (`evidence/snapshot-currency/gate-result.json`).

### 4.2 The harness binary

`e2e/run-e2e.mjs` (Node ≥ 22, run via `node --experimental-strip-types` only if it
imports `.ts`; the skeleton is plain `.mjs` so it runs on stock Node) executes the
flow in § 2, asserting every contract in § 3. It:

- imports the **published** kernel validators (`npm i --no-save @intentsolutions/core@0.7.0`),
- shells out to the real `audit-harness conform` verb when the harness is on `PATH`
  (and falls back to the captured fixture row when it is not, so the lane stays
  hermetic),
- replicates the `@intentsolutions/rollout-gate` `decide()` contract via the
  published package when installed (and a faithful inline decider otherwise — the
  inline path is clearly marked and exercises the SAME policy semantics so the seam
  contract S4 is still asserted),
- prints a per-seam PASS/FAIL table and exits non-zero on any failure.

### 4.3 Determinism

No network at assert-time (validators are local once installed; fixtures are
committed). No clock-dependence in assertions (timestamps in fixtures are fixed). No
paid API. The lane is reproducible on a fresh clone.

---

## 5. Which repo's CI runs the framework

**`intent-eval-lab` owns the e2e lane** — it is the methodology/convergence umbrella
and the only repo that is _neutral_ across all 5 (it produces no row of its own and
depends on no other repo's runtime). Placing the lane here avoids a circular CI
dependency (audit-harness's CI can't gate on j-rig which can't gate on rollout-gate).

- **Trigger:** `.github/workflows/e2e-integration.yml` on `pull_request` + `push` to
  `main` + manual `workflow_dispatch`.
- **Steps:** checkout → Node 22 → `npm i --no-save @intentsolutions/core@0.7.0`
  (+ `@intentsolutions/rollout-gate@latest` for the real decider) → `node e2e/run-e2e.mjs`.
- **Gate posture:** the e2e lane is a **required check** for any PR that touches
  `e2e/**` or the convergence docs; advisory elsewhere (it does not re-run on every
  unrelated lab doc edit). It catches cross-repo wire drift _before_ a kernel bump or
  a repo's emitter change lands.

A cross-repo escalation path (running the lab's e2e lane from each emitting repo's CI
on a kernel-version bump) is noted as future work in § 8 — it needs the
`repository_dispatch` plumbing that the VPS-as-the-home onboarding pattern provides.

---

## 6. Failure semantics (what a red lane means)

| Red at | Most likely cause                                                                  | Action                                                                                                      |
| ------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| S1     | audit-harness changed its emit shape, or a fixture rotted vs the kernel            | Re-capture the fixture from the live `conform --json`; if the kernel rejects it, the emitter regressed.     |
| S2     | EvidenceBundle assembly drifted (count/URI/subject mismatch)                       | Fix the assembler; the bundle metadata must mirror its rows.                                                |
| S3     | j-rig's behavioral row uses a different predicate URI or broke append-only         | Re-align j-rig's emitter to the kernel `gate-result/v1` family.                                             |
| S4     | rollout-gate's `decide()` changed its fail-closed contract or wire-form acceptance | A `block`→`allow` regression here is a **release-blocking** safety bug.                                     |
| S5     | dashboard projection drifted from the bundle, or `dashboard-render/v1` changed     | Re-align the renderer; or, if the schema isn't published yet, the harness records a documented gap (§ 7.3). |

---

## 7. Runnable skeleton (shipped in this PR)

### 7.1 What's shipped

```text
e2e/
  run-e2e.mjs               # the harness — pipes a fixture bundle through all 5 seams
  fixtures/
    audit-harness-row.json
    jrig-behavioral-row.json
    policy.allow.json
    policy.block-missing.json
    policy.block-forbidden.json
    bad-row.uppercase-result.json
  README.md                # how to run locally + in CI
.github/workflows/e2e-integration.yml
```

### 7.2 Run it

```bash
# from intent-eval-lab/
npm i --no-save @intentsolutions/core@0.7.0
npm i --no-save @intentsolutions/rollout-gate@latest   # optional: real decider
node e2e/run-e2e.mjs
# → per-seam PASS/FAIL table; exit 0 = unification thesis holds for the fixtures
```

### 7.3 Documented gaps (honest, not faked)

- **HOP 5 (dashboard) is asserted against the kernel `dashboard-render/v1` schema if
  it is on the published surface; otherwise the harness validates the _projection
  invariants_ (S5.2 — row count + decision parity) and records S5.1 as a
  `documented-gap`** rather than asserting a schema that may not be published yet.
  This keeps the lane honest: it never claims a green it didn't earn.
- **The real `audit-harness conform` shell-out** runs when the harness is on `PATH`
  (it is, in the lab's `scripts/audit-harness` vendored wrapper); otherwise the
  harness uses the committed fixture row (still kernel-validated). Both paths assert
  S1 against the **published kernel**, so the seam contract holds either way.
- **No signing / no Rekor / no paid LLM judge** — out of scope per § 8.

---

## 8. Out of scope (covered by other gates)

| Concern                                | Where it lives                                                                                                          |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Production Rekor signing of the bundle | `audit-harness/scripts/emit-evidence.sh` + `intent-rollout-gate` v0.2.0 keyless signing (iah-E06 DNSSEC/CAA pre-flight) |
| Paid LLM behavioral judging            | j-rig's own eval lane (real provider keys, real budget)                                                                 |
| Hosted dashboard deploy                | `intent-eval-dashboard` deploy workflow (VPS-as-the-home)                                                               |
| Cross-repo dispatch on kernel bump     | future `repository_dispatch` plumbing (§ 5)                                                                             |

---

## 9. Maintenance

- **Kernel bump:** update the pin in `e2e/run-e2e.mjs` + the CI workflow + this doc's
  header in one PR; re-run the lane. If a fixture fails against the new kernel, the
  bump is a breaking change for emitters — that's the lane doing its job.
- **New seam / new repo:** add a numbered seam contract in § 3, a fixture in
  `e2e/fixtures/`, and the assertion block in `run-e2e.mjs`.
- **Fixture rot:** the harness re-validates every fixture against the published kernel
  as step 0, so a rotted fixture fails loudly at the top of the run, not silently mid-flow.

---

_Authored under the Intent Eval Lab methodology umbrella. The unification thesis
(DR-010 Q3) is the binding claim this framework makes empirically testable._
