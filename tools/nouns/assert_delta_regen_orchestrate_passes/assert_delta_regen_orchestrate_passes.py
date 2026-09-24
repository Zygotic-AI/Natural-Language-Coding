"""Landmine UC9 v2: delta-regen --orchestrate --write-queue emits v2 plan + queue."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DELTA = ROOT / "tools" / "nlc-delta-regen.py"
FIXTURE = ROOT / "examples" / "goal-bindings-narrow-missing"


def main() -> int:
    if not DELTA.is_file():
        print("ASSERT:FAIL missing nlc-delta-regen.py")
        return 1
    with tempfile.TemporaryDirectory(prefix="uc9-orchestrate-") as tmp:
        root = Path(tmp)
        shutil.copytree(FIXTURE, root, dirs_exist_ok=True)
        (root / "rules" / "goal-bindings.json").write_text(
            '{"schema":1,"goals":{"one":{"rules":["r1"]},"two":{"rules":[]}}}\n',
            encoding="utf-8",
        )
        proc = subprocess.run(
            [
                sys.executable,
                str(DELTA),
                str(root),
                "--change",
                "rule:r1",
                "--orchestrate",
                "--write-queue",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode != 0:
            print("ASSERT:FAIL delta-regen orchestrate exit non-zero")
            print(out)
            return 1
        if "DELTA_REGEN:ORCHESTRATE" not in out:
            print("ASSERT:FAIL missing DELTA_REGEN:ORCHESTRATE lines")
            return 1
        queue = root / ".nlc" / "delta-regen-queue.json"
        if not queue.is_file():
            print("ASSERT:FAIL missing .nlc/delta-regen-queue.json")
            return 1
        data = json.loads(queue.read_text(encoding="utf-8"))
        if data.get("version") != 2:
            print(f"ASSERT:FAIL queue version expected 2 got {data.get('version')}")
            return 1
        goals = data.get("goals_to_regen") or []
        if goals != ["one"]:
            print(f"ASSERT:FAIL expected goals_to_regen ['one'], got {goals}")
            return 1
    print("ASSERT:PASS UC9 v2 orchestrated rule-tagged delta-regen")
    return 0
