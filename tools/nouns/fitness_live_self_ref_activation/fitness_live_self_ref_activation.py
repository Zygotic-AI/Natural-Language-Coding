"""Refuse live self-ref member edits that are not an activation or first bootstrap."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

from nouns.mandated_paths.mandated_paths import git_changed_paths
from nouns.release_probe.release_probe import ProbeFailure
from nouns.planit_identity.planit_identity import CANONICAL_PATH, REGISTRY_REL, content_hash, load_registry
from nouns.self_ref_set.self_ref_set import STAGING_PREFIX, derive_self_ref_set

ROOT = Path(__file__).resolve().parents[3]
BOOTSTRAP_MARKERS = (
    "tools/fitness-live-self-ref-activation.py",
    "tools/activate-gate-machinery.py",
    "tools/nouns/gate_activate/gate_activate.py",
)


def _hub_repo(root: Path) -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from nlc_pipeline import is_hub_repo

    return is_hub_repo(root)


def _base_paths(root: Path) -> set[str]:
    proc = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/release/v0.4.0"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    base = proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else ""
    if not base:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        base = proc.stdout.strip()
    if not base:
        return set()
    listed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", base],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        line.strip().replace("\\", "/")
        for line in (listed.stdout or "").splitlines()
        if line.strip()
    }


def _current_paths(root: Path) -> set[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        line.strip().replace("\\", "/")
        for line in (proc.stdout or "").splitlines()
        if line.strip()
    }


def _registry_matches(root: Path) -> bool:
    skill = root / CANONICAL_PATH
    if not skill.is_file():
        return False
    try:
        registry = load_registry(root)
    except (OSError, ValueError):
        return False
    return registry.get("content_sha256") == content_hash(skill.read_bytes())


def _is_bootstrap(root: Path) -> bool:
    base = _base_paths(root)
    current = _current_paths(root)
    return any(marker in current and marker not in base for marker in BOOTSTRAP_MARKERS)


def _is_activation_commit(root: Path, changed: list[str]) -> bool:
    changed_set = set(changed)
    sidecar = root / "integrity" / "gate-set-baseline.manifest.sha256"
    armor = Path(str(sidecar) + ".approval" + ".asc")
    if not armor.is_file():
        return False
    if REGISTRY_REL not in changed_set and not _registry_matches(root):
        return False
    if not _registry_matches(root):
        return False
    return True


def live_member_edit_errors(root: Path) -> list[str]:
    try:
        changed_paths = git_changed_paths(root)
    except ProbeFailure as exc:
        return [f"changed-path probe: {exc}"]
    changed = [
        rel
        for rel in changed_paths
        if not rel.startswith(STAGING_PREFIX)
    ]
    self_ref = set(derive_self_ref_set(root))
    live_edits = [rel for rel in changed if rel in self_ref]
    if not live_edits:
        return []
    if _is_activation_commit(root, changed):
        return []
    if _is_bootstrap(root) and _registry_matches(root):
        return []
    return [
        f"live self-ref member edited outside activation: {rel}" for rel in live_edits
    ]


def main() -> int:
    args = sys.argv[1:]
    root = Path(args[0]).resolve() if args and not args[0].startswith("-") else ROOT
    if not _hub_repo(root):
        print("LIVE_SELF_REF:MET skip (hub-only gate, not hub tree)")
        return 0
    errors = live_member_edit_errors(root)
    if errors:
        for item in errors:
            print(f"VIOLATION {item}")
        print("LIVE_SELF_REF:NOT_MET")
        return 1
    print("LIVE_SELF_REF:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
