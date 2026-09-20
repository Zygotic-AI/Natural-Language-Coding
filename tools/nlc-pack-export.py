#!/usr/bin/env python3
"""Export a requirement pack tarball from the current repo (v0.2 foundation)."""

from __future__ import annotations

import argparse
import io
import json
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Export NLC requirement pack")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--name", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("dist"))
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    root = args.root.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema": 1,
        "name": args.name,
        "version": args.version,
        "description": args.description or f"Requirement pack {args.name}",
        "includes": {},
    }
    members: list[tuple[Path, str]] = []
    adrs = root / "adrs"
    if adrs.is_dir():
        adr_files = sorted(p.name for p in adrs.glob("*.md"))
        manifest["includes"]["adrs"] = adr_files
        for name in adr_files:
            members.append((adrs / name, f"adrs/{name}"))
    rules = root / "rules" / "adopted.json"
    if rules.is_file():
        manifest["includes"]["rules"] = "rules/adopted.json"
        members.append((rules, "rules/adopted.json"))
    facts = root / "knowledge" / "facts.json"
    if facts.is_file():
        manifest["includes"]["knowledge_facts"] = "knowledge/facts.json"
        members.append((facts, "knowledge/facts.json"))

    if not members:
        print("PACK_EXPORT:NOT_MET", file=sys.stderr)
        print("  missing: adrs/, rules/adopted.json, or knowledge/facts.json", file=sys.stderr)
        return 1

    archive = out_dir / f"pack-{args.name}-{args.version}.tar.gz"
    with tarfile.open(archive, "w:gz") as tf:
        manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
        data = io.BytesIO(manifest_bytes)
        info = tarfile.TarInfo(name="pack-manifest.json")
        info.size = len(manifest_bytes)
        tf.addfile(info, data)
        for src, arc in members:
            tf.add(src, arcname=arc)

    print(f"PACK_EXPORT:MET path={archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
