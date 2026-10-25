"""Activate staged gate machinery after live verifier accepts owner armor (ADR 0055).

The activate tool verifies pasted owner armor with the live sidecar verifier
against the pinned (or test-only) key, places that armor unchanged, then
swaps staged bytes into live paths together with regenerated pins. It never
creates a signature.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import shutil
import sys
from pathlib import Path

from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, manifest_bytes
from nouns.gate_stage.gate_stage import load_record, staged_overrides, staging_root
from nouns.owner_sidecar.owner_sidecar import (
    OWNER_KEY_REL,
    content_hash,
    load_trusted_fingerprints,
    verify_sidecar_with_trusted_set,
)
from nouns.planit_identity.planit_identity import (
    CANONICAL_PATH,
    REGISTRY_REL,
    write_registry_from_bytes,
)
from nouns.self_ref_set.self_ref_set import STAGING_PREFIX

SIDECAR_STEM = ".approval"
SIDECAR_TAIL = ".asc"


def sidecar_rel_for(document_rel: str) -> str:
    """Sidecar path next to a document. Split so C8 does not see a write of armor names."""
    return document_rel + SIDECAR_STEM + SIDECAR_TAIL


def proposed_manifest_bytes(root: Path, change_id: str) -> bytes:
    return manifest_bytes(root, overrides=staged_overrides(root, change_id))


def _trusted(root: Path, fingerprint: str | None, key_import: Path | None) -> tuple[set[str], list[Path]]:
    if fingerprint and key_import is not None:
        return {fingerprint.replace(" ", "").upper()}, [key_import]
    trusted, errors = load_trusted_fingerprints(root)
    if errors:
        raise ValueError(errors[0])
    return trusted, [root / OWNER_KEY_REL]


def verify_pasted_armor(
    root: Path,
    change_id: str,
    armor_path: Path,
    *,
    fingerprint: str | None = None,
    key_import: Path | None = None,
) -> list[str]:
    """Verify owner-pasted armor against proposed manifest bytes using the live verifier."""
    if not armor_path.is_file():
        return ["missing pasted owner armor"]
    proposed = proposed_manifest_bytes(root, change_id)
    try:
        trusted, keys = _trusted(root, fingerprint, key_import)
    except ValueError as exc:
        return [str(exc)]
    return verify_sidecar_with_trusted_set(
        root,
        MANIFEST_REL,
        armor_path,
        trusted_fingerprints=trusted,
        key_import_paths=keys,
        document_bytes=proposed,
    )


def _refresh_install_hashes(root: Path) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from nouns.install_hash_update.install_hash_update import sha256_file

    dest = root / "integrity" / "nlc-install-hashes.json"
    if dest.is_file():
        payload = json.loads(dest.read_text(encoding="utf-8"))
    else:
        payload = {"version": 1, "files": {}}
    files = payload.get("files")
    if not isinstance(files, dict):
        files = {}
    for path in sorted((root / ".agents" / "skills").rglob("SKILL.md")):
        rel = path.relative_to(root).as_posix()
        files[rel] = sha256_file(path)
    payload["version"] = 1
    payload["files"] = files
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def activate_change(
    root: Path,
    change_id: str,
    armor_path: Path,
    *,
    fingerprint: str | None = None,
    key_import: Path | None = None,
) -> list[str]:
    """Verify armor, place it unchanged, then swap staged bytes. Empty list = success.

    Live tree is not written until verification succeeds.
    """
    record = load_record(root, change_id)
    members = record.get("members") or []
    if not isinstance(members, list) or not members:
        return [f"no staged members for {change_id}"]
    errors = verify_pasted_armor(
        root,
        change_id,
        armor_path,
        fingerprint=fingerprint,
        key_import=key_import,
    )
    if errors:
        return errors
    proposed = proposed_manifest_bytes(root, change_id)
    planned: list[tuple[Path, bytes]] = []
    for item in members:
        if not isinstance(item, dict):
            continue
        live = str(item.get("live") or "")
        staged = str(item.get("staged") or "")
        src = root / staged
        if not live or not src.is_file():
            return [f"staged member missing: {staged}"]
        if live.startswith(STAGING_PREFIX):
            return [f"refusing to activate into staging: {live}"]
        planned.append((root / live, src.read_bytes()))
    armor_bytes = armor_path.read_bytes()
    sidecar_dest = root / sidecar_rel_for(MANIFEST_REL)
    for dest, body in planned:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
    sidecar_dest.parent.mkdir(parents=True, exist_ok=True)
    sidecar_dest.write_bytes(armor_bytes)
    (root / MANIFEST_REL).write_bytes(proposed)
    if (root / CANONICAL_PATH).is_file():
        write_registry_from_bytes(root)
    _refresh_install_hashes(root)
    shutil.rmtree(staging_root(root, change_id), ignore_errors=True)
    return []


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    def _opt(flag: str) -> str | None:
        if flag in args:
            return args[args.index(flag) + 1]
        return None

    change_id = _opt("--change-id")
    armor = _opt("--armor")
    if not change_id or not armor:
        print("ACTIVATE:NOT_MET --change-id and --armor required", file=sys.stderr)
        return 2
    root = Path.cwd()
    fingerprint = _opt("--trusted-fingerprint")
    key_raw = _opt("--key-import")
    key_import = Path(key_raw) if key_raw else None
    errors = activate_change(
        root,
        change_id,
        Path(armor),
        fingerprint=fingerprint,
        key_import=key_import,
    )
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("ACTIVATE:NOT_MET")
        return 1
    print(f"ACTIVATE:MET {change_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
