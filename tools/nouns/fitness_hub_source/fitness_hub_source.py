"""Resolve hub tool source text (thin adapter vs noun implementation)."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
_IMPORT_NOUN = re.compile(
    r"from\s+nouns\.([A-Za-z0-9_]+)(?:\.[A-Za-z0-9_]+)?\s+import"
)
_GOAL_EXEC = re.compile(r"goals/([A-Za-z0-9_]+)/execute\.(sh|ps1)")


def implementation_path(path: Path) -> Path:
    """Return the noun or goal file a thin entrypoint calls, else path."""
    if not path.is_file():
        return path
    text = path.read_text(encoding="utf-8", errors="replace")
    imported = _IMPORT_NOUN.search(text)
    if imported:
        slug = imported.group(1)
        candidate = ROOT / "tools" / "nouns" / slug / f"{slug}.py"
        if candidate.is_file():
            return candidate
    goal = _GOAL_EXEC.search(text.replace("\\", "/"))
    if goal:
        candidate = ROOT / "goals" / goal.group(1) / f"execute.{goal.group(2)}"
        if candidate.is_file():
            return candidate
    return path


def read_tool(rel: str, noun: str | None = None) -> str:
    """Return implementation text for fitness string checks."""
    _ = noun
    rel_norm = rel.replace("\\", "/")
    adapter = ROOT / rel_norm
    if not adapter.is_file():
        return ""
    text = adapter.read_text(encoding="utf-8", errors="replace")
    followed = implementation_path(adapter)
    if followed == adapter:
        return text
    impl = followed.read_text(encoding="utf-8", errors="replace")
    return text + "\n" + impl
