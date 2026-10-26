"""Current heading aliases must retain field extraction and fail on ambiguity."""

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load_agent():
    spec = importlib.util.spec_from_file_location(
        "agent_reference", ROOT / "scripts/extract-agent-definition-projection.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_agent_current_heading_extracts_the_same_required_fields(tmp_path):
    module = load_agent()
    historical = module._FIXTURE_DOC
    current = historical.replace(module._TABLE_HEADING, "### Frontmatter reference")
    path = tmp_path / "agent.md"
    path.write_text(historical)
    expected = module.extract_reference_doc(str(path))
    path.write_text(current)
    assert module.extract_reference_doc(str(path)) == expected


def test_agent_ambiguous_reference_headings_are_not_silently_selected(tmp_path):
    module = load_agent()
    path = tmp_path / "agent.md"
    path.write_text(module._FIXTURE_DOC + "\n### Frontmatter reference\n")
    with pytest.raises(SystemExit) as error:
        module.extract_reference_doc(str(path))
    assert error.value.code == 2


def test_agent_current_heading_still_requires_normative_required_set(tmp_path):
    module = load_agent()
    path = tmp_path / "agent.md"
    path.write_text(
        module._FIXTURE_DOC.replace(module._TABLE_HEADING, "### Frontmatter reference").replace(
            module._REQUIRED_SENTENCE, ""
        )
    )
    with pytest.raises(SystemExit) as error:
        module.extract_reference_doc(str(path))
    assert error.value.code == 2


def test_agent_heading_quoted_in_a_code_fence_is_not_a_second_reference(tmp_path):
    module = load_agent()
    path = tmp_path / "agent.md"
    path.write_text(module._FIXTURE_DOC)
    expected = module.extract_reference_doc(str(path))
    path.write_text("```markdown\n### Frontmatter reference\n```\n" + module._FIXTURE_DOC)
    assert module.extract_reference_doc(str(path)) == expected


@pytest.mark.parametrize("fenced", ["required-set", "table"])
def test_agent_fenced_examples_cannot_replace_normative_facts(tmp_path, fenced):
    module = load_agent()
    text = module._FIXTURE_DOC.replace(module._TABLE_HEADING, "### Frontmatter reference")
    if fenced == "required-set":
        text = text.replace(module._REQUIRED_SENTENCE, f"```text\n{module._REQUIRED_SENTENCE}\n```")
    else:
        before, section = text.split("### Frontmatter reference", 1)
        section, count = re.subn(r"(?m)(^\| Field[^\n]*\n(?:^\|[^\n]*\n)+)", r"```text\n\1```\n", section, count=1)
        assert count == 1
        text = before + "### Frontmatter reference" + section
    path = tmp_path / "agent.md"
    path.write_text(text)
    with pytest.raises(SystemExit) as error:
        module.extract_reference_doc(str(path))
    assert error.value.code == 2


PLUGIN_CURRENT = """# Synthetic current manifest reference
## Manifest file
The manifest is optional.
An unrecognized top-level key is stripped.
Validation fails if the manifest has a type mismatch.
```json
{"name": "example", "commands": {"demo": {"content": "Example"}}}
```
## Fields
`name` is the only required key.
| Field | Type | Description |
| :- | :- | :- |
| [`name`](#name) | String | Identifier; use kebab-case. |
| `commands` | Path, array of paths, or object | Commands. |
| `author` | Object | Maintainer. |
## Component path forms
"""


def load_plugin():
    spec = importlib.util.spec_from_file_location(
        "plugin_reference", ROOT / "scripts/extract-plugin-manifest-projection.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("contract", ["agent", "plugin"])
@pytest.mark.parametrize("declaration", ["`version` is also required.", "`name` is not required."])
def test_required_set_rejects_contradictory_same_line_clauses(tmp_path, contract, declaration):
    module = load_agent() if contract == "agent" else load_plugin()
    original = module._FIXTURE_DOC if contract == "agent" else PLUGIN_CURRENT
    anchor = module._REQUIRED_SENTENCE if contract == "agent" else "`name` is the only required key."
    path = tmp_path / "contradiction.md"
    path.write_text(original.replace(anchor, anchor + " " + declaration))
    with pytest.raises(SystemExit) as exc:
        module.extract_reference_doc(str(path))
    assert exc.value.code == 2


@pytest.mark.parametrize("contract", ["agent", "plugin"])
def test_tilde_fences_cannot_supply_required_set(tmp_path, contract):
    module = load_agent() if contract == "agent" else load_plugin()
    original = module._FIXTURE_DOC if contract == "agent" else PLUGIN_CURRENT
    anchor = module._REQUIRED_SENTENCE if contract == "agent" else "`name` is the only required key."
    path = tmp_path / "quoted.md"
    path.write_text(original.replace(anchor, "~~~text\n" + anchor + "\n~~~"))
    with pytest.raises(SystemExit) as exc:
        module.extract_reference_doc(str(path))
    assert exc.value.code == 2


@pytest.mark.parametrize(
    "lines,expected",
    [
        (["~~~~text", "### Hidden", "~~~", "### Still hidden", "~~~~", "### Visible"], [True] * 5 + [False]),
        (["````markdown", "~~~", "```", "### Hidden", "`````", "### Visible"], [True] * 5 + [False]),
        (["  ~~~text", "### Hidden", "   ~~~", "### Visible"], [True, True, True, False]),
        (["~~~", "### Hidden"], [True, True]),
        (["```tag`invalid", "### Visible"], [False, False]),
        (["~~~", "```", "### Hidden", "~~~", "### Visible"], [True, True, True, True, False]),
    ],
)
def test_fence_delimiters_do_not_expose_quoted_normative_headings(lines, expected):
    module = load_agent()
    assert module.reference_markdown.fence_mask(lines) == expected


def test_plugin_unified_table_preserves_all_documented_types(tmp_path):
    module = load_plugin()
    path = tmp_path / "plugin.md"
    path.write_text(PLUGIN_CURRENT)
    result = module.extract_reference_doc(str(path))
    assert set(result["fields"]) == {"name", "commands", "author"}
    assert result["fields"]["commands"]["type"] == "Path, array of paths, or object"
    assert {k for k, v in result["fields"].items() if v["required"]} == {"name"}
    assert result["manifest_example_fields"] == ["commands", "name"]
    assert result["complete_schema_example_fields"] == []
    assert result["manifest_optional"] and result["wrong_type_fails"]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda text: text.replace("`name` is the only required key.", ""),
        lambda text: text.replace("| [`name`](#name) | String | Identifier; use kebab-case. |", ""),
        lambda text: text.replace("## Fields", "## Renamed unknown fields"),
        lambda text: text + "\n## Fields\n",
        lambda text: text + "\n## Plugin manifest schema\n",
        lambda text: text.replace(
            "| `author` | Object | Maintainer. |",
            "| `author` | Object | Maintainer. |\n| `author` | String | Duplicate. |",
        ),
        lambda text: text.replace("The manifest is optional.", ""),
        lambda text: text.replace("The manifest is optional.", "```text\nThe manifest is optional.\n```"),
        lambda text: text.replace("`name` is the only required key.", "```text\n`name` is the only required key.\n```"),
        lambda text: text.replace("| Field | Type | Description |", "```text\n| Field | Type | Description |").replace(
            "## Component path forms", "```\n## Component path forms"
        ),
        lambda text: text.replace("| Field | Type | Description |", "| Field | Description | Type |"),
        lambda text: text.replace("| `author` | Object | Maintainer. |", "| author | Object | Maintainer. |"),
        lambda text: text.replace('"name": "example"', '"newUndocumentedField": "example"'),
    ],
)
def test_plugin_missing_or_ambiguous_normative_input_refuses(tmp_path, mutation):
    module = load_plugin()
    path = tmp_path / "plugin.md"
    path.write_text(mutation(PLUGIN_CURRENT))
    with pytest.raises(SystemExit) as error:
        module.extract_reference_doc(str(path))
    assert error.value.code == 2


def test_registry_targets_normative_plugin_references_and_refuses_guide_title():
    import json
    import re

    registry = json.loads((ROOT / "specs/upstream-surface-registry.v1.json").read_text())
    rows = {r["name"]: r for r in registry["surfaces"]}
    for identity, suffix, current_title, old_title in (
        ("plugins-reference", "plugins/manifest-reference.md", "Plugin manifest reference", "Plugins reference"),
        (
            "plugin-marketplaces",
            "plugins/marketplace-reference.md",
            "Marketplace reference",
            "Create and distribute a plugin marketplace",
        ),
    ):
        row = rows[identity]
        assert row["url"].endswith(suffix)
        assert row["capture"]["urls"] == [row["url"]]
        assert re.fullmatch(row["capture"]["expect_title"], current_title)
        assert re.fullmatch(row["capture"]["expect_title"], old_title)
    assert not re.fullmatch(rows["plugin-marketplaces"]["capture"]["expect_title"], "Create a marketplace")
