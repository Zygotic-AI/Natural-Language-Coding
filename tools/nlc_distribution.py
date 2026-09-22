BOUNDARY = "bba-emit"
"""NLC distribution: semver, store layout, migrations (ADR 0014, 0015)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_REPO = "Zygotic-AI/Natural-Language-Coding"
DEFAULT_RAW = f"https://raw.githubusercontent.com/{DEFAULT_REPO}/main"
SEMVER_RE = re.compile(r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")

LOCK_SCHEMA = 1
