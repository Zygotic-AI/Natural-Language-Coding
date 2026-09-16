#!/usr/bin/env python3
"""Release audit: AI gates + human gates, with numbered remediations.

Pipeline hook. Run before merge/deploy. Not the same as ci-fitness.sh
(that suite proves landmines + the teaching tree). This tool proves a
*product tree* may ship.

Exit 0 = RELEASE:MET. Exit 1 = RELEASE:NOT_MET.
Class C can pass ci-fitness without a human. It cannot pass this tool
without `Released-by: <human name>` on CONFIRM.md.

Input: optional argv tree (default: cwd).
Output: GATE lines, then UNMET blocks with Step 1…N, then RELEASE:MET|NOT_MET.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import product_tree  # noqa: E402

NOTES = ("CONFIRM.md", "PROPOSAL.md")
CLASS = re.compile(r"change\s*class\s*[:*\s]*([A-F])\b", re.I)
RELEASED = re.compile(r"^Released-by:\s*(.*)$", re.I | re.M)
AGENT = re.compile(
    r"\b(agent|ai|bot|assistant|grok|confirmer|bbp-confirmer|claude|gpt|copilot)\b",
    re.I,
)


def note_text(tree: Path) -> tuple[Path | None, str]:
    for name in NOTES:
        path = tree / name
        if path.is_file():
            return path, path.read_text(errors="replace")
    return None, ""


def run_fitness(script: Path, tree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(script), str(tree)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out


def binders() -> dict[str, dict]:
    matrix = ROOT / "integrity" / "binding-matrix.json"
    if not matrix.is_file():
        return {}
    data = json.loads(matrix.read_text())
    out: dict[str, dict] = {}
    for row in data.get("requirements", []):
        binder = row.get("binder") or ""
        if binder.startswith("tools/fitness"):
            out[Path(binder).name] = row
    return out


def remediate_fitness(script: str, tree: str, row: dict | None) -> list[str]:
    rid = (row or {}).get("id") or script
    audit = (row or {}).get("audit_def") or "integrity/audits/"
    return [
        f"Open `{audit}` (requirement {rid}).",
        f"From repo root run: `python3 tools/{script} {tree}`",
        "Fix every `VIOLATION` line it prints. Do not ignore RESULT:NOT_MET.",
        f"Re-run: `python3 tools/{script} {tree}` until it prints RESULT:MET.",
        f"Re-run: `python3 tools/release-audit.py {tree}`",
    ]


def print_unmet(n: int, gate: str, steps: list[str]) -> None:
    print(f"UNMET {n} {gate}")
    for i, step in enumerate(steps, start=1):
        print(f"  Step {i}: {step}")


def main() -> int:
    tree = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    rel_tree = str(tree.relative_to(ROOT) if tree.is_relative_to(ROOT) else tree)
    unmet: list[tuple[str, list[str]]] = []

    note_path, text = note_text(tree)
    if note_path is None:
        unmet.append((
            "H-CONFIRM",
            [
                f"Create `{rel_tree}/CONFIRM.md`.",
                "Copy the skeleton from `examples/invoice-correct/CONFIRM.md`.",
                "Fill C1–C24 as PASS / FAIL / N/A with file:line evidence.",
                "Do not write Ratified-by or Released-by yourself if you are the confirmer agent.",
                f"Run: `python3 tools/release-audit.py {rel_tree}`",
            ],
        ))
    else:
        m = CLASS.search(text)
        if m is None:
            unmet.append((
                "H-CLASS",
                [
                    f"Open `{note_path.relative_to(ROOT) if note_path.is_relative_to(ROOT) else note_path}`.",
                    "Add a line: `**Change class:** C` (or A/B/D/E/F — A if you changed how a noun works).",
                    f"Run: `python3 tools/fitness-c1.py {rel_tree}`",
                    f"Run: `python3 tools/release-audit.py {rel_tree}`",
                ],
            ))
        released = RELEASED.search(text)
        name = released.group(1).strip() if released else ""
        if not released or not name:
            unmet.append((
                "H-RELEASE",
                [
                    f"Open `{note_path.relative_to(ROOT) if note_path.is_relative_to(ROOT) else note_path}`.",
                    "Add a line at the end: `Released-by: Your Name` (a human in the ship role, not an agent name).",
                    "Do not use agent, ai, bot, confirmer, grok, or any model name.",
                    f"Run: `python3 tools/release-audit.py {rel_tree}`",
                ],
            ))
        elif AGENT.search(name):
            unmet.append((
                "H-RELEASE-AGENT",
                [
                    f"Open `{note_path.relative_to(ROOT) if note_path.is_relative_to(ROOT) else note_path}`.",
                    "Delete the current `Released-by:` value. A human must write their name.",
                    "The confirmer / ship agent is not allowed to sign this line.",
                    f"Run: `python3 tools/release-audit.py {rel_tree}`",
                ],
            ))

    rows = binders()
    fitness_dir = ROOT / "tools"
    for script in sorted(fitness_dir.glob("fitness-*.py")):
        code, out = run_fitness(script, tree)
        if code == 0:
            print(f"GATE MET {script.name}")
            continue
        print(f"GATE NOT_MET {script.name}")
        row = rows.get(script.name)
        rid = (row or {}).get("id") or script.name
        unmet.append((f"AI-{rid}", remediate_fitness(script.name, rel_tree, row)))

    if not unmet:
        print("RELEASE:MET")
        return 0
    print("---")
    for i, (gate, steps) in enumerate(unmet, start=1):
        print_unmet(i, gate, steps)
    print("RELEASE:NOT_MET")
    return 1


if __name__ == "__main__":
    sys.exit(main())
