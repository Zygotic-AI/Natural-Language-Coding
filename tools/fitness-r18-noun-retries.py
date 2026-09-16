#!/usr/bin/env python3
"""R18 v1: retry/compensation orchestration does not live inside the noun.

domain/<noun>/*.py (not tests) must not mention temporalio, retry_policy,
backoff, compensate(, @workflow, or `for attempt in`.

Does not prove the *goal* owns retries. C15 is the caller side.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path>:<line> noun-retry
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
HIT = re.compile(
    r"temporalio|retry_policy|backoff|compensate\s*\(|@workflow|for\s+attempt\s+in",
    re.I,
)


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def noun_py(root: Path) -> list[Path]:
    files: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        files.extend(p for p in domain.rglob("*.py") if p.is_file() and not is_skipped(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("domain"):
            if named.is_dir() and named.name == "domain" and not is_skipped(named):
                files.extend(p for p in named.rglob("*.py") if p.is_file() and not is_skipped(p))
    return sorted(set(files))


def scan_one(scan_root: Path) -> list[tuple[str, int]]:
    violations = []
    for path in noun_py(scan_root):
        if "tests" in path.parts or path.name.startswith("test_"):
            continue
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if HIT.search(line):
                violations.append((rel(path), lineno))
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
            path, lineno = item
            print(f"VIOLATION {path}:{lineno} noun-retry")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
