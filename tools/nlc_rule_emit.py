#!/usr/bin/env python3
"""ADR 0023: compiler-owned nlc:rule= receipts on goal generate/regen."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from nlc_requirements import hub_tool
from nlc_rule_coverage import MARKER_RE, load_adopted
from nlc_rule_marker import marker_line
from nlc_uc9_bindings import load_goal_bindings

GOAL_ID_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


def existing_rule_ids(text: str) -> set[str]:
    return {m.group(1) for m in MARKER_RE.finditer(text)}


def _first_def_body_insert(lines: list[str]) -> tuple[int, str]:
    def_idx = -1
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("def ") and stripped.endswith(":"):
            def_idx = i
            break
    if def_idx < 0:
        return len(lines), "    "
    j = def_idx + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    indent = "    "
    if j < len(lines):
        m = re.match(r"^(\s*)", lines[j])
        if m and m.group(1):
            indent = m.group(1)
        s = lines[j].lstrip()
        if s.startswith('"""') or s.startswith("'''"):
            quote = s[:3]
            if s.count(quote) >= 2 and len(s) > 3:
                j += 1
            else:
                j += 1
                while j < len(lines) and quote not in lines[j]:
                    j += 1
                j += 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                m2 = re.match(r"^(\s*)", lines[j])
                if m2 and m2.group(1):
                    indent = m2.group(1)
    return j, indent


def apply_markers_to_source(text: str, rule_ids: list[str]) -> tuple[str, list[str]]:
    """Insert missing compiler markers; return new text and ids added."""
    have = existing_rule_ids(text)
    missing = [rid for rid in rule_ids if rid not in have]
    if not missing:
        return text, []
    lines = text.splitlines()
    insert_at, indent = _first_def_body_insert(lines)
    new_lines: list[str] = []
    if insert_at == len(lines) or not any(l.strip() for l in lines):
        if lines and lines[-1].strip():
            lines.append("")
    if insert_at > 0 and insert_at <= len(lines):
        prev = lines[insert_at - 1] if insert_at else ""
        if prev.strip() and not prev.rstrip().endswith(":"):
            pass
    block = [f"{indent}{marker_line(rid, 'python')}" for rid in missing]
    out = lines[:insert_at] + block + lines[insert_at:]
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), missing


def rule_ids_for_goal(root: Path, goal_id: str) -> list[str]:
    bindings = load_goal_bindings(root)
    meta = bindings.get(goal_id) if isinstance(bindings.get(goal_id), dict) else None
    if meta and meta.get("rules"):
        return sorted({str(r) for r in meta["rules"]})
    rules_path = root / "rules" / "adopted.json"
    if not rules_path.is_file():
        return []
    return sorted({str(r["rule_id"]) for r in load_adopted(rules_path)})


def sync_goal_implementation(root: Path, goal_id: str, *, dry_run: bool = False) -> tuple[Path, list[str]]:
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
        path, added = sync_goal_implementation(root, args.goal.strip(), dry_run=args.dry_run)
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    rel = path.relative_to(root)
    rel_s = str(rel).replace("\\", "/")

    def _post_emit() -> None:
        from nlc_gate_scope import add_scope_path
        from nlc_generate_provenance import record_generate
        from nlc_rule_runner import materialize_ir, write_snapshot

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
