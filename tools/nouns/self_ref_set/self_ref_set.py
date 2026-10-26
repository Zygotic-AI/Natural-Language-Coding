"""Derived self-referential gate-machinery set (ADR 0055 / Climb 3 Q2).

A path is in this set when it is both mandated (identity pin, install
fingerprint, and/or gate-set member) and part of the machinery that
applies or verifies that pin or signature. Membership is computed from
role detectors over tracked files — not a hand-kept path list.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

SNAPSHOT_REL = "integrity/self-ref-set.json"
STAGING_PREFIX = "staging/"

_ROLE_MARKERS: dict[str, tuple[str, ...]] = {
    "gating_skill": (
        "fitness-planit-identity.py --skill-only",
        "python3 tools/ci_fitness.py",
        "planit-skill-identity",
        "releasable-gates.json",
    ),
    "owner_hook": (
        "nlc-planit-identity.sh",
        "beforeSubmitPrompt",
        "PLANIT_IDENTITY",
    ),
    "identity_tool": (
        "CANONICAL_PATH",
        "planit-skill-registry.json",
        "content_sha256",
    ),
    "gate_set_derivation": (
        "def derive_gate_set_paths",
        "GATE_SET_EXCLUSIONS",
    ),
    "manifest_generator": (
        "def manifest_bytes",
        "gate-set-baseline.manifest.sha256",
        "no ratification",
    ),
    "sidecar_verifier": (
        "def verify_sidecar_p1",
        "gpg_verify_clearsigned",
        "TRUSTED_FINGERPRINTS",
    ),
    "c8": (
        "def ratification_write_errors",
        "no tracked tool writes",
        "*.approval.asc",
    ),
    "install_hash": (
        "nlc-install-hashes.json",
        "INSTALL_VERIFY",
    ),
    "staging_machinery": (
        "def derive_self_ref_set",
        "def stage_paths",
        "def activate_change",
        "live self-ref member edited outside activation",
    ),
}


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
        if not rel or "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        if rel.startswith(STAGING_PREFIX):
            continue
        out.append(rel)
    return out


def _read_text(root: Path, rel: str) -> str:
    path = root / rel
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def _is_machinery_file(rel: str) -> bool:
    if rel.endswith((".py", ".sh", ".json")):
        return True
    if rel.endswith("/SKILL.md"):
        return True
    if rel.startswith(".cursor/hooks/") or rel == ".cursor/hooks.json":
        return True
    if rel.startswith("integrity/owner-keys/"):
        return True
    return False


def _role_hits(root: Path, tracked: list[str], role: str, needles: tuple[str, ...]) -> set[str]:
    hits: set[str] = set()
    needed = 2 if len(needles) > 1 else 1
    for rel in tracked:
        if not _is_machinery_file(rel):
            continue
        text = _read_text(root, rel)
        if not text:
            continue
        matches = sum(1 for needle in needles if needle in text)
        if matches >= needed:
            hits.add(rel)
    return hits


def _skill_role_hits(root: Path, tracked: list[str]) -> set[str]:
    """Gating skills: published SKILL.md that run identity, fitness, or verify pins."""
    hits: set[str] = set()
    needles = _ROLE_MARKERS["gating_skill"]
    for rel in tracked:
        if not rel.startswith(".agents/skills/") or not rel.endswith("/SKILL.md"):
            continue
        text = _read_text(root, rel)
        if any(needle in text for needle in needles):
            hits.add(rel)
    return hits


def _hook_hits(tracked: list[str]) -> set[str]:
    hits: set[str] = set()
    for rel in tracked:
        if rel.startswith(".cursor/hooks/") or rel == ".cursor/hooks.json":
            hits.add(rel)
    return hits


def _owner_key_hits(tracked: list[str]) -> set[str]:
    return {rel for rel in tracked if rel.startswith("integrity/owner-keys/")}


def _registry_and_hash_files(tracked: list[str]) -> set[str]:
    names = {
        "integrity/planit-skill-registry.json",
        "integrity/nlc-install-hashes.json",
        "integrity/gate-set-baseline.manifest.sha256",
        "integrity/releasable-gates.json",
        ".nlc/planit-change-evidence.json",
    }
    return {rel for rel in tracked if rel in names}


def derive_self_ref_set(root: Path) -> list[str]:
    """Return sorted repo-relative paths in the self-referential gate set."""
    tracked = _git_tracked(root)
    hits: set[str] = set()
    hits |= _skill_role_hits(root, tracked)
    hits |= _hook_hits(tracked)
    hits |= _owner_key_hits(tracked)
    hits |= _registry_and_hash_files(tracked)
    for role, needles in _ROLE_MARKERS.items():
        if role == "gating_skill":
            continue
        hits |= _role_hits(root, tracked, role, needles)
    for rel in tracked:
        if not _is_machinery_file(rel):
            continue
        text = _read_text(root, rel)
        if any(
            token in text
            for token in (
                "def stage_paths",
                "def activate_change",
                "def derive_self_ref_set",
                "def derive_mandated_paths",
                "def write_registry_from_bytes",
            )
        ):
            hits.add(rel)
    return sorted(hits)


def snapshot_payload(root: Path) -> dict[str, object]:
    members = derive_self_ref_set(root)
    return {
        "schema": 1,
        "ssot": "tools/nouns/self_ref_set/self_ref_set.py",
        "description": (
            "Derived self-referential gate-machinery set. Do not hand-edit. "
            "Regenerate with python3 tools/derive-self-ref-set.py --write."
        ),
        "members": members,
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
    if on_disk.get("members") != derived["members"]:
        return [f"{SNAPSHOT_REL}: drift versus derive_self_ref_set (regenerate)"]
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
    members = derive_self_ref_set(root)
    if "--write" in args:
        dest = write_snapshot(root)
        print(f"wrote {dest.relative_to(root)} ({len(members)} members)")
    for rel in members:
        print(rel)
    print(f"SELF_REF_SET:{len(members)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
