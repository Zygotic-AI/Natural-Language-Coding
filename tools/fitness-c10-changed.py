#!/usr/bin/env python3
"""C10 diff-scoped (ADR 0006): breaking schema / version≠1 only in CHANGED units.

When CONFIRM CHANGED: (or scoped git dirty) is present, skip schema files
outside touched goal/noun directories. No change list → MET (tree-wide C10 applies).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

import changeset  # noqa: E402


def _load_c10():
    path = Path(__file__).resolve().parent / "fitness-c10.py"
    spec = importlib.util.spec_from_file_location("fitness_c10", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("fitness-c10.py unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c10 = _load_c10()


def unit_for_schema(scan_root: Path, path: Path) -> Path | None:
    try:
        rel = path.resolve().relative_to(scan_root.resolve())
    except ValueError:
        return None
    parts = rel.parts
    if "goals" in parts:
        idx = parts.index("goals")
        if idx + 1 < len(parts):
            return scan_root / "goals" / parts[idx + 1]
    if "domain" in parts:
        idx = parts.index("domain")
        if idx + 1 < len(parts):
            return scan_root / "domain" / parts[idx + 1]
    return None


def scan_one_scoped(scan_root: Path) -> list[tuple[str, str]]:
    try:
        scan_root.resolve().relative_to(ROOT.resolve())
        repo_root = ROOT
    except ValueError:
        repo_root = scan_root
    changed = changeset.effective_changed(scan_root, repo_root)
    if changed is None:
        return []
    violations: list[tuple[str, str]] = []
    adr = c10.has_adr(scan_root)
    for path in c10.schema_files(scan_root):
        unit = unit_for_schema(scan_root, path)
        if unit is not None and not changeset.unit_touched(unit, changed, scan_root, repo_root):
            continue
        try:
            import json

            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict) or "version" not in data:
            continue
        ver = data["version"]
        if not c10.is_one(ver) and not adr:
            violations.append((c10.rel(path), str(ver)))
        prev = c10.previous_schema(path)
        if prev is None:
            continue
        dropped = c10.required_from(prev) - c10.required_from(data)
        if dropped and not adr:
            violations.append((c10.rel(path), "breaking:" + ",".join(sorted(dropped))))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str]] = set()
    printed: list[tuple[str, str]] = []
    for scan_root in scan_roots:
        for item in scan_one_scoped(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, ver = item
            if str(ver).startswith("breaking:"):
                print(f"VIOLATION {path} breaking-no-adr {ver}")
            else:
                print(f"VIOLATION {path} version-bump-no-adr {ver}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
