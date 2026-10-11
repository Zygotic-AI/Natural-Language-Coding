"""Detect term definitions outside docs/TERMS.md (O11)."""

from __future__ import annotations

import re
from pathlib import Path

TERMS_PATH = "docs/TERMS.md"

POINTER_FILES = frozenset(
    {
        "integrity/LEXICON.md",
        "docs/nlc/compiler/GLOSSARY.md",
        "docs/nlc/compiler/NAMES.md",
        "docs/nlc/RULE-VOCAB.md",
    }
)

EXCLUDED_PREFIXES: tuple[str, ...] = (
    "docs/history/",
    "docs/rca/",
    "theory/history/",
    "examples/",
    "tools/nouns/term_definition_bypass_fixtures/",
    "reviews/",
    "node_modules/",
    ".git/",
    "adrs/",
)

EXCLUDED_EXACT: frozenset[str] = frozenset(
    {
        "integrity/TERM-DEFINITION-SSOT-EXCLUSIONS.md",
        "integrity/GAP-LIST-SSOT-EXCLUSIONS.md",
        # Id-prefix table (P/R/C/Q), not TERMS definitions
        "CHARTER.md",
        # Gate criteria binder; links TERMS for the Gate noun
        "integrity/GATE.md",
        # Operational binders that reuse term words as section titles
        "docs/nlc/RULE-TRACE.md",
        "docs/nlc/RCA-PACKET.md",
        "docs/nlc/IMPLEMENTATION-COMPLEXITY-EXAMINATION-PLAN.md",
        "docs/adoption/RELEASE-ZERO-PARAMS-PLAN.md",
        "docs/bba/BBA-EMIT-PROCESS.md",
        "docs/bba/POLICY-ADR-LINEAGE.md",
        "docs/nlc/compiler/INTENT-SURFACE.md",
    }
)

HEADING_DEF = re.compile(r"^#{2,3}\s+(?!\[)([A-Za-z0-9][A-Za-z0-9 \-/']*)\s*$", re.M)
BOLD_COLON = re.compile(r"^\*\*([A-Za-z][A-Za-z0-9 \-/']*)\*\*\s*:\s+\S", re.M)
TABLE_BOLD = re.compile(r"^\|\s*\*\*([A-Za-z][A-Za-z0-9 \-/']*)\*\*\s*\|", re.M)
EM_DASH = re.compile(r"^([A-Za-z][A-Za-z0-9 \-/']*)\s+—\s+\S", re.M)


def load_term_names(terms_text: str) -> frozenset[str]:
    names: set[str] = set()
    for m in HEADING_DEF.finditer(terms_text):
        raw = m.group(1).strip()
        if raw.startswith("Operating bindings"):
            continue
        names.add(raw)
        names.add(raw.lower())
    return frozenset(names)


def is_excluded(rel_posix: str) -> bool:
    if rel_posix == TERMS_PATH:
        return True
    if rel_posix in EXCLUDED_EXACT:
        return True
    for prefix in EXCLUDED_PREFIXES:
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


def term_matches(name: str, terms: frozenset[str]) -> bool:
    n = name.strip()
    return n in terms or n.lower() in terms


def scan_markdown(rel_posix: str, text: str, terms: frozenset[str]) -> list[str]:
    if is_excluded(rel_posix):
        return []
    body = strip_fences(text)
    hits: list[str] = []
    for m in HEADING_DEF.finditer(body):
        title = m.group(1).strip()
        if term_matches(title, terms):
            hits.append(f"{rel_posix}: heading defines {title!r}")
    for pat, label in (
        (BOLD_COLON, "bold-colon"),
        (TABLE_BOLD, "table-bold"),
        (EM_DASH, "em-dash"),
    ):
        for m in pat.finditer(body):
            title = m.group(1).strip()
            if term_matches(title, terms):
                hits.append(f"{rel_posix}: {label} defines {title!r}")
    return hits


def scan_repo(root: Path, terms: frozenset[str]) -> list[str]:
    violations: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".markdown"}:
            continue
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        violations.extend(scan_markdown(rel, text, terms))
    return violations
