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
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def carousel_class(attrs: dict[str, str | None], suffix: str) -> bool:
    return any(
        token.startswith("HeroCarousel-") and token.endswith("__" + suffix)
        for token in (attrs.get("class") or "").split()
    )


class Index(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str | None]]] = []
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
        in_main = any(t == "main" for t, _ in self.stack)
        in_head = any(t == "head" for t, _ in self.stack)
        in_carousel = any(carousel_class(a, "hero-carousel") for _, a in self.stack)
        if tag == "link" and in_head and "canonical" in (attrs.get("rel") or "").split():
            self.canonicals.append(attrs.get("href"))
        if tag == "main":
            self.main_count += 1
        if in_main and carousel_class(attrs, "hero-carousel"):
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
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                if tag == "main":
                    self.main_closed += 1
                del self.stack[i:]
                return

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
        parser = Index()
        parser.feed(sys.stdin.read())
        parser.close()
        article = parser.article()
    except (ValueError, UnicodeError) as exc:
        print(f"ERROR: engineering article extraction indeterminate: {exc}", file=sys.stderr)
        return 2
    print(f'href="{article}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
