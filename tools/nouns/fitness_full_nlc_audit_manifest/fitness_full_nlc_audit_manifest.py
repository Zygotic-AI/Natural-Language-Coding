#!/usr/bin/env python3
"""Every full-nlc-audit manifest profile stage resolves to command or builtin."""

from __future__ import annotations



import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "integrity" / "full-nlc-audit-manifest.json"
SCRIPT = ROOT / "tools" / "full-nlc-audit.py"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not MANIFEST.is_file():
        violations.append("missing integrity/full-nlc-audit-manifest.json")
        print("RESULT:NOT_MET")
        return 1

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    stages = data.get("stages") or {}
    profiles = data.get("profiles") or {}
    script_text = SCRIPT.read_text(encoding="utf-8") if SCRIPT.is_file() else ""

    for profile, ids in profiles.items():
        if not isinstance(ids, list):
            violations.append(f"profile {profile} must be a list")
            continue
        for sid in ids:
            spec = stages.get(sid)
            if not spec:
                violations.append(f"profile {profile}: unknown stage id {sid}")
                continue
            if spec.get("builtin"):
                b = str(spec["builtin"])
                if f'"{b}"' not in script_text:
                    violations.append(f"stage {sid}: unknown builtin {b} in full-nlc-audit.py")
            elif spec.get("command"):
                continue
            else:
                violations.append(f"stage {sid}: needs command or builtin")

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

