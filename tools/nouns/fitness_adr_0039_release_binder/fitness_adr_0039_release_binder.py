#!/usr/bin/env python3
"""ADR 0039/0040: release tag gate + resume wired in script and CI."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _has_fetch_depth_zero(yaml_text: str) -> bool:
    return "fetch-depth: 0" in yaml_text or "fetch-depth:0" in yaml_text.replace(" ", "")


def _runs_hub_fitness_suite(yaml_text: str) -> bool:
    return "ci_fitness.py" in yaml_text or "ci-fitness.sh" in yaml_text


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    script = ROOT / "scripts" / "nlc-release.sh"
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    fitness_wf = ROOT / ".github" / "workflows" / "fitness.yml"
    for path, label in (
        (ROOT / "tools" / "nlc_release_tag_gate.py", "tag gate"),
        (ROOT / "tools" / "nlc_release_resume.py", "resume"),
        (ROOT / "tools" / "nlc_release_record.py", "release record"),
        (ROOT / "tools" / "nlc_release_shipped_tag_audit.py", "shipped tag audit"),
        (ROOT / "integrity/schemas/hub-release-record.schema.json", "record schema"),
        (script, "nlc-release.sh"),
        (workflow, "release.yml"),
    ):
        if not path.is_file():
            violations.append(f"missing {label}")

    text = script.read_text(encoding="utf-8") if script.is_file() else ""
    if "nlc_release_tag_gate.py" not in text:
        violations.append("nlc-release.sh must invoke nlc_release_tag_gate.py")
    if "nlc_release_record.py" not in text:
        violations.append("nlc-release.sh must write hub-release-record via nlc_release_record.py")
    if "nlc_release_resume.py" not in text:
        violations.append("nlc-release.sh must use nlc_release_resume.py")
    if "nlc_release_shipped_tag_audit.py" not in text:
        violations.append("nlc-release.sh must run nlc_release_shipped_tag_audit.py (ADR 0040)")
    if "full-nlc-audit.py" not in text or "--profile release-prep" not in text:
        violations.append(
            "nlc-release.sh must run full-nlc-audit.py --profile release-prep on prepare (ADR 0038)"
        )
    if "release_fail" not in text:
        violations.append("nlc-release.sh must use release_fail for NOT_MET remediation")
    if "apply_release_infer" not in text or "nlc_release_infer.py" not in text:
        violations.append("nlc-release.sh must use nlc_release_infer.py / apply_release_infer (zero-parameter)")
    if "normalize_main_trunk_for_release" not in text:
        violations.append("nlc-release.sh must auto-normalize impure main (zero-parameter ADR 0044)")
    if (ROOT / "tools" / "nlc_release_infer.py").is_file() is False:
        violations.append("missing nlc_release_infer.py")
    if (ROOT / "tools" / "nlc_release_main_purity.py").is_file() is False:
        violations.append("missing nlc_release_main_purity.py (ADR 0044)")
    remediator = (ROOT / "tools" / "nlc_release_remediate.py").read_text(encoding="utf-8")
    if "./release --bump" in remediator:
        violations.append("nlc_release_remediate.py default Re-run must be ./release only (no --bump)")
    forbidden_quiz = (
        "Continue tagging",
        "Choice [p/m/M/k]",
        "Press Enter when merged",
    )
    for phrase in forbidden_quiz:
        if phrase in text:
            violations.append(f"nlc-release.sh must not contain interactive quiz: {phrase!r}")

    import subprocess

    for landmine in (
        "assert-release-resume-invariant-passes.py",
        "assert-release-infer-passes.py",
    ):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / landmine)],
            cwd=str(ROOT),
            check=False,
        )
        if proc.returncode != 0:
            violations.append(f"{landmine} must MET")

    wf = workflow.read_text(encoding="utf-8") if workflow.is_file() else ""
    if "nlc_release_tag_gate.py" not in wf:
        violations.append("release.yml must run tag gate")

    landmine = ROOT / "tools" / "nouns" / "assert_release_tag_gate_fails" / "assert_release_tag_gate_fails.py"
    if landmine.is_file() and "BAD_COMMIT" in landmine.read_text(encoding="utf-8"):
        for wf_path, wf_label in ((fitness_wf, "fitness.yml"), (workflow, "release.yml")):
            wf_text = wf_path.read_text(encoding="utf-8") if wf_path.is_file() else ""
            if _runs_hub_fitness_suite(wf_text) and not _has_fetch_depth_zero(wf_text):
                violations.append(
                    f"{wf_label} must use actions/checkout fetch-depth: 0 "
                    "(hub fitness landmines pin historic commits; shallow CI false-fails)"
                )

    release_md = (ROOT / "docs/adoption/RELEASE.md").read_text(encoding="utf-8", errors="replace")
    if "0044" not in release_md and "production trunk" not in release_md.lower():
        violations.append("RELEASE.md must document production trunk (ADR 0044)")
    hero = release_md.split("## Your workflow", 1)[-1].split("##", 1)[0] if "## Your workflow" in release_md else ""
    if hero and "--bump" in hero:
        violations.append("RELEASE.md seven-step hero must not require --bump flags")
    if "prepare" in release_md and "./release finish" in release_md:
        if "deprecated" not in release_md.lower() and "one command" not in release_md.lower():
            if "/release" not in release_md and "one entrypoint" not in release_md.lower():
                violations.append("RELEASE.md should document single ./release entry (ADR 0039)")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


if __name__ == "__main__":
    sys.exit(main())





BOUNDARY = "bba-emit"

