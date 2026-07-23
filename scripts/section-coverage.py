#!/usr/bin/env python3
"""Coverage gate: how much of each normative page the extractors actually read.

Every extract-*-projection.py consumes its upstream page by slicing named
headings — `_section(lines, "## Hook lifecycle", ...)`. Those heading literals
are the extractor's ANCHORS. Everything on the page that no anchor names is
content the projection cannot represent, which means FF#2 cannot diff it and
the drift board cannot go red on it. Today that unread remainder is the
majority of every page, and nothing measured it.

That is the failure this gate closes. A table-only parser produces a projection
that looks complete and diffs clean while the normative weight of the page —
body prose, budgets, precedence chains, denylists, behaviour tables — sits
outside the projection entirely. "The map got smaller" and "the map is clean"
render identically downstream unless coverage is a published number.

WHAT "REACHED" MEANS (read this before quoting the number)

A heading counts as reached when an extractor names it as a slice anchor. It is
deliberately the strict reading: `_section()` slices from its anchor to the next
stop-prefix, so lines under an anchored heading — including its subsections —
are fed to the extractor even though those subsections are not themselves
anchors. This gate therefore UNDERSTATES bytes-consumed and reports exactly one
thing: how much of the page structure the extractor addresses by name.

That is the honest instrument for the question being asked. A subsection that
happens to fall inside a parent slice is read only incidentally; nothing asserts
its shape, and a heading inserted above it upstream silently changes what the
slice contains. Counting it as covered would let structural drift hide inside a
green number. Both figures are printed — `anchored` is the ratchet, `in-slice`
is reported alongside so the gap between them stays visible.

RATCHET

Per-contract floors live in the registry under `section_coverage_floor`. Like
`semantic_coverage_floor`, they are floors and not targets: coverage shrinking
must be an explicit, reviewed edit in the same change, because a smaller map is
indistinguishable from a clean one at a glance.

Stdlib only, offline. Exit 0 = at or above every floor; 1 = below a floor or a
parse problem; 2 = usage / missing inputs.

Usage:
  section-coverage.py                  # report + enforce floors
  section-coverage.py --report-only    # never exit 1 on a floor breach
  section-coverage.py --contract NAME  # single contract
  section-coverage.py --json           # machine-readable
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPSTREAM = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream")
SCRIPTS = os.path.join(REPO_ROOT, "scripts")
REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")

# A markdown ATX heading, level 1-4. Level is capped at 4 because no extractor
# slices deeper and `#####` does not appear in these pages; raising the cap
# would inflate the denominator with headings nothing could reasonably anchor.
_HEADING = re.compile(r"^(#{1,4}) +(.+?)\s*$")

# Heading string literals inside extractor source. Matches the same 1-4 levels
# so the numerator and denominator are drawn on identical terms.
#
# Newlines are excluded from the character class deliberately. Every extractor
# embeds whole fixture PAGES as triple-quoted literals for its self-test, and a
# newline-permissive class swallows an entire fixture as one giant "anchor" —
# which both invents anchors that do not exist and, because those fakes never
# match a real heading, reports them as stale. The anchors this gate cares
# about are always single-line constants.
#
# Backslashes are excluded for the same reason at smaller scale: the negative
# fixtures are single-line strings carrying an escaped newline
# ("# no hooks reference here\\n"). They are fixture text, never anchors, and
# counting them produces phantom stale-anchor findings that train a reader to
# ignore the stale-anchor report — which is the one signal here that catches an
# extractor slicing on a heading upstream has moved.
_HEADING_LITERAL = re.compile(r"""['"](#{1,4} +[^'"\n\\]+)['"]""")

# Fenced code blocks are masked before headings are counted: these pages embed
# bash and json samples whose comment lines begin with '#', and counting those
# as sections would silently inflate the denominator — making coverage look
# worse than it is and, worse, making the number depend on sample churn.
_FENCE = re.compile(r"^\s*(```|~~~)")


# Contracts whose extractor filename does not follow extract-<contract>-projection.py.
# Kept as an explicit exception map rather than a glob: a glob would silently
# re-bind a contract to whatever extractor happened to match after a rename,
# and this gate's whole job is to notice when the thing it measures moved.
_EXTRACTOR_NAME = {
    "mcp-config": "extract-mcp-projection.py",
}


def _mask_fences(lines: list[str]) -> list[bool]:
    """True for lines inside a fenced block."""
    inside = False
    out: list[bool] = []
    for line in lines:
        if _FENCE.match(line):
            out.append(True)
            inside = not inside
            continue
        out.append(inside)
    return out


def _page_headings(text: str) -> list[str]:
    lines = text.splitlines()
    masked = _mask_fences(lines)
    found: list[str] = []
    for line, in_fence in zip(lines, masked):
        if in_fence:
            continue
        m = _HEADING.match(line)
        if m:
            found.append(f"{m.group(1)} {m.group(2)}")
    return found


def _extractor_anchors(src: str) -> set[str]:
    """Heading literals the extractor names, normalised to '## Title' form."""
    return {re.sub(r"\s+", " ", m).strip() for m in _HEADING_LITERAL.findall(src)}


def _in_slice_count(headings: list[str], anchors: set[str]) -> int:
    """Headings that fall inside an anchored heading's slice.

    A slice runs from its anchor until the next heading at the same level or
    shallower, mirroring how `_section()` is called with stop_prefixes across
    the extractors. Counted for reporting only — never for the ratchet.
    """
    reached = 0
    active_level = 0
    for h in headings:
        level = len(h.split(" ", 1)[0])
        if h in anchors:
            reached += 1
            active_level = level
            continue
        if active_level and level > active_level:
            reached += 1
        else:
            active_level = 0
    return reached


def _primary_doc(contract_dir: str, src: str) -> str | None:
    """The .md file the extractor actually reads, per its own source."""
    candidates = sorted(f for f in os.listdir(contract_dir) if f.endswith(".md") and f != "PROVENANCE.md")
    named = [f for f in candidates if f in src]
    if len(named) == 1:
        return named[0]
    # More than one vendored doc is named (hook-config vendors a supporting
    # page it does NOT consume). Prefer the one whose basename the extractor
    # references most — the supporting doc is mentioned once, in prose.
    if named:
        return max(named, key=src.count)
    return candidates[0] if candidates else None


def _collect(only: str | None) -> tuple[list[dict], list[str]]:
    problems: list[str] = []
    rows: list[dict] = []
    if not os.path.isdir(UPSTREAM):
        problems.append(f"vendored upstream tree not found: {UPSTREAM}")
        return rows, problems

    for contract in sorted(os.listdir(UPSTREAM)):
        if only and contract != only:
            continue
        cdir = os.path.join(UPSTREAM, contract)
        if not os.path.isdir(cdir):
            continue
        extractor = os.path.join(SCRIPTS, _EXTRACTOR_NAME.get(contract, f"extract-{contract}-projection.py"))
        if not os.path.exists(extractor):
            problems.append(f"{contract}: no extractor at scripts/extract-{contract}-projection.py")
            continue
        with open(extractor, encoding="utf-8") as fh:
            src = fh.read()
        doc = _primary_doc(cdir, src)
        if not doc:
            problems.append(f"{contract}: no vendored .md page to measure")
            continue
        with open(os.path.join(cdir, doc), encoding="utf-8") as fh:
            headings = _page_headings(fh.read())
        anchors = _extractor_anchors(src)
        matched = [h for h in headings if h in anchors]
        # An anchor naming a heading the page no longer has is itself a drift
        # signal: the extractor is slicing on something that moved or vanished.
        stale = sorted(a for a in anchors if a not in set(headings))
        # An extractor with no heading literals at all is not necessarily
        # reading nothing — mcp-config anchors on a SENTENCE and then parses
        # the fenced JSON block beneath it. Recording that distinction matters:
        # a bare 0.0% reads as "this page is ignored", when the truth is "this
        # page is parsed by a strategy this gate cannot measure". Conflating
        # the two would put a false alarm next to four real ones and cost the
        # whole report its credibility.
        strategy = "heading-slice" if anchors else "non-heading"
        rows.append(
            {
                "contract": contract,
                "doc": doc,
                "strategy": strategy,
                "sections": len(headings),
                "anchored": len(matched),
                "in_slice": _in_slice_count(headings, anchors),
                "uncovered": [h for h in headings if h not in anchors],
                "stale_anchors": stale,
            }
        )
    return rows, problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--contract", help="measure a single contract")
    ap.add_argument("--report-only", action="store_true", help="never exit 1 on a floor breach")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--list-uncovered", action="store_true", help="print every uncovered heading, not a sample")
    args = ap.parse_args()

    rows, problems = _collect(args.contract)
    if problems and not rows:
        for p in problems:
            print(f"ERROR: {p}", file=sys.stderr)
        return 2

    floors: dict[str, int] = {}
    if os.path.exists(REGISTRY):
        with open(REGISTRY, encoding="utf-8") as fh:
            floors = (json.load(fh).get("section_coverage_floor") or {}).get("per_contract") or {}

    breaches: list[str] = []
    for r in rows:
        floor = floors.get(r["contract"])
        r["floor"] = floor
        if isinstance(floor, int) and not isinstance(floor, bool) and r["anchored"] < floor:
            breaches.append(
                f"{r['contract']}: {r['anchored']} anchored sections is below the declared floor of {floor}. "
                "Section coverage SHRANK. If that is intended, lower the floor in the same change so the "
                "reduction is reviewed."
            )

    if args.as_json:
        print(json.dumps({"contracts": rows, "problems": problems, "breaches": breaches}, indent=2))
        return 1 if (breaches and not args.report_only) or problems else 0

    measurable = [r for r in rows if r["strategy"] == "heading-slice"]
    total_s = sum(r["sections"] for r in measurable)
    total_a = sum(r["anchored"] for r in measurable)
    print("section coverage — page structure addressed by name in each extractor\n")
    print(f"  {'contract':22s} {'doc':40s} {'anchored':>11s} {'in-slice':>10s} {'floor':>6s}")
    for r in rows:
        floor = r["floor"] if r["floor"] is not None else "-"
        if r["strategy"] != "heading-slice":
            print(f"  {r['contract']:22s} {r['doc'][:40]:40s} {'n/a — non-heading strategy':>22s} {str(floor):>6s}")
            continue
        pct = (100.0 * r["anchored"] / r["sections"]) if r["sections"] else 0.0
        print(
            f"  {r['contract']:22s} {r['doc'][:40]:40s} "
            f"{r['anchored']:4d}/{r['sections']:<4d}{pct:5.1f}% {r['in_slice']:4d}/{r['sections']:<4d} {str(floor):>6s}"
        )
    overall = (100.0 * total_a / total_s) if total_s else 0.0
    print(f"\n  TOTAL {total_a}/{total_s} sections anchored ({overall:.1f}%) across heading-slice extractors")
    for r in rows:
        if r["strategy"] != "heading-slice":
            print(
                f"  NOTE {r['contract']} anchors on a sentence, not a heading, so its {r['sections']} "
                f"sections are not comparable here — it needs its own coverage instrument."
            )

    for r in rows:
        if r["stale_anchors"]:
            print(f"\n  {r['contract']}: STALE ANCHORS — named by the extractor, absent from the page:")
            for a in r["stale_anchors"]:
                print(f"      {a}")

    print("\nUncovered sections (named, so the gap is countable rather than implied):")
    for r in rows:
        if not r["uncovered"]:
            continue
        shown = r["uncovered"] if args.list_uncovered else r["uncovered"][:12]
        print(f"\n  {r['contract']} — {len(r['uncovered'])} uncovered:")
        for h in shown:
            print(f"      {h}")
        if len(shown) < len(r["uncovered"]):
            print(f"      … {len(r['uncovered']) - len(shown)} more (--list-uncovered for all)")

    for p in problems:
        print(f"\nPROBLEM: {p}")

    if breaches:
        print("\nsection-coverage: FLOOR BREACH")
        for b in breaches:
            print(f"  - {b}")
        if not args.report_only:
            return 1
    if problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
