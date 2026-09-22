#!/usr/bin/env python3
"""ADR 0019: guided queue + maintainer guide commands wired in hub."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    required = (
        "tools/nlc_dashboard.py",
        "tools/nlc_guide_cmd.py",
        "tools/nlc_regen_continue.py",
        "tools/nlc_requirements_cmd.py",
    )
    for rel in required:
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
    nlc = (ROOT / "tools" / "nlc.py").read_text(encoding="utf-8", errors="replace")
    for needle in ("refresh_work_queue", 'add_parser("guide"'):
        if needle not in nlc:
            violations.append(f"tools/nlc.py must wire ADR 0019: {needle}")
    dash = (ROOT / "tools" / "nlc_dashboard.py").read_text(encoding="utf-8", errors="replace")
    if "YOUR QUEUE" not in dash or "Requirements" not in dash:
        violations.append("dashboard must show kanban YOUR QUEUE stages")
    if "work-queue.json" not in dash:
        violations.append("dashboard must persist work-queue.json")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
