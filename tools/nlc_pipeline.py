"""Kanban pipeline under .nlc/ (ADR 0019). Work flows Requirements → Build → Verify."""

from __future__ import annotations

import json
from pathlib import Path

# Guide (/interview) is not a stage — it is always-on. Queue buckets only:
STAGE_ORDER: list[str] = [
    "requirements",
    "build",
    "verify",
    "maintain",
]

STAGE_TITLES: dict[str, str] = {
    "requirements": "Requirements",
    "build": "Build & compile",
    "verify": "Verify",
    "maintain": "Maintain",
}


def normalize_stage(stage: str) -> str:
    if stage == "guide":
        return "requirements"
    return stage


def is_hub_repo(root: Path) -> bool:
    return (
        (root / "tools" / "nlc.py").is_file()
        and (root / "integrity" / "nlc-install-hashes.json").is_file()
    )


def _pipeline_path(root: Path) -> Path:
    return root / ".nlc" / "pipeline-state.json"


def load_persisted_items(root: Path) -> list[dict]:
    path = _pipeline_path(root)
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    raw = data.get("items")
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for item in raw:
        if isinstance(item, dict) and item.get("id") and item.get("stage"):
            row = dict(item)
            row["stage"] = normalize_stage(str(row["stage"]))
            out.append(row)
    return out


def save_persisted_items(root: Path, items: list[dict]) -> None:
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    payload = {"schema": 1, "items": items}
    _pipeline_path(root).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def upsert_persisted_item(root: Path, item: dict) -> None:
    items = load_persisted_items(root)
    ident = item["id"]
    row = dict(item)
    row["stage"] = normalize_stage(str(row.get("stage", "requirements")))
    items = [i for i in items if i.get("id") != ident]
    items.append(row)
    save_persisted_items(root, items)


def clear_persisted_stage(root: Path, stage: str) -> None:
    stage = normalize_stage(stage)
    items = [
        i
        for i in load_persisted_items(root)
        if normalize_stage(str(i.get("stage", ""))) != stage
    ]
    save_persisted_items(root, items)


def merge_queue_items(scanned: list[dict], persisted: list[dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    for item in scanned + persisted:
        ident = str(item.get("id", ""))
        if not ident:
            continue
        row = dict(item)
        row["stage"] = normalize_stage(str(row.get("stage", "requirements")))
        prev = by_id.get(ident)
        if prev is None or int(row.get("priority", 99)) < int(prev.get("priority", 99)):
            by_id[ident] = row
    merged = list(by_id.values())
    merged.sort(
        key=lambda x: (
            STAGE_ORDER.index(x["stage"])
            if x.get("stage") in STAGE_ORDER
            else len(STAGE_ORDER),
            int(x.get("priority", 99)),
        )
    )
    return merged
