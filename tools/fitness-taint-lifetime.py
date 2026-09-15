#!/usr/bin/env python3
"""A5 v1: tainted adjectives do not leave the consuming unit.

A noun lists taint tokens in domain/<noun>/taint.txt (card_number, pan, cvv).
Outside that noun directory, a line is a violation when it:

  return-taint  — a return statement mentions a taint token
  store-taint   — another object's field is assigned a taint token

A consumer may call a getter and use the value locally. V1 does not prove
the value never reaches a gateway — that is later.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path>:<line> <kind>:<token>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_EXTS = {".ts", ".js", ".py", ".mjs", ".cjs", ".tsx", ".jsx"}
SKIP_DIR_NAMES = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}
OUTSIDE_DIR_NAMES = ("goals", "workflows", "adapters")
IDENT = r"[A-Za-z_][A-Za-z0-9_]*"


def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def source_files(tree: Path) -> list[Path]:
    if not tree.is_dir():
        return []
    return sorted(
        p for p in tree.rglob("*")
        if p.is_file() and p.suffix in SOURCE_EXTS and not is_skipped_dir(p)
    )


def noun_dirs(root: Path) -> list[Path]:
    found: list[Path] = []
    domain = root / "domain"
    if domain.is_dir():
        found.extend(sorted(p for p in domain.iterdir() if p.is_dir()))
    examples = root / "examples"
    if examples.is_dir():
        for domain_dir in sorted(examples.rglob("domain")):
            if domain_dir.is_dir() and domain_dir.name == "domain" and not is_skipped_dir(domain_dir):
                found.extend(sorted(p for p in domain_dir.iterdir() if p.is_dir()))
    return found


def outside_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in OUTSIDE_DIR_NAMES:
        files.extend(source_files(root / name))
    examples = root / "examples"
    if examples.is_dir():
        for path in examples.rglob("*"):
            if path.is_dir() and path.name in OUTSIDE_DIR_NAMES and not is_skipped_dir(path):
                files.extend(source_files(path))
    return sorted(set(files))


def load_list(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    names = set()
    for line in path.read_text().splitlines():
        raw = line.strip()
        if raw and not raw.startswith("#"):
            names.add(raw)
    return names


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def is_comment(line: str) -> bool:
    s = line.strip()
    return s.startswith("#") or s.startswith("//")


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    tokens: set[str] = set()
    for noun_dir in noun_dirs(scan_root):
        tokens |= load_list(noun_dir / "taint.txt")
    violations: list[tuple[str, int, str]] = []
    for tok in sorted(tokens):
        if not re.match(rf"^{IDENT}$", tok):
            continue
        word = re.compile(rf"\b{re.escape(tok)}\b")
        ret = re.compile(rf"\breturn\b.*\b{re.escape(tok)}\b")
        store = re.compile(rf"(?:this|{IDENT})\s*\.\s*{IDENT}\s*=(?!=).*\b{re.escape(tok)}\b")
        for path in outside_files(scan_root):
            for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
                if is_comment(line) or not word.search(line):
                    continue
                if ret.search(line):
                    violations.append((rel(path), lineno, f"return-taint:{tok}"))
                if store.search(line):
                    violations.append((rel(path), lineno, f"store-taint:{tok}"))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, int, str]] = set()
    printed = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, lineno, kind = item
            print(f"VIOLATION {path}:{lineno} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
