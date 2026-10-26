"""Synthetic reference-layout contracts; no downloaded documentation is vendored."""

import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "extract-marketplace-catalog-projection.py"
SPEC = importlib.util.spec_from_file_location("marketplace_layout", PATH)
parser = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parser)


def table(rows):
    return (
        "| Field | Type | Description |\n| :- | :- | :- |\n"
        + "\n".join(f"| {name} | {kind} | {description} |" for name, kind, description in rows)
        + "\n"
    )


def reference():
    # Independently authored prose with the exact structural anchors, deliberately
    # different field values/ordering from the private current-source observation.
    doc = """# Fixture marketplace reference
## Marketplace file
### Reserved names
* **Official marketplace names**: `fixture-official`. Reserved under a source condition.
* **Community marketplace names**: `fixture-community`. Reserved under that condition.
* **Plugin directory names**: `fixture-directory`. Reserved under that condition.
* **Names beginning with fixture-**: conditional on origin.
## Top-level fields
`name`, `owner`, and `plugins` are required.
"""
    doc += table(
        [
            ("`plugins`", "array", "Plugin entries."),
            ("`owner`", "object", "`name` is required; `email` and `url` are optional."),
            ("`name`", "string", "Catalog identity."),
            ("`description`", "string", "Summary."),
            ("`version`", "string", "Catalog revision."),
            ("`metadata.description`, `metadata.version`", "string", "Alternate location for fields."),
            ("`metadata.pluginRoot`", "string", "Bare-name resolution root."),
            ("`forceRemoveDeletedPlugins`", "boolean", "Removal switch."),
            ("`allowCrossMarketplaceDependenciesOn`", "array of strings", "Dependency boundary."),
            ("`renames`", "object", "Rename map."),
            ("`$schema`", "string", "Editor-only."),
        ]
    )
    doc += """## Plugin entries
`name` and `source` are required.
Apart from the [directory listing fields](fixture), an entry also accepts every [`plugin.json` field](fixture).
"""
    doc += table(
        [
            (f"`{name}`", kind, "Fixture field.")
            for name, kind in [
                ("name", "string"),
                ("source", "string or object"),
                ("description", "string"),
                ("version", "string"),
                ("category", "string"),
                ("tags", "array of strings"),
                ("strict", "boolean"),
                ("relevance", "object"),
                ("dependencies", "array"),
                ("defaultEnabled", "boolean"),
                ("displayName", "string"),
                ("metadata", "object"),
                ("headers", "object"),
                ("headersHelper", "string"),
            ]
        ]
    )
    doc += """### Strict mode
`strict: true`, the default, combines manifests subject to the following conditions.
| `strict` | `plugin.json` | Entry component fields | Result |
| :- | :- | :- | :- |
| any | absent | any | Use entry. |
| `true`, the default | present | any | Append except hooks. |
| `false` | present | none | Use manifest. |
| `false` | present | one or more | Refuse conflict. |
## Plugin sources
| Type | Fields | Notes |
| :- | :- | :- |
| Relative path | the string itself | Use `./`, or bare names under `metadata.pluginRoot`; `"."` is the root. |
"""
    sources = {
        "github": ["repo", "ref", "sha"],
        "url": ["url", "ref", "sha"],
        "git-subdir": ["url", "path", "ref", "sha"],
        "npm": ["package", "version", "registry"],
        "archive": ["url", "sha256"],
        "command": ["command", "timeout", "mode"],
    }
    for name, fields in sources.items():
        doc += f"| `{name}` | " + ", ".join(f"`{f}`" for f in fields) + " | Fixture source. |\n"
    doc += """When pinned, Claude Code checks out `sha`.
### Relative path plugin source
```json
{"name":"fixture", "source":"./fixture"}
```
"""
    for name in sources:
        doc += f"### {name} plugin source\n"
        if name == "github":
            doc += "`repo` identifies a repository. `ref` and `sha` are optional.\n"
        doc += "Fixture source rules, separate from settings sources.\n"
        doc += '```json\n{"source":{"source":"' + name + '"}}\n```\n'
    doc += """## Marketplace sources
| Type | Fields | Notes |
| :- | :- | :- |
| `git` | `path`, `sparsePaths` | A settings source, not a plugin source. |
"""
    return doc


def extract(tmp_path, text):
    path = tmp_path / "reference.md"
    path.write_text(text)
    return parser.extract_reference_doc(str(path))


def test_complete_current_inventory_and_no_invented_requiredness(tmp_path):
    result = extract(tmp_path, reference())
    top = result["catalog"]["top_level_fields"]
    assert len(top) == 12
    assert {name for name, value in top.items() if value["required"]} == {"name", "owner", "plugins"}
    assert top["metadata.description"]["type"] == "string"
    assert top["metadata.version"]["type"] == "string"
    assert set(result["owner_fields"]) == {"name", "email", "url"}
    assert result["owner_fields"]["name"]["type"] is None
    assert len(result["plugin_entry"]["fields"]) == 14
    assert result["plugin_entry"]["manifest_passthrough_documented"] is True
    assert len(result["plugin_entry"]["strict_cases"]) == 4
    assert result["plugin_entry"]["strict_cases"][-1] == {
        "`strict`": "`false`",
        "`plugin.json`": "present",
        "Entry component fields": "one or more",
        "Result": "Refuse conflict.",
    }
    assert result["plugin_entry"]["strict_default"] == "true"
    assert "pluginRoot" in result["sources"]["relative_path"]["alternatives_description"]
    assert len(result["catalog"]["reserved_name_rules"]) == 4
    objects = result["sources"]["object_types"]
    assert set(objects) == {"github", "url", "git-subdir", "npm", "archive", "command"}
    assert objects["github"]["optional"] == ["ref", "sha"]
    assert objects["npm"]["requiredness_unspecified"] == ["package", "registry", "version"]
    assert objects["command"]["documented_fields"] == ["command", "mode", "timeout"]
    assert "git" not in objects
    assert "sparsePaths" not in str(objects)
    assert result == extract(tmp_path, reference())


@pytest.mark.parametrize(
    "before,after",
    [
        ("`name`, `owner`, and `plugins` are required.", "No required set."),
        ("`name` and `source` are required.", "No required set."),
        ("| `plugins` | array | Plugin entries. |", ""),
        ("| `renames` | object | Rename map. |", "| `name` | object | Duplicate. |"),
        ("`strict: true`, the default", "An unspecified default"),
        ("| `false` | present | none | Use manifest. |", ""),
        ("### npm plugin source", "### Package source guide"),
        ('{"source":{"source":"npm"}}', '{"source":{"source":"url"}}'),
        ("`ref` and `sha` are optional.", "No optionality statement."),
        ("When pinned, Claude Code checks out `sha`.", "No pin precedence."),
        ('; `"."` is the root.', "."),
        ("## Marketplace sources", "## Setup guide"),
        ("## Top-level fields", "## Top-level fields\n## Top-level fields"),
        ("# Fixture marketplace reference", "# Fixture marketplace reference\n## Marketplace schema"),
        ("| Field | Type | Description |", "| Field | Details |"),
    ],
)
def test_missing_or_ambiguous_normative_facts_refuse(tmp_path, before, after):
    text = reference()
    assert before in text
    with pytest.raises(SystemExit) as exc:
        extract(tmp_path, text.replace(before, after))
    assert exc.value.code == 2


def test_guide_is_not_a_normative_reference(tmp_path):
    with pytest.raises(SystemExit) as exc:
        extract(tmp_path, "# Create a marketplace\n## Plugin entries\nSome examples.\n")
    assert exc.value.code == 2


def test_fenced_prose_cannot_rescue_a_missing_normative_anchor(tmp_path):
    text = reference().replace("`name` and `source` are required.", "```text\n`name` and `source` are required.\n```")
    with pytest.raises(SystemExit) as exc:
        extract(tmp_path, text)
    assert exc.value.code == 2
