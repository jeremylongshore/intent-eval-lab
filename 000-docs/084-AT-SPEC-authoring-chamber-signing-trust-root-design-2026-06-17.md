---
date: 2026-06-17
authors:
  - Jeremy Longshore (Intent Solutions, acting head of board)
status: NORMATIVE
state_label: NORMATIVE
binding_authority: ISEDC — DR-081 Q3 (SAK charter, no-shared-trust-root, BINDING & IMMUTABLE) + DR-082 Q3 (skill-refiner-pass/v1 production trigger 3)
inherits_from: 081-AT-DECR-isedc-sak-class-1-charter-ratification-2026-06-17.md (Q3 — the no-shared-root mandate this document designs the realization of)
master_plan: ~/.claude/plans/se-the-council-bubbly-frog.md
epic: bd_000-projects-rqwk (RC-IEL — refiner coordination, lab)
bead: bd_000-projects-rqwk.1
filing_standard: Document Filing Standard v4.3
related_drs:
  - 081-AT-DECR (SAK Class-1 charter — Q3 bicameral isolation; CFO "provisioned but DORMANT" framing; lint-not-attestation wall)
  - 082-AT-DECR (skill-refiner-pass/v1 — Q3 trigger 3; Q4 CISO divergence-b keyid→authoring-Fulcio binding)
  - 010-AT-DECR (S4 — production-Rekor sequencing; DNSSEC + CAA pre-condition)
  - 004-AT-DECR (S1 — predicate URI namespace; evals.* only)
scope: DESIGN ONLY — provisioning is maintainer-run infra; see § 5 PROVISIONING STEPS + § 6 BLOCKED-ON
forward_refs:
  - 083-AT-SPEC-skill-refiner-pass-v1-normative-spec (the predicate this trust root signs; § 6 trigger 3 there points here)
---

# Authoring-Chamber Signing Trust Root — Design

> **State label: NORMATIVE (design).** This document specifies the **design** of
> the authoring chamber's distinct signing trust root, per DR-081 Q3 (RATIFIED AS
> BINDING & IMMUTABLE: "NO shared signing trust root between runtime and authoring
> chambers") and DR-082 Q3 trigger 3 ("the authoring chamber's SEPARATE signing
> trust root is provisioned-and-live"). Landing this design **advances** DR-082
> Q3 trigger 3 — it does NOT satisfy it. **Satisfying** trigger 3 requires the
> maintainer-run provisioning in § 5; provisioning is security infrastructure a
> human runs, not something a document can complete. Be honest about that line:
> this is the blueprint, § 5 is the build, § 6 is what blocks the build.

> **Honesty about what "trust root" means in the keyless model.** The runtime
> chamber signs with **cosign keyless against the public-good sigstore trust
> root** (`fulcio.sigstore.dev` + `rekor.sigstore.dev`), using GitHub Actions
> ambient OIDC (issuer `https://token.actions.githubusercontent.com`). Both
> chambers use that same public CA + transparency log — you do not stand up a
> private Fulcio to "separate roots." In the keyless model the chamber boundary
> that satisfies DR-081 Q3 is the **distinct OIDC certificate identity** (a
> distinct GitHub Actions workflow-ref, in a distinct signing repo/workflow),
> which a verifier pins with `--certificate-identity[-regexp]` +
> `--certificate-oidc-issuer`. "No shared signing trust root" is realized as **no
> shared signing identity** — the authoring chamber MUST NOT be signable by the
> runtime chamber's identity, and vice versa. This is exactly the multi-root PKI
> idiom "same format, different signer" (DR-082 Q4 VP DevRel). If a future
> deployment moves to key-based signing, the separation becomes two distinct
> keypairs with no shared private material; the design below states both.

---

## 1. Why a separate trust root at all

DR-081 Q3 ratified, 7–0, BINDING & IMMUTABLE: the authoring chamber gets NO
shared signing trust root with the runtime chamber. The threat the council named
(CTO/GC/CSO/CISO, verbatim DR-081 Q3):

- **Confused-deputy / blast-radius coupling.** A shared signing identity means a
  runtime-contract compromise (the key/identity that signs `gate-result/v1` et al.)
  *also* implicates every authoring attestation, and vice versa — one breach, two
  chambers down. A signed Rekor row is forever-proof of the coupling.
- **Trust-class confusion (the lint-vs-attestation wall).** `authoring/v1`
  *conformance* (a SKILL.md passing a kernel JSON Schema) is a DETERMINISTIC LINT
  RESULT, never a signed attestation. `skill-refiner-pass/v1` is the genuine
  exception: it IS a signed behavioral-gate attestation, runtime-class in
  *kind* but emitted from the authoring/refiner chamber. Precisely because the
  chamber also produces non-signable lint results, its one signable predicate
  must sign under an identity a verifier can tell apart from the runtime chamber —
  so nobody can wire a "kernel schema PASS" lint into the authoring signing
  identity and manufacture an unaudited attestation.

The chamber boundary is therefore enforced **cryptographically at the signing
identity** (the keyid the DSSE signature resolves to), never structurally in the
URL string (DR-082 Q1) or the in-toto envelope (DR-082 Q4). Same wire format,
different signer.

---

## 2. The two chambers, side by side

| Property | Runtime chamber (`gate-result/v1`, …) | Authoring chamber (`skill-refiner-pass/v1`) |
| --- | --- | --- |
| **What it signs** | runtime/eval predicates (gate-result, eval-verdict, runtime-receipt, cost-attribution) | the authoring chamber's ONE signable predicate: `skill-refiner-pass/v1` (the refiner behavioral-gate PASS) |
| **Signing model** | cosign keyless, public-good sigstore | cosign keyless, public-good sigstore (SAME CA + log) |
| **Fulcio** | `fulcio.sigstore.dev` (default) | `fulcio.sigstore.dev` (default) — **shared CA, by design; the root is NOT what separates the chambers** |
| **Rekor** | `rekor.sigstore.dev` (production) / `rekor.sigstage.dev` (staging) | same instances; staging until DR-082 Q3 all-four hold |
| **OIDC issuer** | `https://token.actions.githubusercontent.com` (GitHub Actions ambient) | `https://token.actions.githubusercontent.com` (GitHub Actions ambient) |
| **OIDC certificate identity** | the runtime signing **workflow-ref** (e.g. the `intent-rollout-gate` release workflow ref) | a **DISTINCT workflow-ref** — the authoring/refiner signing workflow, ideally in a distinct signing repo/workflow file (§ 3). **This is the separation.** |
| **`$schemaVersion` lane** | runtime lane | independent authoring lane (DR-081 Q3) — runtime bumps never drag it |
| **Evolution clock** | runtime ISEDC cadence | independent authoring ISEDC cadence (DR-082 Q5 CSO) |
| **Carrying cost while idle** | live (already signs to production) | **DORMANT until first signed artifact** (DR-081 Q3 CFO binding — zero key-rotation cost until the chamber actually emits a signed row) |

The single load-bearing difference is the **OIDC certificate identity**. Everything
else a verifier checks (envelope, predicateType string, schema) is intentionally
identical so off-the-shelf cosign / in-toto tooling Just Works (DR-082 Q4).

---

## 3. The authoring signing identity (the design)

The authoring chamber's signing identity is a **dedicated GitHub Actions
workflow** whose `workflow_ref` is the cosign keyless certificate identity. It
MUST be distinct from the runtime chamber's signing workflow such that the two
`--certificate-identity-regexp` patterns are **mutually exclusive** — no string
matches both.

Design constraints (NORMATIVE):

1. **Distinct workflow-ref.** The authoring signing job MUST live in its own
   workflow file (and SHOULD live in its own signing repo or a clearly-namespaced
   path) so its `job_workflow_ref` differs from any runtime signing workflow. The
   recommended identity shape is a GitHub Actions reusable-workflow ref pinned to
   a tag, e.g. a regexp of the form
   `^https://github.com/<authoring-signing-repo>/\.github/workflows/<authoring-sign-workflow>\.yml@refs/tags/.+$`.
   The exact repo/workflow strings are fixed at provisioning (§ 5) and then
   recorded back into § 083 § 7's verifier command and into `PREDICATE-TYPES.md`.
2. **Mutual exclusion with the runtime identity.** The runtime chamber signs
   `gate-result/v1` from its own workflow-ref. A CI/verifier assertion MUST
   confirm the authoring identity regexp and the runtime identity regexp do not
   both match any single certificate-identity string. A `skill-refiner-pass/v1`
   row whose certificate identity resolves to the runtime workflow is INVALID
   (DR-082 Q4 CISO divergence-b: "an authoring predicate signed by a
   runtime-chamber keyid is INVALID").
3. **Least privilege.** The authoring signing workflow requests
   `id-token: write` (for keyless Fulcio OIDC) and `contents: read` only. It MUST
   NOT carry the runtime chamber's deploy/publish permissions.
4. **Dispatch-only, dry-run-default, pre-flight-gated** — mirror the runtime
   chamber's production-signing safety posture (the `intent-rollout-gate`
   release.yml model): production signing is `workflow_dispatch`-only, defaults to
   dry-run (real Fulcio cert + SCT verification, NO Rekor write), and aborts
   before cosign ever runs if the iah-E06-class DNSSEC/CAA pre-flight on
   `evals.intentsolutions.io` is not green. The reversible part (the Rekor write)
   is the only thing the non-dry-run path adds.
5. **Staging by default.** Until DR-082 Q3's four triggers all hold, the workflow
   targets `rekor.sigstage.dev` and emits `signing_mode = sigstore_staging`,
   `rekor_log_index = null`.
6. **Key-based fallback (if ever used).** If a deployment elects cosign key-based
   signing instead of keyless, the authoring chamber MUST use a keypair with NO
   shared private material with the runtime chamber, discoverable via a distinct
   deterministic mechanism (distinct `cosign.pub` / keyref). Keyless is the
   reference flow; this is stated only so "no shared root" has a concrete
   key-based reading too.

---

## 4. Kernel `SigningMode` wiring (how `staging → production` flips, per-chamber)

The kernel `SigningMode` enum (`@intentsolutions/core`,
`src/entities/EvidenceBundle.ts`) is the closed 3-element set:

```ts
type SigningMode = 'sigstore_staging' | 'rekor_production' | 'unsigned_experimental';
```

(The `skill-refiner-pass-v1.ts` kernel header refers to the staging posture by
the shorthand `ln`; the enum value is `sigstore_staging`.)

Wiring rules (NORMATIVE — design intent for the emit path that ships once
`@core` is published and the chamber is live):

1. **Per-predicate, per-chamber — not global.** The `gate-result/v1` runtime
   predicate may be at `rekor_production` while `skill-refiner-pass/v1` is still
   at `sigstore_staging`. The flip is decided independently for each predicate
   under its chamber's trigger set. A global "production on" switch would violate
   the per-chamber-isolation invariant.
2. **The flip is the EFFECT of the four DR-082 Q3 triggers, never a trigger
   itself** (DR-082 Q3 CISO). The emit path MUST resolve `skill-refiner-pass/v1`'s
   mode to `rekor_production` ONLY when ALL of: (1) § 083 normative section landed;
   (2) DNSSEC + CAA green on `evals.intentsolutions.io`; (3) this authoring trust
   root provisioned-and-live (§ 5); (4) ≥1 real SkillVersion cleared the gate on a
   frozen signed eval-set. Otherwise it resolves to `sigstore_staging`.
3. **Cross-field invariant (DR-028 T1 deferred-fields).** A row/bundle with
   `signing_mode = rekor_production` MUST carry a non-null `rekor_log_index`; a
   row with `signing_mode = sigstore_staging` MUST carry `rekor_log_index = null`.
   This is the "`rekor_log_index` iff `signing_mode = production`" invariant. NOTE:
   the SkillVersion entity's status/signing-surface fields (`status`,
   `signing_mode`, `rekor_log_index`, `pending_production`, and the cross-field
   invariant enforcement on the entity) were DEFERRED by DR-028 T1 (line 105) to a
   follow-up DR — see § 6 blocked-on. This design specifies the intended wiring;
   the kernel enforcement of the SkillVersion-side invariant lands when that
   follow-up DR ratifies.
4. **STAGING-STAYS-STAGING (DR-018).** A row signed in staging is never
   retro-promoted. The flip changes the mode for FUTURE rows; it never rewrites a
   signed staging row into a production one.

---

## 5. PROVISIONING STEPS (maintainer-run)

> **These steps are infrastructure a maintainer runs. A document cannot complete
> them.** They satisfy DR-082 Q3 trigger 3 ("provisioned-and-live"). Until they
> are done, trigger 3 is NOT met and `skill-refiner-pass/v1` stays in
> `sigstore_staging` regardless of how many docs land. Per DR-081 Q3 (CFO), the
> identity stays **DORMANT** (provisioned but not yet emitting) until the first
> signed artifact — there is no live key-rotation / monitoring carrying cost for a
> chamber that has not yet signed.

1. **Create the authoring signing workflow** (distinct workflow-ref per § 3) — a
   dedicated reusable workflow with `permissions: { id-token: write, contents: read }`,
   `workflow_dispatch`-only, dry-run-default, iah-E06 pre-flight gate before any
   cosign invocation. Mirror the runtime `release.yml` safety scaffolding; do NOT
   copy its deploy permissions.
2. **Fix the authoring OIDC certificate identity strings** — record the exact
   `--certificate-identity-regexp` and `--certificate-oidc-issuer` the chamber
   signs under. Confirm by inspection that they are MUTUALLY EXCLUSIVE with the
   runtime chamber's identity regexp.
3. **Wire the mutual-exclusion assertion into CI** — a check that fails if the
   authoring and runtime identity regexps can both match a single string (the
   machine proof of "no shared signing identity").
4. **Verify the iah-E06-class pre-flight is green** for `evals.intentsolutions.io`
   (DNSSEC + CAA) — already green for the runtime chamber; this is verify-still-green.
   (This is DR-082 Q3 trigger 2; it shares the host posture, so confirming it for
   the authoring chamber is a re-verification, not a rebuild.)
5. **Staging round-trip** — sign a `skill-refiner-pass/v1` row to
   `rekor.sigstage.dev` under the authoring identity and confirm
   `cosign verify-attestation` succeeds with the authoring identity regexp and
   FAILS with the runtime identity regexp. This proves the separation end-to-end
   before any production write.
6. **Record the identity back into the spec + registry** — update § 083 § 7's
   reference verifier command with the concrete authoring identity strings, and
   record the chamber's signing identity in `specs/PREDICATE-TYPES.md` alongside
   the skill-refiner-pass/v1 row.
7. **(Production, later — gated on all four DR-082 Q3 triggers + the Q3 separate
   ISEDC go several seats requested.)** Only after triggers 1, 2, 3, 4 all hold do
   you run the workflow with dry-run=false to write the first
   `rekor.sigstore.dev` row. The first production row is the single irreversible
   event (DR-082 Q3 CISO); it MUST NOT fire before the staging round-trip (step 5)
   proves the authoring identity is distinct-and-verifiable.

---

## 6. BLOCKED-ON (what gates this design from becoming "live")

This design is buildable now. Turning it into a *live, provisioned* trust root —
and thereby clearing DR-082 Q3 trigger 3, and ultimately enabling the first
production `skill-refiner-pass/v1` signature — is blocked on the following, none
of which a document can clear:

| Blocked-on | Kind | Who clears it |
| --- | --- | --- |
| Provisioning the authoring signing workflow + fixing/recording its OIDC identity (§ 5 steps 1–6) | **Infra (maintainer-run)** | maintainer |
| `@intentsolutions/core` PUBLISHED with the `skill-refiner-pass/v1` predicate body + the `SkillVersion` entity (currently on `main` at 0.7.0-dev but UNPUBLISHED) — any j-rig emit path that imports them is blocked until publish | **Release (maintainer-run)** | maintainer |
| The DR-028 T1-deferred SkillVersion status/signing-surface fields (`status`, `signing_mode`, `rekor_log_index`, `pending_production`) + the "`rekor_log_index` iff `signing_mode=production`" CISO cross-field invariant on the SkillVersion entity | **Decision (ISEDC follow-up DR)** + kernel work | ISEDC + maintainer |
| ≥1 REAL SkillVersion clears the `@j-rig/refiner-core` behavioral gate on a FROZEN, signed eval-set (DR-082 Q3 trigger 4) | **Real run** (needs the publish above + a frozen eval-set) | maintainer |
| The "separate ISEDC production-go" several DR-082 Q3 seats (GC/CFO/CSO/VP-DevRel) requested before the first production signature | **Decision (Class-1 ISEDC)** | ISEDC |

**What this document DOES advance:** DR-082 Q3 trigger 3's **design** — the
chamber's signing topology, the keyid-distinct identity model, the kernel
`SigningMode` wiring, and the exact maintainer provisioning runbook. **What it
does NOT do:** stand up the identity, publish `@core`, run a real refiner, or hold
the ISEDC production-go. Those are infra, release, and decision events — honestly
out of a doc's reach.

---

## 7. References

- The no-shared-root mandate (the binding this realizes): `081-AT-DECR-isedc-sak-class-1-charter-ratification-2026-06-17.md` § Q3
- The predicate this root signs + its four production triggers: `083-AT-SPEC-skill-refiner-pass-v1-normative-spec-2026-06-17.md` + `082-AT-DECR-isedc-skill-refiner-pass-v1-predicate-uri-2026-06-17.md` § Q3
- The keyid→authoring-Fulcio binding (cryptographic chamber separation): `082-AT-DECR-...` § Q4 CISO divergence-b
- The runtime chamber's reference production-signing posture (the safety scaffolding to mirror, NOT the identity to reuse): `intent-rollout-gate/.github/workflows/release.yml` (cosign keyless, public-good trust root, dispatch-only, dry-run-default, iah-E06-gated)
- Kernel `SigningMode` enum: `@intentsolutions/core` `src/entities/EvidenceBundle.ts`
- DNSSEC + CAA pre-flight (trigger 2): iah-E06 (audit-harness); `evals.intentsolutions.io` host posture shared with the runtime chamber
