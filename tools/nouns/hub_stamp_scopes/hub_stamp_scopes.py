"""SSOT for required hub before-generate stamp scopes."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import sys
from pathlib import Path

HUB_STAMP_SCOPES_REL = "integrity/hub-stamp-scopes.json"
HUB_STAMP_REL = ".nlc/before-generate-stamp.json"


def _tools_on_path() -> None:
    tools = Path(__file__).resolve().parents[2]
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))


def is_hub(root: Path) -> bool:
    """True when root is the Natural Language Coding hub tree."""
    _tools_on_path()
    from nlc_pipeline import is_hub_repo

    return is_hub_repo(root)


def load_required_scopes(root: Path) -> tuple[list[str] | None, str | None]:
    """Return required scope names, or (None, error) when the source is unusable."""
    return load_scopes_file(root / HUB_STAMP_SCOPES_REL)


def load_scopes_file(path: Path) -> tuple[list[str] | None, str | None]:
    """Return scope names from one JSON file, or (None, error) when unusable."""
    if not path.is_file():
        return None, "missing hub stamp scopes source"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return None, "unreadable hub stamp scopes source"
    if not raw.strip():
        return None, "empty hub stamp scopes source"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None, "invalid hub stamp scopes source"
    scopes = data.get("scopes")
    if not isinstance(scopes, list) or not scopes:
        return None, "empty hub stamp scopes source"
    if not all(isinstance(s, str) and s for s in scopes):
        return None, "invalid hub stamp scopes source"
    return list(scopes), None


def stamp_scope_gap_errors(required: list[str], stamp_scopes: list[str]) -> list[str]:
    """Return errors when stamp_scopes omit a required name."""
    missing = [name for name in required if name not in stamp_scopes]
    if missing:
        return [f"hub before-generate stamp missing scopes: {', '.join(missing)}"]
    return []


def default_hub_scopes(root: Path) -> list[str] | None:
    """Default --scope list for hub before-generate when the operator passes none."""
    if not is_hub(root):
        return None
    scopes, err = load_required_scopes(root)
    if err or not scopes:
        return None
    return scopes


def writer_scope_errors(root: Path, scopes: list[str]) -> list[str]:
    """Refuse hub stamp writes unless argv scopes include every required name."""
    if not is_hub(root):
        return []
    required, err = load_required_scopes(root)
    if err:
        return [err]
    assert required is not None
    missing = [name for name in required if name not in scopes]
    if missing:
        return [f"hub before-generate missing scopes: {', '.join(missing)}"]
    return []


def stamp_check_errors(root: Path) -> list[str]:
    """Fail when the committed hub stamp lacks a required scope."""
    if not is_hub(root):
        return []
    required, err = load_required_scopes(root)
    if err:
        return [err]
    assert required is not None
    stamp_path = root / HUB_STAMP_REL
    if not stamp_path.is_file():
        return ["missing hub before-generate stamp"]
    try:
        data = json.loads(stamp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ["invalid hub before-generate stamp"]
    stamp_scopes = data.get("scopes")
    if not isinstance(stamp_scopes, list):
        return ["hub before-generate stamp scopes not a list"]
    return stamp_scope_gap_errors(required, stamp_scopes)
