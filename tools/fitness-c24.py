#!/usr/bin/env python3
"""C24: classes A/B/D/E/F need Ratified-by: a human, not the agent.

missing-confirm      — product tree, no note
missing-ratification — class A/B/D/E/F, no `Ratified-by:` line
agent-ratified       — Ratified-by names the agent / AI / bot / confirmer

Class C → skip. Specimens without a note skip.
This is not a cryptographic signature. It is “the bot did not sign for you.”
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import markdown_plain  # noqa: E402
import product_tree  # noqa: E402

NOTES = ("PROPOSAL.md", "CONFIRM.md")
CLASS = re.compile(r"change\s*class\s*[:*\s]*([ABDEF])\b", re.I)
RATIFIED = re.compile(r"^Ratified-by:\s*(.*)$", re.I | re.M)
AGENT = re.compile(
    r"\b(agent|ai|bot|assistant|grok|confirmer|bbp-confirmer|claude|gpt|copilot)\b",
    re.I,
)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def scan_one(scan_root: Path) -> list[tuple[str, str]]:
    notes = [scan_root / n for n in NOTES if (scan_root / n).is_file()]
    if not notes:
        if product_tree.requires_confirm(scan_root):
            return [(rel(scan_root / "CONFIRM.md"), "missing-confirm")]
        return []
    missing = []
    for path in notes:
        text = markdown_plain.strip_links(path.read_text(errors="replace"))
        if CLASS.search(text) is None:
            continue
        m = RATIFIED.search(text)
        if m is None:
            missing.append((rel(path), "missing-ratification"))
            continue
        name = m.group(1).strip()
        if not name or AGENT.search(name):
            missing.append((rel(path), "agent-ratified"))
    return missing


def main() -> int:
    scan_roots = (
        [Path(p).resolve() for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else [ROOT]
    )
    seen: set[tuple[str, str]] = set()
    printed: list[tuple[str, str]] = []
    for scan_root in scan_roots:
        for item in scan_one(scan_root):
            if item in seen:
                continue
            seen.add(item)
            printed.append(item)
            path, kind = item
            print(f"VIOLATION {path} {kind}")
    if printed:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())
