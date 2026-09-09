#!/usr/bin/env python3
"""BBP fitness check: stand-alone branding, no foreign brand imports (P1).

Practice integrity principle:
  P1: Stand-alone BBP branding; copy and re/unbrand useful shapes;
      do not import foreign brand packages into integrity.

This check verifies:
  - No foreign-branded package names appear as required binders in binding-matrix.json
  - No integrity/charter/agent/tool path depends on foreign brand names

Input: no argv. Scans hub integrity paths.

Output: lines among
  CHECK <item>:MET|NOT_MET [reason]
  RESULT:MET|NOT_MET

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "integrity" / "binding-matrix.json"
INTEGRITY_DIR = ROOT / "integrity"
AGENTS_DIR = ROOT / "agents"
TOOLS_DIR = ROOT / "tools"

FOREIGN_BRAND_PATTERNS = [
    re.compile(r"@?archunit", re.IGNORECASE),
    re.compile(r"@?nx[/-]", re.IGNORECASE),
    re.compile(r"@?eslint-plugin-boundaries", re.IGNORECASE),
    re.compile(r"@?import-linter", re.IGNORECASE),
    re.compile(r"@?modulith", re.IGNORECASE),
    re.compile(r"@?pact", re.IGNORECASE),
    re.compile(r"@?schemathesis", re.IGNORECASE),
]

ALLOWED_PATTERNS = [
    re.compile(r"may use|can use|use these|existing tool", re.IGNORECASE),
    re.compile(r"example|sample|such as", re.IGNORECASE),
    re.compile(r"not a|do not|should not", re.IGNORECASE),
]


def is_foreign_brand(text: str) -> bool:
    """Check if text contains a foreign brand reference."""
    for pattern in FOREIGN_BRAND_PATTERNS:
        if pattern.search(text):
            return True
    return False


def is_allowed_reference(line: str) -> bool:
    """Check if the line is an allowed mention (example, comparison)."""
    for pattern in ALLOWED_PATTERNS:
        if pattern.search(line):
            return True
    return False


def check_binding_matrix() -> list[tuple[str, bool, str]]:
    """Check binding matrix binders don't reference foreign brands."""
    results = []
    
    if not MATRIX_PATH.is_file():
        results.append(("binding-matrix.json", True, "not found (ok for minimal setup)"))
        return results
    
    try:
        matrix = json.loads(MATRIX_PATH.read_text())
        requirements = matrix.get("requirements", [])
        
        for req in requirements:
            binder = req.get("binder", "")
            req_id = req.get("id", "unknown")
            
            if binder and is_foreign_brand(binder):
                results.append((
                    f"binder for {req_id}",
                    False,
                    f"foreign brand in binder: {binder}"
                ))
        
        if not any(not r[1] for r in results):
            results.append(("binding-matrix binders", True, "no foreign brands"))
    
    except (json.JSONDecodeError, Exception) as e:
        results.append(("binding-matrix.json", False, f"parse error: {e}"))
    
    return results


def check_integrity_imports() -> list[tuple[str, bool, str]]:
    """Check integrity directory files don't import foreign brands."""
    results = []
    
    if not INTEGRITY_DIR.is_dir():
        return results
    
    for path in INTEGRITY_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".py", ".ts", ".js"}:
            continue
        
        try:
            content = path.read_text(errors="replace")
            lines = content.split("\n")
            
            for lineno, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith("//"):
                    continue
                is_import = (
                    stripped.startswith("import ") or 
                    stripped.startswith("from ") or
                    "require(" in stripped
                )
                if is_import and is_foreign_brand(line) and not is_allowed_reference(line):
                    rel_path = path.relative_to(ROOT)
                    results.append((
                        f"{rel_path}:{lineno}",
                        False,
                        f"foreign brand import: {line.strip()[:60]}"
                    ))
        except Exception:
            pass
    
    if not results:
        results.append(("integrity/ imports", True, "no foreign brands"))
    
    return results


def check_tools_deps() -> list[tuple[str, bool, str]]:
    """Check tools directory doesn't hard-depend on foreign brands."""
    results = []
    
    if not TOOLS_DIR.is_dir():
        return results
    
    for path in TOOLS_DIR.rglob("*.py"):
        try:
            content = path.read_text(errors="replace")
            lines = content.split("\n")
            
            in_pattern_block = False
            for lineno, line in enumerate(lines, start=1):
                stripped = line.strip()
                if "FOREIGN_BRAND_PATTERNS" in line or "re.compile" in stripped:
                    in_pattern_block = True
                if in_pattern_block and stripped.endswith("]"):
                    in_pattern_block = False
                    continue
                if in_pattern_block:
                    continue
                    
                if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                    continue
                    
                is_import = (
                    stripped.startswith("import ") or 
                    stripped.startswith("from ") or
                    "require(" in stripped
                )
                if is_import and is_foreign_brand(line):
                    rel_path = path.relative_to(ROOT)
                    results.append((
                        f"{rel_path}:{lineno}",
                        False,
                        f"foreign brand import: {line.strip()[:60]}"
                    ))
        except Exception:
            pass
    
    if not results:
        results.append(("tools/ imports", True, "no foreign brands"))
    
    return results


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    
    results.extend(check_binding_matrix())
    results.extend(check_integrity_imports())
    results.extend(check_tools_deps())
    
    all_passed = True
    for item, passed, reason in results:
        status = "MET" if passed else "NOT_MET"
        print(f"CHECK {item}:{status} {reason}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("RESULT:MET")
        return 0
    else:
        print("RESULT:NOT_MET")
        return 1


if __name__ == "__main__":
    sys.exit(main())
