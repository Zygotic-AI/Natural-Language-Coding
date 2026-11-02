"""Known-bad and known-good probes for the 22 fail-closed release-tool instances."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import os
import stat
import subprocess
import sys
import tempfile
import urllib.error
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))

from nouns.release_probe.release_probe import ProbeFailure  # noqa: E402

INSTANCES = (
    "main-purity",
    "tag-exists",
    "list-version-tags",
    "tag-is-ancestor",
    "remote-tag-commit-only",
    "align-local-tag-to-remote",
    "changelog-tag-exists",
    "branch-exists",
    "remote-branch-exists",
    "resolve-ref-sha",
    "tag-on-commit",
    "is-resolvable-commit",
    "release-state-out",
    "remote-branch-sha",
    "remote-known",
    "pull-requests",
    "publish-status",
    "publish-decision",
    "git-changed-paths",
    "github-latest-tag",
    "create-release-line-show-ref",
    "sig-ok",
)

SHA = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
SHA2 = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def _fail(msg: str) -> int:
    print(f"ASSERT:FAIL {msg}")
    return 1


def _ok(msg: str) -> int:
    print(f"ASSERT:PASS {msg}")
    return 0


def _proc(rc: int, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["git"], returncode=rc, stdout=stdout, stderr=stderr)


BASH = "/usr/bin/bash"


def _missing(argv: list[str] | None = None, **_kwargs: object) -> subprocess.CompletedProcess[str]:
    raise FileNotFoundError((argv or ["git"])[0])


def _empty(argv: list[str] | None = None, **_kwargs: object) -> subprocess.CompletedProcess[str]:
    return _proc(0, "")


def _boom(argv: list[str] | None = None, **_kwargs: object) -> subprocess.CompletedProcess[str]:
    return _proc(128, "", "fatal: unexpected")


def _expect_kinds(fn: Callable[[], object], kinds: set[str]) -> str | None:
    seen: set[str] = set()
    for kind, runner in (
        ("missing_tool", _missing),
        ("empty", _empty),
        ("unexpected_error", _boom),
    ):
        if kind not in kinds:
            continue
        try:
            fn.__globals__  # keep fn live for type checkers
            result = fn(runner)  # type: ignore[misc,call-arg]
        except TypeError:
            result = fn()
        except ProbeFailure as exc:
            if exc.kind != kind:
                return f"wanted kind={kind} got {exc.kind}: {exc}"
            seen.add(kind)
            continue
        return f"wanted ProbeFailure kind={kind}, got {result!r}"
    missing = kinds - seen
    if missing:
        return f"did not refuse kinds {sorted(missing)}"
    return None


def _scripted(answers: list[object]) -> Callable[..., subprocess.CompletedProcess[str]]:
    queue = list(answers)

    def runner(argv: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        if not queue:
            raise AssertionError(f"no scripted answer left for {argv}")
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        if callable(item):
            return item(argv, **_kwargs)
        return item  # type: ignore[return-value]

    return runner


def _init_repo(path: Path) -> str:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "probe@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "probe"], cwd=path, check=True)
    (path / "f").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "f"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "first"], cwd=path, check=True, capture_output=True)
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, check=True, capture_output=True, text=True
    )
    return proc.stdout.strip()


def _write_exec(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _run_probe_ref(branch: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [BASH, str(ROOT / "goals" / "hub_release" / "execute.sh"), "--probe-ref", branch],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )


def _run_probe_sig(doc: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [BASH, str(ROOT / "goals" / "sign_adrs" / "execute.sh"), "--probe-sig", str(doc)],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )


def _kinds_via_runner(
    call: Callable[..., object], kinds: set[str]
) -> str | None:
    mapping = {
        "missing_tool": _missing,
        "empty": _empty,
        "unexpected_error": _boom,
    }
    for kind in kinds:
        try:
            result = call(runner=mapping[kind])
        except ProbeFailure as exc:
            if exc.kind != kind:
                return f"wanted kind={kind} got {exc.kind}: {exc}"
            continue
        return f"wanted ProbeFailure kind={kind}, got {result!r}"
    return None


def fails_main_purity() -> int:
    from nouns.release_main_purity import check_main_purity, resolve_base_head

    ok, probs = check_main_purity(head=SHA, tag="v1.0.0", tag_at="")
    if ok or not probs:
        return _fail("empty tag_at must NOT_MET")
    ok2, _ = check_main_purity(head=SHA, tag="v1.0.0", tag_at=SHA2, tag_known=False)
    if ok2:
        return _fail("unknown tag probe must NOT_MET")
    err = _kinds_via_runner(
        lambda runner: resolve_base_head("origin", "main", ROOT, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("main-purity refuses empty/unknown/error")


def passes_main_purity() -> int:
    from nouns.release_main_purity import check_main_purity

    ok, probs = check_main_purity(head=SHA, tag="v1.0.0", tag_at=SHA)
    if not ok or probs:
        return _fail("head equals tag must MET")
    ok2, probs2 = check_main_purity(head=SHA, tag=None, tag_at="", tag_known=True)
    if not ok2 or probs2:
        return _fail("confirmed no shipped tag must MET")
    return _ok("main-purity known-good")


def fails_tag_exists() -> int:
    from nouns.release_tags import tag_exists

    err = _kinds_via_runner(
        lambda runner: tag_exists("v1.0.0", root=ROOT, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("tag-exists refuses")


def passes_tag_exists() -> int:
    from nouns.release_tags import tag_exists

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "-a", "v9.9.9", "-m", "t", sha], cwd=repo, check=True)
        if not tag_exists("v9.9.9", root=repo):
            return _fail("annotated tag must exist")
        if tag_exists("v0.0.0", root=repo):
            return _fail("missing tag must be confirmed false")
    return _ok("tag-exists known-good")


def fails_list_version_tags() -> int:
    from nouns.release_tags import list_version_tags

    err = _kinds_via_runner(
        lambda runner: list_version_tags(root=ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("list-version-tags refuses")


def passes_list_version_tags() -> int:
    from nouns.release_tags import list_version_tags

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "v1.2.3", sha], cwd=repo, check=True)
        tags = list_version_tags(root=repo)
        if tags != ["v1.2.3"]:
            return _fail(f"expected [v1.2.3] got {tags}")
    return _ok("list-version-tags known-good")


def fails_tag_is_ancestor() -> int:
    from nouns.release_tags import tag_is_ancestor

    err = _kinds_via_runner(
        lambda runner: tag_is_ancestor("v1.0.0", "HEAD", root=ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("tag-is-ancestor refuses")


def passes_tag_is_ancestor() -> int:
    from nouns.release_tags import tag_is_ancestor

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "v1.2.3", sha], cwd=repo, check=True)
        if not tag_is_ancestor("v1.2.3", "HEAD", root=repo):
            return _fail("tag on HEAD must be ancestor")
    return _ok("tag-is-ancestor known-good")


def fails_remote_tag_commit_only() -> int:
    from nouns.release_tags import remote_tag_commit_only

    err = _kinds_via_runner(
        lambda runner: remote_tag_commit_only("v1.0.0", root=ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("remote-tag-commit-only refuses")


def passes_remote_tag_commit_only() -> int:
    from nouns.release_tags import remote_tag_commit_only

    runner = _scripted([_proc(0, ""), _proc(0, f"{SHA}\trefs/tags/v1.2.3\n")])
    got = remote_tag_commit_only("v1.2.3", runner=runner)
    if got != SHA:
        return _fail(f"expected {SHA} got {got}")
    empty = remote_tag_commit_only("v1.2.3", runner=_scripted([_proc(0, ""), _proc(0, "")]))
    if empty != "":
        return _fail("confirmed absent remote tag must be empty string")
    return _ok("remote-tag-commit-only known-good")


def fails_align_local_tag_to_remote() -> int:
    from nouns.release_tags import align_local_tag_to_remote

    # Divergence confirmed, then fetch missing / empty / unexpected.
    def call(kind: str, runner: object) -> object:
        answers: list[object] = [
            _proc(0, SHA + "\n"),
            _proc(0, ""),
            _proc(0, SHA2 + "\trefs/tags/v1.0.0\n"),
            runner,
        ]
        if kind == "empty":
            answers.append(runner)
        return align_local_tag_to_remote("v1.0.0", root=ROOT, runner=_scripted(answers))

    for kind, runner in (
        ("missing_tool", _missing),
        ("empty", _empty),
        ("unexpected_error", _boom),
    ):
        try:
            result = call(kind, runner)
        except ProbeFailure as exc:
            if exc.kind != kind:
                return _fail(f"align wanted {kind} got {exc.kind}: {exc}")
            continue
        return _fail(f"align wanted refuse kind={kind}, got {result!r}")
    return _ok("align-local-tag-to-remote refuses")


def passes_align_local_tag_to_remote() -> int:
    from nouns.release_tags import align_local_tag_to_remote

    runner = _scripted(
        [
            _proc(0, SHA + "\n"),
            _proc(0, ""),
            _proc(0, SHA2 + "\trefs/tags/v1.0.0\n"),
            _proc(0, ""),
            _proc(0, SHA2 + "\n"),
        ]
    )
    got = align_local_tag_to_remote("v1.0.0", runner=runner)
    if got != SHA2:
        return _fail(f"align should return remote peel {SHA2} got {got}")
    return _ok("align-local-tag-to-remote known-good")


def fails_changelog_tag_exists() -> int:
    from nouns.release_notes import resolve_changelog_from_tag

    err = _kinds_via_runner(
        lambda runner: resolve_changelog_from_tag("v1.0.0", runner=runner, root=ROOT),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("changelog-tag-exists refuses")


def passes_changelog_tag_exists() -> int:
    from nouns.release_notes import resolve_changelog_from_tag

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        subprocess.run(["git", "tag", "v1.2.3", sha], cwd=repo, check=True)
        kept = resolve_changelog_from_tag("v1.2.3", root=repo)
        if kept != "v1.2.3":
            return _fail(f"existing from_tag must stay, got {kept}")
        gone = resolve_changelog_from_tag("v9.9.9", root=repo)
        if gone is not None:
            return _fail("confirmed missing from_tag must clear")
    return _ok("changelog-tag-exists known-good")


def fails_branch_exists() -> int:
    from nouns.release_infer import branch_exists

    err = _kinds_via_runner(
        lambda runner: branch_exists("main", ROOT, runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("branch-exists refuses")


def passes_branch_exists() -> int:
    from nouns.release_infer import branch_exists

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        _init_repo(repo)
        branch = subprocess.run(
            ["git", "branch", "--show-current"], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()
        if not branch_exists(branch, repo):
            return _fail("current branch must exist")
        if branch_exists("no-such-branch", repo):
            return _fail("missing branch must be confirmed false")
    return _ok("branch-exists known-good")


def fails_remote_branch_exists() -> int:
    from nouns.nlc_release_resume import remote_branch_exists

    err = _kinds_via_runner(
        lambda runner: remote_branch_exists("origin", "main", runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("remote-branch-exists refuses")


def passes_remote_branch_exists() -> int:
    from nouns.nlc_release_resume import remote_branch_exists

    present = remote_branch_exists("origin", "main", runner=lambda argv, **k: _proc(0, f"{SHA}\trefs/heads/main\n"))
    absent = remote_branch_exists("origin", "main", runner=lambda argv, **k: _proc(0, ""))
    if not present or absent:
        return _fail(f"present={present} absent={absent}")
    return _ok("remote-branch-exists known-good")


def fails_resolve_ref_sha() -> int:
    from nouns.nlc_release_resume import resolve_ref_sha

    err = _kinds_via_runner(
        lambda runner: resolve_ref_sha("HEAD", runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("resolve-ref-sha refuses")


def passes_resolve_ref_sha() -> int:
    from nouns.nlc_release_resume import resolve_ref_sha

    got = resolve_ref_sha("HEAD", runner=lambda argv, **k: _proc(0, SHA + "\n"))
    if got != SHA:
        return _fail(f"expected {SHA} got {got}")
    missing = resolve_ref_sha("ghost", runner=lambda argv, **k: _proc(1, ""))
    if missing != "":
        return _fail("confirmed missing ref must be empty")
    return _ok("resolve-ref-sha known-good")


def fails_tag_on_commit() -> int:
    from nouns.nlc_release_resume import tag_on_commit

    err = _kinds_via_runner(
        lambda runner: tag_on_commit("v1.0.0", SHA, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("tag-on-commit refuses")


def passes_tag_on_commit() -> int:
    from nouns.nlc_release_resume import tag_on_commit

    yes = tag_on_commit("v1.0.0", SHA, runner=_scripted([_proc(0, SHA + "\n"), _proc(0, SHA + "\n")]))
    no = tag_on_commit("v1.0.0", SHA, runner=_scripted([_proc(1, "")]))
    if not yes or no:
        return _fail(f"yes={yes} no={no}")
    return _ok("tag-on-commit known-good")


def fails_is_resolvable_commit() -> int:
    from nouns.evidence_ref.evidence_ref import is_resolvable_commit

    err = _kinds_via_runner(
        lambda runner: is_resolvable_commit(ROOT, SHA, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("is-resolvable-commit refuses")


def passes_is_resolvable_commit() -> int:
    from nouns.evidence_ref.evidence_ref import is_resolvable_commit

    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        sha = _init_repo(repo)
        if not is_resolvable_commit(repo, sha):
            return _fail("real commit must resolve")
        if is_resolvable_commit(repo, "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"):
            return _fail("dangling commit must be confirmed false")
    return _ok("is-resolvable-commit known-good")


def fails_release_state_out() -> int:
    from nouns.nlc_release_state.nlc_release_state import _out

    err = _kinds_via_runner(
        lambda runner: _out(["git", "rev-parse", "HEAD"], runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("release-state-out refuses")


def passes_release_state_out() -> int:
    from nouns.nlc_release_state.nlc_release_state import _out

    got = _out(["git", "rev-parse", "HEAD"], runner=lambda argv, **k: _proc(0, SHA + "\n"))
    if got != SHA:
        return _fail(f"expected {SHA} got {got}")
    empty = _out(["git", "status", "--porcelain"], empty_ok=True, runner=lambda argv, **k: _proc(0, ""))
    if empty != "":
        return _fail("empty_ok must allow confirmed empty")
    return _ok("release-state-out known-good")


def fails_remote_branch_sha() -> int:
    from nouns.nlc_release_state.nlc_release_state import _remote_branch_sha

    err = _kinds_via_runner(
        lambda runner: _remote_branch_sha("origin", "main", runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("remote-branch-sha refuses")


def passes_remote_branch_sha() -> int:
    from nouns.nlc_release_state.nlc_release_state import _remote_branch_sha

    got = _remote_branch_sha(
        "origin", "main", runner=lambda argv, **k: _proc(0, f"{SHA}\trefs/heads/main\n")
    )
    if got != SHA:
        return _fail(f"expected {SHA} got {got}")
    absent = _remote_branch_sha("origin", "main", runner=lambda argv, **k: _proc(0, ""))
    if absent != "":
        return _fail("confirmed absent remote branch must be empty")
    return _ok("remote-branch-sha known-good")


def fails_remote_known() -> int:
    from nouns.nlc_release_state.nlc_release_state import fetch_marks_remote_known

    err = _kinds_via_runner(
        lambda runner: fetch_marks_remote_known("origin", runner=runner),
        {"missing_tool", "unexpected_error"},
    )
    return _fail(err) if err else _ok("remote-known refuses")


def passes_remote_known() -> int:
    from nouns.nlc_release_state.nlc_release_state import fetch_marks_remote_known

    if fetch_marks_remote_known("origin", runner=lambda argv, **k: _proc(0, "")) is not True:
        return _fail("successful fetch must be True")
    return _ok("remote-known known-good")


def fails_pull_requests() -> int:
    from nouns.nlc_release_state.nlc_release_state import _pull_requests

    err = _kinds_via_runner(
        lambda runner: _pull_requests("release/v0.4.1", "main", runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("pull-requests refuses")


def passes_pull_requests() -> int:
    from nouns.nlc_release_state.nlc_release_state import _pull_requests

    known, rows = _pull_requests(
        "release/v0.4.1", "main", runner=lambda argv, **k: _proc(0, "[]\n")
    )
    if not known or rows != []:
        return _fail(f"empty JSON array must be known, got {known} {rows}")
    return _ok("pull-requests known-good")


def fails_publish_status() -> int:
    from nouns.nlc_release_state.nlc_release_state import _publish_status

    err = _kinds_via_runner(
        lambda runner: _publish_status("v0.4.0", runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("publish-status refuses")


def passes_publish_status() -> int:
    from nouns.nlc_release_state.nlc_release_state import _publish_status

    success = _publish_status(
        "v0.4.0", runner=lambda argv, **k: _proc(0, '{"tagName":"v0.4.0"}\n')
    )
    missing = _publish_status(
        "v0.4.0", runner=lambda argv, **k: _proc(1, "", "release not found")
    )
    if success != "success" or missing != "missing":
        return _fail(f"success={success} missing={missing}")
    return _ok("publish-status known-good")


def fails_publish_decision() -> int:
    from nouns.release_state import plan_release

    facts = {
        "remote_known": True,
        "pr_list_known": True,
        "local_branch": "release/v0.3.0",
        "candidate_sha": SHA,
        "dirty": False,
        "worktree_file_version": "0.3.0",
        "head_file_version": "0.3.0",
        "candidate_record_version": "0.3.0",
        "candidate_record_branch": "release/v0.3.0",
        "remote_relation": "equal",
        "main_context": "contained",
        "active_release_branches": ["release/v0.3.0"],
        "pull_requests": [
            {
                "number": 1,
                "state": "merged",
                "head_sha": SHA,
                "merge_sha": SHA2,
                "merge_file_version": "0.3.0",
                "merge_record_version": "0.3.0",
                "merge_record_branch": "release/v0.3.0",
            }
        ],
        "origin_main_sha": SHA,
        "shipped_tag_sha": SHA,
        "local_tag_peeled_sha": "",
        "remote_tag_peeled_sha": "",
        "local_tag_known": False,
        "publish_status": "missing",
        "migrations_ready": True,
        "shipped_verify_met": True,
        "notes_valid": True,
        "target_verify_met": True,
        "prep_met": True,
    }
    decision = plan_release(facts)
    if decision["action"] != "BLOCKED" or "BLOCKED_TAG_PROBE" not in decision["blockers"]:
        return _fail(f"unknown peel must BLOCK, got {decision}")
    return _ok("publish-decision refuses unknown peel")


def passes_publish_decision() -> int:
    from nouns.release_state import plan_release

    facts = {
        "remote_known": True,
        "pr_list_known": True,
        "local_branch": "release/v0.3.0",
        "candidate_sha": SHA,
        "dirty": False,
        "worktree_file_version": "0.3.0",
        "head_file_version": "0.3.0",
        "candidate_record_version": "0.3.0",
        "candidate_record_branch": "release/v0.3.0",
        "remote_relation": "equal",
        "main_context": "contained",
        "active_release_branches": ["release/v0.3.0"],
        "pull_requests": [
            {
                "number": 1,
                "state": "merged",
                "head_sha": SHA,
                "merge_sha": SHA2,
                "merge_file_version": "0.3.0",
                "merge_record_version": "0.3.0",
                "merge_record_branch": "release/v0.3.0",
            }
        ],
        "origin_main_sha": SHA,
        "shipped_tag_sha": SHA,
        "local_tag_peeled_sha": "",
        "remote_tag_peeled_sha": "",
        "publish_status": "missing",
        "migrations_ready": True,
        "shipped_verify_met": True,
        "notes_valid": True,
        "target_verify_met": True,
        "prep_met": True,
    }
    decision = plan_release(facts)
    if decision["action"] != "CREATE_LOCAL_TAG":
        return _fail(f"confirmed absent peel must CREATE_LOCAL_TAG, got {decision}")
    return _ok("publish-decision known-good")


def fails_git_changed_paths() -> int:
    from nouns.mandated_paths.mandated_paths import git_changed_paths

    err = _kinds_via_runner(
        lambda runner: git_changed_paths(ROOT, runner=runner),
        {"missing_tool", "empty", "unexpected_error"},
    )
    return _fail(err) if err else _ok("git-changed-paths refuses")


def passes_git_changed_paths() -> int:
    from nouns.mandated_paths.mandated_paths import git_changed_paths

    runner = _scripted([_proc(0, SHA + "\n"), _proc(0, "a.py\n"), _proc(0, ""), _proc(0, "")])
    paths = git_changed_paths(ROOT, runner=runner)
    if paths != ["a.py"]:
        return _fail(f"expected [a.py] got {paths}")
    return _ok("git-changed-paths known-good")


class _Http:
    def __init__(self, exc: BaseException | None = None, body: str = "") -> None:
        self.exc = exc
        self.body = body

    def __call__(self, req: object, timeout: int = 60) -> object:
        if self.exc:
            raise self.exc
        return self

    def __enter__(self) -> "_Http":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body.encode("utf-8")


def fails_github_latest_tag() -> int:
    from nouns.nlc_distribution.nlc_distribution import _github_latest_tag

    try:
        _github_latest_tag("org/repo", opener=_Http(urllib.error.HTTPError("u", 401, "no", {}, None)))
        return _fail("HTTP 401 must refuse")
    except ProbeFailure as exc:
        if exc.kind != "unexpected_error":
            return _fail(f"401 kind {exc.kind}")
    try:
        _github_latest_tag("org/repo", opener=_Http(body=""))
        return _fail("empty HTTP body must refuse")
    except ProbeFailure as exc:
        if exc.kind != "empty":
            return _fail(f"empty kind {exc.kind}")
    try:
        _github_latest_tag(
            "org/repo",
            opener=_Http(urllib.error.HTTPError("u", 404, "no", {}, None)),
            runner=_missing,
        )
        return _fail("404 plus missing git must refuse")
    except ProbeFailure as exc:
        if exc.kind != "missing_tool":
            return _fail(f"404 fallback kind {exc.kind}")
    return _ok("github-latest-tag refuses")


def passes_github_latest_tag() -> int:
    from nouns.nlc_distribution.nlc_distribution import _github_latest_tag

    got = _github_latest_tag("org/repo", opener=_Http(body='{"tag_name":"v1.2.3"}'))
    if got != "1.2.3":
        return _fail(f"expected 1.2.3 got {got}")
    return _ok("github-latest-tag known-good")


def fails_create_release_line_show_ref() -> int:
    with tempfile.TemporaryDirectory() as raw:
        empty_bin = Path(raw) / "empty"
        empty_bin.mkdir()
        env = {**os.environ, "PATH": str(empty_bin)}
        missing = _run_probe_ref("release/v0.4.1", env)
        if missing.returncode == 0:
            return _fail("missing git must refuse show-ref")
        if "missing_tool" not in (missing.stderr or "") and missing.returncode != 2:
            return _fail(f"missing git output {missing.stderr!r} rc={missing.returncode}")
        boom = Path(raw) / "boom"
        boom.mkdir()
        _write_exec(boom / "git", "#!/bin/sh\nexit 128\n")
        env2 = {**os.environ, "PATH": str(boom)}
        bad = _run_probe_ref("release/v0.4.1", env2)
        if bad.returncode == 0:
            return _fail("unexpected show-ref rc must refuse")
        empty = subprocess.run(
            [BASH, str(ROOT / "goals" / "hub_release" / "execute.sh"), "--probe-ref"],
            cwd=str(ROOT),
            env={**os.environ},
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        if empty.returncode == 0:
            return _fail("empty branch must refuse")
    return _ok("create-release-line-show-ref refuses")


def passes_create_release_line_show_ref() -> int:
    with tempfile.TemporaryDirectory() as raw:
        repo = Path(raw)
        _init_repo(repo)
        branch = subprocess.run(
            ["git", "branch", "--show-current"], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()
        env = {**os.environ}
        present = subprocess.run(
            [BASH, str(ROOT / "goals" / "hub_release" / "execute.sh"), "--probe-ref", branch],
            cwd=str(repo),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if present.returncode != 0 or present.stdout.strip() != "exists":
            # probe uses repo git via PATH; cwd is repo so show-ref sees local heads
            present = subprocess.run(
                [BASH, "-c", f"cd {repo} && git show-ref --verify --quiet refs/heads/{branch}; echo rc=$?"],
                capture_output=True,
                text=True,
                check=False,
            )
            # Re-run probe from ROOT but GIT_DIR
            env = {**os.environ, "GIT_DIR": str(repo / ".git")}
            present = _run_probe_ref(branch, env)
        if present.returncode != 0 or present.stdout.strip() != "exists":
            return _fail(f"existing branch must be exists: {present.stdout!r} {present.stderr!r}")
        absent = _run_probe_ref("no-such-release-line", env)
        if absent.returncode != 0 or absent.stdout.strip() != "absent":
            return _fail(f"missing branch must be absent: {absent.stdout!r} {absent.stderr!r}")
    return _ok("create-release-line-show-ref known-good")


def fails_sig_ok() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tree = Path(raw)
        doc = tree / "0001-one.md"
        doc.write_text("# ADR\n", encoding="utf-8")
        (tree / "0001-one.md.asc").write_text("sig\n", encoding="utf-8")
        empty_bin = tree / "empty"
        empty_bin.mkdir()
        env = {**os.environ, "PATH": str(empty_bin)}
        missing = _run_probe_sig(doc, env)
        if missing.returncode == 0:
            return _fail("missing gpg must refuse")
        boom = tree / "boom"
        boom.mkdir()
        _write_exec(boom / "gpg", "#!/bin/sh\nexit 2\n")
        env2 = {**os.environ, "PATH": f"{boom}:{os.environ.get('PATH', '')}"}
        bad = _run_probe_sig(doc, env2)
        if bad.returncode == 0:
            return _fail("gpg rc 2 must refuse")
        emptyg = tree / "emptyg"
        emptyg.mkdir()
        _write_exec(emptyg / "gpg", "#!/bin/sh\nexit 0\n")
        env3 = {**os.environ, "PATH": f"{emptyg}:{os.environ.get('PATH', '')}"}
        empty = _run_probe_sig(doc, env3)
        if empty.returncode == 0:
            return _fail("empty gpg status must refuse")
    return _ok("sig-ok refuses")


def passes_sig_ok() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tree = Path(raw)
        doc = tree / "0001-one.md"
        doc.write_text("# ADR\n", encoding="utf-8")
        (tree / "0001-one.md.asc").write_text("sig\n", encoding="utf-8")
        good = tree / "good"
        good.mkdir()
        _write_exec(
            good / "gpg",
            "#!/bin/sh\n"
            "echo '[GNUPG:] VALIDSIG 9D1BD57770FC3A1DE84702750AFD22B063AE01BC' >&2\n"
            "exit 0\n",
        )
        env = {**os.environ, "PATH": f"{good}:{os.environ.get('PATH', '')}"}
        ok = _run_probe_sig(doc, env)
        if ok.returncode != 0:
            return _fail(f"validsig must pass: {ok.stderr!r} rc={ok.returncode}")
        bad = tree / "bad"
        bad.mkdir()
        _write_exec(bad / "gpg", "#!/bin/sh\necho '[GNUPG:] BADSIG' >&2\nexit 1\n")
        env2 = {**os.environ, "PATH": f"{bad}:{os.environ.get('PATH', '')}"}
        unsigned = _run_probe_sig(doc, env2)
        if unsigned.returncode == 0:
            return _fail("bad signature must be confirmed unsigned")
        if unsigned.returncode == 2:
            return _fail("bad signature must not be a probe error")
    return _ok("sig-ok known-good")


_FAILS = {
    "main-purity": fails_main_purity,
    "tag-exists": fails_tag_exists,
    "list-version-tags": fails_list_version_tags,
    "tag-is-ancestor": fails_tag_is_ancestor,
    "remote-tag-commit-only": fails_remote_tag_commit_only,
    "align-local-tag-to-remote": fails_align_local_tag_to_remote,
    "changelog-tag-exists": fails_changelog_tag_exists,
    "branch-exists": fails_branch_exists,
    "remote-branch-exists": fails_remote_branch_exists,
    "resolve-ref-sha": fails_resolve_ref_sha,
    "tag-on-commit": fails_tag_on_commit,
    "is-resolvable-commit": fails_is_resolvable_commit,
    "release-state-out": fails_release_state_out,
    "remote-branch-sha": fails_remote_branch_sha,
    "remote-known": fails_remote_known,
    "pull-requests": fails_pull_requests,
    "publish-status": fails_publish_status,
    "publish-decision": fails_publish_decision,
    "git-changed-paths": fails_git_changed_paths,
    "github-latest-tag": fails_github_latest_tag,
    "create-release-line-show-ref": fails_create_release_line_show_ref,
    "sig-ok": fails_sig_ok,
}

_PASSES = {
    "main-purity": passes_main_purity,
    "tag-exists": passes_tag_exists,
    "list-version-tags": passes_list_version_tags,
    "tag-is-ancestor": passes_tag_is_ancestor,
    "remote-tag-commit-only": passes_remote_tag_commit_only,
    "align-local-tag-to-remote": passes_align_local_tag_to_remote,
    "changelog-tag-exists": passes_changelog_tag_exists,
    "branch-exists": passes_branch_exists,
    "remote-branch-exists": passes_remote_branch_exists,
    "resolve-ref-sha": passes_resolve_ref_sha,
    "tag-on-commit": passes_tag_on_commit,
    "is-resolvable-commit": passes_is_resolvable_commit,
    "release-state-out": passes_release_state_out,
    "remote-branch-sha": passes_remote_branch_sha,
    "remote-known": passes_remote_known,
    "pull-requests": passes_pull_requests,
    "publish-status": passes_publish_status,
    "publish-decision": passes_publish_decision,
    "git-changed-paths": passes_git_changed_paths,
    "github-latest-tag": passes_github_latest_tag,
    "create-release-line-show-ref": passes_create_release_line_show_ref,
    "sig-ok": passes_sig_ok,
}


def run(instance: str, mode: str) -> int:
    if instance not in INSTANCES:
        return _fail(f"unknown instance {instance}")
    if mode == "fails":
        return _FAILS[instance]()
    if mode == "passes":
        return _PASSES[instance]()
    return _fail(f"unknown mode {mode}")


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print("usage: assert_release_probe_fail_closed <instance> fails|passes", file=sys.stderr)
        return 2
    return run(args[0], args[1])


if __name__ == "__main__":
    raise SystemExit(main())
