"""Conservative Markdown visibility and bounded required-set checks."""

from __future__ import annotations

import re


def fence_mask(lines: list[str]) -> list[bool]:
    """Mask CommonMark backtick/tilde fences, including their delimiters.

    A closer uses the same character and at least the opening length; shorter
    or mixed delimiters remain quoted. An unclosed fence masks the remainder.
    """
    result: list[bool] = []
    active: tuple[str, int] | None = None
    for line in lines:
        if active:
            char, length = active
            if re.fullmatch(r" {0,3}" + re.escape(char) + "{" + str(length) + r",}[ \t]*", line):
                active = None
            result.append(True)
            continue
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match and (match[1][0] != "`" or "`" not in match[2]):
            active = (match[1][0], len(match[1]))
            result.append(True)
        else:
            result.append(False)
    return result


def visible_lines(lines: list[str]) -> list[str]:
    return ["" if hidden else line for line, hidden in zip(lines, fence_mask(lines), strict=True)]


_KEYS = r"((?:`[^`]+`(?:,\s*|\s+and\s+|\s*,\s*and\s*)?)+)"
_REQUIRED = re.compile(_KEYS + r"\s+(?:is|are)\s+(?:also\s+|the only\s+)?required\b")
_NOT_REQUIRED = re.compile(_KEYS + r"\s+(?:is|are)\s+(?:not|never)\s+required\b")


def required_set_matches(lines: list[str], expected: set[str]) -> bool:
    """Check consumed explicit field-requiredness clauses in visible prose.

    Table rows are handled by owning extractors; examples never define the set.
    This is bounded clause recognition, not a claim of general prose semantics.
    """
    prose = "\n".join(line for line in visible_lines(lines) if not line.lstrip().startswith("|"))
    clauses = [set(re.findall(r"`([^`]+)`", match[1])) for match in _REQUIRED.finditer(prose)]
    denied = [set(re.findall(r"`([^`]+)`", match[1])) for match in _NOT_REQUIRED.finditer(prose)]
    return bool(clauses) and set.union(*clauses) == expected and not any(names & expected for names in denied)
