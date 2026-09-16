#!/usr/bin/env python3
"""C24 v2: classes A/B/D/E/F record ratification; product trees need a note.

No note on a product tree → missing-confirm. Specimens skip.
Class C with a note → skip ratification.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import product_tree  # noqa: E402

NOTES = ("PROPOSAL.md", "CONFIRM.md")
CLASS = re.compile(r"change\s*class\s*[:*\s]*([ABDEF])\b", re.I)
RATIFY = re.compile(r"\bratify|\bratification\b", re.I)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    notes = [scan_root / n for n in NOTES if (scan_root / n).is_file()]
    if not notes:
        if product_tree.requires_confirm(scan_root):
            return [(rel(scan_root / "CONFIRM.md"), "missing-confirm")]
        return []
    missing = []
    for path in notes:
        text = path.read_text(errors="replace")
        if CLASS.search(text) is None:
            continue
        if RATIFY.search(text) is None:
            missing.append((rel(path), "missing-ratification"))
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
