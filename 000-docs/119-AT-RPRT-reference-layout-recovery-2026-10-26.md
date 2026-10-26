# Reference layout recovery

Observed 2026-10-26. Bead: `compile-then-govern-14z`, discovered during
`compile-then-govern-8pg` upstream reverification.

The fixed Lab source at `dd42d4598b4ef1eadef143b31ef5eab1e2de6d13` could not
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

[The execution record](119-AT-RPRT-reference-layout-recovery-2026-10-26.observations.json)
binds source URL, timestamp, response hash and size to extractor source hashes and
bounded structured results. It records author-run observations, not a signed
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

No snapshot, projection baseline, kernel schema, governance tier, freshness date
or deployed consumer is promoted by this change. Field differences from retained
projections remain findings for the existing review process. Normal source review
and required CI precede merge; adoption remains separate under `8pg`.
