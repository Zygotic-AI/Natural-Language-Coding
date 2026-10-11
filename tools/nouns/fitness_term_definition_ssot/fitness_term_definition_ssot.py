#!/usr/bin/env python3
"""Refuse term definitions outside docs/TERMS.md (O11)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TERMS = ROOT / "docs" / "TERMS.md"
POINTER_MAX_LINES = 10

sys.path.insert(0, str(ROOT / "tools"))
from nouns.term_definition_ssot.term_definition_exclusions import POINTER_FILES  # noqa: E402
from nouns.term_definition_ssot.term_definition_ssot import (  # noqa: E402
    load_term_names,
    scan_repo,
)

REQUIRED_IN_TERMS: tuple[str, ...] = (
    "A-LEXICON-ACTION",
    "A-LEXICON-ATOMIC",
    "A-LEXICON-COMPOUND",
    "A-LEXICON-CONTENT-TYPE",
    "A-LEXICON-CONTRIBUTION",
    "A-LEXICON-CONTRIB-GATE",
    "A-LEXICON-SHARED-DOCS",
    "A-LEXICON-TYPE-RECIPE",
    "PASS / FAIL / REFUSE",
    "refuse-wired",
    "Conflict note (Goal)",
    "Conflict note (BBP vs BBA)",
    "Compile-time intent only",
    "Owner decision 2026-10-10",
    "Not **met** if",
    "Orchestrator term rename (v0.4)",
    "v0.4",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not TERMS.is_file():
        violations.append("missing docs/TERMS.md")
        print("RESULT:NOT_MET")
        return 1
    terms_text = TERMS.read_text(encoding="utf-8", errors="replace")
    terms = load_term_names(terms_text)
    if len(terms) < 20:
        violations.append("docs/TERMS.md term heading set too small")

    for marker in REQUIRED_IN_TERMS:
        if marker not in terms_text:
            violations.append(f"TERMS missing merged lexicon marker: {marker!r}")

    for rel in POINTER_FILES:
        path = ROOT / rel
        if not path.is_file():
            violations.append(f"missing pointer file {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        if len(lines) > POINTER_MAX_LINES:
            violations.append(f"{rel} must be a short pointer (max {POINTER_MAX_LINES} lines)")
        if "TERMS.md" not in text:
            violations.append(f"{rel} must link to TERMS.md")

    violations.extend(scan_repo(ROOT, terms))

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
