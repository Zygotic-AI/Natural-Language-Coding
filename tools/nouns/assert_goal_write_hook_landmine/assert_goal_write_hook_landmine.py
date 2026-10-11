"""Landmine O8: goal-write hook registered, denies goals without stamp, fail-closed prose."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOK = (ROOT / ".cursor" / "hooks" / "nlc-goal-write-gate.sh").resolve()


def run_hook(payload: dict, *, cwd: Path, env: dict[str, str]) -> dict:
    proc = subprocess.run(
        ["/usr/bin/bash", str(HOOK)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(cwd),
        env=env,
        check=False,
    )
    out = (proc.stdout or "").strip()
    if not out:
        print(f"ASSERT:FAIL hook produced no stdout stderr={(proc.stderr or '')[-120:]}")
        sys.exit(1)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        print(f"ASSERT:FAIL invalid hook json: {out[-200:]}")
        sys.exit(1)


def main() -> int:
    if not HOOK.is_file():
        print("ASSERT:FAIL missing hook script")
        return 1
    text = HOOK.read_text(encoding="utf-8")
    if "missing jq and python3" not in text:
        print("ASSERT:FAIL hook must refuse when jq and python3 are both missing")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "goals" / "sample").mkdir(parents=True)
        deny = run_hook(
            {"tool_input": {"path": "goals/sample/implementation.py"}},
            cwd=tmp_path,
            env={**os.environ, "PWD": str(tmp_path)},
        )
        if deny.get("permission") != "deny":
            print("ASSERT:FAIL expected deny for goals/* without before-generate stamp")
            return 1

    allow = run_hook(
        {"tool_input": {"path": "README.md"}},
        cwd=ROOT,
        env={**os.environ, "PWD": str(ROOT)},
    )
    if allow.get("permission") != "allow":
        print("ASSERT:FAIL expected allow for non-goals path")
        return 1

    print("ASSERT:PASS goal-write hook fail-closed and goal-path deny")
    return 0


if __name__ == "__main__":
    sys.exit(main())
