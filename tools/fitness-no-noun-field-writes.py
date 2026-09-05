#!/usr/bin/env python3
"""Fitness check 1: no noun field writes from outside the noun (charter §12.1).

Noun modules: domain/<noun>/ and examples/**/domain/<noun>/.
Outside trees: goals/, workflows/, adapters/ (repo root and examples/**/).

Declared fields: domain/<noun>/fields.txt (one name per line), or inferred from
this.<id> = and <obj>.<id> = in that noun's *.ts / *.js / *.py.

Input: optional argv — zero or more adopter-shaped roots to scan.
  No args → scan hub ROOT (domain/, goals/, workflows/, adapters/, and examples/**).
  With args → each path is scanned as its own tree (that path's domain/ + goals/…).

Output: zero or more `VIOLATION <path>:<line> <field>` lines, then
  `RESULT:MET` or `RESULT:NOT_MET`.

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_EXTS = {".ts", ".js", ".py", ".mjs", ".cjs", ".tsx", ".jsx"}
SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "dist",
    "__pycache__",
    ".venv",
    "venv",
}
OUTSIDE_DIR_NAMES = ("goals", "workflows", "adapters")
IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
THIS_OR_OBJ_ASSIGN = re.compile(
    rf"(?:this|{IDENT})\s*\.\s*({IDENT})\s*=(?!=)"
)
IDENT_RE = re.compile(rf"^{IDENT}$")


def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def source_files(tree: Path) -> list[Path]:
    if not tree.is_dir():
        return []
    out = []
    for path in tree.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in SOURCE_EXTS:
            continue
        if is_skipped_dir(path):
            continue
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
            if not domain_dir.is_dir() or domain_dir.name != "domain":
                continue
            if is_skipped_dir(domain_dir):
                continue
            found.extend(sorted(p for p in domain_dir.iterdir() if p.is_dir()))
    return found


def outside_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in OUTSIDE_DIR_NAMES:
        files.extend(source_files(root / name))
    examples = root / "examples"
    if examples.is_dir():
        for path in examples.rglob("*"):
            if not path.is_dir() or path.name not in OUTSIDE_DIR_NAMES:
                continue
            if is_skipped_dir(path):
                continue
            files.extend(source_files(path))
    # unique, stable
    return sorted(set(files))


def load_fields(noun_dir: Path) -> set[str]:
    fields_txt = noun_dir / "fields.txt"
    if fields_txt.is_file():
        names = set()
        for line in fields_txt.read_text().splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#"):
                continue
            names.add(raw)
        return names
    names = set()
    for path in source_files(noun_dir):
        for line in path.read_text(errors="replace").splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            for match in THIS_OR_OBJ_ASSIGN.finditer(line):
                names.add(match.group(1))
    return names


def assignment_patterns(fields: set[str]) -> list[tuple[str, re.Pattern[str]]]:
    patterns = []
    for field in sorted(fields):
        if not IDENT_RE.match(field):
            escaped = re.escape(field)
        else:
            escaped = re.escape(field)
        dot = re.compile(
            rf"(?:this|{IDENT})\s*\.\s*{escaped}\s*=(?!=)"
        )
        bracket = re.compile(
            rf"\[\s*['\"]{escaped}['\"]\s*\]\s*=(?!=)"
        )
        patterns.append((field, dot))
        patterns.append((field, bracket))
    return patterns


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    """Return VIOLATION tuples for one adopter-shaped or example root."""
    nouns = noun_dirs(scan_root)
    # When scan_root is itself an example (…/domain exists here), also treat
    # scan_root as the project root for outside trees.
    field_to_nouns: dict[str, set[str]] = {}
    for noun_dir in nouns:
        for name in load_fields(noun_dir):
            field_to_nouns.setdefault(name, set()).add(rel(noun_dir))
    # Leaf example roots: domain/ is direct child; noun_dirs already found them.
    # If scan_root has domain/ as child, outside_files(scan_root) covers goals/.
    fields = set(field_to_nouns)
    patterns = assignment_patterns(fields)
    violations: list[tuple[str, int, str]] = []
    for path in outside_files(scan_root):
        text = path.read_text(errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            for field, pattern in patterns:
                if pattern.search(line):
                    violations.append((rel(path), lineno, field))
    return violations


def main() -> int:
    # Optional positional roots: each is scanned as an adopter-shaped tree.
    # No args → whole hub ROOT (includes known-fail fixture under examples/).
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    violations: list[tuple[str, int, str]] = []
    for scan_root in scan_roots:
        violations.extend(scan_one(scan_root))
    # stable unique
    seen = set()
    printed = []
    for item in violations:
        if item in seen:
            continue
        seen.add(item)
        printed.append(item)
        path, lineno, field = item
        print(f"VIOLATION {path}:{lineno} {field}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
