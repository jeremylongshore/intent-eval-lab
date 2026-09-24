# Generic substrate dogfood — 2026-08-02

**Plan:** `IEP-EVAL-EVOLUTION-001`
**Bead:** `bd_000-projects-htjt.4`
**Scope:** deterministic non-skill evaluation receipt for the Phase 5
cross-repo convergence gate.

This sandbox exercises the generic J-Rig substrate without a provider key. The
task and configuration are data, the harness is invoked with `shell: false`,
and the deterministic grader is selected by its immutable snapshot digest in
the final report. The harness output is deliberately boring: it makes the
runner, persistence, grading, and report lineage observable without confusing
synthetic provider output for real-skill quality evidence.

## Reproduction

From the J-Rig producer worktree, after `pnpm run build`:

```bash
SANDBOX=/home/jeremy/000-projects/intent-eval-platform/intent-eval-lab/sandboxes/2026-08-02-iep-phase5-dogfood
DB=/tmp/iep-phase5-generic.db
node packages/cli/dist/index.js run \
  --task "$SANDBOX/task.yaml" \
  --config "$SANDBOX/config.yaml" \
  --db "$DB" \
  --sample-index 0 \
  --json
node packages/cli/dist/index.js grade \
  --run-id '<run_id from the first command>' \
  --grader "$SANDBOX/grader.yaml" \
  --db "$DB" \
  --json
node packages/cli/dist/index.js report \
  --unified \
  --db "$DB" \
  --grader-id answer-checker \
  --grader-version 1.0.0 \
  --grader-snapshot-sha256 '<grader snapshot digest from the grade command>' \
  --json \
  --output /tmp/iep-phase5-generic-report.json
```

The same `run` invocation is idempotent for sample `0`: rerunning it returns
the sealed raw Run with `reused: true`. The report is a local projection; it
is not a signed Evidence Bundle and must not be published as one.
