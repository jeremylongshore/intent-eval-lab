#!/usr/bin/env -S node --experimental-strip-types
/**
 * derive-corpus.ts — build the CANDIDATE public corpus for the `bbb-seed-v1` eval set.
 *
 * Reads the live governed brain (`~/.teamkb/teamkb.db`) READ-ONLY and emits a sanitized
 * candidate document set for human review. It is the executable half of `../ALLOWLIST.md`;
 * that document states why each rule exists and is NORMATIVE.
 *
 * THE LOAD-BEARING PROPERTY — this script never publishes.
 * ---------------------------------------------------------------------------
 * Every one of the brain's 17,321 memories is classified `sensitivity: 'internal'`; not one
 * is `'public'`. So there is no schema-level marker to filter on, and any public corpus is by
 * construction a decision to publish internally-classified content. That decision is a human's.
 * This script therefore writes to a REVIEW directory (`--out`, default `./.candidate/`), never
 * to `corpus/`, and there is deliberately no flag that changes that. Promotion into `corpus/`
 * is a manual step gated on operator sign-off recorded in `corpus/PROVENANCE.md`.
 *
 * NEVER WRITES WHAT IT DID NOT MATCH (ALLOWLIST.md Rule 3): a document is emitted only after
 * passing Rule 1 (category + lifecycle allowlist) and Rule 2 (zero risk markers) explicitly.
 * There is no default-accept branch. Risk markers cause REFUSAL, never redaction — a scrub-and-keep
 * path can partially fail; a refusal cannot.
 *
 * Zero dependencies: `node:sqlite` (built in, Node 22.5+) opened read-only.
 *
 * Usage:
 *   node --experimental-strip-types scripts/derive-corpus.ts [--db PATH] [--out DIR] [--limit N]
 *   node --experimental-strip-types scripts/derive-corpus.ts --report-only
 */

import { DatabaseSync } from 'node:sqlite';
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync, rmSync, existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const EVAL_ROOT = resolve(HERE, '..');

/** ALLOWLIST.md Rule 1 — structural eligibility. `reference` (94% of the brain) is refused wholesale. */
const ALLOWED_CATEGORIES = ['pattern', 'architecture', 'convention', 'decision', 'onboarding'] as const;
const ALLOWED_LIFECYCLE = 'active';

/**
 * ALLOWLIST.md Rule 2 — content refusal markers. Deliberately over-broad: a false refusal costs
 * one document out of a 608-deep pool; a false accept is unrecoverable once published, and if it
 * reaches a signed row it is anchored in an append-only transparency log that cannot be un-logged.
 */
const RISK_MARKERS: ReadonlyArray<readonly [string, RegExp]> = [
  ['ip_address', /\b(?:\d{1,3}\.){3}\d{1,3}\b/],
  ['email', /\b[\w.+-]+@[\w-]+\.[\w.]+\b/],
  ['abs_home_path', /\/home\/\w+/],
  ['secret_kw', /\b(api[_-]?key|token|passphrase|password|secret|credential)\b/i],
  ['long_hex_or_b64', /\b[A-Za-z0-9+/]{32,}={0,2}\b/],
  ['private_host', /\b(intentsolutions|tailnet|100\.\d+\.\d+\.\d+|contabo)\b/i],
  // NOTE: `person_name` is deliberately NOT in this list — see loadPersonNames() below.
];

/**
 * The `person_name` marker's terms live OUTSIDE this file, in the git-ignored
 * `.person-names.local` (one term per line, `#` comments allowed).
 *
 * Two reasons, both hard:
 *   1. intent-eval-lab is a PUBLIC repo. A tracked regex listing real individuals would publish
 *      "here are the people associated with this estate" — the exact disclosure the marker exists
 *      to prevent. A scrubbing rule must not itself be the leak.
 *   2. Some of those terms are partner names, and this repo enforces partner-name discipline
 *      (DR-004 S1Q2) via `.github/workflows/partner-name-guard.yml`, a case-insensitive CI grep.
 *      Hardcoding them here fails that gate — correctly.
 *
 * FAIL-CLOSED: with no local list the person-name rule cannot run, so the script REFUSES to derive
 * rather than silently applying six of seven rules and reporting a clean scan. Override only with
 * `--no-person-names`, which is loud and recorded in the derivation report, so a corpus derived
 * without the rule can never be mistaken for one derived with it.
 */
function loadPersonNames(): string[] | null {
  const p = resolve(EVAL_ROOT, '.person-names.local');
  if (!existsSync(p)) return null;
  return readFileSync(p, 'utf8')
    .split('\n')
    .map((l) => l.replace(/#.*$/, '').trim())
    .filter(Boolean);
}

function personNameMarker(terms: string[]): readonly [string, RegExp] {
  const escaped = terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  return ['person_name', new RegExp(`\\b(${escaped.join('|')})\\b`)];
}

interface MemoryRow {
  id: string;
  title: string;
  category: string;
  content: string;
  lifecycle: string;
  sensitivity: string;
  updated_at: string;
}

interface Decision {
  id: string;
  title: string;
  category: string;
  admitted: boolean;
  /** Empty iff admitted. Named rules, so any published doc traces to the rules that admitted it. */
  refused_by: string[];
}

function parseArgs(argv: string[]) {
  const get = (flag: string, fallback: string | null = null) => {
    const i = argv.indexOf(flag);
    return i >= 0 && argv[i + 1] ? argv[i + 1]! : fallback;
  };
  return {
    db: get('--db', join(homedir(), '.teamkb', 'teamkb.db'))!,
    out: resolve(get('--out', join(EVAL_ROOT, '.candidate'))!),
    limit: Number(get('--limit', '80')),
    reportOnly: argv.includes('--report-only'),
    noPersonNames: argv.includes('--no-person-names'),
  };
}

/** Rule 2. Returns the names of every marker that matched — empty means clean. */
function riskMarkers(row: MemoryRow, markers: ReadonlyArray<readonly [string, RegExp]>): string[] {
  const blob = `${row.title}\n${row.content}`;
  return markers.filter(([, rx]) => rx.test(blob)).map(([name]) => name);
}

/** The gold citation targets of the 42-query `governed-brain-v1` set, if present, sort first:
 *  a corpus that omits its own questions' answers measures nothing. */
function loadGoldIds(): Set<string> {
  const p = resolve(EVAL_ROOT, 'gold-ids.txt');
  if (!existsSync(p)) return new Set();
  const txt = readFileSync(p, 'utf8');
  return new Set(
    txt
      .split('\n')
      .map((l) => l.trim())
      .filter((l) => l && !l.startsWith('#')),
  );
}

function main(): void {
  const args = parseArgs(process.argv.slice(2));

  if (!existsSync(args.db)) {
    console.error(`derive-corpus: no brain database at ${args.db}`);
    process.exit(2);
  }

  // Assemble the active marker set. Fail closed if the person-name list is unavailable.
  const personNames = loadPersonNames();
  const markers = [...RISK_MARKERS];
  if (personNames && personNames.length > 0) {
    markers.push(personNameMarker(personNames));
  } else if (!args.noPersonNames) {
    console.error('derive-corpus: REFUSING TO DERIVE — the person_name rule cannot run.');
    console.error('');
    console.error(`  No term list at ${resolve(EVAL_ROOT, '.person-names.local')}.`);
    console.error('  That file is git-ignored on purpose: intent-eval-lab is a PUBLIC repo, so a');
    console.error('  tracked list of real individuals would itself be the disclosure this rule');
    console.error('  exists to prevent — and some terms are partner names, which the repo\'s');
    console.error('  partner-name-guard CI gate refuses outright (DR-004 S1Q2).');
    console.error('');
    console.error('  Create it (one term per line, # comments allowed), or re-run with');
    console.error('  --no-person-names to derive WITHOUT PII name screening. That flag is recorded');
    console.error('  in the derivation report so the resulting corpus can never be mistaken for');
    console.error('  one that was name-screened.');
    process.exit(2);
  }

  const db = new DatabaseSync(args.db, { readOnly: true });
  const placeholders = ALLOWED_CATEGORIES.map(() => '?').join(',');
  const rows = db
    .prepare(
      `SELECT id, title, category, content, lifecycle, sensitivity, updated_at
         FROM curated_memories
        WHERE lifecycle = ? AND category IN (${placeholders})
        ORDER BY id`,
    )
    .all(ALLOWED_LIFECYCLE, ...ALLOWED_CATEGORIES) as unknown as MemoryRow[];
  db.close();

  const gold = loadGoldIds();
  const decisions: Decision[] = [];
  const admitted: MemoryRow[] = [];
  /**
   * ESCALATED — gold-cited documents that Rule 2 refused.
   *
   * Rule 2 is deliberately over-broad, and its known cost is that a document ABOUT tokens or
   * secrets trips the same marker as a document CONTAINING one: "Token Passthrough", "Spool
   * Boundary Threat Model", and the platform's signature "Compile-Then-Govern Architecture" are
   * all refused for `secret_kw` on subject matter, not on a leaked value.
   *
   * Silently dropping them costs the eval its own answers — a query whose gold document is absent
   * from the corpus is unanswerable, and an eval that cannot answer its own signature question
   * measures nothing. But auto-admitting them would be exactly the default-accept path Rule 3
   * forbids.
   *
   * So they go to a THIRD bucket: refused from the candidate set, written separately with their
   * markers named, for a human to adjudicate one at a time. Nothing here is in the corpus, and
   * nothing here can reach the corpus without someone deciding it should.
   */
  const escalated: Array<{ row: MemoryRow; markers: string[] }> = [];

  for (const row of rows) {
    // Rule 2 — refusal, never redaction.
    const refused = riskMarkers(row, markers);
    decisions.push({
      id: row.id,
      title: row.title,
      category: row.category,
      admitted: refused.length === 0,
      refused_by: refused,
    });
    if (refused.length === 0) admitted.push(row);
    else if (gold.has(row.id)) escalated.push({ row, markers: refused });
  }

  // Gold-cited documents first, then deterministic id order — so a re-run with the same DB and
  // the same limit produces the same candidate set (no clock, no randomness).
  admitted.sort((a, b) => {
    const ga = gold.has(a.id) ? 0 : 1;
    const gb = gold.has(b.id) ? 0 : 1;
    return ga !== gb ? ga - gb : a.id.localeCompare(b.id);
  });

  const selected = Number.isFinite(args.limit) && args.limit > 0 ? admitted.slice(0, args.limit) : admitted;
  const goldCovered = selected.filter((r) => gold.has(r.id)).length;

  const markerTally: Record<string, number> = {};
  for (const d of decisions) for (const m of d.refused_by) markerTally[m] = (markerTally[m] ?? 0) + 1;

  const report = {
    generator: 'derive-corpus.ts',
    allowlist_doc: 'ALLOWLIST.md',
    // NOTE: no timestamp. The report is an input to MANIFEST.json hashing; a clock would make
    // every re-derivation produce a different hash and destroy reproducibility.
    source_db: args.db,
    rules: {
      allowed_categories: [...ALLOWED_CATEGORIES],
      allowed_lifecycle: ALLOWED_LIFECYCLE,
      risk_markers: markers.map(([n]) => n),
      // Recorded so a corpus derived without name screening is never mistaken for one with it.
      person_name_screening: personNames && personNames.length > 0
        ? `active (${personNames.length} terms from .person-names.local)`
        : 'DISABLED via --no-person-names — NOT name-screened',
    },
    eligible_pool: rows.length,
    admitted_by_content_scan: admitted.length,
    refused_by_content_scan: rows.length - admitted.length,
    refusal_tally: markerTally,
    selected_for_review: selected.length,
    gold_cited_in_selection: goldCovered,
    gold_ids_known: gold.size,
    // Gold documents Rule 2 refused. Each makes its query unanswerable until a human either
    // adjudicates the document in or the query is dropped from questions.yaml. Never auto-admitted.
    gold_escalated_for_adjudication: escalated.map((e) => ({
      id: e.row.id,
      title: e.row.title,
      refused_by: e.markers,
    })),
    decisions,
  };

  if (args.reportOnly) {
    console.log(JSON.stringify(report, null, 2));
    return;
  }

  // Write the CANDIDATE set — never `corpus/`. Recreate the dir so a re-run cannot leave a
  // stale document behind that no current rule admitted.
  rmSync(args.out, { recursive: true, force: true });
  mkdirSync(args.out, { recursive: true });

  for (const row of selected) {
    // Front matter mirrors the brain's own governance fields verbatim, INCLUDING
    // `sensitivity: internal` — the corpus must not launder the classification it came with.
    const doc = [
      '---',
      `id: ${row.id}`,
      `title: ${JSON.stringify(row.title)}`,
      `category: ${row.category}`,
      `source_sensitivity: ${row.sensitivity}`,
      `source_lifecycle: ${row.lifecycle}`,
      `qmd_uri: qmd://kb-curated/${row.id}.md`,
      '---',
      '',
      row.content.trimEnd(),
      '',
    ].join('\n');
    writeFileSync(join(args.out, `${row.id}.md`), doc, 'utf8');
  }

  // Escalations go to their own directory so they can never be mistaken for candidates.
  if (escalated.length > 0) {
    const escDir = join(args.out, 'escalated');
    mkdirSync(escDir, { recursive: true });
    for (const { row, markers } of escalated) {
      const doc = [
        '---',
        `id: ${row.id}`,
        `title: ${JSON.stringify(row.title)}`,
        `category: ${row.category}`,
        `source_sensitivity: ${row.sensitivity}`,
        `qmd_uri: qmd://kb-curated/${row.id}.md`,
        `refused_by: [${markers.join(', ')}]`,
        'status: ESCALATED — gold-cited but Rule 2 refused. NOT a candidate. NOT in the corpus.',
        'adjudication: pending human decision — admit with written justification, or drop the',
        '  dependent queries from questions.yaml. Auto-admitting is forbidden (ALLOWLIST.md Rule 3).',
        '---',
        '',
        row.content.trimEnd(),
        '',
      ].join('\n');
      writeFileSync(join(escDir, `${row.id}.md`), doc, 'utf8');
    }
  }

  writeFileSync(join(args.out, 'derivation-report.json'), `${JSON.stringify(report, null, 2)}\n`, 'utf8');

  const digest = createHash('sha256').update(JSON.stringify(report.decisions)).digest('hex');

  console.log(`derive-corpus: eligible pool ${rows.length} (Rule 1: ${ALLOWED_LIFECYCLE} + ${ALLOWED_CATEGORIES.join('/')})`);
  console.log(`               admitted ${admitted.length}, refused ${rows.length - admitted.length} (Rule 2 content scan)`);
  for (const [m, n] of Object.entries(markerTally).sort((a, b) => b[1] - a[1])) {
    console.log(`                 refused by ${m}: ${n}`);
  }
  console.log(`               selected ${selected.length} for review (${goldCovered} of ${gold.size} gold-cited)`);
  if (escalated.length > 0) {
    console.log(`               ESCALATED ${escalated.length} gold-cited doc(s) refused by Rule 2 — human adjudication required:`);
    for (const e of escalated) console.log(`                 [${e.markers.join(',')}] ${e.row.title}`);
    console.log(`               until adjudicated, the queries citing these are UNANSWERABLE and must be dropped.`);
  }
  console.log(`               decision-set sha256 ${digest}`);
  console.log('');
  console.log(`  → CANDIDATES written to ${args.out}`);
  console.log('    This is NOT the corpus. Nothing here is published.');
  console.log('    Every candidate carries `source_sensitivity: internal` — the brain classifies');
  console.log('    ALL 17,321 of its memories that way, so promoting any of this to corpus/ is a');
  console.log('    decision to publish internally-classified content.');
  console.log('    Next step is a HUMAN reading all of them, then recording sign-off in');
  console.log('    corpus/PROVENANCE.md. There is no flag that skips this.');
}

main();
