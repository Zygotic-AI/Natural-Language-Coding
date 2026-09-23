#!/usr/bin/env python3
"""ADR 0023: compiler-owned nlc:rule= receipts on goal generate/regen (CLI adapter)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool
from nlc_uc9_bindings import load_goal_bindings
from nouns.rule_receipt.rule_receipt import (
    MARKER_RE,
    apply_markers_to_source,
    load_adopted,
    materialize_ir,
    write_snapshot,
)

GOAL_ID_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


def existing_rule_ids(text: str) -> set[str]:
    return {m.group(1) for m in MARKER_RE.finditer(text)}


def rule_ids_for_goal(root: Path, goal_id: str) -> list[str]:
    bindings = load_goal_bindings(root)
    meta = bindings.get(goal_id) if isinstance(bindings.get(goal_id), dict) else None
    if meta and meta.get("rules"):
        return sorted({str(r) for r in meta["rules"]})
    rules_path = root / "rules" / "adopted.json"
    if not rules_path.is_file():
        return []
    return sorted({str(r["rule_id"]) for r in load_adopted(rules_path)})


def sync_goal_implementation(
    root: Path, goal_id: str, *, dry_run: bool = False
) -> tuple[Path, list[str]]:
    if not GOAL_ID_RE.match(goal_id):
        raise ValueError("goal id must be lowercase slug (a-z0-9_-)")
    impl = root / "goals" / goal_id / "implementation.py"
    if not impl.is_file():
        raise FileNotFoundError(f"missing {impl.relative_to(root)}")
    rule_ids = rule_ids_for_goal(root, goal_id)
    text = impl.read_text(encoding="utf-8")
    new_text, added = apply_markers_to_source(text, rule_ids)
    if added and not dry_run:
        impl.write_text(new_text, encoding="utf-8")
    return impl, added


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(
        description="ADR 0023: apply compiler-owned nlc:rule= markers to goal implementation",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--goal", required=True, help="Goal id under goals/")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    from nlc_uc_blockers import ensure_before_generate_stamp

    if not args.dry_run:
        stamp = ensure_before_generate_stamp(root)
        if stamp:
            print(stamp[0], file=sys.stderr)
            return 2
    try:
        path, added = sync_goal_implementation(
            root, args.goal.strip(), dry_run=args.dry_run
        )
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    rel = path.relative_to(root)
    rel_s = str(rel).replace("\\", "/")

    def _post_emit() -> None:
        from nlc_gate_scope import add_scope_path
        from nlc_generate_provenance import record_generate

        add_scope_path(root, rel_s)
        record_generate(root, rel_s, "rule-emit")
        write_snapshot(root, materialize_ir(root))

    if not added:
        if not args.dry_run:
            _post_emit()
        print(f"rule-emit: MET {rel} (markers already present)")
        return 0
    if args.dry_run:
        print(f"rule-emit: WOULD_ADD {rel} " + ",".join(added))
        return 0
    _post_emit()
    print(f"rule-emit: MET {rel} added " + ",".join(added))
    return 0


if __name__ == "__main__":
    sys.exit(main())
