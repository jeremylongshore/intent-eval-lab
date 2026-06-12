#!/usr/bin/env bash
# Polls 11 spec sources, compares each against a committed snapshot hash, and
# reports drift. Used by .github/workflows/spec-drift-watch.yml (daily cron)
# and locally for ad-hoc checks or seeding new baselines via --init.
#
# Surface coverage (9k5h): the 6 original surfaces (Claude Code changelog + npm,
# the platform SKILL.md page, the engineering blog, anthropics/skills, agentskills.io)
# plus the Wave-1 expansion (9k5h.7): the MCP protocol spec + machine-readable
# schema.ts, and the Claude Code hooks / settings / slash-commands references.
# Wave 2 (9k5h.8) adds plugins-reference, sub-agents, marketplace, MCP releases.
#
# Sources defined here in one place (DRY); the workflow only handles CI side
# effects (open issue, fire ntfy).
#
# Authority: 000-docs/030-AT-DECR-eval-set-bootstrap-decisions-2026-05-28.md § 6
#
# Usage:
#   scripts/spec-drift-check.sh             # check all sources; exit 1 on drift
#   scripts/spec-drift-check.sh --init      # seed missing baselines (write .sha files)
#   scripts/spec-drift-check.sh --refresh   # overwrite existing baselines with current state
#   scripts/spec-drift-check.sh --json      # emit JSON report to stdout (CI consumption)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SHA_DIR="${REPO_ROOT}/specs/snapshots/.sha"
mkdir -p "${SHA_DIR}"

MODE="check"
case "${1:-}" in
  --init)    MODE="init" ;;
  --refresh) MODE="refresh" ;;
  --json)    MODE="json" ;;
  "")        MODE="check" ;;
  *) echo "Unknown flag: $1" >&2; exit 2 ;;
esac

# Per-source extractor functions. Each prints a stable hash to stdout.
# Extractor failure (404, network) is reported but NOT counted as drift —
# drift = "fetched OK and hash changed", not "couldn't fetch".

fetch_cc_changelog() {
  # Raw GitHub CHANGELOG.md — the upstream source of truth. The published
  # Mintlify page at code.claude.com/docs/en/changelog is generated FROM
  # this file; polling raw GH eliminates publish lag (~minutes) and Mintlify
  # processing variability. Deterministic across consecutive fetches (verified).
  curl -fsSL "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md" \
    | sha256sum | awk '{print $1}'
}

fetch_cc_npm_version() {
  # Authoritative version field on @anthropic-ai/claude-code.
  npm view @anthropic-ai/claude-code version 2>/dev/null | tr -d '\n' | sha256sum | awk '{print $1}'
}

fetch_platform_skills_overview() {
  # Mintlify .md shim. The HTML page mutates non-deterministically (build IDs,
  # cookie banner tokens) — but Mintlify exposes a stable raw-markdown
  # variant at the same path with .md appended. Verified deterministic across
  # consecutive fetches.
  curl -fsSL "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md" \
    | sha256sum | awk '{print $1}'
}

fetch_anthropic_engineering() {
  # Top article slug sentinel — extract the first article link, hash that.
  curl -fsSL "https://www.anthropic.com/engineering" \
    | grep -oE 'href="/engineering/[a-z0-9-]+"' \
    | head -1 \
    | sha256sum | awk '{print $1}'
}

fetch_skills_releases_atom() {
  # Concatenate releases + commits feeds. Drift on either fires.
  {
    curl -fsSL "https://github.com/anthropics/skills/releases.atom" \
      | grep -oE '<id>tag:github.com,[^<]+</id>' | head -1
    curl -fsSL "https://github.com/anthropics/skills/commits/main.atom" \
      | grep -oE '<id>tag:github.com,[^<]+</id>' | head -1
  } | sha256sum | awk '{print $1}'
}

fetch_agentskills_spec() {
  # Mintlify .md shim — direct markdown, no HTML noise.
  curl -fsSL "https://agentskills.io/specification.md" \
    | sha256sum | awk '{print $1}'
}

# ── Wave 1 expansion (9k5h.7): the 5 surfaces with no prior coverage. These add
# the contracts the kernel authoring family governs but the watcher was blind to —
# the MCP protocol (the ONE truly machine-readable upstream) + the Claude Code
# hooks / settings / slash-commands references. Each verified deterministic across
# consecutive fetches (the .md-shim / raw-file pattern the existing extractors use).

fetch_mcp_schema_ts() {
  # THE machine-readable upstream — the MCP protocol schema as TypeScript source.
  # Authority precedence: this spec beats Claude's mcp doc page. It is the
  # field-level-diff proving ground (9k5h.11); the byte-hash here catches any change.
  curl -fsSL "https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/draft/schema.ts" \
    | sha256sum | awk '{print $1}'
}

fetch_mcp_spec_docs() {
  # MCP specification (draft) — the human-facing normative spec page.
  curl -fsSL "https://modelcontextprotocol.io/specification/draft" \
    | sha256sum | awk '{print $1}'
}

fetch_claude_hooks() {
  # Claude Code hooks reference — Mintlify .md shim (deterministic).
  curl -fsSL "https://code.claude.com/docs/en/hooks.md" \
    | sha256sum | awk '{print $1}'
}

fetch_claude_settings() {
  # Claude Code settings reference (incl. hook `if` syntax) — .md shim.
  curl -fsSL "https://code.claude.com/docs/en/settings.md" \
    | sha256sum | awk '{print $1}'
}

fetch_claude_slash_commands() {
  # Claude Code slash-commands reference — .md shim.
  curl -fsSL "https://code.claude.com/docs/en/slash-commands.md" \
    | sha256sum | awk '{print $1}'
}

# Source registry: name | description | extractor
SOURCES=(
  "claude-code-changelog|Claude Code published changelog (code.claude.com/docs/en/changelog.md)|fetch_cc_changelog"
  "claude-code-npm|@anthropic-ai/claude-code npm version|fetch_cc_npm_version"
  "platform-skills-overview|Anthropic SKILL.md spec page|fetch_platform_skills_overview"
  "anthropic-engineering|Anthropic engineering blog (top article)|fetch_anthropic_engineering"
  "skills-releases|github.com/anthropics/skills releases + commits|fetch_skills_releases_atom"
  "agentskills-spec|agentskills.io open standard|fetch_agentskills_spec"
  # Wave 1 (9k5h.7) — MCP protocol + Claude Code hooks/settings/slash-commands.
  "mcp-schema-ts|MCP protocol schema (machine-readable schema.ts, draft)|fetch_mcp_schema_ts"
  "mcp-spec-docs|MCP specification draft (modelcontextprotocol.io)|fetch_mcp_spec_docs"
  "claude-hooks|Claude Code hooks reference|fetch_claude_hooks"
  "claude-settings|Claude Code settings reference (hook if-syntax)|fetch_claude_settings"
  "claude-slash-commands|Claude Code slash-commands reference|fetch_claude_slash_commands"
)

declare -a DRIFT_LIST=()
declare -a FETCH_ERRORS=()
declare -a JSON_ROWS=()

for entry in "${SOURCES[@]}"; do
  IFS='|' read -r name desc extractor <<< "${entry}"
  sha_path="${SHA_DIR}/${name}.sha"

  # Run extractor, capture hash; trap failure separately from drift.
  if ! current_hash="$("${extractor}" 2>/dev/null)" || [[ -z "${current_hash}" ]]; then
    FETCH_ERRORS+=("${name}: extractor failed (network or upstream change)")
    JSON_ROWS+=("{\"source\":\"${name}\",\"status\":\"fetch_error\",\"description\":\"${desc}\"}")
    continue
  fi

  case "${MODE}" in
    init)
      if [[ -f "${sha_path}" ]]; then
        [[ "${MODE}" == "check" ]] || echo "skip (already seeded): ${name}"
        continue
      fi
      printf '%s\n' "${current_hash}" > "${sha_path}"
      echo "seeded: ${name} = ${current_hash:0:12}…"
      JSON_ROWS+=("{\"source\":\"${name}\",\"status\":\"seeded\",\"hash\":\"${current_hash}\"}")
      ;;
    refresh)
      printf '%s\n' "${current_hash}" > "${sha_path}"
      echo "refreshed: ${name} = ${current_hash:0:12}…"
      JSON_ROWS+=("{\"source\":\"${name}\",\"status\":\"refreshed\",\"hash\":\"${current_hash}\"}")
      ;;
    check|json)
      if [[ ! -f "${sha_path}" ]]; then
        FETCH_ERRORS+=("${name}: no baseline (.sha file missing). Run --init to seed.")
        JSON_ROWS+=("{\"source\":\"${name}\",\"status\":\"no_baseline\",\"description\":\"${desc}\"}")
        continue
      fi
      baseline_hash="$(cat "${sha_path}" | tr -d '\n[:space:]')"
      if [[ "${current_hash}" != "${baseline_hash}" ]]; then
        DRIFT_LIST+=("${name}: ${desc} — was ${baseline_hash:0:12}…, now ${current_hash:0:12}…")
        JSON_ROWS+=("{\"source\":\"${name}\",\"status\":\"drift\",\"description\":\"${desc}\",\"baseline\":\"${baseline_hash}\",\"current\":\"${current_hash}\"}")
      else
        JSON_ROWS+=("{\"source\":\"${name}\",\"status\":\"ok\",\"description\":\"${desc}\",\"hash\":\"${current_hash}\"}")
      fi
      ;;
  esac
done

if [[ "${MODE}" == "json" ]]; then
  printf '{"checked_at":"%s","sources":[%s]}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    "$(IFS=,; echo "${JSON_ROWS[*]}")"
  exit 0
fi

if [[ "${MODE}" == "init" || "${MODE}" == "refresh" ]]; then
  if [[ ${#FETCH_ERRORS[@]} -gt 0 ]]; then
    echo ""
    echo "Errors (non-fatal):"
    for err in "${FETCH_ERRORS[@]}"; do echo "  - ${err}"; done
  fi
  exit 0
fi

# check mode: report drift
echo ""
if [[ ${#DRIFT_LIST[@]} -eq 0 && ${#FETCH_ERRORS[@]} -eq 0 ]]; then
  echo "All ${#SOURCES[@]} sources match committed snapshots. No drift."
  exit 0
fi

if [[ ${#DRIFT_LIST[@]} -gt 0 ]]; then
  echo "Spec drift detected (${#DRIFT_LIST[@]} of ${#SOURCES[@]} sources):"
  for d in "${DRIFT_LIST[@]}"; do echo "  - ${d}"; done
fi

if [[ ${#FETCH_ERRORS[@]} -gt 0 ]]; then
  echo ""
  echo "Fetch errors (${#FETCH_ERRORS[@]}):"
  for e in "${FETCH_ERRORS[@]}"; do echo "  - ${e}"; done
fi

# Exit 1 only on drift; fetch errors alone do not fail the gate (upstream
# may be temporarily unavailable; treat as recoverable).
[[ ${#DRIFT_LIST[@]} -gt 0 ]] && exit 1 || exit 0
