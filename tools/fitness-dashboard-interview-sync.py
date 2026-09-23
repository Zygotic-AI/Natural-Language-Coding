#!/usr/bin/env python3
"""ADR 0017/0020: dashboard copy bridges humans to /interview (no gate-first headlines)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "tools" / "nlc_dashboard.py"
DASH_NOUN = ROOT / "tools" / "nouns" / "dashboard" / "dashboard.py"
SPECIMEN = ROOT / "examples" / "invoice-correct"


def main() -> int:
    _ = sys.argv[1:]
    violations: list[str] = []
    if not DASH.is_file():
        violations.append("missing tools/nlc_dashboard.py")
    else:
        parts = [DASH.read_text(encoding="utf-8", errors="replace")]
        if DASH_NOUN.is_file():
            parts.append(DASH_NOUN.read_text(encoding="utf-8", errors="replace"))
        text = "\n".join(parts)
        if "/interview" not in text:
            violations.append("nlc_dashboard.py must reference /interview agent bridge")
        if "YOUR QUEUE" not in text:
            violations.append("format_dashboard must label YOUR QUEUE")
        if re_gate_token_head(text):
            violations.append("nlc_dashboard.py must not lead humans with *:NOT_MET tokens")

    if SPECIMEN.is_dir():
        sys.path.insert(0, str(ROOT / "tools"))
        from nlc_dashboard import format_dashboard, refresh_work_queue

        queue = refresh_work_queue(SPECIMEN, "0.1.0")
        rendered = format_dashboard(SPECIMEN, queue, "0.1.0")
        if "/interview" not in rendered:
            violations.append("rendered dashboard must mention /interview")
        first = next((ln.strip() for ln in rendered.splitlines() if ln.strip()), "")
        if ":NOT_MET" in first:
            violations.append("dashboard first line must not be a NOT_MET gate token")
    else:
        violations.append("missing examples/invoice-correct for dashboard render check")

    for v in violations:
        print(f"VIOLATION {v}")
    if violations:
        print("RESULT:NOT_MET")
        return 1
    print("RESULT:MET")
    return 0


def re_gate_token_head(text: str) -> bool:
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith('"""') or s.startswith("'''"):
            continue
        return s.startswith(("DASHBOARD:", "NLC:", "VERIFY:")) and "NOT_MET" in s
    return False


if __name__ == "__main__":
    sys.exit(main())
