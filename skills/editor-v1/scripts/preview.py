#!/usr/bin/env python3
"""preview.py — prove the install works end to end: a 7-second Editor V1 test, no recording needed.

    $EV1_PY <skill>/scripts/preview.py [--out ~/editor-v1/_preview]

Draws its own test pictures in code (nothing downloaded, nobody's media), treats them with
ev1_treat.py, builds a comp from the real devices (tile-flash reveal, pop + shatter, a shape-matched
strobe, the red shock word, the 3D wall, a datamosh, the chrome title), renders it with HyperFrames,
lays the device-written clicks with mix-sfx.py and opens preview.mp4. Also writes preview-sheet.jpg
(one frame per beat) — look at it. The pictures are abstract on purpose: in a real edit every one
of them is real material found for the line.
"""
import argparse, json, os, shutil, subprocess, sys
import numpy as np, cv2

SK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(SK, 'components')); sys.path.insert(0, os.path.join(SK, 'scripts'))
from ev1_more import *          # noqa
import ev1_treat as T

rng = np.random.default_rng(11)


def city(w=2112, h=1188):
    """a skyline at dusk: gradient sky, blocks with lit windows"""
    y = np.linspace(0, 1, h)[:, None, None]
    im = (np.array([90, 60, 40]) * (1 - y) + np.array([40, 110, 200]) * y) * np.ones((h, w, 3))
    x = 0
    while x < w:
        bw = int(rng.integers(90, 260)); bh = int(rng.integers(300, 900))
        im[h - bh:, x:x + bw] = rng.integers(15, 45)
        for wy in range(h - bh + 30, h - 20, 46):
            for wx in range(x + 16, x + bw - 20, 34):
                if rng.random() < 0.45:
                    im[wy:wy + 20, wx:wx + 14] = (120, 210, 250)
        x += bw + int(rng.integers(6, 30))
    return np.clip(im, 0, 255).astype(np.uint8)


def card(w=900, h=620, seed=0):
    """a page: a header bar, a headline block, text lines"""
    r = np.random.default_rng(seed)
    im = np.full((h, w, 3), 244, np.uint8)
    im[:70] = (40, 40, 40)
    cv2.rectangle(im, (50, 120), (w - int(r.integers(120, 300)), 190), (30, 30, 30), -1)
    for k in range(7):
        y = 240 + k * 50
        cv2.rectangle(im, (50, y), (w - int(r.integers(60, 260)), y + 18), (150, 150, 150), -1)
    return im


def circle(seed):
    r = np.random.default_rng(seed)
    im = np.full((1080, 1920, 3), int(r.integers(10, 40)), np.uint8)
    cv2.circle(im, (960 + int(r.integers(-80, 80)), 540 + int(r.integers(-40, 40))), int(r.integers(280, 400)),
               tuple(int(v) for v in r.integers(120, 255, 3)), -1)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.expanduser('~/editor-v1/_preview'))
    a = ap.parse_args()
    out = a.out
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(f'{out}/assets/img', exist_ok=True)
    shutil.copytree(os.path.join(SK, 'assets'), f'{out}/assets/ev1')
    if not os.path.exists(f'{out}/assets/ev1/vendor/gsap.min.js'):
        sys.exit('preview: GSAP missing: run scripts/doctor.sh first')
    os.chdir(out)
    I = lambda n: f'assets/img/{n}.jpg'
    T.treat(city(), I('city'), 'teal', size=(2112, 1188), ht=0.3, vig=0.7)
    T.treat(city(), I('city_deep'), 'deep', size=(1920, 1080), vig=0.6)
    for k in range(3):
        cv2.imwrite(I(f'card{k}'), card(seed=k))
    for k in range(6):
        T.treat(circle(k), I(f'circ{k}'), ['mono', 'warm', 'teal'][k % 3], size=(1920, 1080))
    for k in range(6):
        T.treat(card(1600, 1000, seed=10 + k), I(f'wall{k}'), 'natural', size=(1280, 794))
    g = T.treat(city(), None, 'warm', size=(1920, 1080))
    for k, fimg in enumerate(T.glitch_frames(g, 4)):
        cv2.imwrite(I(f'gl{k}'), fimg)

    c = Comp(7.0)
    # 0.0 tile-flash reveal from black onto the skyline, then it holds and pushes
    tend = tile_reveal(c, 0.0, I('city'), z=2, seed=3)
    c.clip(0, tend, '<div class="ev1-layer ev1-black"></div>', z=1)
    still(c, tend, 1.4, I('city'), z=1)
    finish(c, 0, 1.4)
    captions(c, [([('This', 0.10), ('is', 0.30), ('Editor', 0.50), ('V1.', 0.82)], 1.4)])
    # 1.4 three cards pop one per word, pull out, shatter into white blocks
    pop_shatter(c, 1.4, 2.6, [(I('card0'), 520, 520, 620, -4, 1.47), (I('card1'), 990, 580, 640, 2, 1.70),
                              (I('card2'), 1440, 510, 600, -3, 1.93)], z=1)
    captions(c, [([('Real', 1.47), ('pictures,', 1.70), ('every', 1.93), ('word.', 2.15)], 2.6)])
    # 2.6 a shape-matched strobe: every image a circle, 3 frames each, a click each
    strobe(c, 2.6, 3.4, [I(f'circ{k}') for k in range(6)], z=1)
    # 3.4 negative flash into the crushed plate, the red shock word cuts on hard
    s = still(c, 3.4, 4.4, I('city_deep'), z=1, push=1.04)
    neg_flash(c, 3.4, [s[1]])
    keyword(c, 3.47, 4.4, 'EVERY CUT', z=10, kind='shock', sound='hit')
    finish(c, 3.4, 4.4)
    # 4.4 the 3D wall the camera sweeps across
    wall3d(c, 4.4, 5.6, [I(f'wall{k}') for k in range(6)], z=1)
    captions(c, [([('on', 4.5), ('the', 4.62), ('beat.', 4.76)], 5.6)])
    # 5.6 a 4-frame datamosh, a white frame, then the chrome title on paper
    t = frames(c, 5.6, [I(f'gl{k}') for k in range(4)], z=1)
    white_flash(c, t)
    c.clip(t + 1 / 30, 7.0, '<div class="ev1-layer ev1-paper"><div class="ev1-vignette"></div></div>', z=1)
    keyword(c, t + 1 / 30, 7.0, 'Editor V1', z=10, kind='title', sound='swish')

    c.write('index.html', 'assets/ev1/tokens.css', title='Editor V1 preview')
    c.write_cues('sfx-cues.txt')
    hf = ['npx', '-y', 'hyperframes@' + os.environ.get('HF_VERSION', '0.8.181')]
    lint = subprocess.run(hf + ['lint', '.'], capture_output=True, text=True)
    print(lint.stdout[-600:])
    r = subprocess.run(hf + ['render', '.', '-q', 'standard', '-f', '30', '-o', 'render.mp4'], capture_output=True, text=True)
    if r.returncode or not os.path.exists('render.mp4'):
        sys.exit('preview: render failed\n' + r.stdout[-1500:] + r.stderr[-1500:])
    subprocess.run([sys.executable, os.path.join(SK, 'scripts', 'mix-sfx.py'), 'render.mp4', 'sfx-cues.txt', 'preview.mp4'], check=True)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', 'preview.mp4', '-vf',
                    "select='eq(n\\,8)+eq(n\\,50)+eq(n\\,62)+eq(n\\,90)+eq(n\\,115)+eq(n\\,150)+eq(n\\,169)+eq(n\\,200)',scale=480:-2,tile=4x2",
                    '-frames:v', '1', 'preview-sheet.jpg'], check=True)
    n = len(open('sfx-cues.txt').read().strip().splitlines()) - 1
    print(f'preview: {out}/preview.mp4  ({n} sound cues)  sheet: {out}/preview-sheet.jpg')
    if sys.platform == 'darwin':
        subprocess.run(['open', 'preview.mp4'])


if __name__ == '__main__':
    main()
