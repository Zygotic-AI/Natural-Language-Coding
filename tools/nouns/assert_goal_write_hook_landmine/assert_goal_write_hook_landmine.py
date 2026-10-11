"""Landmine O8: goal-write hook jq/python fallbacks and fail-closed paths."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOK = (ROOT / ".cursor" / "hooks" / "nlc-goal-write-gate.sh").resolve()

def run_hook(payload: dict | str, *, cwd: Path, env: dict[str, str]) -> dict:
    if isinstance(payload, dict):
        stdin = json.dumps(payload)
    else:
        stdin = payload
    bash = shutil.which("bash") or "bash"
    proc = subprocess.run(
        [bash, str(HOOK)],
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


def make_path_env(*, include_python: bool, include_jq: bool) -> dict[str, str]:
    td = Path(tempfile.mkdtemp(prefix="goal-hook-bin-"))
    for name in ("bash", "cat"):
        src = shutil.which(name)
        if src:
            (td / name).symlink_to(src)
    if include_python:
        py = shutil.which("python3")
        if py:
            (td / "python3").symlink_to(py)
    if include_jq:
        jq = shutil.which("jq")
        if jq:
            (td / "jq").symlink_to(jq)
    env = {k: v for k, v in os.environ.items() if k != "PATH"}
    env["PATH"] = str(td)
    return env


def main() -> int:
    if not HOOK.is_file():
        print("ASSERT:FAIL missing hook script")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "goals" / "sample").mkdir(parents=True)
        env_py_no_jq = make_path_env(include_python=True, include_jq=False)
        env_py_no_jq["PWD"] = str(tmp_path)
        if shutil.which("jq", path=env_py_no_jq["PATH"]):
            print("ASSERT:FAIL landmine PATH still resolves jq")
            return 1
        if not shutil.which("python3", path=env_py_no_jq["PATH"]):
            print("ASSERT:FAIL landmine PATH must include python3 for fallback test")
            return 1
        deny = run_hook(
            {"tool_input": {"path": "goals/sample/implementation.py"}},
            cwd=tmp_path,
            env=env_py_no_jq,
        )
        if deny.get("permission") != "deny":
            print("ASSERT:FAIL (1) python fallback must deny goals without stamp when jq absent")
            return 1

    env_none = {k: v for k, v in os.environ.items() if k != "PATH"}
    env_none["PATH"] = tempfile.mkdtemp(prefix="goal-hook-empty-")
    env_none["PWD"] = str(ROOT)
    refuse = run_hook(
        {"tool_input": {"path": "goals/sample/x.py"}},
        cwd=ROOT,
        env=env_none,
    )
    if refuse.get("permission") != "deny":
        print("ASSERT:FAIL (2) must refuse when jq and python3 are both absent")
        return 1

    for bad in ("", "   ", "{}", '{"tool_input":{}}'):
        bad_out = run_hook(
            bad,
            cwd=ROOT,
            env={**os.environ, "PWD": str(ROOT)},
        )
        if bad_out.get("permission") != "deny":
            print(f"ASSERT:FAIL (3) expected deny for malformed input {bad!r}")
            return 1

    expired_root = ROOT / ".landmine-goal-write-expired"
    expired_root.mkdir(exist_ok=True)
    (expired_root / "goals" / "g").mkdir(parents=True, exist_ok=True)
    (expired_root / ".nlc").mkdir(exist_ok=True)
    (expired_root / ".nlc" / "before-generate-stamp.json").write_text(
        json.dumps({"ok": True, "at": "2020-01-01T00:00:00Z", "scopes": []}),
        encoding="utf-8",
    )
    stale = run_hook(
        {"tool_input": {"path": "goals/g/x.py"}},
        cwd=expired_root,
        env={**os.environ, "PWD": str(expired_root), "NLC_HUB": "/nonexistent/nlc/hub"},
    )
    shutil.rmtree(expired_root, ignore_errors=True)
    if stale.get("permission") != "deny":
        print("ASSERT:FAIL expired stamp must deny without installed hub copy")
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
    if matcher != "Write|Delete":
        print(f"ASSERT:FAIL hooks.json matcher must be Write|Delete got {matcher!r}")
        return 1

    print("ASSERT:PASS goal-write hook landmine")
    return 0


if __name__ == "__main__":
    sys.exit(main())
