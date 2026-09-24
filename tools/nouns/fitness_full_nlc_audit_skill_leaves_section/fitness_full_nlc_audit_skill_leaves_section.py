#!/usr/bin/env python3
"""full-nlc-audit skill must document when to write integration-leaves (F4 guidance)."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / ".agents" / "skills" / "full-nlc-audit" / "SKILL.md"

REQUIRED_HEADING = "## When to write leaves"
REQUIRED_TERMS = ("disposition", "evidence", "claims")


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not SKILL.is_file():
        violations.append("missing full-nlc-audit SKILL.md")
    else:
        text = SKILL.read_text(encoding="utf-8", errors="replace")
        if REQUIRED_HEADING not in text:
            violations.append(f"skill missing section {REQUIRED_HEADING}")
        else:
            section = text.split(REQUIRED_HEADING, 1)[1].split("\n## ", 1)[0].lower()
            for term in REQUIRED_TERMS:
                if term not in section:
                    violations.append(f"When to write leaves section missing {term!r}")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

