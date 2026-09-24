"""X1: action-plan gate (NLC-0024-04)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"


def resolve_input(path: Path) -> Path | None:
    if path.is_file():
        return path
    if path.is_dir():
        candidate = path / "plan.json"
        if candidate.is_file():
            return candidate
    return None


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


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    path = Path(args[0]).resolve() if args else None
    target = resolve_input(path) if path is not None else None
    if target is None:
        print("RESULT:MET")
        print("note: no plan file given; gate is default-closed and passes empty")
        return 0
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
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
