#!/usr/bin/env python3
"""Verify hub mirror matches integrity/nlc-install-hashes.json (post-install)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    hub_tool()
    hub = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    manifest = hub / "integrity" / "nlc-install-hashes.json"
    if not manifest.is_file():
        print("INSTALL_VERIFY:NOT_MET missing integrity/nlc-install-hashes.json")
        return 1
    data = json.loads(manifest.read_text(encoding="utf-8"))
    files: dict[str, str] = dict(data.get("files") or {})
    bad: list[str] = []
    for rel, expected in files.items():
        path = hub / rel
        if not path.is_file():
            bad.append(f"missing {rel}")
            continue
        got = sha256_file(path)
        if got != expected:
            bad.append(f"hash mismatch {rel}")
    if bad:
        print("INSTALL_VERIFY:NOT_MET")
        for line in bad[:20]:
            print(f"  {line}")
        if len(bad) > 20:
            print(f"  … and {len(bad) - 20} more")
        return 1
    print(f"INSTALL_VERIFY:MET files={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
