#!/usr/bin/env python3
"""Scorer + integrity gate for the FROZEN drift-classification/v1 eval set.

The future LLM drift-classifier (advisory-comment mode first) writes NOTHING
until it clears the recall floor on this frozen, human-labeled eval set of
real upstream-snapshot diffs mined from this repo's git history (plus marked
synthetic perturbations of real snapshots). This runner is the deterministic
half of that contract — it only SCORES. No LLM calls, no network, stdlib only.

Two duties:

  1. Manifest integrity (the FROZEN guarantee) — re-hash every case file and
     fail on ANY divergence from evals/drift-classification/v1/manifest.json.
     Existing cases are never edited; extension is append-only (new case dirs
     + new manifest entries in the same PR). See
     000-docs/053-AT-SPEC-drift-classification-eval-set-2026-06-12.md.

  2. Scoring — given a predictions JSONL (one object per line:
     {"case_id": ..., "label": "material"|"immaterial", "contract_owner": ...}),
     compute recall on material cases, precision, a per-case table, and exit
     nonzero if recall < the manifest's recall_floor. A missing prediction for
     a material case counts as a miss (the classifier cannot abstain its way
     past the floor).

Exit 0 = pass; exit 1 = integrity drift or recall below floor; exit 2 = usage
or parse error.

Usage:
  drift-eval-runner.py --verify-manifest [--eval-root DIR]
  drift-eval-runner.py --score PREDICTIONS.jsonl [--eval-root DIR]
  drift-eval-runner.py --self-test          # prove the gate is not vacuous
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_EVAL_ROOT = os.path.join(REPO_ROOT, "evals", "drift-classification", "v1")

LABELS = {"material", "immaterial"}


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest(eval_root: str) -> dict:
    path = os.path.join(eval_root, "manifest.json")
    if not os.path.exists(path):
        print(f"ERROR: manifest not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def verify_manifest(eval_root: str) -> int:
    """Re-hash every case file; ANY divergence from the manifest fails."""
    manifest = _load_manifest(eval_root)
    case_files = manifest.get("case_files", ["before", "after", "meta.json"])
    cases = manifest.get("cases", {})
    problems: list[str] = []

    if manifest.get("case_count") != len(cases):
        problems.append(
            f"case_count {manifest.get('case_count')} != manifest cases entries {len(cases)}"
        )

    for case_id in sorted(cases):
        case_dir = os.path.join(eval_root, "cases", case_id)
        pinned = cases[case_id].get("sha256", {})
        for name in case_files:
            path = os.path.join(case_dir, name)
            if name not in pinned:
                problems.append(f"{case_id}/{name}: no pinned hash in manifest")
                continue
            if not os.path.exists(path):
                problems.append(f"{case_id}/{name}: file missing on disk")
                continue
            actual = _sha256(path)
            if actual != pinned[name]:
                problems.append(
                    f"{case_id}/{name}: hash drift — pinned {pinned[name][:12]}…, actual {actual[:12]}…"
                )

    # Frozen also means no unmanifested case dirs sneaking in silently.
    cases_dir = os.path.join(eval_root, "cases")
    on_disk = sorted(d for d in os.listdir(cases_dir)) if os.path.isdir(cases_dir) else []
    for d in on_disk:
        if d not in cases:
            problems.append(f"case dir on disk but not in manifest: {d}")
    for case_id in cases:
        if case_id not in on_disk:
            problems.append(f"case in manifest but no dir on disk: {case_id}")

    if problems:
        print(f"drift-eval manifest integrity: {len(problems)} PROBLEM(S) — the frozen set has drifted:")
        for p in problems:
            print(f"  - {p}")
        print("\nFrozen means frozen: existing cases are NEVER edited. New cases append")
        print("via PR with new manifest entries; see 000-docs/053-AT-SPEC-drift-classification-eval-set-2026-06-12.md.")
        return 1

    print(
        f"drift-eval manifest integrity: OK — {len(cases)} cases, "
        f"{len(cases) * len(case_files)} files re-hashed, all match (frozen_at {manifest.get('frozen_at')})."
    )
    return 0


def _load_predictions(path: str, known_ids: set[str]) -> dict[str, dict]:
    predictions: dict[str, dict] = {}
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"ERROR: {path}:{lineno}: invalid JSON: {exc}", file=sys.stderr)
                sys.exit(2)
            case_id = row.get("case_id")
            if not case_id or case_id not in known_ids:
                print(f"ERROR: {path}:{lineno}: unknown case_id {case_id!r}", file=sys.stderr)
                sys.exit(2)
            if case_id in predictions:
                print(f"ERROR: {path}:{lineno}: duplicate prediction for {case_id}", file=sys.stderr)
                sys.exit(2)
            if row.get("label") not in LABELS:
                print(f"ERROR: {path}:{lineno}: label must be one of {sorted(LABELS)}", file=sys.stderr)
                sys.exit(2)
            predictions[case_id] = row
    return predictions


def score(eval_root: str, predictions_path: str) -> int:
    """Score predictions against the frozen labels; gate on the recall floor."""
    # Integrity first — scores against a drifted set are meaningless.
    if verify_manifest(eval_root) != 0:
        return 1
    manifest = _load_manifest(eval_root)
    floor = float(manifest.get("recall_floor", 1.0))

    labels: dict[str, dict] = {}
    for case_id in sorted(manifest.get("cases", {})):
        with open(os.path.join(eval_root, "cases", case_id, "meta.json"), encoding="utf-8") as fh:
            labels[case_id] = json.load(fh)

    predictions = _load_predictions(predictions_path, set(labels))

    tp = fn = fp = tn = 0
    owner_hits = owner_total = 0
    rows: list[tuple[str, str, str, str]] = []
    for case_id, meta in labels.items():
        truth = meta["label"]
        pred = predictions.get(case_id)
        pred_label = pred["label"] if pred else "(missing)"
        if truth == "material":
            if pred_label == "material":
                tp += 1
                verdict = "ok"
                owner_total += 1
                if pred.get("contract_owner") == meta.get("expected_contract_owner"):
                    owner_hits += 1
                else:
                    verdict = "ok (owner wrong)"
            else:
                fn += 1
                verdict = "MISSED MATERIAL"
        else:
            if pred_label == "material":
                fp += 1
                verdict = "false positive"
            else:
                tn += 1
                verdict = "ok"
        rows.append((case_id, truth, pred_label, verdict))

    material_total = tp + fn
    recall = (tp / material_total) if material_total else 1.0
    precision = (tp / (tp + fp)) if (tp + fp) else None

    print("\nper-case results:")
    print(f"  {'case':<10} {'truth':<11} {'predicted':<11} verdict")
    for case_id, truth, pred_label, verdict in rows:
        print(f"  {case_id:<10} {truth:<11} {pred_label:<11} {verdict}")

    print(f"\nrecall on material:  {tp}/{material_total} = {recall:.3f} (floor {floor:.3f})")
    print(f"precision:           {f'{precision:.3f}' if precision is not None else 'n/a (no material predictions)'} ({tp} TP, {fp} FP)")
    if owner_total:
        print(f"contract-owner acc:  {owner_hits}/{owner_total} on recalled material (informational, not gated)")
    print(f"confusion: TP={tp} FN={fn} FP={fp} TN={tn}")

    if recall < floor:
        print(f"\nFAIL: recall {recall:.3f} < floor {floor:.3f} — the classifier does NOT clear the write gate.")
        return 1
    print(f"\nPASS: recall {recall:.3f} >= floor {floor:.3f}.")
    return 0


def self_test() -> int:
    """Prove the gate is not vacuous (the spec-projection-diff self-test ethos):
    perfect fixture passes, missed-material fixture fails, tampering fails."""
    failures = 0
    runner = os.path.abspath(__file__)
    fixtures = os.path.join(DEFAULT_EVAL_ROOT, "fixtures")

    def run(args: list[str]) -> int:
        return subprocess.run([sys.executable, runner, *args], stdout=subprocess.DEVNULL).returncode

    checks = [
        ("manifest integrity on the committed set", ["--verify-manifest"], 0),
        ("perfect predictions clear the floor", ["--score", os.path.join(fixtures, "predictions-perfect.jsonl")], 0),
        ("a missed material case fails the floor", ["--score", os.path.join(fixtures, "predictions-miss-material.jsonl")], 1),
    ]
    for desc, args, expected in checks:
        rc = run(args)
        status = "ok" if rc == expected else "FAIL"
        print(f"self-test {status}: {desc} (exit {rc}, expected {expected})")
        failures += rc != expected

    # Tamper detection: a single flipped byte in a copied set must fail verify.
    with tempfile.TemporaryDirectory() as tmp:
        tampered = os.path.join(tmp, "v1")
        shutil.copytree(DEFAULT_EVAL_ROOT, tampered)
        target = os.path.join(tampered, "cases", "real-0001", "before")
        with open(target, "ab") as fh:
            fh.write(b"\n<!-- tampered -->\n")
        rc = run(["--verify-manifest", "--eval-root", tampered])
        status = "ok" if rc == 1 else "FAIL"
        print(f"self-test {status}: tampered case detected by --verify-manifest (exit {rc}, expected 1)")
        failures += rc != 1

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the recall-floor gate is not sound.")
        return 1
    print("\nself-test: all checks passed; the frozen-manifest + recall-floor gate is sound.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen drift-classification eval set: integrity + scoring.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify-manifest", action="store_true", help="re-hash all cases; fail on any drift")
    group.add_argument("--score", metavar="PREDICTIONS.jsonl", help="score predictions; gate on the recall floor")
    group.add_argument("--self-test", action="store_true", help="prove the gate is not vacuous")
    parser.add_argument("--eval-root", default=DEFAULT_EVAL_ROOT, help="eval set root (default: evals/drift-classification/v1)")
    args = parser.parse_args()

    if args.verify_manifest:
        return verify_manifest(args.eval_root)
    if args.score:
        return score(args.eval_root, args.score)
    if args.self_test:
        return self_test()
    return 2


if __name__ == "__main__":
    sys.exit(main())
