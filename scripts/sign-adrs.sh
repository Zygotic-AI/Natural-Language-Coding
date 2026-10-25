#!/usr/bin/env bash
# Thin entrypoint. Policy lives in goals/sign_adrs/execute.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec bash "${ROOT}/goals/sign_adrs/execute.sh" "$@"
