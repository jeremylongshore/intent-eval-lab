# 111 · AT · SPEC — Kernel version skew is by design: what the kernel-shadow detector may and may not check

**Date:** 2026-07-22
**Status:** NORMATIVE for the scope of `audit-harness`'s `kernel-shadow-check`. Restates and applies two already-ratified positions (DR-064, Blueprint B § 7.0.1); introduces no new binding.
**Bead:** "Course-correct the BBB dogfood work against ratified platform architecture" (umbrella workspace; child of the epic "Dogfood the Intent Eval Platform against Bob's Big Brain")
**Refs:** `jeremylongshore/intent-audit-harness#133` (withdrawn), `intent-audit-harness#134` (the false-positive fix that replaced it)
**Related docs:** 012 (Blueprint B § 7.0, § 7.0.1, § 7.2), 064 (predicate compatibility policy), 018 (ISEDC Session 5 — redirect-stub α-minus)

---

## 1. Why this document exists

On 2026-07-22 a PR was opened against `audit-harness` that extended `kernel-shadow-check` with a second detection class: flag any repo whose `@intentsolutions/core` range **cannot resolve to the current kernel**. It was tested, offline-deterministic, and wrong. Run estate-wide it flagged six repos, every one of them operating exactly as the platform's ratified architecture intends.

The idea is intuitive enough that someone will have it again. This document is the record of why it was rejected, so it is not re-derived and re-built.

## 2. The ratified position

### 2.1 Consumers are entitled to lag (DR-064 rule (a))

DR-064 § 3 rule (a) FORWARD compatibility, line 43:

> _"This is the load-bearing rule for incremental kernel releases: `@intentsolutions/core` minor bumps add optional predicate-body fields (Blueprint B § 7.2 already commits the kernel schema to backward-compatibility across minor revisions); FORWARD compatibility is the consumer-side guarantee that makes those additions safe."_

The guarantee is directional and deliberate: a `vN` consumer reads a `v(N+1)` row, ignoring what it does not recognise. That guarantee exists _precisely so that a consumer does not have to be current._

### 2.2 Forcing consumers current is the named anti-goal (Blueprint B § 7.0.1)

Blueprint B § 7.0.1, closing paragraph ("Why this is binding"):

> _"Without an explicit expand-contract discipline, every kernel field addition degrades into a coordinated cross-repo deploy event — **the exact failure mode that independent package versioning exists to prevent.** Parallel Change makes additive schema evolution a sequence of independently-shippable steps, so **a kernel MINOR never forces a same-day deploy** of `audit-harness`, `j-rig-skill-binary-eval`, `intent-rollout-gate`, and the lab simultaneously."_

A CI gate that fails a repo for not resolving to `latest` re-imposes, by automation, the coordinated-deploy event the architecture was built to avoid. It converts a MINOR release into estate-wide red CI.

**Therefore: kernel version skew is a conformant state, not drift.** A repo pinned to `^0.1.1` while the kernel is at `0.10.0` is exercising a guarantee the platform ratified, not accumulating debt.

## 3. Out of bounds: currency checks

A gate MUST NOT fail, warn, or otherwise flag a repo on the grounds that its `@intentsolutions/core` range does not admit the newest published kernel. This holds at every severity — advisory included. An advisory that fires on correct configuration is not harmless; it trains readers to discard the lane, which costs the true positives too.

This bounds `kernel-shadow-check` specifically, and any successor gate that asks "which kernel version does this repo pin?"

Two corollaries:

- **A stale pin is hygiene, not an incident.** Bumping a lagging range is a fine thing to do in an ordinary PR. Framing it as remediation of a live hazard misstates the architecture and inflates the change.
- **A repo may lag indefinitely** so long as it reads rows per DR-064 rules (a)–(c). The floor is DR-064 rule (d): a `vN` predicate URI stays supported at least three years after `v(N+1)` first publishes. That is a _predicate URI_ clock, not a package-version clock.

## 4. In bounds: what the detector is for

`kernel-shadow-check` is a **consumer-side re-declaration detector**. Its subject is _"does this repo define its own copy of a kernel-owned contract?"_ — a supply-chain question about authorship, orthogonal to version. It has two classes:

1. A JSON Schema document claiming a kernel-owned canonical `$id` (`gate-result/*`, `evidence-bundle/*` under `evals.intentsolutions.io`).
2. A TS/Python source **declaring** a `GateResultV1` / `EvidenceBundle` / `EvidenceBundlePayload` type, interface, or class.

Class 2 must key on **declaration syntax**, not on the keyword. `export { type EvidenceBundle } from "@intentsolutions/core/…"` carries the keyword and is the _correct_ pattern — a re-export forwards the kernel's own type. Detecting the keyword alone flagged three `j-rig-skill-binary-eval` files for doing the right thing (`intent-audit-harness#134`).

Class 1 must exempt documents carrying an `x-redirect` marker: the ratified discoverability stub per Blueprint B § 7.0 and ISEDC Session 5 DR-018 § 6.4 Option α-minus, which claims the kernel `$id` in order to `$ref` the kernel's schema. The lab's own `schema-drift.yml` already allowlists that marker.

**The detector is for consumers.** Running it inside `intent-eval-core` flags the kernel for being the kernel — a category error. Any propagation of this gate excludes the kernel repo.

## 5. The legitimate version of the currency idea

There _is_ a real check in this neighbourhood, and Blueprint B § 7.0.1 phase 2 (Age) already specifies it:

> _"During the aging window the kernel MAY emit a **deprecation warning** against the still-optional shape (rows that omit the field, or producers pinned to the pre-field kernel) so that operators see, at producer time, that the field is migrating from optional to required. The deprecation warning is advisory and MUST NOT fail validation while the field is still optional."_

Note every constraint that distinguishes it from a currency gate:

| Property  | § 7.0.1 deprecation warning                            | The withdrawn currency check |
| --------- | ------------------------------------------------------ | ---------------------------- |
| Who emits | the **kernel**                                         | any repo's CI                |
| When      | **producer time** (emitting a row)                     | on every PR, statically      |
| Scope     | one **specific field** mid-optional→required migration | the whole package range      |
| Trigger   | that field is aging toward required                    | the range is not `latest`    |
| Severity  | advisory, MUST NOT fail validation                     | proposed as gateable         |
| Ends when | the field is promoted (Contract phase)                 | never                        |

It is tied to the deprecation registry and to a field actually in migration. Building it is a kernel work item, not a harness one, and it is not currently scheduled. Anything broader than that shape is a Class-1 architectural change and goes through ISEDC — a PR does not get to contradict a ratified DR on its own.

## 6. Empirical note

The severity story behind the withdrawn PR — that a lagging pin leaves a consumer validating against a superseded contract — did not survive checking:

| Check                                                       | Result                                             |
| ----------------------------------------------------------- | -------------------------------------------------- |
| `0.9.0` → `0.10.0` validator exports                        | 164 → 165, purely additive                         |
| `EvidenceBundleSchema` required fields, `0.1.1` vs `0.10.0` | identical                                          |
| Does `0.1.1` export `EvidenceBundleSchema`?                 | yes — a consumer's fail-open path was never firing |
| `bobs-big-brain-compiler` bundles under kernel `0.10.0`     | 17/17 pre-existing tests pass unchanged            |

This is what § 7.0.1 working looks like from the consumer side: nine minor versions of skew, zero observable difference in the contract being validated. The absence of harm is the evidence that the discipline is holding, not evidence that nobody checked.

## 7. What this document does not say

- It does **not** say pins should never be bumped. Keeping current is good practice and a fine PR.
- It does **not** license unbounded skew across a **major** URI version. § 7.2 governs breaking changes; DR-064 rule (d) sets the three-year support floor.
- It does **not** weaken `kernel-shadow-check`. Re-declaration remains detected, and `--strict` still gates it; `intent-audit-harness#134` narrows the pattern to real declarations and adds the detector's first 27 tests.
