#!/usr/bin/env python3
"""Refresh hub-x4-remainder.json classes, counts, and noun_pilots from disk."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"

IMPORT_RE = re.compile(r"from\s+nouns\.([a-zA-Z0-9_]+)\s+import")


def adapter_imports_noun(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    m = IMPORT_RE.search(text)
    if m and len(text) < 2500:
        return m.group(1)
    return None


def classify_entry(filename: str, prev: str) -> str:
    path = TOOLS / filename
    if not path.is_file():
        return prev
    if filename.startswith("assert-"):
        slug = adapter_imports_noun(path)
        return "noun-backed-assert" if slug else "assert-only"
    if filename.startswith("fitness-"):
        slug = adapter_imports_noun(path)
        return "noun-backed-fitness" if slug else "fitness-only"
    if adapter_imports_noun(path):
        return "noun-backed-lib"
    if prev:
        return prev
    return "tool-only"


def rebuild_pilots() -> list[dict]:
    by_noun: dict[str, dict] = {}
    for path in sorted(TOOLS.glob("*.py")):
        slug = adapter_imports_noun(path)
        if not slug:
            continue
        noun_dir = TOOLS / "nouns" / slug
        if not noun_dir.is_dir():
            continue
        row = by_noun.setdefault(
            slug,
            {
                "noun": slug,
                "path": f"tools/nouns/{slug}/",
                "adapters": [],
                "fitness": "tools/fitness-hub-x4-noun-pilot.py",
            },
        )
        row["adapters"].append(path.name)
    for row in by_noun.values():
        row["adapters"] = sorted(set(row["adapters"]))
    return sorted(by_noun.values(), key=lambda r: r["noun"])


def main() -> int:
    _ = sys.argv[1:]
    if not REMAINDER.is_file():
        print("VIOLATION missing hub-x4-remainder.json")
        return 1
    data = json.loads(REMAINDER.read_text(encoding="utf-8"))
    entries = data.get("entries") or []
    by_file = {e.get("file"): e for e in entries if e.get("file")}
    for path in sorted(TOOLS.glob("fitness-*.py")):
        by_file.setdefault(path.name, {"file": path.name, "class": "fitness-only"})
    for path in sorted(TOOLS.glob("assert-*.py")):
        by_file.setdefault(path.name, {"file": path.name, "class": "assert-only"})
    entries = [by_file[k] for k in sorted(by_file)]
    for e in entries:
        fn = e.get("file") or ""
        e["class"] = classify_entry(fn, e.get("class") or "")

    counts = {
        "assert_only": 0,
        "emit_path_open": 0,
        "other_or_lib": 0,
        "noun_backed_lib": 0,
        "noun_backed_assert": 0,
        "noun_backed_fitness": 0,
        "fitness_only": 0,
        "covered_emit_path": data.get("counts", {}).get("covered_emit_path", 26),
    }
    for e in entries:
        c = e.get("class") or ""
        if c == "assert-only":
            counts["assert_only"] += 1
        elif c == "fitness-only":
            counts["fitness_only"] += 1
        elif c == "noun-backed-assert":
            counts["noun_backed_assert"] += 1
        elif c == "noun-backed-fitness":
            counts["noun_backed_fitness"] += 1
        elif c == "noun-backed-lib":
            counts["noun_backed_lib"] += 1

    data["entries"] = entries
    data["counts"] = counts
    data["assert_only_count"] = counts["assert_only"]
    data["fitness_only_count"] = counts["fitness_only"]
    data["noun_pilots"] = rebuild_pilots()
    if counts["fitness_only"] == 0 and counts["assert_only"] == 0:
        data["fitness_tranche_complete"] = True
        data["note"] = (
            "X4: emit-path + lib + assert + fitness hub tools noun-backed via thin adapters."
        )
    data["schema"] = data.get("schema") or 1
    REMAINDER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        f"REFRESH:MET fitness_only={counts['fitness_only']} "
        f"noun_backed_fitness={counts['noun_backed_fitness']} pilots={len(data['noun_pilots'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
