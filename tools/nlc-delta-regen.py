#!/usr/bin/env python3
"""UC9 v1: blast-radius regen plan from an impact graph.

Does not run PLANIT or rewrite code. Given a changed boundary, lists goals
(and paths) to re-bind, re-generate, and re-prove in order.

Input:
  python3 tools/nlc-delta-regen.py [repo-root] --change <kind>:<id>

Kinds:
  verb   — Invoice.apply_payment  (Noun.verb)
  goal   — record-bank-payment     (goal folder name)
  rule   — pan-no-return           (goals via rules/goal-bindings.json + rule tags)
  noun   — Invoice                 (all goals calling any Invoice.* verb)

Output: JSON on stdout. Exit 0. Exit 2 if --change missing or unknown kind.
"""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.delta_regen import *  # noqa: F403
__all__ = ['ROOT', 'all_goal_ids', 'goals_calling', 'goals_calling_noun', 'impact_graph', 'main', 'plan_steps']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

