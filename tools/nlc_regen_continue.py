"""UC9: guided next step for delta-regen queue."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def regen_continue(root: Path) -> int:
    from nlc_guide_state import start_planit

    path = root / ".nlc" / "delta-regen-queue.json"
    if not path.is_file():
        print("No rebuild queue. Nothing to continue.", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Rebuild queue file is invalid.", file=sys.stderr)
        return 1
    steps = data.get("steps") or []
    if not steps:
        print("Rebuild queue is empty.", file=sys.stderr)
        return 0
    cur_path = root / ".nlc" / "regen-current.json"
    index = 0
    if cur_path.is_file():
        try:
            cur = json.loads(cur_path.read_text(encoding="utf-8"))
            index = int(cur.get("index", 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            index = 0
    if index >= len(steps):
        cur_path.unlink(missing_ok=True)
        print("Rebuild queue complete. Run ./nlc maintainer requirements then ./nlc verify-deep.")
        return 0
    step = steps[index]
    gid = step.get("goal_id", "?")
    label = f"Rebuild goal {gid} ({index + 1}/{len(steps)})"
    start_planit(root, label)
    cur_path.write_text(
        json.dumps({"index": index, "goal_id": gid}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(label)
    print(f"  Path: {step.get('path', '')}")
    print("  Next: /planit in your agent — one goal, then run:")
    print("        ./nlc maintainer regen-advance")
    if step.get("planit"):
        for line in step["planit"]:
            print(f"    - {line}")
    return 0


def regen_advance(root: Path) -> int:
    from nlc_guide_state import end_planit

    path = root / ".nlc" / "delta-regen-queue.json"
    cur_path = root / ".nlc" / "regen-current.json"
    if not cur_path.is_file():
        print("No rebuild in progress. Run ./nlc maintainer regen-continue first.", file=sys.stderr)
        return 1
    try:
        cur = json.loads(cur_path.read_text(encoding="utf-8"))
        index = int(cur.get("index", 0)) + 1
    except (json.JSONDecodeError, TypeError, ValueError):
        index = 1
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            steps = data.get("steps") or []
            if index >= len(steps):
                path.unlink(missing_ok=True)
                cur_path.unlink(missing_ok=True)
                end_planit(root)
                print("Rebuild queue finished. Run ./nlc verify-deep")
                return 0
            cur_path.write_text(
                json.dumps({"index": index, "goal_id": steps[index].get("goal_id")}, indent=2)
                + "\n",
                encoding="utf-8",
            )
        except json.JSONDecodeError:
            pass
    end_planit(root)
    print(f"Advanced. Run ./nlc maintainer regen-continue for the next goal.")
    return 0
