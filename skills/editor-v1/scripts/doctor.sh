#!/usr/bin/env bash
# doctor.sh — check (and where it is free and safe, fix) everything Editor V1 needs.
#
#   bash <skill folder>/scripts/doctor.sh
#   bash <skill folder>/scripts/doctor.sh --install-speech --install-matte
#
# Fixes on its own, with no sudo and no money:
#   * a private Python venv (~/.cache/editor-v1/venv) with numpy, opencv, pillow, soundfile
#   * the HyperFrames renderer (npx) and its headless Chrome
#   * GSAP (the animation library) into assets/vendor/
#   * the sound kit, synthesised in code into sfx/
#   * --install-speech: the on-device Parakeet speech model (Apple Silicon; others get whisper)
#   * --install-matte:  PyTorch into the venv, for the cut-out (you in front of a changing world)
# Only TELLS you how to install: Node.js, ffmpeg, Python, Google Chrome.
# Re-run until it prints "All set".
SK="$(cd "$(dirname "$0")/.." && pwd)"
source "$SK/scripts/env.sh"
SPEECH=0; MATTE=0
for a in "$@"; do
  case "$a" in --install-speech) SPEECH=1;; --install-matte) MATTE=1;; esac
done
OS="$(uname -s)"; ARCH="$(uname -m)"
BAD=0
ok(){ printf '  ok      %-12s %s\n' "$1" "$2"; }
no(){ printf '  MISSING %-12s %s\n' "$1" "$2"; BAD=1; }
note(){ printf '  note    %-12s %s\n' "$1" "$2"; }

echo "editor-v1 doctor  ($OS $ARCH)"

# ── Node.js 22+ ─────────────────────────────────────────────────────────────
if command -v node >/dev/null 2>&1; then
  NV="$(node -v | sed 's/^v//')"
  if [ "${NV%%.*}" -ge 22 ] 2>/dev/null; then ok node "v$NV"
  else no node "v$NV is too old, need 22+: the LTS from https://nodejs.org (or: brew install node)"; fi
else
  no node "install the LTS from https://nodejs.org (or: brew install node; on Windows use WSL)"
fi

# ── ffmpeg / ffprobe, with VP9 (the cut-out's alpha video) ──────────────────
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
  ok ffmpeg "$(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
  if ffmpeg -hide_banner -encoders 2>/dev/null | grep -q libvpx-vp9; then ok vp9 "libvpx-vp9 encoder present"
  else note vp9 "this ffmpeg has no libvpx-vp9: the cut-out device needs it (brew install ffmpeg has it)"; fi
else
  case "$OS" in
    Darwin) no ffmpeg "brew install ffmpeg   (Homebrew: https://brew.sh)";;
    Linux)  no ffmpeg "sudo apt install ffmpeg   (or your distro's package)";;
    *)      no ffmpeg "inside WSL: sudo apt install ffmpeg";;
  esac
fi

# ── Python 3.9+ and the private venv ────────────────────────────────────────
if command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'; then
  ok python "$(python3 -V 2>&1 | awk '{print $2}')"
  VENV="$EV1_HOME/venv"
  if [ ! -x "$VENV/bin/python" ]; then
    echo "  ..      venv         creating $VENV (no sudo, nothing system-wide)"
    mkdir -p "$EV1_HOME" && python3 -m venv "$VENV" >/dev/null 2>&1
  fi
  if [ -x "$VENV/bin/python" ]; then
    if ! "$VENV/bin/python" -c 'import numpy, cv2, PIL, soundfile' 2>/dev/null; then
      echo "  ..      packages     installing numpy, opencv, pillow, soundfile into the venv"
      "$VENV/bin/pip" install -q --upgrade pip >/dev/null 2>&1
      "$VENV/bin/pip" install -q numpy opencv-python-headless pillow soundfile >/dev/null 2>&1
    fi
    if "$VENV/bin/python" -c 'import numpy, cv2, PIL, soundfile' 2>/dev/null; then
      EV1_PY="$VENV/bin/python"; ok packages "numpy opencv pillow soundfile"
    else no packages "pip install into $VENV failed: check your connection and re-run"; fi
    if [ $MATTE -eq 1 ] && ! "$VENV/bin/python" -c 'import torch, torchvision' 2>/dev/null; then
      echo "  ..      torch        installing PyTorch for the cut-out (about 1 GB, one time)"
      "$VENV/bin/pip" install -q torch torchvision >/dev/null 2>&1
    fi
    if "$VENV/bin/python" -c 'import torch, torchvision' 2>/dev/null; then ok matte "PyTorch $("$VENV/bin/python" -c 'import torch;print(torch.__version__)')"
    else note matte "not installed: re-run with --install-matte to use the cut-out device"; fi
  else no venv "python3 -m venv failed: install Python from https://www.python.org/downloads/"; fi
else
  no python "need Python 3.9+: https://www.python.org/downloads/ (or: brew install python)"
fi

# ── HyperFrames + its headless Chrome ───────────────────────────────────────
if command -v npx >/dev/null 2>&1; then
  HV="$(hf --version 2>/dev/null | tail -1)"
  if [ -n "$HV" ]; then ok hyperframes "$HV (pinned; override with HF_VERSION)"
  else no hyperframes "npx -y hyperframes@$HF_VERSION --version failed: check your connection"; fi
  if hf browser ensure >/dev/null 2>&1; then ok render-chrome "$(hf browser path 2>/dev/null | tail -1)"
  else no render-chrome "npx hyperframes browser ensure failed: re-run with a working connection"; fi
else
  no hyperframes "needs Node.js (npx) first"
fi

# ── speech-to-text ──────────────────────────────────────────────────────────
if command -v npx >/dev/null 2>&1; then
  if hf models list 2>/dev/null | grep -qi "parakeet.*installed"; then ok speech "Parakeet (on-device)"
  elif [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
    if [ $SPEECH -eq 1 ]; then
      echo "  ..      speech       installing Parakeet (free, on-device, one-time download)"
      if hf models install parakeet >/dev/null 2>&1; then ok speech "Parakeet installed"
      else note speech "Parakeet install failed: whisper is used instead (installed on first use)"; fi
    else note speech "Parakeet not installed: re-run with --install-speech (recommended on Apple Silicon)"; fi
  else note speech "whisper is installed by HyperFrames on the first transcription"; fi
fi

# ── GSAP (downloaded, not bundled) ──────────────────────────────────────────
GS="$SK/assets/vendor/gsap.min.js"
if [ ! -s "$GS" ] || ! head -c 200 "$GS" | grep -q GSAP; then
  mkdir -p "$SK/assets/vendor"
  curl -fsSL "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" -o "$GS" 2>/dev/null \
    || curl -fsSL "https://unpkg.com/gsap@3.14.2/dist/gsap.min.js" -o "$GS" 2>/dev/null
fi
if [ -s "$GS" ] && head -c 200 "$GS" | grep -q GSAP; then ok gsap "$(head -c 80 "$GS" | grep -o 'GSAP [0-9.]*')"
else no gsap "could not download GSAP 3.14.2 from jsdelivr/unpkg: check your connection"; fi

# ── sound kit (synthesised in code) ─────────────────────────────────────────
if [ ! -f "$SK/sfx/peaks.json" ] && [ -x "$EV1_PY" ]; then "$EV1_PY" "$SK/scripts/synth-sfx.py" >/dev/null 2>&1; fi
N_SFX=$(ls "$SK"/sfx/ev1kit/*.wav 2>/dev/null | wc -l | tr -d ' ')
if [ "$N_SFX" -ge 22 ]; then ok sfx "$N_SFX sounds in sfx/ev1kit"
else no sfx "python3 scripts/synth-sfx.py failed (needs numpy)"; fi

# ── a real Chrome for page captures (capture.mjs) ───────────────────────────
CH=""
for c in "${CHROME_PATH:-}" "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "$(command -v google-chrome 2>/dev/null)" "$(command -v google-chrome-stable 2>/dev/null)" "$(command -v chromium 2>/dev/null)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then CH="$c"; break; fi
done
if [ -n "$CH" ]; then ok chrome "$CH"
else note chrome "Google Chrome not found: page captures fall back to the renderer's Chrome (fine for most sites)"; fi

# ── optional ────────────────────────────────────────────────────────────────
if command -v yt-dlp >/dev/null 2>&1; then ok yt-dlp "$(yt-dlp --version 2>/dev/null)"
else note yt-dlp "optional, for pulling short clips: brew install yt-dlp (or pipx install yt-dlp)"; fi

echo
if [ $BAD -eq 0 ]; then echo "All set"; exit 0; fi
echo "Not ready yet: install the MISSING items above, then re-run this script."; exit 1
