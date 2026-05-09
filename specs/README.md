# `specs/` — normative methodology output

The `intent-eval-lab` umbrella covers research and experimentation across multiple classes of operationally-deployed inference systems. The `specs/` tree is where that research crystallizes into **normative methodology** — versioned, testable, vendor-neutral specifications that codify what "operationally ready" means for each class.

Each module under `specs/` covers one class of inference system. Each module ships its own versioned spec, conformance test suite, and per-vendor case studies.

## Modules

| Module | Class of system | First case study | Status |
|---|---|---|---|
| [`mcp-plugin-observability/`](./mcp-plugin-observability/) | MCP plugins for agentic CLIs (Claude Code, Gemini CLI, Codex CLI, Copilot CLI) | `kobiton/automate` | v0.1.0-draft (in progress) |
| [`validator-contract-reliability/`](./validator-contract-reliability/) | AI-generated validator contracts and cryptographic primitives | (pending) | placeholder — RFC welcome |
| [`forecasting-drift-detection/`](./forecasting-drift-detection/) | Time-series forecasting under data-shift conditions | (pending) | placeholder — RFC welcome |
| [`decentralized-crypto-evaluation/`](./decentralized-crypto-evaluation/) | Decentralized cryptographic agents and key-material handling | (pending) | placeholder — RFC welcome |
| [`methodology/`](./methodology/) | Cross-module patterns (Toulmin findings, diagnostic-first auditing, conformance-vs-eval distinction) | n/a | placeholder |

Modules are added as engagements warrant. Placeholder READMEs exist to signal intent and welcome RFC-style input from practitioners working in those domains; they don't represent committed work without a corresponding case study.

## Spec authoring conventions

- **Versioning** — semantic, with explicit `vN.M.K-draft` / `vN.M.K-rc` / `vN.M.K` tags. A spec stays at `-draft` until at least one independent implementation ships against it.
- **Anchoring** — every normative requirement cites the canonical upstream source (Anthropic docs, vendor specs, RFC, ISO standard, etc.) it codifies. Specs are *codifying what's already canonical*, not inventing.
- **Test suites** — every module ships a reference test suite under `conformance-test-suite/`. A claim of conformance without a test pass is not a claim.
- **Case studies** — each module's `case-studies/` dir holds vendor-specific instantiations. Case studies are illustrative, not normative; they show how the spec applies to a real system.
- **Multi-vendor by default** — module specs are vendor-neutral. If a requirement only applies to one vendor's surface, it goes in that vendor's case study, not the spec.

## License

Apache 2.0 — see [LICENSE](../LICENSE) at repo root.
