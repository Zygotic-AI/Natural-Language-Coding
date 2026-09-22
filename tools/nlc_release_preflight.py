#!/usr/bin/env python3
"""Hub ./release preflight — fail early (ADR 0022, ADR 0013)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from nlc_release_tags import last_shipped_tag, last_shipped_version, parse_semver, tag_version

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402
VERSION_PATH = ROOT / "integrity" / "nlc-version.json"


def read_json_version() -> str:
    data = json.loads(VERSION_PATH.read_text(encoding="utf-8"))
    return str(data["version"]).strip()


def current_branch() -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return (proc.stdout or "").strip() or "HEAD"


def check_version_tag_coherence(
    branch: str,
    json_ver: str,
    shipped_ver: str | None,
) -> tuple[bool, list[str]]:
    lines: list[str] = []
    if shipped_ver is None:
        return True, lines

    if parse_semver(json_ver) < parse_semver(shipped_ver):
        lines.append(
            f"integrity/nlc-version.json ({json_ver}) is behind last shipped tag (v{shipped_ver})"
        )
        return False, lines

    if branch == "main" and json_ver != shipped_ver:
        lines.append(
            f"on main: nlc-version.json ({json_ver}) must match last shipped tag (v{shipped_ver})"
        )
        lines.append(
            "  bump version only on release/v* (./release), not on main between tags"
        )
        lines.append(
            f"  fix: git checkout {VERSION_PATH.relative_to(ROOT)} to reset, or merge a release branch"
        )
        return False, lines

    if branch.startswith("release/v") and parse_semver(json_ver) < parse_semver(shipped_ver):
        lines.append("release branch version is behind last shipped tag")
        return False, lines

    return True, lines


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Hub release preflight")
    parser.add_argument("--check", action="store_true", help="Exit 1 if release cannot start")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="Git ref for tag ancestry")
    args = parser.parse_args()

    if not args.check:
        parser.print_help()
        return 2

    json_ver = read_json_version()
    branch = current_branch()
    shipped_tag = last_shipped_tag(args.to_ref)
    shipped_ver = tag_version(shipped_tag) if shipped_tag else None

    print(f"RELEASE_PREFLIGHT: last_shipped_tag={shipped_tag or 'none'}")
    print(f"RELEASE_PREFLIGHT: integrity_version={json_ver}")
    print(f"RELEASE_PREFLIGHT: branch={branch}")

    ok, problems = check_version_tag_coherence(branch, json_ver, shipped_ver)
    if ok and shipped_ver and parse_semver(json_ver) > parse_semver(shipped_ver):
        from nlc_migration_catalog import migration_steps_blockers

        problems.extend(migration_steps_blockers(ROOT, shipped_ver, json_ver))
        ok = not problems
    if ok:
        from nlc_migration_catalog import migration_catalog_blockers

        problems.extend(migration_catalog_blockers(ROOT))
        ok = not problems
    if ok:
        print("RELEASE_PREFLIGHT:MET")
        return 0

    print("RELEASE_PREFLIGHT:NOT_MET", file=sys.stderr)
    for line in problems:
        print(f"  {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
