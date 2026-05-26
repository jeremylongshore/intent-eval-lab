# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning follows [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-05-10

First public release of the Intent Eval Lab repository — the methodology + specs umbrella for the Intent Eval Platform.

### Added

- Initial repository scaffold (`/repo-dress` 21-file canon, 8 governance files)
- Enterprise documentation set (6-doc planning suite)
- `README.md`, `LICENSE` (Apache 2.0), `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`
- CI/CD workflows (`lint.yml`, `test.yml`, release automation)
- GitHub issue templates + PR template
- Dependabot configuration
- `.editorconfig` + `.gitattributes`
- Beads issue tracking initialized at repo scope
- `specs/` Phase A convergence skeleton — Evidence Bundle skeleton + OpenTelemetry RFC draft (`000-docs/001-DR-RFC-otel-agent-rollout-gate-signals-draft.md`)
- `specs/mcp-plugin-observability/` reference module (Go as planned reference runner)
- Normative methodology output tree under `specs/`

### Changed

- `CLAUDE.md` — added three-repo convergence section + partner-name vendor-generic discipline (per DR-004 S1Q2)
- `CLAUDE.md` — clarified tier-1 (Evidence-Bundle-composing platform) vs tier-2 (independent lab research) constituent project distinction
- `CLAUDE.md` — updated absolute paths after move into `intent-eval-platform/` umbrella
- Part 2 ecosystem landscape report + Workstream-D synthesis + first ISEDC Decision Record

### Fixed

- `/validate-consistency` audit fixes — INDEX stale entries, README j-rig claim drift, PB-12 DR mapping

[Unreleased]: https://github.com/jeremylongshore/intent-eval-lab/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.1.0
