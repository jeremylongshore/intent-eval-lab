#!/usr/bin/env python3
"""Deep-capture normative projection for the marketplace-catalog contract (061-AT-SPEC).

The marketplace-catalog contract gets the deep capture skill-frontmatter,
mcp-config, plugin-manifest, agent-definition, and hook-config already have —
the SIXTH and FINAL contract of the deep-capture program: a vendored upstream
snapshot set under specs/_vendor/upstream/marketplace-catalog/ plus a
deterministic NORMATIVE PROJECTION (projection.json) extracted from it. The
projection is the field-diff left-hand side for FF#2 on this contract
(Kleppmann: diff projections field-by-field, never raw page bytes).

Like plugin-manifest, agent-definition, and hook-config: marketplace-catalog
has NO machine-readable upstream schema at all (the $schema URL the official
catalog cites is an editor-autocomplete pointer the page says Claude Code
ignores at load time). The authorities (precedence per
specs/upstream-surface-registry.v1.json + 050-AT-SPEC):

  reference-doc   claude-code-plugin-marketplaces.md —
                  code.claude.com/docs/en/plugin-marketplaces.md, whose
                  Marketplace-schema tables (Required / Owner / Optional +
                  the Reserved-names note + the metadata back-compat
                  sentence), Plugin-entries tables (Required + the
                  Standard-metadata and Component-configuration tables),
                  Plugin-sources tables (the 5-form summary + four per-type
                  Field tables + the sha-beats-ref rule), and Strict-mode
                  table ARE the spec.
  sample-catalog  sample-claude-plugins-official.marketplace.json — THE
                  official ground-truth catalog (anthropics/
                  claude-plugins-official .claude-plugin/marketplace.json,
                  commit-pinned, 223 plugin entries), real-world ground
                  truth that CORROBORATES the doc.

DEVIATIONS from the 058/059/060 templates: (1) "### Required fields" appears
TWICE (under "## Marketplace schema" AND "## Plugin entries") — sections are
sliced two-level (parent "## " section first, then the "### " heading inside
it); (2) requiredness is signaled three different ways — table membership
(top-level + plugin-entry fields), a capitalized Yes/No Required column (the
Owner table), and a "Required."/"Optional." description prefix (the four
per-source-type tables); (3) the "### Optional plugin fields" heading carries
TWO tables introduced by bold markers (**Standard metadata fields:** /
**Component configuration fields:**) — sliced on those markers; (4) the
Plugin-sources summary table marks optional fields with a `?` suffix in its
Fields column — the extractor exact-matches that against the per-type tables
and exits 2 on any contradiction (an internal-consistency anchor the other
captures had no analog for); (5) the object-source discriminator key
("source": "<type>") is documented only via JSON examples — the extractor
parses the first fenced JSON example in each per-type section and verifies
the discriminator; (6) there is exactly ONE sample, but it is the official
catalog itself, so one file carries more corroborating breadth than the
4-5 small samples of 058/059/060 combined.

Provenance rule (conservative by construction): a field the page documents is
source "documented"; anything used in the sample but absent from the page
lands under samples.* *_not_documented / *_outside_documented keys — never
promoted to "documented". This capture has three such tolerances (a `commit`
key on github sources, a `path` key on url sources, the plugin name
`wordpress.com` outside the documented kebab-case). No wall-clock in the
output — regeneration is deterministic from the vendored bytes alone.

The self-test additionally cross-checks the committed projection against the
kernel's upstream-base expectations (intent-eval-core
schemas/authoring/v1/upstream-base/marketplace-catalog.v1.json — read-only
reference, embedded here as fixtures because the kernel lives in another repo
and CI is offline). Agreements AND divergences are both printed; divergences
are findings to report, never kernel edits (tier-3 promotion is human,
052-AT-SPEC). The computed finding sets must exactly match the expected sets,
so any re-capture that shifts a finding fails loud and a human reconciles.

Stdlib only. Offline. Exit 0 = ok; 1 = staleness / self-test failure;
2 = usage / parse error.

Usage:
  extract-marketplace-catalog-projection.py --extract     # fresh projection to stdout
  extract-marketplace-catalog-projection.py --write       # (re)write projection.json
  extract-marketplace-catalog-projection.py --check       # fail if committed projection is stale (vs the FROZEN doc)
  extract-marketplace-catalog-projection.py --check-fresh # fail if it drifted from the CAPTURED upstream page
  extract-marketplace-catalog-projection.py --self-test   # offline fixtures + kernel cross-check
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
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream", "marketplace-catalog")

CONTRACT = "marketplace-catalog"
PROJECTION_VERSION = "spec-projection/v1"

# Mechanical anchors in the plugin-marketplaces reference doc.
_SCHEMA_HEADING = "## Marketplace schema"
_ENTRIES_HEADING = "## Plugin entries"
_SOURCES_HEADING = "## Plugin sources"
_REQUIRED_SUB = "### Required fields"
_OWNER_SUB = "### Owner fields"
_OPTIONAL_SUB = "### Optional fields"
_OPTIONAL_PLUGIN_SUB = "### Optional plugin fields"
_STRICT_SUB = "### Strict mode"
_STD_META_MARKER = "**Standard metadata fields:**"
_COMP_CONF_MARKER = "**Component configuration fields:**"
_RESERVED_MARKER = "**Reserved names**:"
_RESERVED_STOP = ". Names that impersonate"
_BACKCOMPAT_SENTENCE = " are also accepted under `metadata` for backward compatibility"
_MKT_SPECIFIC_MARKER = "plus these marketplace-specific fields:"
_PASSTHROUGH_SENTENCE = "any field from the [plugin manifest schema]"
_SHA_WINS_SENTENCE = "the `sha` is the effective pin"
_SUBDIR_SHORTHAND_SENTENCE = "also accepts a GitHub shorthand"
_MUST_START_SENTENCE = "Must start with `./`"
_DEFAULT_MARKER = "(default)"
# Per-source-type sections, doc order: (heading, type name in the summary table).
_SOURCE_TYPE_SECTIONS = [
    ("### Relative paths", None),  # the string form — example-anchored only
    ("### GitHub repositories", "github"),
    ("### Git repositories", "url"),
    ("### Git subdirectories", "git-subdir"),
    ("### npm packages", "npm"),
]
_FIELD_COLUMNS = ["Field", "Type", "Description"]
_OWNER_COLUMNS = ["Field", "Type", "Required", "Description"]
_SUMMARY_COLUMNS = ["Source", "Type", "Fields", "Notes"]
_STRICT_COLUMNS = ["Value", "Behavior"]
_CELL_SPLIT = re.compile(r"(?<!\\)\|")
_BACKTICK = re.compile(r"`([^`]+)`")
_FENCE = re.compile(r"^```")
_FENCE_JSON = re.compile(r"^```json\b")
_KEBAB = re.compile(r"[a-z0-9]([a-z0-9-]*[a-z0-9])?")


# ── Extraction: the reference doc (the spec — there is no machine schema) ───


def _fence_mask(lines: list[str]) -> list[bool]:
    """True for every line inside a ``` code fence (the page embeds json/bash
    examples whose '#'/'|' lines would fake headings or table rows)."""
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
    heading), fence-aware on both the start and stop scans. Called two-level
    for the '### ' headings that repeat across '## ' sections."""
    mask = _fence_mask(lines)
    start = next((i for i, ln in enumerate(lines) if ln.strip() == heading and not mask[i]), None)
    if start is None:
        print(f"ERROR: {heading!r} anchor not found in the plugin-marketplaces doc", file=sys.stderr)
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
    first cell carries a backticked token; without it (the Plugin-sources
    summary table, whose 'Relative path' row has a plain first cell), every
    row after the separator is data."""
    mask = _fence_mask(section)
    start = next((i for i, ln in enumerate(section) if ln.lstrip().startswith("| ") and not mask[i]), None)
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


def _field_table(section: list[str], what: str) -> tuple[list[str], list[list[str]]]:
    """A Field/Type/Description table (header verified)."""
    header, rows = _table(section, what)
    if header[: len(_FIELD_COLUMNS)] != _FIELD_COLUMNS:
        print(f"ERROR: the {what} table columns changed: {header}", file=sys.stderr)
        sys.exit(2)
    return header, rows


def _anchor_line(section: list[str], marker: str, what: str) -> str:
    line = next((ln for ln in section if marker in ln), None)
    if line is None:
        print(f"ERROR: {marker!r} anchor not found in the {what} section", file=sys.stderr)
        sys.exit(2)
    return line


def _first_json_example(section: list[str], what: str) -> Any:
    """Parse the first ```json fenced example in `section`."""
    start = next((i for i, ln in enumerate(section) if _FENCE_JSON.match(ln.strip())), None)
    if start is None:
        print(f"ERROR: no fenced JSON example in the {what} section", file=sys.stderr)
        sys.exit(2)
    end = next((i for i in range(start + 1, len(section)) if _FENCE.match(section[i].strip())), None)
    if end is None:
        print(f"ERROR: unterminated JSON fence in the {what} section", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads("\n".join(section[start + 1 : end]))
    except json.JSONDecodeError as exc:
        print(f"ERROR: unparseable JSON example in the {what} section: {exc}", file=sys.stderr)
        sys.exit(2)


def extract_reference_doc(doc_path: str) -> dict[str, Any]:
    with open(doc_path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    # 1. "## Marketplace schema": top-level required + optional field tables,
    #    the owner table, the Reserved-names note, the metadata back-compat
    #    sentence. Requiredness here = table membership.
    schema_sec = _section(lines, _SCHEMA_HEADING, ("## ",))
    top_fields: dict[str, dict[str, Any]] = {}
    _, req_rows = _field_table(_section(schema_sec, _REQUIRED_SUB, ("## ", "### ")), "marketplace Required fields")
    for cells in req_rows:
        top_fields[_BACKTICK.search(cells[0]).group(1)] = {"required": True, "source": "documented", "type": cells[1]}
    _, opt_rows = _field_table(_section(schema_sec, _OPTIONAL_SUB, ("## ", "### ")), "marketplace Optional fields")
    for cells in opt_rows:
        top_fields[_BACKTICK.search(cells[0]).group(1)] = {"required": False, "source": "documented", "type": cells[1]}

    header, owner_rows = _table(_section(schema_sec, _OWNER_SUB, ("## ", "### ")), "Owner fields")
    if header != _OWNER_COLUMNS:
        print(f"ERROR: the Owner fields table columns changed: {header}", file=sys.stderr)
        sys.exit(2)
    owner_fields = {
        _BACKTICK.search(cells[0]).group(1): {"required": cells[2] == "Yes", "source": "documented", "type": cells[1]}
        for cells in owner_rows
    }

    reserved_line = _anchor_line(schema_sec, _RESERVED_MARKER, "Marketplace schema")
    stop = reserved_line.find(_RESERVED_STOP)
    if stop == -1:
        print(f"ERROR: {_RESERVED_STOP!r} stop anchor not found in the Reserved-names note", file=sys.stderr)
        sys.exit(2)
    reserved_names = _BACKTICK.findall(reserved_line[reserved_line.find(_RESERVED_MARKER) : stop])

    backcompat_line = _anchor_line(schema_sec, _BACKCOMPAT_SENTENCE, "Marketplace schema")
    backcompat_fields = _BACKTICK.findall(backcompat_line[: backcompat_line.find(_BACKCOMPAT_SENTENCE)])

    # 2. "## Plugin entries": the second "### Required fields" (two-level
    #    slicing), the two bold-marker tables under "### Optional plugin
    #    fields", the marketplace-specific-fields sentence, and the
    #    manifest-passthrough sentence.
    entries_sec = _section(lines, _ENTRIES_HEADING, ("## ",))
    entry_fields: dict[str, dict[str, Any]] = {}
    _, ereq_rows = _field_table(_section(entries_sec, _REQUIRED_SUB, ("## ", "### ")), "plugin-entry Required fields")
    for cells in ereq_rows:
        entry_fields[_BACKTICK.search(cells[0]).group(1)] = {
            "required": True,
            "scope": "entry-required",
            "source": "documented",
            "type": cells[1],
        }
    opt_plugin_sec = _section(entries_sec, _OPTIONAL_PLUGIN_SUB, ("## ", "### "))
    for marker, scope in ((_STD_META_MARKER, "standard-metadata"), (_COMP_CONF_MARKER, "component-config")):
        idx = next((i for i, ln in enumerate(opt_plugin_sec) if ln.strip() == marker), None)
        if idx is None:
            print(f"ERROR: {marker!r} sub-table marker not found under {_OPTIONAL_PLUGIN_SUB!r}", file=sys.stderr)
            sys.exit(2)
        _, rows = _field_table(opt_plugin_sec[idx:], f"{scope} fields")
        for cells in rows:
            entry_fields[_BACKTICK.search(cells[0]).group(1)] = {
                "required": False,
                "scope": scope,
                "source": "documented",
                "type": cells[1],
            }

    specific_line = _anchor_line(entries_sec, _MKT_SPECIFIC_MARKER, "Plugin entries")
    clause = specific_line[specific_line.find(_MKT_SPECIFIC_MARKER) + len(_MKT_SPECIFIC_MARKER) :]
    stop = clause.find(".")
    marketplace_specific = _BACKTICK.findall(clause[:stop] if stop != -1 else clause)
    if not marketplace_specific:
        print("ERROR: the marketplace-specific-fields sentence names no fields", file=sys.stderr)
        sys.exit(2)
    _anchor_line(entries_sec, _PASSTHROUGH_SENTENCE, "Plugin entries")

    # 3. "## Plugin sources": the 5-form summary table, the four per-type
    #    Field tables (Required./Optional. description prefixes — exact-matched
    #    against the summary's `?`-suffix convention), the discriminator-key
    #    JSON examples, the './'-prefix rule, and the sha-beats-ref sentence.
    sources_sec = _section(lines, _SOURCES_HEADING, ("## ",))
    header, summary_rows = _table(sources_sec, "Plugin sources summary", require_backtick=False)
    if header != _SUMMARY_COLUMNS:
        print(f"ERROR: the Plugin-sources summary table columns changed: {header}", file=sys.stderr)
        sys.exit(2)
    summary: dict[str, dict[str, list[str]]] = {}
    relative_path_row = None
    for cells in summary_rows:
        if _BACKTICK.search(cells[0]):
            tokens = _BACKTICK.findall(cells[2])
            summary[_BACKTICK.search(cells[0]).group(1)] = {
                "optional": sorted(t[:-1] for t in tokens if t.endswith("?")),
                "required": sorted(t for t in tokens if not t.endswith("?")),
            }
        else:
            relative_path_row = cells
    if relative_path_row is None or "`string`" not in relative_path_row[1]:
        print("ERROR: the summary table lost its string-typed Relative-path row", file=sys.stderr)
        sys.exit(2)
    if _MUST_START_SENTENCE not in relative_path_row[3]:
        print(f"ERROR: {_MUST_START_SENTENCE!r} rule not found in the Relative-path row", file=sys.stderr)
        sys.exit(2)

    object_types: dict[str, dict[str, list[str]]] = {}
    for heading, type_name in _SOURCE_TYPE_SECTIONS:
        sec = _section(sources_sec, heading, ("## ", "### "))
        example = _first_json_example(sec, heading)
        if type_name is None:  # the string form: example anchors the './' shape
            src = example.get("source")
            if not (isinstance(src, str) and src.startswith("./")):
                print(f"ERROR: the {heading} example is not a './'-prefixed string source", file=sys.stderr)
                sys.exit(2)
            continue
        src = example.get("source")
        if not (isinstance(src, dict) and src.get("source") == type_name):
            print(f"ERROR: the {heading} example does not carry discriminator source={type_name!r}", file=sys.stderr)
            sys.exit(2)
        _, rows = _field_table(sec, heading)
        required, optional = [], []
        for cells in rows:
            field = _BACKTICK.search(cells[0]).group(1)
            desc = cells[2] if len(cells) > 2 else ""
            if desc.startswith("Required."):
                required.append(field)
            elif desc.startswith("Optional."):
                optional.append(field)
            else:
                print(f"ERROR: {heading} row {field!r} has no Required./Optional. prefix", file=sys.stderr)
                sys.exit(2)
        per_type = {"optional": sorted(optional), "required": sorted(required)}
        if summary.get(type_name) != per_type:
            print(
                f"ERROR: summary-table vs per-type contradiction for {type_name!r}: "
                f"{summary.get(type_name)} != {per_type}",
                file=sys.stderr,
            )
            sys.exit(2)
        object_types[type_name] = per_type
    if sorted(object_types) != sorted(summary):
        print(f"ERROR: summary names types {sorted(summary)} but per-type sections cover {sorted(object_types)}", file=sys.stderr)
        sys.exit(2)

    _anchor_line(sources_sec, _SHA_WINS_SENTENCE, "Plugin sources")
    _anchor_line(sources_sec, _SUBDIR_SHORTHAND_SENTENCE, "Git subdirectories")

    # 4. "### Strict mode" (lives under "## Plugin sources"): the Value table.
    header, strict_rows = _table(_section(sources_sec, _STRICT_SUB, ("## ", "### ")), "Strict mode")
    if header != _STRICT_COLUMNS:
        print(f"ERROR: the Strict-mode table columns changed: {header}", file=sys.stderr)
        sys.exit(2)
    strict_values = [_BACKTICK.search(cells[0]).group(1) for cells in strict_rows]
    default_cells = [cells for cells in strict_rows if _DEFAULT_MARKER in cells[0]]
    if len(default_cells) != 1:
        print(f"ERROR: expected exactly one '(default)' Strict-mode row, found {len(default_cells)}", file=sys.stderr)
        sys.exit(2)
    strict_default = _BACKTICK.search(default_cells[0][0]).group(1)

    return {
        "catalog": {
            "metadata_backcompat_fields": backcompat_fields,
            "reserved_names": reserved_names,
            "top_level_fields": top_fields,
        },
        "owner_fields": owner_fields,
        "plugin_entry": {
            "fields": entry_fields,
            "manifest_passthrough_documented": True,
            "marketplace_specific_fields": marketplace_specific,
            "strict_default": strict_default,
            "strict_values": strict_values,
        },
        "sources": {
            "discriminator_key": "source",
            "forms_count": 1 + len(object_types),
            "git_subdir_url_accepts_github_shorthand_and_ssh": True,
            "object_types": object_types,
            "relative_path": {"must_start_with": "./", "type": "string"},
            "sha_wins_over_ref": True,
        },
    }


# ── Extraction: the vendored sample catalog (corroboration only) ────────────


def extract_samples(sample_paths: list[str]) -> dict[str, Any]:
    top_level: set[str] = set()
    metadata_keys: set[str] = set()
    owner_keys: set[str] = set()
    entry_fields: set[str] = set()
    object_types: set[str] = set()
    object_fields: dict[str, set[str]] = {}
    strict_values: set[str] = set()
    names: list[str] = []
    plugin_entries = 0
    string_count = 0
    string_all_dot_slash = True
    for path in sample_paths:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data.get("plugins"), list):
            print(f"ERROR: sample {os.path.basename(path)} has no plugins array", file=sys.stderr)
            sys.exit(2)
        top_level.update(data)
        if isinstance(data.get("metadata"), dict):
            metadata_keys.update(data["metadata"])
        if isinstance(data.get("owner"), dict):
            owner_keys.update(data["owner"])
        for entry in data["plugins"]:
            plugin_entries += 1
            entry_fields.update(entry)
            names.append(entry.get("name", ""))
            source = entry.get("source")
            if isinstance(source, str):
                string_count += 1
                if not source.startswith("./"):
                    string_all_dot_slash = False
            elif isinstance(source, dict):
                stype = source.get("source", "")
                object_types.add(stype)
                object_fields.setdefault(stype, set()).update(k for k in source if k != "source")
            if "strict" in entry:
                strict_values.add(json.dumps(entry["strict"]))
    return {
        "count": len(sample_paths),
        "entry_fields_observed": sorted(entry_fields),
        "metadata_keys_observed": sorted(metadata_keys),
        "object_source_fields_observed": {t: sorted(f) for t, f in sorted(object_fields.items())},
        "object_source_types_observed": sorted(object_types),
        "owner_keys_observed": sorted(owner_keys),
        "plugin_entries": plugin_entries,
        "plugin_names_outside_kebab_case": sorted(n for n in names if not _KEBAB.fullmatch(n)),
        "strict_values_observed": sorted(strict_values),
        "string_sources": {"all_start_with_dot_slash": string_all_dot_slash, "count": string_count},
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
    samples = sorted(f["file"] for f in meta["files"] if f["role"] == "sample-catalog")
    if len(docs) != 1 or not samples:
        print("ERROR: vendor-meta.json needs exactly one reference-doc and >=1 sample-catalog", file=sys.stderr)
        sys.exit(2)

    doc = extract_reference_doc(reference_doc_path or os.path.join(vendor_dir, docs[0]))
    sample_facts = extract_samples([os.path.join(vendor_dir, s) for s in samples])

    # Cross-corroboration (the provenance rule): documented fields get an
    # observed_in_samples marker; anything sample-only lands under
    # *_not_documented / *_outside_documented keys — NEVER promoted to
    # "documented". Dotted top-level fields (metadata.pluginRoot) resolve
    # against the observed metadata sub-keys.
    top = doc["catalog"]["top_level_fields"]
    observed_top = set(sample_facts["top_level_keys_observed"])
    for field, entry in top.items():
        if "." in field:
            parent, child = field.split(".", 1)
            entry["observed_in_samples"] = parent == "metadata" and child in sample_facts["metadata_keys_observed"]
        else:
            entry["observed_in_samples"] = field in observed_top
    for field, entry in doc["owner_fields"].items():
        entry["observed_in_samples"] = field in sample_facts["owner_keys_observed"]
    entry_fields = doc["plugin_entry"]["fields"]
    observed_entry = set(sample_facts["entry_fields_observed"])
    for field, entry in entry_fields.items():
        entry["observed_in_samples"] = field in observed_entry

    documented_top_parents = {f.split(".", 1)[0] for f in top}
    sample_facts["top_level_keys_not_documented"] = sorted(observed_top - documented_top_parents)
    sample_facts["entry_fields_not_documented"] = sorted(observed_entry - set(entry_fields))
    object_types = doc["sources"]["object_types"]
    sample_facts["object_source_types_outside_documented"] = sorted(
        set(sample_facts["object_source_types_observed"]) - set(object_types)
    )
    sample_facts["object_source_fields_outside_documented"] = sorted(
        f"{stype}:{field}"
        for stype, fields in sample_facts["object_source_fields_observed"].items()
        if stype in object_types
        for field in set(fields) - set(object_types[stype]["required"]) - set(object_types[stype]["optional"])
    )

    return {
        "captured_from": {"reference_doc": docs[0], "samples": samples},
        "catalog": doc["catalog"],
        "contract": "marketplace-catalog",
        "owner_fields": doc["owner_fields"],
        "plugin_entry": doc["plugin_entry"],
        "projection_version": PROJECTION_VERSION,
        "samples": sample_facts,
        "sources": doc["sources"],
        "spec_version": meta["spec_version"],
    }


def render(projection: dict[str, Any]) -> str:
    return json.dumps(projection, indent=2, sort_keys=True) + "\n"


def projection_path(vendor_dir: str) -> str:
    return os.path.join(vendor_dir, "projection.json")


def cmd_check(vendor_dir: str) -> int:
    fresh = render(build_projection(vendor_dir))
    path = projection_path(vendor_dir)
    if not os.path.exists(path):
        print(f"extract-marketplace-catalog-projection --check: FAIL — projection missing: {path}")
        return 1
    with open(path, encoding="utf-8") as fh:
        committed = fh.read()
    if committed != fresh:
        print(
            f"extract-marketplace-catalog-projection --check: STALE — {path} does not match a fresh "
            "extraction from the vendored snapshots. The projection is DERIVED — never hand-edit it. "
            "Regenerate: python3 scripts/extract-marketplace-catalog-projection.py --write"
        )
        return 1
    print("extract-marketplace-catalog-projection --check: OK — committed projection is fresh.")
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
    label = "extract-marketplace-catalog-projection --check-fresh"
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
# Source: intent-eval-core schemas/authoring/v1/upstream-base/marketplace-catalog.v1.json
# (the kernel repo). Embedded as fixtures: the kernel is another repo and this
# check is offline. Kernel edits are OUT OF SCOPE — divergences are findings.

KERNEL_EXPECTATIONS = {
    "source": "intent-eval-core schemas/authoring/v1/upstream-base/marketplace-catalog.v1.json",
    "required": ["name", "owner", "plugins"],
    "properties": ["metadata", "name", "owner", "plugins"],
    "owner_required": ["name"],
    "owner_properties": ["email", "name"],
    "plugin_item_required": ["name", "source"],
    "plugin_item_properties": ["name"],
    "plugins_min_items": 1,  # kernel rejects an empty plugins array (corpus rationale in its $comment)
    "name_pattern": "^[a-z0-9]([a-z0-9-]*[a-z0-9])?$",
    "name_max_length": 64,  # kernel cap; the doc states kebab-case prose only, no length
    "source_unmodeled": True,  # kernel requires `source` on items but gives it no schema (no forms/types)
}

# The expected finding sets for the CURRENT capture (plugin-marketplaces.md @
# sha 1f37e87f… + the official catalog @ eb1510e1). A re-capture that shifts
# either set fails the self-test loud; a human reconciles (and only a human
# ever promotes anything into the kernel).
EXPECTED_AGREEMENTS = [
    "top-level-required-exact-name-owner-plugins-both-sides",
    "owner-shape-inner-name-required-email-optional-both-sides",
    "plugin-entry-minimum-name-plus-source-both-sides",
    "samples-corroborate:top-level-keys-entry-fields-and-source-types-within-documented-sets",
]
EXPECTED_DIVERGENCES = [
    "plugins-min-items:kernel-requires-minItems-1;doc-states-no-minimum",
    "doc-top-level-optional-fields-not-in-kernel:$schema,allowCrossMarketplaceDependenciesOn,description,version",
    "doc-plugin-entry-optional-fields-not-in-kernel:agents,author,category,commands,defaultEnabled,description,"
    "displayName,homepage,hooks,keywords,license,lspServers,mcpServers,repository,skills,strict,tags,version",
    "source-forms:doc-documents-relative-path-string-plus-4-object-types;kernel-leaves-source-unmodeled",
    "name-constraints:kernel-adds-maxLength-64-and-kebab-regex;doc-prose-kebab-case-plus-14-reserved-names-not-encoded",
    "samples:tolerances-outside-documented-surface:github:commit,url:path,plugin-name:wordpress.com",
]


def kernel_cross_check(projection: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Compare the projection against the kernel expectations. Returns
    (agreements, divergences) — both are REPORTED; neither is 'fixed' here."""
    agreements: list[str] = []
    divergences: list[str] = []
    top = projection["catalog"]["top_level_fields"]
    owner = projection["owner_fields"]
    entry_fields = projection["plugin_entry"]["fields"]
    samples = projection["samples"]
    sources = projection["sources"]
    k = KERNEL_EXPECTATIONS

    if sorted(f for f, e in top.items() if e["required"]) == k["required"]:
        agreements.append("top-level-required-exact-name-owner-plugins-both-sides")
    else:
        divergences.append("top-level-required:mismatch")

    if (
        owner.get("name", {}).get("required") is True
        and owner.get("email", {}).get("required") is False
        and k["owner_required"] == ["name"]
        and sorted(owner) == k["owner_properties"]
    ):
        agreements.append("owner-shape-inner-name-required-email-optional-both-sides")
    else:
        divergences.append("owner-shape:mismatch")

    if sorted(f for f, e in entry_fields.items() if e["required"]) == k["plugin_item_required"]:
        agreements.append("plugin-entry-minimum-name-plus-source-both-sides")
    else:
        divergences.append("plugin-entry-required:mismatch")

    if (
        not samples["top_level_keys_not_documented"]
        and not samples["entry_fields_not_documented"]
        and not samples["object_source_types_outside_documented"]
    ):
        agreements.append("samples-corroborate:top-level-keys-entry-fields-and-source-types-within-documented-sets")
    else:
        divergences.append(
            "samples:outside-documented-sets:"
            + ",".join(
                samples["top_level_keys_not_documented"]
                + samples["entry_fields_not_documented"]
                + samples["object_source_types_outside_documented"]
            )
        )

    if k["plugins_min_items"] == 1:
        # The doc states no minimum for the plugins array; the kernel's
        # minItems:1 is a corpus-rationalized narrowing. Reported every run.
        divergences.append("plugins-min-items:kernel-requires-minItems-1;doc-states-no-minimum")

    doc_top_only = sorted({f.split(".", 1)[0] for f, e in top.items() if not e["required"]} - set(k["properties"]))
    if doc_top_only:
        divergences.append("doc-top-level-optional-fields-not-in-kernel:" + ",".join(doc_top_only))

    entry_only = sorted(set(f for f, e in entry_fields.items() if not e["required"]) - set(k["plugin_item_properties"]))
    if entry_only:
        divergences.append("doc-plugin-entry-optional-fields-not-in-kernel:" + ",".join(entry_only))

    if sources["forms_count"] == 1 + len(sources["object_types"]) and k["source_unmodeled"]:
        divergences.append(
            f"source-forms:doc-documents-relative-path-string-plus-{len(sources['object_types'])}-object-types;"
            "kernel-leaves-source-unmodeled"
        )

    if k["name_max_length"] and projection["catalog"]["reserved_names"]:
        divergences.append(
            f"name-constraints:kernel-adds-maxLength-{k['name_max_length']}-and-kebab-regex;"
            f"doc-prose-kebab-case-plus-{len(projection['catalog']['reserved_names'])}-reserved-names-not-encoded"
        )

    tolerances = samples["object_source_fields_outside_documented"] + [
        f"plugin-name:{n}" for n in samples["plugin_names_outside_kebab_case"]
    ]
    if tolerances:
        divergences.append("samples:tolerances-outside-documented-surface:" + ",".join(tolerances))

    return agreements, divergences


# ── Deterministic offline self-test ──────────────────────────────────────────

_FIXTURE_DOC = """# Fixture plugin-marketplaces reference

```bash theme={null}
# ## Marketplace schema — a decoy heading inside a fence; the slicer must not start here
```

## Marketplace schema

### Required fields

| Field | Type | Description | Example |
| :---- | :--- | :---------- | :------ |
| `name` | string | Marketplace identifier (kebab-case, no spaces) | `"acme-tools"` |
| `owner` | object | Marketplace maintainer information | |
| `plugins` | array | List of available plugins | See below |

<Note>
  **Reserved names**: These are reserved: `alpha-mart`, `beta-mart`. Names that impersonate official marketplaces, such as `gamma-mart`, are also blocked.
</Note>

### Owner fields

| Field | Type | Required | Description |
| :---- | :--- | :------- | :---------- |
| `name` | string | Yes | Name of the maintainer or team |
| `email` | string | No | Contact email for the maintainer |

### Optional fields

| Field | Type | Description |
| :---- | :--- | :---------- |
| `$schema` | string | JSON Schema URL for editor autocomplete |
| `description` | string | Brief marketplace description |
| `version` | string | Marketplace manifest version |
| `metadata.pluginRoot` | string | Base directory prepended to relative plugin source paths |

`description` and `version` are also accepted under `metadata` for backward compatibility.

## Plugin entries

You can include any field from the [plugin manifest schema](/en/plugins-reference#plugin-manifest-schema), plus these marketplace-specific fields: `source`, `category`, and `strict`.

### Required fields

| Field | Type | Description |
| :---- | :--- | :---------- |
| `name` | string | Plugin identifier (kebab-case, no spaces) |
| `source` | string\\|object | Where to fetch the plugin from |

### Optional plugin fields

**Standard metadata fields:**

| Field | Type | Description |
| :---- | :--- | :---------- |
| `description` | string | Brief plugin description |
| `strict` | boolean | Controls whether plugin.json is the authority |

**Component configuration fields:**

| Field | Type | Description |
| :---- | :--- | :---------- |
| `hooks` | string\\|object | Custom hooks configuration or path to hooks file |

## Plugin sources

| Source | Type | Fields | Notes |
| ------ | ---- | ------ | ----- |
| Relative path | `string` (e.g. `"./my-plugin"`) | none | Local directory. Must start with `./`. Resolved relative to the marketplace root |
| `github` | object | `repo`, `ref?`, `sha?` | |
| `url` | object | `url`, `ref?`, `sha?` | Git URL source |
| `git-subdir` | object | `url`, `path`, `ref?`, `sha?` | Subdirectory within a git repo |
| `npm` | object | `package`, `version?`, `registry?` | Installed via `npm install` |

When both `ref` and `sha` are set on any of them, the `sha` is the effective pin.

### Relative paths

```json theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

### GitHub repositories

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

| Field | Type | Description |
| :---- | :--- | :---------- |
| `repo` | string | Required. GitHub repository in `owner/repo` format |
| `ref` | string | Optional. Git branch or tag |
| `sha` | string | Optional. Full 40-character git commit SHA |

### Git repositories

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

| Field | Type | Description |
| :---- | :--- | :---------- |
| `url` | string | Required. Full git repository URL |
| `ref` | string | Optional. Git branch or tag |
| `sha` | string | Optional. Full 40-character git commit SHA |

### Git subdirectories

```json theme={null}
{
  "name": "sub-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

The `url` field also accepts a GitHub shorthand (`owner/repo`) or SSH URLs.

| Field | Type | Description |
| :---- | :--- | :---------- |
| `url` | string | Required. Git repository URL |
| `path` | string | Required. Subdirectory path within the repo |
| `ref` | string | Optional. Git branch or tag |
| `sha` | string | Optional. Full 40-character git commit SHA |

### npm packages

```json theme={null}
{
  "name": "npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

| Field | Type | Description |
| :---- | :--- | :---------- |
| `package` | string | Required. Package name or scoped package |
| `version` | string | Optional. Version or version range |
| `registry` | string | Optional. Custom npm registry URL |

### Strict mode

| Value | Behavior |
| :---- | :------- |
| `true` (default) | plugin.json is the authority |
| `false` | The marketplace entry is the entire definition |

## Host and distribute marketplaces

Nothing mechanical here.
"""

_FIXTURE_SAMPLE = {
    "name": "fixture-mart",
    "owner": {"name": "Fixture", "email": "f@example.com"},
    "metadata": {"pluginRoot": "./plugins"},
    "plugins": [
        {"name": "alpha", "source": "./plugins/alpha", "description": "d", "strict": False},
        {"name": "Beta.Plugin", "source": {"source": "github", "repo": "o/r", "commit": "c" * 40}},
        {"name": "gamma", "source": {"source": "sorcery", "spell": "x"}, "bogusField": True},
    ],
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
        top = m["catalog"]["top_level_fields"]
        check(
            "fixture doc: fenced decoy heading skipped; 7 top-level fields (3 required by table membership)",
            len(top) == 7 and sorted(f for f, e in top.items() if e["required"]) == ["name", "owner", "plugins"],
        )
        check("fixture doc: dotted optional field kept verbatim", top.get("metadata.pluginRoot", {}).get("required") is False)
        check("fixture doc: reserved names stop before the impersonation clause", m["catalog"]["reserved_names"] == ["alpha-mart", "beta-mart"])
        check("fixture doc: metadata back-compat fields extracted", m["catalog"]["metadata_backcompat_fields"] == ["description", "version"])
        check(
            "fixture doc: owner table capitalized Yes/No Required column",
            m["owner_fields"]["name"]["required"] is True and m["owner_fields"]["email"]["required"] is False,
        )
        entry = m["plugin_entry"]
        check(
            "fixture doc: second '### Required fields' resolved by two-level slicing",
            sorted(f for f, e in entry["fields"].items() if e["required"]) == ["name", "source"],
        )
        check(
            "fixture doc: bold-marker sub-tables scoped standard-metadata / component-config",
            entry["fields"]["strict"]["scope"] == "standard-metadata" and entry["fields"]["hooks"]["scope"] == "component-config",
        )
        check("fixture doc: escaped-pipe types unescaped", entry["fields"]["source"]["type"] == "string|object")
        check("fixture doc: marketplace-specific sentence tokens", entry["marketplace_specific_fields"] == ["source", "category", "strict"])
        check("fixture doc: strict default + values from the Strict-mode table", entry["strict_default"] == "true" and entry["strict_values"] == ["true", "false"])
        src = m["sources"]
        check("fixture doc: 5 source forms (string + 4 object types)", src["forms_count"] == 5 and sorted(src["object_types"]) == ["git-subdir", "github", "npm", "url"])
        check(
            "fixture doc: summary `?`-suffix sets exact-match the per-type Required./Optional. prefixes",
            src["object_types"]["git-subdir"] == {"optional": ["ref", "sha"], "required": ["path", "url"]}
            and src["object_types"]["npm"] == {"optional": ["registry", "version"], "required": ["package"]},
        )

        # Summary-vs-per-type contradiction must hard-fail (exit 2).
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC.replace("| `repo` | string | Required.", "| `repo` | string | Optional."))
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: summary-vs-per-type contradiction exits 2", False)
        except SystemExit as exc:
            check("fixture doc: summary-vs-per-type contradiction exits 2", exc.code == 2)

        # Discriminator mismatch in the JSON example must hard-fail (exit 2).
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC.replace('"source": "npm",', '"source": "mpn",'))
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: example-discriminator mismatch exits 2", False)
        except SystemExit as exc:
            check("fixture doc: example-discriminator mismatch exits 2", exc.code == 2)

        # Missing schema-section anchor must hard-fail (exit 2), not silently emit.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write("# no marketplaces reference here\n")
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing schema-section anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing schema-section anchor exits 2", exc.code == 2)

        sample_path = os.path.join(tmp, "s.marketplace.json")
        with open(sample_path, "w", encoding="utf-8") as fh:
            json.dump(_FIXTURE_SAMPLE, fh)
        s = extract_samples([sample_path])
        check(
            "fixture sample: top-level + metadata + owner keys collected",
            s["top_level_keys_observed"] == ["metadata", "name", "owner", "plugins"]
            and s["metadata_keys_observed"] == ["pluginRoot"]
            and s["owner_keys_observed"] == ["email", "name"],
        )
        check(
            "fixture sample: string sources counted with './' rule honored",
            s["string_sources"] == {"all_start_with_dot_slash": True, "count": 1},
        )
        check(
            "fixture sample: object source types + non-discriminator fields collected",
            s["object_source_types_observed"] == ["github", "sorcery"]
            and s["object_source_fields_observed"] == {"github": ["commit", "repo"], "sorcery": ["spell"]},
        )
        check("fixture sample: non-kebab plugin name caught", s["plugin_names_outside_kebab_case"] == ["Beta.Plugin"])
        check("fixture sample: strict values as JSON literals", s["strict_values_observed"] == ["false"])

    # 2. The committed real projection: fresh (determinism) + sound shape.
    check("committed projection is fresh (--check)", cmd_check(vendor_dir) == 0)
    projection = build_projection(vendor_dir)
    top = projection["catalog"]["top_level_fields"]
    entry_fields = projection["plugin_entry"]["fields"]
    samples = projection["samples"]
    check("real capture: 8 documented top-level fields (3 required)", len(top) == 8 and len([f for f, e in top.items() if e["required"]]) == 3)
    check("real capture: 14 reserved marketplace names", len(projection["catalog"]["reserved_names"]) == 14)
    check(
        "real capture: 20 documented plugin-entry fields (2 required, 12 standard-metadata, 6 component-config)",
        len(entry_fields) == 20
        and len([f for f, e in entry_fields.items() if e["required"]]) == 2
        and len([f for f, e in entry_fields.items() if e["scope"] == "standard-metadata"]) == 12
        and len([f for f, e in entry_fields.items() if e["scope"] == "component-config"]) == 6,
    )
    check(
        "real capture: 5 source forms with sha-beats-ref + strict default true",
        projection["sources"]["forms_count"] == 5
        and projection["sources"]["sha_wins_over_ref"] is True
        and projection["plugin_entry"]["strict_default"] == "true",
    )
    check(
        "real capture: official catalog corroborates — 223 entries, 50 './' string sources",
        samples["plugin_entries"] == 223 and samples["string_sources"] == {"all_start_with_dot_slash": True, "count": 50},
    )
    check(
        "real capture: provenance rule — commit/path source keys observed-in-samples only",
        samples["object_source_fields_outside_documented"] == ["github:commit", "url:path"],
    )
    check(
        "real capture: provenance rule — wordpress.com plugin name outside documented kebab-case",
        samples["plugin_names_outside_kebab_case"] == ["wordpress.com"],
    )
    check(
        "real capture: sample top-level keys, entry fields, and source types all documented",
        samples["top_level_keys_not_documented"] == []
        and samples["entry_fields_not_documented"] == []
        and samples["object_source_types_outside_documented"] == [],
    )
    check("real capture: no wall-clock keys in projection", "fetched_at" not in render(projection) and "generated" not in render(projection))

    # Staleness must be detectable: a hand-edited copy fails --check.
    with tempfile.TemporaryDirectory() as tmp:
        import shutil

        tmp_vendor = os.path.join(tmp, "marketplace-catalog")
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
        print(f"\nself-test: {failures} FAILURE(S) — the marketplace-catalog deep-capture projection machinery is not sound.")
        return 1
    print("\nself-test: extraction anchors, freshness/staleness, and kernel cross-check all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic marketplace-catalog deep-capture projection (061-AT-SPEC).")
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
    print(f"extract-marketplace-catalog-projection: wrote {projection_path(args.vendor_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
