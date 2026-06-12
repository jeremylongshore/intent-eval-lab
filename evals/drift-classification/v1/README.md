# drift-classification/v1 — frozen eval set

Human-labeled before/after diffs of upstream spec snapshots, mined from this
repo's git history (3 real cases — every real snapshot diff that exists) plus
12 synthetic perturbations of real snapshot material (marked `"synthetic": true`).

The future LLM drift-classifier writes nothing until it clears the recall
floor (`manifest.json` `recall_floor`, 1.0 on material cases) on this set.
Scored deterministically by `scripts/drift-eval-runner.py` — no LLM calls here.

- **Frozen**: existing cases are NEVER edited; `manifest.json` pins the SHA-256
  of every case file and CI re-hashes on every PR. Extension is append-only.
- **Spec + label rubric + freeze protocol**:
  `000-docs/053-AT-SPEC-drift-classification-eval-set-2026-06-12.md`.

```bash
python3 scripts/drift-eval-runner.py --verify-manifest          # frozen guarantee
python3 scripts/drift-eval-runner.py --score PREDICTIONS.jsonl  # recall-floor gate
python3 scripts/drift-eval-runner.py --self-test                # gate soundness
```
