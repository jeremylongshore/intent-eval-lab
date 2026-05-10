# `schema/` — JSON Schema 2020-12 files

> **Status: PLACEHOLDER.** Schema files land in Phase B (per `IEL-4`).

## Planned files

| File | Shape |
|---|---|
| `envelope.json` | Top-level bundle envelope (manifest + signature + payload) |
| `gate-result.json` | Single gate-result row (audit-harness emission target) |
| `verdict.json` | Single verdict row (j-rig emission target) |
| `version.json` | Version envelope (`bundle_version` vs `schema_version` semantics) |

All files target [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html) and validate against the meta-schema.

## Authoring conventions

- Every schema declares `$schema: "https://json-schema.org/draft/2020-12/schema"` and a stable `$id`
- Required fields are explicit; unknown fields are accepted (forward-compat)
- Versioning: `schema_version` is a string semver; major bump on field removal/rename, minor bump on additive fields
- Examples in `examples/` directory — at least one positive + one negative per schema

## Cross-references

- Spec: [`../SPEC.md`](../SPEC.md)
- Issue: `IEL-4` ([jeremylongshore/intent-eval-lab#15](https://github.com/jeremylongshore/intent-eval-lab/issues/15))
