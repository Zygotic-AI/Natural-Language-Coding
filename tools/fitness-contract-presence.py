#!/usr/bin/env python3
"""R9/R10/C7/C8 v2: public entrypoints have schema files.

If CONFIRM has a CHANGED: list (or git is dirty under the scan root), only
touched goal/noun dirs are checked. No list and clean git → tree-wide.

Not a semantic contract checker. Files must exist and parse.
"""


from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import changeset  # noqa: E402

SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}


def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def collect_named_children(root: Path, folder: str) -> list[Path]:
    found: list[Path] = []
    direct = root / folder
    if direct.is_dir():
        found.extend(p for p in direct.iterdir() if p.is_dir() and not is_skipped_dir(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob(folder):
            if named.is_dir() and named.name == folder and not is_skipped_dir(named):
                found.extend(p for p in named.iterdir() if p.is_dir() and not is_skipped_dir(p))
    return sorted(set(found))


def has_py(dir_path: Path) -> bool:
    return any(p.is_file() for p in dir_path.glob("*.py"))


def load_json(path: Path):
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def noun_schema_ok(data: dict) -> bool:
    verbs = data["verbs"] if isinstance(data.get("verbs"), dict) else data
    if not verbs:
        return False
    skip = {"$schema", "$id", "$defs", "title", "description", "type", "properties"}
    candidates = verbs["properties"] if isinstance(verbs.get("properties"), dict) else verbs
    for key, spec in candidates.items():
        if key in skip or not isinstance(spec, dict):
            continue
        if "input" in spec and "output" in spec:
            return True
        props = spec.get("properties")
        if isinstance(props, dict) and "input" in props and "output" in props:
            return True
    return False


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    violations: list[tuple[str, str]] = []
    changed = changeset.effective_changed(scan_root, ROOT)
    for goal in collect_named_children(scan_root, "goals"):
        if not has_py(goal):
            continue
        if changed is not None and not changeset.unit_touched(goal, changed, scan_root, ROOT):
            continue
        for name, kind in (("input.schema.json", "missing-goal-input"), ("output.schema.json", "missing-goal-output")):
            path = goal / name
            if not path.is_file() or load_json(path) is None:
                violations.append((rel(path), kind))
    for noun in collect_named_children(scan_root, "domain"):
        if not has_py(noun):
            continue
        if changed is not None and not changeset.unit_touched(noun, changed, scan_root, ROOT):
            continue
        schema = noun / "schemas" / "verbs.schema.json"
        data = load_json(schema) if schema.is_file() else None
        if data is None or not noun_schema_ok(data):
            violations.append((rel(schema), "missing-noun-verbs-schema"))
    return violations



def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str]] = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, kind = item
            print(f"VIOLATION {path} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
