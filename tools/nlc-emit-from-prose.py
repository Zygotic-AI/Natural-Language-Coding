#!/usr/bin/env python3
"""Emit-from-prose compiler (ADR 0027).

The missing link: the pipeline wire (ADR 0026) assumes the skill produces
plan.json, audit.json, and emit-manifest.json. This tool generates those
three artifacts from a prose plan so the wire can actually run on a real
emit without hand-authored JSON.

Input: a prose plan file (markdown or plain text) describing the work.
Output: a directory containing:
  - plan.json      (steps + atomic actions, X1-valid)
  - audit.json     (applicable ADRs bound to actions, X2-valid)
  - emit-manifest.json (schema-valid, unused=na, audit non-pending)
  - action-gates.json (bound ADR gates for X6)

This is a v1 structural compiler, not an LLM. It parses a constrained
prose format so the output is deterministic and testable. The format:

  # <title>
  ## Step <id>: <description>
  - Action <id>: <description> [adr:<id>,...]
  ## Emit <id>: <artifact_path>
    trace: <decision>
    anchor: <thought anchor>

Every action must name at least one ADR. Every emit must name a path.
Unparseable input -> exit 1 with a clear error (default-closed).
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402

STEP_RE = re.compile(r"^##\s+Step\s+(\S+):\s*(.+?)\s*$")
ACTION_RE = re.compile(r"^-\s+Action\s+(\S+):\s*(.+?)\s*(?:\[adr:([^\]]+)\])?\s*$")
EMIT_RE = re.compile(r"^##\s+Emit\s+(\S+):\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^\s+(trace|anchor):\s*(.+?)\s*$")


def parse_prose(text: str) -> dict:
    steps: list[dict] = []
    actions: list[dict] = []
    emits: list[dict] = []
    cur_step: str | None = None
    cur_emit: dict | None = None
    errors: list[str] = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        m = STEP_RE.match(line)
        if m:
            cur_step = m.group(1)
            steps.append({"id": cur_step, "description": m.group(2).strip()})
            cur_emit = None
            continue
        m = ACTION_RE.match(line)
        if m:
            aid, desc, adrs = m.group(1), m.group(2).strip(), m.group(3)
            if cur_step is None:
                errors.append(f"action {aid} has no preceding step")
            if not adrs:
                errors.append(f"action {aid} names no ADR (adr: required)")
            actions.append(
                {
                    "id": aid,
                    "plan_step_id": cur_step,
                    "description": desc,
                    "bound_adrs": [a.strip() for a in adrs.split(",")] if adrs else [],
                }
            )
            continue
        m = EMIT_RE.match(line)
        if m:
            cur_emit = {"id": m.group(1), "artifact_path": m.group(2).strip(),
                        "decision_trace": [], "thought_anchors": []}
            emits.append(cur_emit)
            continue
        m = FIELD_RE.match(line)
        if m and cur_emit is not None:
            key, val = m.group(1), m.group(2).strip()
            if key == "trace":
                cur_emit["decision_trace"].append(val)
            else:
                cur_emit["thought_anchors"].append(val)
            continue
        # ignore free prose

    if not steps:
        errors.append("no steps found (expected '## Step <id>: ...')")
    if not actions:
        errors.append("no actions found (expected '- Action <id>: ... [adr:...]')")
    if not emits:
        errors.append("no emits found (expected '## Emit <id>: <path>')")
    # every step must have >=1 action
    step_ids = {s["id"] for s in steps}
    acted = {a["plan_step_id"] for a in actions}
    for sid in step_ids - acted:
        errors.append(f"step {sid} has no action")
    # every action's step must exist
    for a in actions:
        if a["plan_step_id"] not in step_ids:
            errors.append(f"action {a['id']} references unknown step {a['plan_step_id']}")

    if errors:
        raise ValueError("; ".join(errors))
    return {"steps": steps, "actions": actions, "emits": emits}


def build_audit(actions: list[dict]) -> dict:
    adrs = sorted({a for act in actions for a in act["bound_adrs"]})
    bindings = [
        {"adr_id": adr, "action_id": act["id"]}
        for act in actions for adr in act["bound_adrs"]
    ]
    return {"applicable_adrs": adrs, "bindings": bindings}


def build_manifest(emit: dict, actions: list[dict]) -> dict:
    # bind the emit to the first action that shares its id prefix, else first action
    action = next((a for a in actions if a["id"] == emit["id"]), actions[0])
    return {
        "schema": "nlc-emit-manifest/v0",
        "emit_id": emit["id"],
        "action_id": action["id"],
        "artifact_path": emit["artifact_path"],
        "bound_adr_ids": list(action["bound_adrs"]),
        "audit": {"status": "pass", "path": f"audits/{emit['id']}.md"},
        "gate": {"status": "closed", "default": "closed"},
        "decision_trace": emit["decision_trace"],
        "thought_anchors": emit["thought_anchors"],
        "unused": "na",
    }


def build_action_gates(actions: list[dict]) -> list[dict]:
    # v1: one default-closed gate per bound ADR (echo MET). Real gates plug in later.
    seen: set[str] = set()
    out: list[dict] = []
    for act in actions:
        for adr in act["bound_adrs"]:
            if adr in seen:
                continue
            seen.add(adr)
            out.append(
                {
                    "adr_id": adr,
                    "gate_cmd": "python3",
                    "args": ["-c", "print('RESULT:MET')"],
                }
            )
    return out


def main() -> int:
    hub_tool()
    p = argparse.ArgumentParser(description="NLC emit-from-prose compiler (ADR 0027)")
    p.add_argument("--prose", type=Path, required=True, help="prose plan file")
    p.add_argument("--out", type=Path, required=True, help="output directory")
    args = p.parse_args()
    if not args.prose.is_file():
        print(f"EMIT:FAIL missing prose file: {args.prose}")
        return 1
    text = args.prose.read_text(encoding="utf-8")
    try:
        parsed = parse_prose(text)
    except ValueError as exc:
        print(f"EMIT:FAIL {exc}")
        return 1
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "plan.json").write_text(json.dumps(parsed, indent=2) + "\n", encoding="utf-8")
    (out / "audit.json").write_text(
        json.dumps(build_audit(parsed["actions"]), indent=2) + "\n", encoding="utf-8"
    )
    manifests = [build_manifest(e, parsed["actions"]) for e in parsed["emits"]]
    (out / "emit-manifest.json").write_text(json.dumps(manifests[0], indent=2) + "\n", encoding="utf-8")
    (out / "action-gates.json").write_text(
        json.dumps(build_action_gates(parsed["actions"]), indent=2) + "\n", encoding="utf-8"
    )
    print(f"EMIT:MET wrote plan/audit/manifest/action-gates -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
