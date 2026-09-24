#!/usr/bin/env python3
"""UC18 v1 harness doc + hooks.example (P6.4)."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HARNESS = ROOT / "docs" / "nlc" / "HARNESS.md"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    hooks = [
        ROOT / "templates" / "adopter" / "hooks.example.json",
        ROOT / ".nlc" / "hooks.example.json",
    ]
    if not any(p.is_file() for p in hooks):
        violations.append("missing hooks.example.json (template or .nlc)")
    if not HARNESS.is_file():
        violations.append("missing HARNESS.md")
    else:
        text = HARNESS.read_text(encoding="utf-8", errors="replace")
        for needle in ("before-generate", "hooks.example", "UC18"):
            if needle not in text:
                violations.append(f"HARNESS.md missing {needle}")
    status = json.loads((ROOT / "integrity" / "uc-product-status.json").read_text(encoding="utf-8"))
    exp = (status.get("ucs") or {}).get("UC18", {}).get("expansion_only") or []
    if exp:
        violations.append(f"UC18 expansion_only must be empty after P6.4: {exp}")
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

