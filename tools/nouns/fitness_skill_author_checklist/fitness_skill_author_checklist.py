"""Checklist SSOT + landmine + CLI stay wired (does not require live hub skills MET)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECKLIST = ROOT / "integrity" / "skill-author-checklist.json"
CLI = ROOT / "tools" / "nlc-skill-author-check.py"
LANDMINE = ROOT / "tools" / "assert-skill-author-check-fails.py"
NOUN = ROOT / "tools" / "nouns" / "skill_author_check" / "skill_author_check.py"
REQUIRED_IDS = ("frontmatter-yaml", "in-skill-links")


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    for path, label in (
        (CHECKLIST, "skill-author-checklist.json"),
        (CLI, "nlc-skill-author-check.py"),
        (LANDMINE, "assert-skill-author-check-fails.py"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")
    if CHECKLIST.is_file():
        data = json.loads(CHECKLIST.read_text(encoding="utf-8"))
        ids = [c.get("id") for c in (data.get("checks") or []) if isinstance(c, dict)]
        for cid in REQUIRED_IDS:
            if cid not in ids:
                violations.append(f"checklist missing {cid}")
    if LANDMINE.is_file():
        proc = subprocess.run(
            [sys.executable, str(LANDMINE)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            violations.append("landmine assert-skill-author-check-fails must PASS")
    if NOUN.is_file():
        src = NOUN.read_text(encoding="utf-8")
        if re.search(r"^\s*import\s+yaml\b|^\s*from\s+yaml\b", src, re.M):
            violations.append("skill_author_check must not import PyYAML (piped install has no yaml)")
    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
