"""Landmine ADR 0040: shipped tag audit refuses unprepared v0.2.0 merge."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BAD_COMMIT = "397b1a0"
BAD_TAG = "v0.2.0"


def main() -> int:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_release_shipped_tag_audit.py"),
            "--check",
            "--tag",
            BAD_TAG,
            "--commit",
            BAD_COMMIT,
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL shipped tag audit should refuse bad v0.2.0 commit")
        print(proc.stdout, proc.stderr)
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "RELEASE_SHIPPED_TAG:NOT_MET" not in combined:
        print("ASSERT:FAIL expected RELEASE_SHIPPED_TAG:NOT_MET")
        return 1
    if "hub-release-record" not in combined.lower():
        print("ASSERT:FAIL expected hub-release-record blocker in output")
        return 1
    if "git push origin :refs/tags/" not in combined:
        print("ASSERT:FAIL expected tag deletion remediation")
        return 1
    print("ASSERT:PASS shipped tag audit refuses unprepared tag commit")
    return 0


