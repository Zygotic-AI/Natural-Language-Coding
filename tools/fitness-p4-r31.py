#!/usr/bin/env python3
"""P4 / R31: agent-noun structure AND code-boundary failure modes.

Agent tool ignores argv (always scans agents/).
Code tool (fitness-boundary-io.py) uses argv roots, default hub ROOT.

Either child red → P4/R31 red.

Input: optional argv roots (forwarded to the code-side child).
Output: child stdout, then RESULT:MET|NOT_MET.
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "tools" / "fitness-agent-noun-structure.py"
CODE = ROOT / "tools" / "fitness-boundary-io.py"


def main() -> int:
    failed = False
    print(f"=== {AGENT.name} ===")
    agent = subprocess.run([sys.executable, str(AGENT)])
    if agent.returncode != 0:
        failed = True
    print(f"=== {CODE.name} ===")
    code = subprocess.run([sys.executable, str(CODE), *sys.argv[1:]])
    if code.returncode != 0:
        failed = True
    if failed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
