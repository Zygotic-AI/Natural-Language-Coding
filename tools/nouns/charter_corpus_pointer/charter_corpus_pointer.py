"""Insert ADR 0024 corpus pointer into CHARTER.md §3 if missing."""

from __future__ import annotations

from pathlib import Path

BOUNDARY = "bba-emit"

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


def hub_charter(repo_root: Path) -> Path:
    return repo_root / "CHARTER.md"


def main(repo_root: Path | None = None) -> int:
    root = repo_root or Path(__file__).resolve().parents[3]
    charter = hub_charter(root)
    text = charter.read_text(encoding="utf-8")
    if NEEDLE in text:
        print("CHARTER.md already cites integrity/rule-corpus.json")
        return 0
    if OLD not in text:
        print("NEEDLE paragraph not found; refuse")
        return 2
    charter.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("CHARTER.md updated")
    return 0
