"""UC16 v0: list implementation languages under domain/ and goals/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BOUNDARY = "bba-emit"

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


def main(argv: list[str] | None = None) -> int:
    args_list = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="UC16 code-pack language inventory (v0)")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args(args_list)
    root = args.root.resolve()
    found = scan(root)
    if not found:
        print("LANGUAGE_SCAN: empty")
        return 0
    print(f"LANGUAGE_SCAN: root={root}")
    for lang in sorted(found):
        print(f"  {lang}: {len(found[lang])} file(s)")
    return 0
