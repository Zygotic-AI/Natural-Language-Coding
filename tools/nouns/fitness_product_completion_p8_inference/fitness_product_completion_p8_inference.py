#!/usr/bin/env python3
"""P8.4: full-nlc-audit inference record present + continuity verdict on product SSOT."""

from __future__ import annotations



import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECORD = ROOT / "integrity" / "full-nlc-audit-inference-record.json"


def git_short_head() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return (proc.stdout or "").strip()


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
        head = git_short_head()
        sha = str(data.get("audit_sha") or "")
        if head and sha and not (head.startswith(sha) or sha.startswith(head)):
            violations.append(f"audit_sha {sha} must match HEAD {head} until merge amends record")

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
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

