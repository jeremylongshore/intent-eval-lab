# e2e — End-to-end integration harness for the 5-repo unification thesis

This directory holds the runnable end-to-end integration test for the Intent Eval
Platform **unification thesis** (DR-010 Q3): a single kernel-canonical Evidence
Bundle flows across all 5 repos without re-declaring a schema, and the contract
holds at every seam.

- **Spec:** [`../000-docs/078-AT-SPEC-e2e-integration-test-framework-2026-06-16.md`](../000-docs/078-AT-SPEC-e2e-integration-test-framework-2026-06-16.md)
- **Bead:** `iep-e2e-integration-spec` (epic `i1c0`)
- **CI lane:** [`../.github/workflows/e2e-integration.yml`](../.github/workflows/e2e-integration.yml)

## The flow under test

```text
audit-harness ──▶ kernel ──▶ j-rig ──▶ rollout-gate ──▶ dashboard
  emit row     validate     append     decide          render
   (HOP1)       (S1)        (HOP3)      (HOP4)          (HOP5)
                (S2/S3)                 (S4)            (S5)
```

Every row is a `gate-result/v1` in-toto Statement v1 carrying
`predicateType: https://evals.intentsolutions.io/gate-result/v1`. The harness
asserts a numbered contract at each seam (S1–S5 in the spec).

## Run it locally

```bash
cd e2e
npm install            # pins @intentsolutions/core@0.7.0; rollout-gate optional
node run-e2e.mjs
```

Expected tail:

```text
  21 passed · 0 documented-gap · 0 failed
```

Exit code `0` = the unification thesis holds for the fixtures; `1` = a seam failed.

## What's real vs. what's scoped out

**Real (not mocked):**

- Rows are validated at S1/S2/S3/S5 against the **published**
  `@intentsolutions/core@0.7.0` kernel validators — the single source of truth, never
  a re-declared schema.
- The dashboard render (S5) is validated against the real kernel `dashboard-render/v1`
  schema.
- S4 is decided by a faithful inline reimplementation of
  `@intentsolutions/rollout-gate`'s `decide()` contract, **and cross-checked** against
  the **real published `@intentsolutions/rollout-gate@2.0.0`** package on the exact
  same fixtures (`S4.fidelity`) — identical allow/block outcomes prove the inline path
  is faithful. (The real package is loaded via a CJS subprocess because its published
  2.0.0 ESM bundle has an upstream `__require('process')` shim defect that breaks pure
  ESM `import`; see the `crossCheckRealDecider` comment in `run-e2e.mjs`.)

**Scoped out (covered by other gates — not faked here):**

- Production Rekor signing of the bundle (audit-harness `emit-evidence.sh` +
  intent-rollout-gate v0.2.0 keyless signing).
- Paid LLM behavioral judging (j-rig's own eval lane with real provider budget).
- Hosted dashboard deploy (intent-eval-dashboard deploy workflow).

## Files

| File                                     | What                                                                               |
| ---------------------------------------- | ---------------------------------------------------------------------------------- |
| `run-e2e.mjs`                            | The harness — pipes a fixture bundle through all 5 seams, asserts S1–S5.           |
| `package.json`                           | Self-contained deps: pinned kernel + optional rollout-gate. Not published.         |
| `fixtures/audit-harness-row.json`        | HOP-1 output: a kernel-canonical gate-result/v1 in-toto Statement.                 |
| `fixtures/jrig-behavioral-row.json`      | HOP-3 output: a behavioral gate-result/v1 row j-rig appends.                       |
| `fixtures/jrig-failing-row.json`         | A `fail`-decision row for the S4.3 forbidden-decision case.                        |
| `fixtures/bad-row.uppercase-result.json` | Legacy `result:"PASS"` draft row — MUST be rejected at S1 (enum-case drift guard). |
| `fixtures/policy.allow.json`             | Policy the unified bundle satisfies → expect `allow`.                              |
| `fixtures/policy.block-missing.json`     | Policy requiring a gate the bundle lacks → expect `block`.                         |
| `fixtures/policy.block-forbidden.json`   | Policy used with a `fail` row → expect `block`.                                    |

## Adding a seam / repo

Add a numbered seam contract in spec § 3, a fixture here, and the assertion block in
`run-e2e.mjs`. The harness re-validates every fixture against the published kernel as
its first step, so a rotted fixture fails loudly at the top of the run.

## Known upstream issue surfaced by this harness

The current `audit-harness` `conform`/`audit`/`cred-gate` verbs emit the **legacy
v0.3.0 envelope** (`result: "PASS"` UPPERCASE, `timestamp`, missing
`gate_name`/`gate_version`/`gate_decision`/`coverage`/`policy_ref`) — which does **not**
conform to the kernel `gate-result/v1` body. The lab's own `ci/emit-evidence.ts`
emits the correct kernel-canonical shape. When the harness shells out to a live
`audit-harness conform`, it records this as `S1.live` emitter-alignment gap rather
than silently passing. The kernel-canonical fixture is used for the flow. This is the
e2e lane doing exactly its job: detecting cross-repo wire drift that each repo's own
green CI cannot see.
