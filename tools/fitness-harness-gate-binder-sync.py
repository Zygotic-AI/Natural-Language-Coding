#!/usr/bin/env python3
"""ADR 0010/0023: HARNESS.md lists gate + rule trace maintainer commands."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "docs" / "nlc" / "HARNESS.md"
BINDER = ROOT / "docs" / "nlc" / "GATE-RECORD-BINDER.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not HARNESS.is_file():
        violations.append("missing docs/nlc/HARNESS.md")
    else:
        text = HARNESS.read_text(encoding="utf-8", errors="replace")
        for needle in (
            "gate-record",
            "gate-scope",
            "before-generate",
            "rule-coverage",
            "rule-marker",
            "goal-scaffold",
            "0010",
            "0023",
        ):
            if needle not in text:
                violations.append(f"HARNESS.md must mention {needle}")
    if not BINDER.is_file():
        violations.append("missing GATE-RECORD-BINDER.md")
    elif "nlc_gate_record.py" not in BINDER.read_text(encoding="utf-8", errors="replace"):
        violations.append("GATE-RECORD-BINDER must cite nlc_gate_record.py")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
