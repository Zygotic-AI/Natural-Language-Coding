"""Landmine ADR 0039: tag gate refuses commits without hub-release-record."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# PR #19 merge — predates hub-release-record.json requirement.
BAD_COMMIT = "397b1a0"


def main() -> int:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_release_tag_gate.py"),
            "--check",
            "--commit",
            BAD_COMMIT,
            "--tag",
            "v0.2.0",
            "--skip-verify-deep",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        print("ASSERT:FAIL tag gate should refuse commit without release record")
        print(proc.stdout, proc.stderr)
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "hub-release-record" not in combined and "release record" not in combined.lower():
        print("ASSERT:FAIL expected hub-release-record blocker")
        return 1
    print("ASSERT:PASS release tag gate refuses unprepared merge commit")
    return 0


