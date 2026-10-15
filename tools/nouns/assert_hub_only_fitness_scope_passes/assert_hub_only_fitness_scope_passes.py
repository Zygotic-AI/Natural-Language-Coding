"""Landmine: hub_only_fitness skips apply only on non-hub product trees."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "integrity" / "releasable-gates.json"
PLANIT = ROOT / "tools" / "fitness-planit-identity.py"
INVOICE = ROOT / "examples" / "invoice-correct"
AUDIT = ROOT / "tools" / "release-audit.py"


def main() -> int:
    if not MANIFEST.is_file():
        print("ASSERT:FAIL missing releasable-gates.json")
        return 1
    hub_only = set(json.loads(MANIFEST.read_text(encoding="utf-8")).get("hub_only_fitness") or [])
    if "fitness-planit-identity.py" not in hub_only:
        print("ASSERT:FAIL planit identity must be hub-only in manifest")
        return 1

    hub_proc = subprocess.run(
        [sys.executable, str(PLANIT), "--skill-only", "--loaded", ".agents/skills/planit/SKILL.md"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    hub_out = (hub_proc.stdout or "") + (hub_proc.stderr or "")
    if "skip (hub-only" in hub_out:
        print("ASSERT:FAIL planit must not skip on hub tree")
        return 1
    if "PLANIT_IDENTITY:MET" not in hub_out and hub_proc.returncode != 0:
        print("ASSERT:FAIL planit must MET or NOT_MET on hub, not skip")
        print(hub_out[-400:])
        return 1

    adopter_proc = subprocess.run(
        [sys.executable, str(PLANIT), str(INVOICE)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    adopter_out = (adopter_proc.stdout or "") + (adopter_proc.stderr or "")
    if "skip (hub-only" not in adopter_out:
        print("ASSERT:FAIL planit must skip on adopter tree")
        return 1

    signed = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "assert-release-signed-passes.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if signed.returncode != 0:
        print("ASSERT:FAIL release-signed landmine must pass (human Released-by on product copy)")
        print((signed.stdout or "") + (signed.stderr or ""))[-500:]
        return 1

    print("ASSERT:PASS hub_only_fitness skips adopter trees only; release-signed enforces human sign-off")
    return 0


if __name__ == "__main__":
    sys.exit(main())
