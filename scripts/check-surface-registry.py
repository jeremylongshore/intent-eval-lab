#!/usr/bin/env python3
"""Consistency gate: the upstream-surface registry must equal the watcher's SOURCES.

The registry (specs/upstream-surface-registry.v1.json + 000-docs/050-AT-SPEC-...md)
documents the surfaces the spec-drift watcher monitors; the executable list is the
SOURCES array in spec-drift-check.sh. They are DRY-duplicated today, so they can
silently diverge — exactly the "stale registry" failure the SSoT plan guards against.
This gate asserts they are identical (by surface name) and that every registered
surface names an extractor function that actually exists in the script.

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

    if problems:
        print(f"surface-registry consistency: {len(problems)} PROBLEM(S):")
        for p in problems:
            print(f"  - {p}")
        print("\nFix: edit BOTH spec-drift-check.sh SOURCES and the registry in the same change.")
        return 1

    print(f"surface-registry consistency: OK — {len(reg_surfaces)} surfaces, registry == watcher SOURCES, all extractors defined.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
