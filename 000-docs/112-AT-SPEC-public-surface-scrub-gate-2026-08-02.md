# 112 · AT · SPEC — Public-surface PII and secret scrub gate

| Field | Value |
| --- | --- |
| **Date** | 2026-08-02 |
| **Status** | **NORMATIVE IMPLEMENTATION SPEC** |
| **Authority** | `109-AT-DECR-isedc-governed-judgment-layer-2026-07-12.md` §7 conditions 2–4 and §10 |
| **Bead** | `iel-25a.5.2` |
| **GitHub** | `intent-eval-lab#289` |
| **Plane** | `LAB-135` |

## Decision

Public-surface protection is a changed-lines gate. The scanner reviews only
lines added by a staged diff or a pull-request diff, so pre-existing public
history is not silently rewritten while new exposure is blocked before merge.
An explicit `--path`/`--all` mode supports repository audits and fixture tests.

The implementation is standard-library Python and reads a committed JSON policy.
It performs no network calls and needs no API key, model, hosted service, or
private corpus. A finding reports only the repository-relative path, line, and
detector identifier; matched content is never printed.

## Detector contract

The policy has two scopes:

- **Public scope** covers README and governance files, `.github/`, `000-docs/`,
  `docs/`, `specs/`, `research/`, `evals/`, `site/`, examples, and fixtures.
  It blocks configured personal identifiers, private-brain identifiers,
  partner names, email addresses, and US Social Security number-shaped values.
- **All-file scope** covers every non-exempt changed text file. It blocks
  private-key headers, cloud/provider tokens, GitHub tokens, bearer tokens, and
  credential-shaped assignments.

Generated, vendored, private, and fixture-test paths are explicit policy
exemptions. Adding or changing an exemption is itself a reviewable policy
change; the scanner fails closed on malformed policy, unreadable text, or Git
diff errors.

## Enforcement surfaces

- `lefthook.yml` runs the staged scan for contributors using Lefthook.
- `.pre-commit-config.yaml` runs the same command for the repository's
  pre-commit framework.
- `.github/workflows/public-surface-scrub.yml` scans pull-request and main-push
  added lines with full Git history available.

The existing partner-name workflow remains a complementary public-artifact
backstop. This gate owns PII, private-brain, and credential-shaped detection;
it does not claim to replace secret-management tooling or human consent review.

## Safe operation

When a finding appears, remove or synthesize the data, then rerun the scanner.
Do not paste the matched value into an issue, PR comment, log, or test output.
False-positive policy changes require a bead and review because the policy is a
public-flip control, not a convenience lint rule.
