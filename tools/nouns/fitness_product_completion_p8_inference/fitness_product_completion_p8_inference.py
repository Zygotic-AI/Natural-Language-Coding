#!/usr/bin/env python3
"""P8.4: full-nlc-audit inference record present + continuity verdict on product SSOT."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECORD = ROOT / "integrity" / "full-nlc-audit-inference-record.json"

sys.path.insert(0, str(ROOT / "tools"))
from nouns.evidence_ref.sync_content_tree_hash import verify_content_tree_hash  # noqa: E402


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not RECORD.is_file():
        violations.append("missing full-nlc-audit-inference-record.json")
    else:
        data = json.loads(RECORD.read_text(encoding="utf-8"))
        verdict = str(data.get("continuity_verdict") or "")
        if not verdict.startswith("PASS"):
            violations.append(f"continuity_verdict must be PASS* got {verdict!r}")
        blockers = data.get("p0_p1_product_blockers")
        if blockers is None or list(blockers):
            violations.append("p0_p1_product_blockers must be empty list")
        if data.get("machine_verdict") != "FULL_NLC_AUDIT:MET":
            violations.append("machine_verdict must be FULL_NLC_AUDIT:MET")
        ok, recorded, expected = verify_content_tree_hash(ROOT)
        if not expected:
            violations.append("cannot compute content tree hash (REFUSE)")
        elif not recorded:
            violations.append("missing integrity/hub-content-tree-hash.txt (ADR 0050)")
        elif not ok:
            violations.append(
                f"hub-content-tree-hash {recorded} must match content tree {expected}"
            )
        if data.get("audit_tree_hash"):
            violations.append("audit_tree_hash field removed; use hub-content-tree-hash.txt")
        if not data.get("content_tree_hash_ref"):
            violations.append("content_tree_hash_ref must point at hub-content-tree-hash.txt")

    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "fitness-use-cases-expansion-sync.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("fitness-use-cases-expansion-sync.py must MET")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        if any("REFUSE" in v for v in violations):
            print("RESULT:REFUSE")
            return 2
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())


BOUNDARY = "bba-emit"
