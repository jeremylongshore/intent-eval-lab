# Trace Intelligence Incident and Corruption-Response Runbook

Bead: `bd_000-projects-h08j.8.151` (K10). Reviewed against source on **2026-10-12**.

Use this procedure when trace, annotation, lineage or evidence integrity is in
question. It supplements the existing incident process. It does not establish a
new storage architecture or authorize production adoption; the program's audit,
architecture and owner-approval gates remain in force.

## Authority and operating references

Operators must have the access-controlled `intent-os` checkout and follow:

- `ops/incidents/runbook.md`: lifecycle, response targets and command usage.
- `ops/incidents/authority.md`: incident commander (IC), operator and executive
  approver responsibilities, including owner-unavailable handling.
- `ops/incidents/README.md`: universal containment and the authorized revoke-first
  response to credential compromise.
- `schemas/incident/incident-record.v0.schema.json`: incident record contract.
- The affected asset's registered service and backup/restore runbooks. Resolve the
  exact service, environment, owner and recovery point before any mutation.

The IC coordinates investigation and records decisions. Production containment,
credential actions, destructive recovery, lifting a freeze and post-close reopening
require the scoped human authority specified by the estate runbook. A CLI `--role`
value records a role; it does not grant approval. If approval is unavailable,
continue evidence preservation and permitted investigation, record the parked
operation, and keep the affected decision path closed.

IEP's [runtime blueprint](./012-AT-ARCH-platform-runtime-blueprint.md) defines
hash-verified lineage and replay. The dashboard's
[ingest worker](https://github.com/jeremylongshore/intent-eval-dashboard/blob/d4dfcc58838b0a78941ab44d1f755de3fcf98fe4/src/ingest/worker.ts)
and [payload binding](https://github.com/jeremylongshore/intent-eval-dashboard/blob/d4dfcc58838b0a78941ab44d1f755de3fcf98fe4/src/ingest/gate-result-binding.ts)
provide concrete verification boundaries. Consult the deployed revision's service
runbook when executing recovery; these source references do not prove deployment.

## Severity classification and response

Choose the highest applicable level. An unknown integrity boundary is at least
SEV2 until scoped; confirmed unsafe promotion, data-loss risk or an affected
customer-facing service warrants SEV1. Record uncertainty and reclassify after
triage. These are internal response targets from the estate playbook.

| Level                    | Trace/evidence examples                                                                                                                                 | Response playbook                                                                                                                                                                                                                                  | Timing and review                                                                                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SEV1 — critical**      | Corrupt evidence influenced a release; unauthorized canonical annotation; active disclosure or data-loss risk; customer-facing outage.                  | Assign IC, escalate to the executive approver, preserve originals, and obtain authority to contain the affected producer/consumer. Identify every downstream decision that used the suspect material. Use the relevant corruption procedure below. | Acknowledge within 5 minutes; update every 15 minutes; escalate if unacknowledged at 5 minutes. Reference restoration target: 60 minutes for one stack. Postmortem required. |
| **SEV2 — major**         | Rejected signature/hash or broken lineage blocks evaluation; evidence unavailable but a verified recovery source exists; no confirmed unsafe promotion. | Assign IC, isolate the suspect candidate, bound the affected runs and repositories, preserve verified prior state, and restore through the normal verifier. Escalate to SEV1 if impact or trust loss expands.                                      | Acknowledge within 15 minutes; update every 30 minutes; escalate at the acknowledgment breach. Reference restoration target: 4 hours. Postmortem required.                   |
| **SEV3 — limited**       | Isolated fetch failure or delayed projection with independently verified prior evidence and a usable workaround.                                        | Assign a service owner, confirm the workaround remains valid, investigate freshness/storage failures, and repair the bounded defect. Promote severity if integrity cannot be established.                                                          | Acknowledge within 60 minutes; update daily; escalate on the acknowledgment breach. Target next-business-day restoration. IC decides whether a full postmortem is needed.    |
| **SEV4 — informational** | Rejected malformed test input, near miss or documentation discrepancy with no production impact and no unresolved integrity risk.                       | Record a Bead with evidence, owner and review date; perform normal corrective work. Reclassify immediately if production impact or uncertainty appears.                                                                                            | Review at the next engineering triage; record the chosen due date. Retain a short cause/action/verification note.                                                            |

The existing incident command and schema accept **SEV1–SEV3 only**. SEV4 is this
runbook's informational classification, recorded in Beads; never pass `SEV4` to
`incident.sh` or add an undeclared field to its record. If escalation is warranted,
declare a supported incident severity and cross-reference the original Bead.
Missing a restoration target requires escalation, never a weaker verification gate.

## First response and incident lifecycle

1. **Confirm and scope.** Capture the signal time, affected service/environment,
   producer revision, run IDs and structured verifier reason. Check a second
   source where available. Distinguish an unreachable manifest from a failed
   signature or payload binding; a green workflow is not an integrity verdict.
2. **Track and acknowledge.** For SEV1–SEV3, use the estate command's declare,
   validate-triage and ack steps with the assigned role. Link the incident ID and
   canonical Bead in both directions. Preserve truthful notification outcomes
   such as `spooled`, `rate-limited` or `dry-run`; do not claim delivery from an
   attempted dispatch. SEV4 follows the Bead route above.
3. **Preserve evidence before repair.** Copy original bytes, manifests, signatures,
   verification receipts and relevant logs to the approved restricted evidence
   location. Record capture time, access classification and SHA-256 hashes.
   Preserve raw and canonical forms and the declared retention/hold requirements.
   Keep credentials, raw customer traces and private incident details out of
   public issues, notifications and this repository's public documents.
4. **Contain within authority.** Hold promotion and consumption of suspect
   artifacts using the affected service's authorized control. Do not disable
   verification, change trust pins, bypass review or rewrite history to regain
   a green status. Preserve unaffected service operation where possible.
5. **Recover and verify.** Follow the applicable scenario below in isolated
   recovery storage first. An independent verification pass must succeed before
   approved promotion. Record missing prerequisites explicitly; a partial restore
   is not resolution.
6. **Monitor and close.** Use the existing lifecycle:
   `Detected → Validated → Acknowledged → Investigating → Mitigated → Resolved → Postmortem → Closed`.
   Record a service-appropriate monitoring interval and its observations. Close
   only after the recovery exit criteria and required postmortem are satisfied.
   Recurrence follows the canonical reopen procedure; post-close reopening needs
   owner authority. False positives use the documented cancellation transition.

From the `intent-os` checkout, these commands inspect existing state:

```bash
bash ops/incidents/incident.sh list --active
bash ops/incidents/incident.sh status "$INCIDENT_ID"
```

## Corruption scenarios and recovery

### Chain tamper or signed-payload mismatch

Examples include changed trace bytes, a broken predecessor digest, invalid DSSE
signature, failed Rekor inclusion, mismatched signer/workflow identity, or a
`predicate_binding_invalid` rejection.

1. Preserve both received bytes and the claimed digests/signature. Determine the
   earliest known-good boundary and all descendants or release decisions that
   consumed the suspect artifact. Treat authenticity as unresolved until checked.
2. Re-run the producer's versioned canonicalization and verifier in isolation.
   Record a separate raw-file hash for custody: hashing a pretty-printed JSON file
   is not interchangeable with the contract's canonical payload digest. Check
   signer identity, inclusion proof, schema, subjects, predicates and payload
   binding as applicable; a valid signature alone does not establish correct
   evaluation or lineage.
   If the signing identity may be compromised, invoke the owner-governed
   revoke-first response before restoring trust. Preserve the incident evidence;
   do not use the suspect identity to issue replacement attestations.
3. Recover original, hash-matching bytes from an independently verified source.
   If an authorized rerun is necessary, create a new run and new signed evidence
   with links to the incident and superseded result. Do not re-sign corrupt bytes,
   recalculate a predecessor hash to conceal a break, or relabel an old result.
4. If suspect evidence was published, use the authorized retraction/supersession
   procedure and verify its public effect. Preserve the original attestation and
   audit trail; a local denylist edit alone is not deployed retraction.

### Lineage break or unauthorized annotation ancestry

Examples include a missing parent trace, dataset/taxonomy version mismatch, an
orphaned regression case, or an accepted annotation without its human acceptance
record.

1. Preserve the affected trace, annotation history, dataset/version manifests and
   referenced digests. Stop affected downstream promotion; do not attach a
   convenient available parent or infer missing human approval.
2. Walk the declared ancestry using the pinned schema and versions. Identify
   every missing or inconsistent edge and affected descendant. Distinguish an
   unavailable referenced object from a present object with the wrong digest.
3. Restore the exact verified parent/version and acceptance records where they
   exist. Rebuild derived datasets/regressions from declared inputs in isolation
   and compare their identities and results. New human judgments require new
   recorded decisions; they cannot be backdated into the original history.
4. Re-evaluate affected descendants through their normal gates. If the ancestry
   or approval cannot be proven, retain an explicit unresolved gap and keep those
   results ineligible. Recovery never silently promotes AI proposals to canonical
   annotations.

### Evidence loss or unavailable storage

Examples include missing content-addressed objects, absent signed sidecars, an
unavailable manifest, or loss of the persisted ingest store.

1. Determine whether the loss is a fetch/cache failure, missing authoritative
   bytes or a broader data-loss incident. Inventory missing objects and select a
   verified recovery point through the service's backup runbook. Do not clear
   caches or overwrite the remaining store during diagnosis.
2. Restore into a separate approved location; verify backup manifests, object
   hashes, signatures and references before replacement. A transparency-log entry
   proves a logged claim, not recovery of the lost payload or original trace.
3. Re-ingest restored artifacts through the normal identity, signature, schema
   and payload-binding checks. Preserve the prior verified snapshot and its stale
   indication on a failed pass. Reverify that prior snapshot if its own storage or
   trust boundary is implicated; do not keep serving a suspect “known-good” copy.
4. Verify required objects, gate rows, snapshot references and rendered status
   together. If original evidence is irretrievable, record the loss and affected
   decisions; an authorized rerun produces a new identity and receipt. Do not
   invent an old result, reset freshness timestamps or claim a successful restore.

## Recovery exit criteria

The IC records evidence for each applicable item: bounded blast radius; approved
recovery action; verified restored bytes and ancestry; preserved human approval
history; normal consumer verification and correct projection; observed monitoring
interval; honest notification receipt; and residual risks with owners and expiry
or next-review dates. Corrupt, missing or unapproved inputs must still be rejected.
Validate recovery from a second observation point, not just the repair command's
exit code. An unavailable approval or unverifiable artifact leaves the affected
path contained and the incident unresolved.

## Postmortem template

SEV1/SEV2 require this record; for SEV3 the IC records the review decision. Keep the
full record in the governed incident evidence location and publish only a reviewed,
content-safe summary.

```text
Incident ID / Bead / severity / service / environment:
IC / operator / executive approver where required:
Detection, acknowledgment, containment, recovery and closure times (UTC):
Impact window and affected traces, annotations, datasets, evidence and decisions:
Timeline: time | observed fact | action | actor/authority | evidence reference
Root cause and contributing conditions; distinguish facts from hypotheses:
Why existing detection, verification or recovery controls did/did not work:
Recovery point, commands/revisions used, before/after hashes and verification:
Notification outcomes and any missed response targets:
Irrecoverable loss, retained uncertainty and time-bounded risk acceptance:
Corrective actions: Bead | owner | dependency | acceptance evidence | review date
Reviewer decision, follow-up verification and closure/reopen rationale:
```

## Audit-log requirements

Keep Beads authoritative for work and use the existing schema for incident state.
Append transitions and corrections; preserve earlier entries and original
artifacts. Do not add unrecognized keys to the strict incident schema. Store
additional evidence detail in the governed receipt referenced by the record.

- **Identity and time:** incident ID (or SEV4 Bead), correlation/run IDs, service,
  environment, severity and rationale; event and observation times in UTC; actor,
  authorizing role and scoped approval reference/expiry for controlled actions.
- **Action and result:** prior/new state, trigger, exact bounded target,
  command/tool and version, source revision, outcome (`ok`, `denied` or `failed`),
  exit/result code and reason. Record denied or failed attempts in the authorized
  action receipt even when the incident state machine does not advance.
- **Custody and verification:** access-controlled evidence reference, raw and
  canonical digests with algorithm/version, capture/recovery provenance, affected
  ancestry, verifier results and before/after comparison. Record gaps explicitly.
- **Communications and follow-through:** actual notification receipt/fingerprint,
  containment/recovery approval, monitoring observations, linked corrective Beads,
  postmortem decision and closure authority. Cross-reference incident, Beads and
  their existing GitHub/Plane projections without copying private payloads.

For SEV4, record these applicable facts in the Bead and its evidence reference;
there is no fabricated SEV4 incident-engine record. Apply the estate disclosure and
retention controls to logs and backups as well as primary records.

## Practice and validation

Before operational use, resolve service-specific owners, approved controls,
backup locations and verifier commands. Run a tabletop for each corruption
scenario above, including an irrecoverable object and an unavailable approver;
record the expected refusal and escalation, not an assumed successful recovery.

For the existing **synthetic** incident lifecycle drill, use an unused loopback
port and fresh state directories. From the `intent-os` checkout, with Python 3,
`jsonschema`, Bash and curl available:

```bash
: "${TRACE_DRILL_PORT:?Set an unused loopback port for this exercise}"
drill_root=$(mktemp -d)
INCIDENT_DRY_RUN=0 INCIDENT_NO_DISPATCH=1 \
  INCIDENT_STATE_DIR="$drill_root/incidents" \
  SYNTH_STATE_DIR="$drill_root/service" SYNTH_PORT="$TRACE_DRILL_PORT" \
  bash ops/incidents/tests/synthetic-drill.sh "$drill_root/evidence"
```

Retain the resulting transcript and schema-valid exercise record. Confirm the
synthetic target is removed and notification receipts say `dry-run`.
`INCIDENT_NO_DISPATCH=1` suppresses notifications while exercising the real
synthetic adapter; `INCIDENT_DRY_RUN=1` would skip that adapter too and cannot
prove containment. This drill does not validate a production restore or the
trace program's seven-day adoption gate.

The dashboard's
[payload-binding tests](https://github.com/jeremylongshore/intent-eval-dashboard/blob/d4dfcc58838b0a78941ab44d1f755de3fcf98fe4/src/ingest/gate-result-binding.test.ts),
[failed-pass tests](https://github.com/jeremylongshore/intent-eval-dashboard/blob/d4dfcc58838b0a78941ab44d1f755de3fcf98fe4/src/ingest/live-pass.test.ts)
and [prior-snapshot persistence test](https://github.com/jeremylongshore/intent-eval-dashboard/blob/d4dfcc58838b0a78941ab44d1f755de3fcf98fe4/src/ingest/partial-fetch-lkg.test.ts)
exercise bounded rejection and recovery behavior. Their stubbed verifier cases
are not proof of live cryptographic verification or deployed recovery.
