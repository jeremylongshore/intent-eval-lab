# Harness-Hash Self-Pin Rollout — intent-eval-lab (platform-rollout child 1 of 4)

**Filing**: 020-AA-AACR-harness-hash-rollout-lab-2026-05-22.md
**Date**: 2026-05-22
**Author**: Jeremy Longshore (CTO + beads work; executed by Claude per CEO-mode delegation)
**Bead**: child of `iep-harness-hash-platform-rollout` (`bd_000-projects-g6zu`, P2)
**Sibling rollouts pending**: j-rig-binary-eval (next PR), intent-rollout-gate (deferred to M5)
**Upstream**: audit-harness v1.1.0 (PR jeremylongshore/audit-harness#36 / `iah-self-pin` / `bd_000-projects-itpl`)

---

## 1. What this AAR records

First rollout of the audit-harness self-pin pattern to the rest of the IEP platform. Pre-rollout state: only `intent-eval-core` had `.harness-hash` (default-pattern coverage of `.dependency-cruiser.cjs`). Audit-harness itself landed self-pinning in v1.1.0 via the `.harness-hash-extra-patterns` mechanism. This AAR closes that mechanism's first downstream adoption.

Pin scope for intent-eval-lab is deliberately tight — pin the load-bearing CI workflow definitions + the schema redirect stub (per DR 018), plus the vendored harness itself + the extras file. Frequently-edited content (DRs, Blueprints, glossary, AARs, INDEX) is intentionally NOT pinned.

## 2. What changed

| File | Change |
|---|---|
| `.audit-harness/` (NEW directory tree) | Vendored snapshot of audit-harness@846ff6a (v1.1.0). Contains scripts (arch-check.sh + bias-count.sh + crap-score.py + emit-evidence.sh + escape-scan.sh + gherkin-lint.sh + harness-hash.sh) + bin/audit-harness.js + LICENSE + NOTICE + README + CHANGELOG + VERSION + PROVENANCE (records source commit). |
| `scripts/audit-harness` (NEW) | Wrapper that dispatches into `.audit-harness/scripts/*`. Matches the canonical install.sh-produced wrapper layout. |
| `.harness-hash-extra-patterns` (NEW) | Pin scope declaration: `.github/workflows/*.yml`, `specs/evidence-bundle/v0.1.0-draft/schema/*.schema.json`, vendored harness + wrapper + the extras file itself. |
| `.harness-hash` (NEW) | 15-file pin manifest. Committed. |
| `.github/workflows/harness-hash-verify.yml` (NEW) | CI workflow runs `scripts/audit-harness verify` on every PR + push to main. Exit-2 hard-fails the PR. |
| THIS AAR | Closeout for the lab side of the platform rollout. |

## 3. Why this scope

**Pinned (15 files):**

- 4× `.github/workflows/*.yml` (`ci.yml`, `partner-name-guard.yml`, `schema-drift.yml`, `harness-hash-verify.yml`) — silent edits to these workflows are exactly the silent-policy-erosion failure mode the harness exists to prevent. A drive-by `|| true` added to the partner-name guard could ship partner names to public artifacts. A drive-by edit to schema-drift.yml could re-permit normative schema content in lab `specs/`.
- 1× `specs/evidence-bundle/v0.1.0-draft/schema/gate-result.schema.json` — the redirect stub locked by DR 018 § 6.4 Option α-minus. Per the DR, this file must stay redirect-shaped (carry `x-redirect` field, declare no normative predicate properties). The schema-drift workflow is the runtime check; this hash pin is the integrity floor underneath it.
- 9× `.audit-harness/scripts/*` + `.audit-harness/bin/audit-harness.js` — the vendored policy enforcement surface. Same rationale as audit-harness pinning its own scripts in PR #36.
- 1× `scripts/audit-harness` — the wrapper.
- 1× `.harness-hash-extra-patterns` — bootstrap pin so silent edits to the pin declarations can't subvert the mechanism.

**Intentionally NOT pinned:**

- Decision Records, Blueprints, Canonical Glossary, AARs, READMEs, INDEX, KNOWN-ISSUES.md, FUTURE.md — these are amended via formal process or churn frequently with intentional edits. Pinning would create constant re-init noise without an integrity payoff. The governance process (ISEDC, DR filing discipline) IS the integrity guarantee for these surfaces.
- Anything under `research/` — exploratory work in progress.
- The README's project-status sections — churn.

## 4. Vendor-snapshot vs install.sh

Pre-condition for the upstream install.sh: a tagged audit-harness release. v1.1.0 is the current main HEAD of audit-harness but no `v1.1.0` tag exists yet (the release workflow is gated on `iah-sigstore`, P1 open). install.sh hardcodes `refs/tags/${VERSION}.tar.gz`, so it cannot install v1.1.0 today.

This rollout vendors manually instead — `.audit-harness/PROVENANCE` records the source commit (`audit-harness@846ff6a` = post-PR-#36 main). When `iah-sigstore` lands and v1.1.0 is properly tagged + published, the lab can reinstall via `AUDIT_HARNESS_VERSION=v1.1.0 curl -sSL .../install.sh | bash` to switch from the manual vendor to the canonical install.

## 5. Re-init discipline

When a pinned file legitimately needs to change (deliberate CI workflow edit, schema upgrade after kernel `iec-E12` lands, harness re-vendor on upstream release):

```bash
# Make the legitimate edit
$EDITOR .github/workflows/<file>.yml

# Re-init the manifest
scripts/audit-harness init

# Commit BOTH the edit AND the regenerated manifest
git add <edited-file> .harness-hash
git commit -m "chore: <reason> + re-init .harness-hash"
```

The CI gate refuses PRs where a pinned file's bytes changed without a corresponding manifest update. This is the intended discipline — make the intent of the edit visible.

## 6. Verification

- `scripts/audit-harness --version`: returns `v1.1.0`.
- `scripts/audit-harness init`: pins 15 files cleanly.
- `scripts/audit-harness verify`: `harness-hash: OK`.
- `scripts/audit-harness list`: enumerates all 15 pinned files; exit 0.
- New `harness-hash-verify.yml` workflow lints clean (single job, single-step `scripts/audit-harness verify`).
- Partner-name guard against new files: clean (zero hits; pattern sourced from private umbrella).

### Expected escape-scan false positive on this PR

Running `bash .audit-harness/scripts/escape-scan.sh --staged` on this PR's staged diff returns REFUSE=1 CHALLENGE=3 because the diff includes the literal source of `.audit-harness/scripts/escape-scan.sh`, which contains the grep patterns it matches (`depcruise-disable`, `@ArchIgnore`, `skip_violations`, `ignore_imports`, the `test.skip` markers, etc.) as part of its detection logic. The script's pattern-match-against-staged-diff naturally matches the pattern definitions inside its own newly-added source.

This is a one-time vendoring-event false positive. Future PRs in this repo (where `.audit-harness/` stays unchanged) won't see those files in the diff, so the false positive won't recur. escape-scan is intentionally NOT wired into lab CI — only `harness-hash-verify` runs as a gate — so this false positive doesn't block the PR. Documented here for audit-trail transparency.

## 7. Bead lineage + sibling rollouts

| Bead | Status | Notes |
|---|---|---|
| `bd_000-projects-itpl` (`iah-self-pin`) | ✅ CLOSED (PR #36 / audit-harness@846ff6a) | Upstream — landed the extras-patterns mechanism |
| `bd_000-projects-g6zu` (`iep-harness-hash-platform-rollout`) | In-progress | Umbrella for the 4-repo rollout |
| **`intent-eval-lab` rollout (this AAR)** | **🟢 OPEN — PR pending** | First downstream adopter |
| j-rig-binary-eval rollout | ⏸ Pending | Next PR. j-rig already has a vendored `.audit-harness/` at v0.1.0; needs upgrade to v1.1.0-snapshot then same self-pin pattern. |
| intent-rollout-gate rollout | ⏸ DEFERRED | Repo is largely empty (action.yml stub only). M5 MVP gated on `iaj-E02b` closure; harness install lands when policy surface exists to pin. |

When all 4 children resolve (j-rig adopts + rollout-gate deferral note recorded), the umbrella `g6zu` can close.

## 8. Cross-references

- audit-harness v1.1.0 release notes — `audit-harness/CHANGELOG.md` `[v1.1.0] - 2026-05-22`
- audit-harness v1.1.0 AAR — `audit-harness/000-docs/005-AA-AACR-iah-self-pin-iep-P3-2026-05-22.md`
- IEP Convergence Debt Plan Priority 3 — `iep-P3-audit-harness-hardening` (`bd_000-projects-t3q8`)
- Gap-recheck observation that surfaced this work — `bd_000-projects-74m8` (CLOSED, status table in bd notes)
- DR 018 § 6.4 Option α-minus — `intent-eval-lab/000-docs/018-AT-DECR-isedc-council-session-5-jrig-reconciliation-2026-05-21.md`
- ISEDC Session 5 ratification of the schema-authority precedence that anchors the schema-drift pin

— Jeremy Longshore
intentsolutions.io
