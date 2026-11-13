#!/usr/bin/env bash
# finish.sh — picture + sound -> out/final.mp4, measured, opened for review. Publishes nothing.
#
#   bash <skill>/scripts/finish.sh <video-dir> [picture.mp4]      (default picture: out/render.mp4)
#
# 1. lays work/premix.wav (voice + bed, from bed-mix.py) under the silent render; with no premix,
#    the plain voice (assets/media/vo.wav)
# 2. lays the device-written sfx-cues.txt on top (mix-sfx.py)
# 3. prints loudness, true peak, duration and frame count, and opens the file
set -euo pipefail
SK="$(cd "$(dirname "$0")/.." && pwd)"
source "$SK/scripts/env.sh"
VD="${1:?usage: finish.sh <video-dir> [picture.mp4]}"
cd "$VD"
PIC="${2:-out/render.mp4}"
[ -f "$PIC" ] || { echo "finish: no picture at $PIC (render first)" >&2; exit 1; }
AUD="work/premix.wav"; [ -f "$AUD" ] || AUD="assets/media/vo.wav"
ffmpeg -nostdin -v error -y -i "$PIC" -i "$AUD" -map 0:v:0 -map 1:a:0 -c:v copy -c:a pcm_s24le out/_mux.mov
if [ -s sfx-cues.txt ]; then
  "$EV1_PY" "$SK/scripts/mix-sfx.py" out/_mux.mov sfx-cues.txt out/final.mp4
else
  ffmpeg -nostdin -v error -y -i out/_mux.mov -c:v copy -c:a aac -b:a 256k out/final.mp4
fi
rm -f out/_mux.mov
L=$(ffmpeg -nostdin -i out/final.mp4 -af loudnorm=print_format=summary -f null - 2>&1 | grep -E "Input (Integrated|True Peak)" | awk '{print $3, $4}' | paste -sd' ' -)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/final.mp4)
N=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 out/final.mp4)
echo "finish: out/final.mp4  ${D}s  ${N} frames  loudness/true peak: $L"
case "$(uname -s)" in Darwin) open out/final.mp4 ;; Linux) (xdg-open out/final.mp4 >/dev/null 2>&1 &) ;; esac
