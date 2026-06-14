#!/usr/bin/env bash
#
# coherence-check.sh — read-only coherence verification for the Intent Eval
# Platform (IEP) managed repos.
#
# For each of the 5 managed IEP repos listed in ecosystem/ecosystem.json this
# script verifies, WITHOUT mutating anything:
#   1. the repo's working copy is present on disk,
#   2. its @intentsolutions/core schema pin matches the manifest,
#   3. its @intentsolutions/audit-harness pin matches the manifest
#      (npm devDependency or vendored .audit-harness/VERSION),
#   4. the audit-harness verb resolves (vendored wrapper present, or the
#      npm dep is installed in node_modules).
#
# It is strictly read-only: no installs, no writes, no git operations, no
# network. It only reads package.json / .audit-harness/VERSION and checks
# for the presence of node_modules / wrapper scripts.
#
# claude-code-plugins is DEFERRED (deferred-pending-CCP-study, bead 3wt1f) and
# is intentionally NOT checked here — it carries no ecosystem-sync automation.
#
# Usage:
#   ecosystem/coherence-check.sh [--root <iep-umbrella-dir>] [--manifest <path>]
#
#   --root      Umbrella dir that contains the sibling repos.
#               Default: auto-detected (parent of intent-eval-lab's repo root).
#   --manifest  Path to ecosystem.json. Default: alongside this script.
#
# Exit codes: 0 = all PASS, 1 = one or more FAIL, 2 = setup error.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/ecosystem.json"
ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)     ROOT="${2:-}"; shift 2 ;;
    --manifest) MANIFEST="${2:-}"; shift 2 ;;
    -h|--help)
      grep '^#' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "coherence-check: unknown argument '$1'" >&2
      exit 2
      ;;
  esac
done

command -v jq >/dev/null 2>&1 || { echo "coherence-check: jq is required" >&2; exit 2; }

if [[ ! -f "${MANIFEST}" ]]; then
  echo "coherence-check: manifest not found at ${MANIFEST}" >&2
  exit 2
fi

if ! jq empty "${MANIFEST}" >/dev/null 2>&1; then
  echo "coherence-check: manifest is not valid JSON: ${MANIFEST}" >&2
  exit 2
fi

# Resolve the umbrella root if not supplied. The lab repo (this script's home)
# lives at <root>/intent-eval-lab/ecosystem/, so the umbrella is three levels up.
if [[ -z "${ROOT}" ]]; then
  ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
fi

if [[ ! -d "${ROOT}" ]]; then
  echo "coherence-check: umbrella root not found at ${ROOT}" >&2
  exit 2
fi

GREEN=""; RED=""; YELLOW=""; BOLD=""; RESET=""
if [[ -t 1 ]]; then
  GREEN="$(printf '\033[32m')"; RED="$(printf '\033[31m')"
  YELLOW="$(printf '\033[33m')"; BOLD="$(printf '\033[1m')"; RESET="$(printf '\033[0m')"
fi

PASS_COUNT=0
FAIL_COUNT=0

pass() { printf '  %sPASS%s %s\n' "${GREEN}" "${RESET}" "$1"; PASS_COUNT=$((PASS_COUNT + 1)); }
fail() { printf '  %sFAIL%s %s\n' "${RED}" "${RESET}" "$1"; FAIL_COUNT=$((FAIL_COUNT + 1)); }
info() { printf '  %s•%s    %s\n' "${YELLOW}" "${RESET}" "$1"; }

# Read the npm-dependency value (dependencies + devDependencies) for a package
# from a package.json. Echoes the version string or empty.
pkg_dep() {
  local pkg_json="$1" dep="$2"
  jq -r --arg d "${dep}" '
    (.dependencies // {}) + (.devDependencies // {})
    | .[$d] // empty
  ' "${pkg_json}" 2>/dev/null || true
}

# Read the "version" field of a package.json.
pkg_version() {
  jq -r '.version // empty' "$1" 2>/dev/null || true
}

echo "${BOLD}IEP coherence check${RESET}"
echo "  manifest: ${MANIFEST}"
echo "  root:     ${ROOT}"
echo ""

# Iterate over managed repos only. CCP lives in .deferred and is never touched.
MANAGED_COUNT="$(jq '.managed | length' "${MANIFEST}")"

for idx in $(seq 0 $((MANAGED_COUNT - 1))); do
  repo="$(jq -r ".managed[${idx}].repo" "${MANIFEST}")"
  fs_dir="$(jq -r ".managed[${idx}].fs_dir // .managed[${idx}].repo" "${MANIFEST}")"
  kind="$(jq -r ".managed[${idx}].kind" "${MANIFEST}")"
  want_core="$(jq -r ".managed[${idx}].core_schema_version // \"null\"" "${MANIFEST}")"
  want_harness="$(jq -r ".managed[${idx}].audit_harness_version" "${MANIFEST}")"
  harness_install="$(jq -r ".managed[${idx}].harness_install" "${MANIFEST}")"

  echo "${BOLD}${repo}${RESET} (${kind})"

  repo_dir="${ROOT}/${fs_dir}"
  if [[ ! -d "${repo_dir}" ]]; then
    fail "repo working copy missing at ${repo_dir}"
    echo ""
    continue
  fi
  pass "repo present: ${repo_dir}"

  pkg_json="${repo_dir}/package.json"

  # --- core schema pin ---------------------------------------------------
  if [[ "${want_core}" == "self" ]]; then
    info "core schema: this repo IS the kernel (no pin to verify)"
  elif [[ "${want_core}" == "null" ]]; then
    info "core schema: no direct @intentsolutions/core pin expected"
  else
    if [[ ! -f "${pkg_json}" ]]; then
      fail "core schema: expected pin ${want_core} but no package.json found"
    else
      got_core="$(pkg_dep "${pkg_json}" "@intentsolutions/core")"
      if [[ -z "${got_core}" ]]; then
        fail "core schema: manifest expects ${want_core}, repo declares none"
      elif [[ "${got_core}" == "${want_core}" ]]; then
        pass "core schema pin matches manifest (${got_core})"
      else
        fail "core schema drift: manifest=${want_core} repo=${got_core}"
      fi
    fi
  fi

  # --- audit-harness pin -------------------------------------------------
  case "${harness_install}" in
    self)
      # The harness repo itself: verify its package.json version equals the pin.
      if [[ ! -f "${pkg_json}" ]]; then
        fail "audit-harness: harness repo has no package.json"
      else
        got_ver="$(pkg_version "${pkg_json}")"
        if [[ "${got_ver}" == "${want_harness}" ]]; then
          pass "audit-harness self version matches manifest (${got_ver})"
        else
          fail "audit-harness self drift: manifest=${want_harness} repo=${got_ver}"
        fi
      fi
      ;;
    npm-dep)
      if [[ ! -f "${pkg_json}" ]]; then
        fail "audit-harness: expected npm pin ${want_harness} but no package.json"
      else
        got_harness="$(pkg_dep "${pkg_json}" "@intentsolutions/audit-harness")"
        if [[ -z "${got_harness}" ]]; then
          fail "audit-harness: manifest expects ${want_harness}, repo declares none"
        elif [[ "${got_harness}" == "${want_harness}" ]]; then
          pass "audit-harness npm pin matches manifest (${got_harness})"
        else
          fail "audit-harness drift: manifest=${want_harness} repo=${got_harness}"
        fi
      fi
      ;;
    vendored)
      ver_file="${repo_dir}/.audit-harness/VERSION"
      if [[ ! -f "${ver_file}" ]]; then
        fail "audit-harness: vendored install missing (.audit-harness/VERSION absent)"
      else
        got_harness="$(tr -d '[:space:]' < "${ver_file}")"
        if [[ "${got_harness}" == "${want_harness}" ]]; then
          pass "audit-harness vendored version matches manifest (${got_harness})"
        else
          fail "audit-harness vendored drift: manifest=${want_harness} repo=${got_harness}"
        fi
      fi
      ;;
    *)
      fail "audit-harness: unknown harness_install '${harness_install}' in manifest"
      ;;
  esac

  # --- harness resolves --------------------------------------------------
  case "${harness_install}" in
    self)
      if [[ -x "${repo_dir}/bin/audit-harness.js" ]] || [[ -f "${repo_dir}/bin/audit-harness.js" ]]; then
        pass "audit-harness binary present (bin/audit-harness.js)"
      else
        info "audit-harness binary path not at bin/audit-harness.js (harness repo layout may differ)"
      fi
      ;;
    vendored)
      wrapper="${repo_dir}/scripts/audit-harness"
      scripts_dir="${repo_dir}/.audit-harness/scripts"
      if [[ -f "${wrapper}" && -d "${scripts_dir}" ]]; then
        pass "audit-harness resolves: vendored wrapper + scripts present"
      else
        fail "audit-harness does not resolve: missing scripts/audit-harness or .audit-harness/scripts"
      fi
      ;;
    npm-dep)
      if [[ -e "${repo_dir}/node_modules/@intentsolutions/audit-harness" ]]; then
        pass "audit-harness resolves: installed in node_modules"
      else
        info "audit-harness not installed (node_modules absent) — run install to resolve"
      fi
      ;;
  esac

  echo ""
done

echo "${BOLD}Summary${RESET}: ${PASS_COUNT} pass, ${FAIL_COUNT} fail"

if [[ "${FAIL_COUNT}" -gt 0 ]]; then
  exit 1
fi
exit 0
