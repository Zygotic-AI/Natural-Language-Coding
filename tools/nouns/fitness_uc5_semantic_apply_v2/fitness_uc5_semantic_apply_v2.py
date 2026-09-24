"""UC5 v2 semantic rule apply product boundary (P2 / ADR 0007)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BOUNDARY_JSON = ROOT / "integrity" / "uc5-product-boundary.json"
STATUS = ROOT / "integrity" / "uc-product-status.json"


def run_assert(rel: str) -> bool:
    return (
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / rel)],
            cwd=str(ROOT),
            check=False,
        ).returncode
        == 0
    )


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not BOUNDARY_JSON.is_file():
        violations.append("missing integrity/uc5-product-boundary.json")
    else:
        data = json.loads(BOUNDARY_JSON.read_text(encoding="utf-8"))
        if data.get("remain_expansion"):
            violations.append("uc5-product-boundary remain_expansion must be empty")
    if STATUS.is_file():
        exp = (json.loads(STATUS.read_text(encoding="utf-8")).get("ucs") or {}).get(
            "UC5", {}
        ).get("expansion_only") or []
        if "semantic_apply_adr_0007" in exp:
            violations.append("UC5 expansion_only must not list semantic_apply_adr_0007")
    for script in (
        "assert-rule-semantic-apply-passes.py",
        "assert-rule-semantic-apply-fails.py",
        "assert-rule-emit-sync-passes.py",
        "assert-rule-coverage-passes.py",
    ):
        if not run_assert(script):
            violations.append(f"{script} must PASS")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0
