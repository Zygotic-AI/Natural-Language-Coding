#!/usr/bin/env python3
"""Open a pull request only after verify and fitness succeed on that commit.

No ADR: this command enforces the existing release prove step. It does not add
a requirement, a verb, or a charter rule. Checker-digest members are unchanged
so the owner signature on integrity/checker-digest.sha256 stays valid.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_TOOLS = ROOT / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from nouns.evidence_ref.sync_content_tree_hash import verify_content_tree_hash  # noqa: E402


def _strip_pr_urls(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        if "https://github.com/" in line and "/pull" in line:
            continue
        kept.append(line)
    body = "\n".join(kept)
    if "RESULT:NOT_MET" not in body:
        body = body.rstrip() + ("\n" if body else "") + "RESULT:NOT_MET"
    if not body.endswith("\n"):
        body += "\n"
    return body


def runs_block(runs: object) -> str | None:
    """None when a push fitness run succeeded and every completed run succeeded."""
    if not isinstance(runs, list):
        return "fitness run list unreadable"
    if any(not isinstance(item, dict) for item in runs):
        return "fitness run list unreadable"
    if any(item.get("status") != "completed" for item in runs):
        return "fitness run still in progress"
    push_ok = [
        item
        for item in runs
        if item.get("event") == "push" and item.get("conclusion") == "success"
    ]
    bad = [item for item in runs if item.get("conclusion") != "success"]
    if not push_ok:
        return "no successful push fitness run"
    if bad:
        ids = ",".join(str(item.get("databaseId")) for item in bad)
        return f"completed fitness run not success {ids}"
    return None


def decide(
    *,
    stamp_ok: bool,
    stamp_detail: str,
    verify_code: int,
    verify_text: str,
    runs: object,
    create,
) -> tuple[int, str]:
    """Return (exit code, stdout). create() runs only on the success path."""
    if not stamp_ok:
        return 1, _strip_pr_urls(stamp_detail)
    if verify_code != 0:
        return 1, _strip_pr_urls(verify_text)
    blocked = runs_block(runs)
    if blocked:
        return 1, _strip_pr_urls(f"VIOLATION {blocked}")
    url = create()
    if not url or "https://github.com/" not in url or "/pull" not in url:
        return 1, _strip_pr_urls("VIOLATION gh pr create returned no pull request URL")
    return 0, f"PR_OFFER_GATE:MET\n{url}\n"


def _git_sha(root: Path) -> str:
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    return (proc.stdout or "").strip()


def _verify(root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(root / "tools" / "nlc.py"), "--project", str(root), "verify"],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    text = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, text


def _fitness_runs(root: Path, sha: str) -> tuple[int, object, str]:
    proc = subprocess.run(
        [
            "gh",
            "run",
            "list",
            "--commit",
            sha,
            "--workflow",
            "fitness.yml",
            "--limit",
            "50",
            "--json",
            "databaseId,conclusion,event,status",
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return proc.returncode, None, (proc.stdout or "") + (proc.stderr or "")
    try:
        payload = json.loads(proc.stdout or "null")
    except json.JSONDecodeError:
        return 1, None, proc.stdout or ""
    return 0, payload, ""


def _create_pr(root: Path, args: argparse.Namespace) -> str:
    proc = subprocess.run(
        [
            "gh",
            "pr",
            "create",
            "--base",
            args.base,
            "--head",
            args.head,
            "--title",
            args.title,
            "--body",
            args.body,
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    for line in (proc.stdout or "").splitlines():
        if line.strip().startswith("https://github.com/") and "/pull/" in line:
            return line.strip()
    return (proc.stdout or "").strip()


def _self_test() -> int:
    calls = {"n": 0}

    def _create() -> str:
        calls["n"] += 1
        return "https://github.com/Zygotic-AI/Natural-Language-Coding/pull/1"

    cases: list[tuple[str, dict, int, bool]] = [
        (
            "stamp",
            {
                "stamp_ok": False,
                "stamp_detail": "VIOLATION hub-content-tree-hash deadbeef != content digest cafebabe",
                "verify_code": 0,
                "verify_text": "",
                "runs": [{"event": "push", "conclusion": "success", "status": "completed", "databaseId": 1}],
            },
            1,
            False,
        ),
        (
            "verify",
            {
                "stamp_ok": True,
                "stamp_detail": "",
                "verify_code": 1,
                "verify_text": "VIOLATION hub-content-tree-fresh\nhttps://github.com/Zygotic-AI/Natural-Language-Coding/pull/9\n",
                "runs": [{"event": "push", "conclusion": "success", "status": "completed", "databaseId": 1}],
            },
            1,
            False,
        ),
        (
            "no-push",
            {
                "stamp_ok": True,
                "stamp_detail": "",
                "verify_code": 0,
                "verify_text": "Verify passed.",
                "runs": [],
            },
            1,
            False,
        ),
        (
            "push-failed",
            {
                "stamp_ok": True,
                "stamp_detail": "",
                "verify_code": 0,
                "verify_text": "Verify passed.",
                "runs": [{"event": "push", "conclusion": "failure", "status": "completed", "databaseId": 41385442250}],
            },
            1,
            False,
        ),
        (
            "in-progress",
            {
                "stamp_ok": True,
                "stamp_detail": "",
                "verify_code": 0,
                "verify_text": "Verify passed.",
                "runs": [{"event": "push", "conclusion": "", "status": "in_progress", "databaseId": 2}],
            },
            1,
            False,
        ),
        (
            "mixed",
            {
                "stamp_ok": True,
                "stamp_detail": "",
                "verify_code": 0,
                "verify_text": "Verify passed.",
                "runs": [
                    {"event": "push", "conclusion": "success", "status": "completed", "databaseId": 3},
                    {"event": "pull_request", "conclusion": "failure", "status": "completed", "databaseId": 4},
                ],
            },
            1,
            False,
        ),
        (
            "ready",
            {
                "stamp_ok": True,
                "stamp_detail": "",
                "verify_code": 0,
                "verify_text": "Verify passed.",
                "runs": [
                    {"event": "push", "conclusion": "success", "status": "completed", "databaseId": 5},
                ],
            },
            0,
            True,
        ),
    ]
    for name, kwargs, code, created in cases:
        before = calls["n"]
        exit_code, text = decide(**kwargs, create=_create)
        if exit_code != code:
            print(f"SELF_TEST:FAIL {name} exit {exit_code} != {code}")
            return 1
        if (calls["n"] != before) != created:
            print(f"SELF_TEST:FAIL {name} create called={calls['n'] != before}")
            return 1
        if exit_code != 0:
            if "RESULT:NOT_MET" not in text or "/pull" in text:
                print(f"SELF_TEST:FAIL {name} failure text leaked a pull URL or omitted RESULT:NOT_MET")
                print(text)
                return 1
        elif "PR_OFFER_GATE:MET" not in text or "/pull/1" not in text:
            print(f"SELF_TEST:FAIL {name} success text")
            return 1
    print("PR_OFFER_GATE_SELF_TEST:MET")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offer a pull request only after verify and fitness succeed")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--commit", default="")
    parser.add_argument("--base", default="")
    parser.add_argument("--head", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--body", default="")
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    root = Path(args.root).resolve()
    ok, recorded, expected = verify_content_tree_hash(root)
    detail = (
        f"VIOLATION hub-content-tree-hash {recorded} != content digest {expected}"
        if not ok
        else ""
    )
    verify_code, verify_text = (0, "")
    runs: object = []
    if ok:
        verify_code, verify_text = _verify(root)
    if ok and verify_code == 0:
        sha = args.commit.strip() or _git_sha(root)
        if not sha:
            print(_strip_pr_urls("VIOLATION git rev-parse HEAD failed"), end="")
            return 1
        list_code, payload, list_text = _fitness_runs(root, sha)
        if list_code != 0:
            print(_strip_pr_urls(f"VIOLATION gh run list failed\n{list_text}"), end="")
            return 1
        runs = payload
    missing = [name for name in ("base", "head", "title") if not getattr(args, name).strip()]

    def _create() -> str:
        if missing:
            return ""
        return _create_pr(root, args)

    if ok and verify_code == 0 and runs_block(runs) is None and missing:
        joined = ", ".join(f"--{name}" for name in missing)
        print(
            _strip_pr_urls(
                "VIOLATION gh pr create needs "
                + joined
                + "\nremediate: python3 tools/pr-offer-gate.py --base main --head <branch> --title <title> --body <body>"
            ),
            end="",
        )
        return 1
    code, text = decide(
        stamp_ok=ok,
        stamp_detail=detail,
        verify_code=verify_code,
        verify_text=verify_text,
        runs=runs,
        create=_create,
    )
    print(text, end="")
    return code


if __name__ == "__main__":
    sys.exit(main())
