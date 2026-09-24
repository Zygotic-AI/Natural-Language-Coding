#!/usr/bin/env python3
"""ADR 0015: distribution binders documented and landmined in compile CI."""

from __future__ import annotations



import sys
from pathlib import Path

from fitness_hub_source import read_tool

ROOT = Path(__file__).resolve().parents[3]

LANDMINES = (
    "assert-install-verify-passes.py",
    "assert-project-lock-schema-passes.py",
    "assert-nlc-update-hermetic-passes.py",
    "assert-release-smoke-passes.py",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    ci = read_tool("tools/ci_fitness.py")
    for name in LANDMINES:
        if name not in ci:
            violations.append(f"ci_fitness must run {name}")
    for rel in ("tools/nlc-install-verify.py", "tools/nlc-update.py", "integrity/nlc-install-hashes.json"):
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")
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

