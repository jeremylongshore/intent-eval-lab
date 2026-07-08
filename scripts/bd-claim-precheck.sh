#!/usr/bin/env bash
# bd-claim-precheck.sh — Plan 027 § 13 Step 7 hard-gate enforcement (P0-RATIFY-4 per DR-028)
#
# Honor-system replacement: machine-enforced gate that BLOCKS `bd claim` against any
# Skill Refiner-labeled bead until the Plan Audit STATUS file reads RATIFIED (or
# RATIFIED-WITH-DELTAS with the bead explicitly authorized).
#
# Wire as a bd hook OR call from a `bd-claim` shell wrapper. CI also calls this
# script as a sanity check on PR branches that include a `bd update <id> --claim`.
#
# CI SELF-TEST (hermetic, no live bd required):
#   scripts/bd-claim-precheck.sh --self-test
# runs the STATUS-parse + gate-decision logic against temp fixtures with a stub
# `bd` provider, asserting: RATIFIED allows a refiner bead, a non-RATIFIED state
# refuses it (exit 1), RATIFIED-WITH-DELTAS refuses a non-authorized refiner bead
# but allows an authorized one, non-refiner beads are ungated, a missing STATUS
# file / bd failure / bad bead id fail closed (exit 2). This is the
# external-contributor path: it verifies STATUS-file integrity + the refusal
# logic WITHOUT needing bd/dolt installed on the runner (the umbrella bd
# workspace is not present in CI). See DR-028 P0-RATIFY-4 external-contributor
# delta: external PRs see the gate as a CI check on STATUS integrity, not a
# live `bd claim` block.
#
# Exit codes:
#   0  - permission granted (claim may proceed)  |  --self-test: all assertions passed
#   1  - permission denied (claim is blocked; output explains why)
#   2  - script error (treat as hard fail)       |  --self-test: an assertion failed
#
# NO GATE WEAKENING: the refactor below extracts the STATUS-parse + gate-decision
# into functions so the CI self-test can exercise them hermetically. The real CLI
# path (a bead id argument) drives the SAME functions with the SAME STATUS file
# and the SAME live-bd lookup — behavior is byte-identical to the pre-self-test
# script. The self-test only ADDS enforcement (a CI proof the gate still refuses).

set -u
set -o pipefail   # so a `bd | grep` pipeline reflects bd's failure, not just grep's exit

# ---- config ----
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IEP_LAB_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
STATUS_FILE_DEFAULT="$IEP_LAB_ROOT/000-docs/audit/2026-05-26-plan-audit/STATUS.md"
DR_028="$IEP_LAB_ROOT/000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md"

# Beads that DR-028 explicitly authorized as `bd claim`-eligible under PARTIALLY LIFTED
# hard gate (directives 3-8 of DR-028 § 9). Identified by shorthand; resolved to
# bd_000-projects-* IDs at runtime via the implementation-directives bead list.
# This list is updated when plan 027 v5 ships (gate moves to fully lifted).
DR_028_AUTHORIZED_SHORTHANDS=(
  "SkillVersion-entity-schema-with-version_kind"
  "RefinerStrategy-interface"
  "Phase-A.0-null-hypothesis-baseline"
  "bd-sync-cross-ref-generator"
  "bd-claim-precheck.sh-script"
  "sigstore-Rekor-outbox-reconciler"
)

# ---------------------------------------------------------------------------
# parse_status_state <status-file>
#   Prints the parsed State: token on stdout; returns 0 on success.
#   Returns 2 (via caller) when the file is missing or the State: line is
#   unparseable. Emits diagnostics on stderr.
# ---------------------------------------------------------------------------
parse_status_state() {
  local status_file="$1"
  if [ ! -f "$status_file" ]; then
    echo "ERROR: Plan Audit STATUS file not found at $status_file" >&2
    echo "       (Plan Audit § 12 has not been opened. Run § 13 Step 4 first.)" >&2
    return 2
  fi
  local state
  state=$(grep -oE 'State:\*\*[[:space:]]+[A-Z-]+' "$status_file" 2>/dev/null \
          | head -1 \
          | sed -E 's/State:\*\*[[:space:]]+//')
  if [ -z "$state" ]; then
    echo "ERROR: Could not parse State: line from $status_file" >&2
    return 2
  fi
  printf '%s\n' "$state"
  return 0
}

# ---------------------------------------------------------------------------
# decide <bead-id> <status-file> <bead-text-provider>
#   The single gate-decision entry point. <bead-text-provider> is the name of
#   a function that, given a bead id, prints the bead's `bd show` text on stdout
#   and returns 0 on success / non-zero on lookup failure. Real invocations pass
#   `bd_show_provider` (which shells out to live bd); the self-test passes a
#   fixture provider. This indirection is what makes the CI check hermetic —
#   the gate logic is identical, only the source of the bead text differs.
#
#   Returns the gate exit code (0 allow / 1 deny / 2 error).
# ---------------------------------------------------------------------------
decide() {
  local bead_id="$1" status_file="$2" provider="$3"

  # ---- input validation (same whitelist as the CLI path) ----
  if [ -z "$bead_id" ]; then
    echo "ERROR: empty bead id" >&2
    return 2
  fi
  # Whitelist bead id format to prevent injection (same pattern as validate-trilink.sh)
  if ! [[ "$bead_id" =~ ^bd_000-projects-[a-z0-9]+(\.[0-9]+)?$ ]]; then
    echo "ERROR: invalid bead id format: $bead_id" >&2
    return 2
  fi

  # ---- check 1 + 2: STATUS file exists and State: parses ----
  local state
  state="$(parse_status_state "$status_file")" || return 2

  # ---- check 3: is target bead refiner-labeled? ----
  # Non-refiner beads are not gated; bail early.
  #
  # DEFECT GUARD: the previous `if ! bd show ... | grep -qE refiner` idiom tested
  # only grep's exit status. When bd is missing or errors, grep gets no input,
  # `grep -q` exits non-zero, `! grep` becomes true, and the gate WRONGLY concluded
  # "not refiner-labeled" and opened (exit 0). We now capture the provider's output
  # and its OWN exit code separately, and HARD-FAIL (exit 2, matching the error
  # exits above) when the lookup fails — fail closed, before grepping.
  local bead_text
  if ! bead_text="$("$provider" "$bead_id" 2>/dev/null)"; then
    echo "ERROR: bead lookup for $bead_id failed (bd missing, errored, or unknown bead)." >&2
    echo "       Refusing to open the refiner hard-gate on a failed lookup (fail closed)." >&2
    return 2
  fi
  if ! printf '%s\n' "$bead_text" | grep -qE '^LABELS:.*refiner'; then
    echo "OK: $bead_id is not refiner-labeled; gate does not apply."
    return 0
  fi

  # ---- gate logic ----
  case "$state" in
    RATIFIED)
      echo "OK: STATUS = RATIFIED; hard gate fully lifted; claim permitted."
      return 0
      ;;
    RATIFIED-WITH-DELTAS)
      # Partially lifted: only DR-028-authorized work may claim.
      # Match if bead title or notes contain any of the authorized shorthands.
      # bead_text was already captured (and lookup-success-verified) at check 3
      # above — reuse it rather than re-invoking the provider.
      local shorthand
      for shorthand in "${DR_028_AUTHORIZED_SHORTHANDS[@]}"; do
        # Match shorthand tokens loosely against title + description text.
        # Token boundaries are dashes; case-insensitive.
        if echo "$bead_text" | grep -qiF "$shorthand"; then
          echo "OK: STATUS = RATIFIED-WITH-DELTAS; bead matches DR-028 authorized work '$shorthand'; claim permitted."
          return 0
        fi
      done
      # Also permit beads explicitly noted as DR-028-authorized in their description
      if echo "$bead_text" | grep -qiE 'DR-028.{0,40}authorized|authorized.{0,40}DR-028'; then
        echo "OK: STATUS = RATIFIED-WITH-DELTAS; bead description references DR-028 authorization; claim permitted."
        return 0
      fi
      echo "DENIED: STATUS = RATIFIED-WITH-DELTAS" >&2
      echo "        Hard gate is partially lifted per DR-028, but bead $bead_id is" >&2
      echo "        NOT in the DR-028 authorized set." >&2
      echo "        Authorized work shorthands:" >&2
      local s
      for s in "${DR_028_AUTHORIZED_SHORTHANDS[@]}"; do echo "          - $s" >&2; done
      echo "        To proceed, wait for plan 027 v5 to land (STATUS → RATIFIED)," >&2
      echo "        or obtain explicit DR-028 authorization through the ISEDC process:" >&2
      echo "        $DR_028" >&2
      return 1
      ;;
    OPEN | PHASE-3-SYNTHESIS-COMPLETE*)
      # The glob covers the full "PHASE-3-SYNTHESIS-COMPLETE-—-AWAITING-USER-ARBITRATION"
      # literal; any in-progress Plan-Audit state routes here and is denied.
      echo "DENIED: STATUS = $state" >&2
      echo "        Plan Audit is still in progress; hard gate is FULLY ACTIVE." >&2
      echo "        Per plan 027 § 13 Step 7: no bd claim against any Skill Refiner" >&2
      echo "        bead until STATUS file reads RATIFIED." >&2
      echo "        See: $status_file" >&2
      return 1
      ;;
    *)
      echo "DENIED: Unknown STATUS state '$state'; gate fails closed for safety." >&2
      echo "        See: $status_file" >&2
      return 1
      ;;
  esac
}

# ---------------------------------------------------------------------------
# bd_show_provider <bead-id>
#   The real, live-bd bead-text provider used by the CLI path. Shells out to
#   `bd show`. Returns bd's exit status so `decide` can fail closed on lookup
#   failure. This is the ONLY place live bd is touched; the self-test never
#   reaches it.
# ---------------------------------------------------------------------------
bd_show_provider() {
  # shellcheck disable=SC2317  # invoked indirectly by name via `decide "$provider"`
  bd show "$1"
}

# ---------------------------------------------------------------------------
# cmd_self_test
#   Hermetic, deterministic, no live bd. Builds temp STATUS fixtures + a stub
#   bead-text provider, then asserts the gate's exit code on every class:
#     - RATIFIED               + refiner bead        -> 0 (allow)
#     - OPEN                   + refiner bead        -> 1 (deny, gate fully active)
#     - unknown state          + refiner bead        -> 1 (deny, fail closed)
#     - RATIFIED-WITH-DELTAS   + authorized refiner  -> 0 (allow)
#     - RATIFIED-WITH-DELTAS   + non-authorized      -> 1 (deny)
#     - any state              + non-refiner bead    -> 0 (ungated)
#     - missing STATUS file    + refiner bead        -> 2 (error)
#     - bd lookup fails        + refiner bead        -> 2 (fail closed)
#     - bad bead id                                  -> 2 (error)
#   Exits 0 iff every assertion holds; exits 2 (hard fail) on any mismatch — so a
#   regression that WEAKENS the gate (e.g. a refiner bead under OPEN no longer
#   denied) turns the CI check red.
# ---------------------------------------------------------------------------
cmd_self_test() {
  local failures=0
  local tmp
  tmp="$(mktemp -d "${TMPDIR:-/tmp}/bd-claim-precheck-selftest.XXXXXX")" || {
    echo "self-test ERROR: could not create temp dir" >&2
    return 2
  }
  # shellcheck disable=SC2064
  trap "rm -rf '$tmp'" RETURN

  # --- fixture STATUS files ---
  local status_ratified="$tmp/STATUS-ratified.md"
  local status_open="$tmp/STATUS-open.md"
  local status_deltas="$tmp/STATUS-deltas.md"
  local status_unknown="$tmp/STATUS-unknown.md"
  local status_missing="$tmp/STATUS-does-not-exist.md"   # deliberately not created
  printf '# STATUS\n\n**State:** RATIFIED\n' > "$status_ratified"
  printf '# STATUS\n\n**State:** OPEN\n' > "$status_open"
  printf '# STATUS\n\n**State:** RATIFIED-WITH-DELTAS\n' > "$status_deltas"
  printf '# STATUS\n\n**State:** FROBNICATED\n' > "$status_unknown"

  # --- stub bead-text providers (bd show-shaped, no live bd) ---
  # These are invoked indirectly by name (passed as the <bead-text-provider>
  # arg to `decide`), so shellcheck can't see the call sites.
  # shellcheck disable=SC2317
  # A refiner-labeled bead: emits the `^LABELS:` line the gate greps for.
  fixture_provider_refiner() {
    printf '%s\n' \
      "○ $1 [TASK] · some refiner work" \
      "LABELS: refiner, repo:iel"
    return 0
  }
  # A refiner bead whose description matches a DR-028 authorized shorthand.
  # shellcheck disable=SC2317
  fixture_provider_refiner_authorized() {
    printf '%s\n' \
      "○ $1 [TASK] · Author bead: bd-claim-precheck.sh script (P0-RATIFY-4)" \
      "LABELS: refiner, repo:iel" \
      "DESCRIPTION: implements the bd-claim-precheck.sh-script enforcement"
    return 0
  }
  # A non-refiner bead: no refiner label -> gate does not apply.
  # shellcheck disable=SC2317
  fixture_provider_nonrefiner() {
    printf '%s\n' \
      "○ $1 [TASK] · unrelated work" \
      "LABELS: ci-lint, repo:iel"
    return 0
  }
  # A failing lookup (bd missing / unknown bead) -> non-zero exit, empty output.
  # shellcheck disable=SC2317
  fixture_provider_fail() {
    return 1
  }

  local valid_bead="bd_000-projects-214c.9"
  local bad_bead="bd_000-projects-214c; rm -rf /"

  expect() {
    local name="$1" want="$2" got="$3"
    if [ "$got" -eq "$want" ]; then
      echo "self-test ok: $name (exit $got)"
    else
      echo "self-test FAIL: $name — expected exit $want, got $got" >&2
      failures=$((failures + 1))
    fi
  }

  local rc

  # RATIFIED + refiner -> allow (0)
  decide "$valid_bead" "$status_ratified" fixture_provider_refiner >/dev/null 2>&1; rc=$?
  expect "RATIFIED + refiner bead -> allow" 0 "$rc"

  # OPEN + refiner -> deny (1); gate fully active
  decide "$valid_bead" "$status_open" fixture_provider_refiner >/dev/null 2>&1; rc=$?
  expect "OPEN + refiner bead -> deny" 1 "$rc"

  # Unknown state + refiner -> deny (1); fail closed
  decide "$valid_bead" "$status_unknown" fixture_provider_refiner >/dev/null 2>&1; rc=$?
  expect "unknown STATUS state + refiner bead -> deny (fail closed)" 1 "$rc"

  # RATIFIED-WITH-DELTAS + authorized refiner -> allow (0)
  decide "$valid_bead" "$status_deltas" fixture_provider_refiner_authorized >/dev/null 2>&1; rc=$?
  expect "RATIFIED-WITH-DELTAS + DR-028-authorized refiner -> allow" 0 "$rc"

  # RATIFIED-WITH-DELTAS + non-authorized refiner -> deny (1)
  decide "$valid_bead" "$status_deltas" fixture_provider_refiner >/dev/null 2>&1; rc=$?
  expect "RATIFIED-WITH-DELTAS + non-authorized refiner -> deny" 1 "$rc"

  # Non-refiner bead under OPEN -> ungated allow (0)
  decide "$valid_bead" "$status_open" fixture_provider_nonrefiner >/dev/null 2>&1; rc=$?
  expect "OPEN + non-refiner bead -> ungated (allow)" 0 "$rc"

  # Non-refiner bead under RATIFIED -> ungated allow (0)
  decide "$valid_bead" "$status_ratified" fixture_provider_nonrefiner >/dev/null 2>&1; rc=$?
  expect "RATIFIED + non-refiner bead -> ungated (allow)" 0 "$rc"

  # Missing STATUS file + refiner -> error (2)
  decide "$valid_bead" "$status_missing" fixture_provider_refiner >/dev/null 2>&1; rc=$?
  expect "missing STATUS file -> error" 2 "$rc"

  # bd lookup fails + refiner -> error (2); fail closed, NOT a false 'not refiner'
  decide "$valid_bead" "$status_ratified" fixture_provider_fail >/dev/null 2>&1; rc=$?
  expect "bd lookup failure -> error (fail closed)" 2 "$rc"

  # Bad bead id -> error (2); injection guard
  decide "$bad_bead" "$status_ratified" fixture_provider_refiner >/dev/null 2>&1; rc=$?
  expect "invalid bead id (injection guard) -> error" 2 "$rc"

  echo ""
  if [ "$failures" -ne 0 ]; then
    echo "self-test: $failures FAILURE(S) — the hard gate is NOT sound. See DR-028 P0-RATIFY-4." >&2
    return 2
  fi
  echo "self-test: all assertions passed; the refiner hard gate enforces correctly."
  echo "  (RATIFIED allows · non-RATIFIED refuses · authorized-under-deltas allows ·"
  echo "   non-refiner ungated · missing-STATUS/failed-lookup/bad-id fail closed)"
  return 0
}

# ---- dispatch ----
MODE="${1:-}"

if [ "$MODE" = "--self-test" ]; then
  cmd_self_test
  exit $?
fi

if [ -z "$MODE" ]; then
  echo "usage: $(basename "$0") <bead-id>" >&2
  echo "       $(basename "$0") --self-test" >&2
  echo "       (e.g., $(basename "$0") bd_000-projects-214c.1)" >&2
  exit 2
fi

# Real CLI path: adjudicate the given bead against the live STATUS file + live bd.
decide "$MODE" "$STATUS_FILE_DEFAULT" bd_show_provider
exit $?
