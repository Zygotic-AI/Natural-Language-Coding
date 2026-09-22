#!/usr/bin/env python3
"""C10: a breaking schema change needs an ADR, even at version 1.

Version other than 1 / "1" requires adrs/*.md.
Dropped required fields vs verbs.previous.json (or input.previous.json)
also require an ADR — that is breaking, not "version ≠ 1".
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



def required_from(data: dict) -> set[str]:
    names: set[str] = set()
    if isinstance(data.get("required"), list):
        names.update(str(x) for x in data["required"])
    verbs = data.get("verbs")
    if isinstance(verbs, dict):
        for spec in verbs.values():
            if not isinstance(spec, dict):
                continue
            inp = spec.get("input")
            if isinstance(inp, dict) and isinstance(inp.get("required"), list):
                names.update(str(x) for x in inp["required"])
    return names


def previous_schema(path: Path) -> dict | None:
    prev = path.with_name(path.name.replace(".schema.json", ".previous.json"))
    if not prev.is_file():
        # verbs.schema.json -> verbs.previous.json
        prev = path.with_name(path.stem.replace(".schema", "") + ".previous.json")
    if not prev.is_file():
        return None
    try:
        data = json.loads(prev.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def breaking_contract_events(scan_root: Path) -> list[tuple[str, str]]:
    """Published-contract breaks (ADR 0006), regardless of whether an ADR file exists."""
    events: list[tuple[str, str]] = []
    for path in schema_files(scan_root):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict) or "version" not in data:
            continue
        ver = data["version"]
        prev = previous_schema(path)
        if prev is not None:
            dropped = required_from(prev) - required_from(data)
            if dropped:
                events.append((rel(path), "breaking:" + ",".join(sorted(dropped))))
        if not is_one(ver):
            events.append((rel(path), f"version:{ver}"))
    return events


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
        if not is_one(ver) and not adr:
            violations.append((rel(path), str(ver)))
        prev = previous_schema(path)
        if prev is None:
            continue
        dropped = required_from(prev) - required_from(data)
        if dropped and not adr:
            violations.append((rel(path), "breaking:" + ",".join(sorted(dropped))))
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
            print(f"VIOLATION {path} version-bump-no-adr {ver}" if not str(ver).startswith("breaking:") else f"VIOLATION {path} breaking-no-adr {ver}")

    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
