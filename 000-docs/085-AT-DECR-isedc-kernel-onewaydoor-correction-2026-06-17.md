---
title: ISEDC Corrective Council — IEP Kernel One-Way-Door Correction
date: 2026-06-17
acting_head_of_board: Claude (acting, designated by Jeremy Longshore via CTO-mode delegation, 2026-06-17)
council_size: 7
seats: [CTO, GC, CMO, CFO, CSO, CISO, VP DevRel]
decisions_logged: 5
status: ratified
outcome: 7-0 on all five questions with stacked minority bindings
trigger: 3-reviewer adversarial glance (code-reviewer + martin-kleppmann + rich-hickey) on merged-but-unpublished kernel PRs #56 (skill-refiner-pass/v1 predicate) + #57 (SkillVersion entity)
amends: DR-028 (T1/P0-RATIFY-2 reconciliation), DR-082 (predicate-v1 erratum + freeze-point doctrine)
holds: [intent-eval-lab PR #171 HELD, "@intentsolutions/core untagged until D1-D5 land"]
session_provenance: ~/.claude/skills/exec-decision-council/sessions/2026-06-17-iep-kernel-onewaydoor-correction/session.jsonl
---

# ISEDC Corrective Council — IEP Kernel One-Way-Door Correction (2026-06-17)

## 1. Mission of this Decision Record

A 3-reviewer adversarial glance found one-way-door defects in two **merged-but-unpublished** kernel artifacts — the `skill-refiner-pass/v1` predicate (PR #56) and the `SkillVersion` 14th entity (PR #57). The defects are correctable today at near-zero cost, but the window **closes at the next `git tag v0.8.0`** of `@intentsolutions/core`. Two of the corrections touch artifacts already ratified by prior councils (DR-082 froze v1; DR-028 shaped SkillVersion), and one defect *is* an internal contradiction inside DR-028. Those cannot be changed unilaterally — so this corrective council adjudicates the fixes, amends the conflicting records, and sets the doctrine that governs every future staging-first predicate.

## 2. Why a council, not a single review

The decisions are asymmetric and one-way: a wrong call enshrines a cryptographically-notarized falsehood on a public transparency log, or burns a `/v2` URI on a draft that was never signed, or sets a precedent for how Intent Solutions treats "ratified-but-unsigned" artifacts forever. The author's own review (and the build agent's) already missed these — exactly the failure mode adversarial seats exist to catch. The thinker-reviewers (Kleppmann, Hickey, the code-reviewer) were the **input** to this council, not seats on it.

## 3. Synthesis lenses

1. The arena (5 surfaces): APIs · CLIs · MCP servers · agents · SKILL.md.
2. Both sides: client-side + server-side eval.
3. The transformation pipeline: API → CLI → MCP → SKILL.md → agent.
4. Composable partial attestation: every component a valid entry; silence ≠ failure.
5. **Fix-window lens:** the immutability cost is not yet incurred (nothing on production Rekor; #56/#57 unpublished); the window closes at the next `@core` tag. Weigh "correct cheaply now" against "every correction sets a precedent for ratified-but-unsigned artifacts."

## 4. The questions

| # | Class | Question |
|---|---|---|
| Q1 | Governance | DR-028 T1 (line 105, defer signing fields) vs P0-RATIFY-2 (lines 233-236, add them now) — both 20/20-ratified and contradictory. Which controls the v0.8.0 SkillVersion shape, and what is the fix for the build agent's silent unilateral resolution? |
| Q2 | Immutable | The corrections change the body DR-082 ratified as "v1 frozen." With v1 at `signing_mode=ln` and no production-Rekor signature, amend `skill-refiner-pass/v1` in place, or mint `/v2`? |
| Q3 | Architecture | Content-hash chain (`content_hash` + `parent_content_hash`, alphabet-aligned to `SkillSnapshot.combined_sha`) for tamper-evident lineage vs reassignable `parent_version_id` UUID; and resolve predicate-vs-entity parent nullability so a root attests without forging a parent. |
| Q4 | Schema | `source_snapshot_hash` pre-edit (entity) vs post-edit (predicate) name collision — add `result_snapshot_hash`? Canonical `signing_mode` staging label (`ln` vs `sigstore_staging`)? |
| Q5 | Enforcement | Mandate 3-layer enforcement (JSON-Schema `if/then` + Zod `superRefine` + Pydantic `model_validator`) of the signed cross-field invariants before v0.8.0, plus a standing kernel CI gate for unenforced-invariant-on-a-signed-row? |

## 5. Council composition

Default 7-seat ISEDC roster: **CTO** (schema durability/immutability), **GC** (audit-trail/governance integrity), **CMO** (positioning/narrative), **CFO** (bandwidth/opportunity cost), **CSO** (standards-body realpolitik), **CISO** (attestation integrity/threat model), **VP DevRel** (developer friction-to-adopt). Acting head of board: Claude, delegated by Jeremy via CTO-mode.

## 6. Vote tally

| Question | Outcome | Vote |
|---|---|---|
| Q1 | (c) ratified hybrid + halt-on-conflict governance gate | **7-0** |
| Q2 | (a) amend v1 in place; freeze = first production-Rekor signature | **7-0** |
| Q3 | content-hash chain + nullable parent | **7-0** |
| Q4 | (a) add `result_snapshot_hash` + canonical `sigstore_staging` | **7-0** |
| Q5 | all-three-layer enforcement + standing scoped CI gate | **7-0** |

**Most-costly-to-recover tally:** Q5 ×6 · Q3 ×1 (VP DevRel). **Adversarial-integrity check: PASS** — unanimity on direction, but real value-system collision preserved in the minority bindings (CMO/CFO vs CTO/CISO/GC on cost-and-speed; GC named the CTO seat, the PR #57 reviewer, as the silent-resolver to its face; CFO explicitly out-hawked its own cost-cutting bias on Q3; VP DevRel broke from the 6-seat Q5 tally to name Q3). Not consensus theater — the clash is in *how* to fix, *what* to record, and *how* to scope, never *whether*.

## 7. Decision tree

```
        ISEDC Corrective Council — IEP Kernel One-Way-Door (2026-06-17)
                     7 seats · acting head: Claude (CTO-mode)
                                     │
   ┌──────────────┬─────────────────┼─────────────────┬──────────────┐
  Q1             Q2                Q3                Q4             Q5
DR-028 conflict amend vs /v2   lineage + parent   semantic     enforcement
   │              │                │                │              │
 7-0 (c)        7-0 (a)         7-0 chain        7-0 (a)        7-0 3-layer
 hybrid +       amend in place  + nullable       result_        + standing
 HALT gate      freeze = 1st    parent;          snapshot_hash  scoped gate
 on conflict    prod signature  root = zero-     + sigstore_       │
   │              │             forgery          staging       version_kind
 amends         erratum +          │             retire ln     /v2-trap flagged
 DR-028         no-prior-sig                                       │
                attestation
                                                 ── most-costly: Q5 ×6 · Q3 ×1 ──
                                                 ── adversarial integrity: PASS ──
```

## 8. Verbatim seat positions (Position · Why), by question

> Full per-seat blocks (pros/cons, expected-tension, accepted-compromise, council memos) are preserved verbatim in `session.jsonl`. Below is each seat's recommended answer + core rationale per question.

### Q1 — DR-028 internal conflict
- **CTO:** (c) hybrid — T1 controls sequencing, P0-RATIFY-2 controls eventual shape (defer-then-add); signing fields with no trust root are dead slots. Halt gate on conflict.
- **GC:** (c) hybrid, but the reconciliation MUST be a recorded Class-1 amendment naming line-105 + lines-233-236 verbatim; the *silent unilateral resolution* is the more serious finding — an unrecorded exercise of authority the agent doesn't hold.
- **CMO:** (c) hybrid; a self-contradicting governance record is a narrative liability; conflict-flag duty (halt-and-flag, not halt-and-wait-a-week).
- **CFO:** (c) hybrid — T1's deferral is free bandwidth; premature signing fields force `rekor_log_index`-iff-`production` wiring before a production Rekor exists.
- **CSO:** (c) hybrid recorded as a Class-1 micro-DR; empty signed-surface fields read as cargo-culting to OpenSSF reviewers.
- **CISO:** (c) hybrid; signing fields before the trust root = an attestation field that can only lie; ratification-conflict-marker as a blocking CI gate; dated re-open tied to DR-082 trigger 3.
- **VP DevRel:** (c) hybrid; the implementer needs a stable shape now while the signing surface lands additively; silent resolution is the inverse of OSS norms.

### Q2 — amend-in-place vs /v2
- **CTO:** (a) amend in place; frozen attaches at first production-Rekor signature; window = no production logIndex exists.
- **GC:** (a), conditioned on a DR-082 erratum + a one-time written "frozen = first production signature" ruling + an auditable "no production signature ever existed" attestation.
- **CMO:** (a); a `/v2` minted before `/v1` ever signed is a self-inflicted credibility scar; staging-first is a marketable safety property.
- **CFO:** (a); a `/v2` mint is pure bandwidth tax to escape an immutability cost we have not incurred.
- **CSO:** (a) — the crux for my seat; in-toto/sigstore immutability lives in the transparency log, not a council vote; minting `/v2` for a never-signed shape reads as versioning-hygiene panic.
- **CISO:** (a); immutability is a transparency-log property; bind verbatim diff + "no production signature ever existed" attestation.
- **VP DevRel:** (a); telling a developer a staging predicate is immutable is theater that teaches them to fear the rig; minting `v2` makes the changelog lie about what `v1` was.

### Q3 — lineage integrity + parent nullability
- **CTO:** content-hash chain; `parent_content_hash` = integrity anchor, `parent_version_id` = convenience pointer (both, not either); align alphabet; predicate parent nullable.
- **GC:** chain + alphabet align + predicate parent nullable; a signed row asserting unprovable append-only lineage is a false attestation.
- **CMO:** chain; parent-nullability non-negotiable now; "tamper-evident lineage" is a headline/standards claim — a retracted integrity claim costs 10× a delayed one.
- **CFO:** chain + alphabet align — the one place I out-hawk the cost-cutters; the broken path is already exercised by a shipped fixture.
- **CSO:** chain; an append-only claim a reviewer can falsify by reassigning a UUID can't appear in a SLSA-adjacent attestation; alphabet alignment non-negotiable.
- **CISO:** chain + nullable-with-root-marker; a required-non-null parent FORCES implementers to forge a fake parent on roots — manufacturing the laundering we exist to stop.
- **VP DevRel:** chain + nullable parent — forge-a-fake-parent is the single worst first-run experience; root emission must be provably zero-forgery (null parent_version_id + null parent_content_hash).

### Q4 — semantic collision + label
- **All seats: (a)** add `result_snapshot_hash` (post-edit); `source_snapshot_hash` = pre-edit input consistently across entity + predicate; canonical staging label **`sigstore_staging`**, retire `ln`. CISO: keep the name `source_snapshot_hash` (don't rename both sides — minimize diff). CMO/GC: changelog alias `ln`→`sigstore_staging` + a canonical-label registry entry.

### Q5 — enforcement
- **All seats:** mandate all-three-layer enforcement before v0.8.0 + a standing kernel CI gate, **scoped to signed predicate/entity schemas** (CFO/CISO/CSO). GC/CFO: gate may land warn-only for one tag only if v0.8.0 itself ships fully enforced. CTO: `version_kind` closed enum is a `/v2`-widening trap (per the DR-028 dissent) — make the open/closed posture explicit, enforce the root invariant. CISO: "a predicate whose accept-rule isn't machine-enforced has a forgery cost of zero — the number standards bodies measure us by."

## 9. Council memos (cross-question themes, verbatim digest)

- **CTO** — *"The fix window is a free pass through the one-way door — spend it on correctness."* Most-costly: Q5. Underweighted: CMO/CFO read "staging/unpublished" as low-stakes; it's the inverse.
- **GC** — *"The record must equal the artifact."* Most-costly: Q5. Underweighted: the Q1 silent-resolution defect is the precedent that compounds; flag-and-halt is the load-bearing remedy.
- **CMO** — *"The unsigned window is a gift — ship one clean, provably-true v1 story; a retracted claim costs more narrative than any delay."* Most-costly: Q5. Underweighted: a `/v2` minted before `/v1` signed is itself a permanent scar.
- **CFO** — *"Spend only the bandwidth that prevents an immutable unbounded liability; defer everything else."* Most-costly: Q5. Underweighted: the fix window is the cheapest dollar we'll ever spend on this predicate.
- **CSO** — *"The transparency log is the only real freeze; everything upstream of a production signature is correction surface."* Most-costly: Q5. Underweighted: GC/CISO "ratification=freeze" inverts how in-toto/sigstore reason.
- **CISO** — *"No signed row may assert a property nothing enforces."* Most-costly: Q5 (+ its Q1 signing-field corollary). Underweighted: the real asset is the forgery cost of our predicate.
- **VP DevRel** — *"The integrity that protects us and the experience that protects the implementer are the same thing."* Most-costly: **Q3 parent-nullability** — the only defect that structurally mandates forgery, turning honest developers into launderers on first run. Underweighted: "we declared v1 frozen" is a liability, not an asset.

## 10. Decisions (ratified, with minority bindings)

**D1 (Q1, 7-0) — Ratified hybrid + halt-on-conflict gate.** v0.8.0 `SkillVersion` lands the structural integrity fixes (D3/D4/D5); `status` / `signing_mode` / `rekor_log_index` + the `rekor_log_index`-iff-`production` invariant are **DEFERRED** until the authoring signing trust root is provisioned (DR-082 trigger 3). T1 governs sequencing; P0-RATIFY-2 governs eventual shape. This DR is a **Class-1 amendment to DR-028** reconciling line-105 with lines-233-236 verbatim. **Bindings:** deferred signing fields are pre-specified here and added verbatim later — *no third migration* (CSO/CTO); a dated re-open commitment ties to DR-082 trigger 3 (CISO); a CI gate asserts v0.8.0 must NOT carry signing fields (CTO). **Governance fix:** a standing kernel gate — any build agent detecting two contradictory ratified clauses on a one-way-door artifact MUST HALT and escalate, never silently resolve; the PR #57 silent resolution is logged here as a named governance defect.

**D2 (Q2, 7-0) — Amend `skill-refiner-pass/v1` in place.** URI string unchanged; corrected before the freeze. **DOCTRINE (binding on all staging-first predicates):** "frozen" attaches at the **first production-Rekor signature**, not at ratification; amend-in-place is permitted ONLY while `signing_mode=ln` and zero production-Rekor entries exist; the first production signature is the irrevocable freeze, after which corrections require `/v2`. **Bindings:** the amendment ships as a DR-082 erratum carrying a verbatim body diff + an auditable "no production signature ever existed for the pre-amendment shape" attestation (GC/CISO).

**D3 (Q3, 7-0) — Content-hash chain + nullable parent.** `SkillVersion` adds self `content_hash` + `parent_content_hash`, with the hash alphabet **aligned to `SkillSnapshot.combined_sha`** (one alphabet platform-wide). `parent_version_id` is retained as a convenience pointer; `parent_content_hash` is the integrity anchor (CTO). The predicate's `parent_version_id` becomes **nullable** to match the entity, so a root attests without forging a parent; root emission is provably zero-forgery (null `parent_version_id` + null `parent_content_hash`) (DevRel/CISO). **Minimum at v0.8.0:** alphabet alignment + parent nullability + `parent_content_hash` present; full cycle/fork/orphan verification lands same-tag via the kernel hash util, or as a documented invariant with the verifier before any production signature (CFO/CSO/GC).

**D4 (Q4, 7-0) — Disambiguate snapshot hashes + canonical label.** Add a distinct `result_snapshot_hash` (post-edit output) to the predicate; `source_snapshot_hash` means **pre-edit input** consistently across entity + predicate (retain the name; do not rename both sides — CISO). Canonical staging `signing_mode` = **`sigstore_staging`** across all predicates; retire `ln` with a changelog alias and a canonical-label registry entry (CMO/GC).

**D5 (Q5, 7-0) — Three-layer enforcement + standing scoped gate.** Before v0.8.0, machine-enforce every signed cross-field invariant at all three layers (JSON-Schema `if/then` + Zod `superRefine` + Pydantic `model_validator`): (1) `accept ⇒ every named_dimension_delta.non_regressed = true`; (2) `version_kind ∈ {revert,restore} ⇒ parent_version_id ≠ null`; (3) Python optional-not-nullable parity (`tenant_id`, `cost_record_ref`, `replay_fidelity_level`, `signing_downgrade_reason`). Establish a **standing kernel CI gate** "no unenforced invariant on a signed row," scoped to predicate/entity schemas only (CFO/CISO/CSO). The `version_kind` open/closed-world posture is made explicit and the closed enum flagged as a `/v2`-widening risk (CTO DR-028 dissent). **Binding:** the gate may land warn-only for one tag only if v0.8.0 itself ships fully enforced (GC/CFO).

## 11. Implementation directives

1. **HOLD** intent-eval-lab PR #171 (SPEC.md + authoring signing-root) until D1–D5 land — merging it freezes the flawed v1.
2. **BLOCK** any `@intentsolutions/core` tag/publish until D1–D5 land; the next tag is `v0.8.0` carrying the corrections.
3. Land kernel fixes (D3/D4/D5) + the DR-082 erratum (D2) + the DR-028 amendment (D1) on feature branches → through the **newly-wired Gemini + CodeQL gate** (this is the first real test of that gate).
4. File child beads under the existing refiner/kernel epics; mirror via `bd-sync`. Add the two standing CI gates (D1 conflict-marker; D5 unenforced-invariant) to the kernel boundary suite.
5. Publish this DR via `/doc-filing` into `intent-eval-lab/000-docs/`.

## 12. Reusable pattern reference

Convened via `/exec-decision-council`. This session adds a reusable dynamic: a **corrective council triggered by an adversarial qualified-reviewer glance on already-merged-but-unpublished artifacts**, exploiting the fix-window before a tag/transparency-log signature makes the shape immutable. Session JSONL: `~/.claude/skills/exec-decision-council/sessions/2026-06-17-iep-kernel-onewaydoor-correction/`.

## 13. Acting head of board declaration

I, Claude, as Acting Head of Board (designated by Jeremy Longshore via CTO-mode delegation, 2026-06-17), ratify decisions D1–D5 as written. Minority bindings are absorbed into the majority, not dismissed. The verbatim seat positions and council memos are preserved in the session JSONL for future readers.

## 14. References

- DR-028 (Session 7): `intent-eval-lab/000-docs/028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md` (amended here re: T1 line 105 / P0-RATIFY-2 lines 233-236).
- DR-082: `intent-eval-lab/000-docs/082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md` (erratum here re: freeze-point doctrine + body shape).
- Glance input: code-reviewer + `martin-kleppmann-reviewer` + `rich-hickey-reviewer` adversarial second-look on PRs #56 / #57.
- Session provenance: `session.jsonl` in the session directory above.
