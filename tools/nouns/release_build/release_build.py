"""Build nlc-X.Y.Z.tar.gz for GitHub Releases (maintainer)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from nlc_distribution import normalize_version, read_hub_version  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402

EXCLUDE_DIRS = {".git", ".github", "dist", "__pycache__", ".venv", "node_modules"}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    return False


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Build release tarball")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--version", default=None, help="Override version (default integrity/nlc-version.json)")
    args = parser.parse_args()

    version = normalize_version(args.version or read_hub_version(ROOT))
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"nlc-{version}.tar.gz"

    with tarfile.open(archive, "w:gz") as tf:
        for path in sorted(ROOT.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(ROOT)
            if should_skip(rel):
                continue
            tf.add(path, arcname=str(rel))

    print(f"RELEASE_BUILD:MET path={archive} version={version}")
    return 0


