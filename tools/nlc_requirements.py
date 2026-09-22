BOUNDARY = "bba-emit"
"""Requirements preflight (ADR 0013). Import or run: python tools/nlc_requirements.py <profile>."""

from __future__ import annotations

import shutil
import sys
from typing import Callable

MIN_PYTHON = (3, 9)
