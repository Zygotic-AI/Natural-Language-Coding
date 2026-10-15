"""Landmine ADR 0050: tag gate REFUSEs an unresolvable commit reference."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DANGLING = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"


def main() -> int:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_release_tag_gate.py"),
            "--check",
            "--commit",
            DANGLING,
            "--tag",
            "v0.2.0",
            "--skip-verify-deep",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL tag gate should REFUSE dangling commit")
        return 1
    if proc.returncode != 2:
        print(f"ASSERT:FAIL expected exit 2 (REFUSE), got {proc.returncode}")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "RELEASE_TAG_GATE:REFUSE" not in combined:
        print("ASSERT:FAIL expected RELEASE_TAG_GATE:REFUSE")
        return 1
    if DANGLING not in combined and "unresolved" not in combined.lower():
        print("ASSERT:FAIL expected unresolved reference in output")
        return 1
    if "no nlc-version.json" in combined.lower():
        print("ASSERT:FAIL must not report missing file for unresolvable commit")
        return 1
    print("ASSERT:PASS unresolvable commit reference REFUSE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
