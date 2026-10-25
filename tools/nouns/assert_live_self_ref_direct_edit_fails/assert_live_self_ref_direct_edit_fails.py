"""Known-bad: a direct live self-ref edit without activation must REFUSE."""

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
    tmp = Path(tempfile.mkdtemp(prefix="live-self-ref-"))
    dest = tmp / "hub"
    shutil.copytree(
        ROOT,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"),
    )
    subprocess.run(["git", "init"], cwd=dest, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "scratch@test.invalid"], cwd=dest, check=True)
    subprocess.run(["git", "config", "user.name", "scratch"], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "scratch base with staging machinery"],
        cwd=dest,
        check=True,
        capture_output=True,
    )
    return dest


def main() -> int:
    hub = _scratch_hub()
    skill = hub / CANONICAL
    skill.write_text(skill.read_text(encoding="utf-8") + "\n<!-- live-edit -->\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(hub / "tools" / "fitness-live-self-ref-activation.py")],
        cwd=str(hub),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "LIVE_SELF_REF:NOT_MET" not in out:
        print("ASSERT:FAIL direct live member edit must REFUSE")
        print(out[-2000:])
        return 1
    if "live self-ref member edited outside activation" not in out:
        print("ASSERT:FAIL expected live-member refuse reason")
        print(out[-2000:])
        return 1
    print("ASSERT:PASS live self-ref direct edit REFUSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
