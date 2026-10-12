#!/usr/bin/env python3
"""Exercise the real pre-commit config in an isolated, synthetic Git repository.

Hook environments may be downloaded on the first run. No fixture code is run;
only the configured lint/format/scrub tools execute. Real evidence is never edited.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def check(repo: Path) -> dict[str, object]:
    pre_commit = shutil.which("pre-commit")
    if pre_commit is None:
        raise RuntimeError("Install pre-commit==4.3.0 before running this check")
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    with tempfile.TemporaryDirectory(prefix="lab hygiene fixture ") as directory:
        fixture = Path(directory)

        def run(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(args, cwd=fixture, env=env, capture_output=True, text=True, timeout=300)

        def require(result: subprocess.CompletedProcess[str], code: int) -> None:
            if result.returncode != code:
                raise RuntimeError(f"Expected exit {code}, got {result.returncode}\n{result.stdout}\n{result.stderr}")

        def write(name: str, payload: bytes) -> Path:
            path = fixture / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
            return path

        require(run("git", "init", "--quiet", "-b", "main"), 0)
        for name in (
            ".pre-commit-config.yaml",
            ".markdownlint-cli2.jsonc",
            "pyproject.toml",
            "scripts/public-surface-scan.py",
            "scripts/public-surface-policy.json",
        ):
            write(name, (repo / name).read_bytes())
        protected = {}
        for root in (
            "archive/raw/synthetic",
            "specs/_vendor/synthetic",
            "_vendor/synthetic",
            ".audit-harness/synthetic",
            "research/synthetic/results/raw",
            "research/synthetic/results/normalized",
        ):
            # Unused import, unformatted code, trailing whitespace and missing
            # final newline each tempt a different mutating hook.
            protected[f"{root}/captured.py"] = b"import os\nvalue={'captured':True}  "
        protected.update(
            {
                "archive/raw/synthetic/response.body": b"captured response  \r\n\r\n",
                "specs/_vendor/synthetic/snapshot.yaml": b"captured: true  ",
                "evidence/synthetic/receipt.sigstore.json": b'{"synthetic":true}  ',
                "evidence/synthetic/receipt.bundle.json": b'{"synthetic":true}  ',
                "evidence/synthetic/events.jsonl": b'{"synthetic":true}  ',
            }
        )
        for name, payload in protected.items():
            write(name, payload)
        hashes = {name: hashlib.sha256(payload).hexdigest() for name, payload in protected.items()}
        authored = {
            "scripts/authored.py": b"import os\nvalue={'authored':True}\n",
            "scripts/tests/test_authored.py": b"def test_value():\n assert True\n",
            "notes.txt": b"authored note  ",
            "evidence/synthetic/README.md": b"# Authored evidence notes\n\nKeep this break  \non two lines.",
        }
        for name, payload in authored.items():
            write(name, payload)
        require(run("git", "add", "."), 0)
        first = run(pre_commit, "run", "--all-files")
        # Check immutable bytes before interpreting the hook exit: the original
        # config also exits 1, but corrupts captures while fixing authored files.
        for name, digest in hashes.items():
            if hashlib.sha256((fixture / name).read_bytes()).hexdigest() != digest:
                raise RuntimeError(f"Configured hooks changed immutable fixture: {name}")
        require(first, 1)
        for name, before in authored.items():
            if (fixture / name).read_bytes() == before:
                raise RuntimeError(f"Authored fixture escaped formatting: {name}")
        if b"break  \n" not in (fixture / "evidence/synthetic/README.md").read_bytes():
            raise RuntimeError("Whitespace hook removed an intentional Markdown hard break")
        require(run(pre_commit, "run", "--all-files"), 0)
        for name, digest in hashes.items():
            if hashlib.sha256((fixture / name).read_bytes()).hexdigest() != digest:
                raise RuntimeError(f"Second hook pass changed immutable fixture: {name}")
        # An excluded formatter must not turn off the read-only validators.
        write("specs/_vendor/synthetic/snapshot.yaml", b"invalid: [\n")
        invalid = run(pre_commit, "run", "check-yaml", "--all-files")
        require(invalid, 1)
        if "snapshot.yaml" not in invalid.stdout + invalid.stderr:
            raise RuntimeError("YAML failure did not identify the protected fixture")
        return {
            "protected_files_unchanged": len(protected),
            "authored_files_formatted": len(authored),
            "second_full_pass": "PASS",
            "protected_invalid_yaml": "rejected",
        }


if __name__ == "__main__":
    print(json.dumps(check(REPO), sort_keys=True))
