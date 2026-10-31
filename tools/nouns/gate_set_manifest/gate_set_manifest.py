"""Gate-set baseline manifest + owner sidecar (ADR 0051 SG2 under ADR 0052)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import os
from pathlib import Path

from nouns.gate_set.gate_set import derive_gate_set_paths, iter_gate_set_relative_paths
from nouns.owner_sidecar.owner_sidecar import content_hash

MANIFEST_REL = "integrity/gate-set-baseline.manifest.sha256"


def _file_bytes(root: Path, rel: str, overrides: dict[str, bytes] | None) -> bytes | None:
    if overrides is not None and rel in overrides:
        return overrides[rel]
    file_path = root / rel
    if file_path.is_symlink():
        return os.readlink(file_path).encode("utf-8")
    if file_path.is_file():
        return file_path.read_bytes()
    return None


def _other_manifest_lines(root: Path, *, overrides: dict[str, bytes] | None) -> list[str]:
    lines: list[str] = []
    for rel in iter_gate_set_relative_paths(root):
        if rel == MANIFEST_REL:
            continue
        body = _file_bytes(root, rel, overrides)
        if body is None:
            continue
        lines.append(f"{rel} {content_hash(body)}")
    return sorted(lines)


def manifest_lines(root: Path, *, overrides: dict[str, bytes] | None = None) -> list[str]:
    rels = set(iter_gate_set_relative_paths(root))
    other = _other_manifest_lines(root, overrides=overrides)
    if MANIFEST_REL not in rels:
        return other
    # Self line digests all other member lines (not the manifest file bytes on disk).
    without_self = ("\n".join(other) + "\n").encode("utf-8")
    self_digest = content_hash(without_self)
    return sorted(other + [f"{MANIFEST_REL} {self_digest}"])


def manifest_bytes(root: Path, *, overrides: dict[str, bytes] | None = None) -> bytes:
    return ("\n".join(manifest_lines(root, overrides=overrides)) + "\n").encode("utf-8")


def _manifest_path_set(manifest_bytes_on_disk: bytes) -> set[str]:
    paths: set[str] = set()
    for line in manifest_bytes_on_disk.decode("utf-8", errors="replace").splitlines():
        parts = line.strip().split()
        if len(parts) == 2:
            paths.add(parts[0])
    return paths


def gate_set_manifest_errors(
    root: Path, *, overrides: dict[str, bytes] | None = None
) -> list[str]:
    """MET when the manifest path set matches the closure and the bytes match the tree.

    Owner armor is not a branch requirement (ADR 0057). The tag gate checks
    the checker-digest signature instead.
    """
    errors: list[str] = []
    manifest_path = root / MANIFEST_REL
    if not manifest_path.is_file():
        return [f"missing {MANIFEST_REL}"]
    derived = set(derive_gate_set_paths(root))
    on_disk = manifest_path.read_bytes()
    manifest_paths = _manifest_path_set(on_disk)
    if manifest_paths != derived:
        only_derived = sorted(derived - manifest_paths)
        only_manifest = sorted(manifest_paths - derived)
        if only_derived:
            errors.append(
                f"{MANIFEST_REL}: missing {len(only_derived)} derived gate-set path(s); "
                f"first={only_derived[0]!r}"
            )
        if only_manifest:
            errors.append(
                f"{MANIFEST_REL}: {len(only_manifest)} extra path(s) not in derived closure; "
                f"first={only_manifest[0]!r}"
            )
    expected = manifest_bytes(root, overrides=overrides)
    if on_disk != expected:
        errors.append(f"{MANIFEST_REL}: bytes do not match current gate-set tree")
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
            body = _file_bytes(root, rel, None)
            if body is None:
                return False
            return content_hash(body) == parts[1]
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
