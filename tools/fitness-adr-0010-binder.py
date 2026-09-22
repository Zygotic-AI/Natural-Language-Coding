#!/usr/bin/env python3
"""ADR 0010: gate-record / gate-scope / stamp landmines in compile CI."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LANDMINES = (
    "assert-verify-gate-record-fails.py",
    "assert-verify-before-generate-stamp-fails.py",
    "assert-verify-stale-stamp-fails.py",
    "assert-verify-skill-gate-fails.py",
    "assert-gate-record-describe-passes.py",
)

FITNESS = (
    "fitness-harness-gate-binder-sync.py",
    "fitness-verify-skill-binders.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = (ROOT / "tools" / "ci_fitness.py").read_text(encoding="utf-8", errors="replace")
    for name in LANDMINES + FITNESS:
        if not (ROOT / "tools" / name).is_file():
            violations.append(f"missing tools/{name}")
            continue
        stem = name.removesuffix("-passes.py").removesuffix("-fails.py").removesuffix(".py")
        if stem not in ci and name not in ci:
            violations.append(f"ci_fitness must reference {name}")
    for rel in ("tools/nlc_gate_record.py", "tools/nlc_gate_scope.py", "tools/nlc_compliance.py"):
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
    comp = (ROOT / "tools" / "nlc_compliance.py").read_text(encoding="utf-8", errors="replace")
    if "gate_record_blockers" not in comp:
        violations.append("nlc_compliance must define gate_record_blockers")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
