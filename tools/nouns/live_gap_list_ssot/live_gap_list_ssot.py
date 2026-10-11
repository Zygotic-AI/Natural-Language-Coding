"""Scan in-force markdown for second live gap lists (O10)."""

from __future__ import annotations

import re
from pathlib import Path

from nouns.live_gap_list_ssot.gap_list_exclusions import (
    ALLOWED_GAP_LIST,
    is_path_fully_excluded,
    line_is_exempt,
)

NEEDED_HEADING = re.compile(r"^##+\s+Needed\b", re.M)
STILL_OPEN_HEADING = re.compile(r"^##+\s+(Still open|Remaining)\b", re.M)
BLOCKED_ROW = re.compile(r"^\|(?:[^|\n]*\|)+\s*Blocked\s*\|", re.M)
BLOCKING_GAP_COL = re.compile(r"Blocking gap \(implementation\)", re.I)
OPEN_GAP_SSOT = re.compile(r"\b(open work SSOT|second queue|live queue:)\b", re.I)
UNCHECKED_TASK = re.compile(r"^- \[ \]\s+", re.M)
UNCHECKED_BULLET = re.compile(r"^\* \[ \]\s+", re.M)
UNCHECKED_NUMBERED = re.compile(r"^\d+\. \[ \]\s+", re.M)
OPEN_BOX = re.compile(r"☐")
PENDING_TABLE = re.compile(r"^\|.*\b(Pending|Open)\b.*\|$", re.M)


def strip_fences(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def _scan_body_lines(rel_posix: str, body: str) -> list[str]:
    hits: list[str] = []
    lines = body.splitlines()

    if NEEDED_HEADING.search(body):
        hits.append(f"{rel_posix}: ## Needed section (gap queue)")
    if STILL_OPEN_HEADING.search(body):
        # Section with open/remaining + table row Pending/Open
        for m in STILL_OPEN_HEADING.finditer(body):
            start = m.start()
            rest = body[start:]
            next_h = re.search(r"\n##[^#]", rest[1:])
            section = rest if not next_h else rest[: next_h.start() + 1]
            if PENDING_TABLE.search(section) or UNCHECKED_TASK.search(section):
                hits.append(f"{rel_posix}: ## Still open / Remaining with open or pending work")
                break
    if BLOCKING_GAP_COL.search(body):
        hits.append(f"{rel_posix}: Blocking gap (implementation) column")

    for i, line in enumerate(lines):
        if line_is_exempt(rel_posix, line):
            continue
        if BLOCKED_ROW.match(line):
            hits.append(f"{rel_posix}: table row with Blocked status (line {i + 1})")
        if UNCHECKED_TASK.match(line):
            hits.append(f"{rel_posix}: unchecked '- [ ]' task (line {i + 1})")
        if UNCHECKED_BULLET.match(line):
            hits.append(f"{rel_posix}: unchecked '* [ ]' task (line {i + 1})")
        if UNCHECKED_NUMBERED.match(line):
            hits.append(f"{rel_posix}: numbered '1. [ ]' task (line {i + 1})")
        if OPEN_BOX.search(line) and not line_is_exempt(rel_posix, line):
            hits.append(f"{rel_posix}: open todo marker ☐ (line {i + 1})")

    if rel_posix.endswith("BACKLOG.md") or "/BACKLOG.md" in rel_posix:
        if any(not line_is_exempt(rel_posix, ln) and "|" in ln for ln in lines):
            hits.append(f"{rel_posix}: BACKLOG gap table")

    if OPEN_GAP_SSOT.search(body) and rel_posix not in ALLOWED_GAP_LIST:
        hits.append(f"{rel_posix}: open-gap / second-queue SSOT claim")

    return hits


def scan_markdown(rel_posix: str, text: str) -> list[str]:
    if is_path_fully_excluded(rel_posix):
        return []
    body = strip_fences(text)
    return _scan_body_lines(rel_posix, body)


def scan_repo(root: Path) -> list[str]:
    violations: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".markdown"} and path.name not in {"TODO", "HOLES.md"}:
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if is_path_fully_excluded(rel):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        violations.extend(scan_markdown(rel, text))
    return violations
