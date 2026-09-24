#!/usr/bin/env python3
"""Operator docs must not duplicate full-nlc-audit manifest stage inventories (ADR 0038)."""

from __future__ import annotations



import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "integrity" / "full-nlc-audit-manifest.json"
DOCS = [
    ROOT / "docs" / "nlc" / "FULL-NLC-AUDIT.md",
]

FORBIDDEN_PHRASES = [
    re.compile(r"quick\s+includes", re.I),
    re.compile(r"full\s+adds", re.I),
]

MANIFEST_POINTER = "integrity/full-nlc-audit-manifest.json"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    stage_ids: list[str] = []
    if MANIFEST.is_file():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        stage_ids = list((data.get("stages") or {}).keys())

    for path in DOCS:
        if not path.is_file():
            violations.append(f"missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT).as_posix()
        if MANIFEST_POINTER not in text:
            violations.append(f"{rel}: must cite {MANIFEST_POINTER}")
        for rx in FORBIDDEN_PHRASES:
            if rx.search(text):
                violations.append(f"{rel}: forbidden inventory phrase ({rx.pattern})")
        if stage_ids:
            hits = [sid for sid in stage_ids if sid in text and sid != "verify"]
            if len(hits) >= 3:
                violations.append(
                    f"{rel}: lists {len(hits)} manifest stage ids (inventory drift); use manifest + --list-stages only"
                )

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

