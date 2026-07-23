#!/usr/bin/env python3
"""Deep-capture normative projection for the plugin-manifest contract (058-AT-SPEC).

The plugin-manifest contract gets the deep capture skill-frontmatter and
mcp-config already have: a vendored upstream snapshot set under
specs/_vendor/upstream/plugin-manifest/ plus a deterministic NORMATIVE
PROJECTION (projection.json) extracted from it. The projection is the
field-diff left-hand side for FF#2 on this contract (Kleppmann: diff
projections field-by-field, never raw page bytes).

DEVIATION from the mcp-config capture: plugin-manifest has NO machine-readable
upstream schema at all. The authorities (precedence per
specs/upstream-surface-registry.v1.json + 050-AT-SPEC):

  reference-doc     claude-code-plugins-reference.md —
                    code.claude.com/docs/en/plugins-reference.md, whose
                    "Plugin manifest schema" section IS the spec: the
                    Required fields / Metadata fields / Component path fields
                    tables, the Complete-schema JSON example, and the
                    unrecognized-fields tolerance prose.
  sample-manifests  sample-*.plugin.json — real plugin.json manifests from
                    anthropics/claude-plugins-official (commit-pinned),
                    real-world ground truth that CORROBORATES the doc.

Provenance rule (conservative by construction): a field the page documents is
source "documented"; a field used in samples but absent from the page is
source "observed-in-samples" with required "unknown" — never promoted to
"documented". Everything extracted is mechanical: table rows parsed from the
three named tables (escaped-pipe types like `string\\|array` unescaped, dotted
fields like `experimental.themes` kept verbatim), the Complete-schema fenced
JSON block parsed, anchor sentences matched verbatim, and the sample JSON
parsed. No wall-clock in the output — regeneration is deterministic from the
vendored bytes alone.

The self-test additionally cross-checks the committed projection against the
kernel's upstream-base expectations (intent-eval-core
schemas/authoring/v1/upstream-base/plugin-manifest.v1.json — read-only
reference, embedded here as fixtures because the kernel lives in another repo
and CI is offline). Agreements AND divergences are both printed; divergences
are findings to report, never kernel edits (tier-3 promotion is human,
052-AT-SPEC). The computed finding sets must exactly match the expected sets,
so any re-capture that shifts a finding fails loud and a human reconciles.

Stdlib only. Offline. Exit 0 = ok; 1 = staleness / self-test failure;
2 = usage / parse error.

Usage:
  extract-plugin-manifest-projection.py --extract     # fresh projection to stdout
  extract-plugin-manifest-projection.py --write       # (re)write projection.json
  extract-plugin-manifest-projection.py --check       # fail if committed projection is stale (vs the FROZEN doc)
  extract-plugin-manifest-projection.py --check-fresh # fail if it drifted from the CAPTURED upstream page
  extract-plugin-manifest-projection.py --self-test   # offline fixtures + kernel cross-check
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
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream", "plugin-manifest")

CONTRACT = "plugin-manifest"
PROJECTION_VERSION = "spec-projection/v1"

# Mechanical anchors in the plugins-reference doc.
_SECTION_HEADING = "## Plugin manifest schema"
_TABLE_HEADINGS = {
    "required": "### Required fields",
    "metadata": "### Metadata fields",
    "component-path": "### Component path fields",
}
_COMPLETE_SCHEMA_HEADING = "### Complete schema"
_REQUIRED_SENTENCE = "`name` is the only required field"
_MANIFEST_OPTIONAL_SENTENCE = "The manifest is optional."
_UNRECOGNIZED_SENTENCE = "ignores top-level fields it does not recognize"
_WRONG_TYPE_SENTENCE = "Fields with the wrong type still fail"
_FENCE_OPEN = re.compile(r"^```json\b")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_CELL_SPLIT = re.compile(r"(?<!\\)\|")
_BACKTICK = re.compile(r"`([^`]+)`")


def _json_type_name(value: Any) -> str:
    return {dict: "object", list: "array", str: "string", bool: "boolean", int: "number", float: "number", type(None): "null"}[type(value)]


# ── Extraction: the reference doc (the spec — there is no machine schema) ───


def _manifest_section(lines: list[str]) -> list[str]:
    """Slice the '## Plugin manifest schema' section (up to the next '## ')."""
    start = next((i for i, ln in enumerate(lines) if ln.strip() == _SECTION_HEADING), None)
    if start is None:
        print(f"ERROR: {_SECTION_HEADING!r} anchor not found in the plugins-reference doc", file=sys.stderr)
        sys.exit(2)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start:end]


def _split_row(row: str) -> list[str]:
    """Split a markdown table row on unescaped pipes; unescape cell contents."""
    cells = _CELL_SPLIT.split(row.strip())[1:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


def _table_rows(section: list[str], heading: str) -> list[list[str]]:
    """Data rows of the first table after `heading`. Header/separator rows have
    no backticked first cell, so data rows are exactly those that do."""
    anchor = next((i for i, ln in enumerate(section) if ln.strip() == heading), None)
    if anchor is None:
        print(f"ERROR: {heading!r} anchor not found in the manifest-schema section", file=sys.stderr)
        sys.exit(2)
    start = next((i for i in range(anchor, len(section)) if section[i].lstrip().startswith("| ")), None)
    if start is None:
        print(f"ERROR: no table found after {heading!r}", file=sys.stderr)
        sys.exit(2)
    rows = []
    for ln in section[start:]:
        if not ln.lstrip().startswith("|"):
            break
        cells = _split_row(ln)
        if cells and _BACKTICK.search(cells[0]):
            rows.append(cells)
    if not rows:
        print(f"ERROR: table after {heading!r} has no data rows", file=sys.stderr)
        sys.exit(2)
    return rows


def _enum_from_description(desc: str) -> list[str] | None:
    """Backticked tokens of an 'One of `a`, `b`, or `c`' clause, where stated."""
    idx = desc.find("One of ")
    if idx == -1:
        return None
    clause = desc[idx:]
    stop = clause.find(".")
    if stop != -1:
        clause = clause[:stop]
    tokens = _BACKTICK.findall(clause)
    return tokens or None


def _complete_schema_fields(section: list[str]) -> list[str]:
    """Top-level keys of the Complete-schema JSON example; `experimental` is
    expanded into dotted children to match the tables' field naming."""
    anchor = next((i for i, ln in enumerate(section) if ln.strip() == _COMPLETE_SCHEMA_HEADING), None)
    if anchor is None:
        print(f"ERROR: {_COMPLETE_SCHEMA_HEADING!r} anchor not found", file=sys.stderr)
        sys.exit(2)
    start = next((i for i in range(anchor, len(section)) if _FENCE_OPEN.match(section[i])), None)
    if start is None:
        print("ERROR: no fenced json block after the Complete-schema anchor", file=sys.stderr)
        sys.exit(2)
    end = next(i for i in range(start + 1, len(section)) if _FENCE_CLOSE.match(section[i]))
    example = json.loads("\n".join(section[start + 1 : end]))
    return sorted(_dotted_keys(example))


def _dotted_keys(manifest: dict[str, Any]) -> list[str]:
    keys: list[str] = []
    for key, value in manifest.items():
        if key == "experimental" and isinstance(value, dict):
            keys.extend(f"experimental.{sub}" for sub in value)
        else:
            keys.append(key)
    return keys


def extract_reference_doc(doc_path: str) -> dict[str, Any]:
    with open(doc_path, encoding="utf-8") as fh:
        text = fh.read()
    section = _manifest_section(text.splitlines())
    section_text = "\n".join(section)

    if _REQUIRED_SENTENCE not in section_text:
        print(f"ERROR: required-set anchor {_REQUIRED_SENTENCE!r} not found", file=sys.stderr)
        sys.exit(2)

    fields: dict[str, dict[str, Any]] = {}
    name_kebab = False
    for table, heading in _TABLE_HEADINGS.items():
        for cells in _table_rows(section, heading):
            field = _BACKTICK.search(cells[0]).group(1)
            desc = cells[2] if len(cells) > 2 else ""
            entry: dict[str, Any] = {
                "required": table == "required",
                "source": "documented",
                "table": table,
                "type": cells[1] if len(cells) > 1 else "unknown",
            }
            enum = _enum_from_description(desc)
            if enum:
                entry["enum"] = enum
            fields[field] = entry
            if field == "name" and "kebab-case" in desc:
                name_kebab = True

    example_fields = _complete_schema_fields(section)
    # A field shown only in the Complete-schema example is still page-documented
    # (conservatively: optional, type = the example value's JSON type).
    example_types = _example_field_types(section)
    for field in example_fields:
        if field not in fields:
            fields[field] = {
                "required": False,
                "source": "documented",
                "table": "complete-schema-example",
                "type": example_types[field],
            }

    return {
        "complete_schema_example_fields": example_fields,
        "fields": fields,
        "manifest_optional": _MANIFEST_OPTIONAL_SENTENCE in section_text,
        "name_kebab_case_prose": name_kebab,
        "name_only_required": True,
        "unrecognized_top_level_ignored": _UNRECOGNIZED_SENTENCE in section_text,
        "wrong_type_fails": _WRONG_TYPE_SENTENCE in section_text,
    }


def _example_field_types(section: list[str]) -> dict[str, str]:
    anchor = next(i for i, ln in enumerate(section) if ln.strip() == _COMPLETE_SCHEMA_HEADING)
    start = next(i for i in range(anchor, len(section)) if _FENCE_OPEN.match(section[i]))
    end = next(i for i in range(start + 1, len(section)) if _FENCE_CLOSE.match(section[i]))
    example = json.loads("\n".join(section[start + 1 : end]))
    types: dict[str, str] = {}
    for key, value in example.items():
        if key == "experimental" and isinstance(value, dict):
            for sub, subval in value.items():
                types[f"experimental.{sub}"] = _json_type_name(subval)
        else:
            types[key] = _json_type_name(value)
    return types


# ── Extraction: the vendored sample manifests (corroboration only) ──────────


def extract_samples(sample_paths: list[str]) -> dict[str, Any]:
    observed_types: dict[str, set[str]] = {}
    author_subfields: set[str] = set()
    for path in sample_paths:
        with open(path, encoding="utf-8") as fh:
            manifest = json.load(fh)
        if not isinstance(manifest, dict):
            print(f"ERROR: sample {os.path.basename(path)} is not a JSON object", file=sys.stderr)
            sys.exit(2)
        for key, value in manifest.items():
            if key == "experimental" and isinstance(value, dict):
                for sub, subval in value.items():
                    observed_types.setdefault(f"experimental.{sub}", set()).add(_json_type_name(subval))
            else:
                observed_types.setdefault(key, set()).add(_json_type_name(value))
            if key == "author" and isinstance(value, dict):
                author_subfields.update(value)
    return {
        "author_subfields_observed": sorted(author_subfields),
        "count": len(sample_paths),
        "field_types_observed": {k: "|".join(sorted(v)) for k, v in sorted(observed_types.items())},
        "top_level_fields_observed": sorted(observed_types),
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
    samples = sorted(f["file"] for f in meta["files"] if f["role"] == "sample-manifest")
    if len(docs) != 1 or not samples:
        print("ERROR: vendor-meta.json needs exactly one reference-doc and >=1 sample-manifest", file=sys.stderr)
        sys.exit(2)

    manifest = extract_reference_doc(reference_doc_path or os.path.join(vendor_dir, docs[0]))
    sample_facts = extract_samples([os.path.join(vendor_dir, s) for s in samples])

    # Cross-corroboration (the provenance rule): documented fields get an
    # observed_in_samples marker; sample-only fields are recorded with
    # source "observed-in-samples" and required "unknown" — NEVER "documented".
    observed = set(sample_facts["top_level_fields_observed"])
    for field, entry in manifest["fields"].items():
        entry["observed_in_samples"] = field in observed
    observed_only = sorted(observed - set(manifest["fields"]))
    for field in observed_only:
        manifest["fields"][field] = {
            "observed_in_samples": True,
            "required": "unknown",
            "source": "observed-in-samples",
            "table": None,
            "type": sample_facts["field_types_observed"][field],
        }
    sample_facts["fields_observed_not_documented"] = observed_only

    return {
        "captured_from": {"reference_doc": docs[0], "samples": samples},
        "contract": "plugin-manifest",
        "manifest": manifest,
        "projection_version": PROJECTION_VERSION,
        "samples": sample_facts,
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
        print(f"extract-plugin-manifest-projection --check: FAIL — projection missing: {path}")
        return 1
    with open(path, encoding="utf-8") as fh:
        committed = fh.read()
    if committed != fresh:
        print(
            f"extract-plugin-manifest-projection --check: STALE — {path} does not match a fresh "
            "extraction from the vendored snapshots. The projection is DERIVED — never hand-edit it. "
            "Regenerate: python3 scripts/extract-plugin-manifest-projection.py --write"
        )
        return 1
    print("extract-plugin-manifest-projection --check: OK — committed projection is fresh.")
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
    label = "extract-plugin-manifest-projection --check-fresh"
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

    fresh = build_projection(vendor_dir, reference_doc_path=snapshot)
    context = (
        f"committed projection vs the captured '{surface}' page "
        f"({os.path.relpath(snapshot, REPO_ROOT)}, standing in for {doc_file})"
    )
    return captured_source.report(captured_source.diff_projections(base, fresh), context, label)


# ── Kernel cross-check (read-only reference; reported, never fixed here) ────
#
# Source: intent-eval-core schemas/authoring/v1/upstream-base/plugin-manifest.v1.json
# (the kernel repo). Embedded as fixtures: the kernel is another repo and this
# check is offline. Kernel edits are OUT OF SCOPE — divergences are findings.

KERNEL_EXPECTATIONS = {
    "source": "intent-eval-core schemas/authoring/v1/upstream-base/plugin-manifest.v1.json",
    "required": ["name"],
    "properties": [
        "author", "commands", "description", "homepage", "keywords",
        "license", "metadata", "name", "repository", "version",
    ],
    "field_types": {
        "author": "object", "commands": "array", "description": "string",
        "homepage": "string", "keywords": "array", "license": "string",
        "name": "string", "repository": "string", "version": "string",
    },
    "author_subfields": ["email", "name", "url"],
    "author_required": ["name"],
    "name_pattern_kebab": True,  # pattern ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$
    "name_max_length": 64,  # kernel-imposed cap; the doc states no length limit
}

# The expected finding sets for the CURRENT capture (plugins-reference.md @
# sha bbb4618e… + 5 claude-plugins-official samples @ eb1510e1). A re-capture
# that shifts either set fails the self-test loud; a human reconciles (and
# only a human ever promotes anything into the kernel).
EXPECTED_AGREEMENTS = [
    "name-only-required-both-sides",
    "field-type:description",
    "field-type:homepage",
    "field-type:keywords",
    "field-type:license",
    "field-type:repository",
    "field-type:version",
    "author-object-shape-name-email-url",
    "name-kebab-case-prose-encoded-as-kernel-pattern",
    "samples-corroborate:no-observed-only-fields",
]
EXPECTED_DIVERGENCES = [
    "component-paths:kernel-models-only-commands;missing:agents,channels,"
    "dependencies,experimental.monitors,experimental.themes,hooks,lspServers,"
    "mcpServers,outputStyles,skills,userConfig",
    "commands-type:kernel-narrows-string|array-to-array",
    "metadata-fields-not-in-kernel:$schema,defaultEnabled,displayName",
    "kernel-only-fields-not-documented-upstream:metadata",
    "name-maxlength:kernel-64-cap-not-documented-upstream",
]


def kernel_cross_check(projection: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Compare the projection against the kernel expectations. Returns
    (agreements, divergences) — both are REPORTED; neither is 'fixed' here."""
    agreements: list[str] = []
    divergences: list[str] = []
    fields = projection["manifest"]["fields"]
    samples = projection["samples"]
    k = KERNEL_EXPECTATIONS

    if projection["manifest"]["name_only_required"] and k["required"] == ["name"]:
        agreements.append("name-only-required-both-sides")
    else:
        divergences.append("required-set:mismatch")

    for field in ("description", "homepage", "keywords", "license", "repository", "version"):
        if fields.get(field, {}).get("type") == k["field_types"][field]:
            agreements.append(f"field-type:{field}")
        else:
            divergences.append(f"field-type:{field}")

    if (
        fields.get("author", {}).get("type") == "object"
        and k["author_subfields"] == ["email", "name", "url"]
        and set(samples["author_subfields_observed"]) <= set(k["author_subfields"])
    ):
        agreements.append("author-object-shape-name-email-url")
    else:
        divergences.append("author-shape:mismatch")

    if projection["manifest"]["name_kebab_case_prose"] and k["name_pattern_kebab"]:
        agreements.append("name-kebab-case-prose-encoded-as-kernel-pattern")

    if not samples["fields_observed_not_documented"]:
        agreements.append("samples-corroborate:no-observed-only-fields")
    else:
        divergences.append(
            "samples:observed-only-fields:" + ",".join(samples["fields_observed_not_documented"])
        )

    component = {f for f, e in fields.items() if e.get("table") == "component-path"}
    missing_component = sorted(component - set(k["properties"]))
    if missing_component:
        kept = sorted(component & set(k["properties"]))
        divergences.append(
            f"component-paths:kernel-models-only-{','.join(kept)};missing:{','.join(missing_component)}"
        )

    if fields.get("commands", {}).get("type") != k["field_types"]["commands"]:
        divergences.append(
            f"commands-type:kernel-narrows-{fields['commands']['type']}-to-{k['field_types']['commands']}"
        )

    metadata_fields = {f for f, e in fields.items() if e.get("table") == "metadata"}
    missing_meta = sorted(metadata_fields - set(k["properties"]))
    if missing_meta:
        divergences.append("metadata-fields-not-in-kernel:" + ",".join(missing_meta))

    kernel_only = sorted(set(k["properties"]) - set(fields))
    if kernel_only:
        divergences.append("kernel-only-fields-not-documented-upstream:" + ",".join(kernel_only))

    if k["name_max_length"] is not None:
        # The doc's tables state no name length cap; the kernel's 64 is an
        # IS structural choice layered on the prose.
        divergences.append(f"name-maxlength:kernel-{k['name_max_length']}-cap-not-documented-upstream")

    return agreements, divergences


# ── Deterministic offline self-test ──────────────────────────────────────────

_FIXTURE_DOC = """# Fixture plugins reference

## Some other section

| Field | Type | Description | Example |
| :---- | :--- | :---------- | :------ |
| `decoy` | string | Must never appear in the projection | `"x"` |

## Plugin manifest schema

The manifest is optional. If omitted, components are auto-discovered.

### Complete schema

```json theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "experimental": { "themes": "./themes/" },
  "exampleOnly": true
}
```

### Required fields

If you include a manifest, `name` is the only required field.

| Field  | Type   | Description                               | Example |
| :----- | :----- | :---------------------------------------- | :------ |
| `name` | string | Unique identifier (kebab-case, no spaces) | `"a-b"` |

### Unrecognized fields

Claude Code ignores top-level fields it does not recognize.

Fields with the wrong type still fail.

### Metadata fields

| Field     | Type   | Description                       | Example |
| :-------- | :----- | :--------------------------------- | :------ |
| `version` | string | Semantic version                  | `"1.0"` |
| `mode`    | string | One of `a`, `b`, or `c`. See docs | `"a"`   |

### Component path fields

| Field                 | Type                  | Description        | Example |
| :-------------------- | :-------------------- | :------------------ | :------ |
| `commands`            | string\\|array         | Custom skill files | `"./c"` |
| `hooks`               | string\\|array\\|object | Hook config        | `"./h"` |
| `experimental.themes` | string\\|array         | Theme dirs         | `"./t"` |

## Next section

Nothing here.
"""

_FIXTURE_SAMPLE_A = {"name": "x", "version": "1.0.0", "author": {"name": "A", "url": "https://a"}}
_FIXTURE_SAMPLE_B = {"name": "y", "keywords": ["k"], "x-custom": "v"}


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
        check("fixture doc: decoy table outside the section excluded", "decoy" not in m["fields"])
        check("fixture doc: name is the only required field", [f for f, e in m["fields"].items() if e["required"] is True] == ["name"])
        check("fixture doc: kebab-case prose detected on name", m["name_kebab_case_prose"] is True)
        check("fixture doc: enum extracted where stated", m["fields"]["mode"].get("enum") == ["a", "b", "c"])
        check("fixture doc: no enum invented where unstated", "enum" not in m["fields"]["version"])
        check("fixture doc: escaped-pipe union type unescaped", m["fields"]["hooks"]["type"] == "string|array|object")
        check("fixture doc: dotted component field parsed", m["fields"]["experimental.themes"]["table"] == "component-path")
        check(
            "fixture doc: example-only field documented via complete-schema-example",
            m["fields"]["exampleOnly"] == {"required": False, "source": "documented", "table": "complete-schema-example", "type": "boolean"},
        )
        check("fixture doc: example experimental expanded dotted", "experimental.themes" in m["complete_schema_example_fields"])
        check("fixture doc: tolerance sentences detected", m["manifest_optional"] and m["unrecognized_top_level_ignored"] and m["wrong_type_fails"])

        sample_paths = []
        for i, sample in enumerate((_FIXTURE_SAMPLE_A, _FIXTURE_SAMPLE_B)):
            p = os.path.join(tmp, f"s{i}.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(sample, fh)
            sample_paths.append(p)
        s = extract_samples(sample_paths)
        check("fixture samples: top-level fields observed", s["top_level_fields_observed"] == ["author", "keywords", "name", "version", "x-custom"])
        check("fixture samples: author subfields collected", s["author_subfields_observed"] == ["name", "url"])
        check("fixture samples: observed types recorded", s["field_types_observed"]["x-custom"] == "string")

        # Doc without the section anchor must hard-fail (exit 2), not silently emit.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write("# no manifest section here\n")
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing section anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing section anchor exits 2", exc.code == 2)

        # Section present but required-sentence anchor missing must also exit 2.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC.replace("If you include a manifest, `name` is the only required field.", ""))
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing required-sentence anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing required-sentence anchor exits 2", exc.code == 2)

    # 2. The committed real projection: fresh (determinism) + sound shape.
    check("committed projection is fresh (--check)", cmd_check(vendor_dir) == 0)
    projection = build_projection(vendor_dir)
    fields = projection["manifest"]["fields"]
    check("real capture: 23 documented fields (1 required + 10 metadata + 12 component-path)", len([f for f, e in fields.items() if e["source"] == "documented"]) == 23)
    check("real capture: every sample field is documented (provenance rule holds)", projection["samples"]["fields_observed_not_documented"] == [])
    check("real capture: no wall-clock keys in projection", "fetched_at" not in render(projection) and "generated" not in render(projection))

    # Staleness must be detectable: a hand-edited copy fails --check.
    with tempfile.TemporaryDirectory() as tmp:
        import shutil

        tmp_vendor = os.path.join(tmp, "plugin-manifest")
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
        print(f"\nself-test: {failures} FAILURE(S) — the plugin-manifest deep-capture projection machinery is not sound.")
        return 1
    print("\nself-test: extraction anchors, freshness/staleness, and kernel cross-check all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic plugin-manifest deep-capture projection (058-AT-SPEC).")
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
    print(f"extract-plugin-manifest-projection: wrote {projection_path(args.vendor_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
