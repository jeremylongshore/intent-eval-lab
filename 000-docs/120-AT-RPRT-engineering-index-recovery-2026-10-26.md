---
title: Engineering index recovery
date: 2026-10-26
state_label: INFORMATIVE
---

> **State label: INFORMATIVE.** Execution report; this AT-RPRT carries no normative promotion.

# Engineering index recovery

Bead `compile-then-govern-v0y`, discovered during `compile-then-govern-8pg`.

The captured engineering index now links featured articles under `/research/`.
The baseline watcher's `/engineering/<slug>` pattern finds nothing in the actual
HTTP 200 response. That remains an extraction failure, not an empty hash or a
clean comparison.

The replacement offline parser requires the engineering canonical URL and one
complete main content area. For the current layout, one engineering featured
carousel must supply matching first image and title links. Navigation and unrelated
research links do not select the signal. Missing or ambiguous structure returns
exit 2 without stdout; curl failure remains a failed watcher extraction.

The actual frozen engineering capture still produces exactly the original
`href="/engineering/how-we-contain-claude"` sentinel with its trailing newline,
matching the retained baseline hash. The current captured body produces
`href="/research/redesigning-source-control"` with a trailing newline. A changed
signal is evidence for review, not baseline acceptance or article-content analysis.

[The execution record](../evidence/engineering-index-recovery/observations-2026-10-26.json)
binds the actual input digests, parser source, outputs and exit codes. These are
unsigned author-run observations. Current raw HTML remains private; the historical
capture was already tracked. Mutable URLs may later yield different bodies.

The capture-shape hint supports both path layouts, requires index identity and
looks for the signal within main content. The byte floor is unchanged. Both actual
captures classify `FETCH_OK` under the updated hint; the pure parser provides the
stricter article selection. The shape hint alone does not establish extraction or
compatibility. The detector-health document is regenerated at its retained
evaluation date; the DEGRADED verdict and watcher history remain unchanged.

Registry changes follow [050, Change discipline](050-AT-SPEC-upstream-surface-registry-2026-06-11.md#change-discipline).
The source URL, authority tier, baseline, snapshots and freshness dates are retained.
No watcher poll, baseline refresh, upstream content promotion or deployment is run.
Owning CI, review and guarded merge remain required before this repair is complete.
