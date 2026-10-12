"""ADR 0052 P5: owner key rotation anchored in signed gate-set manifest only."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL
from nouns.owner_sidecar.owner_sidecar import (
    TRUSTED_REL,
    OWNER_KEY_REL,
    content_hash,
    load_trusted_fingerprints_from_text,
    sidecar_path_for_document,
    verify_sidecar_with_trusted_set,
)

KEY_FILES = (
    "integrity/owner-keys/TRUSTED_FINGERPRINTS",
    "integrity/owner-keys/richard-pickett.asc",
)
DEFAULT_BASE_REF = "origin/release/v0.3.0"


def _git_show(root: Path, rev: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "show", f"{rev}:{rel}"],
        cwd=str(root),
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def _merge_base(root: Path, base_ref: str) -> str | None:
    proc = subprocess.run(
        ["git", "merge-base", "HEAD", base_ref],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return (proc.stdout or "").strip() or None


def _key_material_changed(root: Path, base_rev: str) -> bool:
    for rel in KEY_FILES:
        base_bytes = _git_show(root, base_rev, rel)
        path = root / rel
        if base_bytes is None or not path.is_file():
            return True
        if content_hash(base_bytes) != content_hash(path.read_bytes()):
            return True
    return False


def _trusted_before(root: Path, base_rev: str) -> tuple[set[str], list[str]]:
    raw = _git_show(root, base_rev, TRUSTED_REL)
    if raw is None:
        return set(), [f"cannot read {TRUSTED_REL} at base {base_rev}"]
    text = raw.decode("utf-8", errors="replace")
    return load_trusted_fingerprints_from_text(text)


def key_rotation_errors(root: Path, *, base_ref: str = DEFAULT_BASE_REF) -> list[str]:
    """When owner-key bytes changed since base, manifest sidecar must verify under pre-change trust."""
    base_rev = _merge_base(root, base_ref)
    if not base_rev:
        return [f"cannot resolve merge-base with {base_ref}"]
    if not _key_material_changed(root, base_rev):
        return []
    trusted_before, terr = _trusted_before(root, base_rev)
    if terr:
        return terr
    base_key = _git_show(root, base_rev, OWNER_KEY_REL)
    if base_key is None:
        return [f"cannot read {OWNER_KEY_REL} at base {base_rev}"]
    import tempfile

    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        key_path = Path(tmp) / "base-owner.asc"
        key_path.write_bytes(base_key)
        asc_path = root / sidecar_path_for_document(MANIFEST_REL)
        errors.extend(
            verify_sidecar_with_trusted_set(
                root,
                MANIFEST_REL,
                asc_path,
                trusted_fingerprints=trusted_before,
                key_import_paths=[key_path],
            )
        )
    return errors


def key_trust_errors(root: Path) -> list[str]:
    """MET when ALL OF: owner-key paths are in gate-set manifest; rotation uses pre-change signer."""
    from nouns.gate_set_manifest.gate_set_manifest import path_in_manifest_holds

    errors: list[str] = []
    for rel in KEY_FILES:
        if not path_in_manifest_holds(root, rel):
            errors.append(f"{rel}: not listed in ratified gate-set manifest")
    errors.extend(key_rotation_errors(root))
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = key_trust_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
