# SAK community-notice evidence gate

Status: implementation contract; activation evidence remains outstanding.
Tracking: `bd_000-projects-3kye.9`; [SAK coordination issue](https://github.com/jeremylongshore/intent-eval-core/issues/13).
Authority: [DR-049 D-SAK-6](049-AT-DECR-isedc-class-1-charter-ratification-2026-06-10.md#d-sak-6--phase-4-advisoryblocking-flip-995-corpus--30d-advisory--ratified-with-constraints).

## Behavior

The lab's `scripts/sak-state-machine.py` refuses the `READY-TO-FLIP` to `BLOCKING` transition without a complete notice manifest and an explicit evaluation timestamp.
The calendar-ceiling option cannot waive this gate.
Historical state files remain schema-valid without notice evidence; that compatibility does not permit a new blocking transition.
`SAK-STATE.json` remains unchanged and advisory.

The public window starts at the latest publication or issue-pinning timestamp across all four required surfaces: the kernel changelog, marketplace changelog, pinned issue, and fix-it guide.
At least fourteen full 24-hour days must elapse, and the announced `not_before` must be at least that late.
Later announced dates also bind the evaluator.
All evidence timestamps require a timezone; the explicit transition timestamp additionally accepts a date interpreted as midnight UTC.
No clock is read implicitly.

## Evidence contract

The canonical shape is `$defs.communityNotice` in [sak-state.schema.json](../specs/state-machines/schema/sak-state.schema.json).
The [synthetic fixture](../scripts/tests/fixtures/sak-community-notice-valid.json) demonstrates the full structure using example.org URLs; it is never activation evidence.

| Field                               | Meaning                                                                                                          |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `blocking_change_sha256`            | Current proposed blocking-change digest in preconditions                                                         |
| `shadow_deviation_report_sha256`    | Current reviewed shadow-report digest in preconditions                                                           |
| `community_notice.change_sha256`    | Must match the proposed change                                                                                   |
| `community_notice.deviation_report` | HTTPS report URL and matching SHA-256                                                                            |
| `community_notice.artifacts`        | Four mandatory publication objects, each with URL, SHA-256 and `published_at`; pinned issue also has `pinned_at` |
| `community_notice.not_before`       | Announced earliest activation timestamp                                                                          |
| `community_notice.affected_authors` | Unique stable author identifiers from the reviewed report                                                        |
| `community_notice.notifications`    | Exactly one author ID, HTTPS delivery receipt URL and `sent_at` per affected author                              |
| `community_notice.vp_devrel_review` | Manifest digest, HTTPS decision-record URL and `signed_at`                                                       |

Evidence URLs require HTTPS, a hostname and no embedded credentials.
Direct notices must follow the last public publication/pinning and precede the VP DevRel review.
The review must follow publication and cannot be in the future relative to evaluation.
An empty affected-author inventory is valid only as a reviewed assertion; the evaluator cannot establish its truth.

`notice_manifest_sha256()` removes only `vp_devrel_review`, serializes the remaining object with Python JSON sorted keys, compact separators, ASCII escaping and non-finite numbers forbidden, then hashes its UTF-8 bytes with SHA-256.
Arrays retain their order.
Any manifest change requires a new review digest.
This digest binds data; it is not a digital signature or proof of the reviewer's identity.
Successful `emit()` records `community_notice_manifest_sha256` in the new transition-history entry and leaves its input unchanged.
Callers remain responsible for durable storage of the manifest, receipts and resulting state.

## Trust and activation boundary

The evaluator is offline: it validates structure, consistency, ordering and elapsed time, but does not retrieve URLs, authenticate reviewers, check current pin status, compare remote artifact bytes, or establish delivery.
An authorized operator must verify artifact hashes, continued availability, report completeness, actual recipient delivery and reviewer authority before supplying evidence.
Replacing an artifact or expanding the affected-author inventory requires reviewed replacement evidence; a stored digest alone does not detect changes at a remote URL.

This implementation does not certify every ratified flip prerequisite.
The remaining advisory-soak, deterministic-agreement, reviewed coverage-disposition and tested append-only rollback enforcement is tracked in `bd_000-projects-3kye.16`.
Governance booleans remain the existing hand-maintained stub.
Do not use an allowed library result as authorization to activate blocking.

The full `3kye.9` acceptance also requires author-facing diagnostics linking the failed marketplace field, its 6767-h section and the [contributor exception note](../CONTRIBUTING.md#marketplace-acceptance-and-exception-requests), plus actual cross-repository publication, direct delivery, co-sign and elapsed-window evidence.
Those requirements remain outstanding; this document and synthetic tests do not constitute a migration announcement or start its clock.

## Verification

Run from the lab with pytest and jsonschema installed:

```bash
python3 -m pytest scripts/tests/ -q
python3 scripts/sak-state-machine.py --self-test
python3 scripts/sak-state-machine.py --validate --state SAK-STATE.json
```

Regression cases cover missing surfaces, mismatched change/report bindings, stale review digests, missing or duplicate recipients, malformed URLs and timestamps, late publication/pinning, future review/delivery, and the exact fourteen-day boundary with and without calendar-ceiling disposition.
