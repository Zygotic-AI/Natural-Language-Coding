#!/usr/bin/env python3
"""R21 v1: print callers from code. Do not commit the output.

Scans goals/**/*.py for <name>.<verb>( call sites. Writes JSON to stdout
with a generated marker. Hand-checked-in graphs stay forbidden by
fitness-no-hand-authored-graphs.py.

Input: optional argv root. No args → hub ROOT.
Output: JSON on stdout. Exit 0 always unless the tree cannot be read.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALL = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\s*\(")
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
SKIP_CALLEES = {"print", "len", "int", "str", "dict", "list", "set", "Path"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def is_test(path: Path) -> bool:
    return (
        "tests" in path.parts
        or path.name.startswith("test_")
        or path.name.endswith("_test.py")
    )




def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def goal_files(root: Path) -> list[Path]:
    files = []
    for base_name in ("goals",):
        direct = root / base_name
        if direct.is_dir():
            files.extend(
                p for p in direct.rglob("*.py") if p.is_file() and not is_skipped(p) and not is_test(p)

            )
    examples = root / "examples"
    if examples.is_dir():
        for goals in examples.rglob("goals"):
            if goals.is_dir() and goals.name == "goals" and not is_skipped(goals):
                files.extend(
                    p for p in goals.rglob("*.py") if p.is_file() and not is_skipped(p) and not is_test(p)

                )
    return sorted(set(files))


def goal_id(path: Path) -> str:
    parts = path.parts
    if "goals" in parts:
        i = parts.index("goals")
        if i + 1 < len(parts):
            return parts[i + 1]
    return path.stem


def build(root: Path) -> dict:
    goals: dict[str, dict] = {}
    for path in goal_files(root):
        gid = goal_id(path)
        text = path.read_text(errors="replace")
        calls = []
        for match in CALL.finditer(text):
            obj, verb = match.group(1), match.group(2)
            if verb in SKIP_CALLEES:
                continue
            calls.append(f"{obj}.{verb}")
        entry = goals.setdefault(gid, {"path": rel(path), "calls": []})
        for c in calls:
            if c not in entry["calls"]:
                entry["calls"].append(c)
    return {
        "generated": True,
        "do_not_edit": True,
        "source": "tools/generate-impact-graph.py",
        "goals": goals,
    }


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    json.dump(build(root), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
