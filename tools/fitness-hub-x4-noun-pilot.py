#!/usr/bin/env python3
"""X4 noun pilots: RuleReceipt + GateLedger packages exist; CLI adapters import them."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PILOTS = (
    {
        "dir": ROOT / "tools" / "nouns" / "rule_receipt",
        "class": "RuleReceipt",
        "module_file": "rule_receipt.py",
        "import_hint": "nouns.rule_receipt",
        "adapters": (
            "nlc_rule_marker.py",
            "nlc_rule_coverage.py",
            "nlc_rule_runner.py",
            "nlc_rule_emit.py",
        ),
        "required_extra": (
            "schemas/verbs.schema.json",
            "adjectives.txt",
            "fields.txt",
            "README.md",
        ),
    },
    {
        "dir": ROOT / "tools" / "nouns" / "gate_ledger",
        "class": "GateLedger",
        "module_file": "gate_ledger.py",
        "import_hint": "nouns.gate_ledger",
        "adapters": (
            "nlc_gate_record.py",
            "nlc_gate_scope.py",
        ),
        "required_extra": (
            "schemas/verbs.schema.json",
            "adjectives.txt",
            "fields.txt",
            "README.md",
        ),
    },
)


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for pilot in PILOTS:
        noun_dir: Path = pilot["dir"]
        mod = noun_dir / pilot["module_file"]
        if not mod.is_file():
            violations.append(f"missing {mod.relative_to(ROOT)}")
            continue
        for extra in pilot["required_extra"]:
            path = noun_dir / extra
            if not path.is_file():
                violations.append(f"missing {path.relative_to(ROOT)}")
        tree = ast.parse(mod.read_text(encoding="utf-8"), filename=str(mod))
        names = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
        if pilot["class"] not in names:
            violations.append(
                f"{mod.relative_to(ROOT)} missing class {pilot['class']}"
            )
        for name in pilot["adapters"]:
            path = ROOT / "tools" / name
            if not path.is_file():
                violations.append(f"missing {path.relative_to(ROOT)}")
                continue
            text = path.read_text(encoding="utf-8")
            if pilot["import_hint"] not in text:
                violations.append(
                    f"{path.relative_to(ROOT)} must import {pilot['import_hint']}"
                )
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
