#!/usr/bin/env python3
"""Zero-dependency relative-link checker for the Markdown documentation.

Usage:
    python3 scripts/check_links.py

Only local relative links are checked. External URLs, anchors and mail links
are ignored. Links inside fenced code blocks are ignored as well. A small
allowlist covers links that intentionally describe a fictional example project
inside README/template tutorial sections.
"""

from __future__ import annotations

import fnmatch
import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "dist", "build", "out"}

INLINE_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
EXTERNAL = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

# These documents are tutorials that show hypothetical README files. Their
# sample links point at a fictional project and must not be treated as broken
# links of this repository.
EXAMPLE_SOURCES = {
    "docs/15-readme-docs.md",
    "en/docs/15-readme-docs.md",
    "docs/23-team-collaboration.md",
    "en/docs/23-team-collaboration.md",
    "docs/W6-bilingual-readme.md",
    "en/docs/W6-bilingual-readme.md",
    "docs/00-team-collaboration-guide.md",
    "en/docs/00-team-collaboration-guide.md",
    "docs/X8-technical-writing-github.md",
    "en/docs/X8-technical-writing-github.md",
    "docs/Y1-open-source-project-management.md",
    "en/docs/Y1-open-source-project-management.md",
}

EXAMPLE_TARGETS = (
    "docs/*",
    "docs/",
    "examples/",
    "getting-started.md",
    "commands/*",
    "guides/*",
    "faq.md",
    "configuration.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "README_CN.md",
    "README_JA.md",
    "CHANGELOG.md",
    "图片地址",
    "image URL",
)


def strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks, respecting longer fences and info strings."""
    kept: list[str] = []
    fence_char: str | None = None
    fence_len = 0

    for line in text.splitlines():
        match = FENCE.match(line)
        if fence_char is None:
            if match:
                fence_char = match.group(1)[0]
                fence_len = len(match.group(1))
                continue
            kept.append(line)
            continue

        if (
            match
            and match.group(1)[0] == fence_char
            and len(match.group(1)) >= fence_len
            and match.group(2).strip() == ""
        ):
            fence_char = None
            fence_len = 0

    return "\n".join(kept)


def is_allowed_example(source: str, target: str) -> bool:
    if source not in EXAMPLE_SOURCES:
        return False
    return any(fnmatch.fnmatch(target, pattern) for pattern in EXAMPLE_TARGETS)


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".md"):
                files.append(Path(dirpath) / filename)
    return sorted(files)


def check_file(path: Path) -> list[tuple[str, str]]:
    rel_source = path.relative_to(ROOT).as_posix()
    text = strip_fenced_code(path.read_text(encoding="utf-8"))
    text = re.sub(r"`[^`\n]*`", "", text)
    broken: list[tuple[str, str]] = []

    for match in list(INLINE_LINK.finditer(text)) + list(REFERENCE_LINK.finditer(text)):
        raw = match.group(1).strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        if not raw or raw.startswith("#"):
            continue
        if EXTERNAL.match(raw) or raw.startswith("//"):
            continue

        target = urllib.parse.unquote(raw.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue
        if is_allowed_example(rel_source, target):
            continue

        if target.startswith("/"):
            candidate = ROOT / target.lstrip("/")
        else:
            candidate = (path.parent / target).resolve()

        if not candidate.exists():
            broken.append((rel_source, raw))

    return broken


def main() -> int:
    broken: list[tuple[str, str]] = []
    files = iter_markdown_files()
    for path in files:
        broken.extend(check_file(path))

    if broken:
        print(f"Found {len(broken)} broken relative link(s):\n")
        for source, target in broken:
            print(f"  {source}: {target}")
        return 1

    print(f"Link check passed: {len(files)} Markdown files, 0 broken relative links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
