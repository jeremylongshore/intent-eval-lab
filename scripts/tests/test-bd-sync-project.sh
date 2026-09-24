#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
FIXTURE_DIR="$SCRIPT_DIR/fixtures/bd-sync"
TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/bd-sync-project-test.XXXXXX")"
trap 'rm -rf "$TEST_DIR"' EXIT

mkdir -p "$TEST_DIR/000-docs"
cp -f "$FIXTURE_DIR/issue-human.md" "$TEST_DIR/issue.md"
cp -f "$FIXTURE_DIR/doc-human.md" "$TEST_DIR/000-docs/fixture.md"
: > "$TEST_DIR/edits.log"

export BD_SYNC_TEST_STATE="$TEST_DIR"
export PATH="$FIXTURE_DIR/fake-bin:$PATH"

"$ROOT_DIR/scripts/bd-sync.sh" project bd_fixture_0001 --repo-root "$TEST_DIR"
: > "$TEST_DIR/edits.log"

"$ROOT_DIR/scripts/bd-sync.sh" project bd_fixture_0002 --repo-root "$TEST_DIR"
shared_doc=$(<"$TEST_DIR/000-docs/fixture.md")
expected_shared_beads="Beads: \`bd_fixture_0001, bd_fixture_0002\`"
expected_shared_gh="GitHub: \`owner/repo#42, owner/repo#99\`"
case "$shared_doc" in
  *"$expected_shared_beads"*"$expected_shared_gh"*) : ;;
  *)
    echo 'bd-sync project test FAIL: shared document projection lost a bead receipt' >&2
    exit 1
    ;;
esac
shared_doc_sha=$(sha256sum "$TEST_DIR/000-docs/fixture.md")
"$ROOT_DIR/scripts/bd-sync.sh" project bd_fixture_0002 --repo-root "$TEST_DIR"
[ "$shared_doc_sha" = "$(sha256sum "$TEST_DIR/000-docs/fixture.md")" ] || {
  echo 'bd-sync project test FAIL: repeated shared projection was not idempotent' >&2
  exit 1
}
: > "$TEST_DIR/edits.log"

doc_before=$(sha256sum "$TEST_DIR/000-docs/fixture.md")
sed -i 's/^Projection-SHA256: .*/Projection-SHA256: 0000000000000000000000000000000000000000000000000000000000000000/' "$TEST_DIR/issue.md"
issue_after_mutation=$(sha256sum "$TEST_DIR/issue.md")

if "$ROOT_DIR/scripts/bd-sync.sh" project bd_fixture_0002 --repo-root "$TEST_DIR" >/dev/null 2>&1; then
  echo 'bd-sync project test FAIL: mutated projection was accepted' >&2
  exit 1
fi

[ "$issue_after_mutation" = "$(sha256sum "$TEST_DIR/issue.md")" ] || {
  echo 'bd-sync project test FAIL: anomaly changed the GitHub body' >&2
  exit 1
}
[ "$doc_before" = "$(sha256sum "$TEST_DIR/000-docs/fixture.md")" ] || {
  echo 'bd-sync project test FAIL: anomaly changed the document' >&2
  exit 1
}
[ ! -s "$TEST_DIR/edits.log" ] || {
  echo 'bd-sync project test FAIL: anomaly attempted a GitHub write' >&2
  exit 1
}

echo 'bd-sync project self-test: anomaly is fail-closed with no writes'
