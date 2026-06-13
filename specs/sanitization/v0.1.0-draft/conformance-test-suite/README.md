# Sanitization conformance test suite — v0.1.0-draft

The PASS/FAIL fixture suite mandated by SPEC § 7 (the CISO non-negotiable, DR-010 § 7 Q3).
A claim of conformance against the sanitization spec is not a claim without a green run of
this suite (`specs/README.md` authoring conventions).

## What the suite proves

Per SPEC § 7 R13, the suite ships two fixture classes:

- **MUST-REDACT** (`fixtures/must-redact/`) — traces with a planted secret of each forbidden
  class (§ 4 credential shapes, § 5 nested arg secrets, § 6 reasoning that quotes/describes a
  secret) plus adversarial cases. The pipeline MUST redact to a sentinel **or** refuse
  emission; the final escape scan over the result MUST find **zero** matches. A row emitted
  containing the planted secret is a suite **FAIL**.
- **MUST-PRESERVE** (`fixtures/must-preserve/`) — secret-free traces with credential-adjacent
  *benign* content. The pipeline MUST retain forensic semantics (structural fields intact,
  reasoning summary keeps decision content, benign content not over-redacted into uselessness).
  A row that destroys all forensic value is a suite **FAIL** (over-redaction defeats the
  purpose of emitting the trace).

## The fail-closed rule (SPEC R14)

The gate is green **only if** every MUST-REDACT fixture produces zero escape-scan matches (or
a documented emission refusal) **and** every MUST-PRESERVE fixture retains its declared
forensic content. An **indeterminate** outcome (neither clearly redacted nor clearly refused)
counts as a **FAIL**, never a pass — fail-closed per SPEC R2.

## Fixture format

Each fixture is a JSON document:

```jsonc
{
  "fixture_id": "MR-001",                  // MR- = must-redact, MP- = must-preserve
  "class": "must-redact",                  // or "must-preserve"
  "description": "<what this fixture exercises>",
  "spec_rules": ["R4", "R12"],             // the SPEC rules under test
  "input_trace": { /* a SessionTrace-shaped fragment, pre-sanitization */ },
  "planted_secret": "<the exact secret string, MUST-REDACT only>",
  "expected": {
    "escape_scan_matches": 0,              // MUST be 0 for a pass
    "outcome": "redacted | refused",       // MUST-REDACT: one of these
    "preserved_assertions": [ /* MUST-PRESERVE: forensic content that MUST survive */ ]
  }
}
```

The `planted_secret` in a MUST-REDACT fixture is the literal value the escape scan (SPEC R12)
searches the emitted artifact for; finding it anywhere in the output is the FAIL condition.
The fixtures are the only place a literal secret-shaped string lives, and it lives **only in
the test input** — never in any emitted/signed artifact (SPEC R7).

## The CI gate (SPEC R14)

A conforming deployment wires this suite as a **required CI check**. The reference runner
loads every fixture, runs the SPEC § 4–§ 6 pipeline + the § 7 R12 escape scan, and asserts
each fixture's `expected` block. The runner is shipped by the first reference implementer
(the lab test harness or the emitting tool's repo); this directory pins the **fixtures + the
expected outcomes**, which are the normative artifact.

## Status

`v0.1.0-draft` — fixtures defined; the suite goes green when a reference implementation runs
it. Passing this suite satisfies the DR-010 § 7 Q3 CISO revisit trigger for the REJECTED
`agent-loop-trace/v1` predicate URI — it does **not** reserve the URI (a Class-1 ISEDC act,
SPEC R15).
