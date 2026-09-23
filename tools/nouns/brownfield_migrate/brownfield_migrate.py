"""UC15: brownfield migrate plan after inventory (scaffold goals; no auto rewrite)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import subprocess
import sys
from pathlib import Path

from nlc_requirements import hub_tool

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="UC15 brownfield migrate plan (v1)")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--write-plan", action="store_true")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write plan + run inventory-driven scaffold hints (UC15 product v1)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    inv = ROOT / "tools" / "nlc-brownfield-inventory.py"
    proc = subprocess.run(
        [sys.executable, str(inv), str(root)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "inventory failed\n")
        return proc.returncode or 1
    steps = [
        "ratify ADRs and rules/adopted.json",
        "./nlc maintainer goal-scaffold --goal <id> per new goal",
        "./nlc maintainer rule-emit --goal <id> after generate",
        "./nlc maintainer guide before-generate then verify-deep",
    ]
    payload = {"uc": "UC15", "root": str(root), "steps": steps}
    write = args.write_plan or args.apply
    if write:
        nlc = root / ".nlc"
        nlc.mkdir(parents=True, exist_ok=True)
        out = nlc / "brownfield-migrate-plan.json"
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"BROWNFIELD_MIGRATE: plan path={out}")
    else:
        print("BROWNFIELD_MIGRATE: steps")
        for s in steps:
            print(f"  - {s}")
    if args.apply:
        print("BROWNFIELD_MIGRATE: apply (v1 — scaffold hints only)")
        inv_out = (proc.stdout or "").strip().splitlines()
        for line in inv_out[-5:]:
            if line.strip():
                print(f"  inventory: {line.strip()}")
        print("  next: ./nlc maintainer goal-scaffold --goal <id> per inventory row")
    return 0


