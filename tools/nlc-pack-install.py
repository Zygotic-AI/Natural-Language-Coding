#!/usr/bin/env python3
"""Install a requirement pack tarball into an app repo (merge, not replace tree)."""

from __future__ import annotations

import argparse
import json
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_human_gap import emit_gap  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402


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
    print(f"PACK_INSTALL:MET name={name} version={version}")
    print("  next: review ADRs/rules, ratify, run UC9 delta-regen if rules changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
