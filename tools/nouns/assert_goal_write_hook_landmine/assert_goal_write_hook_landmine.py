"""Landmine O8: goal-write hook runs under missing jq/python3 and refuses bad input."""

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

BARE_PATH = Path("/usr/bin:/bin")


def run_hook(payload: dict | str, *, cwd: Path, env: dict[str, str]) -> dict:
    if isinstance(payload, dict):
        stdin = json.dumps(payload)
    else:
        stdin = payload
    proc = subprocess.run(
        ["/usr/bin/bash", str(HOOK)],
        input=stdin,
        text=True,
        capture_output=True,
        cwd=str(cwd),
        env=env,
        check=False,
    )
    out = (proc.stdout or "").strip()
    if not out:
        print(f"ASSERT:FAIL hook produced no stdout stderr={(proc.stderr or '')[-200:]}")
        sys.exit(1)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        print(f"ASSERT:FAIL invalid hook json: {out[-200:]}")
        sys.exit(1)


def env_no_jq(*, keep_python: bool = True) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k != "PATH"}
    env["PATH"] = str(BARE_PATH)
    if not keep_python:
        env.pop("PYTHON", None)
    return env


def main() -> int:
    if not HOOK.is_file():
        print("ASSERT:FAIL missing hook script")
        return 1

    # jq missing, python3 present — must still deny goals without stamp
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "goals" / "sample").mkdir(parents=True)
        deny = run_hook(
            {"tool_input": {"path": "goals/sample/implementation.py"}},
            cwd=tmp_path,
            env={**env_no_jq(keep_python=True), "PWD": str(tmp_path)},
        )
        if deny.get("permission") != "deny":
            print("ASSERT:FAIL expected deny for goals/* without stamp (jq missing)")
            return 1

    # jq and python3 both missing — must refuse (not allow)
    empty_bin = tempfile.mkdtemp()
    no_interp = {k: v for k, v in os.environ.items() if k != "PATH"}
    no_interp["PATH"] = empty_bin
    no_interp["PWD"] = str(ROOT)
    refuse = run_hook(
        {"tool_input": {"path": "goals/sample/x.py"}},
        cwd=ROOT,
        env={**no_interp, "PWD": str(ROOT)},
    )
    if refuse.get("permission") != "deny":
        print("ASSERT:FAIL expected deny when jq and python3 are both missing")
        return 1

    # malformed / empty path must refuse
    for bad in ("", "   ", "{}", '{"tool_input":{}}'):
        bad_out = run_hook(
            bad,
            cwd=ROOT,
            env={**os.environ, "PWD": str(ROOT), "PATH": os.environ.get("PATH", "")},
        )
        if bad_out.get("permission") != "deny":
            print(f"ASSERT:FAIL expected deny for malformed input {bad!r}")
            return 1

    allow = run_hook(
        {"tool_input": {"path": "README.md"}},
        cwd=ROOT,
        env={**os.environ, "PWD": str(ROOT)},
    )
    if allow.get("permission") != "allow":
        print("ASSERT:FAIL expected allow for non-goals path")
        return 1

    hooks = json.loads((ROOT / ".cursor" / "hooks.json").read_text(encoding="utf-8"))
    matcher = ""
    for entry in hooks.get("hooks", {}).get("preToolUse", []) or []:
        if entry.get("command") == ".cursor/hooks/nlc-goal-write-gate.sh":
            matcher = str(entry.get("matcher", ""))
    if "Write" not in matcher:
        print("ASSERT:FAIL hooks.json matcher must include Write")
        return 1
    if "Delete" not in matcher:
        print("ASSERT:FAIL hooks.json matcher must include Delete (Cursor docs: file writes/deletes)")
        return 1

    print("ASSERT:PASS goal-write hook fail-closed and goal-path deny")
    return 0


if __name__ == "__main__":
    sys.exit(main())
