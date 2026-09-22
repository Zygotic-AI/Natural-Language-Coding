#!/usr/bin/env python3
"""Landmine ADR 0023: rule-emit inserts missing nlc:rule= markers on generate."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MINIMAL = ROOT / "examples" / "rule-coverage-minimal"
TOOL = ROOT / "tools" / "nlc_rule_emit.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(MINIMAL / "rules", work / "rules")
        (work / "goals" / "demo").mkdir(parents=True)
        nlc = work / ".nlc"
        nlc.mkdir(parents=True)
        (nlc / "before-generate-stamp.json").write_text(
            '{"ok":true,"at":"2026-09-20T20:00:00Z","scopes":["demo"]}\n',
            encoding="utf-8",
        )
        (work / "goals" / "demo" / "implementation.py").write_text(
            '"""Goal demo."""\n\n\ndef run_demo() -> None:\n    pass\n',
            encoding="utf-8",
        )
        proc = subprocess.run(
            [sys.executable, str(TOOL), "--root", str(work), "--goal", "demo"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            print(f"ASSERT:FAIL rule-emit exit {proc.returncode}: {proc.stderr}")
            return 1
        text = (work / "goals" / "demo" / "implementation.py").read_text(encoding="utf-8")
        if "# nlc:rule=demo-verb-only" not in text:
            print("ASSERT:FAIL rule-emit did not insert marker")
            print(text)
            return 1
    print("ASSERT:PASS rule-emit syncs ADR 0023 markers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
