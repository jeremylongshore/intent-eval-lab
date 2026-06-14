# State-machine single-source + drift gate (Blueprint B ↔ kernel)

**Status:** NORMATIVE · **Date:** 2026-06-13 · **Authority:** Blueprint B
(`012-AT-ARCH-platform-runtime-blueprint.md`) § 3.1 (runtime state machines — NORMATIVE)
and § 2 per-entity "Lifecycle states" rows · **Closes:** Kleppmann finding #5
(`023-AA-AACR-thinker-panel-review-2026-05-25.md` § 2.1) · **Bead:** make the
state-machine spec single-sourced + add a CI drift gate

This spec makes the 13-entity runtime state machines a **machine-checkable single source**
and adds a CI drift gate proving the kernel `@intentsolutions/core` stays conformant to
Blueprint B. It is the home of the artifact + gate; Blueprint B § 3.1 remains the
human-normative source the artifact is extracted from.

## 1. The hole this closes

Blueprint B § 3.1 specifies the runtime state machines as `(from_state, event, to_state)`
prose triples — the EvalRun machine as an explicit table (lines 339–352), the other 12
entities as a per-entity "Lifecycle states" row in § 2. The kernel ships those machines as
`<entity>Transitions: TransitionMap<S>` const exports (consumed by the `canTransition`
helper). **There was no machine-checkable artifact and no gate proving the two are
single-sourced.** A developer could edit a kernel `TransitionMap` without touching the
Blueprint, ship an out-of-spec runtime, and no static gate would catch it — Blueprint A
§ 1.2 principle 10 (schema-is-canon) silently failing at the state-machine layer
(Kleppmann finding #5).

## 2. Direction chosen — Blueprint B is canon, kernel is checked against it

The bead offered two directions: (a) make Blueprint B the machine-readable source and
generate the kernel from it, or (b) flip — let kernel TS be canonical and generate the
Blueprint table from a doc-extractor. **This spec takes direction (a)** because the IEP
source-of-truth hierarchy already makes Blueprint B the normative authority for runtime
architecture (`CLAUDE.md` § "Convergence work — source-of-truth hierarchy", tier 4). The
gate is **lab-side and read-only** w.r.t. the kernel — it never edits `@intentsolutions/core`.

## 3. The artifact — `specs/state-machines/transition-table.v1.json`

The canonical, regenerable extraction of Blueprint B:

- **`entities[]`** — one entry per canonical entity, each with the full
  `(from, event, to, guard)` 4-tuples extracted from Blueprint B (the EvalRun set from the
  § 3.1 table; the other 12 from their § 2 "Lifecycle states" rows), plus a `spec_ref`
  back-pointer (section + line) so it is auditable, not hand-drifted.
- **`kernel_state_map`** — the DERIVED, event-erased `from → sorted-unique [to]` projection.
  This is the shape the kernel's `TransitionMap<S>` uses, and the exact object the gate
  diffs against the kernel. Regenerate it from the 4-tuples with
  `python3 scripts/check-statemachine-drift.py --rebuild-kernel-view` (deterministic).
- **`ambiguities_reconciled[]`** — records the two places where Blueprint B prose was loose
  and the kernel made a defensible refinement (see § 5).

## 4. The gate — `scripts/check-statemachine-drift.py` + `statemachine-drift.yml`

Stdlib-only Python, **zero runtime deps**, offline by default.

- **Default (offline):** compares the committed kernel snapshot
  (`specs/state-machines/kernel-transition-snapshot.v1.json`, vendored per the
  `specs/_vendor/` + `specs/snapshots/.sha` hermetic-CI pattern) against the artifact's
  `kernel_state_map`. REDS (exit 1) on any drift: a missing/extra map, a missing/extra
  from-state, or a mismatched to-state set.
- **`--refresh [--source local|raw|auto]`:** re-reads the live kernel maps (a sibling
  `intent-eval-core` checkout, or `KERNEL_SRC_DIR`, or the GitHub `raw` URL of
  `src/entities/*.ts`), rewrites the snapshot, then compares. CI uses `--source raw` so it
  catches kernel-main drift even with a stale lab snapshot.
- **`--rebuild-kernel-view`:** recomputes `kernel_state_map` from the 4-tuples after a
  Blueprint B edit.

The CI workflow (`.github/workflows/statemachine-drift.yml`) runs both an offline check and
a live `raw` check (which also asserts the committed snapshot is byte-current), on PRs/pushes
touching the artifact/script/Blueprint-B/workflow, plus a daily cron to catch kernel-main
drift when no lab file changed.

### Single-sourcing a legitimate change

When the state machines genuinely need to change, edit all three in the **same PR**:

1. Edit Blueprint B § 3.1 / § 2 (the human-normative source).
2. Update the artifact 4-tuples + `--rebuild-kernel-view`.
3. `--refresh --source raw` to update the snapshot (after the kernel change lands on main).

## 5. Scope + honest reconciliation

**All 13 canonical entities are covered** — the kernel declares a `TransitionMap` for every
one as of `intent-eval-core` E05 (state machines) + E02a–d (13-entity domain model). No
entity is "pending kernel declaration" at this version. A future 14th entity (e.g.
`SkillVersion` per DR-028) with a state machine adds a row here + to the snapshot and falls
under the gate automatically.

Two entities had loose Blueprint prose reconciled to the kernel's shipped (defensible) reading
— recorded in `ambiguities_reconciled[]`:

- **MatcherMap** — § 2.3 line 167 says "Same transition discipline as EvalSpec", but EvalSpec
  is reversible (`deprecated → published`). The kernel ships MatcherMap as **one-way**
  (`deprecated` terminal), consistent with § 2.3 line 163 "Immutable once published; a revision
  is a new row". The artifact encodes the one-way reading; a future Blueprint clarification
  should tighten line 167.
- **FailureTaxonomy** — § 2.13 line 317 prose shows linear `proposed → canonical → deprecated`;
  the kernel also allows `proposed → deprecated` (reject a proposal without canonizing). The
  artifact encodes both (the reconciled normative intent).

These are recorded transparently rather than silently — the gate now makes any FUTURE
divergence loud.

## 6. Relation block

Relates to: Blueprint B (`012-AT-ARCH-platform-runtime-blueprint.md`) § 3.1 + § 2; Blueprint A
§ 1.2 principle 10 (schema-is-canon); the thinker-panel review
(`023-AA-AACR-thinker-panel-review-2026-05-25.md` § 2.1 finding #5); the kernel state-machine
exports (`@intentsolutions/core` `src/entities/*.ts`, `src/state-machines/types.ts`); the
schema-authority drift gate (`schema-drift.yml`, DR-018 § 6.4) it is patterned after.
