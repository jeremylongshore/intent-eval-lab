# 061 — Marketplace-catalog deep capture + projection contract (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + tiers), 054-AT-SPEC (lineage log), 058/059/060-AT-SPEC (the plugin-manifest + agent-definition + hook-config analogs this capture stamps) · **Epic:** 9k5h (GH intent-eval-lab#114)

The `marketplace-catalog` contract gets the deep capture the other five contracts already have — the sixth and **FINAL** stamp of the program. Like 058/059/060: there is **no machine-readable upstream schema** for `.claude-plugin/marketplace.json` and no upstream spec versioning — the `code.claude.com/docs/en/plugin-marketplaces` page IS the spec (the Marketplace-schema Required/Owner/Optional field tables + the Reserved-names note + the metadata back-compat sentence, the Plugin-entries Required + Standard-metadata + Component-configuration tables, the Plugin-sources 5-form summary table + four per-type `Field|Type|Description` tables + the sha-beats-ref rule, and the Strict-mode table) and the **official catalog itself** corroborates it (precedence per 050-AT-SPEC: the reference page is the spec; samples corroborate). **Deviation from 060:** exactly ONE sample, but it is the ground truth — `anthropics/claude-plugins-official` `.claude-plugin/marketplace.json` (commit-pinned `eb1510e1`, the same pin 058/059/060 use; 223 plugin entries; vendored WHOLE at 126,953 bytes, under the 200KB truncation threshold, so no truncated slice was needed). The page documents exactly one catalog file form (negative fact in `vendor-meta.json`). `spec_version` is the capture date (`unversioned-2026-06-12`). Implementation: `specs/_vendor/upstream/marketplace-catalog/` + `scripts/extract-marketplace-catalog-projection.py`.

## The vendored capture (contract-keyed tier-2)

| File | Authority | What |
|---|---|---|
| `claude-code-plugin-marketplaces.md` | reference (registered surface `plugin-marketplaces`) | The plugin-marketplaces reference page, `.md` form — the same URL/form the registry's `fetch_plugin_marketplaces` extractor monitors. Carries the 8 documented top-level fields (3 required), the 14 reserved marketplace names, the owner shape, the 20 documented plugin-entry fields, the 5 source forms, and the strict-mode semantics. |
| `sample-claude-plugins-official.marketplace.json` | sample-corroboration | THE official catalog, commit-pinned (`eb1510e1`). Ground truth: 50 `./`-prefixed string sources, 173 object sources across github/url/git-subdir, 13 of 20 documented entry fields exercised — plus three tolerances on no documented table (`commit` on github sources, `path` on url sources, the plugin name `wordpress.com`). |
| `vendor-meta.json` | — | Per-file provenance (source URL + commit pin + sha256 + bytes + `fetched_at`), 052-AT-SPEC conventions. |
| `projection.json` | — | The **normative projection** (below). GENERATED — never hand-edit. |

The fetch happened **once** at build time (2026-06-12). CI never refetches — offline determinism; ongoing freshness comes from the watcher's daily run over the registered `plugin-marketplaces` surface. `claude-plugins-official` is an `unmonitored_candidates` registry row; the sample's `vendor-meta.json` entry is its provenance record until a sampleable surface is registered per 050-AT-SPEC change discipline.

## The normative projection (FF#2 left-hand side for marketplace-catalog)

`scripts/extract-marketplace-catalog-projection.py` extracts `projection.json` deterministically from the vendored bytes alone — sorted keys, **no wall-clock in the output**. Every fact is mechanical: the top-level required/optional fields by table membership (`name`/`owner`/`plugins` required; `$schema`, `description`, `version`, `metadata.pluginRoot`, `allowCrossMarketplaceDependenciesOn` optional, plus the `description`/`version`-under-`metadata` back-compat sentence and the 14 reserved names), the owner table (capitalized Yes/No Required column), the 20 plugin-entry fields (2 required + 12 standard-metadata + 6 component-config, sliced on the bold sub-table markers; the duplicated `### Required fields` heading is resolved by two-level scoped slicing), the 5 source forms (the `./`-prefixed string form + github/url/git-subdir/npm object types whose summary-table `?`-suffix sets are exact-matched against the per-type `Required.`/`Optional.` description prefixes — any contradiction exits 2 — and whose `source` discriminator key is verified from each section's fenced JSON example), the sha-beats-ref rule, and strict default `true`.

**The documented-vs-observed field provenance rule (conservative by construction):** anything the page documents is `source: "documented"`; anything used in the official catalog but absent from the page lands under the projection's `samples.*_not_documented` / `*_outside_documented` keys — **never promoted to documented**. Current capture: every sample top-level key, entry field, and source type is documented; **three tolerances** sit outside the documented surface (`commit` on 2 github sources, `path` on 5 url sources, the non-kebab plugin name `wordpress.com`), recorded as the divergence below.

## Cross-check against the kernel (read-only; findings, never fixes)

The self-test cross-checks the committed projection against the kernel's expectations (`intent-eval-core` `schemas/authoring/v1/upstream-base/marketplace-catalog.v1.json`, embedded as fixtures — the kernel is another repo and CI is offline). Both finding sets are exact-matched, so a re-capture that shifts any finding fails loud and a human reconciles:

- **Agreements (4):** top-level required is exactly `[name, owner, plugins]` on both sides; the owner shape (inner `name` required, `email` optional) matches; the plugin-entry minimum (`name` + `source`) matches; the sample stays within the documented top-level-key, entry-field, and source-type sets.
- **Divergences (6, reported NOT fixed — tier-3 promotion is human per 052-AT-SPEC):**
  1. `plugins-min-items` — the kernel requires `minItems: 1` (corpus-rationalized in its `$comment`); the doc states no minimum.
  2. `doc-top-level-optional-fields-not-in-kernel` — `$schema`, `allowCrossMarketplaceDependenciesOn`, `description`, `version` (the kernel models `metadata` generically).
  3. `doc-plugin-entry-optional-fields-not-in-kernel` — all 18 documented optional entry fields are unmodeled (the kernel's item schema carries only `name`).
  4. `source-forms` — the doc documents the relative-path string form + 4 object types; the kernel requires `source` but gives it no schema.
  5. `name-constraints` — the kernel adds `maxLength: 64` + the kebab regex; the doc states kebab-case in prose only, and its 14 reserved names are not encoded anywhere in the kernel.
  6. `samples:tolerances-outside-documented-surface` — `github:commit`, `url:path`, `plugin-name:wordpress.com` (upstream tolerances observed in the official catalog).

## Enforcement

- **CI** (`ci.yml` "Validate specs and docs", appended step): `extract-marketplace-catalog-projection.py --check` (committed projection must equal a fresh extraction — staleness fails) + `--self-test` (fixture anchors, contradiction/discriminator/missing-anchor exit-2 modes, staleness detection, kernel cross-check exact-match). Offline, deterministic.
- **Lineage** (054-AT-SPEC): the capture appended `snapshot-updated` event 24 (`plugin-marketplaces`, `upstream_version` = the doc sha256, subject `marketplace-catalog`) via the documented CLI; the coverage map regenerated in the same append, and the detector-health composite (057-AT-SPEC) regenerated in the same commit.
- Workflow files stay harness-hash-pinned; the ci.yml edit re-pinned `.harness-hash` in the same commit.

## Program completion — all six contracts now have deep captures

This capture **completes the deep-capture program**: every authoring contract the kernel models now has a vendored upstream source of record plus a deterministic projection. `skill-frontmatter` got it first via the 6767-b standard + the kernel's base/overlay layers; `mcp-config` (056), `plugin-manifest` (058), `agent-definition` (059), `hook-config` (060), and `marketplace-catalog` (this doc, 061) got it via the `specs/_vendor/upstream/` tier. The accumulated kernel-divergence findings across docs 056/058/059/060/061 are the standing tier-3 reconciliation queue — each is a human-adjudicated promotion candidate per 052-AT-SPEC, and the cross-check exact-match harness in each extractor keeps every queue entry pinned until a human settles it.
