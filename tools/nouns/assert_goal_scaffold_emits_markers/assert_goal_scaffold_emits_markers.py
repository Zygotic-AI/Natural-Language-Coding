"""Landmine ADR 0023: goal-scaffold emits nlc:rule= lines for adopted rules."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MINIMAL = ROOT / "examples" / "rule-coverage-minimal"
TOOL = ROOT / "tools" / "nlc_goal_scaffold.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(MINIMAL / "rules", work / "rules")
        proc = subprocess.run(
            [sys.executable, str(TOOL), "--root", str(work), "--goal", "demo"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print(f"ASSERT:FAIL goal-scaffold exit {proc.returncode}: {proc.stderr}")
            return 1
        impl = work / "goals" / "demo" / "implementation.py"
        text = impl.read_text(encoding="utf-8")
        if "# nlc:rule=demo-verb-only" not in text:
            print("ASSERT:FAIL scaffold missing rule marker")
            print(text)
            return 1
    print("ASSERT:PASS goal-scaffold emits ADR 0023 markers")
    return 0


