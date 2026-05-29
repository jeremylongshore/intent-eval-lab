#!/usr/bin/env bash
# validate-trilink.sh — Plan 027 § 5.5 tri-link verifier (AC-12 enforcement)
#
# Three checks (label-scoped to `refiner` only — legacy work exempt):
#   1. MISS-DOC / MISS-GH    — every refiner-labeled bead carries Doc: + GitHub: lines
#   2. MISS-FRONT             — every 000-docs/*.md citing bd_000-projects-* carries Beads: front-matter row
#   3. MISS-GH-BEAD / MISS-GH-DOC — every refiner-labeled GH issue carries Bead: + Doc: lines
#
# Exit non-zero on any violation. Used by Step 3 + CI .github/workflows/trilink.yml per repo.

set -u

# ---- config ----
# Resolve paths from script location (CI-portable; no hardcoded /home/jeremy).
# Script lives at intent-eval-platform/intent-eval-lab/scripts/validate-trilink.sh
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IEP_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"         # intent-eval-platform/
UMBRELLA="$(cd -- "$IEP_ROOT/.." && pwd)"              # ~/000-projects/ (bd workspace root)
REPOS=(intent-eval-lab intent-eval-core j-rig-binary-eval audit-harness intent-rollout-gate)
GH_REPOS=(
  jeremylongshore/intent-eval-lab
  jeremylongshore/intent-eval-core
  jeremylongshore/j-rig-skill-binary-eval
  jeremylongshore/intent-audit-harness
  jeremylongshore/intent-rollout-gate
)

VIOLATIONS=0
report() {
  echo "$@"
  VIOLATIONS=$((VIOLATIONS+1))
}

# ---- check 1: bead → Doc/GH presence ----
check_beads() {
  echo "=== Check 1: bead → Doc/GitHub presence (label:refiner) ==="
  cd "$UMBRELLA"
  # Get refiner-labeled bead IDs
  local ids
  ids=$(bd list --label refiner --status open --json 2>/dev/null | jq -r '.[].id' 2>/dev/null \
        || bd list --label refiner --status open 2>/dev/null | grep -oE 'bd_000-projects-[a-z0-9]+(\.[0-9]+)?' | sort -u)
  if [ -z "$ids" ]; then
    echo "  (no refiner-labeled open beads found — skipping)"
    return
  fi
  local n=0
  for id in $ids; do
    # Whitelist bead id format — prevents arg-injection if `bd list` output is ever malformed.
    [[ "$id" =~ ^bd_000-projects-[a-z0-9]+(\.[0-9]+)?$ ]] || { report "MISS-BEAD-ID  $id  (rejected — not a valid bd id format)"; continue; }
    n=$((n+1))
    local desc
    # Strip CR to defend against Windows line-endings in description content.
    desc=$(bd show "$id" 2>/dev/null | tr -d '\r')
    if ! printf '%s\n' "$desc" | grep -qE '^Doc:[[:space:]]+'; then
      report "MISS-DOC  $id  (no 'Doc:' line in description)"
    fi
    if ! printf '%s\n' "$desc" | grep -qE '^GitHub:[[:space:]]+'; then
      report "MISS-GH   $id  (no 'GitHub:' line in description)"
    fi
  done
  echo "  ($n beads checked)"
}

# ---- check 2: doc → Bead front-matter row presence ----
# Scope per plan § 11 non-goal: ONLY Skill Refiner-labeled docs (filename contains
# 'skill-refiner' or 'refiner', or doc cites a bd ID that is refiner-labeled).
# Legacy docs citing other bd IDs are exempt.
check_docs() {
  echo "=== Check 2: doc → Bead front-matter row (Skill Refiner-scoped only) ==="
  local n=0
  for repo in "${REPOS[@]}"; do
    local repo_path="$IEP_ROOT/$repo/000-docs"
    [ -d "$repo_path" ] || continue
    while IFS= read -r -d '' doc; do
      local fn=$(basename "$doc")
      # In-scope only if filename matches Skill Refiner pattern
      case "$fn" in
        *skill-refiner*|*refiner*) ;;
        *) continue ;;
      esac
      grep -lE 'bd_000-projects-[a-z0-9]+' "$doc" >/dev/null 2>&1 || continue
      n=$((n+1))
      if ! head -50 "$doc" | grep -qE '^\|[[:space:]]*Beads[[:space:]]*\|' && \
         ! head -50 "$doc" | grep -qE '^Beads:[[:space:]]+'; then
        report "MISS-FRONT  ${doc#$IEP_ROOT/}  (cites bd_000-projects-* but no front-matter Beads row)"
      fi
    done < <(find -P "$repo_path" -maxdepth 1 -name '*.md' -print0)
  done
  echo "  ($n Skill-Refiner-scoped docs checked; legacy docs exempt per plan § 11)"
}

# ---- check 3: GH issue → Bead/Doc presence ----
# NOTE: at scale, --limit 100 per repo × 5 repos × 2 calls each = up to 1000 GH API
# calls per run. GitHub authenticated rate limit is 5000/hour. Raise the limit only
# when the refiner label regularly exceeds 100 open issues.
check_gh() {
  echo "=== Check 3: GH issue → Bead/Doc body lines (label:refiner) ==="
  if ! command -v gh >/dev/null 2>&1; then
    report "MISS-GH-CLI  gh not installed; skipping GH-side check"
    return
  fi
  # P0 — without an explicit auth pre-flight, an unauthenticated `gh` silently
  # produces no output, the `|| echo ''` fallback short-circuits the loop, and
  # check 3 returns a false PASS with zero issues checked.
  if ! gh auth status >/dev/null 2>&1; then
    report "MISS-GH-AUTH  gh is installed but not authenticated; Check 3 cannot run"
    return
  fi
  local n=0
  for repo in "${GH_REPOS[@]}"; do
    local nums
    nums=$(gh issue list --repo "$repo" --label refiner --state open --json number --limit 100 -q '.[].number' 2>/dev/null || echo '')
    [ -z "$nums" ] && continue
    for num in $nums; do
      # Whitelist GH issue number — prevents arg-injection (e.g., a token like `--json` flowing
      # from a corrupted `gh` response would be passed as a flag to `gh issue view`).
      [[ "$num" =~ ^[0-9]+$ ]] || { report "MISS-GH-NUM  $repo: rejected non-numeric issue token '$num'"; continue; }
      n=$((n+1))
      # Fetch body as raw text and strip CR to defend against Windows line-endings.
      local body
      body=$(gh issue view "$num" --repo "$repo" --json body -q .body 2>/dev/null | tr -d '\r' || echo '')
      if ! printf '%s\n' "$body" | grep -qE '^Bead:[[:space:]]+'; then
        report "MISS-GH-BEAD  $repo#$num  (no 'Bead:' line in body)"
      fi
      if ! printf '%s\n' "$body" | grep -qE '^Doc:[[:space:]]+'; then
        report "MISS-GH-DOC   $repo#$num  (no 'Doc:' line in body)"
      fi
    done
  done
  echo "  ($n GH issues checked across ${#GH_REPOS[@]} repos)"
}

# ---- run ----
check_beads
check_docs
check_gh

echo ""
echo "=== Summary ==="
if [ "$VIOLATIONS" -eq 0 ]; then
  echo "PASS — zero tri-linkage violations"
  exit 0
else
  echo "FAIL — $VIOLATIONS violation(s)"
  exit 1
fi
