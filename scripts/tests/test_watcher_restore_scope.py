"""Regression lock: the watcher must never restore HUMAN-OWNED files from its bot branch.

WHAT HAPPENED
-------------
`spec-drift-watch.yml` restores prior bookkeeping from the `spec-drift/auto-promotion`
branch at job start, so the watcher's append-only artifacts accumulate across runs
instead of each run starting from whatever main happens to hold. That is correct and
load-bearing.

But the restore listed `specs/_vendor/` wholesale, and that path contains TWO trees
with opposite ownership:

  specs/_vendor/<surface>/    written by fetch-capture.py on FETCH_OK   — bot-owned
  specs/_vendor/upstream/     hand-vendored reference docs + the derived
                              projections a human reconciles              — HUMAN-owned

`upstream` is not a surface id, so the capture stage cannot write it and the bot
branch can only ever hold a STALER copy. Restoring it could therefore only ever
regress it.

Reproduced before fixing, with the branch at a6ba36e and main at 2c7a2e0: the bulk
restore reverted all three reconciled projections to `unversioned-2026-06-12`,
which turned the ENFORCED sub-agents freshness gate red (`permissionMode.enum`
reappears against a capture that documents `manual`) and would have made the next
promotion PR propose undoing main's reconciliation.

This is the same baseline regression the step's merge-base guard already prevents,
reached by a different route: that guard covers "the branch was merged, so main is
newer wholesale", not "main advanced these specific files independently of the
branch" — which is exactly what a human reconciliation is.

WHY THE TEST IS SHAPED THIS WAY
-------------------------------
The defect lives in bash inside YAML, so there is no function to call. Asserting on
the workflow's own text is weak, but the INVARIANT is checkable: any step that
restores `specs/_vendor/` from a non-HEAD ref must, in the same step, re-pin
`specs/_vendor/upstream/` back to HEAD. That fails loudly if someone deletes the
guard line or adds a second bulk-restore step, which are the two realistic
regressions.

Offline. Reads only the committed workflow.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "spec-drift-watch.yml"

# Trees the watcher itself never writes, so a bot branch can only hold a staler copy.
HUMAN_OWNED = ("specs/_vendor/upstream/", "specs/upstream-surface-registry.v1.json")

_RESTORE_FROM_REF = re.compile(r"git checkout\s+(?!HEAD\b)(\S+)\s+--", re.MULTILINE)
_REPIN_UPSTREAM = re.compile(r"git checkout\s+HEAD\s+--\s+specs/_vendor/upstream/")


def _run_scripts() -> list[tuple[str, str]]:
    """(step name, run script) for every step in the workflow that has one."""
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    out: list[tuple[str, str]] = []
    for job in doc["jobs"].values():
        for step in job.get("steps", []):
            if isinstance(step.get("run"), str):
                out.append((step.get("name", "<unnamed>"), step["run"]))
    return out


def test_the_workflow_still_parses_and_has_steps() -> None:
    """Guard the guard: a parse change must not silently empty these assertions."""
    steps = _run_scripts()
    assert len(steps) > 5, "workflow shape changed — the checks below would be vacuous"


def test_any_bulk_vendor_restore_repins_the_hand_vendored_tree() -> None:
    """THE lock. Restoring specs/_vendor/ from the bot branch must not carry
    specs/_vendor/upstream/ with it."""
    offenders: list[str] = []
    for name, script in _run_scripts():
        restores = _RESTORE_FROM_REF.findall(script)
        if not restores:
            continue
        if "specs/_vendor/" not in script:
            continue
        if not _REPIN_UPSTREAM.search(script):
            offenders.append(
                f"step {name!r} restores specs/_vendor/ from {restores} without re-pinning "
                "specs/_vendor/upstream/ to HEAD — a human-reconciled baseline would be "
                "silently reverted to whatever the bot branch holds"
            )
    assert not offenders, "\n".join(offenders)


@pytest.mark.parametrize("path", HUMAN_OWNED)
def test_human_owned_paths_are_never_restored_from_a_non_head_ref(path: str) -> None:
    """The registry and the hand-vendored tree are authored by people.

    Naming them in a restore list would hand a bot branch the authority to overwrite
    human decisions — including which surfaces are ENFORCED, which is the one setting
    that decides whether this whole gate can fail at all.
    """
    for name, script in _run_scripts():
        for match in _RESTORE_FROM_REF.finditer(script):
            tail = script[match.end() :]
            # Only the argument list of THIS checkout, not the rest of the script.
            args = tail.split("\n\n", 1)[0]
            assert path not in args, (
                f"step {name!r} restores human-owned {path} from {match.group(1)}; "
                "a bot branch must never be authoritative for it"
            )
