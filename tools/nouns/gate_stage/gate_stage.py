"""Copy live self-ref / mandated paths into staging/<change-id>/ (ADR 0055)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import shutil
import sys
from pathlib import Path

from nouns.self_ref_set.self_ref_set import STAGING_PREFIX

RECORD_NAME = "STAGED.json"


def staging_root(root: Path, change_id: str) -> Path:
    if not change_id or "/" in change_id or change_id in {".", ".."}:
        raise ValueError("change_id must be a single path segment")
    return root / STAGING_PREFIX.rstrip("/") / change_id


def staged_path_for(root: Path, change_id: str, live_rel: str) -> Path:
    rel = live_rel.replace("\\", "/")
    if rel.startswith("./"):
        rel = rel[2:]
    if rel.startswith(STAGING_PREFIX):
        raise ValueError(f"already staged: {rel}")
    return staging_root(root, change_id) / rel


def load_record(root: Path, change_id: str) -> dict[str, object]:
    path = staging_root(root, change_id) / RECORD_NAME
    if not path.is_file():
        return {"schema": 1, "change_id": change_id, "members": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"schema": 1, "change_id": change_id, "members": []}


def write_record(root: Path, change_id: str, record: dict[str, object]) -> Path:
    dest = staging_root(root, change_id) / RECORD_NAME
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return dest


def stage_paths(root: Path, change_id: str, live_rels: list[str]) -> dict[str, object]:
    """Copy live bytes into staging/<change-id>/ mirroring live paths."""
    record = load_record(root, change_id)
    members = list(record.get("members") or [])
    if not isinstance(members, list):
        members = []
    known = {
        item.get("live")
        for item in members
        if isinstance(item, dict)
    }
    for live_rel in live_rels:
        rel = live_rel.replace("\\", "/")
        if rel.startswith("./"):
            rel = rel[2:]
        src = root / rel
        if not src.is_file():
            raise FileNotFoundError(rel)
        dest = staged_path_for(root, change_id, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        staged_rel = dest.relative_to(root).as_posix()
        if rel not in known:
            members.append({"live": rel, "staged": staged_rel})
            known.add(rel)
    record["schema"] = 1
    record["change_id"] = change_id
    record["members"] = members
    write_record(root, change_id, record)
    return record


def staged_overrides(root: Path, change_id: str) -> dict[str, bytes]:
    """Map live relative paths to staged candidate bytes."""
    record = load_record(root, change_id)
    overrides: dict[str, bytes] = {}
    for item in record.get("members") or []:
        if not isinstance(item, dict):
            continue
        live = str(item.get("live") or "")
        staged = str(item.get("staged") or "")
        path = root / staged
        if live and path.is_file():
            overrides[live] = path.read_bytes()
    return overrides


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--change-id" not in args:
        print("STAGE:NOT_MET --change-id required", file=sys.stderr)
        return 2
    change_id = args[args.index("--change-id") + 1]
    paths = [item for item in args if not item.startswith("-") and item != change_id]
    if "--path" in args:
        paths = []
        remaining = args[args.index("--path") + 1 :]
        i = 0
        while i < len(remaining):
            if remaining[i] == "--path":
                i += 1
                continue
            if remaining[i].startswith("-"):
                break
            paths.append(remaining[i])
            i += 1
    if not paths:
        print("STAGE:NOT_MET --path required", file=sys.stderr)
        return 2
    root = Path.cwd()
    try:
        record = stage_paths(root, change_id, paths)
    except (ValueError, FileNotFoundError) as exc:
        print(f"STAGE:NOT_MET {exc}", file=sys.stderr)
        return 1
    print(f"STAGE:MET {change_id} {len(record.get('members') or [])} members")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
