#!/usr/bin/env python3
"""matte.py — cut the speaker out of the RAW camera for the hero beat (the world changes behind
them, the big red word sits behind their head). Needs doctor.sh --install-matte (PyTorch).

    $EV1_PY <skill>/scripts/matte.py --plate assets/media/cam_raw.mp4 --start 15.5 --dur 4.4 \
        --out assets/media/matte_a.webm

Writes a VP9 video with an alpha channel (yuva420p), RGB premultiplied over black, taken from
the same raw plate the face beats use, so the cut-out matches the face shots exactly.
Frame 0 of the webm = plate time --start. In the comp: data-media-start = beat_start - start
(components/ev1_more.py cutout_world(matte_src=..., matte_first_s=start) does this for you).

Model: Robust Video Matting (mobilenetv3), loaded at run time from its public repo through
torch.hub (GPL-3.0, not shipped in this kit). Its recurrent state is why the edge does not
crawl frame to frame; two warm-up passes on the first frame kill the first-frame flicker.
--harden lifts the soft fringe (a mic or a chair edge reading as half-transparent).
"""
import argparse, subprocess, sys
import numpy as np

W, H, FPS = 1920, 1080, 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plate', required=True)
    ap.add_argument('--start', type=float, required=True)
    ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--downsample', type=float, default=0.3, help='0.25 sharper hair (slower), 0.4 softer')
    ap.add_argument('--harden', type=float, default=0.04, help='alpha below this -> 0, rescaled; 0 = off')
    ap.add_argument('--device', default='auto', choices=['auto', 'cpu', 'mps', 'cuda'])
    a = ap.parse_args()

    import torch
    dev = a.device
    if dev == 'auto':
        dev = 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu')
    model = torch.hub.load('PeterL1n/RobustVideoMatting', 'mobilenetv3', trust_repo=True).eval().to(dev)

    n = int(round(a.dur * FPS))
    dec = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-ss', f'{a.start:.4f}', '-i', a.plate, '-frames:v', str(n),
                            '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '28',
                            '-row-mt', '1', '-deadline', 'good', '-cpu-used', '4', '-auto-alt-ref', '0', '-g', '30', a.out],
                           stdin=subprocess.PIPE)
    rec = [None] * 4
    k = 0
    with torch.no_grad():
        while True:
            buf = dec.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            x = torch.from_numpy(rgb).to(dev).permute(2, 0, 1)[None].float() / 255
            for _ in range(3 if k == 0 else 1):              # warm-up on frame 0
                _, pha, *rec = model(x, *rec, downsample_ratio=a.downsample)
            al = pha[0, 0].clamp(0, 1).cpu().numpy()
            if a.harden > 0:
                al = np.clip((al - a.harden) / (1 - 2 * a.harden), 0, 1)
            a8 = (al * 255 + 0.5).astype(np.uint8)
            pre = (rgb.astype(np.float32) * al[..., None] + 0.5).astype(np.uint8)
            enc.stdin.write(np.dstack([pre, a8]).tobytes())
            k += 1
            if k % 30 == 0:
                print(f'  {k}/{n} frames', file=sys.stderr)
    enc.stdin.close()
    enc.wait(); dec.wait()
    print(f'matte: {k} frames ({dev}) -> {a.out}  (frame 0 = plate {a.start:.3f}s)')


if __name__ == '__main__':
    main()
