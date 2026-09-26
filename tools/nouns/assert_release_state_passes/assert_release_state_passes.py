"""Landmine: release identity planner oracles and tag-target executor."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from nouns.release_state import annotated_tag_argv, executor_permits, plan_release  # noqa: E402

BOUNDARY = "bba-emit"

MERGE = "ddd99726c051e377d926ee26b0144ac8a449d91a"
HEAD = "0ca1bceb0ae434543e10a55b520e5afa15a64944"
SHIPPED = "023bad16c1ff969d5c3b760fcaa131bf2828fa3c"
GOOD_MERGE = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def _facts(**overrides: object) -> dict:
    base = {
        "remote_known": True,
        "pr_list_known": True,
        "local_branch": "release/v0.3.0",
        "candidate_sha": HEAD,
        "dirty": False,
        "worktree_file_version": "0.3.0",
        "head_file_version": "0.3.0",
        "candidate_record_version": "0.3.0",
        "candidate_record_branch": "release/v0.3.0",
        "remote_relation": "equal",
        "active_release_branches": ["release/v0.3.0"],
        "pull_requests": [],
        "origin_main_sha": SHIPPED,
        "shipped_tag_sha": SHIPPED,
        "local_tag_peeled_sha": "",
        "remote_tag_peeled_sha": "",
        "publish_status": "missing",
        "migrations_ready": True,
        "shipped_verify_met": True,
        "notes_valid": True,
        "target_verify_met": True,
        "prep_met": True,
    }
    base.update(overrides)
    return base


def _expect(name: str, facts: dict, *, phase: str, action: str) -> bool:
    decision = plan_release(facts)
    if decision["phase"] != phase or decision["action"] != action:
        print(
            f"ASSERT:FAIL {name} phase={decision['phase']} action={decision['action']} "
            f"want {phase}/{action} blockers={decision['blockers']}"
        )
        return False
    return True


def _tag_targets_named_commit() -> bool:
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        env_git = ["git", "-C", str(root)]

        def git(*args: str) -> str:
            proc = subprocess.run([*env_git, *args], check=True, capture_output=True, text=True)
            return proc.stdout.strip()

        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "release-state@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "release-state"], cwd=root, check=True)
        (root / "f").write_text("a\n", encoding="utf-8")
        subprocess.run(["git", "add", "f"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "first"], cwd=root, check=True)
        first = git("rev-parse", "HEAD")
        (root / "f").write_text("b\n", encoding="utf-8")
        subprocess.run(["git", "add", "f"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "second"], cwd=root, check=True)
        subprocess.run(annotated_tag_argv("v9.9.9", first, "hub 9.9.9"), cwd=root, check=True)
        peel = git("rev-parse", "v9.9.9^{commit}")
        if peel != first:
            print(f"ASSERT:FAIL tag peel {peel} != merge {first}")
            return False
        if "git" not in annotated_tag_argv("v1.2.3", first, "m")[0]:
            print("ASSERT:FAIL tag argv")
            return False
        if annotated_tag_argv("v1.2.3", first, "m")[-1] != first:
            print("ASSERT:FAIL tag argv omits commit")
            return False
    return True


def main() -> int:
    ok = True
    ok = _expect(
        "prepare-align",
        _facts(
            worktree_file_version="0.2.0",
            head_file_version="0.2.0",
            remote_relation="absent",
            pull_requests=[],
        ),
        phase="PREPARE_DRAFT",
        action="ALIGN_VERSION",
    ) and ok
    ok = _expect(
        "verify-before-align",
        _facts(shipped_verify_met=False, worktree_file_version="0.2.0", remote_relation="absent"),
        phase="PREPARE_DRAFT",
        action="VERIFY_SHIPPED_BASELINE",
    ) and ok
    ok = _expect(
        "push-new",
        _facts(remote_relation="absent"),
        phase="CANDIDATE_READY_LOCAL",
        action="PUSH_NEW",
    ) and ok
    ok = _expect(
        "create-pr",
        _facts(remote_relation="equal"),
        phase="AWAIT_PR",
        action="CREATE_PR",
    ) and ok
    ok = _expect(
        "exit-await",
        _facts(
            pull_requests=[
                {
                    "number": 7,
                    "state": "open",
                    "head_sha": HEAD,
                    "merge_sha": "",
                    "merge_file_version": "",
                    "merge_record_version": "",
                    "merge_record_branch": "",
                }
            ]
        ),
        phase="AWAIT_PR",
        action="EXIT_AWAIT",
    ) and ok
    invalid = plan_release(
        _facts(
            worktree_file_version="0.2.0",
            head_file_version="0.2.0",
            candidate_record_version="0.3.0",
            origin_main_sha=MERGE,
            pull_requests=[
                {
                    "number": 55,
                    "state": "merged",
                    "head_sha": HEAD,
                    "merge_sha": MERGE,
                    "merge_file_version": "0.2.0",
                    "merge_record_version": "0.3.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ],
        )
    )
    if invalid["phase"] != "INVALID_MERGED" or invalid["action"] != "ALIGN_VERSION":
        print(f"ASSERT:FAIL invalid-merged {invalid['phase']} {invalid['action']}")
        ok = False
    elif invalid["allow_local_main_repoint"] or executor_permits(invalid, "create_tag"):
        print("ASSERT:FAIL invalid-merged permitted tag or main repoint")
        ok = False
    elif executor_permits(invalid, "repoint_local_main") or executor_permits(invalid, "force_tag"):
        print("ASSERT:FAIL invalid-merged permitted reset or retag")
        ok = False
    ready = plan_release(
        _facts(
            candidate_sha="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            pull_requests=[
                {
                    "number": 56,
                    "state": "merged",
                    "head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "merge_sha": GOOD_MERGE,
                    "merge_file_version": "0.3.0",
                    "merge_record_version": "0.3.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ],
        )
    )
    if ready["phase"] != "TAG_READY" or ready["action"] != "CREATE_LOCAL_TAG" or ready["merge_sha"] != GOOD_MERGE:
        print(f"ASSERT:FAIL tag-ready {ready}")
        ok = False
    elif not executor_permits(ready, "create_tag") or executor_permits(ready, "force_tag"):
        print("ASSERT:FAIL tag-ready permit")
        ok = False
    ok = _expect(
        "push-tag",
        _facts(
            candidate_sha="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            local_tag_peeled_sha=GOOD_MERGE,
            pull_requests=[
                {
                    "number": 56,
                    "state": "merged",
                    "head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "merge_sha": GOOD_MERGE,
                    "merge_file_version": "0.3.0",
                    "merge_record_version": "0.3.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ],
        ),
        phase="TAG_CREATED_LOCAL",
        action="PUSH_TAG",
    ) and ok
    shipped = plan_release(
        _facts(
            candidate_sha="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            local_tag_peeled_sha=GOOD_MERGE,
            remote_tag_peeled_sha=GOOD_MERGE,
            publish_status="success",
            pull_requests=[
                {
                    "number": 56,
                    "state": "merged",
                    "head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "merge_sha": GOOD_MERGE,
                    "merge_file_version": "0.3.0",
                    "merge_record_version": "0.3.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ],
        )
    )
    if shipped["phase"] != "SHIPPED_COMPLETE" or shipped["action"] != "NONE":
        print(f"ASSERT:FAIL shipped {shipped['phase']} {shipped['action']} {shipped['blockers']}")
        ok = False
    failed_pub = plan_release(
        _facts(
            candidate_sha="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            remote_tag_peeled_sha=GOOD_MERGE,
            publish_status="failed",
            pull_requests=[
                {
                    "number": 56,
                    "state": "merged",
                    "head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "merge_sha": GOOD_MERGE,
                    "merge_file_version": "0.3.0",
                    "merge_record_version": "0.3.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ],
        )
    )
    if failed_pub["phase"] != "PUBLISH_FAILED" or failed_pub["action"] != "RETRY_PUBLISH":
        print(f"ASSERT:FAIL retry-publish {failed_pub['phase']} {failed_pub['action']} {failed_pub['blockers']}")
        ok = False
    wrong = plan_release(
        _facts(
            candidate_sha="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            remote_tag_peeled_sha=SHIPPED,
            pull_requests=[
                {
                    "number": 56,
                    "state": "merged",
                    "head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "merge_sha": GOOD_MERGE,
                    "merge_file_version": "0.3.0",
                    "merge_record_version": "0.3.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ],
        )
    )
    if wrong["phase"] != "BLOCKED" or "BLOCKED_TAG_WRONG" not in wrong["blockers"]:
        print(f"ASSERT:FAIL wrong-tag {wrong['phase']} {wrong['blockers']}")
        ok = False
    elif executor_permits(wrong, "create_tag") or executor_permits(wrong, "force_tag"):
        print("ASSERT:FAIL wrong-tag permitted mutation")
        ok = False
    ok = (
        _expect(
            "remote-ahead",
            _facts(remote_relation="behind"),
            phase="BLOCKED",
            action="BLOCKED",
        )
        and ok
    )
    behind = plan_release(_facts(remote_relation="behind"))
    if "BLOCKED_REMOTE_AHEAD" not in behind["blockers"]:
        print(f"ASSERT:FAIL remote-ahead code {behind['blockers']}")
        ok = False
    diverged = plan_release(_facts(remote_relation="diverged"))
    if "BLOCKED_DIVERGED" not in diverged["blockers"] or executor_permits(diverged, "prepare"):
        print("ASSERT:FAIL diverged")
        ok = False
    unknown = plan_release(_facts(remote_known=False))
    if "BLOCKED_REMOTE_UNKNOWN" not in unknown["blockers"]:
        print("ASSERT:FAIL unknown")
        ok = False
    multi = plan_release(
        _facts(active_release_branches=["release/v0.3.0", "release/v0.4.0"])
    )
    if "BLOCKED_MULTIPLE" not in multi["blockers"]:
        print("ASSERT:FAIL multiple")
        ok = False
    two_prs = plan_release(
        _facts(
            pull_requests=[
                {
                    "number": 1,
                    "state": "open",
                    "head_sha": HEAD,
                    "merge_sha": "",
                    "merge_file_version": "",
                    "merge_record_version": "",
                    "merge_record_branch": "",
                },
                {
                    "number": 2,
                    "state": "open",
                    "head_sha": HEAD,
                    "merge_sha": "",
                    "merge_file_version": "",
                    "merge_record_version": "",
                    "merge_record_branch": "",
                },
            ]
        )
    )
    if "BLOCKED_MULTIPLE_PRS" not in two_prs["blockers"]:
        print("ASSERT:FAIL multiple prs")
        ok = False
    historical = plan_release(
        _facts(
            local_branch="release/v0.3.0",
            active_release_branches=["release/v0.3.0"],
            remote_relation="absent",
            worktree_file_version="0.2.0",
            head_file_version="0.2.0",
        )
    )
    if historical["desired_version"] != "0.3.0" or historical["planned_tag"] != "v0.3.0":
        print("ASSERT:FAIL historical identity")
        ok = False
    if not _tag_targets_named_commit():
        ok = False
    try:
        annotated_tag_argv("v1.0.0", "", "m")
        print("ASSERT:FAIL empty commit accepted")
        ok = False
    except ValueError:
        pass
    if not ok:
        return 1
    print("ASSERT:PASS release state planner")
    return 0


if __name__ == "__main__":
    sys.exit(main())
