# 058 — Plugin-manifest deep capture + projection contract (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** 045-RR-LAND (SSoT + continuous spec-compliance), 050-AT-SPEC (surface registry), 052-AT-SPEC (fetch taxonomy + tiers), 054-AT-SPEC (lineage log), 056-AT-SPEC (the mcp-config template this capture stamps) · **Epic:** 9k5h (GH intent-eval-lab#114)

The `plugin-manifest` contract gets the deep capture `skill-frontmatter` and `mcp-config` already have. **Documented deviation from 056:** there is **no machine-readable upstream schema** for `.claude-plugin/plugin.json` and no upstream spec versioning — the `code.claude.com/docs/en/plugins-reference` page IS the spec (prose + field tables + JSON examples) and sample manifests from `anthropics/claude-plugins-official` are real-world corroboration (authority precedence per 050-AT-SPEC: the reference page is the spec; samples corroborate). `spec_version` is therefore the capture date (`unversioned-2026-06-12`), not an upstream-declared revision. Implementation: `specs/_vendor/upstream/plugin-manifest/` + `scripts/extract-plugin-manifest-projection.py`.

## The vendored capture (contract-keyed tier-2)

| File | Authority | What |
|---|---|---|
| `claude-code-plugins-reference.md` | reference (registered surface `plugins-reference`) | The plugins-reference page, `.md` form — the same URL/form the registry's `fetch_plugins_reference` extractor monitors. § "Plugin manifest schema" carries the Required / Metadata / Component-path field tables, the Complete-schema example, and the tolerance prose. |
| `sample-*.plugin.json` (5) | sample-corroboration | Commit-pinned (`eb1510e1`) manifests from the official plugins repo, chosen for structural diversity (per-file `selection_basis` in `vendor-meta.json`). Ground-truth negative: NO official manifest uses any component-path field. |
| `vendor-meta.json` | — | Per-file provenance (source URL + ref SHA + sha256 + bytes + `fetched_at`), 052-AT-SPEC conventions. |
| `projection.json` | — | The **normative projection** (below). GENERATED — never hand-edit. |

The fetch happened **once** at build time (2026-06-12). CI never refetches — offline determinism; ongoing freshness comes from the watcher's daily run over the registered `plugins-reference` surface. `claude-plugins-official` is an `unmonitored_candidates` registry row, not a registered surface; the samples' `vendor-meta.json` entries are their provenance records until one is registered per 050-AT-SPEC change discipline.

## The normative projection (FF#2 left-hand side for plugin-manifest)

`scripts/extract-plugin-manifest-projection.py` extracts `projection.json` deterministically from the vendored bytes alone — sorted keys, **no wall-clock in the output**. Every fact is mechanical: table rows parsed from the three named tables (escaped-pipe union types like `string\|array` unescaped, dotted `experimental.*` fields verbatim, `One of …` enum clauses where stated), the Complete-schema JSON example parsed, four anchor sentences matched (`name`-only-required is a hard anchor — exit 2 if missing), and the sample JSON cross-corroborated.

**The documented-vs-observed field provenance rule (conservative by construction):** a field the page documents is `source: "documented"` with `required` known (`true` only for `name`, per the page's own sentence); a field used in samples but absent from the page is `source: "observed-in-samples"` with `required: "unknown"` — **never promoted to documented**. Current capture: **23 documented fields** (1 required + 10 metadata + 12 component-path), **zero observed-only fields** — every field the official samples use is page-documented, recorded as the `samples-corroborate` agreement below.

## Cross-check against the kernel (read-only; findings, never fixes)

The self-test cross-checks the committed projection against the kernel's expectations (`intent-eval-core` `schemas/authoring/v1/upstream-base/plugin-manifest.v1.json`, embedded as fixtures — the kernel is another repo and CI is offline). Both finding sets are exact-matched, so a re-capture that shifts any finding fails loud and a human reconciles:

- **Agreements (10):** `name`-only-required on both sides; field types match for `description`/`homepage`/`keywords`/`license`/`repository`/`version`; author is an object with the documented `{name,email,url}` shape (sample-corroborated); the doc's kebab-case prose is what the kernel's `name` pattern encodes; no observed-only sample fields.
- **Divergences (5, reported NOT fixed — tier-3 promotion is human per 052-AT-SPEC):**
  1. `component-paths` — the kernel models only `commands` of the 12 documented component-path fields (`agents`, `channels`, `dependencies`, `experimental.monitors`, `experimental.themes`, `hooks`, `lspServers`, `mcpServers`, `outputStyles`, `skills`, `userConfig` are unmodeled).
  2. `commands-type` — upstream allows `string|array`; the kernel narrows to array-only (a documented IS projection choice).
  3. `metadata-fields` — `$schema`, `defaultEnabled`, `displayName` are page-documented but absent from the kernel.
  4. `kernel-only` — the kernel's `metadata` extension object is not a documented upstream field (it encodes the page's unrecognized-top-level tolerance structurally).
  5. `name-maxlength` — the kernel's 64-char cap on `name` is not documented upstream.

## Enforcement

- **CI** (`ci.yml` "Validate specs and docs", appended step): `extract-plugin-manifest-projection.py --check` (committed projection must equal a fresh extraction — staleness fails) + `--self-test` (fixture anchors, missing-anchor exit-2, staleness detection, kernel cross-check exact-match). Offline, deterministic.
- **Lineage** (054-AT-SPEC): the capture appended `snapshot-updated` event 21 (`plugins-reference`, `upstream_version` = the doc sha256, subject `plugin-manifest`) via the documented CLI; the coverage map regenerated in the same append, and the detector-health composite (057-AT-SPEC, whose inputs include the coverage map) regenerated in the same commit.
- Workflow files stay harness-hash-pinned; the ci.yml edit re-pinned `.harness-hash` in the same commit.
