"""Landmine ADR 0023: rule-emit inserts missing nlc:rule= markers on generate."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MINIMAL = ROOT / "examples" / "rule-coverage-minimal"
TOOL = ROOT / "tools" / "nlc_rule_emit.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(MINIMAL / "rules", work / "rules")
        (work / "goals" / "demo").mkdir(parents=True)
        nlc = work / ".nlc"
        nlc.mkdir(parents=True)
        stamp_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        (nlc / "before-generate-stamp.json").write_text(
            f'{{"ok":true,"at":"{stamp_at}","scopes":["demo"]}}\n',
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


