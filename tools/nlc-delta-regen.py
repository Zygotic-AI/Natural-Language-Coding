#!/usr/bin/env python3
"""UC9 v1: blast-radius regen plan from an impact graph.

Does not run PLANIT or rewrite code. Given a changed boundary, lists goals
(and paths) to re-bind, re-generate, and re-prove in order.

Input:
  python3 tools/nlc-delta-regen.py [repo-root] --change <kind>:<id>

Kinds:
  verb   — Invoice.apply_payment  (Noun.verb)
  goal   — record-bank-payment     (goal folder name)
  rule   — pan-no-return           (conservative: all goals; cite rule id in plan)
  noun   — Invoice                 (all goals calling any Invoice.* verb)

Output: JSON on stdout. Exit 0. Exit 2 if --change missing or unknown kind.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_requirements import hub_tool  # noqa: E402


def impact_graph(root: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "generate-impact-graph.py"), str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "impact graph failed\n")
        sys.exit(1)
    return json.loads(proc.stdout)


def goals_calling(graph: dict, callee: str) -> list[str]:
    out: list[str] = []
    for gid, entry in graph.get("goals", {}).items():
        if callee in entry.get("calls", []):
            out.append(gid)
    return sorted(out)


def goals_calling_noun(graph: dict, noun: str) -> list[str]:
    prefix = f"{noun}."
    out: list[str] = []
    for gid, entry in graph.get("goals", {}).items():
        for call in entry.get("calls", []):
            if call.startswith(prefix):
                out.append(gid)
                break
    return sorted(out)


def all_goal_ids(graph: dict) -> list[str]:
    return sorted(graph.get("goals", {}).keys())


def plan_steps(goal_ids: list[str], graph: dict, reason: str) -> list[dict]:
    steps: list[dict] = []
    for gid in goal_ids:
        path = graph.get("goals", {}).get(gid, {}).get("path", "")
        steps.append(
            {
                "goal_id": gid,
                "path": path,
                "planit": [
                    "bind statements to changed requirement/ADR/rule/contract",
                    "generate goal implementation (PLANIT 6)",
                    "gate artifact (PLANIT 6.5)",
                ],
                "reason": reason,
            }
        )
    return steps


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="UC9 delta-regen plan")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--change",
        required=True,
        help="kind:id e.g. verb:Invoice.apply_payment, goal:record-bank-payment, noun:Invoice, rule:pan-no-return",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    if ":" not in args.change:
        sys.stderr.write("change must be kind:id\n")
        return 2
    kind, ident = args.change.split(":", 1)
    graph = impact_graph(root)

    if kind == "verb":
        goal_ids = goals_calling(graph, ident)
        reason = f"caller of changed verb {ident}"
    elif kind == "goal":
        goal_ids = [ident] if ident in graph.get("goals", {}) else []
        reason = f"direct change to goal {ident}"
    elif kind == "noun":
        goal_ids = goals_calling_noun(graph, ident)
        reason = f"caller of noun {ident} verbs"
    elif kind == "rule":
        goal_ids = all_goal_ids(graph)
        reason = f"conservative regen for rule {ident} (v1: all goals; narrow in UC9 v2)"
    else:
        sys.stderr.write(f"unknown kind: {kind}\n")
        return 2

    payload = {
        "uc": "UC9",
        "version": 1,
        "root": str(root),
        "change": {"kind": kind, "id": ident},
        "goals_to_regen": goal_ids,
        "steps": plan_steps(goal_ids, graph, reason),
        "prove": "python3 tools/ci_fitness.py (or adopter-bound suite) on full tree after all steps",
        "note": "Machine plan only; run PLANIT per step. Do not patch emit without intent change.",
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
