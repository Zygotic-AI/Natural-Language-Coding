#!/usr/bin/env python3
"""Hub release semver: suggest bump from diff heuristics, apply version + migration unit."""
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nlc_requirements import hub_tool  # noqa: E402
from nouns.release_bump import *  # noqa: F403
__all__ = ['MAJOR_HINTS', 'MINOR_PATH_PREFIXES', 'MINOR_TEXT_HINTS', 'POLICY_PATH_PREFIXES', 'ROOT', 'VERSION_PATH', '_git_lines', '_is_policy_path', 'apply_bump', 'bump_semver', 'changed_paths', 'diff_blob', 'main', 'policy_diff_blob', 'read_version', 'suggest_bump', 'write_version']

if __name__ == "__main__":
    hub_tool()
    raise SystemExit(main())

