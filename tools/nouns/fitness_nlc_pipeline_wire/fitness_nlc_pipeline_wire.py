#!/usr/bin/env python3
"""Fitness: nlc-pipeline-wire.py sequences X1→X6 on the ok specimen (ADR 0030)."""

from __future__ import annotations



import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WIRE = ROOT / "tools" / "nlc-pipeline-wire.py"
SPEC = ROOT / "examples" / "pipeline-wire-ok" / "pipeline.json"


def main() -> int:
    if not WIRE.is_file():
        print("fitness-nlc-pipeline-wire: MISSING tools/nlc-pipeline-wire.py")
        return 1
    if not SPEC.is_file():
        print("fitness-nlc-pipeline-wire: MISSING examples/pipeline-wire-ok/pipeline.json")
        return 1
    data = json.loads(SPEC.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        plan = out / "plan.json"
        audit = out / "audit.json"
        manifest = out / "emit-manifest.json"
        gates = out / "action-gates.json"
        plan.write_text(json.dumps(data["plan"], indent=2) + "\n", encoding="utf-8")
        audit.write_text(json.dumps(data["audit"], indent=2) + "\n", encoding="utf-8")
        manifest.write_text(json.dumps(data["manifest"], indent=2) + "\n", encoding="utf-8")
        gates.write_text(json.dumps(data["action_gates"], indent=2) + "\n", encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(WIRE),
                "--plan",
                str(plan),
                "--audit",
                str(audit),
                "--manifest",
                str(manifest),
                "--action-gates",
                str(gates),
            ],
            capture_output=True,
            text=True,
        )
    if proc.returncode != 0 or "PIPELINE:ALL_MET" not in (proc.stdout or ""):
        print("fitness-nlc-pipeline-wire: specimen did not ALL_MET")
        print(proc.stdout)
        print(proc.stderr)
        return 1
    print("fitness-nlc-pipeline-wire: MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

