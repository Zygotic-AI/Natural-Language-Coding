"""Landmine: skill-author checklist must NOT_MET on the broken fixture."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "tools" / "nlc-skill-author-check.py"
SPECIMEN = ROOT / "examples" / "skill-author-check-landmine" / ".agents" / "skills"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(CLI), "--root", str(SPECIMEN)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "SKILL_AUTHOR:NOT_MET" not in out:
        print("ASSERT:FAIL landmine skill tree must SKILL_AUTHOR:NOT_MET")
        print(out[-1200:])
        return 1
    if "frontmatter-yaml" not in out:
        print("ASSERT:FAIL landmine must report frontmatter-yaml")
        return 1
    if "in-skill-links" not in out:
        print("ASSERT:FAIL landmine must report in-skill-links")
        return 1
    print("ASSERT:PASS skill-author checklist refuses the landmine")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
