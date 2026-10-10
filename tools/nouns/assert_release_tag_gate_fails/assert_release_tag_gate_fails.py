"""Landmine ADR 0039: tag gate refuses commits without hub-release-record."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from nouns.evidence_ref.synthetic_release import unprepared_release_commit  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="nlc-tag-gate-lm-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        bad_commit = unprepared_release_commit(repo, "0.2.0")
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "nlc_release_tag_gate.py"),
                "--check",
                "--commit",
                bad_commit,
                "--tag",
                "v0.2.0",
                "--skip-verify-deep",
                "--repo-root",
                str(repo),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
    if proc.returncode == 0:
        print("ASSERT:FAIL tag gate should refuse commit without release record")
        print(proc.stdout, proc.stderr)
        return 1
    combined = (proc.stdout or "") + (proc.stderr or "")
    if "hub-release-record" not in combined and "release record" not in combined.lower():
        print("ASSERT:FAIL expected hub-release-record blocker")
        return 1
    print("ASSERT:PASS release tag gate refuses unprepared merge commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
