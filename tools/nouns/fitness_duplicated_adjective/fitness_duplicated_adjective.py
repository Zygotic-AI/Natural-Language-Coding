#!/usr/bin/env python3
"""C19 v1: the same adjective is implemented in two files of one noun.


Not R24 (token outside the noun). This gate stays inside domain/<noun>/.

For each noun with adjectives.txt, each token must appear in at most one
source file in that noun directory. Two files both containing `== "void"`
is a second implementation.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <noun> <token> <path> <path>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_EXTS = {".ts", ".js", ".py", ".mjs", ".cjs", ".tsx", ".jsx"}
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


def is_test_path(path: Path) -> bool:
    return (
        "tests" in path.parts
        or path.name.startswith("test_")
        or path.name.endswith("_test.py")
        or path.name.endswith("_test.ts")
    )


def source_files(noun: Path) -> list[Path]:
    return sorted(
        p for p in noun.rglob("*")
        if p.is_file()
        and p.suffix in SOURCE_EXTS
        and not is_skipped(p)
        and not is_test_path(p)
    )



def token_in_file(token: str, text: str) -> bool:
    return (
        re.search(rf'["\']{re.escape(token)}["\']', text) is not None
        or re.search(rf"\b{re.escape(token)}\b", text) is not None
    )


def scan_one(scan_root: Path) -> list[tuple[str, str, list[str]]]:
    violations = []
    for noun in noun_dirs(scan_root):
        tokens = load_tokens(noun)
        if not tokens:
            continue
        files = source_files(noun)
        for token in tokens:
            hits = []
            for path in files:
                text = path.read_text(errors="replace")
                if token_in_file(token, text):
                    hits.append(rel(path))
            if len(hits) >= 2:
                violations.append((noun.name, token, hits))
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
        for noun, token, hits in scan_one(scan_root):
            key = (noun, token, tuple(hits))
            if key in seen:
                continue
            seen.add(key)
            printed.append(key)
            print(f"VIOLATION {noun} {token} " + " ".join(hits))
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
