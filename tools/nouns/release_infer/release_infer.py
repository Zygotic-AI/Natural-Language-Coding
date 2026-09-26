"""Infer hub ./release target from git state (zero-parameter human surface)."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from nlc_release_tags import (  # noqa: E402
    canonical_tag_commit,
    last_shipped_version,
    parse_semver,
)
from nouns.release_bump import bump_semver, read_version, suggest_bump  # noqa: E402
from nouns.release_main_purity import evaluate_main_purity  # noqa: E402

BOUNDARY = "bba-emit"

HUB_ROOT = Path(__file__).resolve().parents[3]


def _git(*args: str, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def current_branch(root: Path) -> str:
    proc = _git("rev-parse", "--abbrev-ref", "HEAD", root=root)
    return (proc.stdout or "").strip() or "HEAD"


def release_branch_name(version: str) -> str:
    return f"release/v{version}"


def version_from_release_branch(branch: str) -> str | None:
    m = re.match(r"^release/v(\d+\.\d+\.\d+)$", branch)
    return m.group(1) if m else None


def branch_exists(name: str, root: Path) -> bool:
    return _git("show-ref", "--verify", "--quiet", f"refs/heads/{name}", root=root).returncode == 0


@dataclass
class InferPlan:
    phase: str
    bump: str
    target_version: str
    release_branch: str
    action: str
    source_branch: str
    reasons: list[str] = field(default_factory=list)
    block: bool = False
    block_problem: str = ""
    block_gaps: list[str] = field(default_factory=list)
    work_branch: str = ""
    shipped_tag: str = ""
    shipped_commit: str = ""

    def infer_line(self) -> str:
        why = "; ".join(self.reasons) if self.reasons else "resume or branch state"
        return (
            f"RELEASE:INFER target={self.target_version} "
            f"branch={self.release_branch} bump={self.bump} ({why})"
        )


def plan_target_version(
    shipped_ver: str | None,
    json_ver: str,
    suggest_level: str,
) -> tuple[str, str, list[str]]:
    """Pure: choose target semver and bump class."""
    reasons: list[str] = []
    if shipped_ver is None:
        shipped_ver = json_ver
        reasons.append("no shipped tag; using integrity/nlc-version.json")
    if parse_semver(json_ver) > parse_semver(shipped_ver):
        reasons.append(f"version file {json_ver} ahead of shipped {shipped_ver}")
        return json_ver, "keep", reasons
    target = bump_semver(shipped_ver, suggest_level)
    reasons.append(f"suggest_bump={suggest_level} from shipped {shipped_ver}")
    return target, suggest_level, reasons


def plan_next_release_target(
    shipped_ver: str | None,
    json_ver: str,
) -> tuple[str, str, list[str]]:
    """Next semver to ship after last shipped tag (never re-offer an already-shipped version)."""
    level, suggest_reasons = suggest_bump()
    target, bump, reasons = plan_target_version(shipped_ver, json_ver, level)
    reasons = list(suggest_reasons) + reasons
    if shipped_ver and parse_semver(target) <= parse_semver(shipped_ver):
        target = bump_semver(shipped_ver, "patch")
        bump = "patch"
        reasons.append("next target must be after last shipped tag")
    return target, bump, reasons


def plan_prepare_action(
    branch: str,
    target: str,
    release_branch: str,
    branch_exists_fn: Callable[[str], bool],
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if branch == release_branch:
        return "stay", ["already on release line"]
    if branch_exists_fn(release_branch):
        reasons.append(f"merge {branch} into existing {release_branch}")
        return "merge_into_release", reasons
    reasons.append(f"create {release_branch} from {branch}")
    return "create_release_from_head", reasons


def infer_release(
    hub: Path,
    remote: str = "origin",
    base: str = "main",
    resume: dict | None = None,
    bump_override: str | None = None,
    as_branch: str | None = None,
) -> InferPlan:
    from nlc_release_resume import detect

    hub = hub.resolve()
    branch = (as_branch or "").strip() or current_branch(hub)
    state = resume if resume is not None else detect(remote, base)
    phase = state.get("phase") or "prepare"

    if phase in ("tag_ready", "await_merge", "complete"):
        ver = state.get("version") or read_version()
        rb = state.get("release_branch") or release_branch_name(ver)
        action = "tag_only" if phase == "tag_ready" else "await_merge"
        if phase == "complete":
            action = "complete"
        return InferPlan(
            phase=phase,
            bump="keep",
            target_version=ver,
            release_branch=rb,
            action=action,
            source_branch=branch,
            reasons=[f"resume phase={phase}"],
        )

    shipped_ver = last_shipped_version(f"{remote}/{base}", root=hub) or last_shipped_version(
        base, root=hub
    )
    json_ver = read_version()

    if branch == base:
        next_target, next_bump, next_reasons = plan_next_release_target(shipped_ver, json_ver)
        ok, probs, shipped_tag, _head = evaluate_main_purity(hub, remote=remote, base=base)
        if not ok:
            work_branch = f"work/{next_target}"
            shipped_commit = (
                canonical_tag_commit(shipped_tag, remote, hub) if shipped_tag else ""
            )
            reasons = ["main impure; orchestrator normalizes trunk (ADR 0044)"] + next_reasons
            return InferPlan(
                phase="prepare",
                bump=next_bump,
                target_version=next_target,
                release_branch=release_branch_name(next_target),
                action="normalize_main_trunk",
                source_branch=branch,
                reasons=reasons,
                block=False,
                work_branch=work_branch,
                shipped_tag=shipped_tag or "",
                shipped_commit=shipped_commit,
            )
        return InferPlan(
            phase="prepare",
            bump=next_bump,
            target_version=next_target,
            release_branch=release_branch_name(next_target),
            action="blocked",
            source_branch=branch,
            block=True,
            block_problem="no release work on main",
            block_gaps=[
                "Create a branch from main, commit your changes, then run ./release from that branch"
            ],
            reasons=["blocked on main (no work)"] + next_reasons,
        )

    ver_from_branch = version_from_release_branch(branch)
    if ver_from_branch:
        target = ver_from_branch
        bump = "keep"
        reasons = [f"release line branch {branch}"]
        if parse_semver(json_ver) != parse_semver(target):
            reasons.append(
                f"note: integrity/nlc-version.json is {json_ver}; bump step may align to {target}"
            )
    else:
        level, suggest_reasons = suggest_bump()
        target, bump, reasons = plan_target_version(shipped_ver, json_ver, level)
        reasons = suggest_reasons + reasons

    if bump_override:
        bump = bump_override
        if bump == "keep":
            target = json_ver
        else:
            base_ver = shipped_ver or json_ver
            target = bump_semver(base_ver, bump)

    release_branch = release_branch_name(target)

    def _exists(name: str) -> bool:
        return branch_exists(name, hub)

    action, action_reasons = plan_prepare_action(branch, target, release_branch, _exists)
    reasons.extend(action_reasons)

    return InferPlan(
        phase="prepare",
        bump=bump,
        target_version=target,
        release_branch=release_branch,
        action=action,
        source_branch=branch,
        reasons=reasons,
    )


def emit_shell(plan: InferPlan) -> None:
    print(f"INFER_PHASE={shlex.quote(plan.phase)}")
    print(f"INFER_BUMP={shlex.quote(plan.bump)}")
    print(f"INFER_TARGET={shlex.quote(plan.target_version)}")
    print(f"INFER_RELEASE_BRANCH={shlex.quote(plan.release_branch)}")
    print(f"INFER_ACTION={shlex.quote(plan.action)}")
    print(f"INFER_SOURCE_BRANCH={shlex.quote(plan.source_branch)}")
    print(f"INFER_WORK_BRANCH={shlex.quote(plan.work_branch)}")
    print(f"INFER_SHIPPED_TAG={shlex.quote(plan.shipped_tag)}")
    print(f"INFER_SHIPPED_COMMIT={shlex.quote(plan.shipped_commit)}")
    print(f"INFER_BLOCK={'1' if plan.block else '0'}")
    if plan.block:
        print(f"INFER_BLOCK_PROBLEM={shlex.quote(plan.block_problem)}")
        print(f"INFER_BLOCK_GAPS={shlex.quote('|'.join(plan.block_gaps))}")
    line = plan.infer_line()
    print(f"INFER_LINE={shlex.quote(line)}")
    print(line, file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    from nlc_requirements import hub_tool

    hub_tool()
    args_list = argv if argv is not None else sys.argv[1:]
    import argparse

    parser = argparse.ArgumentParser(description="Infer hub ./release plan")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    parser.add_argument("--emit", choices=("shell", "json"), default="shell")
    parser.add_argument("--bump-override", default="", help="Automation only")
    parser.add_argument("--as-branch", default="", help="Orchestrator: infer as if on this branch")
    args = parser.parse_args(args_list)

    override = args.bump_override.strip() or None
    as_branch = args.as_branch.strip() or None
    plan = infer_release(
        HUB_ROOT,
        remote=args.remote,
        base=args.base,
        bump_override=override,
        as_branch=as_branch,
    )

    if args.emit == "json":
        print(
            json.dumps(
                {
                    "phase": plan.phase,
                    "bump": plan.bump,
                    "target_version": plan.target_version,
                    "release_branch": plan.release_branch,
                    "action": plan.action,
                    "source_branch": plan.source_branch,
                    "reasons": plan.reasons,
                    "block": plan.block,
                    "block_problem": plan.block_problem,
                    "block_gaps": plan.block_gaps,
                    "infer_line": plan.infer_line(),
                }
            )
        )
        return 1 if plan.block else 0

    emit_shell(plan)
    return 1 if plan.block else 0


if __name__ == "__main__":
    sys.exit(main())
