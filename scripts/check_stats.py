#!/usr/bin/env python3
"""Verify the statistics advertised in README.md against the repository.

Usage:
    python3 scripts/check_stats.py

Definitions:
  * tutorials      = docs/*.md
  * exercises      = exercises/*.md
  * Chinese chars  = CJK characters in docs/*.md
  * content files  = tracked files excluding CI, scripts and the web entry

The script exits non-zero when README.md or en/README.md does not contain the
current numbers, or when an expected count cannot be found.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

# Files that are infrastructure, not tutorial content.
NON_CONTENT_PREFIXES = (
    ".github/workflows/ci.yml",
    "scripts/",
    "index.html",
)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def count_cjk(paths: list[Path]) -> int:
    total = 0
    for path in paths:
        total += len(CJK.findall(path.read_text(encoding="utf-8")))
    return total


def main() -> int:
    docs = sorted((ROOT / "docs").glob("*.md"))
    exercises = sorted((ROOT / "exercises").glob("*.md"))
    files = tracked_files()
    content_files = [
        f for f in files if not any(f == p or f.startswith(p) for p in NON_CONTENT_PREFIXES)
    ]

    tutorial_count = len(docs)
    exercise_count = len(exercises)
    cjk_count = count_cjk(docs)
    content_count = len(content_files)

    expected = {
        "tutorial count": str(tutorial_count),
        "exercise count": str(exercise_count),
        "CJK count": f"{cjk_count:,}",
        "content file count": str(content_count),
    }

    print("Actual repository statistics:")
    for key, value in expected.items():
        print(f"  {key}: {value}")

    failures: list[str] = []

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    en_readme = (ROOT / "en" / "README.md").read_text(encoding="utf-8")

    # Chinese README uses a Markdown table row near the end of the page.
    zh_row = f"| {tutorial_count} 篇 | {exercise_count} 个 | {cjk_count:,} | {content_count} 个 |"
    if zh_row not in readme:
        failures.append(f"README.md is missing statistics row: {zh_row!r}")

    en_row = f"| {tutorial_count} | {exercise_count} | {cjk_count:,} | {content_count} |"
    if en_row not in en_readme:
        failures.append(f"en/README.md is missing statistics row: {en_row!r}")

    if failures:
        print("\nStatistics are out of date:")
        for failure in failures:
            print(f"  - {failure}")
        print("\nUpdate the README tables (and run scripts/build_index.py).")
        return 1

    print("\nREADME statistics match the repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
