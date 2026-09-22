#!/usr/bin/env python3
"""Fitness: nlc-pipeline-wire.py must exist and be invokable (ADR 0026 wiring)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIRE = ROOT / "tools" / "nlc-pipeline-wire.py"


def main() -> int:
    if not WIRE.is_file():
        print("fitness-nlc-pipeline-wire: MISSING tools/nlc-pipeline-wire.py")
        return 1
    proc = subprocess.run(
        [sys.executable, str(WIRE), "--help"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print("fitness-nlc-pipeline-wire: --help failed")
        print(proc.stderr)
        return 1
    print("fitness-nlc-pipeline-wire: MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
