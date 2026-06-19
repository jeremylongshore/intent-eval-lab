# 055 — LLM-classifier deterministic walls (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 052-AT-SPEC (fetch taxonomy + three tiers) · **Epic:** 9k5h (GH intent-eval-lab#114)

This is the normative reference for the deterministic walls that bracket the **future** LLM drift classifier. The classifier does **not** exist yet and nothing in this repo calls an LLM; the walls land first, so that when a classification ever arrives it is already fenced on every side. Implementation: `scripts/classifier-walls.py`; contracts: `specs/drift-classification/v1/`.

## The one-hop rule (bead intent — Armstrong / Karpathy / Hickey corrections)

The classifier earns exactly **ONE hop**: classify an **already-detected** diff's materiality + which-contract-owner. It never detects drift (that is the deterministic differ, `spec-projection-diff.py`), never fetches (that is `fetch-capture.py`, 052-AT-SPEC), never edits the kernel, never closes a drift signal. Why:

- **Armstrong:** an LLM verdict is an untrusted input, not a control signal. Every consequence it could drive must pass a deterministic gate that can REJECT it outright.
- **Karpathy:** the walls must be non-vacuous — fixture rows prove each wall actually rejects (accept, substring violation, schema-invalid, forbidden action, tier not earned), and the eval set's recall floor on `material` is the promotion currency.
- **Hickey:** the classification is data, not prose — a schema-validated row that any downstream tool can consume without parsing English.

## The two walls

| Wall          | Check                                                                                                                                                               | On failure                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **PRE-WALL**  | every entry in `claimed_changed_fields` must appear as a **literal substring of the fetched bytes** — the tier-2 vendored snapshot the diff came from (052-AT-SPEC) | REJECT. A classifier cannot claim a field the upstream page never mentions (hallucination firewall).                                   |
| **POST-WALL** | if the classification implies a schema-affecting change (`label: material`), the resulting schema must still validate the known-good **fixture corpus**             | REJECT. The corpus lives in the kernel repo (`@intentsolutions/core`), so here the post-wall is an **interface**: a hook slot (below). |

**Post-wall hook contract** (kernel-side invocation deferred): the slot is `scripts/hooks/classifier-post-wall` (override: `--post-wall-hook`). When present it is invoked as `<hook> <row.json> <snapshot>`; exit 0 = corpus still validates, nonzero = REJECT with the hook's output. When absent, the walls script prints an explicit "deferred" note — never a silent pass-as-checked. Wiring the kernel's fixture corpus behind this slot is kernel-repo work.

## The output contract — `drift-classification/v1` row

A classification is a schema-validated ROW (`specs/drift-classification/v1/row.schema.json`, JSON Schema draft 2020-12), not prose:

```json
{
  "surface_id": "agentskills-spec", // or "case_ref" in eval mode (anyOf)
  "diff_ref": "spec-projection-diff:REQUIRED_CHANGED:allowed-tools",
  "label": "material", // material | immaterial
  "contract_owner": "skill-frontmatter", // registry contract name
  "claimed_changed_fields": ["allowed-tools"], // pre-wall input; material ⇒ minItems 1
  "confidence": 0.92, // [0,1], advisory — never overrides a wall
  "model_pin": "example-model-pin-2026-06-01", // exact pin, no aliases
  "classified_at": "2026-06-12T00:00:00Z"
}
```

`additionalProperties: false`; a `material` row with zero claimed fields is schema-invalid by construction (it would dodge the pre-wall). The `$id` is a schema identifier only — **not** an in-toto attestation predicate URI (operational rule 5 stands).

## The autonomy gradient (`autonomy-policy.json` + `earned-tier.json`)

| Action               | Permitted  | Notes                                                                                                                 |
| -------------------- | ---------- | --------------------------------------------------------------------------------------------------------------------- |
| `advisory_comment`   | **always** | comment carrying the validated row on the existing drift issue — lowest blast radius                                  |
| `low_blast_pr`       | **earned** | snapshot / `.sha` / coverage refresh only, never schema or policy content; requires the eval-set recall floor cleared |
| `kernel_schema_edit` | **NEVER**  | fallback: issue-with-proposed-diff; a human lands the change (tier-3 promotion is HUMAN, 052-AT-SPEC)                 |
| `close_drift_signal` | **NEVER**  | only a human declares a drift reconciled — the classifier must not silence the signal that audits it                  |

Unknown actions are rejected (default-deny). Current tier state lives in `specs/drift-classification/v1/earned-tier.json` (default `advisory_comment`).

**Promotion protocol (human-only):** a human runs the eval set (`python3 scripts/drift-eval-runner.py --verify-manifest`, then `--score <predictions.jsonl>` — exits nonzero below recall floor **1.0 on material** cases), confirms the floor is cleared, and commits the updated `earned-tier.json` (tier + `promoted_by` + `promoted_at` + `evidence`) in a reviewed PR. The tier state, the policy, the row schema, and the walls script are **hash-pinned** (`.harness-hash-extra-patterns`), so promotion — like any edit to the enforcement surface — requires a fresh `scripts/audit-harness init` in the same commit; silent self-promotion fails CI. Demotion is the same protocol in reverse, no evidence needed. The eval runner ships separately; **every invocation is guarded by a file-existence check**, so the walls behave identically before and after it lands. At validate time, when the runner and the recorded `evidence.predictions` file both exist, the floor is re-verified (defense in depth) and a failed score rejects the earned action.

## Enforcement

```text
scripts/classifier-walls.py validate ROW.json --against SNAPSHOT [--policy-action ACTION]
```

exits 0 **only if** (row schema-valid) AND (every claimed field is a literal substring of the snapshot bytes) AND (material ⇒ post-wall hook passes or is explicitly deferred) AND (the requested action is permitted at the current earned tier). Exit 1 = REJECT, exit 2 = usage/config error.

- **Deterministic self-test** (`classifier-walls.py --self-test`, fully offline): fixture rows under `specs/drift-classification/v1/examples/` exercise accept, substring-violation reject, schema-invalid reject (plus 9 mutation cases), forbidden-action reject, tier-not-earned reject, the earned-tier accept, both recall-floor outcomes via stub runners, both post-wall hook outcomes, and stdlib-validator ↔ `row.schema.json` agreement when `jsonschema` is importable (CI installs it). Wired into the "Validate specs and docs" job in `ci.yml`.
- Workflow files are harness-hash-pinned; the `ci.yml` edit re-pins `.harness-hash` in the same commit.
