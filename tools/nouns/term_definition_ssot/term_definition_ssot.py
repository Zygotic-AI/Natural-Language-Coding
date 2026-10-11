"""Detect term definitions outside docs/TERMS.md (O11)."""

from __future__ import annotations

import re
from pathlib import Path

from nouns.term_definition_ssot.term_definition_exclusions import (
    POINTER_FILES,
    TERMS_PATH,
    is_path_fully_excluded,
    line_is_exempt,
)

HEADING_DEF = re.compile(
    r"^(#{2,4})\s+(?!\[)([A-Za-z0-9][A-Za-z0-9 \-/']*)\s*$",
    re.M,
)
BOLD_COLON_OUT = re.compile(r"^\*\*([A-Za-z][A-Za-z0-9 \-/']*)\*\*\s*:\s+\S")
BOLD_COLON_IN = re.compile(r"^\*\*([A-Za-z][A-Za-z0-9 \-/']*):\*\*\s+\S")
TABLE_BOLD = re.compile(r"^\|\s*\*\*([A-Za-z][A-Za-z0-9 \-/']*)\*\*\s*\|")
TABLE_PLAIN = re.compile(r"^\|\s*([A-Za-z][A-Za-z0-9 \-/']*)\s*\|\s*([^|]+?)\s*\|")
TABLE_PLAIN_SKIP_FIRST = frozenset({"ADR", "Condition", "Rule", "Corpus", "Ship"})
EM_DASH = re.compile(r"^([A-Za-z][A-Za-z0-9 \-/']*)\s+—\s+\S")
BULLET_BOLD_EM = re.compile(r"^-\s+\*\*([A-Za-z][A-Za-z0-9 \-/']*)\*\*\s+—\s+\S")
LINE_START_TERM = re.compile(r"^([A-Za-z][A-Za-z0-9 \-/']*):\s+\S")
BOLD_HYPHEN = re.compile(r"^\*\*([A-Za-z][A-Za-z0-9 \-/']*)\*\*\s+-\s+\S")
ITALIC_COLON = re.compile(r"^\*([A-Za-z][A-Za-z0-9 \-/']*)\*:\s+\S")


def load_term_names(terms_text: str) -> frozenset[str]:
    names: set[str] = set()
    for m in HEADING_DEF.finditer(terms_text):
        raw = m.group(2).strip()
        if raw.startswith("Operating bindings"):
            continue
        names.add(raw)
        names.add(raw.lower())
    return frozenset(names)


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


def scan_line(rel_posix: str, line: str, terms: frozenset[str]) -> list[str]:
    if line_is_exempt(rel_posix, line):
        return []
    hits: list[str] = []
    for pat, label in (
        (HEADING_DEF, "heading"),
        (BOLD_COLON_IN, "bold-colon-in"),
        (BOLD_COLON_OUT, "bold-colon-out"),
        (TABLE_BOLD, "table-bold"),
        (TABLE_PLAIN, "table-plain"),
        (EM_DASH, "em-dash"),
        (BULLET_BOLD_EM, "bullet-bold-em"),
        (LINE_START_TERM, "line-start-colon"),
        (BOLD_HYPHEN, "bold-hyphen"),
        (ITALIC_COLON, "italic-colon"),
    ):
        m = pat.match(line)
        if not m:
            continue
        if label == "heading":
            title = m.group(2).strip()
        elif label == "table-plain":
            title = m.group(1).strip()
            second = m.group(2).strip()
            if title in TABLE_PLAIN_SKIP_FIRST or re.fullmatch(r"UC\d+", title):
                continue
            if len(second) < 6:
                continue
        else:
            title = m.group(1).strip()
        if term_matches(title, terms):
            hits.append(f"{rel_posix}: {label} defines {title!r}")
    return hits


def scan_markdown(rel_posix: str, text: str, terms: frozenset[str]) -> list[str]:
    if is_path_fully_excluded(rel_posix):
        return []
    body = strip_fences(text)
    hits: list[str] = []
    for line in body.splitlines():
        hits.extend(scan_line(rel_posix, line, terms))
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
        if is_path_fully_excluded(rel):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        violations.extend(scan_markdown(rel, text, terms))
    return violations
