#!/usr/bin/env python3
"""X4 pilot: RuleReceipt noun package exists; CLI adapters import it."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOUN = ROOT / "tools" / "nouns" / "rule_receipt"
REQUIRED = (
    NOUN / "rule_receipt.py",
    NOUN / "schemas" / "verbs.schema.json",
    NOUN / "adjectives.txt",
    NOUN / "fields.txt",
    NOUN / "README.md",
)
ADAPTERS = (
    ROOT / "tools" / "nlc_rule_marker.py",
    ROOT / "tools" / "nlc_rule_coverage.py",
    ROOT / "tools" / "nlc_rule_runner.py",
    ROOT / "tools" / "nlc_rule_emit.py",
)
IMPORT_HINT = "nouns.rule_receipt"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path in REQUIRED:
        if not path.is_file():
            violations.append(f"missing {path.relative_to(ROOT)}")
    noun_py = NOUN / "rule_receipt.py"
    if noun_py.is_file():
        tree = ast.parse(noun_py.read_text(encoding="utf-8"), filename=str(noun_py))
        names = {
            n.name
            for n in tree.body
            if isinstance(n, ast.ClassDef)
        }
        if "RuleReceipt" not in names:
            violations.append("tools/nouns/rule_receipt/rule_receipt.py missing class RuleReceipt")
    for path in ADAPTERS:
        if not path.is_file():
            violations.append(f"missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if IMPORT_HINT not in text:
            violations.append(f"{path.relative_to(ROOT)} must import {IMPORT_HINT}")
    for row in violations:
        print(f"VIOLATION {row}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
