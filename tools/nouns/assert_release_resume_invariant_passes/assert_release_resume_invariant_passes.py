"""Resume tag_ready requires hub-release-record on merge commit (RCA 26-09-24)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_release_record import git_show_json  # noqa: E402
from nlc_release_resume import (  # noqa: E402
    _is_full_sha,
    detect,
    remote_branch_exists,
    resolve_ref_sha,
)


def main() -> int:
    _ = sys.argv[1:]
    ghost = resolve_ref_sha("origin/release/v0.3.0")
    if ghost and not _is_full_sha(ghost):
        print("ASSERT:FAIL resolve_ref_sha must not treat ref name as commit")
        return 1
    state = detect("origin", "main")
    phase = state.get("phase") or ""
    merge = str(state.get("merge_commit") or "")
    if phase == "tag_ready":
        if not merge or git_show_json(merge, "integrity/hub-release-record.json") is None:
            print("ASSERT:FAIL tag_ready without hub-release-record on merge commit")
            return 1
    stale = state.get("stale_release_branches") or []
    closed = state.get("closed_release_branches") or []
    if phase == "tag_ready" and stale:
        print("ASSERT:FAIL tag_ready with stale_release_branches set")
        return 1
    if phase == "await_merge":
        rel = str(state.get("release_branch") or "")
        if rel and not remote_branch_exists("origin", rel):
            print("ASSERT:FAIL await_merge without remote release branch")
            return 1
    overlap = set(stale) & set(closed)
    if overlap:
        print(f"ASSERT:FAIL branch in both stale and closed: {overlap}")
        return 1
    print(f"ASSERT:PASS resume phase={phase} stale={len(stale)} closed={len(closed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
