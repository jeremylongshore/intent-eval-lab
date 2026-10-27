#!/usr/bin/env python3
"""Emit the engineering index's first article as a nonempty href sentinel.

Offline stdin parser. Exit 2 means indeterminate and emits no stdout. The
sentinel retains the old grep output bytes, including its trailing newline.
The observed first featured link uses a /research/ path; selecting any research
link would mistake site navigation for an engineering article.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser

ARTICLE = re.compile(r"/(engineering|research)/[A-Za-z0-9][A-Za-z0-9-]*")
MAX_INPUT_BYTES = 4 * 1024 * 1024
MAX_OPEN_ELEMENTS = 256
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def carousel_class(attrs: dict[str, str | None], suffix: str) -> bool:
    return any(
        token.startswith("HeroCarousel-") and token.endswith("__" + suffix)
        for token in (attrs.get("class") or "").split()
    )


class Index(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool, bool, bool]] = []
        self.positions: dict[str, list[int]] = {}
        self.in_main = False
        self.in_head = False
        self.in_carousel = False
        self.canonicals: list[str | None] = []
        self.main_count = 0
        self.main_closed = 0
        self.carousel_count = 0
        self.info: list[str | None] = []
        self.slides: list[str | None] = []
        self.legacy: list[str] = []
        self.engineering_topic = False

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        in_main, in_head, in_carousel = self.in_main, self.in_head, self.in_carousel
        is_carousel = carousel_class(attrs, "hero-carousel")
        if tag == "link" and in_head and "canonical" in (attrs.get("rel") or "").split():
            self.canonicals.append(attrs.get("href"))
        if tag == "main":
            self.main_count += 1
        if in_main and is_carousel:
            self.carousel_count += 1
        if tag == "a" and in_main:
            href = attrs.get("href")
            if in_carousel:
                if carousel_class(attrs, "carousel-info-link"):
                    self.info.append(href)
                if carousel_class(attrs, "slide-link"):
                    self.slides.append(href)
                if href == "/engineering":
                    self.engineering_topic = True
            elif href and re.fullmatch(r"/engineering/[a-z0-9-]+", href):
                self.legacy.append(href)
        if tag not in VOID:
            if len(self.stack) >= MAX_OPEN_ELEMENTS:
                raise ValueError("HTML nesting exceeds supported limit")
            self.positions.setdefault(tag, []).append(len(self.stack))
            self.stack.append((tag, in_main, in_head, in_carousel))
            self.in_main = in_main or tag == "main"
            self.in_head = in_head or tag == "head"
            self.in_carousel = in_carousel or is_carousel

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        matches = self.positions.get(tag)
        if not matches:
            return
        index = matches[-1]
        _, self.in_main, self.in_head, self.in_carousel = self.stack[index]
        while len(self.stack) > index:
            popped, *_ = self.stack.pop()
            positions = self.positions[popped]
            positions.pop()
            if not positions:
                del self.positions[popped]
        if tag == "main":
            self.main_closed += 1

    def article(self) -> str:
        if self.canonicals not in (
            ["https://www.anthropic.com/engineering"],
            ["https://www.anthropic.com/engineering/"],
        ):
            raise ValueError("missing or ambiguous engineering index canonical URL")
        if self.main_count != 1 or self.main_closed != 1:
            raise ValueError("missing, unclosed or ambiguous main content")
        if self.carousel_count:
            if self.carousel_count != 1 or not self.info or not self.slides or not self.engineering_topic:
                raise ValueError("missing or ambiguous engineering featured carousel")
            href = self.info[0]
            if not isinstance(href, str) or not ARTICLE.fullmatch(href) or self.slides[0] != href:
                raise ValueError("featured image and title do not identify one supported article path")
            return href
        if not self.legacy:
            raise ValueError("no supported engineering article signal")
        return self.legacy[0]


def main() -> int:
    try:
        body = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(body) > MAX_INPUT_BYTES:
            raise ValueError("input size exceeds supported limit")
        parser = Index()
        parser.feed(body.decode("utf-8"))
        parser.close()
        article = parser.article()
    except (ValueError, UnicodeError) as exc:
        print(f"ERROR: engineering article extraction indeterminate: {exc}", file=sys.stderr)
        return 2
    print(f'href="{article}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
