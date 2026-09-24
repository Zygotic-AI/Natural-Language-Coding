#!/usr/bin/env python3
"""ADR 0038 v1: operator SSOT must not rely on 'remember' without a linked gate or TODO."""

from __future__ import annotations



import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

SCAN_ROOTS = [
    ROOT / ".agents" / "skills",
    ROOT / "docs" / "adoption",
    ROOT / "AGENTS.md",
]

VIOLATION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bremember\s+to\b", re.I), "remember to"),
    (re.compile(r"\bremember\s+that\b", re.I), "remember that"),
    (re.compile(r"\byou must remember\b", re.I), "you must remember"),
    (re.compile(r"\bdon'?t forget\b", re.I), "don't forget"),
    (re.compile(r"\bkeep in mind\b", re.I), "keep in mind"),
]

ALLOW_LINE = re.compile(
    r"memory is not|do not remember|must not remember|never remember|"
    r"not what the reader must keep in mind|does not [\"']?remember|"
    r"ADR 0038|encode the rule in a|machine gate|hub-release-record|"
    r"fitness-adr|nlc_release|\./release|`\./release`|linked gate|TODO",
    re.I,
)


def iter_scan_files() -> list[Path]:
    paths: list[Path] = []
    for entry in SCAN_ROOTS:
        if entry.is_file():
            paths.append(entry)
            continue
        if not entry.is_dir():
            continue
        for path in sorted(entry.rglob("*.md")):
            if path.name.startswith("."):
                continue
            paths.append(path)
    return paths


def scan_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    hits: list[str] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if ALLOW_LINE.search(line):
            continue
        for rx, label in VIOLATION_PATTERNS:
            if rx.search(line):
                snippet = line.strip()[:120]
                hits.append(f"{rel}:{lineno}: {label} — {snippet}")
                break
    return hits


def main() -> int:
    _ = sys.argv[1:]
    failures: list[str] = []
    for path in iter_scan_files():
        failures.extend(scan_file(path))
    if failures:
        print("FAIL fitness-adr-0038-no-memory")
        for f in failures:
            print(f"  {f}")
        print("  Fix: encode in a gate/tool or open a TODO row (ADR 0038).")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

