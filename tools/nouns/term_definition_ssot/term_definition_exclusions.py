"""Line/path term-definition scan exclusions (O11). SSOT: integrity/TERM-DEFINITION-SSOT-EXCLUSIONS.md."""

from __future__ import annotations

import re
from dataclasses import dataclass

TERMS_PATH = "docs/TERMS.md"

POINTER_FILES = frozenset(
    {
        "integrity/LEXICON.md",
        "docs/nlc/compiler/GLOSSARY.md",
        "docs/nlc/compiler/NAMES.md",
        "docs/nlc/RULE-VOCAB.md",
    }
)

PATH_PREFIX_EXCLUSIONS: tuple[tuple[str, str], ...] = (
    ("docs/history/", "Archive"),
    ("docs/rca/", "RCA packets"),
    ("theory/history/", "Frozen theory"),
    ("tools/nouns/term_definition_bypass_fixtures/", "Term landmine plants"),
    ("reviews/", "Ephemeral review packets"),
    ("node_modules/", "Third-party"),
    (".git/", "VCS"),
)

PATH_EXACT_EXCLUSIONS: tuple[tuple[str, str], ...] = (
    ("integrity/TERM-DEFINITION-SSOT-EXCLUSIONS.md", "Meta exclusions doc"),
    ("integrity/GAP-LIST-SSOT-EXCLUSIONS.md", "Gap exclusions meta"),
)


@dataclass(frozen=True)
class LineExemption:
    rel: str
    pattern: re.Pattern[str]
    reason: str


LINE_EXEMPTIONS: tuple[LineExemption, ...] = (
    LineExemption("CHARTER.md", re.compile(r"^\| \*\*[PRCQ]\*\* \|"), "Charter id-prefix table (P/R/C/Q), not term defs"),
    LineExemption("CHARTER.md", re.compile(r"^- \[ \] C\d+\."), "Charter confirmation checklist"),
    LineExemption("CHARTER.md", re.compile(r"^- \[ \] CS\d+\."), "Charter agent-noun checklist"),
    LineExemption("integrity/GATE.md", re.compile(r"^- \[ \] CG\d+\."), "Gate tip checklist (CG1–CG4)"),
    LineExemption("integrity/GATE.md", re.compile(r"^#{2,3}\s+\["), "Gate binder link headings to TERMS"),
    LineExemption("integrity/CONTRIBUTION.md", re.compile(r"^- \[ \] CC\d+\."), "Contribution gate checklist"),
    LineExemption("integrity/BOUNDARY.md", re.compile(r"^- \[ \] CB\d+\."), "Boundary checklist"),
    LineExemption("integrity/PRINCIPLES.md", re.compile(r"^- \[ \] P\d+\."), "Principle checklist"),
    LineExemption(
        "docs/nlc/RULE-TRACE.md",
        re.compile(r"^#{2,3}\s+(Audit|Gate)\s*$"),
        "Operational binder section title cross-ref",
    ),
    LineExemption(
        "docs/nlc/RCA-PACKET.md",
        re.compile(r"^##\s+Gate\b"),
        "RCA packet gate section title",
    ),
    LineExemption(
        "docs/nlc/IMPLEMENTATION-COMPLEXITY-EXAMINATION-PLAN.md",
        re.compile(r"^##\s+Gate\b"),
        "Examination plan gate section title",
    ),
    LineExemption(
        "docs/adoption/RELEASE-ZERO-PARAMS-PLAN.md",
        re.compile(r"^##\s+Prove\b"),
        "Release plan prove section title",
    ),
    LineExemption(
        "docs/bba/BBA-EMIT-PROCESS.md",
        re.compile(r"^\| \*\*(Noun|Adjective)\*\* \|"),
        "Emit process table column headers",
    ),
    LineExemption(
        "docs/bba/POLICY-ADR-LINEAGE.md",
        re.compile(r"^##\s+Lineage\b"),
        "Lineage doc section title",
    ),
    LineExemption(
        "docs/nlc/compiler/INTENT-SURFACE.md",
        re.compile(r"^\| \*\*Goal\*\* \|"),
        "Intent surface comparison table header",
    ),
    LineExemption("examples/", re.compile(r"."), "Specimen trees (negative/positive fixtures)"),
    LineExemption(
        "adrs/",
        re.compile(r"^#{2,3}\s+(Context|Decision|Consequences|Status)\b"),
        "ADR boilerplate headings",
    ),
    LineExemption("adrs/", re.compile(r"^##\s+Gate\b"), "ADR standard Gate wiring section (not lexicon)"),
    LineExemption("adrs/", re.compile(r"^##\s+Refuse"), "ADR standard Refuse section (not lexicon)"),
    LineExemption("docs/USE-CASES-PROOF.md", re.compile(r"^\|"), "UC proof matrix table (not term defs)"),
    LineExemption("docs/ADR-ENFORCEMENT.md", re.compile(r"^\|"), "ADR enforcement table (not term defs)"),
    LineExemption("adrs/INDEX.md", re.compile(r"^\|"), "ADR index table"),
    LineExemption("adrs/CATALOG.md", re.compile(r"^\|"), "ADR catalog table"),
    LineExemption("adrs/ACTIVE.md", re.compile(r"^\|"), "ADR active list table"),
    LineExemption("agents/README.md", re.compile(r"^\|"), "Agent package index table"),
    LineExemption("integrity/GATE.md", re.compile(r"^\| Mechanism \|"), "Gate vs audit comparison table header"),
    LineExemption("integrity/BOUNDARY.md", re.compile(r"^\|"), "Boundary binder tables"),
    LineExemption("CHARTER.md", re.compile(r"^\|"), "Charter tables (not term defs)"),
    LineExemption(".agents/skills/", re.compile(r"^\*\*Waived:\*\*"), "Skill waiver callout line"),
    LineExemption("adrs/ACTIVE.md", re.compile(r"^[A-Za-z]+:"), "ADR ACTIVE manifest field lines"),
    LineExemption(
        "adrs/0029-adr-lineage-active-set-and-bind-snapshot.md",
        re.compile(r"^[A-Za-z]+:"),
        "ADR front-matter field lines",
    ),
    LineExemption(
        "docs/nlc/IMPLEMENTATION-COMPLEXITY-EXAMINATION-PLAN.md",
        re.compile(r"^\|"),
        "Examination plan tables",
    ),
    LineExemption("docs/bba/BBA-EMIT-PROCESS.md", re.compile(r"^\*\*Corpus:\*\*"), "Emit process corpus callout"),
    LineExemption("docs/bba/BBA-EMIT-PROCESS.md", re.compile(r"^- \*\*audit\*\*"), "Emit process bullet label"),
    LineExemption("tools/nouns/releasable_gates/README.md", re.compile(r"^Boundary:"), "Releasable gates README field line"),
)


def documented_exclusion_rows() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for p, r in PATH_PREFIX_EXCLUSIONS:
        rows.append(("prefix", p, r))
    for p, r in PATH_EXACT_EXCLUSIONS:
        rows.append(("exact", p, r))
    for ex in LINE_EXEMPTIONS:
        rows.append(("line", f"{ex.rel} :: {ex.pattern.pattern}", ex.reason))
    return rows


def is_path_fully_excluded(rel_posix: str) -> bool:
    if rel_posix == TERMS_PATH:
        return True
    for exact, _ in PATH_EXACT_EXCLUSIONS:
        if rel_posix == exact:
            return True
    for prefix, _ in PATH_PREFIX_EXCLUSIONS:
        if rel_posix.startswith(prefix):
            return True
    return False


def line_is_exempt(rel_posix: str, line: str) -> bool:
    for ex in LINE_EXEMPTIONS:
        if ex.rel.endswith("/"):
            if not rel_posix.startswith(ex.rel):
                continue
        elif ex.rel != rel_posix:
            continue
        if ex.pattern.search(line):
            return True
    return False
