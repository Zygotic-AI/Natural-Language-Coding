"""Landmine: dangling commit ref in evidence-unresolved-ref specimen must REFUSE."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = ROOT / "examples" / "evidence-unresolved-ref" / "integrity" / "evidence-dangling-ref.json"


def main() -> int:
    if not SPEC.is_file():
        print("ASSERT:FAIL missing evidence-unresolved-ref specimen")
        return 1
    data = json.loads(SPEC.read_text(encoding="utf-8"))
    dangling = str(data.get("dangling_commit_ref") or "").strip()
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "nlc_release_tag_gate.py"),
            "--check",
            "--commit",
            dangling,
            "--tag",
            "v0.2.0",
            "--skip-verify-deep",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 2:
        print(f"ASSERT:FAIL expected REFUSE exit 2, got {proc.returncode}")
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "RELEASE_TAG_GATE:REFUSE" not in combined:
        print("ASSERT:FAIL expected RELEASE_TAG_GATE:REFUSE")
        return 1
    print("ASSERT:PASS evidence unresolved ref REFUSE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
