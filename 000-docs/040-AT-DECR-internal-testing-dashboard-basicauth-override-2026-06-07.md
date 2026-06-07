# DR-040 — Internal testing dashboard: basicauth on a new named gated surface (acting-head override of DR-035 § 8)

**Date:** 2026-06-07
**Type:** AT-DECR (architectural decision record)
**Acting head:** Jeremy Longshore (CEO-mode delegation; enacted by Claude in autonomous-CTO mode)
**Status:** RATIFIED 2026-06-07 (acting-head; ISEDC NOT convened — see § 5)
**Authority:** DR-035 (ISEDC Session 8 — labs dashboard architecture) § 8 + the C1 tiered-access decision; DR-010 § 5 + CISO predicate-URI binding
**Beads:** `bd_000-projects-nr75.6` (the gate) — recorded by this DR. Cluster epic: `bd_000-projects-nr75` (reports hub) + `bd_000-projects-awe3` (internal-ops-portal).
**Companion:** `intent-eval-dashboard/000-docs/002-DR-RFC-internal-testing-dashboard-design-2026-06-07.md`; `intent-eval-dashboard/deploy/internal-testing.caddy`; `intent-eval-dashboard#18`.

---

## 0. Executive summary

The internal testing dashboard (Pillar 1 of the internal-ops-portal — per-repo coverage / mutation / CRAP / architecture / escape-scan results, **taught**) is to be served behind **HTTP basic auth on a public origin** at `internal.intentsolutions.io`, so it is readable from any device behind a password.

DR-035 § 8 carries a ratified hard refusal that this contradicts:

> **"No basicauth on public origin for operator views — operator-internal goes tailnet-only."** (VP DevRel refusal. Rationale: a basicauth-locked route on the public origin signals "real data behind a paywall" to outsiders — the worst possible community signal.)

This DR records the **acting-head decision to override that refusal for one specific, narrowly-scoped surface**, under the same five CISO lift-overs DR-035 already attaches to per-named-view basicauth on a public origin. Per the repo binding that a hard-refusal violation "requires formal dissent recording in a successor DR," this is that record. The original dissent is preserved verbatim (§ 4).

## 1. Decision

1. **The internal testing dashboard is a NEW named gated surface**, served behind Caddy basic auth at `internal.intentsolutions.io`, distinct from the "operator full internal view" that DR-035 § 8 routes tailnet-only.
2. **The pre-existing tailnet-only operator-RESULTS view** (`intent-eval-dashboard` puxu.9, `site-internal/internal/results/`, Tailscale identity) is **UNCHANGED.** This DR does not move it to basicauth.
3. **CISO's five lift-overs (§ 3) are mandatory** before exposure. They are committed in-repo as deploy artifacts (`deploy/internal-testing.caddy` + `deploy/fail2ban/`).
4. **The CISO predicate-URI binding stands undisturbed:** no in-toto predicate URI, OTel attribute namespace, or attestation predicate identifier may be declared at `labs.*` OR `internal.*`. Predicate URIs live ONLY at `evals.intentsolutions.io`. The testing dashboard only ever _renders_ predicate URIs (pointed at `evals.*`); it declares none.

## 2. Why the override is sound (and narrow)

The VP DevRel refusal protects one thing: the **community-facing signal** of the public labs surface. A password wall on `labs.intentsolutions.io` would tell every outsider "the real data is paywalled" — corrosive to an open project's credibility.

This surface does not carry that signal:

- It is a **separate hostname** (`internal.intentsolutions.io`), not a locked route on the community face. `labs.intentsolutions.io` stays fully open, unchanged.
- It is **`noindex, nofollow`** and is never linked from any public page — outsiders do not encounter it and infer a paywall.
- Its purpose is **operator/learning**, not marketing: it is the windshield for "are our own tests healthy and what do I fix," for the operator and (later) internal team members.
- The product requirement — _open it in a browser from any device behind a password_ — is not met by the tailnet-only gate (which requires a tailnet-joined device); basicauth on a public origin is the mechanism that satisfies it.

The override is therefore **scoped to this one named surface** and does not relax the refusal for the public origin or for the operator-results view.

## 3. CISO's five lift-overs (mandatory, committed in-repo)

These are the same lift-overs DR-035 § 8 attaches to per-named-view basicauth on a public origin. Each is honored as a committed artifact or documented deploy step:

1. **TLS, LE-only, CAA-pinned.** Caddy auto-provisions Let's Encrypt; the zone CAA forbids other CAs; DNSSEC inherited. (`internal-testing.caddy`.)
2. **Credential rotation.** The bcrypt credential lives in `pass internal-dashboard/basicauth-*`, never committed; rotate on the standing schedule (re-run `caddy hash-password` + reload).
3. **Weekly leakage-detection grep.** An off-host weekly job greps public sources (the repo, gists, the public site) for the known credential value and alerts on a hit.
4. **Rate-limit.** `caddy-ratelimit` (if built into the VPS binary) or the committed `deploy/fail2ban/` jail (filter + jail on the basicauth access log) — required before exposure. No basicauth surface ships without a brute-force throttle.
5. **Audit log.** A dedicated JSON access log (`/var/log/caddy/internal-testing.access.log`) makes every gated request attributable; retained per ops policy and consumed by the fail2ban jail.

## 4. Dissent preserved (DR-035 § 8, VP DevRel — verbatim)

> Public-origin basicauth on operator views: operator full view must be on the tailnet, not the public origin. A basicauth-locked route on public origin signals "real data behind paywall" to outsiders — worst possible community signal. Tailnet-only hostname for internal view matches existing infrastructure (Netdata, ntfy).

**Acting-head response:** upheld for the labs community face and for the operator-results view; overridden only for the separate, unindexed, never-publicly-linked `internal.intentsolutions.io` testing surface, where the "paywall signal" concern does not apply and the off-tailnet-readability requirement does. Should this surface ever be linked from the public site, host predicate URIs, or otherwise acquire a community-facing signal, this override LAPSES and the question returns to ISEDC.

## 5. Process note

ISEDC was **not convened** for this decision (per directive: skip the council for this work). This is an acting-head record under CEO-mode delegation, not a council session — the lighter instrument the repo binding permits ("formal dissent recording in a successor DR") for a narrowly-scoped override. The full seven-seat council remains the instrument for anything that widens the scope (a new public-facing gate, a predicate-URI placement, or a brand commitment).

## 6. Consequences

- `intent-eval-dashboard` ships the testing render lane to `site-internal/internal/testing/` (PR #18) and the gate artifacts (`deploy/internal-testing.caddy`, `deploy/fail2ban/`).
- VPS wiring (rsync, set credential, set `IEP_INTERNAL_ROOT`, install the fail2ban jail, `caddy validate` + reload, DNS) is the human-gated ops step under `bd_000-projects-nr75.6`.
- DR-035's other § 8 refusals (no aggregate PASS%, no partner-implicated publication without consent, no predicate URIs at labs, no uptime SLA, verify-before-render, etc.) remain fully in force; this DR touches only the basicauth-on-operator-view refusal, only for this surface.
