#!/usr/bin/env bash
# Ratified-clause-conflict HALT-gate reminder (DR-085 D1).
#
# WHAT THIS DOES (and does NOT do — read this before you trust it):
#
#   This script DETECTS that a change set touches a one-way-door artifact
#   (a predicate file, a signed JSON Schema, a kernel entity definition) and,
#   when it does, EMITS THE HALT-ON-CONFLICT REMINDER plus pointers to the
#   governing Decision Records. That is the maximum it can honestly do.
#
#   This script does NOT — and cannot — automatically detect a *semantic
#   contradiction* between two ratified clauses (e.g. DR-028 T1 "defer signing
#   fields" vs P0-RATIFY-2 "add them now"). Deciding that two clauses bear on the
#   same artifact and that one makes the other false is a judgment task, not a
#   regex. Any tool claiming to auto-detect arbitrary ratified-clause conflicts
#   would be lying — which is the exact false-assurance posture DR-085 exists to
#   correct. Conflict DETECTION stays a documented human / reasoning-agent duty,
#   backed by the recorded PR-template affirmation. This script only ensures the
#   duty FIRES at the moments it matters and is never silently skipped.
#
# THE RULE (DR-085 D1, verbatim intent):
#   Any build agent that detects two contradictory RATIFIED clauses on a
#   ONE-WAY-DOOR artifact MUST HALT and escalate — never silently resolve.
#   The motivating defect: the PR #57 silent T1-vs-P0-RATIFY-2 resolution.
#
# EXIT CODES:
#   0 — no one-way-door surface touched (nothing to remind about), OR reminder
#       emitted successfully. This gate is ADVISORY: it never fails CI. Its job
#       is to surface the duty, not to adjudicate the conflict it cannot see.
#
# Authority: 000-docs/087-AT-STND-ratified-clause-conflict-halt-gate-2026-06-18.md
#            000-docs/085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md (D1)
#
# Usage:
#   scripts/ratified-clause-conflict-check.sh                # diff vs origin/main (default)
#   scripts/ratified-clause-conflict-check.sh <base-ref>     # diff vs an explicit base ref
#   scripts/ratified-clause-conflict-check.sh --files f1 f2  # check an explicit file list

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# Path / content patterns that mark a ONE-WAY-DOOR surface. Deterministic,
# path-based — this is the reliable signal. (Conflict semantics are NOT here.)
# NOTE: paths come from `git diff --name-only`, which are ROOT-RELATIVE (no leading
# slash) — so the schema pattern is anchored `(^|/)schemas/`, NOT `/schemas/`.
ONE_WAY_DOOR_PATTERN='(predicate|skill-refiner-pass|gate-result|(^|/)schemas/.*\.schema\.json|skill[-_]?version|evals\.intentsolutions\.io|in-toto|attestation|\$schemaVersion|signing_mode|rekor)'

# Collect the changed-file list.
declare -a CHANGED=()
if [[ "${1:-}" == "--files" ]]; then
  shift
  CHANGED=("$@")
else
  BASE_REF="${1:-origin/main}"
  # Prefer a real merge-base diff; fall back to staged files if the ref is absent
  # (e.g. shallow clone with no origin/main). Never hard-fail on a missing ref.
  if git rev-parse --verify --quiet "${BASE_REF}" >/dev/null 2>&1; then
    mapfile -t CHANGED < <(git diff --name-only "$(git merge-base "${BASE_REF}" HEAD 2>/dev/null || echo "${BASE_REF}")" HEAD 2>/dev/null || true)
  fi
  # Always also include staged + unstaged working-tree changes (local pre-commit use).
  mapfile -t -O "${#CHANGED[@]}" CHANGED < <(git diff --name-only HEAD 2>/dev/null || true)
  mapfile -t -O "${#CHANGED[@]}" CHANGED < <(git diff --name-only --cached 2>/dev/null || true)
fi

# De-dupe + keep only files that still exist.
declare -a UNIQUE=()
declare -A SEEN=()
for f in ${CHANGED[@]+"${CHANGED[@]}"}; do
  [[ -n "${f}" ]] || continue
  [[ -n "${SEEN[$f]:-}" ]] && continue
  SEEN[$f]=1
  UNIQUE+=("${f}")
done

# Which changed files touch a one-way-door surface (by path)?
declare -a HITS=()
for f in ${UNIQUE[@]+"${UNIQUE[@]}"}; do
  [[ -n "${f}" ]] || continue
  if printf '%s' "${f}" | grep -qiE "${ONE_WAY_DOOR_PATTERN}"; then
    HITS+=("${f}")
  fi
done

if [[ ${#HITS[@]} -eq 0 ]]; then
  echo "ratified-clause-conflict-check: no one-way-door surface touched — no reminder needed."
  exit 0
fi

cat <<'REMINDER'

============================================================================
  RATIFIED-CLAUSE-CONFLICT HALT GATE (advisory reminder — DR-085 D1)
============================================================================

This change set touches a ONE-WAY-DOOR artifact (predicate / signed schema /
kernel entity). Before you implement it:

  1. Read the governing Decision Records for the artifact(s) below.
  2. Check whether two RATIFIED clauses contradict each other for this artifact
     (the DR-028 T1 line-105 "defer signing fields" vs P0-RATIFY-2 lines-233-236
     "add them now" contradiction is the canonical example).
  3. If you find a contradiction: HALT. Do NOT pick a side. Quote both clauses
     verbatim (source DR + line numbers) and escalate to the human decision-maker
     / convene a corrective ISEDC. Silently resolving it is the PR #57 defect this
     gate exists to prevent.

This script CANNOT detect the contradiction for you — that is a judgment task.
It only fires this reminder so the duty is never silently skipped.

Governing records:
  - 000-docs/085-AT-DECR-isedc-kernel-onewaydoor-correction-2026-06-17.md (D1)
  - 000-docs/087-AT-STND-ratified-clause-conflict-halt-gate-2026-06-18.md
  - 000-docs/082-AT-DECR-...predicate-uri... + its 086 erratum (predicate shape/freeze)
  - 000-docs/028-AT-DECR-...session-7... (the record with the T1/P0-RATIFY-2 conflict)

One-way-door files in this change set:
REMINDER

for f in "${HITS[@]}"; do
  echo "  - ${f}"
done
echo "============================================================================"
echo ""

# Advisory by design: surfacing the duty, not adjudicating the conflict. Exit 0.
exit 0
