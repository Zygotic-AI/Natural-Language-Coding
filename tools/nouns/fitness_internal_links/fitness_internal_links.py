#!/usr/bin/env python3
"""Fail on broken relative markdown links in in-force documentation (O6)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.hub_in_force_surfaces.hub_in_force_surfaces import iter_in_force_files  # noqa: E402

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def strip_fences(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def resolve_link(source: Path, target: str) -> Path | None:
    raw = target.strip()
    if not raw or raw.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
        return None
    file_part = raw.split("#", 1)[0].strip()
    if not file_part:
        return None
    if file_part.startswith("/"):
        return ROOT / file_part.lstrip("/")
    return (source.parent / file_part).resolve()


def scan_file(path: Path) -> list[str]:
    text = strip_fences(path.read_text(encoding="utf-8", errors="replace"))
    violations: list[str] = []
    rel = path.relative_to(ROOT)
    for match in LINK_RE.finditer(text):
        resolved = resolve_link(path, match.group(1))
        if resolved is None:
            continue
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            violations.append(f"{rel}: link escapes repo {match.group(1)!r}")
            continue
        if resolved.is_dir():
            continue
        if not resolved.is_file():
            violations.append(f"{rel}: broken link {match.group(1)!r}")
    return violations


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in iter_in_force_files(ROOT, suffixes=(".md", ".mdc")):
        violations.extend(scan_file(path))
    for msg in violations:
        print(f"VIOLATION {msg}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
