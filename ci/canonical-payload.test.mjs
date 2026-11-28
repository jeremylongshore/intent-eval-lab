import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { EvidenceBundlePayloadSchema } from '@intentsolutions/core/validators/v1/evidence-statement';
import { assemble } from './assemble-manifest.ts';
import { buildEvidenceBundle, buildRows, stableStringify, writeEmit } from './emit-evidence.ts';

const context = {
  nowIso: '2026-10-12T00:00:00.000Z',
  nowMs: 1791763200000,
  commitSha: 'a'.repeat(40),
  sourceSha: 'a'.repeat(40),
  policyHash: `sha256:${'b'.repeat(64)}`,
  runnerVersion: '0.1.0',
  rand16: () => new Uint8Array(16),
};
const outcomes = ['pass', 'fail', 'advisory', 'error'].map((decision) => ({
  gateName: `synthetic-${decision}`,
  gateVersion: '1.0.0',
  decision,
  reasons: ['synthetic contract fixture; no live gate measurement'],
  dimensionsEvaluated: decision === 'error' ? [] : ['provenance-integrity'],
  dimensionsSkipped: decision === 'error' ? ['provenance-integrity'] : [],
  ...(decision === 'advisory' ? { advisorySeverity: 'warn' } : {}),
  ...(decision === 'fail' || decision === 'error' ? { failureMode: 'fixture-error' } : {}),
}));

function emitted(t) {
  const dir = mkdtempSync(join(tmpdir(), 'iel-canonical-payload-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const rows = buildRows(outcomes, context);
  const skeleton = writeEmit(rows, 'refs/tags/v0.3.0', dir);
  for (let i = 0; i < rows.length; i++) {
    // The assembler transports signatures; CI and ingest verify real signatures.
    writeFileSync(join(dir, `bundle-${i}.sigstore.json`), '{}');
  }
  return { dir, rows, skeleton };
}

test('metadata matches the independently calculated synthetic vector', () => {
  // Unsigned synthetic vector, expected bytes independently calculated in Python.
  assert.equal(
    JSON.parse(
      readFileSync(new URL('./node_modules/@intentsolutions/core/package.json', import.meta.url)),
    ).version,
    '0.10.0',
  );
  const fixture = JSON.parse(
    readFileSync(new URL('./canonical-payload.fixture.json', import.meta.url)),
  );
  assert.deepEqual(fixture.row.gateResult, fixture.row.evidencePayload[0].predicate);
  assert.deepEqual(fixture.row.gateResults, [fixture.row.gateResult]);
  const bundle = buildEvidenceBundle(fixture.row.evidencePayload, context);
  assert.deepEqual(bundle, fixture.row.bundle);
  assert.equal(stableStringify(bundle), fixture.row.canonicalBundle);
});

test('pass, fail, advisory and unavailable rows bind complete canonical statement bytes', (t) => {
  const { dir, rows } = emitted(t);
  const manifest = assemble(dir);
  assert.equal(manifest.repo, 'iel');
  assert.equal(manifest.rows.length, 4);
  assert.equal(
    manifest.signing.subject,
    'repo:jeremylongshore/intent-eval-lab:ref:refs/tags/v0.3.0',
  );
  assert.equal(
    manifest.signing.workflowRef,
    'jeremylongshore/intent-eval-lab/.github/workflows/release.yml@refs/tags/v0.3.0',
  );
  for (const [i, row] of rows.entries()) {
    EvidenceBundlePayloadSchema.parse(row.evidencePayload);
    const statement = row.evidencePayload[0];
    assert.equal(statement.predicate.gate_decision, outcomes[i].decision);
    assert.deepEqual(statement.predicate, row.gateResult);
    assert.equal(statement.subject[0].name, row.gateResult.gate_id);
    assert.equal(statement.subject[0].digest.sha256, row.gateResult.input_hash.slice(7));
    const bytes = readFileSync(join(dir, `evidence-payload-${i}.json`), 'utf8');
    assert.equal(bytes, stableStringify(row.evidencePayload));
    assert.equal(
      row.bundle.storage_key,
      `sha256:${createHash('sha256').update(bytes).digest('hex')}`,
    );
    assert.notEqual(
      row.bundle.storage_key,
      `sha256:${createHash('sha256').update(stableStringify(row.gateResult)).digest('hex')}`,
    );
    assert.deepEqual(manifest.rows[i], {
      bundle: row.bundle,
      sigstoreBundle: {},
      sourceSha: context.commitSha,
      evidencePayload: row.evidencePayload,
      gateResults: [row.gateResult],
    });
  }
});

for (const field of ['storage_key', 'row_count', 'subject_set', 'predicate_uri_set']) {
  test(`assembly rejects changed signed ${field}`, (t) => {
    const { dir, rows } = emitted(t);
    const bundle = structuredClone(rows[0].bundle);
    bundle[field] = {
      storage_key: `sha256:${'f'.repeat(64)}`,
      row_count: 2,
      subject_set: [],
      predicate_uri_set: [],
    }[field];
    writeFileSync(join(dir, 'bundle-0.json'), stableStringify(bundle));
    assert.throws(() => assemble(dir), new RegExp(`signed bundle ${field}`));
  });
}

for (const variant of [
  'payload',
  'body',
  'missing-payload',
  'statement-invariant',
  'subject-digest',
]) {
  test(`assembly refuses ${variant} mutation without legacy fallback`, (t) => {
    const { dir, skeleton } = emitted(t);
    const row = skeleton.rows[0];
    if (variant === 'payload') row.evidencePayload[0].extensions = { tampered: true };
    if (variant === 'body')
      row.gateResults[0] = { ...row.gateResults[0], gate_reasons: ['tampered'] };
    if (variant === 'missing-payload') delete row.evidencePayload;
    if (variant === 'statement-invariant') row.evidencePayload[0].subject[0].name = 'wrong';
    if (variant === 'subject-digest')
      row.evidencePayload[0].subject[0].digest.sha256 = 'f'.repeat(64);
    writeFileSync(join(dir, 'manifest-skeleton.json'), JSON.stringify(skeleton));
    const expected = {
      payload: /signed bundle storage_key/,
      body: /gateResults do not match evidencePayload predicates/,
      'missing-payload': /expected array, received undefined/,
      'statement-invariant': /subject\[0\]\.name must equal predicate\.gate_id/,
      'subject-digest': /subject\[0\]\.digest\.sha256/,
    }[variant];
    assert.throws(() => assemble(dir), expected);
  });
}

test('assembly fails on a missing signature file', (t) => {
  const { dir } = emitted(t);
  rmSync(join(dir, 'bundle-0.sigstore.json'));
  assert.throws(() => assemble(dir), /missing sigstore bundle/);
});
