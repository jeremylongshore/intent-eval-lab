# Tier 2 — vendored last-good snapshots (per upstream surface)

`<surface-id>/snapshot<ext>` + `vendor-meta.json`, written ONLY by
`scripts/fetch-capture.py` and ONLY from a tier-1 raw record whose status is
`FETCH_OK`. `vendor-meta.json` records exactly which raw record the snapshot
came from (`source_raw_record`) — full lineage back to tier 1.

Rules (normative spec: `000-docs/052-AT-SPEC-fetch-failure-taxonomy-and-three-tier-archive-2026-06-12.md`):

- A bad fetch (any non-`FETCH_OK` status) leaves the last-good snapshot here
  **untouched** — it alerts (ntfy `prod-health`) and never opens a
  reconciliation issue/PR.
- **The differ never writes its own reference**: `spec-projection-diff.py`
  reads vendored snapshots; nothing downstream of this tier writes into it.
- Promotion tier 2 → tier 3 (the kernel `@intentsolutions/core`
  `schemas/authoring/v1`, in intent-eval-core) is **human** — this repo only
  documents that contract, never automates it.

Note: `_vendor/upstream/<contract>/` at the repo root is the pre-existing
contract-keyed vendored instance for skill-frontmatter (FF#2); folding it into
this surface-keyed tier is wave-B work (lineage log + classifier walls).
