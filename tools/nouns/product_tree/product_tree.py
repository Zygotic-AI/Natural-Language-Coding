"""Product tree vs designed-fail specimen.

A tree with goals/ or domain/ needs CONFIRM.md unless README marks it
as a specimen (first 800 chars: Specimen / Designed red / Known-fail).
"""

from __future__ import annotations

from pathlib import Path

BOUNDARY = "bba-emit"

MARKERS = ("specimen", "designed red", "known-fail", "known fail")
CONTRACT_OPT_IN = "contract-change applies"


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


def contract_change_applies(root: Path) -> bool:
    """ADR 0006: specimens skip contract fitness unless README opts in."""
    if not (root / "goals").is_dir() and not (root / "domain").is_dir():
        return False
    readme = root / "README.md"
    if not readme.is_file():
        return True
    head = readme.read_text(errors="replace")[:800].lower()
    if is_specimen(root):
        return CONTRACT_OPT_IN in head
    return True
