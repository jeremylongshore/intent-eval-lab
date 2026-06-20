# 089 — Port-not-delete playbook: porting SAK artifacts upstream when a leading-indicator STOP fires (AT-SPEC)

**Status:** NORMATIVE · **Date:** 2026-06-20 · **Authority:** 033-PP-PLAN § 14.14 (the T2 port-not-delete resolution; the inventory + trigger-to-port skeleton this doc operationalizes), 063-AT-SPEC (the 12-indicator leading-indicator watcher whose `STOP` verdict is this playbook's sole trigger), 044-AT-DECR / 081-AT-DECR (the ISEDC Class-1 SAK charter that the re-charter step routes through), 046-AT-STND (the seat-bound governance owners who execute the port) · **Bead:** `bd_000-projects-chje` (iec-E11-port-not-delete-playbook) under epic `bd_000-projects-9k5h` (GH intent-eval-lab#114) · **Closes:** audit T2 (Karpathy–Huyen–Kleppmann resolution)

The operator runbook for the **bitter-lesson off-ramp**. The leading-indicator watcher (063-AT-SPEC) exists to make one moment observable: the moment Anthropic or the upstream ecosystem ships something that signals the Spec Authority Kernel (SAK) should stop investing and cut over to upstream. When that watcher's disposition matrix fires `STOP`, the SAK is wound down — but its hand-engineered investment (the IS 8-field marketplace policy, the 6767-h coverage map, the predicate co-location idioms, the shadow-mode rollback discipline) is **ported upstream as pull requests, not deleted.** This document is the step-by-step playbook for executing that port: what to port, where each artifact goes upstream, the PR-not-delete discipline that governs the wind-down, and the ISEDC checklist that gates it.

This spec **operationalizes** plan 033 § 14.14. Where this document and § 14.14.1's inventory table disagree, § 14.14 wins (it is the ratified T2 resolution); this document expands its four rows into an operator-executable runbook and never re-decides the policy. Terms used here — SAK, predicate URI, kernel, coverage map, Evidence Bundle — are defined in the Canonical Glossary (`014-DR-GLOS`); this spec does not redefine them.

## 1. Why port-not-delete (the T2 rationale)

Rich Sutton's bitter lesson (063-AT-SPEC § "Why"): general methods that scale with compute eventually beat hand-engineered structure. The SAK **is** hand-engineered structure — curated authoring schemas plus an IS-marketplace policy floor. If a frontier model can derive a schema-validator's verdicts from prose-plus-examples, or if Anthropic ships first-party machine-readable spec authority, then continuing to invest in the SAK is paddling against the current.

The audit's T2 tension (033-PP-PLAN § 14.14, line 603) was Karpathy's bitter-lesson concern ("don't sink months into structure the model will subsume") versus Huyen's and Kleppmann's invest-and-ship pragmatism ("the structure has real value today; shipping it is not waste"). The resolution **honors both**: structure the SAK so that if a leading indicator fires, the discipline — governance owners, the consistency model, the snapshot rules — **ports to the upstream-canonical world rather than getting deleted.** The investment transfers; it does not evaporate. A STOP is then not a failure mode but a graduation: the IS-specific learnings become upstream contributions, and the corpus migrates to a canonical authority IS no longer has to maintain.

This is why a STOP is the **only** event that triggers this playbook — and why the playbook's deliverables are upstream PRs, not `git rm`.

## 2. The single trigger: a STOP verdict from the leading-indicator watcher

This playbook fires on exactly one condition: the leading-indicator watcher (063-AT-SPEC) emits a `STOP` verdict. Per the 063 disposition matrix (§ 14.11.2), `STOP` requires **2 CRITICAL indicators firing** — the two CRITICAL indicators being:

- **#5** — Anthropic publishes machine-readable agentskills.io v2 schemas (`github-release` source kind), and
- **#12** — a frontier model demonstrates schema-validator equivalence from prose-plus-examples (`github-release` source kind; the bitter-lesson indicator by name).

No lesser verdict triggers this playbook. For reference, the full ladder from 063 § 14.11.2:

| Indicators firing    | Verdict    | This playbook?                                                       |
| -------------------- | ---------- | -------------------------------------------------------------------- |
| 0–2 Low-severity     | `CONTINUE` | No — continue per plan                                               |
| 1 Medium             | `NOTE`     | No — note in next AAR                                                |
| 2–3 Medium OR 1 High | `RETRO`    | No — ISEDC Class-2 retrospective; consider pausing Phase ≥ 3         |
| 1 CRITICAL           | `PAUSE`    | No — **but** ISEDC Class-1 re-charter to _evaluate_ upstream cutover |
| 2 CRITICAL           | `STOP`     | **YES** — execute this playbook                                      |

**A `PAUSE` is a dress rehearsal, not a trigger.** On `PAUSE` (1 CRITICAL), the ISEDC Class-1 re-charter convenes to _evaluate_ cutover but does not execute the port; the SAK is frozen, not wound down. Only when the second CRITICAL indicator fires — escalating `PAUSE` → `STOP` — does this playbook execute. The re-charter machinery is the same in both cases (§ 5); the difference is the decision the council reaches.

The watcher's typed-fetch-failure posture (063-AT-SPEC § "Deterministic detection") is load-bearing here: **a fetch failure is never a hit.** A STOP can only be reached from clean `FETCH_OK` evidence on both CRITICAL indicators, so this playbook can never be triggered by an unreachable, moved, rate-limited, or shape-changed upstream surface masquerading as an Anthropic signal.

## 3. The port-not-delete inventory (operationalized from 033 § 14.14.1)

When a STOP fires, the following SAK artifacts have port targets in the upstream world. The first four rows expand § 14.14.1's inventory table directly; the row order and port mechanisms are the ratified ones — this column set adds the **source-of-truth path** (where the artifact lives today) and the **port owner** (the seat from 046-AT-STND who drives the PR) so the runbook is executable without re-deriving either.

| #   | SAK artifact                                                                                                                                                                    | Source-of-truth path (today)                                                                                                                                                                            | Port target (upstream)                     | Port mechanism                                                                                                                                                                                                                             | Port owner (046-AT-STND)                                 |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| 1   | **IS 8-field marketplace policy** — `$defs.isMarketplace.requiredFields` (the `{name, description, allowed-tools, version, author, license, compatibility, tags}` required-set) | kernel `intent-eval-core` `schemas/authoring/v1/` `is-overlay/`                                                                                                                                         | Upstream agentskills.io v2 enforcement     | File an issue at agentskills.io; submit a PR codifying the IS extras (`version, author, license, compatibility, tags`) as agentskills.io **OPTIONAL** fields — not as required, so the upstream floor is not raised on the whole ecosystem | CTO + CISO (the `requiredFields` veto-holders)           |
| 2   | **6767-h coverage map** — the derived projection of the append-only lineage log mapping each IS-only extension to its upstream surface                                          | kernel `intent-eval-core` `schemas/authoring/v1/6767h-coverage-map.json` (derived from `specs/lineage/coverage-map.json` per 054-AT-SPEC); 6767-h prose in `claude-code-plugins` `000-docs/6767-h-*.md` | Upstream agentskills.io spec sections      | Submit each IS-only extension as a **"vendor-namespaced metadata"** pattern PR against the agentskills.io spec — one PR per extension, each citing the coverage-map row as the rationale                                                   | CTO (schema evolution)                                   |
| 3   | **Predicate co-location in `$comment`** + the **4-fold `$defs` composition** idiom (the base + 3 universal folds + is-overlay `allOf` structure)                                | kernel `schemas/authoring/v1/skill-frontmatter.schema.json` and siblings                                                                                                                                | Upstream JSON Schema community pattern     | Document each as a public idiom; submit to the JSON Schema Specification community (the two share one mechanism per § 14.14.1)                                                                                                             | CTO                                                      |
| 4   | **Shadow-mode + state machine + rollback protocol** — the advisory→canonical flip discipline (DR-049 flip gates) and the shadow-mode validation lane                            | `claude-code-plugins` validator + `kernel-vendor-hash.yml` consistency machinery                                                                                                                        | Upstream `validate-plugins.yml` equivalent | Contribute as a PR to whatever upstream validator becomes canonical after the STOP — porting the rollback protocol and the bounded-staleness consistency model wholesale                                                                   | CISO (co-signs the Phase 4c flip; owns `securityChecks`) |
| 5   | **Governance triple (CTO + CISO + VP DevRel)**                                                                                                                                  | 046-AT-STND-sak-governance-owners.md                                                                                                                                                                    | **Internal-only — port not applicable**    | Retain as IS internal discipline regardless of the SAK's fate (the seat-bound ownership map outlives the kernel)                                                                                                                           | — (no port; retained)                                    |

**Predicate URIs are a special case (§ 4).** The leading-indicator inventory in § 14.14.1 does not list the SAK's minted predicate URIs because they are **one-way-door immutable artifacts** — they are governed by the supersession protocol, not ported by a PR. They get their own section below.

## 4. Predicate URIs: supersede, never port-by-deletion

The SAK's authoring chamber mints two predicate URIs, both flat siblings on the `evals.intentsolutions.io` host (per the DR-082 / 086-AT-DECR ratified grammar `evals.intentsolutions.io/<predicate-type>/v<version>`, one segment, no chamber token):

- `https://evals.intentsolutions.io/gate-result/v1` — the deterministic-gate verdict predicate (Blueprint B § 7 normative body).
- `https://evals.intentsolutions.io/skill-refiner-pass/v1` — the Skill Refiner behavioral-pass attestation (082-AT-DECR; freeze-point doctrine per 086-AT-DECR).

These are **immutable once a row hits the production Rekor transparency log.** A predicate URI cannot be "ported" by re-pointing or deletion — walking one back means a predicate-version migration plus every downstream verifier reconfiguring its `predicateType` allowlist (082-AT-DECR § "Why this is Class-1"). On a STOP, the discipline is therefore:

1. **Do not delete or re-mint.** Already-signed `gate-result/v1` and `skill-refiner-pass/v1` Statements stay valid forever; the transparency log is append-only and the URIs keep resolving. Tearing down `evals.intentsolutions.io` or 404-ing the predicate schema would strand every historical attestation — the opposite of port-not-delete.
2. **Supersede, do not retract.** If a STOP means IS stops _producing_ new Statements under these URIs, that is recorded via the **Rekor superseding-event protocol** (065-AT-SPEC) — a signed supersession event, not a deletion. The URI's identity and every historical row are preserved; only the production trigger goes quiet.
3. **Offer the predicate _shape_ upstream, not the URI string.** What ports is the **idea** — "a signed `this gate passed` / `this skill provably got better` attestation shape" — submitted as a predicate-type proposal to the canonical upstream registry (e.g., an in-toto / SLSA predicate-type contribution). The IS-host URI string itself never moves; it remains a permanent, resolvable historical identity under IS control. This is the predicate-layer expression of port-not-delete: the _pattern_ graduates upstream; the _artifact_ stays immutable.

This row is deliberately **absent** from § 14.14.1's port table precisely because its mechanism is supersession (065-AT-SPEC), not a PR. Listing it under "port as a PR" would have invited exactly the one-way-door violation 085-AT-DECR and 087-AT-STND exist to prevent.

## 5. Trigger-to-port playbook (the runbook)

When the leading-indicator watcher fires `STOP` (063-AT-SPEC § "Side effects" opens a deduped `[leading-indicator]` GH issue carrying the `STOP` verdict — that issue is this runbook's entry point), execute the following in order. Steps 1–4 expand 033 § 14.14.2; steps 0 and 5–7 add the pre-conditions and the post-conditions the operator needs.

0. **Confirm the STOP is real (not a flake).** Verify the GH issue's verdict was reached from two `FETCH_OK` CRITICAL indicators (063-AT-SPEC § "Flake budget" — structured sources escalate immediately and have no flake surface; the two prose sources are not CRITICAL, so a STOP is never prose-driven). If either CRITICAL hit was actually a typed fetch-failure (`UNREACHABLE | MOVED | RATELIMITED | SHAPE_CHANGED`), it is **not** a hit and there is no STOP — close the issue and continue per plan. Do not proceed past this step on a degraded fetch.

1. **Convene the ISEDC Class-1 re-charter** (per 063-AT-SPEC § 14.11.2 `STOP` action and 081-AT-DECR / 044-AT-DECR — the SAK is a Class-1 immutable-artifact concern, so its wind-down is a Class-1 council decision). The council ratifies (a) that the STOP is accepted (not a transient signal to wait out), and (b) the port scope — which inventory rows in § 3 are ported, in what order. The re-charter follows the ISEDC checklist in § 6.

2. **Port each inventory artifact with a port target.** For each row in § 3 that has a port target (rows 1–4; row 5 is internal-retain), the **port owner** opens the upstream PR per that row's **port mechanism**. The discipline is **PR-not-delete**: the upstream PR is opened _before_ any SAK artifact is removed locally, and the artifact is not deleted until its port is either merged or definitively declined upstream (§ 5.1).

3. **Track upstream PR status.** Record every port PR's state in the `SAK-DASHBOARD.md` **"port progress"** section (the auto-generated dashboard, bead `iel-sak-dashboard`). A STOP that opened port PRs but lost track of them is a half-executed port; the dashboard section is the canonical wind-down status surface.

4. **Migrate the corpus to upstream-canonical.** Once the port PRs are merged (or the council accepts a port as declined-but-documented), the CCP validator and the authoring corpus migrate to the now-canonical upstream authority. The `gate-result/v1` and `skill-refiner-pass/v1` Statements already signed are preserved (§ 4); new validation runs read from upstream.

5. **Supersede the predicate-production triggers** (§ 4). Emit the signed supersession event(s) per 065-AT-SPEC for any predicate URI whose production trigger is going quiet. Do not delete the URIs or their schemas.

6. **Archive the SAK as a historical contribution.** Mark the SAK docs (this 089, 063, 054, 045, the SAK-INDEX) as `ARCHIVED — historical contribution` per the state-labeling standard (069-DR-STND). Archiving ≠ deletion: the docs stay in `000-docs/` as the durable record of what was ported and why. Update `SAK-INDEX.md` Status line to `ARCHIVED — ported upstream (see 089 § 3 port table)`.

7. **Write the wind-down AAR.** File an `AA-AACR` after-action record capturing the STOP trigger evidence, the port-PR outcomes (merged / declined-documented), and the final corpus-migration state. This closes the loop the leading-indicator watcher opened.

### 5.1 PR-not-delete discipline (the load-bearing rule)

The single rule that makes this "port-not-delete" rather than "delete-and-hope": **no SAK artifact is removed from the codebase until its upstream port is resolved.** Concretely:

- An artifact with a **merged** port PR may be removed locally (the canonical authority is now upstream) — or, preferably, left in place and re-pointed to the upstream source via a redirect stub, mirroring the lab-schema-repoint precedent (the kernel-shadow `$ref` + `x-redirect` pattern).
- An artifact whose port PR is **declined upstream** is **retained as IS internal discipline** and the decline is documented in the wind-down AAR. A declined port is not a deleted artifact — it means upstream chose not to absorb the pattern, so the IS-internal version remains the home for it. This is the same disposition as row 5 (the governance triple): retain-internal.
- An artifact with an **open, unresolved** port PR is **never deleted.** Deleting it would strand the very investment the port exists to transfer.

The discipline is asymmetric on purpose: the cost of keeping a ported artifact around an extra release is trivial; the cost of deleting an artifact whose port then gets declined is the permanent loss of the investment T2 exists to protect.

## 6. ISEDC re-charter checklist (the gate on step 1)

The Class-1 re-charter (step 1) is the human gate on the entire wind-down. It convenes the 7-seat ISEDC (CTO · GC · CMO · CFO · CSO · CISO · VP DevRel) per the SAK charter (081-AT-DECR / 044-AT-DECR) and answers, on the record, each of:

- [ ] **STOP acceptance** — is the 2-CRITICAL STOP a durable signal we cut over on, or a transient we wait out? (If wait-out, downgrade to a frozen-PAUSE posture and do not execute the port; record the re-evaluation trigger.)
- [ ] **Port scope** — which § 3 inventory rows are ported, in what order, and which are retained-internal? (CTO + CISO bind rows 1–2 per their `requiredFields` / `securityChecks` vetoes; CISO binds row 4.)
- [ ] **Predicate disposition** — confirm the supersession path (§ 4) for `gate-result/v1` and `skill-refiner-pass/v1`; **explicitly forbid** any deletion / re-mint / 404 of a minted predicate URI (one-way-door, 085-AT-DECR / 087-AT-STND). A re-charter that proposes walking back a production predicate URI MUST HALT per the ratified-clause-conflict halt gate (087-AT-STND).
- [ ] **Corpus-migration target** — which upstream authority does the CCP validator + corpus cut over to, and on what bounded-staleness schedule (the consistency model from 033 § 14.15 carries over to the upstream-canonical world)?
- [ ] **Governance retain** — confirm the governance triple (row 5) is retained as IS internal discipline regardless of the port outcomes.
- [ ] **AAR owner** — assign the seat who files the wind-down `AA-AACR` (step 7).

Each box is decided with verbatim seat positions preserved per the ISEDC adversarial-integrity protocol; the re-charter produces an `AT-DECR` Decision Record so a future reader can reconstruct why each port (or retain) landed where it did.

## 7. What this playbook is NOT

- **Not a delete script.** Its deliverables are upstream PRs and a supersession event, not `git rm`. The PR-not-delete discipline (§ 5.1) is the whole point.
- **Not triggered by anything below STOP.** A `PAUSE` (1 CRITICAL), `RETRO`, `NOTE`, or `CONTINUE` verdict does not execute this playbook (§ 2). `PAUSE` is the dress rehearsal that runs the same re-charter to _evaluate_, not execute.
- **Not a predicate-URI teardown.** Minted predicate URIs are immutable one-way doors (§ 4); they are superseded (065-AT-SPEC), never deleted. The re-charter HALTs on any clause proposing otherwise (087-AT-STND).
- **Not self-executing.** A STOP opens a GH issue; a human operator runs the runbook, gated by the ISEDC Class-1 re-charter. The watcher observes; the council decides; the owners port.

## Cross-references

- **063-AT-SPEC** (`063-AT-SPEC-leading-indicator-watcher-2026-06-12.md`) — the 12-indicator watcher; its `STOP` verdict is this playbook's sole trigger. § "Why" names this playbook as the STOP routing target (line 9).
- **033-PP-PLAN § 14.14** (`033-PP-PLAN-skill-refiner-sak-amendment-v7-2026-05-28.md`) — the T2 resolution this spec operationalizes: the port-not-delete inventory (§ 14.14.1) + trigger-to-port skeleton (§ 14.14.2) + the originating bead `iec-E11-port-not-delete-playbook`.
- **054-AT-SPEC** (`054-AT-SPEC-lineage-log-and-derived-coverage-map-2026-06-12.md`) — the append-only lineage log the 6767-h coverage map (inventory row 2) is a derived projection of.
- **045-RR-LAND** (`045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md`) — the SSoT declaration; the base + 3-fold + is-overlay composition idiom (inventory row 3) lives here.
- **046-AT-STND** (`046-AT-STND-sak-governance-owners.md`) — the seat-bound port owners (CTO / CISO / VP DevRel) referenced in the inventory and the re-charter checklist.
- **044-AT-DECR / 081-AT-DECR** — the ISEDC Class-1 SAK charter the re-charter (step 1) routes through.
- **082-AT-DECR / 086-AT-DECR** — the `skill-refiner-pass/v1` predicate URI mint + freeze-point doctrine (§ 4).
- **065-AT-SPEC** (`065-AT-SPEC-rekor-superseding-event-protocol-2026-06-12.md`) — the supersession protocol used for predicate-production wind-down (§ 4, step 5).
- **085-AT-DECR / 087-AT-STND** — the one-way-door correction + ratified-clause-conflict halt gate that forbid any predicate-URI teardown (§ 4, § 6).
- **069-DR-STND** (`069-DR-STND-state-labeling-standard-2026-06-18.md`) — the `ARCHIVED` state label applied at wind-down (step 6).
- **014-DR-GLOS** (`014-DR-GLOS-canonical-glossary.md`) — terminology source of truth; this spec does not redefine glossary terms.
