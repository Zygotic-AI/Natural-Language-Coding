#!/usr/bin/env python3
"""ADR 0023 / UC15: brownfield inventory points at rule-trace + goal-scaffold."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "nlc-brownfield-inventory.py"
HARNESS = ROOT / "docs" / "nlc" / "HARNESS.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not TOOL.is_file():
        violations.append("missing nlc-brownfield-inventory.py")
    else:
        text = TOOL.read_text(encoding="utf-8", errors="replace")
        if "goal-scaffold" not in text or "RULE-TRACE" not in text:
            violations.append("brownfield inventory must cite goal-scaffold and RULE-TRACE")
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(ROOT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    err = proc.stderr or ""
    if "goal-scaffold" not in err:
        violations.append("brownfield stderr must mention goal-scaffold")
    if HARNESS.is_file() and "goal-scaffold" not in HARNESS.read_text(encoding="utf-8", errors="replace"):
        violations.append("HARNESS.md must list goal-scaffold")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
