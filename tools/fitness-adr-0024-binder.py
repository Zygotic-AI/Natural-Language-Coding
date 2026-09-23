#!/usr/bin/env python3
"""ADR 0024 v1: spine files, corpus map covers published R/C/P, rules listed."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "integrity" / "rule-corpus.json"
RULES = ROOT / "rules" / "nlc-0024.json"
ADR = ROOT / "adrs" / "0024-nlc-factory-spine.md"
README = ROOT / "adrs" / "README.md"
CHARTER = ROOT / "CHARTER.md"
ENFORCEMENT = ROOT / "docs" / "ADR-ENFORCEMENT.md"
REQUIRED_RULES = (
    "NLC-0024-01",
    "NLC-0024-02",
    "NLC-0024-03",
    "NLC-0024-04",
    "NLC-0024-05",
    "NLC-0024-06",
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path, label in (
        (ADR, "adrs/0024-nlc-factory-spine.md"),
        (CORPUS, "integrity/rule-corpus.json"),
        (RULES, "rules/nlc-0024.json"),
        (README, "adrs/README.md"),
        (CHARTER, "CHARTER.md"),
        (ENFORCEMENT, "docs/ADR-ENFORCEMENT.md"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")

    adr_text = ADR.read_text(encoding="utf-8", errors="replace") if ADR.is_file() else ""
    charter = CHARTER.read_text(encoding="utf-8", errors="replace") if CHARTER.is_file() else ""
    if adr_text:
        if not re.search(r"Status:\s*Accepted", adr_text):
            violations.append("ADR 0024 must be Accepted")
        if "Corpus: nlc" not in adr_text:
            violations.append("ADR 0024 must declare Corpus: nlc")
    if "rule-corpus.json" not in adr_text and "rule-corpus.json" not in charter:
        violations.append("ADR 0024 or CHARTER must point at integrity/rule-corpus.json")

    if README.is_file() and "0024-nlc-factory-spine.md" not in README.read_text(
        encoding="utf-8", errors="replace"
    ):
        violations.append("adrs/README.md must index 0024")

    if ENFORCEMENT.is_file() and "| 0024 |" not in ENFORCEMENT.read_text(
        encoding="utf-8", errors="replace"
    ):
        violations.append("ADR-ENFORCEMENT must list 0024")

    expected = {f"R{n}" for n in range(1, 34)} | {f"C{n}" for n in range(1, 27)}
    expected |= {f"P{n}" for n in range(1, 8)}
    if CORPUS.is_file():
        try:
            data = json.loads(CORPUS.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(f"rule-corpus.json invalid: {exc}")
            data = {}
        ids = data.get("ids") if isinstance(data, dict) else None
        if not isinstance(ids, dict):
            violations.append("rule-corpus.json missing ids map")
        else:
            for key, val in ids.items():
                if val not in ("nlc", "bba"):
                    violations.append(f"{key} corpus must be nlc|bba, got {val!r}")
            missing = sorted(expected - set(ids), key=lambda x: (x[0], int(x[1:])))
            if missing:
                violations.append("corpus map missing " + ",".join(missing))

    if RULES.is_file():
        try:
            rules_doc = json.loads(RULES.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(f"nlc-0024.json invalid: {exc}")
            rules_doc = {}
        found = {
            row.get("id") for row in rules_doc.get("rules", []) if isinstance(row, dict)
        }
        for rid in REQUIRED_RULES:
            if rid not in found:
                violations.append(f"missing rule {rid}")
            else:
                row = next(r for r in rules_doc["rules"] if r.get("id") == rid)
                if not row.get("condition") or not row.get("obligation") or not row.get("gate"):
                    violations.append(f"{rid} needs condition, obligation, gate")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
