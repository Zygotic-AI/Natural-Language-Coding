#!/usr/bin/env bash
# UC18: block goal-tree writes until nlc-before-generate stamp is fresh (planit step 6).
set -euo pipefail
input="$(cat)"

deny_fixed() {
  # No jq/python3 — static JSON only (fail-closed bootstrap).
  case "$1" in
    missing_interpreter)
      echo '{"permission":"deny","user_message":"Goal-write hook cannot run (missing jq and python3).","agent_message":"Install jq or python3 so the goal-write hook can fail closed."}'
      ;;
    empty_input)
      echo '{"permission":"deny","user_message":"Goal-write hook refused empty hook input.","agent_message":"Retry the edit; if this persists, fix hook JSON payload."}'
      ;;
    bad_path)
      echo '{"permission":"deny","user_message":"Goal-write hook could not read the target path.","agent_message":"Malformed hook input; refuse rather than allow goal writes."}'
      ;;
    no_stamp)
      echo '{"permission":"deny","user_message":"Run the knowledge check before editing goals (PLANIT step 6).","agent_message":"Run: ./nlc maintainer guide before-generate --scope default (or your scopes), then edit goals."}'
      ;;
    stale_stamp)
      echo '{"permission":"deny","user_message":"Knowledge check stamp expired — re-run before generate.","agent_message":"Run ./nlc maintainer guide before-generate again, then continue PLANIT step 6."}'
      ;;
  esac
  exit 0
}

allow() {
  echo '{"permission":"allow"}'
  exit 0
}

extract_path() {
  if command -v jq >/dev/null 2>&1; then
    echo "$input" | jq -r '.tool_input.path // .tool_input.file_path // .path // empty' 2>/dev/null || true
    return
  fi
  if command -v python3 >/dev/null 2>&1; then
    INPUT="$input" python3 - <<'PY'
import json, os
raw = os.environ.get("INPUT", "")
try:
    data = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    print("")
    raise SystemExit(0)
ti = data.get("tool_input") or {}
print(ti.get("path") or ti.get("file_path") or data.get("path") or "")
PY
    return
  fi
  echo ""
}

if ! command -v jq >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  deny_fixed missing_interpreter
fi

if [[ -z "${input//[[:space:]]/}" ]]; then
  deny_fixed empty_input
fi

path="$(extract_path)"
if [[ -z "$path" ]]; then
  deny_fixed bad_path
fi

case "$path" in
  goals/*|*/goals/*) ;;
  *) allow ;;
esac

root="$(pwd)"
stamp="${root}/.nlc/before-generate-stamp.json"
if [[ ! -f "$stamp" ]]; then
  deny_fixed no_stamp
fi

hub="${NLC_HUB:-$HOME/.local/share/nlc/hub}"
check="${hub}/tools/nlc_guide_state.py"
if [[ -f "$check" ]]; then
  if ! python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, '${hub}/tools')
from nlc_guide_state import before_generate_stamp_valid
sys.exit(0 if before_generate_stamp_valid(Path('${root}')) else 1)
" 2>/dev/null; then
    deny_fixed stale_stamp
  fi
fi
allow
