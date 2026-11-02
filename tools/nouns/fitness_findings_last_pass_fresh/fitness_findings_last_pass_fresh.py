#!/usr/bin/env python3
"""FINDINGS last_pass_tree_hash must match current worktree tree (F2, ADR 0050)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FINDINGS = ROOT / "FINDINGS.md"

sys.path.insert(0, str(ROOT / "tools"))
from nouns.evidence_ref.sync_content_tree_hash import (  # noqa: E402
    read_content_tree_hash,
    verify_content_tree_hash,
)


def main() -> int:
    _ = sys.argv[1:]
    if not FINDINGS.is_file():
        print("VIOLATION missing FINDINGS.md")
        print("RESULT:NOT_MET")
        return 1

    text = FINDINGS.read_text(encoding="utf-8", errors="replace")
    if "hub-content-tree-hash.txt" not in text:
        print("VIOLATION FINDINGS.md must reference integrity/hub-content-tree-hash.txt (F2)")
        print("RESULT:NOT_MET")
        return 1

    if not read_content_tree_hash(ROOT):
        print("VIOLATION missing integrity/hub-content-tree-hash.txt")
        print("RESULT:NOT_MET")
        return 1

    ok, recorded, expected = verify_content_tree_hash(ROOT)
    if not expected:
        print("VIOLATION cannot compute content tree hash")
        print("RESULT:REFUSE")
        return 2
    if not ok:
        print(f"VIOLATION hub-content-tree-hash {recorded} != content digest {expected}")
        print(
            "Reproduce: python3 tools/sync-hub-content-tree-hash.py  "
            "(commit integrity/hub-content-tree-hash.txt when content changed)",
            file=sys.stderr,
        )
        print("Reproduce: ./nlc gate hub-content-tree-fresh --tree .", file=sys.stderr)
        print("RESULT:NOT_MET")
        return 1

    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())


BOUNDARY = "bba-emit"
