#!/usr/bin/env python3
"""O8: goal-write hook registered and hooks.json references the script."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOKS = ROOT / ".cursor" / "hooks.json"
SCRIPT = ROOT / ".cursor" / "hooks" / "nlc-goal-write-gate.sh"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not SCRIPT.is_file():
        violations.append("missing .cursor/hooks/nlc-goal-write-gate.sh")
    if not HOOKS.is_file():
        violations.append("missing .cursor/hooks.json")
    else:
        data = json.loads(HOOKS.read_text(encoding="utf-8"))
        hooks = data.get("hooks") if isinstance(data, dict) else None
        pre = hooks.get("preToolUse") if isinstance(hooks, dict) else None
        found = False
        if isinstance(pre, list):
            for entry in pre:
                if not isinstance(entry, dict):
                    continue
                cmd = entry.get("command")
                if cmd == ".cursor/hooks/nlc-goal-write-gate.sh":
                    found = True
                    if not entry.get("failClosed"):
                        violations.append("goal-write hook must set failClosed: true")
        if not found:
            violations.append("hooks.json must register nlc-goal-write-gate.sh on preToolUse")
    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
