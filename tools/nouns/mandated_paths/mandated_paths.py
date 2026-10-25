"""Derived mandated-path list (ADR 0055 / Climb 2 inheritance).

Every producer that touches a listed path inherits the pins that name
those bytes. The list is computed from in-force mandates (identity,
install fingerprints, gate-set membership, Accepted ADR sidecars,
content-tree evidence, owner keys) — not restated by each recipe.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from nouns.gate_set.gate_set import derive_gate_set_paths
from nouns.planit_identity.planit_identity import CANONICAL_PATH, REGISTRY_REL, content_hash
from nouns.self_ref_set.self_ref_set import STAGING_PREFIX

SNAPSHOT_REL = "integrity/mandated-paths.json"
INSTALL_HASH_REL = "integrity/nlc-install-hashes.json"
MANIFEST_REL = "integrity/gate-set-baseline.manifest.sha256"
CONTENT_TREE_REL = "integrity/hub-content-tree-hash.txt"
FINDINGS_REL = "FINDINGS.md"
EVIDENCE_REL = ".nlc/planit-change-evidence.json"

PIN_IDENTITY = "identity_registry"
PIN_INSTALL = "install_hash"
PIN_MANIFEST = "gate_set_manifest"
PIN_SIDECAR = "owner_sidecar"
PIN_CONTENT_TREE = "content_tree"
PIN_GENERATED_BYTES = "generated_from_bytes"


def _git_tracked(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    out: list[str] = []
    for line in (proc.stdout or "").splitlines():
        rel = line.strip().replace("\\", "/")
        if not rel or rel.startswith(STAGING_PREFIX):
            continue
        out.append(rel)
    return out


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _add(mapping: dict[str, list[str]], rel: str, pin: str) -> None:
    pins = mapping.setdefault(rel, [])
    if pin not in pins:
        pins.append(pin)


def derive_mandated_paths(root: Path) -> dict[str, list[str]]:
    """Return {repo-relative path: pin kinds} derived from in-force mandates."""
    mapping: dict[str, list[str]] = {}
    tracked = set(_git_tracked(root))
    for rel in derive_gate_set_paths(root):
        if rel.startswith(STAGING_PREFIX):
            continue
        _add(mapping, rel, PIN_MANIFEST)
    for rel in tracked:
        if rel.startswith(".agents/skills/") and rel.endswith("/SKILL.md"):
            _add(mapping, rel, PIN_INSTALL)
            if rel == CANONICAL_PATH:
                _add(mapping, rel, PIN_IDENTITY)
        if rel.startswith("adrs/") and rel.endswith(".md") and "/owner-approvals/" not in rel:
            text = (root / rel).read_text(encoding="utf-8") if (root / rel).is_file() else ""
            if "- Status: Accepted" in text:
                _add(mapping, rel, PIN_SIDECAR)
        if rel.startswith("integrity/owner-keys/"):
            _add(mapping, rel, PIN_SIDECAR)
    for rel, pin in (
        (REGISTRY_REL, PIN_GENERATED_BYTES),
        (INSTALL_HASH_REL, PIN_GENERATED_BYTES),
        (MANIFEST_REL, PIN_GENERATED_BYTES),
        (CONTENT_TREE_REL, PIN_CONTENT_TREE),
        (FINDINGS_REL, PIN_CONTENT_TREE),
        (EVIDENCE_REL, PIN_IDENTITY),
    ):
        if rel in tracked or (root / rel).is_file():
            _add(mapping, rel, pin)
    return {key: mapping[key] for key in sorted(mapping)}


def git_changed_paths(root: Path, base: str | None = None) -> list[str]:
    """Repo-relative paths changed versus merge-base (plus dirty and staged)."""
    names: set[str] = set()
    merge_base = base
    if merge_base is None:
        proc = subprocess.run(
            ["git", "merge-base", "HEAD", "origin/release/v0.4.0"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            merge_base = proc.stdout.strip()
        else:
            merge_base = "HEAD"
    commands = (
        ["git", "diff", "--name-only", f"{merge_base}...HEAD"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "diff", "--name-only"],
    )
    if merge_base == "HEAD":
        commands = commands[1:]
    for argv in commands:
        proc = subprocess.run(
            argv,
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            continue
        for line in (proc.stdout or "").splitlines():
            rel = line.strip().replace("\\", "/")
            if rel and not rel.startswith(STAGING_PREFIX):
                names.add(rel)
    return sorted(names)


def _registry_matches(root: Path) -> bool:
    path = root / REGISTRY_REL
    skill = root / CANONICAL_PATH
    if not path.is_file() or not skill.is_file():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return (
        payload.get("canonical_path") == CANONICAL_PATH
        and payload.get("content_sha256") == content_hash(skill.read_bytes())
    )


def _install_hash_matches(root: Path, rel: str) -> bool:
    path = root / INSTALL_HASH_REL
    target = root / rel
    if not path.is_file() or not target.is_file():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    files = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(files, dict):
        return False
    return files.get(rel) == _sha256(target)


def _manifest_matches_tree(root: Path) -> bool:
    from nouns.gate_set_manifest.gate_set_manifest import manifest_bytes

    path = root / MANIFEST_REL
    if not path.is_file():
        return False
    return path.read_bytes() == manifest_bytes(root)


def pin_move_errors(root: Path, changed: list[str] | None = None) -> list[str]:
    """Refuse when a mandated path changed and its pins did not move."""
    changed_list = list(changed) if changed is not None else git_changed_paths(root)
    changed_set = set(changed_list)
    mandated = derive_mandated_paths(root)
    errors: list[str] = []
    for rel in changed_list:
        pins = mandated.get(rel) or []
        if PIN_IDENTITY in pins and REGISTRY_REL not in changed_set:
            errors.append(
                f"mandate-pins {rel}: identity registry {REGISTRY_REL} did not move"
            )
        if PIN_IDENTITY in pins and REGISTRY_REL in changed_set and not _registry_matches(root):
            errors.append(f"mandate-pins {rel}: registry bytes do not match skill bytes")
        if PIN_INSTALL in pins:
            if INSTALL_HASH_REL not in changed_set and not _install_hash_matches(root, rel):
                errors.append(
                    f"mandate-pins {rel}: install hash {INSTALL_HASH_REL} did not move"
                )
            elif not _install_hash_matches(root, rel):
                errors.append(f"mandate-pins {rel}: install hash does not match file bytes")
        if PIN_MANIFEST in pins and rel not in {MANIFEST_REL}:
            if MANIFEST_REL not in changed_set and not _manifest_matches_tree(root):
                errors.append(
                    f"mandate-pins {rel}: gate-set manifest {MANIFEST_REL} did not move"
                )
    if CANONICAL_PATH in changed_set and not _registry_matches(root):
        msg = f"mandate-pins {CANONICAL_PATH}: identity registry {REGISTRY_REL} did not move"
        if msg not in errors:
            errors.append(msg)
    return errors


def unsigned_manifest_incomplete(root: Path, changed: list[str] | None = None) -> list[str]:
    """A regenerated-but-unsigned manifest is INCOMPLETE produce, not a finished step."""
    changed_list = list(changed) if changed is not None else git_changed_paths(root)
    mandated = derive_mandated_paths(root)
    touches_member = any(PIN_MANIFEST in (mandated.get(rel) or []) for rel in changed_list)
    if not touches_member and MANIFEST_REL not in changed_list:
        return []
    sidecar = root / (MANIFEST_REL + ".approval.asc")
    if not sidecar.is_file():
        return [f"INCOMPLETE {MANIFEST_REL}: regenerated without owner sidecar"]
    from nouns.owner_sidecar.owner_sidecar import verify_sidecar_p1

    errors = verify_sidecar_p1(root, MANIFEST_REL)
    if errors:
        return [f"INCOMPLETE {MANIFEST_REL}: {errors[0]}"]
    return []


def snapshot_payload(root: Path) -> dict[str, object]:
    mandated = derive_mandated_paths(root)
    return {
        "schema": 1,
        "ssot": "tools/nouns/mandated_paths/mandated_paths.py",
        "description": (
            "Derived mandated paths imported by the Skill type recipe, "
            "the skill-author checklist, and /release. Do not hand-edit."
        ),
        "paths": mandated,
    }


def snapshot_errors(root: Path) -> list[str]:
    path = root / SNAPSHOT_REL
    derived = snapshot_payload(root)
    if not path.is_file():
        return [f"missing {SNAPSHOT_REL}"]
    try:
        on_disk = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{SNAPSHOT_REL}: JSON error {exc}"]
    if not isinstance(on_disk, dict):
        return [f"{SNAPSHOT_REL}: must be an object"]
    if on_disk.get("paths") != derived["paths"]:
        return [f"{SNAPSHOT_REL}: drift versus derive_mandated_paths (regenerate)"]
    return []


def write_snapshot(root: Path) -> Path:
    dest = root / SNAPSHOT_REL
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(snapshot_payload(root), indent=2) + "\n", encoding="utf-8")
    return dest


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path.cwd()
    if args and not args[0].startswith("-"):
        root = Path(args[0]).resolve()
        args = args[1:]
    payload = snapshot_payload(root)
    if "--write" in args:
        dest = write_snapshot(root)
        print(f"wrote {dest.relative_to(root)} ({len(payload['paths'])} paths)")
    for rel, pins in payload["paths"].items():
        print(f"{rel} {' '.join(pins)}")
    print(f"MANDATED_PATHS:{len(payload['paths'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
