#!/usr/bin/env python3
"""UC18: validate knowledge/facts.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^KF-[a-z0-9][a-z0-9-]*$", re.I)
STATUSES = frozenset({"proposed", "confirmed", "superseded"})


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    path = root / "knowledge" / "facts.json"
    if not path.is_file():
        sys.stdout.write("FACTS:NOT_MET\nmissing knowledge/facts.json\n")
        return 1

    data = json.loads(path.read_text(errors="replace"))
    facts = data.get("facts")
    if not isinstance(facts, list):
        sys.stdout.write("FACTS:NOT_MET\nfacts must be a list\n")
        return 1

    seen: set[str] = set()
    defects: list[str] = []
    for i, fact in enumerate(facts):
        if not isinstance(fact, dict):
            defects.append(f"facts[{i}]: not an object")
            continue
        fid = fact.get("id")
        if not fid or not ID_RE.match(str(fid)):
            defects.append(f"facts[{i}]: bad id")
        elif fid in seen:
            defects.append(f"duplicate id {fid}")
        else:
            seen.add(str(fid))
        if not fact.get("scope"):
            defects.append(f"{fid}: missing scope")
        if not fact.get("statement"):
            defects.append(f"{fid}: missing statement")
        st = fact.get("status")
        if st not in STATUSES:
            defects.append(f"{fid}: bad status")
        if st == "superseded" and not fact.get("superseded_by"):
            defects.append(f"{fid}: superseded without superseded_by")

    if defects:
        sys.stdout.write("FACTS:NOT_MET\n")
        for d in defects:
            sys.stdout.write(d + "\n")
        return 1

    sys.stdout.write("FACTS:MET\n")
    sys.stdout.write(f"facts: {len(facts)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
