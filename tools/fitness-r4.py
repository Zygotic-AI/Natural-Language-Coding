#!/usr/bin/env python3
"""R4 v1: a public verb on a noun must mention a field or adjective.

Methods other than `__init__` / `_private` whose body never contains a token
from fields.txt or adjectives.txt do not belong on the noun.

No fields.txt and no adjectives.txt → skip (MET).

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> stray-verb <name>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
DEF = re.compile(r"^(\s*)def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*(?:->[^:]*)?:\s*$")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def noun_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        found.extend(p for p in domain.iterdir() if p.is_dir() and not is_skipped(p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("domain"):
            if named.is_dir() and named.name == "domain" and not is_skipped(named):
                found.extend(p for p in named.iterdir() if p.is_dir() and not is_skipped(p))
    return found


def tokens(noun_dir: Path) -> set[str]:
    names: set[str] = set()
    for fname in ("fields.txt", "adjectives.txt"):
        path = noun_dir / fname
        if not path.is_file():
            continue
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split("#", 1)[0].strip()
            if line:
                names.add(line)
    return names


def methods(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    found: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        m = DEF.match(lines[i])
        if not m:
            i += 1
            continue
        indent, name = m.group(1), m.group(2)
        body: list[str] = []
        i += 1
        while i < len(lines):
            raw = lines[i]
            if raw.strip() == "":
                i += 1
                continue
            if raw.startswith(indent + "    ") or raw.startswith(indent + "\t"):
                if not raw.strip().startswith("#"):
                    body.append(raw)
                i += 1
                continue
            break
        found.append((name, "\n".join(body)))
    return found


def uses_token(body: str, names: set[str]) -> bool:
    for token in names:
        if re.search(rf"\b{re.escape(token)}\b", body):
            return True
        if f'"{token}"' in body or f"'{token}'" in body:
            return True
    return False


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    violations = []
    for noun in noun_dirs(scan_root):
        names = tokens(noun)
        if not names:
            continue
        for path in noun.rglob("*.py"):
            if not path.is_file() or is_skipped(path) or "tests" in path.parts:
                continue
            if path.name.startswith("test_"):
                continue
            text = path.read_text(errors="replace")
            for name, body in methods(text):
                if name.startswith("_"):
                    continue
                if not uses_token(body, names):
                    violations.append((rel(path), name))
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
            path, name = item
            print(f"VIOLATION {path} stray-verb {name}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
