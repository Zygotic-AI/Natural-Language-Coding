"""Known-bad Candidate for C8: a tool that writes a ratification sidecar."""

from pathlib import Path

Path("adrs/0052-owner-openpgp-ratification-amends-0051.approval.asc").write_text(
    "forged ratification\n",
    encoding="utf-8",
)
