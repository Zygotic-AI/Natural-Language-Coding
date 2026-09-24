#!/usr/bin/env python3
"""C3 / R3 v1: a noun must not call another noun's verb.


Owned verbs = `def name(` in domain/<noun>/*.py (not tests).
If domain/<other>/*.py contains `.that_verb(`, that is orchestration on the
wrong noun.

One noun in the tree → skip (MET). Common names (get, set, …) are ignored.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> cross-noun <verb> owned-by <noun>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
DEF = re.compile(r"^\s+def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.M)
CALL = re.compile(r"\.[A-Za-z_][A-Za-z0-9_]*\s*\(")
SKIP_VERBS = {
    "get", "set", "update", "append", "pop", "keys", "values", "items",
    "read", "write", "load", "save", "format", "join", "split", "replace",
    "__init__", "__repr__", "__str__",
}


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
        found.extend(p for p in domain.iterdir() if p.is_dir() and not is_skipped(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("domain"):
            if named.is_dir() and named.name == "domain" and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir() and not is_skipped(p))
    return found


def noun_py(noun_dir: Path) -> list[Path]:
    return [
        p for p in noun_dir.rglob("*.py")
        if p.is_file() and not is_skipped(p) and "tests" not in p.parts
        and not p.name.startswith("test_")
    ]


def owned_verbs(noun_dir: Path) -> set[str]:
    names: set[str] = set()
    for path in noun_py(noun_dir):
        text = path.read_text(errors="replace")
        for match in DEF.finditer(text):
            name = match.group(1)
            if name not in SKIP_VERBS:
                names.add(name)
    return names


def scan_one(scan_root: Path) -> list[tuple[str, str, str]]:
    nouns = noun_dirs(scan_root)
    owner: dict[str, str] = {}
    for n in nouns:
        for verb in owned_verbs(n):
            owner.setdefault(verb, n.name)
    if len({n.name for n in nouns}) < 2:
        return []
    violations = []
    for n in nouns:
        mine = owned_verbs(n)
        for path in noun_py(n):
            text = path.read_text(errors="replace")
            for match in CALL.finditer(text):
                verb = match.group(0)[1:].split("(")[0].strip()
                if verb in SKIP_VERBS or verb in mine:
                    continue
                if verb in owner and owner[verb] != n.name:
                    violations.append((rel(path), verb, owner[verb]))
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
            path, verb, owner = item
            print(f"VIOLATION {path} cross-noun {verb} owned-by {owner}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
