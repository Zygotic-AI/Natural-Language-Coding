#!/usr/bin/env bash
# Pre-release smoke: version store install + greenfield lock (run from hub repo root).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SMOKE_ROOT="${TMPDIR:-/tmp}/nlc-release-smoke-$$"
APP="${SMOKE_ROOT}/my-app"
STORE="${SMOKE_ROOT}/store"

cleanup() {
  rm -rf "${SMOKE_ROOT}"
}
trap cleanup EXIT

python3 "${ROOT}/tools/nlc-fetch-hub.py" --install-root "${STORE}" --from-path "${ROOT}"
test -f "${STORE}/hub/tools/nlc-update.py"
test "$(tr -d '\n' < "${STORE}/current")" = "0.1.0"

export NLC_HUB="${STORE}/hub"
python3 "${STORE}/hub/tools/nlc-init.py" "${APP}" --name SmokeApp
test -f "${APP}/.nlc/lock.json"
python3 -c "
import json, sys
lock = json.load(open('${APP}/.nlc/lock.json'))
assert lock.get('hub') == '0.1.0', lock
assert lock.get('schema') == 1
"

python3 "${STORE}/hub/tools/nlc-install-verify.py" "${STORE}/hub"

echo "RELEASE_SMOKE:MET"
