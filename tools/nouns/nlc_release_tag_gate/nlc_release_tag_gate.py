#!/usr/bin/env python3
"""ADR 0022/0039: refuse tag unless merge commit passed full release gates."""

from __future__ import annotations

BOUNDARY = "bba-emit"


import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_release_record import git_show_json, read_version_at, validate_record  # noqa: E402
from nlc_release_tags import resolve_shipped_version  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402
from nouns.evidence_ref.evidence_ref import refuse_gate, resolve_commit  # noqa: E402
from nouns.fitness_findings_shipped_tag_sync import (  # noqa: E402
    check_surfaces,
    resolve_shipped_version as f1_shipped_version,
)

RECORD_REL = "integrity/hub-release-record.json"


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )


def tag_from_version(ver: str) -> str:
    return f"v{ver.lstrip('v')}"


def git_show_text(repo_root: Path, commit: str, rel_path: str) -> str | None:
    proc = _git(repo_root, "show", f"{commit}:{rel_path}")
    if proc.returncode != 0:
        return None
    return proc.stdout


def check_static(repo_root: Path, commit: str, tag: str) -> list[str]:
    problems: list[str] = []
    ver = tag.lstrip("v")
    file_ver = read_version_at(commit, repo_root=repo_root)
    if not file_ver:
        problems.append("missing integrity/nlc-version.json at commit")
    elif file_ver != ver:
        problems.append(f"tag {tag} != nlc-version.json ({file_ver})")

    record = git_show_json(commit, RECORD_REL, repo_root=repo_root)
    if not record:
        problems.append(f"missing {RECORD_REL} on commit (./release prepare leg)")
    else:
        problems.extend(validate_record(record, ver, f"release/v{ver}", commit=commit, repo_root=repo_root))

    notes_rel = f"docs/adoption/RELEASE-v{ver}.md"
    notes_text = git_show_text(repo_root, commit, notes_rel)
    if not notes_text:
        problems.append(f"missing {notes_rel} on commit")
    else:
        with tempfile.TemporaryDirectory(prefix="nlc-notes-") as tmp:
            path = Path(tmp) / "RELEASE.md"
            path.write_text(notes_text, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "nlc_release_notes.py"), "--check", "--version", ver],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
                env={**__import__("os").environ, "NLC_RELEASE_NOTES_PATH": str(path)},
            )
            if proc.returncode != 0:
                if "Replace this block with user-facing summary" in notes_text:
                    problems.append("release notes Highlights still placeholder")
                elif "## Highlights" not in notes_text:
                    problems.append("release notes missing Highlights section")

    from nlc_migration_catalog import migration_steps_blockers

    shipped = resolve_shipped_version(commit) or "0.0.0"
    if shipped != ver:
        problems.extend(migration_steps_blockers(ROOT, shipped, ver))

    findings_text = git_show_text(repo_root, commit, "FINDINGS.md") or ""
    describe_text = git_show_text(repo_root, commit, "DESCRIBE.md") or ""
    problems.extend(
        check_surfaces(
            findings_text,
            describe_text,
            shipped_ver=f1_shipped_version(),
            file_ver=ver,
            on_main_or_tag=True,
        )
    )

    return problems


def run_verify_deep_at(commit: str) -> list[str]:
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="nlc-rel-wt-") as tmp:
        wt = Path(tmp) / "wt"
        proc = _git(ROOT, "worktree", "add", "--detach", str(wt), commit)
        if proc.returncode != 0:
            return [f"cannot create worktree at {commit[:12]}: {proc.stderr.strip()}"]
        try:
            # Grade the tag commit with that commit's tools, not the agent's worktree.
            vproc = subprocess.run(
                [sys.executable, str(wt / "tools" / "nlc.py"), "--project", ".", "verify-deep"],
                cwd=str(wt),
                capture_output=True,
                text=True,
                check=False,
            )
            if vproc.returncode != 0:
                problems.append("verify-deep NOT_MET at tag commit")
                tail = ((vproc.stdout or "") + (vproc.stderr or "")).strip().splitlines()
                for line in tail[-6:]:
                    problems.append(f"  {line}")
        finally:
            _git(ROOT, "worktree", "remove", "--force", str(wt))
    return problems


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Hub release tag gate")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--commit", required=True, help="Merge commit to tag")
    parser.add_argument("--tag", default=None, help="vX.Y.Z (default from commit version file)")
    parser.add_argument("--skip-verify-deep", action="store_true")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Git root for object reads (default hub checkout; landmines use synthetic repos)",
    )
    args = parser.parse_args()

    if not args.check:
        parser.print_help()
        return 2

    repo_root = Path(args.repo_root).resolve() if args.repo_root else ROOT
    commit = args.commit.strip()
    _, err = resolve_commit(repo_root, commit)
    if err:
        return refuse_gate("RELEASE_TAG_GATE", commit, err)

    ver = read_version_at(commit, repo_root=repo_root)
    if not ver:
        print("RELEASE_TAG_GATE:NOT_MET", file=sys.stderr)
        print("  What's wrong: no nlc-version.json at commit", file=sys.stderr)
        print("  Fix: merge a release branch that bumps integrity/nlc-version.json", file=sys.stderr)
        return 1
    tag = args.tag or tag_from_version(ver)
    if tag.lstrip("v") != ver:
        print("RELEASE_TAG_GATE:NOT_MET", file=sys.stderr)
        print(f"  What's wrong: --tag {tag} != commit version {ver}", file=sys.stderr)
        return 1

    problems = check_static(repo_root, commit, tag)
    if not problems and not args.skip_verify_deep and repo_root == ROOT:
        problems.extend(run_verify_deep_at(commit))

    if problems:
        print("RELEASE_TAG_GATE:NOT_MET", file=sys.stderr)
        print(f"  Commit: {commit[:12]}  Tag: {tag}", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print("  Fix: run ./release from main; merge release/v* with record + notes + verify-deep.", file=sys.stderr)
        return 1

    print(f"RELEASE_TAG_GATE:MET tag={tag} commit={commit[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
