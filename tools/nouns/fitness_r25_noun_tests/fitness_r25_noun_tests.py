#!/usr/bin/env python3
"""R25 v1: a noun with declared fields/adjectives has tests next to it.


domain/<noun>/ with fields.txt or adjectives.txt must contain tests/ and at
least one *.py there (or test_*.py / *_test.py in the noun dir).

Does not read the tests. C16–C18 stay unbound.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <noun> missing-noun-tests
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}


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


def has_decl(noun: Path) -> bool:
    return (noun / "fields.txt").is_file() or (noun / "adjectives.txt").is_file()


def has_tests(noun: Path) -> bool:
    tests = noun / "tests"
    if tests.is_dir() and any(p.suffix == ".py" for p in tests.iterdir() if p.is_file()):
        return True
    for p in noun.iterdir():
        if p.is_file() and p.suffix == ".py" and (
            p.name.startswith("test_") or p.name.endswith("_test.py")
        ):
            return True
    return False


def scan_one(scan_root: Path) -> list[str]:
    missing = []
    for noun in noun_dirs(scan_root):
        if not has_decl(noun):
            continue
        if not has_tests(noun):
            missing.append(rel(noun))
    return missing


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[str] = set()
    printed: list[str] = []
    for scan_root in scan_roots:
        for noun in scan_one(scan_root):
            if noun in seen:
                continue
            seen.add(noun)
            printed.append(noun)
            print(f"VIOLATION {noun} missing-noun-tests")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
