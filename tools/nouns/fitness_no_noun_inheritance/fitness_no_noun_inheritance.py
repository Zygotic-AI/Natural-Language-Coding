#!/usr/bin/env python3
"""ADR 0008 v1: nouns must not inherit other nouns (domain/ class bases)."""

from __future__ import annotations



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

CLASS_RE = re.compile(r"^\s*class\s+(\w+)\s*\(([^)]+)\)\s*:", re.M)
CLASS_NAME_RE = re.compile(r"^\s*class\s+(\w+)", re.M)

ALLOWED_BASES = frozenset(
    {
        "object",
        "ABC",
        "Enum",
        "Exception",
        "BaseException",
        "TypedDict",
        "Protocol",
        "Generic",
        "NamedTuple",
        "BaseModel",
    }
)


def domain_class_names(domain: Path) -> set[str]:
    names: set[str] = set()
    for path in domain.rglob("*.py"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in CLASS_NAME_RE.finditer(text):
            names.add(m.group(1))
    return names


def find_violations(tree: Path) -> list[tuple[str, str, str]]:
    domain = tree / "domain"
    if not domain.is_dir():
        return []
    defined = domain_class_names(domain)
    violations: list[tuple[str, str, str]] = []
    for path in domain.rglob("*.py"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = str(path.relative_to(tree)).replace("\\", "/")
        for m in CLASS_RE.finditer(text):
            child = m.group(1)
            for raw in m.group(2).split(","):
                base = raw.strip().split(".")[-1]
                if not base or base in ALLOWED_BASES:
                    continue
                if base in defined:
                    violations.append((rel, child, base))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str, str]] = set()
    printed = False
    for tree in scan_roots:
        for item in find_violations(tree):
            if item in seen:
                continue
            seen.add(item)
            printed = True
            rel, child, base = item
            print(f"VIOLATION {rel} noun-inherits-noun {child}({base})")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

