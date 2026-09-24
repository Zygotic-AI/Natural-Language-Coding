"""Change set: CONFIRM CHANGED: list, else dirty git, else origin/main...HEAD.

None means tree-wide (no list, no diff). A non-empty set means only those
paths (and their parent units) are in scope.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.changeset import *  # noqa: F403
