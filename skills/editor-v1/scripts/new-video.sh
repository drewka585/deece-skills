#!/usr/bin/env bash
# new-video.sh — start a new Editor V1 video from a recording.
#
#   bash <skill>/scripts/new-video.sh <recording> [name] [--dir <parent>]
#
#   <recording>  the talking-head take (.mov / .mp4 / .mkv), 16:9
#   [name]       folder name; default: today's date + the file name
#   --dir        where videos live; default: ~/editor-v1/videos
#
# Creates <parent>/<name>/ with
#   build.py  PLAN.md  kit.json        the template (kit.json says where the skill lives)
#   assets/ev1/                        tokens.css, fonts/, vendor/gsap.min.js (the page loads these)
#   assets/media/src.<ext>             the recording (a hard link: no extra disk)
#   assets/media/cam_raw.mp4           the camera, RAW: re-timed to 30 fps CFR with a keyframe a
#                                      second (the renderer seeks badly otherwise), NO grade
#   assets/media/vo.wav                the voice, 48 kHz
#   assets/{img,clips,captures,music}/ work/tx/  out/
set -euo pipefail
SK="$(cd "$(dirname "$0")/.." && pwd)"
source "$SK/scripts/env.sh"
REC="${1:?usage: new-video.sh <recording> [name] [--dir parent]}"; shift
NAME=""; PARENT="$HOME/editor-v1/videos"
while [ $# -gt 0 ]; do
  case "$1" in
    --dir) PARENT="$2"; shift 2;;
    *) NAME="$1"; shift;;
  esac
done
[ -f "$REC" ] || { echo "new-video: no such file: $REC" >&2; exit 1; }
[ -s "$SK/assets/vendor/gsap.min.js" ] || { echo "new-video: GSAP missing: run scripts/doctor.sh first" >&2; exit 1; }
if [ -z "$NAME" ]; then
  base="$(basename "$REC")"; base="${base%.*}"
  NAME="$(date +%Y-%m-%d)-$(printf '%s' "$base" | tr 'A-Z' 'a-z' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//' | cut -c1-40)"
fi
VD="$PARENT/$NAME"
[ -e "$VD" ] && { echo "new-video: $VD already exists" >&2; exit 1; }

mkdir -p "$VD"/assets/{ev1,media,img,clips,captures,music} "$VD"/work/tx "$VD"/out
cp "$SK/assets/tokens.css" "$VD/assets/ev1/"
cp -R "$SK/assets/fonts" "$SK/assets/vendor" "$VD/assets/ev1/"
cp "$SK/template/build.py" "$SK/template/PLAN.md" "$VD/"
printf '{\n  "skill": "%s",\n  "created": "%s"\n}\n' "$SK" "$(date +%Y-%m-%d)" > "$VD/kit.json"

ext="${REC##*.}"
ln "$REC" "$VD/assets/media/src.$ext" 2>/dev/null || cp "$REC" "$VD/assets/media/src.$ext"
echo "new-video: camera -> assets/media/cam_raw.mp4 (raw, 30 fps CFR)"
ffmpeg -nostdin -v error -stats -y -i "$VD/assets/media/src.$ext" -map 0:v:0 -vf "fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 14 -preset medium -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -an "$VD/assets/media/cam_raw.mp4"
echo "new-video: voice -> assets/media/vo.wav"
ffmpeg -nostdin -v error -y -i "$VD/assets/media/src.$ext" -map 0:a:0 -ac 2 -ar 48000 -c:a pcm_s24le "$VD/assets/media/vo.wav"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VD/assets/media/cam_raw.mp4")
echo
echo "new-video: $VD  (${D}s)"
echo "next: \$EV1_PY $SK/scripts/transcribe.py \"$VD\"  then  snap-onsets.py \"$VD\""
