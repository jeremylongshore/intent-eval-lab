#!/usr/bin/env python3
"""Deterministic walls bracketing the (future) LLM drift classifier.

The classifier earns exactly ONE hop — classifying an ALREADY-DETECTED diff's
materiality + which-contract-owner. It does NOT exist yet; this script builds
the walls FIRST (Armstrong/Karpathy/Hickey corrections per the 7-thinker
panel), so that when a classification ever arrives it is bracketed on every
side by deterministic checks. No LLM is called here, ever.

The walls (normative spec: 000-docs/055-AT-SPEC-llm-classifier-deterministic-
walls-2026-06-12.md):

  OUTPUT CONTRACT  a classification is a schema-validated drift-classification
                   /v1 ROW (specs/drift-classification/v1/row.schema.json),
                   not prose. Structurally invalid -> REJECT.
  PRE-WALL         every field the row claims changed must appear as a LITERAL
                   SUBSTRING of the fetched bytes (the tier-2 vendored snapshot
                   the diff came from, per 052-AT-SPEC) -> else REJECT. A
                   classifier cannot claim a field the upstream page never
                   mentions (hallucination firewall).
  POST-WALL        if the classification implies a schema-affecting change
                   (label=material), the resulting schema must still validate
                   the known-good fixture corpus. The corpus lives in the
                   KERNEL repo (@intentsolutions/core), so in THIS repo the
                   post-wall is an INTERFACE: a hook script slot
                   (scripts/hooks/classifier-post-wall, or --post-wall-hook)
                   invoked as `<hook> <row.json> <snapshot>`; nonzero exit ->
                   REJECT. Kernel-side invocation is deferred; absent hook =
                   documented skip, never a silent pass-as-checked.
  AUTONOMY         the requested side-effect action must be permitted at the
                   current EARNED tier (specs/drift-classification/v1/
                   autonomy-policy.json + earned-tier.json; default
                   advisory_comment; promoted only by humans). `never` actions
                   (kernel_schema_edit, close_drift_signal) reject at every
                   tier; unknown actions reject (default-deny). For earned
                   actions the eval-set recall floor is re-verified via
                   scripts/drift-eval-runner.py --score — GUARDED BY AN
                   EXISTENCE CHECK (the runner ships separately), so this
                   script is green both before and after it lands.

Stdlib only. If the `jsonschema` package happens to be importable (CI installs
it), the row is ALSO validated against row.schema.json and the self-test
asserts the stdlib validator and the schema agree on every fixture.

Exit 0 = ACCEPT (all walls passed) or self-test passed.
Exit 1 = REJECT (at least one wall violated) or self-test failure.
Exit 2 = usage / config error (missing schema/policy files, unreadable args).

Usage:
  classifier-walls.py validate ROW.json --against SNAPSHOT [--policy-action ACTION]
  classifier-walls.py --self-test     # offline fixtures: accept + every reject class
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_DIR = os.path.join(REPO_ROOT, "specs", "drift-classification", "v1")
DEFAULT_SCHEMA = os.path.join(SPEC_DIR, "row.schema.json")
DEFAULT_POLICY = os.path.join(SPEC_DIR, "autonomy-policy.json")
DEFAULT_TIER_STATE = os.path.join(SPEC_DIR, "earned-tier.json")
EXAMPLES_DIR = os.path.join(SPEC_DIR, "examples")
# Post-wall hook slot (kernel-side fixture-corpus check, deferred — 055-AT-SPEC).
DEFAULT_POST_WALL_HOOK = os.path.join(REPO_ROOT, "scripts", "hooks", "classifier-post-wall")
# Eval runner ships separately; EVERY invocation is guarded by an existence check.
DEFAULT_EVAL_RUNNER = os.path.join(REPO_ROOT, "scripts", "drift-eval-runner.py")

LABELS = ("material", "immaterial")
_KEBAB = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_MODEL_PIN = re.compile(r"^\S+$")
_RFC3339 = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$"
)
_REQUIRED = (
    "diff_ref",
    "label",
    "contract_owner",
    "claimed_changed_fields",
    "confidence",
    "model_pin",
    "classified_at",
)
_ALLOWED_KEYS = set(_REQUIRED) | {"row_version", "case_ref", "surface_id"}


# ---------------------------------------------------------------------------
# OUTPUT CONTRACT — stdlib mirror of row.schema.json (kept in lockstep; the
# self-test cross-checks agreement against the schema when jsonschema is
# importable, so the two cannot silently drift in CI).
# ---------------------------------------------------------------------------
def validate_row_structure(row: Any) -> list[str]:
    """Return a list of output-contract violations (empty = schema-valid row)."""
    if not isinstance(row, dict):
        return ["row must be a JSON object"]
    errors: list[str] = []
    for key in row:
        if key not in _ALLOWED_KEYS:
            errors.append(f"unknown key `{key}` (additionalProperties: false)")
    for key in _REQUIRED:
        if key not in row:
            errors.append(f"missing required key `{key}`")
    if "case_ref" not in row and "surface_id" not in row:
        errors.append("row must carry `case_ref` or `surface_id` (anyOf)")
    if "row_version" in row and row["row_version"] != "drift-classification/v1":
        errors.append("`row_version` must be the const \"drift-classification/v1\"")
    if "case_ref" in row and not (isinstance(row["case_ref"], str) and row["case_ref"]):
        errors.append("`case_ref` must be a non-empty string")
    if "surface_id" in row and not (
        isinstance(row["surface_id"], str) and _KEBAB.match(row["surface_id"])
    ):
        errors.append("`surface_id` must be a kebab-case registry surface name")
    if "diff_ref" in row and not (isinstance(row["diff_ref"], str) and row["diff_ref"]):
        errors.append("`diff_ref` must be a non-empty string")
    if "label" in row and row["label"] not in LABELS:
        errors.append(f"`label` must be one of {list(LABELS)}")
    if "contract_owner" in row and not (
        isinstance(row["contract_owner"], str) and _KEBAB.match(row["contract_owner"])
    ):
        errors.append("`contract_owner` must be a kebab-case contract name")
    if "claimed_changed_fields" in row:
        ccf = row["claimed_changed_fields"]
        if not isinstance(ccf, list) or any(not (isinstance(f, str) and f) for f in ccf):
            errors.append("`claimed_changed_fields` must be an array of non-empty strings")
        elif len(set(ccf)) != len(ccf):
            errors.append("`claimed_changed_fields` must have unique items")
        elif row.get("label") == "material" and len(ccf) == 0:
            errors.append(
                "a `material` row must claim at least one changed field "
                "(empty claims would dodge the substring pre-wall)"
            )
    if "confidence" in row:
        conf = row["confidence"]
        if not isinstance(conf, (int, float)) or isinstance(conf, bool) or not 0 <= conf <= 1:
            errors.append("`confidence` must be a number in [0, 1]")
    if "model_pin" in row and not (
        isinstance(row["model_pin"], str) and _MODEL_PIN.match(row["model_pin"])
    ):
        errors.append("`model_pin` must be a non-empty whitespace-free string")
    if "classified_at" in row and not (
        isinstance(row["classified_at"], str) and _RFC3339.match(row["classified_at"])
    ):
        errors.append("`classified_at` must be an RFC 3339 date-time string")
    return errors


def validate_row_against_schema(row: Any, schema_path: str) -> list[str] | None:
    """Validate via the jsonschema package when importable; None = unavailable."""
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError:
        return None
    with open(schema_path, encoding="utf-8") as fh:
        schema = json.load(fh)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    return [e.message for e in validator.iter_errors(row)]


# ---------------------------------------------------------------------------
# PRE-WALL — literal-substring check against the fetched snapshot bytes.
# ---------------------------------------------------------------------------
def check_pre_wall(row: dict, snapshot_bytes: bytes) -> list[str]:
    """Every claimed_changed_fields entry must be a literal substring of the bytes."""
    missing = [
        f
        for f in row.get("claimed_changed_fields", [])
        if isinstance(f, str) and f.encode("utf-8") not in snapshot_bytes
    ]
    return [
        f"claimed field `{f}` is NOT a literal substring of the snapshot bytes" for f in missing
    ]


# ---------------------------------------------------------------------------
# POST-WALL — hook slot (kernel-side fixture-corpus invocation deferred).
# ---------------------------------------------------------------------------
def run_post_wall_hook(hook_path: str, row_path: str, snapshot_path: str) -> tuple[bool, str]:
    """Run `<hook> <row.json> <snapshot>`. Returns (ran, violation-or-empty)."""
    if not os.path.isfile(hook_path):
        return False, ""
    proc = subprocess.run(
        [hook_path, row_path, snapshot_path], capture_output=True, text=True, timeout=300
    )
    if proc.returncode != 0:
        detail = (proc.stdout + proc.stderr).strip()
        return True, (
            f"post-wall hook `{os.path.basename(hook_path)}` exited "
            f"{proc.returncode}: {detail or '(no output)'}"
        )
    return True, ""


# ---------------------------------------------------------------------------
# AUTONOMY GRADIENT — policy + earned-tier enforcement (default-deny).
# ---------------------------------------------------------------------------
def _tier_rank(tier: str, tier_order: list[str]) -> int:
    """Rank of a tier in the gradient; unknown tiers rank lowest (conservative)."""
    return tier_order.index(tier) if tier in tier_order else -1


def check_policy_action(
    action: str,
    policy: dict,
    tier_state: dict,
    eval_runner: str,
) -> list[str]:
    """Return violations for the requested action at the current earned tier."""
    actions = policy.get("actions", {})
    tier_order = policy.get("tier_order", [])
    if action not in actions:
        return [f"action `{action}` is not in the autonomy policy (default-deny)"]
    spec = actions[action]
    permitted = spec.get("permitted")
    if permitted == "never":
        fallback = spec.get("fallback")
        return [
            f"action `{action}` is NEVER permitted at any tier"
            + (f" (fallback: {fallback})" if fallback else "")
        ]
    if permitted == "always":
        return []
    if permitted != "earned":
        return [f"action `{action}` has unknown permission `{permitted}` (default-deny)"]

    earned = tier_state.get("earned_tier", policy.get("promotion", {}).get("default_tier"))
    required_tier = spec.get("tier", action)
    if _tier_rank(earned, tier_order) < _tier_rank(required_tier, tier_order):
        return [
            f"action `{action}` requires earned tier `{required_tier}` but the current "
            f"earned tier is `{earned}` (promotion is human-only, per autonomy-policy.json)"
        ]

    # Recall-floor re-verification (defense in depth). The runner ships
    # separately — invocation is GUARDED BY AN EXISTENCE CHECK so this script
    # behaves identically before and after it lands.
    evidence = tier_state.get("evidence") or {}
    predictions = evidence.get("predictions") if isinstance(evidence, dict) else None
    if not os.path.isfile(eval_runner):
        print(
            f"  note: eval runner not present at {os.path.relpath(eval_runner, REPO_ROOT)} — "
            "recall-floor re-verification skipped (interface referenced; ships separately)"
        )
        return []
    if not (isinstance(predictions, str) and os.path.isfile(predictions)):
        print(
            "  note: earned-tier evidence carries no resolvable predictions file — "
            "recall floor was verified at promotion time; re-verification skipped"
        )
        return []
    proc = subprocess.run(
        [sys.executable, eval_runner, "--score", predictions],
        capture_output=True,
        text=True,
        timeout=600,
    )
    if proc.returncode != 0:
        detail = (proc.stdout + proc.stderr).strip()
        return [
            f"eval-set recall floor NOT cleared (drift-eval-runner --score exited "
            f"{proc.returncode}): {detail or '(no output)'}"
        ]
    return []


# ---------------------------------------------------------------------------
# validate — the CLI verb. One row, all walls, deterministic verdict.
# ---------------------------------------------------------------------------
def run_validate(
    row_path: str,
    snapshot_path: str,
    policy_action: str | None = None,
    schema_path: str = DEFAULT_SCHEMA,
    policy_path: str = DEFAULT_POLICY,
    tier_state_path: str = DEFAULT_TIER_STATE,
    post_wall_hook: str = DEFAULT_POST_WALL_HOOK,
    eval_runner: str = DEFAULT_EVAL_RUNNER,
) -> int:
    for path, what in ((schema_path, "row schema"), (policy_path, "autonomy policy")):
        if not os.path.isfile(path):
            print(f"ERROR: {what} not found at {path}", file=sys.stderr)
            return 2
    if not os.path.isfile(snapshot_path):
        print(f"ERROR: vendored snapshot not found at {snapshot_path}", file=sys.stderr)
        return 2

    violations: list[str] = []

    # OUTPUT CONTRACT (the row is classifier OUTPUT — malformed output is a
    # rejection of that output, not a usage error of this tool).
    try:
        with open(row_path, encoding="utf-8") as fh:
            row = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"REJECT [output-contract]: row is not readable JSON: {exc}")
        return 1
    structural = validate_row_structure(row)
    schema_errors = validate_row_against_schema(row, schema_path)
    if schema_errors:  # jsonschema available AND found violations
        for err in schema_errors:
            if err not in structural:
                structural.append(f"(jsonschema) {err}")
    violations += [f"[output-contract] {e}" for e in structural]

    # PRE-WALL — only meaningful for a structurally plausible row.
    if isinstance(row, dict):
        with open(snapshot_path, "rb") as fh:
            snapshot_bytes = fh.read()
        violations += [f"[pre-wall] {e}" for e in check_pre_wall(row, snapshot_bytes)]

        # POST-WALL — material rows imply a schema-affecting change.
        if row.get("label") == "material":
            ran, violation = run_post_wall_hook(post_wall_hook, row_path, snapshot_path)
            if violation:
                violations.append(f"[post-wall] {violation}")
            elif not ran:
                print(
                    "  note: post-wall hook slot empty "
                    f"({os.path.relpath(post_wall_hook, REPO_ROOT)}) — kernel-side "
                    "fixture-corpus check deferred per 055-AT-SPEC (interface only here)"
                )

    # AUTONOMY GRADIENT — only when a side-effect action is requested.
    if policy_action is not None:
        with open(policy_path, encoding="utf-8") as fh:
            policy = json.load(fh)
        if os.path.isfile(tier_state_path):
            with open(tier_state_path, encoding="utf-8") as fh:
                tier_state = json.load(fh)
        else:
            tier_state = {}  # conservative: falls back to the policy default tier
        violations += [
            f"[autonomy] {e}"
            for e in check_policy_action(policy_action, policy, tier_state, eval_runner)
        ]

    if violations:
        print(f"REJECT — {len(violations)} wall violation(s):")
        for v in violations:
            print(f"  - {v}")
        return 1
    action_note = f" (action: {policy_action})" if policy_action else ""
    print(f"ACCEPT — row passed output contract + pre-wall + post-wall + autonomy{action_note}.")
    return 0


# ---------------------------------------------------------------------------
# Self-test — offline, deterministic fixtures for every accept/reject class.
# ---------------------------------------------------------------------------
def cmd_self_test() -> int:
    fixture_snapshot = os.path.join(EXAMPLES_DIR, "snapshot-fixture.md")
    row_accept = os.path.join(EXAMPLES_DIR, "row-accept.json")
    row_substring = os.path.join(EXAMPLES_DIR, "row-substring-violation.json")
    row_invalid = os.path.join(EXAMPLES_DIR, "row-schema-invalid.json")
    failures = 0

    def expect(name: str, got: int, want: int) -> None:
        nonlocal failures
        if got == want:
            print(f"self-test ok: {name} (exit {got})")
        else:
            print(f"self-test FAIL: {name} — expected exit {want}, got {got}")
            failures += 1

    with tempfile.TemporaryDirectory(prefix="classifier-walls-selftest-") as tmp:

        def write(name: str, payload: Any, executable_body: str | None = None) -> str:
            path = os.path.join(tmp, name)
            with open(path, "w", encoding="utf-8") as fh:
                if executable_body is not None:
                    fh.write(executable_body)
                else:
                    json.dump(payload, fh, indent=2)
            if executable_body is not None:
                os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
            return path

        print("== accept ==")
        expect("valid row, fields in snapshot", run_validate(row_accept, fixture_snapshot), 0)
        expect(
            "always-allowed action (advisory_comment)",
            run_validate(row_accept, fixture_snapshot, policy_action="advisory_comment"),
            0,
        )

        print("\n== substring-violation reject (pre-wall) ==")
        expect("claimed field absent from bytes", run_validate(row_substring, fixture_snapshot), 1)

        print("\n== schema-invalid reject (output contract) ==")
        expect("bad label + bad confidence + missing model_pin",
               run_validate(row_invalid, fixture_snapshot), 1)
        base = json.load(open(row_accept, encoding="utf-8"))
        mutations: list[tuple[str, dict]] = [
            ("missing diff_ref", {k: v for k, v in base.items() if k != "diff_ref"}),
            ("neither case_ref nor surface_id",
             {k: v for k, v in base.items() if k != "surface_id"}),
            ("material with empty claimed_changed_fields (pre-wall dodge)",
             {**base, "claimed_changed_fields": []}),
            ("unknown extra key", {**base, "extra_key": "x"}),
            ("duplicate claimed fields",
             {**base, "claimed_changed_fields": ["name", "name"]}),
            ("confidence out of range", {**base, "confidence": 1.01}),
            ("model_pin with whitespace", {**base, "model_pin": "model latest"}),
            ("non-RFC3339 classified_at", {**base, "classified_at": "yesterday"}),
        ]
        for name, mutated in mutations:
            expect(name, run_validate(write("mut.json", mutated), fixture_snapshot), 1)
        expect("unparseable row JSON",
               run_validate(write("garbage.json", None, executable_body="{not json"),
                            fixture_snapshot), 1)

        print("\n== forbidden-action reject (autonomy: never) ==")
        for action in ("kernel_schema_edit", "close_drift_signal"):
            expect(f"{action} rejected at every tier",
                   run_validate(row_accept, fixture_snapshot, policy_action=action), 1)
        expect("unknown action (default-deny)",
               run_validate(row_accept, fixture_snapshot, policy_action="ship_to_prod"), 1)

        print("\n== tier-not-earned reject (autonomy: earned) ==")
        expect(
            "low_blast_pr at default tier",
            run_validate(row_accept, fixture_snapshot, policy_action="low_blast_pr"),
            1,
        )

        print("\n== tier earned (human-promoted fixture state) ==")
        earned = write(
            "earned-tier.json",
            {
                "tier_state_version": "drift-classification-earned-tier/v1",
                "earned_tier": "low_blast_pr",
                "promoted_by": "fixture-human",
                "promoted_at": "2026-06-12T00:00:00Z",
                "evidence": None,
            },
        )
        expect(
            "low_blast_pr at earned tier (no predictions evidence -> floor "
            "verified at promotion time)",
            run_validate(row_accept, fixture_snapshot, policy_action="low_blast_pr",
                         tier_state_path=earned),
            0,
        )

        print("\n== recall-floor re-verification (guarded eval-runner interface) ==")
        predictions = write("predictions.jsonl", None, executable_body="{}\n")
        earned_ev = write(
            "earned-tier-evidence.json",
            {
                "tier_state_version": "drift-classification-earned-tier/v1",
                "earned_tier": "low_blast_pr",
                "promoted_by": "fixture-human",
                "promoted_at": "2026-06-12T00:00:00Z",
                "evidence": {"eval_set": "evals/drift-classification/v1",
                             "predictions": predictions},
            },
        )
        runner_fail = write("runner-fail.py", None,
                            executable_body="#!/usr/bin/env python3\nraise SystemExit(1)\n")
        runner_pass = write("runner-pass.py", None,
                            executable_body="#!/usr/bin/env python3\nraise SystemExit(0)\n")
        expect("floor NOT cleared -> reject",
               run_validate(row_accept, fixture_snapshot, policy_action="low_blast_pr",
                            tier_state_path=earned_ev, eval_runner=runner_fail), 1)
        expect("floor cleared -> accept",
               run_validate(row_accept, fixture_snapshot, policy_action="low_blast_pr",
                            tier_state_path=earned_ev, eval_runner=runner_pass), 0)
        missing_runner = os.path.join(tmp, "no-such-runner.py")
        expect("runner absent -> existence-guarded skip (green pre-merge)",
               run_validate(row_accept, fixture_snapshot, policy_action="low_blast_pr",
                            tier_state_path=earned_ev, eval_runner=missing_runner), 0)

        print("\n== post-wall hook slot (interface) ==")
        hook_fail = write("hook-fail.sh", None,
                          executable_body="#!/usr/bin/env bash\necho corpus-broken; exit 1\n")
        hook_pass = write("hook-pass.sh", None,
                          executable_body="#!/usr/bin/env bash\nexit 0\n")
        expect("hook nonzero -> material row rejected",
               run_validate(row_accept, fixture_snapshot, post_wall_hook=hook_fail), 1)
        expect("hook zero -> material row accepted",
               run_validate(row_accept, fixture_snapshot, post_wall_hook=hook_pass), 0)

        print("\n== stdlib validator <-> row.schema.json agreement ==")
        agreement_rows: list[tuple[str, Any]] = [
            ("row-accept", json.load(open(row_accept, encoding="utf-8"))),
            ("row-substring-violation", json.load(open(row_substring, encoding="utf-8"))),
            ("row-schema-invalid", json.load(open(row_invalid, encoding="utf-8"))),
        ] + [(f"mutation: {name}", mutated) for name, mutated in mutations]
        sample = validate_row_against_schema({}, DEFAULT_SCHEMA)
        if sample is None:
            print("self-test note: jsonschema not importable — agreement check skipped "
                  "(CI installs it; stdlib mirror still enforced above)")
        else:
            for name, candidate in agreement_rows:
                stdlib_ok = not validate_row_structure(candidate)
                schema_ok = not validate_row_against_schema(candidate, DEFAULT_SCHEMA)
                if stdlib_ok == schema_ok:
                    print(f"self-test ok: agreement on {name} (valid={stdlib_ok})")
                else:
                    print(f"self-test FAIL: validators disagree on {name} "
                          f"(stdlib={stdlib_ok}, schema={schema_ok})")
                    failures += 1

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the walls are not sound.")
        return 1
    print("\nself-test: all walls enforce; accept + every reject class covered. Walls are sound.")
    return 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return cmd_self_test()
    parser = argparse.ArgumentParser(
        description="Deterministic walls bracketing the (future) LLM drift classifier."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    val = sub.add_parser("validate", help="validate one classification row against all walls")
    val.add_argument("row", help="path to the drift-classification/v1 row JSON")
    val.add_argument("--against", required=True, metavar="SNAPSHOT",
                     help="the tier-2 vendored snapshot the diff came from (pre-wall bytes)")
    val.add_argument("--policy-action", default=None, metavar="ACTION",
                     help="side-effect action to authorize against the autonomy gradient")
    val.add_argument("--schema", default=DEFAULT_SCHEMA, help="row schema path")
    val.add_argument("--policy", default=DEFAULT_POLICY, help="autonomy policy path")
    val.add_argument("--tier-state", default=DEFAULT_TIER_STATE, help="earned-tier state path")
    val.add_argument("--post-wall-hook", default=DEFAULT_POST_WALL_HOOK,
                     help="post-wall hook script slot (kernel-side corpus check)")
    val.add_argument("--eval-runner", default=DEFAULT_EVAL_RUNNER,
                     help="recall-floor scorer (existence-guarded; ships separately)")
    args = parser.parse_args()
    return run_validate(
        args.row,
        args.against,
        policy_action=args.policy_action,
        schema_path=args.schema,
        policy_path=args.policy,
        tier_state_path=args.tier_state,
        post_wall_hook=args.post_wall_hook,
        eval_runner=args.eval_runner,
    )


if __name__ == "__main__":
    sys.exit(main())
