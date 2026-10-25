"""Known-bad: activation with staged bytes but no sidecar must refuse and leave live untouched."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ".agents/skills/planit/SKILL.md"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _scratch_hub() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="split-land-"))
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
    before = _sha(hub / CANONICAL)
    stage = subprocess.run(
        [
            sys.executable,
            str(hub / "tools" / "stage-gate-machinery.py"),
            "--change-id",
            "split-land",
            "--path",
            CANONICAL,
        ],
        cwd=str(hub),
        capture_output=True,
        text=True,
    )
    if stage.returncode != 0:
        print("ASSERT:FAIL could not stage")
        print((stage.stdout or "") + (stage.stderr or ""))
        return 1
    staged = hub / "staging" / "split-land" / CANONICAL
    staged.write_text(staged.read_text(encoding="utf-8") + "\n<!-- staged -->\n", encoding="utf-8")
    activate = subprocess.run(
        [
            sys.executable,
            str(hub / "tools" / "activate-gate-machinery.py"),
            "--change-id",
            "split-land",
        ],
        cwd=str(hub),
        capture_output=True,
        text=True,
    )
    out = (activate.stdout or "") + (activate.stderr or "")
    after = _sha(hub / CANONICAL)
    if activate.returncode == 0 or "ACTIVATE:NOT_MET" not in out:
        print("ASSERT:FAIL split land (no sidecar) must refuse")
        print(out[-2000:])
        return 1
    if after != before:
        print("ASSERT:FAIL live path changed despite refused activate")
        return 1
    print("ASSERT:PASS split land refused and live untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
