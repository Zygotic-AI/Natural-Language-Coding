#!/usr/bin/env python3
"""Insert ADR 0024 corpus pointer into CHARTER.md §3 if missing."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARTER = ROOT / "CHARTER.md"
NEEDLE = "integrity/rule-corpus.json"
OLD = (
    "An **R** can stand without a matching **C**. "
    "A **C** usually restates an **R** as something you can tick on *this* change.\n\n---"
)
NEW = (
    "An **R** can stand without a matching **C**. "
    "A **C** usually restates an **R** as something you can tick on *this* change.\n\n"
    "Corpus tags for every published **R** / **C** / **P** id live in "
    "[`integrity/rule-corpus.json`](integrity/rule-corpus.json) "
    "([ADR 0024](adrs/0024-nlc-factory-spine.md)): "
    "`bba` = emit shape, `nlc` = factory process.\n\n---"
)


def main() -> int:
    text = CHARTER.read_text(encoding="utf-8")
    if NEEDLE in text:
        print("CHARTER.md already cites integrity/rule-corpus.json")
        return 0
    if OLD not in text:
        print("NEEDLE paragraph not found; refuse")
        return 2
    CHARTER.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("CHARTER.md updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
