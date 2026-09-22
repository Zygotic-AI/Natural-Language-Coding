#!/usr/bin/env python3
"""ADR 0023: scan nlc:rule=<id> markers; map ADR/tag → enforcement sites."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402
MARKER_RE = re.compile(
    r"(?:#|//)\s*nlc:rule=([A-Za-z0-9][A-Za-z0-9._-]*)",
)
SKIP_DIRS = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
SCAN_DIRS = ("goals", "domain", "adapters", "workflows")


def load_adopted(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("adoptions") or []
    return [r for r in rows if isinstance(r, dict) and r.get("rule_id")]


def parse_adr_arg(value: str) -> tuple[int, int] | int | None:
    value = value.strip().lstrip("adr:").lstrip("ADR")
    if ".." in value:
        a, b = value.split("..", 1)
        return (int(a), int(b))
    if value.isdigit():
        return int(value)
    return None


def adr_in_range(adr_id: str, spec: tuple[int, int] | int | None) -> bool:
    if spec is None:
        return True
    try:
        n = int(str(adr_id).strip())
    except ValueError:
        return False
    if isinstance(spec, tuple):
        return spec[0] <= n <= spec[1]
    return n == spec


def rule_tags(rule: dict) -> set[str]:
    match = rule.get("match") or {}
    out: set[str] = set()
    for key in ("tags_all", "tags_any"):
        for t in match.get(key) or []:
            out.add(str(t))
    return out


def filter_rules(
    rules: list[dict],
    adr_spec: tuple[int, int] | int | None,
    tag: str | None,
) -> list[dict]:
    out: list[dict] = []
    for r in rules:
        if not adr_in_range(str(r.get("adr_id", "")), adr_spec):
            continue
        if tag and tag not in rule_tags(r):
            continue
        out.append(r)
    return out


def scan_markers(root: Path) -> list[dict]:
    hits: list[dict] = []
    for dirname in SCAN_DIRS:
        base = root / dirname
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if any(p in SKIP_DIRS for p in path.parts):
                continue
            if path.suffix not in {".py", ".ts", ".js", ".tsx", ".jsx", ".mjs", ".cjs"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = str(path.relative_to(root)).replace("\\", "/")
            goal_id = ""
            if "/goals/" in rel:
                goal_id = rel.split("/goals/", 1)[1].split("/", 1)[0]
            for line_no, line in enumerate(text.splitlines(), start=1):
                for m in MARKER_RE.finditer(line):
                    hits.append(
                        {
                            "rule_id": m.group(1),
                            "file": rel,
                            "line": line_no,
                            "goal_id": goal_id or None,
                        }
                    )
    return hits


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Rule instance coverage (ADR 0023)")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--rules",
        type=Path,
        default=None,
        help="adopted rules JSON (default: <root>/rules/adopted.json)",
    )
    parser.add_argument("--adr", help="ADR id or range e.g. 0007 or 0012..0018")
    parser.add_argument("--tag", help="Filter rules matching tag")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any filtered rule has no marker site",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    rules_path = args.rules or (root / "rules" / "adopted.json")

    adr_spec = parse_adr_arg(args.adr) if args.adr else None
    adopted: list[dict] = []
    if rules_path.is_file():
        adopted = load_adopted(rules_path)
    filtered = filter_rules(adopted, adr_spec, args.tag)
    want_ids = {str(r["rule_id"]) for r in filtered}

    markers = scan_markers(root)
    if want_ids:
        markers = [m for m in markers if m["rule_id"] in want_ids]

    by_rule: dict[str, list[dict]] = {rid: [] for rid in want_ids}
    for m in markers:
        rid = m["rule_id"]
        if rid in by_rule:
            by_rule[rid].append(m)
        elif not want_ids:
            by_rule.setdefault(rid, []).append(m)

    missing = sorted(rid for rid in want_ids if not by_rule.get(rid))

    payload = {
        "root": str(root),
        "rules_file": str(rules_path) if rules_path.is_file() else None,
        "filter": {"adr": args.adr, "tag": args.tag},
        "rule_ids": sorted(want_ids) if want_ids else sorted(by_rule.keys()),
        "sites": markers,
        "missing_rule_ids": missing,
    }

    if args.as_json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"RULE_COVERAGE: root={root}")
        if args.adr:
            print(f"  adr filter: {args.adr}")
        if args.tag:
            print(f"  tag filter: {args.tag}")
        for m in markers:
            g = f" goal={m['goal_id']}" if m.get("goal_id") else ""
            print(f"  {m['rule_id']}  {m['file']}:{m['line']}{g}")
        if missing:
            print("RULE_COVERAGE:NOT_MET")
            for rid in missing:
                print(f"  missing marker: {rid}")
        else:
            print("RULE_COVERAGE:MET")

    if args.check and missing:
        return 1
    if args.check and want_ids and not markers and filtered:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
