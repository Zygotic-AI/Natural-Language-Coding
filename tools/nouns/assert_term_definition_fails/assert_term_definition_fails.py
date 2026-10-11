"""Landmine O11: term-definition plants must fail scan."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLANTS = ROOT / "tools" / "nouns" / "term_definition_bypass_fixtures" / "plants"
TERMS = ROOT / "docs" / "TERMS.md"

sys.path.insert(0, str(ROOT / "tools"))
from nouns.term_definition_ssot.term_definition_ssot import (  # noqa: E402
    load_term_names,
    scan_markdown,
)

PLANT_REL = {
    "gate-h3.md": "docs/plant-gate-h3.md",
    "gate-bold-colon.md": "docs/plant-gate-bold.md",
    "gate-table-row.md": "docs/plant-gate-table.md",
    "gate-h2.md": "docs/plant-gate-h2.md",
    "gate-em-dash.md": "docs/plant-gate-em.md",
    "lexicon-gate-bold.md": "integrity/LEXICON.md",
}


def main() -> int:
    terms = load_term_names(TERMS.read_text(encoding="utf-8"))
    for plant, rel in PLANT_REL.items():
        path = PLANTS / plant
        if not path.is_file():
            print(f"ASSERT:FAIL missing plant {plant}")
            return 1
        hits = scan_markdown(rel, path.read_text(encoding="utf-8"), terms)
        if not hits:
            print(f"ASSERT:FAIL plant {plant} must trigger term-definition scan for {rel}")
            return 1
    print("ASSERT:PASS term-definition landmine plants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
