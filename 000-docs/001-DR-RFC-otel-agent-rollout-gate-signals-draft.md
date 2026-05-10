# RFC Draft: OpenTelemetry Semantic Conventions for Agent Rollout Gate Signals

> **Status: PHASE A DRAFT.** This is RFC draft text authored locally. It is **not yet filed** against [`open-telemetry/semantic-conventions`](https://github.com/open-telemetry/semantic-conventions). Phase B deliverable per `IEL-8` is to file this draft as a public RFC.
>
> **Issue:** [`jeremylongshore/intent-eval-lab#19`](https://github.com/jeremylongshore/intent-eval-lab/issues/19) (`IEL-8`)
> **Umbrella:** [`jeremylongshore/intent-eval-lab#10`](https://github.com/jeremylongshore/intent-eval-lab/issues/10) (`IEL-CONV-7`)
> **Master plan:** `~/.claude/plans/please-take-your-time-glimmering-stardust.md` § "Surprise findings" #6

## Title

**Semantic Conventions for Agent Rollout Gate Signals**

## Author

Jeremy Longshore (Intent Solutions LLC) — `jeremy@intentsolutions.io`

## Abstract

Agent-native CLIs (e.g., Claude Code, Codex CLI, Gemini CLI, Copilot CLI) increasingly ship gated rollout pipelines: a CI step evaluates evidence about a proposed code change against a policy, and emits a ship / no-ship decision. Today this evaluation is invisible to standard observability tooling — there are no canonical signal names, no agreed-upon attributes, no shared vocabulary across vendors.

This RFC proposes a small set of OpenTelemetry semantic conventions to make agent rollout gates **observable across vendors**, so that operators can monitor, audit, and reason about gate decisions using the same primitives regardless of which CLI or evaluation framework produced them.

## Motivation

The agent-native CLI ecosystem is converging on a common pattern:

```
  evidence ─→ policy evaluation ─→ ship | no-ship decision
```

Concrete instances of this pattern include:

- Pre-merge gates that block PRs unless an evaluation suite passes
- Pre-deploy gates that block production rollouts unless a conformance report meets a threshold
- Per-agent-action gates that block the agent from invoking destructive operations unless prior gates passed

Each of these cases produces signals an operator should be able to observe — but today, every framework names those signals differently. An operator running Claude Code in one CI workflow and Codex CLI in another has to learn two telemetry vocabularies, write two dashboards, and write two alerting rules for the same operational concern.

This RFC proposes a vendor-neutral signal vocabulary that any agent rollout gate framework can adopt.

## Status of related work

- [OpenTelemetry semantic conventions for AI agents](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai) — emerging conventions for agent-internal signals (LLM calls, tool calls, sessions). Does not currently cover rollout-gate evaluation as a signal class.
- [Sigstore cosign](https://docs.sigstore.dev/) — signing primitives for evidence artifacts. Adopted by reference implementations of this RFC.
- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) — policy evaluation engine. Reference adopters use OPA for the policy-evaluation step.

## Proposal

### Events

Four new events under the `agent.rollout.gate.*` and `agent.evidence_bundle.*` namespaces:

| Event name | Trigger | Required attributes |
|---|---|---|
| `agent.rollout.gate.evaluated` | Emitted at the start of a rollout gate evaluation | `gate.id` (string), `gate.policy.uri` (string), `gate.policy.hash` (string) |
| `agent.rollout.gate.decision` | Emitted at the end of a rollout gate evaluation | `decision` (enum: `"ship"`, `"no-ship"`), `reasons` (array of strings) |
| `agent.evidence_bundle.signature_verified` | Emitted when an evidence bundle's signature has been checked | `bundle.uri` (string), `signer` (string), `verified` (boolean) |
| `agent.evidence_bundle.schema_validated` | Emitted when an evidence bundle has been validated against its declared schema | `bundle.uri` (string), `schema.version` (string), `valid` (boolean) |

### Span attributes

When a rollout gate evaluation occurs inside a larger trace span (e.g., a CI workflow), these attributes SHOULD be added to the relevant span:

| Attribute | Type | Description |
|---|---|---|
| `evidence.bundle.uri` | string | Stable URI for the evidence bundle being evaluated |
| `evidence.bundle.version` | string | Bundle version (semver string) |
| `evidence.bundle.signer` | string | Identity of the bundle signer (e.g., cosign issuer) |
| `gate.framework` | string | Framework producing the gate decision (e.g., `"intent-eval-lab/rollout-gate"`) |
| `gate.framework.version` | string | Framework version (semver string) |

## Examples

### Example 1: a passing rollout gate

```json
{
  "name": "agent.rollout.gate.evaluated",
  "time": "2026-05-10T18:00:00Z",
  "attributes": {
    "gate.id": "pre-merge:functional-conformance",
    "gate.policy.uri": "https://example.org/policies/v3.rego",
    "gate.policy.hash": "sha256:abc123..."
  }
}
```

```json
{
  "name": "agent.rollout.gate.decision",
  "time": "2026-05-10T18:00:01Z",
  "attributes": {
    "decision": "ship",
    "reasons": [
      "all gate-result rows pass",
      "schema validates",
      "signature verified"
    ]
  }
}
```

### Example 2: a blocking rollout gate

```json
{
  "name": "agent.rollout.gate.decision",
  "time": "2026-05-10T18:00:01Z",
  "attributes": {
    "decision": "no-ship",
    "reasons": [
      "gate-result row 'mutation-kill-rate' below threshold (0.62 < 0.75)",
      "gate-result row 'escape-scan' returned REFUSE"
    ]
  }
}
```

## Alternatives considered

- **Per-vendor signal namespaces** — what exists today. Rejected because operators can't compose dashboards across frameworks.
- **Reusing `gen-ai.*` namespace** — rejected because rollout gates are not AI-internal signals; they're CI-pipeline signals about AI-produced artifacts. Conflating them obscures the distinction between "the agent's behavior" and "the gate's decision about the agent's behavior."
- **Free-text attributes only (no events)** — rejected because event-shape signals are a first-class observability primitive in OpenTelemetry, and rollout-gate decisions are exactly the shape events were designed for.

## Backward compatibility

This RFC adds new signals only. It does not modify any existing semantic convention. Frameworks not emitting these signals continue to function exactly as before.

## Reference implementation

Intent Solutions' [`intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) project ships:

- An **Evidence Bundle** specification (`specs/evidence-bundle/v0.1.0-draft/`) that defines the bundle artifact these signals reference
- A **Rollout Gate GHA** (`gha/rollout-gate/`) that emits these signals when invoked
- A **bundle CLI** (`cli/`) that emits the `agent.evidence_bundle.*` signals during sign / verify / diff operations

The reference implementation is Apache 2.0 and intended to demonstrate that the proposed signals are useful in practice. Other framework authors are explicitly invited to adopt the conventions independently — adoption is not contingent on using the reference implementation.

## Open questions for the OTel community

1. **Namespace.** Is `agent.rollout.gate.*` the right namespace, or should this nest under an existing namespace? `gen-ai.gate.*`? `ci.gate.*`?
2. **Decision enum.** Is `"ship" | "no-ship"` sufficient, or should there be a tri-state (`"ship" | "no-ship" | "indeterminate"`) for cases where policy evaluation cannot conclude?
3. **Reasons cardinality.** Should `reasons` be unbounded array of strings, or a structured object (`{ reason_id: string, severity: enum }`) for better dashboarding?

## Filing plan

This RFC will be filed in **Phase B** of the convergence vision (per `IEL-CONV-7`), once the reference implementation has demonstrated the proposed signals are useful in practice. Phase A (this draft) is the local authoring step.

When filed, the RFC submission location will be:

- [`open-telemetry/semantic-conventions`](https://github.com/open-telemetry/semantic-conventions) — as a draft PR or RFC issue, following their contribution guidelines
- Possibly cross-posted to the [OpenTelemetry SIG GenAI](https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md) for relevant subgroup feedback

## License

This draft is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) for the RFC text. The reference implementation is Apache 2.0.
