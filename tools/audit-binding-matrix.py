#!/usr/bin/env python3
"""BBP binding-matrix audits: coverage, unbound list, promote/bindable list."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nouns.audit_binding_matrix import audit_binding_matrix as _impl

globals().update({name: getattr(_impl, name) for name in dir(_impl) if not name.startswith("__")})


if __name__ == "__main__":
    raise SystemExit(main())
