# RR-LAND-041 — IEP rollback baseline (the safety net, established first)

**Date:** 2026-06-04
**Type:** RR-LAND (landing record — known-good-state manifest)
**Status:** ACTIVE baseline
**Authority:** PP-PLAN-040 § 8 ("IEP rollback baseline = safety net established first") + § 9 Epic 1
**Purpose:** capture a known-good point across all 6 Tier-1 IEP repos *before* any harness surgery,
so every comprehensive-audit change has a deterministic rollback target. This is the first claimable
deliverable of the PP-PLAN-040 epic tree.

> **How to refresh:** re-run the gather commands in § 5 and bump the date + a new `041`-successor doc
> (do **not** overwrite — prior signed work must stay reproducible against the baseline it was cut at).

---

## 1. BASELINES manifest (known-good `origin/main` snapshot)

Captured 2026-06-04 from `origin/main` of each repo (the integration trunk), with the latest tag
reachable on main and the live published artifact version.

| Repo | `origin/main` commit | Latest tag | Published artifact | Notes |
|---|---|---|---|---|
| `audit-harness` (intent-audit-harness) | `4f73146` | `v1.1.5` | `@intentsolutions/audit-harness@1.1.5` (npm) + PyPI `intent-audit-harness` + crates `intent-audit-harness` | **root dependency** — everyone vendors/deps it |
| `intent-eval-core` | `13f2388` | `v0.2.0` | `@intentsolutions/core@0.2.0` (npm, sigstore provenance) | canonical contracts kernel |
| `intent-eval-lab` | `d894883` | `v0.2.0` | (not an npm artifact — spec/methodology repo) | Phase A foundation + all DRs/blueprints |
| `j-rig-binary-eval` (GH: `j-rig-skill-binary-eval`) | `d3d641d` | `v1.1.0` | `@j-rig/*` **unpublished** (workspace-internal monorepo) | local FS dir is `j-rig-binary-eval` |
| `intent-rollout-gate` | `12cfa04` | `v0.0.1` | (GH Action; no npm artifact yet) | consumes `@j-rig/rollout-gate` once published |
| `intent-eval-dashboard` | `cba7b34` | (no tag) | (deployed app; no npm artifact) | renders Evidence Bundles |

**npm verification (2026-06-04):** `@intentsolutions/audit-harness` → `1.1.5`;
`@intentsolutions/core` → `0.2.0`; `@j-rig/{rollout-gate,core,cli}` → unpublished (expected —
they ship as a workspace monorepo, not yet released to npm).

---

## 2. Dependency edges (intra-ecosystem)

Edges measured from `package.json` deps + vendored-harness markers (`.audit-harness/`, `.harness-hash`).

```
audit-harness  (root — published @intentsolutions/audit-harness@1.1.5)
   ▲   ▲   ▲   ▲
   │   │   │   └── intent-eval-dashboard   (dep ^1.1.5  + dep @intentsolutions/core ^0.2.0)
   │   │   └────── j-rig-binary-eval        (vendored .audit-harness/ ; internal @j-rig/core,@j-rig/db = workspace:*)
   │   └────────── intent-eval-lab          (vendored .audit-harness/ + .harness-hash)
   └────────────── intent-eval-core         (dev-dep ^1.1.5 ; vendored .harness-hash)  ── publishes @intentsolutions/core@0.2.0
                                                                              ▲
                                                                              └── intent-eval-dashboard (dep ^0.2.0)

intent-rollout-gate  → (future) @j-rig/rollout-gate  [edge inactive — j-rig @j-rig/* not yet published]
```

**Topological order (forward / install / restore):** `audit-harness` → `intent-eval-core` →
{`intent-eval-lab`, `j-rig-binary-eval`, `intent-eval-dashboard`} → `intent-rollout-gate`.

**Reverse-topological order (rollback):** roll back leaves first
(`intent-rollout-gate`, `intent-eval-dashboard`) → mid (`j-rig-binary-eval`, `intent-eval-lab`,
`intent-eval-core`) → **root last** (`audit-harness`). Rolling back the root before its consumers
would leave dangling version pins.

---

## 3. Rollback recipe

### 3a. Per-repo git rollback to baseline

For any repo `<r>` whose `<sha>` is in the § 1 table:

```bash
cd /home/jeremy/000-projects/intent-eval-platform/<r>
git fetch origin --tags --quiet
git checkout -b rollback/<r>-baseline-2026-06-04 origin/main   # or: git reset --hard <sha> on a recovery branch
git checkout <sha>                                              # detached known-good point
# OR restore via the tag if the change to undo was post-tag:
git checkout <tag>
```

Never `reset --hard` a shared branch. Always cut a `rollback/*` branch from the baseline commit, fix
forward there, and PR. The baseline commit/tag is the *reference*, not a destination to force.

### 3b. Published-artifact rollback (npm)

A published version is immutable. To roll a *consumer* back to a known-good dependency:

```bash
# pin a consumer back to the baseline harness/core
cd <consumer-repo>
pnpm add -D @intentsolutions/audit-harness@1.1.5     # or @intentsolutions/core@0.2.0
git commit -am "chore: pin @intentsolutions/* to baseline (RR-LAND-041)"
```

If a *bad* harness/core gets published, do **not** unpublish — cut a patch release that reverts the
offending change and let Renovate/`ecosystem-sync` fan the fix out (PP-PLAN-040 § 2). Until the fix
publishes, consumers pin to the baseline version above.

### 3c. Vendored-harness rollback

For repos carrying a vendored copy (`intent-eval-lab`, `j-rig-binary-eval`, and `.harness-hash`
in core/dashboard):

```bash
cd <repo>
AUDIT_HARNESS_VERSION=v1.1.5 curl -sSL \
  https://raw.githubusercontent.com/jeremylongshore/intent-audit-harness/main/install.sh | bash
git checkout -- .harness-hash    # restore the pinned manifest if it was touched
```

---

## 4. Coherence check (run after any rollback)

```bash
# 1. Each repo's HEAD matches an intended baseline/recovery point
for r in audit-harness intent-eval-core intent-eval-lab j-rig-binary-eval intent-rollout-gate intent-eval-dashboard; do
  echo "$r: $(git -C $r rev-parse --short HEAD)"; done

# 2. Cross-repo installs/imports resolve
cd intent-eval-core      && pnpm install && pnpm run check
cd ../j-rig-binary-eval  && pnpm install && pnpm run check
cd ../intent-eval-dashboard && pnpm install && pnpm run build

# 3. Harness self-check in every vendored repo
for r in intent-eval-lab j-rig-binary-eval; do (cd $r && scripts/audit-harness verify); done

# 4. Consumer of @intentsolutions/core re-resolves the kernel import surface
node -e "require.resolve('@intentsolutions/core')" 2>/dev/null && echo "core resolves"
```

All four steps green = the ecosystem is back at a coherent known-good state.

---

## 5. How this manifest was gathered (reproducible)

```bash
cd /home/jeremy/000-projects/intent-eval-platform
for r in audit-harness intent-eval-core intent-eval-lab j-rig-binary-eval intent-rollout-gate intent-eval-dashboard; do
  git -C "$r" fetch origin main --tags --quiet
  printf "%-22s main=%s tag=%s\n" "$r" \
    "$(git -C "$r" rev-parse --short origin/main)" \
    "$(git -C "$r" describe --tags --abbrev=0 origin/main 2>/dev/null || echo none)"
done
for p in @intentsolutions/audit-harness @intentsolutions/core @j-rig/rollout-gate; do
  printf "%-30s %s\n" "$p" "$(npm view "$p" version 2>/dev/null || echo unpublished)"
done
```

---

## 6. Known drift flagged at baseline (advisory — not a blocker)

- **`intent-eval-dashboard`** carries both a stale `@intentsolutions/audit-harness: ^0.1.0` reference
  and the current `^1.1.5` across its manifests. Flagged for cleanup under the ecosystem-sync epic
  (PP-PLAN-040 § 9 Epic 8); not part of the baseline rollback target.
- **`intent-rollout-gate`** has no active intra-ecosystem npm edge yet — its `@j-rig/rollout-gate`
  consumption is gated on j-rig publishing `@j-rig/*` (DR-018 sequencing). Baseline records the
  inactive edge so the rollback graph is complete when it activates.

---

*Filed per Document Filing Standard v4.3. This is the known-good reference for PP-PLAN-040; refresh by
cutting a successor doc, never by overwriting.*
