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

## Conventions

- **Branch naming**: `feat/...`, `fix/...`, `docs/...`, `research/...`, `chore/...` — kebab-case description
- **Commit messages**: [Conventional Commits](https://www.conventionalcommits.org/) — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `research:`, `test:`
- **Doc filing**: numbered + dated + category-coded under `000-docs/` per the doc-filing standard. See existing docs for examples.
- **One-sentence-per-line markdown** in body prose where practical (eases review diffs)

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
