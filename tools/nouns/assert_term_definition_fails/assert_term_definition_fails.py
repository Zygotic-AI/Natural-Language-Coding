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

PLANT_REL: dict[str, str] = {
    "gate-h3.md": "docs/plant-gate-h3.md",
    "gate-bold-colon.md": "docs/plant-gate-bold.md",
    "gate-bold-colon-in.md": "docs/plant-gate-bold-in.md",
    "gate-table-row.md": "docs/plant-gate-table.md",
    "gate-table-plain.md": "docs/plant-gate-table-plain.md",
    "gate-h2.md": "docs/plant-gate-h2.md",
    "gate-h4.md": "docs/plant-gate-h4.md",
    "gate-em-dash.md": "docs/plant-gate-em.md",
    "gate-bullet-em.md": "docs/plant-gate-bullet-em.md",
    "gate-line-colon.md": "docs/plant-gate-line-colon.md",
    "gate-bold-hyphen.md": "docs/plant-gate-bold-hyphen.md",
    "gate-italic-colon.md": "docs/plant-gate-italic-colon.md",
    "lexicon-gate-bold.md": "integrity/LEXICON.md",
    "charter-gate-soft-term.md": "CHARTER.md",
    "gate-table-soft-row.md": "integrity/GATE.md",
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
