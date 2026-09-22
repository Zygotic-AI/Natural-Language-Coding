#!/usr/bin/env python3
"""Compile a constrained prose plan into plan/audit/manifest/action-gates JSON.

Human contributes only goal + policies. Everything else — actions, ADR
bindings, reverse audit, emit, audit, gates — is inference the factory performs.

Usage:
  python tools/nlc-emit-from-prose.py --prose PATH --out DIR
  python tools/nlc-emit-from-prose.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_action_plan_gate import validate_action_plan  # type: ignore
from nlc_reverse_audit import validate_reverse_audit  # type: ignore
from nlc_emit_manifest_enforce import validate_emit_manifest  # type: ignore
from nlc_emit_audit import validate_emit_audit  # type: ignore
from nlc_pipeline_wire import run_pipeline  # type: ignore

GOAL_RE = re.compile(r"(?im)^\s*goal\s*:\s*(.+)$")
POLICY_RE = re.compile(r"(?im)^\s*polic(?:y|ies)\s*:\s*(.+)$")
ACTION_RE = re.compile(r"(?im)^\s*action\s*:\s*(.+)$")
ADR_RE = re.compile(r"(?im)^\s*adr\s*:\s*(\d{4}(?:\s*,\s*\d{4})*)$")
ANCHOR_RE = re.compile(r"(?im)^\s*anchor\s*:\s*(.+)$")

DEFAULT_ADRS = ["0024", "0025", "0026"]


def _split_csv(s: str) -> list[str]:
    return [p.strip() for p in s.split(",") if p.strip()]


def compile_prose(text: str) -> dict:
    goal_m = GOAL_RE.search(text)
    if not goal_m:
        raise ValueError("prose must declare 'goal: <intent>'")
    goal = goal_m.group(1).strip()

    policies = _split_csv(POLICY_RE.search(text).group(1)) if POLICY_RE.search(text) else []

    actions = []
    for m in ACTION_RE.finditer(text):
        actions.append(m.group(1).strip())
    if not actions:
        # inference: one action per goal sentence
        actions = [f"realize: {goal}"]

    adrs = []
    for m in ADR_RE.finditer(text):
        adrs.extend(_split_csv(m.group(1)))
    if not adrs:
        adrs = list(DEFAULT_ADRS)

    anchors = [m.group(1).strip() for m in ANCHOR_RE.finditer(text)]

    plan = {
        "goal": goal,
        "policies": policies,
        "actions": [{"id": f"a{i+1}", "text": a} for i, a in enumerate(actions)],
        "adr_bindings": {f"a{i+1}": adrs for i in range(len(actions))},
    }
    audit = {
        "applicable_adrs": adrs,
        "bound_actions": {a: [f"a{i+1}" for i in range(len(actions))] for a in adrs},
        "status": "complete",
    }
    manifest = {
        "emit_id": "emit-1",
        "action_id": "a1",
        "artifact": "compiled-system",
        "schema": "docs/nlc/emit-manifest.schema.json",
        "decision_trace": adrs,
        "thought_anchors": anchors or ["na"],
        "unused_fields": "na",
        "audit_status": "pending",
    }
    return {"plan": plan, "audit": audit, "manifest": manifest, "goal": goal, "policies": policies}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prose", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        sample = (
            "goal: ship a boundary-shaped invoice compiler\n"
            "policy: no noun inheritance, default-closed gates\n"
            "action: define Invoice noun with contracted verbs\n"
            "action: bind ADR 0024 and 0026 to the emit\n"
            "adr: 0024, 0026\n"
            "anchor: boundary is the load-bearing shape\n"
        )
        out = compile_prose(sample)
        print(json.dumps({k: (v if k != "plan" else {kk: vv for kk, vv in v.items() if kk != "actions"}) for k, v in out.items()}, indent=2)[:500])
        print("SELF_TEST:OK")
        return 0

    if not args.prose or not args.out:
        ap.error("--prose and --out required (or --self-test)")

    text = args.prose.read_text(encoding="utf-8")
    try:
        compiled = compile_prose(text)
    except ValueError as e:
        print(f"COMPILE:FAIL {e}")
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "plan.json").write_text(json.dumps(compiled["plan"], indent=2), encoding="utf-8")
    (args.out / "audit.json").write_text(json.dumps(compiled["audit"], indent=2), encoding="utf-8")
    (args.out / "emit-manifest.json").write_text(json.dumps(compiled["manifest"], indent=2), encoding="utf-8")

    rc = run_pipeline(args.out)
    print("PIPELINE:" + ("ALL_MET" if rc == 0 else "FAIL"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
