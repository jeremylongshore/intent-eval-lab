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

    # Every monitored surface must carry a valid capture config (fetch-capture.py).
    for name in sorted(reg_surfaces):
        if reg_surfaces[name].get("monitored"):
            _check_capture(name, reg_surfaces[name], problems)

    if problems:
        print(f"surface-registry consistency: {len(problems)} PROBLEM(S):")
        for p in problems:
            print(f"  - {p}")
        print("\nFix: edit BOTH spec-drift-check.sh SOURCES and the registry in the same change.")
        return 1

    print(
        f"surface-registry consistency: OK — {len(reg_surfaces)} surfaces, registry == watcher "
        "SOURCES, all extractors defined, all capture configs valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
