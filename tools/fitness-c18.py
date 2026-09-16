#!/usr/bin/env python3
"""C18 v2: a goal with code has a use-case test; that test is not the noun suite.

If goals/<id> has implementation .py and no tests → missing-goal-test.
If a goal test mentions a token from domain/*/adjectives.txt → copied-adjective.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> missing-goal-test|copied-adjective <detail>
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


def goal_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    for goals in collect_named(root, "goals"):
        found.extend(p for p in goals.iterdir() if p.is_dir() and not is_skipped(p))
    return found


def impl_files(goal: Path) -> list[Path]:
    return [
        p for p in goal.glob("*.py")
        if p.is_file()
        and not p.name.startswith("test_")
        and not p.name.endswith("_test.py")
    ]


def test_files(goal: Path) -> list[Path]:
    files: list[Path] = []
    tests = goal / "tests"
    if tests.is_dir():
        files.extend(
            p for p in tests.rglob("*")
            if p.is_file() and p.suffix in SOURCE_EXTS and not is_skipped(p)
        )
    files.extend(
        p for p in goal.iterdir()
        if p.is_file()
        and p.suffix in SOURCE_EXTS
        and (p.name.startswith("test_") or p.name.endswith("_test.py"))
    )
    return files


def token_in_text(token: str, text: str) -> bool:
    return (
        re.search(rf'["\']{re.escape(token)}["\']', text) is not None
        or re.search(rf"\b{re.escape(token)}\b", text) is not None
    )


def scan_one(scan_root: Path) -> list[tuple[str, str, str]]:
    tokens = adjective_tokens(scan_root)
    violations: list[tuple[str, str, str]] = []
    for goal in goal_dirs(scan_root):
        if not impl_files(goal):
            continue
        tests = test_files(goal)
        if not tests:
            violations.append((rel(goal), "missing-goal-test", goal.name))
            continue
        for path in tests:
            text = path.read_text(errors="replace")
            for token in tokens:
                if token_in_text(token, text):
                    violations.append((rel(path), "copied-adjective", token))
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
            path, kind, detail = item
            print(f"VIOLATION {path} {kind} {detail}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
