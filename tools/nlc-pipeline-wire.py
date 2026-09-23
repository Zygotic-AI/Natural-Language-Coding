#!/usr/bin/env python3
"""Wire X1/X2/X3 into the PLANIT pipeline (ADR 0024 / 0030).

This module is the single call site the planit skill and nlc-maintainer invoke.
It does not replace the individual runners; it sequences them and fails closed.

Pipeline order (ADR 0024):
  1. action-plan gate  (X1)  -- every action maps to a plan step
  2. reverse audit     (X2)  -- every applicable ADR is bound to an action
  3. emit              -- caller writes artifact + emit-manifest.json
  4. emit audit        (X5)  -- every emit has an audit
  5. emit-manifest     (X3)  -- manifest matches schema, unused=na, gate closed
  6. bound ADR gates   (X6)  -- gates of ADRs bound to this action, default-closed

Usage:
  python3 tools/nlc-pipeline-wire.py --plan <plan.json> --audit <audit.json> \
      --manifest <emit-manifest.json> --action-gates <gates.json>

Exit 0 = all stages MET. Exit 1 = first failing stage, with RESULT:NOT_MET.
Missing inputs are refused (default-closed), never skipped.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


def stage(name: str, cmd: list[str]) -> bool:
    code, out = run(cmd)
    sys.stdout.write(out)
    if code != 0:
        print(f"PIPELINE:FAIL stage={name}")
        return False
    if "RESULT:NOT_MET" in out:
        print(f"PIPELINE:FAIL stage={name}")
        return False
    print(f"PIPELINE:MET stage={name}")
    return True


def main() -> int:
    hub_tool()
    p = argparse.ArgumentParser(description="NLC pipeline wire (X1->X2->X3->X5->X6)")
    p.add_argument("--plan", type=Path, required=True, help="plan JSON (steps+actions)")
    p.add_argument("--audit", type=Path, required=True, help="reverse-audit JSON")
    p.add_argument("--manifest", type=Path, required=True, help="emit-manifest.json")
    p.add_argument(
        "--action-gates",
        type=Path,
        required=True,
        help="JSON list of gate commands for bound ADRs",
    )
    p.add_argument(
        "--skip-action-gates",
        action="store_true",
        help="Skip X6 (bound ADR gates) -- only for dry runs; still logged",
    )
    args = p.parse_args()

    for label, path in (
        ("plan", args.plan),
        ("audit", args.audit),
        ("manifest", args.manifest),
        ("action-gates", args.action_gates),
    ):
        if not path.is_file():
            print(f"PIPELINE:FAIL missing {label} file: {path}")
            return 1

    if not stage("X1-action-plan", [sys.executable, str(TOOLS / "nlc-action-plan-gate.py"), str(args.plan)]):
        return 1
    if not stage("X2-reverse-audit", [sys.executable, str(TOOLS / "nlc-reverse-audit.py"), str(args.audit)]):
        return 1
    if not stage("X5-emit-audit", [sys.executable, str(TOOLS / "nlc_emit_audit.py"), str(args.manifest)]):
        return 1
    if not stage("X3-emit-manifest", [sys.executable, str(TOOLS / "nlc-emit-manifest-enforce.py"), str(args.manifest)]):
        return 1

    if args.skip_action_gates:
        print("PIPELINE:MET stage=X6-action-gates (skipped)")
    else:
        if not stage(
            "X6-action-gates",
            [sys.executable, str(TOOLS / "nlc-action-gates.py"), str(args.action_gates)],
        ):
            return 1

    print("PIPELINE:ALL_MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
