#!/usr/bin/env python3
"""C20: R23 field-writes AND R24 adjective-locality both MET.


One binder, two requirement ids — this wrapper is the honest bind.
Either child red → C20 red.

Input: optional argv roots (forwarded to both children).
Output: child stdout, then RESULT:MET|NOT_MET.
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHILDREN = (
    ROOT / "tools" / "fitness-no-noun-field-writes.py",
    ROOT / "tools" / "fitness-adjective-locality.py",
)


def main() -> int:
    failed = False
    for tool in CHILDREN:
        print(f"=== {tool.name} ===")
        result = subprocess.run([sys.executable, str(tool), *sys.argv[1:]])
        if result.returncode != 0:
            failed = True
    if failed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
