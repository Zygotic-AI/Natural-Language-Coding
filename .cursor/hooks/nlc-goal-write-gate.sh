#!/usr/bin/env bash
# UC18: block goal-tree writes until nlc-before-generate stamp is fresh (planit step 6).
set -euo pipefail

if command -v cat >/dev/null 2>&1; then
  input="$(cat)"
else
  input=""
  while IFS= read -r _line || [[ -n "${_line:-}" ]]; do
    input+="${_line}"$'\n'
  done
  input="${input%$'\n'}"
fi

deny_fixed() {
  case "$1" in
    missing_interpreter)
      printf '%s\n' '{"permission":"deny","user_message":"Goal-write hook cannot run (missing jq and python3).","agent_message":"Install jq or python3 so the goal-write hook can fail closed."}'
      ;;
    empty_input)
      printf '%s\n' '{"permission":"deny","user_message":"Goal-write hook refused empty hook input.","agent_message":"Retry the edit; if this persists, fix hook JSON payload."}'
      ;;
    bad_path)
      printf '%s\n' '{"permission":"deny","user_message":"Goal-write hook could not read the target path.","agent_message":"Malformed hook input; refuse rather than allow goal writes."}'
      ;;
    no_stamp)
      printf '%s\n' '{"permission":"deny","user_message":"Run the knowledge check before editing goals (PLANIT step 6).","agent_message":"Run: ./nlc maintainer guide before-generate --scope default (or your scopes), then edit goals."}'
      ;;
    stale_stamp)
      printf '%s\n' '{"permission":"deny","user_message":"Knowledge check stamp expired — re-run before generate.","agent_message":"Run ./nlc maintainer guide before-generate again, then continue PLANIT step 6."}'
      ;;
  esac
  exit 0
}

allow() {
  printf '%s\n' '{"permission":"allow"}'
  exit 0
}

have_jq=0
have_python=0
command -v jq >/dev/null 2>&1 && have_jq=1
command -v python3 >/dev/null 2>&1 && have_python=1

extract_path() {
  if (( have_jq )); then
    echo "$input" | jq -r '.tool_input.path // .tool_input.file_path // .path // empty' 2>/dev/null || true
    return
  fi
  if (( have_python )); then
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

if (( ! have_jq && ! have_python )); then
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

guide_tools=""
search="${root}"
while [[ "$search" != "/" ]]; do
  if [[ -f "${search}/tools/nlc_guide_state.py" ]]; then
    guide_tools="${search}/tools"
    break
  fi
  search="$(dirname "$search")"
done
if [[ -z "$guide_tools" && -n "${NLC_HUB:-}" && -f "${NLC_HUB}/tools/nlc_guide_state.py" ]]; then
  guide_tools="${NLC_HUB}/tools"
fi
if [[ -z "$guide_tools" && -f "${HOME}/.local/share/nlc/hub/tools/nlc_guide_state.py" ]]; then
  guide_tools="${HOME}/.local/share/nlc/hub/tools"
fi

if [[ -n "$guide_tools" ]] && (( have_python )); then
  if ! python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, '${guide_tools}')
from nlc_guide_state import before_generate_stamp_valid
sys.exit(0 if before_generate_stamp_valid(Path('${root}')) else 1)
" 2>/dev/null; then
    deny_fixed stale_stamp
  fi
else
  deny_fixed stale_stamp
fi

allow
