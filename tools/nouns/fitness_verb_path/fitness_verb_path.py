#!/usr/bin/env python3
"""R6/C5 v1: no persistence / mutation escape in goal or adapter trees.


This is not full R6. Full R6 is "every noun mutation is a public verb."
V1 only fails obvious escapes outside the noun module:

  ORM / repo: .save( .update( .delete( .upsert( .commit( .execute( .raw(
  SQL keywords: INSERT INTO, UPDATE <ident>, DELETE FROM
  Reflection: setattr(

Field assignment (invoice.status =) is R5 / fitness-no-noun-field-writes.py.
Do not treat this tool as a bind for full R6 until more escapes are covered.

Input: optional argv roots. No args → hub ROOT (goals/, adapters/, workflows/,
  examples/** of those). Noun trees are not scanned.

Output: VIOLATION <path>:<line> <kind>
        RESULT:MET|NOT_MET

Failure mode: exit 0 = MET; exit 1 = NOT_MET. No silent exception swallow.
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
    ("orm-save", re.compile(r"\.\s*save\s*\(")),
    ("orm-update", re.compile(r"\.\s*update\s*\(")),
    ("orm-delete", re.compile(r"\.\s*delete\s*\(")),
    ("orm-upsert", re.compile(r"\.\s*upsert\s*\(")),
    ("orm-commit", re.compile(r"\.\s*commit\s*\(")),
    ("orm-execute", re.compile(r"\.\s*execute\s*\(")),
    ("orm-raw", re.compile(r"\.\s*raw\s*\(")),
    ("sql-insert", re.compile(r"\bINSERT\s+INTO\b", re.I)),
    ("sql-update", re.compile(r"\bUPDATE\s+[A-Za-z_][A-Za-z0-9_]*", re.I)),
    ("sql-delete", re.compile(r"\bDELETE\s+FROM\b", re.I)),
    ("setattr", re.compile(r"\bsetattr\s*\(")),
]


def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def source_files(tree: Path) -> list[Path]:
    if not tree.is_dir():
        return []
    out = []
    for path in tree.rglob("*"):
        if not path.is_file() or path.suffix not in SOURCE_EXTS:
            continue
        if is_skipped_dir(path):
            continue
        out.append(path)
    return sorted(out)


def outside_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in OUTSIDE_DIR_NAMES:
        files.extend(source_files(root / name))
    examples = root / "examples"
    if examples.is_dir():
        for path in examples.rglob("*"):
            if not path.is_dir() or path.name not in OUTSIDE_DIR_NAMES:
                continue
            if is_skipped_dir(path):
                continue
            files.extend(source_files(path))
    return sorted(set(files))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def is_comment(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("#") or stripped.startswith("//")


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    violations: list[tuple[str, int, str]] = []
    for path in outside_files(scan_root):
        text = path.read_text(errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if is_comment(line):
                continue
            for kind, pattern in PATTERNS:
                if pattern.search(line):
                    violations.append((rel(path), lineno, kind))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    violations: list[tuple[str, int, str]] = []
    for scan_root in scan_roots:
        violations.extend(scan_one(scan_root))
    seen: set[tuple[str, int, str]] = set()
    printed = []
    for item in violations:
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
