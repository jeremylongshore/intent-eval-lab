---
title: Multi-Tenant Boundaries — tenancy isolation model (doc-now, build-later)
date: 2026-06-18
authors:
  - Jeremy Longshore (Intent Solutions)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: Blueprint B § 5.3 (forward-compatibility trigger — multi-tenant isolation hardening); Blueprint A § 2.3 (Class-1 governance)
inherits_from:
  - 011-AT-ARCH-ecosystem-master-blueprint.md (Blueprint A — constitution)
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — runtime + isolation pillars)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: iel-E13
bead: bd_000-projects-r3se
filing_standard: Document Filing Standard v4.3
related_docs:
  - 012-AT-ARCH-platform-runtime-blueprint.md (Blueprint B — § 4.1 isolation, § 5.3 trigger, § 1 fair-queueing)
  - 068-AT-STND-core-repo-boundaries-2026-06-18.md (repo boundaries)
  - 069-DR-STND-state-labeling-standard-2026-06-18.md (scope-element labels)
  - 014-DR-GLOS-canonical-glossary.md (terminology source of truth)
related_drs:
  - 004-AT-DECR (DR-004 — provider PASS/FAIL gates, credential broker)
  - 010-AT-DECR (DR-010 — Q2 broker pattern CISO non-negotiable; § 13.5 bandwidth-only gate)
---

> **State label: NORMATIVE.** Specifies the tenancy isolation model. The model is
> **documented now and built later** — single-tenant is `CURRENT`; the multi-tenant
> build is `DEFERRED` until the Blueprint B § 5.3 trigger fires.

# Multi-Tenant Boundaries

**Beads:** `bd_000-projects-r3se` (iel-E13c) under epic `bd_000-projects-7gs` (iel-E13).
This is the forward-referenced "multi-tenant boundaries spec" cited in Blueprint B § 4.1,
§ 5.3, and § 1 (weighted-fair-queueing).

## 0. Doc-now, build-later — read this first

This is a **doc-now, build-later** specification. It exists so that the tenancy boundary
is **designed before it is needed**, not improvised under pressure when a second tenant
arrives. Per Blueprint B § 5.3, multi-tenant isolation hardening is a **forward-compatibility
trigger**: the platform runs as a single-tenant modular monolith today, and onboarding a
second tenant whose security posture cannot tolerate single-process isolation is the event
that justifies building the model below.

Scope-element labels (per `069-DR-STND` § 1) used throughout:

| Concern | Label | Meaning |
| --- | --- | --- |
| Single-tenant operation | `CURRENT` | What runs today. |
| Tenant identity + quota model | `PLANNED` | Designed here; reserved; not yet built. |
| Per-tenant deployment / worker pods | `DEFERRED` | Built only when the § 5.3 trigger fires. |
| Cross-tenant data sharing without consent | `REJECTED` | An anti-goal — never. |

Nothing in this document authorizes building tenancy now. Per Blueprint B § 5.3, the build
is a **Class-1 ISEDC governance event**; this spec is the design the council evaluates when
the trigger fires. Per DR-010 § 13.5, the platform is bandwidth-gated, not customer-signal-gated
— so the trigger is a security-posture requirement of a real second tenant, not a speculative
roadmap milestone.

Terms (tenant, isolation, credential broker, sandbox, EvalRun, fair-queueing) are defined in
the Canonical Glossary (`014-DR-GLOS`) and Blueprint B; this document does not redefine them.

## 1. The single tenant today (CURRENT)

The platform today serves a single tenant: the acting head of board's own engineering
practice (Blueprint A § 1.1). The runtime is a modular monolith (Blueprint B § 5) with:

- A single shared PostgreSQL store and a single shared Redis instance (Blueprint B § 1).
- Per-**user** fairness via weighted-fair-queueing (Blueprint B § 1: "each user gets a share
  of total worker concurrency proportional to their declared quota").
- OS-level sandboxed worker execution (Linux user namespace + cgroup v2 + seccomp-bpf,
  Blueprint B § 4.1).
- A process-isolated credential broker that is the only process to see plaintext provider
  credentials (Blueprint B § 4.1, DR-010 Q2 CISO non-negotiable).

In the single-tenant case, "user" is the unit of fairness and the unit of quota. There is no
**tenant** boundary above the user, because there is exactly one tenant. The isolation that
exists protects the platform from evaluated artifacts (the sandbox) and protects credentials
from evaluated artifacts (the broker) — it does not partition one customer's data from another's,
because there is only one customer.

## 2. What a tenant is (PLANNED)

A **tenant** is a top-level isolation boundary above the user: an organization whose users,
EvalSpecs, EvalRuns, SkillSnapshots, Evidence Bundles, and cost ledger are isolated from every
other tenant's. The tenant is the unit of:

- **Data partitioning** — a tenant's rows are never readable by another tenant's users.
- **Quota** — a tenant has an aggregate worker-concurrency share; users within a tenant share it.
- **Billing / cost attribution** — the CostRecord rows (Blueprint B § 2) roll up per tenant.
- **Credential custody** — a tenant's provider credentials are brokered only for that tenant's
  EvalRuns; a credential never crosses a tenant boundary.
- **Signing identity** — Evidence Bundle rows emitted for a tenant carry that tenant's actor
  identity; predicate URIs remain platform-global (`evals.intentsolutions.io`, never per-tenant
  subdomains — the `evals.`/`labs.` reservation in Blueprint B § 7.2 is not tenant-scoped).

The tenant model is **reserved** here. The kernel's 13-entity domain model (Blueprint B § 2)
does not today carry a `tenant_id`; adding one is a kernel change (`iec-*`) that this spec
flags as `PLANNED` but does not author — schema changes are the kernel's to own (per
`068-AT-STND` § 3.1).

## 3. The three isolation tiers

Tenancy isolation is specified as three tiers of increasing strength. Which tier a tenant
requires is the tenant's **security posture**, not the platform's default. The single-tenant
case today is, in effect, Tier 0.

### 3.1 Tier 0 — shared-process, row-scoped (CURRENT for single tenant)

All tenants (today: one) share the monolith process, store, and Redis. Isolation is enforced
at the **query layer**: every read is scoped by `tenant_id`; a row without a matching tenant
scope is never returned. This is the cheapest tier and is acceptable **only** when every tenant
trusts the platform's row-scoping discipline — i.e., the single-tenant case, or a multi-tenant
case where every tenant has explicitly accepted shared-process isolation.

`REJECTED` at Tier 0: serving a second tenant whose security posture forbids shared-process
isolation. That is precisely the Blueprint B § 5.3 trigger; it escalates to Tier 1 or Tier 2.

### 3.2 Tier 1 — per-tenant worker pods (DEFERRED)

The API tier and storage stay shared and row-scoped (Tier 0), but **worker execution** is
partitioned: each tenant's EvalRuns execute in worker pods dedicated to that tenant, with the
tenant's credential broker instance scoped to that pod set. This contains the blast radius of a
sandbox escape to a single tenant's pods and keeps a tenant's provider credentials physically
separate from another tenant's workers.

This is the **first option** Blueprint B § 5.3 names ("per-tenant worker pods"). It is the
right tier for a tenant that requires execution isolation but tolerates shared row-scoped storage.

### 3.3 Tier 2 — per-tenant deployment (DEFERRED)

The entire stack — API, store, Redis, workers, broker — is deployed per tenant. No bytes of one
tenant's data share infrastructure with another's. This is the **second option** Blueprint B § 5.3
names ("per-tenant deployment") and is the right tier for a regulated-industry tenant requiring
hardware-isolated runtimes or strict data-residency partitioning (Blueprint B § 5.3 fourth
trigger). It is the most expensive tier and is justified only by a posture that Tier 1 cannot meet.

| Tier | Process | Store | Worker exec | Broker | Justifying posture |
| --- | --- | --- | --- | --- | --- |
| 0 (`CURRENT`) | Shared | Shared, row-scoped | Shared sandbox | Shared | Single tenant, or all-trust-shared. |
| 1 (`DEFERRED`) | Shared API | Shared, row-scoped | Per-tenant pods | Per-tenant | Execution isolation needed; shared storage tolerated. |
| 2 (`DEFERRED`) | Per tenant | Per tenant | Per tenant | Per tenant | Hardware isolation / data-residency / regulated vertical. |

## 4. Invariants that hold at every tier

Whatever tier is in force, these invariants are binding (they derive from Blueprint A
principles and Blueprint B § 4.1):

1. **No cross-tenant data read without explicit consent.** (`REJECTED` otherwise.) A tenant's
   rows are never returned to another tenant's user, at any tier. At Tier 0 this is query-layer
   discipline; at Tiers 1–2 it is reinforced by infrastructure partitioning.
2. **Credentials never cross a tenant boundary.** The broker pattern (Blueprint B § 4.1) is
   per-tenant from Tier 1 up; at Tier 0 the single shared broker serves the single tenant.
3. **Sandbox isolation is unconditional.** Evaluated artifacts always run sandboxed (Blueprint B
   § 4.1) regardless of tenancy tier — tenancy adds isolation _above_ the sandbox, never removes it.
4. **Predicate URIs stay platform-global.** Evidence Bundle predicate URIs are
   `evals.intentsolutions.io/<type>/v<version>` for all tenants; tenancy is carried in the row's
   actor/subject fields, not in the URI namespace. (`REJECTED`: per-tenant predicate subdomains.)
5. **Cost ceilings are enforced per tenant.** The bandwidth/budget ceilings (Blueprint A
   principle 8; Blueprint B § 4) roll up per tenant so one tenant cannot exhaust another's quota
   or the platform's aggregate budget.
6. **Fair-queueing generalizes from user to tenant.** Blueprint B § 1 already anticipates this:
   "in the future-tenancy case per iel-E13c, each tenant gets a share of total worker concurrency."
   This spec is that future-tenancy case; the fairness unit becomes the tenant, with users sharing
   their tenant's allocation.

## 5. The build trigger and governance path

Per Blueprint B § 5.3, building any tier above Tier 0 is a **Class-1 ISEDC governance event**
(Blueprint A § 2.3). The procedure when a real second tenant with an incompatible posture appears:

1. **Identify the required tier** from the tenant's security posture (§ 3) — not from a roadmap.
2. **Convene the ISEDC** (Class-1, 7 seats) per Blueprint A § 2.3. The trigger itself is the
   governance event; a Decision Record is produced.
3. **The ISEDC evaluates this spec** against the new constraint and ratifies the tier, the
   `tenant_id` kernel addition, and the per-tenant broker / pod / deployment changes.
4. **Build incrementally**, one module boundary at a time (Blueprint B § 5.2), starting from the
   modular-monolith boundaries already preserved in the codebase.

Until the trigger fires: **single-tenant Tier 0**. This spec does not authorize, schedule, or
recommend building tenancy now. It exists so the design is ready, the kernel impact is known, and
the governance path is pre-walked — so that when a second tenant arrives, the platform answers from
a designed position rather than improvising.

## 6. Anti-goals (the `REJECTED` rows)

- **No cross-tenant data sharing without explicit, recorded consent** — at any tier, forever.
- **No per-tenant predicate URI subdomains** — predicate URIs stay platform-global on `evals.`.
- **No tenancy work built ahead of the § 5.3 trigger** — doc-now, build-later is binding; building
  speculative multi-tenancy is a bandwidth violation (DR-010 § 13.5) and an architecture-calibration
  violation (Blueprint B § 5.3: "calibrated to the present operating reality, not to imagined scale").
- **No relaxation of sandbox or broker isolation to simplify tenancy** — tenancy adds isolation;
  it never subtracts the existing sandbox/broker guarantees.

## 7. Cross-references

- Forward-compatibility trigger this spec satisfies: Blueprint B (`012-AT-ARCH`) § 5.3.
- Runtime isolation + credential broker: Blueprint B § 4.1; DR-010 (`010-AT-DECR`) Q2.
- Weighted-fair-queueing (user → tenant generalization): Blueprint B § 1.
- Governance routing for the build trigger (Class-1): Blueprint A (`011-AT-ARCH`) § 2.3.
- Repo ownership of the `tenant_id` kernel change: `068-AT-STND-core-repo-boundaries-2026-06-18.md` § 3.1.
- Bandwidth-only gate (not customer-signal): DR-010 § 13.5.
