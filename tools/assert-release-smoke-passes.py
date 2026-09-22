#!/usr/bin/env python3
"""Landmine ADR 0015: release smoke (local store + init + install-verify)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "nlc-release-smoke.sh"


def main() -> int:
    if not SCRIPT.is_file():
        print(f"ASSERT:FAIL missing {SCRIPT}")
        return 1
    proc = subprocess.run(
        ["bash", str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0 or "RELEASE_SMOKE:MET" not in out:
        print("ASSERT:FAIL nlc-release-smoke.sh")
        print(out[-1000:])
        return 1
    print("ASSERT:PASS release smoke MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
