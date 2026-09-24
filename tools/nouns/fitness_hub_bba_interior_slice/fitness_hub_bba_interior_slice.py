#!/usr/bin/env python3
"""X4 v2: hub tools/ emit-path modules carry BBA boundary markers.

This is a constrained slice, not a full interior rewrite. It asserts that
the hub's own emit-path modules (see EMIT_PATH_MODULES allowlist)
declare their BBA role via a module-level BOUNDARY marker, so the hub's
emit surface is itself boundary-shaped.

Full noun/verb package rewrite of tools/*.py remains future work.
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EMIT_PATH_MODULES = (
    ROOT / "tools" / "nlc-init.py",
    ROOT / "tools" / "nlc_distribution.py",
    ROOT / "tools" / "nlc_requirements.py",
    ROOT / "tools" / "nlc-pack-install.py",
    ROOT / "tools" / "nlc-pack-export.py",
    ROOT / "tools" / "nlc-pack-ingest.py",
    ROOT / "tools" / "nlc-pipeline-wire.py",
    ROOT / "tools" / "nlc-before-generate.py",
    ROOT / "tools" / "nlc-emit-from-prose.py",
    ROOT / "tools" / "nlc_goal_scaffold.py",
    ROOT / "tools" / "nlc_rule_emit.py",
)
MARKER = 'BOUNDARY = "bba-emit"'


def has_marker(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "BOUNDARY":
                    if isinstance(node.value, ast.Constant) and node.value.value == "bba-emit":
                        return True
    return False


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in EMIT_PATH_MODULES:
        if not path.is_file():
            violations.append(f"missing {path.relative_to(ROOT)}")
            continue
        if not has_marker(path):
            violations.append(f"{path.relative_to(ROOT)} lacks {MARKER}")
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
