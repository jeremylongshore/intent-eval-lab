"""The engineering signal comes from the index's featured article, not navigation."""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/extract-engineering-article.py"


def page(content):
    return (
        '<html><head><link rel="canonical" href="https://www.anthropic.com/engineering">'
        '</head><body><nav><a href="/research/navigation-decoy">Navigation</a></nav>'
        f'<main>{content}</main></body></html>'
    )


def carousel(path="/research/First-article"):
    return (
        '<div class="HeroCarousel-module-scss-module__build__hero-carousel">'
        f'<a class="HeroCarousel-module-scss-module__build__slide-link" href="{path}">Image</a>'
        '<a href="/engineering">Engineering</a>'
        f'<a class="HeroCarousel-module-scss-module__build__carousel-info-link" href="{path}">First</a>'
        '<a class="HeroCarousel-module-scss-module__build__carousel-info-link" href="/research/second">Second</a>'
        '</div>'
    )


def run(text):
    return subprocess.run([sys.executable, str(SCRIPT)], input=text, text=True, capture_output=True)


def test_current_featured_article_ignores_navigation_and_preserves_case():
    result = run(page(carousel()))
    assert result.returncode == 0, result.stderr
    assert result.stdout == 'href="/research/First-article"\n'


def test_legacy_nonempty_sentinel_keeps_exact_hash_bytes():
    text = page('<a href="/engineering/old-article">First</a><a href="/engineering/later">Later</a>')
    result = run(text)
    expected = b'href="/engineering/old-article"\n'
    assert result.returncode == 0, result.stderr
    assert result.stdout.encode() == expected
    assert hashlib.sha256(result.stdout.encode()).digest() == hashlib.sha256(expected).digest()


def test_actual_frozen_capture_preserves_original_baseline():
    body = (ROOT / "specs/_vendor/anthropic-engineering/snapshot.html").read_text()
    expected = re.search(r'href="/engineering/[a-z0-9-]+"', body).group() + "\n"
    result = run(body)
    assert result.returncode == 0, result.stderr
    assert result.stdout == expected
    baseline = (ROOT / "specs/snapshots/.sha/anthropic-engineering.sha").read_text().strip()
    assert hashlib.sha256(result.stdout.encode()).hexdigest() == baseline


def test_capture_shape_requires_index_identity_and_supports_both_path_layouts():
    registry = json.loads((ROOT / "specs/upstream-surface-registry.v1.json").read_text())
    capture = next(s["capture"] for s in registry["surfaces"] if s["name"] == "anthropic-engineering")
    pattern = capture["expect_regex"]
    assert capture["min_bytes"] == 16384
    assert re.search(pattern, page(carousel()))
    assert re.search(pattern, page('<a href="/engineering/old">Legacy</a>'))
    assert not re.search(pattern, '<a href="/research/decoy">Not the index</a>')
    assert not re.search(pattern, page('No article links.'))
    assert not re.search(pattern, page(carousel()).replace('rel="canonical"', 'data-rel="canonical"'))
    assert not re.search(pattern, page(carousel()).replace('href=', 'data-href='))


@pytest.mark.parametrize(
    "text",
    [
        "",
        '<html><title>Verify you are human</title><a href="/engineering/decoy">Challenge</a></html>',
        page('<nav><a href="/research/navigation-only">Unrelated</a></nav>'),
        page(carousel()).replace('rel="canonical"', 'rel="alternate"'),
        page(carousel()).replace('https://www.anthropic.com/engineering', 'https://www.anthropic.com/research'),
        page(carousel() + carousel('/research/other-carousel')),
        page(carousel()).replace('</main>', '</main><main></main>'),
        page(carousel()).replace('href="/research/First-article"', 'href="https://evil.example/research/first"'),
        page(carousel()).replace('href="/research/First-article"', 'href="/research/first?tracking=1"'),
        page(carousel()).replace('__carousel-info-link', '__unrecognized-link'),
        page(carousel()).replace('/research/First-article">First', '/research/conflicting">First'),
        page(carousel()).replace('href="/engineering">Engineering', 'href="/research">Research'),
        page('<script>"href=\\"/engineering/script-decoy\\""</script>'),
    ],
)
def test_missing_interstitial_or_ambiguous_signal_is_indeterminate(text):
    result = run(text)
    assert result.returncode == 2
    assert result.stdout == ""
    assert "ERROR:" in result.stderr


def test_watcher_uses_the_parser_and_preserves_fetch_failure(tmp_path):
    source = (ROOT / 'scripts/spec-drift-check.sh').read_text().split('# Source registry:', 1)[0]
    source = 'set -euo pipefail\nSCRIPT_DIR="$ENGINEERING_SCRIPTS"\n' + source[source.index('hash_nonempty()'):]
    fixture = tmp_path / 'index.html'
    fixture.write_text(page(carousel()))
    # Exercise the owning function itself, without polling any upstream URL.
    command = source + '\ncurl() { cat "$ENGINEERING_FIXTURE"; }\nfetch_anthropic_engineering\n'
    env = os.environ.copy()
    env['ENGINEERING_FIXTURE'] = str(fixture)
    env['ENGINEERING_SCRIPTS'] = str(ROOT / 'scripts')
    result = subprocess.run(['bash', '-c', command, str(ROOT / 'scripts/spec-drift-check.sh')], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == hashlib.sha256(b'href="/research/First-article"\n').hexdigest()
    failed = source + '\ncurl() { return 22; }\nfetch_anthropic_engineering\n'
    result = subprocess.run(['bash', '-c', failed, str(ROOT / 'scripts/spec-drift-check.sh')], env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert result.stdout == ''
