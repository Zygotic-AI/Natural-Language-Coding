#!/usr/bin/env python3
"""Install a requirement pack tarball into an app repo (merge, not replace tree)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_human_gap import emit_gap  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402

UC9_HINT = "./nlc maintainer regen-plan --change rule:<id> --write-queue"


def write_pack_consume_status(root: Path, manifest: dict) -> Path:
    """Write machine-checkable post-install consume/regen status (hub_v02.pack_consume_regen)."""
    name = manifest.get("name", "unknown")
    version = manifest.get("version", "0.0.0")
    tags = manifest.get("tags")
    includes = manifest.get("includes") or {}
    scope_data = includes.get("knowledge_facts") or includes.get("rules") or "na"
    if tags is None:
        tags = "na"
    payload = {
        "schema": 1,
        "pack": f"{name}@{version}",
        "name": name,
        "version": version,
        "scope_tags": tags if tags != "na" else "na",
        "scope_data": scope_data if scope_data else "na",
        "uc9_queue_hint": UC9_HINT,
        "written_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out = root / ".nlc" / "pack-consume-status.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Install NLC requirement pack")
    parser.add_argument("archive", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()
    root = args.root.resolve()
    archive = args.archive.resolve()
    if not archive.is_file():
        return emit_gap(
            "Pack install needs the .tar.gz file you received.",
            missing=[f"no file at {archive}"],
            examples=["./nlc pack install ./dist/pack-name-1.0.0.tar.gz"],
            machine="PACK_INSTALL:NOT_MET",
        )

    with tarfile.open(archive, "r:gz") as tf:
        manifest_member = tf.getmember("pack-manifest.json")
        manifest = json.loads(tf.extractfile(manifest_member).read().decode("utf-8"))
        for member in tf.getmembers():
            if member.name == "pack-manifest.json" or member.isdir():
                continue
            dest = root / member.name
            if dest.exists() and not args.force:
                return emit_gap(
                    "This pack would overwrite files already in your repo.",
                    missing=[str(dest.relative_to(root))],
                    ask="Review the pack, then reinstall with --force if you intend to replace those files?",
                    choices=["Abort and diff the pack", "Install with --force after review"],
                    examples=[f"./nlc pack install {archive.name} --force"],
                    machine="PACK_INSTALL:NOT_MET",
                )
            dest.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                continue
            dest.write_bytes(src.read())

    packs_dir = root / ".nlc" / "packs"
    packs_dir.mkdir(parents=True, exist_ok=True)
    name = manifest.get("name", "unknown")
    version = manifest.get("version", "0.0.0")
    record = packs_dir / f"{name}-{version}.json"
    record.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    status_path = write_pack_consume_status(root, manifest)
    print(f"PACK_INSTALL:MET name={name} version={version}")
    print(f"  consume-status: {status_path.relative_to(root)}")
    if (root / "rules" / "adopted.json").is_file():
        pending = root / ".nlc" / "requirements-sync-pending.json"
        pending.parent.mkdir(parents=True, exist_ok=True)
        pending.write_text(
            json.dumps(
                {
                    "reason": "requirement pack install",
                    "pack": f"{name}@{version}",
                    "uc9_hint": UC9_HINT,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print("  next: review ADRs/rules, ratify, run UC9 delta-regen if rules changed")
    print(f"  uc9 hint: {UC9_HINT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
