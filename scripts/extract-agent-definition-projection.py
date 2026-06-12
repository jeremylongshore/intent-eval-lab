#!/usr/bin/env python3
"""Deep-capture normative projection for the agent-definition contract (059-AT-SPEC).

The agent-definition contract gets the deep capture skill-frontmatter,
mcp-config, and plugin-manifest already have: a vendored upstream snapshot set
under specs/_vendor/upstream/agent-definition/ plus a deterministic NORMATIVE
PROJECTION (projection.json) extracted from it. The projection is the
field-diff left-hand side for FF#2 on this contract (Kleppmann: diff
projections field-by-field, never raw page bytes).

Like plugin-manifest (and unlike mcp-config): agent-definition has NO
machine-readable upstream schema at all. The authorities (precedence per
specs/upstream-surface-registry.v1.json + 050-AT-SPEC):

  reference-doc   claude-code-sub-agents.md —
                  code.claude.com/docs/en/sub-agents.md, whose "Supported
                  frontmatter fields" table IS the spec, together with the
                  Write-subagent-files YAML example and the "Choose a model"
                  alias bullets.
  supporting-doc  platform-skill-authoring-best-practices.md — supporting
                  authority only; defines NO agent-frontmatter fields, so the
                  extractor does not consume it (vendored for provenance).
  sample-agents   sample-*.agent.md — real agents/*.md files from
                  anthropics/claude-plugins-official (commit-pinned),
                  real-world ground truth that CORROBORATES the doc.

ADDITIONAL DEVIATION from plugin-manifest: the frontmatter table carries
Field|Required|Description columns only — no Type column and no Example
column — so per-field types are NOT documented tabularly; value-shape facts
come from the page's YAML example (e.g. `tools: Read, Glob, Grep` — the
comma-separated string wire form) instead.

Provenance rule (conservative by construction): a field the page documents is
source "documented"; a field used in samples but absent from the page is
source "observed-in-samples" with required "unknown" — never promoted to
"documented". Enum extraction is mechanical and closed-set only: a value
clause ("Accepts …", "Options: …", or "…: `a`, `b`, or `c`.") becomes an enum
ONLY when >=2 backticked tokens remain after removing tokens, commas, "or",
and whitespace leaves nothing — so the model clause's "a full model ID"
latitude keeps model enum-free in the projection (recorded as
model_full_id_latitude instead). No wall-clock in the output — regeneration
is deterministic from the vendored bytes alone.

The self-test additionally cross-checks the committed projection against the
kernel's upstream-base expectations (intent-eval-core
schemas/authoring/v1/upstream-base/agent-definition.v1.json — read-only
reference, embedded here as fixtures because the kernel lives in another repo
and CI is offline). Agreements AND divergences are both printed; divergences
are findings to report, never kernel edits (tier-3 promotion is human,
052-AT-SPEC). The computed finding sets must exactly match the expected sets,
so any re-capture that shifts a finding fails loud and a human reconciles.

Stdlib only. Offline. Exit 0 = ok; 1 = staleness / self-test failure;
2 = usage / parse error.

Usage:
  extract-agent-definition-projection.py --extract     # fresh projection to stdout
  extract-agent-definition-projection.py --write       # (re)write projection.json
  extract-agent-definition-projection.py --check       # fail if committed projection is stale
  extract-agent-definition-projection.py --self-test   # offline fixtures + kernel cross-check
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream", "agent-definition")

PROJECTION_VERSION = "spec-projection/v1"

# Mechanical anchors in the sub-agents doc.
_TABLE_HEADING = "#### Supported frontmatter fields"
_EXAMPLE_HEADING = "### Write subagent files"
_MODEL_HEADING = "### Choose a model"
_REQUIRED_SENTENCE = "Only `name` and `description` are required."
_EXPECTED_COLUMNS = ["Field", "Required", "Description"]
_ALIAS_MARKER = "available aliases: "
_INHERIT_BULLET = "* **inherit**:"
_FENCE_OPEN_MD = re.compile(r"^```(markdown|yaml)\b")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_CELL_SPLIT = re.compile(r"(?<!\\)\|")
_BACKTICK = re.compile(r"`([^`]+)`")
_SET_TO = re.compile(r"^Set to `([^`]+)`")
_FM_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(.*)$")


# ── Extraction: the reference doc (the spec — there is no machine schema) ───


def _section(lines: list[str], heading: str, stop_prefixes: tuple[str, ...]) -> list[str]:
    """Slice the section under `heading` (up to the next same-or-higher heading)."""
    start = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    if start is None:
        print(f"ERROR: {heading!r} anchor not found in the sub-agents doc", file=sys.stderr)
        sys.exit(2)
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith(stop_prefixes)),
        len(lines),
    )
    return lines[start:end]


def _split_row(row: str) -> list[str]:
    """Split a markdown table row on unescaped pipes; unescape cell contents."""
    cells = _CELL_SPLIT.split(row.strip())[1:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


def _table(section: list[str]) -> tuple[list[str], list[list[str]]]:
    """(header, data rows) of the first table in `section`. Data rows are
    exactly the rows whose first cell carries a backticked field name."""
    start = next((i for i, ln in enumerate(section) if ln.lstrip().startswith("| ")), None)
    if start is None:
        print("ERROR: no table found in the frontmatter-fields section", file=sys.stderr)
        sys.exit(2)
    header = _split_row(section[start])
    rows = []
    for ln in section[start:]:
        if not ln.lstrip().startswith("|"):
            break
        cells = _split_row(ln)
        if cells and _BACKTICK.search(cells[0]):
            rows.append(cells)
    if not rows:
        print("ERROR: the frontmatter-fields table has no data rows", file=sys.stderr)
        sys.exit(2)
    return header, rows


def _enum_from_description(desc: str) -> list[str] | None:
    """Closed-set value clause -> enum; open clauses (leftover prose) -> None.

    Clause selection (first match wins): 'Accepts ' to the next '.';
    'Options: ' to the next ';' or '.'; otherwise the first ': ' to the next
    '. '. The clause becomes an enum ONLY when removing backticked tokens,
    commas, 'or', and whitespace leaves nothing AND >=2 tokens remain."""
    for marker, stops in (("Accepts ", "."), ("Options: ", ";."), (": ", ".")):
        idx = desc.find(marker)
        if idx == -1:
            continue
        clause = desc[idx + len(marker) :]
        stop = min((j for j in (clause.find(s) for s in stops) if j != -1), default=-1)
        if stop != -1:
            clause = clause[:stop]
        tokens = _BACKTICK.findall(clause)
        residue = re.sub(r"`[^`]+`", "", clause)
        residue = re.sub(r"\bor\b|,|\s", "", residue)
        if len(tokens) >= 2 and not residue:
            return tokens
        return None
    return None


def _example_frontmatter(section: list[str]) -> dict[str, str]:
    """Top-level frontmatter keys -> raw values of the first fenced markdown
    example in the Write-subagent-files section."""
    start = next((i for i, ln in enumerate(section) if _FENCE_OPEN_MD.match(ln)), None)
    if start is None:
        print("ERROR: no fenced markdown example in the Write-subagent-files section", file=sys.stderr)
        sys.exit(2)
    end = next(i for i in range(start + 1, len(section)) if _FENCE_CLOSE.match(section[i]))
    body = section[start + 1 : end]
    if not body or body[0].strip() != "---":
        print("ERROR: the Write-subagent-files example carries no frontmatter", file=sys.stderr)
        sys.exit(2)
    fields: dict[str, str] = {}
    for ln in body[1:]:
        if ln.strip() == "---":
            break
        m = _FM_KEY.match(ln)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def _model_facts(section: list[str]) -> dict[str, Any]:
    alias_line = next((ln for ln in section if _ALIAS_MARKER in ln), None)
    if alias_line is None:
        print(f"ERROR: {_ALIAS_MARKER!r} anchor not found in the Choose-a-model section", file=sys.stderr)
        sys.exit(2)
    aliases = _BACKTICK.findall(alias_line[alias_line.find(_ALIAS_MARKER) + len(_ALIAS_MARKER) :])
    return {
        "model_aliases_documented": aliases,
        "model_inherit_documented": any(ln.startswith(_INHERIT_BULLET) for ln in section),
    }


def extract_reference_doc(doc_path: str) -> dict[str, Any]:
    with open(doc_path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    table_section = _section(lines, _TABLE_HEADING, ("## ", "### ", "#### "))
    if _REQUIRED_SENTENCE not in "\n".join(table_section):
        print(f"ERROR: required-set anchor {_REQUIRED_SENTENCE!r} not found", file=sys.stderr)
        sys.exit(2)

    header, rows = _table(table_section)
    fields: dict[str, dict[str, Any]] = {}
    name_lowercase_hyphens = False
    model_full_id = False
    model_default_inherit = False
    tools_inherit_all = False
    for cells in rows:
        field = _BACKTICK.search(cells[0]).group(1)
        required_cell = cells[1] if len(cells) > 1 else ""
        desc = cells[2] if len(cells) > 2 else ""
        entry: dict[str, Any] = {
            "required": required_cell == "Yes",
            "source": "documented",
        }
        enum = _enum_from_description(desc)
        if enum:
            entry["enum"] = enum
        set_to = _SET_TO.match(desc)
        if set_to:
            entry["set_to_value"] = set_to.group(1)
        fields[field] = entry
        if field == "name" and "lowercase letters and hyphens" in desc:
            name_lowercase_hyphens = True
        if field == "model":
            model_full_id = "a full model ID" in desc
            model_default_inherit = "Defaults to `inherit`" in desc
        if field == "tools" and "Inherits all tools if omitted" in desc:
            tools_inherit_all = True

    example = _example_frontmatter(_section(lines, _EXAMPLE_HEADING, ("## ", "### ")))
    undocumented_example = sorted(set(example) - set(fields))
    if undocumented_example:
        print(f"ERROR: example frontmatter uses undocumented field(s): {undocumented_example}", file=sys.stderr)
        sys.exit(2)
    tools_in_example = example.get("tools", "")

    facts: dict[str, Any] = {
        "fields": fields,
        "model_default_inherit": model_default_inherit,
        "model_full_id_latitude": model_full_id,
        "name_description_only_required": True,
        "name_lowercase_hyphens_prose": name_lowercase_hyphens,
        "table_columns": header,
        "table_documents_no_types": header == _EXPECTED_COLUMNS,
        "tools_inherit_all_if_omitted": tools_inherit_all,
        "tools_wire_form_in_example": (
            "comma-separated-string" if ", " in tools_in_example and not tools_in_example.startswith("[") else None
        ),
        "write_example_fields": sorted(example),
    }
    facts.update(_model_facts(_section(lines, _MODEL_HEADING, ("## ", "### "))))
    return facts


# ── Extraction: the vendored sample agents (corroboration only) ─────────────


def _sample_frontmatter(path: str) -> dict[str, str]:
    """Top-level frontmatter keys -> raw values of one agents/*.md sample.
    Minimal mechanical parse (stdlib only — no YAML library): top-level
    `key: value` lines between the opening and closing --- markers; indented
    block-scalar continuation lines belong to the preceding key."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0].strip() != "---":
        print(f"ERROR: sample {os.path.basename(path)} carries no frontmatter", file=sys.stderr)
        sys.exit(2)
    fields: dict[str, str] = {}
    for ln in lines[1:]:
        if ln.strip() == "---":
            return fields
        m = _FM_KEY.match(ln)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    print(f"ERROR: sample {os.path.basename(path)} frontmatter is unterminated", file=sys.stderr)
    sys.exit(2)


def _tools_wire_form(raw: str) -> str:
    if raw.startswith("["):
        return "flow-array"
    if ", " in raw:
        return "comma-separated-string"
    return "plain-string"


def extract_samples(sample_paths: list[str]) -> dict[str, Any]:
    observed: set[str] = set()
    tools_forms: set[str] = set()
    model_values: set[str] = set()
    color_values: set[str] = set()
    block_scalar_descriptions = 0
    for path in sample_paths:
        fm = _sample_frontmatter(path)
        observed.update(fm)
        if "tools" in fm:
            tools_forms.add(_tools_wire_form(fm["tools"]))
        if "model" in fm:
            model_values.add(fm["model"])
        if "color" in fm:
            color_values.add(fm["color"])
        if fm.get("description", "") in ("|", ">", ""):
            block_scalar_descriptions += 1
    return {
        "block_scalar_description_count": block_scalar_descriptions,
        "color_values_observed": sorted(color_values),
        "count": len(sample_paths),
        "model_values_observed": sorted(model_values),
        "tools_wire_forms_observed": sorted(tools_forms),
        "top_level_fields_observed": sorted(observed),
    }


# ── The projection ───────────────────────────────────────────────────────────


def load_vendor_meta(vendor_dir: str) -> dict[str, Any]:
    with open(os.path.join(vendor_dir, "vendor-meta.json"), encoding="utf-8") as fh:
        return json.load(fh)


def build_projection(vendor_dir: str) -> dict[str, Any]:
    meta = load_vendor_meta(vendor_dir)
    docs = [f["file"] for f in meta["files"] if f["role"] == "reference-doc"]
    supporting = sorted(f["file"] for f in meta["files"] if f["role"] == "supporting-doc")
    samples = sorted(f["file"] for f in meta["files"] if f["role"] == "sample-agent")
    if len(docs) != 1 or not samples:
        print("ERROR: vendor-meta.json needs exactly one reference-doc and >=1 sample-agent", file=sys.stderr)
        sys.exit(2)

    frontmatter = extract_reference_doc(os.path.join(vendor_dir, docs[0]))
    sample_facts = extract_samples([os.path.join(vendor_dir, s) for s in samples])

    # Cross-corroboration (the provenance rule): documented fields get an
    # observed_in_samples marker; sample-only fields are recorded with
    # source "observed-in-samples" and required "unknown" — NEVER "documented".
    observed = set(sample_facts["top_level_fields_observed"])
    for field, entry in frontmatter["fields"].items():
        entry["observed_in_samples"] = field in observed
    observed_only = sorted(observed - set(frontmatter["fields"]))
    for field in observed_only:
        frontmatter["fields"][field] = {
            "observed_in_samples": True,
            "required": "unknown",
            "source": "observed-in-samples",
        }
    sample_facts["fields_observed_not_documented"] = observed_only
    documented_color_enum = set(frontmatter["fields"].get("color", {}).get("enum") or [])
    sample_facts["color_values_outside_documented_enum"] = sorted(
        set(sample_facts["color_values_observed"]) - documented_color_enum
    )

    return {
        "captured_from": {"reference_doc": docs[0], "samples": samples, "supporting_docs": supporting},
        "contract": "agent-definition",
        "frontmatter": frontmatter,
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
        print(f"extract-agent-definition-projection --check: FAIL — projection missing: {path}")
        return 1
    with open(path, encoding="utf-8") as fh:
        committed = fh.read()
    if committed != fresh:
        print(
            f"extract-agent-definition-projection --check: STALE — {path} does not match a fresh "
            "extraction from the vendored snapshots. The projection is DERIVED — never hand-edit it. "
            "Regenerate: python3 scripts/extract-agent-definition-projection.py --write"
        )
        return 1
    print("extract-agent-definition-projection --check: OK — committed projection is fresh.")
    return 0


# ── Kernel cross-check (read-only reference; reported, never fixed here) ────
#
# Source: intent-eval-core schemas/authoring/v1/upstream-base/agent-definition.v1.json
# (the kernel repo). Embedded as fixtures: the kernel is another repo and this
# check is offline. Kernel edits are OUT OF SCOPE — divergences are findings.

KERNEL_EXPECTATIONS = {
    "source": "intent-eval-core schemas/authoring/v1/upstream-base/agent-definition.v1.json",
    "required": ["description", "name"],
    "properties": ["color", "description", "metadata", "model", "name", "tools"],
    "model_enum": ["fable", "haiku", "inherit", "opus", "sonnet"],
    "color_enum": ["blue", "cyan", "green", "orange", "pink", "purple", "red", "yellow"],
    "tools_type": "array",  # kernel narrows the documented comma-separated string wire form
    "name_pattern_kebab": True,  # pattern ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$
    "name_max_length": 64,  # kernel-imposed cap; the doc states no length limit
}

# The expected finding sets for the CURRENT capture (sub-agents.md @
# sha 82416220… + 5 claude-plugins-official samples @ eb1510e1). A re-capture
# that shifts either set fails the self-test loud; a human reconciles (and
# only a human ever promotes anything into the kernel).
EXPECTED_AGREEMENTS = [
    "name-description-only-required-both-sides",
    "name-lowercase-hyphens-prose-encoded-as-kernel-pattern",
    "color-enum-exact-8-values",
    "model-enum-matches-documented-aliases-plus-inherit",
    "samples-corroborate:no-observed-only-fields",
]
EXPECTED_DIVERGENCES = [
    "doc-fields-not-in-kernel:background,disallowedTools,effort,hooks,"
    "initialPrompt,isolation,maxTurns,mcpServers,memory,permissionMode,skills",
    "kernel-only-fields-not-documented-upstream:metadata",
    "tools-wire-form:kernel-narrows-comma-separated-string-to-array;samples-also-use-flow-array",
    "model-full-id-latitude-not-modeled-in-kernel",
    "name-maxlength:kernel-64-cap-not-documented-upstream",
    "samples:color-outside-documented-enum:magenta",
]


def kernel_cross_check(projection: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Compare the projection against the kernel expectations. Returns
    (agreements, divergences) — both are REPORTED; neither is 'fixed' here."""
    agreements: list[str] = []
    divergences: list[str] = []
    fm = projection["frontmatter"]
    fields = fm["fields"]
    samples = projection["samples"]
    k = KERNEL_EXPECTATIONS

    doc_required = sorted(f for f, e in fields.items() if e.get("required") is True)
    if fm["name_description_only_required"] and doc_required == k["required"]:
        agreements.append("name-description-only-required-both-sides")
    else:
        divergences.append("required-set:mismatch")

    if fm["name_lowercase_hyphens_prose"] and k["name_pattern_kebab"]:
        agreements.append("name-lowercase-hyphens-prose-encoded-as-kernel-pattern")

    if sorted(fields.get("color", {}).get("enum") or []) == k["color_enum"]:
        agreements.append("color-enum-exact-8-values")
    else:
        divergences.append("color-enum:mismatch")

    doc_model_values = sorted(set(fm["model_aliases_documented"]) | ({"inherit"} if fm["model_inherit_documented"] else set()))
    if doc_model_values == k["model_enum"]:
        agreements.append("model-enum-matches-documented-aliases-plus-inherit")
    else:
        divergences.append("model-enum:mismatch")

    if not samples["fields_observed_not_documented"]:
        agreements.append("samples-corroborate:no-observed-only-fields")
    else:
        divergences.append(
            "samples:observed-only-fields:" + ",".join(samples["fields_observed_not_documented"])
        )

    doc_only = sorted(set(fields) - set(k["properties"]))
    if doc_only:
        divergences.append("doc-fields-not-in-kernel:" + ",".join(doc_only))

    kernel_only = sorted(set(k["properties"]) - set(fields))
    if kernel_only:
        divergences.append("kernel-only-fields-not-documented-upstream:" + ",".join(kernel_only))

    if fm["tools_wire_form_in_example"] == "comma-separated-string" and k["tools_type"] == "array":
        suffix = ";samples-also-use-flow-array" if "flow-array" in samples["tools_wire_forms_observed"] else ""
        divergences.append(f"tools-wire-form:kernel-narrows-comma-separated-string-to-array{suffix}")

    if fm["model_full_id_latitude"]:
        # The doc admits a full model ID; the kernel's closed alias enum is an
        # IS narrowing layered on the prose.
        divergences.append("model-full-id-latitude-not-modeled-in-kernel")

    if k["name_max_length"] is not None:
        # The doc states no name length cap; the kernel's 64 is an IS
        # structural choice layered on the prose.
        divergences.append(f"name-maxlength:kernel-{k['name_max_length']}-cap-not-documented-upstream")

    outside = samples["color_values_outside_documented_enum"]
    if outside:
        divergences.append("samples:color-outside-documented-enum:" + ",".join(outside))

    return agreements, divergences


# ── Deterministic offline self-test ──────────────────────────────────────────

_FIXTURE_DOC = """# Fixture sub-agents reference

## Some other section

| Field | Required | Description |
| :---- | :------- | :---------- |
| `decoy` | Yes | Must never appear in the projection |

### Write subagent files

```markdown theme={null}
---
name: code-reviewer
description: Reviews code
tools: Read, Glob, Grep
model: sonnet
---

Body prompt.
```

#### Supported frontmatter fields

The following fields can be used in the YAML frontmatter. Only `name` and `description` are required.

| Field | Required | Description |
| :---- | :------- | :---------- |
| `name` | Yes | Unique identifier using lowercase letters and hyphens. The filename does not have to match |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Tools the subagent can use. Inherits all tools if omitted |
| `model` | No | [Model](#choose-a-model) to use: `sonnet`, `opus`, a full model ID (for example, `claude-opus-4-8`), or `inherit`. Defaults to `inherit` |
| `memory` | No | [Persistent memory scope](#enable-persistent-memory): `user`, `project`, or `local`. Enables cross-session learning |
| `effort` | No | Effort level. Default: inherits from session. Options: `low`, `high`; available levels depend on the model |
| `isolation` | No | Set to `worktree` to run the subagent in a temporary git worktree |
| `color` | No | Display color. Accepts `red`, `blue`, or `cyan`. Shown in the task list |

### Choose a model

* **Model alias**: Use one of the available aliases: `sonnet`, `opus`, `haiku`, or `fable`
* **inherit**: Use the same model as the main conversation

## Next section

Nothing here.
"""

_FIXTURE_SAMPLE_A = "---\nname: a\ndescription: |\n  Multi-line\n  delegation cue\ntools: [\"Read\", \"Grep\"]\ncolor: magenta\n---\nBody.\n"
_FIXTURE_SAMPLE_B = "---\nname: b\ndescription: One-liner\ntools: Read, Glob, Grep\nmodel: inherit\nx-custom: v\n---\nBody.\n"


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
        check(
            "fixture doc: name+description required, rest optional",
            sorted(f for f, e in m["fields"].items() if e["required"] is True) == ["description", "name"],
        )
        check("fixture doc: lowercase-hyphens prose detected on name", m["name_lowercase_hyphens_prose"] is True)
        check("fixture doc: no-Type-column deviation recorded", m["table_documents_no_types"] is True)
        check("fixture doc: closed ': '-list enum extracted (memory)", m["fields"]["memory"].get("enum") == ["user", "project", "local"])
        check("fixture doc: 'Options:' enum stops at semicolon (effort)", m["fields"]["effort"].get("enum") == ["low", "high"])
        check("fixture doc: 'Accepts' enum extracted (color)", m["fields"]["color"].get("enum") == ["red", "blue", "cyan"])
        check("fixture doc: open model clause yields NO enum", "enum" not in m["fields"]["model"])
        check("fixture doc: model full-ID latitude + inherit default detected", m["model_full_id_latitude"] and m["model_default_inherit"])
        check("fixture doc: 'Set to' single value recorded (isolation)", m["fields"]["isolation"].get("set_to_value") == "worktree")
        check("fixture doc: tools inherit-all sentence detected", m["tools_inherit_all_if_omitted"] is True)
        check("fixture doc: example fields parsed", m["write_example_fields"] == ["description", "model", "name", "tools"])
        check("fixture doc: example tools wire form is the comma string", m["tools_wire_form_in_example"] == "comma-separated-string")
        check("fixture doc: model aliases from Choose-a-model bullet", m["model_aliases_documented"] == ["sonnet", "opus", "haiku", "fable"])
        check("fixture doc: inherit bullet detected", m["model_inherit_documented"] is True)

        sample_paths = []
        for i, sample in enumerate((_FIXTURE_SAMPLE_A, _FIXTURE_SAMPLE_B)):
            p = os.path.join(tmp, f"s{i}.agent.md")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(sample)
            sample_paths.append(p)
        s = extract_samples(sample_paths)
        check(
            "fixture samples: top-level fields observed (block-scalar body lines excluded)",
            s["top_level_fields_observed"] == ["color", "description", "model", "name", "tools", "x-custom"],
        )
        check("fixture samples: both tools wire forms observed", s["tools_wire_forms_observed"] == ["comma-separated-string", "flow-array"])
        check("fixture samples: model + color values collected", s["model_values_observed"] == ["inherit"] and s["color_values_observed"] == ["magenta"])
        check("fixture samples: block-scalar description counted", s["block_scalar_description_count"] == 1)

        # Doc without the table-section anchor must hard-fail (exit 2), not silently emit.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write("# no frontmatter section here\n")
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing section anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing section anchor exits 2", exc.code == 2)

        # Section present but required-sentence anchor missing must also exit 2.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC.replace(_REQUIRED_SENTENCE, ""))
        try:
            extract_reference_doc(doc_path)
            check("fixture doc: missing required-sentence anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing required-sentence anchor exits 2", exc.code == 2)

    # 2. The committed real projection: fresh (determinism) + sound shape.
    check("committed projection is fresh (--check)", cmd_check(vendor_dir) == 0)
    projection = build_projection(vendor_dir)
    fields = projection["frontmatter"]["fields"]
    check(
        "real capture: 16 documented fields (2 required + 14 optional)",
        len([f for f, e in fields.items() if e["source"] == "documented"]) == 16
        and len([f for f, e in fields.items() if e.get("required") is True]) == 2,
    )
    check("real capture: every sample field is documented (provenance rule holds)", projection["samples"]["fields_observed_not_documented"] == [])
    check("real capture: no wall-clock keys in projection", "fetched_at" not in render(projection) and "generated" not in render(projection))

    # Staleness must be detectable: a hand-edited copy fails --check.
    with tempfile.TemporaryDirectory() as tmp:
        import shutil

        tmp_vendor = os.path.join(tmp, "agent-definition")
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
        print(f"\nself-test: {failures} FAILURE(S) — the agent-definition deep-capture projection machinery is not sound.")
        return 1
    print("\nself-test: extraction anchors, freshness/staleness, and kernel cross-check all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic agent-definition deep-capture projection (059-AT-SPEC).")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--extract", action="store_true", help="print a fresh projection to stdout")
    mode.add_argument("--write", action="store_true", help="(re)write projection.json")
    mode.add_argument("--check", action="store_true", help="fail if the committed projection is stale")
    mode.add_argument("--self-test", action="store_true", help="offline fixtures + kernel cross-check")
    parser.add_argument("--vendor-dir", default=DEFAULT_VENDOR_DIR, help="vendored capture directory")
    args = parser.parse_args()

    if args.self_test:
        return cmd_self_test(args.vendor_dir)
    if args.check:
        return cmd_check(args.vendor_dir)
    fresh = render(build_projection(args.vendor_dir))
    if args.extract:
        sys.stdout.write(fresh)
        return 0
    with open(projection_path(args.vendor_dir), "w", encoding="utf-8") as fh:
        fh.write(fresh)
    print(f"extract-agent-definition-projection: wrote {projection_path(args.vendor_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
