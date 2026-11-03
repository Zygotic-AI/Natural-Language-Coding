"""Known-bad: an unsigned checker digest is refused once the tag verifier exists."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARMOR_REL = "integrity/checker-digest.sha256.approval.asc"


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    """Grade a detached copy with the signature file removed.

    The live tree may already carry a valid sidecar. This landmine still has
    to prove that a tree without that sidecar is refused.
    """
    with tempfile.TemporaryDirectory(prefix="nlc-unsigned-digest-") as tmp:
        work = Path(tmp) / "tree"
        added = _git("worktree", "add", "--detach", str(work), "HEAD")
        if added.returncode != 0:
            print(f"ASSERT:FAIL unsigned worktree: {added.stderr.strip()}")
            return 1
        try:
            armor = work / ARMOR_REL
            if armor.is_file():
                armor.unlink()
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "check-checker-digest-signature.py"),
                    "--root",
                    str(work),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                check=False,
            )
        finally:
            _git("worktree", "remove", "--force", str(work))
    blob = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 0 or "CHECKER_DIGEST_SIGNATURE:NOT_MET" not in blob:
        print(f"ASSERT:FAIL tag verifier accepted unsigned digest: {blob}")
        return 1
    if "missing sidecar" not in blob:
        print(f"ASSERT:FAIL unsigned digest was refused for another reason: {blob}")
        return 1
    print("ASSERT:PASS unsigned checker digest is refused by the tag verifier")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
