#!/usr/bin/env python3
"""Human command surface for Natural Language Coding (ADR 0017)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from nlc_distribution import default_install_root, hub_active_path, read_hub_version  # noqa: E402
from nlc_cli_help import (  # noqa: E402
    help_new,
    help_pack,
    help_pack_export,
    help_pack_install,
    help_regen_plan,
)
from nlc_dashboard import format_dashboard, refresh_work_queue  # noqa: E402
from nlc_human_gap import emit_gap  # noqa: E402
from nlc_menu_data import INSTALL_CMD  # noqa: E402
from nlc_preflight import preflight_issues  # noqa: E402
from nlc_requirements import hub_tool  # noqa: E402
from nlc_requirements_cmd import run_requirements  # noqa: E402
from nlc_guide_cmd import dispatch_guide  # noqa: E402
from nlc_regen_continue import regen_advance, regen_continue  # noqa: E402
from nlc_verify import emit_verify_fail, verify_deep, verify_fast  # noqa: E402


def hub_root() -> Path:
    if os.environ.get("NLC_HUB"):
        return Path(os.environ["NLC_HUB"]).resolve()
    active = hub_active_path(default_install_root())
    if (active / "tools" / "nlc.py").is_file():
        return active
    return ROOT


def project_root(arg: Path | None) -> Path:
    return (arg or Path.cwd()).resolve()


def _human_status(root: Path, hub: Path) -> tuple[str, int]:
    issues = preflight_issues(hub, root)
    if issues:
        lines = [
            "Natural Language Coding",
            "=======================",
            "",
            "Cannot continue yet.",
            "",
        ]
        for i, iss in enumerate(issues, start=1):
            lines.append(f"{i}. {iss['problem']}")
            lines.append(f"   Fix: {iss['fix']}")
        lines.append("")
        return "\n".join(lines), 1
    try:
        hub_ver = read_hub_version(hub)
    except (OSError, json.JSONDecodeError, KeyError, ValueError):
        hub_ver = "unknown"
    queue = refresh_work_queue(root, hub_ver)
    return format_dashboard(root, queue, hub_ver), 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    hub = hub_root()
    text, code = _human_status(root, hub)
    print(text)
    return code


def print_menu(root: Path) -> int:
    hub = hub_root()
    text, code = _human_status(root, hub)
    print(text)
    return code


def run_tool(script: str, argv: list[str], *, cwd: Path | None = None) -> int:
    hub = hub_root()
    path = hub / "tools" / script
    if not path.is_file():
        path = ROOT / "tools" / script
    proc = subprocess.run([sys.executable, str(path), *argv], cwd=str(cwd) if cwd else None)
    return proc.returncode


def cmd_doctor_fix(_: argparse.Namespace) -> int:
    hub = hub_root()
    script = hub / "scripts" / "install.sh"
    if script.is_file():
        print("Re-running install to repair hub and agent skills…")
        return subprocess.run(["bash", str(script)], cwd=str(hub)).returncode
    print("Install script not found.")
    print(f"  Fix: {INSTALL_CMD}")
    return 1


def cmd_doctor(args: argparse.Namespace) -> int:
    if getattr(args, "doctor_cmd", None) == "fix":
        return cmd_doctor_fix(args)
    root = project_root(args.project)
    hub = hub_root()
    issues = preflight_issues(hub, root)
    if issues:
        print("Install check failed.")
        for iss in issues:
            print(f"  {iss['problem']}")
            print(f"  Fix: {iss['fix']}")
        return 1
    ver = read_hub_version(hub)
    print("Install check passed.")
    print(f"  Compiler {ver} at {hub}")
    return 0


def cmd_requirements(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    hub = hub_root()
    issues = preflight_issues(hub, root)
    if issues:
        print(issues[0]["problem"], file=sys.stderr)
        print(f"  Fix: {issues[0]['fix']}", file=sys.stderr)
        return 1
    refresh_work_queue(root, read_hub_version(hub))
    return run_requirements(root, hub)


def cmd_new(args: argparse.Namespace) -> int:
    if args.path is None:
        return help_new()
    return run_tool(
        "nlc-init.py",
        [str(args.path), "--name", args.name] + (["--force"] if args.force else []),
    )


def cmd_verify(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    ok, reasons = verify_fast(root)
    if ok:
        print("Verify passed.")
        return 0
    emit_verify_fail(reasons)
    return 1


def cmd_verify_deep(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    hub = hub_root()
    try:
        hub_ver = read_hub_version(hub)
    except (OSError, json.JSONDecodeError, KeyError, ValueError):
        hub_ver = "unknown"
    return verify_deep(root, hub, hub_ver)


def cmd_prove_removed(_: argparse.Namespace) -> int:
    return emit_gap(
        "The prove command was removed.",
        ask="Use verify for CI and verify-deep after material changes.",
        examples=["./nlc verify", "./nlc verify-deep"],
        machine=None,
    )


def cmd_ship_check(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    return run_tool("release-audit.py", [str(root)])


def cmd_upgrade(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    return run_tool("nlc-update.py", ["--project", str(root)])


def cmd_check_rules(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    adopted = root / "rules" / "adopted.json"
    if not adopted.is_file():
        return emit_gap(
            "No adopted rules file yet.",
            ask="Use /interview to add requirements first.",
            examples=["./nlc maintainer check-rules  (after rules/adopted.json exists)"],
        )
    return run_tool("check-rule-adoption.py", [str(adopted)])


def cmd_rule_coverage(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = [str(root)]
    if args.adr:
        argv.extend(["--adr", args.adr])
    if args.tag:
        argv.extend(["--tag", args.tag])
    if args.check:
        argv.append("--check")
    if args.json:
        argv.append("--json")
    return run_tool("nlc_rule_coverage.py", argv)


def cmd_rule_marker(args: argparse.Namespace) -> int:
    argv = ["--id", args.rule_id, "--lang", args.lang]
    return run_tool("nlc_rule_marker.py", argv)


def cmd_goal_scaffold(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = ["--root", str(root), "--goal", args.goal]
    if args.force:
        argv.append("--force")
    return run_tool("nlc_goal_scaffold.py", argv)


def cmd_rule_emit(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = ["--root", str(root), "--goal", args.goal]
    if args.dry_run:
        argv.append("--dry-run")
    return run_tool("nlc_rule_emit.py", argv)


def cmd_regen_plan(args: argparse.Namespace) -> int:
    if not args.change:
        return help_regen_plan()
    root = project_root(args.project)
    argv = [str(root), "--change", args.change]
    if args.orchestrate:
        argv.append("--orchestrate")
    if args.write_queue:
        argv.append("--write-queue")
    return run_tool("nlc-delta-regen.py", argv)


def cmd_guide(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    hub = hub_root()
    return dispatch_guide(args, root, hub)


def cmd_regen_continue(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    return regen_continue(root)


def cmd_regen_advance(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    return regen_advance(root)


def cmd_plan_audit(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    from nlc_plan_audit import install_audit

    src = args.src.resolve()
    if not src.is_file():
        print("Plan audit source file not found.", file=sys.stderr)
        return 2
    try:
        import json

        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Plan audit source is not valid JSON.", file=sys.stderr)
        return 2
    ok, msg = install_audit(root, data)
    if not ok:
        print(f"Plan audit invalid: {msg}", file=sys.stderr)
        return 1
    print(f"plan-audit:MET {msg}")
    return 0


def cmd_gate_record(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    from nlc_gate_record import append_record

    append_record(
        root,
        artifact=args.artifact,
        gate_id=args.gate_id,
        outcome=args.outcome,
        command=args.command or None,
    )
    print(f"gate-record: MET artifact={args.artifact}")
    return 0


def cmd_gate_scope(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    from nlc_gate_scope import add_scope_path, load_scope_paths

    if args.list_scope:
        for rel in load_scope_paths(root):
            print(rel)
        return 0
    if not args.artifact:
        print("gate-scope needs --add <path> or --list", file=sys.stderr)
        return 2
    add_scope_path(root, args.artifact)
    print(f"gate-scope: MET artifact={args.artifact}")
    return 0


def cmd_contract_break_accept(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    from nlc_contract_break_accept import append_acceptance

    append_acceptance(
        root,
        schema_path=args.schema,
        adr_id=args.adr,
        accepted_by=args.accepted_by,
        requirement_id=args.requirement,
    )
    print(f"contract-break-accept: MET schema={args.schema}")
    return 0


def cmd_adopt_existing(args: argparse.Namespace) -> int:
    root = project_root(args.path)
    code = run_tool("nlc-brownfield-inventory.py", [str(root)])
    print("\nNext:")
    print("  ./nlc maintainer goal-scaffold --goal <id>   # ADR 0023 rule markers")
    print("  ./nlc maintainer rule-emit --goal <id>       # ADR 0023 compiler-owned markers")
    print("  docs/nlc/RULE-TRACE.md")
    print("  /interview in your agent")
    return code


def cmd_pack_export(args: argparse.Namespace) -> int:
    if not args.name or not args.version:
        return help_pack_export()
    root = project_root(args.project)
    argv = ["--name", args.name, "--version", args.version, "--root", str(root)]
    if args.description:
        argv.extend(["--description", args.description])
    return run_tool("nlc-pack-export.py", argv)


def cmd_pack_install(args: argparse.Namespace) -> int:
    if args.archive is None:
        return help_pack_install()
    root = project_root(args.project)
    argv = [str(args.archive), "--root", str(root)]
    if args.force:
        argv.append("--force")
    return run_tool("nlc-pack-install.py", argv)


def cmd_pack_ingest(args: argparse.Namespace) -> int:
    argv: list[str] = []
    if args.source is not None:
        argv.append(str(args.source))
    return run_tool("nlc-pack-ingest.py", argv)


def cmd_brownfield_migrate(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = [str(root)]
    if args.write_plan:
        argv.append("--write-plan")
    if getattr(args, "apply", False):
        argv.append("--apply")
    return run_tool("nlc-brownfield-migrate.py", argv)


def cmd_rule_runner(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = ["--root", str(root)]
    if args.materialize:
        argv.append("--materialize")
    if args.check:
        argv.append("--check")
    return run_tool("nlc_rule_runner.py", argv)


def cmd_call_tree(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = ["--root", str(root)]
    if args.sync:
        argv.append("--sync")
    if args.check:
        argv.append("--check")
    return run_tool("nlc_call_tree.py", argv)


def cmd_primitive_propose(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    argv = ["--name", args.name, "--root", str(root)]
    return run_tool("nlc_primitive_propose.py", argv)


def cmd_language_scan(args: argparse.Namespace) -> int:
    root = project_root(args.project)
    return run_tool("nlc_language_scan.py", [str(root)])


def main() -> int:
    hub_tool()
    parser = argparse.ArgumentParser(
        prog="nlc",
        description="Natural Language Coding — human menu and commands (ADR 0017)",
    )
    parser.add_argument("--project", type=Path, default=None, help="App repo root")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("dashboard", help="Dashboard (default)").set_defaults(func=cmd_dashboard)
    sub.add_parser("menu", help="Show menu and queue").set_defaults(
        func=lambda a: print_menu(project_root(a.project))
    )
    p_doc = sub.add_parser("doctor", help="Check install")
    doc_sub = p_doc.add_subparsers(dest="doctor_cmd")
    doc_sub.add_parser("fix", help="Re-run install to repair hub and skills")
    p_doc.set_defaults(func=cmd_doctor)

    p_new = sub.add_parser("new", help="Start a new empty app repo")
    p_new.add_argument("path", type=Path, nargs="?", default=None)
    p_new.add_argument("--name", default="MyApp")
    p_new.add_argument("--force", action="store_true")
    p_new.set_defaults(func=cmd_new)

    sub.add_parser("verify", help="Fast verify (fingerprints; CI-friendly)").set_defaults(
        func=cmd_verify
    )
    sub.add_parser(
        "verify-deep",
        help="Full gates + refresh .nlc/verified.json",
    ).set_defaults(func=cmd_verify_deep)

    sub.add_parser("prove", help=argparse.SUPPRESS).set_defaults(func=cmd_prove_removed)

    p_ship = sub.add_parser("ship-check", help="Promotion or release bundle check")
    p_ship.set_defaults(func=cmd_ship_check)

    p_up = sub.add_parser("upgrade", help="Upgrade compiler for this app lock")
    p_up.set_defaults(func=cmd_upgrade)

    p_bf = sub.add_parser("adopt-existing", help="Beta: existing codebase inventory")
    p_bf.add_argument("path", type=Path, nargs="?", default=".")
    p_bf.set_defaults(func=cmd_adopt_existing)

    pack = sub.add_parser("pack", help="Requirement packs")
    pack_sub = pack.add_subparsers(dest="pack_cmd")
    p_ex = pack_sub.add_parser("export", help="Export ratified pack")
    p_ex.add_argument("--name", default=None)
    p_ex.add_argument("--version", default=None)
    p_ex.add_argument("--description", default="")
    p_ex.set_defaults(func=cmd_pack_export)
    p_in = pack_sub.add_parser("install", help="Install pack tarball")
    p_in.add_argument("archive", type=Path, nargs="?", default=None)
    p_in.add_argument("--force", action="store_true")
    p_in.set_defaults(func=cmd_pack_install)
    p_ing = pack_sub.add_parser("ingest", help="Ingest source docs into pack (v0.2 stub)")
    p_ing.add_argument("source", type=Path, nargs="?", default=None)
    p_ing.set_defaults(func=cmd_pack_ingest)

    maint = sub.add_parser(
        "maintainer",
        help="Agent/CI tools (see tools/README.md)",
    )
    msub = maint.add_subparsers(dest="maintainer_cmd", required=True)
    msub.add_parser(
        "requirements",
        help="Sync rules after ratification (agents)",
    ).set_defaults(func=cmd_requirements)
    msub.add_parser("check-rules", help="Rule adoption conflicts").set_defaults(
        func=cmd_check_rules
    )
    p_rc = msub.add_parser(
        "rule-coverage",
        help="ADR 0023: list nlc:rule=<id> sites; --check fails if adopted rules lack markers",
    )
    p_rc.add_argument("--adr", default=None, help="e.g. 0007 or 0012..0018")
    p_rc.add_argument("--tag", default=None)
    p_rc.add_argument("--check", action="store_true")
    p_rc.add_argument("--json", action="store_true")
    p_rc.set_defaults(func=cmd_rule_coverage)
    p_rm = msub.add_parser(
        "rule-marker",
        help="ADR 0023: print nlc:rule= receipt line for generate",
    )
    p_rm.add_argument("--id", dest="rule_id", required=True)
    p_rm.add_argument("--lang", default="python")
    p_rm.set_defaults(func=cmd_rule_marker)
    p_gsf = msub.add_parser(
        "goal-scaffold",
        help="ADR 0023: scaffold goals/<id>/implementation.py with rule markers",
    )
    p_gsf.add_argument("--goal", required=True)
    p_gsf.add_argument("--force", action="store_true")
    p_gsf.set_defaults(func=cmd_goal_scaffold)
    p_re = msub.add_parser(
        "rule-emit",
        help="ADR 0023: apply compiler-owned nlc:rule= markers after generate",
    )
    p_re.add_argument("--goal", required=True)
    p_re.add_argument("--dry-run", action="store_true")
    p_re.set_defaults(func=cmd_rule_emit)
    msub.add_parser(
        "language-scan",
        help="UC16 v0: list languages under domain/ and goals/",
    ).set_defaults(func=cmd_language_scan)
    p_bm = msub.add_parser(
        "brownfield-migrate",
        help="UC15: brownfield migrate plan after inventory",
    )
    p_bm.add_argument("--write-plan", action="store_true")
    p_bm.add_argument("--apply", action="store_true")
    p_bm.set_defaults(func=cmd_brownfield_migrate)
    p_rr = msub.add_parser(
        "rule-runner",
        help="UC4/UC5: materialize/check rule IR snapshot",
    )
    p_rr.add_argument("--materialize", action="store_true")
    p_rr.add_argument("--check", action="store_true")
    p_rr.set_defaults(func=cmd_rule_runner)
    p_ct = msub.add_parser(
        "call-tree",
        help="UC20: sync/check verb primitive inventory (Python v1)",
    )
    p_ct.add_argument("--sync", action="store_true")
    p_ct.add_argument("--check", action="store_true")
    p_ct.set_defaults(func=cmd_call_tree)
    p_pp = msub.add_parser(
        "primitive-propose",
        help="UC12: draft ADR before expanding primitives.md",
    )
    p_pp.add_argument("--name", required=True)
    p_pp.set_defaults(func=cmd_primitive_propose)
    p_regen = msub.add_parser("regen-plan", help="Delta regen plan")
    p_regen.add_argument("--change", default=None, help="kind:id e.g. verb:Invoice.pay")
    p_regen.add_argument("--orchestrate", action="store_true")
    p_regen.add_argument("--write-queue", action="store_true")
    p_regen.set_defaults(func=cmd_regen_plan)

    p_guide = msub.add_parser("guide", help="Interview/planit durable state under .nlc/")
    gsub = p_guide.add_subparsers(dest="guide_cmd", required=True)
    p_ps = gsub.add_parser("planit-start", help="Mark build session active")
    p_ps.add_argument("--label", default=None)
    p_ps.set_defaults(func=cmd_guide)
    gsub.add_parser("planit-end", help="Clear build session").set_defaults(func=cmd_guide)
    p_pc = gsub.add_parser("policy-change", help="Record kind:id after policy edit")
    p_pc.add_argument("--change", default=None)
    p_pc.set_defaults(func=cmd_guide)
    gsub.add_parser("requirements-dirty", help="Flag requirements sync pending").set_defaults(
        func=cmd_guide
    )
    gsub.add_parser("handoff-build", help="Queue build stage after ratification").set_defaults(
        func=cmd_guide
    )
    p_bg = gsub.add_parser(
        "before-generate",
        help="UC18 knowledge gate + stamp (run before PLANIT generate)",
    )
    p_bg.add_argument("--scope", action="append", default=None)
    p_bg.set_defaults(func=cmd_guide)

    msub.add_parser(
        "regen-continue",
        help="UC9: next delta-regen goal (/planit then regen-advance)",
    ).set_defaults(func=cmd_regen_continue)
    msub.add_parser(
        "regen-advance",
        help="UC9: advance after one regen goal completes",
    ).set_defaults(func=cmd_regen_advance)

    p_gs = msub.add_parser(
        "gate-scope",
        help="ADR 0010: declare a Planit-generated artifact path (skills, docs, code)",
    )
    p_gs.add_argument("--add", dest="artifact", default=None)
    p_gs.add_argument("--list", dest="list_scope", action="store_true")
    p_gs.set_defaults(func=cmd_gate_scope)

    p_gr = msub.add_parser("gate-record", help="ADR 0010: record PLANIT 6.5 PASS for an artifact")
    p_gr.add_argument("--artifact", required=True)
    p_gr.add_argument("--gate-id", required=True)
    p_gr.add_argument("--outcome", default="PASS")
    p_gr.add_argument("--command", default="")
    p_gr.set_defaults(func=cmd_gate_record)

    p_cba = msub.add_parser(
        "contract-break-accept",
        help="ADR 0006: record manager acceptance for breaking published contract",
    )
    p_cba.add_argument("--schema", required=True)
    p_cba.add_argument("--adr", required=True)
    p_cba.add_argument("--requirement", default=None)
    p_cba.add_argument("--accepted-by", required=True)
    p_cba.set_defaults(func=cmd_contract_break_accept)

    p_pa = msub.add_parser("plan-audit", help="Install bbp-reviewer plan audit JSON")
    p_pa.add_argument("--from", dest="src", type=Path, required=True)
    p_pa.set_defaults(func=cmd_plan_audit)

    args = parser.parse_args()
    if args.command is None:
        return cmd_dashboard(args)
    if args.command == "pack" and not args.pack_cmd:
        return help_pack()
    if args.command == "pack" and args.pack_cmd == "export":
        if not args.name or not args.version:
            return help_pack_export()
    if args.command == "pack" and args.pack_cmd == "install":
        if args.archive is None:
            return help_pack_install()
    if args.command == "maintainer" and args.maintainer_cmd == "regen-plan":
        if not args.change:
            return help_regen_plan()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
