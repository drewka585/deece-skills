#!/usr/bin/env python
"""ev1_clip.py — cut, fill and grade a moving clip for Editor V1 (the footage is the point).

    python ev1_clip.py <src> <out.mp4> --ss 12.0 --dur 0.6 [--look teal] [--speed 1.0]
                       [--focus 0.5,0.5] [--zoom 1.0] [--grain 0]

Every clip leaves here as 1920x1080, 30fps CFR, -g 30, yuv420p, no audio — the shape the
renderer seeks reliably (long-GOP and VFR sources render black or frozen). The
grade is baked in with ffmpeg because CSS filters on <video> do not reach the renderer.

looks (ffmpeg chains, matching ev1_treat.py's still looks):
  natural  slight contrast           mono   hard B&W            teal  teal shadows / warm highs
  warm     amber sepia               cold   blue night grade    archive  keeps colour, lifts grain+vignette
--zoom >1 crops tighter around --focus (a punch-in baked in, for when the source is wide).
--speed <1 slows (setpts), the references slow-mo their stock about half the time.
"""
import argparse, subprocess

LOOKS = {
    'natural': 'eq=contrast=1.08:saturation=1.02',
    'mono': 'hue=s=0,eq=contrast=1.38:brightness=-0.02',
    'teal': 'eq=contrast=1.14:saturation=0.78,colorbalance=rs=-0.14:gs=-0.02:bs=0.12:rm=-0.04:bm=0.04:rh=0.06:gh=0.02:bh=-0.07',
    'warm': 'eq=contrast=1.12:saturation=0.6,colorchannelmixer=.45:.70:.18:0:.35:.62:.14:0:.22:.42:.10',
    'cold': 'eq=contrast=1.15:saturation=0.7:brightness=-0.03,colorbalance=rs=-0.10:bs=0.14:rm=-0.06:bm=0.08',
    'archive': 'eq=contrast=1.10:saturation=0.9,noise=alls=9:allf=t',
}


def make(src, out, ss, dur, look='natural', speed=1.0, focus=(0.5, 0.5), zoom=1.0, grain=0, vignette=True):
    fx, fy = focus
    vf = [f'setpts=PTS/{speed}' if speed != 1 else None,
          'scale=w=1920*{z}:h=1080*{z}:force_original_aspect_ratio=increase'.format(z=zoom),
          f"crop=1920:1080:(in_w-1920)*{fx}:(in_h-1080)*{fy}",
          'setsar=1', LOOKS[look],
          f'noise=alls={grain}:allf=t' if grain else None,
          'vignette=angle=PI/4.5' if vignette else None,
          'fps=30', 'format=yuv420p']
    vf = ','.join(v for v in vf if v)
    need = dur * speed + 0.2
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{ss}', '-t', f'{need}', '-i', src,
                    '-vf', vf, '-t', f'{dur}', '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
                    '-g', '30', '-keyint_min', '30', '-fps_mode', 'cfr', '-color_range', 'tv', '-colorspace', 'bt709',
                    '-color_primaries', 'bt709', '-color_trc', 'bt709', out], check=True)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--ss', type=float, required=True); ap.add_argument('--dur', type=float, required=True)
    ap.add_argument('--look', default='natural'); ap.add_argument('--speed', type=float, default=1.0)
    ap.add_argument('--focus', default='0.5,0.5'); ap.add_argument('--zoom', type=float, default=1.0)
    ap.add_argument('--grain', type=int, default=0)
    a = ap.parse_args()
    make(a.src, a.out, a.ss, a.dur, a.look, a.speed, tuple(map(float, a.focus.split(','))), a.zoom, a.grain)
    print('wrote', a.out)
