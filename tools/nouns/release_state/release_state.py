"""Release identity planner. Facts in, one legal action out. No git I/O."""

from __future__ import annotations

BOUNDARY = "bba-emit"

from typing import Any


def annotated_tag_argv(tag: str, merge_sha: str, message: str) -> list[str]:
    """Annotated tag on an explicit commit. Never tags HEAD by omission."""
    if not tag or not merge_sha:
        raise ValueError("tag and merge_sha are required")
    return ["git", "tag", "-a", tag, "-m", message, merge_sha]


def _s(facts: dict[str, Any], key: str) -> str:
    value = facts.get(key)
    return "" if value is None else str(value).strip()


def _b(facts: dict[str, Any], key: str) -> bool:
    return bool(facts.get(key))


def _list(facts: dict[str, Any], key: str) -> list[Any]:
    value = facts.get(key) or []
    return list(value)


def desired_from_branch(branch: str) -> str:
    prefix = "release/v"
    if branch.startswith(prefix):
        body = branch[len(prefix) :]
        parts = body.split(".")
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            return body
    return ""


def _decision(
    *,
    phase: str,
    action: str,
    desired_version: str,
    desired_branch: str,
    planned_tag: str,
    merge_sha: str = "",
    blockers: list[str] | None = None,
    problem: str = "",
    fixes: list[str] | None = None,
    allow_local_main_repoint: bool = False,
) -> dict[str, Any]:
    codes = blockers or []
    return {
        "phase": phase,
        "action": action if not codes else "BLOCKED",
        "desired_version": desired_version,
        "desired_branch": desired_branch,
        "planned_tag": planned_tag,
        "merge_sha": merge_sha,
        "blockers": codes,
        "problem": problem,
        "fixes": fixes or [],
        "allow_local_main_repoint": allow_local_main_repoint and not codes,
    }


def _blocked(
    code: str,
    problem: str,
    fixes: list[str],
    *,
    desired_version: str = "",
    desired_branch: str = "",
    planned_tag: str = "",
    extra: list[str] | None = None,
) -> dict[str, Any]:
    return _decision(
        phase="BLOCKED",
        action="BLOCKED",
        desired_version=desired_version,
        desired_branch=desired_branch,
        planned_tag=planned_tag,
        blockers=[code, *(extra or [])],
        problem=problem,
        fixes=fixes,
    )


def next_prepare_action(facts: dict[str, Any], desired: str) -> str | None:
    """ADR 0022 order. None means the candidate commit is ready to publish as a branch."""
    if not _b(facts, "migrations_ready"):
        return "ENSURE_MIGRATIONS"
    if not _b(facts, "shipped_verify_met"):
        return "VERIFY_SHIPPED_BASELINE"
    if not _b(facts, "notes_valid"):
        return "WRITE_NOTES"
    if _s(facts, "worktree_file_version") != desired:
        return "ALIGN_VERSION"
    if not _b(facts, "target_verify_met"):
        return "VERIFY_TARGET"
    if not _b(facts, "prep_met"):
        return "PREP"
    if _s(facts, "candidate_record_version") != desired or _s(
        facts, "candidate_record_branch"
    ) != f"release/v{desired}":
        return "WRITE_RECORD"
    if _b(facts, "dirty") or _s(facts, "head_file_version") != desired:
        return "COMMIT"
    return None


def _exact_prs(facts: dict[str, Any], candidate_sha: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for row in _list(facts, "pull_requests"):
        if not isinstance(row, dict):
            continue
        if str(row.get("head_sha") or "") == candidate_sha:
            matches.append(row)
    return matches


def _identity_ok(row: dict[str, Any], desired: str, branch: str) -> bool:
    return (
        str(row.get("merge_file_version") or "") == desired
        and str(row.get("merge_record_version") or "") == desired
        and str(row.get("merge_record_branch") or "") == branch
    )


def _publish_decision(
    facts: dict[str, Any],
    *,
    desired: str,
    branch: str,
    tag: str,
    merge_sha: str,
) -> dict[str, Any]:
    local_peel = _s(facts, "local_tag_peeled_sha")
    remote_peel = _s(facts, "remote_tag_peeled_sha")
    if local_peel and local_peel != merge_sha:
        return _blocked(
            "BLOCKED_TAG_WRONG",
            f"Local {tag} peels to {local_peel[:12]}, not merge {merge_sha[:12]}.",
            [f"Do not move {tag}. Fix the candidate and create a new tag name only with a new release."],
            desired_version=desired,
            desired_branch=branch,
            planned_tag=tag,
        )
    if remote_peel and remote_peel != merge_sha:
        return _blocked(
            "BLOCKED_TAG_WRONG",
            f"Remote {tag} peels to {remote_peel[:12]}, not merge {merge_sha[:12]}.",
            [f"Do not move {tag}."],
            desired_version=desired,
            desired_branch=branch,
            planned_tag=tag,
        )
    if remote_peel == merge_sha:
        publish = _s(facts, "publish_status") or "missing"
        if publish == "success":
            return _decision(
                phase="SHIPPED_COMPLETE",
                action="NONE",
                desired_version=desired,
                desired_branch=branch,
                planned_tag=tag,
                merge_sha=merge_sha,
            )
        if publish == "failed":
            return _decision(
                phase="PUBLISH_FAILED",
                action="RETRY_PUBLISH",
                desired_version=desired,
                desired_branch=branch,
                planned_tag=tag,
                merge_sha=merge_sha,
                problem=f"{tag} is on {merge_sha[:12]} but GitHub Release publication failed.",
                fixes=[
                    "Re-run the tag workflow or create the GitHub Release from that existing tag.",
                    "Do not move the tag.",
                ],
            )
        return _decision(
            phase="TAGGED_PUBLISH_PENDING",
            action="OBSERVE_PUBLISH",
            desired_version=desired,
            desired_branch=branch,
            planned_tag=tag,
            merge_sha=merge_sha,
        )
    if local_peel == merge_sha:
        return _decision(
            phase="TAG_CREATED_LOCAL",
            action="PUSH_TAG",
            desired_version=desired,
            desired_branch=branch,
            planned_tag=tag,
            merge_sha=merge_sha,
        )
    return _decision(
        phase="TAG_READY",
        action="CREATE_LOCAL_TAG",
        desired_version=desired,
        desired_branch=branch,
        planned_tag=tag,
        merge_sha=merge_sha,
    )


def executor_permits(decision: dict[str, Any], mutation: str) -> bool:
    """Mutations the executor may perform for this decision. Retag is never permitted."""
    if mutation in {"force_tag", "stash", "detach_checkout"}:
        return False
    if decision.get("action") == "BLOCKED" or decision.get("phase") in {"BLOCKED", "INVALID_MERGED"}:
        return False
    if mutation == "repoint_local_main":
        return bool(decision.get("allow_local_main_repoint"))
    if mutation == "create_tag":
        return decision.get("action") == "CREATE_LOCAL_TAG" and bool(decision.get("merge_sha"))
    if mutation == "push_tag":
        return decision.get("action") == "PUSH_TAG" and bool(decision.get("merge_sha"))
    if mutation == "retry_publish":
        return decision.get("action") == "RETRY_PUBLISH"
    if mutation == "prepare":
        return decision.get("action") in {
            "ENSURE_MIGRATIONS",
            "VERIFY_SHIPPED_BASELINE",
            "WRITE_NOTES",
            "ALIGN_VERSION",
            "VERIFY_TARGET",
            "PREP",
            "WRITE_RECORD",
            "COMMIT",
            "PUSH_NEW",
            "PUSH_FAST_FORWARD",
            "CREATE_PR",
            "CREATE_RELEASE_LINE",
        }
    return False


def plan_release(facts: dict[str, Any]) -> dict[str, Any]:
    if not _b(facts, "remote_known"):
        return _blocked(
            "BLOCKED_REMOTE_UNKNOWN",
            "Remote release facts are unavailable.",
            ["git fetch origin --prune --tags", "Re-run ./release"],
        )

    branch = _s(facts, "local_branch")
    desired = desired_from_branch(branch) or _s(facts, "desired_version")
    if not desired:
        if _list(facts, "active_release_branches"):
            return _blocked(
                "BLOCKED_MULTIPLE",
                "HEAD is not a release line and more than one active release branch is open.",
                ["Checkout the one release/vX.Y.Z line you intend to ship, then re-run ./release"],
            )
        return _decision(
            phase="PREPARE_DRAFT",
            action="CREATE_RELEASE_LINE",
            desired_version="",
            desired_branch="",
            planned_tag="",
            problem="No release/vX.Y.Z line exists yet.",
            fixes=["./release will create the inferred release line. Do not tag main."],
        )
    release_branch = f"release/v{desired}"
    tag = f"v{desired}"
    if "pr_list_known" in facts and not _b(facts, "pr_list_known"):
        return _blocked(
            "BLOCKED_REMOTE_UNKNOWN",
            f"Pull requests for {release_branch} could not be listed.",
            ["gh pr list --head " + release_branch, "Re-run ./release"],
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
        )
    active = [
        name
        for name in _list(facts, "active_release_branches")
        if str(name) != release_branch
    ]
    if active:
        return _blocked(
            "BLOCKED_MULTIPLE",
            "More than one active release line is open.",
            [
                "Leave only one active release/vX.Y.Z branch.",
                "Closed tagged lines stay; do not retag them.",
                "Re-run ./release",
            ],
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
            extra=[f"branch:{name}" for name in active],
        )

    relation = _s(facts, "remote_relation") or "absent"
    if relation == "unknown":
        return _blocked(
            "BLOCKED_REMOTE_UNKNOWN",
            f"Cannot compare local {release_branch} with origin.",
            ["git fetch origin --prune", "Re-run ./release"],
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
        )
    if relation == "behind":
        return _blocked(
            "BLOCKED_REMOTE_AHEAD",
            f"origin/{release_branch} has commits the local branch does not.",
            [f"git fetch origin {release_branch}", f"git merge origin/{release_branch}", "./release"],
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
        )
    if relation == "diverged":
        return _blocked(
            "BLOCKED_DIVERGED",
            f"Local {release_branch} diverged from origin/{release_branch}.",
            ["Reconcile without force-push, then re-run ./release"],
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
        )

    candidate = _s(facts, "candidate_sha")
    exact = _exact_prs(facts, candidate)
    if len(exact) > 1:
        return _blocked(
            "BLOCKED_MULTIPLE_PRS",
            f"More than one pull request matches candidate {candidate[:12]}.",
            ["Close or distinguish the extra PRs so one head SHA remains, then re-run ./release"],
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
        )

    shipped_sha = _s(facts, "shipped_tag_sha")
    origin_main = _s(facts, "origin_main_sha")
    rejected = [
        row
        for row in _list(facts, "pull_requests")
        if isinstance(row, dict)
        and str(row.get("state") or "") == "merged"
        and not _identity_ok(row, desired, release_branch)
    ]
    allow_repoint = (
        not rejected
        and bool(shipped_sha)
        and origin_main == shipped_sha
        and relation in {"absent", "equal", "ahead"}
    )

    if len(exact) == 1 and str(exact[0].get("state") or "") == "merged":
        row = exact[0]
        merge_sha = str(row.get("merge_sha") or "")
        if not _identity_ok(row, desired, release_branch):
            action = next_prepare_action(facts, desired) or "COMMIT"
            return _decision(
                phase="INVALID_MERGED",
                action=action,
                desired_version=desired,
                desired_branch=release_branch,
                planned_tag=tag,
                merge_sha=merge_sha,
                problem=(
                    f"Merged {merge_sha[:12]} for {release_branch} does not have "
                    f"version {desired} in the version file, record, and branch together."
                ),
                fixes=[
                    f"Do not tag {merge_sha[:12]}.",
                    f"Repair on {release_branch}: align integrity/nlc-version.json to {desired}, commit, push, open a new PR.",
                    "Re-run ./release",
                ],
                allow_local_main_repoint=False,
            )
        if not merge_sha:
            return _blocked(
                "BLOCKED_MERGE_SHA_MISSING",
                "The merged pull request has no merge commit SHA.",
                ["Inspect the PR and re-run ./release"],
                desired_version=desired,
                desired_branch=release_branch,
                planned_tag=tag,
            )
        decision = _publish_decision(
            facts,
            desired=desired,
            branch=release_branch,
            tag=tag,
            merge_sha=merge_sha,
        )
        decision["allow_local_main_repoint"] = False
        return decision

    prepare = next_prepare_action(facts, desired)
    if prepare is not None:
        return _decision(
            phase="PREPARE_DRAFT" if prepare != "COMMIT" else "PREPARE_DRAFT",
            action=prepare,
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
            allow_local_main_repoint=allow_repoint,
        )

    if relation == "absent":
        return _decision(
            phase="CANDIDATE_READY_LOCAL",
            action="PUSH_NEW",
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
            allow_local_main_repoint=allow_repoint,
        )
    if relation == "ahead":
        return _decision(
            phase="CANDIDATE_READY_LOCAL",
            action="PUSH_FAST_FORWARD",
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
            allow_local_main_repoint=allow_repoint,
        )

    if len(exact) == 0:
        return _decision(
            phase="AWAIT_PR",
            action="CREATE_PR",
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
            allow_local_main_repoint=False,
        )
    row = exact[0]
    if str(row.get("state") or "") == "open":
        number = row.get("number")
        return _decision(
            phase="AWAIT_PR",
            action="EXIT_AWAIT",
            desired_version=desired,
            desired_branch=release_branch,
            planned_tag=tag,
            problem=f"Pull request #{number} is open.",
            fixes=[
                f"Merge pull request #{number} when CI is green.",
                "Re-run ./release",
            ],
            allow_local_main_repoint=False,
        )
    return _blocked(
        "BLOCKED_PR_STATE",
        f"Pull request state {row.get('state')!r} is not actionable.",
        ["Open one pull request for this candidate SHA, then re-run ./release"],
        desired_version=desired,
        desired_branch=release_branch,
        planned_tag=tag,
    )
