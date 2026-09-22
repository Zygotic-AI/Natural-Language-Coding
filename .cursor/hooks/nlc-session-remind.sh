#!/usr/bin/env bash
# Remind agent to read ./nlc queue at session start (hub / app repos).
set -euo pipefail
if [[ -x ./nlc ]] || command -v nlc >/dev/null 2>&1; then
  echo '{"followup_message": "Run ./nlc (or nlc) and read YOUR QUEUE before generating code. Human judgment gates: docs/nlc/HUMAN-JUDGMENT-GATES.md"}'
else
  echo '{}'
fi
exit 0
