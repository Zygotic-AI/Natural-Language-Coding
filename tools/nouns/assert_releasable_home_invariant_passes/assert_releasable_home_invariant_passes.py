"""Landmine: releasable verify profile verdict is independent of HOME (RCA-1 C3)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "tools" / "nlc_gate.py"


def run_once(home: Path) -> tuple[int, str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    env.pop("NLC_HUB", None)
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--profile", "verify", "--tree", str(ROOT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    if not RUNNER.is_file():
        print("ASSERT:FAIL missing nlc_gate.py")
        return 1
    with tempfile.TemporaryDirectory(prefix="bbp-home-a-") as ha, tempfile.TemporaryDirectory(
        prefix="bbp-home-b-"
    ) as hb:
        code_a, out_a = run_once(Path(ha))
        code_b, out_b = run_once(Path(hb))
    if code_a != code_b:
        print("ASSERT:FAIL verify profile exit code differed across HOME")
        print(f"HOME-a={code_a} HOME-b={code_b}")
        print(out_a[-400:])
        print(out_b[-400:])
        return 1
    print(f"ASSERT:PASS same verify verdict ({code_a}) under two HOME roots")
    return 0


if __name__ == "__main__":
    sys.exit(main())
