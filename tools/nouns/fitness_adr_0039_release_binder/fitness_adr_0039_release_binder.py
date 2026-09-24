#!/usr/bin/env python3
"""ADR 0039/0040: release tag gate + resume wired in script and CI."""

from __future__ import annotations



import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    script = ROOT / "scripts" / "nlc-release.sh"
    workflow = ROOT / ".github" / "workflows" / "release.yml"
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

    import subprocess

    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "assert-release-resume-invariant-passes.py")],
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        violations.append("assert-release-resume-invariant-passes.py must MET")

    wf = workflow.read_text(encoding="utf-8") if workflow.is_file() else ""
    if "nlc_release_tag_gate.py" not in wf:
        violations.append("release.yml must run tag gate")

    release_md = (ROOT / "docs/adoption/RELEASE.md").read_text(encoding="utf-8", errors="replace")
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

