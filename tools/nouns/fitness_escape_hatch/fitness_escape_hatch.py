#!/usr/bin/env python3
"""R33 / C26: reflection, ORM, and SQL escape hatches in goal/adapter trees.


Fails in goals/, adapters/, workflows/:

  dict-hatch / vars-hatch / exec-hatch / eval-hatch
  setattr-hatch — setattr(
  save-hatch    — .save(
  sql-hatch     — .execute( / .executemany( / .raw( / SELECT|INSERT|UPDATE|DELETE

obj.field = is R5.
"""








from __future__ import annotations

BOUNDARY = "bba-emit"



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_EXTS = {".ts", ".js", ".py", ".mjs", ".cjs", ".tsx", ".jsx"}
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
OUTSIDE_DIR_NAMES = ("goals", "workflows", "adapters")

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("dict-hatch", re.compile(r"\.__dict__\b")),
    ("vars-hatch", re.compile(r"\bvars\s*\(")),
    ("exec-hatch", re.compile(r"\bexec\s*\(")),
    ("eval-hatch", re.compile(r"\beval\s*\(")),
    ("setattr-hatch", re.compile(r"\bsetattr\s*\(")),
    ("save-hatch", re.compile(r"\.save\s*\(")),
    ("sql-hatch", re.compile(r"\.(?:execute|executemany|raw)\s*\(")),
    ("sql-hatch", re.compile(r"\b(?:SELECT|INSERT|UPDATE|DELETE)\b")),
]



def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def source_files(tree: Path) -> list[Path]:
    if not tree.is_dir():
        return []
    return sorted(
        p for p in tree.rglob("*")
        if p.is_file()
        and p.suffix in SOURCE_EXTS
        and not is_skipped_dir(p)
        and "tests" not in p.parts
        and not p.name.startswith("test_")
    )



def outside_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in OUTSIDE_DIR_NAMES:
        files.extend(source_files(root / name))
    examples = root / "examples"
    if examples.is_dir():
        for path in examples.rglob("*"):
            if path.is_dir() and path.name in OUTSIDE_DIR_NAMES and not is_skipped_dir(path):
                files.extend(source_files(path))
    return sorted(set(files))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def is_comment(line: str) -> bool:
    s = line.strip()
    return s.startswith("#") or s.startswith("//")


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    violations: list[tuple[str, int, str]] = []
    for path in outside_files(scan_root):
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            if is_comment(line):
                continue
            for kind, pat in PATTERNS:
                if pat.search(line):
                    violations.append((rel(path), lineno, kind))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, int, str]] = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, lineno, kind = item
            print(f"VIOLATION {path}:{lineno} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
