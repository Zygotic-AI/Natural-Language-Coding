#!/usr/bin/env python3
"""ADR 0013: hub nlc*.py CLIs call hub_tool() before work."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
EXEMPT = frozenset({"nlc_requirements.py"})


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in sorted(TOOLS.glob("nlc*.py")):
        if path.name in EXEMPT:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if 'if __name__ == "__main__"' not in text:
            continue
        if "hub_tool()" not in text:
            violations.append(f"{path.name} must call hub_tool() (ADR 0013)")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
