#!/usr/bin/env python3
"""BBP fitness check: goal modules must not import other goals' internals (C12, R14).

Charter rules:
  C12: No goal imports another goal's internals.
  R14: Goal internals are not callable from other goals.

Input: optional argv — zero or more adopter-shaped roots to scan.
  No args → scan hub ROOT (goals/ + examples/**/).
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


def goal_dirs(root: Path) -> list[Path]:
    """Find all goal directories (goals/<goal>/)."""
    found: list[Path] = []
    goals = root / "goals"
    if goals.is_dir():
        found.extend(sorted(p for p in goals.iterdir() if p.is_dir()))
    examples = root / "examples"
    if examples.is_dir():
        for goals_dir in sorted(examples.rglob("goals")):
            if not goals_dir.is_dir() or goals_dir.name != "goals":
                continue
            if is_skipped_dir(goals_dir):
                continue
            found.extend(sorted(p for p in goals_dir.iterdir() if p.is_dir()))
    return found


def extract_imports(content: str) -> list[tuple[int, str]]:
    """Extract import statements with line numbers."""
    imports = []
    lines = content.split("\n")
    for lineno, line in enumerate(lines, start=1):
        for pattern in IMPORT_PATTERNS:
            for match in pattern.finditer(line):
                imports.append((lineno, match.group(1)))
    return imports


def is_goal_internal_import(import_path: str, current_goal: str) -> bool:
    """Check if import references another goal's internals."""
    import_lower = import_path.lower()
    
    if "/goals/" not in import_lower and "goals/" not in import_lower:
        if not import_lower.startswith("goals"):
            return False
    
    goal_match = re.search(r"goals?[/\\]([^/\\]+)", import_path, re.IGNORECASE)
    if not goal_match:
        return False
    
    imported_goal = goal_match.group(1).lower()
    
    if imported_goal == current_goal.lower():
        return False
    
    has_internals = (
        "/implementation/" in import_path.lower() or
        "/internal/" in import_path.lower() or
        "/lib/" in import_path.lower() or
        "/_" in import_path
    )
    
    is_public_contract = (
        "contract" in import_path.lower() or
        import_path.endswith("/index") or
        import_path.endswith("/goal")
    )
    
    if is_public_contract:
        return False
    
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_one(scan_root: Path) -> list[tuple[str, int, str]]:
    """Return VIOLATION tuples for one adopter-shaped root."""
    violations: list[tuple[str, int, str]] = []
    
    for goal_dir in goal_dirs(scan_root):
        current_goal = goal_dir.name
        
        for path in source_files(goal_dir):
            content = path.read_text(errors="replace")
            imports = extract_imports(content)
            
            for lineno, import_path in imports:
                if is_goal_internal_import(import_path, current_goal):
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
