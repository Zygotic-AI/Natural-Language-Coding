#!/usr/bin/env python3
"""Link dictionary terms in markdown to docs/TERMS.md#anchor (one pass, longest match first)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TERMS = ROOT / "docs" / "TERMS.md"

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "dist",
    "reviews",
    "theory/history",
}

EXTRA_ALIASES: dict[str, str] = {
    "Natural Language Coding": "NLC",
    "verify deep": "verify-deep",
    "gate-record": "Gate record",
    "gate record": "Gate record",
    "handoff refused": "handoff_refused",
    "produce package": "Produce package",
    "plan-audit": "Plan audit",
    "plan audit": "Plan audit",
    "change-adversarial": "Change adversarial",
    "delta-regen": "Delta-regen queue",
    "delta regen": "Delta-regen queue",
    "requirement pack": "Requirement pack",
    "requirement packs": "Requirement pack",
    "code pack": "Code pack",
    "code packs": "Code pack",
    "compiled system": "Compiled system",
    "knowledge domain": "Knowledge domain",
    "knowledge domains": "Knowledge domain",
    "agent noun": "Agent noun",
    "agent nouns": "Agent noun",
    "binding matrix": "Binding matrix",
    "type recipe": "Type recipe",
    "content type": "Content type",
    "Contribution Gate": "Contribution Gate",
    "add-X": "Contribution Gate",
    "SSOT exit": "SSOT exit evidence",
    "quality snapshot": "Quality snapshot",
    "quality evidence": "Quality evidence",
    "Published verb contract": "Published verb contract",
    "published verb contract": "Published verb contract",
    "Ratified-by": "Ratified-by",
    "Released-by": "Released-by",
    "Released-by:": "Released-by",
    "Ratified-by:": "Ratified-by",
    "/planit": "PLANIT",
    "/interview": "Interview",
    "/verify": "verify",
    "verify-deep": "verify-deep",
    "ship-check": "ship-check",
    "BBA-Bindings": "BBA-Bindings",
    "P-020": "SSOT exit evidence",
    "UC9": "UC9",
    "UC14": "UC14",
    "UC15": "UC15",
    "UC16": "UC16",
    "UC18": "UC18",
    "UC19": "UC19",
    "UC20": "UC20",
    "UC21": "UC21",
    "zero-variance": "Zero variance",
    "zero variance": "Zero variance",
    "default-closed": "Default-closed",
    "refuse-wired": "Default-closed",
    "fail-closed": "Default-closed",
    "ai system compiler": "Compiler",
    "AI system compiler": "Compiler",
    "Boundary-Based Programming": "BBP",
    "Boundary-Based Architecture": "BBA",
    "noun inheritance": "Noun inheritance",
    "god-noun": "God-noun",
    "greenfield": "Greenfield",
    "brownfield": "Brownfield",
    "adopter repo": "Adopter",
    "app repo": "Adopter",
    "lock file": "Lock file",
    "lock.json": "Lock file",
    "verified.json": "verify",
    "gate-records.json": "Gate record",
}


def github_slug(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def load_terms() -> dict[str, str]:
    """Map match phrase -> canonical heading for slug."""
    text = TERMS.read_text(encoding="utf-8")
    headings = re.findall(r"^### (.+)$", text, re.M)
    phrase_to_canonical: dict[str, str] = {}
    for h in headings:
        canonical = h.strip()
        phrase_to_canonical[canonical] = canonical
        phrase_to_canonical[canonical.lower()] = canonical
    for alias, canonical in EXTRA_ALIASES.items():
        if canonical in headings or canonical in [phrase_to_canonical.get(canonical, canonical)]:
            phrase_to_canonical[alias] = canonical
        else:
            # canonical might be from headings list with different casing
            for h in headings:
                if h.strip() == canonical:
                    phrase_to_canonical[alias] = h.strip()
                    break
            else:
                phrase_to_canonical[alias] = canonical
    return phrase_to_canonical


def build_patterns(phrase_to_canonical: dict[str, str]) -> list[tuple[re.Pattern[str], str, str]]:
    # Dedupe by canonical; keep longest phrases first
    by_len: list[tuple[str, str]] = []
    seen: set[str] = set()
    for phrase, canonical in sorted(
        phrase_to_canonical.items(), key=lambda x: len(x[0]), reverse=True
    ):
        if phrase in seen:
            continue
        seen.add(phrase)
        escaped = re.escape(phrase)
        # Word boundaries where phrase starts/ends with alnum
        prefix = r"(?<![\w/-])" if phrase[0].isalnum() or phrase[0] == "/" else ""
        suffix = r"(?![\w/-])" if phrase[-1].isalnum() or phrase[-1] in ":)" else ""
        pat = re.compile(prefix + escaped + suffix, re.IGNORECASE if phrase.islower() else 0)
        slug = github_slug(canonical)
        by_len.append((pat, phrase, slug))
    return [(p, ph, sl) for p, ph, sl in by_len]


def rel_terms_href(from_file: Path) -> str:
    rel = Path(os_path_relpath(TERMS, from_file.parent))
    return str(rel).replace("\\", "/")


def os_path_relpath(target: Path, start: Path) -> Path:
    import os

    return Path(os.path.relpath(target, start))


def _inside_existing_link(text: str, start: int) -> bool:
    before = text[:start]
    open_b = before.rfind("[")
    close_b = before.rfind("]")
    open_p = before.rfind("(")
    close_p = before.rfind(")")
    if open_b > close_b:
        return True
    if open_p > close_p and open_p > open_b:
        return True
    return False


def link_segment(segment: str, patterns: list, href: str) -> str:
    if not segment or "TERMS.md#" in segment:
        return segment
    out = segment
    for pat, _phrase, slug in patterns:
        link_tpl = f"[{{}}]({href}#{slug})"
        new_out: list[str] = []
        last = 0
        for m in pat.finditer(out):
            if _inside_existing_link(out, m.start()):
                new_out.append(out[last : m.start()])
                new_out.append(m.group(0))
                last = m.end()
                continue
            new_out.append(out[last : m.start()])
            new_out.append(link_tpl.format(m.group(0)))
            last = m.end()
        new_out.append(out[last:])
        out = "".join(new_out)
    return out


def process_line(line: str, patterns: list, href: str, in_fence: bool) -> str:
    if in_fence:
        return line
    if line.lstrip().startswith("```"):
        return line
    # Split on inline code
    parts = re.split(r"(`[^`]*`)", line)
    for i, part in enumerate(parts):
        if part.startswith("`"):
            continue
        parts[i] = link_segment(part, patterns, href)
    return "".join(parts)


def should_skip_file(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "docs/TERMS.md":
        return True
    for skip in SKIP_DIRS:
        if rel.startswith(skip):
            return True
    return False


def iter_markdown_files() -> list[Path]:
    roots = [
        ROOT / "docs",
        ROOT / "adrs",
        ROOT / "integrity",
        ROOT / "agents",
        ROOT / "content-types",
        ROOT / "migrations",
        ROOT / "templates",
        ROOT / ".agents",
        ROOT / "examples",
    ]
    files: list[Path] = []
    for base in roots:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if should_skip_file(path):
                continue
            files.append(path)
    for name in ("README.md", "AGENTS.md", "DESCRIBE.md", "CHARTER.md", "FINDINGS.md"):
        p = ROOT / name
        if p.is_file():
            files.append(p)
    return files


def process_file(path: Path, patterns: list) -> bool:
    href = rel_terms_href(path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    in_fence = False
    changed = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            new_lines.append(line)
            continue
        new_line = process_line(line, patterns, href, in_fence)
        if new_line != line:
            changed = True
        new_lines.append(new_line)
    if changed:
        path.write_text("".join(new_lines), encoding="utf-8")
    return changed


def main() -> int:
    if not TERMS.is_file():
        print("missing docs/TERMS.md", file=sys.stderr)
        return 1
    phrase_map = load_terms()
    headings = set(re.findall(r"^### (.+)$", TERMS.read_text(encoding="utf-8"), re.M))
    # Fix phrase_map to only use valid canonical headings
    for k, v in list(phrase_map.items()):
        if v not in headings:
            # try case-insensitive
            for h in headings:
                if h.lower() == v.lower():
                    phrase_map[k] = h
                    break
    patterns = build_patterns(phrase_map)
    n = 0
    for path in iter_markdown_files():
        if process_file(path, patterns):
            n += 1
            print(f"linked: {path.relative_to(ROOT)}")
    print(f"TERMS_LINK:MET files_updated={n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
