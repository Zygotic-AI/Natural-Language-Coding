#!/usr/bin/env python3
"""UC16 reference adapter fixture + pass landmine (P3)."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    fixture = ROOT / "examples" / "non-python-with-adapter"
    if not fixture.is_dir():
        violations.append("missing non-python-with-adapter example")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "assert-non-python-adapter-passes.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("assert-non-python-adapter-passes must PASS")
    status = json.loads((ROOT / "integrity" / "uc-product-status.json").read_text(encoding="utf-8"))
    exp = (status.get("ucs") or {}).get("UC16", {}).get("expansion_only") or []
    if exp:
        violations.append(f"UC16 expansion_only must be empty: {exp}")
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

