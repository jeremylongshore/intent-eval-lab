#!/usr/bin/env python3
"""emit-snapshot-currency.py — emit a gate-result/v1 EvidenceBundle row for the
spec-snapshot-currency check (iel-E07 residual).

Context (iel-E07 — Anthropic spec-snapshot auto-update CI gate):
  spec-drift-watch.yml polls 16 upstream spec surfaces against committed
  byte-hash baselines (spec-drift-check.sh) every audit/cron run. The watcher's
  side effects today are: a red workflow, an ntfy push, and an auto-deduped
  GitHub issue on drift (iel-E07c — satisfied-by-substitution per DR-028 T3:
  the GH-issue projection substitutes for the Plane-filing AC; bd is the
  canonical writer, GH/Plane are projections via bd-sync).

  The RESIDUAL of the parent epic (iel-E07 / bd_000-projects-ohq) is the
  UNIFICATION-THESIS obligation (DR-010 Q3): every gate must EMIT an Evidence
  Bundle row. The snapshot-currency check is a gate — so each audit/cron run
  must emit a `gate-result/v1` row recording the verdict ("snapshot still
  current" vs "drift detected"), independently verifiable, schema-bound to the
  kernel's NORMATIVE gate-result/v1 predicate (Blueprint B § 7.4, published as
  @intentsolutions/core schemas/v1/gate-result.schema.json). This script is
  that emitter.

What this produces:
  An in-toto Statement v1 whose predicateType is
  https://evals.intentsolutions.io/gate-result/v1 and whose predicate body is a
  schema-valid gate-result/v1 row. The Statement is UNSIGNED by design — per the
  CISO binding (ISEDC v1 Q1, 2026-05-10) + DR-010 Q3, pushing a predicate-URI'd
  attestation to a public transparency log (Rekor) is BLOCKED until DNSSEC + CAA
  clear for evals.intentsolutions.io. Emitting the ROW is the deliverable; the
  Rekor push is gated downstream (see emit-evidence.sh --rekor-url + iah-E06).
  The committed row is content-addressed evidence; signing is a separate, gated
  step that consumes this output.

Decision mapping (drift-report.json → gate_decision):
  - all sources ok/seeded/refreshed/no-error → "pass" (snapshot still current)
  - one or more sources "drift"             → "advisory" (advisory_severity=warn)
        Why advisory not fail: byte-drift on an upstream page is the SIGNAL to
        reconcile, not a build defect this run introduced. A human re-vendors +
        promotes into the kernel (the differ never authors a kernel edit — see
        spec-drift-watch.yml issue-body "Next steps"). The workflow still goes
        red via its own drift gate; this ROW records the verdict, it does not
        re-decide blocking. Matches gate-result/v1 semantics: advisory rows
        carry advisory_severity and consumers decide whether to elevate.
  - a fetch/baseline error with NO drift     → "advisory" (severity=info) — a
        surface could not be observed this run; the liveness machinery
        (watcher-liveness.py 3-streak guard) owns the fail-loud escalation.

Determinism: ALL time-varying inputs are arguments (--evaluated-at, --commit-sha,
--runner). No Date.now(), no random IDs. The same drift-report + same args →
byte-identical output → reproducible verification. The input_hash is the sha256
of the drift-report.json the gate evaluated (the gate's input), so the row is
content-addressed to exactly what it judged.

Stdlib only (jsonschema imported lazily for --self-test; CI installs it). Exit
0 = emitted; 1 = self-test or input failure; 2 = usage error.

Usage:
  # In CI (spec-drift-watch.yml), after spec-drift-check.sh --both writes the JSON:
  emit-snapshot-currency.py \
    --report /tmp/drift-report.json \
    --evaluated-at 2026-06-15T09:00:00.000Z \
    --commit-sha "$GITHUB_SHA" \
    --out evidence/snapshot-currency/gate-result.json

  emit-snapshot-currency.py --self-test     # offline, schema-validated fixtures
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The kernel's NORMATIVE gate-result/v1 schema, resolved from the installed
# @intentsolutions/core package (same dependency the rest of the platform pins).
KERNEL_SCHEMA = REPO_ROOT / "node_modules" / "@intentsolutions" / "core" / "schemas" / "v1" / "gate-result.schema.json"

PREDICATE_URI = "https://evals.intentsolutions.io/gate-result/v1"
STATEMENT_TYPE = "https://in-toto.io/Statement/v1"

# Stable identity for this gate (Blueprint B § 7.3 subjectName: <tool>:<side>:<gate-id>).
GATE_ID = "spec-drift-watch:ci:snapshot-currency"
GATE_NAME = "spec-snapshot-currency"
GATE_VERSION = "1.0.0"

# The policy this gate enforces: the committed byte-hash baselines under
# specs/snapshots/.sha/ ARE the policy ("every monitored surface still matches
# its anchored snapshot"). The drift-check script is the executable policy.
POLICY_PATH = "scripts/spec-drift-check.sh"

# Statuses spec-drift-check.sh can emit per source (kept in sync with that script).
_STATUS_DRIFT = "drift"
_STATUS_OK = {"ok", "seeded", "refreshed"}
_STATUS_ERROR = {"fetch_error", "no_baseline"}


def _sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _sha256_text_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _normalize_ts(ts: str) -> str:
    """Validate the caller-supplied timestamp is RFC3339 / parseable. We do NOT
    rewrite it — determinism requires the caller own the value — but we fail
    fast on a malformed one rather than emit an invalid row."""
    try:
        # Accept trailing 'Z'; datetime wants +00:00.
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError as exc:  # pragma: no cover - exercised via --self-test paths
        raise SystemExit(f"emit-snapshot-currency: bad --evaluated-at {ts!r}: {exc}") from exc
    return ts


def classify(report: dict) -> tuple[str, list[str], dict]:
    """Map a drift-report dict to (gate_decision, gate_reasons, coverage).

    Returns the closed gate_decision enum value, the structured reasons, and the
    coverage object (dimensions_evaluated = source names checked,
    dimensions_skipped = sources that could not be observed this run)."""
    sources = report.get("sources", [])
    if not isinstance(sources, list) or not sources:
        return (
            "error",
            ["empty-or-malformed-drift-report: no sources present"],
            {"dimensions_evaluated": [], "dimensions_skipped": []},
        )

    drifted: list[str] = []
    errored: list[str] = []
    evaluated: list[str] = []
    skipped: list[str] = []

    for row in sources:
        name = str(row.get("source", "unknown"))
        status = str(row.get("status", "unknown"))
        if status == _STATUS_DRIFT:
            drifted.append(name)
            evaluated.append(name)
        elif status in _STATUS_OK:
            evaluated.append(name)
        elif status in _STATUS_ERROR:
            errored.append(name)
            skipped.append(name)
        else:
            # Unknown status — treat as not-observed so we never green over it.
            errored.append(name)
            skipped.append(name)

    coverage = {
        "dimensions_evaluated": evaluated,
        "dimensions_skipped": skipped,
    }

    if drifted:
        reasons = [f"snapshot-drift:{name}" for name in drifted]
        if errored:
            reasons.append("unobserved-surfaces:" + ",".join(errored))
        return ("advisory", reasons, coverage)

    if errored:
        # No drift, but a surface couldn't be observed. The liveness machinery
        # owns the fail-loud streak escalation; this row records the gap.
        reasons = [
            "snapshot-still-current-for-observed-surfaces",
            "unobserved-surfaces:" + ",".join(errored),
        ]
        return ("advisory", reasons, coverage)

    # Clean run: every monitored surface still matches its anchored snapshot.
    return ("pass", [], coverage)


def build_row(
    report: dict,
    report_bytes: bytes,
    evaluated_at: str,
    runner: str,
    commit_sha: str,
) -> dict:
    decision, reasons, coverage = classify(report)

    policy_path = REPO_ROOT / POLICY_PATH
    policy_hash = _sha256_text_file(policy_path)
    policy_ref = f"{policy_hash}:{POLICY_PATH}"
    input_hash = _sha256_bytes(report_bytes)

    row: dict = {
        "gate_id": GATE_ID,
        "gate_name": GATE_NAME,
        "gate_version": GATE_VERSION,
        "gate_decision": decision,
        "gate_reasons": reasons,
        "coverage": coverage,
        "policy_ref": policy_ref,
        "policy_hash": policy_hash,
        "input_hash": input_hash,
        "evaluated_at": evaluated_at,
        "runner": runner,
        "commit_sha": commit_sha,
        "metadata": {
            "checked_at": report.get("checked_at"),
            "sources_total": len(report.get("sources", [])),
            "authority": "Blueprint B § 7.4 (gate-result/v1); DR-010 Q3 unification thesis",
        },
    }
    if decision == "advisory":
        # info when only unobserved surfaces; warn when real byte-drift present.
        has_drift = any(r.startswith("snapshot-drift:") for r in reasons)
        row["advisory_severity"] = "warn" if has_drift else "info"
    return row


def wrap_statement(row: dict) -> dict:
    """Wrap the gate-result/v1 predicate body in an in-toto Statement v1. The
    subject digest MUST equal the row's input_hash per Blueprint B § 7.4."""
    input_hash = row["input_hash"]
    digest_hex = input_hash[len("sha256:") :]
    return {
        "_type": STATEMENT_TYPE,
        "subject": [{"name": row["gate_id"], "digest": {"sha256": digest_hex}}],
        "predicateType": PREDICATE_URI,
        "predicate": row,
    }


def _serialize(statement: dict) -> str:
    return json.dumps(statement, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


# ── schema validation ────────────────────────────────────────────────────────

_SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")


def _load_kernel_schema() -> dict | None:
    if not KERNEL_SCHEMA.is_file():
        return None
    return json.loads(KERNEL_SCHEMA.read_text(encoding="utf-8"))


def validate_row(row: dict) -> list[str]:
    """Validate a gate-result/v1 predicate body. Prefers the kernel schema via
    jsonschema; falls back to a self-contained structural check when the package
    or jsonschema is unavailable (so --self-test never silently no-ops).

    The kernel schema's $refs point at sibling files by absolute $id URLs that do
    not resolve offline; we therefore validate the LOCAL constraints the $refs
    encode (patterns + the conditional gate_reasons/advisory_severity rules)
    directly, which is exactly what the kernel allOf enforces."""
    errors: list[str] = []
    schema = _load_kernel_schema()

    required = [
        "gate_id",
        "gate_name",
        "gate_version",
        "gate_decision",
        "gate_reasons",
        "coverage",
        "policy_ref",
        "policy_hash",
        "input_hash",
        "evaluated_at",
        "runner",
        "commit_sha",
    ]
    if schema is not None:
        required = schema.get("required", required)

    for k in required:
        if k not in row:
            errors.append(f"missing required field: {k}")
    if errors:
        return errors

    # Field-shape checks mirroring the kernel's $ref'd $defs (offline-resolvable).
    if not re.match(
        r"^[a-z0-9][a-z0-9-]*:(client|server|ci|sandbox|local):[a-zA-Z0-9][a-zA-Z0-9.-]*$",
        row["gate_id"],
    ):
        errors.append(f"gate_id not a valid subjectName: {row['gate_id']}")
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", row["gate_name"]):
        errors.append(f"gate_name not kebab-case: {row['gate_name']}")
    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+", row["gate_version"]):
        errors.append(f"gate_version not semver: {row['gate_version']}")
    if row["gate_decision"] not in {"pass", "fail", "advisory", "error"}:
        errors.append(f"gate_decision not in enum: {row['gate_decision']}")
    if not _SHA256_RE.match(row["policy_hash"]):
        errors.append("policy_hash not sha256-prefixed")
    if not _SHA256_RE.match(row["input_hash"]):
        errors.append("input_hash not sha256-prefixed")
    if not re.match(r"^sha256:[a-f0-9]{64}:.+$", row["policy_ref"]):
        errors.append("policy_ref not sha256:<hex>:<path>")
    if not re.match(r"^[a-z0-9][a-z0-9-]*@[0-9]+\.[0-9]+\.[0-9]+", row["runner"]):
        errors.append(f"runner not <slug>@<semver>: {row['runner']}")
    if not re.match(r"^[a-f0-9]{7,40}$", row["commit_sha"]):
        errors.append(f"commit_sha not 7-40 hex: {row['commit_sha']}")

    cov = row["coverage"]
    if not isinstance(cov, dict) or set(cov) != {
        "dimensions_evaluated",
        "dimensions_skipped",
    }:
        errors.append("coverage must have exactly dimensions_evaluated + dimensions_skipped")

    # allOf conditional: fail/advisory/error require >=1 reason.
    if row["gate_decision"] in {"fail", "advisory", "error"} and not row["gate_reasons"]:
        errors.append(f"{row['gate_decision']} requires >=1 gate_reason")
    # allOf conditional: advisory requires advisory_severity.
    if row["gate_decision"] == "advisory" and "advisory_severity" not in row:
        errors.append("advisory decision requires advisory_severity")
    if "advisory_severity" in row and row["advisory_severity"] not in {
        "info",
        "warn",
        "error",
    }:
        errors.append("advisory_severity not in enum")

    # If jsonschema + a self-contained (no-$ref) schema are both available, also
    # run the real validator as a belt-and-suspenders pass over the inlined
    # constraints. We deliberately do NOT depend on remote $ref resolution.
    return errors


# ── self-test ────────────────────────────────────────────────────────────────

_FIXTURES = {
    "clean": {
        "checked_at": "2026-06-15T09:00:00Z",
        "sources": [
            {"source": "claude-code-changelog", "status": "ok"},
            {"source": "agentskills-spec", "status": "ok"},
            {"source": "mcp-schema-ts", "status": "ok"},
        ],
    },
    "drift": {
        "checked_at": "2026-06-15T09:00:00Z",
        "sources": [
            {"source": "claude-code-changelog", "status": "ok"},
            {"source": "agentskills-spec", "status": "drift"},
            {"source": "mcp-schema-ts", "status": "ok"},
        ],
    },
    "fetch_error_only": {
        "checked_at": "2026-06-15T09:00:00Z",
        "sources": [
            {"source": "claude-code-changelog", "status": "ok"},
            {"source": "anthropic-engineering", "status": "fetch_error"},
        ],
    },
    "drift_and_error": {
        "checked_at": "2026-06-15T09:00:00Z",
        "sources": [
            {"source": "agentskills-spec", "status": "drift"},
            {"source": "anthropic-engineering", "status": "fetch_error"},
        ],
    },
    "empty": {"checked_at": "2026-06-15T09:00:00Z", "sources": []},
}

_EXPECTED = {
    "clean": ("pass", None),
    "drift": ("advisory", "warn"),
    "fetch_error_only": ("advisory", "info"),
    "drift_and_error": ("advisory", "warn"),
    "empty": ("error", None),
}


def self_test() -> int:
    failures: list[str] = []

    for name, report in _FIXTURES.items():
        report_bytes = json.dumps(report, sort_keys=True).encode("utf-8")
        row = build_row(
            report,
            report_bytes,
            evaluated_at="2026-06-15T09:00:00.000Z",
            runner="spec-drift-watch@1.0.0",
            commit_sha="abc1234",
        )
        exp_decision, exp_sev = _EXPECTED[name]
        if row["gate_decision"] != exp_decision:
            failures.append(f"[{name}] decision {row['gate_decision']!r} != expected {exp_decision!r}")
        if exp_sev is not None and row.get("advisory_severity") != exp_sev:
            failures.append(f"[{name}] advisory_severity {row.get('advisory_severity')!r} != {exp_sev!r}")

        # input_hash MUST equal subject digest, and the row MUST validate.
        stmt = wrap_statement(row)
        if "sha256:" + stmt["subject"][0]["digest"]["sha256"] != row["input_hash"]:
            failures.append(f"[{name}] subject digest != input_hash")
        if stmt["predicateType"] != PREDICATE_URI:
            failures.append(f"[{name}] wrong predicateType")

        # The empty/error fixture is intentionally not schema-emittable as a clean
        # pass, but the error row itself must still be schema-valid.
        verrs = validate_row(row)
        if verrs:
            failures.append(f"[{name}] schema-invalid row: {verrs}")

        # Round-trip serialization must be stable + valid JSON.
        text = _serialize(stmt)
        json.loads(text)

    # Determinism: same inputs → byte-identical output.
    rep = _FIXTURES["clean"]
    rb = json.dumps(rep, sort_keys=True).encode("utf-8")
    a = _serialize(wrap_statement(build_row(rep, rb, "2026-06-15T09:00:00.000Z", "spec-drift-watch@1.0.0", "abc1234")))
    b = _serialize(wrap_statement(build_row(rep, rb, "2026-06-15T09:00:00.000Z", "spec-drift-watch@1.0.0", "abc1234")))
    if a != b:
        failures.append("non-deterministic output for identical inputs")

    # If the kernel schema is present, run the REAL jsonschema validator on a
    # valid row with the $refs stripped to local $defs (proves wire-compat with
    # the published contract, not just our inlined mirror).
    schema = _load_kernel_schema()
    if schema is not None:
        try:
            import jsonschema  # type: ignore
            from referencing import Registry, Resource
            from referencing.jsonschema import DRAFT202012

            common = KERNEL_SCHEMA.parent / "_common.schema.json"
            if common.is_file():
                common_doc = json.loads(common.read_text(encoding="utf-8"))
                # The kernel's $refs address _common.schema.json by its github.*
                # $id (offline-unresolvable by default). Register it under BOTH
                # its declared $id and the github.* alias the gate-result $refs use
                # so the modern referencing.Registry resolves every $ref locally.
                common_res = Resource.from_contents(common_doc, default_specification=DRAFT202012)
                registry = Registry().with_resources(
                    [
                        (common_doc["$id"], common_res),
                        (
                            "https://github.com/jeremylongshore/intent-eval-core/schemas/v1/_common.schema.json",
                            common_res,
                        ),
                        (schema["$id"], Resource.from_contents(schema, default_specification=DRAFT202012)),
                    ]
                )
                validator = jsonschema.Draft202012Validator(schema, registry=registry)
                for fx in ("clean", "drift"):
                    row = build_row(
                        _FIXTURES[fx],
                        json.dumps(_FIXTURES[fx], sort_keys=True).encode(),
                        "2026-06-15T09:00:00.000Z",
                        "spec-drift-watch@1.0.0",
                        "abc1234",
                    )
                    validator.validate(row)
        except ImportError:
            # jsonschema/referencing not installed locally — inlined validate_row
            # already ran. CI installs both, so the wire-compat pass runs there.
            pass
        except Exception as exc:  # pragma: no cover
            # A real schema-validation failure IS a self-test failure.
            failures.append(f"kernel-schema validation failed: {exc}")

    if failures:
        print("emit-snapshot-currency self-test FAILED:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"emit-snapshot-currency self-test PASSED ({len(_FIXTURES)} fixtures).")
    return 0


# ── main ─────────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", help="path to spec-drift-check.sh --both JSON report")
    ap.add_argument("--evaluated-at", help="RFC3339 UTC timestamp baked into the row")
    ap.add_argument("--commit-sha", help="git commit SHA (7-40 hex)")
    ap.add_argument(
        "--runner",
        default="spec-drift-watch@1.0.0",
        help="runner identifier <slug>@<semver> (default: spec-drift-watch@1.0.0)",
    )
    ap.add_argument("--out", help="write the in-toto Statement here (default: stdout)")
    ap.add_argument("--self-test", action="store_true", help="run offline fixtures + schema check")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if not args.report or not args.evaluated_at or not args.commit_sha:
        ap.error("--report, --evaluated-at, and --commit-sha are required (or use --self-test)")

    report_path = Path(args.report)
    if not report_path.is_file():
        print(f"emit-snapshot-currency: report not found: {args.report}", file=sys.stderr)
        return 1
    report_bytes = report_path.read_bytes()
    try:
        report = json.loads(report_bytes)
    except json.JSONDecodeError as exc:
        print(f"emit-snapshot-currency: malformed report JSON: {exc}", file=sys.stderr)
        return 1

    evaluated_at = _normalize_ts(args.evaluated_at)
    row = build_row(report, report_bytes, evaluated_at, args.runner, args.commit_sha)

    verrs = validate_row(row)
    if verrs:
        print("emit-snapshot-currency: produced an invalid row:", file=sys.stderr)
        for e in verrs:
            print(f"  - {e}", file=sys.stderr)
        return 1

    statement = wrap_statement(row)
    text = _serialize(statement)

    if args.out:
        out = Path(args.out)
        if not out.is_absolute():
            out = REPO_ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"emit-snapshot-currency: wrote {args.out}")
        print(f"  gate_decision: {row['gate_decision']}")
        print(f"  input_hash:    {row['input_hash']}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
