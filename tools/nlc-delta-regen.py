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
    parser.add_argument(
        "--orchestrate",
        action="store_true",
        help="Emit DELTA_REGEN:STEP lines and optional queue file (UC9 v2)",
    )
    parser.add_argument(
        "--write-queue",
        action="store_true",
        help="Write .nlc/delta-regen-queue.json under repo root",
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

    steps = plan_steps(goal_ids, graph, reason)
    payload = {
        "uc": "UC9",
        "version": 2 if args.orchestrate else 1,
        "root": str(root),
        "change": {"kind": kind, "id": ident},
        "goals_to_regen": goal_ids,
        "steps": steps,
        "prove": "python3 tools/ci_fitness.py (or adopter-bound suite) on full tree after all steps",
        "note": "Run PLANIT per step; gate after each generate (ADR 0010). Do not patch emit without intent change.",
    }
    if args.write_queue:
        queue_dir = root / ".nlc"
        queue_dir.mkdir(parents=True, exist_ok=True)
        queue_path = queue_dir / "delta-regen-queue.json"
        queue_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"DELTA_REGEN:QUEUE path={queue_path}", file=sys.stderr)
    if args.orchestrate:
        total = len(steps)
        for i, step in enumerate(steps, start=1):
            gid = step.get("goal_id", "")
            print(f"DELTA_REGEN:STEP index={i} total={total} goal={gid}")
            print(f"  path: {step.get('path', '')}")
            print(f"  reason: {step.get('reason', '')}")
        print(f"DELTA_REGEN:ORCHESTRATE total={total} change={args.change}")
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
