#!/usr/bin/env python3
"""ADR 0041: hub pack registry v1 wired + uc-product pack_registry closed."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for rel in (
        "integrity/hub-pack-registry.json",
        "integrity/schemas/hub-pack-registry.schema.json",
        "docs/nlc/PACK-REGISTRY.md",
        "tools/validate-hub-pack-registry.py",
        "tools/nlc_pack_registry.py",
    ):
        if not (ROOT / rel).is_file():
            violations.append(f"missing {rel}")

    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate-hub-pack-registry.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("validate-hub-pack-registry.py must MET")

    status_path = ROOT / "integrity" / "uc-product-status.json"
    if status_path.is_file():
        data = json.loads(status_path.read_text(encoding="utf-8"))
        hub = data.get("hub_v02") or {}
        if hub.get("pack_registry") != "closed":
            violations.append("hub_v02.pack_registry must be closed")
        packs = data.get("packs_v02") or {}
        if packs.get("expansion_only"):
            violations.append("packs_v02.expansion_only must be empty after registry v1")

    install = ROOT / "tools" / "nlc-pack-install.py"
    if install.is_file() and "nlc_pack_registry" not in install.read_text(encoding="utf-8"):
        violations.append("nlc-pack-install.py must use nlc_pack_registry")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

