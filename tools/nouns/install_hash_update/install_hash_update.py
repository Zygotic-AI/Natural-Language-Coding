"""Regenerate integrity/nlc-install-hashes.json (maintainer)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402

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
    "tools/nlc.py",
    "tools/validate-knowledge-facts.py",
    "tools/release-audit.py",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_install_files(root: Path) -> dict[str, str] | None:
    """Return path → sha256, or None when a required path is missing."""
    files: dict[str, str] = {}
    for rel in GLOBS:
        path = root / rel
        if not path.is_file():
            print(f"missing {rel}", file=sys.stderr)
            return None
        files[rel.replace("\\", "/")] = sha256_file(path)
    for path in sorted((root / "tools").glob("nlc-*.py")):
        rel = path.relative_to(root).as_posix()
        files[rel] = sha256_file(path)
    skills = root / ".agents" / "skills"
    if skills.is_dir():
        for path in sorted(skills.rglob("SKILL.md")):
            rel = path.relative_to(root).as_posix()
            files[rel] = sha256_file(path)
    return files


def write_install_hashes(root: Path, out: Path | None = None) -> bool | None:
    """Write the install ledger only when a recorded hash changed.

    Returns True if written, False if left untouched, None if a required file is missing.
    """
    files = collect_install_files(root)
    if files is None:
        return None
    dest = out if out is not None else root / "integrity" / "nlc-install-hashes.json"
    if dest.is_file():
        try:
            old = json.loads(dest.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            old = None
        if isinstance(old, dict) and old.get("version") == 1 and old.get("files") == files:
            return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps({"version": 1, "files": files}, indent=2) + "\n",
        encoding="utf-8",
    )
    return True


def main() -> int:
    hub_tool()
    wrote = write_install_hashes(ROOT, OUT)
    if wrote is None:
        return 1
    if wrote:
        count = len(json.loads(OUT.read_text(encoding="utf-8"))["files"])
        print(f"wrote {OUT.relative_to(ROOT)} ({count} files)")
    else:
        count = len(json.loads(OUT.read_text(encoding="utf-8"))["files"])
        print(f"unchanged {OUT.relative_to(ROOT)} ({count} files)")
    return 0


