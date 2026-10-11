"""Scan in-force markdown for second live gap lists (O10)."""

from __future__ import annotations

import re
from pathlib import Path

# Paths (posix, repo-relative) where gap markers are allowed or ignored.
# SSOT prose: integrity/GAP-LIST-SSOT-EXCLUSIONS.md
ALLOWED_GAP_LIST: frozenset[str] = frozenset({"FINDINGS.md"})

EXCLUDED_PREFIXES: tuple[str, ...] = (
    "docs/history/",
    "docs/rca/",
    "theory/history/",
    "examples/",
    "tools/nouns/live_gap_list_bypass_fixtures/",
    "node_modules/",
    ".git/",
)

EXCLUDED_EXACT: frozenset[str] = frozenset(
    {
        "TODO",
        "HOLES.md",
        "docs/nlc/SESSION-FOLLOWTHROUGH.md",
        "AGENTS.md",
        "DESCRIBE.md",
        "CHARTER.md",
        # Contribution / gate checklists (not product gap queues)
        "integrity/GATE.md",
        "integrity/ACTIONS.md",
        "integrity/BOUNDARY.md",
        "integrity/CONTRIBUTION.md",
        "integrity/PRINCIPLES.md",
        "integrity/BOUNDED_CONTEXT.md",
        "integrity/QUALITY_METRIC.md",
        "integrity/GAP-LIST-SSOT-EXCLUSIONS.md",
        ".agents/instructions/todo-product-uc-completion.md",
    }
)

EXCLUDED_PREFIXES_EXTRA: tuple[str, ...] = (
    ".agents/skills/planit/references/",
)

# Audit skill checklists (orchestration checklists, not gap SSOT)
EXCLUDED_SKILL_CHECKLIST_PREFIXES: tuple[str, ...] = (
    ".agents/skills/full-nlc-audit/",
    ".agents/skills/nlc-hub-audit/",
    ".cursor/skills/full-nlc-audit/",
    ".cursor/skills/nlc-hub-audit/",
)

NEEDED_HEADING = re.compile(r"^##+\s+Needed\b", re.M)
BLOCKED_ROW = re.compile(r"^\|.*\bBlocked\b.*\|$", re.M)
BLOCKING_GAP_COL = re.compile(r"Blocking gap \(implementation\)", re.I)
OPEN_GAP_SSOT = re.compile(r"\b(open work SSOT|second queue|live queue:)\b", re.I)
UNCHECKED_TASK = re.compile(r"^- \[ \]\s+", re.M)
OPEN_BOX = re.compile(r"☐")


def is_scan_excluded(rel_posix: str) -> bool:
    if rel_posix in EXCLUDED_EXACT:
        return True
    if rel_posix in ALLOWED_GAP_LIST:
        return True
    for prefix in EXCLUDED_PREFIXES:
        if rel_posix.startswith(prefix):
            return True
    for prefix in EXCLUDED_SKILL_CHECKLIST_PREFIXES:
        if rel_posix.startswith(prefix):
            return True
    for prefix in EXCLUDED_PREFIXES_EXTRA:
        if rel_posix.startswith(prefix):
            return True
    return False


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


def scan_markdown(rel_posix: str, text: str) -> list[str]:
    if is_scan_excluded(rel_posix):
        return []
    body = strip_fences(text)
    hits: list[str] = []
    if NEEDED_HEADING.search(body):
        hits.append(f"{rel_posix}: ## Needed section (gap queue)")
    if BLOCKED_ROW.search(body):
        hits.append(f"{rel_posix}: table row with Blocked status")
    if BLOCKING_GAP_COL.search(body):
        hits.append(f"{rel_posix}: Blocking gap (implementation) column")
    if OPEN_GAP_SSOT.search(body) and rel_posix != "FINDINGS.md":
        hits.append(f"{rel_posix}: open-gap / second-queue SSOT claim")
    if rel_posix.endswith("BACKLOG.md") or "/BACKLOG.md" in rel_posix:
        if UNCHECKED_TASK.search(body) or "|" in body:
            hits.append(f"{rel_posix}: BACKLOG gap table or unchecked tasks")
    elif UNCHECKED_TASK.search(body):
        hits.append(f"{rel_posix}: unchecked '- [ ]' task (use FINDINGS)")
    if OPEN_BOX.search(body):
        hits.append(f"{rel_posix}: open todo marker ☐ (use FINDINGS)")
    return hits


def scan_repo(root: Path) -> list[str]:
    violations: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".markdown"}:
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        if is_scan_excluded(rel):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        violations.extend(scan_markdown(rel, text))
    return violations
