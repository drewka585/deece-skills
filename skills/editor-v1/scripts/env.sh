#!/usr/bin/env bash
# env.sh — source this at the top of every step:   source "<skill>/scripts/env.sh"
#
# Claude Code runs commands in non-interactive shells that often skip your shell profile, so
# node / ffmpeg installed with nvm, Homebrew or ~/.local/bin come back "command not found"
# even though they work in your terminal. This puts the usual install places on PATH
# (newest nvm Node first), pins the renderer version this kit was tested with, and points
# EV1_PY at the kit's private Python.
# Every line must exit 0: callers run under `set -e`.
_ev1_add(){ case ":$PATH:" in *":$1:"*) ;; *) if [ -d "$1" ]; then PATH="$1:$PATH"; fi;; esac; return 0; }
_ev1_add /usr/local/bin
_ev1_add /opt/homebrew/bin
_ev1_add "$HOME/.local/bin"
_ev1_add "$HOME/.volta/bin"
_ev1_add "$HOME/.fnm/aliases/default/bin"
if [ -d "$HOME/.nvm/versions/node" ]; then
  _ev1_node=$(ls -1 "$HOME/.nvm/versions/node" 2>/dev/null | sed 's/^v//' | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)
  if [ -n "$_ev1_node" ]; then _ev1_add "$HOME/.nvm/versions/node/v$_ev1_node/bin"; fi
fi
export PATH

# the renderer, pinned (override: export HF_VERSION=latest)
export HF_VERSION="${HF_VERSION:-0.8.181}"
hf(){ npx -y "hyperframes@${HF_VERSION}" "$@"; }

# the kit's private Python: numpy, opencv, pillow, soundfile (+ torch for the cut-out, optional)
export EV1_HOME="$HOME/.cache/editor-v1"
if [ -x "$EV1_HOME/venv/bin/python" ]; then EV1_PY="$EV1_HOME/venv/bin/python"; else EV1_PY="$(command -v python3)"; fi
export EV1_PY
true
