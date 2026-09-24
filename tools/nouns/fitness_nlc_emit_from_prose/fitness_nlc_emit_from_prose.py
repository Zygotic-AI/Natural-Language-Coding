#!/usr/bin/env python3
"""Fitness: nlc-emit-from-prose.py compiles a prose plan end-to-end (ADR 0027)."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOL = ROOT / "tools" / "nlc-emit-from-prose.py"
WIRE = ROOT / "tools" / "nlc-pipeline-wire.py"

PROSE = """# billing
## Step s1: create invoice
- Action a1: emit Invoice.issue [adr:0001]
## Emit e1: domain/invoice.py
  trace: chose noun Invoice per ADR 0003
  anchor: noun vs goal
"""


def main() -> int:
    if not TOOL.is_file():
        print("fitness-nlc-emit-from-prose: MISSING tools/nlc-emit-from-prose.py")
        return 1
    with tempfile.TemporaryDirectory() as td:
        prose = Path(td) / "plan.md"
        out = Path(td) / "out"
        prose.write_text(PROSE, encoding="utf-8")
        r1 = subprocess.run(
            [sys.executable, str(TOOL), "--prose", str(prose), "--out", str(out)],
            capture_output=True, text=True,
        )
        if r1.returncode != 0 or "EMIT:MET" not in r1.stdout:
            print("fitness-nlc-emit-from-prose: compile failed")
            print(r1.stdout); print(r1.stderr)
            return 1
        for name in ("plan.json", "audit.json", "emit-manifest.json", "action-gates.json"):
            if not (out / name).is_file():
                print(f"fitness-nlc-emit-from-prose: missing {name}")
                return 1
        manifest = json.loads((out / "emit-manifest.json").read_text())
        if manifest.get("unused") != "na":
            print("fitness-nlc-emit-from-prose: unused != na")
            return 1
        r2 = subprocess.run(
            [sys.executable, str(WIRE),
             "--plan", str(out / "plan.json"),
             "--audit", str(out / "audit.json"),
             "--manifest", str(out / "emit-manifest.json"),
             "--action-gates", str(out / "action-gates.json")],
            capture_output=True, text=True,
        )
        if r2.returncode != 0 or "PIPELINE:ALL_MET" not in r2.stdout:
            print("fitness-nlc-emit-from-prose: wire did not ALL_MET")
            print(r2.stdout); print(r2.stderr)
            return 1
    print("fitness-nlc-emit-from-prose: MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
