#!/usr/bin/env python3
"""Validate integrity/hub-pack-registry.json (ADR 0041 v1)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "integrity" / "hub-pack-registry.json"

ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")


def validate(data: dict) -> list[str]:
    bad: list[str] = []
    if data.get("schema") != 1:
        bad.append("schema must be 1")
    if data.get("ssot") != "integrity/hub-pack-registry.json":
        bad.append("ssot must be integrity/hub-pack-registry.json")
    policy = data.get("policy") or {}
    if not str(policy.get("trust_model", "")).strip():
        bad.append("policy.trust_model required")
    if not str(policy.get("scope", "")).strip():
        bad.append("policy.scope required")
    packs = data.get("packs")
    if not isinstance(packs, list):
        bad.append("packs must be array")
        return bad
    seen: set[str] = set()
    for i, row in enumerate(packs):
        if not isinstance(row, dict):
            bad.append(f"packs[{i}] must be object")
            continue
        pid = str(row.get("id", ""))
        if not ID_RE.match(pid):
            bad.append(f"packs[{i}].id invalid")
        if pid in seen:
            bad.append(f"duplicate pack id {pid}")
        seen.add(pid)
        if not str(row.get("name", "")).strip():
            bad.append(f"packs[{i}].name required")
        ver = str(row.get("version", ""))
        if not VER_RE.match(ver):
            bad.append(f"packs[{i}].version must be semver")
        sha = row.get("manifest_sha256")
        if sha is not None and not SHA_RE.match(str(sha)):
            bad.append(f"packs[{i}].manifest_sha256 must be 64 hex chars")
    return bad


def main() -> int:
    _ = sys.argv[1:]
    if not REGISTRY.is_file():
        print("HUB_PACK_REGISTRY:NOT_MET missing file", file=sys.stderr)
        return 1
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("HUB_PACK_REGISTRY:NOT_MET invalid json", file=sys.stderr)
        return 1
    bad = validate(data)
    if bad:
        for msg in bad:
            print(f"HUB_PACK_REGISTRY:NOT_MET {msg}", file=sys.stderr)
        return 1
    print("HUB_PACK_REGISTRY:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
