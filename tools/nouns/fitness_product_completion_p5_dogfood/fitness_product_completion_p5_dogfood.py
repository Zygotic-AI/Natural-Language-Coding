#!/usr/bin/env python3
"""P5.3: hub BBA dogfood + interior slice + X4 noun pilot bundle."""

from __future__ import annotations



import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "docs" / "nlc" / "HUB-BBA-DOGFOOD.md"


def run_fitness(name: str) -> int:
    return subprocess.run(
        [sys.executable, str(ROOT / "tools" / name)],
        cwd=str(ROOT),
        check=False,
    ).returncode


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not DOC.is_file():
        violations.append("missing HUB-BBA-DOGFOOD.md")
    else:
        text = DOC.read_text(encoding="utf-8", errors="replace")
        for needle in (
            "fitness-hub-bba-dogfood.py",
            "hub-x4-remainder.json",
            "fitness-hub-x4-noun-pilot.py",
            "fitness-hub-x4-tranche-t1.py",
            "fitness-hub-x4-tranche-t2.py",
            "fitness-hub-x4-tranche-t3.py",
            "fitness-hub-x4-tranche-t4.py",
        ):
            if needle not in text:
                violations.append(f"HUB-BBA-DOGFOOD missing {needle}")
    for script in (
        "fitness-hub-bba-dogfood.py",
        "fitness-hub-bba-interior-slice.py",
        "fitness-hub-x4-noun-pilot.py",
        "fitness-hub-x4-tranche-t1.py",
        "fitness-hub-x4-tranche-t2.py",
        "fitness-hub-x4-tranche-t3.py",
        "fitness-hub-x4-tranche-t4.py",
    ):
        if run_fitness(script) != 0:
            violations.append(f"{script} must MET")
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

