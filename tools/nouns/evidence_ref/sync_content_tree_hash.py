"""Converge integrity/hub-content-tree-hash.txt (tree hash excluding that file)."""

from __future__ import annotations

import sys
from pathlib import Path

from nouns.evidence_ref.evidence_ref import worktree_tree_hash_excluding

ROOT = Path(__file__).resolve().parents[3]
HASH_REL = "integrity/hub-content-tree-hash.txt"
HASH_PATH = ROOT / HASH_REL


def sync_content_tree_hash(root: Path | None = None) -> str:
    """
    Write hub-content-tree-hash.txt to the worktree tree hash excluding itself.

    Returns the converged 40-char tree hash.
    """
    base = root or ROOT
    path = base / HASH_REL
    h = "0" * 40
    for _ in range(64):
        path.write_text(h + "\n", encoding="utf-8")
        h_new = worktree_tree_hash_excluding(base, {HASH_REL})
        if not h_new:
            raise RuntimeError("cannot compute content tree hash")
        if h_new == h:
            return h
        h = h_new
    raise RuntimeError("hub-content-tree-hash.txt did not converge")


def read_content_tree_hash(root: Path | None = None) -> str:
    """Return recorded hub content tree hash or empty string."""
    base = root or ROOT
    path = base / HASH_REL
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8").strip().lower()


def verify_content_tree_hash(root: Path | None = None) -> tuple[bool, str, str]:
    """Return (ok, recorded, expected) for the content-tree fingerprint."""
    base = root or ROOT
    recorded = read_content_tree_hash(base)
    expected = worktree_tree_hash_excluding(base, {HASH_REL}).lower()
    if not recorded or not expected:
        return False, recorded, expected
    return recorded == expected, recorded, expected


def main() -> int:
    try:
        h = sync_content_tree_hash()
    except RuntimeError as exc:
        print(f"SYNC:REFUSE {exc}", file=sys.stderr)
        return 2
    print(f"SYNC:MET tree={h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
