#!/usr/bin/env python3
"""mix-sfx.py — lay the device-written cue sheet onto a video's sound.

    $EV1_PY <skill>/scripts/mix-sfx.py <in.mp4> <sfx-cues.txt> <out.mp4>

sfx-cues.txt is written by the devices (Comp.write_cues); one cue per line:
    <time>  <sound>  <gain>
  time  = when the FILE starts, in seconds. The devices already pre-roll each cue by its
          transient, so the click lands on the frame the picture changes. Don't hand-edit.
  sound = a name under <skill>/sfx/ without the extension (ev1kit/click_3, ev1/tick),
          or a path to any audio file.
  gain  = linear volume.
'#' lines and blank lines are skipped.

The video stream is copied untouched; the audio is rebuilt at 48 kHz stereo: the input's own
audio (voice + bed) plus every cue, through a peak limiter at -1 dBFS (no auto-levelling).
A video with no audio track gets silence underneath.
"""
import os, subprocess, sys
import numpy as np
import soundfile as sf

SR = 48000
SFX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx')


def probe_dur(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                       capture_output=True, text=True, check=True).stdout.strip()
    return float(o)


def has_audio(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', p],
                       capture_output=True, text=True).stdout.strip()
    return bool(o)


def decode(p):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', p, '-map', '0:a:0', '-ac', '2', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def resolve(name):
    if os.path.isfile(name):
        return name
    for ext in ('', '.wav', '.mp3', '.aif', '.aiff', '.flac'):
        p = os.path.join(SFX, name + ext)
        if os.path.isfile(p):
            return p
    sys.exit(f"mix-sfx: unknown sound '{name}' (looked in {os.path.normpath(SFX)}); run scripts/synth-sfx.py")


_cache = {}


def load(path):
    if path not in _cache:
        if path.endswith(('.wav', '.flac', '.aif', '.aiff')):
            x, sr = sf.read(path, dtype='float32', always_2d=True)
        else:
            x, sr = decode(path), SR
        if sr != SR:   # rare: resample through ffmpeg
            x, sr = decode(path), SR
        if x.shape[1] == 1:
            x = np.repeat(x, 2, axis=1)
        x = x[:, :2].copy()
        n = min(len(x), int(0.006 * SR))     # 6 ms fade-in so no file starts on a click of its own
        x[:n] *= np.linspace(0, 1, n, dtype=np.float32)[:, None]
        _cache[path] = x
    return _cache[path]


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    src, cues_p, out = sys.argv[1:]
    dur = probe_dur(src)
    n = int(round(dur * SR))
    base = decode(src) if has_audio(src) else np.zeros((n, 2), np.float32)
    base = np.pad(base, ((0, max(0, n - len(base))), (0, 0)))[:n]
    k = 0
    for line in open(cues_p):
        parts = line.split('#', 1)[0].split()
        if not parts:
            continue
        t, name = float(parts[0]), parts[1]
        g = float(parts[2]) if len(parts) > 2 else 0.12
        x = load(resolve(name)) * g
        a = int(round(max(0.0, t) * SR))
        if a >= n:
            continue
        m = min(len(x), n - a)
        base[a:a + m] += x[:m]
        k += 1
    if not k:
        sys.exit(f'mix-sfx: no cues in {cues_p}')
    enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src,
                            '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                            '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                            '-af', 'alimiter=limit=0.891:level=0:attack=2:release=40',
                            '-c:a', 'aac', '-b:a', '256k', out],   # no -shortest: it can eat the last frame
                           stdin=subprocess.PIPE)
    enc.stdin.write(base.astype(np.float32).tobytes())
    enc.stdin.close()
    if enc.wait():
        sys.exit('mix-sfx: ffmpeg failed')
    print(f'mix-sfx: {k} cues -> {out}')


if __name__ == '__main__':
    main()
