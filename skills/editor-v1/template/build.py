"""build.py — the Editor V1 edit of this video, keyed to the speaker's word onsets.

One block per line of PLAN.md: a device from components/ev1_devices.py or ev1_more.py, fed with the
real material sourced for that line (work/assets.json, filled by work/prep.py). The devices write their
own sound cues, so the cue sheet can never drift from the cut.

    $EV1_PY build.py                       -> index.html + sfx-cues.txt + work/shots.json
    hf lint .  &&  hf snapshot . --at <every beat> --no-end -o out/snaps     (read every frame)
    hf render . -q high -f 30 -o out/render.mp4
    bash <skill>/scripts/finish.sh .

Beats that show the video itself (its own timeline, filmstrip, cue sheet) need a second pass:
PASS=1 render -> work/pass2_prep.py -> PASS=2 build + render (see template/example/).
The full worked example of a 45 s cold open is template/example/build.py.
"""
import json, os, sys
KIT = json.load(open('kit.json'))['skill']
sys.path.insert(0, os.path.join(KIT, 'components'))
from ev1_more import *          # noqa  (every device: ev1_devices + ev1_more)

PASS = int(os.environ.get('PASS', '1'))
FINAL = os.environ.get('FINAL') == '1'          # FINAL=1 refuses to write while placeholders remain

W_ = json.load(open('work/tx/words.json'))
WORDS = [(w['w'], w['s']) for w in W_]
VO_END = W_[-1]['e']
DUR = fr(VO_END + 1.4)                           # ~1.4 s end card after the last word


def norm(w): return w.strip('.,:;?!"').lower()


def find(word, after=0.0):
    """onset of the first `word` at or after `after` seconds"""
    for w, t in WORDS:
        if norm(w) == norm(word) and t >= after - 1e-6:
            return t
    raise KeyError(word)


def span(first, last, after=0.0):
    """[(word, onset)] from `first` to `last`: one caption group"""
    out, on = [], False
    for w, t in WORDS:
        if not on and norm(w) == norm(first) and t >= after - 1e-6:
            on = True
        if on:
            out.append((w, t))
            if norm(w) == norm(last):
                return out
    raise KeyError(first)


A = json.load(open('work/assets.json')) if os.path.exists('work/assets.json') else {}
SIL = [tuple(map(float, l.split())) for l in open('work/silences.txt')] if os.path.exists('work/silences.txt') else []
c = Comp(DUR)
F1 = 1 / FPS
MISSING, PLACEHOLDERS, SHOTS = [], [], []


def has(*ks):
    ok = all(k in A and os.path.exists(A[k]) for k in ks)
    if not ok:
        MISSING.extend(k for k in ks if k not in A)
    return ok


def ph(t0, t1, label, z=1):
    """a loud magenta placeholder for a beat whose material isn't sourced yet (never ships: FINAL=1 refuses)"""
    PLACEHOLDERS.append(label)
    c.clip(t0, t1, f'<div class="ev1-layer" style="background:#2a2a2a"><div style="position:absolute;left:80px;top:80px;'
                   f'font:700 60px var(--ev1-sans);color:#f0f">{esc(label)}</div></div>', z)


def shot(t0, t1, name):
    SHOTS.append((fr(t0), fr(t1), name))


def face(t0, t1, punch=None, z=1):
    """the speaker on camera, RAW (no grade, no B&W, no vignette): one more picture in the stream.
    punch = (t, scale) a hard punch-in on the stressed word."""
    v = broll(c, t0, t1, 'assets/media/cam_raw.mp4', z=z, rate=0.012, media_start=fr(t0),
              punches=[punch] if punch else ())
    shot(t0, t1, 'face')
    return v


# ============================================================ BEATS — one block per PLAN.md line
# Replace these with the real beats. Each: b, e = beat start/end from the words; the device; captions.
#
# Line 1 — the opening: a tile-flash reveal from black onto a real still, then its moving clip.
b, e = 0.0, fr(WORDS[min(3, len(WORDS) - 1)][1])
if has('open_still', 'open_clip'):
    tend = tile_reveal(c, b, A['open_still'], z=2, seed=3, size=(1920, 1080))
    c.clip(b, tend, '<div class="ev1-layer ev1-black"></div>', z=1)
    broll(c, tend, e, A['open_clip'], z=1, rate=0.07)
else:
    ph(b, e, 'line 1: open_still + open_clip')
shot(b, e, 'open')
captions(c, [(WORDS[:3], e)])
#
# Line 2 — the speaker, raw, with the stressed word huge and red BEHIND the head needs the matte:
#   $EV1_PY <skill>/scripts/matte.py --plate assets/media/cam_raw.mp4 --start <b> --dur <e-b> --out assets/media/matte_a.webm
#   cutout_world(c, b, e, [('video', 'assets/media/cam_raw.mp4', b, None, b)], 'assets/media/matte_a.webm', b, z=1,
#                mega=('EDIT', find('edit'), 560))
# The rest of the take, until it's built:
b = e
if b < fr(VO_END):
    face(b, fr(VO_END))
    ph(b, fr(VO_END), 'the rest: one device per line (PLAN.md)', z=2)

# end card
c.clip(fr(VO_END), DUR, '<div class="ev1-layer ev1-black"></div>', z=1)
sfx(c, fr(VO_END), 'outro', 0.8)

finish(c, 0, DUR, z=80, grid=False, vignette=False)   # grid/vignette per beat is better: finish(c, b, e) on image beats

if FINAL and (PLACEHOLDERS or MISSING):
    sys.exit(f'build.py: FINAL refused — placeholders {PLACEHOLDERS}, missing assets {sorted(set(MISSING))}')
c.write('index.html', 'assets/ev1/tokens.css', title='Editor V1')
c.write_cues('sfx-cues.txt')
json.dump(sorted(SHOTS), open('work/shots.json', 'w'))
print('PASS', PASS, 'dur', DUR, 'cues', len(c.cues), 'shots', len(SHOTS),
      'placeholders', len(PLACEHOLDERS), 'missing', sorted(set(MISSING)))
