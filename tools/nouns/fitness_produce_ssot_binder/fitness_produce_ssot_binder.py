#!/usr/bin/env python3
"""ADR 0005: produce package validation enforces SSOT exit evidence."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]
PRODUCE = ROOT / "tools" / "nlc_produce_package.py"
AGENTS = ROOT / "AGENTS.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PRODUCE.is_file():
        violations.append("missing nlc_produce_package.py")
    else:
        text = read_tool("tools/nlc_produce_package.py")
        for needle in ("ssot_leaf_ids", "ssot_exit_status", "SSOT_EXIT_EVIDENCE"):
            if needle not in text:
                violations.append(f"nlc_produce_package must enforce {needle}")
    if AGENTS.is_file():
        agents = AGENTS.read_text(encoding="utf-8", errors="replace")
        if "ssot_leaf_ids" not in agents or "ssot_exit_status" not in agents:
            violations.append("AGENTS.md must document SSOT exit evidence (P-020)")
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

