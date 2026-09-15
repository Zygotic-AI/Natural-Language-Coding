#!/usr/bin/env python3
"""R24 v1: named adjectives and field math stay under domain/<noun>/.

Not R5. R5 is assignment (invoice.status =). This tool fails a goal that
*reimplements* the adjective: compares a status token, or does money math
on a declared field, then maybe even calls the verb.

Declaration:
  domain/<noun>/adjectives.txt  — one token per line (paid, void, …)
  domain/<noun>/fields.txt      — field names; used for math/compare on
                                  those fields outside the noun

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path>:<line> <kind>:<token>
        RESULT:MET|NOT_MET
Failure mode: exit 0 = MET; exit 1 = NOT_MET. No silent swallow.
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
    out = []
    for path in tree.rglob("*"):
        if path.is_file() and path.suffix in SOURCE_EXTS and not is_skipped_dir(path):
            out.append(path)
    return sorted(out)


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
        if not raw or raw.startswith("#"):
            continue
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
    fields: set[str] = set()
    for noun_dir in noun_dirs(scan_root):
        tokens |= load_list(noun_dir / "adjectives.txt")
        fields |= load_list(noun_dir / "fields.txt")
    violations: list[tuple[str, int, str]] = []
    token_pats = [
        (tok, re.compile(rf"['\"]{re.escape(tok)}['\"]"))
        for tok in sorted(tokens)
        if tok
    ]
    field_pats = []
    for field in sorted(fields):
        if not re.match(rf"^{IDENT}$", field):
            continue
        field_pats.append(
            (
                field,
                re.compile(
                    rf"\.\s*{re.escape(field)}\s*(?:[+\-*/]=|[+\-*/]|==|!=|<=|>=|<|>)"
                ),
            )
        )
    for path in outside_files(scan_root):
        for lineno, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            if is_comment(line):
                continue
            for tok, pat in token_pats:
                if pat.search(line):
                    violations.append((rel(path), lineno, f"token:{tok}"))
            for field, pat in field_pats:
                if pat.search(line):
                    violations.append((rel(path), lineno, f"field-math:{field}"))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    printed = []
    seen: set[tuple[str, int, str]] = set()
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
