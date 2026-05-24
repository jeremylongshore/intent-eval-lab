#!/usr/bin/env node
/**
 * audit-harness CLI dispatcher
 *
 * Thin wrapper that invokes the canonical shell/python implementations in scripts/.
 * Keeping the scripts as-is (not a TS port) for v0.x — they're battle-tested
 * and language-portable. The CLI just adds discoverability + cross-platform-ish shell resolution.
 */
const { spawn } = require('node:child_process');
const { resolve, dirname } = require('node:path');
const { existsSync } = require('node:fs');

const SCRIPTS = resolve(__dirname, '..', 'scripts');

const COMMANDS = {
  'verify':        { script: 'harness-hash.sh',  args: ['--verify'] },
  'init':          { script: 'harness-hash.sh',  args: ['--init'] },
  'list':          { script: 'harness-hash.sh',  args: ['--list'] },
  'escape-scan':   { script: 'escape-scan.sh',   args: [] },
  'arch':          { script: 'arch-check.sh',    args: [] },
  'bias':          { script: 'bias-count.sh',    args: [] },
  'gherkin-lint':  { script: 'gherkin-lint.sh',  args: [] },
  'crap':          { script: 'crap-score.py',    args: [] },
  'emit-evidence': { script: 'emit-evidence.sh', args: [] },
};

function usage() {
  console.log(`audit-harness — deterministic test-enforcement toolkit

Usage:
  audit-harness <command> [args...]

Commands:
  verify                   Verify hash-pinned artifacts (exit 2 = HARNESS_TAMPERED)
  init                     Initialize or re-init the .harness-hash manifest
  list                     List currently pinned files
  escape-scan <source>     Scan a diff for escape attempts
                           source: --staged | --range A..B | - (stdin) | path.patch
  arch                     Run architecture-rule checks (Wall 7)
  bias                     Count test-bias patterns (tautology, smoke-only, etc.)
  gherkin-lint             Advisory Gherkin quality check
  crap [args...]           CRAP complexity × coverage scorer (multi-language)
  emit-evidence            Wrap a gate-result JSON envelope in an in-toto
                           Statement v1 (predicate https://evals.intentsolutions.io/gate-result/v1)
                           Read JSON on stdin: <gate> --json | audit-harness emit-evidence

Evidence Bundle (v0.3.0+):
  All gates support --json to emit machine-readable gate-result envelopes
  suitable for piping to emit-evidence. See SEMVER.md for compatibility rules
  and intent-eval-lab/specs/evidence-bundle/v0.1.0-draft/SPEC.md for the
  envelope schema.

Options:
  --version, -v            Print version
  --help, -h               Print this help

Exit codes (escape-scan):
  0 = clean
  1 = CHALLENGE (engineer-approved comment required)
  2 = REFUSE (pipeline halted)
`);
}

const [cmd, ...rest] = process.argv.slice(2);

if (!cmd || cmd === '--help' || cmd === '-h') {
  usage();
  process.exit(0);
}

if (cmd === '--version' || cmd === '-v') {
  const pkg = require('../package.json');
  console.log(pkg.version);
  process.exit(0);
}

const entry = COMMANDS[cmd];
if (!entry) {
  console.error(`audit-harness: unknown command '${cmd}'`);
  usage();
  process.exit(2);
}

const scriptPath = resolve(SCRIPTS, entry.script);
if (!existsSync(scriptPath)) {
  console.error(`audit-harness: script not found at ${scriptPath}`);
  process.exit(2);
}

const isPython = entry.script.endsWith('.py');
const interpreter = isPython ? 'python3' : 'bash';
const finalArgs = [scriptPath, ...entry.args, ...rest];

const child = spawn(interpreter, finalArgs, { stdio: 'inherit' });
child.on('exit', (code, signal) => {
  if (signal) {
    console.error(`audit-harness: ${entry.script} killed by ${signal}`);
    process.exit(128);
  }
  process.exit(code ?? 0);
});
child.on('error', (err) => {
  console.error(`audit-harness: failed to spawn ${interpreter}: ${err.message}`);
  process.exit(2);
});
