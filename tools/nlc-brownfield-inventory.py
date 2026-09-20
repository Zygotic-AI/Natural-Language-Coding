#!/usr/bin/env python3
"""UC15 beta: inventory non-NLC product paths in an existing repo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

NLC_MARKERS = frozenset(
    {"adrs", "domain", "goals", "knowledge", "rules", ".nlc", "CONFIRM.md", "CHARTER.md"}
)
SKIP = frozenset({".git", "node_modules", "__pycache__", ".venv", "venv", "dist"})

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Brownfield inventory (UC15 beta)")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    legacy: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(p in SKIP for p in path.parts):
            continue
        rel = path.relative_to(root)
        top = rel.parts[0] if rel.parts else ""
        if top in NLC_MARKERS or str(rel) in NLC_MARKERS:
            continue
        if path.suffix in {".py", ".ts", ".js", ".go", ".java", ".cs"}:
            legacy.append(str(rel))
    payload = {
        "uc": "UC15",
        "root": str(root),
        "legacy_files": legacy[:500],
        "legacy_count": len(legacy),
        "note": "Manual BOOTSTRAP.md path; introduce one noun+goal before bulk migrate.",
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    if legacy:
        print(f"BROWNFIELD:INVENTORY count={len(legacy)}", file=sys.stderr)
    else:
        print("BROWNFIELD:INVENTORY count=0", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
