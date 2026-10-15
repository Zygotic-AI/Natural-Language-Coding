"""Single runner for releasable gate profiles (RCA-1 containment)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BOUNDARY = "bba-emit"

ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = ROOT / "integrity" / "releasable-gates.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def tree_label(tree: Path) -> str:
    try:
        return str(tree.resolve().relative_to(ROOT))
    except ValueError:
        return str(tree.resolve())


def emit_gate_failure(gate_id: str, reproduce: str, tree: Path) -> None:
    """Print deterministic failure (RCA-1 C2): gate name + reproduce command."""
    print(f"FAILED {gate_id} on tree {tree_label(tree)}", file=sys.stderr)
    print(f"Reproduce: {reproduce}", file=sys.stderr)


def format_reproduce(template: str, tree: Path) -> str:
    return template.replace("{tree}", tree_label(tree))


def run_argv(argv: list[str], tree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        argv,
        cwd=str(tree),
        capture_output=True,
        text=True,
        check=False,
    )
    combined = (proc.stdout or "") + (proc.stderr or "")
    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.stderr:
        print(proc.stderr, end="" if proc.stderr.endswith("\n") else "\n", file=sys.stderr)
    return proc.returncode, combined


def gate_passed(combined: str, gate: dict) -> bool:
    for needle in gate.get("pass_substrings") or []:
        if needle in combined:
            return True
    return False


def run_builtin(gate_id: str, gate: dict, tree: Path) -> tuple[bool, list[str]]:
    name = gate.get("builtin")
    if name == "pipeline_blockers":
        sys.path.insert(0, str(ROOT / "tools"))
        from nouns.verify.verify import pipeline_blockers

        reasons = pipeline_blockers(tree)
        if reasons:
            reproduce = format_reproduce(gate.get("reproduce") or "./nlc verify --project {tree}", tree)
            emit_gate_failure(gate_id, reproduce, tree)
            for r in reasons[:12]:
                print(f"  {r}", file=sys.stderr)
            return False, reasons
        return True, []
    return False, [f"unknown builtin {name!r}"]


def run_gate(gate_id: str, tree: Path, *, manifest: dict | None = None) -> bool:
    data = manifest or load_manifest()
    gate = (data.get("gates") or {}).get(gate_id)
    if not gate:
        print(f"GATE:REFUSE unknown gate {gate_id}", file=sys.stderr)
        return False
    scope = gate.get("scope") or "all"
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_pipeline import is_hub_repo

    if scope == "hub" and not is_hub_repo(tree):
        print(f"GATE:MET {gate_id} skip (hub-only, not hub tree)")
        return True
    if gate.get("builtin"):
        ok, _ = run_builtin(gate_id, gate, tree)
        return ok
    if gate.get("suite") == "hub_ci_fitness":
        from nouns.ci_fitness.ci_fitness import run_ci_fitness_suite

        code = run_ci_fitness_suite()
        if code != 0:
            reproduce = format_reproduce(
                gate.get("reproduce") or "./nlc gate hub-ci-fitness --tree {tree}",
                tree,
            )
            emit_gate_failure(gate_id, reproduce, tree)
        return code == 0
    argv = [str(x).replace("{tree}", tree_label(tree)) for x in (gate.get("argv") or [])]
    if argv and argv[0] == "python3":
        argv[0] = sys.executable
    code, combined = run_argv(argv, tree)
    if code != 0 or not gate_passed(combined, gate):
        reproduce = format_reproduce(
            gate.get("reproduce") or " ".join(gate.get("argv") or []),
            tree,
        )
        emit_gate_failure(gate_id, reproduce, tree)
        return False
    return True


def run_profile(profile: str, tree: Path, *, fail_fast: bool = False) -> int:
    data = load_manifest()
    ids = (data.get("profiles") or {}).get(profile) or []
    if not ids:
        print(f"GATE:REFUSE unknown profile {profile}", file=sys.stderr)
        return 2
    failed = False
    for gate_id in ids:
        ok = run_gate(gate_id, tree, manifest=data)
        if not ok:
            failed = True
            if fail_fast:
                return 1
    return 1 if failed else 0


def verify_subset_of_release() -> list[str]:
    """Return violations if verify profile is not a subset of release gates."""
    data = load_manifest()
    verify_ids = list(data.get("profiles", {}).get("verify") or [])
    release_ids = set(data.get("profiles", {}).get("release") or [])
    violations: list[str] = []
    if not release_ids:
        violations.append("release profile empty")
    if "hub-ci-fitness" not in release_ids:
        violations.append("release profile must include hub-ci-fitness")
    for gid in verify_ids:
        if gid not in (data.get("gates") or {}):
            violations.append(f"verify gate {gid} missing from gates map")
        elif gid not in release_ids:
            violations.append(f"verify gate {gid} must appear in release profile")
    return violations


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run releasable gate profile")
    parser.add_argument("gate_id", nargs="?", help="Single gate id (or use --profile)")
    parser.add_argument("--profile", choices=("verify", "release"))
    parser.add_argument("--tree", default=".", help="Tree under test (default cwd)")
    parser.add_argument("--check-ssot", action="store_true", help="Validate manifest subset rules")
    args = parser.parse_args()
    if args.check_ssot:
        v = verify_subset_of_release()
        v.extend(_release_prep_sync_violations())
        for item in v:
            print(f"VIOLATION {item}")
        print("RESULT:NOT_MET" if v else "RESULT:MET")
        return 1 if v else 0
    tree = Path(args.tree).resolve()
    if args.profile:
        return run_profile(args.profile, tree)
    if not args.gate_id:
        parser.print_help()
        return 2
    return 0 if run_gate(args.gate_id, tree) else 1


def _release_prep_sync_violations() -> list[str]:
    data = load_manifest()
    prep = data.get("release_prep_stages") or []
    audit_path = ROOT / "integrity" / "full-nlc-audit-manifest.json"
    if not audit_path.is_file():
        return ["missing full-nlc-audit-manifest.json"]
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    audit_prep = (audit.get("profiles") or {}).get("release-prep") or []
    if prep != audit_prep:
        return ["release_prep_stages must match full-nlc-audit release-prep profile"]
    return []


if __name__ == "__main__":
    sys.exit(main())
