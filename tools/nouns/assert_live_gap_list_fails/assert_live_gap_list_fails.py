"""Landmine O10: gap-list plants must trigger scan_markdown violations."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLANTS = ROOT / "tools" / "nouns" / "live_gap_list_bypass_fixtures" / "plants"

sys.path.insert(0, str(ROOT / "tools"))
from nouns.live_gap_list_ssot.live_gap_list_ssot import scan_markdown  # noqa: E402

PLANT_REL: dict[str, str] = {
    "backlog-gap-table.md": "docs/BACKLOG.md",
    "use-cases-needed-section.md": "docs/USE-CASES.md",
    "jobs-blocked-row.md": "docs/JOBS-TO-BE-DONE.md",
    "asterisk-task.md": "docs/plant-asterisk-task.md",
    "numbered-task.md": "docs/plant-numbered-task.md",
    "still-open-section.md": "docs/plant-still-open.md",
    "charter-gate-soft.md": "CHARTER.md",
}


def main() -> int:
    if not PLANTS.is_dir():
        print("ASSERT:FAIL missing live_gap_list_bypass_fixtures/plants")
        return 1
    for plant_name, rel in PLANT_REL.items():
        path = PLANTS / plant_name
        if not path.is_file():
            print(f"ASSERT:FAIL missing plant {plant_name}")
            return 1
        text = path.read_text(encoding="utf-8")
        hits = scan_markdown(rel, text)
        if not hits:
            print(f"ASSERT:FAIL plant {plant_name} must trigger gap-list violations for {rel}")
            return 1
    if scan_markdown("FINDINGS.md", (ROOT / "FINDINGS.md").read_text(encoding="utf-8")):
        print("ASSERT:FAIL FINDINGS.md must not trip gap-list scan")
        return 1
    print("ASSERT:PASS live gap list landmine plants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
