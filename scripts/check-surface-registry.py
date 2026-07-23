#!/usr/bin/env python3
"""Consistency gate: the upstream-surface registry must equal the watcher's SOURCES.

The registry (specs/upstream-surface-registry.v1.json + 000-docs/050-AT-SPEC-...md)
documents the surfaces the spec-drift watcher monitors; the executable list is the
SOURCES array in spec-drift-check.sh. They are DRY-duplicated today, so they can
silently diverge — exactly the "stale registry" failure the SSoT plan guards against.
This gate asserts they are identical (by surface name) and that every registered
surface names an extractor function that actually exists in the script.

It also validates each surface's `capture` config — the per-surface fetch kind,
expected extractor pattern (shape hint) and min-bytes floor that drive the
raw-fetch capture stage (scripts/fetch-capture.py; 000-docs/052-AT-SPEC-...md).

And each surface's `semantic_coverage` block — whether the surface has a
field-level projection checker (and which, and whether it is enforced) or is
byte-hash-only with a named reason. That block is the coverage map the freshness
driver (scripts/projection-freshness.py) executes, so it must be present and
well-formed on EVERY surface: an unstated coverage level is how "no extractor"
gets quietly mistaken for "not covered by design".

Stdlib only, offline. Exit 0 = consistent; exit 1 = drift; exit 2 = usage/parse.

Usage: check-surface-registry.py
"""

from __future__ import annotations

import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")
SCRIPT = os.path.join(REPO_ROOT, "scripts", "spec-drift-check.sh")

_SOURCE_ROW = re.compile(r'^\s*"([a-z0-9-]+)\|[^|]*\|([a-z_]+)"\s*$')

_CAPTURE_KINDS = {"http", "command"}

_COVERAGE_STATUSES = {"field-level", "byte-hash-only"}
_ENFORCEMENTS = {"failing", "report-only"}

# Which flag makes each checker compare against the CAPTURED tree, i.e. which flag
# actually performs a FRESHNESS check rather than a self-consistency one.
#
# Validating only that `checker[0]` is an existing file is not enough, and the gap
# is not theoretical: swapping `--check-fresh` for `--check` on any extractor
# re-arms the exact frozen-vs-frozen bug this machinery exists to end, and the
# driver then prints an authoritative all-green board — including for surfaces
# with real outstanding findings. `--surface` is a top-level arg, so the wrong
# mode accepts it and silently ignores it; nothing else in the chain objects.
#
# The registry is precisely the file humans are told to edit ("flipping a surface
# to `failing` is a one-line registry edit"), so the next person who sees red and
# "fixes" the flag would get a green board. Hence: pin the SEMANTICS of the argv,
# not just its head. A checker absent from this table is an error — adding one is
# a deliberate, reviewed act.
_FRESH_MODE_FLAG = {
    # spec-projection-diff's --check reads specs/_vendor/<surface>/snapshot<ext>
    # (repointed in #234); it has no separate --check-fresh.
    "scripts/spec-projection-diff.py": "--check",
    "scripts/extract-agent-definition-projection.py": "--check-fresh",
    "scripts/extract-hook-config-projection.py": "--check-fresh",
    "scripts/extract-marketplace-catalog-projection.py": "--check-fresh",
    "scripts/extract-plugin-manifest-projection.py": "--check-fresh",
}

# Mode flags a checker must never carry instead of (or in addition to) its fresh
# mode. `--write` would have the gate MUTATE the baseline it is meant to guard.
_MODE_FLAGS = {"--check", "--check-fresh", "--extract", "--write", "--self-test", "--diff", "--list", "--strict"}


def _check_semantic_coverage(name: str, surface: dict, problems: list[str]) -> None:
    """Validate one surface's semantic_coverage block (projection-freshness.py contract)."""
    cov = surface.get("semantic_coverage")
    if not isinstance(cov, dict):
        problems.append(
            f"{name}: missing semantic_coverage block. Every surface must state whether it has a "
            "field-level projection checker or is byte-hash-only, and why."
        )
        return

    status = cov.get("status")
    if status not in _COVERAGE_STATUSES:
        problems.append(f"{name}: semantic_coverage.status '{status}' not one of {sorted(_COVERAGE_STATUSES)}")
        return

    if status == "byte-hash-only":
        reason = cov.get("reason")
        if not isinstance(reason, str) or len(reason) < 20:
            problems.append(
                f"{name}: byte-hash-only coverage needs a substantive `reason` — an unexplained gap "
                "reads as a design choice."
            )
        if "checker" in cov:
            problems.append(f"{name}: byte-hash-only coverage must not declare a checker")
        return

    checker = cov.get("checker")
    if not isinstance(checker, list) or not checker or not all(isinstance(a, str) for a in checker):
        problems.append(f"{name}: field-level coverage needs `checker` as a non-empty list of argv strings")
    elif not os.path.isfile(os.path.join(REPO_ROOT, checker[0])):
        problems.append(f"{name}: semantic_coverage.checker script not found: {checker[0]}")
    elif checker[0] not in _FRESH_MODE_FLAG:
        problems.append(
            f"{name}: '{checker[0]}' is not a registered freshness checker. Add it to _FRESH_MODE_FLAG in "
            "this script, naming the flag that makes it read the CAPTURED tree — a checker whose mode is "
            "unpinned can silently compare frozen against frozen."
        )
    else:
        required = _FRESH_MODE_FLAG[checker[0]]
        supplied = [a for a in checker[1:] if a in _MODE_FLAGS]
        if supplied != [required]:
            problems.append(
                f"{name}: checker must run '{checker[0]}' in its freshness mode '{required}', got mode flag(s) "
                f"{supplied or 'none'}. A checker in the wrong mode compares frozen against frozen and reports "
                "an authoritative green — the exact failure this gate exists to detect."
            )

    enforcement = cov.get("enforcement")
    # str() first: a list/dict here is unhashable and `in` would raise TypeError,
    # killing the gate with a traceback instead of naming the problem.
    if not isinstance(enforcement, str) or enforcement not in _ENFORCEMENTS:
        problems.append(
            f"{name}: semantic_coverage.enforcement {enforcement!r} not one of {sorted(_ENFORCEMENTS)}"
        )
    if enforcement == "report-only" and not isinstance(cov.get("note"), str):
        problems.append(f"{name}: report-only coverage needs a `note` saying what is pending and when it flips")


def _check_capture(name: str, surface: dict, problems: list[str]) -> None:
    """Validate one surface's capture config (fetch-capture.py contract)."""
    cap = surface.get("capture")
    if not isinstance(cap, dict):
        problems.append(f"{name}: missing capture config (kind/urls-or-argv/expect_regex/min_bytes/ext)")
        return
    kind = cap.get("kind")
    if kind not in _CAPTURE_KINDS:
        problems.append(f"{name}: capture.kind '{kind}' not one of {sorted(_CAPTURE_KINDS)}")
    if kind == "http":
        urls = cap.get("urls")
        if (
            not isinstance(urls, list)
            or not urls
            or not all(isinstance(u, str) and u.startswith("https://") for u in urls)
        ):
            problems.append(f"{name}: capture.urls must be a non-empty list of https:// URLs")
    if kind == "command":
        argv = cap.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
            problems.append(f"{name}: capture.argv must be a non-empty list of strings")
    min_bytes = cap.get("min_bytes")
    if not isinstance(min_bytes, int) or isinstance(min_bytes, bool) or min_bytes < 1:
        problems.append(f"{name}: capture.min_bytes must be a positive integer (got {min_bytes!r})")
    expect_regex = cap.get("expect_regex")
    if not isinstance(expect_regex, str) or not expect_regex:
        problems.append(f"{name}: capture.expect_regex must be a non-empty string")
    else:
        try:
            re.compile(expect_regex)
        except re.error as exc:
            problems.append(f"{name}: capture.expect_regex does not compile: {exc}")
    ext = cap.get("ext")
    if not isinstance(ext, str) or not ext.startswith("."):
        problems.append(f"{name}: capture.ext must be a string starting with '.' (got {ext!r})")


def main() -> int:
    if not os.path.exists(REGISTRY):
        print(f"ERROR: registry not found: {REGISTRY}", file=sys.stderr)
        return 2
    if not os.path.exists(SCRIPT):
        print(f"ERROR: watcher script not found: {SCRIPT}", file=sys.stderr)
        return 2

    reg = json.load(open(REGISTRY, encoding="utf-8"))
    reg_surfaces = {s["name"]: s for s in reg.get("surfaces", [])}

    src_text = open(SCRIPT, encoding="utf-8").read()
    src_surfaces: dict[str, str] = {}
    for line in src_text.splitlines():
        m = _SOURCE_ROW.match(line)
        if m:
            src_surfaces[m.group(1)] = m.group(2)
    defined_fns = set(re.findall(r"^([a-z0-9_]+)\s*\(\)\s*\{", src_text, re.MULTILINE))

    problems: list[str] = []

    only_script = set(src_surfaces) - set(reg_surfaces)
    only_registry = set(reg_surfaces) - set(src_surfaces)
    for s in sorted(only_script):
        problems.append(f"in spec-drift-check.sh SOURCES but NOT registry: {s}")
    for s in sorted(only_registry):
        problems.append(f"in registry but NOT spec-drift-check.sh SOURCES: {s}")

    # Every registered surface's declared extractor must match the script + exist.
    for name in sorted(set(reg_surfaces) & set(src_surfaces)):
        reg_fn = reg_surfaces[name].get("extractor")
        src_fn = src_surfaces[name]
        if reg_fn != src_fn:
            problems.append(f"{name}: registry extractor '{reg_fn}' != script '{src_fn}'")
        if src_fn not in defined_fns:
            problems.append(f"{name}: extractor function '{src_fn}' not defined in the script")

    # Every monitored surface must carry a valid capture config (fetch-capture.py)
    # and a stated semantic-coverage level (projection-freshness.py).
    for name in sorted(reg_surfaces):
        if reg_surfaces[name].get("monitored"):
            _check_capture(name, reg_surfaces[name], problems)
            _check_semantic_coverage(name, reg_surfaces[name], problems)

    if problems:
        print(f"surface-registry consistency: {len(problems)} PROBLEM(S):")
        for p in problems:
            print(f"  - {p}")
        print("\nFix: edit BOTH spec-drift-check.sh SOURCES and the registry in the same change.")
        return 1

    field_level = sum(
        1 for s in reg_surfaces.values() if (s.get("semantic_coverage") or {}).get("status") == "field-level"
    )
    # A floor, so shrinking semantic coverage is a visible edit rather than a
    # quietly smaller green board. Without it, "the map got smaller" and "the map
    # is clean" look identical downstream.
    floor = (reg.get("semantic_coverage_floor") or {}).get("field_level")
    if not isinstance(floor, int) or isinstance(floor, bool) or floor < 1:
        problems.append("registry: semantic_coverage_floor.field_level must be a positive integer")
    elif field_level < floor:
        problems.append(
            f"registry: {field_level} field-level surfaces is below the declared floor of {floor}. "
            "Semantic coverage SHRANK. If that is intended, lower the floor in the same change so the "
            "reduction is reviewed."
        )
    if problems:
        print(f"surface-registry consistency: {len(problems)} PROBLEM(S):")
        for problem in problems:
            print(f"  - {problem}")
        print("\nFix: edit BOTH spec-drift-check.sh SOURCES and the registry in the same change.")
        return 1
    print(
        f"surface-registry consistency: OK — {len(reg_surfaces)} surfaces, registry == watcher "
        f"SOURCES, all extractors defined, all capture configs valid, all semantic-coverage levels "
        f"stated ({field_level} field-level, {len(reg_surfaces) - field_level} byte-hash-only)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
