# Greptile review orientation — `intent-eval-lab`

This file briefs an AI reviewer on what this repository _is_ and what a
high-quality review of it catches. Read it before reviewing any change here.
The machine-checkable rules live in `.greptile/config.json`; the load-bearing
documents to ground a review live in `.greptile/files.json`. This file is the
narrative that connects them.

## 1. What this repo is — the constitution of a 6-repo platform

The **Intent Eval Platform (IEP)** is an agent-native evaluation platform built
as a small set of independent open-source repositories that converge via a
single shared **Evidence Bundle** schema — not via package consolidation.
Convergence happens at the schema layer.

The six repos:

- the canonical **contracts kernel** (`@intentsolutions/core`) — TypeScript
  types + JSON Schemas + Zod validators + Pydantic models + state machines for
  the platform's domain entities. No execution, no judges, no runtime.
- **this repo, `intent-eval-lab`** — the methodology, the specs, the Blueprints,
  the canonical glossary, and the Decision Records.
- the deterministic-gate **audit harness** — emits Evidence Bundle gate-result
  rows.
- the behavioral-eval **j-rig** harness — consumes and emits Evidence Bundle
  rows.
- the **rollout-gate** GitHub Action — consumes a bundle plus a policy and emits
  a ship / no-ship decision.
- the public **reports dashboard** (the 6th platform repo).

**This `intent-eval-lab` repo is the constitution.** It holds the governance
that the other five repos (and any code anywhere in the ecosystem) must obey.
The most important consequence for a reviewer:

> If code or docs **anywhere else** in the ecosystem conflict with a ratified
> Decision Record, a Blueprint, or the glossary **here**, the documents here
> win. A change in this repo that quietly contradicts one of these higher-tier
> sources without reconciling it is a defect, even when the prose reads cleanly.

## 2. Source-of-truth hierarchy (apply when documents conflict)

When two authored statements disagree, the higher tier wins. The reviewer's job
is to flag any new normative assertion that contradicts a higher tier without
citing and reconciling it.

1. **bd workspace** — wins for task state, dependencies, and bead clusters.
   (Lives in the umbrella, not this repo, but it is tier 1 of the hierarchy.)
2. **DR-010** (`000-docs/010-AT-DECR-...`) — wins for governance bindings: the
   unification thesis (every validator emits an Evidence Bundle), the
   TS-primary / Python-permitted language rule, the predicate-URI grammar, the
   `labs.*` reserved-don't-touch rule, and the override addenda
   (§ 13.5 customer-signal gate removed → Phase B is bandwidth-gated;
   § 13.6 external-pattern non-borrow).
3. **Blueprint A** (`000-docs/011-AT-ARCH-...`) — wins for ecosystem principles,
   the repo taxonomy, anti-goals, and governance routing.
4. **Blueprint B** (`000-docs/012-AT-ARCH-...`) — wins for runtime architecture,
   the canonical domain model, and the normative `gate-result/v1` predicate
   contract.
5. **Canonical glossary** (`000-docs/014-DR-GLOS-...`) — the single source for
   platform terminology. Every other doc cites it rather than redefining a term
   inline.

Two related authorities sit alongside this stack:

- **The Spec Authority Kernel (SAK).** The kernel's `authoring/v1` chamber is
  the single internal source of truth for **authoring-artifact validity** — what
  makes a valid agent-native artifact (skill, plugin, agent, MCP server, hook,
  marketplace catalog). It is chartered by DR-044 and ratified by DR-049 /
  DR-081. On any question of "is this authoring artifact shape valid", the
  kernel `authoring/v1` schema wins; prose specs are amended to match the
  schema, never the reverse.
- **Machine-readable schema beats prose.** Where a normative prose spec and the
  kernel JSON Schema describe the same contract, the schema is authoritative and
  the prose is corrected to match it (see `000-docs/083-AT-SPEC-...` for the
  explicit statement of this rule for `skill-refiner-pass/v1`).

## 3. The Decision Record (DR) system — how governance changes legitimately

Governance is changed only through ratified **Decision Records** (filed as
`AT-DECR` docs). A reviewer treats the DR system as load-bearing:

- **Every change to ratified governance must cite the amending DR.** A change to
  a predicate, schema, entity shape, acceptance gate, or any other ratified
  clause that does **not** reference the DR that authorizes it is an
  un-ratified governance change — flag it.
- **DRs supersede and amend each other; track the chain.** For example, the
  `skill-refiner-pass/v1` predicate is minted by DR-082, corrected by DR-085,
  and amended in place by DR-086; the SAK charter is DR-044 → DR-049 → DR-081.
  A change that cites a superseded clause without acknowledging the correcting
  DR is reasoning from stale governance.
- **One-way-door artifacts get extra protection.** Immutable or signed surfaces
  (predicate URIs, attestation envelopes, frozen payload shapes, standards-body
  identifiers) cannot be edited in place once frozen — they are corrected only
  by an erratum/amending DR with the proper attestation. If a build agent
  detects two contradictory ratified clauses on a one-way-door artifact, the
  rule (`000-docs/087-AT-STND-...`, the ratified-clause-conflict halt gate) is
  to **HALT and escalate**, not to silently pick a side. A change that resolves
  such a contradiction unilaterally is a finding.
- **State labels are real.** Every numbered doc carries a lifecycle label
  (NORMATIVE / DRAFT / SUPERSEDED / PLANNED / CURRENT) per
  `000-docs/069-DR-STND-...`. A change that treats a SUPERSEDED doc as live, or
  that asserts NORMATIVE force from a DRAFT, is a finding.

## 4. Hard bindings — non-negotiable, enforced by CI and by review

These are the disciplines a reviewer must never let slip. Several are also
enforced by deterministic CI gates; review is the second line.

- **Partner-name vendor-generic discipline.** No company, vendor, or partner
  proper name appears in public repo content (specs, `000-docs/`, README,
  CLAUDE.md, or any committed file) until that party has **explicitly consented
  in writing** to being named. Use vendor-generic phrasing instead — for
  example "an enterprise partner engagement" or "the inaugural case study
  (engagement-private)". This applies even to negative-affirmation phrasings
  ("we don't name X, Y, Z" still names them). The concrete grep pattern lives in
  a PRIVATE source and a CI guard; **never inline a partner name in any file in
  this repo, including this one** — describe the discipline generically. A real
  partner name leaking into a public spec is a high-severity finding.
- **Predicate URIs live only at `evals.*`.** Predicate URIs, in-toto attestation
  predicate identifiers, and OpenTelemetry attribute namespaces may exist only
  at `evals.intentsolutions.io`, following the locked single-segment grammar
  `evals.intentsolutions.io/<predicate-type>/v<version>`. The
  `labs.intentsolutions.io` subdomain is **permanently reserved-don't-touch** for
  predicate identity — it may host blog/methodology/dashboard content but never a
  predicate URI, attestation identifier, or OTel namespace. Flag any predicate
  URI that points at `labs.*`, or that deviates from the locked grammar (for
  example inserting an extra path segment).
- **No aggregate PASS% across heterogeneous predicates.** Do not average, roll
  up, or headline a single pass-rate across distinct predicate types or distinct
  failure-mode categories. This violates the composable-partial-attestation
  principle (Blueprint B § 7): each Evidence Bundle row is independently
  verifiable, bundles are **unioned, not joined**, and **silence is not
  failure** — a bundle covering 3 of 6 categories means "these 3 were tested; the
  other 3 were not", never "the other 3 failed". Flag any code, doc, or report
  that collapses non-comparable predicates into one number, or that treats an
  absent row as a failing row.
- **Doc-filing standard.** Every authored doc under `000-docs/` follows
  `NNN-CC-ABCD-<short-description>-<date>.md`: `NNN` a zero-padded sequence,
  `CC` a category code (AT decision/architecture, DR draft/standard/glossary, RR
  research/recon, PP plan, AA after-action), `ABCD` a short sub-type. Flag a new
  `000-docs/` file that is unnumbered, undated, or uncoded. Generator-owned
  dashboards (for example `SAK-DASHBOARD.md`, `docs/detector-health.md`) are
  exempt — their bytes belong to their generators.
- **Repo boundaries.** Each repo owns a defined slice; the contracts kernel
  carries **no** execution, judges, or runtime (`000-docs/068-AT-STND-...`).
  Flag a change that places logic on the wrong side of the Evidence Bundle seam.

## 5. What a high-quality review of this repo catches

Beyond ordinary correctness and prose quality, a strong review here surfaces:

- **A normative doc contradicting a higher-tier source without reconciliation.**
  A new claim in a NORMATIVE doc that disagrees with DR-010, a Blueprint, the
  glossary, or the kernel `authoring/v1` schema, and does not cite and reconcile
  the higher source.
- **An un-ratified governance change.** A change to a predicate, schema, entity
  shape, acceptance gate, or other ratified clause that does not reference the
  amending DR — or that contradicts a ratified clause without an erratum.
- **A unilateral resolution of a ratified-clause conflict on a one-way-door
  artifact** instead of a HALT-and-escalate.
- **A partner name leaking into a public spec**, or any reintroduction of a
  vendor name that lacks recorded written consent.
- **A predicate URI on `labs.*`, or off the locked grammar.**
- **An aggregate pass-rate across heterogeneous predicates**, or an absent
  Evidence Bundle row read as a failure.
- **A stale-state hazard** — a SUPERSEDED doc cited as live, or a doc whose
  `state_label` no longer matches its content.
- **A doc-filing violation** — a new `000-docs/` file that breaks the naming
  scheme.

When in doubt about which source governs, prefer the higher tier in § 2 and ask
for the DR that authorizes the change.

## Review priorities — what to weight, what to skip

Greptile is **advisory** here. The deterministic merge gate is this repo's own
required CI (typecheck, lint, tests, coverage/mutation where applicable, the
audit-harness self-check, and CodeQL). Greptile's job is the semantic layer those
gates structurally cannot see — weight findings accordingly.

**Prioritize** (worth a comment): correctness and logic errors; security and
supply-chain / credential exposure; data-integrity and signed-evidence invariants;
concurrency and ordering hazards; input validation; auth / authorization
boundaries; secret handling; and regressions against the scoped invariants in
`config.json`.

**Deprioritize** (do not spend a comment here): style and naming; formatting;
churn in generated or build artifacts; and anything the L1 linters or CodeQL
already report. Never restate a deterministic gate — state the problem, the
`file:line`, and the concrete fix.
