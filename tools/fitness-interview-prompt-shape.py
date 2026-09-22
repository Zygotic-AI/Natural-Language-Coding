#!/usr/bin/env python3
"""ADR 0018: interview skill documents five-part blocking shape for humans."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERVIEW = ROOT / ".agents" / "skills" / "interview" / "SKILL.md"
PROPOSER = ROOT / ".agents" / "skills" / "bbp-proposer" / "SKILL.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not INTERVIEW.is_file():
        violations.append("missing .agents/skills/interview/SKILL.md")
    else:
        text = INTERVIEW.read_text(encoding="utf-8", errors="replace")
        for needle in (
            "ADR 0018",
            "plain language",
            "/interview",
            "/planit",
            "When you block",
        ):
            if needle not in text:
                violations.append(f"interview SKILL must mention: {needle}")
        for needle in ("Problem", "Ask", "Example"):
            if needle not in text:
                violations.append(f"interview SKILL must document blocking part: {needle}")

    if not PROPOSER.is_file():
        violations.append("missing bbp-proposer SKILL.md")
    elif "rule-marker" not in PROPOSER.read_text(encoding="utf-8", errors="replace"):
        violations.append("bbp-proposer must prescribe rule-marker CLI (ADR 0023)")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
