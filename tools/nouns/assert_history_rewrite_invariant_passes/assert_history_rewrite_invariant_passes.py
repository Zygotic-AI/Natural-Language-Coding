"""CI drill: fitness verdict unchanged after history rewrite and shallow clone (ADR 0050)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


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


def rewrite_history(repo: Path) -> None:
    """Change author metadata on all commits so commit ids change, trees unchanged."""
    env_filter = (
        "GIT_AUTHOR_NAME='history-rewrite-drill';"
        "GIT_AUTHOR_EMAIL='drill@example.com';"
        "GIT_COMMITTER_NAME='history-rewrite-drill';"
        "GIT_COMMITTER_EMAIL='drill@example.com'"
    )
    subprocess.run(
        [
            "git",
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


def trees_equal(a: Path, b: Path) -> bool:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=str(a),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return False
    tree_a = (proc.stdout or "").strip()
    proc_b = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=str(b),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_b.returncode != 0:
        return False
    return tree_a == (proc_b.stdout or "").strip()


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="nlc-rewrite-drill-") as tmp:
        tmp_path = Path(tmp)
        baseline_clone = tmp_path / "baseline"
        subprocess.run(
            ["git", "clone", "--local", str(ROOT), str(baseline_clone)],
            check=True,
            capture_output=True,
        )
        baseline = run_releasable_release(baseline_clone)
        clone = tmp_path / "full"
        subprocess.run(
            ["git", "clone", "--local", str(baseline_clone), str(clone)],
            check=True,
            capture_output=True,
        )
        rewrite_history(clone)
        if not trees_equal(baseline_clone, clone):
            print("ASSERT:FAIL rewrite drill changed HEAD tree content")
            return 1
        rewritten = run_releasable_release(clone)
        if rewritten != baseline:
            print(
                f"ASSERT:FAIL fitness exit {baseline} on hub != {rewritten} after history rewrite"
            )
            return 1

        shallow = tmp_path / "shallow"
        subprocess.run(
            ["git", "clone", "--depth", "1", "--local", str(baseline_clone), str(shallow)],
            check=True,
            capture_output=True,
        )
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
