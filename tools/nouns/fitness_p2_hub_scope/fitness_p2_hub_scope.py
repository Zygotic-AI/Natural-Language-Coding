#!/usr/bin/env python3
"""ADR 0002: P2 hub gates — session preflight + matrix in compile suite."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    if "session_preflight" not in ci:
        violations.append("ci_fitness.py must call session_preflight (P2 hub gates)")
    if "audit-binding-matrix" not in ci:
        violations.append("ci_fitness.py must run audit-binding-matrix")
    principles = (ROOT / "integrity" / "PRINCIPLES.md").read_text(encoding="utf-8")
    if "0002-p2-scope" not in principles:
        violations.append("PRINCIPLES.md must cite ADR 0002 P2 scope")
    charter = (ROOT / "CHARTER.md").read_text(encoding="utf-8", errors="replace")
    if "0002-p2-scope" not in charter and "ADR 0002" not in charter:
        violations.append("CHARTER.md must reference ADR 0002 P2 scope")
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

