#!/usr/bin/env python3
"""UC requirement packs v0.2: ingest source → candidate ADRs/rules (human ratifies)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from nlc_human_gap import emit_gap
from nlc_requirements import hub_tool

HEADING = re.compile(r"^#{1,3}\s+(.+)$", re.M)
BULLET = re.compile(r"^\s*[-*]\s+(.+)$", re.M)


def candidates_from_text(text: str, source: str) -> dict:
    title = "Imported requirement"
    for m in HEADING.finditer(text):
        title = m.group(1).strip()
        break
    reqs: list[str] = []
    for m in BULLET.finditer(text):
        line = m.group(1).strip()
        if len(line) > 8:
            reqs.append(line[:240])
    if not reqs:
        reqs = [title]
    return {
        "schema": 1,
        "source": source,
        "candidate_adrs": [
            {
                "title": title,
                "status": "Proposed",
                "requirements": reqs[:20],
            }
        ],
        "candidate_rules": [],
        "ratify": "Move accepted rows into adrs/ and rules/adopted.json via /interview",
    }


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Requirement pack ingest (v0.2)")
    parser.add_argument("source", type=Path, nargs="?", default=None)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    if args.source is None:
        return emit_gap(
            "Pack ingest needs a source markdown file.",
            ask="Point at policy/requirements markdown; human ratifies output.",
            examples=[
                "./nlc maintainer pack-ingest ./policy/pci-notes.md",
                "See .agents/skills/requirement-pack-ingest/SKILL.md",
            ],
            machine="PACK_INGEST:NOT_MET",
        )
    src = args.source.resolve()
    if not src.is_file():
        return emit_gap(
            "Source file missing.",
            missing=[str(src)],
            machine="PACK_INGEST:NOT_MET",
        )
    text = src.read_text(encoding="utf-8", errors="replace")
    payload = candidates_from_text(text, str(src.relative_to(root) if src.is_relative_to(root) else src))
    nlc = root / ".nlc"
    nlc.mkdir(parents=True, exist_ok=True)
    out = nlc / "pack-ingest-candidates.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"PACK_INGEST:MET candidates={out.relative_to(root)}")
    print("PACK_INGEST: ratify via /interview before export")
    return 0


if __name__ == "__main__":
    sys.exit(main())
