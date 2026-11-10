# SAK blocking-flip prerequisite evidence

Status: implementation contract; no blocking activation or governance approval is recorded here.
Tracking: `bd_000-projects-3kye.16`; [SAK coordination](https://github.com/jeremylongshore/intent-eval-core/issues/13).
Authority: DR-049 D-SAK-6, retained by DR-081 Q4, together with plan 048 Delta 3.
The [notice contract](121-AT-SPEC-sak-community-notice-gate-2026-11-10.md) remains a separate hard gate.

## Required evidence

The evaluator now validates the complete preconditions object before comparisons, rejecting malformed types, unknown properties and non-finite numbers.
Legacy state files without new evidence remain structurally valid, but cannot emit a new blocking transition.
Legacy governance flags must be exactly boolean true; truthy strings or integers are not approval.

`flip_evidence` is defined in [sak-state.schema.json](../specs/state-machines/schema/sak-state.schema.json).
It must bind the current blocking-change digest, current shadow-deviation report digest and complete notice-manifest digest.
Its measurement time and reviewer-selected validity deadline must contain the explicit evaluation time.
The evaluator does not choose a freshness period or silently extend one.

| Requirement               | Checked evidence                                                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| At least 30 days advisory | Continuous observation assertion with timezone-bearing start/end timestamps spanning at least 30 full days; observation ends no later than measurement |
| Deterministic agreement   | Positive total fold count; agreed count equals total exactly                                                                                           |
| Published measurements    | HTTPS URL, SHA-256 and publication time for agreement, shadow log, false-reject report and P0 report                                                   |
| Zero open P0              | Explicit typed count of zero, bound into all three approvals                                                                                           |
| Shadow observation        | Known integer duration of at least seven days; known deviation below 0.5 percent                                                                       |
| Day-zero security checks  | Explicit assertion that security checks already block independently of shadow                                                                          |
| Rollback                  | Implemented and tested assertions, append-only-supersession strategy, test time and published receipt; test precedes measurement                       |
| Governance triple         | Separate CTO, CISO and VP DevRel approval records, each with the full input-manifest digest, signing time and published decision record                |
| Community notice          | Existing four-surface publication, recipient coverage, review and elapsed fourteen-day checks                                                          |

Measurement artifacts must be published after measurement.
Approvals must follow publication of all evidence and must themselves be published before evaluation.
Every receipt URL requires HTTPS, a hostname and no embedded credentials.
This implementation makes missing evidence a refusal; it does not turn an assertion into authenticated proof.

## Coverage-only calendar disposition

Passing `allow_calendar_ceiling=True` requests evaluation of a reviewed exception; it cannot authorize an exception by itself.
The disposition must explicitly say `flip-with-quarantine`, refer to published decision and quarantine records, and be reviewed at or after day 30.
`extend` or `park` is not a flip decision.
The quarantined file list must be nonempty, unique and explicitly advisory-only.

The evaluator checks the disposition's corpus size and passed-file count against the measured coverage percentage.
Passed files and quarantined files must fit within that corpus.
Evidence counts are bounded to the interoperable JSON safe-integer range to prevent arithmetic overflow.
Quarantined files must be less than 0.5 percent of the original corpus, and the retained corpus must still meet the 99.5 percent pass floor.
These are conservative arithmetic checks on operator-reviewed counts; the evaluator cannot inspect the report's actual file inventory.
For example, 9,940 passing files in a 10,000-file corpus and 20 quarantined nonpassing files give 99.4 percent original coverage and about 99.599 percent retained coverage.
The distinct deterministic-fold requirement remains exactly 100 percent in this case.
Unknown coverage, inconsistent counts, an excessive quarantine, or a missing review is refused.

No other prerequisite is dispositionable through the calendar flag.
A refusal requires human re-evaluation under the charter's escalation process; this offline library does not convene a council, send a message or schedule an automatic flip.
The caller must route that refusal to the authorized operators.

## Approval binding and transition record

`flip_manifest_sha256()` hashes the entire preconditions object after removing only `flip_evidence.approvals`.
It uses sorted-key compact ASCII JSON with non-finite numbers forbidden, encoded as UTF-8 and hashed with SHA-256.
Array order is retained.
Changing any measured count, notice evidence, proposed change or validity deadline invalidates all three review digests.
The three approval objects are excluded to avoid a self-referential digest; their identity and authority must be established from the decision records by the operator.

Successful `emit()` appends `flip_evidence_manifest_sha256` alongside the notice-manifest digest and does not mutate the input state.
It still performs no persistence, network calls, Rekor writes or workflow activation.
The caller must retain the full evidence and decisions durably; a digest alone cannot reconstruct them.

## Trust boundary and verification

The input source remains operator-maintained.
Before evaluating a live proposal, authorized reviewers must verify the actual corpus and report hashes, continuous observation, current P0 status, security-gate behavior, reviewer identities, and the rollback rehearsal's append-only behavior.
The local checks neither fetch nor authenticate external receipts and cannot establish that a reported rehearsal actually happened.
A changed live report must be supplied with updated evidence and fresh approvals; unchanged local inputs cannot detect a remote report changing underneath them.

`SAK-STATE.json` remains unchanged and advisory.
The [synthetic fixture](../scripts/tests/fixtures/sak-flip-evidence.json) is test data, never an approval or activation receipt.
The tests exercise absent evidence, malformed types, stale bindings, expiry, future dates, the exact 30-day boundary, partial deterministic agreement, rollback failures, missing governance, and unsafe coverage dispositions.

```bash
python3 -m pytest scripts/tests/ -q
python3 scripts/sak-state-machine.py --self-test
python3 scripts/sak-state-machine.py --validate --state SAK-STATE.json
```
