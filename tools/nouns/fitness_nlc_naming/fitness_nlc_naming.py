#!/usr/bin/env python3
"""ADR 0011: consumer-facing naming (NLC product, not ACS-as-whole-product)."""

from __future__ import annotations



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SCAN = (
    ROOT / "README.md",
    ROOT / "docs" / "adoption" / "BOOTSTRAP.md",
    ROOT / "docs" / "adoption" / "RELEASE.md",
    ROOT / "docs" / "JOBS-TO-BE-DONE.md",
)

BANNED = (
    (re.compile(r"\bACS is the (?:whole )?product\b", re.I), "retired: ACS is the product"),
    (re.compile(r"\bAI-Compiled Systems is the product\b", re.I), "use Natural Language Coding"),
    (re.compile(r"\bBoundary-Based-Architecture\b", re.I), "legacy repo name in consumer copy"),
)

REQUIRE_NLC = re.compile(r"Natural Language Coding", re.I)


def scan_file(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    violations: list[str] = []
    if path.name == "README.md" and not REQUIRE_NLC.search(text[:2000]):
        violations.append(f"{rel}: missing 'Natural Language Coding' in hero")
    for pattern, msg in BANNED:
        if pattern.search(text):
            violations.append(f"{rel}: {msg}")
    return violations


def main() -> int:
    all_v: list[str] = []
    for path in SCAN:
        all_v.extend(scan_file(path))
    names = ROOT / "docs" / "nlc" / "compiler" / "NAMES.md"
    if names.is_file() and "Natural Language Coding" not in names.read_text(encoding="utf-8")[:500]:
        all_v.append("docs/nlc/compiler/NAMES.md: missing NLC product name")
    for v in all_v:
        print(f"VIOLATION {v}")
    if all_v:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

