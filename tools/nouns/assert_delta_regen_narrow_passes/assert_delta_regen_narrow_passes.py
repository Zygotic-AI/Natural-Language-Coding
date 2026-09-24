"""Landmine UC9: goals_for_rule_change narrows with goal-bindings.json."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_uc9_bindings import goals_for_rule_change

    import shutil
    import tempfile

    src = ROOT / "examples" / "goal-bindings-narrow-missing"
    with tempfile.TemporaryDirectory(prefix="uc9-narrow-") as tmp:
        root = Path(tmp)
        shutil.copytree(src, root, dirs_exist_ok=True)
        all_goals = ["one", "two"]
        graph = {"goals": {g: {} for g in all_goals}}
        narrowed, msg = goals_for_rule_change(root, graph, "r1", all_goals)
        if narrowed != all_goals:
            print(f"ASSERT:FAIL without bindings expected all goals, got {narrowed}: {msg}")
            return 1
        bindings = root / "rules" / "goal-bindings.json"
        bindings.write_text(
            '{"schema":1,"goals":{"one":{"rules":["r1"]},"two":{"rules":[]}}}\n',
            encoding="utf-8",
        )
        narrowed2, _msg = goals_for_rule_change(root, graph, "r1", all_goals)
        if narrowed2 != ["one"]:
            print(f"ASSERT:FAIL expected ['one'], got {narrowed2}")
            return 1
    print("ASSERT:PASS goals_for_rule_change narrows with bindings (UC9)")
    return 0


