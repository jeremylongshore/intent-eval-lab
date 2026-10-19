#!/usr/bin/env python3
"""Read retained Phase A.0 records and replay input scores with the pinned judge.

This diagnostic emits no experiment decision, corrected effect, or p-value.
Raw experiment files stay read-only; --out must be a new file. PyYAML is needed
by the historical validator. No model/provider calls are made.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from statistics import mean
from typing import Any

VALIDATOR_COMMIT = "7b9eb8f0a77d285dee3ffe99c913d039c4878aec"
VALIDATOR_SHA256 = "b74bd109e56356653b85f4ac72917ad0dc94d2feec7023c8e0647f8588d5c501"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def prompt_frontmatter(prompt: str) -> str:
    if "<input>\n" not in prompt or not prompt.endswith("\n</input>"):
        raise ValueError("Unrecognized retained prompt boundary")
    return prompt.rsplit("<input>\n", 1)[1].removesuffix("\n</input>")


def recover_input(final: str, accepted: bool, proposal: dict[str, Any] | None) -> str:
    if not accepted:
        return final
    # Historical run-arm-b.py apply_proposal preserves the suffix after the
    # closing delimiter. The prompt retains the original frontmatter verbatim.
    end = final.find("\n---", 4)
    if not final.startswith("---") or end < 0 or proposal is None:
        raise ValueError("Cannot reconstruct accepted specimen input")
    return prompt_frontmatter(proposal["prompt"]) + final[end + 4 :]


def replay_score(validator: Path, content: str, directory: Path) -> int:
    slot = directory / f"_score_{sha256(content.encode())[:8]}"
    slot.mkdir()
    path = slot / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(validator), "--marketplace", str(path)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    grades = re.findall(r"GRADE:\s*[A-F]\s*\((\d+)/100\)", result.stdout)
    if result.returncode not in (0, 1) or len(grades) != 1:
        raise ValueError("Pinned validator did not emit exactly one grade")
    return int(grades[0])


def audit(root: Path, validator: Path) -> dict[str, Any]:
    if sha256(validator.read_bytes()) != VALIDATOR_SHA256:
        raise ValueError("Validator bytes differ from the reviewed historical pin")
    hashes: dict[str, str] = {}

    def read(relative: str) -> str:
        data = (root / relative).read_bytes()
        hashes[relative] = sha256(data)
        return data.decode("utf-8")

    def read_json(relative: str) -> Any:
        return json.loads(read(relative))

    manifest = read_json("corpus/manifest.json")
    a_prefix = "results/arm-a/nvidia-llama-70b"
    b_prefix = "results/arm-b/nvidia-llama-70b"
    summary = read_json(f"{b_prefix}/_summary.json")
    records = summary["per_specimen_results"]
    by_id = {record["sha8"]: record for record in records}
    expected = [(stratum, rec) for stratum, group in manifest["strata"].items() for rec in group]
    if len(expected) != 60 or len(by_id) != 60 or len(records) != 60:
        raise ValueError("Historical audit requires all 60 unique records")
    if set(by_id) != {rec["sha256"][:8] for _, rec in expected}:
        raise ValueError("Historical summary and manifest IDs differ")
    errors = [json.loads(line) for line in read(f"{b_prefix}/errors.jsonl").splitlines() if line]
    rows = []
    with tempfile.TemporaryDirectory(prefix="phase-a0-history-audit-") as directory:
        for stratum, specimen in sorted(expected, key=lambda pair: pair[1]["sha256"]):
            declared_sha = specimen["sha256"]
            if not re.fullmatch(r"[0-9a-f]{64}", declared_sha):
                raise ValueError("Malformed specimen digest")
            sha8 = declared_sha[:8]
            record = by_id[sha8]
            trajectory = read_json(f"{b_prefix}/{sha8}/trajectory.json")
            if record["accepted"] != trajectory["accepted"]:
                raise ValueError("Summary and trajectory acceptance disagree")
            proposal_path = f"{b_prefix}/{sha8}/proposal-0.json"
            proposal = read_json(proposal_path) if (root / proposal_path).is_file() else None
            final = read(f"{b_prefix}/{sha8}/final.md")
            content = recover_input(final, record["accepted"], proposal)
            end = content.find("\n---", 4)
            if end < 0:
                raise ValueError("Missing recovered frontmatter delimiter")
            fm = content[: end + 4]
            a_scores = []
            frontmatter_matches = []
            for k in (0, 3, 8, 16):
                a_scores.append(read_json(f"{a_prefix}/{sha8}/k={k}/score.json"))
                prompt = read_json(f"{a_prefix}/{sha8}/k={k}/prompt.json")
                frontmatter_matches.append(prompt_frontmatter(prompt["prompt_text"]) == fm)
            a_baselines = {score["baseline_marketplace_score_pct"] for score in a_scores}
            if len(a_baselines) != 1:
                raise ValueError("Arm A K slots disagree on baseline")
            a_baseline = a_baselines.pop()
            b_baseline = record["baseline_marketplace_score_pct"]
            proposal_files = sorted((root / b_prefix / sha8).glob("proposal-*.json"))
            for path in proposal_files:
                read(str(path.relative_to(root)))
            initial_429 = sum(
                error.get("sha8") == sha8
                and error.get("context", {}).get("iteration") == 0
                and error.get("error", "").startswith("API call failed")
                and "429" in error.get("error", "")
                for error in errors
            )
            replay = replay_score(validator, content, Path(directory))
            rows.append(
                {
                    "declared_sha256": declared_sha,
                    "stratum": stratum,
                    "recovered_input_sha256": sha256(content.encode()),
                    "input_matches_manifest": sha256(content.encode()) == declared_sha,
                    "recovery": "original frontmatter plus preserved body" if record["accepted"] else "rejected final",
                    "arm_a_frontmatter_matches": all(frontmatter_matches),
                    "manifest_baseline": specimen["marketplace_score"],
                    "arm_a_baseline": a_baseline,
                    "arm_b_baseline": b_baseline,
                    "baseline_difference_pp": a_baseline - b_baseline,
                    "replayed_arm_b_baseline": replay,
                    "replay_matches": replay == b_baseline,
                    "accepted": record["accepted"],
                    "proposal_count": len(proposal_files),
                    "trajectory_length": len(trajectory["trajectory"]),
                    "initial_api_429_count": initial_429,
                }
            )
    # These are recorded historical values, not newly computed experiment results.
    historical = read_json("results/aggregated/statistics.json")
    read("results/aggregated/decision.json")
    return {
        "schema": "phase-a0-input-audit/v1",
        "purpose": "Diagnostic input replay; no replacement experiment decision",
        "validator_commit": VALIDATOR_COMMIT,
        "validator_sha256": VALIDATOR_SHA256,
        "summary": {
            "specimens": len(rows),
            "baseline_mismatches": sum(row["baseline_difference_pp"] != 0 for row in rows),
            "mean_arm_a_minus_arm_b_baseline_pp": mean(row["baseline_difference_pp"] for row in rows),
            "arm_a_baselines_match_manifest": all(row["arm_a_baseline"] == row["manifest_baseline"] for row in rows),
            "input_hash_mismatches": sum(not row["input_matches_manifest"] for row in rows),
            "arm_a_frontmatter_matches": sum(row["arm_a_frontmatter_matches"] for row in rows),
            "replayed_baseline_matches": sum(row["replay_matches"] for row in rows),
            "zero_proposal_specimens": sum(row["proposal_count"] == 0 for row in rows),
            "zero_proposal_initial_429_specimens": sum(
                row["proposal_count"] == 0 and row["initial_api_429_count"] > 0 for row in rows
            ),
            "reported_arm_b_error_count": summary["error_count"],
            "historical_n_paired": historical["n_specimens_paired"],
            "historical_b_minus_a_mean_pp": historical["raw_means"]["b_minus_a_mean"],
        },
        "specimens": rows,
        "source_sha256": dict(sorted(hashes.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-root", type=Path, required=True)
    parser.add_argument("--validator", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.out.exists():
            raise ValueError("Output exists; choose a fresh audit file")
        report = audit(args.research_root.resolve(), args.validator.resolve())
        serialized = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
        with args.out.open("x", encoding="utf-8") as out:
            out.write(serialized)
        print(json.dumps(report["summary"], sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"Audit refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
