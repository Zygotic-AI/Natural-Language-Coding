#!/usr/bin/env python3
"""Fitness: ADR 0029 lineage check + bind snapshot round-trip + freshness."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out


def main() -> int:
    _ = sys.argv[1:]
    code, out = run([PY, str(ROOT / "tools" / "nlc-adr-lineage-check.py")])
    if code != 0:
        print(out)
        print("RESULT:NOT_MET lineage-check")
        return 1
    with tempfile.TemporaryDirectory() as td:
        snap = Path(td) / "adr-bind-snapshot.json"
        code, out = run(
            [
                PY,
                str(ROOT / "tools" / "nlc-adr-bind-snapshot.py"),
                "--root",
                td,
                "--out",
                str(snap),
            ]
        )
        if code != 0 or not snap.is_file():
            print(out)
            print("RESULT:NOT_MET bind-snapshot")
            return 1
        payload = json.loads(snap.read_text(encoding="utf-8"))
        if not payload.get("active_sha256") or not payload.get("adrs"):
            print("RESULT:NOT_MET empty snapshot")
            return 1
        code, out = run(
            [
                PY,
                str(ROOT / "tools" / "nlc-adr-active-freshness.py"),
                "--root",
                td,
                "--snapshot",
                str(snap),
            ]
        )
        if code != 0:
            print(out)
            print("RESULT:NOT_MET freshness")
            return 1
    print("RESULT:MET adr-0029-tools")
    return 0


if __name__ == "__main__":
    sys.exit(main())
