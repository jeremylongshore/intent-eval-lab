#!/usr/bin/env python3
"""Deep-capture normative projection for the hook-config contract (060-AT-SPEC).

The hook-config contract gets the deep capture skill-frontmatter, mcp-config,
plugin-manifest, and agent-definition already have: a vendored upstream
snapshot set under specs/_vendor/upstream/hook-config/ plus a deterministic
NORMATIVE PROJECTION (projection.json) extracted from it. The projection is
the field-diff left-hand side for FF#2 on this contract (Kleppmann: diff
projections field-by-field, never raw page bytes).

Like plugin-manifest and agent-definition (and unlike mcp-config): hook-config
has NO machine-readable upstream schema at all. The authorities (precedence
per specs/upstream-surface-registry.v1.json + 050-AT-SPEC):

  reference-doc   claude-code-hooks.md — code.claude.com/docs/en/hooks.md,
                  whose Hook-lifecycle event table, three-levels-of-nesting
                  Configuration statement, Matcher-patterns tables, and five
                  handler-field tables ARE the spec.
  supporting-doc  claude-code-settings.md — the hooks page's Hook-locations
                  section references /en/settings#hook-configuration for
                  hooks-block placement + allowManagedHooksOnly; it defines
                  NO handler fields, so the extractor does not consume it
                  (vendored for provenance; it IS a registered surface,
                  claude-settings, unlike 059's supporting doc).
  sample-hooks    sample-*.hooks.json — real plugin hooks/hooks.json files
                  from anthropics/claude-plugins-official (commit-pinned),
                  real-world ground truth that CORROBORATES the doc.

DEVIATIONS from the 059 template: (1) the handler-field tables carry
lowercase yes/no in the Required column; (2) the residue rule for "Accepts"
enum clauses additionally tolerates a literal "(default)" marker (the shell
field: Accepts `"bash"` (default) or `"powershell"`); (3) enum tokens are
stripped of surrounding double quotes (the doc backticks JSON string
literals); (4) the section slicer is fence-aware — the hooks page embeds
bash/json code fences whose comment lines start with '#'.

Provenance rule (conservative by construction): a handler field the page
documents is source "documented"; a field used in samples but absent from
the page is recorded under fields_observed_not_documented — never promoted
to "documented". This capture has two such fields (rewakeMessage,
rewakeSummary). No wall-clock in the output — regeneration is deterministic
from the vendored bytes alone.

The self-test additionally cross-checks the committed projection against the
kernel's upstream-base expectations (intent-eval-core
schemas/authoring/v1/upstream-base/hook-config.v1.json — read-only
reference, embedded here as fixtures because the kernel lives in another
repo and CI is offline). Agreements AND divergences are both printed;
divergences are findings to report, never kernel edits (tier-3 promotion is
human, 052-AT-SPEC). The computed finding sets must exactly match the
expected sets, so any re-capture that shifts a finding fails loud and a
human reconciles.

Stdlib only. Offline. Exit 0 = ok; 1 = staleness / self-test failure;
2 = usage / parse error.

Usage:
  extract-hook-config-projection.py --extract     # fresh projection to stdout
  extract-hook-config-projection.py --write       # (re)write projection.json
  extract-hook-config-projection.py --check       # fail if committed projection is stale (vs the FROZEN doc)
  extract-hook-config-projection.py --check-fresh # fail if it drifted from the CAPTURED upstream page
  extract-hook-config-projection.py --self-test   # offline fixtures + kernel cross-check
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from typing import Any

# The shared captured-snapshot resolver lives in scripts/lib/. Hyphenated script
# filenames are not importable as modules, so this script puts its OWN directory on
# sys.path first: it runs as `python3 scripts/<name>.py` in CI (where sys.path[0] is
# already scripts/) but is loaded by file path under pytest, where it is not.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import captured_source  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream", "hook-config")

CONTRACT = "hook-config"
PROJECTION_VERSION = "spec-projection/v1"

# Mechanical anchors in the hooks reference doc.
_LIFECYCLE_HEADING = "## Hook lifecycle"
_CONFIG_HEADING = "## Configuration"
_LOCATIONS_HEADING = "### Hook locations"
_MATCHER_HEADING = "### Matcher patterns"
_HANDLER_HEADING = "### Hook handler fields"
_COMMON_HEADING = "#### Common fields"
_COMMAND_HEADING = "#### Command hook fields"
_HTTP_HEADING = "#### HTTP hook fields"
_MCP_HEADING = "#### MCP tool hook fields"
_PROMPT_AGENT_HEADING = "#### Prompt and agent hook fields"
_NESTING_SENTENCE = "The configuration has three levels of nesting:"
_FIVE_TYPES_SENTENCE = "There are five types:"
_NO_MATCHER_CELL = "no matcher support"
_DEFAULTS_MARKER = "Defaults: "
_EXPECTED_COLUMNS = ["Field", "Required", "Description"]
_CELL_SPLIT = re.compile(r"(?<!\\)\|")
_BACKTICK = re.compile(r"`([^`]+)`")
_TYPE_BULLET = re.compile(r"^\*\s+\*\*\[[^\]]+\]\([^)]+\)\*\*\s+\(`type: \"([a-z_]+)\"`\)")
_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_FENCE = re.compile(r"^```")


# ── Extraction: the reference doc (the spec — there is no machine schema) ───


def _fence_mask(lines: list[str]) -> list[bool]:
    """True for every line inside a ``` code fence (the hooks page embeds
    bash/json examples whose '#' comment lines would fake headings)."""
    mask, inside = [], False
    for ln in lines:
        if _FENCE.match(ln.strip()):
            mask.append(True)  # fence delimiters themselves never match headings
            inside = not inside
        else:
            mask.append(inside)
    return mask


def _section(lines: list[str], heading: str, stop_prefixes: tuple[str, ...]) -> list[str]:
    """Slice the section under `heading` (up to the next same-or-higher
    heading), fence-aware on both the start and stop scans."""
    mask = _fence_mask(lines)
    start = next((i for i, ln in enumerate(lines) if ln.strip() == heading and not mask[i]), None)
    if start is None:
        print(f"ERROR: {heading!r} anchor not found in the hooks doc", file=sys.stderr)
        sys.exit(2)
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith(stop_prefixes) and not mask[i]),
        len(lines),
    )
    return lines[start:end]


def _split_row(row: str) -> list[str]:
    """Split a markdown table row on unescaped pipes; unescape cell contents."""
    cells = _CELL_SPLIT.split(row.strip())[1:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


_SEPARATOR_CELL = re.compile(r"^:?-+:?$")


def _table(section: list[str], what: str, require_backtick: bool = True) -> tuple[list[str], list[list[str]]]:
    """(header, data rows) of the first table in `section`. With
    require_backtick (the Field tables), data rows are exactly the rows whose
    first cell carries a backticked token; without it (the Hook-locations and
    matcher-evaluation tables, whose first cells mix code spans, links, and
    plain prose), every row after the separator is data."""
    start = next((i for i, ln in enumerate(section) if ln.lstrip().startswith("| ")), None)
    if start is None:
        print(f"ERROR: no table found in the {what} section", file=sys.stderr)
        sys.exit(2)
    header = _split_row(section[start])
    rows = []
    for ln in section[start + 1 :]:
        if not ln.lstrip().startswith("|"):
            break
        cells = _split_row(ln)
        if not cells or all(_SEPARATOR_CELL.match(c) for c in cells):
            continue
        if require_backtick and not _BACKTICK.search(cells[0]):
            continue
        rows.append(cells)
    if not rows:
        print(f"ERROR: the {what} table has no data rows", file=sys.stderr)
        sys.exit(2)
    return header, rows


def _strip_quotes(token: str) -> str:
    return token[1:-1] if len(token) >= 2 and token[0] == token[-1] == '"' else token


def _enum_from_description(desc: str) -> list[str] | None:
    """Closed-set value clause -> enum; open clauses -> None.

    Two mechanical forms on the hooks page: (a) the WHOLE description is a
    backticked closed list (the `type` row); (b) an 'Accepts ' clause up to
    the next '.'. A clause becomes an enum ONLY when removing backticked
    tokens, commas, 'or', a literal '(default)' marker, and whitespace
    leaves nothing AND >=2 tokens remain. Tokens shed surrounding double
    quotes (the doc backticks JSON string literals)."""
    idx = desc.find("Accepts ")
    clause = desc if idx == -1 else desc[idx + len("Accepts ") :]
    if idx != -1:
        stop = clause.find(".")
        if stop != -1:
            clause = clause[:stop]
    tokens = _BACKTICK.findall(clause)
    residue = re.sub(r"`[^`]+`", "", clause)
    residue = re.sub(r"\(default\)|\bor\b|,|\s", "", residue)
    if len(tokens) >= 2 and not residue:
        return [_strip_quotes(t) for t in tokens]
    return None


def _field_rows(section: list[str], what: str, scope: str) -> dict[str, dict[str, Any]]:
    """One handler-field table -> {field: {required, scope, source, enum?}}.
    The Required column carries lowercase yes/no on this page (059 deviation)."""
    header, rows = _table(section, what)
    if header != _EXPECTED_COLUMNS:
        print(f"ERROR: the {what} table columns changed: {header}", file=sys.stderr)
        sys.exit(2)
    fields: dict[str, dict[str, Any]] = {}
    for cells in rows:
        field = _BACKTICK.search(cells[0]).group(1)
        desc = cells[2] if len(cells) > 2 else ""
        entry: dict[str, Any] = {
            "required": (cells[1] if len(cells) > 1 else "") == "yes",
            "scope": scope,
            "source": "documented",
        }
        enum = _enum_from_description(desc)
        if enum:
            entry["enum"] = enum
        fields[field] = entry
    return fields


def _timeout_defaults(desc: str) -> dict[str, int]:
    """'Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`;
    60 for `agent`.' -> {handler type: seconds}."""
    idx = desc.find(_DEFAULTS_MARKER)
    if idx == -1:
        print(f"ERROR: {_DEFAULTS_MARKER!r} anchor not found in the timeout row", file=sys.stderr)
        sys.exit(2)
    clause = desc[idx + len(_DEFAULTS_MARKER) :]
    stop = clause.find(".")
    if stop != -1:
        clause = clause[:stop]
    defaults: dict[str, int] = {}
    for part in clause.split(";"):
        m = re.match(r"\s*(\d+) for (.+)", part)
        if not m:
            print(f"ERROR: unparseable timeout-defaults part: {part!r}", file=sys.stderr)
            sys.exit(2)
        for token in _BACKTICK.findall(m.group(2)):
            defaults[_strip_quotes(token)] = int(m.group(1))
    return defaults


def _strip_markup(cell: str) -> str:
    """Markdown links -> their text; backticks dropped (the Hook-locations
    Location column mixes plain text, links, and code spans)."""
    return re.sub(r"\s+", " ", _MD_LINK.sub(r"\1", cell).replace("`", "")).strip()


def extract_reference_doc(doc_path: str) -> dict[str, Any]:
    with open(doc_path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    # 1. The Hook-lifecycle table: THE documented event enumeration.
    _, event_rows = _table(_section(lines, _LIFECYCLE_HEADING, ("## ", "### ")), "Hook lifecycle")
    events = [_BACKTICK.search(cells[0]).group(1) for cells in event_rows]

    # 2. The Configuration section: the three-levels-of-nesting statement is
    #    a hard anchor — the config shape's one-sentence spec.
    config_section = _section(lines, _CONFIG_HEADING, ("## ",))
    if not any(_NESTING_SENTENCE in ln for ln in config_section):
        print(f"ERROR: nesting anchor {_NESTING_SENTENCE!r} not found", file=sys.stderr)
        sys.exit(2)

    # 3. Hook locations: where a hooks block may be defined.
    _, location_rows = _table(_section(lines, _LOCATIONS_HEADING, ("## ", "### ")), "Hook locations", require_backtick=False)
    locations = [_strip_markup(cells[0]) for cells in location_rows]

    # 4. Matcher patterns: evaluation forms + the no-matcher-support events.
    matcher_section = _section(lines, _MATCHER_HEADING, ("## ", "### "))
    _, eval_rows = _table(matcher_section, "Matcher patterns", require_backtick=False)
    match_all_cell = next((cells[0] for cells in eval_rows if len(cells) > 1 and cells[1] == "Match all"), None)
    if match_all_cell is None:
        print("ERROR: no 'Match all' row in the matcher-evaluation table", file=sys.stderr)
        sys.exit(2)
    match_all_forms = {
        "empty": '""' in match_all_cell,
        "omitted": "omitted" in match_all_cell,
        "star": '"*"' in match_all_cell,
    }
    regex_fallback = any(len(c) > 1 and "regular expression" in c[1] for c in eval_rows)
    # The second matcher table (per-event filter fields) carries the
    # no-matcher-support rows; its first cell may list several events.
    no_matcher: set[str] = set()
    rest = matcher_section[next(i for i, ln in enumerate(matcher_section) if ln.lstrip().startswith("| ")) :]
    after_first = next(i for i, ln in enumerate(rest) if not ln.lstrip().startswith("|"))
    _, filter_rows = _table(rest[after_first:], "matcher per-event filter")
    for cells in filter_rows:
        if len(cells) > 1 and cells[1] == _NO_MATCHER_CELL:
            no_matcher.update(_BACKTICK.findall(cells[0]))
    unknown_no_matcher = sorted(no_matcher - set(events))
    if unknown_no_matcher:
        print(f"ERROR: no-matcher-support row names undocumented event(s): {unknown_no_matcher}", file=sys.stderr)
        sys.exit(2)

    # 5. Handler types: the five-types bullet list under Hook handler fields.
    handler_section = _section(lines, _HANDLER_HEADING, ("## ", "### "))
    if not any(_FIVE_TYPES_SENTENCE in ln for ln in handler_section):
        print(f"ERROR: anchor {_FIVE_TYPES_SENTENCE!r} not found", file=sys.stderr)
        sys.exit(2)
    handler_types = [m.group(1) for m in (_TYPE_BULLET.match(ln) for ln in handler_section) if m]
    if len(handler_types) != 5:
        print(f"ERROR: expected 5 handler-type bullets, found {handler_types}", file=sys.stderr)
        sys.exit(2)

    # 6. The five handler-field tables.
    fields = _field_rows(_section(lines, _COMMON_HEADING, ("## ", "### ", "#### ")), "Common fields", "common")
    fields.update(_field_rows(_section(lines, _COMMAND_HEADING, ("## ", "### ", "#### ")), "Command hook fields", "command"))
    fields.update(_field_rows(_section(lines, _HTTP_HEADING, ("## ", "### ", "#### ")), "HTTP hook fields", "http"))
    fields.update(_field_rows(_section(lines, _MCP_HEADING, ("## ", "### ", "#### ")), "MCP tool hook fields", "mcp_tool"))
    fields.update(
        _field_rows(_section(lines, _PROMPT_AGENT_HEADING, ("## ", "### ", "#### ")), "Prompt and agent hook fields", "prompt-agent")
    )
    if "timeout" not in fields:
        print("ERROR: the common-fields table lost its timeout row", file=sys.stderr)
        sys.exit(2)
    common_section = _section(lines, _COMMON_HEADING, ("## ", "### ", "#### "))
    _, common_rows = _table(common_section, "Common fields")
    timeout_desc = next(cells[2] for cells in common_rows if _BACKTICK.search(cells[0]).group(1) == "timeout")

    return {
        "config": {
            "locations": locations,
            "three_level_nesting": True,
        },
        "events": {
            "count": len(events),
            "enum": events,
        },
        "handler_fields": fields,
        "handler_types": handler_types,
        "matcher": {
            "match_all_forms": match_all_forms,
            "no_matcher_support_events": sorted(no_matcher),
            "regex_fallback_documented": regex_fallback,
        },
        "timeout_defaults": _timeout_defaults(timeout_desc),
    }


# ── Extraction: the vendored sample hooks.json files (corroboration only) ───


def extract_samples(sample_paths: list[str]) -> dict[str, Any]:
    top_level: set[str] = set()
    events: set[str] = set()
    types: set[str] = set()
    handler_fields: set[str] = set()
    matcher_values: set[str] = set()
    timeout_values: set[int] = set()
    matcher_omitted = False
    for path in sample_paths:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if "hooks" not in data or not isinstance(data["hooks"], dict):
            print(f"ERROR: sample {os.path.basename(path)} has no hooks object", file=sys.stderr)
            sys.exit(2)
        top_level.update(data)
        for event, groups in data["hooks"].items():
            events.add(event)
            for group in groups:
                if "matcher" in group:
                    matcher_values.add(group["matcher"])
                else:
                    matcher_omitted = True
                for handler in group.get("hooks", []):
                    handler_fields.update(handler)
                    if "type" in handler:
                        types.add(handler["type"])
                    if isinstance(handler.get("timeout"), int):
                        timeout_values.add(handler["timeout"])
    return {
        "count": len(sample_paths),
        "events_observed": sorted(events),
        "handler_fields_observed": sorted(handler_fields),
        "handler_types_observed": sorted(types),
        "matcher_omitted_observed": matcher_omitted,
        "matcher_values_observed": sorted(matcher_values),
        "timeout_values_observed": sorted(timeout_values),
        "top_level_keys_observed": sorted(top_level),
    }


# ── The projection ───────────────────────────────────────────────────────────


def load_vendor_meta(vendor_dir: str) -> dict[str, Any]:
    with open(os.path.join(vendor_dir, "vendor-meta.json"), encoding="utf-8") as fh:
        return json.load(fh)


def build_projection(vendor_dir: str, reference_doc_path: str | None = None) -> dict[str, Any]:
    """Extract the normative projection from the vendored capture.

    `reference_doc_path` repoints ONLY the file this extractor parses — used by
    --check-fresh to read the captured upstream page instead of the frozen
    hand-vendored copy. Samples and supporting docs are never repointed: being
    commit-pinned ground truth that corroborates the doc is precisely their value,
    and the provenance rule (documented vs observed-in-samples, never promoted)
    depends on them holding still.
    """
    meta = load_vendor_meta(vendor_dir)
    docs = [f["file"] for f in meta["files"] if f["role"] == "reference-doc"]
    supporting = sorted(f["file"] for f in meta["files"] if f["role"] == "supporting-doc")
    samples = sorted(f["file"] for f in meta["files"] if f["role"] == "sample-hooks")
    if len(docs) != 1 or not samples:
        print("ERROR: vendor-meta.json needs exactly one reference-doc and >=1 sample-hooks", file=sys.stderr)
        sys.exit(2)

    doc = extract_reference_doc(reference_doc_path or os.path.join(vendor_dir, docs[0]))
    sample_facts = extract_samples([os.path.join(vendor_dir, s) for s in samples])

    # Cross-corroboration (the provenance rule): documented handler fields get
    # an observed_in_samples marker; sample-only fields are recorded under
    # fields_observed_not_documented — NEVER promoted to "documented".
    observed = set(sample_facts["handler_fields_observed"])
    for field, entry in doc["handler_fields"].items():
        entry["observed_in_samples"] = field in observed
    sample_facts["fields_observed_not_documented"] = sorted(observed - set(doc["handler_fields"]))
    sample_facts["events_outside_documented_enum"] = sorted(
        set(sample_facts["events_observed"]) - set(doc["events"]["enum"])
    )
    sample_facts["types_outside_documented_enum"] = sorted(
        set(sample_facts["handler_types_observed"]) - set(doc["handler_types"])
    )

    return {
        "captured_from": {"reference_doc": docs[0], "samples": samples, "supporting_docs": supporting},
        "config": doc["config"],
        "contract": "hook-config",
        "events": doc["events"],
        "handler_fields": doc["handler_fields"],
        "handler_types": doc["handler_types"],
        "matcher": doc["matcher"],
        "projection_version": PROJECTION_VERSION,
        "samples": sample_facts,
        "spec_version": meta["spec_version"],
        "timeout_defaults": doc["timeout_defaults"],
    }


def render(projection: dict[str, Any]) -> str:
    return json.dumps(projection, indent=2, sort_keys=True) + "\n"


def projection_path(vendor_dir: str) -> str:
    return os.path.join(vendor_dir, "projection.json")


def cmd_check(vendor_dir: str) -> int:
    fresh = render(build_projection(vendor_dir))
    path = projection_path(vendor_dir)
    if not os.path.exists(path):
        print(f"extract-hook-config-projection --check: FAIL — projection missing: {path}")
        return 1
    with open(path, encoding="utf-8") as fh:
        committed = fh.read()
    if committed != fresh:
        print(
            f"extract-hook-config-projection --check: STALE — {path} does not match a fresh "
            "extraction from the vendored snapshots. The projection is DERIVED — never hand-edit it. "
            "Regenerate: python3 scripts/extract-hook-config-projection.py --write"
        )
        return 1
    print("extract-hook-config-projection --check: OK — committed projection is fresh.")
    return 0


def cmd_check_fresh(vendor_dir: str, surface: str | None = None) -> int:
    """Diff the committed projection against a projection of the CAPTURED page.

    `--check` proves the committed projection still matches the FROZEN vendored doc
    it was derived from. That is honest self-consistency, and it is green by
    construction: specs/_vendor/upstream/ is hand-vendored and fetch-capture.py
    cannot write it, so neither operand can move. This is the missing other half —
    it repoints the parsed reference doc at specs/_vendor/<surface>/snapshot<ext>,
    the tier-2 tree the capture stage advances on a FETCH_OK fetch, and reports what
    actually changed field by field.

    0 = no semantic drift; 1 = drift (a human reconciles); 2 = the comparison could
    not be set up. Treat 2 as red: a gate that did not run is not a gate that passed.
    """
    label = "extract-hook-config-projection --check-fresh"
    try:
        meta = load_vendor_meta(vendor_dir)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{label}: INOPERABLE — cannot read vendor-meta.json in {vendor_dir}: {exc}", file=sys.stderr)
        return 2
    try:
        doc_file, doc_surface = captured_source.reference_doc_surface(meta)
        surface = surface or doc_surface
        snapshot = captured_source.resolve_captured_snapshot(surface, expected_contract=CONTRACT)
    except captured_source.InoperableError as exc:
        print(f"{label}: INOPERABLE — {exc}", file=sys.stderr)
        return 2

    committed_path = projection_path(vendor_dir)
    try:
        with open(committed_path, encoding="utf-8") as fh:
            base = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{label}: INOPERABLE — cannot read {committed_path}: {exc}", file=sys.stderr)
        return 2

    try:
        fresh = build_projection(vendor_dir, reference_doc_path=snapshot)
    except SystemExit as exc:
        # A deliberate anchor failure already exits 2; keep that code.
        return exc.code if isinstance(exc.code, int) else 2
    except Exception as exc:  # noqa: BLE001 - any parse breakage is INOPERABLE, never drift
        # Bare next()/json.loads() inside the extractors raise StopIteration /
        # JSONDecodeError on a malformed capture. Uncaught, python exits 1, which
        # the driver reads as DRIFT — so the watcher would open a RECONCILIATION
        # issue for a PARSER breakage. Reconciling a phantom drift is worse than
        # no signal, which is the distinction the 0/1/2 split exists to protect.
        print(
            f"{label}: INOPERABLE — the extractor could not parse the captured page "
            f"({os.path.relpath(snapshot, REPO_ROOT)}): {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return 2
    context = (
        f"committed projection vs the captured '{surface}' page "
        f"({os.path.relpath(snapshot, REPO_ROOT)}, standing in for {doc_file})"
    )
    return captured_source.report(captured_source.diff_projections(base, fresh), context, label)


# ── Kernel cross-check (read-only reference; reported, never fixed here) ────
#
# Source: intent-eval-core schemas/authoring/v1/upstream-base/hook-config.v1.json
# (the kernel repo). Embedded as fixtures: the kernel is another repo and this
# check is offline. Kernel edits are OUT OF SCOPE — divergences are findings.

KERNEL_EXPECTATIONS = {
    "source": "intent-eval-core schemas/authoring/v1/upstream-base/hook-config.v1.json",
    "required": ["command", "event", "matcher", "type"],
    "properties": ["command", "event", "matcher", "metadata", "type"],
    "event_enum": [
        "SessionStart", "Setup", "UserPromptSubmit", "UserPromptExpansion", "PreToolUse",
        "PermissionRequest", "PermissionDenied", "PostToolUse", "PostToolUseFailure",
        "PostToolBatch", "Notification", "MessageDisplay", "SubagentStart", "SubagentStop",
        "TaskCreated", "TaskCompleted", "Stop", "StopFailure", "TeammateIdle",
        "InstructionsLoaded", "ConfigChange", "CwdChanged", "FileChanged", "WorktreeCreate",
        "WorktreeRemove", "PreCompact", "PostCompact", "Elicitation", "ElicitationResult",
        "SessionEnd",
    ],
    "type_enum": ["command", "http", "mcp_tool", "prompt", "agent"],
    "flattened_single_hook": True,  # kernel projects the 3-level nesting to one flat entry
    "matcher_min_length": 1,  # kernel requires an explicit non-empty matcher
}

# The expected finding sets for the CURRENT capture (hooks.md @ sha bd7d4bae…
# + 4 claude-plugins-official samples @ eb1510e1). A re-capture that shifts
# either set fails the self-test loud; a human reconciles (and only a human
# ever promotes anything into the kernel).
EXPECTED_AGREEMENTS = [
    "event-enum-exact-30-values-lifecycle-table-order",
    "type-enum-exact-5-handler-kinds",
    "command-required-for-command-handlers-both-sides",
    "samples-corroborate:events-and-types-within-documented-enums",
]
EXPECTED_DIVERGENCES = [
    "shape:kernel-flattens-3-level-nesting-to-single-hook-entry-carrying-event-and-matcher",
    "matcher:doc-allows-omit-empty-star-match-all;kernel-requires-explicit-non-empty",
    "doc-handler-fields-not-in-kernel:allowedEnvVars,args,async,asyncRewake,headers,if,"
    "input,model,once,prompt,server,shell,statusMessage,timeout,tool,url",
    "kernel-only-fields-not-documented-upstream:metadata",
    "per-type-required-fields:kernel-models-command-handler-only;unmodeled-required:prompt,server,tool,url",
    "samples:handler-fields-outside-documented-set:rewakeMessage,rewakeSummary",
]


def kernel_cross_check(projection: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Compare the projection against the kernel expectations. Returns
    (agreements, divergences) — both are REPORTED; neither is 'fixed' here."""
    agreements: list[str] = []
    divergences: list[str] = []
    fields = projection["handler_fields"]
    samples = projection["samples"]
    k = KERNEL_EXPECTATIONS

    if projection["events"]["enum"] == k["event_enum"]:
        agreements.append("event-enum-exact-30-values-lifecycle-table-order")
    else:
        divergences.append("event-enum:mismatch")

    if projection["handler_types"] == k["type_enum"]:
        agreements.append("type-enum-exact-5-handler-kinds")
    else:
        divergences.append("type-enum:mismatch")

    if fields.get("command", {}).get("required") is True and "command" in k["required"]:
        agreements.append("command-required-for-command-handlers-both-sides")
    else:
        divergences.append("command-required:mismatch")

    if not samples["events_outside_documented_enum"] and not samples["types_outside_documented_enum"]:
        agreements.append("samples-corroborate:events-and-types-within-documented-enums")
    else:
        divergences.append(
            "samples:outside-documented-enums:"
            + ",".join(samples["events_outside_documented_enum"] + samples["types_outside_documented_enum"])
        )

    if projection["config"]["three_level_nesting"] and k["flattened_single_hook"]:
        # The kernel's $comment documents this projection choice; it is still
        # a structural divergence from the wire shape, reported every run.
        divergences.append("shape:kernel-flattens-3-level-nesting-to-single-hook-entry-carrying-event-and-matcher")

    forms = projection["matcher"]["match_all_forms"]
    if (forms["empty"] or forms["omitted"] or forms["star"]) and (
        "matcher" in k["required"] and k["matcher_min_length"] >= 1
    ):
        divergences.append("matcher:doc-allows-omit-empty-star-match-all;kernel-requires-explicit-non-empty")

    doc_only = sorted(set(fields) - set(k["properties"]))
    if doc_only:
        divergences.append("doc-handler-fields-not-in-kernel:" + ",".join(doc_only))

    # event + matcher are the flattened nesting levels (covered by the shape
    # divergence above), not handler fields the doc tables carry.
    kernel_only = sorted(set(k["properties"]) - set(fields) - {"event", "matcher"})
    if kernel_only:
        divergences.append("kernel-only-fields-not-documented-upstream:" + ",".join(kernel_only))

    unmodeled_required = sorted(
        f for f, e in fields.items() if e["required"] and e["scope"] not in ("common", "command")
    )
    if unmodeled_required:
        divergences.append(
            "per-type-required-fields:kernel-models-command-handler-only;unmodeled-required:"
            + ",".join(unmodeled_required)
        )

    if samples["fields_observed_not_documented"]:
        divergences.append(
            "samples:handler-fields-outside-documented-set:" + ",".join(samples["fields_observed_not_documented"])
        )

    return agreements, divergences


# ── Deterministic offline self-test ──────────────────────────────────────────

_FIXTURE_DOC = """# Fixture hooks reference

## Hook lifecycle

```bash theme={null}
# Configuration — a decoy heading inside a fence; the slicer must not stop here
```

| Event | When it fires |
| :---- | :------------ |
| `AlphaEvent` | When alpha happens |
| `BetaEvent` | When beta happens |
| `GammaEvent` | When gamma happens |

### How a hook resolves

Nothing mechanical here.

## Configuration

Hooks are defined in JSON settings files. The configuration has three levels of nesting:

### Hook locations

| Location | Scope | Shareable |
| :------- | :---- | :-------- |
| `~/.claude/settings.json` | All your projects | No |
| Managed policy settings | Organization-wide | Yes |
| [Plugin](/en/plugins) `hooks/hooks.json` | When plugin is enabled | Yes |

### Matcher patterns

| Matcher value | Evaluated as | Example |
| :------------ | :----------- | :------ |
| `"*"`, `""`, or omitted | Match all | fires on every occurrence |
| Only letters, digits, `_`, and `\\|` | Exact string, or `\\|`-separated list of exact strings | `Bash` matches only Bash |
| Contains any other character | JavaScript regular expression | `^Notebook` |

Each event type matches on a different field:

| Event | What the matcher filters | Example matcher values |
| :---- | :----------------------- | :--------------------- |
| `AlphaEvent` | tool name | `Bash` |
| `BetaEvent`, `GammaEvent` | no matcher support | always fires on every occurrence |

### Hook handler fields

There are five types:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): run a shell command.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): send a POST request.
* **[MCP tool hooks](#mcp-tool-hook-fields)** (`type: "mcp_tool"`): call a tool.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): single-turn evaluation.
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): spawn a subagent.

#### Common fields

| Field | Required | Description |
| :---- | :------- | :---------- |
| `type` | yes | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"`, or `"agent"` |
| `if` | no | Permission rule syntax to filter when this hook runs |
| `timeout` | no | Seconds before canceling. Defaults: 600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`. Some events lower it |
| `once` | no | If `true`, runs once per session then is removed |

#### Command hook fields

| Field | Required | Description |
| :---- | :------- | :---------- |
| `command` | yes | Shell command to execute |
| `shell` | no | Shell to use for this hook. Accepts `"bash"` (default) or `"powershell"`. Ignored when `args` is set |

#### HTTP hook fields

| Field | Required | Description |
| :---- | :------- | :---------- |
| `url` | yes | URL to send the POST request to |

#### MCP tool hook fields

| Field | Required | Description |
| :---- | :------- | :---------- |
| `server` | yes | Name of a configured MCP server |
| `tool` | yes | Name of the tool to call on that server |

#### Prompt and agent hook fields

| Field | Required | Description |
| :---- | :------- | :---------- |
| `prompt` | yes | Prompt text to send to the model. Use `$ARGUMENTS` as a placeholder |
| `model` | no | Model to use for evaluation. Defaults to a fast model |

## Hook input and output

Nothing here.
"""

_FIXTURE_SAMPLE_A = {
    "description": "fixture",
    "hooks": {
        "AlphaEvent": [
            {
                "matcher": "Bash",
                "hooks": [
                    {"type": "command", "command": "x.sh", "timeout": 7, "if": "Bash(git *)", "bogusField": True}
                ],
            }
        ]
    },
}
_FIXTURE_SAMPLE_B = {
    "hooks": {
        "BetaEvent": [{"hooks": [{"type": "command", "command": "y.sh"}]}],
        "UnknownEvent": [{"hooks": [{"type": "sorcery", "command": "z.sh"}]}],
    },
}


def cmd_self_test(vendor_dir: str) -> int:
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    # 1. Fixture extraction — every mechanical anchor exercised offline.
    with tempfile.TemporaryDirectory() as tmp:
        doc_path = os.path.join(tmp, "doc.md")
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC)

        m = extract_reference_doc(doc_path)
        check("fixture doc: fenced decoy heading skipped (fence-aware slicer)", m["events"]["enum"] == ["AlphaEvent", "BetaEvent", "GammaEvent"])
        check("fixture doc: event count derived", m["events"]["count"] == 3)
        check("fixture doc: three-level nesting anchor found", m["config"]["three_level_nesting"] is True)
        check(
            "fixture doc: locations parsed with link/code markup stripped",
            m["config"]["locations"] == ["~/.claude/settings.json", "Managed policy settings", "Plugin hooks/hooks.json"],
        )
        check(
            "fixture doc: match-all forms star/empty/omitted all detected",
            m["matcher"]["match_all_forms"] == {"empty": True, "omitted": True, "star": True},
        )
        check("fixture doc: regex fallback row detected", m["matcher"]["regex_fallback_documented"] is True)
        check(
            "fixture doc: multi-event no-matcher-support row split",
            m["matcher"]["no_matcher_support_events"] == ["BetaEvent", "GammaEvent"],
        )
        check("fixture doc: five handler types in doc order", m["handler_types"] == ["command", "http", "mcp_tool", "prompt", "agent"])
        check(
            "fixture doc: type enum extracted with quotes stripped",
            m["handler_fields"]["type"].get("enum") == ["command", "http", "mcp_tool", "prompt", "agent"],
        )
        check(
            "fixture doc: shell 'Accepts' enum tolerates the (default) marker",
            m["handler_fields"]["shell"].get("enum") == ["bash", "powershell"],
        )
        check("fixture doc: open clauses stay enum-free (if/once/prompt)", all("enum" not in m["handler_fields"][f] for f in ("if", "once", "prompt", "model")))
        check(
            "fixture doc: required set from lowercase yes column",
            sorted(f for f, e in m["handler_fields"].items() if e["required"]) == ["command", "prompt", "server", "tool", "type", "url"],
        )
        check(
            "fixture doc: per-table scopes recorded",
            (m["handler_fields"]["type"]["scope"], m["handler_fields"]["command"]["scope"], m["handler_fields"]["url"]["scope"], m["handler_fields"]["prompt"]["scope"])
            == ("common", "command", "http", "prompt-agent"),
        )
        check(
            "fixture doc: timeout defaults parsed per handler type",
            m["timeout_defaults"] == {"agent": 60, "command": 600, "http": 600, "mcp_tool": 600, "prompt": 30},
        )

        sample_paths = []
        for i, sample in enumerate((_FIXTURE_SAMPLE_A, _FIXTURE_SAMPLE_B)):
            p = os.path.join(tmp, f"s{i}.hooks.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(sample, fh)
            sample_paths.append(p)
        s = extract_samples(sample_paths)
        check("fixture samples: events + types + fields collected", s["events_observed"] == ["AlphaEvent", "BetaEvent", "UnknownEvent"] and s["handler_types_observed"] == ["command", "sorcery"])
        check("fixture samples: matcher value + omission both observed", s["matcher_values_observed"] == ["Bash"] and s["matcher_omitted_observed"] is True)
        check("fixture samples: timeout values + top-level keys collected", s["timeout_values_observed"] == [7] and s["top_level_keys_observed"] == ["description", "hooks"])

        # Doc without the lifecycle anchor must hard-fail (exit 2), not silently emit.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write("# no hooks reference here\n")
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing lifecycle anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing lifecycle anchor exits 2", exc.code == 2)

        # Section present but nesting-sentence anchor missing must also exit 2.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC.replace(_NESTING_SENTENCE, ""))
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing nesting-sentence anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing nesting-sentence anchor exits 2", exc.code == 2)

    # 2. The committed real projection: fresh (determinism) + sound shape.
    check("committed projection is fresh (--check)", cmd_check(vendor_dir) == 0)
    projection = build_projection(vendor_dir)
    fields = projection["handler_fields"]
    check("real capture: 30 documented lifecycle events", projection["events"]["count"] == 30)
    check(
        "real capture: 18 documented handler fields (6 required)",
        len(fields) == 18 and len([f for f, e in fields.items() if e["required"]]) == 6,
    )
    check(
        "real capture: provenance rule — rewake fields observed-in-samples only",
        projection["samples"]["fields_observed_not_documented"] == ["rewakeMessage", "rewakeSummary"],
    )
    check(
        "real capture: samples stay within documented event/type enums",
        projection["samples"]["events_outside_documented_enum"] == [] and projection["samples"]["types_outside_documented_enum"] == [],
    )
    check("real capture: no wall-clock keys in projection", "fetched_at" not in render(projection) and "generated" not in render(projection))

    # Staleness must be detectable: a hand-edited copy fails --check.
    with tempfile.TemporaryDirectory() as tmp:
        import shutil

        tmp_vendor = os.path.join(tmp, "hook-config")
        shutil.copytree(vendor_dir, tmp_vendor)
        with open(projection_path(tmp_vendor), "a", encoding="utf-8") as fh:
            fh.write("\n")
        check("--check FAILS on a hand-edited projection", cmd_check(tmp_vendor) == 1)

    # 3. Kernel cross-check: report agreements + divergences; exact-match the
    #    expected sets so any re-capture that shifts a finding fails loud.
    agreements, divergences = kernel_cross_check(projection)
    print(f"\nkernel cross-check vs {KERNEL_EXPECTATIONS['source']}:")
    for a in agreements:
        print(f"  AGREEMENT:  {a}")
    for d in divergences:
        print(f"  DIVERGENCE: {d}  (finding to report — kernel edits are out of scope; tier-3 promotion is human)")
    check("cross-check: agreements match expected set", agreements == EXPECTED_AGREEMENTS)
    check("cross-check: divergences match expected set (findings, not fixes)", divergences == EXPECTED_DIVERGENCES)

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the hook-config deep-capture projection machinery is not sound.")
        return 1
    print("\nself-test: extraction anchors, freshness/staleness, and kernel cross-check all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic hook-config deep-capture projection (060-AT-SPEC).")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--extract", action="store_true", help="print a fresh projection to stdout")
    mode.add_argument("--write", action="store_true", help="(re)write projection.json")
    mode.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed projection is stale vs the FROZEN vendored doc (self-consistency)",
    )
    mode.add_argument(
        "--check-fresh",
        action="store_true",
        help="fail if the committed projection has drifted from the CAPTURED upstream page (freshness)",
    )
    mode.add_argument("--self-test", action="store_true", help="offline fixtures + kernel cross-check")
    parser.add_argument("--vendor-dir", default=DEFAULT_VENDOR_DIR, help="vendored capture directory")
    parser.add_argument(
        "--surface",
        default=None,
        help="registry surface whose captured snapshot --check-fresh diffs "
        "(default: the reference-doc's own surface, per vendor-meta.json)",
    )
    args = parser.parse_args()

    # --surface only means anything in --check-fresh. Accepting and IGNORING it
    # in another mode is what let a registry entry name `--check --surface X` and
    # still exit 0 with an authoritative "OK", comparing frozen against frozen.
    if args.surface is not None and not args.check_fresh:
        parser.error("--surface applies only to --check-fresh; in any other mode it would be silently ignored")

    if args.self_test:
        return cmd_self_test(args.vendor_dir)
    if args.check:
        return cmd_check(args.vendor_dir)
    if args.check_fresh:
        return cmd_check_fresh(args.vendor_dir, args.surface)
    fresh = render(build_projection(args.vendor_dir))
    if args.extract:
        sys.stdout.write(fresh)
        return 0
    with open(projection_path(args.vendor_dir), "w", encoding="utf-8") as fh:
        fh.write(fresh)
    print(f"extract-hook-config-projection: wrote {projection_path(args.vendor_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
