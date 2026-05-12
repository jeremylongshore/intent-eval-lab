# CONTRIBUTING — failure-shape contributions (MM-7+)

> **Status:** Normative — admission criteria for new failure-mode (MM-N) categories beyond MM-1..MM-6.
> **Authority:** ISEDC v1 Q3 binding constraint (`000-docs/004-AT-DECR-isedc-council-record-2026-05-10.md`)
> applied to Milestone 1 of the build journey (`~/.claude/plans/se-the-council-bubbly-frog.md`).

---

## 1. What this document is

The Intentional Mapping vocabulary defines six failure-mode categories at v0.1.0-draft:

| ID | Shorthand |
|---|---|
| MM-1 | async race |
| MM-2 | shape drift |
| MM-3 | cooldown |
| MM-4 | side-effect |
| MM-5 | (reserved — see `intentional-mapping-template.md`) |
| MM-6 | (reserved — see `intentional-mapping-template.md`) |

ISEDC v1 explicitly **deferred MM-7+** in Q3 with the discipline that new categories admit only
through a community contribution path that prevents MM-N inflation. This file is that path.

A new MM-N is a permanent addition to the Intent Eval Platform's behavioral evaluation surface.
Once MM-7 exists, it carries a normative obligation across every conforming j-rig run. Adding
one is irreversible — minor versions add MM-Ns; major versions cannot remove them without
breaking conformance for every prior signed Evidence Bundle row that referenced them.

## 2. Admission criteria — all three required

A proposal for MM-N (where N ≥ 7) is admitted into a future minor version of this spec only when
**all three** criteria are demonstrably met. A reviewing maintainer who cannot verify any one of
the three rejects the proposal with a written explanation against the unmet criterion.

### C1 — Independent observation in ≥2 engagements

The proposed failure shape **MUST** have been observed in at least **two independent
engagements**. "Independent" means:

- Two distinct codebases (different repos, different organizations);
- Two distinct teams (no shared engineer between the two);
- Two distinct evaluation runs (each run produced telemetry the proposer can cite).

A single engagement that hits the failure shape twice does not satisfy C1. A failure observed
once in production and once in a sandbox by the same engineer does not satisfy C1.

The proposer **MUST** cite both engagements in the proposal. Engagement names **MAY** be redacted
under the project's brand-name policy (`intent-eval-lab/CLAUDE.md` § "Brand-name policy") if
written partner consent is not on file. In that case, the proposer cites generic identifiers
(e.g. "engagement A — enterprise SaaS in healthcare; engagement B — open-source library
maintainer team") and the reviewing maintainer takes the redaction at face value.

### C2 — Type-distinct from MM-1..MM-6

The proposed failure shape **MUST NOT** type-fit any existing MM category. A proposal that is a
specialization of MM-2 ("shape drift, but for response headers specifically") is a metadata
refinement of MM-2, not a new category. A proposal that overlaps two existing categories
("looks like MM-3 cooldown but with the side-effect signal of MM-4") is a categorization
ambiguity, not a new category.

The proposer **MUST** include a comparative analysis: for each of MM-1..MM-6, why the new shape
is not an instance of that category. The analysis **MUST** cite specific behavioral signals that
distinguish the new shape from each existing category.

A reviewing maintainer who finds the new shape is more naturally MM-K (for K ∈ {1..6}) rejects
the proposal and recommends instead opening an issue against MM-K's documentation to clarify the
boundary.

### C3 — OTel signal vocabulary draft

The proposer **MUST** include a draft OpenTelemetry signal-vocabulary entry for the new MM-N
category. The draft **MUST**:

- Propose a stable signal name in the `agent.mm_category` family (e.g. `agent.mm_category.MM-7`).
- Define the attributes that distinguish a passing observation from a failing observation.
- Cite the OTel semantic-conventions repository's review process for the relevant SIG group
  (typically `semconv-genai`).
- Indicate whether the proposer commits to championing the OTel RFC themselves or is delegating
  to Intent Solutions / the spec maintainer to file.

C3 ensures that adding a category to the spec is matched by extending the platform's
observability surface. A category that is not OTel-emittable is invisible to operator dashboards
and undermines the platform's "single observability plane" property (system brief
`007-DR-BRIEF` § 7).

## 3. Submission process

1. **Open a GitHub issue** in `jeremylongshore/intent-eval-lab` titled
   `[mcp-plugin-observability] MM-N proposal: <shorthand>`.
2. **Cite this document** explicitly in the issue body — confirm each of C1, C2, C3 is met
   and provide the supporting evidence.
3. **Tag `[mcp-plugin-observability]`** so triage routes to the correct maintainer.
4. **Expect a response within 14 calendar days**. Maintainer either accepts (issue moves to a
   PR adding the category to the spec at the next minor version), requests revision (specific
   criterion not met), or rejects with explanation (no category warranted).

The maintainer **MUST NOT** silently accept or silently reject. Every proposal receives written
adjudication against C1, C2, C3 in the issue thread.

## 4. After admission — what minor-version landing entails

When a proposal is admitted, the next minor version of `mcp-plugin-observability` (e.g.
`v0.2.0`) ships:

- A new section in the spec defining MM-N's failure shape, signals, and PASS/FAIL/NOT_APPLICABLE
  semantics.
- An update to `intentional-mapping-template.md` with the new category.
- An update to the OTel signal vocabulary draft for filing against the OTel SIG-GenAI working
  group on the next standards-track cycle.
- A note in `000-docs/008-DR-GAPS-...md` (or its successor) recording the admission.

J-rig adds an emitter for the new category in its next compatible minor version. Existing signed
Evidence Bundle rows that pre-date the new category are unaffected; coverage policies in
`tests/TESTING.md` may opt in to requiring the new category at the team's discretion.

## 5. Why this gate exists

ISEDC Session 1 deliberated MM-7+ admission and concluded:

> Adding categories under engineering pressure or external suggestion (without independent
> observation) inflates the vocabulary into noise. The discipline is that a new category is
> earned through observation in the field, not proposed in a brainstorm.
>
> — paraphrased from ISEDC v1 Q3 council memos

This file operationalizes that discipline. A proposal that does not meet C1, C2, C3 is not a
failure of the proposer — it is a signal that the failure shape is either not yet generalizable
(needs more observation) or is naturally an extension of an existing category.

## 6. License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
