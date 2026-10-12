#!/usr/bin/env python3
"""Regenerate integrity/gate-set-baseline.manifest.sha256 from gate-set paths (no ratification)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, manifest_bytes


def main() -> int:
    out = ROOT / MANIFEST_REL
    body = manifest_bytes(ROOT)
    out.write_bytes(body)
    print(f"wrote {MANIFEST_REL} ({len(body)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
