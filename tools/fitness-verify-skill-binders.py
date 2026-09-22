#!/usr/bin/env python3
"""ADR 0021/0010/0023: /verify skill cites gate + rule trace remediation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / ".agents" / "skills" / "verify" / "SKILL.md"


def main() -> int:
    _ = sys.argv[1:]
    if not VERIFY.is_file():
        print("VIOLATION missing verify SKILL")
        print("RESULT:NOT_MET")
        return 1
    text = VERIFY.read_text(encoding="utf-8", errors="replace")
    violations: list[str] = []
    for needle in ("verify-deep", "gate-record", "rule-coverage"):
        if needle not in text:
            violations.append(f"verify SKILL must mention remediation: {needle}")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
