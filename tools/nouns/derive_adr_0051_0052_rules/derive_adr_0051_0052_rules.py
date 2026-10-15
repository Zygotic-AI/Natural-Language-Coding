#!/usr/bin/env python3
"""Derive normative rules from ADR 0051 and 0052. Usage: derive-adr-0051-0052-rules.py <repo> -> TSV id<TAB>file:line<TAB>text
Rule sources (ALL scanned):
 - table rows whose Layer is Policy|Standard|Rule|Codified constraint  (id = bold Id, or CC-<SG>)
 - numbered items under '## Rule against regress', '### Amendment', '## Decision'
 - bullets under '## Rejected'; the '**Gate-set member**' definition
 - any other line containing MUST/must/only/never/may not/required/to implement/step 2 (id = file:line)
Principle rows (quotations of other docs) are context, not rules."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import re
import sys
from pathlib import Path

KW = re.compile(r"\b(must|MUST|only|never|may not|required|to implement|step 2|NOT_MET|REFUSE)\b")


def derive_rules(root: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for adr, tag in (
        ("adrs/0051-hub-own-produce-principles.md", "0051"),
        ("adrs/0052-owner-openpgp-ratification-amends-0051.md", "0052"),
    ):
        lines = (root / adr).read_text().splitlines()
        sec, sg, seen = "", "", set()
        for i, l in enumerate(lines, 1):
            if l.startswith("#"):
                sec = l.strip("# ").strip()
                m = re.match(r"(SG\d)", sec)
                sg = m.group(1) if m else sg
                continue
            if l.startswith("|") and not l.startswith("|---"):
                cells = [c.strip() for c in l.strip("|").split("|")]
                if len(cells) == 3 and re.search(r"Policy|Standard|Rule|Codified", cells[0]):
                    m = re.search(r"\*\*([A-Z][A-Z0-9-]+)\*\*", cells[1])
                    rid = m.group(1) if m else f"CC-{sg}"
                    rows.append((f"{tag}:{rid}", f"{adr}:{i}", cells[2]))
                    seen.add(i)
                    continue
            m = re.match(r"^(\d+)\.\s+(.*)", l)
            if m and re.search(r"regress|Amendment|Decision", sec):
                key = "REGRESS" if "regress" in sec else ("DEC" if sec.startswith("Decision") else "AMEND-0047")
                rows.append((f"{tag}:{key}-{m.group(1)}", f"{adr}:{i}", m.group(2)))
                seen.add(i)
                continue
            if sec == "Rejected" and l.startswith("- "):
                rows.append((f"{tag}:REJ-{i}", f"{adr}:{i}", l[2:].strip()))
                continue
            if l.startswith("**Gate-set member**"):
                rows.append((f"{tag}:GATE-SET-DEF", f"{adr}:{i}", l.strip()))
                continue
            if i not in seen and KW.search(l) and not l.startswith("|") and not l.startswith("- **Kind"):
                rows.append((f"{tag}:L{i}", f"{adr}:{i}", l.strip()))
    return rows


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    for rid, loc, text in derive_rules(root):
        print(f"{rid}\t{loc}\t{text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
