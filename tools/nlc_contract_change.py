"""ADR 0006: loud prove for breaking published contract changes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _fitness_blocker(root: Path, script: str, label: str) -> str | None:
    hub = Path(__file__).resolve().parents[1]
    tools = hub / "tools"
    path = tools / script
    proc = subprocess.run(
        [sys.executable, str(path), str(root.resolve())],
        cwd=str(hub),
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return None
    detail = ""
    for line in (proc.stdout or "").splitlines():
        if line.startswith("VIOLATION"):
            detail = line.removeprefix("VIOLATION ").strip()
            break
    if not detail:
        detail = (proc.stdout or proc.stderr or "NOT_MET").strip().splitlines()[-1]
    return f"ADR 0006 ({label}): {detail}"


def _has_changed_scope(root: Path) -> bool:
    hub = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(hub / "tools"))
    import changeset

    try:
        root.resolve().relative_to(hub.resolve())
        repo_root = hub
    except ValueError:
        repo_root = root
    return changeset.changed_paths(root, repo_root) is not None


def _c10_script(root: Path) -> str:
    if _has_changed_scope(root):
        return "fitness-c10-changed.py"
    return "fitness-c10.py"


def _c21_script(root: Path) -> str:
    if _has_changed_scope(root):
        return "fitness-c21-changed.py"
    return "fitness-c21.py"


def contract_change_blockers(root: Path) -> list[str]:
    """C10 breaking schema + C21 impact list on non-hub product trees."""
    from nlc_pipeline import is_hub_repo
    import product_tree

    if is_hub_repo(root):
        return []
    if not product_tree.contract_change_applies(root):
        return []

    blockers: list[str] = []
    for script, label in ((_c10_script(root), "C10"), (_c21_script(root), "C21")):
        msg = _fitness_blocker(root, script, label)
        if msg:
            blockers.append(msg)

    from nlc_contract_break_accept import acceptance_blockers

    blockers.extend(acceptance_blockers(root))
    return blockers
