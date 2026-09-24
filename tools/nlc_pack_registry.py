#!/usr/bin/env python3
"""Hub curated pack registry helpers (ADR 0041)."""

from __future__ import annotations

import json
from pathlib import Path

REGISTRY_REL = Path("integrity") / "hub-pack-registry.json"


def load_registry(hub_root: Path) -> dict | None:
    path = hub_root / REGISTRY_REL
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def registry_allows_manifest(hub_root: Path, manifest: dict) -> tuple[bool, str]:
    """When registry lists packs, install must match name+version; empty list allows all."""
    data = load_registry(hub_root)
    if data is None:
        return False, "missing integrity/hub-pack-registry.json"
    packs = data.get("packs") or []
    if not packs:
        return True, "registry empty (no constraint)"
    name = str(manifest.get("name", "")).strip()
    version = str(manifest.get("version", "")).strip()
    for row in packs:
        if row.get("name") == name and row.get("version") == version:
            return True, "listed in hub-pack-registry"
    return False, f"pack {name}@{version} not in hub-pack-registry.json"
