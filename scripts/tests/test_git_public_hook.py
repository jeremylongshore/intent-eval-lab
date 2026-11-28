"""Exercise the tracked pre-commit hook through actual, isolated Git commits."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]


class HookRepository:
    def __init__(self, tmp_path: Path) -> None:
        self.primary = tmp_path / "nested project" / "intent-eval-lab"
        self.primary.mkdir(parents=True)
        self.bin = tmp_path / "isolated-bin"
        self.bin.mkdir()
        for name in ("git", "sh", "timeout"):
            executable = shutil.which(name)
            assert executable, f"test prerequisite missing: {name}"
            (self.bin / name).symlink_to(executable)
        (self.bin / "python3").symlink_to(sys.executable)
        self.trace = tmp_path / "beads-calls.log"
        self.bd = self.bin / "bd"
        self.bd.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$HOOK_TEST_TRACE"\n' 'exit "${HOOK_TEST_BD_EXIT:-0}"\n')
        self.bd.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(
            PATH=str(self.bin),
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
            HOOK_TEST_TRACE=str(self.trace),
            HOOK_TEST_BD_EXIT="0",
        )
        self.git(self.primary, "init", "--quiet", "-b", "main")
        self.git(self.primary, "config", "user.name", "Synthetic Hook Fixture")
        self.git(self.primary, "config", "user.email", "fixture@example.invalid")
        self.git(self.primary, "config", "commit.gpgsign", "false")
        shutil.copytree(REPO / ".beads" / "hooks", self.primary / ".beads" / "hooks")
        scripts = self.primary / "scripts"
        scripts.mkdir()
        for name in ("public-surface-scan.py", "public-surface-policy.json"):
            shutil.copy2(REPO / "scripts" / name, scripts / name)
        (self.primary / "README.md").write_text("# Synthetic safe fixture\n")
        self.git(self.primary, "config", "core.hooksPath", str(self.primary / ".beads" / "hooks"))
        self.git(self.primary, "add", ".")
        self.git(self.primary, "commit", "--quiet", "-m", "seed safe fixture")

    def git(self, cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=cwd, env=self.env, capture_output=True, text=True, check=check, timeout=30
        )

    def checkout(self, tmp_path: Path, layout: str) -> Path:
        if layout == "primary":
            return self.primary
        linked = tmp_path / "linked worktree"
        self.git(self.primary, "worktree", "add", "--quiet", "-b", "fixture-linked", str(linked))
        return linked


@pytest.mark.parametrize("layout", ["primary", "linked"])
@pytest.mark.parametrize("beads_exit", [0, 3, 124, None])
def test_real_commit_scrubs_current_index_despite_beads_fallback(
    tmp_path: Path, layout: str, beads_exit: int | None
) -> None:
    fixture = HookRepository(tmp_path)
    checkout = fixture.checkout(tmp_path, layout)
    if beads_exit is None:
        fixture.bd.unlink()
    else:
        fixture.env["HOOK_TEST_BD_EXIT"] = str(beads_exit)
    fixture.trace.write_text("")
    before = fixture.git(checkout, "rev-parse", "HEAD").stdout.strip()
    document = checkout / "README.md"
    synthetic = "synthetic-person@example.invalid"
    document.write_text(f"# Synthetic fixture\n{synthetic}\n")
    fixture.git(checkout, "add", "README.md")
    # An innocent worktree file must not hide prohibited content in the index.
    document.write_text("# Safe unstaged replacement\n")
    rejected = fixture.git(checkout, "commit", "--quiet", "-m", "must reject fixture", check=False)
    assert rejected.returncode != 0
    assert "email-address" in rejected.stdout + rejected.stderr
    assert synthetic not in rejected.stdout + rejected.stderr
    assert fixture.git(checkout, "rev-parse", "HEAD").stdout.strip() == before
    if beads_exit is not None:
        assert "hooks run pre-commit" in fixture.trace.read_text()
    else:
        assert not fixture.trace.read_text()

    fixture.git(checkout, "add", "README.md")
    accepted = fixture.git(checkout, "commit", "--quiet", "-m", "accept safe fixture")
    assert "public-surface-scan: PASS" in accepted.stdout + accepted.stderr
    assert fixture.git(checkout, "rev-parse", "HEAD").stdout.strip() != before


@pytest.mark.parametrize("missing", ["public-surface-scan.py", "public-surface-policy.json", "python3"])
def test_missing_scrub_dependency_blocks_commit(tmp_path: Path, missing: str) -> None:
    fixture = HookRepository(tmp_path)
    before = fixture.git(fixture.primary, "rev-parse", "HEAD").stdout.strip()
    (fixture.primary / "README.md").write_text("# Another safe fixture\n")
    fixture.git(fixture.primary, "add", "README.md")
    target = fixture.bin / missing if missing == "python3" else fixture.primary / "scripts" / missing
    target.unlink()
    rejected = fixture.git(fixture.primary, "commit", "--quiet", "-m", "missing gate", check=False)
    assert rejected.returncode != 0
    assert fixture.git(fixture.primary, "rev-parse", "HEAD").stdout.strip() == before
