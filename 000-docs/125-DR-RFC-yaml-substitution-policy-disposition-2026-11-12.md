# YAML substitution policy disposition — decision packet

Status: **DRAFT — decision requested, not ratified or implemented.**
Tracking: `bd_000-projects-9pey`; measurement `bd_000-projects-h9r9`;
[kernel coordination issue 13](https://github.com/jeremylongshore/intent-eval-core/issues/13).
This packet does not close either bead, authorize a release, or activate enforcement.

## Decision required

Choose whether a newly versioned kernel security profile should adopt the
marketplace substitution policy, or whether the two policies should remain
intentionally distinct with a formally amended measurement contract. Record
which artifact locations and tokens each profile governs, the compatibility
vehicle, the authority accepting any relaxation, and the follow-through owner.
Neither option is selected here. The existing failed target remains visible
until an authorized disposition and its required follow-through are complete.

## Evidence and provenance

The evidence is the existing October 19 experiment, read from core commit
`488cf6aa999700e1c71ff3b07be42959fe4b6650`; no validators or tests were rerun
for this packet. The lab base is `f5a6d1a737a0d35f05c849b0b444791edcbc5555`.
These are source snapshots, not an assertion that a later release has adopted
new policy. The [measurement report][report] and [kernel baseline][kernel]
state their limitations explicitly.

| Evidence                                           | SHA-256                                                            |
| -------------------------------------------------- | ------------------------------------------------------------------ |
| [100-fixture manifest][manifest] / corpus identity | `feac22e7d61ba4064f00855c9b7dfb640b0850572cfd80eacba9a9b76f335dc4` |
| Kernel baseline JSON                               | `50aaf275befc2a05f93d963bcc8cbc1a00554ba241c3b29b27350d2a169b15c8` |
| [Marketplace baseline JSON][marketplace]           | `00e84cedfd1a8e712008a8643343f077f57a6a7724de43af8a0b174f0840803d` |

The marketplace baseline identifies actual checker revision
`6d2613e0d17c8602328c9f96234c4a0e52a2dc77`, path
`scripts/validate-skills-schema.py`, hash
`2b0cb1d864108d593b6207c04fbc60ee856f8c54cb2e916542b5db837ab2e4d4`.
Kernel baseline records bind each v1/v2 schema and validator hash separately.
The measurement invokes actual JSON Schema/Ajv and Zod folds; the marketplace
runner imports the actual committed Python checker. It does not reimplement it.

The corpus has 50 legitimate and 50 forbidden examples according to the
**marketplace label policy**, distributed equally across five locations.
Fixtures use JSON flow frontmatter, a YAML subset. Paired clean controls pass,
and JSON Schema/Zod classifications agree on all cases. This is neither a
population error-rate estimate nor proof of execution safety, general YAML
parser equivalence, full authoring conformance, or Python kernel parity.

## What disagrees

Each location below contains ten legitimate and ten forbidden cases. Values
are false positives / false negatives relative to the frozen marketplace labels.

| Location                    | Kernel v1 | Kernel v2 | Marketplace checker |
| --------------------------- | --------- | --------- | ------------------- |
| `description`               | 10 / 3    | 10 / 0    | 0 / 0               |
| `compatibility`             | 0 / 10    | 0 / 10    | 0 / 0               |
| Metadata string             | 0 / 10    | 0 / 10    | 0 / 0               |
| Metadata list string        | 0 / 10    | 0 / 10    | 0 / 0               |
| Nested metadata string      | 0 / 10    | 0 / 10    | 0 / 0               |
| Total, denominators 50 / 50 | 10 / 43   | 10 / 40   | 0 / 0               |

Thus v1 has FP 20%, FN 86%; v2 has FP 20%, FN 80%; neither meets
FP < 2%, FN < 5%. One FP already equals 2% and fails the strict bound.
The marketplace checker meets both bounds on this corpus only.

The [v1 fold][v1] rejects `${` in description. The [v2 fold][v2] additionally
rejects `$(` and backticks there. The three v1 description misses are command
substitution, backtick command, and nested substitution. Both folds omit the
other four measured locations. Both reject all ten legitimate description
examples, which contain allowed braced templates.

The marketplace checker recursively visits parsed string values and removes
seven named braced tokens before checking residual forbidden syntax:
`${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${SKILL_DIR}`, `${PLUGIN_ROOT}`,
`${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_SESSION_ID}`, and `${CLAUDE_EFFORT}`.
The manifest also records `$ARGUMENTS` and `$1` for mixed examples. This is an
observed checker policy; the experiment does not establish that every token is
an upstream guarantee in every field or execution context.

## Binding authority and the unresolved interpretation

- [Plan 033 §14.25][plan] requires the 100-fixture, 50/50 measurement and the
  strict FP/FN targets, with quarterly follow-through. Its reference to the
  validator's `securityChecks` leaves the measured profile/allow-list authority
  in need of explicit resolution; the result cannot be made passing by relabeling.
- Plan 033 §14.27 and [DR-049 D-SAK-1][charter] freeze published authoring/v1
  and require a new version for breaking changes. A package version bump alone
  is not permission to change a frozen contract path.
- DR-049 D-SAK-2 makes `securityChecks` non-optional in the canonical marketplace
  composition. D-SAK-3 requires a Class-1 ADR with explicit CISO co-sign for
  removal or weakening of a security conjunct. Accepting a template currently
  rejected by the description fold is a relaxation even if recursive checking
  tightens other locations. The two effects must not be netted away.
- DR-049 D-SAK-6 keeps deterministic fold agreement at 100%, security checks
  outside the quality-shadow grace period, and the blocking flip behind its
  independent notice, evidence, rollback and governance gates.
- [DR-081 Q2/Q4][ratification] separates charter ratification from funding and
  promotion. Docs [121][notice] and [122][flip] describe executable checks;
  they do not supply real notices, approvals or activation authority.

The present experiment demonstrates disagreement between profiles, not a
breach of the kernel's declared description-only behavior. Conversely, calling
profiles different does not by itself satisfy the original measurement target.

## Option A — versioned alignment

Propose a new, explicitly named authoring security contract with recursively
checked string values and a governed allow-list. Specify token boundaries,
malformed/nested expressions, lists/maps, non-string values and description
handling before implementation. Preserve existing v1/v2 bytes and behavior;
select the new contract's version and lifecycle through the decision process.

This option seeks common behavior for marketplace consumers, but combines
relaxation in description with tightening elsewhere. It therefore needs the
Class-1/CISO disposition above, compatibility analysis and a separately
approved implementation. Do not implement it as a Zod-only refinement: JSON
Schema recursion/reference semantics and the executable validator must describe
the same accepted values. If a portable JSON Schema cannot express the agreed
policy, resolve that architectural issue before calling the contract canonical.

After approval, use the frozen corpus as a retained comparison, add separately
versioned cases for any newly specified semantics, preserve old baselines, and
prove positive/negative parity. Full consumer inventory and corpus impact must
precede pin changes; the 100 cases do not establish migration volume. Introduce
explicit version selection and diagnostics before any enforcement transition.

## Option B — deliberately distinct profiles

Retain description-only kernel folds and the recursive marketplace checker,
but ratify a precise measurement amendment explaining why both are needed,
which consumers require each, and which authority owns the marketplace policy.
Keep the existing comparison and failed target visible. Any new conformance
measurement must have distinct labels, profile identity, denominator and
acceptance criteria; it cannot silently replace this historical experiment.

This avoids a compatibility change to current validators, but risks continuing
policy drift and a second de facto schema authority. The decision must explain
how marketplace-specific checks compose with the kernel without advertising
kernel-only validation as equivalent. Additional new labels require independent
review rather than deriving expected answers from implementation behavior.
A statement that the original requirement was out of scope must be a recorded
amendment, not an implementation team's unilateral closure rationale.

## Representation, migration and rollback obligations

| Surface     | Required treatment after a decision                                                                                                                                                                                                                                                                                        |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TypeScript  | Explicit version/profile API and types; no evaluator or execution runtime added to the kernel.                                                                                                                                                                                                                             |
| JSON Schema | Preserve existing `$id` and published bytes; define the new profile's complete structural/security behavior, including recursive scope if selected.                                                                                                                                                                        |
| Zod         | Match accepted/rejected values and field paths with JSON Schema; retain existing exports and old-version tests.                                                                                                                                                                                                            |
| Python      | Inventory actual exported models/schema consumers first. The current comparison tests the marketplace Python checker, not a Python kernel authoring validator; no authoring model was found in the pinned generated Python inventory. Add or document the approved validation surface and prove parity before claiming it. |
| Consumers   | Inventory pinned validator/creator/J-Rig/marketplace versions and required security checks; preserve existing defenses until their replacements are proven and approved.                                                                                                                                                   |

For Option A, rollback uses reviewed consumer pin/config reversal while retaining
new and old immutable artifacts and measurements. It must not silently remove
existing marketplace security checks. Any affected signed records follow
append-only supersession, never log mutation. For Option B, rollback of a
measurement amendment restores the previous named measurement contract while
retaining both reports; it cannot erase the failed baseline. Neither option
waives corpus migration, notice delivery or blocking-flip prerequisites.

## Proposed decision record and next boundary

The authorized decision should record: selected option and rationale; exact
locations/token policy; version/profile identity; compatibility assessment;
required Class-1/CISO disposition for any relaxation; consumer migration and
rollback owner; implementation funding where applicable; and the evidence
needed to accept `h9r9` and close `9pey`. Until then both remain unresolved.
The next quarterly reminder is January 17, 2027 (`9k5h.21`); relevant policy or
validator changes can require earlier measurement. Time passing is not approval.

This packet changes documentation only. Existing source, schemas, fixtures,
labels, thresholds, enforcement and published distributions remain untouched.

[report]: https://github.com/jeremylongshore/intent-eval-core/blob/488cf6aa999700e1c71ff3b07be42959fe4b6650/000-docs/015-AA-EVAL-yaml-shell-substitution-baseline-2026-10-19.md
[manifest]: https://github.com/jeremylongshore/intent-eval-core/blob/488cf6aa999700e1c71ff3b07be42959fe4b6650/tests/security-measurement/shell-substitution-v1/manifest.json
[kernel]: https://github.com/jeremylongshore/intent-eval-core/blob/488cf6aa999700e1c71ff3b07be42959fe4b6650/tests/security-measurement/shell-substitution-v1/kernel-baseline.json
[marketplace]: https://github.com/jeremylongshore/intent-eval-core/blob/488cf6aa999700e1c71ff3b07be42959fe4b6650/tests/security-measurement/shell-substitution-v1/marketplace-baseline.json
[v1]: https://github.com/jeremylongshore/intent-eval-core/blob/488cf6aa999700e1c71ff3b07be42959fe4b6650/src/validators/v1/authoring/marketplace-tier.ts#L103-L127
[v2]: https://github.com/jeremylongshore/intent-eval-core/blob/488cf6aa999700e1c71ff3b07be42959fe4b6650/src/validators/v1/authoring/v2/marketplace-tier.ts#L110-L147
[plan]: 033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md
[charter]: 049-AT-DECR-isedc-class-1-charter-ratification-2026-06-10.md
[ratification]: 081-AT-DECR-isedc-sak-class-1-charter-ratification-2026-06-17.md
[notice]: 121-AT-SPEC-sak-community-notice-gate-2026-11-10.md
[flip]: 122-AT-SPEC-sak-flip-prerequisite-evidence-2026-11-10.md
