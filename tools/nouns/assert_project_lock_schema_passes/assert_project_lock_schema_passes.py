"""Landmine ADR 0015: nlc-init writes a valid .nlc/lock.json."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_lock_validate import validate_lock

    with tempfile.TemporaryDirectory(prefix="nlc-lock-") as tmp:
        app = Path(tmp) / "app"
        env = os.environ.copy()
        env["NLC_HUB"] = str(ROOT)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "nlc-init.py"), str(app), "--name", "LockTest"],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print("ASSERT:FAIL nlc-init", proc.stderr)
            return 1
        lock_path = app / ".nlc" / "lock.json"
        if not lock_path.is_file():
            print("ASSERT:FAIL missing lock.json")
            return 1
        data = json.loads(lock_path.read_text(encoding="utf-8"))
        ok, reason = validate_lock(data)
        if not ok:
            print(f"ASSERT:FAIL lock invalid: {reason}")
            return 1
    print("ASSERT:PASS project lock schema (ADR 0015)")
    return 0


