#!/usr/bin/env python3
"""Hub release prepare receipt (ADR 0039 / tag gate)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "integrity" / "hub-release-record.json"


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def git_show_json(commit: str, rel_path: str) -> dict | None:
    proc = _git("show", f"{commit}:{rel_path}")
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def read_version_at(commit: str) -> str | None:
    proc = _git("show", f"{commit}:integrity/nlc-version.json")
    if proc.returncode != 0:
        return None
    try:
        return str(json.loads(proc.stdout)["version"]).strip()
    except (json.JSONDecodeError, KeyError):
        return None


def write_record(version: str, release_branch: str, prepare_head: str) -> Path:
    payload = {
        "schema": 1,
        "version": version,
        "release_branch": release_branch,
        "prepare_head": prepare_head,
    }
    RECORD_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return RECORD_PATH


def validate_record(data: dict, version: str, release_branch: str) -> list[str]:
    bad: list[str] = []
    if data.get("schema") != 1:
        bad.append("hub-release-record schema must be 1")
    if data.get("version") != version:
        bad.append("hub-release-record version mismatch")
    if data.get("release_branch") != release_branch:
        bad.append("hub-release-record release_branch mismatch")
    if not str(data.get("prepare_head", "")).strip():
        bad.append("hub-release-record missing prepare_head")
    return bad


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_requirements import hub_tool  # noqa: E402

    hub_tool()
    parser = argparse.ArgumentParser(description="Write hub-release-record.json after prepare")
    parser.add_argument("--version", required=True)
    parser.add_argument("--branch", required=True, help="release/vX.Y.Z")
    parser.add_argument("--prepare-head", default=None)
    args = parser.parse_args()

    head = args.prepare_head or _git("rev-parse", "HEAD").stdout.strip()
    path = write_record(args.version, args.branch, head)
    print(f"RELEASE_RECORD:WROTE {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
