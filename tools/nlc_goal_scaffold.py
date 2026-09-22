#!/usr/bin/env python3
"""ADR 0023: scaffold goals/<id>/implementation.py with rule receipt placeholders."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from nlc_requirements import hub_tool

GOAL_ID_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


def load_rule_ids(rules_path: Path) -> list[str]:
    if not rules_path.is_file():
        return []
    data = json.loads(rules_path.read_text(encoding="utf-8"))
    out: list[str] = []
    for row in data.get("adoptions") or []:
        if isinstance(row, dict) and row.get("rule_id"):
            out.append(str(row["rule_id"]))
    return sorted(set(out))


def render_implementation(goal_id: str, rule_ids: list[str]) -> str:
    from nlc_rule_marker import marker_line

    fn = goal_id.replace("-", "_")
    lines = [
        f'"""Goal {goal_id} — regenerate via /planit step 6; do not hand-edit to pass audits."""',
        "",
        f"def {fn}() -> None:",
        '    """Public goal entrypoint."""',
    ]
    if rule_ids:
        lines.append("    # Adopted rules — emit marker at each enforcement site (ADR 0023):")
        for rid in rule_ids:
            lines.append(f"    {marker_line(rid, 'python')}")
    else:
        lines.append("    # nlc:rule=<rule_id>  # at each enforcement site (ADR 0023)")
    lines.append("    pass")
    lines.append("")
    return "\n".join(lines)


def write_scaffold(root: Path, goal_id: str, *, force: bool) -> Path:
    if not GOAL_ID_RE.match(goal_id):
        raise ValueError("goal id must be lowercase slug (a-z0-9_-)")
    goal_dir = root / "goals" / goal_id
    goal_dir.mkdir(parents=True, exist_ok=True)
    path = goal_dir / "implementation.py"
    if path.is_file() and not force:
        raise FileExistsError(f"exists: {path.relative_to(root)} (use --force)")
    rules = root / "rules" / "adopted.json"
    text = render_implementation(goal_id, load_rule_ids(rules))
    path.write_text(text, encoding="utf-8")
    return path


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Scaffold goal implementation with ADR 0023 markers")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--goal", required=True, help="Goal id directory under goals/")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    from nlc_uc_blockers import ensure_before_generate_stamp

    stamp = ensure_before_generate_stamp(root)
    if stamp:
        print(stamp[0], file=sys.stderr)
        return 2
    try:
        path = write_scaffold(root, args.goal.strip(), force=args.force)
    except (ValueError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    rel = str(path.relative_to(root)).replace("\\", "/")
    from nlc_gate_scope import add_scope_path
    from nlc_generate_provenance import record_generate

    add_scope_path(root, rel)
    record_generate(root, rel, "goal-scaffold")
    from nlc_rule_runner import materialize_ir, write_snapshot

    write_snapshot(root, materialize_ir(root))
    print(f"goal-scaffold: MET {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
