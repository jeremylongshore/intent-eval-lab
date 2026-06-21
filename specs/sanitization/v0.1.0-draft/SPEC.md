# Agent-Loop-Trace Sanitization Spec — v0.1.0-draft

> **Status: NORMATIVE DRAFT.** This specification defines the sanitization discipline that
> an agent-loop trace MUST pass before any portion of it may be embedded in a signed
> in-toto Statement and pushed to a transparency log under the
> `https://evals.intentsolutions.io/agent-loop-trace/v1` predicate URI.
>
> **Gating notice.** The `agent-loop-trace/v1` predicate URI is **REJECTED for v1** per
> DR-010 § 7 Q3 (ISEDC Session 4, CISO veto), recorded in
> [`specs/PREDICATE-TYPES.md`](../../PREDICATE-TYPES.md) REJECTED registry. The veto's
> stated trigger to revisit (FUTURE.md "Deferred predicate URIs" → REJECTED, and
> PREDICATE-TYPES.md REJECTED row) is: **a trace-sanitization spec is authored AND passes
> the CISO PASS/FAIL sanitization-test fixture in CI.** This document is that spec; the
> fixture suite (§ 7) is that fixture set. Authoring this spec does **not** un-reject the
> URI — un-rejecting and reserving it is a **Class-1 ISEDC act** (DR-010 § 7 Q6). This spec
> supplies the precondition; the reservation is a separate council act.
>
> **Authority precedence.** Where this spec touches the Evidence Bundle envelope, signing,
> or the predicate registry, the canonical
> [`specs/evidence-bundle/v0.1.0-draft/SPEC.md`](../../evidence-bundle/v0.1.0-draft/SPEC.md)
> and the kernel schema win on conflict (Blueprint B § 7.0). This spec adds the
> **sanitization layer** that sits _before_ emission; it does not redefine the envelope.

## 1. Purpose

An **agent-loop trace** is the execution lineage of an agent run — the `SessionTrace`
(canonical glossary § 2.10): the DAG of `ToolInvocation` events, retries, `JudgeDecision`
events, prompts sent to providers, tool-call arguments, tool outputs, and agent reasoning
text. It is the platform's richest forensic surface and its most dangerous one. The DR-010
§ 7 Q3 CISO veto states the threat precisely: loop traces _"contain prompts, tool calls,
credential-shaped strings, agent reasoning. Permanent Rekor record of potentially
sensitive trace data is unacceptable."_ (FUTURE.md, REJECTED for v1.)

The threat model is **write-once permanence.** A Rekor entry is immutable; a transparency
log cannot be un-published; a credential leaked into a signed attestation is a credential
leaked into a public, permanent, globally-replicated record — and, by way of public
training corpora, potentially into a provider's model weights. This is the CISO's named
failure mode: _"permanent credential leakage to provider training corpus; not recoverable"_
(DR-010 § 8 CISO memo).

This spec defines the **sanitization pipeline** every loop trace MUST pass before any of its
content is embedded in a `agent-loop-trace/v1` row: prompt redaction (§ 4), tool-call-arg
sanitization (§ 5), agent-reasoning summarization (§ 6), and the PASS/FAIL conformance
fixtures (§ 7) that prove the pipeline works.

## 2. Scope

### 2.1 In scope (v0.1.0-draft)

| Concern                                                                  | Where |
| ------------------------------------------------------------------------ | ----- |
| The sanitization pipeline ordering + the fail-closed boundary            | § 3   |
| Prompt-redaction rules (the prompt body sent to a provider)              | § 4   |
| Tool-call-argument sanitization rules (the `args` of a `ToolInvocation`) | § 5   |
| Agent-reasoning summarization rules (chain-of-thought / reasoning text)  | § 6   |
| PASS/FAIL conformance fixture suite (the CISO non-negotiable)            | § 7   |
| Residual-risk handling + emission refusal                                | § 8   |

### 2.2 Out of scope (v0.1.0-draft)

- **The `agent-loop-trace/v1` predicate body schema.** This spec gates emission; the
  predicate body schema is a kernel concern reserved by a future Class-1 act (Blueprint B
  § 7.0; PREDICATE-TYPES.md). Until the URI is reserved, **no** `agent-loop-trace/v1` row is
  emitted regardless of sanitization status.
- **The credential broker.** Provider-response redaction at the runtime boundary (Blueprint
  B § 4.1) is a sibling control. This spec composes with it (§ 3 R3) but does not redefine
  it.
- **General PII compliance regimes** (GDPR, CCPA). This spec defends against credential and
  secret leakage into immutable transparency logs; it is a necessary, not a sufficient,
  control for a regulated-PII program.
- **Non-trace evidence.** `gate-result/v1`, `cost-attribution/v1`, etc. carry digests and
  enums by construction (`067-AT-SPEC` § 5) and are out of scope here.

## 3. Conformance keywords + pipeline ordering

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY** are used per
[RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) /
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174).

### R1 — The pipeline is ordered and total

Every loop-trace artifact considered for emission MUST pass, in order:

1. **Prompt redaction** (§ 4) over every prompt body.
2. **Tool-call-arg sanitization** (§ 5) over every `ToolInvocation.args`.
3. **Agent-reasoning summarization** (§ 6) over every reasoning/chain-of-thought segment.
4. **A final escape scan** (§ 7 R12) over the _fully-assembled_ candidate row.

No content reaches step 4 without passing steps 1–3. The pipeline is **total**: every field
of the trace that will appear in the emitted row is covered by exactly one of the three
content rules, or it is a structural field (an ID, a digest, an enum, a timestamp) that
carries no free text. A field that is neither structural nor covered by a rule is a
**coverage gap** and MUST cause emission refusal (R2).

### R2 — Fail-closed

The sanitization boundary is **fail-closed.** If any stage cannot establish that its output
is free of the forbidden classes (§ 4–§ 6), or if the final escape scan (R12) finds a
single match, the candidate row is **NOT emitted.** Emission refusal is the safe default; a
trace that _might_ contain a credential is treated identically to one that _does._ This
mirrors the `ToolInvocation` persistence discipline (glossary § 2.11): a row containing a
credential-shaped string in `args` or `result_summary` causes the runtime to **reject
persistence and fail the parent EvalRun** — sanitization for emission is the same wall, one
layer further out.

A refusal emits the `bundle.emission.refused` event (`067-AT-SPEC` § 3.1) with
`bundle.emission.refused_reason` set to the failing stage, and MUST NOT emit the row. There
is no "emit with a warning" path.

### R3 — Sanitization composes with, does not replace, the credential broker

The credential broker (Blueprint B § 4.1) redacts provider responses _at the runtime
boundary_, before telemetry is emitted. This spec's pipeline is a **second, independent**
wall applied at _emission_ time. Defense in depth: the broker prevents most secret-bearing
content from ever entering a trace; this pipeline assumes the broker is fallible and
re-scans at the immutable-emission boundary, where the cost of a miss is permanent. A
conforming implementation MUST run both — never rely on the broker alone for emission
safety.

## 4. Prompt-redaction rules (the prompt body)

A **prompt body** is the text sent to a provider as part of a model call recorded in the
trace. The forbidden classes below MUST be redacted before a prompt body may appear in a
candidate row.

### R4 — Forbidden classes (redact, never emit)

| Class                            | Examples                                                                                                                                                                                             | Action                                                                                        |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Credential-shaped strings**    | API keys (`sk-...`, `AKIA...`, `ghp_...`, bearer tokens, `Authorization:` header values), private-key PEM blocks, JWTs, connection strings with embedded passwords, `.env`-style `KEY=secret` lines. | Replace with `[REDACTED:credential]`.                                                         |
| **Secret-bearing URLs**          | URLs with credentials in userinfo (`https://user:pass@host`), pre-signed URLs with signature query params, webhook URLs with embedded tokens.                                                        | Replace credential-bearing component with `[REDACTED:url-secret]`; the host MAY be preserved. |
| **Verbatim user-secret content** | Content the user explicitly marked secret, or content matching a deployment-configured secret pattern (a `SANITIZATION_PATTERNS` allowlist-of-shapes).                                               | Replace with `[REDACTED:user-secret]`.                                                        |

### R5 — Redaction is shape-based, not value-based, and conservative

Redaction MUST match on _shape_ (the structural pattern of a secret) rather than requiring
a known _value._ A new, never-before-seen API key is still credential-shaped; the pipeline
MUST catch it. The rule is deliberately **over-broad**: a false positive (redacting a
non-secret that looks credential-shaped) is acceptable; a false negative (emitting a real
secret) is a spec violation. When shape-detection is uncertain, redact.

### R6 — Redaction preserves structure, removes value

A redaction MUST preserve enough structure for the trace to remain forensically useful (the
_position_ of the secret, its _class_) while removing the value entirely. `[REDACTED:credential]`
tells a reader "a credential was here" without revealing it. A redaction MUST NOT be
reversible — no length-preserving masking that leaks entropy, no partial reveal (not even a
prefix; "starts with `sk-`" is itself a leak of secret structure). The redacted token is a
fixed sentinel, not a transformation of the secret.

### R7 — Redaction is recorded, the original is not retained in the emitted artifact

The candidate row MAY carry a count of redactions performed per class (`redaction_count`)
so a consumer knows redaction occurred. The original (pre-redaction) bytes MUST NOT appear
anywhere in the emitted artifact, including in any "for audit" sidecar that travels with the
row. The pre-redaction trace MAY persist in the platform's _private_ content-addressed store
(Blueprint B § 5.1) under access control — but never in the signed, transparency-logged row.

## 5. Tool-call-argument sanitization rules (`ToolInvocation.args`)

A **tool-call argument** is a value passed to a tool recorded as a `ToolInvocation`
(glossary § 2.11). Args are structured (typically JSON), which makes them both easier to
walk and more dangerous (a secret can hide deep in a nested field).

### R8 — Walk every leaf

Sanitization MUST recurse to every leaf value of the args structure — every string in every
nested object and array. A secret in `args.config.auth.headers.Authorization` is exactly as
forbidden as one in a top-level `args.token`. There is no depth at which scanning stops.

### R9 — Apply the § 4 forbidden classes to every string leaf

Every string leaf of the args structure is subject to the same forbidden-class redaction as
a prompt body (R4–R6). In addition:

| Arg-specific class                           | Examples                                                                                                                                                                      | Action                                                                                                                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Filesystem paths revealing user identity** | absolute home paths (`/home/<user>/...`, `/Users/<user>/...`), paths embedding usernames or org-internal hostnames.                                                           | Replace the identity-revealing segment with `[REDACTED:path-identity]`; the relative structure MAY be preserved.                                                         |
| **Known-sensitive parameter names**          | leaves whose _key_ is in a sensitive-key set (`password`, `secret`, `token`, `api_key`, `private_key`, `passphrase`, `credential`, case-insensitive, with common separators). | Redact the _value_ regardless of whether the value matches a value-shape, per R5's conservatism. A field named `password` is redacted even if its value looks innocuous. |

### R10 — Structural fields are preserved, value fields are sanitized

Tool name, invocation timestamp, `retry_attempt`, span IDs, and digests are **structural**
and pass through unredacted — they carry no free text (`067-AT-SPEC` § 5). Only string
_values_ that could carry a secret are sanitized. A sanitized args structure MUST remain
schema-valid (the same keys, the same shape) so the trace's structure is intact; only leaf
values change.

## 6. Agent-reasoning summarization rules (chain-of-thought)

**Agent reasoning** is the model's chain-of-thought / reasoning text recorded in the trace.
It is the hardest class: it is free-form natural language that may _quote_ a secret, _describe_
a secret, or _reconstruct_ one from context — and it is exactly the content most valuable to
a provider's training corpus, which is the CISO's named permanence hazard.

### R11 — Summarize, do not transcribe

Agent reasoning MUST NOT be emitted verbatim. It MUST be replaced by a **summary** that
preserves the _semantic content needed for forensic analysis_ — what the agent decided and
why, the reasoning _shape_ — while removing:

- Any verbatim secret, credential, path-identity, or secret-URL (the § 4/§ 5 forbidden
  classes), whether _quoted_ or _described in enough detail to reconstruct._
- Any verbatim user-supplied content the user marked secret.
- Any literal tool output the reasoning quotes (tool outputs are sanitized at their own
  source per R3/the broker, but reasoning that re-quotes raw output bypasses that wall —
  the summary breaks the re-quote).

The summarization rule is **preserve semantics, strip credentials** (the iel-E10c bead
mandate). A conforming summary lets an analyst answer "what did the agent reason about and
conclude?" without ever exposing a secret the reasoning touched.

### R11a — Summarization is itself sanitized

The summary produced by R11 is **re-run through § 4 and § 5** before it may appear in a
candidate row. A summary is generated text; if the summarizer accidentally echoes a
credential-shaped substring from the source, that substring is caught by the prompt-redaction
pass over the summary. Summarization is not trusted to be secret-free on its own — it is
sanitized like any other content (the pipeline is total, R1).

## 7. PASS/FAIL conformance fixture suite (the CISO non-negotiable)

> Per the FUTURE.md / PREDICATE-TYPES.md REJECTED trigger, the URI is revisited only when a
> sanitization spec is authored **AND passes the CISO PASS/FAIL sanitization-test fixture in
> CI.** This section defines that fixture suite. A claim of conformance without a green run
> of this suite is not a claim (`specs/README.md` authoring conventions).

### R12 — The final escape scan

After the pipeline (§ 4–§ 6) assembles a candidate row, an **escape scan** runs over the
_entire serialized candidate row_ — every byte that would be signed. The escape scan applies
the § 4 forbidden-class shape detectors to the fully-assembled artifact. **A single match
fails the scan, and a failed scan refuses emission (R2).** The escape scan is the last wall:
it catches a secret that slipped between stages, that lives in a field no content rule
claimed (a coverage gap, R1), or that the summarizer re-introduced.

The escape scan reuses the `audit-harness` escape-scan gate discipline (the same
shape-detection family that runs as a pre-commit gate); a conforming implementation SHOULD
delegate to that gate rather than re-implement shape detectors, so the detection corpus stays
single-sourced.

### R13 — The fixture suite shape

The conformance suite under
[`conformance-test-suite/`](./conformance-test-suite/) ships two fixture classes:

| Fixture class              | Contains                                                                                                                                                                                                                                                                                                                         | Required result                                                                                                                                                                                                                                                                                                                                             |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MUST-REDACT fixtures**   | Traces carrying a planted secret of each forbidden class (§ 4 credential shapes, § 5 arg secrets at depth, § 6 reasoning that quotes and that describes a secret), plus adversarial cases: secret split across a retry boundary, secret in a deeply-nested arg, secret echoed by a summary, secret only in a coverage-gap field. | The pipeline either redacts the secret to a sentinel **or** refuses emission. The escape scan over the result finds **zero** matches. A fixture that emits a row containing the planted secret is a **FAIL** of the suite.                                                                                                                                  |
| **MUST-PRESERVE fixtures** | Traces with no secrets but with credential-_adjacent_ benign content (a variable literally named `token` holding a UUID; a path that is not identity-revealing; reasoning that _mentions the word_ "password" without a value).                                                                                                  | The pipeline preserves forensic semantics: structural fields intact, reasoning summary retains decision content, benign content not over-redacted into uselessness. A fixture that destroys all forensic value (e.g. redacts the entire trace to sentinels) is a **FAIL** — over-redaction that makes the trace useless defeats the purpose of emitting it. |

### R14 — The CI gate

A conforming deployment runs the fixture suite as a **required CI check.** The gate is green
**only if**: every MUST-REDACT fixture produces zero escape-scan matches (or a documented
emission refusal), **and** every MUST-PRESERVE fixture retains its declared forensic content.
A single MUST-REDACT leak reds the gate. Per R2's fail-closed posture, a fixture whose outcome
is _indeterminate_ (the pipeline neither clearly redacted nor clearly refused) counts as a
**FAIL**, not a pass.

### R15 — The suite is the un-rejection precondition, not the un-rejection

A green run of this suite **satisfies the CISO veto's stated revisit trigger.** It does
**not** itself reserve or activate `agent-loop-trace/v1`. Reserving the URI — minting it in
the namespace, fixing its predicate body schema in the kernel, recording it in
PREDICATE-TYPES.md — is a **Class-1 ISEDC act** (DR-010 § 7 Q6). This suite passing is the
_evidence the council requires_; the council's act is the _reservation._ The two are
distinct on purpose: the precondition is mechanical and testable; the irreversible act is
deliberative.

## 8. Residual risk + emission refusal

### R16 — Emission refusal is a first-class, recorded outcome

When the pipeline refuses to emit (R2), that refusal is **recorded**, not silent: a
`bundle.emission.refused` event (`067-AT-SPEC` § 3.1) with the failing stage, and the parent
`EvalRun`'s trace marked as "trace-emission-withheld." The forensic trace still exists in the
platform's private store (R7) under access control; only its _public, signed emission_ is
withheld. Refusal is not data loss — it is the correct, safe outcome when sanitization cannot
be established.

### R17 — Residual-risk acknowledgment

This spec defends against the _known_ forbidden classes (§ 4–§ 6). A novel secret shape that
matches no detector is a residual risk. The mitigations: (a) shape-based, conservative
detection (R5) catches structurally-secret-shaped novelties even when their value is unknown;
(b) the fail-closed boundary (R2) plus the coverage-gap rule (R1) refuse rather than guess;
(c) the detection corpus is single-sourced through the `audit-harness` escape-scan family
(R12) so a new shape added there propagates here. The residual risk is **non-zero**; the
reservation of `agent-loop-trace/v1` (Class-1) is where the council weighs that residual risk
against the trace's value, with this suite's green run as the evidence floor.

## 9. Conformance reporting

A claim of conformance against this spec at `v0.1.0` (or later) MUST be substantiated by:

1. A green run of the § 7 fixture suite in the producing repo's CI (the CISO non-negotiable).
2. Evidence that both walls run (the credential broker AND this pipeline, R3).
3. The commit SHA of the codebase that ran the suite.
4. The version of the shape-detection corpus (the `audit-harness` escape-scan version) the
   escape scan delegated to.

Conformance reports land under `specs/sanitization/v0.1.0-draft/conformance-reports/`.

## 10. Anchoring — sources this spec composes

This spec invents no primitives. It composes:

- [in-toto Statement v1](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md) +
  [DSSE](https://github.com/secure-systems-lab/dsse) + [Sigstore cosign](https://docs.sigstore.dev/cosign/overview/) +
  [Rekor](https://docs.sigstore.dev/rekor/overview/) — the immutable-emission surface this
  spec gates (via the Evidence Bundle SPEC).
- The **Evidence Bundle SPEC** (`specs/evidence-bundle/v0.1.0-draft/SPEC.md`) — the envelope
  - signing this pipeline runs before.
- The **canonical glossary** (`014-DR-GLOS-canonical-glossary.md`) — SessionTrace (§ 2.10),
  ToolInvocation (§ 2.11) + its credential-redaction persistence wall, JudgeDecision (§ 2.5).
- **Blueprint B** (`012-AT-ARCH-platform-runtime-blueprint.md`) § 4.1 (credential broker),
  § 5.1 (content-addressed private store), § 7.0 (kernel-schema precedence).
- The **runtime event taxonomy** (`067-AT-SPEC-runtime-event-taxonomy-2026-06-12.md`) § 3.1
  (`bundle.emission.refused`), § 5 (PII-in-payloads anti-pattern this spec enforces at the
  trace surface).
- The **`audit-harness` escape-scan** gate — the single-sourced shape-detection corpus the
  final escape scan (R12) delegates to.
- [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) /
  [RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174) — conformance keywords.
- **DR-010** (`010-AT-DECR`) § 7 Q3 + § 8 CISO memo — the veto this spec exists to lift the
  precondition on, and the threat model it codifies.
- **PREDICATE-TYPES.md** — the REJECTED `agent-loop-trace/v1` registry row this spec gates.

## 11. RFC

Comments, corrections, and counter-proposals are welcome via GitHub issues on
[`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with
`[sanitization]` in the title. Per the brand-name policy in the umbrella CLAUDE.md, do not
file issues that name partner engagements absent written consent.

## 12. License

Apache 2.0 — see [LICENSE](../../../LICENSE) at repo root.
