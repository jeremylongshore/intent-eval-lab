#!/usr/bin/env python3
"""Three-way completeness ledger: upstream documented / kernel modelled / validator knows.

For each authoring contract this prints THREE independently-sourced field
inventories side by side and never sums them:

  upstream   what the captured upstream page documents
  kernel     what @intentsolutions/core schemas/authoring/v1 models
  validator  what claude-code-plugins' validate-skills-schema.py recognises

WHY THREE AND NOT TWO

A two-way ledger (upstream vs kernel) can only show the SSoT lagging upstream.
It structurally cannot show the case that actually blocks the authority flip:
the CONSUMER being ahead of the SSoT. If the marketplace validator already
enforces fields the kernel does not model, then repointing that validator at
the kernel — the whole point of the Spec Authority Kernel — would REGRESS the
gate to a thinner contract than it enforces today. Completeness is therefore
the precondition for the flip, not a follow-up to it, and only the three-way
comparison makes that visible.

The three columns are also why this never reports a single "completeness
percentage". Summing across independent inventories is how "58 fields missing"
gets produced from six unrelated schemas — a number with no referent. Every
figure here is per-contract and per-source, and the gaps are named.

READING THE GAPS

  upstream-only    documented upstream, modelled nowhere — extraction debt
  kernel-missing   the validator knows it but the kernel does not — FLIP BLOCKER
  kernel-only      modelled but undocumented upstream — IS overlay, or drift
  validator-gap    kernel models it, validator ignores it — enforcement debt

Stdlib only, offline. Exit 0 always unless inputs are unreadable (2): this is
an instrument, not a gate. Ratcheting it before extraction catches up would
just wire today's incompleteness into CI as a permanent red.

Usage:
  completeness-ledger.py                  # full ledger
  completeness-ledger.py --contract NAME
  completeness-ledger.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATFORM = os.path.dirname(REPO_ROOT)
UPSTREAM = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream")
KERNEL = os.path.join(PLATFORM, "intent-eval-core", "schemas", "authoring", "v1")
VALIDATOR = os.path.join(PLATFORM, os.pardir, "claude-code-plugins", "scripts", "validate-skills-schema.py")

# Where each contract's upstream-documented field map lives inside its
# projection.json. Explicit per contract because the projections are shaped by
# what each page actually documents, not by a common template — hook-config
# carries handler fields, marketplace-catalog carries plugin-entry fields.
_PROJECTION_FIELDS = {
    "agent-definition": ("frontmatter", "fields"),
    "plugin-manifest": ("manifest", "fields"),
    "hook-config": ("handler_fields",),
    "marketplace-catalog": ("plugin_entry", "fields"),
}

# skill-frontmatter has no extractor of its own (FF#2 diffs the agentskills.io
# projection against the kernel). Its upstream inventory is read directly from
# the captured Claude Code skills page, whose "Frontmatter reference" table is
# the authoritative field list for SKILL.md.
_SKILL_PAGE = os.path.join(REPO_ROOT, "specs", "_vendor", "claude-slash-commands", "snapshot.md")
_SKILL_HEADING = re.compile(r"^#{1,4} +Frontmatter reference\s*$")

# The validator's per-contract field inventories, by module-level constant.
_VALIDATOR_SETS = {
    "skill-frontmatter": "SKILL_FIELDS",
    "agent-definition": "AGENT_FIELDS",
    "plugin-manifest": "PLUGIN_JSON_FIELDS",
}

_HEADING = re.compile(r"^#{1,4} ")
_TABLE_FIELD = re.compile(r"^`([A-Za-z$][A-Za-z0-9_.-]*)`")


def _dig(obj: dict, path: tuple[str, ...]):
    for key in path:
        if not isinstance(obj, dict):
            return None
        obj = obj.get(key)
    return obj


def _upstream_fields(contract: str) -> tuple[set[str], str]:
    """Fields the captured upstream page documents, with the source that proves it."""
    if contract == "skill-frontmatter":
        if not os.path.exists(_SKILL_PAGE):
            return set(), "MISSING captured skills page"
        with open(_SKILL_PAGE, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        start = next((i for i, l in enumerate(lines) if _SKILL_HEADING.match(l)), None)
        if start is None:
            return set(), "no 'Frontmatter reference' heading in captured page"
        found: set[str] = set()
        for line in lines[start + 1 :]:
            if _HEADING.match(line):
                break
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or set(cells[0]) <= set("-: "):
                continue
            m = _TABLE_FIELD.match(cells[0])
            if m:
                found.add(m.group(1))
        return found, "captured skills page, Frontmatter reference table"

    proj = os.path.join(UPSTREAM, contract, "projection.json")
    if not os.path.exists(proj):
        return set(), "no projection.json"
    with open(proj, encoding="utf-8") as fh:
        data = json.load(fh)
    path = _PROJECTION_FIELDS.get(contract)
    if not path:
        return set(), "no field path mapped for this contract"
    fields = _dig(data, path)
    if not isinstance(fields, dict):
        return set(), f"projection path {'.'.join(path)} is not a field map"
    return set(fields), f"projection.json {'.'.join(path)}"


def _schema_properties(path: str) -> set[str]:
    """Every `properties` key in a schema file, at any nesting depth."""
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    acc: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "properties" and isinstance(value, dict):
                    acc.update(value.keys())
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return acc


def _kernel_fields(contract: str) -> tuple[set[str], set[str]]:
    """(upstream-base properties, is-overlay properties) for a contract.

    The composed schema is a pure allOf of $refs, so reading it directly yields
    nothing — the parts must be read individually. Keeping base and overlay
    separate is deliberate: it distinguishes "upstream says so" from "IS chose
    to require it", which is exactly the line the authority flip turns on.
    """
    base = _schema_properties(os.path.join(KERNEL, "upstream-base", f"{contract}.v1.json"))
    overlay = _schema_properties(os.path.join(KERNEL, "is-overlay", f"{contract}.v1.json"))
    return base, overlay


def _validator_fields(contract: str) -> tuple[set[str], str]:
    """Field names from the marketplace validator's module-level inventory.

    Parsed from source rather than imported: importing executes a 5,000-line
    module belonging to another repo, and this instrument must stay stdlib-only
    and side-effect-free.
    """
    const = _VALIDATOR_SETS.get(contract)
    if not const:
        return set(), "validator models no inventory for this contract"
    path = os.path.abspath(VALIDATOR)
    if not os.path.exists(path):
        return set(), "validator not checked out alongside this repo"
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    m = re.search(rf"^{const}\s*=\s*\{{(.*?)^\}}", src, re.S | re.M)
    if not m:
        return set(), f"{const} not found in the validator"
    # Only TOP-LEVEL keys, pinned to exactly one indent level and to a dict
    # value. These inventories map each field to a descriptor
    # ({"type": ..., "source": ..., "tier": ...}), so an indent-agnostic match
    # harvests the descriptor keys too and reports `type`, `source`, `tier` and
    # `valid` as though they were frontmatter fields — inventing flip blockers
    # that do not exist, in the one report whose whole purpose is an honest count.
    return set(re.findall(r"^ {4}[\"']([A-Za-z$][A-Za-z0-9_.-]*)[\"']\s*:\s*\{", m.group(1), re.M)), const


def _row(contract: str) -> dict:
    upstream, up_src = _upstream_fields(contract)
    base, overlay = _kernel_fields(contract)
    kernel = base | overlay
    validator, val_src = _validator_fields(contract)
    return {
        "contract": contract,
        "upstream": sorted(upstream),
        "upstream_source": up_src,
        "kernel_base": sorted(base),
        "kernel_overlay": sorted(overlay),
        "validator": sorted(validator),
        "validator_source": val_src,
        # Named gaps, never a summed score.
        "upstream_only": sorted(upstream - kernel - validator),
        "kernel_missing": sorted(validator - kernel),
        "kernel_only": sorted(kernel - upstream) if upstream else [],
        "validator_gap": sorted(kernel - validator) if validator else [],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--contract")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    contracts = ["skill-frontmatter", "agent-definition", "plugin-manifest", "hook-config", "marketplace-catalog"]
    if args.contract:
        if args.contract not in contracts:
            print(f"ERROR: unknown contract {args.contract!r}; known: {', '.join(contracts)}", file=sys.stderr)
            return 2
        contracts = [args.contract]

    rows = [_row(c) for c in contracts]

    if args.as_json:
        print(json.dumps({"contracts": rows}, indent=2))
        return 0

    print("completeness ledger — three independent inventories, never summed\n")
    print(f"  {'contract':22s} {'upstream':>9s} {'kernel':>18s} {'validator':>10s}")
    for r in rows:
        kern = f"{len(r['kernel_base'])}+{len(r['kernel_overlay'])}"
        val = str(len(r["validator"])) if r["validator"] else "—"
        print(f"  {r['contract']:22s} {len(r['upstream']):9d} {kern:>18s} {val:>10s}")
    print("\n  kernel column reads base+overlay (upstream-modelled + IS-added).")

    for r in rows:
        print(f"\n─ {r['contract']}")
        print(f"    upstream  : {len(r['upstream'])} fields  ({r['upstream_source']})")
        print(f"    kernel    : {len(r['kernel_base'])} base + {len(r['kernel_overlay'])} overlay")
        print(f"    validator : {len(r['validator'])} fields  ({r['validator_source']})")
        if r["kernel_missing"]:
            print(f"    !! FLIP BLOCKER — validator enforces, kernel does not model ({len(r['kernel_missing'])}):")
            print(f"       {', '.join(r['kernel_missing'])}")
        if r["upstream_only"]:
            print(f"    extraction debt — documented upstream, modelled nowhere ({len(r['upstream_only'])}):")
            print(f"       {', '.join(r['upstream_only'])}")
        if r["validator_gap"]:
            print(f"    enforcement debt — kernel models, validator ignores ({len(r['validator_gap'])}):")
            print(f"       {', '.join(r['validator_gap'])}")
        if r["kernel_only"]:
            print(f"    kernel-only — IS overlay or drift ({len(r['kernel_only'])}):")
            print(f"       {', '.join(r['kernel_only'])}")

    blockers = sum(len(r["kernel_missing"]) for r in rows)
    print(
        f"\n  {blockers} field(s) are enforced by the marketplace validator but unmodelled by the kernel. "
        "Until that is zero, repointing the validator at the kernel narrows the contract it enforces."
        if blockers
        else "\n  No flip blockers: the kernel models everything the validator enforces."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
