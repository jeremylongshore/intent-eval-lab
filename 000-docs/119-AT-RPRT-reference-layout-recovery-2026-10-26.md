---
title: Reference layout recovery
date: 2026-10-26
state_label: INFORMATIVE
---

> **State label: INFORMATIVE.** Execution report; this AT-RPRT carries no normative promotion.

# Reference layout recovery

Observed 2026-10-26. Bead: `compile-then-govern-14z`, discovered during
`compile-then-govern-8pg` upstream reverification.

The baseline Lab source at `dd42d4598b4ef1eadef143b31ef5eab1e2de6d13` could not
extract three current reference pages. Those failures correctly returned exit 2;
they did not establish a clean comparison. This repair supports the new layouts
while preserving extraction from historical frozen captures.

| Reference           | Recovery                                                                                                                                        | Actual private-capture result                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Agent definition    | Recognize the current frontmatter heading; reject duplicate or missing anchors and ignore headings quoted in fences                             | 19 documented fields; required pair retained                                                  |
| Plugin manifest     | Parse the unified Fields table and illustrative manifest separately; preserve table types and refuse missing required-set or validation anchors | 34 documented fields                                                                          |
| Marketplace catalog | Capture the linked normative reference rather than the creation guide; parse unified fields, source forms and conditional strict behavior       | 12 top-level paths, 14 directly listed entry fields, seven source forms and four strict cases |

The registry and byte-hash fetch helpers target the canonical manifest and
marketplace reference URLs. Capture-title checks recognize historical and current
reference titles so existing evidence stays interpretable; the current marketplace
creation-guide title remains refused. Frozen captured files and their provenance
metadata are not rewritten.

[The execution record](../evidence/reference-layout-recovery/observations-2026-10-26.json)
binds source URL, timestamp, response hash and size to extractor source hashes and
bounded structured results. Baseline and current probe results each carry the
same input hash and their exit codes. The initial fix commit is recorded separately
from current extractor blob IDs; later review fixes are identified by their exact
content hashes. A separate guide observation binds the refused guide's URL, title
and response bytes. It records author-run observations, not a signed
attestation. Full upstream documents and generated projections remain private;
future fetches of mutable URLs may return different bytes.

The current marketplace page does not specify every source-field requiredness or
owner-member type. Those remain explicitly unspecified. Inherited manifest fields
are referenced, not inferred from examples. Plugin sources remain separate from
settings-level marketplace sources. A current illustrative manifest is not called
a complete schema.

Recovery tests cover historical extraction, current layouts, missing required
facts, duplicate sections and fields, guide-page refusal, source discriminators,
relative-source alternatives and all strict-table result cells. Strict zip
checking exposed and fixed a reused-header bug that otherwise dropped the fourth
strict-table column. Earlier passing fixture counts alone did not catch that bug.

Existing frozen capture and projection freshness records are unchanged; new
source-observation timestamps record the URL migrations. No snapshot, projection
baseline, kernel schema, governance tier or deployed consumer is promoted.
Field differences from retained
projections remain findings for the existing review process. Normal source review
and required CI precede merge; adoption remains separate under `8pg`.

The URL corrections are normative registry changes under
[050, Change discipline](050-AT-SPEC-upstream-surface-registry-2026-06-11.md#change-discipline),
subject to the owning review, changelog and CI gates. They retain the same surface
identities and reference authority tier. They do not authorize kernel adoption:
[052, The three tiers](052-AT-SPEC-fetch-failure-taxonomy-and-three-tier-archive-2026-06-12.md#the-three-tiers-promotion-is-one-directional)
requires a separate tier-3 review and release path.

Local test counts and static checks in the PR are author-reported runs. Independent
GitHub evidence for the pre-review-fix head `103ba83` includes
[the scripts and research tests](https://github.com/jeremylongshore/intent-eval-lab/actions/runs/40410988337)
and [the full spec/document gate](https://github.com/jeremylongshore/intent-eval-lab/actions/runs/40410987857).
Later source changes require their own checks; these links do not certify a later head.
