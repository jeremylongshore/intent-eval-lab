#!/usr/bin/env python3
"""Deep-capture normative projection for the mcp-config contract (056-AT-SPEC).

The mcp-config contract gets the deep capture skill-frontmatter already has
(_vendor/upstream/skill-frontmatter/): a vendored upstream snapshot pair under
specs/_vendor/upstream/mcp-config/ plus a deterministic NORMATIVE PROJECTION
(projection.json) extracted from it. The projection is the field-diff
left-hand side for FF#2 on this contract (Kleppmann: diff projections
field-by-field, never raw page bytes).

MCP is the first contract whose primary upstream surface is truly
machine-readable — github.com/modelcontextprotocol/modelcontextprotocol
publishes schema/<version>/schema.json. The capture pairs two authorities
(precedence per specs/upstream-surface-registry.v1.json):

  machine-schema    mcp-schema-2025-11-25.json — the official protocol schema
                    for the CURRENT spec revision. Load-bearing negative fact:
                    it defines NO transport enum and NO server-config keys
                    (command/args/env). The extractor records that absence
                    explicitly instead of papering over it.
  claude-code-doc   claude-code-mcp.md — code.claude.com/docs/en/mcp.md, the
                    authority for the `.mcp.json` per-server config shape the
                    kernel's mcp-config contract projects (the "standardized
                    format" block + the transport sections).

Everything extracted is mechanical: JSON parsed from the schema, and the
fenced standardized-format block / `--transport X` / `"type": "X"` / alias /
deprecation sentences regexed from the doc. No wall-clock in the output —
regeneration is deterministic from the vendored bytes alone.

The self-test additionally cross-checks the committed projection against the
kernel's upstream-base expectations (intent-eval-core
schemas/authoring/v1/upstream-base/mcp-config.v1.json — read-only reference,
embedded here as fixtures because the kernel lives in another repo and CI is
offline). Agreements AND divergences are both printed; divergences are
findings to report, never kernel edits (tier-3 promotion is human,
052-AT-SPEC). The computed finding sets must exactly match the expected sets,
so any re-capture that shifts a finding fails loud and a human reconciles.

Stdlib only. Offline. Exit 0 = ok; 1 = staleness / self-test failure;
2 = usage / parse error.

Usage:
  extract-mcp-projection.py --extract           # fresh projection to stdout
  extract-mcp-projection.py --write             # (re)write projection.json
  extract-mcp-projection.py --check             # fail if committed projection is stale
  extract-mcp-projection.py --self-test         # offline fixtures + kernel cross-check
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
DEFAULT_VENDOR_DIR = os.path.join(REPO_ROOT, "specs", "_vendor", "upstream", "mcp-config")

PROJECTION_VERSION = "spec-projection/v1"

# Mechanical anchors in the Claude Code MCP doc.
_STANDARDIZED_SENTENCE = "follows a standardized format:"
_FENCE_OPEN = re.compile(r"^```json\b")
_FENCE_CLOSE = re.compile(r"^```\s*$")
_CLI_TRANSPORT = re.compile(r"--transport ([a-z][a-z-]*)")
_JSON_TYPE = re.compile(r"\"type\"\s*:\s*\"([a-z][a-z-]*)\"")
_ALIAS = re.compile(r"`([a-z-]+)` as an alias for `([a-z-]+)`")
_DEPRECATED = re.compile(r"The ([A-Za-z]+) \([^)]*\) transport is deprecated", re.IGNORECASE)


def _json_type_name(value: Any) -> str:
    return {dict: "object", list: "array", str: "string", bool: "boolean", int: "number", float: "number", type(None): "null"}[type(value)]


# ── Extraction: machine schema (the official MCP schema.json) ───────────────


def extract_machine_schema(schema_path: str) -> dict[str, Any]:
    with open(schema_path, encoding="utf-8") as fh:
        schema = json.load(fh)
    defs = schema.get("$defs") or schema.get("definitions") or {}

    # Server-config absence is a load-bearing fact: any definition carrying the
    # command/args/env triple, or named like a transport, would flip these.
    server_config_defs = sorted(
        name
        for name, d in defs.items()
        if isinstance(d.get("properties"), dict) and {"command", "args", "env"} <= set(d["properties"])
    )
    transport_defs = sorted(name for name in defs if re.search("transport", name, re.IGNORECASE))

    implementation: dict[str, Any] | None = None
    if "Implementation" in defs:
        impl = defs["Implementation"]
        implementation = {
            "required": sorted(impl.get("required", [])),
            "properties": {
                name: prop.get("type", "ref" if "$ref" in prop else "unknown")
                for name, prop in impl.get("properties", {}).items()
            },
        }

    return {
        "defs_count": len(defs),
        "defines_server_config": bool(server_config_defs),
        "server_config_defs": server_config_defs,
        "transport_defs": transport_defs,
        "implementation": implementation,
    }


# ── Extraction: Claude Code MCP doc (the `.mcp.json` authority) ─────────────


def _standardized_format_block(lines: list[str]) -> dict[str, Any]:
    """Parse the fenced JSON block that follows the 'standardized format' sentence."""
    anchor = next((i for i, ln in enumerate(lines) if _STANDARDIZED_SENTENCE in ln), None)
    if anchor is None:
        print("ERROR: 'standardized format' anchor not found in the Claude Code MCP doc", file=sys.stderr)
        sys.exit(2)
    start = next((i for i in range(anchor, len(lines)) if _FENCE_OPEN.match(lines[i])), None)
    if start is None:
        print("ERROR: no fenced json block after the standardized-format anchor", file=sys.stderr)
        sys.exit(2)
    end = next(i for i in range(start + 1, len(lines)) if _FENCE_CLOSE.match(lines[i]))
    return json.loads("\n".join(lines[start + 1 : end]))


def extract_claude_code_doc(doc_path: str) -> dict[str, Any]:
    with open(doc_path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    block = _standardized_format_block(lines)
    servers = block.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        print("ERROR: standardized-format block has no mcpServers map", file=sys.stderr)
        sys.exit(2)
    entry = next(iter(servers.values()))
    fields = {key: _json_type_name(value) for key, value in entry.items()}

    aliases = {alias: target for alias, target in _ALIAS.findall(text)}
    tokens = set(_CLI_TRANSPORT.findall(text)) | set(_JSON_TYPE.findall(text))
    transport_types = sorted(tokens - set(aliases))
    deprecated = sorted({m.lower() for m in _DEPRECATED.findall(text)} & set(transport_types))

    return {
        "name_is_map_key": True,  # mcpServers keys server entries by name
        "standardized_format_fields": dict(sorted(fields.items())),
        "transport_field": "type",
        "transport_field_in_standardized_format": "type" in entry,
        "transport_types": transport_types,
        "transport_aliases": dict(sorted(aliases.items())),
        "transports_deprecated": deprecated,
    }


# ── The projection ───────────────────────────────────────────────────────────


def load_vendor_meta(vendor_dir: str) -> dict[str, Any]:
    with open(os.path.join(vendor_dir, "vendor-meta.json"), encoding="utf-8") as fh:
        return json.load(fh)


def build_projection(vendor_dir: str) -> dict[str, Any]:
    meta = load_vendor_meta(vendor_dir)
    by_role = {f["role"]: f["file"] for f in meta["files"]}
    for role in ("machine-schema", "claude-code-doc"):
        if role not in by_role:
            print(f"ERROR: vendor-meta.json has no file with role {role!r}", file=sys.stderr)
            sys.exit(2)
    return {
        "projection_version": PROJECTION_VERSION,
        "contract": "mcp-config",
        "spec_version": meta["spec_version"],
        "captured_from": {
            "machine_schema": by_role["machine-schema"],
            "claude_code_doc": by_role["claude-code-doc"],
        },
        "machine_schema": extract_machine_schema(os.path.join(vendor_dir, by_role["machine-schema"])),
        "server_config": extract_claude_code_doc(os.path.join(vendor_dir, by_role["claude-code-doc"])),
    }


def render(projection: dict[str, Any]) -> str:
    return json.dumps(projection, indent=2, sort_keys=True) + "\n"


def projection_path(vendor_dir: str) -> str:
    return os.path.join(vendor_dir, "projection.json")


def cmd_check(vendor_dir: str) -> int:
    fresh = render(build_projection(vendor_dir))
    path = projection_path(vendor_dir)
    if not os.path.exists(path):
        print(f"extract-mcp-projection --check: FAIL — projection missing: {path}")
        return 1
    with open(path, encoding="utf-8") as fh:
        committed = fh.read()
    if committed != fresh:
        print(
            f"extract-mcp-projection --check: STALE — {path} does not match a fresh extraction "
            "from the vendored snapshots. The projection is DERIVED — never hand-edit it. "
            "Regenerate: python3 scripts/extract-mcp-projection.py --write"
        )
        return 1
    print("extract-mcp-projection --check: OK — committed projection is fresh.")
    return 0


# ── Kernel cross-check (read-only reference; reported, never fixed here) ────
#
# Source: intent-eval-core schemas/authoring/v1/upstream-base/mcp-config.v1.json
# (the kernel repo). Embedded as fixtures: the kernel is another repo and this
# check is offline. Kernel edits are OUT OF SCOPE — divergences are findings.

KERNEL_EXPECTATIONS = {
    "source": "intent-eval-core schemas/authoring/v1/upstream-base/mcp-config.v1.json",
    "required": ["args", "command", "env", "name", "transport"],
    "optional": ["metadata"],
    "field_types": {"args": "array", "command": "string", "env": "object", "metadata": "object", "name": "string"},
    "transport_field": "transport",
    "transport_enum": ["stdio", "http", "sse", "ws"],
    "marks_sse_deprecated": True,  # per the kernel $comment "SSE (deprecated)"
}

# The expected finding sets for the CURRENT capture (2025-11-25 schema +
# claude-code-mcp.md @ sha 9006b0bb…). A re-capture that shifts either set
# fails the self-test loud; a human reconciles (and only a human ever
# promotes anything into the kernel).
EXPECTED_AGREEMENTS = [
    "transport-enum-membership",
    "field-type:args",
    "field-type:command",
    "field-type:env",
    "name-lifted-from-map-key",
    "sse-deprecated-both-sides",
]
EXPECTED_DIVERGENCES = [
    "required-set:transport-not-in-upstream-standardized-format",
    "selector-name:kernel-transport-vs-upstream-type",
    "alias:streamable-http-accepted-upstream-not-in-kernel-enum",
    "provenance:machine-schema-defines-no-transport-enum-or-server-config",
]


def kernel_cross_check(projection: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Compare the projection against the kernel expectations. Returns
    (agreements, divergences) — both are REPORTED; neither is 'fixed' here."""
    agreements: list[str] = []
    divergences: list[str] = []
    sc = projection["server_config"]
    ms = projection["machine_schema"]
    k = KERNEL_EXPECTATIONS

    upstream_transports = set(sc["transport_types"]) | set(sc["transport_aliases"].values())
    if set(k["transport_enum"]) <= upstream_transports:
        agreements.append("transport-enum-membership")
    else:
        divergences.append(
            f"transport-enum-membership:kernel-members-missing-upstream:{sorted(set(k['transport_enum']) - upstream_transports)}"
        )

    for field in ("args", "command", "env"):
        if sc["standardized_format_fields"].get(field) == k["field_types"][field]:
            agreements.append(f"field-type:{field}")
        else:
            divergences.append(f"field-type:{field}")

    if sc["name_is_map_key"]:
        # The kernel lifts the mcpServers map key into a `name` field for the
        # one-server-per-document contract shape — documented in its $comment.
        agreements.append("name-lifted-from-map-key")

    if "sse" in sc["transports_deprecated"] and k["marks_sse_deprecated"]:
        agreements.append("sse-deprecated-both-sides")

    if k["transport_field"] in k["required"] and not sc["transport_field_in_standardized_format"]:
        divergences.append("required-set:transport-not-in-upstream-standardized-format")
    if k["transport_field"] != sc["transport_field"]:
        divergences.append("selector-name:kernel-transport-vs-upstream-type")
    for alias in sc["transport_aliases"]:
        if alias not in k["transport_enum"]:
            divergences.append(f"alias:{alias}-accepted-upstream-not-in-kernel-enum")
    if not ms["defines_server_config"] and not ms["transport_defs"]:
        divergences.append("provenance:machine-schema-defines-no-transport-enum-or-server-config")

    return agreements, divergences


# ── Deterministic offline self-test ──────────────────────────────────────────

_FIXTURE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$defs": {
        "Implementation": {
            "required": ["name", "version"],
            "properties": {"name": {"type": "string"}, "version": {"type": "string"}, "icons": {"type": "array"}},
        },
        "SomethingElse": {"properties": {"x": {"type": "string"}}},
    },
}

_FIXTURE_DOC = """# Fixture MCP doc

The SSE (Server-Sent Events) transport is deprecated. Use HTTP instead.

the `type` field accepts `streamable-http` as an alias for `http`.

```bash
claude mcp add --transport http <name> <url>
claude mcp add --transport sse <name> <url>
claude mcp add --transport stdio <name> -- cmd
```

Configure WebSocket servers: '{"type":"ws","url":"wss://x"}'

The resulting `.mcp.json` file follows a standardized format:

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```
"""


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
        schema_path = os.path.join(tmp, "schema.json")
        doc_path = os.path.join(tmp, "doc.md")
        with open(schema_path, "w", encoding="utf-8") as fh:
            json.dump(_FIXTURE_SCHEMA, fh)
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write(_FIXTURE_DOC)

        ms = extract_machine_schema(schema_path)
        check("fixture schema: defines_server_config is False", ms["defines_server_config"] is False)
        check("fixture schema: no transport defs", ms["transport_defs"] == [])
        check("fixture schema: Implementation required parsed", ms["implementation"]["required"] == ["name", "version"])

        # A schema that DOES define the server-config triple must flip the flag.
        with open(schema_path, "w", encoding="utf-8") as fh:
            json.dump(
                {"$defs": {"McpServerConfig": {"properties": {"command": {}, "args": {}, "env": {}}}}}, fh
            )
        ms2 = extract_machine_schema(schema_path)
        check(
            "fixture schema: command/args/env triple flips defines_server_config",
            ms2["defines_server_config"] is True and ms2["server_config_defs"] == ["McpServerConfig"],
        )

        sc = extract_claude_code_doc(doc_path)
        check("fixture doc: standardized-format fields", sc["standardized_format_fields"] == {"args": "array", "command": "string", "env": "object"})
        check("fixture doc: transport types (alias excluded)", sc["transport_types"] == ["http", "sse", "stdio", "ws"])
        check("fixture doc: streamable-http alias mapped", sc["transport_aliases"] == {"streamable-http": "http"})
        check("fixture doc: sse deprecation detected", sc["transports_deprecated"] == ["sse"])
        check("fixture doc: type absent from standardized format", sc["transport_field_in_standardized_format"] is False)

        # Doc without the anchor must hard-fail (exit 2), not silently emit.
        with open(doc_path, "w", encoding="utf-8") as fh:
            fh.write("# no anchor here\n")
        try:
            extract_claude_code_doc(doc_path)
            check("fixture doc: missing anchor exits 2", False)
        except SystemExit as exc:
            check("fixture doc: missing anchor exits 2", exc.code == 2)

    # 2. The committed real projection: fresh (determinism) + sound shape.
    check("committed projection is fresh (--check)", cmd_check(vendor_dir) == 0)
    projection = build_projection(vendor_dir)
    check("real capture: machine schema defines no server config", projection["machine_schema"]["defines_server_config"] is False)
    check("real capture: no wall-clock keys in projection", "fetched_at" not in render(projection) and "generated" not in render(projection))

    # Staleness must be detectable: a hand-edited copy fails --check.
    with tempfile.TemporaryDirectory() as tmp:
        import shutil

        tmp_vendor = os.path.join(tmp, "mcp-config")
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
        print(f"\nself-test: {failures} FAILURE(S) — the mcp deep-capture projection machinery is not sound.")
        return 1
    print("\nself-test: extraction anchors, freshness/staleness, and kernel cross-check all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic mcp-config deep-capture projection (056-AT-SPEC).")
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
    print(f"extract-mcp-projection: wrote {projection_path(args.vendor_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
