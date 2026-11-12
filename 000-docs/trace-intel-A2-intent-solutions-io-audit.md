# A2 — Organization trace, evaluation and evidence audit

**Status: DRAFT — owner sign-off pending; A3 remains held.**

Bead: `bd_000-projects-h08j.8.2`. Organization: `intent-solutions-io`.
Observation period begins **2026-11-12T04:58:47.588228+00:00**; individual requests retain their own timestamps. This is source-presence discovery, not architecture selection, runtime qualification, deployment proof or adoption approval.

## Coverage and disclosure

The fully paginated authenticated census contains **43 repositories: 15 public and 28 private**. Active organization-admin membership and admin access to all 43 were observed. Counts reconcile exactly to the organization's reported public/private totals. The earlier October preflight contained 41; it is historical evidence, not the current census. No token or organization setting changed.

All 43 repositories have independently checked visibility, pinned default-branch HEAD and tree, and fully paginated tag/release enumeration. The complete trees contain **13881 blobs**, with no truncation. **1499 inspected files** have HTTP200 Contents receipts, decoded-content SHA256 and matching Git blob/tree identity. **3 category/path pairs** remain outside the inspected candidate set; **2 files** exceeded the 2 MB limit. Two inspected files are non-UTF-8: byte identity is verified, with no textual or line-level conclusion. “No positive reference” never asserts a missing capability.

Only permitted public repository identities and public pinned source links appear here. Fourteen public identities are disclosed; one API-public repository is additionally withheld by the existing publication policy. Each private repository has a randomly assigned opaque identifier; its metadata, source paths, workflow names, license and tags are confined to the owner annex and raw evidence in the ignored, access-restricted lab archive. No private-repository source excerpts appear in this projection. Per-repository acceptance data for all 43 is complete in that restricted annex, subject to the stated inspection limits.

## Method and limitations

- Census: `gh api --paginate --slurp 'orgs/intent-solutions-io/repos?type=all&per_page=100&sort=full_name'`, deduplicated by repository ID; membership and organization counts independently reconciled.
- Each repository's visibility was also checked with `gh repo view --json visibility`.
- HEAD was observed first. Ancestry count uses `/commits?sha=PINNED_SHA&per_page=1` and its last-page link. It counts commits reachable from that pinned default-branch SHA, **not every commit across all branches**.
- Recursive trees use pinned tree SHAs and explicitly check truncation; every referenced file is fetched at the pinned commit and checked against the tree's blob identity.
- Inspection includes keyword-named trace/telemetry/annotation/evaluation/evidence/taxonomy files within 2 MB, all workflow/changelog paths and root overview/license files and the organization profile README where present, plus up to three ranked code entrypoints per repository. Other filenames and source contents are not exhaustively reviewed.
- Category admission excludes language-type annotations, spell-check vocabulary, bare TRACE logging levels, shell eval and incidental words without category-specific context. Original lexical hits and exclusions remain in private receipts. Context filtering is not an exhaustive semantic review; representative implementations below received manual source review.
- Artifact-type labels separate authored-source lexical hits, tests/fixtures, vendored/generated tooling, workflow declarations and documentation. These labels do not prove correctness, execution, ownership of vendored work, or deployed integration. Representative behavior reviews below are narrower, explicit assessments.
- Tags and releases are completely paginated at observation time. Separate GitHub reads are **not one atomic snapshot**; refs and release text may change afterward. Raw request timestamps and page receipts are retained.
- Thirteen explicit organization/name discovery probes returned two HTTP200 and eleven HTTP404 responses. Exact requested names, canonical resolutions and statuses remain in the restricted annex. A 404 is an observed API result, not proof that a similarly named component is absent elsewhere or never existed.

## Representative reviewed public source behavior

- **buzz:** TraceContextLookup retrieves valid OpenTelemetry context from registered tracing spans; optional exporter configuration is documented separately. This is tracing integration code, not proof a production collector is receiving spans. [Pinned source, lines 44–76](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-relay/src/telemetry.rs#L44-L76).
- **buzz:** The benchmark adapter normalizes relay messages and preserves protocol tags in a versioned verifier-facing evidence structure; this is task-specific transcript evidence, not a universal trace schema. [Pinned source, lines 39–80](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/src/harbor_buzz_orchestra/evidence.py#L39-L80).
- **iam-bob-eino:** Execution records carry authorization, verification and content-hash fields; the JSONL sink opens append-only storage and resumes a prior hash chain. A hash chain is not, by itself, a signed Sigstore release receipt. [Pinned source, lines 38–110](https://github.com/intent-solutions-io/iam-bob-eino/blob/0d0a0f01242ef0fbbedb156e758971938b65065f/internal/evidence/evidence.go#L38-L110).
- **now-lms:** Evaluation helpers query learner course attempts and pass status. This is domain-specific learning assessment, not an agent-evaluation framework. [Pinned source, lines 24–65](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/now_lms/vistas/evaluation_helpers.py#L24-L65).
- **catalyst-onboarding-v2:** The management command requires an approval reference and releases eligible held collection actions inside transactions. This is application workflow evidence gating, not proof of a shared annotation backbone. [Pinned source, lines 23–79](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/assessments/management/commands/activate_evidence_collection.py#L23-L79).

## Repository evidence map

### A2-R001: .github

Repository: [intent-solutions-io/.github](https://github.com/intent-solutions-io/.github). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `b82af5d3e7951d85e39ea9e65cc24ee8278722a7`; branch `main`; reachable ancestry commits: **11** at `2026-11-12T05:00:33Z`. GitHub license metadata: **unclassified by GitHub (not a license grant)**. Complete tree: **12 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** [`profile/README.md:12](https://github.com/intent-solutions-io/.github/blob/b82af5d3e7951d85e39ea9e65cc24ee8278722a7/profile/README.md#L12) (documentation/configuration reference)
- **Evidence:** [`profile/README.md:51](https://github.com/intent-solutions-io/.github/blob/b82af5d3e7951d85e39ea9e65cc24ee8278722a7/profile/README.md#L51) (documentation/configuration reference)
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** none in complete pinned tree.
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 1 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R002: identity withheld by publication policy

API visibility is public. The existing public-surface policy additionally withholds this repository identity and related metadata; complete pinned evidence remains in the restricted owner annex. No scanner exception was introduced.

### A2-R003: buzz

Repository: [intent-solutions-io/buzz](https://github.com/intent-solutions-io/buzz). Visibility: **public**. Fork: **true**. Archived: **false**.

Pinned default-branch head: `0451adb3cb8154e05398d707d5aea16b48fbf6ba`; branch `main`; reachable ancestry commits: **2763** at `2026-11-12T05:00:32Z`. GitHub license metadata: **Apache-2.0**. Complete tree: **5421 blobs**.

- **Trace:** [`crates/buzz-relay/src/telemetry.rs:1](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-relay/src/telemetry.rs#L1) (source context reference; execution not established); [`crates/buzz-datastore-tracing/src/lib.rs:101](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-datastore-tracing/src/lib.rs#L101) (source context reference; execution not established); [`crates/buzz-datastore-tracing/tests/runtime.rs:1](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-datastore-tracing/tests/runtime.rs#L1) (test/fixture reference)
- **Telemetry:** [`crates/buzz-relay/src/telemetry.rs:1](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-relay/src/telemetry.rs#L1) (source context reference; execution not established); [`crates/buzz-datastore-tracing/src/lib.rs:72](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-datastore-tracing/src/lib.rs#L72) (source context reference; execution not established); [`crates/buzz-db/src/runtime/observability.rs:1602](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/crates/buzz-db/src/runtime/observability.rs#L1602) (source context reference; execution not established)
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** [`benchmarks/harbor-buzz-orchestra/scripts/benchmark.py:2](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/scripts/benchmark.py#L2) (source context reference; execution not established); [`benchmarks/harbor-buzz-orchestra/scripts/run_leaderboard.py:13](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/scripts/run_leaderboard.py#L13) (source context reference; execution not established); [`benchmarks/harbor-buzz-orchestra/forwarder/relay_forwarder.rs:1](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/forwarder/relay_forwarder.rs#L1) (source context reference; execution not established)
- **Evidence:** [`benchmarks/harbor-buzz-orchestra/src/harbor_buzz_orchestra/evidence.py:10](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/src/harbor_buzz_orchestra/evidence.py#L10) (source context reference; execution not established); [`benchmarks/harbor-buzz-orchestra/testbed/src/harbor_buzz_testbed/keys.py:1](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/testbed/src/harbor_buzz_testbed/keys.py#L1) (source context reference; execution not established); [`benchmarks/harbor-buzz-orchestra/src/harbor_buzz_orchestra/container_runtime.py:224](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/benchmarks/harbor-buzz-orchestra/src/harbor_buzz_orchestra/container_runtime.py#L224) (source context reference; execution not established)
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh:260](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.audit-harness/scripts/emit-evidence.sh#L260) (vendored/generated artifact; not independent implementation); [`.audit-harness/CHANGELOG.md:34](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.audit-harness/CHANGELOG.md#L34) (vendored/generated artifact; not independent implementation)
- **Actions files:** [`.github/workflows/_ci-clients.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/_ci-clients.yml); [`.github/workflows/_ci-desktop-macos.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/_ci-desktop-macos.yml); [`.github/workflows/_ci-desktop.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/_ci-desktop.yml); [`.github/workflows/_ci-relay.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/_ci-relay.yml); [`.github/workflows/_ci-rust.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/_ci-rust.yml); [`.github/workflows/_ci-security.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/_ci-security.yml); [`.github/workflows/auto-tag-on-release-pr-merge.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/auto-tag-on-release-pr-merge.yml); [`.github/workflows/benchmark-harbor.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/benchmark-harbor.yml); [`.github/workflows/ci.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/ci.yml); [`.github/workflows/codex-security-review.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/codex-security-review.yml); [`.github/workflows/desktop-release-cache-proof.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/desktop-release-cache-proof.yml); [`.github/workflows/desktop-release-candidate.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/desktop-release-candidate.yml); [`.github/workflows/docker.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/docker.yml); [`.github/workflows/fork-gates.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/fork-gates.yml); [`.github/workflows/helm-chart.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/helm-chart.yml); [`.github/workflows/linux-canary.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/linux-canary.yml); [`.github/workflows/macos-intel-canary.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/macos-intel-canary.yml); [`.github/workflows/mesh-lifecycle.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/mesh-lifecycle.yml); [`.github/workflows/minio-image.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/minio-image.yml); [`.github/workflows/mobile-release-candidate.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/mobile-release-candidate.yml); [`.github/workflows/promote-oss-desktop-release.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/promote-oss-desktop-release.yml); [`.github/workflows/push-gateway-helm-chart.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/push-gateway-helm-chart.yml); [`.github/workflows/release.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/release.yml); [`.github/workflows/signed-macos-canary.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/signed-macos-canary.yml); [`.github/workflows/sprig-image.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/sprig-image.yml); [`.github/workflows/sprig.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/sprig.yml); [`.github/workflows/staging-dev-relay-image.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/staging-dev-relay-image.yml); [`.github/workflows/windows-canary.yml`](https://github.com/intent-solutions-io/buzz/blob/0451adb3cb8154e05398d707d5aea16b48fbf6ba/.github/workflows/windows-canary.yml).
- **Tags/releases:** 146 tags and 0 releases, fully paginated. Tag names: `v0.5.0`, `v0.4.26`, `v0.4.25`, `v0.4.24`, `v0.4.23`, `v0.4.22`, `v0.4.21`, `v0.4.20`, `v0.4.19`, `v0.4.18`, `v0.4.17`, `v0.4.16`, `v0.4.15`, `v0.4.14`, `v0.4.13`. Additional names retained in owner annex.
- **Inspection:** 154 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R004: catalyst-onboarding-v2

Repository: [intent-solutions-io/catalyst-onboarding-v2](https://github.com/intent-solutions-io/catalyst-onboarding-v2). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `378e6796f3962b2cfdb7d0317786f0aeb371d900`; branch `main`; reachable ancestry commits: **187** at `2026-11-12T05:00:34Z`. GitHub license metadata: **Apache-2.0**. Complete tree: **741 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** [`000-docs/018-AT-DSGN-p3-evidence-assessment-specification.md:1157](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/000-docs/018-AT-DSGN-p3-evidence-assessment-specification.md#L1157) (documentation/configuration reference)
- **Evaluation:** [`.claude/agents/catalyst-minimax-evaluation.md:2](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/.claude/agents/catalyst-minimax-evaluation.md#L2) (documentation/configuration reference); [`000-docs/000-aars/020-AA-AACR-p3-evidence-assessment.md:47](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/000-docs/000-aars/020-AA-AACR-p3-evidence-assessment.md#L47) (documentation/configuration reference); [`000-docs/018-AT-DSGN-p3-evidence-assessment-specification.md:185](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/000-docs/018-AT-DSGN-p3-evidence-assessment-specification.md#L185) (documentation/configuration reference)
- **Evidence:** [`scripts/verify_image_attestation.sh:5](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/scripts/verify_image_attestation.sh#L5) (source context reference; execution not established); [`assessments/management/commands/activate_evidence_collection.py:1](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/assessments/management/commands/activate_evidence_collection.py#L1) (source context reference; execution not established); [`tests/test_evidence.py:1](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/tests/test_evidence.py#L1) (test/fixture reference)
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/browser.yml`](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/.github/workflows/browser.yml); [`.github/workflows/ci.yml`](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/.github/workflows/ci.yml); [`.github/workflows/image.yml`](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/.github/workflows/image.yml); [`.github/workflows/release.yml`](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/.github/workflows/release.yml); [`.github/workflows/targeted.yml`](https://github.com/intent-solutions-io/catalyst-onboarding-v2/blob/378e6796f3962b2cfdb7d0317786f0aeb371d900/.github/workflows/targeted.yml).
- **Tags/releases:** 1 tags and 1 releases, fully paginated. Tag names: `v0.1.0`.
- **Inspection:** 22 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R005: claude-code-plugins-plus

Repository: [intent-solutions-io/claude-code-plugins-plus](https://github.com/intent-solutions-io/claude-code-plugins-plus). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `a8cc64f12a69dae1759c89218181b48bdd205b8d`; branch `main`; reachable ancestry commits: **4** at `2026-11-12T05:00:30Z`. GitHub license metadata: **unclassified by GitHub (not a license grant)**. Complete tree: **2 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** none in complete pinned tree.
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 1 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R006: claude-code-slack-channel

Repository: [intent-solutions-io/claude-code-slack-channel](https://github.com/intent-solutions-io/claude-code-slack-channel). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `b550b16afee70aa4f2a4662eaee2f274a938200c`; branch `main`; reachable ancestry commits: **4** at `2026-11-12T05:00:30Z`. GitHub license metadata: **unclassified by GitHub (not a license grant)**. Complete tree: **2 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** none in complete pinned tree.
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 1 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R007: iam-bob-eino

Repository: [intent-solutions-io/iam-bob-eino](https://github.com/intent-solutions-io/iam-bob-eino). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `0d0a0f01242ef0fbbedb156e758971938b65065f`; branch `main`; reachable ancestry commits: **62** at `2026-11-12T05:00:35Z`. GitHub license metadata: **Apache-2.0**. Complete tree: **121 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** [`internal/cli/cli.go:23](https://github.com/intent-solutions-io/iam-bob-eino/blob/0d0a0f01242ef0fbbedb156e758971938b65065f/internal/cli/cli.go#L23) (source context reference; execution not established); [`internal/evidence/redact.go:6](https://github.com/intent-solutions-io/iam-bob-eino/blob/0d0a0f01242ef0fbbedb156e758971938b65065f/internal/evidence/redact.go#L6) (source context reference; execution not established); [`internal/cli/evidence_cmd.go:2](https://github.com/intent-solutions-io/iam-bob-eino/blob/0d0a0f01242ef0fbbedb156e758971938b65065f/internal/cli/evidence_cmd.go#L2) (source context reference; execution not established)
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/ci.yml`](https://github.com/intent-solutions-io/iam-bob-eino/blob/0d0a0f01242ef0fbbedb156e758971938b65065f/.github/workflows/ci.yml); [`.github/workflows/release.yml`](https://github.com/intent-solutions-io/iam-bob-eino/blob/0d0a0f01242ef0fbbedb156e758971938b65065f/.github/workflows/release.yml).
- **Tags/releases:** 3 tags and 3 releases, fully paginated. Tag names: `v0.1.0`, `v0.1.0-rc.2`, `v0.1.0-rc.1`.
- **Inspection:** 15 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R008: intent-demos

Repository: [intent-solutions-io/intent-demos](https://github.com/intent-solutions-io/intent-demos). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `e33921cbd68ae032c6658a7f393bc7b5bb26522d`; branch `main`; reachable ancestry commits: **36** at `2026-11-12T05:00:35Z`. GitHub license metadata: **unclassified by GitHub (not a license grant)**. Complete tree: **98 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** [`site/assets/project-evidence.json:3](https://github.com/intent-solutions-io/intent-demos/blob/e33921cbd68ae032c6658a7f393bc7b5bb26522d/site/assets/project-evidence.json#L3) (documentation/configuration reference); [`site/assets/screens/evals.webp.json:2](https://github.com/intent-solutions-io/intent-demos/blob/e33921cbd68ae032c6658a7f393bc7b5bb26522d/site/assets/screens/evals.webp.json#L2) (documentation/configuration reference)
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/ci.yml`](https://github.com/intent-solutions-io/intent-demos/blob/e33921cbd68ae032c6658a7f393bc7b5bb26522d/.github/workflows/ci.yml).
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 8 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R009: intent-doc-filing-solution

Repository: [intent-solutions-io/intent-doc-filing-solution](https://github.com/intent-solutions-io/intent-doc-filing-solution). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `f61599d88fe2dbecffaecb04f75f3c6f494fd0ba`; branch `main`; reachable ancestry commits: **8** at `2026-11-12T05:00:34Z`. GitHub license metadata: **MIT**. Complete tree: **15 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/ci.yml`](https://github.com/intent-solutions-io/intent-doc-filing-solution/blob/f61599d88fe2dbecffaecb04f75f3c6f494fd0ba/.github/workflows/ci.yml).
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 4 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R010: intent-eval-platform

Repository: [intent-solutions-io/intent-eval-platform](https://github.com/intent-solutions-io/intent-eval-platform). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `95213f33d73141a97386a77a2f255a59604f3b26`; branch `main`; reachable ancestry commits: **33** at `2026-11-12T05:00:32Z`. GitHub license metadata: **Apache-2.0**. Complete tree: **38 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** [`README.md:9](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/README.md#L9) (documentation/configuration reference); [`CHANGELOG.md:107](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/CHANGELOG.md#L107) (documentation/configuration reference)
- **Evidence:** [`README.md:48](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/README.md#L48) (documentation/configuration reference); [`CHANGELOG.md:78](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/CHANGELOG.md#L78) (documentation/configuration reference)
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/aggregate-changelog.yml`](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/.github/workflows/aggregate-changelog.yml); [`.github/workflows/codeql.yml`](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/.github/workflows/codeql.yml); [`.github/workflows/doc-quality.yml`](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/.github/workflows/doc-quality.yml); [`.github/workflows/ecosystem-drift.yml`](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/.github/workflows/ecosystem-drift.yml); [`.github/workflows/lint.yml`](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/.github/workflows/lint.yml); [`.github/workflows/typos.yml`](https://github.com/intent-solutions-io/intent-eval-platform/blob/95213f33d73141a97386a77a2f255a59604f3b26/.github/workflows/typos.yml).
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 9 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R011: irsb

Repository: [intent-solutions-io/irsb](https://github.com/intent-solutions-io/irsb). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `2960d26518ac0bd37ddebac83810c475462beb62`; branch `main`; reachable ancestry commits: **6** at `2026-11-12T05:00:30Z`. GitHub license metadata: **unclassified by GitHub (not a license grant)**. Complete tree: **2 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** [`README.md:27](https://github.com/intent-solutions-io/irsb/blob/2960d26518ac0bd37ddebac83810c475462beb62/README.md#L27) (documentation/configuration reference)
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** none in complete pinned tree.
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 1 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R012: learn-intent-solutions-hub

Repository: [intent-solutions-io/learn-intent-solutions-hub](https://github.com/intent-solutions-io/learn-intent-solutions-hub). Visibility: **public**. Fork: **false**. Archived: **true**.

Pinned default-branch head: `3d243fb67951caeeb4a66109f94b5ff2bc22e53a`; branch `main`; reachable ancestry commits: **8** at `2026-11-12T05:00:32Z`. GitHub license metadata: **Apache-2.0**. Complete tree: **31 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/ci.yml`](https://github.com/intent-solutions-io/learn-intent-solutions-hub/blob/3d243fb67951caeeb4a66109f94b5ff2bc22e53a/.github/workflows/ci.yml); [`.github/workflows/deploy.yml`](https://github.com/intent-solutions-io/learn-intent-solutions-hub/blob/3d243fb67951caeeb4a66109f94b5ff2bc22e53a/.github/workflows/deploy.yml); [`.github/workflows/release.yml`](https://github.com/intent-solutions-io/learn-intent-solutions-hub/blob/3d243fb67951caeeb4a66109f94b5ff2bc22e53a/.github/workflows/release.yml).
- **Tags/releases:** 3 tags and 2 releases, fully paginated. Tag names: `v0.3.0`, `v0.2.0`, `v0.1.0`.
- **Inspection:** 6 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R013: now-lms

Repository: [intent-solutions-io/now-lms](https://github.com/intent-solutions-io/now-lms). Visibility: **public**. Fork: **true**. Archived: **false**.

Pinned default-branch head: `a85195d56e16cbdd9589270a244dcb10be1cd8be`; branch `deploy/now-lms-fixed`; reachable ancestry commits: **720** at `2026-11-12T05:00:34Z`. GitHub license metadata: **Apache-2.0**. Complete tree: **887 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** [`.audit-harness/scripts/emit-evidence.sh:259](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.audit-harness/scripts/emit-evidence.sh#L259) (vendored/generated artifact; not independent implementation); [`.audit-harness/CHANGELOG.md:9](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.audit-harness/CHANGELOG.md#L9) (vendored/generated artifact; not independent implementation)
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** [`now_lms/vistas/evaluations.py:7](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/now_lms/vistas/evaluations.py#L7) (source context reference; execution not established); [`now_lms/vistas/evaluation_helpers.py:7](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/now_lms/vistas/evaluation_helpers.py#L7) (source context reference; execution not established); [`tests/test_evaluation_helpers.py:4](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/tests/test_evaluation_helpers.py#L4) (test/fixture reference)
- **Evidence:** [`.audit-harness/scripts/emit-evidence.sh:2](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.audit-harness/scripts/emit-evidence.sh#L2) (vendored/generated artifact; not independent implementation); [`.audit-harness/CHANGELOG.md:84](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.audit-harness/CHANGELOG.md#L84) (vendored/generated artifact; not independent implementation)
- **Taxonomy:** [`.audit-harness/scripts/emit-evidence.sh:260](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.audit-harness/scripts/emit-evidence.sh#L260) (vendored/generated artifact; not independent implementation); [`.audit-harness/CHANGELOG.md:149](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.audit-harness/CHANGELOG.md#L149) (vendored/generated artifact; not independent implementation)
- **Actions files:** [`.github/workflows/ai-code-review.yml`](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.github/workflows/ai-code-review.yml); [`.github/workflows/deploy-line-ci.yml`](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.github/workflows/deploy-line-ci.yml); [`.github/workflows/pypi.yml`](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.github/workflows/pypi.yml); [`.github/workflows/release.yml`](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.github/workflows/release.yml); [`.github/workflows/security-scans.yml`](https://github.com/intent-solutions-io/now-lms/blob/a85195d56e16cbdd9589270a244dcb10be1cd8be/.github/workflows/security-scans.yml).
- **Tags/releases:** 19 tags and 0 releases, fully paginated. Tag names: `v1.2.3`, `v1.2.2`, `v1.2.1`, `v1.1.8`, `v1.1.7`, `v1.1.7.post1`, `v1.1.6`, `v1.1.5`, `v1.1.4`, `v1.1.3`, `v1.1.2`, `v1.1.1`, `v1.1.0`, `v1.0.5`, `v1.0.4`. Additional names retained in owner annex.
- **Inspection:** 21 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R014: omarchy-plugins

Repository: [intent-solutions-io/omarchy-plugins](https://github.com/intent-solutions-io/omarchy-plugins). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `09b6927b6a74bd3ac15332ee3473f494664a3b37`; branch `main`; reachable ancestry commits: **142** at `2026-11-12T05:00:30Z`. GitHub license metadata: **MIT**. Complete tree: **218 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** no positive reference in inspected material; feature absence is not established.
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** no positive reference in inspected material; feature absence is not established.
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/deploy-site.yml`](https://github.com/intent-solutions-io/omarchy-plugins/blob/09b6927b6a74bd3ac15332ee3473f494664a3b37/.github/workflows/deploy-site.yml); [`.github/workflows/refresh-metrics.yml`](https://github.com/intent-solutions-io/omarchy-plugins/blob/09b6927b6a74bd3ac15332ee3473f494664a3b37/.github/workflows/refresh-metrics.yml); [`.github/workflows/site-ci.yml`](https://github.com/intent-solutions-io/omarchy-plugins/blob/09b6927b6a74bd3ac15332ee3473f494664a3b37/.github/workflows/site-ci.yml); [`.github/workflows/worktree-hygiene.yml`](https://github.com/intent-solutions-io/omarchy-plugins/blob/09b6927b6a74bd3ac15332ee3473f494664a3b37/.github/workflows/worktree-hygiene.yml).
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 8 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

### A2-R015: wild-rails-ai-ops

Repository: [intent-solutions-io/wild-rails-ai-ops](https://github.com/intent-solutions-io/wild-rails-ai-ops). Visibility: **public**. Fork: **false**. Archived: **false**.

Pinned default-branch head: `4016b9c2bb5b1976196ac45dad1bf7603ecd618e`; branch `main`; reachable ancestry commits: **13** at `2026-11-12T05:00:31Z`. GitHub license metadata: **NOASSERTION**. Complete tree: **26 blobs**.

- **Trace:** no positive reference in inspected material; feature absence is not established.
- **Telemetry:** [`README.md:47](https://github.com/intent-solutions-io/wild-rails-ai-ops/blob/4016b9c2bb5b1976196ac45dad1bf7603ecd618e/README.md#L47) (documentation/configuration reference)
- **Annotation:** no positive reference in inspected material; feature absence is not established.
- **Evaluation:** [`README.md:46](https://github.com/intent-solutions-io/wild-rails-ai-ops/blob/4016b9c2bb5b1976196ac45dad1bf7603ecd618e/README.md#L46) (documentation/configuration reference)
- **Evidence:** no positive reference in inspected material; feature absence is not established.
- **Taxonomy:** no positive reference in inspected material; feature absence is not established.
- **Actions files:** [`.github/workflows/minimax-review.yml`](https://github.com/intent-solutions-io/wild-rails-ai-ops/blob/4016b9c2bb5b1976196ac45dad1bf7603ecd618e/.github/workflows/minimax-review.yml).
- **Tags/releases:** 0 tags and 0 releases, fully paginated. No tags observed.
- **Inspection:** 3 Contents-verified files; 0 uninspected category/path pairs; 0 files above the declared 2 MB limit.

## Restricted repository coverage

### A2-P001

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P002

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P003

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P004

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P005

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P006

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P007

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P008

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P009

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P010

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P011

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P012

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P013

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P014

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P015

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P016

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P017

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P018

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P019

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P020

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P021

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P022

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P023

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P024

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P025

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P026

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P027

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

### A2-P028

Private repository. Identity, commit history, license, source paths, Actions, tags and findings are withheld from this public projection. Complete pinned records are retained in the restricted owner annex.

## Disposition

A2 discovery does not authorize architecture changes or A3. Owner review must consider both this public projection and the restricted annex. Existing A1 draft/sign-off status remains independent. No service was deployed and no repository source was modified by this audit.
