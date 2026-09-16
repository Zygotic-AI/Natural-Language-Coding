#!/usr/bin/env python3
"""C10 v1: a schema version other than 1 requires an ADR.

Does not detect that a change was breaking. R12 already requires a version
field. This only fires when version is not 1 / "1".

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> version-bump-no-adr <version>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
SCHEMA_NAMES = {"input.schema.json", "output.schema.json", "failure.schema.json", "verbs.schema.json"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def is_one(value) -> bool:
    if value == 1 or value == 1.0:
        return True
    if isinstance(value, str) and value.strip() in {"1", "1.0", "v1"}:
        return True
    return False


def schema_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.json"):
        if not path.is_file() or is_skipped(path):
            continue
        if path.name in SCHEMA_NAMES:
            files.append(path)
    return files


def has_adr(root: Path) -> bool:
    base = root / "adrs"
    if not base.is_dir():
        return False
    return any(p.suffix == ".md" and p.name.lower() != "readme.md" for p in base.glob("*.md"))



def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    adr = has_adr(scan_root)
    violations = []
    for path in schema_files(scan_root):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict) or "version" not in data:
            continue
        ver = data["version"]
        if is_one(ver):
            continue
        if not adr:
            violations.append((rel(path), str(ver)))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, ver = item
            print(f"VIOLATION {path} version-bump-no-adr {ver}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
