#!/usr/bin/env python3
"""Hub release notes: draft from last tag, validate Highlights, refresh change log."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_notes import *  # noqa: F403
__all__ = ['HIGHLIGHTS_PLACEHOLDER', 'NOTES_DIR', 'ROOT', '_git', 'build_draft', 'changelog_base_tag', 'check_notes', 'commit_lines', 'diff_stat', 'highlights_body', 'main', 'notes_path', 'refresh_changes_section']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

