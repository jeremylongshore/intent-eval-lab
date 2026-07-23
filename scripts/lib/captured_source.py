#!/usr/bin/env python3
"""Resolve a vendored reference doc to the CAPTURED snapshot of the same surface.

WHY THIS EXISTS
---------------
Every deep-capture extractor (scripts/extract-*-projection.py) ships a `--check`
that re-extracts its normative projection from `specs/_vendor/upstream/<contract>/`
and fails if the committed `projection.json` no longer matches. That check is
honest SELF-CONSISTENCY: the projection is derived, never hand-edited, and
`--check` proves it wasn't.

What it is NOT is a freshness check. `specs/_vendor/upstream/` is a hand-vendored
tree that `fetch-capture.py` cannot write (`upstream` is not a surface id); every
`vendor-meta.json` there is stamped 2026-06-12. So `--check` compares a frozen
projection against the frozen doc it was derived from — green by construction, no
matter what upstream does. The five CI steps that ran it were even titled
"…projection freshness", which is the overclaim this module exists to retire.

The design was right all along; the missing half was the wiring. The extractors'
own comments say so: "CI never refetches: the capture is a one-time build-time
fetch; ongoing freshness is the watcher's job." The watcher never got them.

WHAT IT DOES
------------
Each `vendor-meta.json` already records, per file, the registry surface it was
fetched from:

    { "file": "claude-code-sub-agents.md", "role": "reference-doc",
      "surface": "sub-agents", ... }

So no new mapping has to be invented. Given a vendor-meta, this module finds the
one file the extractor actually parses (`role == "reference-doc"`) and resolves
its surface to `specs/_vendor/<surface>/snapshot<ext>` — the tier-2 tree
`fetch-capture.py` promotes into, and only ever on a FETCH_OK classification, so
the fetch firewall is intact and this module performs no network I/O.

Sample corpora and supporting docs are deliberately NOT repointed. Their value is
being commit-pinned ground truth that corroborates the doc, and the provenance
rule (`documented` vs `observed-in-samples`, never promoted) depends on them
staying put.

FAIL LOUD, NEVER FALL BACK
--------------------------
`InoperableError` is raised for anything that would otherwise degrade into a
silent frozen-vs-frozen comparison: unknown surface, unmonitored surface, wrong
contract, missing snapshot. Callers map it to exit code 2 — "the gate did not
run" — which must be treated as red, distinctly from exit 1 "the shape drifted".
Collapsing those two is how a broken detector reads as a clean bill of health.

Stdlib only. Offline. No writes.
"""

from __future__ import annotations

import json
import os
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Where fetch-capture.py promotes a FETCH_OK body: specs/_vendor/<surface>/snapshot<ext>.
CAPTURE_VENDOR_ROOT = os.path.join(REPO_ROOT, "specs", "_vendor")
SURFACE_REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")

# Longest rendered value kept verbatim in a CHANGED_VALUE finding. Enums like the
# 30-event hook list would otherwise bury the finding they are attached to.
_VALUE_RENDER_LIMIT = 400


class InoperableError(RuntimeError):
    """The freshness comparison could not be set up. Maps to exit 2, never to 'clean'."""


# ── Registry ─────────────────────────────────────────────────────────────────


def load_registry(path: str = SURFACE_REGISTRY) -> dict[str, Any]:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise InoperableError(f"cannot read surface registry {path}: {exc}") from exc


def surface_row(surface_name: str, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """The one registry row named `surface_name`. Raises if it is not exactly one."""
    reg = registry if registry is not None else load_registry()
    matches = [s for s in reg.get("surfaces", []) if s.get("name") == surface_name]
    if len(matches) != 1:
        raise InoperableError(
            f"expected exactly one registry surface named '{surface_name}', found {len(matches)}. "
            "Pass --surface explicitly, or fix specs/upstream-surface-registry.v1.json."
        )
    return matches[0]


def resolve_captured_snapshot(
    surface_name: str,
    expected_contract: str | None = None,
    registry: dict[str, Any] | None = None,
    capture_root: str | None = None,
) -> str:
    """Path of the captured snapshot for `surface_name`.

    Every failure mode raises rather than falling back to the frozen tree — the
    fallback IS the bug this resolver removes.

    `capture_root` defaults to the module global at CALL time, not at def time, so
    a test can redirect the whole capture tree by setting CAPTURE_VENDOR_ROOT. A
    def-time default silently ignores that, which made the first version of the
    "missing capture must be loud" test pass green against the real tree.
    """
    capture_root = capture_root or CAPTURE_VENDOR_ROOT
    surface = surface_row(surface_name, registry)

    if not surface.get("monitored"):
        raise InoperableError(
            f"surface '{surface_name}' is not monitored, so its captured snapshot never advances; "
            "a comparison against it would be frozen-vs-frozen again."
        )
    if expected_contract is not None and surface.get("contract") != expected_contract:
        raise InoperableError(
            f"surface '{surface_name}' declares contract '{surface.get('contract')}', "
            f"but this extractor projects '{expected_contract}'. Projecting the wrong surface "
            "with this extractor would produce confident nonsense."
        )

    ext = surface.get("capture", {}).get("ext", ".md")
    path = os.path.join(capture_root, surface_name, f"snapshot{ext}")
    if not os.path.isfile(path):
        raise InoperableError(
            f"captured snapshot missing: {path}. The tier-2 capture stage (scripts/fetch-capture.py) "
            "has not promoted this surface yet. Refusing to fall back to the frozen hand-vendored "
            "doc — that fallback is what made these checks structurally unable to detect drift."
        )
    return path


# ── vendor-meta ──────────────────────────────────────────────────────────────


def reference_doc_entry(meta: dict[str, Any], role: str = "reference-doc") -> dict[str, Any]:
    """The single vendor-meta file entry the extractor parses.

    Exactly one is required: the extractors already assert `len(docs) == 1`, and a
    second one would make "which file do we repoint?" ambiguous.
    """
    docs = [f for f in meta.get("files", []) if f.get("role") == role]
    if len(docs) != 1:
        raise InoperableError(f"vendor-meta.json needs exactly one '{role}' entry, found {len(docs)}")
    return docs[0]


def reference_doc_surface(meta: dict[str, Any], role: str = "reference-doc") -> tuple[str, str]:
    """(vendored filename, registry surface name) of the parsed reference doc."""
    entry = reference_doc_entry(meta, role)
    surface = entry.get("surface")
    if not surface:
        raise InoperableError(
            f"vendor-meta.json entry '{entry.get('file')}' records surface {surface!r}; it cannot be "
            "repointed at a captured snapshot until its source URL is registered as a surface in "
            "specs/upstream-surface-registry.v1.json."
        )
    return entry["file"], surface


# ── Field-level projection diff ──────────────────────────────────────────────


def _render(value: Any) -> str:
    text = json.dumps(value, sort_keys=True)
    if len(text) > _VALUE_RENDER_LIMIT:
        return text[:_VALUE_RENDER_LIMIT] + f"… (truncated, {len(text)} chars)"
    return text


def _walk(prefix: str, base: Any, fresh: Any, out: list[str]) -> None:
    if isinstance(base, dict) and isinstance(fresh, dict):
        for key in sorted(set(base) | set(fresh)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in fresh:
                out.append(f"REMOVED_KEY: {path}")
            elif key not in base:
                out.append(f"ADDED_KEY: {path}")
            else:
                _walk(path, base[key], fresh[key], out)
        return
    if base != fresh:
        out.append(f"CHANGED_VALUE: {prefix or '<root>'}: {_render(base)} -> {_render(fresh)}")


def diff_projections(base: dict[str, Any], fresh: dict[str, Any]) -> list[str]:
    """Recursive key-path diff of two projection documents.

    Deliberately generic: the five contracts have five different projection shapes,
    and a per-contract differ would be five places to forget to extend. Lists are
    compared whole (order matters — the extractors already sort what should be
    sorted, so a reordering IS a finding worth a human's eye).
    """
    findings: list[str] = []
    _walk("", base, fresh, findings)
    return findings


def report(findings: list[str], context: str, label: str) -> int:
    """Print a reconciliation report. 0 = clean, 1 = semantic drift."""
    if not findings:
        print(f"{label}: {context} — NO semantic drift (0 findings).")
        return 0
    print(f"{label}: {context} — SEMANTIC DRIFT ({len(findings)} findings):")
    for finding in findings:
        print(f"  - {finding}")
    print(
        "\nReconcile (never bulk-refresh): a human reads the captured page, decides whether each "
        "finding is a real upstream spec change or a stale extractor anchor, and only then promotes "
        "it into the kernel (@intentsolutions/core authoring/v1) and re-vendors the reference doc. "
        "This check never authors a kernel edit and never closes its own signal."
    )
    return 1
