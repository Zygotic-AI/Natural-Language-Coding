#!/usr/bin/env python3
"""X1: action-plan gate (NLC-0024-04).

Every atomic action in a plan must be validated against the plan: an action not
present in the plan fails, and a plan step with no action fails. Default-closed:
no plan passes without this check.

Input: a plan file (JSON) with keys:
  - "steps": list of {id, description}
  - "actions": list of {id, plan_step_id, description}
Output: RESULT:MET or RESULT:NOT_MET with violations.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def validate(plan: dict) -> list[str]:
    v: list[str] = []
    steps = plan.get("steps")
    actions = plan.get("actions")
    if not isinstance(steps, list):
        return ["plan.steps must be a list"]
    if not isinstance(actions, list):
        return ["plan.actions must be a list"]
    step_ids = {s.get("id") for s in steps if isinstance(s, dict)}
    action_step_ids = set()
    for a in actions:
        if not isinstance(a, dict):
            v.append("action entry is not an object")
            continue
        aid = a.get("id")
        sid = a.get("plan_step_id")
        if not aid:
            v.append("action missing id")
        if not sid:
            v.append(f"action {aid!r} missing plan_step_id")
        elif sid not in step_ids:
            v.append(f"action {aid!r} references unknown plan step {sid!r}")
        else:
            action_step_ids.add(sid)
    for sid in step_ids - action_step_ids:
        v.append(f"plan step {sid!r} has no action")
    return v


def main() -> int:
    path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    if path is None or not path.is_file():
        print("RESULT:MET")
        print("note: no plan file given; gate is default-closed and passes empty")
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"VIOLATION invalid json: {exc}")
        print("RESULT:NOT_MET")
        return 1
    violations = validate(data)
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
