# CoreWeave dogfood — Evidence Bundles

`gate-result/v1` Evidence Bundles from running the Intent Eval Platform's 7-layer skill
evaluation (j-rig) against Intent Solutions' own published CoreWeave skills — the platform
grading its own work, held to the same bench and the same signature discipline as everything else.

## Provenance

- **Eval'd** 2026-07-06, locally, via `j-rig eval <skill> --provider deepseek --run-self-test`.
- **Judge:** `deepseek-v4-flash`. **No CoreWeave API keys** — the skills reason over pasted
  evidence + fixtures; only the DeepSeek _judge_ key is used.
- Each bundle is committed here, reviewed, then signed by
  `.github/workflows/sign-dogfood-bundle.yml` (cosign keyless → **production Rekor**),
  reviewer-gated behind the `evidence-prod` environment. The signature attests integrity,
  this workflow's identity, and time — **not** that the verdict is "correct" (the science
  stands on the eval, not the signature).

## Signed

| Skill                          | Self-test                     | Judgment | Decision        | Reproduced                                              |
| ------------------------------ | ----------------------------- | -------- | --------------- | ------------------------------------------------------- |
| `coreweave-gpu-node-forensics` | 20/20 (deterministic blocker) | 17/17    | **pass (SHIP)** | yes — identical to intent-os `022-RA-DATA` (2026-07-05) |

The `.sigstore.json` alongside the bundle (added by the signing workflow) carries the Fulcio
cert + signature + Rekor inclusion proof; verify it yourself with `cosign verify-blob`.

## Held — deliberately NOT signed

- **`coreweave-gpu-cost-leak-hunter`** is not signed. Its verdict is **nondeterministic**: SHIP
  10/10 on 2026-07-05 (`022-RA-DATA`) → BLOCK 5/10 on a 2026-07-06 re-run of the same skill,
  same harness, same judge model. A permanent, public, non-deletable signature must not ride a
  single noisy sample. It is held pending a **seeded or multi-run majority** verdict before it
  earns an attestation. This is a real finding about judge determinism, not a pass/fail verdict
  on the skill.
