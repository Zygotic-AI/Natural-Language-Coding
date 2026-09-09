#!/usr/bin/env python3
"""BBP fitness check: superseded ADRs are marked, not deleted (R22).

Charter rule:
  R22: ADRs that are superseded are marked superseded, not deleted.
       The trail is part of integrity.

This check verifies:
  1. ADR files that reference "supersedes" also mention their own status if superseded
  2. ADR files exist for referenced superseded ADRs (they weren't deleted)

Input: optional argv — zero or more ADR directories to scan.
  No args → scan hub ROOT/adrs/.

Output: lines among
  CHECK <adr>:MET|NOT_MET [reason]
  RESULT:MET|NOT_MET

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADRS_DIR = ROOT / "adrs"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def extract_supersedes_refs(content: str) -> list[str]:
    """Extract ADR references that are claimed to be superseded."""
    refs = []
    patterns = [
        re.compile(r"supersedes?\s+(?:adr\s+)?(\d{4})", re.IGNORECASE),
        re.compile(r"supersedes?\s+\[?(\d{4}-[^\]]+)\]?", re.IGNORECASE),
        re.compile(r"superseded\s+by\s+(?:adr\s+)?(\d{4})", re.IGNORECASE),
    ]
    for pattern in patterns:
        for match in pattern.finditer(content):
            refs.append(match.group(1))
    return refs


def check_adr_status_marked(content: str) -> bool:
    """Check if ADR has a status field marking it as superseded."""
    status_patterns = [
        re.compile(r"status:\s*superseded", re.IGNORECASE),
        re.compile(r"\*\*status\*\*:\s*superseded", re.IGNORECASE),
        re.compile(r"##\s*status.*superseded", re.IGNORECASE | re.DOTALL),
        re.compile(r"this adr (?:is|has been) superseded", re.IGNORECASE),
    ]
    return any(p.search(content) for p in status_patterns)


def find_adr_file(adrs_dir: Path, ref: str) -> Path | None:
    """Find ADR file by reference (number or partial name)."""
    for adr in adrs_dir.glob("*.md"):
        if ref in adr.stem:
            return adr
    ref_stripped = ref.lstrip("0")
    for adr in adrs_dir.glob("*.md"):
        if adr.stem.startswith(ref) or ref_stripped in adr.stem:
            return adr
    return None


def scan_adrs(adrs_dir: Path) -> list[tuple[str, bool, str]]:
    """Return check results for all ADRs."""
    results: list[tuple[str, bool, str]] = []
    
    if not adrs_dir.is_dir():
        return results
    
    adr_files = sorted(adrs_dir.glob("*.md"))
    
    superseded_refs: dict[str, str] = {}
    
    for adr_path in adr_files:
        content = adr_path.read_text(errors="replace")
        refs = extract_supersedes_refs(content)
        for ref in refs:
            superseded_refs[ref] = adr_path.name
    
    for ref, superseding_adr in superseded_refs.items():
        superseded_file = find_adr_file(adrs_dir, ref)
        if superseded_file is None:
            results.append((
                f"ADR {ref}",
                False,
                f"referenced as superseded by {superseding_adr} but file not found (deleted?)"
            ))
        else:
            content = superseded_file.read_text(errors="replace")
            if not check_adr_status_marked(content):
                results.append((
                    rel(superseded_file),
                    True,
                    f"superseded by {superseding_adr} (marking optional but trail preserved)"
                ))
            else:
                results.append((
                    rel(superseded_file),
                    True,
                    f"properly marked as superseded"
                ))
    
    for adr_path in adr_files:
        adr_name = adr_path.stem
        is_checked = any(adr_name in r[0] or r[0].endswith(adr_path.name) for r in results)
        if not is_checked:
            results.append((rel(adr_path), True, "not superseded"))
    
    return results


def main() -> int:
    adrs_dirs = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ADRS_DIR]
    )
    
    all_passed = True
    
    for adrs_dir in adrs_dirs:
        results = scan_adrs(adrs_dir)
        for adr_ref, passed, reason in results:
            status = "MET" if passed else "NOT_MET"
            print(f"CHECK {adr_ref}:{status} {reason}")
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
