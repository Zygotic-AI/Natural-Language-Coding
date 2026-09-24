"""UC5 v1 coverage + v2 semantic apply product boundary (ADR 0042)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not (ROOT / "integrity" / "uc5-product-boundary.json").is_file():
        violations.append("missing uc5-product-boundary.json")
    else:
        data = json.loads((ROOT / "integrity" / "uc5-product-boundary.json").read_text(encoding="utf-8"))
        if data.get("remain_expansion"):
            violations.append("uc5-product-boundary remain_expansion must be empty after v2")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "fitness-uc5-semantic-apply-v2.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("fitness-uc5-semantic-apply-v2.py must MET")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
