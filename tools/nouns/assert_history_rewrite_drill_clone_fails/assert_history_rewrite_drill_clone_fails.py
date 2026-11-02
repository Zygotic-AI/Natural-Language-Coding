"""Known-bad: history drill clone must surface git stderr and refuse fail-closed."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import io
import os
import sys
import tempfile
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.assert_history_rewrite_invariant_passes.assert_history_rewrite_invariant_passes import (  # noqa: E402
    drill_git_clone,
    resolve_drill_git,
)


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def _bad_clone_surfaces_stderr() -> int | None:
    with tempfile.TemporaryDirectory(prefix="nlc-drill-clone-fail-") as tmp:
        dest = Path(tmp) / "dest"
        git_cmd = resolve_drill_git()
        if git_cmd is None:
            return _fail("expected working git for bad-clone case")
        buf = io.StringIO()
        with redirect_stderr(buf):
            rc = drill_git_clone(
                git_cmd,
                "/nonexistent/nlc-history-drill-clone-source",
                dest,
            )
        blob = buf.getvalue()
        if rc == 0:
            return _fail("bad clone source must exit nonzero")
        if "fatal:" not in blob.lower() and "error" not in blob.lower():
            return _fail(f"expected git stderr in job log, got {blob!r}")
    return None


def _missing_git_refuses() -> int | None:
    env = {"NLC_DRILL_GIT": "/nonexistent/nlc-history-drill-git-binary"}
    if resolve_drill_git(env) is not None:
        return _fail("missing git binary must resolve to unknown")
    return None


def _empty_version_refuses() -> int | None:
    with tempfile.TemporaryDirectory(prefix="nlc-drill-empty-git-") as tmp:
        fake = Path(tmp) / "git-empty-version"
        fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        fake.chmod(0o755)
        env = {**os.environ, "NLC_DRILL_GIT": str(fake)}
        if resolve_drill_git(env) is not None:
            return _fail("empty git --version must refuse as unknown")
    return None


def main() -> int:
    for check in (_bad_clone_surfaces_stderr, _missing_git_refuses, _empty_version_refuses):
        err = check()
        if err is not None:
            return err
    print("ASSERT:PASS history-rewrite drill clone fail-closed landmines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
