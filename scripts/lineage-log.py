#!/usr/bin/env python3
"""Append-only lineage log + derived coverage-map projection (054-AT-SPEC).

Kleppmann correction (045-RR-LAND § 4): the kernel's relationship to upstream
is an append-only EVENT LOG keyed on (upstream-identity, upstream-version);
the coverage map is a DERIVED projection of that log — never a hand-maintained
file. The log records WHEN each kernel authoring contract adopted an upstream
surface, WHERE it intentionally diverges (each divergence carrying its
convergence trigger, sourced from the kernel is-overlay `$comment`s), WHEN a
trigger fires, and WHEN the tier-2 vendored snapshot advanced (052-AT-SPEC).

Event vocabulary (exactly five types — the decision is documented in
000-docs/054-AT-SPEC-lineage-log-and-derived-coverage-map-2026-06-12.md):

  adopt                      a kernel contract adopts an upstream surface as a
                             source of truth (kernel upstream-base/*)
  diverge                    the kernel intentionally departs from upstream
                             (is-overlay extras); details.convergence_trigger
                             is REQUIRED — a divergence without a documented
                             way home is drift, not policy
  convergence-trigger-fired  a recorded divergence's trigger condition was
                             observed upstream; the overlay->base move is due
  snapshot-updated           the tier-2 vendored snapshot for a surface was
                             promoted from a FETCH_OK raw record (emitted by
                             scripts/fetch-capture.py at promotion time)
  fetch-degraded             a surface's capture is MATERIALLY degraded
                             (details.status = one non-FETCH_OK taxonomy
                             status). Defined now; per-attempt failures stay
                             in tier 1 (archive/raw/ meta records every
                             attempt) — this event is the materiality roll-up
                             (e.g. streak >= 3 per watcher-liveness), wiring
                             of which is a tracked follow-up.

Append-only enforcement (kept simple, per the bead): `append` snapshots the
existing bytes, writes exactly one line, re-reads, and refuses unless the new
content is old-content + one line (prefix unchanged, line count grew by one).
`verify` re-validates every line, sequential event_ids and monotonic
timestamps — a rewrite/reorder fails loud. `project-coverage --check` fails
when the committed projection is stale vs the log (CI gate).

Stdlib only. Offline. Exit 0 = ok; 1 = validation/staleness failure;
2 = usage / parse error.

Usage:
  lineage-log.py append --event-type TYPE --upstream-identity ID \
      --upstream-version VER --subject SUBJ [--details JSON] [--at ISO] \
      [--log PATH] [--registry PATH]
  lineage-log.py verify [--log PATH]
  lineage-log.py project-coverage [--log PATH] [--out PATH] [--check]
  lineage-log.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG = os.path.join(REPO_ROOT, "specs", "lineage", "log.jsonl")
DEFAULT_REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")

EVENT_TYPES = (
    "adopt",
    "diverge",
    "convergence-trigger-fired",
    "snapshot-updated",
    "fetch-degraded",
)
# The non-FETCH_OK statuses of the 052-AT-SPEC fetch taxonomy.
DEGRADED_STATUSES = ("UNREACHABLE", "MOVED", "RATELIMITED", "SHAPE_CHANGED", "TRUNCATED")

REQUIRED_KEYS = ("event_id", "at", "event_type", "upstream_identity", "upstream_version", "subject", "details")
_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

GENERATED_HEADER = (
    "GENERATED-DO-NOT-EDIT — derived projection of the append-only lineage log "
    "(specs/lineage/log.jsonl). Regenerate: python3 scripts/lineage-log.py project-coverage. "
    "Normative spec: 000-docs/054-AT-SPEC-lineage-log-and-derived-coverage-map-2026-06-12.md"
)


# ── Event validation (shared by append + verify) ────────────────────────────


def validate_event(event: Any, prior: dict | None) -> list[str]:
    """Validate one event's shape + its ordering relative to the prior event."""
    problems: list[str] = []
    if not isinstance(event, dict):
        return ["event is not a JSON object"]
    for key in REQUIRED_KEYS:
        if key not in event:
            problems.append(f"missing required key: {key}")
    unknown = set(event) - set(REQUIRED_KEYS)
    if unknown:
        problems.append(f"unknown key(s): {', '.join(sorted(unknown))}")
    if problems:
        return problems

    if not isinstance(event["event_id"], int) or isinstance(event["event_id"], bool) or event["event_id"] < 1:
        problems.append(f"event_id must be a positive integer (got {event['event_id']!r})")
    at = event["at"]
    if not isinstance(at, str) or not _AT_RE.match(at):
        problems.append(f"at must be UTC ISO 'YYYY-MM-DDTHH:MM:SSZ' (got {at!r})")
    if event["event_type"] not in EVENT_TYPES:
        problems.append(f"event_type {event['event_type']!r} not one of {EVENT_TYPES}")
    for key in ("upstream_identity", "upstream_version", "subject"):
        if not isinstance(event[key], str) or not event[key]:
            problems.append(f"{key} must be a non-empty string (got {event[key]!r})")
    details = event["details"]
    if not isinstance(details, dict):
        problems.append(f"details must be an object (got {type(details).__name__})")
    else:
        if event["event_type"] == "diverge":
            trigger = details.get("convergence_trigger")
            if not isinstance(trigger, str) or not trigger:
                problems.append("diverge events require details.convergence_trigger (non-empty string)")
        if event["event_type"] == "fetch-degraded" and details.get("status") not in DEGRADED_STATUSES:
            problems.append(f"fetch-degraded requires details.status in {DEGRADED_STATUSES}")

    if prior is not None and not problems:
        if event["event_id"] != prior["event_id"] + 1:
            problems.append(f"event_id {event['event_id']} is not prior event_id {prior['event_id']} + 1 (sequential)")
        if event["at"] < prior["at"]:
            problems.append(f"at {event['at']} is earlier than prior event's {prior['at']} (monotonic)")
    elif prior is None and not problems and event["event_id"] != 1:
        problems.append(f"first event_id must be 1 (got {event['event_id']})")
    return problems


def load_log(log_path: str) -> list[dict]:
    """Parse the log without validating (verify does that line by line)."""
    if not os.path.exists(log_path):
        return []
    events = []
    with open(log_path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"ERROR: {log_path}:{n}: not valid JSON: {exc}", file=sys.stderr)
                sys.exit(2)
    return events


# ── append ───────────────────────────────────────────────────────────────────


def registry_surface_names(registry_path: str) -> set[str]:
    with open(registry_path, encoding="utf-8") as fh:
        return {s["name"] for s in json.load(fh).get("surfaces", [])}


def cmd_append(args: argparse.Namespace) -> int:
    try:
        details = json.loads(args.details)
    except json.JSONDecodeError as exc:
        print(f"ERROR: --details is not valid JSON: {exc}", file=sys.stderr)
        return 2

    # Write-time typo guard: the identity must be a registered surface. (verify
    # deliberately does NOT re-check this — historical events outlive registry rows.)
    names = registry_surface_names(args.registry)
    if args.upstream_identity not in names:
        print(
            f"lineage-log append: REFUSED — upstream_identity {args.upstream_identity!r} "
            f"is not a surface in {args.registry}",
        )
        return 1

    events = load_log(args.log)
    prior = events[-1] if events else None
    event = {
        "event_id": (prior["event_id"] + 1) if prior else 1,
        "at": args.at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event_type": args.event_type,
        "upstream_identity": args.upstream_identity,
        "upstream_version": args.upstream_version,
        "subject": args.subject,
        "details": details,
    }
    problems = validate_event(event, prior)
    if problems:
        print(f"lineage-log append: REFUSED — {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1

    # Append-only enforcement: snapshot prior bytes, append one line, re-read,
    # refuse unless content == prior bytes + the new line (prefix unchanged,
    # line count grew by exactly one).
    os.makedirs(os.path.dirname(args.log) or ".", exist_ok=True)
    before = b""
    if os.path.exists(args.log):
        with open(args.log, "rb") as fh:
            before = fh.read()
    line = json.dumps(event, sort_keys=True) + "\n"
    with open(args.log, "a", encoding="utf-8") as fh:
        fh.write(line)
    with open(args.log, "rb") as fh:
        after = fh.read()
    if not after.startswith(before) or after != before + line.encode("utf-8"):
        print(
            "lineage-log append: APPEND-ONLY VIOLATION — the log's existing prefix changed "
            "during append (concurrent writer or tamper). Inspect the log before retrying.",
        )
        return 1

    # The coverage map is a derived view: regenerate it on every append so the
    # committed projection can never go stale through the script path.
    write_coverage(events + [event], coverage_path_for(args.log))
    print(f"lineage-log append: event_id={event['event_id']} {event['event_type']} {event['upstream_identity']}")
    return 0


# ── verify ───────────────────────────────────────────────────────────────────


def cmd_verify(log_path: str) -> int:
    events = load_log(log_path)
    if not events:
        print(f"lineage-log verify: FAIL — log missing or empty: {log_path}")
        return 1
    problems: list[str] = []
    prior: dict | None = None
    for n, event in enumerate(events, start=1):
        for p in validate_event(event, prior):
            problems.append(f"line {n}: {p}")
        prior = event if isinstance(event, dict) else prior
    if problems:
        print(f"lineage-log verify: FAIL — {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(
        f"lineage-log verify: OK — {len(events)} events, event_ids sequential 1..{events[-1]['event_id']}, "
        "timestamps monotonic, all shapes valid."
    )
    return 0


# ── project-coverage (the derived view) ──────────────────────────────────────


def coverage_path_for(log_path: str) -> str:
    return os.path.join(os.path.dirname(log_path) or ".", "coverage-map.json")


def project_coverage(events: list[dict]) -> dict:
    """Derive the coverage map: per upstream surface -> latest adopt state,
    divergences with convergence triggers outstanding, fired triggers, last
    snapshot promotion, last material fetch degradation."""
    surfaces: dict[str, dict] = {}
    for ev in events:
        s = surfaces.setdefault(
            ev["upstream_identity"],
            {
                "contract": None,
                "adopted": None,
                "divergences_outstanding": [],
                "convergence_fired": [],
                "last_snapshot_updated": None,
                "last_fetch_degraded": None,
            },
        )
        ref = {"at": ev["at"], "event_id": ev["event_id"]}
        et = ev["event_type"]
        if et == "adopt":
            s["adopted"] = ref
            s["contract"] = ev["subject"]
        elif et == "diverge":
            s["divergences_outstanding"].append(
                {
                    "subject": ev["subject"],
                    "convergence_trigger": ev["details"]["convergence_trigger"],
                    "since": ev["at"],
                    "event_id": ev["event_id"],
                }
            )
        elif et == "convergence-trigger-fired":
            s["divergences_outstanding"] = [d for d in s["divergences_outstanding"] if d["subject"] != ev["subject"]]
            s["convergence_fired"].append({"subject": ev["subject"], **ref})
        elif et == "snapshot-updated":
            s["last_snapshot_updated"] = {"upstream_version": ev["upstream_version"], **ref}
        elif et == "fetch-degraded":
            s["last_fetch_degraded"] = {"status": ev["details"]["status"], **ref}
        if s["contract"] is None:
            s["contract"] = ev["subject"].split("/")[0]
    for s in surfaces.values():
        s["convergence_triggers_outstanding"] = len(s["divergences_outstanding"])
    return {
        "_generated": GENERATED_HEADER,
        "projection_version": "lineage-coverage/v1",
        "derived_from": {
            "log": "specs/lineage/log.jsonl",
            "line_count": len(events),
            "last_event_id": events[-1]["event_id"] if events else 0,
        },
        "surfaces": surfaces,
    }


def render_coverage(events: list[dict]) -> str:
    return json.dumps(project_coverage(events), indent=2, sort_keys=True) + "\n"


def write_coverage(events: list[dict], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(render_coverage(events))


def cmd_project_coverage(log_path: str, out_path: str, check: bool) -> int:
    events = load_log(log_path)
    fresh = render_coverage(events)
    if check:
        if not os.path.exists(out_path):
            print(f"lineage-log project-coverage --check: FAIL — projection missing: {out_path}")
            return 1
        with open(out_path, encoding="utf-8") as fh:
            committed = fh.read()
        if committed != fresh:
            print(
                f"lineage-log project-coverage --check: STALE — {out_path} does not match a fresh "
                f"derivation of {log_path} ({len(events)} events). The coverage map is a DERIVED "
                "view — never hand-edit it. Regenerate: python3 scripts/lineage-log.py project-coverage"
            )
            return 1
        print(f"lineage-log project-coverage --check: OK — projection is fresh ({len(events)} events).")
        return 0
    write_coverage(events, out_path)
    print(f"lineage-log project-coverage: wrote {out_path} ({len(events)} events).")
    return 0


# ── Deterministic offline self-test ──────────────────────────────────────────


def cmd_self_test() -> int:  # noqa: SIM117
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    def ns(**kw: Any) -> argparse.Namespace:
        return argparse.Namespace(**{"details": "{}", "at": None, **kw})

    with tempfile.TemporaryDirectory() as tmp:
        registry = os.path.join(tmp, "registry.json")
        with open(registry, "w", encoding="utf-8") as fh:
            json.dump({"surfaces": [{"name": "fixture-a"}, {"name": "fixture-b"}]}, fh)
        log = os.path.join(tmp, "lineage", "log.jsonl")
        cov = coverage_path_for(log)

        def append(**kw: Any) -> int:
            base = {"log": log, "registry": registry}
            return cmd_append(ns(**{**base, **kw}))

        # 1. One valid append per event type; ids sequential; verify passes.
        rc = append(event_type="adopt", upstream_identity="fixture-a", upstream_version="reg/v1",
                    subject="contract-a", at="2026-06-01T00:00:00Z")
        check("append adopt accepted", rc == 0)
        rc = append(event_type="diverge", upstream_identity="fixture-a", upstream_version="sha-1",
                    subject="contract-a/extra-field", at="2026-06-02T00:00:00Z",
                    details='{"convergence_trigger": "upstream adds extra-field"}')
        check("append diverge (with trigger) accepted", rc == 0)
        rc = append(event_type="snapshot-updated", upstream_identity="fixture-a", upstream_version="sha-2",
                    subject="contract-a", at="2026-06-03T00:00:00Z")
        check("append snapshot-updated accepted", rc == 0)
        rc = append(event_type="fetch-degraded", upstream_identity="fixture-b", upstream_version="sha-2",
                    subject="contract-b", at="2026-06-04T00:00:00Z", details='{"status": "MOVED"}')
        check("append fetch-degraded accepted", rc == 0)
        check("verify passes on a clean log", cmd_verify(log) == 0)

        # 2. Append rejections — every guard refuses (exit 1), log does not grow.
        lines_before = len(load_log(log))
        rejects = [
            ("unknown event_type", append(event_type="mutate", upstream_identity="fixture-a",
                                          upstream_version="v", subject="s", at="2026-06-05T00:00:00Z")),
            ("identity not in registry", append(event_type="adopt", upstream_identity="nope",
                                                upstream_version="v", subject="s", at="2026-06-05T00:00:00Z")),
            ("diverge without trigger", append(event_type="diverge", upstream_identity="fixture-a",
                                               upstream_version="v", subject="s", at="2026-06-05T00:00:00Z")),
            ("fetch-degraded bad status", append(event_type="fetch-degraded", upstream_identity="fixture-a",
                                                 upstream_version="v", subject="s",
                                                 at="2026-06-05T00:00:00Z", details='{"status": "FETCH_OK"}')),
            ("non-monotonic at", append(event_type="adopt", upstream_identity="fixture-a",
                                        upstream_version="v", subject="s", at="2026-05-01T00:00:00Z")),
            ("empty subject", append(event_type="adopt", upstream_identity="fixture-a",
                                     upstream_version="v", subject="", at="2026-06-05T00:00:00Z")),
        ]
        for label, rc in rejects:
            check(f"append refuses: {label}", rc == 1)
        check("refused appends did not grow the log", len(load_log(log)) == lines_before)

        # 3. Projection correctness (derived, never hand-maintained).
        m = project_coverage(load_log(log))
        a, b = m["surfaces"]["fixture-a"], m["surfaces"]["fixture-b"]
        check("projection: fixture-a adopted", a["adopted"] == {"at": "2026-06-01T00:00:00Z", "event_id": 1})
        check("projection: 1 divergence outstanding with its trigger",
              a["convergence_triggers_outstanding"] == 1
              and a["divergences_outstanding"][0]["convergence_trigger"] == "upstream adds extra-field")
        check("projection: last snapshot-updated tracked",
              a["last_snapshot_updated"] == {"upstream_version": "sha-2", "at": "2026-06-03T00:00:00Z", "event_id": 3})
        check("projection: fetch-degraded tracked on fixture-b",
              b["last_fetch_degraded"] == {"status": "MOVED", "at": "2026-06-04T00:00:00Z", "event_id": 4})
        check("projection: line_count == log lines", m["derived_from"]["line_count"] == 4)

        # 4. convergence-trigger-fired clears the matching outstanding divergence.
        rc = append(event_type="convergence-trigger-fired", upstream_identity="fixture-a",
                    upstream_version="sha-3", subject="contract-a/extra-field", at="2026-06-06T00:00:00Z")
        check("append convergence-trigger-fired accepted", rc == 0)
        a = project_coverage(load_log(log))["surfaces"]["fixture-a"]
        check("projection: trigger fired -> 0 outstanding, 1 fired",
              a["convergence_triggers_outstanding"] == 0 and len(a["convergence_fired"]) == 1)

        # 5. Projection freshness gate: append auto-regenerated it (fresh) …
        check("--check passes right after append", cmd_project_coverage(log, cov, check=True) == 0)
        # … and a hand-edit / stale copy FAILS the check (the staleness failure).
        with open(cov, "a", encoding="utf-8") as fh:
            fh.write("\n")
        check("--check FAILS on a hand-edited projection", cmd_project_coverage(log, cov, check=True) == 1)
        check("regenerate restores freshness",
              cmd_project_coverage(log, cov, check=False) == 0 and cmd_project_coverage(log, cov, check=True) == 0)

        # 6. verify catches tampering: reorder (ids no longer sequential) + a
        #    rewritten non-monotonic timestamp both fail loud.
        events = load_log(log)
        with open(log, "w", encoding="utf-8") as fh:
            for ev in [events[1], events[0], *events[2:]]:
                fh.write(json.dumps(ev, sort_keys=True) + "\n")
        check("verify FAILS on reordered log", cmd_verify(log) == 1)
        events[2]["at"] = "2025-01-01T00:00:00Z"
        with open(log, "w", encoding="utf-8") as fh:
            for ev in events:
                fh.write(json.dumps(ev, sort_keys=True) + "\n")
        check("verify FAILS on non-monotonic rewrite", cmd_verify(log) == 1)

    # 7. The committed real log + projection must themselves be sound + fresh.
    if os.path.exists(DEFAULT_LOG):
        check("committed log verifies", cmd_verify(DEFAULT_LOG) == 0)
        check("committed projection is fresh",
              cmd_project_coverage(DEFAULT_LOG, coverage_path_for(DEFAULT_LOG), check=True) == 0)

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the lineage log machinery is not sound.")
        return 1
    print("\nself-test: append/verify/project sound; staleness + tamper failure modes all detected.")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Append-only lineage log + derived coverage map (054-AT-SPEC).")
    parser.add_argument("--self-test", action="store_true", help="offline deterministic check")
    sub = parser.add_subparsers(dest="cmd")

    p_append = sub.add_parser("append", help="validate + append one event (refuses invalid shape / non-append)")
    p_append.add_argument("--event-type", required=True, choices=EVENT_TYPES)
    p_append.add_argument("--upstream-identity", required=True, help="surface name from the registry")
    p_append.add_argument("--upstream-version", required=True, help="snapshot sha256 or registry-declared version")
    p_append.add_argument("--subject", required=True, help="kernel contract or contract/field")
    p_append.add_argument("--details", default="{}", help="JSON object (diverge requires convergence_trigger)")
    p_append.add_argument("--at", default=None, help="UTC ISO timestamp (default: now)")
    p_append.add_argument("--log", default=DEFAULT_LOG)
    p_append.add_argument("--registry", default=DEFAULT_REGISTRY)

    p_verify = sub.add_parser("verify", help="schema-validate every line; sequential ids; monotonic timestamps")
    p_verify.add_argument("--log", default=DEFAULT_LOG)

    p_proj = sub.add_parser("project-coverage", help="derive the coverage map (--check: fail if committed copy stale)")
    p_proj.add_argument("--log", default=DEFAULT_LOG)
    p_proj.add_argument("--out", default=None, help="output path (default: coverage-map.json beside the log)")
    p_proj.add_argument("--check", action="store_true")

    args = parser.parse_args()
    if args.self_test:
        return cmd_self_test()
    if args.cmd == "append":
        return cmd_append(args)
    if args.cmd == "verify":
        return cmd_verify(args.log)
    if args.cmd == "project-coverage":
        return cmd_project_coverage(args.log, args.out or coverage_path_for(args.log), args.check)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
