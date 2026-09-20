#!/usr/bin/env python3
"""Regenerate integrity/nlc-install-hashes.json (maintainer)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "integrity" / "nlc-install-hashes.json"

GLOBS = [
    "scripts/install.sh",
    "scripts/install.ps1",
    "CHARTER.md",
    "tools/ci_fitness.py",
    "tools/ci-fitness.ps1",
    "tools/nlc_requirements.py",
    "tools/nlc-install-verify.py",
    "tools/nlc-before-generate.py",
    "tools/load-knowledge-domain.py",
    "tools/nlc-init.py",
    "tools/validate-knowledge-facts.py",
    "tools/release-audit.py",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    files: dict[str, str] = {}
    for rel in GLOBS:
        path = ROOT / rel
        if not path.is_file():
            print(f"missing {rel}", file=sys.stderr)
            return 1
        files[rel.replace("\\", "/")] = sha256_file(path)
    for path in sorted((ROOT / "tools").glob("nlc-*.py")):
        rel = path.relative_to(ROOT).as_posix()
        files[rel] = sha256_file(path)
    for path in sorted((ROOT / ".agents" / "skills").rglob("SKILL.md")):
        rel = path.relative_to(ROOT).as_posix()
        files[rel] = sha256_file(path)
    payload = {"version": 1, "files": files}
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
