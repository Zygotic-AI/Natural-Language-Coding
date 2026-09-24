#!/usr/bin/env python3
"""P8.2–P8.4 product completion SSOT closeout bundle."""

from __future__ import annotations



import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SCRIPTS = (
    "fitness-use-cases-expansion-sync.py",
    "fitness-integration-leaves-hygiene.py",
    "fitness-product-completion-p8-inference.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for name in SCRIPTS:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / name)],
            cwd=str(ROOT),
            check=False,
        )
        if proc.returncode != 0:
            violations.append(f"{name} must MET")
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

