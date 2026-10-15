"""Landmine: release main-context observation is closed and merge-aware."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import tempfile
from pathlib import Path

from nouns.nlc_release_context import nlc_release_context as context

ROOT = Path(__file__).resolve().parents[3]


def _git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


def main() -> int:
    source = (ROOT / "tools/nouns/nlc_release_context/nlc_release_context.py").read_text(
        encoding="utf-8"
    )
    if '"15"' in source or "--max-count=15" in source:
        print("ASSERT:FAIL release context still has a commit cap")
        return 1

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        _git(repo, "init")
        _git(repo, "config", "user.email", "release-context@example.invalid")
        _git(repo, "config", "user.name", "release-context")
        (repo / "value").write_text("base\n", encoding="utf-8")
        _git(repo, "add", "value")
        _git(repo, "commit", "-m", "base")
        base = _git(repo, "rev-parse", "HEAD")

        _git(repo, "checkout", "-b", "release/v9.0.0")
        (repo / "value").write_text("release\n", encoding="utf-8")
        _git(repo, "commit", "-am", "release")
        release = _git(repo, "rev-parse", "HEAD")

        _git(repo, "checkout", "-b", "main", base)
        _git(repo, "merge", "--no-ff", "release/v9.0.0", "-m", "merge release")
        contained_merge = _git(repo, "rev-parse", "HEAD")
        _git(repo, "update-ref", "refs/remotes/origin/main", contained_merge)

        def repo_git(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ["git", *args],
                cwd=str(repo),
                capture_output=True,
                text=True,
                check=False,
            )

        try:
            status, details = context.main_context(
                "origin", "main", "release/v9.0.0", git=repo_git
            )
            if status != "contained" or details:
                print(f"ASSERT:FAIL contained merge status={status} details={details}")
                return 1

            (repo / "unique").write_text("main only\n", encoding="utf-8")
            _git(repo, "add", "unique")
            _git(repo, "commit", "-m", "main only")
            _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
            status, _ = context.main_context(
                "origin", "main", "release/v9.0.0", git=repo_git
            )
            if status != "not_contained":
                print(f"ASSERT:FAIL unique main commit status={status}")
                return 1

            release_tree = _git(repo, "rev-parse", f"{release}^{{tree}}")
            lossy = _git(
                repo,
                "commit-tree",
                f"{base}^{{tree}}",
                "-p",
                base,
                "-p",
                release,
                "-m",
                "lossy merge",
            )
            if release_tree == _git(repo, "rev-parse", f"{lossy}^{{tree}}"):
                print("ASSERT:FAIL lossy merge specimen has release tree")
                return 1
            _git(repo, "update-ref", "refs/remotes/origin/main", lossy)
            status, _ = context.main_context(
                "origin", "main", "release/v9.0.0", git=repo_git
            )
            if status != "not_contained":
                print(f"ASSERT:FAIL merge-only tree status={status}")
                return 1

            def missing_parent(*args: str) -> subprocess.CompletedProcess[str]:
                if args[:2] == ("rev-list", "--parents"):
                    return subprocess.CompletedProcess(args, 128, "", "missing parent")
                return repo_git(*args)

            status, _ = context.main_context(
                "origin", "main", "release/v9.0.0", git=missing_parent
            )
            if status != "unknown":
                print(f"ASSERT:FAIL missing parent status={status}")
                return 1

            status, _ = context.main_context(
                "missing-remote", "main", "release/v9.0.0", git=repo_git
            )
            if status != "unknown":
                print(f"ASSERT:FAIL git error status={status}")
                return 1
        finally:
            pass

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        _git(repo, "init")
        _git(repo, "config", "user.email", "release-context@example.invalid")
        _git(repo, "config", "user.name", "release-context")
        (repo / "value").write_text("base\n", encoding="utf-8")
        _git(repo, "add", "value")
        _git(repo, "commit", "-m", "base")
        base = _git(repo, "rev-parse", "HEAD")

        _git(repo, "checkout", "-b", "old-release", base)
        (repo / "value").write_text("old-release\n", encoding="utf-8")
        _git(repo, "commit", "-am", "old release")
        old_release = _git(repo, "rev-parse", "HEAD")

        _git(repo, "checkout", "-b", "main", base)
        _git(repo, "merge", "--no-ff", old_release, "-m", "merge old release")

        _git(repo, "checkout", "-b", "release/v9.0.0", old_release)
        (repo / "value").write_text("new-release\n", encoding="utf-8")
        _git(repo, "commit", "-am", "new release")
        new_release = _git(repo, "rev-parse", "HEAD")

        _git(repo, "checkout", "main")
        _git(repo, "merge", "--no-ff", "release/v9.0.0", "-m", "merge new release")
        github_merge = _git(repo, "rev-parse", "HEAD")
        if _git(repo, "rev-parse", f"{github_merge}^{{tree}}") != _git(
            repo, "rev-parse", f"{new_release}^{{tree}}"
        ):
            print("ASSERT:FAIL diverged GitHub merge specimen tree != release")
            return 1
        _git(repo, "update-ref", "refs/remotes/origin/main", github_merge)

        def repo_git(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ["git", *args],
                cwd=str(repo),
                capture_output=True,
                text=True,
                check=False,
            )

        status, details = context.main_context(
            "origin", "main", "release/v9.0.0", git=repo_git
        )
        if status != "contained" or details:
            print(
                f"ASSERT:FAIL diverged GitHub merge status={status} details={details}"
            )
            return 1

    print("ASSERT:PASS release context is closed and merge-aware")
    return 0
