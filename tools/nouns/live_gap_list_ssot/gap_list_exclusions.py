"""Line/path gap-scan exclusions (O10). SSOT prose: integrity/GAP-LIST-SSOT-EXCLUSIONS.md."""

from __future__ import annotations

import re
from dataclasses import dataclass

ALLOWED_GAP_LIST: frozenset[str] = frozenset({"FINDINGS.md"})

# Prefixes excluded entirely (archives, landmines, VCS).
PATH_PREFIX_EXCLUSIONS: tuple[tuple[str, str], ...] = (
    ("docs/history/", "Archived work logs and wave ledgers"),
    ("docs/rca/", "RCA packets (not live gap queues)"),
    ("theory/history/", "Frozen theory archive"),
    ("tools/nouns/live_gap_list_bypass_fixtures/", "Gap-list landmine plants"),
    ("node_modules/", "Third-party"),
    (".git/", "VCS metadata"),
)

# Exact paths excluded entirely (stubs + meta).
PATH_EXACT_EXCLUSIONS: tuple[tuple[str, str], ...] = (
    ("integrity/GAP-LIST-SSOT-EXCLUSIONS.md", "Meta: documents exclusions"),
    ("examples/open-findings/FINDINGS.md", "C23 specimen: adversarial open FINDINGS (not live SSOT)"),
)

# Skill trees: audit orchestration checklists only (paths under these prefixes).
SKILL_CHECKLIST_PREFIXES: tuple[tuple[str, str], ...] = (
    (".agents/skills/full-nlc-audit/", "Full NLC audit skill checklists"),
    (".agents/skills/nlc-hub-audit/", "Hub audit skill checklists"),
    (".cursor/skills/full-nlc-audit/", "Cursor mirror of full-nlc-audit checklists"),
    (".cursor/skills/nlc-hub-audit/", "Cursor mirror of nlc-hub-audit checklists"),
    (".agents/skills/planit/references/", "Planit reference checklists"),
)

# Per-file line patterns that are not live gap queues (checklist conventions).
@dataclass(frozen=True)
class LineExemption:
    rel: str
    pattern: re.Pattern[str]
    reason: str


LINE_EXEMPTIONS: tuple[LineExemption, ...] = (
    LineExemption("CHARTER.md", re.compile(r"^- \[ \] C\d+\."), "Charter change confirmation checklist (C1–C26)"),
    LineExemption("CHARTER.md", re.compile(r"^- \[ \] CS\d+\."), "Charter agent-noun confirmation checklist (CS1–CS10)"),
    LineExemption(
        "AGENTS.md",
        re.compile(r"task queue.*`☐`"),
        "Documents TODO `☐` convention (not an open-work queue)",
    ),
    LineExemption(
        "DESCRIBE.md",
        re.compile(r"`☐`"),
        "Documents TODO `☐` convention (not an open-work queue)",
    ),
    LineExemption("integrity/CONTRIBUTION.md", re.compile(r"^- \[ \] CC\d+\."), "Contribution gate checklist (CC1–CC8)"),
    LineExemption("integrity/BOUNDARY.md", re.compile(r"^- \[ \] CB\d+\."), "Boundary tip checklist (CB1–CB7)"),
    LineExemption("integrity/GATE.md", re.compile(r"^- \[ \] CG\d+\."), "Gate tip checklist (CG1–CG4)"),
    LineExemption("integrity/ACTIONS.md", re.compile(r"^- \[ \] CA\d+\."), "Action tip checklist"),
    LineExemption("integrity/PRINCIPLES.md", re.compile(r"^- \[ \] P\d+\."), "Principle checklist lines"),
    LineExemption("integrity/BOUNDED_CONTEXT.md", re.compile(r"^- \[ \]"), "Bounded-context checklist"),
    LineExemption("integrity/QUALITY_METRIC.md", re.compile(r"^- \[ \]"), "Quality metric checklist"),
    LineExemption(
        ".agents/instructions/todo-product-uc-completion.md",
        re.compile(r"^- \[ \]"),
        "Product UC completion instruction checklist",
    ),
    LineExemption(
        ".agents/instructions/todo-product-uc-completion.md",
        re.compile(r"`☐`\s*product"),
        "Documents TODO `☐` product-row convention (not live gap queue)",
    ),
    LineExemption("TODO", re.compile(r"^☐"), "Root TODO stub convention (points at history)"),
    LineExemption("HOLES.md", re.compile(r"."), "Stub pointer only"),
    LineExemption(
        "docs/nlc/SESSION-FOLLOWTHROUGH.md",
        re.compile(r"."),
        "Stub pointer to history SESSION-FOLLOWTHROUGH",
    ),
)


def documented_exclusion_rows() -> list[tuple[str, str, str]]:
    """(kind, locator, reason) for doc parity fitness."""
    rows: list[tuple[str, str, str]] = []
    for p, r in PATH_PREFIX_EXCLUSIONS:
        rows.append(("prefix", p, r))
    for p, r in PATH_EXACT_EXCLUSIONS:
        rows.append(("exact", p, r))
    for p, r in SKILL_CHECKLIST_PREFIXES:
        rows.append(("skill_prefix", p, r))
    for ex in LINE_EXEMPTIONS:
        rows.append(("line", f"{ex.rel} :: {ex.pattern.pattern}", ex.reason))
    return rows


def is_path_fully_excluded(rel_posix: str) -> bool:
    if rel_posix in ALLOWED_GAP_LIST:
        return True
    for prefix, _ in PATH_PREFIX_EXCLUSIONS:
        if rel_posix.startswith(prefix):
            return True
    for exact, _ in PATH_EXACT_EXCLUSIONS:
        if rel_posix == exact:
            return True
    for prefix, _ in SKILL_CHECKLIST_PREFIXES:
        if rel_posix.startswith(prefix):
            return True
    return False


def line_is_exempt(rel_posix: str, line: str) -> bool:
    for ex in LINE_EXEMPTIONS:
        if ex.rel != rel_posix:
            continue
        if ex.pattern.search(line):
            return True
    return False
