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
# Exit codes:
#   0  - permission granted (claim may proceed)
#   1  - permission denied (claim is blocked; output explains why)
#   2  - script error (treat as hard fail)

set -u
set -o pipefail   # so a `bd | grep` pipeline reflects bd's failure, not just grep's exit

# ---- config ----
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IEP_LAB_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
STATUS_FILE="$IEP_LAB_ROOT/000-docs/audit/2026-05-26-plan-audit/STATUS.md"
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

# ---- input ----
BEAD_ID="${1:-}"
if [ -z "$BEAD_ID" ]; then
  echo "usage: $(basename "$0") <bead-id>" >&2
  echo "       (e.g., $(basename "$0") bd_000-projects-214c.1)" >&2
  exit 2
fi

# Whitelist bead id format to prevent injection (same pattern as validate-trilink.sh)
if ! [[ "$BEAD_ID" =~ ^bd_000-projects-[a-z0-9]+(\.[0-9]+)?$ ]]; then
  echo "ERROR: invalid bead id format: $BEAD_ID" >&2
  exit 2
fi

# ---- check 1: STATUS file exists ----
if [ ! -f "$STATUS_FILE" ]; then
  echo "ERROR: Plan Audit STATUS file not found at $STATUS_FILE" >&2
  echo "       (Plan Audit § 12 has not been opened. Run § 13 Step 4 first.)" >&2
  exit 2
fi

# ---- check 2: read STATUS state ----
STATE=$(grep -oE 'State:\*\*[[:space:]]+[A-Z-]+' "$STATUS_FILE" 2>/dev/null \
        | head -1 \
        | sed -E 's/State:\*\*[[:space:]]+//')

if [ -z "$STATE" ]; then
  echo "ERROR: Could not parse State: line from $STATUS_FILE" >&2
  exit 2
fi

# ---- check 3: is target bead refiner-labeled? ----
# Non-refiner beads are not gated; bail early.
#
# DEFECT GUARD: the previous `if ! bd show ... | grep -qE refiner` idiom tested
# only grep's exit status. When bd is missing or errors, grep gets no input,
# `grep -q` exits non-zero, `! grep` becomes true, and the gate WRONGLY concluded
# "not refiner-labeled" and opened (exit 0). We now capture bd's output and its
# OWN exit code separately, and HARD-FAIL (exit 2, matching the error exits above)
# when bd fails — fail closed, before grepping.
if ! BEAD_TEXT="$(bd show "$BEAD_ID" 2>/dev/null)"; then
  echo "ERROR: 'bd show $BEAD_ID' failed (bd missing, errored, or unknown bead)." >&2
  echo "       Refusing to open the refiner hard-gate on a failed bd lookup (fail closed)." >&2
  exit 2
fi
if ! printf '%s\n' "$BEAD_TEXT" | grep -qE '^LABELS:.*refiner'; then
  echo "OK: $BEAD_ID is not refiner-labeled; gate does not apply."
  exit 0
fi

# ---- gate logic ----
case "$STATE" in
  RATIFIED)
    echo "OK: STATUS = RATIFIED; hard gate fully lifted; claim permitted."
    exit 0
    ;;
  RATIFIED-WITH-DELTAS)
    # Partially lifted: only DR-028-authorized work may claim.
    # Match if bead title or notes contain any of the authorized shorthands.
    # BEAD_TEXT was already captured (and bd-success-verified) at check 3 above —
    # reuse it rather than re-shelling bd (which would re-expose the same idiom).
    for shorthand in "${DR_028_AUTHORIZED_SHORTHANDS[@]}"; do
      # Match shorthand tokens loosely against title + description text.
      # Token boundaries are dashes; case-insensitive.
      if echo "$BEAD_TEXT" | grep -qiF "$shorthand"; then
        echo "OK: STATUS = RATIFIED-WITH-DELTAS; bead matches DR-028 authorized work '$shorthand'; claim permitted."
        exit 0
      fi
    done
    # Also permit beads explicitly noted as DR-028-authorized in their description
    if echo "$BEAD_TEXT" | grep -qiE 'DR-028.{0,40}authorized|authorized.{0,40}DR-028'; then
      echo "OK: STATUS = RATIFIED-WITH-DELTAS; bead description references DR-028 authorization; claim permitted."
      exit 0
    fi
    echo "DENIED: STATUS = RATIFIED-WITH-DELTAS" >&2
    echo "        Hard gate is partially lifted per DR-028, but bead $BEAD_ID is" >&2
    echo "        NOT in the DR-028 authorized set." >&2
    echo "        Authorized work shorthands:" >&2
    for s in "${DR_028_AUTHORIZED_SHORTHANDS[@]}"; do echo "          - $s" >&2; done
    echo "        To proceed, wait for plan 027 v5 to land (STATUS → RATIFIED)," >&2
    echo "        or obtain explicit DR-028 authorization through the ISEDC process:" >&2
    echo "        $DR_028" >&2
    exit 1
    ;;
  OPEN | PHASE-3-SYNTHESIS-COMPLETE* | "PHASE-3-SYNTHESIS-COMPLETE-—-AWAITING-USER-ARBITRATION")
    echo "DENIED: STATUS = $STATE" >&2
    echo "        Plan Audit is still in progress; hard gate is FULLY ACTIVE." >&2
    echo "        Per plan 027 § 13 Step 7: no bd claim against any Skill Refiner" >&2
    echo "        bead until STATUS file reads RATIFIED." >&2
    echo "        See: $STATUS_FILE" >&2
    exit 1
    ;;
  *)
    echo "DENIED: Unknown STATUS state '$STATE'; gate fails closed for safety." >&2
    echo "        See: $STATUS_FILE" >&2
    exit 1
    ;;
esac
