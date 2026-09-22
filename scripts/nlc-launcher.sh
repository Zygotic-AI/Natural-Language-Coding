#!/usr/bin/env bash
# Installed to ~/.local/bin/nlc — runs hub CLI with NLC_HUB set.
set -euo pipefail
INSTALL_ROOT="${NLC_INSTALL_ROOT:-${HOME}/.local/share/nlc}"
export NLC_HUB="${NLC_HUB:-${INSTALL_ROOT}/hub}"
exec python3 "${NLC_HUB}/tools/nlc.py" "$@"
