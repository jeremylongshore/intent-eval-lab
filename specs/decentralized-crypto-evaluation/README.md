# Decentralized Crypto Evaluation — placeholder module

> **Status: placeholder.** This module is reserved for evaluation methodology covering decentralized cryptographic agents and key-material handling. No spec has been authored yet. RFC welcome.

## Class of system in scope

When AI agents interact with decentralized cryptographic infrastructure — distributed key generation networks, threshold-signing protocols, programmable key-pair (PKP) systems, MPC custody networks — a class of failure modes emerges that doesn't appear in centralized AI deployments:

- **Key-material exposure under adversarial framing** — agent prompted with carefully crafted instructions reveals or signs against material that policy says it shouldn't, even when the underlying cryptographic protocol is sound.
- **Quorum / threshold-state confusion** — agent makes decisions on the assumption of an `m`-of-`n` threshold state but the actual on-chain or off-chain state has shifted (slashed nodes, rotation events, jailed validators) — agent's decision is technically valid but operationally wrong.
- **Replay / freshness gaps** — agent signs a payload that's structurally valid but stale (nonce reuse, expired session, rotated key window), and the downstream consumer accepts it because the agent's signing identity is still authorized.
- **Cross-chain assumption drift** — agent reasoning across multiple chains assumes invariants from one chain (finality semantics, gas pricing, mempool model) apply to another, leading to MEV-able decisions or stuck transactions.

## Why this needs its own module

These failure modes are not addressed by general-purpose agent evaluation. They require evaluation against adversarial input distributions specific to decentralized cryptographic systems: prompt-injection vectors targeting key material, simulated quorum-state desync, replay-window probes, and cross-chain consistency attacks.

A spec under this module would codify what it means for an AI agent operating against decentralized cryptographic infrastructure to be *operationally ready* — including the audit trail and adversarial-test surface required before such an agent should hold privileged signing or decryption authority.

## When this module will graduate from placeholder

When a partner engagement covering this domain produces enough specific failure-mode evidence to anchor a draft spec. Likely vendors: decentralized key-management networks, MPC custody platforms, threshold-signing infrastructure, validator-operations tooling.

## RFC

Practitioners working on AI agents in decentralized cryptographic systems — file a GitHub issue on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with `[decentralized-crypto-evaluation]` in the title.
