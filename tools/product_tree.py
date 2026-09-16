"""Product tree vs designed-fail specimen.

A tree with goals/ or domain/ needs CONFIRM.md unless README marks it
as a specimen (first 800 chars: Specimen / Designed red / Known-fail).
"""

from __future__ import annotations

from pathlib import Path

MARKERS = ("specimen", "designed red", "known-fail", "known fail")


def is_specimen(root: Path) -> bool:
    readme = root / "README.md"
    if not readme.is_file():
        return False
    head = readme.read_text(errors="replace")[:800].lower()
    return any(m in head for m in MARKERS)


def requires_confirm(root: Path) -> bool:
    if is_specimen(root):
        return False
    return (root / "goals").is_dir() or (root / "domain").is_dir()
