# Plan Audit Findings — Martin Kleppmann seat

**Plan under audit:** `027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md` (v4.1)
**Reviewer persona:** Martin Kleppmann (DDIA; local-first software; CRDTs and causality)
**Primary axes:** (b) RISK — distributed-data failure modes; (c) RISK MITIGATION — risks named but hand-waved
**Severity rubric:** P0 BLOCKER / P1 CRITICAL / P2 MAJOR / P3 MINOR / NIT
**Date:** 2026-05-27

---

This is a distributed-data plan. It has an append-only log, a content-addressed store, a mutable pointer, lineage records spanning multiple writer/reader systems, and a permanent transparency log as a downstream durability tier. The plan does not, anywhere in v4.1, state a consistency model. The findings below are the ones a DDIA reader would raise on first pass.

---

## F-MK-1 — Rollback breaks append-only causality; the lineage graph silently re-roots

**Severity:** P0 BLOCKER
**Axis:** (c) RISK MITIGATION — risk named but hand-waved

**Plan text invoked.** AC-2: _"Append-only event log; never in-place SKILL.md mutation (Hickey-aligned). Each accepted edit produces a content-addressed `SkillVersion` value; 'current best' is a separate mutable pointer."_ Phase F § 9 item 8 lists _"first rollback incident"_ as a Phase F trigger. The plan's response to a prior rollback concern (line 1446-1447) is: _"rollback is a new SkillVersion record citing the prior."_

**Kleppmann position invoked.** DDIA ch. 5 (replication) + ch. 11 (stream processing): in an append-only log with content-addressed values and a mutable "current" pointer, the log is the source of truth and the pointer is a derived projection. A rollback is therefore _not_ a new record that mutates history — it is a new record whose `parent_version_id` points at an ancestor of the version being rolled back from. The plan does not say which.

**What the plan actually specifies.** § 4 Phase C `SkillVersion` schema has exactly one parent pointer: `"parent_version_id": "uuidv7 | null"`. Reading line 1446-1447 in the only way the schema permits, a rollback record's `parent_version_id` would point at the version being rolled back _from_ (the bad version that's currently "best"). That is observationally indistinguishable from "I made a new edit on top of the bad version that happens to look identical to its grandparent." The lineage graph cannot represent the operation `revert(v_bad) → v_good_again` because there is no `revert_of` / `restores` / `supersedes` edge type and no semantic difference between "I deleted bad-edit and restored prior" and "I added new content that happens to coincide with prior."

**Why this embarrasses Kleppmann to leave unflagged.** Operational transformation and CRDT literature has spent 20 years on exactly this issue: in an append-only model, a delete is a write, and a revert is a different kind of write. Conflating the two means the system cannot answer the question that any auditor of a signed evidence chain will ask first — "Did the human revert the previous edit, or did they make a new edit?" The signed `skill-refiner-pass/v1` row carries `actor: <human|claude>` but not `intent: <new-edit|revert|restore>`, so the Rekor-anchored audit trail cannot tell those operations apart after the fact.

**Mitigation must specify (not optional).**

1. Add a discriminated `version_kind: "edit" | "revert" | "restore"` field to `SkillVersion`.
2. For `revert`, require a second pointer field `reverts_version_id`; for `restore`, require `restores_to_version_id`. Both in addition to `parent_version_id`, which always points at the _immediate_ lineage ancestor (so the append-only log property is preserved structurally).
3. Update D5 (SkillVersion ER diagram) to draw the second edge type explicitly. Right now D5 shows exactly one `parent_hash (FK)` arrow.
4. Add a cross-field invariant to the kernel: `version_kind="revert" ⊢ reverts_version_id IS NOT NULL ∧ reverts_version_id ∈ ancestors(parent_version_id)`. Pair this with the existing CISO invariant filed as `bd_000-projects-1is2`.
5. State the inversion in plain language in AC-2: "rollback is a new SkillVersion record whose `version_kind='revert'` and which cites _both_ its lineage parent AND the version it reverts." Hickey alignment is preserved; the schema becomes capable of representing the operation.

Without this, AC-2's "append-only" claim is technically true and semantically empty — the log can be replayed but the resulting projection cannot reconstruct human intent.

---

## F-MK-2 — Sigstore Rekor unavailability has no defined Refiner behavior; the plan treats a remote third-party service as a local invariant

**Severity:** P0 BLOCKER
**Axis:** (b) RISK — failure mode not named

**Plan text invoked.** § 4 Phase C `SkillVersion` schema field `"rekor_log_index": "int64 | null"` paired with the CISO invariant _"`rekor_log_index` non-null iff `signing_mode='production'`"_ (line 450). § 4 Phase E.3 storage spec: _"Rekor log entry | Public sigstore Rekor | Permanent (by design — one-way door)"_ (line 584). § 8 risks table does not mention Rekor at all. AC-9 (line 192): _"Single-signer audit trail (ISEDC pattern). Refiner proposes; human + acting CTO disposes."_

**Kleppmann position invoked.** DDIA ch. 8 (unreliable networks) + ch. 9 (consistency): a system that synchronously requires a third-party network service to make local progress is not an append-only log — it is a synchronously-replicated distributed log with an SLA dependency that the operator does not control. Local-first software thesis (Kleppmann et al., 2019): the seven ideals require _no spinners_ — the user's work must not block on a remote service being reachable.

**What the plan actually specifies.** The Refiner's L3 Hook fires on `git commit | git push` (Phase B § 4 hook table). Phase C signs a `skill-refiner-pass/v1` row to _production_ Rekor as part of Phase C exit criteria (line 1254). The cross-field invariant says you cannot have `signing_mode='production'` without `rekor_log_index` non-null. What the plan does not say:

- **What happens when Rekor is down at L3 commit time?** Does the commit block? Fail open? Fall back to staging? Queue locally and retry?
- **What is the consistency contract between the SkillVersion landing on disk (local append-only log) and the Rekor entry landing on rekor.sigstage.dev (remote append-only log)?** These are two append-only logs that need to be eventually consistent, and the plan never says "eventually consistent" — it just assumes Rekor is durable like a local file.
- **What if the commit succeeds, the SkillVersion is written, and the Rekor write fails?** Now the local store has a `signing_mode='production'` row with `rekor_log_index=null`, which violates the CISO invariant filed as `bd_000-projects-1is2`. The system is in an unrepresentable state.
- **What is the offline-mode behavior?** A user on an airplane refining a skill in `claude-code-plugins` cannot reach Rekor. Does the Refiner refuse to run? Run with `signing_mode='staging'` and silently downgrade? The plan does not say.

**Why this embarrasses Kleppmann to leave unflagged.** Rekor outages are not hypothetical. The transparency log has had degraded windows. A plan that mints `evals.intentsolutions.io/skill-refiner-pass/v1` as a _production_ predicate URI (Phase C exit criterion 5, line 1254) and writes signed bundles synchronously to that URI's Rekor instance, with no degraded-mode story, is a plan that will discover its consistency model the first time AWS us-east-1 has a bad afternoon.

**Mitigation must specify (not optional).**

1. **Define the writer's local invariant before the remote write.** The SkillVersion record's `signing_mode` field must be writable as `pending_production` for the window between local commit and Rekor confirmation. The CISO invariant becomes: `signing_mode ∈ {staging, pending_production, production}; rekor_log_index NOT NULL iff signing_mode = production`. The `pending_production` state is the local-first state; a background reconciler closes the gap.
2. **Define the offline-mode contract.** When Rekor is unreachable, the Refiner SHALL: (a) complete the acceptance gate locally; (b) write the SkillVersion record with `signing_mode='pending_production'`; (c) queue the Rekor write to a local outbox; (d) NOT block the user's `git commit` / `git push`. The reconciler retries with exponential backoff. This is the same outbox pattern DDIA ch. 11 specifies for any local-to-remote durable handoff.
3. **State the eventual-consistency contract.** "A SkillVersion record with `signing_mode='pending_production'` MUST reach `production` within N hours OR be downgraded to `staging` with an operator-acknowledged Decision Record." Pick N. Without a deadline, the queue grows unboundedly under sustained Rekor unavailability.
4. **Add a new Phase E E.3 row.** Rekor _as the durability tier the plan claims it is_ is permanent only IF reached. The plan currently treats the unreached state as nonexistent. Add: "Pending-Rekor outbox | local jsonl at `.j-rig/refiner/outbox/` | drained on next reconciler tick; retained on disk until confirmed."
5. **Add a risk row to § 8.** Currently § 8 has no Rekor row at all. This is the most-cited failure mode for any sigstore-anchored system in the last 18 months of operational reports.

The plan claims (E.3) that Rekor is _"Permanent (by design — one-way door)"_. That is true of the data once it lands. It is not true of the write path.

---

## F-MK-3 — AC-12 tri-link spans three writer systems (bd + GH + Plane) with no consistency model

**Severity:** P0 BLOCKER
**Axis:** (b) RISK — failure mode not named; (c) RISK MITIGATION — risk named but hand-waved

**Plan text invoked.** AC-12 (line 195): _"NEW AC-12: tri-linkage discipline. Every Refiner doc cites driving beads + GH issues; every Refiner bead description ends with `Doc:` + `GitHub:` lines; every Refiner GH issue body ends with `Bead:` + `Doc:` lines. CI-verified."_ § 3.5 PR-1 elaborates the format. § 5.5 introduces `validate-trilink.sh` as the _"tri-linkage verifier"_. § 8 (risks) row: _"per-repo bead clusters require label discipline that's easy to forget | § 5.5 `validate-trilink.sh` runs in CI; bd-sync extension enforces at link-time; beads-guru agent at `~/.claude/agents/beads-guru.md` is the authoritative reference for any human in doubt."_

**Kleppmann position invoked.** DDIA ch. 9 (linearizability, consistency, and consensus) + the local-first paper § 3 (collaboration without a server). Three systems that each independently accept writes (bd workspace; GitHub Issues; Plane) and that each carry pointers to the other two are a three-way replicated dataset. Any three-way replicated dataset has exactly one of three possible consistency stories: (1) strong consistency via consensus, (2) eventual consistency with a conflict-resolution rule (last-write-wins, CRDT merge, operational transformation), or (3) the operator manually reconciles divergence. The plan implements (3) without admitting it.

**What the plan actually specifies.** A bash script (`validate-trilink.sh`) that reads each layer and reports missing back-references. That is a _drift detector_. It is not a _consistency model_. Specifically the plan does not say:

- **What is the source of truth when the three layers disagree?** The umbrella `CLAUDE.md` § "Convergence work — source-of-truth hierarchy" lists bd as Tier 1, which is excellent — but the plan never cites that hierarchy in AC-12 or PR-1. Inside the plan, all three layers are equal.
- **What is the write-order requirement?** PR-3 sequential execution discipline says "beads first, then GH issues, then validate" — that is a write-order. But the plan does not say what happens when a write to layer 2 (GH) fails after layer 1 (bd) succeeded. Now bd has a record pointing at a GH issue that does not exist.
- **What happens when GH/Plane comments are created out-of-band** (by Gemini bot, by partners, by other team members not running `bd-sync`)? The plan's PR-1 says these "must be mirrored back via `bd-sync note <bead>`," but that is enforcement-by-policy, not enforcement-by-CRDT. Real systems have non-`bd-sync` writers.
- **What happens when bd's 60s JSONL throttle (documented in the umbrella `CLAUDE.md`) interacts with `validate-trilink.sh` in CI?** A bead update made within the throttle window has happened in the DB but is not in the JSONL. CI reading the JSONL sees a missing reference that the DB actually has. The plan's mitigation `export.interval=1s` reduces but does not eliminate the window.
- **At-least-once or at-most-once?** A `bd-sync note` that times out partway through mirroring to GH and Plane — does it retry? If yes, does GH/Plane deduplicate comments? (They do not.)

**Why this embarrasses Kleppmann to leave unflagged.** This is the canonical distributed-systems beginner mistake: building a multi-system invariant out of optimistic point-in-time writes and a periodic detector. It always works in demos. It always breaks in production. The plan's § 8 risk row says _"label discipline that's easy to forget"_ — that frames a distributed-consistency problem as a human-discipline problem. Kleppmann's career is largely a polemic against that frame.

**Mitigation must specify (not optional).**

1. **Declare bd as the linearizable writer; declare GH and Plane as eventually-consistent followers.** Cite the existing source-of-truth hierarchy. State it inline in AC-12, not by reference to a CLAUDE.md elsewhere. The kernel team should be able to read this plan and know which system to ask.
2. **Specify the write protocol.** A new tri-linked artifact's creation MUST follow: (1) bd create; (2) on success, bd-sync writes to GH + Plane and records the returned IDs back into the bead's description; (3) if step 2 fails, the bead is in `pending_mirror` state and the next `bd-sync` invocation retries. The bead is the durable record; GH and Plane are projections.
3. **State the dedup contract for at-least-once delivery.** `bd-sync note` MUST be idempotent: each note carries a `bd_note_id` UUID; GH/Plane comment bodies include the UUID; the mirror checks for an existing comment with that UUID before posting. Without this, a retry doubles the audit trail.
4. **Define drift-resolution semantics, not just drift detection.** When `validate-trilink.sh` reports a MISS-GH (bead claims a GH issue that does not exist), what is the remediation? Create the GH issue retroactively? Mark the bead as orphaned? The plan does not say, so each future operator will pick differently and the audit trail will diverge.
5. **Acknowledge non-`bd-sync` writers.** GitHub issues are written by Gemini bot, by partner engineers, by external contributors. The plan needs a story for "a GH issue was created without a Bead/Doc footer." Currently the CI gate (line 819) _"filter --label refiner to that repo's GH"_ means anyone who forgets the `refiner` label is invisible. That is a giant footgun.
6. **Add a § 8 risk row that names the failure mode honestly.** "Three-way replication between bd, GH, and Plane has no formal consistency model; we operate under last-write-wins-with-human-reconciliation. Divergence WILL occur and MUST be reconciled by the operator. Frequency is bounded by the discipline of using `bd-sync` exclusively, which we cannot enforce for external writers."

The plan's current mitigation — "CI gate + agent reference + bash verifier" — is the operational equivalent of saying "we'll handle replication lag by having the user read the docs." Kleppmann's verdict on that approach is on record (DDIA ch. 9 § "Linearizability vs Consistency").

---

## F-MK-4 — Schema evolution from 13 → 14 entities has no migration story for existing v0.1.0 consumers

**Severity:** P1 CRITICAL
**Axis:** (a) GAPS / (b) RISK

**Plan text invoked.** AC-1 (line 184): _"Tier-1 IEP integration (user choice): new `SkillVersion` entity in `intent-eval-core` kernel … The 14th canonical entity."_ § 4.5 ecosystem matrix row `iec-E12`: _"Adding 14th entity simultaneously with EvidenceBundlePayload work creates merge hazard | Honor Parallel Change discipline; SkillVersion lands in v0.3.0 only after v0.2.0 ships."_ § 4 Phase C: kernel version goes from `0.2.x → 0.3.0 (MINOR bump because new entity is additive; following Parallel Change discipline per bd_000-projects-xcs4)`.

**Kleppmann position invoked.** DDIA ch. 4 (encoding and evolution): a schema-versioned kernel package with downstream consumers requires explicit forward- and backward-compatibility contracts. "Additive" is a property of _fields_, not of _entities_. Adding a 14th top-level entity to a schema registry that downstream codegen enumerates is not transparent to consumers — every consumer that ran `for entity in registry.entities()` now gets 14 entities instead of 13, and every consumer that exhaustively switched on entity type now has a non-exhaustive match.

**What the plan actually specifies.** A MINOR semver bump (0.2.x → 0.3.0) and a one-line justification ("additive"). The plan does not specify:

- **What downstream consumers exist of `@intentsolutions/core@0.2.x` at the time v0.3.0 ships?** j-rig, audit-harness, and intent-rollout-gate are listed. What does each one do on encountering an unknown predicate URI or an unknown entity reference?
- **The Zod codegen contract.** `pnpm run codegen:validators` (per umbrella `CLAUDE.md`) regenerates validators. If a v0.2.x consumer pins to a specific generated artifact and a SkillVersion-bearing Evidence Bundle row arrives at runtime, the consumer's Zod validator does not recognize it. Does it: fail closed (reject the bundle), fail open (pass through), or skip the unknown predicate?
- **The `schemas/v1/index.json` registry contract.** Line 646: _"`schemas/v1/index.json` — register new entity + predicate."_ When does a consumer re-read that registry? At install time? At runtime? Never (baked into the consumer's compiled artifact)? Each answer has a different schema-evolution story.
- **Forward-compatibility for v0.4.0.** If a consumer is on v0.3.0 and a producer is on v0.4.0 (15th entity), the same problem recurs. The plan needs a one-time-or-permanent decision: does the kernel guarantee "consumers ignore unknown entity types" forever, or does the kernel commit to "every consumer upgrades in lockstep"?

**Why this matters.** This is the entire reason DDIA chapter 4 exists. A package on npm with `sigstore provenance` and multiple downstream consumers is a public schema contract. "Additive" is a claim that requires the consumer to have been written defensively. The plan inherits whatever defensiveness `intent-eval-core@0.1.0` shipped with, and the v0.1.0 release AAR (cited from umbrella `CLAUDE.md`) does not, on quick reading, specify the unknown-entity behavior.

**Mitigation must specify.**

1. State the forward-compatibility contract for the kernel: "Consumers MUST skip unrecognized predicate URIs and entity types; SHOULD log them. Kernel consumers that fail closed on unknown types are non-conforming." Or the opposite — pick one.
2. Add a Phase C exit criterion: "All three named downstream consumers (`j-rig`, `audit-harness`, `intent-rollout-gate`) have been tested against a v0.3.0 bundle while still pinned to `@intentsolutions/core@0.2.x` and exhibit the documented forward-compatibility behavior." Without this test, the "additive" claim is unverified.
3. State whether `schemas/v1/index.json` is consumer-readable at runtime or compile-time. The answer changes the migration story dramatically.
4. Add a § 8 risk row: "v0.3.0 ships a 14th entity assuming consumers ignore unknown entities; this is untested at v0.1.0 release boundary."

---

## F-MK-5 — Content-addressed store has no garbage-collection consistency model

**Severity:** P2 MAJOR
**Axis:** (a) GAPS

**Plan text invoked.** § 4 Phase A deliverables: _"Append-only event log at `.j-rig/refiner/log.jsonl` … Content-addressed store at `.j-rig/refiner/store/<hash>` … Single mutable pointer file: `.j-rig/refiner/pointers/<skill>/best` (just a hash)."_ Phase E.3: _"Signed Evidence Bundle | `<repo>/.j-rig/refiner/evidence/<sha>.json` (gitignored if signed-prod, committed if signed-staging) | Indexed by sha; orphaned bundles GC'd after 90 days."_

**Kleppmann position invoked.** DDIA ch. 3 (storage engines) + content-addressed store literature (Camlistore, IPFS, Git's loose-object store): a content-addressed store with a separate mutable pointer needs a defined liveness criterion — which objects are reachable, which are not, and what process safely deletes the unreachable ones without racing against new writes.

**What the plan does not specify.**

- **What references count toward "reachable"?** The `best` pointer reaches one version; the lineage chain (parent_version_id) reaches the ancestry; the rejected-edit buffer reaches some EditProposal hashes; the Evidence Bundle rows reach the SkillVersion they attest to. Are all four reference types tracked for GC purposes, or only some?
- **What is the GC-safe-window?** Line 583 says "orphaned bundles GC'd after 90 days." Orphaned how? Last-touched? Last-referenced? The plan does not say what creates the "orphaned" verdict. A bundle that becomes referenced again during the 90-day window — say, a partner re-pins an old SkillVersion — would presumably reset the clock, but the plan does not say so.
- **What happens during concurrent GC and write?** A reader has a hash in hand and is about to fetch it; the GC has just decided it is unreachable. This is the classic race that mark-and-sweep GCs solve with read barriers or epoch-based reclamation. The plan does not say.
- **What is the audit trail for GC?** Deleting a bundle that has a Rekor entry is fine (Rekor still has the entry); deleting the local mirror means a future verifier cannot replay. Does GC record what it deleted?

**Mitigation must specify.** Pick a GC model (reference-counted with weak refs from the rejected buffer; or mark-and-sweep with a defined root set; or "never GC, storage is cheap"), document the safe window, and state the audit-trail discipline.

This is P2 not P1 because the system can ship without GC for the first six months — but the moment "orphaned bundles GC'd after 90 days" goes into production prose, the contract has been declared.

---

## F-MK-6 — `accept()`'s "strict improvement on all dimensions" is a partial-order rule with no defined tie-breaking

**Severity:** P2 MAJOR
**Axis:** (b) RISK — failure mode not named

**Plan text invoked.** AC-3 (line 186): _"Multi-dimensional score records (Goodhart-resistant). Score is `(skill_hash, eval_set_hash, behavioral_score, readability_score, adversarial_pass_rate, ...)` — never collapsed to a scalar."_ § 4 Phase A: _"`accept()` — pure transformation + strict-improvement gate."_ D4 diagram (line 992-993): _"strict improvement | on all dims?"_.

**Kleppmann position invoked.** Multi-dimensional score comparisons form a _partial order_ (Pareto), not a total order. Append-only logs that branch on partial-order comparisons need a defined behavior when the comparison is _incomparable_ — version A is better on behavioral but worse on readability; version B is the reverse. The plan's "strict improvement on all dimensions" is the most conservative possible rule (Pareto-strict-dominance), which means:

- **Almost no edit will be accepted.** Any edit that improves behavioral by 2pp but loses 0.1pp of readability is rejected. Real-world refinement does not produce strict-dominance improvements; it produces trade-offs.
- **The `accept()` gate is therefore the bottleneck**, and the rejected-edit buffer (mentioned in D4) will dominate the accepted ledger.

**What the plan does not specify.**

- Is "strict improvement" actually strict Pareto-dominance (all dims ≥, at least one >)? Or is it "at least one dim strictly improved, others non-degraded by more than ε"? The plan reads as the former; production reality demands the latter.
- What is the human-override path when a human evaluator looks at a Pareto-incomparable edit and says "yes, this is better"? Phase B has the `promote` command (human-gated per AC-4), but does the promote bypass `accept()` or compose with it?

**Mitigation must specify.** Either (a) document strict Pareto-dominance as the gate, accept that most edits fail it, and design the workflow around that (this is the conservative-but-coherent choice); or (b) introduce a tolerance vector / weight vector and document how it is set, audited, and versioned. Either way, the gate's behavior in the incomparable case must be stated, not left to the reader.

---

## F-MK-7 — Phase B end-of-turn `line.sh` background refiner has no defined consistency with the local SKILL.md

**Severity:** P3 MINOR
**Axis:** (b) RISK

**Plan text invoked.** § 4 Phase B hook table, L2 row: _"Line (L2) | `Stop` hook | If a skill was invoked during the turn AND j-rig has scored its rollouts: append to `.j-rig/refiner/log.jsonl`. After N rollouts on a skill: fire refiner in background, surface candidate in next-turn context."_

**Kleppmann position invoked.** A background process operating on a file that the user is actively editing in the foreground is a concurrent-writer scenario. The plan does not specify what happens when the user edits the SKILL.md between the L2 background refiner reading it (to compute a candidate) and the next turn surfacing that candidate. The candidate's `parent_version_id` will point at a SkillVersion that no longer matches the on-disk SKILL.md.

**Mitigation.** State that L2 always operates on the hashed SkillVersion captured at the moment the rollout was scored, not on the live on-disk file; if the user has since edited the on-disk file, the next-turn candidate surfaces with an explicit "candidate is against version X; your current working copy is at version Y; reconciliation required" message. This is a minor finding but it costs nothing to specify and will be ugly the first time it happens in a demo.

---

VERDICT: AMEND
