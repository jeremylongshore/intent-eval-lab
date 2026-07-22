#!/usr/bin/env node
/**
 * verify-manifest.mjs — verify the `bbb-seed-v1` corpus against its pinned MANIFEST.json.
 *
 * The roster refuses to run against an unpinned corpus — the same invariant as `roster.source.ref`.
 * A published number is only reproducible if the bytes it was produced from are pinned, so this is
 * the gate that makes "reproduce our result" a real instruction rather than a hopeful one.
 *
 * Checks, all fail-closed:
 *   1. MANIFEST.json exists and parses.
 *   2. Every file the manifest pins exists on disk and its sha256 matches.
 *   3. No file in `corpus/` is MISSING from the manifest — an unpinned document that the eval
 *      nonetheless reads is exactly the hole this guards. (Extra-file detection matters more than
 *      hash mismatch: a mismatch is loud, an unpinned addition is silent.)
 *   4. The question bank is pinned too, not just the corpus. Swapping the questions changes the
 *      measurement as surely as swapping the documents.
 *
 * Zero dependencies. Exit 0 = green, 1 = drift, 2 = structural (missing/unparseable manifest).
 *
 * Usage: node evals/bbb-seed-v1/scripts/verify-manifest.mjs [--root DIR]
 */

import { createHash } from 'node:crypto';
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, resolve, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const rootFlag = argv.indexOf('--root');
const ROOT = resolve(rootFlag >= 0 && argv[rootFlag + 1] ? argv[rootFlag + 1] : resolve(HERE, '..'));

const MANIFEST_PATH = join(ROOT, 'MANIFEST.json');

function fail(code, msg) {
  console.error(`verify-manifest: ${msg}`);
  process.exit(code);
}

function sha256(path) {
  return createHash('sha256').update(readFileSync(path)).digest('hex');
}

/** Every file under dir, recursively, as paths relative to ROOT. */
function walk(dir) {
  if (!existsSync(dir)) return [];
  const out = [];
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else out.push(relative(ROOT, p));
  }
  return out.sort();
}

if (!existsSync(MANIFEST_PATH)) {
  fail(2, `no MANIFEST.json at ${MANIFEST_PATH} — the corpus is UNPINNED and must not be run against.`);
}

let manifest;
try {
  manifest = JSON.parse(readFileSync(MANIFEST_PATH, 'utf8'));
} catch (err) {
  fail(2, `MANIFEST.json does not parse: ${err.message}`);
}

const pinned = manifest.files ?? {};
const pinnedPaths = Object.keys(pinned).sort();
if (pinnedPaths.length === 0) {
  // An empty manifest that reports OK is the hollow-gate failure — refuse it explicitly.
  fail(2, 'MANIFEST.json pins ZERO files. An empty manifest verifies nothing; refusing to report green.');
}

const problems = [];

// Checks 1 + 2 — every pinned file present and unchanged.
for (const rel of pinnedPaths) {
  const abs = join(ROOT, rel);
  if (!existsSync(abs)) {
    problems.push(`MISSING   ${rel} — pinned by the manifest but not on disk`);
    continue;
  }
  const actual = sha256(abs);
  const expected = pinned[rel].sha256 ?? pinned[rel];
  if (actual !== expected) {
    problems.push(`MISMATCH  ${rel}\n            expected ${expected}\n            actual   ${actual}`);
  }
}

// Check 3 — nothing in corpus/ escapes the pin.
const onDisk = walk(join(ROOT, 'corpus'));
const pinnedSet = new Set(pinnedPaths);
for (const rel of onDisk) {
  if (!pinnedSet.has(rel)) {
    problems.push(`UNPINNED  ${rel} — present in corpus/ but absent from the manifest`);
  }
}

// Check 4 — the question bank is pinned.
const QUESTIONS = 'questions.yaml';
if (existsSync(join(ROOT, QUESTIONS)) && !pinnedSet.has(QUESTIONS)) {
  problems.push(`UNPINNED  ${QUESTIONS} — the question bank must be pinned; changing the questions changes the measurement`);
}

if (problems.length > 0) {
  console.error(`verify-manifest: ${problems.length} problem(s) against ${manifest.manifest_version ?? 'unknown manifest version'}\n`);
  for (const p of problems) console.error(`  ${p}`);
  console.error('\nThe corpus does NOT match its pin. Do not run the roster against it and do not');
  console.error('publish any number derived from it until this is resolved.');
  process.exit(1);
}

console.log(`verify-manifest: OK — ${pinnedPaths.length} file(s) pinned and matching`);
console.log(`  manifest: ${manifest.manifest_version ?? '(no version)'}  frozen_at: ${manifest.frozen_at ?? '(not frozen)'}`);
console.log(`  corpus:   ${onDisk.length} file(s), all pinned`);
