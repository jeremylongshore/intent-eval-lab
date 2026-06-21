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

## Layout

```text
conformance-test-suite/
├── README.md                     # this file
├── run.py                        # stdlib-only runner: re-implements the § 6 algebra and
│                                 #   asserts every fixture's expected_final against it
└── fixtures/
    ├── TB-0NN-*.json             # 11 reachable (t1, t2, t3) -> expected_final tuples
    └── unreachable/
        └── TB-U0N-*.json         #  4 forbidden triples the algebra MUST reject
```

Each reachable fixture is one JSON object: `fixture_id`, a prose `description`, the `spec_rules`
it exercises, the `input` triple `{ t1, t2, t3 }`, the `expected_final` verdict, and a `why`
citing the governing § 6 / § 5 / § 9 rules. Unreachable fixtures carry `expected: "rejected"`
instead of `expected_final`.

### Reachable fixtures (the § 6 R9 decision table, by example)

| Fixture | `(t1, t2, t3)`            | Expected   | Rule(s)        |
| ------- | ------------------------- | ---------- | -------------- |
| TB-001  | `(FAIL, GREEN, SKIPPED)`  | `FAIL`     | R3 fail-fast   |
| TB-002  | `(FAIL, YELLOW, SKIPPED)` | `FAIL`     | R3 (any `t2`)  |
| TB-003  | `(FAIL, RED, SKIPPED)`    | `FAIL`     | R2+R3          |
| TB-004  | `(PASS, RED, SKIPPED)`    | `FAIL`     | R2 fail-fast   |
| TB-005  | `(PASS, GREEN, GREEN)`    | `VERIFIED` | R6             |
| TB-006  | `(PASS, YELLOW, GREEN)`   | `VERIFIED` | R6 (YELLOW OK) |
| TB-007  | `(PASS, GREEN, RED)`      | `FAIL`     | R7             |
| TB-008  | `(PASS, YELLOW, RED)`     | `FAIL`     | R7             |
| TB-009  | `(PASS, GREEN, SKIPPED)`  | `PASS`     | R8             |
| TB-010  | `(PASS, YELLOW, SKIPPED)` | `PASS`     | R8             |
| TB-011  | `(PASS, GREEN, SKIPPED*)` | `PASS`     | R15+R16        |

(\* TB-011's `SKIPPED` is caused by the behavioral harness being **unavailable**, not opt-out —
algebraically identical to TB-009, which is exactly the point of R15: absence is never `FAIL` and
never `VERIFIED`, regardless of _why_ Tier 3 was skipped.)

### Unreachable fixtures (rejected, never combined)

| Fixture | `(t1, t2, t3)`         | Why forbidden       |
| ------- | ---------------------- | ------------------- |
| TB-U01  | `(FAIL, GREEN, GREEN)` | R3 forces `SKIPPED` |
| TB-U02  | `(FAIL, GREEN, RED)`   | R3 forces `SKIPPED` |
| TB-U03  | `(PASS, RED, GREEN)`   | R2 forces `SKIPPED` |
| TB-U04  | `(PASS, RED, RED)`     | R2 forces `SKIPPED` |

## Running the suite

```bash
# from this directory:
python3 run.py            # exit 0 = all fixtures match the § 6 algebra; exit 1 = any mismatch
python3 run.py --list     # list every discovered fixture + the runner's computed verdict
```

`run.py` is stdlib-only, offline, and deterministic. It re-implements the § 6 (R5–R9) algebra plus
the § 5 / § 9 reachability guard as a single pure `combine(t1, t2, t3)`, loads every fixture, and
fails if any reachable fixture's computed verdict ≠ its `expected_final` or any unreachable fixture
is NOT rejected. The runner's `combine()` is the authority-following reference: SPEC.md § 6 wins on
any disagreement, and the runner + fixtures move in lock-step with the spec.

## Why this matters

The verdict-combination algebra (§ 6) is the load-bearing contract: two heterogeneous tier
verdicts — one byte-deterministic (static), one probabilistic (behavioral) — must compose into
exactly one reproducible promotion decision. The suite is what proves the algebra is total and
that the probabilistic tier's non-determinism is confined to _producing_ its verdict, never to
_combining_ the tiers (§ R14).

## Status

**Fixtures + runner landed.** The 11 reachable + 4 unreachable fixtures and the stdlib `run.py`
encode the full § 6 R9 decision table and the § 5 / § 9 fail-fast + reachability invariants; the
runner is green against the spec algebra. This proves the **composition algebra** (the bridge's
load-bearing contract) by example, independent of any tool wiring.

What is **still** pending the first end-to-end tier-bridge implementation: the validator + harness
wiring that actually emits a multi-tier Evidence Bundle per § 7 R11 (i.e. real `gate-result/v1`
rows from `validate-skillmd` Tier 1/2 and a real behavioral row from `j-rig` Tier 3, then the
RolloutGate re-deriving the final verdict from the bundle). Those emitters live in other repos
(SPEC § 9.5.1.1 + § 9.5.2.1 cross-repo remainders); this suite proves the algebra those emitters
must compose under, not the emitters themselves.

## License

Apache 2.0 — see [LICENSE](../../../../LICENSE) at repo root.
