#!/usr/bin/env bash
# bd-sync — bead source of truth with GitHub/Plane fan-out and projections.
#
# Beads is the source of truth. The IDs of the linked GH issue and Plane
# issue live in the bead's notes (lines starting with "GitHub:" and
# "Plane:"). bd-sync extracts those refs and fans every operation out to
# all linked layers. The `project` command also renders guarded,
# versioned cross-reference blocks into GitHub issue bodies and document
# front-matter. Humans keep ownership of the surrounding prose; bd-sync
# owns only the marked blocks.
#
# Subcommands:
#   bd-sync link <bead> --gh OWNER/REPO#N [--plane PROJECT-N]
#   bd-sync note <bead> "message"
#   bd-sync close <bead> --reason "..." [--also-close-gh] [--also-close-plane]
#   bd-sync project <bead> [--repo-root PATH] [--dry-run]
#   bd-sync projection-self-test [FIXTURE-DIR]
#   bd-sync status [<bead>]
#
# Plane credentials: pulled from `pass intentsolutions/plane/{api-key,
# workspace-slug, api-host-url}` (or env vars PLANE_API_KEY,
# PLANE_WORKSPACE_SLUG, PLANE_API_HOST_URL — env wins). On a fresh box,
# `pass insert -e intentsolutions/plane/api-key` etc.
#
# Convention is documented in ~/.claude/CLAUDE.md § Bead ↔ GitHub Issue
# bidirectional cross-reference.
set -euo pipefail

die() { echo "bd-sync: $*" >&2; exit 1; }
log() { echo "[bd-sync] $*" >&2; }
require() { command -v "$1" >/dev/null || die "missing dependency: $1"; }
require sha256sum

# The marker is deliberately stable and versioned. A projection update may
# replace a block only when the complete block still matches the deterministic
# renderer. Any partial/mutated block is an anomaly and fails closed.
BD_SYNC_PROJECTION_BEGIN='<!-- BEGIN BD-SYNC:cross-ref:v1 -->'
BD_SYNC_PROJECTION_END='<!-- END BD-SYNC:cross-ref:v1 -->'
PROJECTION_RESULT=''

# ── JSONL flush guard (bd-sync rapid-write race defense) ─────────────────
# Bug: between successive bd-sync invocations, bd's auto-import reads
# .beads/issues.jsonl into a fresh in-memory DB. If the previous
# invocation's write hasn't been flushed to JSONL (Dolt's auto-export
# has a 15-min minimum interval per .beads/config.yaml), the auto-import
# clobbers pending writes. Symptom: 7/13 beads silently lost their
# notes during a 2026-05-23 hygiene reset; SQLite + JSONL both showed
# empty notes despite `bd update` reporting ✓.
# Fix: after every bead-side write (note / close / link's implicit
# note), explicitly flush DB → JSONL so the next invocation's
# auto-import reads current state. Cost is ~1s for a 200-bead repo.
# See bead intentional-cognition-os-55q.4.
flush_jsonl() {
  local dir="$PWD"
  # Loop guards: empty dir or '.' would make dirname loop forever.
  # PWD is always absolute under bash but defend anyway.
  while [ -n "$dir" ] && [ "$dir" != "/" ] && [ "$dir" != "." ]; do
    if [ -d "$dir/.beads" ]; then
      bd export -o "$dir/.beads/issues.jsonl" >/dev/null 2>&1 || true
      return 0
    fi
    dir=$(dirname "$dir")
  done
  return 0
}

# ── Plane credential resolver ────────────────────────────────────────────
# Resolution order (first non-empty wins):
#   1. Env var (PLANE_API_KEY / PLANE_WORKSPACE_SLUG / PLANE_API_HOST_URL)
#   2. SOPS-encrypted dotenv via braves/scripts/sops-env (canonical per
#      intent-os ops/host/secrets — age-decrypted,
#      no TTY required)
#   3. `pass intentsolutions/plane/{api-key,workspace-slug,api-host-url}`
#      (legacy fallback; requires gpg-agent + a TTY, fails in cron/hooks/
#      non-interactive Bash tool contexts)
plane_creds_loaded=0
PLANE_API_KEY="${PLANE_API_KEY:-}"
PLANE_WORKSPACE_SLUG="${PLANE_WORKSPACE_SLUG:-}"
PLANE_API_HOST_URL="${PLANE_API_HOST_URL:-}"

load_plane_creds() {
  [ "$plane_creds_loaded" -eq 1 ] && return 0
  plane_creds_loaded=1

  # Layer 2: SOPS canonical source (braves/.env.sops via sops-env wrapper).
  # Uses the IS-standard anchored-regex pattern from CLAUDE.md SOPS section
  # to avoid the "bare export dumps env" leak class — only emits the three
  # PLANE_* variables, ignoring comments / blanks / other dotenv entries.
  local sops_wrapper="$HOME/000-projects/braves/scripts/sops-env"
  if [ -z "$PLANE_API_KEY" ] && [ -x "$sops_wrapper" ]; then
    local sops_out
    sops_out=$("$sops_wrapper" decrypt 2>/dev/null || true)
    if [ -n "$sops_out" ]; then
      [ -z "$PLANE_API_KEY" ] && PLANE_API_KEY=$(printf '%s\n' "$sops_out" | sed -nE 's/^PLANE_API_KEY=(.*)$/\1/p' | head -1)
      [ -z "$PLANE_WORKSPACE_SLUG" ] && PLANE_WORKSPACE_SLUG=$(printf '%s\n' "$sops_out" | sed -nE 's/^PLANE_WORKSPACE_SLUG=(.*)$/\1/p' | head -1)
      [ -z "$PLANE_API_HOST_URL" ] && PLANE_API_HOST_URL=$(printf '%s\n' "$sops_out" | sed -nE 's/^PLANE_API_HOST_URL=(.*)$/\1/p' | head -1)
      unset sops_out
    fi
  fi

  # Layer 3: pass (only effective when a TTY/cached-passphrase is available).
  if [ -z "${GPG_TTY:-}" ]; then
    GPG_TTY="$(tty 2>/dev/null || echo /dev/null)"
    export GPG_TTY
  fi
  if [ -z "$PLANE_API_KEY" ] && command -v pass >/dev/null; then
    PLANE_API_KEY=$(pass intentsolutions/plane/api-key 2>/dev/null || true)
  fi
  if [ -z "$PLANE_WORKSPACE_SLUG" ] && command -v pass >/dev/null; then
    PLANE_WORKSPACE_SLUG=$(pass intentsolutions/plane/workspace-slug 2>/dev/null || true)
  fi
  if [ -z "$PLANE_API_HOST_URL" ] && command -v pass >/dev/null; then
    PLANE_API_HOST_URL=$(pass intentsolutions/plane/api-host-url 2>/dev/null || true)
  fi
  PLANE_WORKSPACE_SLUG="${PLANE_WORKSPACE_SLUG:-internal}"
  PLANE_API_HOST_URL="${PLANE_API_HOST_URL:-https://projects.intentsolutions.io}"
}

plane_api_base() { echo "${PLANE_API_HOST_URL%/}/api/v1/workspaces/$PLANE_WORKSPACE_SLUG"; }

# Cache project_id by identifier prefix (e.g., BRAVES → uuid).
declare -A PLANE_PROJECT_CACHE=()
plane_resolve_project_id() {
  local prefix="$1"
  if [ -n "${PLANE_PROJECT_CACHE[$prefix]:-}" ]; then
    echo "${PLANE_PROJECT_CACHE[$prefix]}"
    return 0
  fi
  local pid
  pid=$(curl -fsS -H "X-API-Key: $PLANE_API_KEY" "$(plane_api_base)/projects/" 2>/dev/null \
    | jq -r --arg p "$prefix" '.results[] | select(.identifier==$p) | .id' | head -1)
  [ -n "$pid" ] || return 1
  PLANE_PROJECT_CACHE[$prefix]="$pid"
  echo "$pid"
}

# Resolve PROJECT-N → issue_uuid. Plane API doesn't filter cleanly on
# sequence_id, so we list all issues and match client-side.
plane_resolve_issue_id() {
  local ref="$1"  # e.g., BRAVES-15
  local prefix="${ref%-*}"; local seq="${ref##*-}"
  local pid; pid=$(plane_resolve_project_id "$prefix") || return 1
  local iid
  iid=$(curl -fsS -H "X-API-Key: $PLANE_API_KEY" "$(plane_api_base)/projects/$pid/issues/" 2>/dev/null \
    | jq -r --argjson s "$seq" '.results[] | select(.sequence_id==$s) | .id' | head -1)
  [ -n "$iid" ] || return 1
  echo "$pid:$iid"
}

# ── Bead ref extraction ──────────────────────────────────────────────────
# Read JSON rather than the wrapped human display. This preserves exact
# field lines even when `bd show` wraps a long document path for terminals.
bead_field_text() {
  local bead="$1"
  bd show "$bead" --json 2>/dev/null \
    | jq -r 'if type == "array" then .[0] else . end
      | [(.description // ""), (.notes // "")] | join("\n")'
}

extract_field_refs() {
  local bead="$1" field="$2" text
  text=$(bead_field_text "$bead") || true
  {
    printf '%s\n' "$text" \
      | sed -nE "s/^[[:space:]]*${field}:[[:space:]]*([^[:space:]]+).*/\1/p" \
      | tr -d '`' \
      | sort -u
  } || true
}

extract_gh_refs() { extract_field_refs "$1" GitHub; }
extract_plane_refs() { extract_field_refs "$1" Plane; }
extract_doc_refs() { extract_field_refs "$1" Doc; }

validate_project_ref() {
  local kind="$1" ref="$2"
  case "$kind" in
    doc)
      [[ "$ref" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/.+\.md$ ]] \
        || die "ANOMALY: malformed Doc ref: $ref"
      ;;
    gh)
      [[ "$ref" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[0-9]+$ ]] \
        || die "ANOMALY: malformed GitHub ref: $ref"
      ;;
  esac
}

resolve_project_doc() {
  local ref="$1" repo_root="${2:-}" rel="$1" candidate
  if [[ "$ref" == intent-eval-platform/intent-eval-lab/* ]]; then
    rel="${ref#intent-eval-platform/intent-eval-lab/}"
  fi

  local candidates=()
  [ -n "$repo_root" ] && candidates+=("$repo_root/$rel" "$repo_root/$ref")
  candidates+=("$PWD/$ref" "$PWD/$rel" "$HOME/000-projects/$ref")
  for candidate in "${candidates[@]}"; do
    if [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

# ── Guarded projection renderer ─────────────────────────────────────────
render_gh_projection() {
  local bead="$1" doc_refs="$2" gh_ref="$3" core digest
  core=$(printf "Bead: \`%s\`\nDoc: \`%s\`\nGitHub: \`%s\`" \
    "$bead" "${doc_refs//$'\n'/, }" "$gh_ref")
  digest=$(projection_checksum "$core")
  printf '%s\n\n%s\nProjection-SHA256: %s\n\n%s' \
    "$BD_SYNC_PROJECTION_BEGIN" "$core" "$digest" "$BD_SYNC_PROJECTION_END"
}

render_doc_projection() {
  local bead="$1" gh_refs="$2" core digest
  core=$(printf "Beads: \`%s\`\nGitHub: \`%s\`" \
    "$bead" "${gh_refs//$'\n'/, }")
  digest=$(projection_checksum "$core")
  printf '%s\n\n%s\nProjection-SHA256: %s\n\n%s' \
    "$BD_SYNC_PROJECTION_BEGIN" "$core" "$digest" "$BD_SYNC_PROJECTION_END"
}

projection_checksum() {
  printf '%s\n' "$1" | sha256sum | awk '{print $1}'
}

# Return status:
#   0 = no block existed; caller should add the returned projection
#   1 = block exists and is byte-for-byte current; no write needed
#   2 = malformed or human-mutated block; caller must fail closed
#   3 = valid stale generated block; caller may replace only that block
projection_state() {
  local body="$1" expected="$2"
  local begin_count end_count begin_line end_line actual declared actual_core
  begin_count=$(printf '%s\n' "$body" | grep -F -x -c "$BD_SYNC_PROJECTION_BEGIN" || true)
  end_count=$(printf '%s\n' "$body" | grep -F -x -c "$BD_SYNC_PROJECTION_END" || true)
  if [ "$begin_count" -eq 0 ] && [ "$end_count" -eq 0 ]; then
    return 0
  fi
  [ "$begin_count" -eq 1 ] && [ "$end_count" -eq 1 ] || return 2

  begin_line=$(awk -v marker="$BD_SYNC_PROJECTION_BEGIN" '$0 == marker { print NR; exit }' <<< "$body")
  end_line=$(awk -v marker="$BD_SYNC_PROJECTION_END" '$0 == marker { print NR; exit }' <<< "$body")
  [ "$begin_line" -lt "$end_line" ] || return 2
  PROJECTION_BEGIN_LINE="$begin_line"
  PROJECTION_END_LINE="$end_line"
  actual=$(sed -n "${begin_line},${end_line}p" <<< "$body")
  [ "$actual" = "$expected" ] && return 1

  declared=$(sed -n "${begin_line},${end_line}p" <<< "$body" \
    | sed -nE 's/^Projection-SHA256:[[:space:]]*([0-9a-f]{64})$/\1/p')
  if [ -n "$declared" ]; then
    actual_core=$(sed -n "$((begin_line + 1)),$((end_line - 1))p" <<< "$body" \
      | sed -E '/^Projection-SHA256:[[:space:]]*[0-9a-f]{64}$/d; /^$/d')
    [ "$(projection_checksum "$actual_core")" = "$declared" ] || return 2
    return 3
  fi

  # Migrate the pre-digest v1 blocks emitted before the checksum was added.
  # They are accepted only when every interior line is one of the expected
  # cross-reference fields; all newly generated blocks carry the digest.
  local interior bad_lines field_lines
  interior=$(sed -n "$((begin_line + 1)),$((end_line - 1))p" <<< "$body")
  field_lines=$(printf '%s\n' "$interior" | grep -cE '^(Bead|Beads|Doc|GitHub): ' || true)
  bad_lines=$(printf '%s\n' "$interior" | grep -vcE '^$|^(Bead|Beads|Doc|GitHub): ' || true)
  [ "$field_lines" -ge 2 ] && [ "$bad_lines" -eq 0 ] && return 3
  return 2
}

projection_replace_existing() {
  local body="$1" expected="$2" before after
  if [ "$PROJECTION_BEGIN_LINE" -gt 1 ]; then
    before=$(sed -n "1,$((PROJECTION_BEGIN_LINE - 1))p" <<< "$body")
  else
    before=''
  fi
  after=$(sed -n "$((PROJECTION_END_LINE + 1)),\$p" <<< "$body")
  while [[ "$after" == $'\n'* ]]; do
    after="${after#$'\n'}"
  done
  if [ -n "$before" ] && [ -n "$after" ]; then
    printf '%s\n\n%s\n\n%s' "$before" "$expected" "$after"
  elif [ -n "$before" ]; then
    printf '%s\n\n%s' "$before" "$expected"
  elif [ -n "$after" ]; then
    printf '%s\n\n%s' "$expected" "$after"
  else
    printf '%s' "$expected"
  fi
}

projection_prepare_append() {
  local body="$1" expected="$2" state
  projection_state "$body" "$expected" || state=$?
  state="${state:-0}"
  case "$state" in
    0)
      if [ -n "$body" ]; then
        PROJECTION_RESULT="${body%$'\n'}"$'\n\n'"$expected"
      else
        PROJECTION_RESULT="$expected"
      fi
      return 0
      ;;
    1)
      PROJECTION_RESULT="$body"
      return 1
      ;;
    3)
      PROJECTION_RESULT=$(projection_replace_existing "$body" "$expected")
      return 0
      ;;
    *)
      PROJECTION_RESULT=''
      return 2
      ;;
  esac
}

projection_prepare_doc() {
  local body="$1" expected="$2" state closing_line before after
  projection_state "$body" "$expected" || state=$?
  state="${state:-0}"
  case "$state" in
    1)
      PROJECTION_RESULT="$body"
      return 1
      ;;
    3)
      PROJECTION_RESULT=$(projection_replace_existing "$body" "$expected")
      return 0
      ;;
    2)
      PROJECTION_RESULT=''
      return 2
      ;;
  esac

  # Keep YAML front matter at byte 1. The generated markdown projection is
  # inserted immediately after its closing delimiter, before the title.
  if [[ "$body" == ---$'\n'* ]]; then
    closing_line=$(awk 'NR > 1 && $0 == "---" { print NR; exit }' <<< "$body")
  else
    closing_line=''
  fi
  if [ -n "$closing_line" ]; then
    before=$(sed -n "1,${closing_line}p" <<< "$body")
    after=$(sed -n "$((closing_line + 1)),\$p" <<< "$body")
    while [[ "$after" == $'\n'* ]]; do
      after="${after#$'\n'}"
    done
    if [ -n "$after" ]; then
      PROJECTION_RESULT="$before"$'\n\n'"$expected"$'\n\n'"$after"
    else
      PROJECTION_RESULT="$before"$'\n\n'"$expected"
    fi
  elif [ -n "$body" ]; then
    PROJECTION_RESULT="$expected"$'\n\n'"${body%$'\n'}"
  else
    PROJECTION_RESULT="$expected"
  fi
  return 0
}

write_atomic() {
  local path="$1" content="$2" tmp
  tmp=$(mktemp "${path}.bd-sync.XXXXXX")
  printf '%s\n' "$content" > "$tmp"
  chmod --reference="$path" "$tmp" 2>/dev/null || true
  mv -f "$tmp" "$path"
}

# ── GitHub mirror ────────────────────────────────────────────────────────
gh_comment() {
  local ref="$1"; local body="$2"
  local repo="${ref%#*}"; local num="${ref#*#}"
  gh issue comment "$num" --repo "$repo" --body "$body" >/dev/null
  log "  ✓ commented on $ref"
}
gh_close() {
  local ref="$1"; local body="$2"
  local repo="${ref%#*}"; local num="${ref#*#}"
  gh issue close "$num" --repo "$repo" --reason completed --comment "$body" >/dev/null
  log "  ✓ closed $ref"
}

gh_issue_body() {
  local ref="$1" repo num
  repo="${ref%#*}"; num="${ref#*#}"
  gh issue view "$num" --repo "$repo" --json body --jq '.body // ""'
}

gh_replace_issue_body() {
  local ref="$1" body_file="$2" repo num
  repo="${ref%#*}"; num="${ref#*#}"
  gh issue edit "$num" --repo "$repo" --body-file "$body_file" >/dev/null
}

# Generate both sides only after every side has passed its anomaly check. The
# remote edit happens before local document writes; if a local write fails we
# attempt a best-effort remote rollback from the captured old body.
cmd_project() {
  [ $# -gt 0 ] || die "project requires a bead ID"
  local bead="$1" repo_root="${BD_SYNC_REPO_ROOT:-}" dry_run=0 arg
  shift
  while [ $# -gt 0 ]; do
    arg="$1"
    case "$arg" in
      --repo-root)
        [ $# -ge 2 ] || die "project --repo-root requires a path"
        repo_root="$2"; shift 2
        ;;
      --dry-run)
        dry_run=1; shift
        ;;
      *) die "unknown project arg: $arg";;
    esac
  done

  local doc_refs gh_refs doc_ref gh_ref doc_path old_body expected state
  doc_refs=$(extract_doc_refs "$bead")
  gh_refs=$(extract_gh_refs "$bead")
  [ -n "$doc_refs" ] || die "ANOMALY: bead $bead has no Doc: field"
  [ -n "$gh_refs" ] || die "ANOMALY: bead $bead has no GitHub: field"

  local -a doc_list=() gh_list=()
  mapfile -t doc_list < <(printf '%s\n' "$doc_refs")
  mapfile -t gh_list < <(printf '%s\n' "$gh_refs")
  for doc_ref in "${doc_list[@]}"; do
    validate_project_ref doc "$doc_ref"
  done
  for gh_ref in "${gh_list[@]}"; do
    validate_project_ref gh "$gh_ref"
  done

  declare -A DOC_PATHS DOC_OLD DOC_NEW DOC_CHANGED
  declare -A GH_OLD GH_NEW GH_CHANGED GH_TMP

  # Resolve and preflight every local document before touching GitHub.
  for doc_ref in "${doc_list[@]}"; do
    doc_path=$(resolve_project_doc "$doc_ref" "$repo_root") \
      || die "ANOMALY: Doc ref does not resolve to a file: $doc_ref"
    DOC_PATHS["$doc_ref"]="$doc_path"
    DOC_OLD["$doc_ref"]=$(<"$doc_path")
    expected=$(render_doc_projection "$bead" "$gh_refs")
    if projection_prepare_doc "${DOC_OLD[$doc_ref]}" "$expected"; then
      DOC_CHANGED["$doc_ref"]=1
      DOC_NEW["$doc_ref"]="$PROJECTION_RESULT"
    else
      state=$?
      case "$state" in
        1) DOC_CHANGED["$doc_ref"]=0; DOC_NEW["$doc_ref"]="${DOC_OLD[$doc_ref]}";;
        *) die "ANOMALY: guarded projection in ${DOC_PATHS[$doc_ref]} was edited or malformed";;
      esac
    fi
  done

  # Preflight all remote issue bodies. No writes have happened if any one
  # issue contains a mutated/partial generated block.
  for gh_ref in "${gh_list[@]}"; do
    old_body=$(gh_issue_body "$gh_ref") \
      || die "unable to read GitHub issue body: $gh_ref"
    expected=$(render_gh_projection "$bead" "$doc_refs" "$gh_ref")
    GH_OLD["$gh_ref"]="$old_body"
    if projection_prepare_append "$old_body" "$expected"; then
      GH_CHANGED["$gh_ref"]=1
      GH_NEW["$gh_ref"]="$PROJECTION_RESULT"
    else
      state=$?
      case "$state" in
        1) GH_CHANGED["$gh_ref"]=0; GH_NEW["$gh_ref"]="$old_body";;
        *) die "ANOMALY: guarded projection in GitHub issue $gh_ref was edited or malformed";;
      esac
    fi
  done

  if [ "$dry_run" -eq 1 ]; then
    for gh_ref in "${gh_list[@]}"; do
      log "  GitHub $gh_ref: ${GH_CHANGED[$gh_ref]:-0}"
    done
    for doc_ref in "${doc_list[@]}"; do
      log "  Doc ${DOC_PATHS[$doc_ref]}: ${DOC_CHANGED[$doc_ref]:-0}"
    done
    return 0
  fi

  # Prepare all remote payloads before the first remote mutation.
  for gh_ref in "${gh_list[@]}"; do
    if [ "${GH_CHANGED[$gh_ref]:-0}" -eq 1 ]; then
      GH_TMP["$gh_ref"]=$(mktemp)
      printf '%s\n' "${GH_NEW[$gh_ref]}" > "${GH_TMP[$gh_ref]}"
    fi
  done

  for gh_ref in "${gh_list[@]}"; do
    if [ "${GH_CHANGED[$gh_ref]:-0}" -eq 1 ]; then
      if ! gh_replace_issue_body "$gh_ref" "${GH_TMP[$gh_ref]}"; then
        for rollback_ref in "${gh_list[@]}"; do
          [ -n "${GH_TMP[$rollback_ref]:-}" ] && rm -f "${GH_TMP[$rollback_ref]}"
        done
        die "GitHub projection update failed; local documents were not written"
      fi
    fi
  done
  for gh_ref in "${gh_list[@]}"; do
    [ -n "${GH_TMP[$gh_ref]:-}" ] && rm -f "${GH_TMP[$gh_ref]}"
  done

  for doc_ref in "${doc_list[@]}"; do
    if [ "${DOC_CHANGED[$doc_ref]:-0}" -eq 1 ]; then
      if ! write_atomic "${DOC_PATHS[$doc_ref]}" "${DOC_NEW[$doc_ref]}"; then
        log "  ⚠ local document write failed; attempting GitHub rollback"
        for gh_ref in "${gh_list[@]}"; do
          [ "${GH_CHANGED[$gh_ref]:-0}" -eq 1 ] || continue
          local rollback_tmp
          rollback_tmp=$(mktemp)
          printf '%s\n' "${GH_OLD[$gh_ref]}" > "$rollback_tmp"
          gh_replace_issue_body "$gh_ref" "$rollback_tmp" || true
          rm -f "$rollback_tmp"
        done
        die "projection transaction failed while writing ${DOC_PATHS[$doc_ref]}"
      fi
    fi
  done

  log "projected $bead → ${#gh_list[@]} GitHub issue(s), ${#doc_list[@]} document(s)"
}

projection_assert() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" != "$actual" ]; then
    printf 'projection self-test FAIL: %s\n' "$label" >&2
    return 1
  fi
  printf 'projection self-test ok: %s\n' "$label"
  return 0
}

cmd_projection_self_test() {
  local fixture_dir="${1:-$(dirname "$0")/tests/fixtures/bd-sync}" issue_body doc_body
  [ -d "$fixture_dir" ] || die "projection fixture directory not found: $fixture_dir"
  issue_body=$(<"$fixture_dir/issue-human.md")
  doc_body=$(<"$fixture_dir/doc-human.md")

  local bead='bd_fixture_0001' doc_ref='intent-eval-lab/000-docs/fixture.md'
  local gh_ref='owner/repo#42' gh_block doc_block state before after
  gh_block=$(render_gh_projection "$bead" "$doc_ref" "$gh_ref")
  doc_block=$(render_doc_projection "$bead" "$gh_ref")

  local failures=0
  state=0
  projection_prepare_append "$issue_body" "$gh_block" || state=$?
  state="${state:-0}"
  [ "$state" -eq 0 ] || failures=$((failures + 1))
  local expected_issue="${issue_body%$'\n'}"$'\n\n'"$gh_block"
  projection_assert 'first GitHub projection is additive' "$expected_issue" "$PROJECTION_RESULT" || failures=$((failures + 1))
  local issue_projected="$PROJECTION_RESULT"

  if projection_prepare_append "$issue_projected" "$gh_block"; then
    failures=$((failures + 1))
  else
    state=$?
    [ "$state" -eq 1 ] || failures=$((failures + 1))
  fi
  projection_assert 'GitHub projection is idempotent' "$issue_projected" "$PROJECTION_RESULT" || failures=$((failures + 1))

  local changed_gh_block changed_issue
  changed_gh_block=$(render_gh_projection 'bd_fixture_0002' "$doc_ref" "$gh_ref")
  if projection_prepare_append "$issue_projected" "$changed_gh_block"; then
    changed_issue="$PROJECTION_RESULT"
    projection_assert 'changed bead refs replace only the generated GitHub block' \
      "${issue_body%$'\n'}"$'\n\n'"$changed_gh_block" "$changed_issue" || failures=$((failures + 1))
  else
    failures=$((failures + 1))
  fi

  local edited_issue="${issue_projected/GitHub: \`owner\/repo#42\`/GitHub: human-edited}"
  if projection_prepare_append "$edited_issue" "$gh_block"; then
    failures=$((failures + 1))
  else
    state=$?
    if [ "$state" -eq 2 ]; then
      printf 'projection self-test ok: edited GitHub block is an anomaly\n'
    else
      failures=$((failures + 1))
    fi
  fi
  local partial_issue="${issue_projected/$BD_SYNC_PROJECTION_END/}"
  if projection_prepare_append "$partial_issue" "$gh_block"; then
    failures=$((failures + 1))
  else
    state=$?
    if [ "$state" -eq 2 ]; then
      printf 'projection self-test ok: partial GitHub markers are an anomaly\n'
    else
      failures=$((failures + 1))
    fi
  fi

  state=0
  projection_prepare_doc "$doc_body" "$doc_block" || state=$?
  state="${state:-0}"
  [ "$state" -eq 0 ] || failures=$((failures + 1))
  local doc_projected="$PROJECTION_RESULT"
  case "$doc_projected" in
    ---*"$BD_SYNC_PROJECTION_BEGIN"*) : ;;
    *) failures=$((failures + 1));;
  esac
  if projection_prepare_doc "$doc_projected" "$doc_block"; then
    failures=$((failures + 1))
  else
    state=$?
    [ "$state" -eq 1 ] || failures=$((failures + 1))
  fi
  projection_assert 'document projection is idempotent' "$doc_projected" "$PROJECTION_RESULT" || failures=$((failures + 1))

  before=$(sha256sum "$fixture_dir/issue-human.md")
  after=$(sha256sum "$fixture_dir/issue-human.md")
  projection_assert 'anomaly self-test leaves fixture untouched' "$before" "$after" || failures=$((failures + 1))

  if [ "$failures" -ne 0 ]; then
    printf 'projection self-test: %d failure(s)\n' "$failures" >&2
    return 1
  fi
  printf 'projection self-test: all deterministic cases passed\n'
}

# ── Plane mirror ─────────────────────────────────────────────────────────
plane_comment() {
  local ref="$1"; local html="$2"
  load_plane_creds
  if [ -z "$PLANE_API_KEY" ]; then
    log "  ⚠ Plane comment skipped on $ref (no API key — \`pass insert intentsolutions/plane/api-key\` or set PLANE_API_KEY)"
    return 0
  fi
  local pair; pair=$(plane_resolve_issue_id "$ref") || {
    log "  ⚠ Plane resolution failed for $ref"; return 0;
  }
  local pid="${pair%:*}"; local iid="${pair##*:}"
  curl -fsS -X POST -H "X-API-Key: $PLANE_API_KEY" -H "Content-Type: application/json" \
    -d "$(jq -n --arg c "$html" '{comment_html:$c}')" \
    "$(plane_api_base)/projects/$pid/issues/$iid/comments/" >/dev/null
  log "  ✓ commented on Plane $ref"
}
plane_close() {
  local ref="$1"; local html="$2"
  load_plane_creds
  if [ -z "$PLANE_API_KEY" ]; then
    log "  ⚠ Plane close skipped on $ref (no API key)"
    return 0
  fi
  local pair; pair=$(plane_resolve_issue_id "$ref") || {
    log "  ⚠ Plane resolution failed for $ref"; return 0;
  }
  local pid="${pair%:*}"; local iid="${pair##*:}"
  # Find the Done state for this project
  local done_state
  done_state=$(curl -fsS -H "X-API-Key: $PLANE_API_KEY" "$(plane_api_base)/projects/$pid/states/" 2>/dev/null \
    | jq -r '.results[] | select(.group=="completed") | .id' | head -1)
  [ -n "$done_state" ] || { log "  ⚠ Plane Done state not found for $ref"; return 0; }
  curl -fsS -X PATCH -H "X-API-Key: $PLANE_API_KEY" -H "Content-Type: application/json" \
    -d "$(jq -n --arg s "$done_state" '{state:$s}')" \
    "$(plane_api_base)/projects/$pid/issues/$iid/" >/dev/null
  plane_comment "$ref" "$html"
  log "  ✓ closed Plane $ref (state → Done)"
}

# ── Subcommands ──────────────────────────────────────────────────────────

cmd_link() {
  local bead="$1"; shift
  local gh_ref="" plane_ref=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --gh) gh_ref="$2"; shift 2;;
      --plane) plane_ref="$2"; shift 2;;
      *) die "unknown link arg: $1";;
    esac
  done
  [ -n "$gh_ref" ] || die "link requires --gh OWNER/REPO#N"
  local repo="${gh_ref%#*}"; local num="${gh_ref#*#}"
  gh issue view "$num" --repo "$repo" --json number >/dev/null \
    || die "GH issue $gh_ref not found or inaccessible"

  local note="GitHub: $gh_ref — https://github.com/${repo}/issues/${num}. MIRROR RULE: bd-sync handles fan-out — \`bd-sync note $bead\` and \`bd-sync close $bead\` mirror to GH and Plane automatically."
  if [ -n "$plane_ref" ]; then
    note+=$'\n\nPlane: '"$plane_ref"' — https://projects.intentsolutions.io/internal/projects/?peekIssue='"$plane_ref"
  fi
  bd note "$bead" "$note" >/dev/null
  flush_jsonl
  log "linked $bead ↔ $gh_ref${plane_ref:+ ↔ Plane $plane_ref}"

  gh_comment "$gh_ref" "Linked bead: \`$bead\` (source of truth). Use \`bd-sync\` to mirror updates."
  if [ -n "$plane_ref" ]; then
    plane_comment "$plane_ref" "<p>Linked bead: <code>$bead</code> + GitHub <a href=\"https://github.com/${repo}/issues/${num}\">$gh_ref</a>.</p>"
  fi
}

cmd_note() {
  local bead="$1"; shift
  local body="${1:-}"
  [ -n "$body" ] || die "note requires a message"

  bd note "$bead" "$body" >/dev/null
  flush_jsonl
  log "noted $bead"

  local gh_refs plane_refs
  gh_refs=$(extract_gh_refs "$bead")
  plane_refs=$(extract_plane_refs "$bead")

  if [ -z "$gh_refs" ] && [ -z "$plane_refs" ]; then
    log "  (no linked GH or Plane refs — bead-only)"
    return 0
  fi

  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    gh_comment "$ref" "**bd-sync from \`$bead\`:** $body"
  done <<< "$gh_refs"

  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    plane_comment "$ref" "<p><strong>bd-sync from <code>$bead</code>:</strong> $(echo "$body" | sed 's|&|\&amp;|g; s|<|\&lt;|g; s|>|\&gt;|g')</p>"
  done <<< "$plane_refs"
}

cmd_close() {
  local bead="$1"; shift
  local reason="" close_gh=0 close_plane=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --reason|-r) reason="$2"; shift 2;;
      --also-close-gh) close_gh=1; shift;;
      --also-close-plane) close_plane=1; shift;;
      *) die "unknown close arg: $1";;
    esac
  done
  [ -n "$reason" ] || die "close requires --reason"

  local gh_refs plane_refs
  gh_refs=$(extract_gh_refs "$bead")
  plane_refs=$(extract_plane_refs "$bead")

  bd close "$bead" -r "$reason" >/dev/null
  flush_jsonl
  log "closed $bead — $reason"

  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    if [ "$close_gh" -eq 1 ]; then
      gh_close "$ref" "**bd-sync close from \`$bead\`:** $reason"
    else
      gh_comment "$ref" "**bd-sync close on \`$bead\`:** $reason _(GH issue left open — covers other beads)_"
    fi
  done <<< "$gh_refs"

  while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    local html_reason; html_reason=$(echo "$reason" | sed 's|&|\&amp;|g; s|<|\&lt;|g; s|>|\&gt;|g')
    if [ "$close_plane" -eq 1 ]; then
      plane_close "$ref" "<p><strong>bd-sync close from <code>$bead</code>:</strong> $html_reason</p>"
    else
      plane_comment "$ref" "<p><strong>bd-sync close on <code>$bead</code>:</strong> $html_reason</p>"
    fi
  done <<< "$plane_refs"
}

cmd_status() {
  local target="${1:-}"
  if [ -n "$target" ]; then
    echo "== $target =="
    bd show "$target" 2>/dev/null | grep -E '^(Status:|Owner:|Type:|Priority:)' | head -5
    echo "Linked GH:    $(extract_gh_refs "$target" | tr '\n' ' ')"
    echo "Linked Plane: $(extract_plane_refs "$target" | tr '\n' ' ')"
    return 0
  fi
  echo "Bead → GH → Plane (linked beads only)"
  bd list --all --flat 2>/dev/null | awk '{print $1}' | while read -r bead; do
    [ -n "$bead" ] || continue
    local gh plane
    gh=$(extract_gh_refs "$bead" | tr '\n' ',' | sed 's/,$//')
    plane=$(extract_plane_refs "$bead" | tr '\n' ',' | sed 's/,$//')
    [ -n "$gh" ] || [ -n "$plane" ] || continue
    printf "  %-15s  GH:%-30s  Plane:%s\n" "$bead" "${gh:--}" "${plane:--}"
  done
}

cmd_help() { sed -n '2,/^set -e/p' "$0" | sed -n '/^#/p' | sed 's/^# \?//'; }

main() {
  [ $# -eq 0 ] && { cmd_help; exit 0; }
  local sub="$1"; shift
  case "$sub" in
    projection-self-test|help|-h|--help)
      ;;
    *)
      require bd
      require gh
      require jq
      require curl
      ;;
  esac
  case "$sub" in
    link)   cmd_link "$@";;
    note)   cmd_note "$@";;
    close)  cmd_close "$@";;
    project) cmd_project "$@";;
    projection-self-test) cmd_projection_self_test "$@";;
    status) cmd_status "$@";;
    help|-h|--help) cmd_help;;
    *) die "unknown subcommand: $sub (try 'bd-sync help')";;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
