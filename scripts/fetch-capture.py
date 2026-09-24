#!/usr/bin/env python3
"""Typed fetch-failure taxonomy + tier-1/tier-2 capture for the spec-drift watcher.

The byte-hash watcher (spec-drift-check.sh) answers "did the page change?" but
collapses every failure into a single fetch_error bucket and keeps no record of
what was actually fetched. This stage EXTENDS that machinery (never replaces it)
with two things the SSoT plan requires (045-RR-LAND; Armstrong/Kleppmann
corrections per the 7-thinker panel):

  1. A typed fetch-failure taxonomy. Every fetch attempt is classified as
     exactly ONE of:
       FETCH_OK | UNREACHABLE | MOVED | RATELIMITED | SHAPE_CHANGED | TRUNCATED
     Only FETCH_OK output may feed the differ/classifier downstream. Any other
     status: the last-good vendored snapshot stays untouched, the CI side
     effects alert (ntfy prod-health), and NO reconciliation issue/PR is ever
     opened off a bad fetch (Armstrong: a failed fetch is a typed, isolated
     failure — it must never masquerade as upstream change).

  2. The first two of the three append-only tiers (Kleppmann: the raw log is
     the immutable source of record; everything downstream is a derived view):
       tier 1  archive/raw/<surface-id>/<UTC-stamp>.{body,meta.json}
               — immutable, append-only; EVERY fetch attempt lands here.
               Bodies are sha256-deduplicated: a body identical to the
               previous record's is not rewritten; meta.json still appends,
               with body_ref naming the record that stores those bytes.
       tier 2  specs/_vendor/<surface-id>/snapshot<ext> + vendor-meta.json
               — the last-good snapshot, updated ONLY from a FETCH_OK raw
               record, recording exactly which raw record it came from.
       tier 3  the kernel (@intentsolutions/core authoring/v1) lives in
               intent-eval-core. Promotion tier-2 -> tier-3 is HUMAN; this
               script never automates it (see 000-docs/052-AT-SPEC).
     THE DIFFER NEVER WRITES ITS OWN REFERENCE: spec-projection-diff.py reads
     vendored snapshots; nothing downstream of tier 2 writes into tier 2.

Driven by specs/upstream-surface-registry.v1.json (per-surface `capture`
config: kind, urls/argv, expect_regex shape hint, min_bytes floor, ext).
Stdlib only. Network ONLY in live mode; --self-test is fully offline.

Exit 0 = all captures FETCH_OK (or self-test passed); exit 1 = at least one
non-FETCH_OK status (or self-test failure); exit 2 = usage / config error.

Usage:
  fetch-capture.py                          # capture all monitored surfaces
  fetch-capture.py --surface NAME           # capture one surface
  fetch-capture.py --report REPORT.json     # also write a JSON report (CI)
  fetch-capture.py --self-test              # offline fixtures: all 6 statuses
                                            # + archive append/dedup + tier-2 gating
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_REGISTRY = os.path.join(REPO_ROOT, "specs", "upstream-surface-registry.v1.json")
DEFAULT_ARCHIVE_ROOT = os.path.join(REPO_ROOT, "archive", "raw")
DEFAULT_VENDOR_ROOT = os.path.join(REPO_ROOT, "specs", "_vendor")
DEFAULT_LINEAGE_LOG = os.path.join(REPO_ROOT, "specs", "lineage", "log.jsonl")
LINEAGE_SCRIPT = os.path.join(REPO_ROOT, "scripts", "lineage-log.py")

FETCH_OK = "FETCH_OK"
UNREACHABLE = "UNREACHABLE"
MOVED = "MOVED"
RATELIMITED = "RATELIMITED"
SHAPE_CHANGED = "SHAPE_CHANGED"
TRUNCATED = "TRUNCATED"
STATUSES = (FETCH_OK, UNREACHABLE, MOVED, RATELIMITED, SHAPE_CHANGED, TRUNCATED)

TIMEOUT_SECONDS = 30
USER_AGENT = "intent-eval-lab-fetch-capture/1.0"


@dataclass
class RawFetch:
    """One transport-level fetch attempt, before classification.

    For command-kind surfaces (e.g. `npm view`), a clean exit is recorded as
    http_code=200 (transport-OK sentinel); the archived meta carries the real
    transport in its url field.
    """

    requested_url: str = ""
    http_code: int | None = None
    body: bytes | None = None
    error: str | None = None
    # (status_code, target_url) per redirect hop, in order.
    redirects: list[tuple[int, str]] = field(default_factory=list)


def _host(url: str) -> str:
    return (urllib.parse.urlparse(url).hostname or "").lower()


def classify_fetch(raw: RawFetch, capture: dict) -> str:
    """Map one fetch attempt to exactly one taxonomy status (first rule wins).

    Heuristics (052-AT-SPEC): HTTP errors/timeouts -> UNREACHABLE; 404 or a
    301/302 redirect to a different host -> MOVED; 429 -> RATELIMITED; body
    under the per-surface floor -> TRUNCATED; body not matching the surface's
    expected extractor pattern -> SHAPE_CHANGED; else FETCH_OK.
    """
    if raw.http_code == 429:
        return RATELIMITED
    if raw.http_code == 404:
        return MOVED
    for code, target in raw.redirects:
        if code in (301, 302) and raw.requested_url and _host(target) != _host(raw.requested_url):
            return MOVED
    if raw.error is not None or raw.http_code is None:
        return UNREACHABLE
    if raw.http_code >= 400:
        return UNREACHABLE
    body = raw.body if raw.body is not None else b""
    if len(body) < int(capture.get("min_bytes", 1)):
        return TRUNCATED
    text = body.decode("utf-8", errors="replace")
    pattern = capture.get("expect_regex")
    if pattern and not re.search(pattern, text):
        return SHAPE_CHANGED

    # expect_title: the page must still be the DOCUMENT we registered.
    #
    # expect_regex alone cannot answer that. Every surface's pattern is
    # effectively "(?m)^#{1,3} " — any heading — so a page that upstream replaces
    # wholesale still matches and still classifies FETCH_OK. That is not
    # hypothetical: slash-commands.md was replaced by a document titled "Extend
    # Claude with skills", the capture promoted it as the last-good snapshot, and
    # nothing anywhere went red. A shape hint answers "is this still a document";
    # expect_title answers "is this still THAT document".
    #
    # Mapped onto the existing SHAPE_CHANGED rather than a seventh status: the
    # six statuses are normative in 052-AT-SPEC, and "the document I expected is
    # not what I got" is already what SHAPE_CHANGED means. Adding a status to
    # express a subtype would widen a normative taxonomy for no new handling.
    title = capture.get("expect_title")
    if title:
        heading = next((l for l in text.splitlines() if l.startswith("# ")), None)
        if heading is None or not re.search(title, heading[2:].strip()):
            return SHAPE_CHANGED
    return FETCH_OK


def classify_surface(raws: list[RawFetch], capture: dict) -> tuple[str, bytes | None, int | None]:
    """Classify a surface's fetch attempts (1+ URLs). First non-OK wins
    (conservative); on all-OK the bodies concatenate into one raw record."""
    bodies: list[bytes] = []
    for raw in raws:
        status = classify_fetch(raw, capture)
        if status != FETCH_OK:
            return status, raw.body, raw.http_code
        bodies.append(raw.body or b"")
    return FETCH_OK, b"\n".join(bodies), raws[-1].http_code if raws else None


class _RedirectRecorder(urllib.request.HTTPRedirectHandler):
    """Record every redirect hop so MOVED (cross-host 301/302) is detectable."""

    def __init__(self) -> None:
        self.chain: list[tuple[int, str]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        self.chain.append((code, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def http_fetch(url: str) -> RawFetch:
    recorder = _RedirectRecorder()
    opener = urllib.request.build_opener(recorder)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as resp:
            return RawFetch(
                requested_url=url,
                http_code=resp.status,
                body=resp.read(),
                redirects=recorder.chain,
            )
    except urllib.error.HTTPError as exc:
        return RawFetch(
            requested_url=url, http_code=exc.code, error=str(exc), redirects=recorder.chain
        )
    except Exception as exc:  # URLError, timeout, ConnectionError, ...
        return RawFetch(requested_url=url, error=str(exc), redirects=recorder.chain)


def command_fetch(argv: list[str]) -> RawFetch:
    label = " ".join(argv)
    try:
        proc = subprocess.run(argv, capture_output=True, timeout=TIMEOUT_SECONDS, check=False)
    except Exception as exc:  # FileNotFoundError, TimeoutExpired, ...
        return RawFetch(requested_url=label, error=str(exc))
    if proc.returncode != 0:
        return RawFetch(requested_url=label, error=f"command exited {proc.returncode}")
    return RawFetch(requested_url=label, http_code=200, body=proc.stdout)


def default_fetcher(surface: dict) -> list[RawFetch]:
    capture = surface["capture"]
    if capture["kind"] == "command":
        return [command_fetch(list(capture["argv"]))]
    return [http_fetch(url) for url in capture["urls"]]


# ── Tier 1: append-only raw archive ─────────────────────────────────────────


def _latest_record(surface_dir: str) -> dict | None:
    if not os.path.isdir(surface_dir):
        return None
    metas = sorted(f for f in os.listdir(surface_dir) if f.endswith(".meta.json"))
    if not metas:
        return None
    with open(os.path.join(surface_dir, metas[-1]), encoding="utf-8") as fh:
        return json.load(fh)


def append_raw_record(
    archive_root: str,
    surface_id: str,
    display_url: str,
    status: str,
    http_code: int | None,
    body: bytes | None,
    now: datetime,
) -> dict:
    """Append exactly one raw record. Never deletes or rewrites an existing
    record (append-only). Bodies are sha256-deduplicated against the previous
    record: identical bytes are not rewritten; the new meta's body_ref names
    the record whose .body file stores them."""
    surface_dir = os.path.join(archive_root, surface_id)
    os.makedirs(surface_dir, exist_ok=True)
    prior = _latest_record(surface_dir)

    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    record = stamp
    suffix = 0
    while os.path.exists(os.path.join(surface_dir, f"{record}.meta.json")):
        suffix += 1  # same-second collision: append a counter, never overwrite
        record = f"{stamp}-{suffix}"

    sha = hashlib.sha256(body).hexdigest() if body is not None else None
    body_ref: str | None = None
    if body is not None:
        if prior is not None and prior.get("sha256") == sha and prior.get("body_ref"):
            body_ref = prior["body_ref"]  # dedup: bytes already archived there
        else:
            with open(os.path.join(surface_dir, f"{record}.body"), "wb") as fh:
                fh.write(body)
            body_ref = record

    meta = {
        "record": record,
        "surface_id": surface_id,
        "url": display_url,
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": status,
        "http_code": http_code,
        "sha256": sha,
        "bytes": len(body) if body is not None else 0,
        "body_stored": body_ref == record,
        "body_ref": body_ref,
    }
    with open(os.path.join(surface_dir, f"{record}.meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


# ── Tier 2: last-good vendored snapshot (FETCH_OK promotions only) ──────────


def update_vendored(
    vendor_root: str, surface_id: str, ext: str, body: bytes, meta: dict, now: datetime
) -> bool:
    """Promote a FETCH_OK raw record into the vendored tier. Returns True when
    the snapshot changed. The caller MUST gate this on status == FETCH_OK; the
    function refuses anything else (defense in depth)."""
    if meta["status"] != FETCH_OK:
        raise ValueError(f"refusing tier-2 update from a {meta['status']} record")
    vendor_dir = os.path.join(vendor_root, surface_id)
    os.makedirs(vendor_dir, exist_ok=True)
    vendor_meta_path = os.path.join(vendor_dir, "vendor-meta.json")
    if os.path.exists(vendor_meta_path):
        with open(vendor_meta_path, encoding="utf-8") as fh:
            if json.load(fh).get("sha256") == meta["sha256"]:
                return False  # unchanged — no rewrite
    with open(os.path.join(vendor_dir, f"snapshot{ext}"), "wb") as fh:
        fh.write(body)
    vendor_meta = {
        "surface_id": surface_id,
        "sha256": meta["sha256"],
        "bytes": meta["bytes"],
        "updated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_raw_record": f"archive/raw/{surface_id}/{meta['record']}.meta.json",
    }
    with open(vendor_meta_path, "w", encoding="utf-8") as fh:
        json.dump(vendor_meta, fh, indent=2)
        fh.write("\n")
    return True


# ── Lineage emission (054-AT-SPEC: the capture stage emits; the differ writes nothing) ──


def append_lineage_event(
    lineage_log: str, registry_path: str, surface: dict, meta: dict, now: datetime
) -> bool:
    """Append a snapshot-updated event to the lineage log for a tier-2 promotion.
    Delegates to scripts/lineage-log.py append (which validates the event shape,
    enforces append-only, and regenerates the derived coverage map). A failure is
    loud (stderr) but never rolls back the promotion that already happened."""
    details = {
        "source_raw_record": f"archive/raw/{surface['name']}/{meta['record']}.meta.json",
        "bytes": meta["bytes"],
    }
    argv = [
        sys.executable, LINEAGE_SCRIPT, "append",
        "--log", lineage_log,
        "--registry", registry_path,
        "--event-type", "snapshot-updated",
        "--upstream-identity", surface["name"],
        "--upstream-version", meta["sha256"],
        "--subject", surface.get("contract", surface["name"]),
        "--at", now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "--details", json.dumps(details),
    ]
    proc = subprocess.run(argv, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        print(
            f"WARNING: lineage snapshot-updated append failed for {surface['name']}: "
            f"{(proc.stdout + proc.stderr).strip()}",
            file=sys.stderr,
        )
        return False
    return True


# ── Orchestration ────────────────────────────────────────────────────────────


def load_registry(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        registry = json.load(fh)
    surfaces = [s for s in registry.get("surfaces", []) if s.get("monitored")]
    missing = [s["name"] for s in surfaces if not isinstance(s.get("capture"), dict)]
    if missing:
        print(f"ERROR: surfaces missing capture config: {', '.join(missing)}", file=sys.stderr)
        sys.exit(2)
    return surfaces


def run_capture(
    surfaces: list[dict],
    archive_root: str,
    vendor_root: str,
    fetcher: Callable[[dict], list[RawFetch]] = default_fetcher,
    now: datetime | None = None,
    report_path: str | None = None,
    lineage_log: str | None = None,
    lineage_registry: str = DEFAULT_REGISTRY,
) -> int:
    now = now or datetime.now(timezone.utc)
    rows: list[dict] = []
    bad = 0
    for surface in surfaces:
        capture = surface["capture"]
        raws = fetcher(surface)
        status, body, http_code = classify_surface(raws, capture)
        meta = append_raw_record(
            archive_root, surface["name"], surface["url"], status, http_code, body, now
        )
        vendor_updated = False
        if status == FETCH_OK and body is not None:
            vendor_updated = update_vendored(
                vendor_root, surface["name"], capture.get("ext", ".txt"), body, meta, now
            )
            # A tier-2 promotion is a lineage fact: emit snapshot-updated
            # (054-AT-SPEC). Only the capture stage emits; the differ writes
            # nothing. Non-promotions (dedup or bad fetch) emit nothing.
            if vendor_updated and lineage_log:
                append_lineage_event(lineage_log, lineage_registry, surface, meta, now)
        else:
            bad += 1
        rows.append(
            {
                "surface": surface["name"],
                "status": status,
                "record": meta["record"],
                "body_stored": meta["body_stored"],
                "vendor_updated": vendor_updated,
            }
        )
        flag = "" if status == FETCH_OK else "  <-- last-good vendored snapshot kept"
        print(
            f"{surface['name']}: {status} (record={meta['record']}, "
            f"body_stored={meta['body_stored']}, vendor_updated={vendor_updated}){flag}"
        )

    if report_path:
        with open(report_path, "w", encoding="utf-8") as fh:
            json.dump(
                {"captured_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "surfaces": rows},
                fh,
                indent=2,
            )
            fh.write("\n")

    if bad:
        print(
            f"\nfetch-capture: {bad} of {len(surfaces)} surfaces NOT FETCH_OK — vendored "
            "snapshots untouched; alert only, never a reconciliation issue/PR off a bad fetch."
        )
        return 1
    print(f"\nfetch-capture: all {len(surfaces)} surfaces FETCH_OK.")
    return 0


# ── Deterministic self-test (offline; fixtures exercise all 6 statuses) ─────


def cmd_self_test() -> int:
    failures = 0

    def check(label: str, condition: bool) -> None:
        nonlocal failures
        if condition:
            print(f"self-test ok: {label}")
        else:
            print(f"self-test FAIL: {label}")
            failures += 1

    capture = {"min_bytes": 64, "expect_regex": r"(?m)^# ", "ext": ".md", "kind": "http"}
    good_body = b"# Spec heading\n\n" + b"x" * 128
    url = "https://example.com/spec.md"

    # 1. Classification fixtures — every status reachable, exactly one each.
    fixtures: list[tuple[str, RawFetch]] = [
        (FETCH_OK, RawFetch(requested_url=url, http_code=200, body=good_body)),
        (UNREACHABLE, RawFetch(requested_url=url, error="timed out")),
        (UNREACHABLE, RawFetch(requested_url=url, http_code=500, error="HTTP 500")),
        (MOVED, RawFetch(requested_url=url, http_code=404, error="HTTP 404")),
        (
            MOVED,
            RawFetch(
                requested_url=url,
                http_code=200,
                body=good_body,
                redirects=[(301, "https://elsewhere.example.org/spec.md")],
            ),
        ),
        (
            FETCH_OK,  # same-host redirect is NOT a move (no false positive)
            RawFetch(
                requested_url=url,
                http_code=200,
                body=good_body,
                redirects=[(302, "https://example.com/spec-v2.md")],
            ),
        ),
        (RATELIMITED, RawFetch(requested_url=url, http_code=429, error="HTTP 429")),
        (
            SHAPE_CHANGED,
            RawFetch(requested_url=url, http_code=200, body=b"<!DOCTYPE html>" + b"y" * 128),
        ),
        (TRUNCATED, RawFetch(requested_url=url, http_code=200, body=b"# Spec")),
    ]
    for expected, raw in fixtures:
        got = classify_fetch(raw, capture)
        check(f"classify -> {expected}", got == expected and got in STATUSES)

    # 2. End-to-end archive/vendor behavior in a temp dir with a fake fetcher.
    surface = {"name": "fixture-surface", "url": url, "monitored": True, "capture": capture}
    script: list[list[RawFetch]] = []

    def fake_fetcher(_surface: dict) -> list[RawFetch]:
        return script.pop(0)

    with tempfile.TemporaryDirectory() as tmp:
        archive_root = os.path.join(tmp, "archive", "raw")
        vendor_root = os.path.join(tmp, "specs", "_vendor")
        surface_dir = os.path.join(archive_root, "fixture-surface")
        vendor_snap = os.path.join(vendor_root, "fixture-surface", "snapshot.md")
        lineage_log = os.path.join(tmp, "specs", "lineage", "log.jsonl")
        fixture_registry = os.path.join(tmp, "registry.json")
        with open(fixture_registry, "w", encoding="utf-8") as fh:
            json.dump({"surfaces": [surface]}, fh)

        def lineage_events() -> list[dict]:
            if not os.path.exists(lineage_log):
                return []
            with open(lineage_log, encoding="utf-8") as fh:
                return [json.loads(line) for line in fh if line.strip()]

        def run_at(minute: int, raws: list[RawFetch]) -> int:
            script.append(raws)
            return run_capture(
                [surface],
                archive_root,
                vendor_root,
                fetcher=fake_fetcher,
                now=datetime(2026, 6, 12, 9, minute, 0, tzinfo=timezone.utc),
                lineage_log=lineage_log,
                lineage_registry=fixture_registry,
            )

        # run 1: FETCH_OK body A -> body stored, vendored == A
        rc1 = run_at(0, [RawFetch(requested_url=url, http_code=200, body=good_body)])
        check("run1 exit 0 on FETCH_OK", rc1 == 0)
        check("run1 vendored snapshot == body A", open(vendor_snap, "rb").read() == good_body)
        events = lineage_events()
        check(
            "run1 lineage: tier-2 promotion emitted snapshot-updated (054-AT-SPEC)",
            len(events) == 1
            and events[0]["event_type"] == "snapshot-updated"
            and events[0]["upstream_identity"] == "fixture-surface"
            and events[0]["upstream_version"] == hashlib.sha256(good_body).hexdigest(),
        )

        # run 2: identical body -> meta appends, body deduplicated (not rewritten)
        run_at(1, [RawFetch(requested_url=url, http_code=200, body=good_body)])
        check("run2 lineage: dedup (no promotion) emitted nothing", len(lineage_events()) == 1)
        metas = sorted(f for f in os.listdir(surface_dir) if f.endswith(".meta.json"))
        bodies = sorted(f for f in os.listdir(surface_dir) if f.endswith(".body"))
        meta2 = json.load(open(os.path.join(surface_dir, metas[1]), encoding="utf-8"))
        check("run2 meta appended (2 metas)", len(metas) == 2)
        check("run2 body deduplicated (1 body file)", len(bodies) == 1)
        check(
            "run2 body_ref names run1's record",
            meta2["body_stored"] is False and meta2["body_ref"] == metas[0][: -len(".meta.json")],
        )

        # run 3: UNREACHABLE -> meta appends; last-good vendored snapshot untouched
        rc3 = run_at(2, [RawFetch(requested_url=url, error="connection refused")])
        meta3 = json.load(
            open(
                os.path.join(
                    surface_dir,
                    sorted(f for f in os.listdir(surface_dir) if f.endswith(".meta.json"))[-1],
                ),
                encoding="utf-8",
            )
        )
        check("run3 exit 1 on bad fetch", rc3 == 1)
        check("run3 archived as UNREACHABLE", meta3["status"] == UNREACHABLE)
        check("run3 last-good vendored untouched", open(vendor_snap, "rb").read() == good_body)
        check("run3 lineage: bad fetch emitted nothing", len(lineage_events()) == 1)

        # run 4: FETCH_OK body B -> new body stored, vendored == B
        body_b = b"# Spec heading v2\n\n" + b"z" * 128
        run_at(3, [RawFetch(requested_url=url, http_code=200, body=body_b)])
        bodies = sorted(f for f in os.listdir(surface_dir) if f.endswith(".body"))
        check("run4 new body stored (2 body files)", len(bodies) == 2)
        check("run4 vendored snapshot == body B", open(vendor_snap, "rb").read() == body_b)
        events = lineage_events()
        check(
            "run4 lineage: second promotion appended event_id 2 with body B's sha",
            len(events) == 2
            and events[1]["event_id"] == 2
            and events[1]["upstream_version"] == hashlib.sha256(body_b).hexdigest(),
        )

        # append-only: run1's meta is byte-identical to what was first written
        meta1 = json.load(open(os.path.join(surface_dir, metas[0]), encoding="utf-8"))
        check("append-only: run1 meta unchanged", meta1["record"] == metas[0][: -len(".meta.json")])

        # tier-2 guard: a non-FETCH_OK record must be refused outright
        try:
            update_vendored(
                vendor_root,
                "fixture-surface",
                ".md",
                b"bad",
                {"status": UNREACHABLE, "sha256": "0", "bytes": 3, "record": "x"},
                datetime(2026, 6, 12, 9, 4, 0, tzinfo=timezone.utc),
            )
            check("tier-2 refuses non-FETCH_OK record", False)
        except ValueError:
            check("tier-2 refuses non-FETCH_OK record", True)

    # 3. Registry capture-config sanity (local file, offline).
    surfaces = load_registry(DEFAULT_REGISTRY)
    check(f"registry: all {len(surfaces)} monitored surfaces carry capture config", bool(surfaces))
    for s in surfaces:
        ok = True
        try:
            re.compile(s["capture"]["expect_regex"])
        except (KeyError, re.error):
            ok = False
        if not ok:
            check(f"registry: {s['name']} expect_regex compiles", False)

    if failures:
        print(f"\nself-test: {failures} FAILURE(S) — the taxonomy/tier machinery is not sound.")
        return 1
    print("\nself-test: all 6 statuses exercised; append/dedup/tier-2 gating sound.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Typed fetch-failure taxonomy + tier-1/tier-2 capture."
    )
    parser.add_argument("--self-test", action="store_true", help="offline fixtures-driven check")
    parser.add_argument("--surface", default=None, help="capture only this surface")
    parser.add_argument("--report", default=None, help="write a JSON report here (CI)")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY, help="surface registry path")
    parser.add_argument("--archive-root", default=DEFAULT_ARCHIVE_ROOT, help="tier-1 root")
    parser.add_argument("--vendor-root", default=DEFAULT_VENDOR_ROOT, help="tier-2 root")
    parser.add_argument(
        "--lineage-log", default=DEFAULT_LINEAGE_LOG, help="lineage log appended on tier-2 promotion"
    )
    args = parser.parse_args()

    if args.self_test:
        return cmd_self_test()

    surfaces = load_registry(args.registry)
    if args.surface:
        surfaces = [s for s in surfaces if s["name"] == args.surface]
        if not surfaces:
            print(f"ERROR: unknown surface: {args.surface}", file=sys.stderr)
            return 2
    return run_capture(
        surfaces,
        args.archive_root,
        args.vendor_root,
        report_path=args.report,
        lineage_log=args.lineage_log,
        lineage_registry=args.registry,
    )


if __name__ == "__main__":
    sys.exit(main())
