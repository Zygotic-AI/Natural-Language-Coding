"""Growable authoring checks for a published skills tree (pre-release and post-install)."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CHECKLIST = ROOT / "integrity" / "skill-author-checklist.json"
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")
MD_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")


def load_checklist() -> list[dict]:
    data = json.loads(CHECKLIST.read_text(encoding="utf-8"))
    checks = data.get("checks") or []
    if not isinstance(checks, list):
        return []
    return [c for c in checks if isinstance(c, dict) and c.get("id")]


def extract_frontmatter(text: str) -> tuple[str | None, str | None]:
    if not text.startswith("---\n"):
        return None, "missing opening ---"
    rest = text[4:]
    end = rest.find("\n---\n")
    if end < 0:
        return None, "missing closing ---"
    return rest[:end], None


def check_frontmatter_yaml(skill_dir: Path, skill_md: Path, text: str) -> list[str]:
    rel = skill_md.as_posix()
    fm, err = extract_frontmatter(text)
    if err:
        return [f"frontmatter-yaml {rel}: {err}"]
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError as exc:
        return [f"frontmatter-yaml {rel}: YAML parse error: {exc}"]
    if not isinstance(data, dict):
        return [f"frontmatter-yaml {rel}: frontmatter must be a mapping"]
    name = data.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name):
        return [
            f"frontmatter-yaml {rel}: name must be a plain identifier matching the folder "
            f"(got {name!r})"
        ]
    if name != skill_dir.name:
        return [f"frontmatter-yaml {rel}: name {name!r} does not match folder {skill_dir.name!r}"]
    return []


def _href_is_in_tree(href: str, from_file: Path, skills_root: Path) -> str | None:
    target = href.strip()
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    path_part = target.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return None
    if path_part.startswith("/"):
        return f"absolute path {target!r}"
    resolved = (from_file.parent / path_part).resolve()
    root = skills_root.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return f"leaves skills tree: {target}"
    if not resolved.is_file():
        return f"missing target {target}"
    return None


def check_in_skill_links(skills_root: Path, md_path: Path, text: str) -> list[str]:
    rel = md_path.as_posix()
    violations: list[str] = []
    for match in MD_LINK.finditer(text):
        href = match.group(2).strip()
        reason = _href_is_in_tree(href, md_path, skills_root)
        if reason:
            violations.append(f"in-skill-links {rel}: {reason}")
    return violations


def run_checks(skills_root: Path) -> list[str]:
    root = skills_root.resolve()
    if not root.is_dir():
        return [f"skills root missing: {root}"]
    wanted = {c["id"] for c in load_checklist()}
    unknown = wanted - {"frontmatter-yaml", "in-skill-links"}
    violations: list[str] = []
    for cid in sorted(unknown):
        violations.append(f"checklist id {cid} has no implementation")
    skill_files = sorted(root.glob("*/SKILL.md"))
    if not skill_files:
        violations.append(f"no SKILL.md under {root}")
        return violations
    for skill_md in skill_files:
        text = skill_md.read_text(encoding="utf-8")
        skill_dir = skill_md.parent
        if "frontmatter-yaml" in wanted:
            violations.extend(check_frontmatter_yaml(skill_dir, skill_md, text))
    if "in-skill-links" in wanted:
        for md_path in sorted(root.rglob("*.md")):
            if md_path.name == "README.md" and md_path.parent == root:
                continue
            text = md_path.read_text(encoding="utf-8")
            violations.extend(check_in_skill_links(root, md_path, text))
    return violations


def report(violations: list[str]) -> int:
    for item in violations:
        print(f"VIOLATION {item}")
    if violations:
        print("SKILL_AUTHOR:NOT_MET")
        return 1
    print("SKILL_AUTHOR:MET")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = ROOT / ".agents" / "skills"
    if "--root" in args:
        i = args.index("--root")
        if i + 1 >= len(args):
            print("VIOLATION --root needs a path", file=sys.stderr)
            print("SKILL_AUTHOR:NOT_MET")
            return 2
        root = Path(args[i + 1])
    if not CHECKLIST.is_file():
        print("VIOLATION missing integrity/skill-author-checklist.json")
        print("SKILL_AUTHOR:NOT_MET")
        return 1
    return report(run_checks(root))


if __name__ == "__main__":
    raise SystemExit(main())
