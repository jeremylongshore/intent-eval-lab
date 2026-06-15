# Snapshot-currency Evidence Bundle rows

This directory holds the **`gate-result/v1` Evidence Bundle row** emitted by the
spec-drift-watch gate on every audit/cron run (`iel-E07` residual; DR-010 Q3
unification thesis: *every gate emits an Evidence Bundle row*).

## What `gate-result.json` is

An [in-toto Statement v1](https://in-toto.io/Statement/v1) whose
`predicateType` is `https://evals.intentsolutions.io/gate-result/v1` and whose
predicate body is a schema-valid `gate-result/v1` row (the kernel's NORMATIVE
predicate — Blueprint B § 7.4, published as
`@intentsolutions/core` `schemas/v1/gate-result.schema.json`).

The row records the verdict of the spec-snapshot-currency check — *"do all 16
monitored upstream spec surfaces still match their committed byte-hash
snapshots?"*:

| Run condition | `gate_decision` | `advisory_severity` |
| --- | --- | --- |
| All monitored surfaces still match their anchored snapshots | `pass` | — |
| One or more surfaces drifted (byte-hash changed) | `advisory` | `warn` |
| No drift, but a surface could not be observed this run | `advisory` | `info` |
| Empty / malformed drift report | `error` | — |

Byte-drift is `advisory`, not `fail`: a changed upstream page is the **signal to
reconcile** (re-vendor + promote into the kernel — see the auto-opened drift
issue's "Next steps"), not a defect this run introduced. The workflow still goes
red via its own drift gate; this row records the verdict, it does not re-decide
blocking.

## How it is produced

`scripts/emit-snapshot-currency.py` reads the live `drift-report.json` that
`spec-drift-check.sh --both` wrote, classifies it, and emits the Statement. The
row is **content-addressed**: `input_hash` (and the in-toto subject digest) is
the sha256 of the exact drift report the gate evaluated, so the row is provably
bound to what it judged. Determinism: all time-varying inputs are arguments, so
the same report + args produce byte-identical output.

`gate-result.json` is **regenerated and committed each run** — it always holds
the latest verdict. History is recoverable from git (each run is a commit) and
from the append-only `archive/` + `specs/lineage/` tiers the same workflow
maintains.

## Signing posture (gated, deliberate)

The committed row is **UNSIGNED**. Pushing a predicate-URI'd attestation to a
public transparency log (Rekor) under `evals.intentsolutions.io` is BLOCKED
until DNSSEC + CAA clear for that namespace (CISO binding, ISEDC v1 Q1
2026-05-10; tracked as `iah-E06`). Emitting the **row** is the deliverable;
signing is a separate, gated step that consumes this output via
`audit-harness` `emit-evidence.sh --sign --rekor-url …`.
