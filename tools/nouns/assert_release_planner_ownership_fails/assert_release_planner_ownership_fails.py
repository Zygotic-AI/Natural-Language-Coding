"""Landmine specimens for ADR 0049 release-planner ownership."""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from nouns.fitness_release_planner_ownership.fitness_release_planner_ownership import (
    EXECUTOR_REL,
    OBSERVER_REL,
    PLANNER_REL,
    planner_ownership_errors,
)

BOUNDARY = "bba-emit"

ROOT = Path(__file__).resolve().parents[3]
Mutation = tuple[str, str, Callable[[str], str]]


def _append(text: str, addition: str) -> str:
    return f"{text.rstrip()}\n{addition.strip()}\n"


def _replace(old: str, new: str) -> Callable[[str], str]:
    def apply(text: str) -> str:
        if old not in text:
            raise RuntimeError(f"specimen anchor missing: {old!r}")
        return text.replace(old, new, 1)

    return apply


MUTATIONS: tuple[Mutation, ...] = (
    (
        "renamed-failure-helper",
        EXECUTOR_REL,
        lambda text: _append(
            text, "halt_release() { exit 1; }\ntrue || halt_release"
        ),
    ),
    (
        "return-1",
        EXECUTOR_REL,
        lambda text: _append(text, "abandon_release() { return 1; }"),
    ),
    (
        "dynamic-exit",
        EXECUTOR_REL,
        lambda text: _append(text, 'finish_dynamic() { exit "$1"; }'),
    ),
    ("set-e", EXECUTOR_REL, _replace("set -uo pipefail", "set -euo pipefail")),
    (
        "untyped-action",
        PLANNER_REL,
        _replace(
            '    "NONE": "TERMINAL",\n',
            '    "NONE": "TERMINAL",\n    "SIDE_QUEST": "UNTYPED",\n',
        ),
    ),
    (
        "missing-progress-tuple",
        PLANNER_REL,
        _replace('    "VERIFY_TARGET": ("target_verify_met", "effective_tree_sha"),\n', ""),
    ),
    (
        "generic-runtime-error",
        OBSERVER_REL,
        lambda text: _append(text, 'GENERIC_FAILURE = {"runtime_error": "boom"}'),
    ),
    (
        "python-bypass",
        EXECUTOR_REL,
        lambda text: _append(
            text, "bypass_planner() { python3 tools/explode.py || exit 1; }"
        ),
    ),
    (
        "git-merge",
        EXECUTOR_REL,
        lambda text: _append(text, "sync_branches() { git merge feature-branch; }"),
    ),
    (
        "git-force-push",
        EXECUTOR_REL,
        lambda text: _append(text, "overwrite_remote() { git push --force origin main; }"),
    ),
    (
        "git-tag-move",
        EXECUTOR_REL,
        lambda text: _append(text, "move_tag() { git tag -f v9.9.9 HEAD; }"),
    ),
    (
        "git-stash",
        EXECUTOR_REL,
        lambda text: _append(text, "hide_work() { git stash push; }"),
    ),
    (
        "git-hard-reset",
        EXECUTOR_REL,
        lambda text: _append(text, "rewrite_branch() { git reset --hard HEAD~1; }"),
    ),
    (
        "local-main-repoint",
        EXECUTOR_REL,
        lambda text: _append(
            text,
            "repoint_main() { git checkout main && git reset --hard v0.2.0; }",
        ),
    ),
    (
        "absent-main-context",
        OBSERVER_REL,
        _replace('        "main_context": context_status,\n', ""),
    ),
    (
        "unproved-main-context",
        OBSERVER_REL,
        _replace(
            '        else ("unknown", ["release line is not selected"])\n',
            '        else ("contained", [])\n',
        ),
    ),
)


def _copy_control(root: Path) -> None:
    for relative in (EXECUTOR_REL, PLANNER_REL, OBSERVER_REL):
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        temp = Path(raw)
        control = temp / "control"
        _copy_control(control)
        errors = planner_ownership_errors(control)
        if errors:
            print("ASSERT:FAIL control specimen was rejected")
            for item in errors:
                print(item)
            return 1
        for name, relative, mutate in MUTATIONS:
            specimen = temp / name
            shutil.copytree(control, specimen)
            path = specimen / relative
            path.write_text(mutate(path.read_text(encoding="utf-8")), encoding="utf-8")
            if not planner_ownership_errors(specimen):
                print(f"ASSERT:FAIL {name} was accepted")
                return 1
    print("ASSERT:PASS")
    return 0
