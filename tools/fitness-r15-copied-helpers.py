#!/usr/bin/env python3
"""R15 v1: the same helper body must not be copied into two goals.

A function of 3+ non-empty, non-comment lines whose normalized body
appears under two different goals/<id>/ dirs fails.

One-liners (a single verb call) are ignored. Logic belongs on the noun.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <fn> copied-helper <goal> <goal>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv", "tests"}
FN = re.compile(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*:\s*$", re.M)
MIN_LINES = 3


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def goal_py(root: Path) -> list[tuple[str, Path]]:
    out: list[tuple[str, Path]] = []
    goals = root / "goals"
    if goals.is_dir():
        for g in goals.iterdir():
            if g.is_dir():
                for p in g.glob("*.py"):
                    if p.is_file():
                        out.append((g.name, p))
    examples = root / "examples"
    if examples.is_dir():
        for named in examples.rglob("goals"):
            if not named.is_dir() or named.name != "goals" or is_skipped(named):
                continue
            for g in named.iterdir():
                if not g.is_dir():
                    continue
                for p in g.glob("*.py"):
                    if p.is_file() and "tests" not in p.parts:
                        out.append((g.name, p))
    return out


def functions(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    found: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        m = re.match(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*:\s*$", lines[i])
        if not m:
            i += 1
            continue
        name = m.group(1)
        body: list[str] = []
        i += 1
        while i < len(lines):
            raw = lines[i]
            if raw.startswith("def ") or raw.startswith("class "):
                break
            if raw.strip() == "" or raw.strip().startswith("#"):
                i += 1
                continue
            if raw.startswith(" ") or raw.startswith("\t"):
                body.append(re.sub(r"\s+", " ", raw.strip()))
                i += 1
                continue
            break
        if len(body) >= MIN_LINES:
            found.append((name, "\n".join(body)))
    return found


def scan_one(scan_root: Path) -> list[tuple[str, str, list[str]]]:
    by_body: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for gid, path in goal_py(scan_root):
        text = path.read_text(errors="replace")
        for name, body in functions(text):
            by_body[body].append((gid, name))
    violations = []
    for body, hits in by_body.items():
        goals = sorted({g for g, _ in hits})
        if len(goals) < 2:
            continue
        names = sorted({n for _, n in hits})
        fn = names[0]
        violations.append((fn, body.split("\n")[0], goals))
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
        for fn, _head, goals in scan_one(scan_root):
            key = (fn, tuple(goals))
            if key in seen:
                continue
            seen.add(key)
            printed.append(key)
            print(f"VIOLATION {fn} copied-helper " + " ".join(goals))
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
