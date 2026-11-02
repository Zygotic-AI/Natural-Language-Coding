#!/usr/bin/env python3
"""Observe hub release facts and print the one legal action. Does not mutate git."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_release_record import git_show_json, read_version_at  # noqa: E402
from nlc_release_context import main_context  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_probe.release_probe import (  # noqa: E402
    ProbeFailure,
    confirmed_text,
    run_argv,
)
from nouns.release_state import (  # noqa: E402
    annotated_tag_argv,
    executor_permits,
    plan_release,
)

ROOT = Path(__file__).resolve().parents[3]
STAMP = ROOT / ".nlc" / "release-prepare-facts.json"


def _token_from_checkout_header() -> str:
    """actions/checkout stores the job token in local git config, not in GH_TOKEN."""
    proc = subprocess.run(
        ["git", "config", "--local", "--get-all", "http.https://github.com/.extraheader"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    prefix = "x-access-token:"
    for raw in reversed((proc.stdout or "").splitlines()):
        line = raw.strip()
        marker = "basic "
        idx = line.lower().rfind(marker)
        if idx < 0:
            continue
        try:
            decoded = base64.b64decode(line[idx + len(marker):].strip()).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            continue
        if decoded.startswith(prefix) and decoded[len(prefix):].strip():
            return decoded[len(prefix):].strip()
    return ""


def _ensure_gh_token() -> None:
    """gh in Actions exits unless GH_TOKEN is set. The workflow does not export it."""
    if os.environ.get("GH_TOKEN", "").strip():
        return
    github = os.environ.get("GITHUB_TOKEN", "").strip() or _token_from_checkout_header()
    if github:
        os.environ["GH_TOKEN"] = github


def _run(args: list[str], runner: object | None = None) -> subprocess.CompletedProcess[str]:
    if args and args[0] == "gh":
        _ensure_gh_token()
    return run_argv(args, cwd=ROOT, runner=runner)


def _out(
    args: list[str],
    *,
    empty_ok: bool = False,
    absent_codes: tuple[int, ...] = (),
    runner: object | None = None,
) -> str:
    proc = _run(args, runner=runner)
    return confirmed_text(proc, empty_ok=empty_ok, absent_codes=absent_codes)


def _worktree_version() -> str:
    path = ROOT / "integrity" / "nlc-version.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(payload.get("version") or "")


def _effective_tree() -> str:
    """Hash tracked and untracked worktree content without changing the real index."""
    fd, raw = tempfile.mkstemp(prefix="nlc-release-index-")
    os.close(fd)
    path = Path(raw)
    path.unlink(missing_ok=True)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = raw
    try:
        read = subprocess.run(
            ["git", "read-tree", "HEAD"],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if read.returncode != 0:
            return ""
        add = subprocess.run(
            ["git", "add", "-A"],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if add.returncode != 0:
            return ""
        tree = subprocess.run(
            ["git", "write-tree"],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return tree.stdout.strip() if tree.returncode == 0 else ""
    finally:
        path.unlink(missing_ok=True)


def _record_at(commit: str) -> tuple[str, str]:
    payload = git_show_json(commit, "integrity/hub-release-record.json")
    if not isinstance(payload, dict):
        return "", ""
    return str(payload.get("version") or ""), str(payload.get("release_branch") or "")


def _closed_branches(remote: str) -> set[str]:
    closed: set[str] = set()
    names = _out(["git", "tag", "-l", "v*.*.*"], empty_ok=True).split()
    for tag in names:
        if not tag.startswith("v"):
            continue
        version = tag[1:]
        peel = _out(
            ["git", "rev-parse", "-q", "--verify", f"{tag}^{{commit}}"],
            empty_ok=True,
            absent_codes=(1,),
        )
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


def _remote_tag_peel(remote: str, tag: str, runner: object | None = None) -> str:
    proc = _run(
        ["git", "ls-remote", remote, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
        runner=runner,
    )
    confirmed_text(proc, empty_ok=True)
    peeled = ""
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        sha, ref = parts
        if ref.endswith("^{}"):
            peeled = sha
    return peeled


def _remote_branch_sha(remote: str, branch: str, runner: object | None = None) -> str:
    proc = _run(["git", "ls-remote", remote, f"refs/heads/{branch}"], runner=runner)
    confirmed_text(proc, empty_ok=True)
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


def _pull_requests(
    branch: str, base: str, runner: object | None = None
) -> tuple[bool, list[dict[str, Any]]]:
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
        ],
        runner=runner,
    )
    text = confirmed_text(proc, empty_ok=False)
    try:
        rows = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProbeFailure(f"empty output: pr list JSON: {exc}", kind="empty") from exc
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


def _publish_status(tag: str, runner: object | None = None) -> str:
    proc = _run(["gh", "release", "view", tag, "--json", "tagName"], runner=runner)
    if proc.returncode == 0:
        if not (proc.stdout or "").strip() or tag not in proc.stdout:
            raise ProbeFailure("empty output: gh release view", kind="empty")
        return "success"
    if proc.returncode == 1:
        blob = ((proc.stderr or "") + (proc.stdout or "")).lower()
        if "not found" in blob or "could not find" in blob:
            return "missing"
    raise ProbeFailure(
        f"unexpected error rc={proc.returncode} {(proc.stderr or '').strip()}".strip(),
        kind="unexpected_error",
    )


def _load_stamp() -> dict[str, Any]:
    if not STAMP.is_file():
        return {}
    try:
        payload = json.loads(STAMP.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _stamp_met(stamp: dict[str, Any], name: str, sha: str) -> bool:
    return bool(sha) and stamp.get(name) is True and stamp.get(f"{name}_sha") == sha


def record_fact(name: str, remote: str, base: str) -> None:
    """Record a prepare fact the executor just proved, keyed to the observed commit."""
    if name not in {"shipped_verify_met", "target_verify_met", "prep_met"}:
        raise ValueError(name)
    current = observe(remote, base)
    if name == "shipped_verify_met":
        sha = str(current.get("shipped_tag_sha") or current.get("candidate_sha") or "")
    else:
        sha = str(current.get("effective_tree_sha") or "")
    stamp = _load_stamp()
    stamp[name] = True
    stamp[f"{name}_sha"] = sha
    STAMP.parent.mkdir(parents=True, exist_ok=True)
    STAMP.write_text(json.dumps(stamp, indent=2) + "\n", encoding="utf-8")


def fetch_marks_remote_known(remote: str, runner: object | None = None) -> bool:
    """Fetch then confirm remote state. Probe error refuses (does not return False)."""
    fetch = _run(["git", "fetch", remote, "--prune", "--tags"], runner=runner)
    confirmed_text(fetch, empty_ok=True)
    return True


def observe(remote: str, base: str) -> dict[str, Any]:
    remote_known = fetch_marks_remote_known(remote)
    head_branch = _out(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    closed = _closed_branches(remote) if remote_known else set()
    listed = _out(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/release/v*"],
        empty_ok=True,
    ).split()
    active = [name for name in listed if name not in closed]
    plan_branch = head_branch
    if not head_branch.startswith("release/v") and len(active) == 1:
        plan_branch = active[0]
    candidate = (
        _out(["git", "rev-parse", "-q", "--verify", plan_branch], absent_codes=(1,))
        if plan_branch
        else ""
    )
    if len(candidate) != 40:
        candidate = _out(["git", "rev-parse", "-q", "--verify", "HEAD"])
    remote_sha = _remote_branch_sha(remote, plan_branch) if remote_known and plan_branch.startswith("release/v") else ""
    pr_known, prs = (False, [])
    if plan_branch.startswith("release/v"):
        pr_known, prs = _pull_requests(plan_branch, base)
    version = ""
    if plan_branch.startswith("release/v"):
        version = plan_branch[len("release/v") :]
    record_version, record_branch = _record_at(candidate) if len(candidate) == 40 else ("", "")
    tag = f"v{version}" if version else ""
    shipped = (
        _out(["git", "rev-parse", "-q", "--verify", "origin/main"], absent_codes=(1,))
        if remote_known
        else ""
    )
    last_tag = ""
    if remote_known:
        describe = _run(
            ["git", "describe", "--tags", "--abbrev=0", "--match", "v*.*.*", "origin/main"]
        )
        if describe.returncode == 0:
            last_tag = (describe.stdout or "").strip()
            if not last_tag:
                raise ProbeFailure("empty output: git describe", kind="empty")
        else:
            blob = ((describe.stderr or "") + (describe.stdout or "")).lower()
            if "no names found" not in blob and "no tags" not in blob:
                raise ProbeFailure(
                    f"unexpected error rc={describe.returncode} {(describe.stderr or '').strip()}".strip(),
                    kind="unexpected_error",
                )
    shipped_peel = (
        _out(
            ["git", "rev-parse", "-q", "--verify", f"{last_tag}^{{commit}}"],
            empty_ok=True,
            absent_codes=(1,),
        )
        if last_tag
        else ""
    )
    stamp = _load_stamp()
    shipped_key = shipped_peel if len(shipped_peel) == 40 else candidate
    effective_tree = _effective_tree()
    context_status, context_details = (
        main_context(remote, base, plan_branch)
        if plan_branch.startswith("release/v")
        else ("unknown", ["release line is not selected"])
    )
    local_tag_peeled_sha = ""
    remote_tag_peeled_sha = ""
    local_tag_known = True
    remote_tag_known = True
    if tag:
        local_tag_peeled_sha = _out(
            ["git", "rev-parse", "-q", "--verify", f"{tag}^{{commit}}"],
            empty_ok=True,
            absent_codes=(1,),
        )
        if remote_known:
            remote_tag_peeled_sha = _remote_tag_peel(remote, tag)
    return {
        "remote_known": remote_known,
        "pr_list_known": pr_known if plan_branch.startswith("release/v") else True,
        "local_tag_known": local_tag_known,
        "remote_tag_known": remote_tag_known,
        "local_branch": plan_branch,
        "desired_version": version,
        "candidate_sha": candidate,
        "effective_tree_sha": effective_tree,
        "dirty": bool(_out(["git", "status", "--porcelain"], empty_ok=True)),
        "worktree_file_version": _worktree_version(),
        "head_file_version": read_version_at("HEAD") or "",
        "candidate_record_version": record_version,
        "candidate_record_branch": record_branch,
        "remote_relation": _relation(candidate, remote_sha, remote_known),
        "active_release_branches": active,
        "pull_requests": prs,
        "origin_main_sha": shipped if len(shipped) == 40 else "",
        "shipped_tag_sha": shipped_peel if len(shipped_peel) == 40 else "",
        "local_tag_peeled_sha": local_tag_peeled_sha,
        "remote_tag_peeled_sha": remote_tag_peeled_sha,
        "publish_status": _publish_status(tag) if tag else "missing",
        "main_context": context_status,
        "main_context_details": context_details,
        "runtime_blocker": os.environ.get("NLC_RELEASE_RUNTIME_BLOCKER", ""),
        "failed_action": os.environ.get("NLC_RELEASE_FAILED_ACTION", ""),
        "stalled_action": os.environ.get("NLC_RELEASE_STALLED_ACTION", ""),
        "migrations_ready": True,
        "shipped_verify_met": _stamp_met(stamp, "shipped_verify_met", shipped_key),
        "notes_valid": _notes_valid(version) if version else False,
        "target_verify_met": _stamp_met(stamp, "target_verify_met", effective_tree),
        "prep_met": _stamp_met(stamp, "prep_met", effective_tree),
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
    parser.add_argument("--record-fact", choices=("shipped_verify_met", "target_verify_met", "prep_met"))
    args = parser.parse_args()
    if args.record_fact:
        try:
            record_fact(args.record_fact, args.remote, args.base)
        except ProbeFailure as exc:
            print(f"RELEASE:NOT_MET probe={exc}", file=sys.stderr)
            return 1
        return 0
    if args.tag_argv:
        version = args.tag[1:] if args.tag.startswith("v") else args.tag
        for part in annotated_tag_argv(args.tag, args.commit, f"Natural Language Compiler hub {version}"):
            print(part)
        return 0
    if args.facts:
        facts = json.loads(args.facts.read_text(encoding="utf-8"))
    else:
        try:
            facts = observe(args.remote, args.base)
        except ProbeFailure as exc:
            print(f"RELEASE:NOT_MET probe={exc}", file=sys.stderr)
            return 1
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
