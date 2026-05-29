# DR-035 — ISEDC Session 8: Lab Reports Dashboard (`labs.intentsolutions.io`)

**Date:** 2026-05-29
**Type:** AT-DECR (architectural decision record)
**Acting head:** Jeremy Longshore (CEO-mode delegation; ratification enacted 2026-05-29)
**Convening:** Intent Solutions Executive Decision Council, 7-seat adversarial
**Status:** RATIFIED 2026-05-29
**Supersedes:** Acting-head's prior locks on A1 (host repo = lab) and C2 (internal-default visibility), both unlocked at acting-head's request 2026-05-29
**Pre-flight basis:** 4-reviewer thinker-canon panel (Fowler, Gregg, Karpathy, Armstrong)
**Session artifacts:** `~/.claude/skills/exec-decision-council/sessions/2026-05-29-labs-dashboard/`

---

## 0. Executive summary

Intent Solutions will stand up a public-facing lab reports dashboard at `labs.intentsolutions.io`. ISEDC Session 8 ratified 14 decisions across 4 themes and surfaced 3 net-new bindings beyond the original 12-decision agenda. Two acting-head prior locks were directly challenged and overridden by unanimous-or-near-unanimous council vote.

**Headline outcomes:**

- **A1 host repo:** UNANIMOUS (7/7) override of acting-head lock — new dedicated repo `intent-eval-dashboard` as the 6th member of the platform. Lab stays the constitution repo.
- **C2 default visibility:** 4/4 of primary seats reject acting-head lock — adopt CSO's hybrid (Tier 1 IS-internal eventually-public-with-disclosed-embargo; Tier 2 partner-implicated tiered-by-source with affirmative written consent; Tier 3 third-party case-by-case).
- **C1 tiered access redirect:** internal full view moves OFF public origin onto **tailnet-only hostname** (matches existing Netdata + ntfy pattern). Per-partner basicauth on public origin only, with CISO's 5 lift-over requirements.
- **A3 bi-modal layout:** RATIFIED — TUI **deferred to v0.2.0**; v0.1.0 ships web-only on tailnet-internal + public-anonymous; TUI reserved as v0.2.0+ pending validated demand signal.
- **D3 production-system commitment:** "ops-lite" — ntfy alerts + best-effort waking-hours + public `/status` + CISO's 7-day-silence hard pager threshold; no PagerDuty-grade SLO.
- **Cross-tier policy (net-new from CSO):** tier-2 work (semantic-flux, ICOS) gets ZERO surface until patent clocks run; ICOS removed from supervision tree.
- **D1 sequencing (adopted, not voted):** eval-set browser ships before results browser; CMO amplifies it as THE brand asset (OG image, social card, SEO landing).
- **D4 narrative red-team ownership:** CSO primary (cryptographic = CISO; narrative = CSO); GC consulted on partner-implicated attacks; VP DevRel signal-source for AI-eng community attacks.
- **Bandwidth (CFO):** ~5.6 FTE-weeks MVP. **Queue placement RATIFIED Option C:** eval-set browser MVP (~1.5 FTE-weeks) ships in parallel with `D28-PHASE-A0`; results browser + ingest infrastructure (~4 FTE-weeks) deferred to Skill Refiner Phase C external-wait slot.

---

## 1. Convening + seat roster

| Seat | Lens | Argued |
|---|---|---|
| CTO | Technical correctness, repo topology, build systems | 12 of 14 decisions |
| GC | Legal exposure, IP, partner contracts, disclosure | 5 of 14 |
| CMO | Brand, audience inference, peer-org positioning | 6 of 14 |
| CFO | Bandwidth, cost, opportunity cost, queue placement | 7 of 14 |
| CSO | Strategic signal, partner dynamics, patent clocks, cross-tier | 5 of 14 |
| CISO | Supply-chain security, attack surface, DNS posture | 8 of 14 |
| VP DevRel | Community signal, developer experience, OSS posture | 7 of 14 |

Adversarial-integrity protocol: verbatim positions preserved in session-folder `inputs/seat-*.md`. Steel-manned dissent surfaced. No suppression.

---

## 2. Theme A — Repo + scope

### A1. Host repo

**Outcome:** RATIFIED — new dedicated repo **`jeremylongshore/intent-eval-dashboard`** as the 6th platform repo. UNANIMOUS 7/7 override of acting-head's prior lock on `intent-eval-lab`.

**Vote breakdown:**

| Seat | Vote | Reasoning |
|---|---|---|
| CTO | NEW | Eat-our-own-ecosystem; dashboard is the most visible kernel consumer; Fowler's BoundedContext is technically correct |
| GC | NEW | Litigation-hold + discovery-scope cleanliness; lab repo stays constitution-only |
| CMO | NEW | Brand purity — methodology-authority brand can't co-exist with marketing surface |
| CFO | NEW | 12-month amortized cost is lower; 0.5 FTE-day scaffold once vs ongoing dual-cognitive-load tax on every lab PR |
| CSO | NEW | Strategic signal of architectural seriousness to external technical audiences |
| VP DevRel | NEW | Reference consumer of `@intentsolutions/core` signals "consumable by anyone" far stronger than co-located |
| CISO | NEW | Failure-domain isolation — dashboard deploy key must not inherit lab repo's constitution-authoring authority |

**Implementation directive:** Create `jeremylongshore/intent-eval-dashboard` (Apache 2.0). Vendors `@intentsolutions/core` as published kernel consumer, exactly as any external integrator would. Lab repo CLAUDE.md scope line ("spec + methodology; no build system") is preserved unchanged.

### A2. Lab scope-widening text

**Outcome:** N/A given A1. Surgical widening text from CTO's seat position retained at session-folder `outputs/contingency-a2-lab-scope-widening.md` for record only.

### A3. Bi-modal repo layout (web `site/` + Go TUI `cmd/labs-tui/`)

**Outcome:** RATIFIED — TUI **deferred to v0.2.0**. v0.1.0 ships web-only.

**Acting-head decision:** With C1 redirecting operator-internal view to a tailnet-only web hostname, the original TUI use-case (operator dashboard) is now served by the private web view. TUI's residual value (ssh-only / low-bandwidth / mobile-tethering contexts) does not justify 4 FTE-days against zero validated demand at v0.1.0. CFO's invocation of DR-028 anti-goal discipline (same anti-goal that killed Skill Refiner Phase D) is sound.

**Reservation:** `cmd/labs-tui/` directory + module-path reserved in the dashboard repo from v0.1.0. TUI shipped at v0.2.0+ only with validated demand signal.

---

## 3. Theme B — Trust + integrity

### B1. Render-from-manifest re-verify contract

**Outcome:** RATIFIED BINDING. Both CTO and CISO vote binding-non-negotiable.

**Specification:**
- Pinned OIDC issuer + subject AND `workflow_ref:` claim per source repo (CISO insists `repo:` pinning alone is insufficient — supply-chain compromise can preserve `repo:` while swapping `workflow_ref:`)
- Rekor inclusion-proof verification at ingest, row-by-row
- DSSE signature verification, row-by-row
- Schema validation against `@intentsolutions/core` (kernel-pinned version) at ingest
- Any failure → ingest worker crashes with structured failure reason; staging dir marked `last_known_good_stale_since=<ts>`; renderer uses previous successful snapshot + visible `stale_since` badge

**Hard refusal triggers** (acting head cannot override these): CTO + CISO both refuse to ratify a dashboard that renders unverified manifests.

### B2. Content-address Evidence Bundles into object storage at ingest

**Outcome:** RATIFIED. Storage backend: **local Contabo VPS disk at v0.1.0** (per CFO's 36 GB/year worst-case projection); migrate to **Backblaze B2** (per CISO's GCP-exodus binding) at the 12-month storage review or when local disk projection exceeds 100 GB.

**Constraint:** Storage backend MUST NEVER be GCP (CISO hard refusal, aligns with VPS-as-the-home GCP-exodus program).

**Quarterly credential rotation** for B2 once adopted.

### B3. Sign-your-own-homework (dashboard renders its own attestation)

**Outcome:** RATIFIED SEQUENCED. CTO + CISO concur on sequencing.

**Specification:**
- v0.1.0: STAGING-STAYS-STAGING — no `dashboard-render/v1` predicate URI declared; rendered HTML carries `<meta>` tags pointing at source bundle manifest + ingest snapshot hash, but NO claim of independent verification
- v0.2.0+: introduce `dashboard-render/v1` predicate URI at **`evals.intentsolutions.io/dashboard-render/v1`** (NEVER `labs.*`) only after a second independent verifier exists (e.g., a partner-operated verifier, or a published verification script anyone can run)

**Rationale:** premature sign-your-own-homework is theater (CISO). The attestation only carries weight when a third party can independently re-run the verification.

### B4. Retraction protocol

**Outcome:** RATIFIED with GC's amendments.

**Specification:**
- `retractions.json` denylist in dashboard repo: `{predicate_input_hash, retracted_at, reason_class}`
- **Closed-set `reason_class` taxonomy** (GC binding): `partner-request | methodology-error | data-quality | consent-withdrawn | legal-hold | pre-publication-recall`. **No open-text reason field.** Open reasons are admission-against-interest exposure.
- **4-hour contractual SLO** from retraction request to public tombstone (GC binding)
- Caddy-level kill-switch reads `/etc/caddy/retractions.snippet`; one SSH + `systemctl reload caddy` → 410 Gone at the URL. NO Hugo rebuild required for retraction.
- Each retraction is itself a signed in-toto Statement with predicate type **`retraction/v1`** at `evals.intentsolutions.io/retraction/v1` (CISO binding — predicate URI at evals.* not labs.*)
- Tombstone page states the truth: "this attestation exists in the transparency log and we have chosen not to surface it because `<reason_class>`." Sigstore is append-only — cannot pretend otherwise (Armstrong canonical position).

**Hard refusal triggers:** GC refuses to ratify open-text retraction reasons or any retraction protocol that depends on Hugo/GHA rebuild.

---

## 4. Theme C — Public surface + narrative

### C1. Tiered access model

**Outcome:** RATIFIED with VP DevRel's redirect — internal full view moves OFF public origin onto **tailnet-only hostname**.

**Final access model:**

| Tier | Where | Auth | Audience |
|---|---|---|---|
| Public homepage + opt-in reports | `labs.intentsolutions.io` (anonymous) | None | External technical audience |
| Per-partner views (future) | `labs.intentsolutions.io/<partner-slug>/` | Per-partner basicauth (5 CISO lift-overs apply) | Named partners |
| Operator full internal view | `labs-internal.<tailnet-hostname>` OR `labs-internal.intentsolutions:9999` | Tailscale identity | Acting head (+ later: IS team members on tailnet) |

**Rationale (VP DevRel):** basicauth-locked route on public origin signals "real data behind paywall" to outsiders — worst possible community signal. Tailnet-only hostname for internal view matches existing infrastructure (Netdata at `intentsolutions:19999`, ntfy at `intentsolutions:8080`).

**Anonymous root substance constraint (CMO):** root must carry enough material — eval-set browser, freshness strip, methodology docs, end-to-end signed example — that cold visitors don't read tiers as "real data hidden."

**CISO's 5 lift-overs for per-partner basicauth on public origin (when first per-partner view ships):**
1. 90-day rotation for low-sensitivity; 180-day for high-sensitivity
2. Caddy access-log audit logging enabled per-partner-path
3. Weekly leakage-detection grep job (greps public sources for known basicauth values)
4. Per-partner PATH isolation (not subdomain) — share certificate, scope creds tightly
5. Credentials in `pass` or `/etc/intentsolutions/` mode 600 — NEVER env vars in git, NEVER `.env` files

### C2. Default visibility

**Outcome:** RATIFIED CSO's hybrid — acting-head's prior internal-default lock is OVERRIDDEN.

**Final policy:**

| Source | Default | Override mechanism | Reason |
|---|---|---|---|
| **Tier 1 — IS-internal artifacts** (intent-eval-core, intent-eval-lab, intent-audit-harness, j-rig, intent-rollout-gate, claude-code-plugins) | **Eventually-public with disclosed embargo** | Tag `embargo_until:<date>` on the report; embargo window itself is published metadata | Public status-page precedent: internal-default biases toward optimism, external trust erodes (Gregg canonical) |
| **Tier 2 — partner-implicated artifacts** | **Internal-default + affirmative written consent gate** | Per-partner publication clause required in engagement contract; written sign-off per artifact | No current partner has a publication clause; GC hard refusal otherwise |
| **Tier 3 — third-party non-contract evals** | **Case-by-case** | GC review per artifact | Case-by-case until pattern emerges |

**4 of 4 primary seats** (CMO, GC, CSO, VP DevRel) rejected internal-default. CSO's hybrid synthesizes CMO's eventually-public + GC's tiered-by-source.

**Hard refusal triggers:** CMO refuses to ratify internal-default-as-steady-state. GC refuses to ratify publishing any partner-implicated bundle without written consent.

### C3. NO top-line aggregate PASS% across heterogeneous predicates

**Outcome:** RATIFIED BINDING type-level lock.

**Specification:**
- Schema-level type prevents constructing an aggregate PASS% across rows of mixed predicate semantics
- CI lint enforces — any HTML/MD/JSON output containing `<X>/<N> pass` or `<X>% pass` where the denominator spans multiple predicate URIs fails the lint gate
- Headline slot on landing page is filled by **eval-set browser entry point** (per VP DevRel + CMO): "what we measure" beats "how we did"

**Rationale:** NOT_APPLICABLE ≠ PASS. ADVISORY ≠ PASS. Failure-mode taxonomy not commensurable across runners (Karpathy canonical). Public leaderboard precedent is proof the trap is attractive — and proof of why following it is brand-trust-corrosive (CMO).

**Hard refusal triggers:** CTO + CMO + VP DevRel each independently refuse to ratify any rendering that publishes aggregate PASS%.

### C4. Per-repo freshness + decision-mix strip on landing page

**Outcome:** RATIFIED MANDATORY with CMO's color addendum.

**Specification:**
- Top strip on landing page: one row per source repo, columns = last 24h hourly buckets, color = mix of `{pass, fail, advisory, error, no-data}` of `gate-result/v1` rows ingested in that window (Gregg's "if absent makes dashboard useless" view)
- **`no-data` gets distinct visually-loud color equal weight with `fail`** (CMO addendum) — silent failures must surface as loud as red failures
- USE-method analogues for ingest pipeline itself surface on a `/status` route (CTO's right-sizing of CISO's D3 binding)

**Framing (VP DevRel):** honest ingest-health disclosure, not marketing activity. The strip is the dashboard's `top`-equivalent.

---

## 5. Theme D — Sequencing + operations

### D1. Eval-set browser ships before results browser (CONSTRAINT — adopted, not voted)

**Status:** ADOPTED 2026-05-29 by acting head pre-Session. Carried forward as constraint, not decision.

**Council reinforcement:**
- CMO amplifies: eval-set browser becomes THE brand asset — OG image, social card, SEO landing. Resource it like it IS the product.
- VP DevRel: "publish the spec first" framing aligns with Karpathy's eval-set-as-spec Software 2.0 frame.

**Implementation directive:** First epic ships a versioned, lineage-tracked, adversarially-audited eval-set browser at `labs.intentsolutions.io/eval-sets/`. Results browser is the second epic, derivative of the first.

### D2. Phase A.0 pre-registration rendering symmetry

**Outcome:** RATIFIED BINDING with HTML structural diff CI test + GC pre-pub review + blog-only fallback.

**Specification:**
- New schema field `pre_registration_hash` in Evidence Bundle (NORMATIVE addition; predicate spec evolution)
- Both arms (Naive-Opus-in-context + Refiner) rendered with **identical layout, identical font weights, identical chart axes, identical headline slot** (Karpathy canonical)
- **Null result rendered identically to positive result** — no green/red badges, no "winner" UI, no asymmetric font weighting
- CI test: HTML structural diff between the two arm-rendering paths must produce zero non-trivial diff (CTO binding)
- **GC pre-publication review** for any named-technique comparative claims — protects against named-technique comparative-claim exposure
- **Fallback:** if engineering can't deliver symmetric rendering on the A.0 timeline, **blog-only publication** per VP DevRel's DR-028 binding — never asymmetric dashboard render

**Hard refusal triggers:** VP DevRel refuses asymmetric A.0 dashboard render. CTO refuses A.0 render without HTML structural diff CI test.

### D3. Ingest-pipeline SLO + on-call ownership

**Outcome:** RATIFIED as **"ops-lite"** — threads the needle between CFO's refusal of production-system commitment and CISO's "silent ingest > 7d MUST page" security signal.

**Specification:**
- **Alerting:** ntfy push notifications to `prod-alerts` topic (existing tailnet-only ntfy on VPS). NO PagerDuty, NO email-blast, NO 24/7 rota.
- **Response:** best-effort waking-hours (US Central). No SLO commitment.
- **Public `/status` route:** ingest health, per-repo freshness, last-successful-ingest-per-source visible to anyone. Trust calibration in the open.
- **Hard pager threshold (CISO binding):** `last_successful_ingest > 7d` for any source repo MUST page (security signal — silent ingest is potentially a supply-chain compromise indicator)
- **Public commitment language:** "best-effort, single-operator, see /status for liveness." No "99.9% uptime" claims.

**Tensions resolved:**
- CFO refused production-system commitment with paging — preserved.
- CISO required pager threshold for security signal — preserved as the only paging trigger.
- CTO's right-sizing made the compromise viable.

### D4. Narrative-integrity red-team ownership

**Outcome:** RATIFIED — **CSO primary**, with consultative roles for GC and VP DevRel.

**Specification:**
- **CSO primary:** narrative-integrity red-team is CSO scope extension. Boundary: cryptographic integrity = CISO; narrative integrity = CSO.
- **GC consulted:** on partner-implicated narrative attacks + litigation-narrative adversary scenarios
- **VP DevRel signal-source:** for external technical-audience attacks (community is VP DevRel's listening surface)
- Quarterly narrative-integrity review against current public dashboard surface

**Tension resolution:** GC's preferred "GC + VP DevRel joint, NOT CSO scope-extend" was rejected in favor of CSO's "extend CSO scope" because the cross-functional boundary (crypto/narrative) was cleaner under CSO ownership. GC retains hard refusal authority on partner-implicated narrative attacks.

### NEW. Cross-tier coverage policy

**Outcome:** RATIFIED CSO's hard-line — net-new decision surfaced during deliberation.

**Specification:**
- **Tier 1 platform repos** (intent-eval-core, intent-eval-lab, intent-audit-harness, j-rig, intent-rollout-gate, intent-eval-dashboard, claude-code-plugins): full ingest worker per Armstrong's supervision tree
- **Tier 2 patent-clock projects** (semantic-flux patent clock 2026-06-12, ICOS): **ZERO surface** on `labs.intentsolutions.io` until patent clocks run
- **ICOS removed** from Armstrong's 7-worker supervision tree → revised to 6 workers (iec, iel, iah, iaj, iar, ccp/claude-code-plugins) plus self-ingest from `intent-eval-dashboard` itself (sign-your-own-homework feeder)

**Hard refusal triggers:** CSO refuses to ratify any tier-2 surfacing before patent clocks complete.

### NEW. DNS + CAA + DNSSEC posture (CISO primary)

**Outcome:** RATIFIED as HARD GATE before any labs content publishes.

**Specification:**
- `labs.intentsolutions.io` A-record creation via Porkbun
- **CAA record:** `issue "letsencrypt.org"` only; bans wildcards; no other issuers
- **DNSSEC** zone-signed; DS record published at Porkbun
- **HSTS preload** submission before first published report
- **No CNAME-takeover surface** — labs.* MUST resolve to a static A record, never a CNAME chain
- Verification gate before first content publish

**Hard refusal triggers:** CISO refuses to ratify any content publish before DNS + CAA + DNSSEC + HSTS posture is in place.

---

## 6. Queue placement + bandwidth (RATIFIED Option C)

**CFO bandwidth estimate:** ~5.6 FTE-weeks MVP (64% of Skill Refiner 8.8 FTE-weeks anchor). Co-headline scale, NOT "small follow-on."

**Acting-head decision: Option C — synthesis compromise.**

| Phase | What | Bandwidth | When |
|---|---|---|---|
| Parallel-with-A.0 | Eval-set browser MVP + DNS posture + repo bootstrap | ~1.5 FTE-weeks | Start now in parallel with `D28-PHASE-A0` |
| Phase C external-wait slot | Results browser + ingest infrastructure + supervision tree + ops-lite | ~4 FTE-weeks | Defers to Skill Refiner Phase C external-wait slot |

**Rationale:** Eval-set browser doesn't depend on A.0 outcome (the eval-set is the spec; A.0 tests whether Refiner improves against that spec). CMO's brand-asset framing + VP DevRel's "publish the spec first" binding both pull eval-set browser to the front. If A.0 nulls and Refiner descopes, the eval-set browser still has standalone value as the spec-publication surface. The remaining ~4 FTE-weeks of ingest + results infrastructure honor CFO's bandwidth concern by waiting for A.0 to return.

**Honors CFO's structural-correctness argument** ("spending FTE-weeks before A.0 returns is malpractice") while preserving the CMO/VPDevRel brand-cadence concern.

---

## 7. Acting-head decisions (RATIFIED 2026-05-29)

| # | Decision | Outcome |
|---|---|---|
| 1 | A3 TUI: v0.1.0 inclusion vs defer to v0.2.0 | **DEFER to v0.2.0.** C1's tailnet-only internal web view obviates the original TUI use-case. Reserve `cmd/labs-tui/` module path; ship at v0.2.0+ only with validated demand signal. |
| 2 | Queue placement: Option A / B / C | **Option C — synthesis compromise.** Eval-set browser MVP parallel with A.0 (~1.5 FTE-weeks); results browser + ingest infra deferred to Phase C external-wait slot (~4 FTE-weeks). |
| 3 | Override of unanimous (A1) or near-unanimous (C2, C3) | **NO OVERRIDES.** Council reasoning sound across all three positions; ratified as stated. |

---

## 8. Hard refusal catalog (cannot be silently overridden)

Any future acting-head override of these items must be recorded as formal dissent in a successor DR, with the refusing seat's name + reasoning preserved verbatim:

| Seat | Refusal | Trigger |
|---|---|---|
| CTO | B1 re-verify bypass | Renderer trusting unverified manifests |
| CTO | C3 aggregate PASS% | Any rendering publishing top-line aggregate PASS% across heterogeneous predicates |
| GC | Partner consent | Publishing partner-implicated bundles without written consent |
| GC | Open-text retraction reasons | Any retraction protocol without closed reason_class taxonomy |
| GC | Hugo-dependent retraction | Retraction protocol that requires Hugo/GHA rebuild |
| CMO | Hero-stat / leaderboard | Any aggregate PASS% or leaderboard-style ranking |
| CMO | Internal-default steady-state | Internal-default as the long-term visibility policy |
| CMO | Eval-set deferral | Shipping results browser before eval-set browser |
| CFO | Production SLO with paging | Beyond CISO's 7-day-silence threshold |
| CSO | Tier-2 premature surfacing | semantic-flux, ICOS before patent clocks |
| CSO | Narrative red-team bypass | Skipping CSO narrative-integrity review |
| VP DevRel | C3 aggregate PASS% | (Independent refusal — same as CTO + CMO) |
| VP DevRel | Public-origin basicauth on operator views | Operator full view on public origin (must be tailnet) |
| VP DevRel | Asymmetric A.0 render | Phase A.0 dashboard render that differs structurally between arms |
| CISO | DNS/CAA/DNSSEC bypass | Publishing any labs content before posture in place |
| CISO | B1 bypass | Same as CTO B1 refusal — independent |
| CISO | Co-located deploy keys | Dashboard sharing lab repo's deploy key authority |
| CISO | Premature B3 | Sign-your-own-homework before second independent verifier exists |
| CISO | Predicate URI at labs.* | Any predicate URI declared under labs.intentsolutions.io (must be evals.*) |
| CISO | GCP object storage | Storage backend on GCP (violates VPS-as-the-home exodus) |

---

## 9. Implementation directives (binding)

1. **Create repo** `jeremylongshore/intent-eval-dashboard` (PUBLIC, Apache 2.0)
2. **DNS posture** (BLOCKING first publish): A-record + CAA + DNSSEC + HSTS preload
3. **First epic:** eval-set browser MVP — versioned, lineage-tracked, adversarially-audited at `labs.intentsolutions.io/eval-sets/`
4. **Tailnet-only hostname** for internal view (`labs-internal.<tailnet-hostname>`)
5. **Schema evolution:** new fields `pre_registration_hash` (D2) and new predicate types `retraction/v1` + `dashboard-render/v1` at `evals.intentsolutions.io/*` (B3, B4) — kernel `@intentsolutions/core` v0.2.0 carries these
6. **Caddy block** with `/etc/caddy/retractions.snippet` include directive
7. **Storage:** local Contabo disk to start; B2 migration triggered at 12-month review or 100 GB
8. **CI gates:** B1 re-verify contract, C3 aggregate-PASS% lint, C4 freshness-strip render check, D2 HTML structural diff for Phase A.0
9. **Ingest worker supervision tree** (Armstrong): 6 workers (iec, iel, iah, iaj, iar, ccp); ICOS struck per cross-tier policy
10. **Sequencing:** eval-set browser → results browser → Phase A.0 pre-registration rendering (D2 schema field lands BEFORE A.0 results)
11. **TUI reservation:** `cmd/labs-tui/` directory + module-path reserved from v0.1.0; TUI implementation deferred to v0.2.0+ pending validated demand
12. **Queue placement:** eval-set browser MVP (~1.5 FTE-weeks) ships parallel with `D28-PHASE-A0`; remaining ~4 FTE-weeks defer to Skill Refiner Phase C external-wait slot

---

## 10. Beads + GH + Plane mirror plan

Plan-file to be authored at `~/.claude/plans/intent-solutions-lab-reports-<color>-<noun>.md` (random color-noun slug per established pattern).

Epic structure:
- **Umbrella epic:** "Public lab reports dashboard at labs.intentsolutions.io"
  - Children clustered by theme: A (repo + scope), B (trust + integrity), C (public surface), D (sequencing + ops), DNS posture, cross-tier policy

Three-layer mirror via `bd-sync`:
- bd workspace: `~/000-projects/.beads/` (existing IEP workspace; new prefix `ied-` for intent-eval-dashboard)
- GH umbrella issue: `jeremylongshore/intent-eval-dashboard#1` (created with repo)
- Plane LAB-N (new module under LAB project)

---

## 11. Open follow-ups (post-ratification)

1. **Plan file authoring** — random color-noun slug per pattern, replacing the current "Merge PR #85 + dismiss Slack warning" tactical-wrap-up file at `~/.claude/plans/se-the-council-bubbly-frog.md`
2. **Epic + bead filing** with three-layer mirror via `bd-sync`
3. **Create `jeremylongshore/intent-eval-dashboard` repo** (PUBLIC, Apache 2.0)
4. **Schema evolution PR** to `intent-eval-core` for v0.2.0: new field `pre_registration_hash`, new predicate types `retraction/v1` + `dashboard-render/v1`
5. **DNS work**: `labs.intentsolutions.io` A-record + CAA + DNSSEC + HSTS preload via Porkbun + VPS
6. **PR #85 merge + Slack residual-risk note** ride along as tactical wrap-ups in the new plan's "open tactical wrap-ups" footnote — preserved across this strategic-pivot

---

## 12. Signature

Acting head: **Jeremy Longshore** (CEO-mode delegation; ratification enacted 2026-05-29 by Claude in CTO-mode per established delegation pattern; subject to acting-head override if reviewed)
Council session date: **2026-05-29**
Verbatim seat positions preserved at: `~/.claude/skills/exec-decision-council/sessions/2026-05-29-labs-dashboard/inputs/seat-*.md`
Pre-flight thinker-canon at: `~/.claude/skills/exec-decision-council/sessions/2026-05-29-labs-dashboard/inputs/0X-thinker-canon-*.md`
Synthesis: `~/.claude/skills/exec-decision-council/sessions/2026-05-29-labs-dashboard/inputs/00-synthesis.md`

Adversarial-integrity protocol: observed. Dissent preserved.
