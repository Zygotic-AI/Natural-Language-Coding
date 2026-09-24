"""Landmine: full-nlc-audit --emit-inference-checklist exits 0 and prints checklist path."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "full-nlc-audit.py"),
            "--emit-inference-checklist",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        print("ASSERT:FAIL emit-inference-checklist exit", proc.returncode)
        print(out)
        return 1
    if "INFERENCE_CHECKLIST:" not in out:
        print("ASSERT:FAIL missing INFERENCE_CHECKLIST: prefix")
        print(out)
        return 1
    skill = ROOT / ".agents" / "skills" / "full-nlc-audit" / "SKILL.md"
    skill_text = skill.read_text(encoding="utf-8", errors="replace") if skill.is_file() else ""
    if "--emit-inference-checklist" not in skill_text:
        print("ASSERT:FAIL skill must document --emit-inference-checklist")
        return 1
    print("ASSERT:PASS full-nlc-audit emit-inference-checklist")
    return 0


