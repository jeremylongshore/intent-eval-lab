#!/usr/bin/env python3
"""Detector-health composite dashboard (057-AT-SPEC; Gregg correction, 9k5h.13).

Leads with DETECTOR HEALTH — never a vanity green count that masks a dead
watcher. A drift table full of "ok" rows is meaningless if the watcher that
produces those rows stopped running three days ago; the verdict tile therefore
reports the health of the detection machinery FIRST, and the per-surface drift
table renders BELOW it.

Derives a composite health document from EXISTING committed state only (no
network, no new state of its own):

  specs/snapshots/.state.json               watcher-liveness state — last
                                            successful run + per-surface
                                            fetch_error_streaks
  specs/upstream-surface-registry.v1.json   registered + monitored surface
                                            counts -> coverage%
  specs/lineage/coverage-map.json           adopt / diverge / outstanding-
                                            trigger counts (054-AT-SPEC)
  specs/snapshots/.sha/<surface>.sha        drift baselines -> per-surface
                                            drift rows

Composite predicate (057-AT-SPEC): HEALTHY iff ALL of
  1. watcher-run-recent      last successful watcher run <= max_gap_hours ago
                             (26 — one daily cron + slack, same constant as
                             watcher-liveness.py). A null last-run (bootstrap)
                             FAILS: a watcher that has never proven life is
                             DEGRADED, never green.
  2. no-fetch-error-streaks  zero surfaces with fetch_error_streak >=
                             streak_threshold (3) — such a surface is
                             effectively unmonitored.
  3. coverage-at-target      monitored surfaces / registered surfaces at the
                             registry-declared target: 100% of registered
                             surfaces monitored.
Anything else = DEGRADED, with the FAILING condition(s) named first.

Outputs (both GENERATED; deterministic given the inputs + --now):
  specs/detector-health.json   machine document, carrying a sha256 fingerprint
                               of every source file consumed
  docs/detector-health.md      compact rendering — verdict tile first, drift
                               table below

--check fails when a committed output is stale vs the sources: it re-derives
at the COMMITTED evaluated_at, so mere passage of time never trips it — the
same pattern as lineage-log.py project-coverage --check. --self-test is
offline + fixture-driven (healthy / dead-watcher / streak / coverage-gap).

Stdlib only. Exit 0 = ok; 1 = check or self-test failure; 2 = usage error.

Usage:
  detector-health.py                # regenerate both outputs
  detector-health.py --check        # fail if a committed output is stale
  detector-health.py --self-test    # offline deterministic fixtures
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")
DEFAULT_STATE = os.path.join(REPO_ROOT, "specs", "snapshots", ".state.json")
DEFAULT_COVERAGE = os.path.join(REPO_ROOT, "specs", "lineage", "coverage-map.json")
DEFAULT_SHA_DIR = os.path.join(REPO_ROOT, "specs", "snapshots", ".sha")
DEFAULT_JSON_OUT = os.path.join(REPO_ROOT, "specs", "detector-health.json")
DEFAULT_MD_OUT = os.path.join(REPO_ROOT, "docs", "detector-health.md")

SPEC_DOC = "000-docs/057-AT-SPEC-detector-health-composite-dashboard-2026-06-12.md"
GENERATED_HEADER = (
    "GENERATED-DO-NOT-EDIT — composite detector-health document derived from committed state "
    "(watcher-liveness state + surface registry + lineage coverage map + drift baselines). "
    f"Regenerate: python3 scripts/detector-health.py. Normative spec: {SPEC_DOC}"
)

COND_WATCHER = "watcher-run-recent"
COND_STREAKS = "no-fetch-error-streaks"
COND_COVERAGE = "coverage-at-target"
CONDITION_ORDER = (COND_WATCHER, COND_STREAKS, COND_COVERAGE)


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _label(path: str, root: str) -> str:
    """Repo-relative label for a source path (committed JSON must never carry
    absolute paths); paths outside root (test fixtures) keep their own name."""
    abspath, absroot = os.path.abspath(path), os.path.abspath(root)
    if abspath.startswith(absroot + os.sep):
        return os.path.relpath(abspath, absroot)
    return path


def _load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ── Derivation (pure given inputs + now) ─────────────────────────────────────


def derive(
    registry_path: str,
    state_path: str,
    coverage_path: str,
    sha_dir: str,
    now: datetime,
    label_root: str,
) -> dict:
    registry = _load_json(registry_path)
    state = _load_json(state_path)
    coverage_map = _load_json(coverage_path)

    inputs = {
        _label(registry_path, label_root): _sha256_file(registry_path),
        _label(state_path, label_root): _sha256_file(state_path),
        _label(coverage_path, label_root): _sha256_file(coverage_path),
    }

    reg_surfaces = sorted(registry.get("surfaces", []), key=lambda s: s["name"])
    total = len(reg_surfaces)
    monitored = sum(1 for s in reg_surfaces if s.get("monitored"))

    state_surfaces = state.get("surfaces", {}) or {}
    max_gap = float(state.get("max_gap_hours", 26))
    threshold = int(state.get("streak_threshold", 3))
    last_run = state.get("last_run_utc")

    cov_surfaces = coverage_map.get("surfaces", {}) or {}
    adopted = sum(1 for s in cov_surfaces.values() if s.get("adopted"))
    outstanding = sum(len(s.get("divergences_outstanding", [])) for s in cov_surfaces.values())
    fired = sum(len(s.get("convergence_fired", [])) for s in cov_surfaces.values())

    # Condition 1 — the watcher itself ran recently (the dead-watcher guard).
    if last_run:
        gap_hours: float | None = round((now - _parse_iso(last_run)).total_seconds() / 3600.0, 1)
        watcher_pass = gap_hours <= max_gap
        watcher_detail = f"last successful watcher run {last_run} was {gap_hours}h ago (max gap {max_gap:g}h)"
    else:
        gap_hours = None
        watcher_pass = False
        watcher_detail = (
            "no successful watcher run recorded — bootstrap state is not proof of life; "
            "an unproven watcher is DEGRADED, never green"
        )

    # Condition 2 — no surface is effectively unmonitored via error streaks.
    streak_rows = sorted(
        (name, int(rec.get("fetch_error_streak", 0)))
        for name, rec in state_surfaces.items()
        if int(rec.get("fetch_error_streak", 0)) >= threshold
    )
    streaks_pass = not streak_rows
    if streaks_pass:
        streaks_detail = f"all {len(state_surfaces)} tracked surfaces under the streak threshold ({threshold})"
    else:
        streaks_detail = f"effectively unmonitored (fetch_error_streak >= {threshold}): " + ", ".join(
            f"{name} (streak={streak})" for name, streak in streak_rows
        )

    # Condition 3 — coverage at the registry-declared target (100% of registered).
    coverage_pct = round(100.0 * monitored / total, 1) if total else 0.0
    target_pct = 100.0
    coverage_pass = total > 0 and monitored == total
    if total == 0:
        coverage_detail = "registry declares zero surfaces — nothing is monitored"
    else:
        coverage_detail = (
            f"{monitored}/{total} registered surfaces monitored "
            f"({coverage_pct}% of target {target_pct:g}%)"
        )

    conditions = {
        COND_WATCHER: {
            "pass": watcher_pass,
            "detail": watcher_detail,
            "last_run_utc": last_run,
            "gap_hours": gap_hours,
            "max_gap_hours": max_gap,
        },
        COND_STREAKS: {
            "pass": streaks_pass,
            "detail": streaks_detail,
            "streak_threshold": threshold,
            "surfaces_at_or_over_threshold": [
                {"surface": name, "fetch_error_streak": streak} for name, streak in streak_rows
            ],
        },
        COND_COVERAGE: {
            "pass": coverage_pass,
            "detail": coverage_detail,
            "registered_surfaces": total,
            "monitored_surfaces": monitored,
            "coverage_pct": coverage_pct,
            "target_pct": target_pct,
        },
    }
    failing = [c for c in CONDITION_ORDER if not conditions[c]["pass"]]

    drift_rows = []
    for surface in reg_surfaces:
        name = surface["name"]
        sha_path = os.path.join(sha_dir, f"{name}.sha")
        baseline = None
        if os.path.exists(sha_path):
            with open(sha_path, encoding="utf-8") as fh:
                baseline = fh.read().strip()
            inputs[_label(sha_path, label_root)] = _sha256_file(sha_path)
        rec = state_surfaces.get(name, {})
        cov = cov_surfaces.get(name, {})
        drift_rows.append(
            {
                "surface": name,
                "contract": surface.get("contract"),
                "authority_tier": surface.get("authority_tier"),
                "monitored": bool(surface.get("monitored")),
                "baseline_sha256": baseline,
                "fetch_error_streak": int(rec.get("fetch_error_streak", 0)),
                "last_ok_utc": rec.get("last_ok_utc"),
                "adopted": bool(cov.get("adopted")),
                "divergences_outstanding": len(cov.get("divergences_outstanding", [])),
            }
        )

    return {
        "_generated": GENERATED_HEADER,
        "health_version": "detector-health/v1",
        "evaluated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": "HEALTHY" if not failing else "DEGRADED",
        "failing_conditions": failing,
        "conditions": conditions,
        "lineage": {
            "surfaces_adopted": adopted,
            "divergences_outstanding": outstanding,
            "convergence_triggers_fired": fired,
        },
        "inputs": inputs,
        "drift_rows": drift_rows,
    }


# ── Rendering ────────────────────────────────────────────────────────────────


def render_json(doc: dict) -> str:
    return json.dumps(doc, indent=2, sort_keys=True) + "\n"


def render_markdown(doc: dict) -> str:
    lines = [f"<!-- {GENERATED_HEADER} -->", "", "# Detector health", ""]
    lines.append(f"## Verdict: {doc['verdict']}")
    lines.append("")
    if doc["failing_conditions"]:
        lines.append("Failing condition(s) first:")
    else:
        lines.append("All composite-predicate conditions pass:")
    lines.append("")
    ordered = list(doc["failing_conditions"]) + [
        c for c in CONDITION_ORDER if c not in doc["failing_conditions"]
    ]
    for cond in ordered:
        c = doc["conditions"][cond]
        marker = "ok" if c["pass"] else "**FAIL**"
        lines.append(f"- {marker} `{cond}` — {c['detail']}")
    lines.append("")
    lineage = doc["lineage"]
    lines.append(
        f"Lineage: {lineage['surfaces_adopted']} surfaces adopted, "
        f"{lineage['divergences_outstanding']} divergences outstanding, "
        f"{lineage['convergence_triggers_fired']} convergence triggers fired. "
        f"Evaluated at {doc['evaluated_at']}."
    )
    lines.append("")
    lines.append("## Drift table (per registered surface)")
    lines.append("")
    lines.append("| Surface | Contract | Monitored | Baseline | Error streak | Adopted | Divergences outstanding |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in doc["drift_rows"]:
        baseline = f"`{row['baseline_sha256'][:12]}…`" if row["baseline_sha256"] else "MISSING"
        lines.append(
            f"| {row['surface']} | {row['contract']} | "
            f"{'yes' if row['monitored'] else 'NO'} | {baseline} | "
            f"{row['fetch_error_streak']} | {'yes' if row['adopted'] else '—'} | "
            f"{row['divergences_outstanding']} |"
        )
    return "\n".join(lines) + "\n"


# ── Commands ─────────────────────────────────────────────────────────────────


def _derive_from_args(args: argparse.Namespace, now: datetime) -> dict:
    return derive(args.registry, args.state, args.coverage_map, args.sha_dir, now, args.label_root)


def cmd_generate(args: argparse.Namespace) -> int:
    now = _parse_iso(args.now) if args.now else datetime.now(timezone.utc)
    doc = _derive_from_args(args, now)
    for out_path, content in ((args.json_out, render_json(doc)), (args.md_out, render_markdown(doc))):
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(content)
    failing = ", ".join(doc["failing_conditions"]) or "none"
    print(
        f"detector-health: wrote {args.json_out} + {args.md_out} — "
        f"verdict {doc['verdict']} (failing: {failing})."
    )
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    if not os.path.exists(args.json_out):
        print(f"detector-health --check: FAIL — committed output missing: {args.json_out}")
        return 1
    try:
        with open(args.json_out, encoding="utf-8") as fh:
            committed_json = fh.read()
        evaluated_at = json.loads(committed_json)["evaluated_at"]
        now = _parse_iso(evaluated_at)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"detector-health --check: FAIL — committed JSON unreadable ({exc})")
        return 1

    doc = _derive_from_args(args, now)
    stale = []
    if committed_json != render_json(doc):
        stale.append(args.json_out)
    if not os.path.exists(args.md_out):
        stale.append(f"{args.md_out} (missing)")
    else:
        with open(args.md_out, encoding="utf-8") as fh:
            if fh.read() != render_markdown(doc):
                stale.append(args.md_out)
    if stale:
        print(
            "detector-health --check: STALE — committed output(s) do not match a fresh "
            f"derivation from the current sources (re-derived at the committed evaluated_at {evaluated_at}):"
        )
        for path in stale:
            print(f"  - {path}")
        print("The dashboard is a DERIVED view — never hand-edit it. Regenerate: python3 scripts/detector-health.py")
        return 1
    print(f"detector-health --check: OK — committed dashboard is fresh (verdict {doc['verdict']}).")
    return 0


# ── Deterministic offline self-test ──────────────────────────────────────────

FIXTURE_NOW = "2026-06-12T12:00:00Z"


def _write_fixture(
    tmp: str,
    *,
    last_run: str | None = "2026-06-12T09:00:00Z",
    streaks: dict[str, int] | None = None,
    monitored: tuple[bool, bool, bool] = (True, True, True),
    baselines: tuple[bool, bool, bool] = (True, True, True),
) -> argparse.Namespace:
    names = ("fixture-a", "fixture-b", "fixture-c")
    registry = {
        "registry_version": "upstream-surface-registry/v1",
        "surfaces": [
            {"name": n, "contract": "contract-x", "authority_tier": "official-spec", "monitored": m}
            for n, m in zip(names, monitored)
        ],
    }
    state = {
        "state_version": "watcher-liveness/v1",
        "last_run_utc": last_run,
        "max_gap_hours": 26,
        "streak_threshold": 3,
        "surfaces": {
            n: {"fetch_error_streak": (streaks or {}).get(n, 0), "last_ok_utc": last_run} for n in names
        },
    }
    coverage = {
        "surfaces": {
            "fixture-a": {
                "adopted": {"at": "2026-06-01T00:00:00Z", "event_id": 1},
                "divergences_outstanding": [{"subject": "contract-x/extra"}],
                "convergence_fired": [],
            },
            "fixture-b": {
                "adopted": {"at": "2026-06-01T00:00:00Z", "event_id": 2},
                "divergences_outstanding": [],
                "convergence_fired": [{"subject": "contract-x/old"}],
            },
        }
    }
    paths = {
        "registry": os.path.join(tmp, "registry.json"),
        "state": os.path.join(tmp, "state.json"),
        "coverage_map": os.path.join(tmp, "coverage-map.json"),
        "sha_dir": os.path.join(tmp, "sha"),
        "json_out": os.path.join(tmp, "out", "detector-health.json"),
        "md_out": os.path.join(tmp, "out", "detector-health.md"),
    }
    for path, payload in (
        (paths["registry"], registry),
        (paths["state"], state),
        (paths["coverage_map"], coverage),
    ):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
            fh.write("\n")
    os.makedirs(paths["sha_dir"], exist_ok=True)
    for n, has_baseline in zip(names, baselines):
        if has_baseline:
            with open(os.path.join(paths["sha_dir"], f"{n}.sha"), "w", encoding="utf-8") as fh:
                fh.write(hashlib.sha256(n.encode()).hexdigest() + "\n")
    return argparse.Namespace(now=FIXTURE_NOW, label_root=tmp, **paths)


def cmd_self_test() -> int:
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    def quiet_derive(ns: argparse.Namespace) -> dict:
        return _derive_from_args(ns, _parse_iso(ns.now))

    with tempfile.TemporaryDirectory() as tmp:
        # 1. Healthy: recent run, no streaks, full coverage.
        os.makedirs(os.path.join(tmp, "healthy"))
        ns = _write_fixture(os.path.join(tmp, "healthy"))
        doc = quiet_derive(ns)
        check("healthy fixture -> HEALTHY", doc["verdict"] == "HEALTHY" and doc["failing_conditions"] == [])
        check(
            "healthy fixture: every source fingerprinted (3 docs + 3 baselines)",
            len(doc["inputs"]) == 6 and all(len(v) == 64 for v in doc["inputs"].values()),
        )
        check(
            "fingerprint labels are fixture-relative (no absolute paths)",
            all(not k.startswith("/") for k in doc["inputs"]),
        )
        check(
            "lineage counts derived from the coverage map",
            doc["lineage"] == {"surfaces_adopted": 2, "divergences_outstanding": 1, "convergence_triggers_fired": 1},
        )

        # 2. Dead watcher (> 26h since last run).
        os.makedirs(os.path.join(tmp, "dead"))
        ns_dead = _write_fixture(os.path.join(tmp, "dead"), last_run="2026-06-10T00:00:00Z")
        doc = quiet_derive(ns_dead)
        check(
            "dead watcher (60h) -> DEGRADED naming watcher-run-recent",
            doc["verdict"] == "DEGRADED" and doc["failing_conditions"] == [COND_WATCHER],
        )
        check("dead watcher: gap_hours computed", doc["conditions"][COND_WATCHER]["gap_hours"] == 60.0)

        # 3. Never ran (bootstrap null) is DEGRADED, not green.
        os.makedirs(os.path.join(tmp, "never"))
        ns_never = _write_fixture(os.path.join(tmp, "never"), last_run=None)
        doc = quiet_derive(ns_never)
        check(
            "null last-run (bootstrap) -> DEGRADED naming watcher-run-recent",
            doc["verdict"] == "DEGRADED" and doc["failing_conditions"] == [COND_WATCHER],
        )

        # 4. Fetch-error streak >= 3 on one surface.
        os.makedirs(os.path.join(tmp, "streak"))
        ns_streak = _write_fixture(os.path.join(tmp, "streak"), streaks={"fixture-b": 3})
        doc = quiet_derive(ns_streak)
        check(
            "streak >= 3 -> DEGRADED naming no-fetch-error-streaks",
            doc["verdict"] == "DEGRADED" and doc["failing_conditions"] == [COND_STREAKS],
        )
        check(
            "streak offender listed by name",
            doc["conditions"][COND_STREAKS]["surfaces_at_or_over_threshold"]
            == [{"surface": "fixture-b", "fetch_error_streak": 3}],
        )

        # 5. Coverage gap: a registered-but-unmonitored surface misses target.
        os.makedirs(os.path.join(tmp, "gap"))
        ns_gap = _write_fixture(os.path.join(tmp, "gap"), monitored=(True, True, False))
        doc = quiet_derive(ns_gap)
        check(
            "coverage gap -> DEGRADED naming coverage-at-target",
            doc["verdict"] == "DEGRADED" and doc["failing_conditions"] == [COND_COVERAGE],
        )
        check("coverage gap: 2/3 = 66.7%", doc["conditions"][COND_COVERAGE]["coverage_pct"] == 66.7)

        # 6. Multiple failures: fixed naming order, failing conditions FIRST in md.
        os.makedirs(os.path.join(tmp, "multi"))
        ns_multi = _write_fixture(
            os.path.join(tmp, "multi"), last_run="2026-06-10T00:00:00Z", streaks={"fixture-a": 5}
        )
        doc = quiet_derive(ns_multi)
        check(
            "multi-failure order is the fixed condition order",
            doc["failing_conditions"] == [COND_WATCHER, COND_STREAKS],
        )
        md = render_markdown(doc)
        md_lines = md.splitlines()
        fail_idx = [i for i, line in enumerate(md_lines) if line.startswith("- **FAIL**")]
        ok_idx = [i for i, line in enumerate(md_lines) if line.startswith("- ok")]
        check("markdown names failing conditions before passing ones", max(fail_idx) < min(ok_idx))
        verdict_idx = next(i for i, line in enumerate(md_lines) if line.startswith("## Verdict:"))
        table_idx = next(i for i, line in enumerate(md_lines) if line.startswith("| Surface |"))
        check("markdown tile renders above the drift table", verdict_idx < table_idx)

        # 7. Missing baseline renders as MISSING, never crashes.
        os.makedirs(os.path.join(tmp, "nobase"))
        ns_nobase = _write_fixture(os.path.join(tmp, "nobase"), baselines=(True, False, True))
        doc = quiet_derive(ns_nobase)
        row = next(r for r in doc["drift_rows"] if r["surface"] == "fixture-b")
        check("missing baseline -> baseline_sha256 null", row["baseline_sha256"] is None)
        check("missing baseline renders MISSING in the table", "| MISSING |" in render_markdown(doc))

        # 8. Determinism: two generations from the same inputs are byte-identical.
        check("generate exits 0", cmd_generate(ns) == 0)
        with open(ns.json_out, encoding="utf-8") as fh:
            first_json = fh.read()
        with open(ns.md_out, encoding="utf-8") as fh:
            first_md = fh.read()
        check("regenerate exits 0", cmd_generate(ns) == 0)
        with open(ns.json_out, encoding="utf-8") as fh:
            same_json = fh.read() == first_json
        with open(ns.md_out, encoding="utf-8") as fh:
            same_md = fh.read() == first_md
        check("deterministic given inputs (json + md byte-identical)", same_json and same_md)

        # 9. Freshness gate: fresh passes; hand-edit fails; source change fails;
        #    regenerate restores; missing json fails.
        check("--check passes right after generate", cmd_check(ns) == 0)
        with open(ns.md_out, "a", encoding="utf-8") as fh:
            fh.write("\nhand edit\n")
        check("--check FAILS on a hand-edited markdown", cmd_check(ns) == 1)
        check("regenerate restores freshness", cmd_generate(ns) == 0 and cmd_check(ns) == 0)
        state_doc = _load_json(ns.state)
        state_doc["surfaces"]["fixture-a"]["fetch_error_streak"] = 1
        with open(ns.state, "w", encoding="utf-8") as fh:
            json.dump(state_doc, fh, indent=2)
        check("--check FAILS when a source changed under the committed output", cmd_check(ns) == 1)
        check("regenerate after source change restores freshness", cmd_generate(ns) == 0 and cmd_check(ns) == 0)
        os.remove(ns.json_out)
        check("--check FAILS when the committed JSON is missing", cmd_check(ns) == 1)

    # 10. The committed real outputs must themselves be fresh (mirrors
    #     lineage-log self-test step 7); guarded so fixtures-only envs skip.
    if os.path.exists(DEFAULT_JSON_OUT):
        ns_real = argparse.Namespace(
            registry=DEFAULT_REGISTRY,
            state=DEFAULT_STATE,
            coverage_map=DEFAULT_COVERAGE,
            sha_dir=DEFAULT_SHA_DIR,
            json_out=DEFAULT_JSON_OUT,
            md_out=DEFAULT_MD_OUT,
            label_root=REPO_ROOT,
            now=None,
        )
        check("committed dashboard is fresh", cmd_check(ns_real) == 0)

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the detector-health composite is not sound.")
        return 1
    print("\nself-test: verdict logic, naming order, determinism, and freshness failure modes all sound.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Detector-health composite dashboard (057-AT-SPEC).")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if a committed output is stale vs sources")
    mode.add_argument("--self-test", action="store_true", help="offline deterministic fixtures")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY)
    parser.add_argument("--state", default=DEFAULT_STATE)
    parser.add_argument("--coverage-map", default=DEFAULT_COVERAGE)
    parser.add_argument("--sha-dir", default=DEFAULT_SHA_DIR)
    parser.add_argument("--json-out", default=DEFAULT_JSON_OUT)
    parser.add_argument("--md-out", default=DEFAULT_MD_OUT)
    parser.add_argument("--now", default=None, help="override 'now' (UTC ISO) for deterministic generation")
    parser.add_argument(
        "--label-root",
        default=REPO_ROOT,
        help="root for relative path labels in the inputs fingerprint map (default: repo root)",
    )
    args = parser.parse_args()

    if args.self_test:
        return cmd_self_test()
    if args.check:
        return cmd_check(args)
    return cmd_generate(args)


if __name__ == "__main__":
    sys.exit(main())
