# Draft decision on Phase A.0 evidence and public claims

**Status:** DRAFT — awaiting acting-head adjudication.

**Date:** 2026-10-19

**Beads:** `bd_000-projects-436s`; parent `bd_000-projects-1j6k`.

**Authority:** proposed successor to [DR-036](./036-AT-DECR-phase-a0-result-proceed-2026-05-31.md), under its section 4 acting-head override; publication follows [DR-039 section 2](./039-AT-DECR-evidence-bench-public-scorecard-2026-06-02.md).

The retained Phase A.0 records do not support the published attribution of the
Refiner's apparent advantage entirely to its editing mechanism. The arms used
different baseline scores, seven inputs differ from their manifest identities,
and ten Arm B specimens entered the analysis without a completed proposal after
an initial API failure. The proposal is to correct the public interpretation,
preserve the original records and signature, and require a newly registered
experiment before presenting this run as evidence of comparative effectiveness.

This draft does not replace the historical PROCEED with DESCOPE, change the
existing product roadmap, or select a revised statistical estimator. Acting-head
approval would adopt the dispositions below; until then they remain proposals.

## Reproducible findings

The [input audit](../research/phase-a-0-baseline/reviews/2026-10-19/input-audit.json)
records each specimen and SHA-256 hashes of all 761 source files read by the
[replay script](../scripts/audit-phase-a0-history.py). It uses the retained local
raw run archive, which the original design deliberately excluded from Git.
The public aggregate is reviewable here; a complete replay also needs that
archive. It contains no provider calls and produces no revised experiment verdict.

| Finding                                      | Evidence                                                                                                                                                                                                                                         | Consequence                                                                                                                                                                                               |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Different baseline scores in all 60 pairs    | Arm A used cached manifest scores; Arm B scored the loaded file in an isolated directory. Mean A baseline minus B baseline: 7.5667 percentage points.                                                                                            | The historical 6.6833-point difference between arm deltas combines edit effects with unequal baselines.                                                                                                   |
| Filesystem context affects the judge         | Validator `7b9eb8f0a77d285dee3ffe99c913d039c4878aec` scores name/directory agreement and supporting references. A dated local check of six unchanged source files reproduced their manifest scores in place and lower Arm B scores in isolation. | An unchanged instruction body does not make all non-header score components cancel.                                                                                                                       |
| Seven inputs differ from manifest hashes     | Recovered inputs match the manifest for 53 of 60 specimens. The mismatched prefixes are `22875bce`, `4223d993`, `4c9239de`, `92af0bd2`, `c7cc88ef`, `e0d0d400`, `f2a8f2e9`.                                                                      | A manifest identifier in a record does not establish which bytes were loaded. The historical runners read mutable paths without validating the digest.                                                    |
| Ten specimens contain no completed proposal  | Each has zero proposal files, an empty trajectory and a matching iteration-0 HTTP 429 error. The Arm B summary nevertheless reports zero errors; the aggregate includes all 60 specimens.                                                        | These are infrastructure failures, not evidence that the acceptance mechanism rejected an edit. DESIGN section 6 requires failed samples to be excluded from headline statistics and reported separately. |
| All retained baseline scores can be replayed | The pinned validator reproduces all 60 Arm B baseline scores from recovered inputs. All 240 Arm A prompt headers agree with those inputs' headers.                                                                                               | The score discrepancy is reproducible; this does not independently establish the exact executable used during the historical run or the original supporting-directory snapshot.                           |

For 51 rejected specimens, `final.md` retains the loaded input. For the nine
accepted specimens, recovery combines the original header from `proposal-0.json`
with the body preserved by the historical `apply_proposal` function. All nine
reconstructions match the full manifest digest. This establishes those recovered
bytes without treating generated edits as original inputs.

The ten zero-proposal prefixes are `272a48af`, `2b9b4960`, `3834230f`, `51b81c90`,
`8a7bb1a0`, `a4978361`, `bc56c6d1`, `c25434b3`, `c564eed3`, `f8ba830b`.
Their retained error events explain why a reported no-change observation must
not be described as a successful conservative rejection.

The original judge executable was not cryptographically verified by the runner:
`score-fixture.py --commit` supplied a label while executing a configured script
path. Matching today's pinned replay establishes compatibility with that judge,
not independent proof of the executable's historical identity. The six source
context observations likewise do not reconstruct every historical directory.

## Methodology dispositions proposed for approval

| Surface                  | Retained implementation or record                                                                                                                                                                                                        | Proposed disposition                                                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scalar decision rule     | DR-028 uses projected lift; the analyzer uses the fixed 1.5-point projection and strict greater-than-70% comparison. The template also describes an observed A/B ratio, reverses margin labels and connects the verdict to significance. | Preserve the historical output as a record. Reconcile the denominator, direction and role of hypothesis tests explicitly in a new registration before collecting new data. No retrospective threshold choice. |
| Primary test             | Shapiro on paired differences, then paired t-test or signed rank; the template shows normality for each arm and an independent-sample t-test. The historical run used signed rank.                                                       | Correct labels, disclose the method discrepancy and select a matched-design analysis prospectively. Do not substitute a new test into the signed historical result.                                           |
| Stratum interaction      | Separate Welch tests within strata; no two-way ANOVA interaction test.                                                                                                                                                                   | Withdraw the interaction/generalization interpretation. Specify a suitable design and multiplicity policy before a new experiment.                                                                            |
| K comparisons            | Unadjusted one-sided contrasts; the template describes adjusted paired comparisons.                                                                                                                                                      | Label these exploratory historical calculations. Pre-specify correction and best-K selection for the new run.                                                                                                 |
| Goodhart audit           | Acceptance counts stand in for a five-dimension audit. The template and implementation disagree on dimensions, including description length versus security findings.                                                                    | Do not call the audit completed. Define each dimension, its direction and correction policy before auditing or collecting new evidence. Acceptance flags alone do not prove non-degradation.                  |
| Infrastructure failures  | Ten unexecuted proposal sequences remain in the 60-pair result.                                                                                                                                                                          | Disclose failures separately. Register treatment of incomplete pairs and retries before the next run; do not remove rows post hoc and present a replacement confirmatory verdict.                             |
| Input and judge identity | Mutable source paths, cached versus rescored baselines, and a descriptive judge-commit label.                                                                                                                                            | Freeze complete input contexts, verify file and executable digests at execution, score both baselines in equivalent contexts, and keep per-attempt provenance.                                                |

[PR #407](https://github.com/jeremylongshore/intent-eval-lab/pull/407) and
[PR #408](https://github.com/jeremylongshore/intent-eval-lab/pull/408) already make
the current analyzer refuse incomplete or incomparable cohorts, non-finite
statistics, existing output files, and missing or simulated response records.
They expose method limitations; they do not repair the historical experiment.

## Proposed decision

1. **Retire the comparative-effectiveness interpretation of this run.** Treat
   the historical p-value, effect size and lift comparison as recorded outputs
   from an experiment with unresolved validity defects, not as evidence that
   the Refiner outperforms the naive arm. This is not evidence that the opposite
   claim is true.
2. **Preserve historical evidence.** Keep RESULTS, DESIGN, the original decision
   record, aggregate JSON, signed bundle and Rekor entry unchanged. Publish this
   successor record and a prominent correction on the scorecard and walkthrough.
   Any future signed correction must be a new bundle referencing the original,
   as DR-039 requires.
3. **Separate the product decision from this empirical claim.** Preserve the
   fact that PROCEED was decided in May. Continuing engineering must not be
   presented as newly justified by this experiment. This decision alone neither
   cancels nor reauthorizes the present roadmap or package releases.
4. **Require new registered evidence for renewed effectiveness claims.** Freeze
   input context and executable identity, resolve the methods above, define
   failure treatment, complete the Goodhart audit and report both arms
   symmetrically. A corrected analysis of old observations may be exploratory;
   it must be versioned and must not be called a new confirmatory experiment.

## Exact public correction proposed

> **Correction to the Phase A.0 interpretation**
>
> The original experiment was reported as evidence that the Refiner outperformed
> naive prompting. A later audit found unequal baseline scoring contexts, seven
> inputs that differ from their manifest hashes, and ten Arm B specimens with
> no completed proposal after API failures. Those problems prevent attributing
> the published comparison to the editing mechanism. We no longer present this
> run as evidence of comparative effectiveness. The original results and
> signature remain available as historical records; the signature establishes
> artifact integrity, not scientific validity. A new registered experiment is
> required before renewing the effectiveness claim.

The walkthrough should replace the claim of a demonstrated win, the attribution
of an example's entire score drop to its header edit, and the interpretation of
a p-value as the probability that the result was a fluke. Both arms' original
numbers may remain together in a clearly labeled historical table, with the
correction above it and links to this record and the original proof.

## Affected claims and publication scope

| Surface                                                                               | Required treatment after approval                                                                                                                                                    |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Public walkthrough](https://labs.intentsolutions.io/eval-sets/j-rig-bench/phase-a0/) | Replace the current efficacy narrative and header-only causal attribution with the correction, historical table, method limits and unchanged proof links.                            |
| [Evidence Bench row](https://labs.intentsolutions.io/eval-sets/j-rig-bench/)          | Mark the interpretation corrected; remove the current positive comparative conclusion. Keep the historical verdict and signature clearly distinguished.                              |
| RESULTS and DR-036                                                                    | Preserve exact bytes; link to them as historical records from this successor.                                                                                                        |
| DR-037, DR-039 and optimizer-safety standard 074                                      | Preserve the records. Their references to this experiment cannot supply current efficacy evidence after approval. General requirements for baselines and evidence remain applicable. |
| `000-docs/FUTURE.md` and document index                                               | Add the successor cross-reference when adopted; do not silently rewrite an earlier decision.                                                                                         |
| Blog or other derivative publication                                                  | Search and verify any additional published version before applying a correction there. No blog publication is established by the historical recommendation alone.                    |

The walkthrough and scorecard were inspected on 2026-10-19. The scope above
identifies confirmed repository and web surfaces; it does not assert an
estate-wide search was completed. Signed bytes will not be replaced or re-signed
as part of the page correction. A separate retraction would need its own
explicit disposition and the existing retraction protocol.

## Replay and verification

Export the validator directly from the recorded Git commit, then use an unused
output filename. The script checks the executable SHA-256 before executing it.
The retained archive root contains `corpus/` and `results/`; it is not a fresh
public clone's incomplete raw-results directory.

```bash
git -C /path/to/claude-code-plugins show 7b9eb8f0a77d285dee3ffe99c913d039c4878aec:scripts/validate-skills-schema.py > /tmp/phase-a0-validator.py
python scripts/audit-phase-a0-history.py --research-root /path/to/retained/phase-a-0-baseline --validator /tmp/phase-a0-validator.py --out /tmp/phase-a0-input-audit-new.json
cmp /tmp/phase-a0-input-audit-new.json research/phase-a-0-baseline/reviews/2026-10-19/input-audit.json
```

The recorded replay ran with network access disabled, a cleared environment
and the raw archive mounted read-only. Its report contains counts, scores,
identifiers and hashes, without publishing original skill text or error messages.
It reproduces input-baseline scoring only; it does not rerun the models, compute
corrected treatment effects, complete the Goodhart audit or approve this decision.

## Approval record

**Pending.** Requested approver: the acting head. Adoption requires an explicit
response approving the proposed decision and the concrete public correction.
The prior autonomous-CTO delegation recorded for the May decision is historical;
this draft does not claim that delegation for a new ratification. Public
comparative-claim publication is gated by DR-039 section 2.6 and DR-035's
pre-publication binding. Record the approval and linked publication revisions
here before changing the status to RATIFIED.
