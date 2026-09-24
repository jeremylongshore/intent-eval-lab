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

WHICH snapshot, and why it matters
----------------------------------
`--check` used to read `_vendor/upstream/skill-frontmatter/agentskills-spec-v1.0.md`
— a snapshot hand-vendored on 2026-05-28 that the capture pipeline never writes to
and cannot advance. So both sides of the diff were frozen committed files and the
differ reported "NO semantic drift (0 findings)" by construction: it was
structurally incapable of firing no matter what upstream did. That is how 11 of 16
sources drifted for six weeks behind a green check.

It now reads the CAPTURED snapshot at `specs/_vendor/<surface>/snapshot<ext>` —
the tier-2 tree `fetch-capture.py` actually promotes into, and only ever on a
FETCH_OK classification, so the firewall is intact. The differ itself stays
network-free: it takes paths, not URLs.

That one path change gives the same command two correct meanings:
  - on a scheduled run, `--check` executes AFTER the capture step, so it diffs
    freshly-fetched content against the committed projection — real drift detection;
  - on a PR run, no capture happens, so it diffs the committed captured snapshot
    against the committed projection — a consistency check on the pair.

The legacy `_vendor/upstream/skill-frontmatter/` tree is deliberately KEPT, with a
narrowed role: it holds the curated normative projection (the baseline, hand-owned
by a human reconciling upstream into the kernel) and the frozen 2026-05-28 snapshot
that the synthetic drift-classification eval set perturbs as a stable fixture
(`evals/drift-classification/v1/cases/*/meta.json`). It is no longer a drift input.

Stdlib only. Exit 0 = no semantic drift; exit 1 = drift detected (the CI step
opens a reconciliation issue); exit 2 = usage / parse error / missing snapshot.

Usage:
  spec-projection-diff.py --check [--vendor-dir DIR] [--snapshot PATH]
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

# Home of the curated normative projection (the baseline a human owns). NOT a
# drift input — see the module docstring.
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "_vendor", "upstream", "skill-frontmatter")

# Home of the CAPTURED snapshots that fetch-capture.py promotes on FETCH_OK.
# This is the left-hand side of the diff — the side that must be able to move.
CAPTURE_VENDOR_ROOT = os.path.join(REPO_ROOT, "specs", "_vendor")
SURFACE_REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")

# The contract this differ projects. The other five authoring contracts have their
# own extractors (scripts/extract-*-projection.py) with a different projection
# shape; wiring them into --check is tracked separately and is NOT done here.
CONTRACT = "skill-frontmatter"

# The specific surface this differ's committed projection was extracted from. Note
# the contract -> surface relation is 1:MANY, not 1:1 — `platform-skills-overview`
# (the Anthropic SKILL.md spec page) and `skills-releases` also declare contract
# `skill-frontmatter`, and NEITHER is covered here: the row regex below is written
# against the agentskills.io frontmatter table specifically. Extending coverage to
# them needs their own extractors and their own committed projections, which is
# separate work. Naming it here so "no extractor" is never mistaken for
# "not covered by design".
DEFAULT_SURFACE = "agentskills-spec"

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


def resolve_captured_snapshot(surface_name: str = DEFAULT_SURFACE) -> str:
    """Path of the captured snapshot for `surface_name`, resolved via the surface registry.

    Fails loudly (exit 2) rather than falling back to a frozen snapshot: a silent
    fallback is exactly the failure this function exists to remove.
    """
    try:
        registry = _load(SURFACE_REGISTRY)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read surface registry {SURFACE_REGISTRY}: {exc}", file=sys.stderr)
        sys.exit(2)

    matches = [s for s in registry.get("surfaces", []) if s.get("name") == surface_name]
    if len(matches) != 1:
        print(
            f"ERROR: expected exactly one registry surface named '{surface_name}', found {len(matches)}. "
            "Pass --snapshot explicitly, or fix the registry.",
            file=sys.stderr,
        )
        sys.exit(2)

    surface = matches[0]
    if not surface.get("monitored"):
        print(
            f"ERROR: surface '{surface_name}' is not monitored, so its captured snapshot never advances.",
            file=sys.stderr,
        )
        sys.exit(2)
    if surface.get("contract") != CONTRACT:
        print(
            f"ERROR: surface '{surface_name}' declares contract '{surface.get('contract')}', "
            f"but this differ projects '{CONTRACT}'.",
            file=sys.stderr,
        )
        sys.exit(2)
    ext = surface.get("capture", {}).get("ext", ".md")
    path = os.path.join(CAPTURE_VENDOR_ROOT, surface["name"], f"snapshot{ext}")
    if not os.path.isfile(path):
        print(
            f"ERROR: captured snapshot missing: {path}\n"
            "The tier-2 capture stage (scripts/fetch-capture.py) has not promoted this surface yet. "
            "Refusing to fall back to the frozen legacy snapshot — that fallback is what made this "
            "check structurally unable to detect drift.",
            file=sys.stderr,
        )
        sys.exit(2)
    return path


def cmd_check(vendor_dir: str, snapshot: str | None = None, surface: str = DEFAULT_SURFACE) -> int:
    snapshot = snapshot or resolve_captured_snapshot(surface)
    committed = os.path.join(vendor_dir, "projection.v1.json")
    fresh = extract_projection(snapshot)
    base = _load(committed)
    context = f"captured snapshot ({os.path.relpath(snapshot, REPO_ROOT)}) vs committed projection"
    return _report(diff_projections(base, fresh), context)


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
    group.add_argument("--check", action="store_true", help="diff the captured snapshot vs the committed projection")
    group.add_argument("--extract", metavar="SNAPSHOT.md", help="emit a projection JSON from a snapshot")
    group.add_argument("--diff", nargs=2, metavar=("BASE.json", "FRESH.json"), help="diff two projection JSONs")
    group.add_argument("--self-test", action="store_true", help="prove the differ detects every drift class")
    parser.add_argument(
        "--vendor-dir",
        default=DEFAULT_VENDOR_DIR,
        help="dir holding the committed normative projection (projection.v1.json)",
    )
    parser.add_argument(
        "--snapshot",
        default=None,
        help="snapshot to extract from; defaults to the captured specs/_vendor/<surface>/snapshot<ext>",
    )
    parser.add_argument(
        "--surface",
        default=DEFAULT_SURFACE,
        help=f"registry surface whose captured snapshot to diff (default: {DEFAULT_SURFACE})",
    )
    args = parser.parse_args()

    if args.check:
        return cmd_check(args.vendor_dir, args.snapshot, args.surface)
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
