#!/usr/bin/env python3
"""ADR 0043: UC14 adopt-time boundary + landmines."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run_script(name: str) -> int:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / name)],
        cwd=str(ROOT),
        check=False,
    ).returncode


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in (
        ROOT / "integrity" / "uc14-product-boundary.json",
        ROOT / "adrs" / "0043-uc14-composable-adopt-boundary.md",
    ):
        if not path.is_file():
            violations.append(f"missing {path.name}")
    for script in ("assert-rule-adoption-conflicts-fails.py", "assert-rule-adoption-passes.py"):
        if run_script(script) != 0:
            violations.append(f"{script} must PASS")
    status = json.loads((ROOT / "integrity" / "uc-product-status.json").read_text(encoding="utf-8"))
    exp = (status.get("ucs") or {}).get("UC14", {}).get("expansion_only") or []
    if exp:
        violations.append(f"UC14 expansion_only must be empty: {exp}")
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

