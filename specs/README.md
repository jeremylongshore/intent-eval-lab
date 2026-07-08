# `specs/` — normative methodology output

The `intent-eval-lab` umbrella covers research and experimentation across multiple classes of operationally-deployed inference systems. The `specs/` tree is where that research crystallizes into **normative methodology** — versioned, testable, vendor-neutral specifications that codify what "operationally ready" means for each class.

Each module under `specs/` covers one class of inference system. Each module ships its own versioned spec, conformance test suite, and per-vendor case studies.

## Modules

| Module                                                                   | Class of system                                                                                                                                                              | First case study                                                     | Status                                        |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------- |
| [`mcp-plugin-observability/`](./mcp-plugin-observability/)               | MCP plugins for agentic CLIs (Claude Code, Gemini CLI, Codex CLI, Copilot CLI)                                                                                               | (engagement-private; not for public release without partner consent) | v0.1.0-draft (in progress)                    |
| [`prompt-evaluation/`](./prompt-evaluation/)                             | Prompts + context templates as eval targets (the prompt→context-engineering unit, generalizing beyond skills)                                                                | (pending)                                                            | v0.1.0-draft skeleton — gated; see 043-DR-RFC |
| [`validator-contract-reliability/`](./validator-contract-reliability/)   | AI-generated validator contracts and cryptographic primitives                                                                                                                | (pending)                                                            | placeholder — RFC welcome                     |
| [`forecasting-drift-detection/`](./forecasting-drift-detection/)         | Time-series forecasting under data-shift conditions                                                                                                                          | (pending)                                                            | placeholder — RFC welcome                     |
| [`decentralized-crypto-evaluation/`](./decentralized-crypto-evaluation/) | Decentralized cryptographic agents and key-material handling                                                                                                                 | (pending)                                                            | placeholder — RFC welcome                     |
| [`methodology/`](./methodology/)                                         | Cross-module patterns (Toulmin findings, diagnostic-first auditing, conformance-vs-eval distinction)                                                                         | n/a                                                                  | placeholder                                   |
| [`tier-bridge/`](./tier-bridge/)                                         | Platform-internal: how a skill's static tiers (grading + static production gate) compose with the behavioral (`j-rig`) tier into one promotion verdict                       | n/a (platform-internal)                                              | v0.1.0-draft (normative)                      |
| [`taxonomy/`](./taxonomy/)                                               | Platform-internal: the 7-layer testing taxonomy (git-hooks → static → unit → integration → system → E2E → acceptance) the `audit-tests` / `implement-tests` skills reference | n/a (platform-internal)                                              | v0.1.0-draft (normative)                      |
| [`skill-refiner-evidence-report/`](./skill-refiner-evidence-report/)     | Platform-internal: the per-pass Skill Refiner evidence report — the human-readable + machine-verifiable view of one `skill-refiner-pass/v1` attestation                      | n/a (platform-internal)                                              | v1.0.0-draft (normative)                      |

Most modules cover a _class of inference system_; the last three (`tier-bridge`, `taxonomy`, `skill-refiner-evidence-report`) are **platform-internal process specs** — they codify how the platform's own tooling composes, not an external system class. Modules are added as engagements warrant. Placeholder READMEs exist to signal intent and welcome RFC-style input from practitioners working in those domains; they don't represent committed work without a corresponding case study.

## Spec authoring conventions

- **Versioning** — semantic, with explicit `vN.M.K-draft` / `vN.M.K-rc` / `vN.M.K` tags. A spec stays at `-draft` until at least one independent implementation ships against it.
- **Anchoring** — every normative requirement cites the canonical upstream source (Anthropic docs, vendor specs, RFC, ISO standard, etc.) it codifies. Specs are _codifying what's already canonical_, not inventing.
- **Test suites** — every module ships a reference test suite under `conformance-test-suite/`. A claim of conformance without a test pass is not a claim.
- **Case studies** — each module's `case-studies/` dir holds vendor-specific instantiations. Case studies are illustrative, not normative; they show how the spec applies to a real system.
- **Multi-vendor by default** — module specs are vendor-neutral. If a requirement only applies to one vendor's surface, it goes in that vendor's case study, not the spec.

## License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
