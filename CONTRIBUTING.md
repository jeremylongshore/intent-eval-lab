# Contributing to Intent Eval Lab

Thanks for your interest in contributing. This repo is currently maintained by a single author (Jeremy Longshore / Intent Solutions LLC) — review cycles are slower than a multi-maintainer project, but contributions are welcome.

## What this repo accepts

- Research notes, literature surveys, and competitive landscape additions to `research/`
- New experiment sandboxes under `sandboxes/YYYY-MM-DD-<name>/` (with `REPORT.md`)
- Methodology proposals as numbered docs in `000-docs/`
- Reusable test-harness scripts in `scripts/`
- Corrections to existing methodology or evidence interpretation
- Citations to relevant academic work, blog posts, or open-source tools

## What this repo does NOT accept

- PRs to constituent projects (`projects/` is a symlink — those projects accept PRs in their own repos)
- Pure marketing content
- Speculative methodology without empirical evidence (research docs that can't point to a sandbox run)

## Process

1. **Open an issue first** for anything beyond a typo or doc fix. Describe what you'd like to contribute and why. Most issues get a response within 7 business days.
2. **Fork the repo** and create a branch named `feat/<short-description>`, `fix/<short-description>`, `docs/<short-description>`, or `research/<short-description>`.
3. **Sign your commits** with `git commit -s` (DCO sign-off). The `Signed-off-by:` line certifies you have the right to contribute under the project's license (Apache 2.0).
4. **Open a PR** referencing the issue. Keep it focused — one logical change per PR.
5. **Expect feedback within ~7 business days.** A solo maintainer means slower turnaround. Patience appreciated.

External-contributor PRs should include the exact line
`contributor-acknowledgment: bd-claim-precheck` in the PR body. The claim
precheck workflow reports a missing acknowledgment as a warning for maintainer
review; it does not hard-block fork contributions.

## Conventions

- **Branch naming**: `feat/...`, `fix/...`, `docs/...`, `research/...`, `chore/...` — kebab-case description
- **Commit messages**: [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `research:`, `test:`
- **Doc filing**: numbered + dated + category-coded under `000-docs/` per the doc-filing standard. See existing docs for examples.
- **One-sentence-per-line markdown** in body prose where practical (eases review diffs)

### Cross-repository references

Beads is the canonical writer for bead↔document↔GitHub cross-references. When
an issue and document are linked, run `bd-sync project <bead>` from the shared
`~/000-projects` beads workspace. The command owns only the marked
`BD-SYNC:cross-ref:v1` block; edit the bead and re-project rather than editing
inside that block. A mutated or partial block is a fail-closed anomaly.

## Local git hooks (optional)

The tracked `.beads/hooks/` scripts preserve Beads integration and run the public-surface scrub before commits.
Enable them from the primary checkout or a linked worktree:

```bash
lab_primary=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
git config --local core.hooksPath "$lab_primary/.beads/hooks"
git config --show-origin --get core.hooksPath
```

Run this setup again after relocating the primary checkout; Git retains an absolute path that does not follow a move.
Linked worktrees share this configuration, while the scrub resolves the current worktree and checks its staged changes.
Keep the repository-owned scrub after the managed Beads section: it must still run if `bd` is unavailable, its database is uninitialized, or its hook times out.
Python 3 is required; a missing scanner, interpreter or policy blocks the commit.
CI remains authoritative for contributors who have not enabled local hooks.

The optional [pre-commit](https://pre-commit.com) framework adds `ruff`, Markdown and hygiene checks.
Run `pre-commit run --all-files` manually instead of replacing the managed Git hooks.
If the framework's Node bootstrap rejects `--ignore-prepublish` with the system npm, use an isolated compatible npm invocation:

```bash
npm exec --yes --package npm@10.9.2 -- pre-commit run --all-files
```

This does not change the globally installed npm version.
The alternative `lefthook.yml` remains available for contributors who intentionally manage their own hook chain; do not run competing installers over the tracked Beads hooks.

### Preserve captured evidence

The optional framework's mutating hooks exclude `archive/raw/`, `specs/_vendor/`,
`_vendor/`, `.audit-harness/`, `research/**/results/`, and JSON/JSONL records under
`evidence/`. Their exact bytes carry capture hashes, vendor provenance or signed
evidence. Update them through the owning capture, re-vendoring or signing process.
Read-only syntax/conflict checks and the existing public-content scrub still run
under their own policies. Authored scripts, tests, configuration and evidence
README files remain subject to formatting checks.

For a focused change, use `pre-commit run --files PATH...`. A full
`pre-commit run --all-files` can still fix pre-existing formatting in authored
files; review those changes separately and do not commit unrelated cleanup.
The prior baseline run changed 165 files across captures and authored content;
protecting evidence does not settle the remaining source-formatting backlog.
Run `python3 scripts/check-hygiene-preservation.py` to exercise the real configured
hooks in a disposable Git fixture and verify captured bytes stay unchanged.

## Sandbox contributions

If you're contributing a new experiment sandbox:

- Create the dir as `sandboxes/YYYY-MM-DD-<short-id>/`
- Include a `REPORT.md` with: hypothesis, methodology, prompts/fixtures used, evidence captured, findings, threats to validity
- Reference any reusable code in `scripts/` or note where the experiment-specific code lives
- Keep evidence captures (JSON, screenshots, OTEL traces) to a reasonable size — large captures should be summarized in the report and the raw data linked from external storage rather than committed

## DCO sign-off

Every commit must be signed off:

```bash
git commit -s -m "feat: add cross-CLI invocation comparison sandbox"
```

The `-s` flag appends a `Signed-off-by: Your Name <your@email>` line. By signing off, you certify the contribution complies with the [Developer Certificate of Origin](https://developercertificate.org/).

## Questions

- General questions → open a GitHub issue with the `question` label
- Security concerns → see [SECURITY.md](SECURITY.md) for responsible disclosure
- Anything time-sensitive → email the maintainer directly via the contact info on [intentsolutions.io](https://intentsolutions.io)

## Code of Conduct

This project follows the Contributor Covenant. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). By participating you agree to uphold it.
