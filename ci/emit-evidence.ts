#!/usr/bin/env -S node --experimental-strip-types
/**
 * ci/emit-evidence.ts — produce intent-eval-lab's own signed-ready spec-integrity
 * evidence for the intent-eval-dashboard reports hub (bead nr75.13).
 *
 * ── Why CI-only, in ci/ ──
 *
 * intent-eval-lab is a spec/docs/Python repo with NO package.json and NO node
 * build. This emitter imports `@intentsolutions/core` (kernel validators), so CI
 * installs the kernel with `npm i --no-save @intentsolutions/core@<v>` just for
 * the emit job — see `.github/workflows/release.yml`. `ci/` is not shipped
 * anywhere; nothing about the lab's published surface changes.
 *
 * ── Gate selection (honest spec-integrity, no fake evidence) ──
 *
 * The lab ships specs + decision records, not a product eval — so it emits
 * META-gate(s) about its own integrity, NOT product gate-results. Its one clean,
 * deterministic gate is HARNESS-HASH (`scripts/audit-harness verify`), which the
 * lab's `.harness-hash` manifest pins over a broad spec-integrity surface: the CI
 * workflow definitions (including partner-name-guard.yml and schema-drift.yml),
 * the kernel schema redirect stub, and the vendored audit-harness scripts. So a
 * passing harness-hash transitively attests that those OTHER spec-integrity gates'
 * definitions are themselves untampered — making it the right single meta-gate.
 * partner-name-guard + schema-drift are NOT emitted as separate rows: doing so
 * would either duplicate the PRIVATE partner-name pattern or re-implement the
 * schema-drift checker — both anti-patterns. harness-hash covers their integrity.
 *
 * Output (gitignored build/), contract, and canonicalisation are identical to the
 * iec/iah emitters; see those for the field-by-field rationale. Signing + Rekor +
 * assembly happen in CI; this script does NO crypto.
 *
 * Usage:
 *   node --experimental-strip-types ci/emit-evidence.ts [--out build/evidence] [--self-check]
 */

import { execFileSync } from 'node:child_process';
import { createHash, randomBytes } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import {
  GateResultV1Schema,
  GATE_RESULT_V1_URI,
} from '@intentsolutions/core/validators/v1/gate-result-v1';
import { EvidenceBundleSchema } from '@intentsolutions/core/validators/v1/evidence-bundle';

const GITHUB_REPO = 'jeremylongshore/intent-eval-lab';
const REPO_KEY = 'iel';

interface GateOutcome {
  readonly gateName: string;
  readonly gateVersion: string;
  readonly decision: 'pass' | 'fail' | 'advisory' | 'error';
  readonly reasons: readonly string[];
  readonly dimensionsEvaluated: readonly string[];
  readonly dimensionsSkipped: readonly string[];
  readonly advisorySeverity?: 'info' | 'warn' | 'error';
  readonly failureMode?: string;
}

interface EmitContext {
  readonly nowIso: string;
  readonly nowMs: number;
  readonly commitSha: string;
  readonly sourceSha: string;
  readonly policyHash: string;
  readonly runnerVersion: string;
  readonly rand16: () => Uint8Array;
}

function sortDeep(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortDeep);
  if (value !== null && typeof value === 'object') {
    const entries = Object.entries(value as Record<string, unknown>)
      .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
      .map(([k, v]) => [k, sortDeep(v)] as const);
    return Object.fromEntries(entries);
  }
  return value;
}

export function stableStringify(value: unknown): string {
  return JSON.stringify(sortDeep(value));
}

function sha256Hex(s: string): string {
  return createHash('sha256').update(Buffer.from(s, 'utf8')).digest('hex');
}

export function uuidv7(nowMs: number, rand: Uint8Array): string {
  const b = Buffer.from(rand.slice(0, 16));
  const ts = BigInt(nowMs);
  b[0] = Number((ts >> 40n) & 0xffn);
  b[1] = Number((ts >> 32n) & 0xffn);
  b[2] = Number((ts >> 24n) & 0xffn);
  b[3] = Number((ts >> 16n) & 0xffn);
  b[4] = Number((ts >> 8n) & 0xffn);
  b[5] = Number(ts & 0xffn);
  b[6] = (b[6]! & 0x0f) | 0x70;
  b[8] = (b[8]! & 0x3f) | 0x80;
  const h = b.toString('hex');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20, 32)}`;
}

export interface EmitRow {
  readonly bundle: unknown;
  readonly canonicalBundle: string;
  readonly gateResult: unknown;
  readonly sourceSha: string;
}

export function buildGateResult(o: GateOutcome, ctx: EmitContext): Record<string, unknown> {
  const gateId = `${REPO_KEY}:ci:${o.gateName}`;
  const inputHash = `sha256:${sha256Hex(`${ctx.commitSha}:${o.gateName}:${ctx.policyHash}`)}`;
  const body: Record<string, unknown> = {
    gate_id: gateId,
    gate_name: o.gateName,
    gate_version: o.gateVersion,
    gate_decision: o.decision,
    gate_reasons: [...o.reasons],
    coverage: {
      dimensions_evaluated: [...o.dimensionsEvaluated],
      dimensions_skipped: [...o.dimensionsSkipped],
    },
    policy_ref: `${ctx.policyHash}:.harness-hash`,
    policy_hash: ctx.policyHash,
    input_hash: inputHash,
    evaluated_at: ctx.nowIso,
    runner: `iel-emit@${ctx.runnerVersion}`,
    commit_sha: ctx.commitSha,
    ...(o.advisorySeverity !== undefined ? { advisory_severity: o.advisorySeverity } : {}),
    ...(o.failureMode !== undefined ? { failure_mode: o.failureMode } : {}),
  };
  GateResultV1Schema.parse(body); // fail-closed
  return body;
}

export function buildEvidenceBundle(
  gateResult: Record<string, unknown>,
  ctx: EmitContext,
): Record<string, unknown> {
  const grHashHex = sha256Hex(stableStringify(gateResult));
  const inputHash = String(gateResult['input_hash']);
  const subjectDigest = inputHash.startsWith('sha256:')
    ? inputHash.slice('sha256:'.length)
    : inputHash;
  const bundle: Record<string, unknown> = {
    id: uuidv7(ctx.nowMs, ctx.rand16()),
    eval_run_id: uuidv7(ctx.nowMs, ctx.rand16()),
    created_at: ctx.nowIso,
    predicate_uri_set: [GATE_RESULT_V1_URI],
    row_count: 1,
    subject_set: [{ name: String(gateResult['gate_id']), digest: { sha256: subjectDigest } }],
    storage_key: `sha256:${grHashHex}`,
    signing_mode: 'rekor_production',
    rekor_log_indices: [],
    verification_status: 'unverified',
    verification_last_checked_at: ctx.nowIso,
  };
  EvidenceBundleSchema.parse(bundle); // fail-closed
  return bundle;
}

export function buildRows(outcomes: readonly GateOutcome[], ctx: EmitContext): EmitRow[] {
  return outcomes.map((o) => {
    const gateResult = buildGateResult(o, ctx);
    const bundle = buildEvidenceBundle(gateResult, ctx);
    return {
      bundle,
      canonicalBundle: stableStringify(bundle),
      gateResult,
      sourceSha: ctx.sourceSha,
    };
  });
}

export interface ManifestSkeleton {
  readonly repo: string;
  readonly signing: { readonly issuer: string; readonly subject: string; readonly workflowRef: string };
  readonly rows: readonly {
    readonly bundleFile: string;
    readonly gateResults: readonly unknown[];
    readonly sourceSha: string;
  }[];
}

export function signingClaims(ref: string): ManifestSkeleton['signing'] {
  return {
    issuer: 'https://token.actions.githubusercontent.com',
    subject: `repo:${GITHUB_REPO}:ref:${ref}`,
    workflowRef: `${GITHUB_REPO}/.github/workflows/release.yml@${ref}`,
  };
}

export function writeEmit(rows: readonly EmitRow[], ref: string, outDir: string): ManifestSkeleton {
  mkdirSync(outDir, { recursive: true });
  const skeletonRows = rows.map((row, i) => {
    const bundleFile = `bundle-${i}.json`;
    writeFileSync(join(outDir, bundleFile), row.canonicalBundle, 'utf8');
    writeFileSync(join(outDir, `gate-result-${i}.json`), stableStringify(row.gateResult), 'utf8');
    return { bundleFile, gateResults: [row.gateResult], sourceSha: row.sourceSha };
  });
  const skeleton: ManifestSkeleton = { repo: REPO_KEY, signing: signingClaims(ref), rows: skeletonRows };
  writeFileSync(join(outDir, 'manifest-skeleton.json'), JSON.stringify(skeleton, null, 2), 'utf8');
  return skeleton;
}

// ── Gate collection (CI-run; runs the lab's real spec-integrity self-gate) ──

function run(cmd: string, args: readonly string[]): { ok: boolean; out: string } {
  try {
    const out = execFileSync(cmd, args as string[], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    return { ok: true, out };
  } catch (err: unknown) {
    const e = err as { stdout?: string; stderr?: string; message?: string };
    return { ok: false, out: `${e.stdout ?? ''}${e.stderr ?? ''}${e.message ?? ''}` };
  }
}

/**
 * harness-hash (`scripts/audit-harness verify`): the lab's `.harness-hash`
 * manifest is consistent with the working tree — i.e. the pinned spec-integrity
 * surface (CI workflow definitions incl. partner-name-guard + schema-drift, the
 * schema redirect stub, the vendored audit-harness) is untampered.
 */
function harnessHashOutcome(): GateOutcome {
  const r = run('scripts/audit-harness', ['verify']);
  return {
    gateName: 'harness-hash',
    gateVersion: '1.0.0',
    decision: r.ok ? 'pass' : 'fail',
    reasons: r.ok
      ? [
          '.harness-hash manifest verified consistent',
          'pins the spec-integrity surface: CI workflows (incl. partner-name-guard + schema-drift), schema redirect stub, vendored audit-harness',
        ]
      : [firstLines(r.out, 6) || 'harness-hash verify reported drift'],
    dimensionsEvaluated: ['hash-manifest-consistency'],
    dimensionsSkipped: [],
    ...(r.ok ? {} : { failureMode: 'harness-hash-drift' }),
  };
}

function firstLines(s: string, n: number): string {
  return s
    .split('\n')
    .filter((l) => l.trim().length > 0)
    .slice(0, n)
    .join(' ')
    .slice(0, 500);
}

function gitSha(): string {
  const r = run('git', ['rev-parse', 'HEAD']);
  return r.ok ? r.out.trim() : '0'.repeat(40);
}

function harnessPolicyHash(): string {
  try {
    const h = readFileSync(join(process.cwd(), '.harness-hash'), 'utf8').trim();
    if (/^[a-f0-9]{64}$/.test(h)) return `sha256:${h}`;
    return `sha256:${sha256Hex(h)}`; // multi-line manifest → hash full content
  } catch {
    return `sha256:${sha256Hex('no-policy')}`;
  }
}

/** Derive a version label from the release ref (refs/tags/vX.Y.Z → X.Y.Z). */
function versionFromRef(ref: string): string {
  const m = /refs\/tags\/v?(.+)$/.exec(ref);
  return m?.[1] ?? '0.0.0';
}

// ── Self-check ──

function selfCheck(): void {
  const ctx = synthCtx();
  const outcomes: GateOutcome[] = [
    {
      gateName: 'harness-hash',
      gateVersion: '1.0.0',
      decision: 'pass',
      reasons: ['.harness-hash manifest verified consistent', 'pins the spec-integrity surface'],
      dimensionsEvaluated: ['hash-manifest-consistency'],
      dimensionsSkipped: [],
    },
    {
      gateName: 'harness-hash',
      gateVersion: '1.0.0',
      decision: 'fail',
      reasons: ['harness-hash verify reported drift'],
      dimensionsEvaluated: ['hash-manifest-consistency'],
      dimensionsSkipped: [],
      failureMode: 'harness-hash-drift',
    },
  ];
  const rows = buildRows(outcomes, ctx);
  for (const row of rows) {
    if (stableStringify(JSON.parse(row.canonicalBundle)) !== row.canonicalBundle) {
      throw new Error('canonical bundle is not stable under re-canonicalisation');
    }
  }
  if (rows.length !== 2) throw new Error('expected 2 rows');
  console.log(`✓ self-check: ${rows.length} kernel-valid, canonical-stable rows built`);
}

function synthCtx(): EmitContext {
  let n = 0;
  return {
    nowIso: '2026-06-08T00:00:00.000Z',
    nowMs: 1780617600000,
    commitSha: 'a'.repeat(40),
    sourceSha: 'a'.repeat(40),
    policyHash: `sha256:${'b'.repeat(64)}`,
    runnerVersion: '0.3.0',
    rand16: () => {
      n += 1;
      return Uint8Array.from(Array.from({ length: 16 }, (_v, i) => (n * 31 + i) & 0xff));
    },
  };
}

function ciCtx(ref: string): EmitContext {
  const sha = gitSha();
  return {
    nowIso: new Date().toISOString(),
    nowMs: Date.now(),
    commitSha: sha,
    sourceSha: sha,
    policyHash: harnessPolicyHash(),
    runnerVersion: versionFromRef(ref),
    rand16: () => Uint8Array.from(randomBytes(16)),
  };
}

function parseArgs(argv: readonly string[]): { out: string; selfCheck: boolean; ref: string } {
  let out = 'build/evidence';
  let ref = process.env['GITHUB_REF'] ?? 'refs/tags/v0.0.0';
  let sc = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--out') {
      out = argv[i + 1] ?? out;
      i++;
    } else if (argv[i] === '--ref') {
      ref = argv[i + 1] ?? ref;
      i++;
    } else if (argv[i] === '--self-check') {
      sc = true;
    }
  }
  return { out, selfCheck: sc, ref };
}

function main(argv: readonly string[]): number {
  const args = parseArgs(argv);
  if (args.selfCheck) {
    selfCheck();
    return 0;
  }
  const ctx = ciCtx(args.ref);
  mkdirSync(args.out, { recursive: true });
  const outcomes: GateOutcome[] = [harnessHashOutcome()];
  const rows = buildRows(outcomes, ctx);
  writeEmit(rows, args.ref, args.out);
  console.log(
    `✓ emit-evidence: ${rows.length} kernel-valid gate-result/v1 row(s) written to ${args.out}\n` +
      `  decisions: ${outcomes.map((o) => `${o.gateName}=${o.decision}`).join(', ')}\n` +
      `  next (CI): cosign sign-blob each bundle-<i>.json -> ci/assemble-manifest.ts -> report-manifest.json`,
  );
  return 0;
}

const invokedDirectly = process.argv[1]?.endsWith('emit-evidence.ts') === true;
if (invokedDirectly) {
  try {
    process.exit(main(process.argv.slice(2)));
  } catch (err: unknown) {
    console.error('emit-evidence FAILED (fail-closed):', err instanceof Error ? err.message : String(err));
    process.exit(1);
  }
}
