# Decision Record — `iah-E02` scope clarified and deferred to `iah-E04` (emit-evidence)

| Field          | Value                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------- |
| **Doc code**   | AT-DECR (Architectural / Technical Decision Record)                                      |
| **Number**     | 021                                                                                      |
| **Date**       | 2026-05-23                                                                               |
| **Author**     | Jeremy Longshore (acting head of board, per CEO-mode delegation)                         |
| **Status**     | Ratified — single-signer call (NOT an ISEDC session)                                     |
| **Supersedes** | `iah-E02` scope as written in IEP Convergence Debt Plan Priority 1                       |
| **Closes**     | `iah-E02` parent bead (`bd_000-projects-46x`) with reason "scope clarified by inventory" |
| **Plan**       | IEP Convergence Debt Plan Priority 1 (`iep-P1-kernel-adoption`), § Discovery 1           |

## 1. Decision

`iah-E02` ("Migrate audit-harness internal type definitions to import from `@intentsolutions/core`; remove duplicated type definitions") is **closed with no codemod work** and **its consumption scope is folded into `iah-E04` (the `emit-evidence` subcommand)**, which is the natural kernel-consumption surface for audit-harness.

Effective immediately:

- `iah-E02` parent bead (`bd_000-projects-46x`) and all 4 children (`iah-E02a/b/c/d` — `bd_000-projects-urxx/l1pq/5kp3/78p5`) are **closed with `--reason "deferred to iah-E04 per AT-DECR 021"`** (or superseded, see § 6).
- `iah-E02` is **removed from `iep-P1-kernel-adoption`'s dependency list** (this was already provisionally done 2026-05-21 pending this DR; this document ratifies the change).
- `iah-kernel-shadow-check` (`bd_000-projects-873c`, P0 standing safety rule) is **unblocked**: it scopes its grep-detector enforcement against the **actual** kernel surface materializing in `iah-E04`, not against the inventory's plan-recollection list (see § 4 of this DR for the touchpoint and § 5 of this DR for the plan-recollection corrections it must enforce against).
- `iep-P1-kernel-adoption` umbrella can now close on **3-of-4 children** (`iel-link-schemas-to-kernel` — DONE via PR #65 + lab cluster, `iaj-E02b` — pending shape-reconciliation per the **IEP Convergence Debt Plan § Discoveries, Discovery 2** (j-rig `EvalSpec` is a name-collision with kernel's `EvalSpec`, not a duplicate; needs shape-level comparison before any codemod), `iar-consumer-migration` — subsumed into Priority 4 M5 MVP). The audit-harness arm is **N/A**, not pending.

## 2. Inventory evidence (the decisive finding)

The kernel-shadow inventory `intent-eval-lab/000-docs/016-RR-LAND-kernel-shadow-inventory-2026-05-20.md` § 4.1 documents:

> **audit-harness production code: ZERO local kernel-canonical type re-definitions.** The Node CLI (`bin/audit-harness.js`) is a thin dispatcher; the deterministic scripts (`scripts/*.sh`, `scripts/*.py`) emit JSON envelopes that conform to `@intentsolutions/core/schemas/v1/gate-result.schema.json` **by hand-rolled JSON construction**, not by importing kernel TypeScript types. There is no `EvidenceBundle`, `EvalSpec`, `GateResultV1`, or any of the other 13 kernel entities defined locally in audit-harness. There are no Zod validators, no type re-exports, no shadow definitions.

The scripts speak Evidence Bundle by emitting JSON that **matches** the kernel's published JSON Schema — not by importing kernel's TypeScript types into the scripts. JSON-Schema conformance is verified empirically by the regression suite at `tests/regression/run-regression.sh` (CI job `backward-compat regression suite (v0.3.0+)`).

**A codemod task with nothing to mod is not a task.** `iah-E02` as originally written ("migrate type definitions") has no target.

## 3. Why options (b) and (c) are theater or out-of-scope

Three resolution paths were considered for `iah-E02` (per IEP Convergence Debt Plan § Discoveries):

| Option  | Action                                                                                           | Verdict                                                                    |
| ------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| **(a)** | Defer until `iah-E04` (emit-evidence) is ready — kernel consumption naturally materializes there | **✅ Ratified**                                                            |
| **(b)** | Add `@intentsolutions/core` as a `peerDependency` only — symbolic; no runtime cost               | ❌ Rejected — theater                                                      |
| **(c)** | Full TypeScript port of scripts so they can `import` from kernel                                 | ❌ Rejected — violates audit-harness Rule 1 with no concrete justification |

### Why (b) is theater

A `peerDependency` declaration without an `import` is a metadata claim that audit-harness _would consume kernel if it consumed anything from any package_. It does not change behavior. It does not produce a runtime tie-in. It does not let audit-harness validate against kernel-published Zod schemas (scripts can't `import` from npm-published TypeScript in any meaningful way — they're bash + python). It would be a marketing change to the manifest that creates the impression of consumption without the substance.

### Why (c) is out-of-scope for this DR

audit-harness's Rule 1 (from `audit-harness/CLAUDE.md` § "Core design rules"):

> **Scripts are the source of truth.** The Node CLI (`bin/audit-harness.js`) is a thin dispatcher. All logic lives in `scripts/*.sh` and `scripts/*.py`. Don't port to TypeScript unless there's a concrete reason (cross-platform Windows bug, etc.).

A full TS port would require:

1. Re-implementing 6 scripts (escape-scan, harness-hash, crap-score, emit-evidence, bias-count, gherkin-lint) in TypeScript while preserving their bash/python deterministic behavior.
2. Adding `@intentsolutions/core` as a runtime dependency — violates Rule 2 ("Zero runtime deps").
3. Justifying the change against Rule 1 — needs a concrete cross-platform or correctness reason that does NOT exist today.

The cost-benefit is asymmetric: large rewrite cost, zero behavioral benefit (audit-harness already emits JSON that conforms to kernel schemas). If a future correctness or cross-platform reason emerges (e.g., a Windows engineer needs to run audit-harness without WSL), that future DR can revisit. Today it would be invention without justification.

## 4. Where kernel consumption actually lives

`iah-E04` (emit-evidence subcommand) is the natural and only kernel-consumption surface for audit-harness:

- `audit-harness emit-evidence` wraps a gate-result JSON envelope in an in-toto Statement v1 with `predicateType` = `https://evals.intentsolutions.io/gate-result/v1`.
- The predicate body conforms structurally to kernel's `GateResultV1` predicate (`intent-eval-core/src/predicates/gate-result-v1.ts`).
- The cross-field invariants (`subject.name == predicate.gate_id`; `subject.digest.sha256 == predicate.input_hash[7:]`) are enforced inline in `scripts/emit-evidence.sh`'s python composer at lines 128–169 of the script (per v1.1.1 the line numbers may shift slightly).
- The schema conformance is verified empirically by `tests/regression/run-regression.sh` against the kernel-published schema (fetched from `intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/schema/` until M2; thereafter from `@intentsolutions/core/schemas/v1/gate-result.schema.json` per the lab schema-repoint AAR `019`).

When kernel ships v0.2.0 (per `iec-E12`, blocked on `iec-E12a` + `iec-E12b`), the `EvidenceBundlePayload` cross-field invariant additions land in kernel as Zod validators. audit-harness's `iah-E04` becomes the consumption tie-in: the emit-evidence python composer can either continue conforming by hand (current pattern) OR a separate `iah-E04` sub-bead can wire a Node-side pre-emit validation step that DOES import kernel's Zod validator. **That** is the architecturally honest place to do kernel consumption.

`iah-kernel-shadow-check` (the P0 standing safety rule) will scope its grep-detector against this same `iah-E04` touchpoint — checking for any local re-definition of `EvidenceBundle`, `GateResultV1`, `MatcherInputPattern`, `ScoringConfig`, etc., that would shadow the kernel-canonical version once it lands. Today the detector reports clean (zero shadows). After `iah-E04` lands the detector enforces.

## 5. Plan-recollection errors corrected

The IEP Convergence Debt Plan Priority 0 enumerated "the 11 canonical types" — that count and list were a plan-author recollection, not the actual kernel surface. The actual kernel surface per `intent-eval-core/src/entities/index.ts` is **13 entities + 1 predicate + 3 sub-types** (17 exports total). The plan listed three names (`EvalCase`, `Provider`, `JudgeAdapter`) that are **not** kernel exports. Any grep-detector or codemod that enforces against the plan list will produce false positives.

This DR re-anchors enforcement to `intent-eval-core/src/entities/index.ts` as the actual source of truth, not the plan text. The `iah-kernel-shadow-check` implementation MUST read the live kernel exports, not the plan's enumeration.

## 6. Bead lifecycle action items

1. **Close `iah-E02` parent** (`bd_000-projects-46x`) with reason: _"Scope clarified by 016-RR-LAND inventory — zero local kernel-canonical type re-defs in audit-harness production code. Consumption tie-in naturally materializes at iah-E04 emit-evidence subcommand. See AT-DECR 021."_
2. **Close `iah-E02a/b/c/d`** with the same reason (children of a closed-no-work parent).
3. **`iah-kernel-shadow-check`** (`bd_000-projects-873c`) — remove the blocker on `iah-E02` (was provisionally removed 2026-05-21). Re-scope acceptance criteria to: "grep-detector enforces against `intent-eval-core/src/entities/index.ts` live exports; today emits zero hits; after iah-E04 lands the detector becomes load-bearing."
4. **`iep-P1-kernel-adoption`** umbrella — update notes to reflect 3-of-4-children scope (audit-harness arm is N/A, not pending). Umbrella can close after j-rig shape-reconciliation (`iaj-E02b`) and `iar-consumer-migration` close (Priority 4 M5 MVP).
5. **No new bead filed** for the future `iah-E04` kernel-consumption tie-in — `iah-E04` already exists in the audit-harness bead workspace; its scope expands implicitly to include the kernel-consumption work when it's claimed.

## 7. Escalation path (if anyone disagrees)

This DR is a single-signer (acting-head-of-board) call. If a future maintainer or stakeholder believes audit-harness should consume kernel earlier than `iah-E04` (or via a different mechanism than emit-evidence-side consumption), escalation path:

1. File a new bead with the proposed alternative (option (c) full TS port; a Rust runtime layer; etc.) including a concrete justification per audit-harness Rule 1.
2. Convene ISEDC if the proposal ripples across consumers (it likely won't — audit-harness is a consumer of kernel, not consumed by other repos for type purposes).
3. Update this DR to "Superseded by AT-DECR NNN" if a future decision overrides it.

The bar for overturning this DR is: a **concrete reason** that meets Rule 1's "concrete reason" bar (cross-platform Windows bug; a security correctness issue requiring runtime type validation; etc.). Symbolic alignment with the rest of the ecosystem is not a concrete reason.

## 8. References

- **Inventory** (decisive evidence): `intent-eval-lab/000-docs/016-RR-LAND-kernel-shadow-inventory-2026-05-20.md` § 4.1
- **audit-harness design rules**: `intent-eval-platform/audit-harness/CLAUDE.md` § "Core design rules"
- **Kernel exports source of truth**: `intent-eval-platform/intent-eval-core/src/entities/index.ts` (13 entities) + `src/predicates/gate-result-v1.ts` (1 predicate) + sub-types in `EvalSpec.ts` / `MatcherMap.ts`
- **Plan section**: IEP Convergence Debt Plan § Discoveries during partial execution (2026-05-21 architecture review), Discovery 1
- **Parent bead**: `iah-E02` (`bd_000-projects-46x`)
- **Beneficiary bead**: `iah-E04` (existing; scope expands implicitly)
- **Unblocked**: `iah-kernel-shadow-check` (`bd_000-projects-873c`), `iep-P1-kernel-adoption` (`bd_000-projects-6hd6`)

— end DR —
