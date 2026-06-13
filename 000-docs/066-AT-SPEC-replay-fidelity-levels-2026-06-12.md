# Replay fidelity levels (RF-0..RF-4) — capture, verification, retention

**Status:** NORMATIVE · **Date:** 2026-06-12 · **Authority:** Blueprint B § 3.2 (replay
semantics — locks the semantics, defers the level enumeration to this doc) + § 4.3 (the
`replay.*` OTel event category) · **Epic:** iel-E11 (replay fidelity levels) ·
**Beads:** 3vf9, 84l2, doij, cp8k, czgl

This spec enumerates the replay-fidelity levels that Blueprint B § 3.2 deferred. Blueprint B
locks the SEMANTICS replay must honor (re-executable inputs, `replay.input.drift`,
`replay.verdict`, the "audit-grade deterministic, not approximately reproducible" standard);
this doc locks the LEVELS, the mandatory replayable-record metadata, the verification rules, the
anti-patterns, and the storage/retention obligations. The glossary forward-references the level
enumeration as "RF-N" (`014-DR-GLOS` § 3 **replay**, § 7); this is its normative home.

**Relation block.** Relates to: Blueprint B (`012-AT-ARCH-platform-runtime-blueprint.md`)
§ 3.2 + § 4.3; the lineage log (`054-AT-SPEC-lineage-log-and-derived-coverage-map-2026-06-12.md`);
the fetch taxonomy + three-tier archive (`052-AT-SPEC-fetch-failure-taxonomy-and-three-tier-archive-2026-06-12.md`);
the predicate compatibility policy (`064-AT-DECR-evidence-bundle-predicate-compatibility-policy-2026-06-12.md`);
the Rekor superseding-event protocol (`065-AT-SPEC-rekor-superseding-event-protocol-2026-06-12.md`);
the kernel runtime contracts (iec-E06, `@intentsolutions/core`). The runtime-event-name taxonomy
that pins the per-event `replay.*` names is iel-E12 (forthcoming, `067-AT-ARCH` runtime event
taxonomy); this doc cites the four `replay.*` attributes already pinned in Blueprint B § 4.3 and
defers the full name registry to iel-E12.

## 1. The five levels (RF-0 .. RF-4)

A replay-fidelity level is a per-predicate, per-record declaration of **what re-execution
reproduces** and **what it costs to make that reproduction possible**. Blueprint B § 3.2
expresses fidelity per predicate (`gate-result/v1` = RF-strict; `eval-verdict/v1` = best-effort;
`cost-attribution/v1` = N/A); RF-0..RF-4 are the named, ordered scale those qualitative phrases
resolve to. A higher level is a strict superset of the guarantees below it and a strict superset
of the metadata they require (§ 2).

| Level | Name | GUARANTEE — re-execution reproduces | Does NOT guarantee | Cost |
| --- | --- | --- | --- | --- |
| **RF-0** | record-only | nothing is re-executed; the record is preserved for inspection but cannot be replayed | any reproduction at all | metadata only; no frozen inputs |
| **RF-1** | deterministic-output | the recorded outputs are returned for the recorded inputs **without re-invoking the model** — a faithful playback of what was captured | that re-running the model today would still produce those outputs | recorded input/output pairs + their hashes |
| **RF-2** | model+seed re-execution | re-invoking the **pinned model id+version with the pinned seed** against the pinned, tokenized inputs reproduces the verdict | environment/feature-flag invariance — only model+seed are frozen | RF-1 + model id/version + tokenizer + seed |
| **RF-3** | environment-pinned re-execution | RF-2 **plus** pinned runtime/OS versions and a frozen feature-flag snapshot reproduce the verdict; the full execution context is specifiable | bit-exact transport/floating-point identity across hardware | RF-2 + environment block + feature-flags snapshot |
| **RF-4** | bit-exact / full-provenance | byte-identical re-execution: same bytes in, same bytes out, with a complete signed provenance chain to the original | (this is the ceiling — it guarantees identity, at the cost of pinning everything) | RF-3 + full provenance chain + deterministic transport |

**When a consumer needs each.**

- **RF-0** — telemetry, ephemeral diagnostics, or any record whose value is the *fact that it
  happened*, not its re-runnability (e.g. a `cost-attribution/v1` row, which Blueprint B § 3.2
  flags RF-N/A because cost is not replay-deterministic by nature).
- **RF-1** — dashboards, side-by-side diff views, and incident forensics that need *what was
  observed* without paying to re-invoke a provider. RF-1 answers "what did the system record?"
- **RF-2** — regression analysis and one-variable-change discipline (Blueprint A § 1.2
  principle 6): change exactly the model or the seed and observe the verdict shift, everything
  else held.
- **RF-3** — a SOC2-grade audit that must defend "this verdict is reproducible under the
  recorded conditions," and any `gate-result/v1` row gating a real ship/no-ship decision. RF-3 is
  the floor for production-Rekor-anchored gate decisions.
- **RF-4** — standards-body filings, dispute resolution, and any attestation whose binding force
  rests on byte-identity rather than semantic equivalence. RF-4 is expensive and reserved for the
  one-way-door artifacts where "approximately reproducible" is categorically unacceptable.

Blueprint B § 3.2's mapping resolves as: `gate-result/v1` = **RF-3 minimum** (RF-4 where the
predicate body and transport are fully deterministic); `eval-verdict/v1` = **RF-1** by default,
**RF-2** when `verdict_source=llm_with_seed` with a frozen model snapshot; `cost-attribution/v1`
= **RF-0**. A record MUST NOT claim a level whose required metadata (§ 2) it does not carry.

## 2. Mandatory replayable-record metadata

Every record that declares an RF level MUST carry the metadata its level requires. Field names
align with the kernel RuntimeReceipt contract (Blueprint B § 2.6, iec-E06) and the `replay.*` OTel
attribute names already pinned in Blueprint B § 4.3 — those are the naming AUTHORITY; this table
MUST NOT contradict a pinned name. Where a field overlaps RuntimeReceipt, the receipt is the
canonical carrier and the replay record references it by `eval_run_id`; fields below that do not
already live on the receipt are the replay-specific additions.

| Field | Type | Required at RF level | Brief |
| --- | --- | --- | --- |
| `rf_level` | enum `RF-0..RF-4` | all | the level achieved (not merely targeted); a verifier checks the level against the metadata actually present |
| `eval_run_id` | UUIDv7 | all | FK to the originating EvalRun; the lineage anchor (§ 3) |
| `recorded_at` | RFC 3339 UTC | all | when the original execution was captured (mirrors RuntimeReceipt `created_at`) |
| `model_id` | string | RF-2+ | provider+model identifier (e.g. an Anthropic/OpenAI model slug) |
| `model_version` | string | RF-2+ | the pinned model version/snapshot; "latest" is NEVER acceptable at RF-2+ |
| `seed` | integer / null | RF-2+ | the seed frozen at original execution; `verdict_source=llm_no_seed` rows cannot reach RF-2 |
| `tokenizer_id` | string | RF-2+ | the tokenizer used to freeze inputs (input freeze is tokenized per Blueprint B § 3.2.1) |
| `tokenizer_version` | string | RF-2+ | tokenizer version; a tokenizer bump that changes token boundaries is `replay.input.drift` |
| `clock_basis` | RFC 3339 UTC / null | RF-2+ | any clock value injected into the run (frozen "now"); null when the run is clock-independent |
| `environment` | object | RF-3+ | `{runtime_versions: {tool_id: version}, os: string, arch: string}` — mirrors RuntimeReceipt `tool_versions` + adds OS/arch |
| `feature_flags_snapshot` | object | RF-3+ | the exact flag→value map in effect at execution; a content-addressed snapshot, never a live read |
| `provider_adapter_versions` | object | RF-3+ | `{provider_id: version_string}` — mirrors RuntimeReceipt `provider_adapter_versions` |
| `retry_attempt` | integer | RF-1+ | which attempt produced this record (retries are new rows per Blueprint B ToolInvocation rule, not mutations) |
| `attempt_count` | integer | RF-1+ | total attempts observed for the logical step (lets a verifier detect a missing intermediate attempt) |
| `cost_basis_version` | string | RF-1+ | the cost-basis in effect (mirrors CostRecord `cost_basis_version`); a replay declares original-vs-replay basis |
| `input_digest` | `sha256:` | RF-1+ | content hash of the frozen, tokenized inputs |
| `output_digest` | `sha256:` | RF-1+ | content hash of the recorded outputs (the RF-1 playback target) |
| `provenance_chain` | array of `sha256:` | RF-4 | the full ordered digest chain from this record to the original signed attestation |

A record claiming RF-N but missing any field marked required at RF-N is **malformed**, not
"degraded RF" — it is rejected at the emission boundary the same way Blueprint B § 3.3 rejects a
predicate-contract violation (`bundle.emission.refused`, parent EvalRun → `archived_failed`).

## 3. Replay verification rules

A verifier confirms a replay is faithful by four checks, gated to the claimed RF level. A replay
is faithful only if every check applicable at its level passes; the verdict is emitted as a
`replay.verdict` OTel event (Blueprint B § 4.3) carrying one of `match`, `semantic_match`,
`drift`, or `failed`.

1. **Hash equality.** Verify `input_digest` equals the sha256 of the frozen tokenized inputs and,
   at RF-1+, that the playback `output_digest` equals the sha256 of the returned outputs. At RF-4
   the equality is byte-exact over the full output bytes; at RF-2/RF-3 it is over the canonical
   predicate body (verdict + reasons), since transport-level byte identity is not guaranteed
   below RF-4.
2. **Lineage chain.** Walk the lineage per Blueprint B § 3.2.2: `EvalRun → SessionTrace →
   ToolInvocation` chain hashes must match, and the replay record's `eval_run_id` must resolve to
   the original through the append-only lineage log (`054-AT-SPEC`). The replay is keyed to the
   original by `eval_run_id` + the originating record's content digest — never by mutable position.
3. **Integrity checks.** Verify the RuntimeReceipt signature (RF-2+) and, at RF-3+, that the
   `environment` + `feature_flags_snapshot` + `provider_adapter_versions` present at replay time
   match the frozen snapshot. Any frozen-input mismatch is a `replay.input.drift` OTel event
   (Blueprint B § 3.2.1) — surfaced, never silently re-interpreted.
4. **Divergence handling.** A divergence is any discrepancy that survives checks 1–3 at the
   claimed level. What counts as divergence is level-dependent:

   | Level | `match` | `semantic_match` | `drift` |
   | --- | --- | --- | --- |
   | RF-1 | output bytes identical to recorded | n/a (playback, no re-execution) | recorded output absent or hash mismatch |
   | RF-2 | verdict + reasons identical | verdict identical, reasons differ in non-load-bearing text | verdict differs under pinned model+seed |
   | RF-3 | RF-2 `match` under pinned environment | RF-2 `semantic_match` under pinned environment | RF-2 result diverges, or a frozen-input mismatch fired |
   | RF-4 | full output bytes identical | (RF-4 admits no `semantic_match` — bit-exact or it is `drift`) | any byte difference |

   `failed` is reserved for a verification that could not complete (the original record is
   unreadable, the lineage chain is broken, or a required signature is invalid) — distinct from
   `drift`, which is a completed verification that found a discrepancy.

**Divergence as superseding (not mutation).** When a replay yields `drift` or `failed` on a
production-Rekor-anchored record, the divergence is recorded by appending — never by editing the
original. The original signed row is byte-frozen forever (`065-AT-SPEC` § 6); the divergence is
expressed as a superseding event per `065-AT-SPEC` § 5, referencing the diverged row by its
content-addressed subject digest (and `log_index` where known) and marking it
`rolled-back-superseded` on the appended event's reference — never on the original's stored bytes.
A consumer resolves current-vs-superseded binding state from the log alone (`065-AT-SPEC` § 5
resolution rules). This is the same append-only discipline the lineage log enforces
(`054-AT-SPEC` § 4): the transparency record only ever grows.

## 4. Anti-patterns, storage, and retention

**Anti-patterns — refuse on sight.**

- **Claiming a level you did not pin.** Declaring RF-3 without a `feature_flags_snapshot`, or RF-2
  with `model_version: "latest"` (an unpinned, drifting target), or RF-2 on an `llm_no_seed`
  verdict. The metadata table (§ 2) is the discriminator; a missing required field demotes the
  claim to malformed, not to a lower RF.
- **Storing outputs without the metadata to replay them.** An output blob with no `model_version`,
  `seed`, `environment`, or digests is an RF-0 record dressed as something higher. If you cannot
  re-derive the level from the stored fields, the level is RF-0 regardless of what the row claims.
- **"Approximately reproducible" passed off as audit-grade.** Blueprint B § 3.2.4's load-bearing
  standard — **"audit-grade deterministic, not approximately reproducible"** — forbids accepting a
  near-match as a `match` for a SOC2-grade audit. A near-match is `semantic_match` at best and is
  reported as such.
- **Mutating a replay artifact after creation.** Replay records are immutable (Blueprint B § 3.2.4).
  Corrections happen by emitting a new record that references the prior `input_digest`/`output_digest`
  and, for anchored rows, by appending a superseding event (§ 3) — never by editing bytes in place.

**Storage implications — what MUST be persisted per level.**

| Level | Persist |
| --- | --- |
| RF-0 | the record + its metadata only; no frozen inputs/outputs |
| RF-1 | RF-0 + recorded input/output blobs + `input_digest`/`output_digest` |
| RF-2 | RF-1 + model id/version + tokenizer id/version + seed + clock basis |
| RF-3 | RF-2 + the `environment` block + the content-addressed `feature_flags_snapshot` + provider-adapter versions |
| RF-4 | RF-3 + the full `provenance_chain` + transport-deterministic output bytes |

The frozen inputs/outputs are content-addressed blobs in object storage (Blueprint B § 5.1); the
record row carries only the digests. A `feature_flags_snapshot` at RF-3+ is itself
content-addressed, so two records pinning the same flag set share one blob.

**Retention rules.** Replay capability is bounded by the retention of the artifacts it depends on,
per the Blueprint B § 4.2 lifecycle classes. A record's effective replayable lifetime is the
MINIMUM of: its own retention, its RuntimeReceipt's retention (hot 90 d / cold 1 yr / archive
thereafter), and its SessionTrace's retention (hot 30 d / cold 180 d). Once any dependency expires,
the record's achievable RF level degrades — a verifier MUST recompute the level from the metadata
still present rather than trust the recorded `rf_level`. Production-Rekor-anchored records are an
exception: the anchored attestation and its EvidenceBundle index are retained for the life of the
transparency log (never expired), so an RF-3/RF-4 anchored gate decision remains verifiable
indefinitely even after its hot/cold operational copies age out.

## 5. Cross-references

- **Blueprint B § 3.2** (`012-AT-ARCH-platform-runtime-blueprint.md`) — replay semantics; the
  re-executable-inputs rule, `replay.input.drift`, the per-predicate fidelity mapping, and the
  audit-grade-deterministic standard this doc enumerates levels for.
- **Blueprint B § 4.3** — the `replay.*` OTel event category and the four pinned attributes
  (`replay.verdict`, `replay.input.drift`, `replay.is_replay`, `replay.original_trace_id`). The
  `replay.verdict` enum used in § 3 (`match`/`semantic_match`/`drift`/`failed`) is the one pinned
  there.
- **iec-E06** (`@intentsolutions/core`, kernel runtime contracts) — the RuntimeReceipt,
  SessionTrace, ToolInvocation, and CostRecord field contracts the § 2 metadata table aligns to
  (`eval_spec_content_hash`, `skill_snapshot_sha`, `provider_adapter_versions`, `tool_versions`,
  `cost_basis_version`, `verdict_source`).
- **`054-AT-SPEC` (lineage log)** — the append-only `(EvalRun → SessionTrace → ToolInvocation)`
  chain the § 3 lineage check walks; divergence-as-append shares its grow-only discipline.
- **`064-AT-DECR` (predicate compatibility policy)** — the FORWARD/BACKWARD/MIXING/DEPRECATION
  rules every predicate URI obeys; a new RF-bearing field added to a predicate body MUST satisfy
  Rule (a) FORWARD compatibility so an existing reader ignores it safely.
- **`065-AT-SPEC` (Rekor superseding-event protocol)** — the divergence-as-superseding mechanism
  in § 3: the `superseded_window` reference shape, the `rolled-back-superseded` marker on the
  appended event, and the consumer's current-vs-superseded resolution.
- **iel-E12** (forthcoming runtime-event-name taxonomy) — the canonical registry of `replay.*`
  per-event names; this doc cites the four already-pinned attributes and defers the rest.
