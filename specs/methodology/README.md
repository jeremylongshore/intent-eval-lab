# Methodology — cross-module patterns

> **Status: placeholder.** This module is reserved for cross-module methodology patterns that apply to multiple specs under [`specs/`](../). Patterns get promoted here once they're observed working in at least two modules.

## Methodology-spec index

Most modules under [`specs/`](../) are **contract / conformance** specs (a system class → its normative requirements). A few are **methodology** specs — they codify _how to evaluate_ a kind of artifact, reusing the platform's shared substrate (MatcherMap / JudgeDecision / EvidenceBundle) rather than defining a new system class. This section indexes them:

| Methodology spec                                                                         | Codifies                                                                                                             | Status                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`../prompt-evaluation/v0.1.0-draft/SPEC.md`](../prompt-evaluation/v0.1.0-draft/SPEC.md) | Evaluating prompts + context templates as eval targets (the prompt→context-engineering generalization beyond skills) | v0.1.0-draft skeleton; gated — see [`000-docs/043-DR-RFC-intent-eval-target-generalization-2026-06-06.md`](../../000-docs/043-DR-RFC-intent-eval-target-generalization-2026-06-06.md) and landscape [`000-docs/042-RR-LAND-...md`](../../000-docs/042-RR-LAND-prompt-and-context-eval-landscape-2026-06-06.md) |

New methodology specs are added here as research warrants. The patterns below are the
cross-cutting disciplines every methodology spec inherits.

## Patterns observed in early modules (provisional, not yet normative)

- **Toulmin-structured findings.** Every finding in a conformance report includes a _claim_ (what the spec requirement is), a _warrant_ (the canonical authority the requirement codifies), _grounds_ (the empirical evidence the requirement isn't satisfied), and a _qualifier_ (severity / scope of the failure). This structure is currently in use in the `mcp-plugin-observability` module's case-study reports.

- **Diagnostic-first auditing.** Findings are stated as _observed failure modes_ with reproduction steps, not as _prescribed fixes_. The fix shape is left to the implementer; the spec describes what conformance looks like, not how to achieve it. Implementers may converge on common fix patterns (and those patterns get codified later as informative annexes), but the spec itself stays diagnostic.

- **Conformance vs eval distinction.** A spec module is _conformance-shaped_ — pass/fail against normative requirements. A research output is _eval-shaped_ — relative measurement, ranking, A/B comparison. Both are valid outputs; they belong in different artifacts. Don't conflate "this plugin is conformant against v0.1.0-draft" (a binary claim) with "this plugin scored 87/100 on the discovery-rate eval" (a quantitative measurement).

- **Vendor-neutrality enforcement.** Every spec module's normative section should be readable as if the reader has never heard of the first case-study vendor. Vendor-specific instantiation goes in `case-studies/`. If a normative requirement reads as "X must do Y where X is the first vendor we worked with," it's drifted out of the module spec and into the case study.

- **Anchoring discipline.** Every normative requirement cites the canonical upstream source it codifies — the vendor's own docs, an RFC, an ISO standard, a published academic methodology. Specs are _codifying what's already canonical_, not inventing. Inventions belong in research outputs (`000-docs/` or `research/` at repo root), not in `specs/`.

## When this module will get a real authored doc

When at least two modules (e.g., `mcp-plugin-observability` and one of the placeholder modules) have shipped to `vN.M.K-rc` or beyond, the patterns observable across both get promoted from this provisional list to a properly authored cross-module methodology document.

## RFC

Methodology suggestions, counter-proposals, and challenges to the conformance-vs-eval distinction welcome via GitHub issues on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab).
