#!/usr/bin/env bash
# Hub CI — delegates to cross-platform ci_fitness.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/tools/ci_fitness.py"
