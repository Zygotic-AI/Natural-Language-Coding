"""Designed pass: invoice-correct produces a generated apply_payment edge."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TREE = ROOT / "examples" / "invoice-correct"
GEN = ROOT / "tools" / "generate-impact-graph.py"


def load_gen():
    spec = importlib.util.spec_from_file_location("generate_impact_graph", GEN)
    if spec is None or spec.loader is None:
        print("ASSERT:FAIL cannot load generate-impact-graph.py")
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    if not TREE.is_dir():
        print("ASSERT:FAIL missing examples/invoice-correct")
        return 1
    graph = load_gen().build(TREE.resolve())
    if not graph.get("generated"):
        print("ASSERT:FAIL missing generated marker")
        return 1
    goals = graph.get("goals") or {}
    payment = goals.get("record-bank-payment") or {}
    calls = payment.get("calls") or []
    print("GRAPH record-bank-payment " + ",".join(calls))
    if "invoice.apply_payment" not in calls:
        print("ASSERT:FAIL expected invoice.apply_payment on record-bank-payment")
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    print("ASSERT:PASS generated graph includes invoice.apply_payment")
    return 0


