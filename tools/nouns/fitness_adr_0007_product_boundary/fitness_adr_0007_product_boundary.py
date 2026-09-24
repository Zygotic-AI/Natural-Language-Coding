#!/usr/bin/env python3
"""ADR 0042: rule IR product boundary JSON + landmines wired."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRODUCT_BOUNDARY = ROOT / "integrity" / "rule-ir-product-boundary.json"
ADR = ROOT / "adrs" / "0042-rule-ir-hub-product-boundary.md"
FIXTURE = ROOT / "examples" / "adopter-verify-fast-green"


def run_tool(name: str) -> int:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / name)],
        cwd=str(ROOT),
        check=False,
    )
    return proc.returncode


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not PRODUCT_BOUNDARY.is_file() or not ADR.is_file():
        violations.append("missing boundary JSON or ADR 0042")
    else:
        data = json.loads(PRODUCT_BOUNDARY.read_text(encoding="utf-8"))
        remain = data.get("remain_expansion") or []
        if "UC14.composable_ir_cross_primitive" not in remain:
            violations.append("remain_expansion must list UC14.composable_ir_cross_primitive")
    for script in ("assert-rule-runner-fails.py", "assert-rule-runner-passes.py"):
        if run_tool(script) != 0:
            violations.append(f"{script} must PASS")
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_rule_runner.py"),
            "--check",
            "--root",
            str(FIXTURE),
        ],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("nlc_rule_runner --check on adopter-verify-fast-green")

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

