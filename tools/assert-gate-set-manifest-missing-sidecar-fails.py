#!/usr/bin/env python3
"""Landmine: unsigned gate-set manifest must NOT_MET with missing sidecar."""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.gate_set_manifest.gate_set_manifest import (  # noqa: E402
    MANIFEST_REL,
    gate_set_manifest_errors,
)
from nouns.owner_sidecar.owner_sidecar import sidecar_path_for_document  # noqa: E402


def main() -> int:
    asc_rel = sidecar_path_for_document(MANIFEST_REL)
    asc_path = ROOT / asc_rel
    if asc_path.is_file():
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp) / "tree"
            copy_root.mkdir()
            # Minimal tree: manifest only; sidecar explicitly absent.
            (copy_root / "integrity").mkdir(parents=True)
            shutil.copy2(ROOT / MANIFEST_REL, copy_root / MANIFEST_REL)
            errors = gate_set_manifest_errors(copy_root)
    else:
        errors = gate_set_manifest_errors(ROOT)

    if not errors:
        print("ASSERT:FAIL expected NOT_MET for missing gate-set manifest sidecar")
        return 1
    missing = [e for e in errors if "missing sidecar" in e]
    if not missing:
        print(f"ASSERT:FAIL expected missing sidecar in violations, got {errors!r}")
        return 1
    print(f"ASSERT:PASS missing sidecar yields NOT_MET ({missing[0]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
