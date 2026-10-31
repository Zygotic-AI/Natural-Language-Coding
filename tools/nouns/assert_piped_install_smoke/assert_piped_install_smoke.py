"""Landmine O1: curl | bash install entrypoint reaches execute.sh (not /tmp/goals/…)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INSTALL = ROOT / "scripts" / "install.sh"


def main() -> int:
    if not INSTALL.is_file():
        print("ASSERT:FAIL missing scripts/install.sh")
        return 1
    env = {
        **os.environ,
        "NLC_RAW_BASE": f"file://{ROOT}",
        "NLC_INSTALL_ROOT": "/tmp/nlc-piped-install-smoke-root",
    }
    proc = subprocess.run(
        ["bash", "-c", f'curl -fsSL "file://{INSTALL}" | bash -s'],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if "Natural Language Compiler — install" not in out:
        print("ASSERT:FAIL piped install never reached execute.sh banner")
        print(out[-600:])
        return 1
    if "goals/hub_install/execute.sh: No such file" in out or "/tmp/goals/hub_install" in out:
        print("ASSERT:FAIL piped install still uses broken thin-entrypoint path")
        return 1
    print("ASSERT:PASS piped install.sh bootstraps execute.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
