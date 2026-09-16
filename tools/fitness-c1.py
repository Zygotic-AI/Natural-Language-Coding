#!/usr/bin/env python3
"""C1 v2: product trees have a note that states change class A–F.

No note on a product tree (goals/ or domain/, not a specimen) → missing-confirm.
Specimens (README Specimen / Designed red / Known-fail) still skip.

Input: optional argv roots. No args → hub ROOT.
Output: VIOLATION <path> missing-confirm|missing-change-class
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import product_tree  # noqa: E402

NOTES = ("PROPOSAL.md", "CONFIRM.md")
CLASS = re.compile(r"change\s*class\s*[:*\s]*[A-F]\b", re.I)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def note_files(scan_root: Path) -> list[Path]:
    return [scan_root / n for n in NOTES if (scan_root / n).is_file()]


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    notes = note_files(scan_root)
    if not notes:
        if product_tree.requires_confirm(scan_root):
            return [(rel(scan_root / "CONFIRM.md"), "missing-confirm")]
        return []
    missing = []
    for path in notes:
        text = path.read_text(errors="replace")
        if CLASS.search(text) is None:
            missing.append((rel(path), "missing-change-class"))
    return missing


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str]] = set()
    printed: list[tuple[str, str]] = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, kind = item
            print(f"VIOLATION {path} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
