"""UC10: record prescribed generate path for goal implementations."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
from datetime import datetime, timezone
from pathlib import Path

PROVENANCE_FILE = "generate-provenance.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record_generate(root: Path, artifact: str, tool: str) -> None:
    rel = artifact.replace("\\", "/").strip().lstrip("./")
    if not rel:
        return
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    path = nlc / PROVENANCE_FILE
    data: dict = {"schema": 1, "artifacts": {}}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"schema": 1, "artifacts": {}}
    arts = data.get("artifacts")
    if not isinstance(arts, dict):
        arts = {}
    arts[rel] = {"tool": tool, "at": _utc_now(), "prescribed_path": True}
    data["schema"] = 1
    data["artifacts"] = arts
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def provenance_for(root: Path, artifact: str) -> dict | None:
    rel = artifact.replace("\\", "/").strip().lstrip("./")
    path = root / ".nlc" / PROVENANCE_FILE
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    arts = data.get("artifacts") or {}
    row = arts.get(rel)
    return row if isinstance(row, dict) else None
