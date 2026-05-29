#!/usr/bin/env python3
"""score-fixture.py — wrap validate-skills-schema.py and emit expected.json.

Usage:
    score-fixture.py <SKILL.md path> [--validator-path PATH] [--commit SHA]

Emits JSON to stdout matching DESIGN.md § 5.1 expected.json schema:

    {
      "fixture_sha": "sha256(input.md)",
      "validator_version": "3.7.0",
      "validator_commit": "<sha>",
      "tiers": {
        "standard":    { "pass": true,  "score_pct": 100, "findings": [] },
        "marketplace": { "pass": false, "score_pct": 82,  "findings": [...] },
      },
      "field_completeness": <int 0-8>,
      "deprecated_field_count": <int>,
      "security_finding_count": <int>,
      "is_extras_present": <int 0-11>
    }

Runs the validator twice: once at --standard tier, once at --marketplace tier.
Parses WARN/INFO lines and the GRADE: X (N/100) summary line. Does NOT honor
--deep — deep-eval costs compute; expected.json captures the marketplace verdict
that Phase A.0 + SAK ackp fixtures gate on.

Why a parser instead of patching the validator: minimal blast radius. The
validator was just patched for D4 (SCHEMA 3.7.0) and is the rubric authority
of record. Adding a single-file marketplace JSON emit path is a separate
bead (logged below). Until that lands, this wrapper unblocks fixture work
without touching the validator script.

TODO bead candidate: file as repo:ccp / sak / json-emit P1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# IS marketplace tier required fields per SCHEMA_CHANGELOG NON-NEGOTIABLES #1
IS_MARKETPLACE_REQUIRED = {
    "name", "description", "allowed-tools",
    "version", "author", "license", "compatibility", "tags",
}

# IS extras per plan 033 § 14.10 ("extras beyond the 8-field set")
IS_EXTRAS_FIELDS = {
    "requires_env", "requires_tools", "fallback_for_env", "fallback_for_tools",
    "required_environment_variables", "model", "effort",
    "disallowed-tools",  # D4 addition, SCHEMA 3.7.0
}
# plus 3 conceptual extras counted separately (metadata.intent-solutions.config,
# progressive-disclosure markers, shell enum) — for now we count what's parseable
# from frontmatter directly. Refine in Session 3 if signal is noisy.

DEPRECATED_FIELDS = {"compatible-with"}  # per SCHEMA 3.3.0+


def sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_frontmatter(skill_md_text: str) -> dict:
    """Extract YAML frontmatter without depending on PyYAML at runtime.

    Returns {} if no frontmatter detected. This is a permissive parser — it
    captures top-level scalar keys for field-presence accounting; nested YAML
    is not flattened. Adequate for the field-completeness + deprecated-field
    + is-extras counts. Phase A.0 doesn't need full YAML semantics.
    """
    if not skill_md_text.startswith("---"):
        return {}
    end = skill_md_text.find("\n---", 4)
    if end == -1:
        return {}
    block = skill_md_text[4:end]
    fm: dict = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:", line)
        if m:
            fm[m.group(1)] = True
    return fm


def run_validator(validator_path: Path, skill_path: Path, tier_flag: str) -> str:
    """Invoke validate-skills-schema.py; return combined stdout+stderr text."""
    result = subprocess.run(
        ["python3", str(validator_path), tier_flag, str(skill_path)],
        capture_output=True, text=True, check=False,
    )
    return result.stdout + result.stderr


def parse_grade(text: str) -> tuple[str, int]:
    """Return (letter, percentage). Default to ('F', 0) if not parseable."""
    m = re.search(r"GRADE:\s*([A-F])\s*\((\d+)/100\)", text)
    if m:
        return m.group(1), int(m.group(2))
    return "F", 0


def parse_findings(text: str) -> list[dict]:
    """Extract WARN and INFO lines into structured findings.

    Format observed:
        WARN: [section] message
        INFO: [section] message
    """
    findings = []
    for line in text.splitlines():
        s = line.strip()
        for sev in ("ERROR", "WARN", "INFO"):
            prefix = f"{sev}:"
            if s.startswith(prefix):
                rest = s[len(prefix):].strip()
                section_match = re.match(r"\[([^\]]+)\]\s*(.*)$", rest)
                if section_match:
                    findings.append({
                        "severity": sev,
                        "section": section_match.group(1),
                        "message": section_match.group(2),
                    })
                else:
                    findings.append({
                        "severity": sev,
                        "section": None,
                        "message": rest,
                    })
                break
    return findings


def has_error(text: str) -> bool:
    """A tier 'pass' iff no ERROR-level finding emitted."""
    return any(line.strip().startswith("ERROR:") for line in text.splitlines())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_md", type=Path, help="Path to SKILL.md fixture")
    ap.add_argument("--validator-path", type=Path,
                    default=Path("/home/jeremy/000-projects/claude-code-plugins/scripts/validate-skills-schema.py"))
    ap.add_argument("--commit", default="7b9eb8f",
                    help="Validator commit SHA pinned in expected.json")
    args = ap.parse_args()

    if not args.skill_md.is_file():
        print(f"ERROR: {args.skill_md} not found", file=sys.stderr)
        return 2
    if not args.validator_path.is_file():
        print(f"ERROR: validator not found at {args.validator_path}", file=sys.stderr)
        return 2

    skill_text = args.skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(skill_text)

    field_completeness = sum(1 for f in IS_MARKETPLACE_REQUIRED if f in fm)
    deprecated_count = sum(1 for f in DEPRECATED_FIELDS if f in fm)
    is_extras_count = sum(1 for f in IS_EXTRAS_FIELDS if f in fm)

    standard_text = run_validator(args.validator_path, args.skill_md, "--standard")
    marketplace_text = run_validator(args.validator_path, args.skill_md, "--marketplace")

    std_letter, std_pct = parse_grade(standard_text)
    mkt_letter, mkt_pct = parse_grade(marketplace_text)

    expected = {
        "fixture_sha": sha256_of_file(args.skill_md),
        "validator_version": "3.7.0",
        "validator_commit": args.commit,
        "tiers": {
            "standard": {
                "pass": not has_error(standard_text),
                "score_pct": std_pct,
                "grade": std_letter,
                "findings": parse_findings(standard_text),
            },
            "marketplace": {
                "pass": not has_error(marketplace_text),
                "score_pct": mkt_pct,
                "grade": mkt_letter,
                "findings": parse_findings(marketplace_text),
            },
        },
        "field_completeness": field_completeness,
        "deprecated_field_count": deprecated_count,
        "is_extras_present": is_extras_count,
        "security_finding_count": sum(
            1 for f in parse_findings(marketplace_text)
            if (f.get("section") or "").startswith("security")
            or "security" in (f.get("message") or "").lower()
        ),
    }

    json.dump(expected, sys.stdout, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
