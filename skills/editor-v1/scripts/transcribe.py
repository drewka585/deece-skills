#!/usr/bin/env python3
"""transcribe.py — word timings for the take, in 20 s windows, checked for dropped speech.

    $EV1_PY <skill>/scripts/transcribe.py <video-dir>                 reads assets/media/vo.wav
    $EV1_PY <skill>/scripts/transcribe.py <video-dir> --src take.mov --language fr

Writes <video-dir>/work/tx/words.json  [{"w": "Right", "s": 0.0, "e": 0.24}, ...]
       <video-dir>/work/tx/transcript.txt  (the words, one sentence per line, to read through)

Why windows: on long files the Parakeet engine can SILENTLY drop whole spans of speech (it
once lost 77 s of a 164 s take with no error). Every file is cut into 20 s windows with 2 s
of overlap; each window owns its middle, so a word on a seam is kept once. Afterwards every
stretch of speech-level audio with no words in it is printed — read those before building.
Then run snap-onsets.py: the engine puts the first word after a pause 60-220 ms early.

Engine: HyperFrames picks Parakeet when installed (doctor.sh --install-speech, Apple
Silicon), else whisper. ASR mishears names (ChatGPT, Claude, product names): fix them in
words.json by hand against what was said, keeping the timings.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
import numpy as np

WIN, OVL = 20.0, 2.0


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def duration(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).stdout.strip())


def window(src, ss, t, lang, tmp):
    d = tempfile.mkdtemp(dir=tmp)
    clip = os.path.join(d, 'clip.mp4')
    # a tiny video stream is kept on purpose: audio-only inputs can come back with no transcript
    run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=320x180:r=10',
         '-ss', f'{ss:.3f}', '-t', f'{t:.3f}', '-i', src, '-map', '0:v', '-map', '1:a:0', '-shortest',
         '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '40', '-c:a', 'aac', '-b:a', '128k', '-ac', '1', '-ar', '16000', clip])
    cmd = ['npx', '-y', 'hyperframes@' + os.environ.get('HF_VERSION', '0.8.181'), 'transcribe', clip, '-d', d, '--json']
    if lang:
        cmd += ['--language', lang]
    res = json.loads(run(cmd).stdout.strip().splitlines()[-1])
    words = json.load(open(res.get('transcriptPath') or os.path.join(d, 'transcript.json')))
    return [(w['text'].strip(), w['start'] + ss, w['end'] + ss) for w in words if w.get('text', '').strip()], res.get('engine')


def rms_100ms(src):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(x) // 1600
    return 20 * np.log10(np.sqrt((x[:n * 1600].reshape(n, 1600) ** 2).mean(1)) + 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video_dir')
    ap.add_argument('--src', default=None)
    ap.add_argument('--language', default=None)
    a = ap.parse_args()
    vd = a.video_dir
    src = a.src or os.path.join(vd, 'assets', 'media', 'vo.wav')
    if not os.path.isfile(src):
        sys.exit(f'transcribe: no such file {src}')
    D = duration(src)
    tmp = tempfile.mkdtemp(prefix='ev1tx-')
    words, engine = [], None
    try:
        starts = [0.0] if D <= WIN + 1 else list(np.arange(0, D - OVL, WIN - OVL))
        for k, ss in enumerate(starts):
            t = min(WIN, D - ss)
            got, engine = window(src, ss, t, a.language, tmp)
            lo = 0.0 if k == 0 else ss + OVL / 2
            hi = D + 1 if k == len(starts) - 1 else ss + WIN - OVL / 2
            words += [w for w in got if lo <= w[1] < hi]
            print(f'  window {k + 1}/{len(starts)}  {ss:6.1f}-{ss + t:6.1f}s  {len(got)} words', file=sys.stderr)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    words.sort(key=lambda w: w[1])
    out = os.path.join(vd, 'work', 'tx')
    os.makedirs(out, exist_ok=True)
    json.dump([{'w': w, 's': round(s, 3), 'e': round(e, 3)} for w, s, e in words], open(os.path.join(out, 'words.json'), 'w'), indent=0)
    text = ' '.join(w for w, _, _ in words)
    open(os.path.join(out, 'transcript.txt'), 'w').write(re.sub(r'([.?!])\s+', r'\1\n', text) + '\n')
    # dropped-speech check: speech-level audio (within 20 dB of the loud parts) with no word for > 1.5 s
    r = rms_100ms(src)
    speech = r > np.percentile(r, 95) - 20
    covered = np.zeros(len(r), bool)
    for _, s, e in words:
        covered[int(s * 10):int(e * 10) + 1] = True
    gaps, run_ = [], 0
    for i, (sp, cv) in enumerate(zip(speech, covered)):
        run_ = run_ + 1 if (sp and not cv) else 0
        if run_ == 15:
            gaps.append(i / 10 - 1.4)
    print(f'transcribe: {len(words)} words, {engine}, {D:.1f}s -> {out}/words.json')
    for g in gaps:
        print(f'  CHECK {g:6.1f}s: speech-level audio with no words for 1.5 s+ (a dropped span?)')
    if not gaps:
        print('  no dropped spans found')


if __name__ == '__main__':
    main()
