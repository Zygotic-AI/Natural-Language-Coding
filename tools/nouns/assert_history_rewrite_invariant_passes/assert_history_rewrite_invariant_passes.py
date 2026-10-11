"""CI drill: fitness verdict unchanged after history rewrite and shallow clone (ADR 0050)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run_fitness(cwd: Path) -> int:
    env = os.environ.copy()
    env["NLC_CI_FITNESS_DEPTH"] = str(int(env.get("NLC_CI_FITNESS_DEPTH", "0") or "0") + 1)
    proc = subprocess.run(
        [sys.executable, str(cwd / "tools" / "ci_fitness.py")],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
        env=env,
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
        baseline = run_fitness(baseline_clone)
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
        rewritten = run_fitness(clone)
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
        shallow_code = run_fitness(shallow)
        if shallow_code != baseline:
            print(
                f"ASSERT:FAIL fitness exit {baseline} on hub != {shallow_code} on depth-1 clone"
            )
            return 1

    print(f"ASSERT:PASS history rewrite invariant (fitness exit {baseline})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
