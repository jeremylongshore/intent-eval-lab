# 052 — Typed fetch-failure taxonomy + three append-only tiers (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry) · **Epic:** 9k5h (GH intent-eval-lab#114)

This is the normative reference for the watcher's fetch pipeline. Wave B (lineage log + classifier walls) builds against this contract. Implementation: `scripts/fetch-capture.py`, driven by `specs/upstream-surface-registry.v1.json` per-surface `capture` config.

## Why (bead intent — Armstrong / Kleppmann corrections)

- **Armstrong:** a failed fetch is a _typed, isolated_ failure, never a boolean and never something to limp past. The watcher previously collapsed every failure into one `fetch_error` bucket; a restructured page could masquerade as drift (or as silence). Each fetch now classifies into exactly one status, and nothing but `FETCH_OK` propagates.
- **Kleppmann:** the raw fetch log is the immutable source of record; everything downstream is a derived view. Tier 1 is append-only; tiers 2 and 3 are projections of it, promoted one direction only. **The differ never writes its own reference** — `spec-projection-diff.py` reads tier 2 and writes nothing into it.

## The taxonomy (exactly one status per fetch attempt)

| Status          | Detection heuristic                                                                                                                                  | Downstream effect                                           |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `FETCH_OK`      | none of the below                                                                                                                                    | archives; may update tier 2; may feed the differ/classifier |
| `UNREACHABLE`   | HTTP 5xx / non-404/429 4xx, timeout, DNS/connection error                                                                                            | archive meta only                                           |
| `MOVED`         | 404, or a 301/302 redirect to a **different host** (same-host redirects are fine)                                                                    | archive meta only                                           |
| `RATELIMITED`   | HTTP 429                                                                                                                                             | archive meta only                                           |
| `TRUNCATED`     | body shorter than the surface's `min_bytes` floor (truncated-mid-structure proxy)                                                                    | archive meta only                                           |
| `SHAPE_CHANGED` | body does not match the surface's `expect_regex` (the expected extractor pattern, e.g. markdown headings, `<id>tag:github.com,`, `export interface`) | archive meta only                                           |

Precedence when several could apply: `RATELIMITED` > `MOVED` > `UNREACHABLE` > `TRUNCATED` > `SHAPE_CHANGED` > `FETCH_OK` (first match wins; classification is conservative).

**On any non-`FETCH_OK` status:** the last-good tier-2 snapshot stays untouched; the run alerts via the repo's existing ntfy pattern (topic `prod-health`, same step family as drift/liveness in `spec-drift-watch.yml`); and **no reconciliation issue or PR is ever opened off a bad fetch** — the issue-open condition in the workflow deliberately excludes `bad_fetch`.

## The three tiers (promotion is one-directional)

| Tier                  | Location                                                          | Written by                                                | Mutability                                                           |
| --------------------- | ----------------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------- |
| 1 — raw-fetch archive | `archive/raw/<surface-id>/<UTC-stamp>.{body,meta.json}`           | `fetch-capture.py` (every attempt)                        | **immutable, append-only** — no deletions/rewrites, in CI or by hand |
| 2 — vendored snapshot | `specs/_vendor/<surface-id>/snapshot<ext>` + `vendor-meta.json`   | `fetch-capture.py`, **only** from a `FETCH_OK` raw record | replace-in-place, lineage recorded                                   |
| 3 — the kernel        | `@intentsolutions/core` `schemas/authoring/v1` (intent-eval-core) | a **human**                                               | governed by SAK change discipline (DR-044/046)                       |

- **Tier-1 meta** carries `{surface_id, url, fetched_at, status, http_code, sha256, bytes, body_stored, body_ref}`. Growth control: bodies are sha256-deduplicated — a body identical to the previous record's is not rewritten; the meta still appends, with `body_ref` naming the record that stores those bytes.
- **Tier-2 promotion (automatic, gated):** only a `FETCH_OK` raw record updates the snapshot; `vendor-meta.json.source_raw_record` records exactly which raw record it came from. `update_vendored()` refuses any other status outright.
- **Tier-3 promotion (HUMAN):** a person inspects the tier-2 delta (typically via the field-level projection diff) and lands a kernel change through intent-eval-core's own review + release gates. This repo documents that contract and **never automates it** — no script here may write into the kernel.
- The pre-existing `_vendor/upstream/<contract>/` (contract-keyed, FF#2 skill-frontmatter) remains the differ's reference until wave B folds it into the surface-keyed tier 2.

## Registry contract (per-surface `capture` config)

Each monitored surface in `specs/upstream-surface-registry.v1.json` carries:

```json
"capture": { "kind": "http|command", "urls": ["https://..."], "expect_regex": "...", "min_bytes": 4096, "ext": ".md" }
```

`expect_regex` is the shape hint (the surface's expected extractor pattern); `min_bytes` is the per-surface truncation floor (set ≤ ½ of the observed body size, verified live 2026-06-12); `command` surfaces (e.g. the npm version probe) use `argv` instead of `urls`. `scripts/check-surface-registry.py` validates all of this offline in the "Validate specs and docs" CI job.

## Enforcement

- **Deterministic self-test** (`fetch-capture.py --self-test`, offline fixtures exercising all 6 statuses + append/dedup/tier-2 gating) gates every PR in both `ci.yml` ("Validate specs and docs") and `spec-drift-watch.yml`.
- **Daily capture** runs in `spec-drift-watch.yml` (schedule/dispatch only), commits the archive delta back append-only (`[skip ci]`), and falls back to a workflow artifact if the push is rejected.
- Workflow files are harness-hash-pinned; any edit re-pins `.harness-hash` in the same commit.
