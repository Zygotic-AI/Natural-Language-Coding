"""PR touched-file check selection. Fail-closed: narrow only on a hard binary true."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from nouns.check_inputs.check_inputs import SNAPSHOT_REL, check_inputs_map, load_committed

ROOT = Path(__file__).resolve().parents[3]


@dataclass
class Selection:
    """Suite selection for one fitness run."""

    full_suite: bool
    reason: str
    selected: list[str] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)


_ACTIVE: Selection | None = None


def detect_mode() -> str:
    """pr or full. Release-time and main are always full."""
    forced = (os.environ.get("NLC_FITNESS_MODE") or "").strip()
    if forced == "pr":
        return "pr"
    if forced in {"full", "main", "release"}:
        return "full"
    if os.environ.get("NLC_RELEASE_ORCHESTRATOR"):
        return "full"
    event = (os.environ.get("GITHUB_EVENT_NAME") or "").strip()
    if event == "pull_request":
        return "pr"
    return "full"


def _git_changed(root: Path, base: str) -> tuple[list[str] | None, str | None]:
    ref = base if base.startswith("origin/") else f"origin/{base}"
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{ref}...HEAD"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None, "git diff for changed files failed"
    lines = [ln.strip().replace("\\", "/") for ln in (proc.stdout or "").splitlines() if ln.strip()]
    return lines, None


def changed_files(root: Path) -> tuple[list[str] | None, str | None]:
    """Changed paths for this run, or an error reason."""
    override = os.environ.get("NLC_FITNESS_CHANGED")
    if override is not None:
        return [ln.strip().replace("\\", "/") for ln in override.splitlines() if ln.strip()], None
    base = (os.environ.get("NLC_FITNESS_BASE") or os.environ.get("GITHUB_BASE_REF") or "").strip()
    if not base:
        return None, "no base ref for changed files"
    return _git_changed(root, base)


def _file_to_checks(check_inputs: dict[str, list[str]]) -> dict[str, list[str]]:
    inverse: dict[str, list[str]] = {}
    for label, inputs in check_inputs.items():
        for rel in inputs:
            inverse.setdefault(rel, []).append(label)
    return inverse


def select_checks(
    *,
    changed: list[str] | None,
    check_inputs: dict[str, list[str]] | None,
    mode: str,
    error: str | None = None,
) -> Selection:
    """Return a narrowed set only when every step is a hard binary true."""
    if error:
        return Selection(True, f"selection error: {error}")
    if mode != "pr":
        return Selection(True, f"mode={mode} runs the full suite")
    if check_inputs is None:
        return Selection(True, "unreadable map")
    if not isinstance(check_inputs, dict) or not check_inputs:
        return Selection(True, "unreadable map")
    if changed is None:
        return Selection(True, "selection error: missing changed files")
    if not changed:
        return Selection(True, "selection error: empty changed-file list")
    try:
        inverse = _file_to_checks(check_inputs)
    except Exception as exc:  # noqa: BLE001
        return Selection(True, f"selection error: {exc}")
    selected: set[str] = set()
    for rel in changed:
        hits = inverse.get(rel)
        if not hits:
            return Selection(True, f"unmapped file {rel}")
        selected.update(hits)
    skip_reason = "inputs do not intersect changed files"
    skipped = [(label, skip_reason) for label in sorted(check_inputs) if label not in selected]
    return Selection(False, "touched-files intersection", sorted(selected), skipped)


def load_map(root: Path) -> tuple[dict[str, list[str]] | None, str | None]:
    override = (os.environ.get("NLC_CHECK_INPUTS") or "").strip()
    path = Path(override) if override else root / SNAPSHOT_REL
    if override:
        if not path.is_file():
            return None, "unreadable map"
        try:
            import json

            data = json.loads(path.read_text(encoding="utf-8"))
            return check_inputs_map(root, data), None
        except (OSError, ValueError, json.JSONDecodeError):
            return None, "unreadable map"
    try:
        data = load_committed(root)
        return check_inputs_map(root, data), None
    except (TypeError, ValueError):
        return None, "unreadable map"


def select_for_run(root: Path) -> Selection:
    """Resolve mode, map, and changed files, then select. Fail-closed."""
    mode = detect_mode()
    if mode != "pr":
        return select_checks(changed=[], check_inputs={}, mode=mode)
    mapping, map_err = load_map(root)
    if map_err:
        return select_checks(changed=[], check_inputs=None, mode=mode, error=map_err)
    files, files_err = changed_files(root)
    if files_err:
        return select_checks(changed=None, check_inputs=mapping, mode=mode, error=files_err)
    return select_checks(changed=files, check_inputs=mapping, mode=mode)


def apply_run_selection(root: Path) -> Selection:
    """Compute selection once and store it for run()."""
    global _ACTIVE
    _ACTIVE = select_for_run(root)
    return _ACTIVE


def active_selection() -> Selection | None:
    return _ACTIVE


def should_run_check(label: str) -> bool:
    sel = _ACTIVE
    if sel is None or sel.full_suite:
        return True
    return label in sel.selected


def skip_reason_for(label: str) -> str:
    sel = _ACTIVE
    if sel is None:
        return "unknown"
    for name, reason in sel.skipped:
        if name == label:
            return reason
    return sel.reason
