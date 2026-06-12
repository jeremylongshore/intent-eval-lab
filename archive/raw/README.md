# Tier 1 — raw-fetch archive (immutable, append-only)

Every fetch attempt by `scripts/fetch-capture.py` lands here as
`<surface-id>/<UTC-stamp>.meta.json` (+ `<UTC-stamp>.body` when the bytes are
new). Bodies are sha256-deduplicated: a body identical to the previous record's
is not rewritten — the meta still appends, with `body_ref` naming the record
that stores those bytes.

Rules (normative spec: `000-docs/052-AT-SPEC-fetch-failure-taxonomy-and-three-tier-archive-2026-06-12.md`):

- **Append-only.** No deletions, no rewrites — in CI or by hand.
- Every record carries exactly one taxonomy status:
  `FETCH_OK | UNREACHABLE | MOVED | RATELIMITED | SHAPE_CHANGED | TRUNCATED`.
- Only a `FETCH_OK` record may be promoted to tier 2 (`specs/_vendor/`).

Populated by the daily `spec-drift-watch.yml` scheduled run (commit-back).
