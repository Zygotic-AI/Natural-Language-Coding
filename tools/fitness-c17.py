#!/usr/bin/env python3
"""C17 v1: each public noun-verb name appears in the noun's tests.

Does not check success vs precondition vs preservation. That stays unbound.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <noun> untested-verb <verb>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
SOURCE_EXTS = {".py", ".ts", ".js"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def noun_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        found.extend(p for p in domain.iterdir() if p.is_dir())
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("domain"):
            if named.is_dir() and named.name == "domain" and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir())
    return sorted(set(found))


def verb_names(noun: Path) -> list[str]:
    schema = noun / "schemas" / "verbs.schema.json"
    if not schema.is_file():
        return []
    try:
        data = json.loads(schema.read_text())
    except json.JSONDecodeError:
        return []
    verbs = data.get("verbs")
    if not isinstance(verbs, dict):
        return []
    return [str(k) for k in verbs.keys()]


def test_blob(noun: Path) -> str:
    files = []
    tests = noun / "tests"
    if tests.is_dir():
        files.extend(p for p in tests.rglob("*") if p.is_file() and p.suffix in SOURCE_EXTS)
    files.extend(
        p for p in noun.iterdir()
        if p.is_file() and p.suffix in SOURCE_EXTS
        and (p.name.startswith("test_") or p.name.endswith("_test.py"))
    )
    return "\n".join(p.read_text(errors="replace") for p in files)


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    violations = []
    for noun in noun_dirs(scan_root):
        names = verb_names(noun)
        if not names:
            continue
        blob = test_blob(noun)
        for name in names:
            if re.search(rf"\b{re.escape(name)}\b", blob) is None:
                violations.append((rel(noun), name))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            noun, name = item
            print(f"VIOLATION {noun} untested-verb {name}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
