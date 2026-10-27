---
title: Engineering index recovery
date: 2026-10-26
state_label: INFORMATIVE
---

> **State label: INFORMATIVE.** Execution report; this AT-RPRT carries no normative promotion.

# Engineering index recovery

Bead `compile-then-govern-v0y`, discovered during `compile-then-govern-8pg`.

The observed first featured link uses `/research/`.
The baseline watcher's `/engineering/<slug>` relative-href pattern finds nothing in the actual
HTTP 200 response. That remains an extraction failure, not an empty hash or a
clean comparison.

The replacement offline parser requires the engineering canonical URL and one
complete main content area. When a recognized `HeroCarousel` is present,
exactly one carousel must have the Engineering topic and matching first image and
title article links. Otherwise the parser falls back to the first legacy
`/engineering/<slug>` link within that sole main area. It cannot distinguish a
legacy page from a newer page that lost its carousel but retains a legacy link.
Without either supported signal, or with ambiguous structure, it returns exit 2
without stdout; curl failure remains a failed watcher extraction.

Parser input is capped at 4 MiB and 256 simultaneously open elements. Overflow
is indeterminate (exit 2 without stdout), even when a valid article prefix exists.
Context flags and indexed open-tag positions avoid full ancestor scans for each
start or unmatched end tag. The capture hint commits to the first main-shaped
area, and canonical attribute searches stay within each link-shaped tag. Timed
synthetic controls cover repeated main markers, deep nesting, unmatched closes,
and the input-size boundary; they do not establish a universal CPU-time bound.

The actual frozen engineering capture still produces exactly the original
`href="/engineering/how-we-contain-claude"` sentinel with its trailing newline,
matching the retained baseline hash. The unsigned author observation record
reports that the current captured body produces
`href="/research/redesigning-source-control"` with a trailing newline. A changed
signal is evidence for review, not baseline acceptance or article-content analysis.

[The execution record](../evidence/engineering-index-recovery/observations-2026-10-26.json)
binds the actual input digests, parser source, outputs and exit codes. These are
unsigned author-run observations. The canonical URL is a declared content marker;
HTTP origin, final URL, status and transport provenance are separate fetch metadata.
Current raw HTML remains private; the historical
capture was already tracked. Mutable URLs may later yield different bodies.

The capture-shape hint supports both path layouts and looks for canonical-shaped
markup plus a signal within main-shaped markup. Attribute boundaries reject
`data-rel` and `data-href` decoys. This remains a regex heuristic; the pure HTML
parser provides the stricter declared-canonical checks and article selection. The byte floor is
unchanged. The unsigned author observation record reports that both actual
captures classify `FETCH_OK` under the updated hint; the pure parser provides the
stricter article selection. The shape hint alone does not establish extraction or
compatibility. The detector-health document is regenerated at its retained
evaluation date; the DEGRADED verdict and watcher history remain unchanged.

Registry changes follow [050, Change discipline](050-AT-SPEC-upstream-surface-registry-2026-06-11.md#change-discipline).
The source URL, authority tier, baseline, snapshots and freshness dates are retained.
No watcher poll, baseline refresh, upstream content promotion or deployment is run.
Owning CI, review and guarded merge remain required before this repair is complete.
