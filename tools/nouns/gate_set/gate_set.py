"""ADR 0051 gate-set path enumeration (SSOT for S-GATE-SET-REGISTRY)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

from pathlib import Path


def iter_gate_set_relative_paths(root: Path) -> list[str]:
    """Return sorted repo-relative paths that are gate-set members per ADR 0051."""
    rels: set[str] = set()
    tools = root / "tools"
    nouns = tools / "nouns"
    if nouns.is_dir():
        for prefix in ("fitness_", "assert_"):
            for directory in sorted(nouns.glob(f"{prefix}*")):
                if not directory.is_dir():
                    continue
                for path in directory.rglob("*"):
                    if path.is_file():
                        rels.add(path.relative_to(root).as_posix())
    for path in sorted(tools.glob("fitness-*.py")):
        if path.is_file():
            rels.add(path.relative_to(root).as_posix())
    for path in sorted(tools.glob("assert-*.py")):
        if path.is_file():
            rels.add(path.relative_to(root).as_posix())
    integrity = root / "integrity"
    if integrity.is_dir():
        for path in sorted(integrity.glob("*EXCLUSIONS*")):
            if path.is_file():
                rels.add(path.relative_to(root).as_posix())
        for path in sorted(integrity.glob("*-exclusions*.json")):
            if path.is_file():
                rels.add(path.relative_to(root).as_posix())
    releasable = integrity / "releasable-gates.json"
    if releasable.is_file():
        rels.add(releasable.relative_to(root).as_posix())
    return sorted(rels)


def is_gate_set_path(root: Path, rel_posix: str) -> bool:
    """True when rel_posix is a gate-set member."""
    normalized = rel_posix.replace("\\", "/").lstrip("./")
    return normalized in set(iter_gate_set_relative_paths(root))
