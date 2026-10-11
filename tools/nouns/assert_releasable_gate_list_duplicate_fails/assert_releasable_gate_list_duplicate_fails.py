"""Landmine: a second verify/release profile JSON must fail SSOT fitness."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FITNESS = ROOT / "tools" / "fitness-releasable-gate-ssot.py"
FIXTURE_DIR = ROOT / "examples" / "releasable-gate-list-duplicate"


def main() -> int:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    shadow = FIXTURE_DIR / "shadow-profiles.json"
    shadow.write_text(
        json.dumps(
            {
                "schema": 1,
                "profiles": {"verify": ["shadow"], "release": ["shadow"]},
                "gates": {},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    try:
        proc = subprocess.run(
            [sys.executable, str(FITNESS)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
    finally:
        shadow.unlink(missing_ok=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0:
        print("ASSERT:FAIL fitness-releasable-gate-ssot must NOT_MET with shadow profile")
        print(out[-800:])
        return 1
    if "second releasable profile home" not in out:
        print("ASSERT:FAIL expected duplicate profile violation token")
        print(out[-800:])
        return 1
    print("ASSERT:PASS second gate-list home refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
