#!/usr/bin/env python3
"""Hub release prepare receipt (ADR 0039 / tag gate)."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECORD_PATH = ROOT / "integrity" / "hub-release-record.json"

sys.path.insert(0, str(ROOT / "tools"))
from nouns.evidence_ref.sync_content_tree_hash import sync_content_tree_hash  # noqa: E402

CONTENT_TREE_REF = "integrity/hub-content-tree-hash.txt"


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )


def git_show_json(commit: str, rel_path: str, *, repo_root: Path | None = None) -> dict | None:
    root = repo_root or ROOT
    proc = _git(root, "show", f"{commit}:{rel_path}")
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def read_version_at(commit: str, *, repo_root: Path | None = None) -> str | None:
    root = repo_root or ROOT
    proc = _git(root, "show", f"{commit}:integrity/nlc-version.json")
    if proc.returncode != 0:
        return None
    try:
        return str(json.loads(proc.stdout)["version"]).strip()
    except (json.JSONDecodeError, KeyError):
        return None


def write_record(version: str, release_branch: str) -> Path:
    payload = {
        "schema": 2,
        "version": version,
        "release_branch": release_branch,
        "content_tree_hash_ref": CONTENT_TREE_REF,
    }
    RECORD_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return RECORD_PATH


def validate_record(
    data: dict,
    version: str,
    release_branch: str,
    *,
    commit: str | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    bad: list[str] = []
    schema = data.get("schema")
    if schema not in (1, 2):
        bad.append("hub-release-record schema must be 1 or 2")
    if data.get("version") != version:
        bad.append("hub-release-record version mismatch")
    if data.get("release_branch") != release_branch:
        bad.append("hub-release-record release_branch mismatch")
    if schema == 2:
        if data.get("content_tree_hash_ref") != CONTENT_TREE_REF:
            bad.append("hub-release-record must cite integrity/hub-content-tree-hash.txt")
    legacy_head = str(data.get("prepare_head") or "").strip()
    legacy_tree = str(data.get("prepare_tree_hash") or "").strip()
    if schema == 2 and (legacy_head or legacy_tree):
        bad.append("hub-release-record must not use prepare_head/prepare_tree_hash (ADR 0050)")
    if schema == 1 and not legacy_head and not legacy_tree:
        bad.append("hub-release-record schema 1 requires prepare_head")
    if commit and schema == 2:
        root = repo_root or ROOT
        proc = _git(root, "show", f"{commit}:{CONTENT_TREE_REF}")
        if proc.returncode != 0:
            bad.append(f"missing {CONTENT_TREE_REF} on commit")
    return bad


def main() -> int:
    from nlc_requirements import hub_tool  # noqa: E402

    hub_tool()
    parser = argparse.ArgumentParser(description="Write hub-release-record.json after prepare")
    parser.add_argument("--version", required=True)
    parser.add_argument("--branch", required=True, help="release/vX.Y.Z")
    args = parser.parse_args()

    try:
        sync_content_tree_hash(ROOT)
    except RuntimeError as exc:
        print(f"RELEASE_RECORD:REFUSE {exc}", file=sys.stderr)
        return 2
    from nouns.release_prep_surfaces.release_prep_surfaces import write_all  # noqa: E402

    write_all(ROOT, version=args.version, release_branch=args.branch)
    path = write_record(args.version, args.branch)
    print(f"RELEASE_RECORD:WROTE {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
