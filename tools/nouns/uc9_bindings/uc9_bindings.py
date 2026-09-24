"""UC9 goal ↔ rule/tag bindings for blast-radius (shared)."""

from __future__ import annotations

import json
from pathlib import Path

BOUNDARY = "bba-emit"


def load_goal_bindings(root: Path) -> dict[str, dict]:
    path = root / "rules" / "goal-bindings.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    goals = data.get("goals")
    return goals if isinstance(goals, dict) else {}


def load_rule_adoption(root: Path, rule_id: str) -> dict | None:
    path = root / "rules" / "adopted.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    for row in data.get("adoptions") or []:
        if row.get("rule_id") == rule_id:
            return row
    return None


def rule_match_tags(rule: dict) -> set[str]:
    match = rule.get("match") or {}
    tags: set[str] = set()
    for key in ("tags_all", "tags_any"):
        for t in match.get(key) or []:
            tags.add(str(t))
    return tags


def goals_for_rule_change(
    root: Path,
    graph: dict,
    rule_id: str,
    all_goal_ids: list[str],
) -> tuple[list[str], str]:
    bindings = load_goal_bindings(root)
    rule = load_rule_adoption(root, rule_id)
    rule_tags = rule_match_tags(rule) if rule else set()

    if not bindings:
        return all_goal_ids, (
            f"conservative regen for rule {rule_id} "
            "(add rules/goal-bindings.json to narrow)"
        )

    graph_goals = graph.get("goals") or {}
    matched: list[str] = []
    for gid, meta in bindings.items():
        if gid not in graph_goals:
            continue
        if rule_id in (meta.get("rules") or []):
            matched.append(gid)
            continue
        gtags = set(meta.get("tags") or [])
        if rule_tags and gtags & rule_tags:
            matched.append(gid)

    if matched:
        return sorted(set(matched)), (
            f"goal-bindings hit rule {rule_id} "
            f"(tags={sorted(rule_tags) if rule_tags else 'n/a'})"
        )
    return all_goal_ids, (
        f"conservative regen for rule {rule_id} (no binding overlap; check goal-bindings)"
    )
