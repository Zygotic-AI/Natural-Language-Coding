#!/usr/bin/env python3
"""UC20 reference TypeScript call-tree pack (P4)."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    manifest = ROOT / "integrity" / "call-tree-packs.json"
    if not manifest.is_file():
        violations.append("missing call-tree-packs.json")
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "assert-call-tree-pack-reference-passes.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("assert-call-tree-pack-reference-passes must PASS")
    status = json.loads((ROOT / "integrity" / "uc-product-status.json").read_text(encoding="utf-8"))
    exp = (status.get("ucs") or {}).get("UC20", {}).get("expansion_only") or []
    if exp:
        violations.append(f"UC20 expansion_only must be empty: {exp}")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

