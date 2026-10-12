"""Gate-set baseline manifest + owner sidecar (ADR 0051 SG2 under ADR 0052)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
from pathlib import Path

from nouns.gate_set.gate_set import iter_gate_set_relative_paths
from nouns.owner_sidecar.owner_sidecar import content_hash, verify_sidecar_p1

MANIFEST_REL = "integrity/gate-set-baseline.manifest.sha256"


def manifest_lines(root: Path) -> list[str]:
    lines: list[str] = []
    for rel in iter_gate_set_relative_paths(root):
        file_path = root / rel
        if not file_path.is_file():
            continue
        digest = content_hash(file_path.read_bytes())
        lines.append(f"{rel} {digest}")
    return sorted(lines)


def manifest_bytes(root: Path) -> bytes:
    return ("\n".join(manifest_lines(root)) + "\n").encode("utf-8")


def gate_set_manifest_errors(root: Path) -> list[str]:
    """MET when ALL OF: manifest bytes match tree; sidecar passes P1 on manifest."""
    errors: list[str] = []
    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        return [f"missing {MANIFEST_REL}"]
    expected = manifest_bytes(root)
    actual = manifest_path.read_bytes()
    if actual != expected:
        errors.append(f"{MANIFEST_REL}: bytes do not match current gate-set tree")
    errors.extend(verify_sidecar_p1(root, MANIFEST_REL))
    return errors


def path_in_manifest_holds(root: Path, rel_path: str) -> bool:
    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        return False
    rel = rel_path.replace("\\", "/").lstrip("./")
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[0] == rel:
            file_path = root / rel
            if not file_path.is_file():
                return False
            return content_hash(file_path.read_bytes()) == parts[1]
    return False


def gate_paths_manifest_errors(root: Path, gate_paths: list[str]) -> list[str]:
    if not gate_paths:
        return []
    base_errors = gate_set_manifest_errors(root)
    if base_errors:
        return base_errors
    errors: list[str] = []
    for rel in gate_paths:
        if not path_in_manifest_holds(root, rel):
            errors.append(f"{rel}: not covered by ratified gate-set manifest")
    return errors


def manifest_member_digest(root: Path, rel_path: str) -> str | None:
    """SHA-256 recorded in manifest for rel_path, or None if absent."""
    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        return None
    rel = rel_path.replace("\\", "/").lstrip("./")
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[0] == rel:
            return parts[1]
    return None


def fixture_edit_would_break_manifest(root: Path, rel_path: str, tampered: bytes) -> bool:
    """True when tampered bytes would NOT match ratified manifest (NOT_MET if on disk)."""
    recorded = manifest_member_digest(root, rel_path)
    if recorded is None:
        return True
    return content_hash(tampered) != recorded
