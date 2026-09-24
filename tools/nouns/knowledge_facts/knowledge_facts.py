"""UC18: validate knowledge/facts.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOUNDARY = "bba-emit"

ID_RE = re.compile(r"^KF-[a-z0-9][a-z0-9-]*$", re.I)
STATUSES = frozenset({"proposed", "confirmed", "superseded"})


def validate_facts_file(path: Path) -> tuple[bool, list[str], int]:
    if not path.is_file():
        return False, ["missing knowledge/facts.json"], 0
    data = json.loads(path.read_text(errors="replace"))
    facts = data.get("facts")
    if not isinstance(facts, list):
        return False, ["facts must be a list"], 0
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
    return len(defects) == 0, defects, len(facts)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[0]).resolve() if args else Path.cwd()
    path = root / "knowledge" / "facts.json"
    ok, defects, count = validate_facts_file(path)
    if not ok:
        sys.stdout.write("FACTS:NOT_MET\n")
        for d in defects:
            sys.stdout.write(d + "\n")
        return 1
    sys.stdout.write("FACTS:MET\n")
    sys.stdout.write(f"facts: {count}\n")
    return 0
