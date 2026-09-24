"""UC14 / ADR 0012: adopt-time check for conflicting rules."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(errors="replace"))


def tier_index(tiers: list[str], name: str) -> int:
    try:
        return tiers.index(name)
    except ValueError:
        return -1


def match_key(rule: dict) -> str:
    match = rule.get("match") or {}
    tags = match.get("tags_all") or []
    prim = match.get("primitive") or ""
    return "|".join(sorted(tags)) + "|" + str(prim)


def effects_conflict(a: dict, b: dict) -> bool:
    ea, eb = a.get("effect"), b.get("effect")
    if ea == "forbid" and eb == "must":
        return True
    if ea == "must" and eb == "forbid":
        return True
    if ea == "must" and eb == "must":
        oa = (a.get("obligation") or "").strip()
        ob = (b.get("obligation") or "").strip()
        if oa and ob and oa != ob:
            return True
    return False


def rule_strength(tiers: list[str], rule: dict) -> tuple[int, int]:
    tier = rule.get("precedence_tier") or "project"
    ti = tier_index(tiers, tier)
    rank = int(rule.get("precedence_rank") or 0)
    return ti, rank


def winner(
    tiers: list[str],
    a: dict,
    b: dict,
    overrides: list[dict],
    key: str,
) -> str | None:
    sa, sb = rule_strength(tiers, a), rule_strength(tiers, b)
    if sa != sb:
        return a["rule_id"] if sa > sb else b["rule_id"]
    for ov in overrides:
        if ov.get("conflict_key") == key:
            return ov.get("winner")
    return None


def main(argv: list[str] | None = None, hub_root: Path | None = None) -> int:
    hub = (hub_root or HUB_ROOT).resolve()
    args = argv if argv is not None else sys.argv[1:]
    if len(args) < 1:
        sys.stderr.write(
            "usage: check-rule-adoption.py <rules.json> [--overrides path]\n"
        )
        return 2

    rules_path = Path(args[0]).resolve()
    overrides_path = hub / "integrity" / "precedence-overrides.json"
    if "--overrides" in args:
        i = args.index("--overrides")
        if i + 1 < len(args):
            overrides_path = Path(args[i + 1]).resolve()

    prec = load_json(hub / "integrity" / "adr-precedence.json")
    tiers: list[str] = list(prec.get("tiers") or [])
    overrides_doc = load_json(overrides_path)
    overrides: list[dict] = list(overrides_doc.get("overrides") or [])

    doc = load_json(rules_path)
    adoptions: list[dict] = list(doc.get("adoptions") or [])

    by_key: dict[str, list[dict]] = {}
    for rule in adoptions:
        if not rule.get("rule_id"):
            sys.stdout.write("ADOPTION:NOT_MET\nmissing rule_id\n")
            return 1
        key = match_key(rule)
        by_key.setdefault(key, []).append(rule)

    conflicts: list[str] = []
    for key, group in by_key.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                if not effects_conflict(a, b):
                    continue
                w = winner(tiers, a, b, overrides, key)
                if w is None:
                    conflicts.append(
                        f"{key}: {a['rule_id']} vs {b['rule_id']} "
                        "(tie; need precedence-overrides.json)"
                    )

    if conflicts:
        sys.stdout.write("ADOPTION:NOT_MET\n")
        for line in conflicts:
            sys.stdout.write(line + "\n")
        return 1

    sys.stdout.write("ADOPTION:MET\n")
    sys.stdout.write(f"rules_checked: {len(adoptions)}\n")
    return 0
