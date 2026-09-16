#!/usr/bin/env python3
"""C15 v1: a retrying goal must call verbs marked idempotent.

If a goal .py contains retry/temporalio/durable/`for attempt in`, each
`obj.verb(` call must have `"idempotent": true` on that verb in some
domain/*/schemas/verbs.schema.json.

No retry marker → skip (MET).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <goal> missing-idempotent <verb>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
RETRY = re.compile(r"\b(retry|temporalio|durable)\b|for\s+attempt\s+in", re.I)
CALL = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\.([A-Za-z_][A-Za-z0-9_]*)\s*\(")
SKIP_VERBS = {"print", "append", "get", "set", "update"}


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def collect(root: Path, name: str) -> list[Path]:
    found: list[Path] = []
    direct = root / name
    if direct.is_dir():
        found.append(direct)
    examples = root / "examples"
    if examples.is_dir():
        for p in examples.rglob(name):
            if p.is_dir() and p.name == name and not is_skipped(p):
                found.append(p)
    return found


def idempotent_verbs(root: Path) -> set[str]:
    names: set[str] = set()
    for domain in collect(root, "domain"):
        for schema in domain.rglob("verbs.schema.json"):
            try:
                data = json.loads(schema.read_text())
            except (OSError, json.JSONDecodeError):
                continue
            verbs = data.get("verbs") if isinstance(data, dict) else None
            if not isinstance(verbs, dict):
                continue
            for key, spec in verbs.items():
                if isinstance(spec, dict) and spec.get("idempotent") is True:
                    names.add(str(key))
    return names


def goal_py(root: Path) -> list[Path]:
    files: list[Path] = []
    for goals in collect(root, "goals"):
        files.extend(
            p for p in goals.rglob("*.py")
            if p.is_file() and not is_skipped(p) and "tests" not in p.parts
        )
    return files


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    marked = idempotent_verbs(scan_root)
    violations = []
    for path in goal_py(scan_root):
        text = path.read_text(errors="replace")
        body = "\n".join(
            ln for ln in text.splitlines() if not ln.strip().startswith("#")
        )
        if RETRY.search(body) is None:
            continue
        for match in CALL.finditer(body):
            verb = match.group(1)
            if verb in SKIP_VERBS:
                continue
            if verb not in marked:
                violations.append((rel(path), verb))
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
            path, verb = item
            print(f"VIOLATION {path} missing-idempotent {verb}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
