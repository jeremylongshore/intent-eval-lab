# Tier-bridge conformance test suite — v0.1.0-draft

The fixture suite mandated by [`SPEC.md`](../SPEC.md) § 10. A claim of conformance against the
tier-bridge spec is not a claim without a green run of this suite (`specs/README.md` authoring
conventions).

## What the suite proves

The suite enumerates each _reachable_ `(t1, t2, t3)` tier-verdict triple from the § 6 R9
decision table and asserts the spec-mandated final verdict, plus the fail-fast invariants:

| `t1`   | `t2`              | `t3`                    | Expected final | Invariant                                                                   |
| ------ | ----------------- | ----------------------- | -------------- | --------------------------------------------------------------------------- |
| `FAIL` | _any_             | must be `SKIPPED`       | `FAIL`         | R3 fail-fast — behavioral tier never runs after a structural-floor miss     |
| `PASS` | `RED`             | must be `SKIPPED`       | `FAIL`         | R2 fail-fast — behavioral tier never runs against a known production hazard |
| `PASS` | `GREEN`\|`YELLOW` | `GREEN`                 | `VERIFIED`     | R6 — behavioral eval actually ran and passed                                |
| `PASS` | `GREEN`\|`YELLOW` | `RED`                   | `FAIL`         | R7 — behavioral failure blocks                                              |
| `PASS` | `GREEN`\|`YELLOW` | `SKIPPED`               | `PASS`         | R8 — static-only promotion                                                  |
| `PASS` | `GREEN`           | `SKIPPED` (unavailable) | `PASS`         | R15 + R16 — absence is never `FAIL`, never `VERIFIED`                       |

It also asserts the **unreachable** triples (a behavioral tier present after a fail-fast skip)
are rejected, not silently combined — a conformant implementation MUST NOT produce
`(FAIL, _, GREEN)`, `(FAIL, _, RED)`, `(_, RED, GREEN)`, or `(_, RED, RED)`.

## Why this matters

The verdict-combination algebra (§ 6) is the load-bearing contract: two heterogeneous tier
verdicts — one byte-deterministic (static), one probabilistic (behavioral) — must compose into
exactly one reproducible promotion decision. The suite is what proves the algebra is total and
that the probabilistic tier's non-determinism is confined to _producing_ its verdict, never to
_combining_ the tiers (§ R14).

## Status

Fixtures land alongside the first tier-bridge implementation (the validator + harness wiring
that emits a multi-tier Evidence Bundle per § 7 R11). The decision table above is the
authored-ahead contract those fixtures will encode.

## License

Apache 2.0 — see [LICENSE](../../../../LICENSE) at repo root.
