"""Fail-closed probe results for release-tool checks.

A gate opens only when every check is a hard binary true.
Missing tool, empty output, or unexpected error is false (refuse).
# nlc:rule=default-closed
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import subprocess
from pathlib import Path
from typing import Callable, Sequence

Runner = Callable[..., subprocess.CompletedProcess[str]]


class ProbeFailure(Exception):
    """Probe did not produce a confirmed result."""

    def __init__(self, message: str, *, kind: str) -> None:
        super().__init__(message)
        self.kind = kind
        self.message = message


def run_argv(
    argv: Sequence[str],
    *,
    cwd: Path | str | None = None,
    runner: Runner | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run argv. Missing binary is a refuse, not a false negative."""
    run = runner or subprocess.run
    try:
        kwargs: dict[str, object] = {
            "capture_output": True,
            "text": True,
            "check": False,
        }
        if cwd is not None:
            kwargs["cwd"] = str(cwd)
        if env is not None:
            kwargs["env"] = env
        return run(list(argv), **kwargs)
    except FileNotFoundError as exc:
        name = argv[0] if argv else "command"
        raise ProbeFailure(f"missing tool: {name}", kind="missing_tool") from exc
    except OSError as exc:
        name = argv[0] if argv else "command"
        raise ProbeFailure(f"missing tool: {name}: {exc}", kind="missing_tool") from exc


def confirmed_exists(
    proc: subprocess.CompletedProcess[str],
    *,
    require_stdout: bool = False,
) -> bool:
    """Map a verify-style probe to a hard bool. rc 0/1 only; else refuse."""
    if proc.returncode == 0:
        if require_stdout and not (proc.stdout or "").strip():
            raise ProbeFailure("empty output", kind="empty")
        return True
    if proc.returncode == 1:
        return False
    err = (proc.stderr or "").strip() or (proc.stdout or "").strip()
    raise ProbeFailure(
        f"unexpected error rc={proc.returncode} {err}".strip(),
        kind="unexpected_error",
    )


def confirmed_text(
    proc: subprocess.CompletedProcess[str],
    *,
    empty_ok: bool = False,
    absent_codes: tuple[int, ...] = (),
) -> str:
    """Return stdout only for a confirmed success. Else refuse."""
    if proc.returncode == 0:
        text = (proc.stdout or "").strip()
        if not text and not empty_ok:
            raise ProbeFailure("empty output", kind="empty")
        return text
    if proc.returncode in absent_codes:
        return ""
    err = (proc.stderr or "").strip() or (proc.stdout or "").strip()
    raise ProbeFailure(
        f"unexpected error rc={proc.returncode} {err}".strip(),
        kind="unexpected_error",
    )


def refuse_empty(value: str, *, label: str) -> str:
    """Refuse an empty confirmed-string result."""
    if not value:
        raise ProbeFailure(f"empty output: {label}", kind="empty")
    return value
