# `schema/` — JSON Schema 2020-12 files (REDIRECT STUB)

> **Status: REDIRECT TO KERNEL.** Schemas in this directory are REDIRECT STUBS. The canonical, normative JSON Schemas for the Intent Eval Platform's wire formats live in the kernel package `@intentsolutions/core`. Do not edit the stub files — edits have no normative force. See `000-docs/018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-21.md`.

## Canonical sources

| File                      | Canonical location                                                                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gate-result.schema.json` | [`@intentsolutions/core/schemas/v1/gate-result.schema.json`](https://github.com/jeremylongshore/intent-eval-core/blob/main/schemas/v1/gate-result.schema.json) |
| (other predicate URIs)    | Pending — file each in the kernel before it leaves `sigstore_staging` per DR-010 Q3                                                                            |

## What changed (2026-05-21)

The lab previously hosted the JSON Schema for `gate-result/v1` directly in this directory. Per ISEDC Session 5 (DR 018) Option α-minus ratification, the canonical schema MIGRATED to the kernel package `@intentsolutions/core`. The redirect stub here remains so that:

1. Consumers following old links (Blueprint B § 7.4 line references; SPEC.md § 5 references) land on a discoverable redirect.
2. Cross-origin JSON-Schema `$ref` resolution still produces valid validation (the stub forwards via `$ref` to the kernel's canonical schema).
3. CI drift-check (`.github/workflows/schema-drift.yml`) can detect any attempt to re-introduce normative schema content in this directory.

## Why the migration happened

j-rig's local `GateResultPredicateSchema` mirrored the v0.1.0-draft shape (`result` enum, `timestamp` field). Blueprint B § 7.4 — merged to lab main 2026-05-15 — landed a normative shape (`gate_decision` enum, `evaluated_at` field, +5 required fields). The kernel package `@intentsolutions/core@0.1.0` (published 2026-05-17 with sigstore provenance) shipped the normative shape. The 5-repo IEP convergence requires ONE source of truth; the kernel is it.

Full audit trail:

- **016-RR-LAND-kernel-shadow-inventory-2026-05-20.md** — per-repo per-type re-definition inventory
- **017-RR-LAND-shape-reconciliation-addendum-2026-05-21.md** — field-by-field shape comparison
- **018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-21.md** — ISEDC ratification (Option α-minus)
- **019-AA-AACR-schema-repoint-iel-link-schemas-2026-05-21.md** — Priority 5 closeout AAR

## Cross-references

- Spec (prose, in this repo): [`../SPEC.md`](../SPEC.md) — kernel-canonical declaration block at top
- Normative prose: `intent-eval-lab/000-docs/012-AT-ARCH-platform-runtime-blueprint.md` § 7 (Blueprint B)
- Kernel repo: <https://github.com/jeremylongshore/intent-eval-core>
- Predicate URI namespace: `https://evals.intentsolutions.io/gate-result/v1` (URI is immutable per Blueprint B § 7.2; only the schema location migrated)
