"""Landmine: release identity planner oracles and tag-target executor."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from nouns.release_state import (  # noqa: E402
    ACTION_KINDS,
    ACTION_PROGRESS_FACTS,
    action_progress,
    annotated_tag_argv,
    executor_permits,
    plan_release,
    present_resume_phase,
)

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
        "main_context": "contained",
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


def _merged_tip_with_newer_local_stays_in_prepare() -> bool:
    """Remote release tip is merged; local release branch has newer commits."""
    old_tip = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    decision = plan_release(
        _facts(
            remote_relation="ahead",
            shipped_verify_met=False,
            pull_requests=[
                {
                    "number": 55,
                    "state": "merged",
                    "head_sha": old_tip,
                    "merge_sha": MERGE,
                    "merge_file_version": "0.2.0",
                    "merge_record_version": "0.2.0",
                    "merge_record_branch": "release/v0.2.0",
                }
            ],
        )
    )
    presented = present_resume_phase(decision)
    if decision["phase"] != "PREPARE_DRAFT" or decision["action"] != "VERIFY_SHIPPED_BASELINE":
        print(
            f"ASSERT:FAIL newer local branch phase={decision['phase']} action={decision['action']}"
        )
        return False
    if presented == "tag_ready":
        print("ASSERT:FAIL merged older tip selected tagging")
        return False
    shell = Path(__file__).resolve().parents[3] / "goals" / "hub_release" / "execute.sh"
    text = shell.read_text(encoding="utf-8")
    if "Resume: merged" in text or "tagging ${RESUME_TAG}" in text:
        print("ASSERT:FAIL executor still prints a tagging resume")
        return False
    if "for iteration in $(seq 1 64)" not in text or "dispatch_release_plan" not in text:
        print("ASSERT:FAIL planner action loop is not handled")
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
    elif executor_permits(invalid, "create_tag") or executor_permits(invalid, "force_tag"):
        print("ASSERT:FAIL invalid-merged permitted tag or retag")
        ok = False
    invalid_prepared = plan_release(
        _facts(
            pull_requests=[
                {
                    "number": 55,
                    "state": "merged",
                    "head_sha": HEAD,
                    "merge_sha": MERGE,
                    "merge_file_version": "0.2.0",
                    "merge_record_version": "0.2.0",
                    "merge_record_branch": "release/v0.3.0",
                }
            ]
        )
    )
    if (
        invalid_prepared["phase"] != "INVALID_MERGED"
        or invalid_prepared["action"] != "CREATE_REPAIR_COMMIT"
        or invalid_prepared["action_kind"] != "REPAIR"
        or not executor_permits(invalid_prepared, "prepare")
    ):
        print(f"ASSERT:FAIL prepared invalid merge {invalid_prepared}")
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
            phase="PREPARE_DRAFT",
            action="FAST_FORWARD_LOCAL",
        )
        and ok
    )
    behind = plan_release(_facts(remote_relation="behind"))
    if behind["action_kind"] != "REPAIR":
        print(f"ASSERT:FAIL remote-ahead kind {behind['action_kind']}")
        ok = False
    diverged = plan_release(_facts(remote_relation="diverged"))
    if "BLOCKED_DIVERGED" not in diverged["blockers"] or executor_permits(diverged, "prepare"):
        print("ASSERT:FAIL diverged")
        ok = False
    unknown = plan_release(_facts(remote_known=False))
    if unknown["action"] != "FETCH_REMOTE" or unknown["action_kind"] != "REPAIR":
        print("ASSERT:FAIL unknown")
        ok = False
    context_unknown = plan_release(_facts(main_context="unknown"))
    if (
        context_unknown["action"] != "BLOCKED"
        or context_unknown["action_kind"] != "HUMAN_DECISION"
        or "BLOCKED_MAIN_CONTEXT_UNKNOWN" not in context_unknown["blockers"]
    ):
        print("ASSERT:FAIL unknown main context")
        ok = False
    failed = plan_release(_facts(failed_action="VERIFY_TARGET"))
    if (
        failed["action"] != "BLOCKED"
        or "BLOCKED_VERIFY_TARGET_FAILED" not in failed["blockers"]
    ):
        print("ASSERT:FAIL failed repair fact")
        ok = False
    stalled = plan_release(_facts(stalled_action="VERIFY_TARGET"))
    if (
        stalled["action"] != "BLOCKED"
        or "BLOCKED_VERIFY_TARGET_STALLED" not in stalled["blockers"]
    ):
        print("ASSERT:FAIL stalled repair fact")
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
    repairs = {action for action, kind in ACTION_KINDS.items() if kind == "REPAIR"}
    if repairs != set(ACTION_PROGRESS_FACTS) or not all(ACTION_PROGRESS_FACTS.values()):
        print("ASSERT:FAIL repair progress fact coverage")
        ok = False
    for action, names in ACTION_PROGRESS_FACTS.items():
        _, before = action_progress(action, _facts())
        changed = _facts(**{names[0]: "progress-sentinel"})
        _, after = action_progress(action, changed)
        if before == after:
            print(f"ASSERT:FAIL repair progress token action={action}")
            ok = False
    if not _tag_targets_named_commit():
        ok = False
    if not _merged_tip_with_newer_local_stays_in_prepare():
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
