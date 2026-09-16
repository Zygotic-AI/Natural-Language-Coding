#!/usr/bin/env python3
"""C18 v1: goal tests must not copy the noun's adjective tokens.

If goals/**/tests (or test_*.py under a goal) mention a token from
domain/<noun>/adjectives.txt, that is a copied adjective suite.

No goal tests → skip (MET). That is not proof the use-case is tested.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> copied-adjective <token>
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


def collect_named(root: Path, name: str) -> list[Path]:
    found: list[Path] = []
    direct = root / name
    if direct.is_dir():
        found.append(direct)
    examples = root / "examples"
    if examples.is_dir():
        for p in examples.rglob(name):
            if p.is_dir() and p.name == name and not is_skipped(p):
                found.append(p)
    return found


def adjective_tokens(root: Path) -> list[str]:
    tokens: list[str] = []
    for domain in collect_named(root, "domain"):
        for noun in domain.iterdir():
            path = noun / "adjectives.txt"
            if not path.is_file():
                continue
            for raw in path.read_text(errors="replace").splitlines():
                line = raw.split("#", 1)[0].strip()
                if line and line not in tokens:
                    tokens.append(line)
    return tokens


def goal_test_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for goals in collect_named(root, "goals"):
        for path in goals.rglob("*"):
            if not path.is_file() or path.suffix not in SOURCE_EXTS:
                continue
            if is_skipped(path):
                continue
            if "tests" in path.parts or path.name.startswith("test_") or path.name.endswith("_test.py"):
                files.append(path)
    return sorted(set(files))


def token_in_text(token: str, text: str) -> bool:
    return (
        re.search(rf'["\']{re.escape(token)}["\']', text) is not None
        or re.search(rf"\b{re.escape(token)}\b", text) is not None
    )


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    tokens = adjective_tokens(scan_root)
    if not tokens:
        return []
    violations = []
    for path in goal_test_files(scan_root):
        text = path.read_text(errors="replace")
        for token in tokens:
            if token_in_text(token, text):
                violations.append((rel(path), token))
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
            path, token = item
            print(f"VIOLATION {path} copied-adjective {token}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
