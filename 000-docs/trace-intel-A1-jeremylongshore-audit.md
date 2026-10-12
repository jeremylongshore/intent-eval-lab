# A1 — Account repository evidence audit

**Status: DRAFT — owner sign-off pending; A3 remains blocked.**

Bead: `bd_000-projects-h08j.8.1`. Account: `jeremylongshore`. Observation date: **2026-10-12 UTC**. This is the repository census and evidence map for the trace-intelligence audit, not an architecture decision, production-readiness assessment or authorization to adopt a component.

## Coverage and disclosure

The authenticated census contains **184 owned repositories: 159 public and 25 private**, including **53 forks**. Public listing and authenticated owner listing were reconciled by GitHub repository ID. Every repository has an independently successful `gh repo view --json visibility` receipt, pinned default-branch SHA, reachable commit count, GitHub license metadata, complete recursive tree and fully paginated tag/release enumeration. The trees contain **148,763 files**; none was truncated.

The Contents API verified **1669/1669 selected files** at those exact commits. All workflow and changelog filenames were requested; up to three ranked filename candidates per category and the root README were also inspected. **136 repositories** have at least one lexical match in the inspected material. Keyword hits can be tests, documentation, generic language annotations or ordinary stack traces: the references below are discovery evidence, not proof of a trace-intelligence capability. Uninspected candidates and negative results remain explicit; no whole-repository absence claim is made.

The public projection retains one row for every repository. **29 repository identities** and any policy-restricted file references are withheld; the complete local owner annex binds each alias to its actual repository, metadata and references. This preserves the lab's partner-consent, private-brain and private-repository boundaries. It does not remove those repositories from audit scope. The owner must review the annex as well as this projection before sign-off.

Owner-annex SHA-256: `d8812e01e4a3e4b0c6e0af04c09825dda1815395c8d587d6ecfdeb07e0044425`. Its location and API receipt directory are recorded on the Bead. The annex is a local audit artifact, not a committed public asset.

## Reproduction and interpretation

The collector used the authenticated `gh` CLI and stable REST API version `2022-11-28`; it performed no clone, source mutation, workflow dispatch, release or deployment. The listing commands were:

```bash
gh api --paginate --slurp 'users/jeremylongshore/repos?per_page=100&type=owner&sort=full_name'
gh api --paginate --slurp 'user/repos?per_page=100&affiliation=owner&visibility=all&sort=full_name'
```

The deterministic projection flattens both page arrays, selects `owner.login == "jeremylongshore"`, deduplicates by repository ID and sorts by `full_name`. For each repository, the collector records:

- `gh repo view OWNER/REPO --json visibility`; the result must agree with REST visibility.
- `GET /repos/OWNER/REPO/commits?per_page=1`: first SHA and the last-page number give the observed default-branch reachable commit count. This is not a count across every branch.
- `GET /repos/OWNER/REPO/git/trees/TREE_SHA?recursive=1`: complete filename census. Truncation is checked explicitly.
- `GET /repos/OWNER/REPO/contents/PATH?ref=COMMIT_SHA`: HTTP 200, blob SHA, decoded content SHA-256 and matching line numbers. Every published file reference has this receipt.
- Fully paginated `tags` and `releases` endpoints. Release-body matches are retained privately; linked release text may subsequently change.

Discovery terms cover trace/trajectory, telemetry/OpenTelemetry/observability, annotation/human review/labeling, eval/benchmark/grading/scoring, evidence/attestation/Sigstore/Rekor, and taxonomy/failure classification. Candidate selection prefers authored source over tests, dependencies and prose. Paths are not invented; tree-only candidates are never presented as Contents-verified evidence.

GitHub license metadata is reported literally. `NOASSERTION` or an unclassified result does not prove the repository lacks a license. Forks are retained and labeled; inherited upstream code is not claimed as an internally owned platform capability. Each repository has its own observation time, so the census is not an atomic estate snapshot.

## Known aliases and missing-reference check

The audit reconciled 92 names from existing local remotes, the umbrella ecosystem manifest and documented historical aliases. Six unlisted names resolved to listed canonical repositories with **HTTP 200**. The CLI exposed the final response only; no redirect status is invented. No tested reference returned 404 or 410. This finite baseline cannot enumerate deleted repositories that have no surviving reference.

| Requested name                                    | Canonical repository                         | Observed status |
| ------------------------------------------------- | -------------------------------------------- | --------------- |
| `jeremylongshore/audit-harness`                   | `jeremylongshore/intent-audit-harness`       | 200             |
| `jeremylongshore/claude-code-plugins`             | `jeremylongshore/tons-of-skills-marketplace` | 200             |
| `jeremylongshore/claude-code-plugins-plus-skills` | `jeremylongshore/tons-of-skills-marketplace` | 200             |
| `jeremylongshore/excel-analyst-pro`               | `jeremylongshore/excel-analyst-pro-skill-md` | 200             |
| `jeremylongshore/iam-bob-adk`                     | `jeremylongshore/iam-bob-adk-python`         | 200             |
| `jeremylongshore/j-rig-binary-eval`               | `jeremylongshore/j-rig-skill-binary-eval`    | 200             |

## Repository evidence map

Line ranges link to the observed commit. “No positive reference” is a bounded sample result, not evidence that a feature is absent. The owner annex retains all inspected references and remaining filename candidates.

### A1-R001: .github

Repository: [jeremylongshore/.github](https://github.com/jeremylongshore/.github). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **11**; head: `2a5a6248c4aecb4dc91f8e6e252722c78ad14149`. GitHub license metadata: **unclassified by GitHub**. Tree: **6 files**, complete. Observation: `2026-10-12T06:29:21Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R002

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R003: Content-Nuke-Claude

Repository: [jeremylongshore/Content-Nuke-Claude](https://github.com/jeremylongshore/Content-Nuke-Claude). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **25**; head: `8d794376ec52e1b8a9d80d694d38a6c61700d68c`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **102 files**, complete. Observation: `2026-10-12T06:29:21Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 4 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R004: DiagnosticPro

Repository: [jeremylongshore/DiagnosticPro](https://github.com/jeremylongshore/DiagnosticPro). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **189**; head: `92b7f1def2a3ec0912aca85cadeb89006d6c2fa4`. GitHub license metadata: **AGPL-3.0**. Tree: **785 files**, complete. Observation: `2026-10-12T06:29:24Z`.

- **Trace:** [`CHANGELOG.md` L330–332](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/CHANGELOG.md#L330-L332) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`tests/prompt-eval/judge.mjs` L2–4](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/tests/prompt-eval/judge.mjs#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`05-scripts/smoke-evidence.sh` L2–4](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/05-scripts/smoke-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L10–12](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/.github/workflows/minimax-review.yml#L10-L12) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/deploy.yml` L109–111](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/.github/workflows/deploy.yml#L109-L111); [`.github/workflows/minimax-review.yml` L10–12](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/.github/workflows/minimax-review.yml#L10-L12).
- **Release/changelog evidence:** 21 tags and 4 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L11–13](https://github.com/jeremylongshore/DiagnosticPro/blob/92b7f1def2a3ec0912aca85cadeb89006d6c2fa4/CHANGELOG.md#L11-L13).
- **Verification scope:** 11/11 Contents requests returned HTTP 200; 157 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R005: Hybrid-ai-stack-intent-solutions

Repository: [jeremylongshore/Hybrid-ai-stack-intent-solutions](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **31**; head: `2332f444b88318e62478147657efc046713caf2a`. GitHub license metadata: **MIT**. Tree: **129 files**, complete. Observation: `2026-10-12T06:29:24Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/blob/2332f444b88318e62478147657efc046713caf2a/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`scripts/benchmark_ternary.py` L3–5](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/blob/2332f444b88318e62478147657efc046713caf2a/scripts/benchmark_ternary.py#L3-L5) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/blob/2332f444b88318e62478147657efc046713caf2a/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/blob/2332f444b88318e62478147657efc046713caf2a/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 3 tags and 3 releases enumerated; 1 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/blob/2332f444b88318e62478147657efc046713caf2a/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L89–91](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/blob/2332f444b88318e62478147657efc046713caf2a/CHANGELOG.md#L89-L91); [release `v1.1.0`](https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions/releases/tag/v1.1.0).
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R006: No-You-Pick. (repository)

Repository: [jeremylongshore/No-You-Pick.](https://github.com/jeremylongshore/No-You-Pick.). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **47**; head: `2e661238a14a65ba417641eeb2a682e641a57f01`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **74 files**, complete. Observation: `2026-10-12T06:29:24Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R007: OmaSafe

Repository: [jeremylongshore/OmaSafe](https://github.com/jeremylongshore/OmaSafe). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **2**; head: `2fc424d544581b7715fbe86de4daca3c70d3ffa0`. GitHub license metadata: **MIT**. Tree: **10 files**, complete. Observation: `2026-10-12T06:29:26Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R008: ServiceGraph

Repository: [jeremylongshore/ServiceGraph](https://github.com/jeremylongshore/ServiceGraph). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **45**; head: `1ec908c0724a48410c0d00fac46df96651d6d9a1`. GitHub license metadata: **MIT**. Tree: **61 files**, complete. Observation: `2026-10-12T06:29:26Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`eval/find-cpa-firm/run.sh` L2–4](https://github.com/jeremylongshore/ServiceGraph/blob/1ec908c0724a48410c0d00fac46df96651d6d9a1/eval/find-cpa-firm/run.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L469–471](https://github.com/jeremylongshore/ServiceGraph/blob/1ec908c0724a48410c0d00fac46df96651d6d9a1/README.md#L469-L471) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 32 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R009: a2a-samples

Repository: [jeremylongshore/a2a-samples](https://github.com/jeremylongshore/a2a-samples). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **327**; head: `44ed6197f493ed7120e969ca8cbc691fe0df743d`. GitHub license metadata: **Apache-2.0**. Tree: **714 files**, complete. Observation: `2026-10-12T06:29:27Z`.

- **Trace:** [`samples/python/agents/a2a_telemetry/__main__.py` L12–14](https://github.com/jeremylongshore/a2a-samples/blob/44ed6197f493ed7120e969ca8cbc691fe0df743d/samples/python/agents/a2a_telemetry/__main__.py#L12-L14) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`samples/python/agents/a2a_telemetry/__main__.py` L12–14](https://github.com/jeremylongshore/a2a-samples/blob/44ed6197f493ed7120e969ca8cbc691fe0df743d/samples/python/agents/a2a_telemetry/__main__.py#L12-L14) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 2 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R010: agent-brain

Repository: [jeremylongshore/agent-brain](https://github.com/jeremylongshore/agent-brain). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **621**; head: `1d6132582db3392acdf1b44b1c6bc322c84f2607`. GitHub license metadata: **MIT**. Tree: **1349 files**, complete. Observation: `2026-10-12T06:29:29Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`docs/CHANGELOG.md` L30–32](https://github.com/jeremylongshore/agent-brain/blob/1d6132582db3392acdf1b44b1c6bc322c84f2607/docs/CHANGELOG.md#L30-L32) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`scripts/query_benchmark.py` L810–812](https://github.com/jeremylongshore/agent-brain/blob/1d6132582db3392acdf1b44b1c6bc322c84f2607/scripts/query_benchmark.py#L810-L812) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`scripts/query_benchmark.py` L2–4](https://github.com/jeremylongshore/agent-brain/blob/1d6132582db3392acdf1b44b1c6bc322c84f2607/scripts/query_benchmark.py#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`docs/CHANGELOG.md` L67–69](https://github.com/jeremylongshore/agent-brain/blob/1d6132582db3392acdf1b44b1c6bc322c84f2607/docs/CHANGELOG.md#L67-L69) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 4 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 30 tags and 0 releases enumerated; 0 release records have lexical matches. [`docs/CHANGELOG.md` L18–20](https://github.com/jeremylongshore/agent-brain/blob/1d6132582db3392acdf1b44b1c6bc322c84f2607/docs/CHANGELOG.md#L18-L20).
- **Verification scope:** 10/10 Contents requests returned HTTP 200; 9 other filename candidates remain uninspected. All 4 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R011: agent-governance-plane

Repository: [jeremylongshore/agent-governance-plane](https://github.com/jeremylongshore/agent-governance-plane). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **275**; head: `2076dec5264a194e28302fbb1ce26a5d0305a576`. GitHub license metadata: **Apache-2.0**. Tree: **288 files**, complete. Observation: `2026-10-12T06:29:29Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`scripts/evidence-bundle.sh` L2–4](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/scripts/evidence-bundle.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L138–140](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/.github/workflows/ci.yml#L138-L140); [`.github/workflows/dogfood.yml` L6–8](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/.github/workflows/dogfood.yml#L6-L8).
- **Release/changelog evidence:** 108 tags and 108 releases enumerated; 2 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L106–108](https://github.com/jeremylongshore/agent-governance-plane/blob/2076dec5264a194e28302fbb1ce26a5d0305a576/CHANGELOG.md#L106-L108); [release `v0.1.78`](https://github.com/jeremylongshore/agent-governance-plane/releases/tag/v0.1.78); [release `v0.1.54`](https://github.com/jeremylongshore/agent-governance-plane/releases/tag/v0.1.54).
- **Verification scope:** 10/10 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R012: agent-starter-pack

Repository: [jeremylongshore/agent-starter-pack](https://github.com/jeremylongshore/agent-starter-pack). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **502**; head: `37947c3351d2349ffb53f5e3e37d777df0aed6c9`. GitHub license metadata: **Apache-2.0**. Tree: **284 files**, complete. Observation: `2026-10-12T06:29:29Z`.

- **Trace:** [`agent_starter_pack/base_template/{{cookiecutter.agent_directory}}/app_utils/telemetry.py` L63–65](https://github.com/jeremylongshore/agent-starter-pack/blob/37947c3351d2349ffb53f5e3e37d777df0aed6c9/agent_starter_pack/base_template/%7B%7Bcookiecutter.agent_directory%7D%7D/app_utils/telemetry.py#L63-L65) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`agent_starter_pack/base_template/{{cookiecutter.agent_directory}}/app_utils/telemetry.py` L22–24](https://github.com/jeremylongshore/agent-starter-pack/blob/37947c3351d2349ffb53f5e3e37d777df0aed6c9/agent_starter_pack/base_template/%7B%7Bcookiecutter.agent_directory%7D%7D/app_utils/telemetry.py#L22-L24) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L24–26](https://github.com/jeremylongshore/agent-starter-pack/blob/37947c3351d2349ffb53f5e3e37d777df0aed6c9/README.md#L24-L26) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 45 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R013: agglayer-docs

Repository: [jeremylongshore/agglayer-docs](https://github.com/jeremylongshore/agglayer-docs). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **156**; head: `d09a4b908de016739b5978916da1255e19a2fee3`. GitHub license metadata: **MIT**. Tree: **205 files**, complete. Observation: `2026-10-12T06:29:32Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`docs/agglayer/core-concepts/pessimistic-proof/benchmarks.md` L2–4](https://github.com/jeremylongshore/agglayer-docs/blob/d09a4b908de016739b5978916da1255e19a2fee3/docs/agglayer/core-concepts/pessimistic-proof/benchmarks.md#L2-L4) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R014

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R015: ai-blog-journalist-n8n

Repository: [jeremylongshore/ai-blog-journalist-n8n](https://github.com/jeremylongshore/ai-blog-journalist-n8n). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **10**; head: `419f0aa7dc61a5fc50579c50449fcff7ac828334`. GitHub license metadata: **MIT**. Tree: **20 files**, complete. Observation: `2026-10-12T06:29:33Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R016: ai-card

Repository: [jeremylongshore/ai-card](https://github.com/jeremylongshore/ai-card). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **20**; head: `71ca831ec8ca035939094f8eaf62fcec4948320e`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **3 files**, complete. Observation: `2026-10-12T06:29:35Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R017: anthropic-sdk-typescript

Repository: [jeremylongshore/anthropic-sdk-typescript](https://github.com/jeremylongshore/anthropic-sdk-typescript). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **1014**; head: `84d3409bd3b8b50288eb25f2c1388e7b486d017e`. GitHub license metadata: **MIT**. Tree: **262 files**, complete. Observation: `2026-10-12T06:29:35Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`CHANGELOG.md` L109–111](https://github.com/jeremylongshore/anthropic-sdk-typescript/blob/84d3409bd3b8b50288eb25f2c1388e7b486d017e/CHANGELOG.md#L109-L111) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 4 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 229 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L109–111](https://github.com/jeremylongshore/anthropic-sdk-typescript/blob/84d3409bd3b8b50288eb25f2c1388e7b486d017e/CHANGELOG.md#L109-L111).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 4 workflow paths and 4 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R018: automate

Repository: [jeremylongshore/automate](https://github.com/jeremylongshore/automate). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **25**; head: `278f0b4b9518d101a236d70faf466fb5f828f759`. GitHub license metadata: **MIT**. Tree: **49 files**, complete. Observation: `2026-10-12T06:29:36Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L149–151](https://github.com/jeremylongshore/automate/blob/278f0b4b9518d101a236d70faf466fb5f828f759/README.md#L149-L151) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 4 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R019: awesome-agent-skills

Repository: [jeremylongshore/awesome-agent-skills](https://github.com/jeremylongshore/awesome-agent-skills). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **164**; head: `b40e90b33ef91591250b15e1d04ff99af7b0cf56`. GitHub license metadata: **MIT**. Tree: **4 files**, complete. Observation: `2026-10-12T06:29:37Z`.

- **Trace:** [`README.md` L388–390](https://github.com/jeremylongshore/awesome-agent-skills/blob/b40e90b33ef91591250b15e1d04ff99af7b0cf56/README.md#L388-L390) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`README.md` L273–275](https://github.com/jeremylongshore/awesome-agent-skills/blob/b40e90b33ef91591250b15e1d04ff99af7b0cf56/README.md#L273-L275) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L169–171](https://github.com/jeremylongshore/awesome-agent-skills/blob/b40e90b33ef91591250b15e1d04ff99af7b0cf56/README.md#L169-L171) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R020: awesome-claude-skills

Repository: [jeremylongshore/awesome-claude-skills](https://github.com/jeremylongshore/awesome-claude-skills). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **42**; head: `eb596888a17151464c26a80abe18197238da342c`. GitHub license metadata: **unclassified by GitHub**. Tree: **4 files**, complete. Observation: `2026-10-12T06:29:38Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L429–431](https://github.com/jeremylongshore/awesome-claude-skills/blob/eb596888a17151464c26a80abe18197238da342c/README.md#L429-L431) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R021: awesome-claude-skills-1

Repository: [jeremylongshore/awesome-claude-skills-1](https://github.com/jeremylongshore/awesome-claude-skills-1). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `master`; reachable commits: **54**; head: `970d1fa3db81fd72df39fa498f70eb1ace0128ae`. GitHub license metadata: **unclassified by GitHub**. Tree: **1247 files**, complete. Observation: `2026-10-12T06:29:38Z`.

- **Trace:** [`README.md` L121–123](https://github.com/jeremylongshore/awesome-claude-skills-1/blob/970d1fa3db81fd72df39fa498f70eb1ace0128ae/README.md#L121-L123) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`README.md` L121–123](https://github.com/jeremylongshore/awesome-claude-skills-1/blob/970d1fa3db81fd72df39fa498f70eb1ace0128ae/README.md#L121-L123) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`document-skills/pdf/scripts/fill_pdf_form_with_annotations.py` L5–7](https://github.com/jeremylongshore/awesome-claude-skills-1/blob/970d1fa3db81fd72df39fa498f70eb1ace0128ae/document-skills/pdf/scripts/fill_pdf_form_with_annotations.py#L5-L7) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`mcp-builder/scripts/evaluation.py` L1–3](https://github.com/jeremylongshore/awesome-claude-skills-1/blob/970d1fa3db81fd72df39fa498f70eb1ace0128ae/mcp-builder/scripts/evaluation.py#L1-L3) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`mcp-builder/reference/evaluation.md` L70–72](https://github.com/jeremylongshore/awesome-claude-skills-1/blob/970d1fa3db81fd72df39fa498f70eb1ace0128ae/mcp-builder/reference/evaluation.md#L70-L72) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R022: azure-landing-zone-starter

Repository: [jeremylongshore/azure-landing-zone-starter](https://github.com/jeremylongshore/azure-landing-zone-starter). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **19**; head: `0801dfbbe2e56f48f2f8252ce340bd270410356e`. GitHub license metadata: **MIT**. Tree: **46 files**, complete. Observation: `2026-10-12T06:29:39Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 8 tags and 7 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R023: beads

Repository: [jeremylongshore/beads](https://github.com/jeremylongshore/beads). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **8452**; head: `11e3aaa0609eccfbde24bd31254aae6532e6778a`. GitHub license metadata: **MIT**. Tree: **1544 files**, complete. Observation: `2026-10-12T06:29:40Z`.

- **Trace:** [`internal/telemetry/storage.go` L10–12](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/internal/telemetry/storage.go#L10-L12) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`internal/telemetry/otlp.go` L1–3](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/internal/telemetry/otlp.go#L1-L3) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`internal/storage/annotation_queries.go` L10–12](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/internal/storage/annotation_queries.go#L10-L12) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`internal/query/evaluator.go` L24–26](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/internal/query/evaluator.go#L24-L26) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/release.yml` L325–326](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/.github/workflows/release.yml#L325-L326) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/release.yml` L325–326](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/.github/workflows/release.yml#L325-L326).
- **Release/changelog evidence:** 63 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L14–16](https://github.com/jeremylongshore/beads/blob/11e3aaa0609eccfbde24bd31254aae6532e6778a/CHANGELOG.md#L14-L16).
- **Verification scope:** 25/25 Contents requests returned HTTP 200; 5 other filename candidates remain uninspected. All 9 workflow paths and 8 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R024

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R025: blur-extension

Repository: [jeremylongshore/blur-extension](https://github.com/jeremylongshore/blur-extension). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **20**; head: `04706fe6d46115b4d734a356600b168c897a3aba`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **61 files**, complete. Observation: `2026-10-12T06:29:41Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R026

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R027

Visibility: **public**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R028

Visibility: **public**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R029

Visibility: **public**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R030: box-cloud-filesystem

Repository: [jeremylongshore/box-cloud-filesystem](https://github.com/jeremylongshore/box-cloud-filesystem). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **14**; head: `e95343dc5b718f671b20064ff813af64ed0062d3`. GitHub license metadata: **MIT**. Tree: **27 files**, complete. Observation: `2026-10-12T06:29:44Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R031

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R032: cad-ai-agent

Repository: [jeremylongshore/cad-ai-agent](https://github.com/jeremylongshore/cad-ai-agent). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **345**; head: `3215dc0b0b706e5b280798e00bf8b512dbb9cfbc`. GitHub license metadata: **Apache-2.0**. Tree: **718 files**, complete. Observation: `2026-10-12T06:29:46Z`.

- **Trace:** [`src/cad_dxf_agent/otel.py` L1–3](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/src/cad_dxf_agent/otel.py#L1-L3) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`src/cad_dxf_agent/otel.py` L1–3](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/src/cad_dxf_agent/otel.py#L1-L3) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`src/cad_dxf_agent/otel.py` L8–10](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/src/cad_dxf_agent/otel.py#L8-L10) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`tests/eval/test_scorecard.py` L1–3](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/tests/eval/test_scorecard.py#L1-L3) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L111–113](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/.github/workflows/ci.yml#L111-L113).
- **Release/changelog evidence:** 14 tags and 14 releases enumerated; 5 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L44–46](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/CHANGELOG.md#L44-L46); [`src/cad_dxf_agent/core/comparison/changelog.py` L3–5](https://github.com/jeremylongshore/cad-ai-agent/blob/3215dc0b0b706e5b280798e00bf8b512dbb9cfbc/src/cad_dxf_agent/core/comparison/changelog.py#L3-L5); [release `v0.11.0`](https://github.com/jeremylongshore/cad-ai-agent/releases/tag/v0.11.0); [release `v0.7.0`](https://github.com/jeremylongshore/cad-ai-agent/releases/tag/v0.7.0); [release `v0.6.0`](https://github.com/jeremylongshore/cad-ai-agent/releases/tag/v0.6.0).
- **Verification scope:** 24/24 Contents requests returned HTTP 200; 32 other filename candidates remain uninspected. All 8 workflow paths and 5 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R033: cal.com

Repository: [jeremylongshore/cal.com](https://github.com/jeremylongshore/cal.com). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **15387**; head: `c12b2544d45c081eed33b244dc95fa8efa5f6852`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **9664 files**, complete. Observation: `2026-10-12T06:29:46Z`.

- **Trace:** [`packages/lib/tracing/index.ts` L8–10](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/packages/lib/tracing/index.ts#L8-L10) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`packages/lib/telemetry.ts` L7–9](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/packages/lib/telemetry.ts#L7-L9) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`.github/workflows/publish-report.yml` L96–98](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/.github/workflows/publish-report.yml#L96-L98) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** [`packages/lib/raqb/evaluateRaqbLogic.ts` L15–17](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/packages/lib/raqb/evaluateRaqbLogic.ts#L15-L17) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/companion-build.yml` L36–38](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/.github/workflows/companion-build.yml#L36-L38); [`.github/workflows/nextjs-bundle-analysis-annotation.yml` L1–3](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/.github/workflows/nextjs-bundle-analysis-annotation.yml#L1-L3); [`.github/workflows/publish-report.yml` L96–98](https://github.com/jeremylongshore/cal.com/blob/c12b2544d45c081eed33b244dc95fa8efa5f6852/.github/workflows/publish-report.yml#L96-L98).
- **Release/changelog evidence:** 600 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 71/71 Contents requests returned HTTP 200; 4 other filename candidates remain uninspected. All 52 workflow paths and 8 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R034: centaur

Repository: [jeremylongshore/centaur](https://github.com/jeremylongshore/centaur). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **231**; head: `def9276add3ab4e5be4ac8810a33f9e0a39fb1db`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **825 files**, complete. Observation: `2026-10-12T06:29:48Z`.

- **Trace:** [`services/api/api/otel.py` L10–12](https://github.com/jeremylongshore/centaur/blob/def9276add3ab4e5be4ac8810a33f9e0a39fb1db/services/api/api/otel.py#L10-L12) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`services/api/api/otel.py` L10–12](https://github.com/jeremylongshore/centaur/blob/def9276add3ab4e5be4ac8810a33f9e0a39fb1db/services/api/api/otel.py#L10-L12) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`services/api/api/otel.py` L1–3](https://github.com/jeremylongshore/centaur/blob/def9276add3ab4e5be4ac8810a33f9e0a39fb1db/services/api/api/otel.py#L1-L3) (source; lexical evidence, not an operational verdict).
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** [`.agents/skills/dogfood/references/issue-taxonomy.md` L1–3](https://github.com/jeremylongshore/centaur/blob/def9276add3ab4e5be4ac8810a33f9e0a39fb1db/.agents/skills/dogfood/references/issue-taxonomy.md#L1-L3) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 5 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 14/14 Contents requests returned HTTP 200; 2 other filename candidates remain uninspected. All 5 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R035

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R036: claude-code

Repository: [jeremylongshore/claude-code](https://github.com/jeremylongshore/claude-code). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **407**; head: `deb92edab617baf2ac21032e7ab4512a9d81fdad`. GitHub license metadata: **unclassified by GitHub**. Tree: **174 files**, complete. Observation: `2026-10-12T06:29:50Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`CHANGELOG.md` L386–388](https://github.com/jeremylongshore/claude-code/blob/deb92edab617baf2ac21032e7ab4512a9d81fdad/CHANGELOG.md#L386-L388) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`CHANGELOG.md` L247–249](https://github.com/jeremylongshore/claude-code/blob/deb92edab617baf2ac21032e7ab4512a9d81fdad/CHANGELOG.md#L247-L249) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/oncall-triage.yml` L49–51](https://github.com/jeremylongshore/claude-code/blob/deb92edab617baf2ac21032e7ab4512a9d81fdad/.github/workflows/oncall-triage.yml#L49-L51) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/oncall-triage.yml` L49–51](https://github.com/jeremylongshore/claude-code/blob/deb92edab617baf2ac21032e7ab4512a9d81fdad/.github/workflows/oncall-triage.yml#L49-L51).
- **Release/changelog evidence:** 2 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L245–247](https://github.com/jeremylongshore/claude-code/blob/deb92edab617baf2ac21032e7ab4512a9d81fdad/CHANGELOG.md#L245-L247).
- **Verification scope:** 13/13 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 11 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R037: claude-code-action

Repository: [jeremylongshore/claude-code-action](https://github.com/jeremylongshore/claude-code-action). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **402**; head: `804c252f483ebd0f1a1b5814b20a84c8dfd737bb`. GitHub license metadata: **MIT**. Tree: **173 files**, complete. Observation: `2026-10-12T06:29:51Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`README.md` L44–46](https://github.com/jeremylongshore/claude-code-action/blob/804c252f483ebd0f1a1b5814b20a84c8dfd737bb/README.md#L44-L46) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`README.md` L20–22](https://github.com/jeremylongshore/claude-code-action/blob/804c252f483ebd0f1a1b5814b20a84c8dfd737bb/README.md#L20-L22) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 11 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 94 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 12/12 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 11 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R038: claude-code-slack-channel

Repository: [jeremylongshore/claude-code-slack-channel](https://github.com/jeremylongshore/claude-code-slack-channel). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **366**; head: `5c7a04bafb26cf612402a3805faca62a509d656e`. GitHub license metadata: **Apache-2.0**. Tree: **191 files**, complete. Observation: `2026-10-12T06:29:52Z`.

- **Trace:** [`CHANGELOG.md` L159–161](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/CHANGELOG.md#L159-L161) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`CHANGELOG.md` L121–123](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/CHANGELOG.md#L121-L123) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 6 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 15 tags and 15 releases enumerated; 3 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L20–22](https://github.com/jeremylongshore/claude-code-slack-channel/blob/5c7a04bafb26cf612402a3805faca62a509d656e/CHANGELOG.md#L20-L22); [release `v0.10.0`](https://github.com/jeremylongshore/claude-code-slack-channel/releases/tag/v0.10.0); [release `v0.6.0`](https://github.com/jeremylongshore/claude-code-slack-channel/releases/tag/v0.6.0); [release `v0.5.0`](https://github.com/jeremylongshore/claude-code-slack-channel/releases/tag/v0.5.0).
- **Verification scope:** 11/11 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 6 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R039: claude-cookbooks

Repository: [jeremylongshore/claude-cookbooks](https://github.com/jeremylongshore/claude-cookbooks). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **474**; head: `cad7f50d79f2aa9748a703e66560ad47db62f6e6`. GitHub license metadata: **MIT**. Tree: **388 files**, complete. Observation: `2026-10-12T06:29:52Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`claude_agent_sdk/observability_agent/agent.py` L2–4](https://github.com/jeremylongshore/claude-cookbooks/blob/cad7f50d79f2aa9748a703e66560ad47db62f6e6/claude_agent_sdk/observability_agent/agent.py#L2-L4) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L60–62](https://github.com/jeremylongshore/claude-cookbooks/blob/cad7f50d79f2aa9748a703e66560ad47db62f6e6/README.md#L60-L62) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 9 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 16/16 Contents requests returned HTTP 200; 33 other filename candidates remain uninspected. All 9 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R040: claude-plugins-official

Repository: [jeremylongshore/claude-plugins-official](https://github.com/jeremylongshore/claude-plugins-official). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **55**; head: `7d1ab19d0e0db537387d2c6c47ebb1285b856137`. GitHub license metadata: **unclassified by GitHub**. Tree: **212 files**, complete. Observation: `2026-10-12T06:29:53Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R041: claude-quickstarts

Repository: [jeremylongshore/claude-quickstarts](https://github.com/jeremylongshore/claude-quickstarts). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **83**; head: `b6a9395a190599961930e99284cf5126c63e9039`. GitHub license metadata: **MIT**. Tree: **223 files**, complete. Observation: `2026-10-12T06:29:54Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`browser-use-demo/CHANGELOG.md` L32–33](https://github.com/jeremylongshore/claude-quickstarts/blob/b6a9395a190599961930e99284cf5126c63e9039/browser-use-demo/CHANGELOG.md#L32-L33) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`browser-use-demo/CHANGELOG.md` L32–33](https://github.com/jeremylongshore/claude-quickstarts/blob/b6a9395a190599961930e99284cf5126c63e9039/browser-use-demo/CHANGELOG.md#L32-L33).
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R042: claude-skills-collection

Repository: [jeremylongshore/claude-skills-collection](https://github.com/jeremylongshore/claude-skills-collection). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **11**; head: `c7c2a0ec030a3db9696056185a8e951f4e4b110d`. GitHub license metadata: **unclassified by GitHub**. Tree: **2 files**, complete. Observation: `2026-10-12T06:29:54Z`.

- **Trace:** [`README.md` L102–104](https://github.com/jeremylongshore/claude-skills-collection/blob/c7c2a0ec030a3db9696056185a8e951f4e4b110d/README.md#L102-L104) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L174–176](https://github.com/jeremylongshore/claude-skills-collection/blob/c7c2a0ec030a3db9696056185a8e951f4e4b110d/README.md#L174-L176) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R043

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R044

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R045: comehomealabama

Repository: [jeremylongshore/comehomealabama](https://github.com/jeremylongshore/comehomealabama). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **55**; head: `ab74dfabfeaf66b857178485482f28e4f983aa76`. GitHub license metadata: **MIT**. Tree: **86 files**, complete. Observation: `2026-10-12T06:29:56Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R046: contributing-clanker

Repository: [jeremylongshore/contributing-clanker](https://github.com/jeremylongshore/contributing-clanker). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **183**; head: `3c4212cd0e6ab96a5571bc3030bc4e9407f0e495`. GitHub license metadata: **MIT**. Tree: **287 files**, complete. Observation: `2026-10-12T06:29:57Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`skills/contribute/scripts/gates/c23-mcp-tool-annotations-spec.sh` L2–4](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/skills/contribute/scripts/gates/c23-mcp-tool-annotations-spec.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 5 tags and 5 releases enumerated; 3 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L14–16](https://github.com/jeremylongshore/contributing-clanker/blob/3c4212cd0e6ab96a5571bc3030bc4e9407f0e495/CHANGELOG.md#L14-L16); [release `v0.3.0`](https://github.com/jeremylongshore/contributing-clanker/releases/tag/v0.3.0); [release `v0.2.0`](https://github.com/jeremylongshore/contributing-clanker/releases/tag/v0.2.0); [release `v0.1.0`](https://github.com/jeremylongshore/contributing-clanker/releases/tag/v0.1.0).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R047: cortex

Repository: [jeremylongshore/cortex](https://github.com/jeremylongshore/cortex). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **316**; head: `c5667328c97c1ca320ebc205208947f42d96e907`. GitHub license metadata: **Apache-2.0**. Tree: **234 files**, complete. Observation: `2026-10-12T06:29:58Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`CHANGELOG.md` L90–92](https://github.com/jeremylongshore/cortex/blob/c5667328c97c1ca320ebc205208947f42d96e907/CHANGELOG.md#L90-L92) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 6 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L90–92](https://github.com/jeremylongshore/cortex/blob/c5667328c97c1ca320ebc205208947f42d96e907/CHANGELOG.md#L90-L92).
- **Verification scope:** 8/8 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 6 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R048: cost-plus-db

Repository: [jeremylongshore/cost-plus-db](https://github.com/jeremylongshore/cost-plus-db). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **177**; head: `8a30fc22f1c1dbac47820a2f7db71e976c80b36e`. GitHub license metadata: **MIT**. Tree: **353 files**, complete. Observation: `2026-10-12T06:29:58Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`testing/benchmarks/run-multitenant-benchmark.sh` L2–4](https://github.com/jeremylongshore/cost-plus-db/blob/8a30fc22f1c1dbac47820a2f7db71e976c80b36e/testing/benchmarks/run-multitenant-benchmark.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 4 tags and 2 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L28–30](https://github.com/jeremylongshore/cost-plus-db/blob/8a30fc22f1c1dbac47820a2f7db71e976c80b36e/CHANGELOG.md#L28-L30).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 23 other filename candidates remain uninspected. All 0 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R049

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R050: daily-energizer-workflow-n8n

Repository: [jeremylongshore/daily-energizer-workflow-n8n](https://github.com/jeremylongshore/daily-energizer-workflow-n8n). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **34**; head: `772d13eec68db1fc95d6b3702648f9f5dad7f8e0`. GitHub license metadata: **unclassified by GitHub**. Tree: **35 files**, complete. Observation: `2026-10-12T06:30:00Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L15–17](https://github.com/jeremylongshore/daily-energizer-workflow-n8n/blob/772d13eec68db1fc95d6b3702648f9f5dad7f8e0/README.md#L15-L17) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R051: database-skills

Repository: [jeremylongshore/database-skills](https://github.com/jeremylongshore/database-skills). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **7**; head: `d5ba9b16cbebcf8750246d1a2f5a33623794ddaf`. GitHub license metadata: **MIT**. Tree: **61 files**, complete. Observation: `2026-10-12T06:30:01Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R052: dental-billing-mcp-demo

Repository: [jeremylongshore/dental-billing-mcp-demo](https://github.com/jeremylongshore/dental-billing-mcp-demo). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **3**; head: `657cb4712340ab6c046b8401f566c1b4182df1ec`. GitHub license metadata: **unclassified by GitHub**. Tree: **3 files**, complete. Observation: `2026-10-12T06:30:03Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 0/0 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R053: derivatives-signal-agent

Repository: [jeremylongshore/derivatives-signal-agent](https://github.com/jeremylongshore/derivatives-signal-agent). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **6**; head: `c98d69d9a468eb6af8ec454567adb8925a04fc9b`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **41 files**, complete. Observation: `2026-10-12T06:30:04Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`CHANGELOG.md` L13–15](https://github.com/jeremylongshore/derivatives-signal-agent/blob/c98d69d9a468eb6af8ec454567adb8925a04fc9b/CHANGELOG.md#L13-L15) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L13–15](https://github.com/jeremylongshore/derivatives-signal-agent/blob/c98d69d9a468eb6af8ec454567adb8925a04fc9b/CHANGELOG.md#L13-L15).
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R054

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R055

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R056: diagnosticpro-schema-sql

Repository: [jeremylongshore/diagnosticpro-schema-sql](https://github.com/jeremylongshore/diagnosticpro-schema-sql). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **13**; head: `3cf2693c71c8d0885ca3a764cd33cbbbb98602db`. GitHub license metadata: **MIT**. Tree: **132 files**, complete. Observation: `2026-10-12T06:30:07Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 2 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R057: disposable-marketplace-n8n

Repository: [jeremylongshore/disposable-marketplace-n8n](https://github.com/jeremylongshore/disposable-marketplace-n8n). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `master`; reachable commits: **13**; head: `cbd789c9cf5244dc34ef94cf8ab1e21bb0ba7a87`. GitHub license metadata: **MIT**. Tree: **33 files**, complete. Observation: `2026-10-12T06:30:07Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`tests/performance/benchmark.js` L2–4](https://github.com/jeremylongshore/disposable-marketplace-n8n/blob/cbd789c9cf5244dc34ef94cf8ab1e21bb0ba7a87/tests/performance/benchmark.js#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/test.yml` L165–167](https://github.com/jeremylongshore/disposable-marketplace-n8n/blob/cbd789c9cf5244dc34ef94cf8ab1e21bb0ba7a87/.github/workflows/test.yml#L165-L167).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 1 release records have lexical matches. [release `v1.0.0`](https://github.com/jeremylongshore/disposable-marketplace-n8n/releases/tag/v1.0.0).
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R058: dolt-mcp-vcs-plugin

Repository: [jeremylongshore/dolt-mcp-vcs-plugin](https://github.com/jeremylongshore/dolt-mcp-vcs-plugin). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **18**; head: `8a61fba16f362ebb277ef8bccb999d4834fb7d63`. GitHub license metadata: **Apache-2.0**. Tree: **46 files**, complete. Observation: `2026-10-12T06:30:09Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L169–171](https://github.com/jeremylongshore/dolt-mcp-vcs-plugin/blob/8a61fba16f362ebb277ef8bccb999d4834fb7d63/README.md#L169-L171) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L50–52](https://github.com/jeremylongshore/dolt-mcp-vcs-plugin/blob/8a61fba16f362ebb277ef8bccb999d4834fb7d63/README.md#L50-L52) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** [`CHANGELOG.md` L35–37](https://github.com/jeremylongshore/dolt-mcp-vcs-plugin/blob/8a61fba16f362ebb277ef8bccb999d4834fb7d63/CHANGELOG.md#L35-L37) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L33–35](https://github.com/jeremylongshore/dolt-mcp-vcs-plugin/blob/8a61fba16f362ebb277ef8bccb999d4834fb7d63/CHANGELOG.md#L33-L35).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R059: editor

Repository: [jeremylongshore/editor](https://github.com/jeremylongshore/editor). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **490**; head: `f25806ee8f10b3778a38c8b5cc917c7fa9edb3c5`. GitHub license metadata: **MIT**. Tree: **723 files**, complete. Observation: `2026-10-12T06:30:09Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 8 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R060: excel-analyst-pro-skill-md

Repository: [jeremylongshore/excel-analyst-pro-skill-md](https://github.com/jeremylongshore/excel-analyst-pro-skill-md). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **19**; head: `62ab55ece132a1c1b91ce64e86fa4e0f4ad4947d`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **35 files**, complete. Observation: `2026-10-12T06:30:10Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`CHANGELOG.md` L48–50](https://github.com/jeremylongshore/excel-analyst-pro-skill-md/blob/62ab55ece132a1c1b91ce64e86fa4e0f4ad4947d/CHANGELOG.md#L48-L50) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L3–5](https://github.com/jeremylongshore/excel-analyst-pro-skill-md/blob/62ab55ece132a1c1b91ce64e86fa4e0f4ad4947d/README.md#L3-L5) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 2 tags and 2 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L25–27](https://github.com/jeremylongshore/excel-analyst-pro-skill-md/blob/62ab55ece132a1c1b91ce64e86fa4e0f4ad4947d/CHANGELOG.md#L25-L27); [release `v1.1.0`](https://github.com/jeremylongshore/excel-analyst-pro-skill-md/releases/tag/v1.1.0).
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R061: executive-assistant-skills

Repository: [jeremylongshore/executive-assistant-skills](https://github.com/jeremylongshore/executive-assistant-skills). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **17**; head: `49a6f28a617b4bd38ff6f85e61e3ad0e850304e9`. GitHub license metadata: **unclassified by GitHub**. Tree: **13 files**, complete. Observation: `2026-10-12T06:30:11Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R062: executive-intent

Repository: [jeremylongshore/executive-intent](https://github.com/jeremylongshore/executive-intent). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **37**; head: `985479cd909763f43945833033b3c0849e64a3bc`. GitHub license metadata: **unclassified by GitHub**. Tree: **159 files**, complete. Observation: `2026-10-12T06:30:11Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`src/lib/evidence/types.ts` L164–166](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/src/lib/evidence/types.ts#L164-L166) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`src/app/evidence/page.tsx` L17–19](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/src/app/evidence/page.tsx#L17-L19) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`src/lib/evidence/types.ts` L4–6](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/src/lib/evidence/types.ts#L4-L6) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/deploy-dev.yml` L66–68](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/.github/workflows/deploy-dev.yml#L66-L68); [`.github/workflows/deploy-prod.yml` L66–68](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/.github/workflows/deploy-prod.yml#L66-L68); [`.github/workflows/deploy.yml` L94–96](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/.github/workflows/deploy.yml#L94-L96).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/executive-intent/blob/985479cd909763f43945833033b3c0849e64a3bc/.audit-harness/CHANGELOG.md#L23-L25).
- **Verification scope:** 10/10 Contents requests returned HTTP 200; 12 other filename candidates remain uninspected. All 5 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R063: feishin

Repository: [jeremylongshore/feishin](https://github.com/jeremylongshore/feishin). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `development`; reachable commits: **3153**; head: `cb749480a4866c8f3ae5466539bde4a3b86b7061`. GitHub license metadata: **GPL-3.0**. Tree: **1021 files**, complete. Observation: `2026-10-12T06:30:12Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 12 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 58 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 15/15 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 12 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R064: field-of-greens

Repository: [jeremylongshore/field-of-greens](https://github.com/jeremylongshore/field-of-greens). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `master`; reachable commits: **7**; head: `0524c12ac23d1f12cc2183482a45a20021b69c80`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **44 files**, complete. Observation: `2026-10-12T06:30:13Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R065: filament

Repository: [jeremylongshore/filament](https://github.com/jeremylongshore/filament). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `4.x`; reachable commits: **28902**; head: `c2e564e80c91f036c3ff2e2fbf68690a1c59a7dc`. GitHub license metadata: **MIT**. Tree: **6429 files**, complete. Observation: `2026-10-12T06:30:14Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 11 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1211 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 13/13 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 11 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R066: firebase-gen2-buildpack-failure

Repository: [jeremylongshore/firebase-gen2-buildpack-failure](https://github.com/jeremylongshore/firebase-gen2-buildpack-failure). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **1**; head: `fbfeb14ac59671b1f9a115e8f3d1cd7aed1fabc2`. GitHub license metadata: **MIT**. Tree: **6 files**, complete. Observation: `2026-10-12T06:30:14Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** [`README.md` L22–24](https://github.com/jeremylongshore/firebase-gen2-buildpack-failure/blob/fbfeb14ac59671b1f9a115e8f3d1cd7aed1fabc2/README.md#L22-L24) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R067

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R068: frontend-slides

Repository: [jeremylongshore/frontend-slides](https://github.com/jeremylongshore/frontend-slides). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **14**; head: `f12faf93da6b5bca775efa877b7fc71f49355664`. GitHub license metadata: **MIT**. Tree: **9 files**, complete. Observation: `2026-10-12T06:30:17Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R069: gastown

Repository: [jeremylongshore/gastown](https://github.com/jeremylongshore/gastown). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **5715**; head: `4623be8f84667ec6a50cf446a7ba4bd3eb05fc78`. GitHub license metadata: **MIT**. Tree: **1190 files**, complete. Observation: `2026-10-12T06:30:18Z`.

- **Trace:** [`CHANGELOG.md` L123–125](https://github.com/jeremylongshore/gastown/blob/4623be8f84667ec6a50cf446a7ba4bd3eb05fc78/CHANGELOG.md#L123-L125) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`internal/cmd/telemetry.go` L16–18](https://github.com/jeremylongshore/gastown/blob/4623be8f84667ec6a50cf446a7ba4bd3eb05fc78/internal/cmd/telemetry.go#L16-L18) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`gt-model-eval/scripts/results-to-discussion.sh` L2–4](https://github.com/jeremylongshore/gastown/blob/4623be8f84667ec6a50cf446a7ba4bd3eb05fc78/gt-model-eval/scripts/results-to-discussion.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`gt-model-eval/README.md` L7–9](https://github.com/jeremylongshore/gastown/blob/4623be8f84667ec6a50cf446a7ba4bd3eb05fc78/gt-model-eval/README.md#L7-L9) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 10 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 17 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L120–122](https://github.com/jeremylongshore/gastown/blob/4623be8f84667ec6a50cf446a7ba4bd3eb05fc78/CHANGELOG.md#L120-L122).
- **Verification scope:** 18/18 Contents requests returned HTTP 200; 23 other filename candidates remain uninspected. All 10 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R070: gastown-series

Repository: [jeremylongshore/gastown-series](https://github.com/jeremylongshore/gastown-series). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **11**; head: `7206115a67f3cfc910cece1b5a75a1fbe19e604d`. GitHub license metadata: **MIT**. Tree: **55 files**, complete. Observation: `2026-10-12T06:30:19Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R071: gastown-viewer-intent

Repository: [jeremylongshore/gastown-viewer-intent](https://github.com/jeremylongshore/gastown-viewer-intent). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **64**; head: `402c2d573a47e0b044a9c2b5251eec854258264d`. GitHub license metadata: **MIT**. Tree: **104 files**, complete. Observation: `2026-10-12T06:30:20Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 9 tags and 9 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R072: gmail-drive-organizer-n8n

Repository: [jeremylongshore/gmail-drive-organizer-n8n](https://github.com/jeremylongshore/gmail-drive-organizer-n8n). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **10**; head: `8dd72e54c8bf3f4f3d586ce03738f3bf9520e3f4`. GitHub license metadata: **MIT**. Tree: **20 files**, complete. Observation: `2026-10-12T06:30:21Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R073: guidewire-mcp-for-claude

Repository: [jeremylongshore/guidewire-mcp-for-claude](https://github.com/jeremylongshore/guidewire-mcp-for-claude). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **129**; head: `4ea87cb940f3258c6e57c6caf69b90c6941cc911`. GitHub license metadata: **Apache-2.0**. Tree: **291 files**, complete. Observation: `2026-10-12T06:30:21Z`.

- **Trace:** [`packages/observability/src/error.ts` L16–18](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/packages/observability/src/error.ts#L16-L18) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`packages/harness/tests/evidence.test.ts` L2–4](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/packages/harness/tests/evidence.test.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`.github/workflows/dependabot-automerge.yml` L5–7](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/.github/workflows/dependabot-automerge.yml#L5-L7) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** [`packages/harness/src/evidence/exporter.ts` L179–181](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/packages/harness/src/evidence/exporter.ts#L179-L181) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`packages/harness/tests/evidence.test.ts` L4–6](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/packages/harness/tests/evidence.test.ts#L4-L6) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/cloud-api-contract.yml` L42–44](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/.github/workflows/cloud-api-contract.yml#L42-L44); [`.github/workflows/dependabot-automerge.yml` L5–7](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/.github/workflows/dependabot-automerge.yml#L5-L7).
- **Release/changelog evidence:** 3 tags and 3 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L40–42](https://github.com/jeremylongshore/guidewire-mcp-for-claude/blob/4ea87cb940f3258c6e57c6caf69b90c6941cc911/CHANGELOG.md#L40-L42); [release `v0.1.0`](https://github.com/jeremylongshore/guidewire-mcp-for-claude/releases/tag/v0.1.0).
- **Verification scope:** 16/16 Contents requests returned HTTP 200; 8 other filename candidates remain uninspected. All 8 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R074: hustle

Repository: [jeremylongshore/hustle](https://github.com/jeremylongshore/hustle). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **513**; head: `0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **1102 files**, complete. Observation: `2026-10-12T06:30:22Z`.

- **Trace:** [`.github/workflows/synthetic-qa.yml` L169–171](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/.github/workflows/synthetic-qa.yml#L169-L171) (workflow; lexical evidence, not an operational verdict).
- **Telemetry:** [`.github/workflows/deploy.yml` L40–42](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/.github/workflows/deploy.yml#L40-L42) (workflow; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`CHANGELOG.md` L999–1001](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/CHANGELOG.md#L999-L1001) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`CHANGELOG.md` L751–753](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/CHANGELOG.md#L751-L753) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** [`CHANGELOG.md` L543–545](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/CHANGELOG.md#L543-L545) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/deploy.yml` L40–42](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/.github/workflows/deploy.yml#L40-L42); [`.github/workflows/synthetic-qa.yml` L169–171](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/.github/workflows/synthetic-qa.yml#L169-L171).
- **Release/changelog evidence:** 26 tags and 26 releases enumerated; 3 release records have lexical matches. [`CHANGELOG.md` L318–320](https://github.com/jeremylongshore/hustle/blob/0fe52bffd99c3e7b0bc4e5b74b6f96bf9cb135d3/CHANGELOG.md#L318-L320); [release `v2.0.0`](https://github.com/jeremylongshore/hustle/releases/tag/untagged-efd39037c108a50bb645); [release `v2.0.0`](https://github.com/jeremylongshore/hustle/releases/tag/v2.0.0); [release `v1.0.0`](https://github.com/jeremylongshore/hustle/releases/tag/v1.0.0).
- **Verification scope:** 11/11 Contents requests returned HTTP 200; 1 other filename candidates remain uninspected. All 6 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R075

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R076: iam-bob-adk-python

Repository: [jeremylongshore/iam-bob-adk-python](https://github.com/jeremylongshore/iam-bob-adk-python). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **382**; head: `e3ab610ba825a54cc4c41fff5d314e53dece3817`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **3160 files**, complete. Observation: `2026-10-12T06:30:24Z`.

- **Trace:** [`archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/tracing.js` L19–21](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/tracing.js#L19-L21) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/tracing.js` L33–35](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/tracing.js#L33-L35) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/tracing.js` L43–45](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/tracing.js#L43-L45) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/evaluator.js` L19–21](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/archive/2025-11-11-final-cleanup/2025-11-10-genkit-agent/node_modules/genkit/lib/evaluator.js#L19-L21) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`agents/shared_contracts/evidence_bundle.py` L2–4](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/agents/shared_contracts/evidence_bundle.py#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`CHANGELOG.md` L201–203](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/CHANGELOG.md#L201-L203) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/agent-engine-inline-deploy.yml` L107–109](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/.github/workflows/agent-engine-inline-deploy.yml#L107-L109); [`.github/workflows/ci.yml` L212–214](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/.github/workflows/ci.yml#L212-L214); [`.github/workflows/deploy-dev.yml` L136–138](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/.github/workflows/deploy-dev.yml#L136-L138); [`.github/workflows/deploy-prod.yml` L113–115](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/.github/workflows/deploy-prod.yml#L113-L115).
- **Release/changelog evidence:** 49 tags and 37 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L201–203](https://github.com/jeremylongshore/iam-bob-adk-python/blob/e3ab610ba825a54cc4c41fff5d314e53dece3817/CHANGELOG.md#L201-L203); [release `v2.0.0`](https://github.com/jeremylongshore/iam-bob-adk-python/releases/tag/v2.0.0).
- **Verification scope:** 31/31 Contents requests returned HTTP 200; 109 other filename candidates remain uninspected. All 17 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R077: iam-bob-intendant

Repository: [jeremylongshore/iam-bob-intendant](https://github.com/jeremylongshore/iam-bob-intendant). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **27**; head: `afa7f568d9f228fce6d801a822b663861492922c`. GitHub license metadata: **Apache-2.0**. Tree: **102 files**, complete. Observation: `2026-10-12T06:30:25Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/iam-bob-intendant/blob/afa7f568d9f228fce6d801a822b663861492922c/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/iam-bob-intendant/blob/afa7f568d9f228fce6d801a822b663861492922c/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/iam-bob-intendant/blob/afa7f568d9f228fce6d801a822b663861492922c/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/iam-bob-intendant/blob/afa7f568d9f228fce6d801a822b663861492922c/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 12 tags and 12 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/iam-bob-intendant/blob/afa7f568d9f228fce6d801a822b663861492922c/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L61–63](https://github.com/jeremylongshore/iam-bob-intendant/blob/afa7f568d9f228fce6d801a822b663861492922c/CHANGELOG.md#L61-L63).
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R078: iam-bob-langgraph

Repository: [jeremylongshore/iam-bob-langgraph](https://github.com/jeremylongshore/iam-bob-langgraph). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **9**; head: `14606d29ed0ac683f7ebcd656b62c504ff7ca512`. GitHub license metadata: **unclassified by GitHub**. Tree: **13 files**, complete. Observation: `2026-10-12T06:30:25Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** [`README.md` L9–11](https://github.com/jeremylongshore/iam-bob-langgraph/blob/14606d29ed0ac683f7ebcd656b62c504ff7ca512/README.md#L9-L11) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R079: iam-bob-pydantic

Repository: [jeremylongshore/iam-bob-pydantic](https://github.com/jeremylongshore/iam-bob-pydantic). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **9**; head: `b33db225dbba4ebe3ab64da23d6c0e9765c267cf`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **41 files**, complete. Observation: `2026-10-12T06:30:27Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/ci.yml` L31–33](https://github.com/jeremylongshore/iam-bob-pydantic/blob/b33db225dbba4ebe3ab64da23d6c0e9765c267cf/.github/workflows/ci.yml#L31-L33) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L23–25](https://github.com/jeremylongshore/iam-bob-pydantic/blob/b33db225dbba4ebe3ab64da23d6c0e9765c267cf/README.md#L23-L25) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/ci.yml` L31–33](https://github.com/jeremylongshore/iam-bob-pydantic/blob/b33db225dbba4ebe3ab64da23d6c0e9765c267cf/.github/workflows/ci.yml#L31-L33).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R080: iam-git-with-intent

Repository: [jeremylongshore/iam-git-with-intent](https://github.com/jeremylongshore/iam-git-with-intent). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **431**; head: `0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **1205 files**, complete. Observation: `2026-10-12T06:30:27Z`.

- **Trace:** [`scripts/arv/observability-gate.ts` L10–12](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/scripts/arv/observability-gate.ts#L10-L12) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`scripts/arv/observability-gate.ts` L3–5](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/scripts/arv/observability-gate.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`apps/cli/src/commands/eval.ts` L2–4](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/apps/cli/src/commands/eval.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`packages/core/src/evidence/index.ts` L2–4](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/packages/core/src/evidence/index.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/auto-fix.yml` L331–333](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/.github/workflows/auto-fix.yml#L331-L333); [`.github/workflows/deploy-agents.yml` L170–172](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/.github/workflows/deploy-agents.yml#L170-L172); [`.github/workflows/golden-tasks.yml` L2–4](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/.github/workflows/golden-tasks.yml#L2-L4).
- **Release/changelog evidence:** 11 tags and 11 releases enumerated; 4 release records have lexical matches. [`CHANGELOG.md` L12–14](https://github.com/jeremylongshore/iam-git-with-intent/blob/0e1bcf2f68f10a7da5e71d22fbe32421a52dfdd5/CHANGELOG.md#L12-L14); [release `v0.10.0`](https://github.com/jeremylongshore/iam-git-with-intent/releases/tag/v0.10.0); [release `v0.8.0`](https://github.com/jeremylongshore/iam-git-with-intent/releases/tag/v0.8.0); [release `v0.7.0`](https://github.com/jeremylongshore/iam-git-with-intent/releases/tag/v0.7.0).
- **Verification scope:** 33/33 Contents requests returned HTTP 200; 55 other filename candidates remain uninspected. All 18 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R081: iam-local-rag

Repository: [jeremylongshore/iam-local-rag](https://github.com/jeremylongshore/iam-local-rag). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **83**; head: `b8c9468250f2d3dde198af7e58c576c6287ed42d`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **115 files**, complete. Observation: `2026-10-12T06:30:27Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`nexus/evals/run.py` L7–9](https://github.com/jeremylongshore/iam-local-rag/blob/b8c9468250f2d3dde198af7e58c576c6287ed42d/nexus/evals/run.py#L7-L9) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`nexus/evals/run.py` L2–4](https://github.com/jeremylongshore/iam-local-rag/blob/b8c9468250f2d3dde198af7e58c576c6287ed42d/nexus/evals/run.py#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`03-Tests/test_evals.py` L57–59](https://github.com/jeremylongshore/iam-local-rag/blob/b8c9468250f2d3dde198af7e58c576c6287ed42d/03-Tests/test_evals.py#L57-L59) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 19 tags and 18 releases enumerated; 2 release records have lexical matches. [`CHANGELOG.md` L110–112](https://github.com/jeremylongshore/iam-local-rag/blob/b8c9468250f2d3dde198af7e58c576c6287ed42d/CHANGELOG.md#L110-L112); [release `v1.1.5`](https://github.com/jeremylongshore/iam-local-rag/releases/tag/v1.1.5); [release `v1.1.4`](https://github.com/jeremylongshore/iam-local-rag/releases/tag/v1.1.4).
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 13 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R082: intent-agent-model-jvp-base

Repository: [jeremylongshore/intent-agent-model-jvp-base](https://github.com/jeremylongshore/intent-agent-model-jvp-base). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `master`; reachable commits: **16**; head: `137c4854b14933f566d51e86881e94bb1b2f13b1`. GitHub license metadata: **Apache-2.0**. Tree: **84 files**, complete. Observation: `2026-10-12T06:30:29Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`README.md` L248–250](https://github.com/jeremylongshore/intent-agent-model-jvp-base/blob/137c4854b14933f566d51e86881e94bb1b2f13b1/README.md#L248-L250) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R083: intent-audit-harness

Repository: [jeremylongshore/intent-audit-harness](https://github.com/jeremylongshore/intent-audit-harness). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **159**; head: `735134f3a0bf8a644c5078b70a8b8d87031e2f86`. GitHub license metadata: **Apache-2.0**. Tree: **269 files**, complete. Observation: `2026-10-12T06:30:29Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`scripts/emit-evidence.sh` L302–304](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/scripts/emit-evidence.sh#L302-L304) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`.github/workflows/ci.yml` L214–216](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/.github/workflows/ci.yml#L214-L216) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** [`ci/emit-evidence.ts` L4–6](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/ci/emit-evidence.ts#L4-L6) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`ci/emit-evidence.ts` L3–5](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/ci/emit-evidence.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`scripts/emit-evidence.sh` L303–305](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/scripts/emit-evidence.sh#L303-L305) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L17–19](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/.github/workflows/ci.yml#L17-L19); [`.github/workflows/claim-precheck.yml` L17–19](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/.github/workflows/claim-precheck.yml#L17-L19); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/release.yml` L3–5](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/.github/workflows/release.yml#L3-L5); [`.github/workflows/rollout-gate-dogfood.yml` L4–6](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/.github/workflows/rollout-gate-dogfood.yml#L4-L6).
- **Release/changelog evidence:** 21 tags and 14 releases enumerated; 10 release records have lexical matches. [`CHANGELOG.md` L38–40](https://github.com/jeremylongshore/intent-audit-harness/blob/735134f3a0bf8a644c5078b70a8b8d87031e2f86/CHANGELOG.md#L38-L40); [release `v1.5.0`](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.5.0); [release `v1.3.1`](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.3.1); [release `v1.3.0`](https://github.com/jeremylongshore/intent-audit-harness/releases/tag/v1.3.0).
- **Verification scope:** 18/18 Contents requests returned HTTP 200; 4 other filename candidates remain uninspected. All 9 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R084

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R085: intent-blueprint-docs

Repository: [jeremylongshore/intent-blueprint-docs](https://github.com/jeremylongshore/intent-blueprint-docs). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **127**; head: `1c5913bb18be8a908b08018f28978b486308024e`. GitHub license metadata: **Apache-2.0**. Tree: **401 files**, complete. Observation: `2026-10-12T06:30:31Z`.

- **Trace:** [`CHANGELOG.md` L15–17](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/CHANGELOG.md#L15-L17) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L178–180](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/.audit-harness/scripts/emit-evidence.sh#L178-L180) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`CHANGELOG.md` L15–17](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/CHANGELOG.md#L15-L17) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`test/doc-quality-eval.test.ts` L5–7](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/test/doc-quality-eval.test.ts#L5-L7) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`test/release-evidence.test.ts` L9–11](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/test/release-evidence.test.ts#L9-L11) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/CHANGELOG.md` L164–166](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/.audit-harness/CHANGELOG.md#L164-L166) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/release.yml` L10–12](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/.github/workflows/release.yml#L10-L12).
- **Release/changelog evidence:** 20 tags and 14 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L9–11](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/.audit-harness/CHANGELOG.md#L9-L11); [`CHANGELOG.md` L15–17](https://github.com/jeremylongshore/intent-blueprint-docs/blob/1c5913bb18be8a908b08018f28978b486308024e/CHANGELOG.md#L15-L17).
- **Verification scope:** 17/17 Contents requests returned HTTP 200; 7 other filename candidates remain uninspected. All 8 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R086: intent-eval-core

Repository: [jeremylongshore/intent-eval-core](https://github.com/jeremylongshore/intent-eval-core). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **115**; head: `863f60eb3f2579090066dd1790597f9ecb2e8e75`. GitHub license metadata: **Apache-2.0**. Tree: **735 files**, complete. Observation: `2026-10-12T06:30:32Z`.

- **Trace:** [`src/otel/v1/attributes.ts` L41–43](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/src/otel/v1/attributes.ts#L41-L43) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`src/otel/v1/index.ts` L2–4](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/src/otel/v1/index.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`src/validators/v1/eval-spec.ts` L37–39](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/src/validators/v1/eval-spec.ts#L37-L39) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`scripts/emit-evidence.ts` L5–7](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/scripts/emit-evidence.ts#L5-L7) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`scripts/emit-evidence.ts` L3–5](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/scripts/emit-evidence.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`src/entities/FailureTaxonomy.ts` L2–4](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/src/entities/FailureTaxonomy.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/changelog-observance.yml` L3–5](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/changelog-observance.yml#L3-L5); [`.github/workflows/ci.yml` L52–54](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/ci.yml#L52-L54); [`.github/workflows/claim-precheck.yml` L17–19](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/claim-precheck.yml#L17-L19); [`.github/workflows/coverage-map-gates.yml` L12–14](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/coverage-map-gates.yml#L12-L14); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/release.yml` L3–5](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/release.yml#L3-L5); [`.github/workflows/typos.yml` L5–7](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/typos.yml#L5-L7).
- **Release/changelog evidence:** 14 tags and 13 releases enumerated; 13 release records have lexical matches. [`.github/workflows/changelog-observance.yml` L3–5](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/.github/workflows/changelog-observance.yml#L3-L5); [`CHANGELOG.md` L40–42](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/CHANGELOG.md#L40-L42); [`schemas/authoring/v1/CHANGELOG.md` L6–8](https://github.com/jeremylongshore/intent-eval-core/blob/863f60eb3f2579090066dd1790597f9ecb2e8e75/schemas/authoring/v1/CHANGELOG.md#L6-L8); [release `v0.11.0`](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.11.0); [release `v0.10.0`](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.10.0); [release `v0.9.0`](https://github.com/jeremylongshore/intent-eval-core/releases/tag/v0.9.0).
- **Verification scope:** 36/36 Contents requests returned HTTP 200; 40 other filename candidates remain uninspected. All 13 workflow paths and 5 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R087: intent-eval-dashboard

Repository: [jeremylongshore/intent-eval-dashboard](https://github.com/jeremylongshore/intent-eval-dashboard). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **258**; head: `4bd2d35dc3477b4427b1996c5d92da66c29673f6`. GitHub license metadata: **Apache-2.0**. Tree: **1676 files**, complete. Observation: `2026-10-12T06:30:32Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`README.md` L39–41](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/README.md#L39-L41) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`src/alerting/evaluate.ts` L2–4](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/src/alerting/evaluate.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`src/ingest/rekor-anchor.ts` L2–4](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/src/ingest/rekor-anchor.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`src/ingest/verifier-sigstore.ts` L56–58](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/src/ingest/verifier-sigstore.ts#L56-L58) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/deploy.yml` L4–6](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/.github/workflows/deploy.yml#L4-L6); [`.github/workflows/ingest-ci.yml` L7–9](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/.github/workflows/ingest-ci.yml#L7-L9); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/partner-name-guard.yml` L6–8](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/.github/workflows/partner-name-guard.yml#L6-L8); [`.github/workflows/regenerate.yml` L1–3](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/.github/workflows/regenerate.yml#L1-L3); [`.github/workflows/typos.yml` L6–8](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/.github/workflows/typos.yml#L6-L8).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L3–5](https://github.com/jeremylongshore/intent-eval-dashboard/blob/4bd2d35dc3477b4427b1996c5d92da66c29673f6/CHANGELOG.md#L3-L5).
- **Verification scope:** 17/17 Contents requests returned HTTP 200; 10 other filename candidates remain uninspected. All 9 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R088: intent-eval-lab

Repository: [jeremylongshore/intent-eval-lab](https://github.com/jeremylongshore/intent-eval-lab). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **264**; head: `04cdc4530a26d0bf24626717f2b10e0aceced831`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **2600 files**, complete. Observation: `2026-10-12T06:30:33Z`.

- **Trace:** [`README.md` L26–28](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/README.md#L26-L28) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`scripts/drift-eval-runner.py` L34–36](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/scripts/drift-eval-runner.py#L34-L36) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`ci/emit-evidence.ts` L3–5](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/ci/emit-evidence.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`ci/emit-evidence.ts` L3–5](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/ci/emit-evidence.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L73–75](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/ci.yml#L73-L75); [`.github/workflows/claim-precheck-reusable.yml` L7–9](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/claim-precheck-reusable.yml#L7-L9); [`.github/workflows/codeql.yml` L10–12](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/codeql.yml#L10-L12); [`.github/workflows/e2e-integration.yml` L4–6](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/e2e-integration.yml#L4-L6); [`.github/workflows/harness-hash-verify.yml` L11–13](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/harness-hash-verify.yml#L11-L13); [`.github/workflows/leading-indicator-watch.yml` L152–154](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/leading-indicator-watch.yml#L152-L154); [`.github/workflows/lint.yml` L3–5](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/lint.yml#L3-L5); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/public-surface-scrub.yml` L22–24](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/public-surface-scrub.yml#L22-L24); [`.github/workflows/release.yml` L3–5](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/release.yml#L3-L5); [`.github/workflows/schema-drift.yml` L5–7](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/schema-drift.yml#L5-L7); [`.github/workflows/sign-dogfood-bundle.yml` L3–5](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/sign-dogfood-bundle.yml#L3-L5); [`.github/workflows/sign-evidence-bundle.yml` L1–3](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/sign-evidence-bundle.yml#L1-L3); [`.github/workflows/spec-drift-watch.yml` L5–7](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/spec-drift-watch.yml#L5-L7); [`.github/workflows/typos.yml` L3–5](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.github/workflows/typos.yml#L3-L5).
- **Release/changelog evidence:** 3 tags and 3 releases enumerated; 3 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L10–12](https://github.com/jeremylongshore/intent-eval-lab/blob/04cdc4530a26d0bf24626717f2b10e0aceced831/CHANGELOG.md#L10-L12); [release `v0.3.0`](https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.3.0); [release `v0.2.0`](https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.2.0); [release `v0.1.0`](https://github.com/jeremylongshore/intent-eval-lab/releases/tag/v0.1.0).
- **Verification scope:** 37/37 Contents requests returned HTTP 200; 54 other filename candidates remain uninspected. All 20 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R089: intent-longbox

Repository: [jeremylongshore/intent-longbox](https://github.com/jeremylongshore/intent-longbox). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **165**; head: `d7b8de8053f77791900ab6dfe0f61b44890dd6ea`. GitHub license metadata: **Apache-2.0**. Tree: **483 files**, complete. Observation: `2026-10-12T06:30:34Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`.github/workflows/minimax-review.yml` L93–95](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/.github/workflows/minimax-review.yml#L93-L95) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/minimax-review.yml` L145–147](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/.github/workflows/minimax-review.yml#L145-L147) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/ci.yml` L202–204](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/.github/workflows/ci.yml#L202-L204) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** [`000-docs/018-AT-DECR-longbox-evidence-rules-2026-09-03.md` L1–3](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/000-docs/018-AT-DECR-longbox-evidence-rules-2026-09-03.md#L1-L3) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L202–204](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/.github/workflows/ci.yml#L202-L204); [`.github/workflows/minimax-review.yml` L91–93](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/.github/workflows/minimax-review.yml#L91-L93).
- **Release/changelog evidence:** 22 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L40–42](https://github.com/jeremylongshore/intent-longbox/blob/d7b8de8053f77791900ab6dfe0f61b44890dd6ea/CHANGELOG.md#L40-L42).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 1 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R090

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R091: intent-mail

Repository: [jeremylongshore/intent-mail](https://github.com/jeremylongshore/intent-mail). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **259**; head: `7f1104576422b9cecc0466195fcb12d7ffec5537`. GitHub license metadata: **Apache-2.0**. Tree: **356 files**, complete. Observation: `2026-10-12T06:30:35Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/release.yml` L14–16](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/.github/workflows/release.yml#L14-L16).
- **Release/changelog evidence:** 4 tags and 4 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L45–47](https://github.com/jeremylongshore/intent-mail/blob/7f1104576422b9cecc0466195fcb12d7ffec5537/CHANGELOG.md#L45-L47).
- **Verification scope:** 8/8 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 4 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R092: intent-outreach

Repository: [jeremylongshore/intent-outreach](https://github.com/jeremylongshore/intent-outreach). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **152**; head: `6380ec709f001da8862a6ac066a8cebc9b1ad644`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **390 files**, complete. Observation: `2026-10-12T06:30:36Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`evals/run.ts` L2–4](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/evals/run.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`evals/run.ts` L830–832](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/evals/run.ts#L830-L832) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L48–50](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/.github/workflows/ci.yml#L48-L50).
- **Release/changelog evidence:** 3 tags and 2 releases enumerated; 2 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L17–19](https://github.com/jeremylongshore/intent-outreach/blob/6380ec709f001da8862a6ac066a8cebc9b1ad644/CHANGELOG.md#L17-L19); [release `v0.3.0`](https://github.com/jeremylongshore/intent-outreach/releases/tag/v0.3.0); [release `v0.2.0`](https://github.com/jeremylongshore/intent-outreach/releases/tag/v0.2.0).
- **Verification scope:** 11/11 Contents requests returned HTTP 200; 64 other filename candidates remain uninspected. All 4 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R093: intent-rollout-gate

Repository: [jeremylongshore/intent-rollout-gate](https://github.com/jeremylongshore/intent-rollout-gate). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **72**; head: `b10d955073c99a936ec11b8a1b1b5b295da2e7f8`. GitHub license metadata: **Apache-2.0**. Tree: **110 files**, complete. Observation: `2026-10-12T06:30:37Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L19–21](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/README.md#L19-L21) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`.github/workflows/release-gate-self-test.yml` L102–104](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/release-gate-self-test.yml#L102-L104) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** [`ci/emit-evidence.ts` L4–6](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/ci/emit-evidence.ts#L4-L6) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`ci/emit-evidence.ts` L3–5](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/ci/emit-evidence.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`README.md` L3–5](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/README.md#L3-L5) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L128–130](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/ci.yml#L128-L130); [`.github/workflows/claim-precheck.yml` L17–19](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/claim-precheck.yml#L17-L19); [`.github/workflows/dogfood.yml` L4–6](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/dogfood.yml#L4-L6); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/release-gate-self-test.yml` L11–13](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/release-gate-self-test.yml#L11-L13); [`.github/workflows/release-gate.yml` L18–20](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/release-gate.yml#L18-L20); [`.github/workflows/release.yml` L5–7](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/.github/workflows/release.yml#L5-L7).
- **Release/changelog evidence:** 7 tags and 6 releases enumerated; 4 release records have lexical matches. [`CHANGELOG.md` L13–15](https://github.com/jeremylongshore/intent-rollout-gate/blob/b10d955073c99a936ec11b8a1b1b5b295da2e7f8/CHANGELOG.md#L13-L15); [release `v0.3.2`](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.3.2); [release `v0.3.1`](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.3.1); [release `v0.2.0`](https://github.com/jeremylongshore/intent-rollout-gate/releases/tag/v0.2.0).
- **Verification scope:** 16/16 Contents requests returned HTTP 200; 9 other filename candidates remain uninspected. All 11 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R094: intent-scout

Repository: [jeremylongshore/intent-scout](https://github.com/jeremylongshore/intent-scout). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **35**; head: `9d45f1227100e617e04f33a6d668a36ba4ba1991`. GitHub license metadata: **MIT**. Tree: **119 files**, complete. Observation: `2026-10-12T06:30:37Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/intent-scout/blob/9d45f1227100e617e04f33a6d668a36ba4ba1991/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/intent-scout/blob/9d45f1227100e617e04f33a6d668a36ba4ba1991/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/intent-scout/blob/9d45f1227100e617e04f33a6d668a36ba4ba1991/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/intent-scout/blob/9d45f1227100e617e04f33a6d668a36ba4ba1991/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/intent-scout/blob/9d45f1227100e617e04f33a6d668a36ba4ba1991/.audit-harness/CHANGELOG.md#L23-L25).
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R095: intent-solutions-landing

Repository: [jeremylongshore/intent-solutions-landing](https://github.com/jeremylongshore/intent-solutions-landing). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **340**; head: `4883cff31f542f6309e4da428d3f9df0851e30f9`. GitHub license metadata: **MIT**. Tree: **535 files**, complete. Observation: `2026-10-12T06:30:38Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 4 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 37 tags and 37 releases enumerated; 1 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L433–435](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/CHANGELOG.md#L433-L435); [`estate-bar/CHANGELOG.md` L5–7](https://github.com/jeremylongshore/intent-solutions-landing/blob/4883cff31f542f6309e4da428d3f9df0851e30f9/estate-bar/CHANGELOG.md#L5-L7); [release `v3.0.0`](https://github.com/jeremylongshore/intent-solutions-landing/releases/tag/v3.0.0).
- **Verification scope:** 13/13 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 4 workflow paths and 4 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R096: intent-vision

Repository: [jeremylongshore/intent-vision](https://github.com/jeremylongshore/intent-vision). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **31**; head: `82d9a534669112d6cac59fdf3433984b43609498`. GitHub license metadata: **unclassified by GitHub**. Tree: **436 files**, complete. Observation: `2026-10-12T06:30:39Z`.

- **Trace:** [`000-docs/049-DR-ADRC-production-deployment-observability.md` L335–337](https://github.com/jeremylongshore/intent-vision/blob/82d9a534669112d6cac59fdf3433984b43609498/000-docs/049-DR-ADRC-production-deployment-observability.md#L335-L337) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`packages/api/src/observability/metrics.ts` L6–8](https://github.com/jeremylongshore/intent-vision/blob/82d9a534669112d6cac59fdf3433984b43609498/packages/api/src/observability/metrics.ts#L6-L8) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`000-docs/049-DR-ADRC-production-deployment-observability.md` L114–116](https://github.com/jeremylongshore/intent-vision/blob/82d9a534669112d6cac59fdf3433984b43609498/000-docs/049-DR-ADRC-production-deployment-observability.md#L114-L116) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`packages/pipeline/src/eval/index.ts` L2–4](https://github.com/jeremylongshore/intent-vision/blob/82d9a534669112d6cac59fdf3433984b43609498/packages/pipeline/src/eval/index.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L12–14](https://github.com/jeremylongshore/intent-vision/blob/82d9a534669112d6cac59fdf3433984b43609498/CHANGELOG.md#L12-L14).
- **Verification scope:** 11/11 Contents requests returned HTTP 200; 1 other filename candidates remain uninspected. All 2 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R097: intentsolutions-vps-runbook

Repository: [jeremylongshore/intentsolutions-vps-runbook](https://github.com/jeremylongshore/intentsolutions-vps-runbook). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **1**; head: `8739c086e4277ea4a9843ba0f3ad8cf43f3b9801`. GitHub license metadata: **unclassified by GitHub**. Tree: **2 files**, complete. Observation: `2026-10-12T06:30:39Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L23–25](https://github.com/jeremylongshore/intentsolutions-vps-runbook/blob/8739c086e4277ea4a9843ba0f3ad8cf43f3b9801/README.md#L23-L25) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** [`README.md` L33–35](https://github.com/jeremylongshore/intentsolutions-vps-runbook/blob/8739c086e4277ea4a9843ba0f3ad8cf43f3b9801/README.md#L33-L35) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R098

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R099: intentsolutionskills

Repository: [jeremylongshore/intentsolutionskills](https://github.com/jeremylongshore/intentsolutionskills). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **8**; head: `a68c528c586674f2299a41dd683a975b8a040736`. GitHub license metadata: **MIT**. Tree: **16 files**, complete. Observation: `2026-10-12T06:30:41Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L3–5](https://github.com/jeremylongshore/intentsolutionskills/blob/a68c528c586674f2299a41dd683a975b8a040736/README.md#L3-L5) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R100: irsb

Repository: [jeremylongshore/irsb](https://github.com/jeremylongshore/irsb). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **51**; head: `920e9382b0bebe8bdafa18d0661b5ca2ef84afd3`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **908 files**, complete. Observation: `2026-10-12T06:30:41Z`.

- **Trace:** [`services/solver/000-docs/025-PR-ADDM-phase-6-observability.md` L96–98](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/services/solver/000-docs/025-PR-ADDM-phase-6-observability.md#L96-L98) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`services/solver/CHANGELOG.md` L66–68](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/services/solver/CHANGELOG.md#L66-L68) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L284–286](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/README.md#L284-L286) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`services/solver/src/evidence/index.ts` L2–4](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/services/solver/src/evidence/index.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 5 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 25 tags and 1 releases enumerated; 0 release records have lexical matches. [`archive/agent-passkey/CHANGELOG.md` L45–47](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/archive/agent-passkey/CHANGELOG.md#L45-L47); [`protocol/CHANGELOG.md` L213–215](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/protocol/CHANGELOG.md#L213-L215); [`protocol/dashboard/CHANGELOG.md` L110–112](https://github.com/jeremylongshore/irsb/blob/920e9382b0bebe8bdafa18d0661b5ca2ef84afd3/protocol/dashboard/CHANGELOG.md#L110-L112).
- **Verification scope:** 21/21 Contents requests returned HTTP 200; 16 other filename candidates remain uninspected. All 5 workflow paths and 8 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R101: j-rig-skill-binary-eval

Repository: [jeremylongshore/j-rig-skill-binary-eval](https://github.com/jeremylongshore/j-rig-skill-binary-eval). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **342**; head: `b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4`. GitHub license metadata: **Apache-2.0**. Tree: **627 files**, complete. Observation: `2026-10-12T06:30:42Z`.

- **Trace:** [`packages/cli/src/commands/eval.ts` L475–477](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/packages/cli/src/commands/eval.ts#L475-L477) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`scripts/otel-smoke.sh` L2–4](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/scripts/otel-smoke.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`packages/refiner-core/src/eval-set.ts` L21–23](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/packages/refiner-core/src/eval-set.ts#L21-L23) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`scripts/otel-smoke.sh` L4–6](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/scripts/otel-smoke.sh#L4-L6) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`scripts/emit-evidence.ts` L3–5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/scripts/emit-evidence.ts#L3-L5) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`scripts/otel-smoke.sh` L5–7](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/scripts/otel-smoke.sh#L5-L7) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/ci.yml` L40–42](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/ci.yml#L40-L42); [`.github/workflows/claim-precheck.yml` L17–19](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/claim-precheck.yml#L17-L19); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/nightly-skill-evals.yml` L1–3](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/nightly-skill-evals.yml#L1-L3); [`.github/workflows/publish-jrig-cli.yml` L3–5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/publish-jrig-cli.yml#L3-L5); [`.github/workflows/publish-pr-comment.yml` L3–5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/publish-pr-comment.yml#L3-L5); [`.github/workflows/publish-refiner.yml` L3–5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/publish-refiner.yml#L3-L5); [`.github/workflows/publish-rollout-gate.yml` L3–5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/publish-rollout-gate.yml#L3-L5); [`.github/workflows/release.yml` L3–5](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.github/workflows/release.yml#L3-L5).
- **Release/changelog evidence:** 63 tags and 48 releases enumerated; 48 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L25–27](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/b75364db5f21b874ca1f7fa12ce76c01e3c9a7b4/CHANGELOG.md#L25-L27); [release `v0.2.7`](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/untagged-21462d732cf3814aaa9d); [release `jrig-cli-v0.5.0`](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/jrig-cli-v0.5.0); [release `evidence-latest`](https://github.com/jeremylongshore/j-rig-skill-binary-eval/releases/tag/evidence-latest); tag `evidence-latest` at `98d705dc6582a54b80cee813df555e232a05621b`.
- **Verification scope:** 28/28 Contents requests returned HTTP 200; 113 other filename candidates remain uninspected. All 13 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R102: jeremylongshore

Repository: [jeremylongshore/jeremylongshore](https://github.com/jeremylongshore/jeremylongshore). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **46**; head: `56a4f32b80bc74a174656c525867bf2bd92deb04`. GitHub license metadata: **unclassified by GitHub**. Tree: **23 files**, complete. Observation: `2026-10-12T06:30:43Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L44–46](https://github.com/jeremylongshore/jeremylongshore/blob/56a4f32b80bc74a174656c525867bf2bd92deb04/README.md#L44-L46) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L44–46](https://github.com/jeremylongshore/jeremylongshore/blob/56a4f32b80bc74a174656c525867bf2bd92deb04/README.md#L44-L46) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R103: jeremylongshore.com

Repository: [jeremylongshore/jeremylongshore.com](https://github.com/jeremylongshore/jeremylongshore.com). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **484**; head: `ac9fbce7c253d50ff41e2185f457b8356d31def8`. GitHub license metadata: **MIT**. Tree: **865 files**, complete. Observation: `2026-10-12T06:30:43Z`.

- **Trace:** [`vendor/bundle/ruby/3.2.0/gems/bundler-2.6.6/CHANGELOG.md` L1315–1317](https://github.com/jeremylongshore/jeremylongshore.com/blob/ac9fbce7c253d50ff41e2185f457b8356d31def8/vendor/bundle/ruby/3.2.0/gems/bundler-2.6.6/CHANGELOG.md#L1315-L1317) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`vendor/bundle/ruby/3.2.0/gems/bundler-2.6.6/CHANGELOG.md` L890–892](https://github.com/jeremylongshore/jeremylongshore.com/blob/ac9fbce7c253d50ff41e2185f457b8356d31def8/vendor/bundle/ruby/3.2.0/gems/bundler-2.6.6/CHANGELOG.md#L890-L892) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`vendor/bundle/ruby/3.2.0/gems/liquid-5.5.1/History.md` L30–32](https://github.com/jeremylongshore/jeremylongshore.com/blob/ac9fbce7c253d50ff41e2185f457b8356d31def8/vendor/bundle/ruby/3.2.0/gems/liquid-5.5.1/History.md#L30-L32) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 95 tags and 95 releases enumerated; 0 release records have lexical matches. [`vendor/bundle/ruby/3.2.0/gems/bundler-2.6.6/CHANGELOG.md` L228–230](https://github.com/jeremylongshore/jeremylongshore.com/blob/ac9fbce7c253d50ff41e2185f457b8356d31def8/vendor/bundle/ruby/3.2.0/gems/bundler-2.6.6/CHANGELOG.md#L228-L230); [`vendor/bundle/ruby/3.2.0/gems/liquid-5.5.1/History.md` L30–32](https://github.com/jeremylongshore/jeremylongshore.com/blob/ac9fbce7c253d50ff41e2185f457b8356d31def8/vendor/bundle/ruby/3.2.0/gems/liquid-5.5.1/History.md#L30-L32); [`vendor/bundle/ruby/3.2.0/gems/nokogiri-1.18.5-x86_64-linux-gnu/gumbo-parser/CHANGES.md` L39–41](https://github.com/jeremylongshore/jeremylongshore.com/blob/ac9fbce7c253d50ff41e2185f457b8356d31def8/vendor/bundle/ruby/3.2.0/gems/nokogiri-1.18.5-x86_64-linux-gnu/gumbo-parser/CHANGES.md#L39-L41).
- **Verification scope:** 11/11 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 7 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R104: kilocode

Repository: [jeremylongshore/kilocode](https://github.com/jeremylongshore/kilocode). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **31685**; head: `1c8fba5ab928fb653c0fd59c36c899f1e4c35c15`. GitHub license metadata: **Apache-2.0**. Tree: **5431 files**, complete. Observation: `2026-10-12T06:30:45Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.github/workflows/code-qa.yml` L109–111](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/.github/workflows/code-qa.yml#L109-L111) (workflow; lexical evidence, not an operational verdict).
- **Annotation:** [`CHANGELOG.md` L1660–1662](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/CHANGELOG.md#L1660-L1662) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/evals.yml` L1–3](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/.github/workflows/evals.yml#L1-L3) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/auto-triage.yml` L44–46](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/.github/workflows/auto-triage.yml#L44-L46); [`.github/workflows/code-qa.yml` L109–111](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/.github/workflows/code-qa.yml#L109-L111); [`.github/workflows/evals.yml` L1–3](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/.github/workflows/evals.yml#L1-L3).
- **Release/changelog evidence:** 301 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L457–459](https://github.com/jeremylongshore/kilocode/blob/1c8fba5ab928fb653c0fd59c36c899f1e4c35c15/CHANGELOG.md#L457-L459).
- **Verification scope:** 60/60 Contents requests returned HTTP 200; 171 other filename candidates remain uninspected. All 12 workflow paths and 42 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R105: knowledge-work-plugins

Repository: [jeremylongshore/knowledge-work-plugins](https://github.com/jeremylongshore/knowledge-work-plugins). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **5**; head: `7d17c7bd9b9e6613f5e976de877bcbe3b31309af`. GitHub license metadata: **Apache-2.0**. Tree: **239 files**, complete. Observation: `2026-10-12T06:30:45Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R106

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R107: lead-followup-system-n8n

Repository: [jeremylongshore/lead-followup-system-n8n](https://github.com/jeremylongshore/lead-followup-system-n8n). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **10**; head: `1aeb1d91c051eb7b46ed7a6929f5b31227a6fa8d`. GitHub license metadata: **MIT**. Tree: **20 files**, complete. Observation: `2026-10-12T06:30:47Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L20–22](https://github.com/jeremylongshore/lead-followup-system-n8n/blob/1aeb1d91c051eb7b46ed7a6929f5b31227a6fa8d/README.md#L20-L22) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R108: learn-intentsolutions

Repository: [jeremylongshore/learn-intentsolutions](https://github.com/jeremylongshore/learn-intentsolutions). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **14**; head: `b599ad88b8489aabbde403f70c0e64b0969485e8`. GitHub license metadata: **MIT**. Tree: **30 files**, complete. Observation: `2026-10-12T06:30:48Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R109: lilly-75-holy

Repository: [jeremylongshore/lilly-75-holy](https://github.com/jeremylongshore/lilly-75-holy). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **20**; head: `2791d83c15c1f594bab0dec5dc4c08fa2900a514`. GitHub license metadata: **MIT**. Tree: **83 files**, complete. Observation: `2026-10-12T06:30:49Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 3 tags and 3 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R110: minimax-code-review

Repository: [jeremylongshore/minimax-code-review](https://github.com/jeremylongshore/minimax-code-review). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **49**; head: `58867f12dd52362fefda74f4d3c48541f1784e2f`. GitHub license metadata: **MIT**. Tree: **12 files**, complete. Observation: `2026-10-12T06:30:50Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 6 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R111: mnemos

Repository: [jeremylongshore/mnemos](https://github.com/jeremylongshore/mnemos). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **65**; head: `906976eced02935e1db12dcfe5a8ca0c8579862a`. GitHub license metadata: **MIT**. Tree: **205 files**, complete. Observation: `2026-10-12T06:30:50Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 15 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R112: moat

Repository: [jeremylongshore/moat](https://github.com/jeremylongshore/moat). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **46**; head: `ea9acdbae56dfc10e58f264a597adf01225653ef`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **188 files**, complete. Observation: `2026-10-12T06:30:51Z`.

- **Trace:** [`CHANGELOG.md` L49–51](https://github.com/jeremylongshore/moat/blob/ea9acdbae56dfc10e58f264a597adf01225653ef/CHANGELOG.md#L49-L51) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`services/trust-plane/app/scoring.py` L18–20](https://github.com/jeremylongshore/moat/blob/ea9acdbae56dfc10e58f264a597adf01225653ef/services/trust-plane/app/scoring.py#L18-L20) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`services/trust-plane/app/scoring.py` L2–4](https://github.com/jeremylongshore/moat/blob/ea9acdbae56dfc10e58f264a597adf01225653ef/services/trust-plane/app/scoring.py#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/ci.yml` L209–211](https://github.com/jeremylongshore/moat/blob/ea9acdbae56dfc10e58f264a597adf01225653ef/.github/workflows/ci.yml#L209-L211).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L49–51](https://github.com/jeremylongshore/moat/blob/ea9acdbae56dfc10e58f264a597adf01225653ef/CHANGELOG.md#L49-L51).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R113: myshell-handrolled-in-c

Repository: [jeremylongshore/myshell-handrolled-in-c](https://github.com/jeremylongshore/myshell-handrolled-in-c). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **3**; head: `9902bbaaa20d1e5138a3ecf005e983df0eeb55e3`. GitHub license metadata: **unclassified by GitHub**. Tree: **4 files**, complete. Observation: `2026-10-12T06:30:52Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 0/0 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R114: n8n-workflow-template

Repository: [jeremylongshore/n8n-workflow-template](https://github.com/jeremylongshore/n8n-workflow-template). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **7**; head: `dab8294facbe742cdb73bab82e2a139953818ec8`. GitHub license metadata: **MIT**. Tree: **21 files**, complete. Observation: `2026-10-12T06:30:53Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R115: navigating-github

Repository: [jeremylongshore/navigating-github](https://github.com/jeremylongshore/navigating-github). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **15**; head: `3d88871fa9e8d15610e8b26998751a26bc4d5523`. GitHub license metadata: **MIT**. Tree: **18 files**, complete. Observation: `2026-10-12T06:30:53Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R116: news-pipeline-n8n

Repository: [jeremylongshore/news-pipeline-n8n](https://github.com/jeremylongshore/news-pipeline-n8n). Visibility: **public**. Fork: **no**. Archived: **yes**.

Observed default branch: `main`; reachable commits: **9**; head: `12448444d530d5ac85cfc096f2edbf7b8c75c470`. GitHub license metadata: **MIT**. Tree: **14 files**, complete. Observation: `2026-10-12T06:30:54Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L23–25](https://github.com/jeremylongshore/news-pipeline-n8n/blob/12448444d530d5ac85cfc096f2edbf7b8c75c470/README.md#L23-L25) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 3 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L88–90](https://github.com/jeremylongshore/news-pipeline-n8n/blob/12448444d530d5ac85cfc096f2edbf7b8c75c470/CHANGELOG.md#L88-L90).
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R117: omarchy-bazaar-entry

Repository: [jeremylongshore/omarchy-bazaar-entry](https://github.com/jeremylongshore/omarchy-bazaar-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **22**; head: `016326846d001a96a1bdf5578ecb0d470b95b9f3`. GitHub license metadata: **MIT**. Tree: **80 files**, complete. Observation: `2026-10-12T06:30:55Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-bazaar-entry/blob/016326846d001a96a1bdf5578ecb0d470b95b9f3/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-bazaar-entry/blob/016326846d001a96a1bdf5578ecb0d470b95b9f3/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-bazaar-entry/blob/016326846d001a96a1bdf5578ecb0d470b95b9f3/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 2 tags and 2 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R118: omarchy-capture-conveyor-entry

Repository: [jeremylongshore/omarchy-capture-conveyor-entry](https://github.com/jeremylongshore/omarchy-capture-conveyor-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **34**; head: `11f1230b31251626f248f82144fd1f35754098ad`. GitHub license metadata: **MIT**. Tree: **76 files**, complete. Observation: `2026-10-12T06:30:55Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`CHANGELOG.md` L31–33](https://github.com/jeremylongshore/omarchy-capture-conveyor-entry/blob/11f1230b31251626f248f82144fd1f35754098ad/CHANGELOG.md#L31-L33) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-capture-conveyor-entry/blob/11f1230b31251626f248f82144fd1f35754098ad/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-capture-conveyor-entry/blob/11f1230b31251626f248f82144fd1f35754098ad/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-capture-conveyor-entry/blob/11f1230b31251626f248f82144fd1f35754098ad/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L31–33](https://github.com/jeremylongshore/omarchy-capture-conveyor-entry/blob/11f1230b31251626f248f82144fd1f35754098ad/CHANGELOG.md#L31-L33).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R119: omarchy-crew-chief-entry

Repository: [jeremylongshore/omarchy-crew-chief-entry](https://github.com/jeremylongshore/omarchy-crew-chief-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **33**; head: `c677cfd29e389ddbd742fd640a2b0f25b1eb40d5`. GitHub license metadata: **MIT**. Tree: **81 files**, complete. Observation: `2026-10-12T06:30:56Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L98–100](https://github.com/jeremylongshore/omarchy-crew-chief-entry/blob/c677cfd29e389ddbd742fd640a2b0f25b1eb40d5/README.md#L98-L100) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-crew-chief-entry/blob/c677cfd29e389ddbd742fd640a2b0f25b1eb40d5/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-crew-chief-entry/blob/c677cfd29e389ddbd742fd640a2b0f25b1eb40d5/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-crew-chief-entry/blob/c677cfd29e389ddbd742fd640a2b0f25b1eb40d5/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R120: omarchy-desk-transition-entry

Repository: [jeremylongshore/omarchy-desk-transition-entry](https://github.com/jeremylongshore/omarchy-desk-transition-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **36**; head: `a9e1688ae421df833e98ed9803f8cbf32e5719a6`. GitHub license metadata: **MIT**. Tree: **74 files**, complete. Observation: `2026-10-12T06:30:57Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-desk-transition-entry/blob/a9e1688ae421df833e98ed9803f8cbf32e5719a6/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-desk-transition-entry/blob/a9e1688ae421df833e98ed9803f8cbf32e5719a6/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-desk-transition-entry/blob/a9e1688ae421df833e98ed9803f8cbf32e5719a6/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R121: omarchy-docket-entry

Repository: [jeremylongshore/omarchy-docket-entry](https://github.com/jeremylongshore/omarchy-docket-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **32**; head: `14f11da8883c60615f6a58102cdb8340f75f60f2`. GitHub license metadata: **MIT**. Tree: **85 files**, complete. Observation: `2026-10-12T06:30:57Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-docket-entry/blob/14f11da8883c60615f6a58102cdb8340f75f60f2/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-docket-entry/blob/14f11da8883c60615f6a58102cdb8340f75f60f2/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-docket-entry/blob/14f11da8883c60615f6a58102cdb8340f75f60f2/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L24–26](https://github.com/jeremylongshore/omarchy-docket-entry/blob/14f11da8883c60615f6a58102cdb8340f75f60f2/CHANGELOG.md#L24-L26).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R122: omarchy-flow-boundary-entry

Repository: [jeremylongshore/omarchy-flow-boundary-entry](https://github.com/jeremylongshore/omarchy-flow-boundary-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **40**; head: `07eade2718ee2444682f0357a200e5de89ca80fb`. GitHub license metadata: **MIT**. Tree: **69 files**, complete. Observation: `2026-10-12T06:30:58Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L16–18](https://github.com/jeremylongshore/omarchy-flow-boundary-entry/blob/07eade2718ee2444682f0357a200e5de89ca80fb/README.md#L16-L18) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-flow-boundary-entry/blob/07eade2718ee2444682f0357a200e5de89ca80fb/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-flow-boundary-entry/blob/07eade2718ee2444682f0357a200e5de89ca80fb/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-flow-boundary-entry/blob/07eade2718ee2444682f0357a200e5de89ca80fb/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R123: omarchy-foundry-entry

Repository: [jeremylongshore/omarchy-foundry-entry](https://github.com/jeremylongshore/omarchy-foundry-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **29**; head: `3149654e685015246d919104c06fd468fc3731f4`. GitHub license metadata: **MIT**. Tree: **70 files**, complete. Observation: `2026-10-12T06:30:59Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L23–25](https://github.com/jeremylongshore/omarchy-foundry-entry/blob/3149654e685015246d919104c06fd468fc3731f4/README.md#L23-L25) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-foundry-entry/blob/3149654e685015246d919104c06fd468fc3731f4/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-foundry-entry/blob/3149654e685015246d919104c06fd468fc3731f4/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-foundry-entry/blob/3149654e685015246d919104c06fd468fc3731f4/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R124: omarchy-listening-post-entry

Repository: [jeremylongshore/omarchy-listening-post-entry](https://github.com/jeremylongshore/omarchy-listening-post-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **44**; head: `02da2d08799d476debed507676d3ea5902005bee`. GitHub license metadata: **MIT**. Tree: **212 files**, complete. Observation: `2026-10-12T06:30:59Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L198–200](https://github.com/jeremylongshore/omarchy-listening-post-entry/blob/02da2d08799d476debed507676d3ea5902005bee/README.md#L198-L200) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-listening-post-entry/blob/02da2d08799d476debed507676d3ea5902005bee/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-listening-post-entry/blob/02da2d08799d476debed507676d3ea5902005bee/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-listening-post-entry/blob/02da2d08799d476debed507676d3ea5902005bee/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 2 tags and 2 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 5 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R125: omarchy-loose-ends-entry

Repository: [jeremylongshore/omarchy-loose-ends-entry](https://github.com/jeremylongshore/omarchy-loose-ends-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **24**; head: `ffead99ed58d0f1acf52e95c064e897d081575a6`. GitHub license metadata: **MIT**. Tree: **78 files**, complete. Observation: `2026-10-12T06:31:00Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-loose-ends-entry/blob/ffead99ed58d0f1acf52e95c064e897d081575a6/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-loose-ends-entry/blob/ffead99ed58d0f1acf52e95c064e897d081575a6/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-loose-ends-entry/blob/ffead99ed58d0f1acf52e95c064e897d081575a6/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R126: omarchy-mlb-booth-entry

Repository: [jeremylongshore/omarchy-mlb-booth-entry](https://github.com/jeremylongshore/omarchy-mlb-booth-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **35**; head: `79a47e3cd1ab8227ce7c563ba2ed29e0d9f6bcd1`. GitHub license metadata: **MIT**. Tree: **79 files**, complete. Observation: `2026-10-12T06:31:01Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-mlb-booth-entry/blob/79a47e3cd1ab8227ce7c563ba2ed29e0d9f6bcd1/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-mlb-booth-entry/blob/79a47e3cd1ab8227ce7c563ba2ed29e0d9f6bcd1/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-mlb-booth-entry/blob/79a47e3cd1ab8227ce7c563ba2ed29e0d9f6bcd1/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 2 tags and 2 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R127

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R128: omarchy-omatrail-entry

Repository: [jeremylongshore/omarchy-omatrail-entry](https://github.com/jeremylongshore/omarchy-omatrail-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **80**; head: `d4667749c7f5838af94fb53d0407970a43024ce3`. GitHub license metadata: **MIT**. Tree: **173 files**, complete. Observation: `2026-10-12T06:31:02Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L129–131](https://github.com/jeremylongshore/omarchy-omatrail-entry/blob/d4667749c7f5838af94fb53d0407970a43024ce3/README.md#L129-L131) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`CHANGELOG.md` L18–20](https://github.com/jeremylongshore/omarchy-omatrail-entry/blob/d4667749c7f5838af94fb53d0407970a43024ce3/CHANGELOG.md#L18-L20) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/minimax-review.yml` L207–209](https://github.com/jeremylongshore/omarchy-omatrail-entry/blob/d4667749c7f5838af94fb53d0407970a43024ce3/.github/workflows/minimax-review.yml#L207-L209) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L235–237](https://github.com/jeremylongshore/omarchy-omatrail-entry/blob/d4667749c7f5838af94fb53d0407970a43024ce3/.github/workflows/minimax-review.yml#L235-L237) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L207–209](https://github.com/jeremylongshore/omarchy-omatrail-entry/blob/d4667749c7f5838af94fb53d0407970a43024ce3/.github/workflows/minimax-review.yml#L207-L209).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L18–20](https://github.com/jeremylongshore/omarchy-omatrail-entry/blob/d4667749c7f5838af94fb53d0407970a43024ce3/CHANGELOG.md#L18-L20).
- **Verification scope:** 8/8 Contents requests returned HTTP 200; 23 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R129: omarchy-pit-wall-entry

Repository: [jeremylongshore/omarchy-pit-wall-entry](https://github.com/jeremylongshore/omarchy-pit-wall-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **33**; head: `f54d730648c3e918b61c9acde812c03b2f90fcd3`. GitHub license metadata: **MIT**. Tree: **80 files**, complete. Observation: `2026-10-12T06:31:04Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-pit-wall-entry/blob/f54d730648c3e918b61c9acde812c03b2f90fcd3/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-pit-wall-entry/blob/f54d730648c3e918b61c9acde812c03b2f90fcd3/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-pit-wall-entry/blob/f54d730648c3e918b61c9acde812c03b2f90fcd3/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R130: omarchy-quiet-queue-entry

Repository: [jeremylongshore/omarchy-quiet-queue-entry](https://github.com/jeremylongshore/omarchy-quiet-queue-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **38**; head: `8616c6d14779a0b84859927dc083ce4af170085b`. GitHub license metadata: **MIT**. Tree: **76 files**, complete. Observation: `2026-10-12T06:31:04Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-quiet-queue-entry/blob/8616c6d14779a0b84859927dc083ce4af170085b/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-quiet-queue-entry/blob/8616c6d14779a0b84859927dc083ce4af170085b/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-quiet-queue-entry/blob/8616c6d14779a0b84859927dc083ce4af170085b/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R131: omarchy-ship

Repository: [jeremylongshore/omarchy-ship](https://github.com/jeremylongshore/omarchy-ship). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **4**; head: `83f5ed873e95c04911e46b6ad131dc6ef91daef0`. GitHub license metadata: **MIT**. Tree: **23 files**, complete. Observation: `2026-10-12T06:31:04Z`.

- **Trace:** [`CHANGELOG.md` L28–30](https://github.com/jeremylongshore/omarchy-ship/blob/83f5ed873e95c04911e46b6ad131dc6ef91daef0/CHANGELOG.md#L28-L30) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L121–123](https://github.com/jeremylongshore/omarchy-ship/blob/83f5ed873e95c04911e46b6ad131dc6ef91daef0/README.md#L121-L123) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L28–30](https://github.com/jeremylongshore/omarchy-ship/blob/83f5ed873e95c04911e46b6ad131dc6ef91daef0/CHANGELOG.md#L28-L30).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R132

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R133: omarchy-wait-state-entry

Repository: [jeremylongshore/omarchy-wait-state-entry](https://github.com/jeremylongshore/omarchy-wait-state-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **19**; head: `2c84ec04540578ced9403fc74aa7c153bff7bb95`. GitHub license metadata: **MIT**. Tree: **76 files**, complete. Observation: `2026-10-12T06:31:06Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L93–95](https://github.com/jeremylongshore/omarchy-wait-state-entry/blob/2c84ec04540578ced9403fc74aa7c153bff7bb95/README.md#L93-L95) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-wait-state-entry/blob/2c84ec04540578ced9403fc74aa7c153bff7bb95/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-wait-state-entry/blob/2c84ec04540578ced9403fc74aa7c153bff7bb95/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-wait-state-entry/blob/2c84ec04540578ced9403fc74aa7c153bff7bb95/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 1 release records have lexical matches. [release `v1.0.0`](https://github.com/jeremylongshore/omarchy-wait-state-entry/releases/tag/v1.0.0).
- **Verification scope:** 8/8 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R134: omarchy-widget-template

Repository: [jeremylongshore/omarchy-widget-template](https://github.com/jeremylongshore/omarchy-widget-template). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **37**; head: `09dee7afbcbe565057c9a9f744fd2eeb5af3dc4d`. GitHub license metadata: **MIT**. Tree: **70 files**, complete. Observation: `2026-10-12T06:31:06Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L207–209](https://github.com/jeremylongshore/omarchy-widget-template/blob/09dee7afbcbe565057c9a9f744fd2eeb5af3dc4d/.github/workflows/minimax-review.yml#L207-L209) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L235–237](https://github.com/jeremylongshore/omarchy-widget-template/blob/09dee7afbcbe565057c9a9f744fd2eeb5af3dc4d/.github/workflows/minimax-review.yml#L235-L237) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L207–209](https://github.com/jeremylongshore/omarchy-widget-template/blob/09dee7afbcbe565057c9a9f744fd2eeb5af3dc4d/.github/workflows/minimax-review.yml#L207-L209).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R135: omarchy-workspace-storyboard-entry

Repository: [jeremylongshore/omarchy-workspace-storyboard-entry](https://github.com/jeremylongshore/omarchy-workspace-storyboard-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **37**; head: `fadbe463f541a382c207694ac74b303e367081f0`. GitHub license metadata: **MIT**. Tree: **80 files**, complete. Observation: `2026-10-12T06:31:08Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-workspace-storyboard-entry/blob/fadbe463f541a382c207694ac74b303e367081f0/.github/workflows/minimax-review.yml#L155-L157) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L183–185](https://github.com/jeremylongshore/omarchy-workspace-storyboard-entry/blob/fadbe463f541a382c207694ac74b303e367081f0/.github/workflows/minimax-review.yml#L183-L185) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L155–157](https://github.com/jeremylongshore/omarchy-workspace-storyboard-entry/blob/fadbe463f541a382c207694ac74b303e367081f0/.github/workflows/minimax-review.yml#L155-L157).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L35–37](https://github.com/jeremylongshore/omarchy-workspace-storyboard-entry/blob/fadbe463f541a382c207694ac74b303e367081f0/CHANGELOG.md#L35-L37).
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 3 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R136: omarchy-x-files-entry

Repository: [jeremylongshore/omarchy-x-files-entry](https://github.com/jeremylongshore/omarchy-x-files-entry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **31**; head: `7d942d7291072bd79935e239f3ef626441d0787a`. GitHub license metadata: **MIT**. Tree: **82 files**, complete. Observation: `2026-10-12T06:31:08Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L212–214](https://github.com/jeremylongshore/omarchy-x-files-entry/blob/7d942d7291072bd79935e239f3ef626441d0787a/README.md#L212-L214) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-x-files-entry/blob/7d942d7291072bd79935e239f3ef626441d0787a/.github/workflows/minimax-review.yml#L197-L199) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/omarchy-x-files-entry/blob/7d942d7291072bd79935e239f3ef626441d0787a/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L197–199](https://github.com/jeremylongshore/omarchy-x-files-entry/blob/7d942d7291072bd79935e239f3ef626441d0787a/.github/workflows/minimax-review.yml#L197-L199).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R137: oss-agent-lab

Repository: [jeremylongshore/oss-agent-lab](https://github.com/jeremylongshore/oss-agent-lab). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **39**; head: `7f188f6b89300523bf0e9864fc26f35a621df981`. GitHub license metadata: **MIT**. Tree: **145 files**, complete. Observation: `2026-10-12T06:31:08Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`scoring/scorer.py` L184–186](https://github.com/jeremylongshore/oss-agent-lab/blob/7f188f6b89300523bf0e9864fc26f35a621df981/scoring/scorer.py#L184-L186) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`scoring/index.py` L81–83](https://github.com/jeremylongshore/oss-agent-lab/blob/7f188f6b89300523bf0e9864fc26f35a621df981/scoring/index.py#L81-L83) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/validate.yml` L40–42](https://github.com/jeremylongshore/oss-agent-lab/blob/7f188f6b89300523bf0e9864fc26f35a621df981/.github/workflows/validate.yml#L40-L42).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L42–44](https://github.com/jeremylongshore/oss-agent-lab/blob/7f188f6b89300523bf0e9864fc26f35a621df981/CHANGELOG.md#L42-L44); [release `v1.0.0`](https://github.com/jeremylongshore/oss-agent-lab/releases/tag/v1.0.0).
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 11 other filename candidates remain uninspected. All 1 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R138

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R139: perception-with-intent

Repository: [jeremylongshore/perception-with-intent](https://github.com/jeremylongshore/perception-with-intent). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **100**; head: `b812b4406c41584a095b109b41ff5dfc58700b03`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **329 files**, complete. Observation: `2026-10-12T06:31:10Z`.

- **Trace:** [`.github/workflows/deploy.yml` L86–88](https://github.com/jeremylongshore/perception-with-intent/blob/b812b4406c41584a095b109b41ff5dfc58700b03/.github/workflows/deploy.yml#L86-L88) (workflow; lexical evidence, not an operational verdict).
- **Telemetry:** [`README.md` L517–519](https://github.com/jeremylongshore/perception-with-intent/blob/b812b4406c41584a095b109b41ff5dfc58700b03/README.md#L517-L519) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L148–150](https://github.com/jeremylongshore/perception-with-intent/blob/b812b4406c41584a095b109b41ff5dfc58700b03/README.md#L148-L150) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/deploy-agents.yml` L79–81](https://github.com/jeremylongshore/perception-with-intent/blob/b812b4406c41584a095b109b41ff5dfc58700b03/.github/workflows/deploy-agents.yml#L79-L81); [`.github/workflows/deploy.yml` L86–88](https://github.com/jeremylongshore/perception-with-intent/blob/b812b4406c41584a095b109b41ff5dfc58700b03/.github/workflows/deploy.yml#L86-L88).
- **Release/changelog evidence:** 3 tags and 3 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L105–107](https://github.com/jeremylongshore/perception-with-intent/blob/b812b4406c41584a095b109b41ff5dfc58700b03/CHANGELOG.md#L105-L107).
- **Verification scope:** 13/13 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 9 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R140: plane

Repository: [jeremylongshore/plane](https://github.com/jeremylongshore/plane). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `preview`; reachable commits: **6988**; head: `13db2f883f141f139b106f9459c44ad030772d73`. GitHub license metadata: **AGPL-3.0**. Tree: **4929 files**, complete. Observation: `2026-10-12T06:31:10Z`.

- **Trace:** [`apps/api/plane/utils/telemetry.py` L10–12](https://github.com/jeremylongshore/plane/blob/13db2f883f141f139b106f9459c44ad030772d73/apps/api/plane/utils/telemetry.py#L10-L12) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`apps/api/plane/utils/telemetry.py` L10–12](https://github.com/jeremylongshore/plane/blob/13db2f883f141f139b106f9459c44ad030772d73/apps/api/plane/utils/telemetry.py#L10-L12) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`.github/workflows/feature-deployment.yml` L162–164](https://github.com/jeremylongshore/plane/blob/13db2f883f141f139b106f9459c44ad030772d73/.github/workflows/feature-deployment.yml#L162-L164) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/feature-deployment.yml` L162–164](https://github.com/jeremylongshore/plane/blob/13db2f883f141f139b106f9459c44ad030772d73/.github/workflows/feature-deployment.yml#L162-L164).
- **Release/changelog evidence:** 55 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 12/12 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 7 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R141

Visibility: **public**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R142: posthog

Repository: [jeremylongshore/posthog](https://github.com/jeremylongshore/posthog). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `master`; reachable commits: **32350**; head: `9363415156300413a0eb614b70428eeae1ba2a24`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **15432 files**, complete. Observation: `2026-10-12T06:31:12Z`.

- **Trace:** [`nodejs/src/common/tracing/otel.ts` L2–4](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/nodejs/src/common/tracing/otel.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`nodejs/src/common/tracing/otel.ts` L1–3](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/nodejs/src/common/tracing/otel.ts#L1-L3) (source; lexical evidence, not an operational verdict).
- **Annotation:** [`frontend/src/models/annotationsModel.ts` L10–12](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/frontend/src/models/annotationsModel.ts#L10-L12) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/scripts/post-eval-summary.js` L6–8](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/scripts/post-eval-summary.js#L6-L8) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** [`frontend/src/taxonomy/helpers.ts` L1–3](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/frontend/src/taxonomy/helpers.ts#L1-L3) (source; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/cd-ai-evals-image.yml` L2–4](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/workflows/cd-ai-evals-image.yml#L2-L4); [`.github/workflows/ci-ai.yml` L17–19](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/workflows/ci-ai.yml#L17-L19); [`.github/workflows/ci-backend.yml` L839–841](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/workflows/ci-backend.yml#L839-L841); [`.github/workflows/ci-frontend.yml` L138–140](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/workflows/ci-frontend.yml#L138-L140); [`.github/workflows/ci-python.yml` L121–123](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/workflows/ci-python.yml#L121-L123); [`.github/workflows/ci-rust.yml` L210–212](https://github.com/jeremylongshore/posthog/blob/9363415156300413a0eb614b70428eeae1ba2a24/.github/workflows/ci-rust.yml#L210-L212).
- **Release/changelog evidence:** 135 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 70/70 Contents requests returned HTTP 200; 249 other filename candidates remain uninspected. All 50 workflow paths and 5 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R143: pr-to-prompt

Repository: [jeremylongshore/pr-to-prompt](https://github.com/jeremylongshore/pr-to-prompt). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **65**; head: `c77dee8fc83ca4ad1ad1bcfae437939c427a96b9`. GitHub license metadata: **MIT**. Tree: **145 files**, complete. Observation: `2026-10-12T06:31:13Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`src/core/contracts/evaluator.ts` L182–184](https://github.com/jeremylongshore/pr-to-prompt/blob/c77dee8fc83ca4ad1ad1bcfae437939c427a96b9/src/core/contracts/evaluator.ts#L182-L184) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** [`CHANGELOG.md` L79–81](https://github.com/jeremylongshore/pr-to-prompt/blob/c77dee8fc83ca4ad1ad1bcfae437939c427a96b9/CHANGELOG.md#L79-L81) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 5 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 8 tags and 7 releases enumerated; 2 release records have lexical matches. [`CHANGELOG.md` L79–81](https://github.com/jeremylongshore/pr-to-prompt/blob/c77dee8fc83ca4ad1ad1bcfae437939c427a96b9/CHANGELOG.md#L79-L81); [release `v0.8.0`](https://github.com/jeremylongshore/pr-to-prompt/releases/tag/v0.8.0); [release `v0.7.0`](https://github.com/jeremylongshore/pr-to-prompt/releases/tag/v0.7.0).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 5 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R144

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R145: prompts-intent-solutions

Repository: [jeremylongshore/prompts-intent-solutions](https://github.com/jeremylongshore/prompts-intent-solutions). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **38**; head: `571b5842ba418b08f295f26b4995ddf7122629f8`. GitHub license metadata: **MIT**. Tree: **324 files**, complete. Observation: `2026-10-12T06:31:15Z`.

- **Trace:** [`prompts/03-cloud-observability-audit.md` L17–19](https://github.com/jeremylongshore/prompts-intent-solutions/blob/571b5842ba418b08f295f26b4995ddf7122629f8/prompts/03-cloud-observability-audit.md#L17-L19) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`prompts/03-cloud-observability-audit.md` L2–4](https://github.com/jeremylongshore/prompts-intent-solutions/blob/571b5842ba418b08f295f26b4995ddf7122629f8/prompts/03-cloud-observability-audit.md#L2-L4) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`prompts/03-cloud-observability-audit.md` L13–15](https://github.com/jeremylongshore/prompts-intent-solutions/blob/571b5842ba418b08f295f26b4995ddf7122629f8/prompts/03-cloud-observability-audit.md#L13-L15) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L51–53](https://github.com/jeremylongshore/prompts-intent-solutions/blob/571b5842ba418b08f295f26b4995ddf7122629f8/README.md#L51-L53) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 6 tags and 5 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R146: publishing-skills

Repository: [jeremylongshore/publishing-skills](https://github.com/jeremylongshore/publishing-skills). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **13**; head: `43fbe3d700d0c658ed71acf51b8a26188b719e11`. GitHub license metadata: **MIT-0**. Tree: **22 files**, complete. Observation: `2026-10-12T06:31:17Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L5–7](https://github.com/jeremylongshore/publishing-skills/blob/43fbe3d700d0c658ed71acf51b8a26188b719e11/README.md#L5-L7) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L9–11](https://github.com/jeremylongshore/publishing-skills/blob/43fbe3d700d0c658ed71acf51b8a26188b719e11/README.md#L9-L11) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** [`README.md` L11–13](https://github.com/jeremylongshore/publishing-skills/blob/43fbe3d700d0c658ed71acf51b8a26188b719e11/README.md#L11-L13) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R147: resume-firebase

Repository: [jeremylongshore/resume-firebase](https://github.com/jeremylongshore/resume-firebase). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **129**; head: `58fa356b8d7619131ad776517778b65d5d805cbe`. GitHub license metadata: **unclassified by GitHub**. Tree: **238 files**, complete. Observation: `2026-10-12T06:31:17Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L125–127](https://github.com/jeremylongshore/resume-firebase/blob/58fa356b8d7619131ad776517778b65d5d805cbe/README.md#L125-L127) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 5 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 5 tags and 5 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 5 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R148: resume-realtime

Repository: [jeremylongshore/resume-realtime](https://github.com/jeremylongshore/resume-realtime). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **17**; head: `db0d66c46b655fbb95facf3a5e45dedf4965bdc1`. GitHub license metadata: **MIT**. Tree: **45 files**, complete. Observation: `2026-10-12T06:31:18Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R149: rtfm-testing

Repository: [jeremylongshore/rtfm-testing](https://github.com/jeremylongshore/rtfm-testing). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **3**; head: `667675dcba160eef8e580926c4d4a8152d6e2e7e`. GitHub license metadata: **unclassified by GitHub**. Tree: **5 files**, complete. Observation: `2026-10-12T06:31:18Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R150: schedule-after-usage-reset

Repository: [jeremylongshore/schedule-after-usage-reset](https://github.com/jeremylongshore/schedule-after-usage-reset). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **8**; head: `c294becc35125f6d8e0aff7709314205e54b4e6d`. GitHub license metadata: **MIT**. Tree: **11 files**, complete. Observation: `2026-10-12T06:31:19Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R151: searchcarriers

Repository: [jeremylongshore/searchcarriers](https://github.com/jeremylongshore/searchcarriers). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **32**; head: `f7e2babef3b8dd147c3f3a5168290aa02e1d5b64`. GitHub license metadata: **Apache-2.0**. Tree: **186 files**, complete. Observation: `2026-10-12T06:31:20Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L5–7](https://github.com/jeremylongshore/searchcarriers/blob/f7e2babef3b8dd147c3f3a5168290aa02e1d5b64/README.md#L5-L7) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L89–91](https://github.com/jeremylongshore/searchcarriers/blob/f7e2babef3b8dd147c3f3a5168290aa02e1d5b64/CHANGELOG.md#L89-L91).
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R152: searchcarriers-tools

Repository: [jeremylongshore/searchcarriers-tools](https://github.com/jeremylongshore/searchcarriers-tools). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **6**; head: `579ad1d612e9fe85a6739c8bba05964475d518aa`. GitHub license metadata: **Apache-2.0**. Tree: **350 files**, complete. Observation: `2026-10-12T06:31:20Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh` L259–261](https://github.com/jeremylongshore/searchcarriers-tools/blob/579ad1d612e9fe85a6739c8bba05964475d518aa/.audit-harness/scripts/emit-evidence.sh#L259-L261) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.audit-harness/scripts/emit-evidence.sh` L9–11](https://github.com/jeremylongshore/searchcarriers-tools/blob/579ad1d612e9fe85a6739c8bba05964475d518aa/.audit-harness/scripts/emit-evidence.sh#L9-L11) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/searchcarriers-tools/blob/579ad1d612e9fe85a6739c8bba05964475d518aa/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh` L260–262](https://github.com/jeremylongshore/searchcarriers-tools/blob/579ad1d612e9fe85a6739c8bba05964475d518aa/.audit-harness/scripts/emit-evidence.sh#L260-L262) (source; lexical evidence, not an operational verdict).
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L23–25](https://github.com/jeremylongshore/searchcarriers-tools/blob/579ad1d612e9fe85a6739c8bba05964475d518aa/.audit-harness/CHANGELOG.md#L23-L25); [`CHANGELOG.md` L32–34](https://github.com/jeremylongshore/searchcarriers-tools/blob/579ad1d612e9fe85a6739c8bba05964475d518aa/CHANGELOG.md#L32-L34).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 23 other filename candidates remain uninspected. All 2 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R153

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R154

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R155: skill.md

Repository: [jeremylongshore/skill.md](https://github.com/jeremylongshore/skill.md). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `master`; reachable commits: **6**; head: `f6740b67d1acef885c18e6e5fd1f629b648e81c9`. GitHub license metadata: **unclassified by GitHub**. Tree: **5 files**, complete. Observation: `2026-10-12T06:31:23Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R156: skills

Repository: [jeremylongshore/skills](https://github.com/jeremylongshore/skills). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **47**; head: `7c71a845071e8f994253db0d26c7e36fa90e2b5e`. GitHub license metadata: **MIT**. Tree: **429 files**, complete. Observation: `2026-10-12T06:31:23Z`.

- **Trace:** [`README.md` L116–118](https://github.com/jeremylongshore/skills/blob/7c71a845071e8f994253db0d26c7e36fa90e2b5e/README.md#L116-L118) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`README.md` L1011–1013](https://github.com/jeremylongshore/skills/blob/7c71a845071e8f994253db0d26c7e36fa90e2b5e/README.md#L1011-L1013) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`README.md` L394–396](https://github.com/jeremylongshore/skills/blob/7c71a845071e8f994253db0d26c7e36fa90e2b5e/README.md#L394-L396) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`README.md` L90–92](https://github.com/jeremylongshore/skills/blob/7c71a845071e8f994253db0d26c7e36fa90e2b5e/README.md#L90-L92) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L156–158](https://github.com/jeremylongshore/skills/blob/7c71a845071e8f994253db0d26c7e36fa90e2b5e/README.md#L156-L158) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R157: startaitools.com

Repository: [jeremylongshore/startaitools.com](https://github.com/jeremylongshore/startaitools.com). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `master`; reachable commits: **1557**; head: `0a1813dd3c75658f3900733be5f97eea233ed4c0`. GitHub license metadata: **MIT**. Tree: **5215 files**, complete. Observation: `2026-10-12T06:31:24Z`.

- **Trace:** [`content/posts/wild-deep-dive-3-observability.md` L55–57](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/content/posts/wild-deep-dive-3-observability.md#L55-L57) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`CHANGELOG.md` L3586–3588](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/CHANGELOG.md#L3586-L3588) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`scripts/blog/blogpipe/evidence.py` L38–40](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/scripts/blog/blogpipe/evidence.py#L38-L40) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`CHANGELOG.md` L3365–3367](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/CHANGELOG.md#L3365-L3367) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`scripts/blog/blogpipe/evidence.py` L1–3](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/scripts/blog/blogpipe/evidence.py#L1-L3) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/deploy.yml` L3–5](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/.github/workflows/deploy.yml#L3-L5).
- **Release/changelog evidence:** 337 tags and 335 releases enumerated; 13 release records have lexical matches. [`CHANGELOG.md` L310–312](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/CHANGELOG.md#L310-L312); [`content/mcp-for-beginners/changelog.md` L34–36](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/content/mcp-for-beginners/changelog.md#L34-L36); [`content/mcp-for-beginners/translations/en/changelog.md` L43–45](https://github.com/jeremylongshore/startaitools.com/blob/0a1813dd3c75658f3900733be5f97eea233ed4c0/content/mcp-for-beginners/translations/en/changelog.md#L43-L45); [release `v1.29.0`](https://github.com/jeremylongshore/startaitools.com/releases/tag/v1.29.0); [release `v1.27.1`](https://github.com/jeremylongshore/startaitools.com/releases/tag/v1.27.1); [release `v1.23.0`](https://github.com/jeremylongshore/startaitools.com/releases/tag/v1.23.0).
- **Verification scope:** 14/14 Contents requests returned HTTP 200; 11 other filename candidates remain uninspected. All 3 workflow paths and 3 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R158: stci-standard-inference-token-cost-index

Repository: [jeremylongshore/stci-standard-inference-token-cost-index](https://github.com/jeremylongshore/stci-standard-inference-token-cost-index). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **129**; head: `d432b0a0571961187e647c5468dcb6248105f2f1`. GitHub license metadata: **MIT**. Tree: **283 files**, complete. Observation: `2026-10-12T06:31:25Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L26–28](https://github.com/jeremylongshore/stci-standard-inference-token-cost-index/blob/d432b0a0571961187e647c5468dcb6248105f2f1/README.md#L26-L28) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L201–203](https://github.com/jeremylongshore/stci-standard-inference-token-cost-index/blob/d432b0a0571961187e647c5468dcb6248105f2f1/README.md#L201-L203) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 5 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 6 tags and 6 releases enumerated; 2 release records have lexical matches. [`CHANGELOG.md` L12–14](https://github.com/jeremylongshore/stci-standard-inference-token-cost-index/blob/d432b0a0571961187e647c5468dcb6248105f2f1/CHANGELOG.md#L12-L14); [release `v0.5.0`](https://github.com/jeremylongshore/stci-standard-inference-token-cost-index/releases/tag/v0.5.0); [release `v0.2.0`](https://github.com/jeremylongshore/stci-standard-inference-token-cost-index/releases/tag/v0.2.0).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 5 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R159: tldraw

Repository: [jeremylongshore/tldraw](https://github.com/jeremylongshore/tldraw). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **5205**; head: `988379f9c4c267f8e848ff0f09c5d29ed60cb812`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **3761 files**, complete. Observation: `2026-10-12T06:31:25Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`apps/examples/src/examples/image-annotator/types.tsx` L1–3](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/apps/examples/src/examples/image-annotator/types.tsx#L1-L3) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`internal/scripts/benchmark-validators.ts` L2–4](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/internal/scripts/benchmark-validators.ts#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/checks.yml` L11–13](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/checks.yml#L11-L13); [`.github/workflows/deploy-analytics.yml` L21–23](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/deploy-analytics.yml#L21-L23); [`.github/workflows/deploy-bemo.yml` L13–15](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/deploy-bemo.yml#L13-L15); [`.github/workflows/deploy-dotcom.yml` L15–17](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/deploy-dotcom.yml#L15-L17); [`.github/workflows/playwright-dotcom.yml` L11–13](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/playwright-dotcom.yml#L11-L13); [`.github/workflows/playwright-examples.yml` L11–13](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/playwright-examples.yml#L11-L13); [`.github/workflows/playwright-update-snapshots.yml` L22–24](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/playwright-update-snapshots.yml#L22-L24); [`.github/workflows/prune-preview-deploys.yml` L14–16](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/prune-preview-deploys.yml#L14-L16); [`.github/workflows/publish-editor-extensions.yml` L11–13](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/publish-editor-extensions.yml#L11-L13); [`.github/workflows/publish-templates.yml` L14–16](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/publish-templates.yml#L14-L16); [`.github/workflows/staging-e2e.yml` L17–19](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/.github/workflows/staging-e2e.yml#L17-L19).
- **Release/changelog evidence:** 276 tags and 0 releases enumerated; 0 release records have lexical matches. [`packages/editor/src/lib/editor/managers/HistoryManager/HistoryManager.test.ts` L492–494](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/packages/editor/src/lib/editor/managers/HistoryManager/HistoryManager.test.ts#L492-L494); [`packages/editor/src/lib/editor/managers/HistoryManager/HistoryManager.ts` L39–41](https://github.com/jeremylongshore/tldraw/blob/988379f9c4c267f8e848ff0f09c5d29ed60cb812/packages/editor/src/lib/editor/managers/HistoryManager/HistoryManager.ts#L39-L41).
- **Verification scope:** 42/42 Contents requests returned HTTP 200; 3 other filename candidates remain uninspected. All 30 workflow paths and 6 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R160: tonone

Repository: [jeremylongshore/tonone](https://github.com/jeremylongshore/tonone). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **209**; head: `b06717187547dd931a973a69b41d8a2c2013803e`. GitHub license metadata: **MIT**. Tree: **2005 files**, complete. Observation: `2026-10-12T06:31:27Z`.

- **Trace:** [`team/trace/scripts/setup.sh` L3–3](https://github.com/jeremylongshore/tonone/blob/b06717187547dd931a973a69b41d8a2c2013803e/team/trace/scripts/setup.sh#L3-L3) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`README.md` L113–115](https://github.com/jeremylongshore/tonone/blob/b06717187547dd931a973a69b41d8a2c2013803e/README.md#L113-L115) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`team/cortex/scripts/cortex_agent/prompt_evaluator.py` L3–5](https://github.com/jeremylongshore/tonone/blob/b06717187547dd931a973a69b41d8a2c2013803e/team/cortex/scripts/cortex_agent/prompt_evaluator.py#L3-L5) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`team/eval/scripts/setup.sh` L3–3](https://github.com/jeremylongshore/tonone/blob/b06717187547dd931a973a69b41d8a2c2013803e/team/eval/scripts/setup.sh#L3-L3) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 1 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L20–22](https://github.com/jeremylongshore/tonone/blob/b06717187547dd931a973a69b41d8a2c2013803e/CHANGELOG.md#L20-L22).
- **Verification scope:** 10/10 Contents requests returned HTTP 200; 24 other filename candidates remain uninspected. All 1 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R161: tons-of-skills-marketplace

Repository: [jeremylongshore/tons-of-skills-marketplace](https://github.com/jeremylongshore/tons-of-skills-marketplace). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **2840**; head: `0d6ff1b7183c1cf4603187fc861c46466603e1b9`. GitHub license metadata: **MIT**. Tree: **25998 files**, complete. Observation: `2026-10-12T06:31:29Z`.

- **Trace:** [`skills/.curated/setting-up-distributed-tracing/scripts/setup_jaeger.py` L3–5](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/skills/.curated/setting-up-distributed-tracing/scripts/setup_jaeger.py#L3-L5) (source; lexical evidence, not an operational verdict).
- **Telemetry:** [`CHANGELOG.md` L974–976](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/CHANGELOG.md#L974-L976) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`skills/.curated/production-upgrade/scripts/audit_evidence.py` L4–6](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/skills/.curated/production-upgrade/scripts/audit_evidence.py#L4-L6) (source; lexical evidence, not an operational verdict).
- **Evaluation:** [`scripts/run-jrig-eval.sh` L2–4](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/scripts/run-jrig-eval.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`scripts/run-jrig-eval.sh` L39–41](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/scripts/run-jrig-eval.sh#L39-L41) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/minimax-review.yml#L12-L14) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/auto-bump-on-pr.yml` L120–122](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/auto-bump-on-pr.yml#L120-L122); [`.github/workflows/capture-marketplace-compliance-baseline.yml` L109–109](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/capture-marketplace-compliance-baseline.yml#L109-L109); [`.github/workflows/cli-publish.yml` L158–160](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/cli-publish.yml#L158-L160); [`.github/workflows/consistency-fixture-gate.yml` L4–6](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/consistency-fixture-gate.yml#L4-L6); [`.github/workflows/emit-evidence.yml` L1–3](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/emit-evidence.yml#L1-L3); [`.github/workflows/emit-publication-evidence.yml` L1–3](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/emit-publication-evidence.yml#L1-L3); [`.github/workflows/external-sync-fs-contract.yml` L14–16](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/external-sync-fs-contract.yml#L14-L16); [`.github/workflows/jrig-proofs-test.yml` L3–5](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/jrig-proofs-test.yml#L3-L5); [`.github/workflows/kernel-shadow-validation.yml` L16–18](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/kernel-shadow-validation.yml#L16-L18); [`.github/workflows/kernel-vendor-hash.yml` L86–88](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/kernel-vendor-hash.yml#L86-L88); [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/minimax-review.yml#L12-L14); [`.github/workflows/pr-prescreen-respond.yml` L15–17](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/pr-prescreen-respond.yml#L15-L17); [`.github/workflows/pr-prescreen.yml` L148–150](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/pr-prescreen.yml#L148-L150); [`.github/workflows/publish-all-packages.yml` L264–266](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/publish-all-packages.yml#L264-L266); [`.github/workflows/publish-changed-packages.yml` L6–8](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/publish-changed-packages.yml#L6-L8); [`.github/workflows/publish-mcp-registry.yml` L90–92](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/publish-mcp-registry.yml#L90-L92); [`.github/workflows/release.yml` L163–165](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/release.yml#L163-L165); [`.github/workflows/skill-conform.yml` L11–13](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/skill-conform.yml#L11-L13); [`.github/workflows/skill-eval-advisory.yml` L1–3](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/skill-eval-advisory.yml#L1-L3); [`.github/workflows/sync-external.yml` L35–37](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/sync-external.yml#L35-L37); [`.github/workflows/validate-plugins.yml` L31–33](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/validate-plugins.yml#L31-L33); [`.github/workflows/windows-path-contract.yml` L12–14](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/.github/workflows/windows-path-contract.yml#L12-L14).
- **Release/changelog evidence:** 234 tags and 218 releases enumerated; 27 release records have lexical matches. [`CHANGELOG.md` L5–7](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/CHANGELOG.md#L5-L7); [`plugins/community/skills-janitor/CHANGELOG.md` L77–79](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/plugins/community/skills-janitor/CHANGELOG.md#L77-L79); [`plugins/database/freshie-inventory-manager/CHANGELOG.md` L30–31](https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0d6ff1b7183c1cf4603187fc861c46466603e1b9/plugins/database/freshie-inventory-manager/CHANGELOG.md#L30-L31); [release `@intentsolutionsio/agency-os@0.1.12`](https://github.com/jeremylongshore/tons-of-skills-marketplace/releases/tag/%40intentsolutionsio/agency-os%400.1.12); [release `@intentsolutionsio/governed-second-brain@0.1.7`](https://github.com/jeremylongshore/tons-of-skills-marketplace/releases/tag/%40intentsolutionsio/governed-second-brain%400.1.7); [release `@intentsolutionsio/000-jeremy-content-consistency-validator@3.0.2`](https://github.com/jeremylongshore/tons-of-skills-marketplace/releases/tag/%40intentsolutionsio/000-jeremy-content-consistency-validator%403.0.2); tag `evidence-latest` at `12f47f290dbb3a6127d31dd7b3298ac4d8a4411a`.
- **Verification scope:** 76/76 Contents requests returned HTTP 200; 831 other filename candidates remain uninspected. All 39 workflow paths and 21 changelog paths were requested. 1 verified file references withheld from this projection.

### A1-R162: twenty-mcp

Repository: [jeremylongshore/twenty-mcp](https://github.com/jeremylongshore/twenty-mcp). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **21**; head: `f98f20caf32bc935674f3b0f4ed75264385f325f`. GitHub license metadata: **MIT**. Tree: **80 files**, complete. Observation: `2026-10-12T06:31:29Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L185–187](https://github.com/jeremylongshore/twenty-mcp/blob/f98f20caf32bc935674f3b0f4ed75264385f325f/README.md#L185-L187) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 3 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L30–32](https://github.com/jeremylongshore/twenty-mcp/blob/f98f20caf32bc935674f3b0f4ed75264385f325f/CHANGELOG.md#L30-L32).
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R163: ui-ux-pro-max-skill

Repository: [jeremylongshore/ui-ux-pro-max-skill](https://github.com/jeremylongshore/ui-ux-pro-max-skill). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **92**; head: `442307554ba70b9034914241eb5b6a8c3374663b`. GitHub license metadata: **MIT**. Tree: **117 files**, complete. Observation: `2026-10-12T06:31:31Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R164: uizze

Repository: [jeremylongshore/uizze](https://github.com/jeremylongshore/uizze). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **40**; head: `d2cacfdcbe25d506820fa74bae4b7678e1c05de5`. GitHub license metadata: **MIT**. Tree: **251 files**, complete. Observation: `2026-10-12T06:31:33Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`integrations/benchmark/scripts/verify.mjs` L11–13](https://github.com/jeremylongshore/uizze/blob/d2cacfdcbe25d506820fa74bae4b7678e1c05de5/integrations/benchmark/scripts/verify.mjs#L11-L13) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`integrations/benchmark/scripts/benchmark-lib.mjs` L90–92](https://github.com/jeremylongshore/uizze/blob/d2cacfdcbe25d506820fa74bae4b7678e1c05de5/integrations/benchmark/scripts/benchmark-lib.mjs#L90-L92) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 4 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 13 tags and 0 releases enumerated; 0 release records have lexical matches. [`integrations/benchmark/CHANGELOG.md` L6–7](https://github.com/jeremylongshore/uizze/blob/d2cacfdcbe25d506820fa74bae4b7678e1c05de5/integrations/benchmark/CHANGELOG.md#L6-L7).
- **Verification scope:** 13/13 Contents requests returned HTTP 200; 34 other filename candidates remain uninspected. All 4 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R165: vertex-ai-samples

Repository: [jeremylongshore/vertex-ai-samples](https://github.com/jeremylongshore/vertex-ai-samples). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **4123**; head: `3e4ed5a9fded94bac8b5dbe6d8c59e8d5c5195f1`. GitHub license metadata: **Apache-2.0**. Tree: **1275 files**, complete. Observation: `2026-10-12T06:31:33Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`README.md` L84–86](https://github.com/jeremylongshore/vertex-ai-samples/blob/3e4ed5a9fded94bac8b5dbe6d8c59e8d5c5195f1/README.md#L84-L86) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`community-content/vertex_pipeline_kfpv2/evaluate-model.py` L4–6](https://github.com/jeremylongshore/vertex-ai-samples/blob/3e4ed5a9fded94bac8b5dbe6d8c59e8d5c5195f1/community-content/vertex_pipeline_kfpv2/evaluate-model.py#L4-L6) (source; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 6 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R166: walkie-talkie

Repository: [jeremylongshore/walkie-talkie](https://github.com/jeremylongshore/walkie-talkie). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **2**; head: `0b74f4d361022f51297896e2ef884c0ed5bfd0df`. GitHub license metadata: **MIT**. Tree: **5 files**, complete. Observation: `2026-10-12T06:31:35Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L34–36](https://github.com/jeremylongshore/walkie-talkie/blob/0b74f4d361022f51297896e2ef884c0ed5bfd0df/README.md#L34-L36) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L15–17](https://github.com/jeremylongshore/walkie-talkie/blob/0b74f4d361022f51297896e2ef884c0ed5bfd0df/README.md#L15-L17) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 0 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 1/1 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 0 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R167: wasteland

Repository: [jeremylongshore/wasteland](https://github.com/jeremylongshore/wasteland). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **232**; head: `468ef42644f816afcf846eae534b1d57d8d3a3e0`. GitHub license metadata: **MIT**. Tree: **334 files**, complete. Observation: `2026-10-12T06:31:35Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evidence:** [`README.md` L52–54](https://github.com/jeremylongshore/wasteland/blob/468ef42644f816afcf846eae534b1d57d8d3a3e0/README.md#L52-L54) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 2 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 5 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 3/3 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R168

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R169: waygate-mcp

Repository: [jeremylongshore/waygate-mcp](https://github.com/jeremylongshore/waygate-mcp). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **25**; head: `f045782a952b565b43a70cf23442e1e5801eff61`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **171 files**, complete. Observation: `2026-10-12T06:31:36Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/ci.yml` L232–234](https://github.com/jeremylongshore/waygate-mcp/blob/f045782a952b565b43a70cf23442e1e5801eff61/.github/workflows/ci.yml#L232-L234) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/ci.yml` L232–234](https://github.com/jeremylongshore/waygate-mcp/blob/f045782a952b565b43a70cf23442e1e5801eff61/.github/workflows/ci.yml#L232-L234).
- **Release/changelog evidence:** 3 tags and 2 releases enumerated; 0 release records have lexical matches. [`RELEASE_NOTES_v2.1.0.md` L134–136](https://github.com/jeremylongshore/waygate-mcp/blob/f045782a952b565b43a70cf23442e1e5801eff61/RELEASE_NOTES_v2.1.0.md#L134-L136).
- **Verification scope:** 5/5 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 2 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R170

Visibility: **private**, verified with `gh repo view --json visibility`. Identity, SHA, count, license, paths and findings are available in the matching owner-annex row; they are withheld from this public projection under the lab disclosure policy.

### A1-R171: wild

Repository: [jeremylongshore/wild](https://github.com/jeremylongshore/wild). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **115**; head: `ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2`. GitHub license metadata: **MIT**. Tree: **650 files**, complete. Observation: `2026-10-12T06:31:37Z`.

- **Trace:** [`.github/workflows/minimax-review.yml` L138–140](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/.github/workflows/minimax-review.yml#L138-L140) (workflow; lexical evidence, not an operational verdict).
- **Telemetry:** [`lib/wild/telemetry/analysis.rb` L3–5](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/lib/wild/telemetry/analysis.rb#L3-L5) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`lib/wild/telemetry/analysis.rb` L40–42](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/lib/wild/telemetry/analysis.rb#L40-L42) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh` L2–4](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/.audit-harness/scripts/emit-evidence.sh#L2-L4) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.audit-harness/CHANGELOG.md` L164–166](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/.audit-harness/CHANGELOG.md#L164-L166) (documentation-or-config; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L8–10](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/.github/workflows/minimax-review.yml#L8-L10).
- **Release/changelog evidence:** 0 tags and 0 releases enumerated; 0 release records have lexical matches. [`.audit-harness/CHANGELOG.md` L9–11](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/.audit-harness/CHANGELOG.md#L9-L11); [`CHANGELOG.md` L21–23](https://github.com/jeremylongshore/wild/blob/ac8a6b442b805ccd5aa0be3775d688f42dd3a6c2/CHANGELOG.md#L21-L23).
- **Verification scope:** 16/16 Contents requests returned HTTP 200; 125 other filename candidates remain uninspected. All 4 workflow paths and 4 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R172: wild-admin-tools-mcp

Repository: [jeremylongshore/wild-admin-tools-mcp](https://github.com/jeremylongshore/wild-admin-tools-mcp). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **34**; head: `0c647ee611b338fb5435d69abbd60362c20c6071`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **143 files**, complete. Observation: `2026-10-12T06:31:38Z`.

- **Trace:** [`000-docs/018-AT-ADEC-telemetry-emission-hook-interface.md` L135–137](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/000-docs/018-AT-ADEC-telemetry-emission-hook-interface.md#L135-L137) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`000-docs/018-AT-ADEC-telemetry-emission-hook-interface.md` L1–3](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/000-docs/018-AT-ADEC-telemetry-emission-hook-interface.md#L1-L3) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`CHANGELOG.md` L14–15](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/CHANGELOG.md#L14-L15) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/minimax-review.yml` L138–140](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/.github/workflows/minimax-review.yml#L138-L140) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L230–232](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/.github/workflows/minimax-review.yml#L230-L232) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L138–140](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/.github/workflows/minimax-review.yml#L138-L140).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L14–15](https://github.com/jeremylongshore/wild-admin-tools-mcp/blob/0c647ee611b338fb5435d69abbd60362c20c6071/CHANGELOG.md#L14-L15).
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R173: wild-capability-gate

Repository: [jeremylongshore/wild-capability-gate](https://github.com/jeremylongshore/wild-capability-gate). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **33**; head: `4992cef0a264f44cc0bd3aad81abb812ed08df8e`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **85 files**, complete. Observation: `2026-10-12T06:31:39Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`lib/wild/capability_gate/evaluator.rb` L17–19](https://github.com/jeremylongshore/wild-capability-gate/blob/4992cef0a264f44cc0bd3aad81abb812ed08df8e/lib/wild/capability_gate/evaluator.rb#L17-L19) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L146–148](https://github.com/jeremylongshore/wild-capability-gate/blob/4992cef0a264f44cc0bd3aad81abb812ed08df8e/.github/workflows/minimax-review.yml#L146-L148) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L96–98](https://github.com/jeremylongshore/wild-capability-gate/blob/4992cef0a264f44cc0bd3aad81abb812ed08df8e/.github/workflows/minimax-review.yml#L96-L98).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L23–25](https://github.com/jeremylongshore/wild-capability-gate/blob/4992cef0a264f44cc0bd3aad81abb812ed08df8e/CHANGELOG.md#L23-L25).
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 3 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R174: wild-gap-miner

Repository: [jeremylongshore/wild-gap-miner](https://github.com/jeremylongshore/wild-gap-miner). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **13**; head: `e54d66f3622daf57498ec3a7ee6b1c566fff6dc4`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **86 files**, complete. Observation: `2026-10-12T06:31:40Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`spec/support/telemetry_fixtures.rb` L3–5](https://github.com/jeremylongshore/wild-gap-miner/blob/e54d66f3622daf57498ec3a7ee6b1c566fff6dc4/spec/support/telemetry_fixtures.rb#L3-L5) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`lib/wild_gap_miner/scoring/priority_ranker.rb` L4–6](https://github.com/jeremylongshore/wild-gap-miner/blob/e54d66f3622daf57498ec3a7ee6b1c566fff6dc4/lib/wild_gap_miner/scoring/priority_ranker.rb#L4-L6) (source; lexical evidence, not an operational verdict).
- **Evidence:** [`spec/support/telemetry_fixtures.rb` L73–75](https://github.com/jeremylongshore/wild-gap-miner/blob/e54d66f3622daf57498ec3a7ee6b1c566fff6dc4/spec/support/telemetry_fixtures.rb#L73-L75) (source; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L6–8](https://github.com/jeremylongshore/wild-gap-miner/blob/e54d66f3622daf57498ec3a7ee6b1c566fff6dc4/.github/workflows/minimax-review.yml#L6-L8) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L6–8](https://github.com/jeremylongshore/wild-gap-miner/blob/e54d66f3622daf57498ec3a7ee6b1c566fff6dc4/.github/workflows/minimax-review.yml#L6-L8).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L29–31](https://github.com/jeremylongshore/wild-gap-miner/blob/e54d66f3622daf57498ec3a7ee6b1c566fff6dc4/CHANGELOG.md#L29-L31); [release `v0.1.0`](https://github.com/jeremylongshore/wild-gap-miner/releases/tag/v0.1.0).
- **Verification scope:** 9/9 Contents requests returned HTTP 200; 1 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R175: wild-hook-ops

Repository: [jeremylongshore/wild-hook-ops](https://github.com/jeremylongshore/wild-hook-ops). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **13**; head: `f90ad3beca86b1f290318467a963f0ee91e87300`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **70 files**, complete. Observation: `2026-10-12T06:31:41Z`.

- **Trace:** [`.github/workflows/minimax-review.yml` L123–125](https://github.com/jeremylongshore/wild-hook-ops/blob/f90ad3beca86b1f290318467a963f0ee91e87300/.github/workflows/minimax-review.yml#L123-L125) (workflow; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L225–227](https://github.com/jeremylongshore/wild-hook-ops/blob/f90ad3beca86b1f290318467a963f0ee91e87300/.github/workflows/minimax-review.yml#L225-L227) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L217–219](https://github.com/jeremylongshore/wild-hook-ops/blob/f90ad3beca86b1f290318467a963f0ee91e87300/.github/workflows/minimax-review.yml#L217-L219) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L13–15](https://github.com/jeremylongshore/wild-hook-ops/blob/f90ad3beca86b1f290318467a963f0ee91e87300/.github/workflows/minimax-review.yml#L13-L15) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L13–15](https://github.com/jeremylongshore/wild-hook-ops/blob/f90ad3beca86b1f290318467a963f0ee91e87300/.github/workflows/minimax-review.yml#L13-L15).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R176: wild-permission-analyzer

Repository: [jeremylongshore/wild-permission-analyzer](https://github.com/jeremylongshore/wild-permission-analyzer). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **14**; head: `561da62837363f52939a11e049d5b516bd71fbb1`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **74 files**, complete. Observation: `2026-10-12T06:31:41Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L111–113](https://github.com/jeremylongshore/wild-permission-analyzer/blob/561da62837363f52939a11e049d5b516bd71fbb1/.github/workflows/minimax-review.yml#L111-L113) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L127–129](https://github.com/jeremylongshore/wild-permission-analyzer/blob/561da62837363f52939a11e049d5b516bd71fbb1/.github/workflows/minimax-review.yml#L127-L129) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L111–113](https://github.com/jeremylongshore/wild-permission-analyzer/blob/561da62837363f52939a11e049d5b516bd71fbb1/.github/workflows/minimax-review.yml#L111-L113).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L33–35](https://github.com/jeremylongshore/wild-permission-analyzer/blob/561da62837363f52939a11e049d5b516bd71fbb1/CHANGELOG.md#L33-L35).
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R177: wild-rails-safe-introspection-mcp

Repository: [jeremylongshore/wild-rails-safe-introspection-mcp](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **57**; head: `f4bddf72c2565ffe5be246c747c190c726cc2bec`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **114 files**, complete. Observation: `2026-10-12T06:31:42Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`CHANGELOG.md` L48–50](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/blob/f4bddf72c2565ffe5be246c747c190c726cc2bec/CHANGELOG.md#L48-L50) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** [`.github/workflows/minimax-review.yml` L168–170](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/blob/f4bddf72c2565ffe5be246c747c190c726cc2bec/.github/workflows/minimax-review.yml#L168-L170) (workflow; lexical evidence, not an operational verdict).
- **Evaluation:** [`.github/workflows/minimax-review.yml` L120–122](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/blob/f4bddf72c2565ffe5be246c747c190c726cc2bec/.github/workflows/minimax-review.yml#L120-L122) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L215–217](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/blob/f4bddf72c2565ffe5be246c747c190c726cc2bec/.github/workflows/minimax-review.yml#L215-L217) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L120–122](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/blob/f4bddf72c2565ffe5be246c747c190c726cc2bec/.github/workflows/minimax-review.yml#L120-L122).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L26–28](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/blob/f4bddf72c2565ffe5be246c747c190c726cc2bec/CHANGELOG.md#L26-L28); [release `v0.1.0`](https://github.com/jeremylongshore/wild-rails-safe-introspection-mcp/releases/tag/v0.1.0).
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R178: wild-session-telemetry

Repository: [jeremylongshore/wild-session-telemetry](https://github.com/jeremylongshore/wild-session-telemetry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **40**; head: `14bd29ad374e51e2bad1250e99306a847f890699`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **80 files**, complete. Observation: `2026-10-12T06:31:43Z`.

- **Trace:** [`README.md` L76–78](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/README.md#L76-L78) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** [`lib/wild_session_telemetry.rb` L3–5](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/lib/wild_session_telemetry.rb#L3-L5) (source; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L63–65](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/README.md#L63-L65) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L12–14](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/.github/workflows/minimax-review.yml#L12-L14) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L7–9](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/.github/workflows/minimax-review.yml#L7-L9) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L3–5](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/.github/workflows/minimax-review.yml#L3-L5).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L44–46](https://github.com/jeremylongshore/wild-session-telemetry/blob/14bd29ad374e51e2bad1250e99306a847f890699/CHANGELOG.md#L44-L46); [release `v0.1.0`](https://github.com/jeremylongshore/wild-session-telemetry/releases/tag/v0.1.0).
- **Verification scope:** 7/7 Contents requests returned HTTP 200; 28 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R179: wild-skillops-registry

Repository: [jeremylongshore/wild-skillops-registry](https://github.com/jeremylongshore/wild-skillops-registry). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **14**; head: `4645f079fe70b4b14026395ee99f96671db68eb2`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **77 files**, complete. Observation: `2026-10-12T06:31:44Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`.github/workflows/minimax-review.yml` L92–94](https://github.com/jeremylongshore/wild-skillops-registry/blob/4645f079fe70b4b14026395ee99f96671db68eb2/.github/workflows/minimax-review.yml#L92-L94) (workflow; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L101–103](https://github.com/jeremylongshore/wild-skillops-registry/blob/4645f079fe70b4b14026395ee99f96671db68eb2/.github/workflows/minimax-review.yml#L101-L103) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L203–205](https://github.com/jeremylongshore/wild-skillops-registry/blob/4645f079fe70b4b14026395ee99f96671db68eb2/.github/workflows/minimax-review.yml#L203-L205) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L151–153](https://github.com/jeremylongshore/wild-skillops-registry/blob/4645f079fe70b4b14026395ee99f96671db68eb2/.github/workflows/minimax-review.yml#L151-L153) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L92–94](https://github.com/jeremylongshore/wild-skillops-registry/blob/4645f079fe70b4b14026395ee99f96671db68eb2/.github/workflows/minimax-review.yml#L92-L94).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 6/6 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 3 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R180: wild-test-flake-forensics

Repository: [jeremylongshore/wild-test-flake-forensics](https://github.com/jeremylongshore/wild-test-flake-forensics). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **14**; head: `61deece4bd8fb5a8e80871e993c19b27c043a011`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **80 files**, complete. Observation: `2026-10-12T06:31:44Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L135–137](https://github.com/jeremylongshore/wild-test-flake-forensics/blob/61deece4bd8fb5a8e80871e993c19b27c043a011/.github/workflows/minimax-review.yml#L135-L137) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L199–201](https://github.com/jeremylongshore/wild-test-flake-forensics/blob/61deece4bd8fb5a8e80871e993c19b27c043a011/.github/workflows/minimax-review.yml#L199-L201) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L135–137](https://github.com/jeremylongshore/wild-test-flake-forensics/blob/61deece4bd8fb5a8e80871e993c19b27c043a011/.github/workflows/minimax-review.yml#L135-L137).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L33–35](https://github.com/jeremylongshore/wild-test-flake-forensics/blob/61deece4bd8fb5a8e80871e993c19b27c043a011/CHANGELOG.md#L33-L35).
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R181: wild-transcript-pipeline

Repository: [jeremylongshore/wild-transcript-pipeline](https://github.com/jeremylongshore/wild-transcript-pipeline). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **12**; head: `945ac662156a5ef8634c85bffaae75b9c1f6ef2a`. GitHub license metadata: **NOASSERTION (GitHub did not identify an SPDX license)**. Tree: **71 files**, complete. Observation: `2026-10-12T06:31:45Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** [`README.md` L18–20](https://github.com/jeremylongshore/wild-transcript-pipeline/blob/945ac662156a5ef8634c85bffaae75b9c1f6ef2a/README.md#L18-L20) (documentation-or-config; lexical evidence, not an operational verdict).
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`.github/workflows/minimax-review.yml` L131–133](https://github.com/jeremylongshore/wild-transcript-pipeline/blob/945ac662156a5ef8634c85bffaae75b9c1f6ef2a/.github/workflows/minimax-review.yml#L131-L133) (workflow; lexical evidence, not an operational verdict).
- **Evidence:** [`.github/workflows/minimax-review.yml` L184–186](https://github.com/jeremylongshore/wild-transcript-pipeline/blob/945ac662156a5ef8634c85bffaae75b9c1f6ef2a/.github/workflows/minimax-review.yml#L184-L186) (workflow; lexical evidence, not an operational verdict).
- **Taxonomy:** [`.github/workflows/minimax-review.yml` L15–17](https://github.com/jeremylongshore/wild-transcript-pipeline/blob/945ac662156a5ef8634c85bffaae75b9c1f6ef2a/.github/workflows/minimax-review.yml#L15-L17) (workflow; lexical evidence, not an operational verdict).
- **Related workflow references:** [`.github/workflows/minimax-review.yml` L15–17](https://github.com/jeremylongshore/wild-transcript-pipeline/blob/945ac662156a5ef8634c85bffaae75b9c1f6ef2a/.github/workflows/minimax-review.yml#L15-L17).
- **Release/changelog evidence:** 1 tags and 1 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 4/4 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 2 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R182: x-bug-triage-plugin

Repository: [jeremylongshore/x-bug-triage-plugin](https://github.com/jeremylongshore/x-bug-triage-plugin). Visibility: **public**. Fork: **no**. Archived: **no**.

Observed default branch: `main`; reachable commits: **66**; head: `06f262b4150e08df087649bf63df77160de0f6e0`. GitHub license metadata: **MIT**. Tree: **129 files**, complete. Observation: `2026-10-12T06:31:46Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`README.md` L24–26](https://github.com/jeremylongshore/x-bug-triage-plugin/blob/06f262b4150e08df087649bf63df77160de0f6e0/README.md#L24-L26) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** [`README.md` L57–59](https://github.com/jeremylongshore/x-bug-triage-plugin/blob/06f262b4150e08df087649bf63df77160de0f6e0/README.md#L57-L59) (documentation-or-config; lexical evidence, not an operational verdict).
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 4 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 25 tags and 25 releases enumerated; 1 release records have lexical matches. [`CHANGELOG.md` L147–149](https://github.com/jeremylongshore/x-bug-triage-plugin/blob/06f262b4150e08df087649bf63df77160de0f6e0/CHANGELOG.md#L147-L149); [release `v0.1.0`](https://github.com/jeremylongshore/x-bug-triage-plugin/releases/tag/v0.1.0).
- **Verification scope:** 8/8 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 4 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R183: xireactor-brilliant

Repository: [jeremylongshore/xireactor-brilliant](https://github.com/jeremylongshore/xireactor-brilliant). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **7**; head: `574ca31637370204a5c1c84ca0618a65399d811e`. GitHub license metadata: **Apache-2.0**. Tree: **78 files**, complete. Observation: `2026-10-12T06:31:46Z`.

- **Trace:** no public positive reference in the inspected sample; absence is **not established**.
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** [`README.md` L43–45](https://github.com/jeremylongshore/xireactor-brilliant/blob/574ca31637370204a5c1c84ca0618a65399d811e/README.md#L43-L45) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evaluation:** [`README.md` L3–5](https://github.com/jeremylongshore/xireactor-brilliant/blob/574ca31637370204a5c1c84ca0618a65399d811e/README.md#L3-L5) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 1 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 2 tags and 0 releases enumerated; 0 release records have lexical matches. No publishable positive reference in the inspected release/changelog material.
- **Verification scope:** 2/2 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 1 workflow paths and 0 changelog paths were requested. 0 verified file references withheld from this projection.

### A1-R184: zcf

Repository: [jeremylongshore/zcf](https://github.com/jeremylongshore/zcf). Visibility: **public**. Fork: **yes**. Archived: **no**.

Observed default branch: `main`; reachable commits: **391**; head: `83390947ff22bcbb05e82d0766999ed7a42f6591`. GitHub license metadata: **MIT**. Tree: **710 files**, complete. Observation: `2026-10-12T06:31:47Z`.

- **Trace:** [`.bmad-core/tasks/trace-requirements.md` L3–5](https://github.com/jeremylongshore/zcf/blob/83390947ff22bcbb05e82d0766999ed7a42f6591/.bmad-core/tasks/trace-requirements.md#L3-L5) (documentation-or-config; lexical evidence, not an operational verdict).
- **Telemetry:** no public positive reference in the inspected sample; absence is **not established**.
- **Annotation:** no public positive reference in the inspected sample; absence is **not established**.
- **Evaluation:** [`CHANGELOG.md` L2291–2293](https://github.com/jeremylongshore/zcf/blob/83390947ff22bcbb05e82d0766999ed7a42f6591/CHANGELOG.md#L2291-L2293) (documentation-or-config; lexical evidence, not an operational verdict).
- **Evidence:** no public positive reference in the inspected sample; absence is **not established**.
- **Taxonomy:** no public positive reference in the inspected sample; absence is **not established**.
- **Related workflows:** no publishable lexical match among 3 inspected workflow paths; this does not establish behavior or absence.
- **Release/changelog evidence:** 81 tags and 0 releases enumerated; 0 release records have lexical matches. [`CHANGELOG.md` L2291–2293](https://github.com/jeremylongshore/zcf/blob/83390947ff22bcbb05e82d0766999ed7a42f6591/CHANGELOG.md#L2291-L2293).
- **Verification scope:** 8/8 Contents requests returned HTTP 200; 0 other filename candidates remain uninspected. All 3 workflow paths and 1 changelog paths were requested. 0 verified file references withheld from this projection.

## Acceptance and next action

Metadata and visibility cover every accessible owned repository in this census. Source references are verified at immutable commits, with sampling limits, restricted records and failed requests stated explicitly. Related workflows and release/changelog evidence are included per repository.

**Remaining work:** review the semantic relevance of lexical hits; resolve repository categories that have no confirmed source reference and any failed Contents requests; establish a durable restricted-annex disposition; obtain owner sign-off on this complete audit package. A1 remains in progress. A2 is a separate organization audit. A3 must not begin until both audits have the required owner sign-off. This draft does not satisfy that gate.
