#!/usr/bin/env python3
"""Full NLC audit — single machine entrypoint (manifest + continuity blockers).

Inference phases (roof, ratification, soft-green) live in `.agents/skills/full-nlc-audit/SKILL.md`.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from nlc_requirements import hub_tool  # noqa: E402

MANIFEST_PATH = ROOT / "integrity" / "full-nlc-audit-manifest.json"
ENFORCEMENT_PATH = ROOT / "docs" / "ADR-ENFORCEMENT.md"
FINDINGS_PATH = ROOT / "FINDINGS.md"
LEAVES_PATH = ROOT / "integrity" / "integration-leaves.json"
LEAVES_WAIVE_PATH = ROOT / "integrity" / "integration-leaves-waive.json"
INFERENCE_CHECKLIST = (
    ROOT / ".agents" / "skills" / "full-nlc-audit" / "references" / "inference-phases.md"
)
RULES_DIR = ROOT / "rules"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def run_command(argv: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, combined


def stage_passed(exit_code: int, output: str, pass_substrings: list[str]) -> bool:
    if pass_substrings:
        return any(s in output for s in pass_substrings)
    return exit_code == 0


def adr_enforcement_continuity() -> list[str]:
    """ADR-ENFORCEMENT **gap** rows must be parked in FINDINGS (gate missing) or docs/backlog."""
    if not ENFORCEMENT_PATH.is_file():
        return ["missing docs/ADR-ENFORCEMENT.md"]
    text = ENFORCEMENT_PATH.read_text(encoding="utf-8", errors="replace")
    findings = (
        FINDINGS_PATH.read_text(encoding="utf-8", errors="replace")
        if FINDINGS_PATH.is_file()
        else ""
    )
    problems: list[str] = []
    for line in text.splitlines():
        if "|" not in line or "**gap**" not in line:
            continue
        m = re.search(r"\|\s*(\d{4})\s*\|", line)
        if not m:
            continue
        adr = m.group(1)
        if "docs/backlog" in line.lower():
            continue
        if adr in findings and ("gate missing" in findings or "Parked" in findings):
            if f"ADR {adr}" in findings or f"adr {adr}" in findings.lower() or adr in findings:
                continue
        if adr in findings:
            continue
        problems.append(
            f"ADR {adr} marked gap in ADR-ENFORCEMENT but not cited in FINDINGS.md Parked/Needed"
        )
    return problems


def rules_gate_orphan() -> list[str]:
    problems: list[str] = []
    if not RULES_DIR.is_dir():
        return problems
    for path in sorted(RULES_DIR.glob("nlc-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{path.name}: invalid JSON ({exc})")
            continue
        for rule in data.get("rules") or []:
            gate = rule.get("gate")
            if not gate or not isinstance(gate, str):
                continue
            if gate.startswith("partial:"):
                continue
            rel = gate.split()[0] if " " in gate else gate
            candidates = [ROOT / rel, ROOT / "tools" / rel, ROOT / "tools" / Path(rel).name]
            if not any(p.is_file() for p in candidates):
                problems.append(f"{path.name} gate missing file: {rel}")
    return problems


def _git_is_ancestor(commit: str, ref: str = "HEAD") -> bool:
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, ref],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def git_worktree_clean(allow_dirty: bool) -> list[str]:
    if allow_dirty:
        return []
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    dirty = (proc.stdout or "").strip()
    if dirty:
        return [
            "git working tree dirty (use --allow-dirty for local runs)",
            *dirty.splitlines()[:8],
        ]
    return []


def integration_leaves() -> list[str]:
    if LEAVES_WAIVE_PATH.is_file():
        try:
            w = json.loads(LEAVES_WAIVE_PATH.read_text(encoding="utf-8"))
            if w.get("waived") and w.get("reason"):
                return []
        except json.JSONDecodeError:
            return ["integration-leaves-waive.json: invalid JSON"]
    if not LEAVES_PATH.is_file():
        return ["missing integration-leaves.json (or integration-leaves-waive.json)"]
    try:
        data = json.loads(LEAVES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"integration-leaves.json: invalid JSON ({exc})"]
    if not (data.get("leaves") or []):
        return ["integration-leaves.json empty and no waive record"]
    problems: list[str] = []
    for leaf in data.get("leaves") or []:
        if not isinstance(leaf, dict):
            problems.append("integration-leaves: leaf must be object")
            continue
        lid = leaf.get("id") or leaf.get("name") or "?"
        disp = (leaf.get("disposition") or "").strip().lower()
        evidence = leaf.get("evidence") or {}
        sha = (evidence.get("commit") or evidence.get("sha") or "").strip()
        if disp == "on_main" and sha:
            if not _git_is_ancestor(sha):
                problems.append(f"leaf {lid}: on_main evidence {sha[:12]} not ancestor of HEAD")
        if disp == "parked":
            ref = (evidence.get("findings_ref") or evidence.get("findings") or "").strip()
            if ref and ref not in FINDINGS_PATH.read_text(encoding="utf-8", errors="replace"):
                problems.append(f"leaf {lid}: parked findings_ref not found in FINDINGS.md")
        if disp not in ("on_main", "parked", "rejected", "absent", ""):
            problems.append(f"leaf {lid}: unknown disposition {disp!r}")
    return problems


_ALLOW_DIRTY = False


BUILTINS = {
    "adr_enforcement_continuity": adr_enforcement_continuity,
    "rules_gate_orphan": rules_gate_orphan,
    "integration_leaves": integration_leaves,
}


def run_builtin(name: str) -> tuple[bool, str]:
    if name == "git_worktree_clean":
        problems = git_worktree_clean(_ALLOW_DIRTY)
    else:
        fn = BUILTINS.get(name)
        if fn is None:
            return False, f"unknown builtin {name!r}"
        problems = fn()
    if problems:
        return False, "\n".join(problems)
    return True, "builtin:MET"


def run_stage(stage_id: str, spec: dict) -> tuple[bool, str]:
    label = spec.get("label") or stage_id
    if spec.get("builtin"):
        ok, detail = run_builtin(str(spec["builtin"]))
        return ok, f"[{stage_id}] {label}\n{detail}"

    cmd = spec.get("command")
    if not cmd or not isinstance(cmd, list):
        return False, f"[{stage_id}] missing command"
    argv = [str(c) for c in cmd]
    if argv[0] == "python3":
        argv[0] = sys.executable
    exit_code, output = run_command(argv, ROOT)
    pass_subs = list(spec.get("pass_substrings") or [])
    ok = stage_passed(exit_code, output, pass_subs)
    tail = output.strip().splitlines()[-8:] if output.strip() else [f"exit {exit_code}"]
    detail = "\n".join(tail)
    return ok, f"[{stage_id}] {label}\n{detail}"


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(description="Full NLC audit (machine manifest)")
    parser.add_argument("--check", action="store_true", help="Run audit; exit 1 on NOT_MET")
    parser.add_argument(
        "--profile",
        choices=["quick", "full", "release-prep"],
        default="quick",
        help="Stage set (full adds verify-deep + verify; release-prep for ./release 0c)",
    )
    parser.add_argument("--list-stages", action="store_true", help="Print profile stage ids")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Skip git_worktree_clean builtin (full profile)",
    )
    parser.add_argument(
        "--emit-inference-checklist",
        action="store_true",
        help="Print inference checklist path and exit 0",
    )
    args = parser.parse_args()

    global _ALLOW_DIRTY
    _ALLOW_DIRTY = bool(args.allow_dirty)

    if args.emit_inference_checklist:
        if not INFERENCE_CHECKLIST.is_file():
            print("FULL_NLC_AUDIT:NOT_MET", file=sys.stderr)
            print(f"  missing {INFERENCE_CHECKLIST}", file=sys.stderr)
            return 1
        print(f"INFERENCE_CHECKLIST:{INFERENCE_CHECKLIST.relative_to(ROOT)}")
        print(INFERENCE_CHECKLIST.read_text(encoding="utf-8"))
        return 0

    if not MANIFEST_PATH.is_file():
        print("FULL_NLC_AUDIT:NOT_MET", file=sys.stderr)
        print(f"  missing {MANIFEST_PATH.relative_to(ROOT)}", file=sys.stderr)
        return 1

    manifest = load_manifest()
    profiles = manifest.get("profiles") or {}
    stages = manifest.get("stages") or {}
    stage_ids = profiles.get(args.profile) or []

    if args.list_stages:
        print(f"FULL_NLC_AUDIT: list-stages profile={args.profile}")
        for sid in stage_ids:
            print(sid)
        return 0

    if not args.check:
        parser.print_help()
        return 2

    print(f"FULL_NLC_AUDIT: profile={args.profile} stages={len(stage_ids)}")
    failures: list[str] = []

    for sid in stage_ids:
        spec = stages.get(sid)
        if not spec:
            failures.append(f"unknown stage id in profile: {sid}")
            continue
        blocking = bool(spec.get("blocking", True))
        ok, detail = run_stage(sid, spec)
        status = "PASS" if ok else "FAIL"
        print(f"--- stage {sid} {status} ---")
        print(detail)
        if not ok and blocking:
            failures.append(sid)

    if failures:
        print("FULL_NLC_AUDIT:NOT_MET", file=sys.stderr)
        print(f"  failed stages: {', '.join(failures)}", file=sys.stderr)
        print(
            "  inference: run skill `.agents/skills/full-nlc-audit/SKILL.md` after machine PASS",
            file=sys.stderr,
        )
        return 1

    print("FULL_NLC_AUDIT:MET")
    print(
        "next: agent skill full-nlc-audit (inference phases) — audit-only unless user asked to fix"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
