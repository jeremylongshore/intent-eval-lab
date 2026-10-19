"""Commit-bound snapshot review and actual promotion-shell contracts, offline."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("snapshot_review", ROOT / "scripts/snapshot-review.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE).decode().strip()


def capture(root, text, *, status="FETCH_OK", digest=None):
    data = text.encode()
    sha = digest or review.hashlib.sha256(data).hexdigest()
    prefix = root / "specs/_vendor/agentskills-spec"
    prefix.mkdir(parents=True, exist_ok=True)
    (prefix / "snapshot.md").write_bytes(data)
    meta = {"surface_id": "agentskills-spec", "sha256": sha, "bytes": len(data)}
    record = root / "archive/raw/agentskills-spec/capture.meta.json"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps({**meta, "status": status}))
    (prefix / "vendor-meta.json").write_text(json.dumps({**meta, "source_raw_record": str(record.relative_to(root))}))


def commit(root):
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture")
    return git(root, "rev-parse", "HEAD")


@pytest.fixture()
def repository(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "Fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    (root / "specs").mkdir()
    (root / review.REGISTRY).write_text(
        json.dumps({"surfaces": [{"name": "agentskills-spec", "contract": "skill-frontmatter"}]})
    )
    (root / "scripts").symlink_to(ROOT / "scripts", target_is_directory=True)
    capture(root, "| `name` | Yes | Name. |\n| `license` | No | License. |\n")
    base = commit(root)
    return root, base


@pytest.mark.parametrize(
    ("new", "expected"),
    [
        ("| `name` | Yes | Name. |\n| `license` | No | License. |\n| `icon` | No | Glyph. |\n", "additive"),
        ("| `name` | Yes | Name. |\n| `license` | Yes | License. |\n", "potential-breaking"),
        ("| `name` | Yes | Name. |\n", "potential-breaking"),
        (
            "New normative prose not covered by the table.\n| `name` | Yes | Name. |\n| `license` | No | License. |\n",
            "unchanged-projection",
        ),
        ("The former field-table anchor is gone.\n", "review-required"),
    ],
)
def test_actual_captured_change_recommendations(repository, new, expected):
    root, base = repository
    capture(root, new)
    head = commit(root)
    # A poisoned working-tree snapshot must not influence a Git-bound report.
    capture(root, "uncommitted bytes")
    report = review.build_report(root, base, head)
    assert report["base_commit"] == base and report["head_commit"] == head
    assert report["surfaces"][0]["recommendation"] == expected
    assert "uncommitted bytes" not in report["surfaces"][0]["diff_excerpt"]
    body = review.render(report, "test/review", "https://github.com/test/review/actions/runs/123")
    assert "Human merge required" in body and "not proof of prose-only" in body
    assert f"/compare/{base}..{head}" in body


@pytest.mark.parametrize(("status", "digest"), [("RATELIMITED", None), ("FETCH_OK", "0" * 64)])
def test_bad_capture_provenance_refused(repository, status, digest):
    root, base = repository
    capture(root, "| `name` | Yes | Changed. |\n", status=status, digest=digest)
    head = commit(root)
    with pytest.raises(ValueError, match="provenance|metadata"):
        review.build_report(root, base, head)


def test_byte_only_change_never_becomes_textual_approval(repository):
    root, base = repository
    # Use a registered surface that intentionally has no field extractor.
    git(root, "mv", "specs/_vendor/agentskills-spec", "specs/_vendor/platform-skills-overview")
    git(root, "mv", "archive/raw/agentskills-spec", "archive/raw/platform-skills-overview")
    for path in [
        root / review.REGISTRY,
        root / "specs/_vendor/platform-skills-overview/vendor-meta.json",
        root / "archive/raw/platform-skills-overview/capture.meta.json",
    ]:
        path.write_text(path.read_text().replace("agentskills-spec", "platform-skills-overview"))
    base = commit(root)
    path = root / "specs/_vendor/platform-skills-overview/snapshot.md"
    data = path.read_bytes() + b"More prose.\n"
    path.write_bytes(data)
    for p in [path.with_name("vendor-meta.json"), root / "archive/raw/platform-skills-overview/capture.meta.json"]:
        value = json.loads(p.read_text())
        value.update(sha256=review.hashlib.sha256(data).hexdigest(), bytes=len(data))
        p.write_text(json.dumps(value))
    report = review.build_report(root, base, commit(root))
    assert report["surfaces"][0]["recommendation"] == "review-required"
    assert "Byte-only" in report["surfaces"][0]["reason"]


def test_no_snapshot_change_and_reused_output(repository, tmp_path):
    root, base = repository
    assert review.build_report(root, base, base)["surfaces"] == []
    out = tmp_path / "existing"
    out.mkdir()
    (out / "report.json").write_text("keep")
    run = subprocess.run(
        [
            "python3",
            str(ROOT / "scripts/snapshot-review.py"),
            "--repo-root",
            str(root),
            "--base",
            base,
            "--head",
            base,
            "--repository",
            "test/review",
            "--run-url",
            "https://github.com/test/review/actions/runs/123",
            "--out-dir",
            str(out),
        ],
        capture_output=True,
        text=True,
    )
    assert run.returncode == 2 and (out / "report.json").read_text() == "keep"


def test_enum_narrowing_and_unrecognized_changes_are_not_additive():
    assert review.recommendation(review.differences({"enum": ["a", "b"]}, {"enum": ["a"]})) == "potential-breaking"
    assert review.recommendation(review.differences({"enum": ["a"]}, {"enum": ["a", "b"]})) == "additive"
    assert review.recommendation(review.differences({"default": 1}, {"default": 2})) == "review-required"
    assert review.differences({"enum": ["a", "b"]}, {"enum": ["b", "a"]}) == []
    assert review.recommendation(review.differences({"default": True}, {"default": 1})) == "review-required"


@pytest.mark.parametrize("existing", ["381", ""])
@pytest.mark.parametrize("bad_capture", [False, True])
def test_actual_workflow_shell_refreshes_review_even_without_new_commits(repository, tmp_path, existing, bad_capture):
    root, base = repository
    capture(
        root,
        "| `name` | Yes | Name. |\n| `license` | Yes | License. |\n",
        status="TRUNCATED" if bad_capture else "FETCH_OK",
    )
    head = commit(root)
    git(root, "branch", "spec-drift/auto-promotion", head)
    git(root, "checkout", "--detach", base)
    git(root, "update-ref", "refs/remotes/origin/main", base)
    git(root, "remote", "add", "origin", str(root))
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls = tmp_path / "gh-calls.jsonl"
    gh = bin_dir / "gh"
    gh.write_text(
        "#!/usr/bin/env python3\nimport sys,json,os\nfrom pathlib import Path\n"
        "args=sys.argv[1:]\n"
        "body=Path(args[args.index('--body-file')+1]).read_text() if '--body-file' in args else None\n"
        "with open(os.environ['GH_CALLS'],'a') as f:f.write(json.dumps({'args':args,'body':body})+'\\n')\n"
        "print(os.environ['EXISTING'] if args[:2]==['pr','list'] else 'https://github.com/test/review/pull/381')\n"
    )
    gh.chmod(0o755)
    workflow = yaml.safe_load((ROOT / ".github/workflows/spec-drift-watch.yml").read_text())
    step = next(s for s in workflow["jobs"]["spec-drift-check"]["steps"] if s.get("id") == "promote")
    env = {
        **os.environ,
        "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
        "EXISTING": existing,
        "GH_CALLS": str(calls),
        "PROMO_BRANCH": "spec-drift/auto-promotion",
        "GITHUB_REF_NAME": "main",
        "GITHUB_REPOSITORY": "test/review",
        "GITHUB_SERVER_URL": "https://github.com",
        "GITHUB_RUN_ID": "123",
        "GITHUB_RUN_ATTEMPT": "1",
        "RUNNER_TEMP": str(tmp_path),
        "GITHUB_OUTPUT": str(tmp_path / "outputs"),
    }
    run = subprocess.run(["bash", "-c", step["run"]], cwd=root, env=env, capture_output=True, text=True, timeout=30)
    if bad_capture:
        assert run.returncode == 1 and "refusing a misleading PR summary" in run.stdout
        assert not calls.exists()
        return
    assert run.returncode == 0, run.stdout + run.stderr
    observed = [json.loads(line) for line in calls.read_text().splitlines()]
    action = observed[-1]
    assert action["args"][:2] == ["pr", "edit" if existing else "create"]
    assert "potential-breaking" in action["body"] and head in action["body"]
    assert "actions/runs/123" in action["body"]
    assert all("merge" not in c["args"] for c in observed)
    report = json.loads((tmp_path / "snapshot-review-123-1/report.json").read_text())
    assert report["head_commit"] == head and report["human_merge_required"] is True
