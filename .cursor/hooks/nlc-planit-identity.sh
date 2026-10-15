#!/usr/bin/env bash
# Prove the on-disk Planit skill matches this repository's registry before a prompt is sent.
input="$(cat)"
root="$(cd "$(dirname "$0")/../.." && pwd)"
if ! python3 "$root/tools/fitness-planit-identity.py" --skill-only --loaded .agents/skills/planit/SKILL.md >/dev/null 2>&1; then
  printf '%s\n' '{"permission":"deny","user_message":"This repository Planit skill does not match the registered hash.","agent_message":"Run python3 tools/fitness-planit-identity.py --skill-only --loaded .agents/skills/planit/SKILL.md and load .agents/skills/planit/SKILL.md."}'
  exit 2
fi
printf '%s\n' '{"permission":"allow"}'
exit 0
