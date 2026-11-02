"""Durable guide state under .nlc/ (interview / planit / requirements)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
from datetime import datetime, timezone
from pathlib import Path


def _nlc(root: Path) -> Path:
    d = root / ".nlc"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def start_planit(root: Path, label: str) -> None:
    _write_json(
        _nlc(root) / "planit-in-progress.json",
        {
            "active": True,
            "label": label,
            "started_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    )


def end_planit(root: Path) -> None:
    path = _nlc(root) / "planit-in-progress.json"
    if path.is_file():
        path.unlink()


def policy_change(root: Path, change: str) -> None:
    _write_json(_nlc(root) / "last-requirement-change.json", {"change": change})
    _write_json(_nlc(root) / "requirements-sync-pending.json", {"pending": True})


def requirements_dirty(root: Path) -> None:
    _write_json(_nlc(root) / "requirements-sync-pending.json", {"pending": True})


def handoff_build(root: Path) -> None:
    items = []
    path = _nlc(root) / "pipeline-state.json"
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            items = [i for i in (data.get("items") or []) if i.get("id") != "handoff-build"]
        except json.JSONDecodeError:
            items = []
    items.append(
        {
            "id": "handoff-build",
            "stage": "build",
            "label": "Build & compile waiting",
            "next": "/planit in your agent",
            "priority": 20,
        }
    )
    _write_json(path, {"schema": 1, "items": items})


def before_generate_ok(root: Path, scopes: list[str]) -> int:
    sys_path = Path(__file__).resolve().parents[2]
    import sys

    if str(sys_path) not in sys.path:
        sys.path.insert(0, str(sys_path))
    from nouns.compliance.compliance import product_content_fingerprint
    from nouns.hub_stamp_scopes.hub_stamp_scopes import writer_scope_errors

    scope_errors = writer_scope_errors(root, scopes)
    if scope_errors:
        for item in scope_errors:
            print(item, file=sys.stderr)
        return 1

    stamp_path = _nlc(root) / "before-generate-stamp.json"
    fingerprint = product_content_fingerprint(root)
    if stamp_path.is_file():
        try:
            old = json.loads(stamp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            old = None
        if (
            isinstance(old, dict)
            and old.get("ok") is True
            and old.get("scopes") == scopes
            and old.get("product_content_sha256") == fingerprint
            and isinstance(old.get("at"), str)
            and old.get("at")
        ):
            return 0
    _write_json(
        stamp_path,
        {
            "ok": True,
            "scopes": scopes,
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "product_content_sha256": fingerprint,
        },
    )
    return 0


def before_generate_stamp_valid(root: Path, max_age_seconds: int = 7200) -> bool:
    path = _nlc(root) / "before-generate-stamp.json"
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if not data.get("ok"):
        return False
    recorded = data.get("product_content_sha256")
    if isinstance(recorded, str) and recorded:
        sys_path = Path(__file__).resolve().parents[2]
        import sys

        if str(sys_path) not in sys.path:
            sys.path.insert(0, str(sys_path))
        from nouns.compliance.compliance import product_content_fingerprint

        # Same bytes: keep the existing "at". Age alone must not force a rewrite.
        return recorded == product_content_fingerprint(root)
    at = data.get("at", "")
    try:
        ts = datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    age = (datetime.now(timezone.utc) - ts).total_seconds()
    return age <= max_age_seconds
