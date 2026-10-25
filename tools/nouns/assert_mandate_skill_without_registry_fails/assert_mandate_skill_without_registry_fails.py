"""Known-bad: a Planit skill edit without a registry move is a produce-time refuse."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ".agents/skills/planit/SKILL.md"


def _scratch_hub() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="mandate-pins-"))
    dest = tmp / "hub"
    shutil.copytree(
        ROOT,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"),
    )
    subprocess.run(["git", "init"], cwd=dest, check=True, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "scratch base"],
        cwd=dest,
        check=True,
        capture_output=True,
    )
    return dest


def main() -> int:
    hub = _scratch_hub()
    skill = hub / CANONICAL
    skill.write_text(skill.read_text(encoding="utf-8") + "\n<!-- no registry -->\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(hub / "tools" / "nlc-skill-author-check.py"), "--root", str(hub / ".agents" / "skills")],
        cwd=str(hub),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    fitness = subprocess.run(
        [sys.executable, str(hub / "tools" / "fitness-mandate-inheritance.py")],
        cwd=str(hub),
        capture_output=True,
        text=True,
    )
    fit_out = (fitness.stdout or "") + (fitness.stderr or "")
    if "mandate-pins" not in out and "mandate-pins" not in fit_out:
        print("ASSERT:FAIL produce-time refuse missing mandate-pins")
        print(out[-1500:])
        print(fit_out[-1500:])
        return 1
    if fitness.returncode == 0 and "MANDATE_INHERITANCE:NOT_MET" not in fit_out:
        print("ASSERT:FAIL mandate inheritance must NOT_MET without registry move")
        print(fit_out[-1500:])
        return 1
    print("ASSERT:PASS skill edit without registry move refused at produce time")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
