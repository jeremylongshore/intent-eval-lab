#!/usr/bin/env python3
"""Fitness Function #2 — field-level extract-then-diff for skill-frontmatter.

The byte-hash watcher (spec-drift-check.sh) answers "did the page change?". This
answers the harder, load-bearing question: "did the *normative shape* change —
a field added/removed, a required flag flipped, an EXPERIMENTAL flag flipped, a
deprecation introduced?". Per the 7-thinker panel (Kleppmann/Gregg): the diff
anchor is a per-surface NORMATIVE PROJECTION, not a byte-sha of the page. We
extract the projection from the vendored snapshot and diff it field-by-field
against the committed `projection.v1.json`. The byte-hash is demoted to a cheap
"should we re-extract?" tripwire.

Determinism + safety (Armstrong): no network here. It operates on the vendored
firewall snapshot + the committed projection. Only a FETCH_OK snapshot ever
reaches this differ; live fetching + classification is a separate, gated stage.

Stdlib only. Exit 0 = no semantic drift; exit 1 = drift detected (the CI step
opens a reconciliation issue); exit 2 = usage / parse error.

Usage:
  spec-projection-diff.py --check [--vendor-dir DIR]      # extract from snapshot, diff vs committed projection
  spec-projection-diff.py --extract SNAPSHOT.md           # emit a projection JSON to stdout
  spec-projection-diff.py --diff BASE.json FRESH.json     # diff two projection JSONs
  spec-projection-diff.py --self-test                     # prove the differ detects every drift class
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "_vendor", "upstream", "skill-frontmatter")

# A frontmatter table row: | `field` | Yes/No | constraint... |
_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(Yes|No)\s*\|\s*(.*?)\s*\|\s*$")


def extract_projection(markdown_path: str) -> dict[str, Any]:
    """Parse the agentskills.io snapshot's frontmatter field table into a projection."""
    with open(markdown_path, encoding="utf-8") as fh:
        lines = fh.readlines()

    fields: dict[str, dict[str, bool]] = {}
    for line in lines:
        m = _ROW.match(line.rstrip("\n"))
        if not m:
            continue
        field, required, constraint = m.group(1).strip(), m.group(2), m.group(3)
        fields[field] = {
            "required": required == "Yes",
            "experimental": "experimental" in constraint.lower(),
        }
    if not fields:
        print(f"ERROR: no frontmatter field table found in {markdown_path}", file=sys.stderr)
        sys.exit(2)
    return {
        "projection_version": "spec-projection/v1",
        "contract": "skill-frontmatter",
        "surface": "agentskills.io/specification",
        "captured_from": os.path.basename(markdown_path),
        "fields": fields,
        "deprecations": [],
    }


def diff_projections(base: dict[str, Any], fresh: dict[str, Any]) -> list[str]:
    """Field-by-field semantic diff. Returns a list of human-readable drift findings."""
    findings: list[str] = []
    bf, ff = base.get("fields", {}), fresh.get("fields", {})

    for field in ff:
        if field not in bf:
            findings.append(f"ADDED_FIELD: `{field}` appeared upstream (not in the vendored base)")
    for field in bf:
        if field not in ff:
            findings.append(f"REMOVED_FIELD: `{field}` disappeared upstream (was in the vendored base)")
    for field in sorted(set(bf) & set(ff)):
        if bool(bf[field].get("required")) != bool(ff[field].get("required")):
            findings.append(
                f"REQUIRED_CHANGED: `{field}` required {bf[field].get('required')} -> {ff[field].get('required')}"
            )
        if bool(bf[field].get("experimental")) != bool(ff[field].get("experimental")):
            findings.append(
                f"EXPERIMENTAL_CHANGED: `{field}` experimental "
                f"{bool(bf[field].get('experimental'))} -> {bool(ff[field].get('experimental'))}"
            )

    base_dep = json.dumps(base.get("deprecations", []), sort_keys=True)
    fresh_dep = json.dumps(fresh.get("deprecations", []), sort_keys=True)
    if base_dep != fresh_dep:
        findings.append(f"DEPRECATIONS_CHANGED: {base_dep} -> {fresh_dep}")

    return findings


def _load(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _report(findings: list[str], context: str) -> int:
    if not findings:
        print(f"spec-projection-diff: {context} — NO semantic drift ({0} findings).")
        return 0
    print(f"spec-projection-diff: {context} — SEMANTIC DRIFT ({len(findings)} findings):")
    for f in findings:
        print(f"  - {f}")
    print(
        "\nReconcile: a human promotes the change into the kernel "
        "(@intentsolutions/core authoring/v1) and refreshes the vendored projection. "
        "The differ never authors a kernel edit and never closes the drift signal."
    )
    return 1


def cmd_check(vendor_dir: str) -> int:
    snapshot = os.path.join(vendor_dir, "agentskills-spec-v1.0.md")
    committed = os.path.join(vendor_dir, "projection.v1.json")
    fresh = extract_projection(snapshot)
    base = _load(committed)
    return _report(diff_projections(base, fresh), "vendored snapshot vs committed projection")


def cmd_self_test() -> int:
    """Prove the differ is not vacuous: every drift class must be detected (Karpathy)."""
    base = {
        "fields": {
            "name": {"required": True, "experimental": False},
            "allowed-tools": {"required": False, "experimental": True},
        },
        "deprecations": [],
    }
    cases: list[tuple[str, dict[str, Any]]] = [
        ("ADDED_FIELD", {"fields": {**base["fields"], "new_field": {"required": False}}, "deprecations": []}),
        ("REMOVED_FIELD", {"fields": {"name": base["fields"]["name"]}, "deprecations": []}),
        (
            "REQUIRED_CHANGED",
            {"fields": {**base["fields"], "allowed-tools": {"required": True, "experimental": True}}, "deprecations": []},
        ),
        (
            "EXPERIMENTAL_CHANGED",
            {"fields": {**base["fields"], "allowed-tools": {"required": False, "experimental": False}}, "deprecations": []},
        ),
        ("DEPRECATIONS_CHANGED", {"fields": dict(base["fields"]), "deprecations": [{"when_to_use": "description"}]}),
    ]
    failures = 0
    # A no-op diff must be empty (no false positive).
    if diff_projections(base, json.loads(json.dumps(base))):
        print("self-test FAIL: identical projections reported drift (false positive)")
        failures += 1
    for expected, mutated in cases:
        findings = diff_projections(base, mutated)
        if not any(f.startswith(expected) for f in findings):
            print(f"self-test FAIL: drift class {expected} not detected; got {findings}")
            failures += 1
        else:
            print(f"self-test ok: {expected} detected")
    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the fitness function is not sound.")
        return 1
    print("\nself-test: all drift classes detected; no false positive. Fitness function is sound.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Field-level extract-then-diff for skill-frontmatter.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="diff the vendored snapshot vs the committed projection")
    group.add_argument("--extract", metavar="SNAPSHOT.md", help="emit a projection JSON from a snapshot")
    group.add_argument("--diff", nargs=2, metavar=("BASE.json", "FRESH.json"), help="diff two projection JSONs")
    group.add_argument("--self-test", action="store_true", help="prove the differ detects every drift class")
    parser.add_argument("--vendor-dir", default=DEFAULT_VENDOR_DIR, help="vendored upstream dir")
    args = parser.parse_args()

    if args.check:
        return cmd_check(args.vendor_dir)
    if args.extract:
        print(json.dumps(extract_projection(args.extract), indent=2))
        return 0
    if args.diff:
        return _report(diff_projections(_load(args.diff[0]), _load(args.diff[1])), "base vs fresh")
    if args.self_test:
        return cmd_self_test()
    return 2


if __name__ == "__main__":
    sys.exit(main())
