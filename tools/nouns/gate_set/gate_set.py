"""ADR 0051 gate-set path enumeration (SSOT for S-GATE-SET-REGISTRY)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
from pathlib import Path


def _git_tracked_files(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in (proc.stdout or "").splitlines() if line.strip()]


def _is_gate_set_rel(rel: str) -> bool:
    if "/__pycache__/" in rel or rel.endswith(".pyc"):
        return False
    if rel.startswith("tools/nouns/fitness_") or rel.startswith("tools/nouns/assert_"):
        return True
    if rel.startswith("tools/fitness-") and rel.endswith(".py"):
        return True
    if rel.startswith("tools/assert-") and rel.endswith(".py"):
        return True
    name = rel.rsplit("/", 1)[-1]
    if rel.startswith("integrity/") and "EXCLUSIONS" in name:
        return True
    if rel.startswith("integrity/") and name.endswith("-exclusions.json"):
        return True
    if rel == "integrity/releasable-gates.json":
        return True
    return False


def iter_gate_set_relative_paths(root: Path) -> list[str]:
    """Return sorted repo-relative tracked paths that are gate-set members per ADR 0051."""
    rels = [rel for rel in _git_tracked_files(root) if _is_gate_set_rel(rel)]
    return sorted(set(rels))


def is_gate_set_path(root: Path, rel_posix: str) -> bool:
    """True when rel_posix is a gate-set member."""
    normalized = rel_posix.replace("\\", "/").lstrip("./")
    return normalized in set(iter_gate_set_relative_paths(root))
