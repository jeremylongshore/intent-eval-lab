# Ecosystem coordination

Cross-repo coordination for the Intent Eval Platform (IEP) lives here, in
`intent-eval-lab` — the platform's methodology / coordination home.

## Files

| File                 | What it is                                                                                                                                                                                                                                                                                          |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ecosystem.json`     | Manifest of every **managed** IEP repo: its `kind`, the `@intentsolutions/core` schema version it pins, the `@intentsolutions/audit-harness` version it pins, and how the harness is installed (`npm-dep`, `vendored`, or `self`). The source of truth for "what versions should every repo be on". |
| `coherence-check.sh` | Read-only verifier. For each managed repo it confirms the working copy is present, the pinned schema + harness versions match `ecosystem.json`, and the harness resolves. Clear `PASS` / `FAIL` per check; exit 0 = all pass, 1 = drift, 2 = setup error. Mutates nothing.                          |

## Managed repos

`intent-eval-core` (kernel) · `intent-eval-lab` (methodology) ·
`audit-harness` (gates) · `j-rig-skill-binary-eval` (behavioral-eval) ·
`intent-rollout-gate` (action).

`claude-code-plugins` is **deferred-pending-CCP-study** (bead `3wt1f`): it has
bespoke in-flight CI/CD and is intentionally **not** wired with any
ecosystem-sync automation. It is recorded under `.deferred` in the manifest so
the deferral is explicit, and `coherence-check.sh` never touches it.

## Running the check

```bash
# Auto-detect the umbrella root (parent of this repo):
ecosystem/coherence-check.sh

# Or point it at an explicit IEP umbrella dir:
ecosystem/coherence-check.sh --root /path/to/intent-eval-platform
```

## Keeping the manifest current

When any managed repo bumps the `@intentsolutions/core` schema version or the
`@intentsolutions/audit-harness` version it pins, update the matching entry in
`ecosystem.json`. `coherence-check.sh` reports `FAIL` the moment a repo drifts
from the recorded values, so the manifest stays honest.
