#!/usr/bin/env python3
"""C21 diff-scoped (ADR 0006): impact callers only for CHANGED goal units.


When CONFIRM CHANGED: (or scoped git dirty) is present, skip goals outside
touched goal directories. No change list → MET (tree-wide C21 applies).
"""






from __future__ import annotations

BOUNDARY = "bba-emit"



import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import changeset  # noqa: E402
import product_tree  # noqa: E402


def _load_c21():
    path = ROOT / "tools" / "fitness-c21.py"
    spec = importlib.util.spec_from_file_location("fitness_c21", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("fitness-c21.py unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c21 = _load_c21()


def goal_dir(scan_root: Path, goal_id: str) -> Path:
    return scan_root / "goals" / goal_id


def scan_one_scoped(scan_root: Path) -> list[tuple[str, str, str]]:
    try:
        scan_root.resolve().relative_to(ROOT.resolve())
        repo_root = ROOT
    except ValueError:
        repo_root = scan_root
    changed = changeset.effective_changed(scan_root, repo_root)
    if changed is None:
        return []

    notes = c21.note_files(scan_root)
    if not notes:
        if product_tree.requires_confirm(scan_root):
            return [(c21.rel_note(scan_root / "CONFIRM.md"), "-", "missing-confirm")]
        return []

    text = "\n".join(p.read_text(errors="replace") for p in notes).casefold()
    graph = c21.load_graph().build(scan_root)
    violations: list[tuple[str, str, str]] = []
    for gid, body in graph.get("goals", {}).items():
        unit = goal_dir(scan_root, gid)
        if unit.is_dir() and not changeset.unit_touched(unit, changed, scan_root, repo_root):
            continue
        for call in body.get("calls", []):
            if call.casefold() not in text:
                note = notes[0]
                rel = (
                    str(note.relative_to(ROOT))
                    if note.is_relative_to(ROOT)
                    else str(note)
                )
                violations.append((rel, gid, call))
    return violations


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str, str]] = set()
    printed: list[tuple[str, str, str]] = []
    for scan_root in scan_roots:
        for item in scan_one_scoped(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, gid, call = item
            if call == "missing-confirm":
                print(f"VIOLATION {path} missing-confirm")
            else:
                print(f"VIOLATION {path} missing-caller {gid} {call}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
