#!/usr/bin/env python3
"""Validate agent noun packages for BBP completeness.

Checks that each agent noun package under agents/<name>/ has:
  - AGENT.md with identity, adjectives, handoff-in, completion artifact, success criteria
  - verbs.md where every verb declares input contract, output contract, and failure mode

Input: optional argv[1:] = specific agent names; if none, scans all agents/*/ directories.

Output: lines among
  PACKAGE:<name>:VALID|INVALID
  AGENT_MISSING <name>
  VERBS_MISSING <name>
  AGENT_MISSING_SECTION <name> <section>
  VERB_MISSING_INPUT <name> <verb>
  VERB_MISSING_OUTPUT <name> <verb>
  VERB_MISSING_FAILURE <name> <verb>
  RESULT:MET|NOT_MET

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.validate_agent_noun_packages import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
