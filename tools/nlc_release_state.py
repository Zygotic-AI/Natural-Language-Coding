#!/usr/bin/env python3
"""Observe hub release facts and print the one legal action. Does not mutate git."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_release_record import git_show_json, read_version_at  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_state import (  # noqa: E402
    annotated_tag_argv,
    executor_permits,
    plan_release,
)

ROOT = Path(__file__).resolve().parents[1]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True, check=False)


def _out(args: list[str]) -> str:
    proc = _run(args)
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def _worktree_version() -> str:
    path = ROOT / "integrity" / "nlc-version.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(payload.get("version") or "")


def _record_at(commit: str) -> tuple[str, str]:
    payload = git_show_json(commit, "integrity/hub-release-record.json")
    if not isinstance(payload, dict):
        return "", ""
    return str(payload.get("version") or ""), str(payload.get("release_branch") or "")


def _closed_branches(remote: str) -> set[str]:
    closed: set[str] = set()
    names = _out(["git", "tag", "-l", "v*.*.*"]).split()
    for tag in names:
        if not tag.startswith("v"):
            continue
        version = tag[1:]
        peel = _out(["git", "rev-parse", f"{tag}^{{commit}}"])
        if len(peel) != 40:
            remote_peel = _remote_tag_peel(remote, tag)
            peel = remote_peel
        if len(peel) != 40:
            continue
        file_version = read_version_at(peel) or ""
        record_version, record_branch = _record_at(peel)
        if file_version == version and record_version == version and record_branch == f"release/v{version}":
            closed.add(record_branch)
    return closed


def _remote_tag_peel(remote: str, tag: str) -> str:
    proc = _run(["git", "ls-remote", remote, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"])
    peeled = ""
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        sha, ref = parts
        if ref.endswith("^{}"):
            peeled = sha
    return peeled


def _remote_branch_sha(remote: str, branch: str) -> str:
    proc = _run(["git", "ls-remote", remote, f"refs/heads/{branch}"])
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == f"refs/heads/{branch}":
            return parts[0]
    return ""


def _relation(local_sha: str, remote_sha: str, remote_known: bool) -> str:
    if not remote_known:
        return "unknown"
    if not remote_sha:
        return "absent"
    if remote_sha == local_sha:
        return "equal"
    if _run(["git", "merge-base", "--is-ancestor", remote_sha, local_sha]).returncode == 0:
        return "ahead"
    if _run(["git", "merge-base", "--is-ancestor", local_sha, remote_sha]).returncode == 0:
        return "behind"
    return "diverged"


def _pull_requests(branch: str, base: str) -> tuple[bool, list[dict[str, Any]]]:
    proc = _run(
        [
            "gh",
            "pr",
            "list",
            "--head",
            branch,
            "--base",
            base,
            "--state",
            "all",
            "--json",
            "number,state,headRefOid,mergeCommit",
        ]
    )
    if proc.returncode != 0:
        return False, []
    try:
        rows = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return False, []
    found: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        merge = row.get("mergeCommit")
        merge_sha = ""
        if isinstance(merge, dict):
            merge_sha = str(merge.get("oid") or "")
        elif isinstance(merge, str):
            merge_sha = merge
        merge_file = read_version_at(merge_sha) or "" if merge_sha else ""
        merge_record_version, merge_record_branch = _record_at(merge_sha) if merge_sha else ("", "")
        found.append(
            {
                "number": row.get("number"),
                "state": str(row.get("state") or "").lower(),
                "head_sha": str(row.get("headRefOid") or ""),
                "merge_sha": merge_sha,
                "merge_file_version": merge_file,
                "merge_record_version": merge_record_version,
                "merge_record_branch": merge_record_branch,
            }
        )
    return True, found


def _notes_valid(version: str) -> bool:
    if not version:
        return False
    proc = _run(["python3", "tools/nlc_release_notes.py", "--check", "--version", version])
    return proc.returncode == 0


def _publish_status(tag: str) -> str:
    proc = _run(["gh", "release", "view", tag, "--json", "tagName"])
    if proc.returncode == 0 and tag in proc.stdout:
        return "success"
    return "missing"


def observe(remote: str, base: str) -> dict[str, Any]:
    fetch = _run(["git", "fetch", remote, "--prune", "--tags"])
    remote_known = fetch.returncode == 0
    head_branch = _out(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    closed = _closed_branches(remote) if remote_known else set()
    listed = _out(["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/release/v*"]).split()
    active = [name for name in listed if name not in closed]
    plan_branch = head_branch
    if not head_branch.startswith("release/v") and len(active) == 1:
        plan_branch = active[0]
    candidate = _out(["git", "rev-parse", plan_branch]) if plan_branch else ""
    if len(candidate) != 40:
        candidate = _out(["git", "rev-parse", "HEAD"])
    remote_sha = _remote_branch_sha(remote, plan_branch) if remote_known and plan_branch.startswith("release/v") else ""
    pr_known, prs = (False, [])
    if plan_branch.startswith("release/v"):
        pr_known, prs = _pull_requests(plan_branch, base)
    version = ""
    if plan_branch.startswith("release/v"):
        version = plan_branch[len("release/v") :]
    record_version, record_branch = _record_at(candidate) if len(candidate) == 40 else ("", "")
    tag = f"v{version}" if version else ""
    shipped = _out(["git", "rev-parse", "origin/main"]) if remote_known else ""
    last_tag = _out(["git", "describe", "--tags", "--abbrev=0", "--match", "v*.*.*", "origin/main"]) if remote_known else ""
    shipped_peel = _out(["git", "rev-parse", f"{last_tag}^{{commit}}"]) if last_tag else ""
    return {
        "remote_known": remote_known,
        "pr_list_known": pr_known if plan_branch.startswith("release/v") else True,
        "local_branch": plan_branch,
        "desired_version": version,
        "candidate_sha": candidate,
        "dirty": bool(_out(["git", "status", "--porcelain"])),
        "worktree_file_version": _worktree_version(),
        "head_file_version": read_version_at("HEAD") or "",
        "candidate_record_version": record_version,
        "candidate_record_branch": record_branch,
        "remote_relation": _relation(candidate, remote_sha, remote_known),
        "active_release_branches": active,
        "pull_requests": prs,
        "origin_main_sha": shipped if len(shipped) == 40 else "",
        "shipped_tag_sha": shipped_peel if len(shipped_peel) == 40 else "",
        "local_tag_peeled_sha": _out(["git", "rev-parse", f"{tag}^{{commit}}"]) if tag else "",
        "remote_tag_peeled_sha": _remote_tag_peel(remote, tag) if tag and remote_known else "",
        "publish_status": _publish_status(tag) if tag else "missing",
        "migrations_ready": True,
        "shipped_verify_met": False,
        "notes_valid": _notes_valid(version) if version else False,
        "target_verify_met": False,
        "prep_met": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan one hub release action from observed facts")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--emit", choices=("json", "facts", "remediation"), default="json")
    parser.add_argument("--print", dest="print_field", default="")
    parser.add_argument("--permits", default="")
    parser.add_argument("--tag-argv", action="store_true")
    parser.add_argument("--tag", default="")
    parser.add_argument("--commit", default="")
    parser.add_argument("--facts", type=Path, help="Plan from a JSON facts file instead of git")
    args = parser.parse_args()
    if args.tag_argv:
        version = args.tag[1:] if args.tag.startswith("v") else args.tag
        for part in annotated_tag_argv(args.tag, args.commit, f"Natural Language Coding hub {version}"):
            print(part)
        return 0
    if args.facts:
        facts = json.loads(args.facts.read_text(encoding="utf-8"))
    else:
        facts = observe(args.remote, args.base)
    if args.emit == "facts":
        print(json.dumps(facts, indent=2))
        return 0
    decision = plan_release(facts)
    if args.permits:
        print("yes" if executor_permits(decision, args.permits) else "no")
        return 0
    if args.print_field:
        value = decision.get(args.print_field, "")
        print("true" if value is True else "false" if value is False else value)
        return 0
    if args.emit == "remediation":
        print(f"RELEASE:NOT_MET phase={decision['phase']} action={decision['action']}")
        if decision.get("problem"):
            print(f"Problem: {decision['problem']}")
        for code in decision.get("blockers") or []:
            print(f"Gap: {code}")
        for fix in decision.get("fixes") or []:
            print(f"Fix: {fix}")
        print("Re-run: ./release")
        return 1 if decision["action"] == "BLOCKED" or decision["phase"] == "INVALID_MERGED" else 0
    print(json.dumps(decision, indent=2))
    return 0


if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())
