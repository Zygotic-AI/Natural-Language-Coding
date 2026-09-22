#!/usr/bin/env python3
"""ADR 0001: binding matrix audited in session + CI landmine."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    matrix = ROOT / "integrity" / "binding-matrix.json"
    audit = ROOT / "tools" / "audit-binding-matrix.py"
    if not matrix.is_file():
        violations.append("missing integrity/binding-matrix.json")
    if not audit.is_file():
        violations.append("missing audit-binding-matrix.py")
    ci = (ROOT / "tools" / "ci_fitness.py").read_text(encoding="utf-8", errors="replace")
    if "assert-binding-matrix-met" not in ci:
        violations.append("ci_fitness must run assert-binding-matrix-met")
    if "session_preflight" not in ci or "audit-binding-matrix" not in ci:
        violations.append("ci_fitness session must run audit-binding-matrix")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
