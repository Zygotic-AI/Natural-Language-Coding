#!/usr/bin/env python3
"""Refuse term definitions outside docs/TERMS.md (O11)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TERMS = ROOT / "docs" / "TERMS.md"
POINTER_MAX_LINES = 10
DEFINITION_HEADING = re.compile(r"^###\s+(?!\[).+", re.M)

POINTER_FILES = (
    ROOT / "integrity" / "LEXICON.md",
    ROOT / "docs" / "nlc" / "compiler" / "GLOSSARY.md",
    ROOT / "docs" / "nlc" / "compiler" / "NAMES.md",
    ROOT / "docs" / "nlc" / "RULE-VOCAB.md",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not TERMS.is_file():
        violations.append("missing docs/TERMS.md")
    elif "## A" not in TERMS.read_text(encoding="utf-8", errors="replace"):
        violations.append("docs/TERMS.md must contain alphabetized term sections")

    for path in POINTER_FILES:
        rel = path.relative_to(ROOT)
        if not path.is_file():
            violations.append(f"missing pointer file {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        if len(lines) > POINTER_MAX_LINES:
            violations.append(f"{rel} must be a short pointer (max {POINTER_MAX_LINES} lines)")
        if "TERMS.md" not in text:
            violations.append(f"{rel} must link to TERMS.md")
        if DEFINITION_HEADING.search(text):
            violations.append(f"{rel} must not host ### term definitions")

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
