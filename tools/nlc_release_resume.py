#!/usr/bin/env python3
"""Detect ./release resume phase (ADR 0039)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_release_record import git_show_json  # noqa: E402
from nlc_release_tags import tag_exists  # noqa: E402


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def _is_full_sha(value: str) -> bool:
    value = value.strip().lower()
    return len(value) == 40 and all(c in "0123456789abcdef" for c in value)


def resolve_ref_sha(ref: str) -> str:
    """Git rev-parse; git may print ref name on stderr path — ignore non-SHA stdout."""
    proc = _git("rev-parse", ref)
    if proc.returncode != 0:
        return ""
    sha = (proc.stdout or "").strip()
    return sha if _is_full_sha(sha) else ""


def remote_branch_exists(remote: str, branch: str) -> bool:
    proc = _git("ls-remote", "--heads", remote, f"refs/heads/{branch}")
    return proc.returncode == 0 and bool((proc.stdout or "").strip())


def list_release_branches(remote: str) -> list[str]:
    branches: list[str] = []
    for proc_args in (
        ["branch", "-r", "--list", f"{remote}/release/v*"],
        ["branch", "--list", "release/v*"],
    ):
        proc = _git(*proc_args)
        for line in (proc.stdout or "").splitlines():
            name = line.strip().lstrip("* ").strip()
            if "->" in name:
                continue
            if name.startswith(f"{remote}/"):
                name = name[len(remote) + 1 :]
            if re.match(r"release/v\d+\.\d+\.\d+$", name):
                branches.append(name)
    return sorted(set(branches), key=_branch_key, reverse=True)


def _branch_key(branch: str) -> tuple[int, int, int]:
    ver = branch.replace("release/v", "")
    parts = ver.split(".")
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return (0, 0, 0)


def merged_commit_for_branch(remote: str, base: str, rel_branch: str, tip: str) -> str | None:
    if _git("merge-base", "--is-ancestor", tip, f"{remote}/{base}").returncode == 0:
        proc = _git("rev-list", "--ancestry-path", f"{tip}..{remote}/{base}")
        if proc.returncode == 0 and proc.stdout.strip():
            lines = [ln for ln in proc.stdout.strip().splitlines() if ln]
            return lines[-1] if lines else tip
        return tip
    return None


def tag_on_commit(tag: str, commit: str) -> bool:
    if not tag_exists(tag):
        return False
    proc = _git("rev-parse", f"{tag}^{{commit}}")
    return proc.returncode == 0 and proc.stdout.strip() == commit


def release_record_on_commit(commit: str) -> bool:
    return git_show_json(commit, "integrity/hub-release-record.json") is not None


def detect(remote: str, base: str) -> dict:
    _git("fetch", remote, base, "--tags", "--prune", "--quiet")
    stale_branches: list[str] = []
    closed_branches: list[str] = []
    await_merge_row: dict | None = None
    for rel in list_release_branches(remote):
        if not remote_branch_exists(remote, rel):
            # Local-only release lines resume via prepare/infer — not PR wait (RCA 26-09-25).
            continue
        ver = rel.replace("release/v", "")
        tag = f"v{ver}"
        tip = resolve_ref_sha(f"{remote}/{rel}")
        if not tip:
            continue
        merge = merged_commit_for_branch(remote, base, rel, tip)
        if merge:
            if not release_record_on_commit(merge):
                stale_branches.append(rel)
                continue
            exists_on_merge = tag_on_commit(tag, merge)
            if exists_on_merge or tag_exists(tag):
                # Shipped (tag on merge or tag exists) — skip orchestration; not "stale" (RCA 26-09-25)
                closed_branches.append(rel)
                continue
            row = {
                "phase": "tag_ready",
                "version": ver,
                "release_branch": rel,
                "merge_commit": merge,
                "planned_tag": tag,
                "tag": tag,
                "git_tag_on_merge": False,
                "release_record_on_merge": True,
                "stale_release_branches": stale_branches,
                "closed_release_branches": closed_branches,
            }
            return row
        if await_merge_row is None:
            await_merge_row = {
                "phase": "await_merge",
                "version": ver,
                "release_branch": rel,
                "merge_commit": "",
                "planned_tag": tag,
                "tag": tag,
                "git_tag_on_merge": False,
                "release_record_on_merge": False,
            }
    if await_merge_row is not None:
        await_merge_row["stale_release_branches"] = stale_branches
        await_merge_row["closed_release_branches"] = closed_branches
        return await_merge_row
    return {
        "phase": "prepare",
        "version": "",
        "release_branch": "",
        "merge_commit": "",
        "planned_tag": "",
        "tag": "",
        "git_tag_on_merge": False,
        "release_record_on_merge": False,
        "stale_release_branches": stale_branches,
        "closed_release_branches": closed_branches,
    }


def main() -> int:
    from nlc_requirements import hub_tool  # noqa: E402

    hub_tool()
    parser = argparse.ArgumentParser(description="Release resume phase")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--emit", choices=("shell", "json"), default="shell")
    args = parser.parse_args()

    state = detect(args.remote, args.base)
    if args.emit == "json":
        import json

        print(json.dumps(state))
        return 0

    print(f"RESUME_PHASE={state['phase']}")
    print(f"RESUME_VERSION={state['version']}")
    print(f"RESUME_BRANCH={state['release_branch']}")
    print(f"RESUME_MERGE_COMMIT={state['merge_commit']}")
    print(f"RESUME_TAG={state['tag']}")
    print(f"RESUME_GIT_TAG_ON_MERGE={'1' if state.get('git_tag_on_merge') else '0'}")
    stale = state.get("stale_release_branches") or []
    closed = state.get("closed_release_branches") or []
    print(f"RESUME_STALE_BRANCHES={','.join(stale)}")
    print(f"RESUME_CLOSED_BRANCHES={','.join(closed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
