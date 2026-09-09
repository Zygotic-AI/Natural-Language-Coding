#!/usr/bin/env python3
"""BBP fitness check: noun modules must not import goal/workflow modules (C6, R7).

Charter rules:
  C6: No noun module imports a goal or workflow module.
  R7: Nouns never call goals. Nouns never call workflows.

Input: optional argv — zero or more adopter-shaped roots to scan.
  No args → scan hub ROOT (domain/ + examples/**/).
  With args → each path is scanned as its own tree.

Output: zero or more `VIOLATION <path>:<line> imports <module>` lines, then
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

IMPORT_PATTERNS = [
    re.compile(r"^\s*import\s+.*?from\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
    re.compile(r"^\s*import\s+['\"]([^'\"]+)['\"]", re.MULTILINE),
    re.compile(r"^\s*from\s+([^\s]+)\s+import", re.MULTILINE),
    re.compile(r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", re.MULTILINE),
]

FORBIDDEN_PATTERNS = [
    re.compile(r"goals?[/\\]", re.IGNORECASE),
    re.compile(r"workflows?[/\\]", re.IGNORECASE),
    re.compile(r"[/\\]goals?[/\\]", re.IGNORECASE),
    re.compile(r"[/\\]workflows?[/\\]", re.IGNORECASE),
    re.compile(r"^goals?\.", re.IGNORECASE),
    re.compile(r"^workflows?\.", re.IGNORECASE),
]


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
    """Find all noun directories (domain/<noun>/)."""
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


def noun_files(root: Path) -> list[Path]:
    """Get all source files inside noun directories."""
    files: list[Path] = []
    for noun_dir in noun_dirs(root):
        files.extend(source_files(noun_dir))
    return sorted(set(files))


def is_forbidden_import(import_path: str) -> bool:
    """Check if an import path references goals or workflows."""
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(import_path):
            return True
    return False


def extract_imports(content: str) -> list[tuple[int, str]]:
    """Extract import statements with line numbers."""
    imports = []
    lines = content.split("\n")
    for lineno, line in enumerate(lines, start=1):
        for pattern in IMPORT_PATTERNS:
            for match in pattern.finditer(line):
                imports.append((lineno, match.group(1)))
    return imports


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    """Return VIOLATION tuples for one adopter-shaped root."""
    violations: list[tuple[str, int, str]] = []
    
    for path in noun_files(scan_root):
        content = path.read_text(errors="replace")
        imports = extract_imports(content)
        
        for lineno, import_path in imports:
            if is_forbidden_import(import_path):
                violations.append((rel(path), lineno, import_path))
    
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    
    violations: list[tuple[str, int, str]] = []
    for scan_root in scan_roots:
        violations.extend(scan_one(scan_root))
    
    seen = set()
    printed = []
    for item in violations:
        if item in seen:
            continue
        seen.add(item)
        printed.append(item)
        path, lineno, import_path = item
        print(f"VIOLATION {path}:{lineno} imports {import_path}")
    
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
