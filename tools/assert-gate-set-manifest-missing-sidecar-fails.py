#!/usr/bin/env python3
"""Landmine: a missing gate-set sidecar must not fail the branch suite (ADR 0057)."""
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

    missing = [e for e in errors if "missing sidecar" in e or "Content-SHA256" in e]
    if missing:
        print(f"ASSERT:FAIL branch suite still requires manifest armor: {missing!r}")
        return 1
    print("ASSERT:PASS missing sidecar does not fail the branch suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
