#!/usr/bin/env python3
"""Rewrite the derived release files from one command (ADR 0057)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.checker_digest.checker_digest import DIGEST_REL, write_digest  # noqa: E402
from nouns.evidence_ref.sync_content_tree_hash import sync_content_tree_hash  # noqa: E402
from nouns.gate_set_manifest.gate_set_manifest import MANIFEST_REL, manifest_bytes  # noqa: E402
from nouns.install_hash_update.install_hash_update import write_install_hashes  # noqa: E402
from nouns.mandated_paths.mandated_paths import write_snapshot as write_mandated  # noqa: E402
from nouns.self_ref_set.self_ref_set import write_snapshot as write_self_ref  # noqa: E402


def main() -> int:
    # Order: snapshots the gate-set manifest hashes, then the manifest,
    # then the content-tree digest (excluded from the gate set). The checker
    # digest does not list those generated files, so it is written before the
    # manifest and is not rewritten after.
    print(f"wrote {write_mandated(ROOT).relative_to(ROOT)}")
    print(f"wrote {write_self_ref(ROOT).relative_to(ROOT)}")
    wrote = write_install_hashes(ROOT)
    print(f"install hashes wrote={wrote}")
    write_digest(ROOT)
    print(f"wrote {DIGEST_REL}")
    manifest = ROOT / MANIFEST_REL
    manifest.write_bytes(manifest_bytes(ROOT))
    print(f"wrote {MANIFEST_REL}")
    print(f"content tree {sync_content_tree_hash(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
