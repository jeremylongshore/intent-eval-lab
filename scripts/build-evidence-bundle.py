#!/usr/bin/env python3
"""
build-evidence-bundle.py — construct a canonical Evidence Bundle JSON for the
Phase A.0 baseline result, conforming to @intentsolutions/core's
schemas/v1/evidence-bundle.schema.json.

What this bundle IS:
  A content-addressed, append-only statement that names the Phase A.0 result
  artifacts by their SHA-256 digests. When signed with `cosign sign-blob`
  against PRODUCTION sigstore (rekor.sigstore.dev), the resulting .sigstore.json
  attests — under the GitHub Actions workflow identity — that these exact files
  existed and were signed at that time, anchored in the public transparency log.

What this bundle is NOT (deliberate, per DR-018 + DR-010 Q3):
  - It declares NO predicate URI. `predicate_uri_set` is empty. The
    `skill-binary-eval/v1` predicate is RESERVED, not declared — production-Rekor
    predicate declaration is gated on SPEC.md normative + DNSSEC + CAA clearing
    for evals.intentsolutions.io, none of which have. Signing the bundle as a
    BLOB does not declare a predicate; it attests file integrity + identity +
    time. That distinction is the whole point.
  - It does NOT claim the statistics are "correct." A signature attests
    authenticity of the artifacts, not the truth of the science. The science
    stands on the pre-registered analysis in RESULTS.md / DR-036.

Determinism: this script takes ALL time-varying inputs as arguments
(--created-at, --eval-run-id, --bundle-id) so CI and local runs produce
byte-identical output → identical signed digest → reproducible verification.
No Date.now(), no random UUIDs generated here. NOTE: the signed bundle is
deliberately COMMIT-INDEPENDENT — it does not embed a git SHA. The bundle
attests content by digest; which commit signed it is recorded in the sigstore
certificate's GitHub OIDC claims (GITHUB_SHA), not baked into the signed
payload. Embedding the commit would be self-referential (committing the bundle
changes the SHA the next rebuild embeds → can never match).

Usage:
  build-evidence-bundle.py \
    --created-at 2026-06-01T00:00:00.000Z \
    --eval-run-id 0197f8a0-0000-7000-8000-000000000000 \
    --bundle-id   0197f8a0-0000-7000-8000-000000000001 \
    --out evidence/phase-a-0-baseline/evidence-bundle.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# The result artifacts this bundle attests, by repo-relative path. Each becomes
# an in-toto Subject (name + sha256 digest). subjectName pattern per kernel:
# <tool>:<side>:<gate-id>, side ∈ {client,server,ci,sandbox,local}.
SUBJECTS = [
    (
        "phase-a0:ci:decision",
        "research/phase-a-0-baseline/results/aggregated/decision.json",
    ),
    (
        "phase-a0:ci:statistics",
        "research/phase-a-0-baseline/results/aggregated/statistics.json",
    ),
    (
        "phase-a0:ci:results-md",
        "research/phase-a-0-baseline/RESULTS.md",
    ),
    (
        "phase-a0:ci:decision-record",
        "000-docs/036-AT-DECR-phase-a0-result-proceed-2026-05-31.md",
    ),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_bundle(created_at: str, eval_run_id: str, bundle_id: str) -> dict:
    subject_set = []
    for name, rel in SUBJECTS:
        p = REPO_ROOT / rel
        if not p.exists():
            print(f"FATAL: subject artifact missing: {rel}", file=sys.stderr)
            sys.exit(2)
        subject_set.append(
            {"name": name, "digest": {"sha256": sha256_file(p)}}
        )

    # storage_key: a stable, commit-INDEPENDENT content-addressed key. Must not
    # embed a git SHA (that would be self-referential — committing the bundle
    # changes the SHA the next rebuild embeds, so it could never match). The
    # signing commit is recorded in the sigstore certificate, not here.
    storage_key = "git:jeremylongshore/intent-eval-lab:evidence/phase-a-0-baseline/evidence-bundle.json"

    bundle = {
        "id": bundle_id,
        "eval_run_id": eval_run_id,
        "created_at": created_at,
        # EMPTY by design — no predicate URI declared (DR-018 / DR-010 Q3).
        "predicate_uri_set": [],
        "row_count": 0,
        "subject_set": subject_set,
        "storage_key": storage_key,
        # The bundle's own signing posture. It is signed as a BLOB to PRODUCTION
        # sigstore, but it makes NO predicate claim. We encode the honest posture:
        # the artifacts are real + signed, but this is not a predicate attestation.
        "signing_mode": "unsigned_experimental",
        "rekor_log_indices": [],
        "verification_status": "unverified",
        "verification_last_checked_at": created_at,
    }
    return bundle


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--created-at", required=True)
    ap.add_argument("--eval-run-id", required=True)
    ap.add_argument("--bundle-id", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    bundle = build_bundle(
        args.created_at, args.eval_run_id, args.bundle_id
    )

    # Canonical serialization: sorted keys, compact-but-readable, trailing newline.
    # Deterministic so CI + local produce identical bytes → identical signed digest.
    out = REPO_ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(bundle, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    out.write_text(text, encoding="utf-8")

    bundle_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"Evidence Bundle written: {args.out}")
    print(f"  subjects:       {len(bundle['subject_set'])}")
    print(f"  bundle sha256:  {bundle_digest}")
    print(f"  predicate_uri:  (none — reserved, not declared)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
