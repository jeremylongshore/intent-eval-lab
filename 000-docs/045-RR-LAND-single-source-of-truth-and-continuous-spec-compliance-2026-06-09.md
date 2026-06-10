# Single Source of Truth + Continuous Spec-Compliance

| Field | Value |
|---|---|
| Doc | `045-RR-LAND-single-source-of-truth-and-continuous-spec-compliance-2026-06-09.md` |
| Status | LANDED (skeleton) — declares the model; the epic carries the rest |
| Authority above | DR-044 (`044-AT-DECR-...`), DR-029 § 6 (`030-AT-DECR-...`), Blueprint A |
| Epic | "Continuous Spec-Compliance + Single-Source-of-Truth" (bd umbrella, prefix `iel-`) |
| Pressure-tested by | 7-thinker canon panel (Hickey, Kleppmann, Thompson, Karpathy, Gregg, Armstrong, Fowler), 2026-06-09 |

## 1. The value proposition this protects

The Intent Eval Platform's claim is to be the top-of-class, enterprise-grade authority for
"what is a valid agent-native artifact" (skill / plugin / agent / mcp / hook / marketplace). That
authority is only real if **one internal source of truth** stays continuously adherent to the
**upstream sources of truth**, and then **feeds the whole ecosystem**: the `claude-code-plugins`
(CCP) validator, the internal SKILL.md testing skills, and j-rig.

- **Upstream truth** (we do not own it): `agentskills.io` (the open standard Claude Code follows)
  + Claude/Anthropic OFFICIAL published surfaces (`code.claude.com/docs`,
  `platform.claude.com/docs`, `github.com/anthropics/claude-code`, `.../skills`) + the official
  Model Context Protocol spec (`modelcontextprotocol.io` / its `schema.ts`).
- **Internal single source of truth**: the kernel `@intentsolutions/core`
  `schemas/authoring/v1/*` (JSON Schema canonical; Zod + `$comment` manifests generated from it).
- The kernel **feeds** the ecosystem; consumer copies become CI-asserted generated derivations
  (no local patches). 6767-b / 6767-h are the prose citation layer; the kernel schemas are the
  machine source of truth.

## 2. THE PAIN POINT (the thing that cannot be ignored)

We are coupling **one artifact the entire ecosystem trusts absolutely** (the kernel schema) to a
**moving, externally-owned, untrusted input** (upstream docs we don't control and that can change,
404, restructure, or be silently wrong at any time).

> **The catastrophic, asymmetric failure — named independently by all seven thinkers:** a wrong or
> stale schema silently becomes the single source of truth and fans out authoritatively to every
> consumer at once, masked by green dashboards and alert fatigue. A *missed* upstream change ships a
> stale contract that customers' gates then validate against — corrupted signed evidence, discovered
> months later by a customer, fleet-wide.

Centralizing on one SSoT maximizes leverage **and** blast radius simultaneously. Staying
top-of-class = making *that specific failure* structurally impossible. Every design choice below is
in service of that. (This section is intentionally durable — future sessions inherit the "why".)

## 3. The deterministic / probabilistic boundary (the safety spine)

- **Detection stays deterministic + primary.** We EXTEND the existing `spec-drift-watch` — never
  replace it with an LLM. The vendored `_vendor/upstream/<contract>/` snapshot is the **firewall**:
  captured deterministically (fetch + classify); the LLM reads only; deterministic gates (changelog
  + lineage present, monotonicity holds, the known-good corpus still validates) are the SOLE
  admission path to the kernel.
- **The LLM earns exactly ONE hop:** classify an ALREADY-detected diff's *materiality + which
  contract owns it*. Bracketed by deterministic walls — (pre) every field it claims changed must
  appear as a literal substring in the fetched bytes else reject (Armstrong); (post) the resulting
  schema must still validate the known-good corpus else reject (Armstrong); output is a
  schema-validated `drift-classification/v1` row, not prose (Karpathy).
- **The LLM never authors a kernel schema edit and never closes the deterministic drift signal.**
  It starts in advisory comment-mode; it graduates to opening *low-blast-radius* PRs (snapshot /
  `.sha` / coverage refresh) only after clearing a recall floor on a frozen eval. Kernel schema
  edits = agent opens an issue with a proposed diff; a human authors. **Autonomy gradient by
  artifact immutability tier.**
- **Diff anchor (Kleppmann/Gregg):** NOT byte-sha256 of the page. Extract a per-surface **normative
  projection** (field set + required/optional + allowed values + deprecations) → diff projections
  field-by-field. Byte-hash demoted to a "should we re-extract?" tripwire. The projection IS the
  coverage-map's left-hand side.

## 4. The 7-thinker corrections (folded into the design)

| Thinker | Correction | Where it lives |
|---|---|---|
| **Hickey** | Don't braid our rules with theirs in one file. Each contract = three artifacts: `upstream-base` (theirs), `is-overlay` (ours, each field with a convergence trigger), and the published `allOf` composition (zero authored fields). Convergence = a mechanical MOVE overlay→base. | kernel `authoring/v1/{upstream-base,is-overlay}/*` + composition |
| **Kleppmann** | Extract-then-diff a normative projection, not a page byte-hash. Append-only **lineage log** keyed on (upstream-identity, upstream-version); coverage-map = derived view. Honor the advisory currency model (`pins.v1.json`) rather than inventing exit authority. | `scripts/spec-projection-diff.py`, `_vendor/.../projection.v1.json`; lineage = beaded |
| **Thompson** | `git diff _vendor/` IS the upstream changelog. The `/spec-currency` skill is a disciplined classifier+router, not an unsupervised fleet. | `_vendor/` under git; beaded |
| **Karpathy** | The `.md` shims are deterministic across fetches — gold. The classifier writes nothing until it clears a recall≈1.0 floor on a frozen, human-labeled eval set; output is a schema-validated row, not prose. | beaded (`drift-classification/v1` eval set) |
| **Gregg** | The watcher must not fail silent-green: per-surface `fetch_error_streak` (>=3 → fail) + a dead-man heartbeat (no run in 26h → alert). Dashboard = composite DETECTOR-HEALTH top tile, drift table below. | `scripts/watcher-liveness.py` + workflow (LANDED) |
| **Armstrong** | Three append-only tiers (raw-fetch archive → vendored snapshot from FETCH_OK only → kernel, human-promoted); typed fetch-failure taxonomy; change-class supervision tree (additive→auto-PR / breaking→sign-off / conflict→stop). The differ never writes its own reference. | partial (LANDED firewall + FETCH_OK gating); rest beaded |
| **Fowler** | Build the walking skeleton first (skill-frontmatter — deepest capture + hardest overlay). Build the sensor before the dashboard. Closure invariant + WIP-1 so the epic doesn't become immortal. | kernel PR (skill-frontmatter) + this epic |

## 5. What LANDED this pass (the walking skeleton)

1. **Kernel: skill-frontmatter contract #1** (separate PR on `intent-eval-core`) — the three-artifact
   base+overlay composition + the D7 foundation refactor (3 universal folds, `securityChecks`
   universal-immutable, `requiredFields` per-contract) + ajv↔Zod fold-agreement + the **monotonicity
   property test** (the 2026-04-28-debacle guard) + 100% coverage.
2. **Fitness Function #2** (`scripts/spec-projection-diff.py`) — field-level extract-then-diff for
   skill-frontmatter, running on a real `_vendor/` snapshot. `--check` (snapshot↔projection
   consistency) + `--self-test` (proves the differ detects every drift class with no false positive,
   so it cannot pass green vacuously).
3. **Two P0 watcher-liveness fixes** (`scripts/watcher-liveness.py` + the workflow) — per-surface
   `fetch_error_streak` (>=3 consecutive errors → fail loud) and a dead-man heartbeat (external ping
   = true dead-man + retrospective gap check on resume). Both deterministic, unit-verified.
4. **The vendored firewall** (`_vendor/upstream/skill-frontmatter/`) — the single vendored source +
   its normative projection.
5. **The upstream-surface registry** (`specs/upstream-surfaces/registry.v1.json`) — per-contract
   authoritative surfaces + authority precedence + machine-readable? + monitored?, including the
   **MCP official spec + `schema.ts`** (the critical unmonitored gap).
6. **This declaration** — the SSoT model + the pain point + the 7-thinker corrections.

## 6. The changelog-observance gate (specification)

Changelog observance is **mandatory** and is the cheapest guard against a silent schema swap:

- The kernel CHANGELOG (`schemas/authoring/v1/CHANGELOG.md`) is canonical. **A schema change without
  a matching changelog entry + a lineage-log record fails CI.** (`git diff _vendor/` is the upstream
  changelog — Thompson.)
- The dashboard surfaces `captured_sha == last_observed_sha`; the gap IS the reconciliation number.
- The CCP `SCHEMA_CHANGELOG.md` cites the kernel rather than re-deriving rules (consumer-cutover bead
  `rqwh`).

This gate is **specified here**; its CI implementation is a child bead under the epic.

## 7. What is beaded (NOT built this pass)

Under the epic, WIP-limit = 1 contract in flight; closure invariant = the PATTERN exists and
skill-frontmatter rides it end-to-end (deep-capture → base/overlay schema → drift-watch → classify →
reconcile). Beaded: the `drift-classification/v1` eval set (recall≈1.0-before-write); the LLM
classifier walls (substring pre-check + corpus post-check; advisory comment-mode first); the
6→~15 watcher expansion (Wave 1: MCP spec + `schema.ts`, hooks, settings, slash-commands); the
deep upstream capture for the other 5 contracts (MCP first — it has a real schema); the
scattered-shadow-copy collapse into one `_vendor/`; `pins.v1.json` reuse as the freshness substrate;
the append-only lineage log + three-tier archive; the change-class supervision tree; the
DETECTOR-HEALTH composite dashboard; the changelog-observance CI gate; and the three sequenced,
staged consumer cutovers (internal SKILL.md validators → j-rig → CCP last — CCP carries the
Grade-D+ cleanup).

## 8. Consumer cutover posture (declared; executed later)

The kernel is declared the SSoT for (1) the CCP validator, (2) the 7 internal SKILL.md validators,
(3) j-rig. Staging discipline: version-pinned consumers (never float on `main`); shadow-mode
(run kernel schema alongside the hand-rolled one, log disagreements, zero-on-corpus is the gate);
declared fail-open (advisory validators) vs fail-closed (j-rig rollout-gate) posture per consumer;
a canary consumer auto-bumps first; sequence **blast-radius ASCENDING** — internal skills → j-rig →
CCP last (public, hardest to walk back). Each cutover deletes the local schema in the same PR as the
`$ref`.

---

— Jeremy Longshore
intentsolutions.io
