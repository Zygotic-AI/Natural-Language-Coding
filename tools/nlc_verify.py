#!/usr/bin/env python3
from __future__ import annotations

BOUNDARY = "bba-emit"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.verify import *  # noqa: F403
__all__ = ['SKIP_DIR_NAMES', '_load_manifest', '_run_verify_suite', '_sha256_file', 'build_fingerprint_manifest', 'emit_verify_fail', 'fingerprint_mismatches', 'iter_verify_paths', 'pipeline_blockers', 'verified_path', 'verify_deep', 'verify_fast', 'write_verified']

