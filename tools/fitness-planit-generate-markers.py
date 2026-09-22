#!/usr/bin/env python3
"""ADR 0023: planit generate step prescribes goal-scaffold + rule-marker emit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANIT = ROOT / ".agents" / "skills" / "planit" / "SKILL.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PLANIT.is_file():
        violations.append("missing .agents/skills/planit/SKILL.md")
    else:
        text = PLANIT.read_text(encoding="utf-8", errors="replace")
        for needle in (
            "goal-scaffold",
            "rule-marker",
            "rule-emit",
            "nlc:rule=",
            "gate-scope",
            "gate-record",
        ):
            if needle not in text:
                violations.append(f"planit SKILL must mention generate binder: {needle}")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
