# Skill Refiner Evidence Report Spec — v1.0.0-draft

> **Status: NORMATIVE DRAFT.** This module defines the canonical shape of the
> **Skill Refiner Evidence Report** — the dual-format (markdown + HTML) artifact
> the Skill Refiner emits when its acceptance gate reaches a verdict on a
> proposed `SKILL.md` edit. It is the **human-readable and machine-verifiable
> view** of a single `skill-refiner-pass/v1` in-toto attestation.
>
> **Predicate-authority notice.** The predicate this report renders —
> `skill-refiner-pass/v1` — is defined **normatively by the kernel**, not by
> this document. The canonical JSON Schema is
> `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json` and the Zod
> validator / Pydantic mirror ship in the same package. The normative prose
> here (and the § 11 data-model trace) MUST agree with the kernel schema; **the
> kernel schema wins on any conflict.** This document specifies the _report_ —
> field layout, section ordering, rendering, verification instructions — not the
> attestation shape.
>
> **URI-declaration discipline (CISO binding, DR-004 / DR-010).** The predicate
> URI `https://evals.intentsolutions.io/skill-refiner-pass/v1` is **declared**
> only by the kernel + `PREDICATE-TYPES.md`. This document **renders and
> references** that URI; it does NOT declare, reserve, or mint it.
> `labs.intentsolutions.io` is reserved-don't-touch and MUST NOT appear as a
> predicate URI, OTel attribute namespace, or attestation predicate identifier
> anywhere in a report.
>
> **Stage-gate role.** Landing this SPEC.md normative section is DR-082 Q3
> production-trigger #1 — the trigger that moves `skill-refiner-pass/v1` from
> `RESERVED` to `ACTIVE` in [`specs/PREDICATE-TYPES.md`](../../PREDICATE-TYPES.md).
> Activation does NOT unlock production-Rekor signing on its own: the remaining
> three DR-082 Q3 triggers (DNSSEC + CAA green on `evals.intentsolutions.io`;
> the authoring chamber's separate signing trust root live; ≥1 real SkillVersion
> cleared on a frozen signed eval-set) are AND-gated with it. Until all four
> hold a report renders `signing_mode = staging` and `rekor_log_index = null`.

## 1. Purpose

A **Skill Refiner Evidence Report** is the per-pass deliverable that lets any
reader — a partner, an auditor, a future maintainer — _see_ that the eval ran,
what it decided, and why the decision is defensible, without trusting the team
that produced it.

The Skill Refiner proposes safe, minimal edits to a `SKILL.md` and accepts an
edit only on a strict predicate: **significant Pareto-dominance on the
kernel-pinned `behavioral` dimension AND non-regression on every other named
dimension**, by a one-sided z-test at the stated `alpha` (DR-028 P0-RATIFY-1).
The Evidence Report is the record of one such verdict. Its value proposition is
**independent verifiability**: every claim in the report either traces to a
field in the signed `skill-refiner-pass/v1` attestation body or is explicitly
marked as provenance bulk carried out-of-band by hash.

A report is a **projection of one attestation**, not a second source of truth.
The signed predicate body is canonical; the report MUST NOT assert any accept
determinant that contradicts the body it renders.

## 2. Scope

### 2.1 In scope (v1.0.0-draft)

| Concern                                                               | Where in this spec |
| --------------------------------------------------------------------- | ------------------ |
| The 10 required report sections + metadata header                     | § 5–§ 6            |
| Normative field layout of the metadata header table                   | § 5                |
| Data-model trace from every rendered field to the kernel predicate    | § 11               |
| Before/after behavioral-metric table + Pareto-dominance visualization | § 7                |
| Provenance + signature-verification rendering (Rekor + cosign)        | § 8                |
| Determinism + reproducibility of the render                           | § 9                |
| Dual-format contract (canonical markdown, derived HTML)               | § 10               |
| Report storage + retention                                            | § 12               |
| Conformance reporting                                                 | § 13               |

### 2.2 Out of scope (v1.0.0-draft)

- **The attestation shape itself.** `skill-refiner-pass/v1`'s field set, closed
  enums, cross-field invariants, and immutability doctrine are defined by the
  kernel schema + DR-082 / DR-085. This document renders that shape; it does not
  define it.
- **The acceptance-gate mechanism.** How the one-sided z-test is computed, how
  the RefinerStrategy proposes edits, and how the behavioral eval-set is
  constructed live in `@intentsolutions/refiner-core` + the eval-set governance
  spec.
- **The predicate URI reservation lifecycle.** Owned by `PREDICATE-TYPES.md`
  (RESERVED / ACTIVE / etc.); a Class-1 ISEDC act.
- **HTML renderer implementation.** § 10 specifies the _contract_ the renderer
  MUST satisfy; the Hugo template + chart code is a downstream deliverable.
- **Signing-key custody + Rekor operations.** Owned by the CISO signing runbook.

## 3. Conformance keywords

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are used per
[RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174).

## 4. Report identity + naming

The canonical form of a report is the **markdown AAR** (§ 10.1); the HTML render
(§ 10.2) is a derived view. A conforming markdown report:

- MUST be filed per the Document Filing Standard v4.x as
  `<repo>/000-docs/NNN-RL-REPT-skill-refiner-<skill-id>-<date>.md`.
- MUST be committed to git in the repository whose `SKILL.md` was refined.
- MUST render exactly one `skill-refiner-pass/v1` verdict. A report that renders
  more than one verdict is non-conforming; multi-pass campaigns emit one report
  per verdict and MAY be cross-linked.
- MUST carry the 10 numbered sections of § 6 **in order**, each with its
  section number. A missing required section fails the BLOCKING completeness
  gate (§ 13).

## 5. Metadata header table (REQUIRED)

Every report MUST open, immediately below its H1 title, with a metadata header
table carrying the following rows. Each row is REQUIRED unless marked OPTIONAL.
Hash-valued rows MUST render an 8-character hex prefix of the full
`sha256:`-prefixed value AND MUST NOT drop the full value's traceability — the
full hash is carried in the § 7 attestation body reference.

| Row                    | Source (kernel predicate field or derived)                          | Requirement |
| ---------------------- | ------------------------------------------------------------------- | ----------- |
| Date                   | envelope timestamp (in-toto Statement / DSSE, NOT the signed body)  | REQUIRED    |
| Skill                  | in-toto `subject[].name`                                            | REQUIRED    |
| Skill version (input)  | `source_snapshot_hash` (pre-edit input), 8-char prefix              | REQUIRED    |
| Skill version (output) | `result_snapshot_hash` (post-edit output), 8-char prefix            | REQUIRED    |
| SkillVersion id        | `skill_version_id`                                                  | REQUIRED    |
| Parent SkillVersion id | `parent_version_id` (render `— (root)` when `null`)                 | REQUIRED    |
| Eval set               | `eval_set_ref.hash` (8-char prefix) + `eval_set_ref.version`        | REQUIRED    |
| Verdict                | `verdict` (`accept` \| `reject`)                                    | REQUIRED    |
| Behavioral delta       | `behavioral_delta` (rendered as signed pp)                          | REQUIRED    |
| Named-dimension deltas | `named_dimension_deltas[]` summarized (id +delta, non-regress flag) | REQUIRED    |
| Significance level (α) | `alpha`                                                             | REQUIRED    |
| Test statistic         | `test_statistic_kind` (`one-sided-z`)                               | REQUIRED    |
| Refiner strategy       | `refiner_strategy_id`                                               | REQUIRED    |
| Edit proposal          | `edit_proposal_hash` (8-char prefix)                                | REQUIRED    |
| Signing mode           | `signing_mode` (`staging` \| `production`)                          | REQUIRED    |
| Rekor log index        | `rekor_log_index` (render `null` under `staging`)                   | REQUIRED    |
| Compute cost           | `cost_record_ref` → CostRecord (per-tier breakdown)                 | OPTIONAL    |
| Wall-clock             | derived from the refiner run                                        | OPTIONAL    |
| Replay fidelity        | `replay_fidelity_level` (RF-0 … RF-4)                               | OPTIONAL    |

The metadata header is a **summary index**, not an authority: on any conflict
between a header cell and the § 7 attestation body, the attestation body wins,
and the report is non-conforming until reconciled.

## 6. Required sections (the 10)

Plan § E.1 enumerates **exactly 10** required narrative sections. A conforming
report MUST include all 10, numbered `## 1` … `## 10`, in the order below.

### 6.1 — § 1 Context

The report MUST state why this skill was refined and the trigger class
(`manual` | `drift` | `scheduled`). It SHOULD name the upstream event (e.g. a
frontier-model bump, a persistent-drift alarm) when the trigger was not manual.

### 6.2 — § 2 Eval set composition

The report MUST describe the frozen eval-set the verdict was derived against:
source (`synthetic` | `harvested` | `golden` | `hybrid`), size (N items),
diversity/stratification, and the `eval_set_ref` (hash + version + lineage_id)
that pins it. This section is the **epistemic basis** of the claim; it MUST NOT
be omitted or hand-waved. The rendered `eval_set_ref` MUST match the kernel body
byte-for-byte on the hash.

### 6.3 — § 3 Score trajectory

The report MUST show the before/after behavioral metric and every named
dimension's delta across the pass, per § 7. It MUST render the final
`behavioral_delta` and each `named_dimension_deltas[].delta` against the
baseline, and MUST make the Pareto-dominance judgment visible (§ 7).

### 6.4 — § 4 Accepted edits (replayable)

For an `accept` verdict, the report MUST render the accepted edit as a
**replayable** record: the RefinerStrategy identifier + verbatim rationale, the
op class (`add` | `delete` | `replace`), a unified diff, pre-score → post-score,
and the acceptance-gate evidence (the deltas + α + test statistic that cleared
the gate). The rendered edit MUST hash to `edit_proposal_hash`; a reader MUST be
able to re-derive the bounded edit-ops and reproduce the post-edit artifact
whose content hashes to `result_snapshot_hash`. A `reject` verdict renders this
section as `— (no accepted edit; see § 5)`.

### 6.5 — § 5 Rejected edits (audit trail)

The report MUST record every rejected candidate considered in reaching this
verdict: op class, RefinerStrategy, pre-score → post-score (showing the absent
or insufficient improvement), and the structured rejection reason (e.g.
`pareto-incomparable`, `named-dimension-regressed`) drawn from the gate output.
Rejected-edit prose is provenance bulk and MUST NOT leak `SKILL.md` content onto
a public transparency log; reason codes are structured, not free prose (CISO +
GC binding).

### 6.6 — § 6 Hook-layer gate evidence (per pass)

The report MUST map the pass to its enforcement evidence: a table joining
pass-number → `skill_version_id` → ScoreRecord hash → the signed
`skill-refiner-pass/v1` row, with the `rekor_log_index` per signed row (or
`null` under `staging`) and which hook layer fired — sinker (L1) / line (L2) /
hook (L3, `PreToolUse:Bash`). This section binds the _decision_ to the _machine
that enforced it_.

### 6.7 — § 7 Signed Evidence Bundle (in-toto Statement v1)

The report MUST render or link the signed `skill-refiner-pass/v1` in-toto
Statement v1 row: `predicateType` =
`https://evals.intentsolutions.io/skill-refiner-pass/v1`, the `subject`
(post-edit artifact, whose `digest.sha256` equals `result_snapshot_hash` without
the `sha256:` prefix), and the predicate body. It MUST include the
verification command (§ 8). Under `staging` the report MUST state that the row
is `sigstore_staging` and carries no production Rekor index.

### 6.8 — § 8 Architectural bindings

The report MUST cite the governance it honors: DR-010, Blueprint B § 7 (the
predicate-authority + no-top-level-bundle-signature rules), the Canonical
Glossary, DR-028 (the accept predicate + SkillVersion semantics), and
DR-082 / DR-085 (the predicate URI + one-way-door corrections). It SHOULD name
the P0 beads honored by the emission path.

### 6.9 — § 9 Limitations + risks

The report MUST disclose the failure modes the eval-set may not have exercised,
Goodhart corner-cases the behavioral dimension may reward perversely, and a
recommended re-validation cadence. An accept verdict is a claim bounded by the
frozen eval-set — this section states those bounds honestly.

### 6.10 — § 10 Status banding

The report MUST carry a status band from the closed vocabulary: `ACTIVE` |
`SUPERSEDED-BY-NNN` | `INVERTED-BY-EMPIRICAL-FINDING` | `RATIFIED-AND-STABLE`.
This is the report's own lifecycle label per the State-Labeling Standard, and is
distinct from the predicate's `RESERVED`/`ACTIVE` stage in `PREDICATE-TYPES.md`.

## 7. Before/after behavioral table + Pareto-dominance visualization (REQUIRED)

Section § 3 (score trajectory) MUST render a **before/after behavioral-metric
table** and a **Pareto-dominance visualization**. This is the visual core of the
report's defensibility and is normative, not decorative.

### 7.1 Before/after table

The table MUST have one row per evaluated dimension and MUST include the
behavioral dimension plus every entry in `named_dimension_deltas[]`. Each row
MUST render: dimension id; baseline (pre-edit) score; candidate (post-edit)
score; delta (signed); and, for named dimensions, the `non_regressed` boolean.
The behavioral row's delta MUST equal `behavioral_delta`; each named row's delta
MUST equal the corresponding `named_dimension_deltas[].delta`.

### 7.2 Pareto-dominance visualization

The report MUST make the accept predicate **visible at a glance**:

- It MUST show that the behavioral dimension is significantly Pareto-dominant
  (behavioral delta positive and significant at `alpha`) AND that no named
  dimension regressed (every `named_dimension_deltas[].non_regressed === true`
  for an `accept` verdict — the DR-085 D5 machine-enforced invariant).
- It MUST distinguish the three outcomes the gate can reach: **accept**
  (behavioral-dominant, all named non-regressed), **reject —
  named-dimension-regressed**, and **reject — pareto-incomparable** (neither
  version dominates; DR-028 tie-break).
- It SHOULD render as a dominance quadrant / delta bar-set keyed on
  behavioral-vs-named, but the exact chart form is a rendering choice; the
  MUST is that the predicate outcome is unambiguous from the visualization.

A report whose visualization contradicts its rendered `verdict` (e.g. shows a
regressed named dimension under an `accept`) is non-conforming.

## 8. Provenance + signature verification (REQUIRED)

The report exists to be _checked_, not trusted. Section § 7 MUST carry a
verification block that a reader can run unchanged.

### 8.1 Rekor + cosign rendering

- The report MUST render the predicate URI as
  `https://evals.intentsolutions.io/skill-refiner-pass/v1`. It MUST NOT render,
  declare, or reference any predicate URI under `labs.intentsolutions.io`.
- Under `signing_mode = production`, the report MUST render the
  `rekor_log_index` as a concrete integer and SHOULD link the Rekor transparency
  entry. Under `signing_mode = staging`, it MUST render `rekor_log_index: null`
  and state that the row is anchored to `sigstore_staging` (no production
  transparency entry exists yet).
- The report MUST include a copy-pasteable `cosign verify-blob` command that
  verifies the DSSE-wrapped in-toto Statement, plus the `jq` filter that pulls
  the rendered determinants back out of the verified body. The command MUST NOT
  embed secrets; it references the public key / certificate identity and the
  Rekor URL only.

### 8.2 No top-level bundle signature

Consistent with Blueprint B § 7, each row is **independently verifiable** and
there is NO top-level bundle signature. The report MUST NOT imply that a bundle
wrapper is itself signed; verification is per-row against the `skill-refiner-pass/v1`
DSSE envelope.

### 8.3 Subject-digest binding

The report MUST state the DR-082 Q4 / DR-085 D4 wire discipline: the in-toto
`subject[].digest.sha256` equals `result_snapshot_hash` **without** the
`sha256:` prefix (the subject is the post-edit artifact being attested). A
reader verifying the row MUST be able to confirm this binding from the rendered
values.

## 9. Determinism + reproducibility (REQUIRED)

The markdown report is a **deterministic projection** of a single attestation.

- Given the same `skill-refiner-pass/v1` body (+ the referenced provenance
  artifacts), the renderer MUST produce byte-identical markdown. No wall-clock,
  no non-deterministic ordering, no locale-dependent formatting in the canonical
  markdown.
- `named_dimension_deltas[]` MUST render in a stable order (the order in the
  signed body); the renderer MUST NOT re-sort them.
- Any value NOT present in the signed body (compute cost, wall-clock,
  human-readable diff prose, dashboard-render metadata) is **provenance bulk**
  and MUST be sourced by hash-reference through the EvidenceBundle side-channel,
  never fabricated. Absence of an OPTIONAL value MUST render as an explicit
  `—`, never as an invented placeholder.
- Reproducibility claim: a third party holding the signed body + the referenced
  eval-set + edit-proposal MUST be able to re-derive the verdict determinants
  (deltas, α, test statistic) and re-run the one-sided z-test to independently
  confirm the accept/reject decision. The report SHOULD state the replay-fidelity
  level (`replay_fidelity_level`, RF-0 … RF-4) achieved.

## 10. Dual-format contract

### 10.1 Markdown AAR (canonical)

The markdown report is the single source of truth: git-versioned,
machine-parseable, carrying the § 5 header + the 10 § 6 sections. Every other
format is derived from it.

### 10.2 HTML projection (derived)

The HTML render MUST be generated deterministically FROM the canonical markdown
(not authored separately). It MUST preserve every REQUIRED datum and MUST NOT
introduce a claim absent from the markdown. It MUST render at minimum: a hero
(skill + behavioral delta + verdict); the § 7 before/after table + Pareto
visualization; a side-by-side diff for the accepted edit; the collapsible
rejected-edits table; and a **verification panel** exposing the `rekor_log_index`
(or the `staging`/`null` state) and the copy-pasteable `cosign verify-blob`
command. Reports render under `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/`
and MUST NOT be served from, or declare any predicate URI at,
`labs.intentsolutions.io`.

## 11. Data model — kernel-predicate field trace (NORMATIVE)

Every rendered accept determinant MUST trace to a field of the
`skill-refiner-pass/v1` predicate body. The canonical definition is the kernel
schema `@intentsolutions/core/schemas/v1/skill-refiner-pass.schema.json`
([GitHub](https://github.com/jeremylongshore/intent-eval-core/blob/main/schemas/v1/skill-refiner-pass.schema.json))
and its Zod / Pydantic mirrors. The table below is the report-side trace; **the
kernel schema wins on any conflict.**

### 11.1 Required predicate fields (13) → report surface

| Kernel field (required)  | Type                          | Rendered in                                 |
| ------------------------ | ----------------------------- | ------------------------------------------- |
| `verdict`                | `'accept' \| 'reject'`        | § 5 header (Verdict); § 6.7                 |
| `reason`                 | `string[]` (structured codes) | § 6.5 (rejection) / § 6.4 (accept evidence) |
| `refiner_strategy_id`    | `string`                      | § 5 header; § 6.4 (rationale attribution)   |
| `skill_version_id`       | UUIDv7                        | § 5 header; § 6.6 gate-evidence join        |
| `parent_version_id`      | UUIDv7 \| `null`              | § 5 header (`— (root)` when null)           |
| `source_snapshot_hash`   | sha256-prefixed (pre-edit)    | § 5 header (Skill version input)            |
| `result_snapshot_hash`   | sha256-prefixed (post-edit)   | § 5 header (output); § 8.3 subject binding  |
| `eval_set_ref`           | `{hash, version, lineage_id}` | § 6.2 (composition)                         |
| `edit_proposal_hash`     | sha256-prefixed               | § 5 header; § 6.4 (replay binding)          |
| `behavioral_delta`       | `number`                      | § 5 header; § 7.1 behavioral row            |
| `named_dimension_deltas` | `NamedDimensionDelta[]`       | § 7.1 table; § 7.2 dominance viz            |
| `alpha`                  | `number` in (0, 1)            | § 5 header; § 7.2; § 8 verification         |
| `test_statistic_kind`    | `'one-sided-z'` (const)       | § 5 header; § 7.2                           |

`NamedDimensionDelta` = `{ id: kebab-slug, delta: number, non_regressed: boolean }`.
For an `accept` verdict, every `non_regressed` MUST be `true` (DR-085 D5). § 7.2
MUST render this invariant visibly.

### 11.2 Optional predicate fields (3) → report surface

| Kernel field (optional)    | Type                     | Rendered in                            |
| -------------------------- | ------------------------ | -------------------------------------- |
| `cost_record_ref`          | UUIDv7 (FK → CostRecord) | § 5 header (Compute cost), if present  |
| `replay_fidelity_level`    | `RF-0 … RF-4`            | § 5 header; § 9 reproducibility claim  |
| `signing_downgrade_reason` | `string`                 | § 6.6 / § 8.1, when signing downgraded |

### 11.3 Envelope-derived fields (NOT in the signed body)

The signed determinant body carries **no timestamp** and no signing coordinates;
those live on the surrounding in-toto Statement / DSSE envelope and are rendered
as envelope-derived, clearly distinguished from body fields:

| Envelope / derived value | Source                                                 | Rendered in            |
| ------------------------ | ------------------------------------------------------ | ---------------------- |
| Date                     | in-toto Statement / DSSE envelope timestamp            | § 5 header (Date)      |
| Skill (subject name)     | in-toto `subject[].name`                               | § 5 header (Skill)     |
| `signing_mode`           | EvidenceBundle emission context (cross-field w/ Rekor) | § 5 header; § 8.1      |
| `rekor_log_index`        | transparency-log entry (`null` under `staging`)        | § 5 header; § 6.6; § 8 |

The `signing_mode` / `rekor_log_index` pair MUST satisfy the DR-028 cross-field
invariant: a non-null `rekor_log_index` iff `signing_mode = production`. A report
rendering a non-null Rekor index under `staging` is non-conforming.

## 12. Report storage + retention

| Artifact               | Storage                                                             | Retention                                  |
| ---------------------- | ------------------------------------------------------------------- | ------------------------------------------ |
| Markdown AAR           | `<repo>/000-docs/NNN-RL-REPT-skill-refiner-*.md` (committed to git) | Permanent                                  |
| Signed attestation row | `<repo>/.j-rig/refiner/evidence/<sha>.json`                         | Indexed by sha; orphans GC'd after 90 days |
| HTML render            | `evals.intentsolutions.io/reports/<skill-id>/<sha-prefix>/`         | Pinned per version; never overwritten      |
| Rekor log entry        | Public sigstore Rekor (production) / staging log                    | Permanent by design (one-way door)         |

## 13. Conformance

A report is **conforming** to this spec iff:

1. It carries the § 5 metadata header with every REQUIRED row.
2. It carries all 10 § 6 sections, numbered and in order (BLOCKING completeness
   gate — a missing required section fails).
3. Every rendered accept determinant traces to a kernel predicate field per
   § 11 and does not contradict the signed body.
4. The § 7 before/after table + Pareto-dominance visualization are present and
   agree with the rendered `verdict`.
5. The § 8 verification block renders the `evals.intentsolutions.io` predicate
   URI (never `labs.*`), the correct `signing_mode` / `rekor_log_index` state,
   and a runnable `cosign verify-blob` command.
6. The markdown render is deterministic (§ 9) and the HTML projection introduces
   no claim absent from the markdown (§ 10.2).

A claim of conformance without these checks passing is not a claim.

---

- Jeremy Longshore
  intentsolutions.io
