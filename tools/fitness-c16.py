#!/usr/bin/env python3
"""C16 v1: each adjectives.txt token appears in the noun's tests.

Not C19 (two implementations). Tests are allowed to name adjectives.
Not C17 (verbs). Tokens only.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <noun> untested-adjective <token>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

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


def load_tokens(noun: Path) -> list[str]:
    path = noun / "adjectives.txt"
    if not path.is_file():
        return []
    out = []
    for raw in path.read_text(errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            out.append(line)
    return out


def test_files(noun: Path) -> list[Path]:
    files = []
    tests = noun / "tests"
    if tests.is_dir():
        files.extend(p for p in tests.rglob("*") if p.is_file() and p.suffix in SOURCE_EXTS)
    files.extend(
        p for p in noun.iterdir()
        if p.is_file() and p.suffix in SOURCE_EXTS
        and (p.name.startswith("test_") or p.name.endswith("_test.py"))
    )
    return sorted(set(files))


def token_in_text(token: str, text: str) -> bool:
    return (
        re.search(rf'["\']{re.escape(token)}["\']', text) is not None
        or re.search(rf"\b{re.escape(token)}\b", text) is not None
    )


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    violations = []
    for noun in noun_dirs(scan_root):
        tokens = load_tokens(noun)
        if not tokens:
            continue
        tests = test_files(noun)
        blob = "\n".join(p.read_text(errors="replace") for p in tests)
        for token in tokens:
            if not token_in_text(token, blob):
                violations.append((rel(noun), token))
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
            noun, token = item
            print(f"VIOLATION {noun} untested-adjective {token}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
