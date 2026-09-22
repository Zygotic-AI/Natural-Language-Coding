#!/usr/bin/env bash
# UC18: block goal-tree writes until nlc-before-generate stamp is fresh (planit step 6).
set -euo pipefail
input="$(cat)"
path=""
if command -v jq >/dev/null 2>&1; then
  path="$(echo "$input" | jq -r '.tool_input.path // .tool_input.file_path // .path // empty' 2>/dev/null || true)"
fi
if [[ -z "$path" ]]; then
  echo '{"permission":"allow"}'
  exit 0
fi
case "$path" in
  goals/*|*/goals/*) ;;
  *)
    echo '{"permission":"allow"}'
    exit 0
    ;;
esac
root="$(pwd)"
stamp="${root}/.nlc/before-generate-stamp.json"
if [[ ! -f "$stamp" ]]; then
  echo '{
    "permission": "deny",
    "user_message": "Run the knowledge check before editing goals (PLANIT step 6).",
    "agent_message": "Run: ./nlc maintainer guide before-generate --scope default (or your scopes), then edit goals."
  }'
  exit 0
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
    echo '{
      "permission": "deny",
      "user_message": "Knowledge check stamp expired — re-run before generate.",
      "agent_message": "Run ./nlc maintainer guide before-generate again, then continue PLANIT step 6."
    }'
    exit 0
  fi
fi
echo '{"permission":"allow"}'
exit 0
