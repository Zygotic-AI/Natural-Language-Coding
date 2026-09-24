#!/usr/bin/env python3
"""Move fitness-*.py interiors into tools/nouns/<slug>/ with thin adapters (X4 t4)."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
NOUNS = TOOLS / "nouns"
REMAINDER = ROOT / "integrity" / "hub-x4-remainder.json"

VERBS_SCHEMA = """{
  "version": "1",
  "verbs": {
    "run": {
      "input": { "type": "object" },
      "output": { "type": "object" },
      "error": { "type": "object" }
    }
  }
}
"""

ADAPTER_TEMPLATE = '''#!/usr/bin/env python3
"""{doc}"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.{slug} import *  # noqa: F403


if __name__ == "__main__":
    sys.exit(main())
'''


def kebab_to_slug(name: str) -> str:
    base = name.removesuffix(".py")
    return base.replace("-", "_")


def one_line_doc(path: Path) -> str:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        doc = ast.get_docstring(tree) or path.name
        return doc.splitlines()[0].strip()
    except SyntaxError:
        return path.name


def is_thin_adapter(text: str, slug: str) -> bool:
    return f"nouns.{slug}" in text and len(text) < 2500


def ensure_scaffold(noun_dir: Path, slug: str, doc: str) -> None:
    noun_dir.mkdir(parents=True, exist_ok=True)
    init_py = noun_dir / "__init__.py"
    if not init_py.is_file():
        init_py.write_text(
            f'"""Noun package for tools/{slug.replace("_", "-")}.py fitness adapter."""\n'
            f"from .{slug} import *  # noqa: F403\n",
            encoding="utf-8",
        )
    readme = noun_dir / "README.md"
    if not readme.is_file():
        readme.write_text(f"# {slug}\n\nX4 noun for hub `fitness-*` adapter.\n", encoding="utf-8")
    for name, body in (
        ("adjectives.txt", "run\n"),
        ("fields.txt", ""),
        ("schemas/verbs.schema.json", VERBS_SCHEMA),
    ):
        p = noun_dir / name
        if not p.is_file():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")


def insert_boundary(source: str) -> str:
    import ast as _ast

    if 'BOUNDARY = "bba-emit"' in source:
        try:
            tree = _ast.parse(source)
            for node in _ast.walk(tree):
                if isinstance(node, _ast.Assign):
                    for t in node.targets:
                        if (
                            isinstance(t, _ast.Name)
                            and t.id == "BOUNDARY"
                            and isinstance(node.value, _ast.Constant)
                            and node.value.value == "bba-emit"
                        ):
                            return source
        except SyntaxError:
            pass
    cleaned = source.replace('\n\nBOUNDARY = "bba-emit"\n\n', "\n\n")
    lines = cleaned.splitlines(keepends=True)
    insert_at = 0
    if lines and lines[0].startswith("#!"):
        insert_at = 1
    if insert_at < len(lines) and lines[insert_at].strip().startswith('"""'):
        if lines[insert_at].count('"""') >= 2:
            insert_at += 1
        else:
            insert_at += 1
            while insert_at < len(lines) and '"""' not in lines[insert_at]:
                insert_at += 1
            insert_at += 1
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    while insert_at < len(lines) and lines[insert_at].strip().startswith("from __future__"):
        insert_at += 1
    if insert_at > 0 and "from __future__" in cleaned:
        lines.insert(insert_at, '\nBOUNDARY = "bba-emit"\n\n')
    else:
        lines.insert(insert_at, '\nBOUNDARY = "bba-emit"\n\n')
    return "".join(lines)


SKIP_NAMES = {
    "hub-x4-migrate-fitness-noun.py",
    "hub-x4-refresh-inventory.py",
}


def migrate_file(adapter_path: Path, dry_run: bool) -> str | None:
    if adapter_path.name in SKIP_NAMES:
        return "skip:tooling"
    if not adapter_path.name.startswith("fitness-") or not adapter_path.suffix == ".py":
        return "skip:not-fitness"
    slug = kebab_to_slug(adapter_path.name)
    noun_dir = NOUNS / slug
    noun_py = noun_dir / f"{slug}.py"
    text = adapter_path.read_text(encoding="utf-8")
    if is_thin_adapter(text, slug) and noun_py.is_file():
        return "skip:already"
    if noun_py.is_file() and not is_thin_adapter(text, slug):
        return f"error:{adapter_path.name}:noun exists but adapter not thin"
    doc = one_line_doc(adapter_path)
    body = insert_boundary(text)
    body = body.replace(
        "Path(__file__).resolve().parents[1]",
        "Path(__file__).resolve().parents[3]",
    )
    if dry_run:
        return f"would:{adapter_path.name}->{slug}"
    ensure_scaffold(noun_dir, slug, doc)
    noun_py.write_text(body, encoding="utf-8")
    adapter_path.write_text(
        ADAPTER_TEMPLATE.format(doc=doc.replace('"', "'"), slug=slug),
        encoding="utf-8",
    )
    return f"ok:{adapter_path.name}"


def fitness_only_files() -> list[str]:
    if not REMAINDER.is_file():
        return sorted(p.name for p in TOOLS.glob("fitness-*.py"))
    data = json.loads(REMAINDER.read_text(encoding="utf-8"))
    names = [
        e["file"]
        for e in (data.get("entries") or [])
        if e.get("class") == "fitness-only" and (e.get("file") or "").startswith("fitness-")
    ]
    if names:
        return sorted(names)
    return sorted(
        p.name
        for p in TOOLS.glob("fitness-*.py")
        if p.name not in SKIP_NAMES
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()
    targets = args.files or fitness_only_files()
    if args.limit > 0:
        targets = targets[: args.limit]
    results: list[str] = []
    errors = 0
    for name in targets:
        path = TOOLS / name
        if not path.is_file():
            results.append(f"missing:{name}")
            errors += 1
            continue
        r = migrate_file(path, args.dry_run)
        results.append(r or "error:unknown")
        if r and r.startswith("error:"):
            errors += 1
    for line in results:
        print(line)
    if errors:
        return 1
    print(f"MIGRATE:{'DRY' if args.dry_run else 'DONE'} count={len(targets)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
