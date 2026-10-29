"""CI drill: fitness verdict unchanged after history rewrite and shallow clone (ADR 0050)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def resolve_drill_git(env: dict[str, str] | None = None) -> str | None:
    """Return git executable path for the drill, or None when missing or unknown."""
    use_env = env if env is not None else os.environ
    git_cmd = (use_env.get("NLC_DRILL_GIT") or "git").strip() or "git"
    try:
        proc = subprocess.run(
            [git_cmd, "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None
    if proc.returncode != 0:
        return None
    if not (proc.stdout or "").strip() and not (proc.stderr or "").strip():
        return None
    return git_cmd


def drill_git_clone(
    git_cmd: str,
    source: str | Path,
    dest: str | Path,
    *,
    depth: int | None = None,
    local: bool = False,
) -> int:
    """Run git clone for the drill with --no-hardlinks; print git stderr on failure."""
    cmd = [git_cmd, "clone", "--no-hardlinks"]
    if local:
        cmd.append("--local")
    if depth is not None:
        cmd.extend(["--depth", str(int(depth))])
    cmd.extend([str(source), str(dest)])
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        if err:
            print(err, file=sys.stderr)
        else:
            print(
                "history-rewrite-drill: git clone failed with empty stderr",
                file=sys.stderr,
            )
        return proc.returncode if proc.returncode != 0 else 1
    return 0


def run_releasable_release(cwd: Path) -> int:
    """Same releasable release profile as ./nlc gate --profile release (no CI-only side effects)."""
    proc = subprocess.run(
        [
            sys.executable,
            str(cwd / "tools" / "nlc_gate.py"),
            "--profile",
            "release",
            "--tree",
            ".",
        ],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode


def rewrite_history(repo: Path, git_cmd: str = "git") -> None:
    """Change author metadata on all commits so commit ids change, trees unchanged."""
    env_filter = (
        "GIT_AUTHOR_NAME='history-rewrite-drill';"
        "GIT_AUTHOR_EMAIL='drill@example.com';"
        "GIT_COMMITTER_NAME='history-rewrite-drill';"
        "GIT_COMMITTER_EMAIL='drill@example.com'"
    )
    subprocess.run(
        [
            git_cmd,
            "filter-branch",
            "-f",
            "--env-filter",
            env_filter,
            "--",
            "--all",
        ],
        cwd=str(repo),
        check=True,
        capture_output=True,
    )


def trees_equal(a: Path, b: Path, git_cmd: str = "git") -> bool:
    proc = subprocess.run(
        [git_cmd, "rev-parse", "HEAD^{tree}"],
        cwd=str(a),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return False
    tree_a = (proc.stdout or "").strip()
    proc_b = subprocess.run(
        [git_cmd, "rev-parse", "HEAD^{tree}"],
        cwd=str(b),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_b.returncode != 0:
        return False
    return tree_a == (proc_b.stdout or "").strip()


def main() -> int:
    git_cmd = resolve_drill_git()
    if git_cmd is None:
        print(
            "ASSERT:FAIL history rewrite drill refuses: git missing or unknown",
            file=sys.stderr,
        )
        return 2

    with tempfile.TemporaryDirectory(prefix="nlc-rewrite-drill-") as tmp:
        tmp_path = Path(tmp)
        baseline_clone = tmp_path / "baseline"
        rc = drill_git_clone(git_cmd, ROOT, baseline_clone, local=True)
        if rc != 0:
            return rc
        baseline = run_releasable_release(baseline_clone)
        clone = tmp_path / "full"
        rc = drill_git_clone(git_cmd, baseline_clone, clone, local=True)
        if rc != 0:
            return rc
        rewrite_history(clone, git_cmd=git_cmd)
        if not trees_equal(baseline_clone, clone, git_cmd=git_cmd):
            print("ASSERT:FAIL rewrite drill changed HEAD tree content")
            return 1
        rewritten = run_releasable_release(clone)
        if rewritten != baseline:
            print(
                f"ASSERT:FAIL fitness exit {baseline} on hub != {rewritten} after history rewrite"
            )
            return 1

        shallow = tmp_path / "shallow"
        rc = drill_git_clone(git_cmd, baseline_clone, shallow, depth=1, local=True)
        if rc != 0:
            return rc
        shallow_code = run_releasable_release(shallow)
        if shallow_code != baseline:
            print(
                f"ASSERT:FAIL fitness exit {baseline} on hub != {shallow_code} on depth-1 clone"
            )
            return 1

    print(f"ASSERT:PASS history rewrite invariant (release profile exit {baseline})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
