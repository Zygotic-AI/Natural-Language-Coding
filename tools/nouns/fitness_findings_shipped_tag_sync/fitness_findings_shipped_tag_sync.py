#!/usr/bin/env python3
"""FINDINGS ship/tag prose must match reachable git tags on HEAD (F1)."""

from __future__ import annotations



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"

TAGGED_ON_ORIGIN = re.compile(
    r"v(\d+\.\d+\.\d+)\s+is\s+tagged\s+on\s+origin|tagged\s+on\s+origin.*v(\d+\.\d+\.\d+)",
    re.I,
)
VERSION_TAG = re.compile(r"\bv(\d+\.\d+\.\d+)\b")


def main() -> int:
    _ = sys.argv[1:]
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_release_tags import last_shipped_tag, tag_version  # noqa: E402

    if not FINDINGS.is_file():
        print("VIOLATION missing FINDINGS.md")
        print("RESULT:NOT_MET")
        return 1

    text = FINDINGS.read_text(encoding="utf-8", errors="replace")
    shipped = last_shipped_tag("HEAD")
    shipped_ver = tag_version(shipped) if shipped else None

    violations: list[str] = []
    for m in TAGGED_ON_ORIGIN.finditer(text):
        claimed = m.group(1) or m.group(2)
        if shipped_ver is None:
            violations.append(
                f"FINDINGS claims v{claimed} tagged on origin but no reachable v*.*.* tag on HEAD"
            )
        elif claimed != shipped_ver:
            violations.append(
                f"FINDINGS claims v{claimed} on origin but newest reachable tag is v{shipped_ver}"
            )

    if shipped_ver is None and re.search(r"tagged\s+on\s+origin", text, re.I):
        if TAGGED_ON_ORIGIN.search(text):
            pass  # already caught
        else:
            violations.append("FINDINGS mentions tagged on origin without matching reachable tag")

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

