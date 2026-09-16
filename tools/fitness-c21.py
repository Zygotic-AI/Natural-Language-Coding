#!/usr/bin/env python3
"""C21 v1: if a proposal/confirm note exists, it must name generated callers.

Looks for PROPOSAL.md or CONFIRM.md under the scan root.
Callers come from generate-impact-graph.build (not a hand JSON).
No proposal file → skip (MET). That is not "the change had no impact."

Input: optional argv roots. No args → hub ROOT (will skip; hub has no single proposal).
Output: VIOLATION <path> missing-caller <goal> <call>
Failure mode: exit 0 = MET; exit 1 = NOT_MET.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "tools" / "generate-impact-graph.py"
NOTES = ("PROPOSAL.md", "CONFIRM.md")


def load_graph():
    spec = importlib.util.spec_from_file_location("gen_impact", GRAPH)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generate-impact-graph.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def note_files(scan_root: Path) -> list[Path]:
    found = []
    for name in NOTES:
        p = scan_root / name
        if p.is_file():
            found.append(p)
    return found


def scan_one(scan_root: Path) -> list[tuple[str, str, str]]:
    notes = note_files(scan_root)
    if not notes:
        return []
    text = "\n".join(p.read_text(errors="replace") for p in notes).casefold()
    graph = load_graph().build(scan_root)
    violations = []
    for gid, body in graph.get("goals", {}).items():
        for call in body.get("calls", []):
            if call.casefold() not in text:
                violations.append((str(notes[0].relative_to(ROOT) if notes[0].is_relative_to(ROOT) else notes[0]), gid, call))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    printed = []
    seen = set()
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, gid, call = item
            print(f"VIOLATION {path} missing-caller {gid} {call}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
