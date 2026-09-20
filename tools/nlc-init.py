#!/usr/bin/env python3
"""UC15 greenfield: scaffold a new compiled-system repo.

Brownfield (existing code) is beta — this tool refuses non-empty product trees.

Usage:
  python3 tools/nlc-init.py /path/to/new-app --name MyApp
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_distribution import (  # noqa: E402
    default_install_root,
    hub_active_path,
    read_hub_version,
    write_project_lock,
)
from nlc_requirements import hub_tool  # noqa: E402

CHARTER_POINTER = """# Charter

This adopter uses Boundary-Based Programming. SSOT:

https://github.com/Zygotic-AI/Natural-Language-Coding/blob/main/CHARTER.md

Pin a commit or fork when you ratify adoption.
"""

README = """# {name}

Greenfield **compiled system** under Natural Language Coding (NLC).

## Agent workflow

1. `/interview` — goals, requirements, knowledge domains
2. `/planit` — bind, generate, gate, prove

## Prove and ship

```bash
python3 "$NLC_HUB/tools/ci_fitness.py"
python3 "$NLC_HUB/tools/release-audit.py" .
```

Set `NLC_HUB` to your hub install (default `~/.local/share/nlc/hub`).

Prove PASS ≠ shipped. Human `Released-by:` on `CONFIRM.md` when required.
"""

CONFIRM = """# Confirm

change class: E

Released-by:
"""


def has_product_content(target: Path) -> bool:
    for sub in ("domain", "goals"):
        p = target / sub
        if not p.is_dir():
            continue
        if any(p.iterdir()):
            return True
    return False


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="NLC greenfield repo scaffold")
    parser.add_argument("target", type=Path, help="New empty directory to create")
    parser.add_argument("--name", default="MyApp", help="Project title for README")
    parser.add_argument("--force", action="store_true", help="Allow existing empty dirs only")
    args = parser.parse_args()
    target = args.target.resolve()

    if target.exists() and has_product_content(target):
        sys.stderr.write(
            "nlc-init: brownfield / non-empty domain or goals — beta only.\n"
            "See docs/adoption/BROWNFIELD.md (manual BOOTSTRAP.md path).\n"
        )
        return 2

    target.mkdir(parents=True, exist_ok=True)
    (target / "adrs").mkdir(exist_ok=True)
    (target / "domain").mkdir(exist_ok=True)
    (target / "goals").mkdir(exist_ok=True)
    (target / "knowledge").mkdir(exist_ok=True)
    (target / "rules").mkdir(exist_ok=True)

    (target / "CHARTER.md").write_text(CHARTER_POINTER, encoding="utf-8")
    (target / "README.md").write_text(
        README.format(name=args.name), encoding="utf-8"
    )
    (target / "CONFIRM.md").write_text(CONFIRM, encoding="utf-8")
    (target / "knowledge" / "facts.json").write_text(
        json.dumps({"facts": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    (target / "rules" / "adopted.json").write_text(
        json.dumps({"adoptions": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    gitignore = target / ".gitignore"
    extra = ".nlc/store/\n"
    if gitignore.is_file():
        text = gitignore.read_text(encoding="utf-8")
        if ".nlc/store/" not in text:
            gitignore.write_text(text.rstrip() + "\n" + extra, encoding="utf-8")
    else:
        gitignore.write_text(
            "__pycache__/\n.venv/\nnode_modules/\n" + extra,
            encoding="utf-8",
        )

    if os.environ.get("NLC_HUB"):
        hub_root = Path(os.environ["NLC_HUB"]).resolve()
    else:
        hub_root = hub_active_path(default_install_root())
        if not (hub_root / "integrity" / "nlc-version.json").is_file():
            hub_root = ROOT
    hub_ver = read_hub_version(hub_root)
    lock_path = write_project_lock(target, hub_version=hub_ver, store="user")

    wf_src = ROOT / "templates" / "adopter" / "github-workflows-nlc-prove.yml"
    if wf_src.is_file():
        wf_dest = target / ".github" / "workflows" / "nlc-prove.yml"
        wf_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(wf_src, wf_dest)

    sys.stdout.write(f"NLC_INIT:MET\npath: {target}\n")
    sys.stdout.write(f"lock: {lock_path}\nhub: {hub_ver}\n")
    sys.stdout.write("next: /interview in Cursor, then /planit\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
