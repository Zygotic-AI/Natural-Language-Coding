#!/usr/bin/env bash
# Thin entrypoint. Policy lives in goals/hub_release_smoke/execute.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "${ROOT}/goals/hub_release_smoke/execute.sh" "$@"
