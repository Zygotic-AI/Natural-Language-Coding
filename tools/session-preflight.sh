#!/usr/bin/env bash
# Thin entrypoint. Policy lives in goals/hub_session/execute.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "${ROOT}/goals/hub_session/execute.sh" "$@"
