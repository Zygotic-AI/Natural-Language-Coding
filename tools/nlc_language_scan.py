#!/usr/bin/env python3
"""UC16 v0: list implementation languages under domain/ and goals/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nlc_requirements import hub_tool

EXT = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
}


def scan(root: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for dirname in ("domain", "goals"):
        base = root / dirname
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            lang = EXT.get(path.suffix.lower())
            if not lang:
                continue
            rel = str(path.relative_to(root)).replace("\\", "/")
            out.setdefault(lang, []).append(rel)
    return out


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="UC16 code-pack language inventory (v0)")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    found = scan(root)
    if not found:
        print("LANGUAGE_SCAN: empty")
        return 0
    print(f"LANGUAGE_SCAN: root={root}")
    for lang in sorted(found):
        print(f"  {lang}: {len(found[lang])} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
