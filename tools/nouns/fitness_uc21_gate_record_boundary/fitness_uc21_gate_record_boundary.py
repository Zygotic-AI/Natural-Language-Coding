#!/usr/bin/env python3
"""UC21 v1 gate-record + scope harness (P6.5)."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for rel in (
        "docs/nlc/GATE-RECORD-BINDER.md",
        "docs/nlc/HARNESS.md",
        "tools/nlc_gate_record.py",
        "tools/nlc_gate_scope.py",
    ):
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "assert-gate-record-describe-passes.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("assert-gate-record-describe-passes must PASS")
    status = json.loads((ROOT / "integrity" / "uc-product-status.json").read_text(encoding="utf-8"))
    exp = (status.get("ucs") or {}).get("UC21", {}).get("expansion_only") or []
    if exp:
        violations.append(f"UC21 expansion_only must be empty: {exp}")
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

