#!/usr/bin/env python3
"""build-fixtures.py — materialize Phase A.0 corpus into ccp test fixtures.

Reads the pre-registered manifest.json, runs score-fixture.py against each
specimen, and stages a fixture directory per the DESIGN.md § 5.1 schema:

    tests/fixtures/skill-frontmatter/<sha8>/
    ├── input.md
    ├── expected.json
    ├── label.txt
    └── provenance.json

Idempotent: re-running skips existing fixtures unless --force is passed.
No Anthropic API calls. Local validator + filesystem only.

Usage:
    build-fixtures.py --manifest <path> --out <dir> --score-script <path>
                      [--force] [--strata A,B,C,held_out]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path


def run_scorer(score_script: Path, skill_path: Path) -> dict:
    result = subprocess.run(
        ["python3", str(score_script), str(skill_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"scorer exit {result.returncode} on {skill_path}: {result.stderr[:200]}")
    return json.loads(result.stdout)


def stage_fixture(
    out_dir: Path, sha8: str, input_path: Path, expected: dict, label: str, provenance: dict, force: bool
) -> bool:
    target = out_dir / sha8
    if target.exists() and not force:
        return False
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_path, target / "input.md")
    (target / "expected.json").write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    (target / "label.txt").write_text(label + "\n")
    (target / "provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    return True


def label_for(stratum: str, expected: dict) -> str:
    pass_flag = expected["tiers"]["marketplace"]["pass"]
    if stratum == "A":
        return f"global-{'pass' if pass_flag else 'fail'}-marketplace"
    if stratum == "B":
        return "marketplace-corpus-pass"
    if stratum == "C":
        return "marketplace-corpus-fail"
    return f"{stratum}-{'pass' if pass_flag else 'fail'}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--score-script", type=Path, required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--strata", default="A,B,C,held_out", help="Comma-separated subset of strata to materialize.")
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text())
    seed = manifest.get("pre_registration", {}).get("seed")
    val_commit = manifest.get("pre_registration", {}).get("validator_commit", "unknown")

    args.out.mkdir(parents=True, exist_ok=True)
    selected = set(s.strip() for s in args.strata.split(","))

    staged = 0
    skipped = 0
    errors = []
    started = dt.datetime.utcnow()

    for stratum_key in ("strata", "held_out"):
        if stratum_key == "strata":
            groups = manifest["strata"]
            held = False
        else:
            groups = manifest["held_out"]
            held = True

        for letter, items in groups.items():
            full_label = f"held_out_{letter}" if held else letter
            if full_label not in selected and letter not in selected and stratum_key not in selected:
                continue

            for item in items:
                skill_path = Path(item["path"])
                sha = item["sha256"]
                sha8 = sha[:8]
                try:
                    expected = run_scorer(args.score_script, skill_path)
                except Exception as e:
                    errors.append({"path": str(skill_path), "error": str(e)})
                    continue

                provenance = {
                    "source_path": str(skill_path),
                    "source_sha256": sha,
                    "manifest_stratum": full_label,
                    "manifest_seed": seed,
                    "validator_commit": val_commit,
                    "captured_at": dt.datetime.utcnow().isoformat() + "Z",
                    "held_out": held,
                }
                changed = stage_fixture(
                    args.out,
                    sha8,
                    skill_path,
                    expected,
                    label_for(letter, expected),
                    provenance,
                    args.force,
                )
                if changed:
                    staged += 1
                else:
                    skipped += 1

    elapsed = (dt.datetime.utcnow() - started).total_seconds()
    summary = {
        "staged": staged,
        "skipped_existing": skipped,
        "errors": errors,
        "wall_seconds": round(elapsed, 1),
        "out": str(args.out),
        "fixture_count_total": staged + skipped,
    }
    print(json.dumps(summary, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
