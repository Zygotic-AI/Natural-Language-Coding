#!/usr/bin/env python3
"""O6: public hub docs must not depend on private repos or person names (CG-R4).

Scans in-force markdown/json surfaces only (not reviews/, rcas/, history/).
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

IN_FORCE_FILES = [
    ROOT / "AGENTS.md",
    ROOT / "DESCRIBE.md",
    ROOT / "CHARTER.md",
    ROOT / "README.md",
    ROOT / "docs" / "OPERATING_BINDINGS.md",
    ROOT / "docs" / "TERMS.md",
    ROOT / "docs" / "bba" / "BBA-EMIT-PROCESS.md",
    ROOT / "integrity" / "ACTIONS.md",
    ROOT / "integrity" / "BOUNDARY.md",
    ROOT / "integrity" / "GATE.md",
    ROOT / ".agents" / "skills" / "planit" / "SKILL.md",
    ROOT / "docs" / "nlc" / "compiler" / "PLANIT-ORCHESTRATION.md",
]

FORBIDDEN_MARKERS = (
    "BBA-Bindings",
    "richardpickett/BBA-Bindings",
    "github.com/richardpickett/BBA-Bindings",
    "app.notion.com",
    "ai-vault maintainer",
    "ai-vault-only",
)

PERSON_PATTERNS = (
    re.compile(r"Richard\s+Pickett", re.IGNORECASE),
    re.compile(r"richardpickett", re.IGNORECASE),
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in IN_FORCE_FILES:
        if not path.is_file():
            violations.append(f"missing in-force surface {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                violations.append(f"{rel}: forbidden marker {marker!r}")
        for pat in PERSON_PATTERNS:
            if pat.search(text):
                violations.append(f"{rel}: person-name pattern {pat.pattern}")
    take_me = ROOT / ".agents" / "instructions" / "take-me-literally.md"
    if not take_me.is_file():
        violations.append("missing .agents/instructions/take-me-literally.md")
    agents = ROOT / "AGENTS.md"
    if agents.is_file() and "take-me-literally.md" not in agents.read_text(encoding="utf-8"):
        violations.append("AGENTS.md must link take-me-literally.md")

    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
