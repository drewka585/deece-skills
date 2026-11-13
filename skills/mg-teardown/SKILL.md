---
name: mg-teardown
description: >-
  Tear down the motion graphics in a reference video by measuring timing, easing, stagger and
  layout from native frame rate frames, write each beat up as a JSON spec, then rebuild it as a
  reusable HTML and GSAP beat (rendered with HyperFrames or any headless browser renderer) and
  check the render against the source frame by frame. Use when the user says "tear down this
  video's motion graphics", "replicate that MG style", "how does this channel animate its
  graphics", or wants a new animation beat derived from a real video instead of invented.
---

# Motion graphics teardown and replication

The point is measurement, not vibes. A beat is accepted only when its render matches the
numbers taken from the source frames.

**Needs:** `yt-dlp`, `ffmpeg` and `ffprobe` on PATH. For the build step, Node 18+ and a
HTML to video renderer. HyperFrames (`npx hyperframes`) is what this was built on, and any
headless Chrome capture works. GSAP is the animation library. Download it into the beat's
own folder rather than loading it from a CDN at render time.

## 1. Verified download

```bash
mkdir -p mg/<id> && cd mg/<id>
yt-dlp -f "bv*[height>=1080]+ba/b[height>=720]" -o source.mp4 "<url>"
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,nb_frames -of json source.mp4 > info.json
```

Read `info.json` before anything else. Below 720p, stop and update yt-dlp. A silent low
resolution fallback ruins every measurement after it.

**Frame rate trap:** web video is often 23.976 fps (24000/1001), not 30. Frame N sits at
`start + N / fps_measured`. Never assume 30.

## 2. Locate the beats

Pull one frame every few seconds plus the transcript, and log every motion graphics beat to
`beats.json` as `{start_s, end_s, description, script_role, mg_type}`. Tag the script role
(hook, rehook, point, payoff), because most channels map graphics one to one onto script
structure.

**Feasibility gate before any build time:** reject beats that need a true 3D camera move,
dense particle simulation, hand drawn frame animation or a plugin look that CSS and GSAP
cannot express. Log each reject with its reason.

## 3. Measure from native frame rate frames

```bash
ffmpeg -ss <start> -t <dur> -i source.mp4 -vsync 0 frames/beat01_%04d.png
```

Sampling at a tenth of a second cannot resolve a 0.3 second entrance. Extract every frame
around each entrance and measure per element:

- `onset_s` relative to the beat start. This is what encodes the stagger rhythm.
- `exit_onset_s`
- `entrance`: `duration_s`, `travel`, `easing_name`, `pct_at_25_50_75`, `stagger_offset_s`
- `settled_bbox_pct` as `{x, y, w, h}`, plus `anchor`, `z`, opacity and blur keyframes
- `confidence` per element

Name the easing from the measured percentage of travel or opacity at 25, 50 and 75 percent of
the duration:

| Easing | 25% | 50% | 75% |
|---|---|---|---|
| linear | 25 | 50 | 75 |
| quad out | 44 | 75 | 94 |
| cubic out | 58 | 88 | 98 |
| quad in | 8 | 31 | 56 |

A number you cannot resolve is recorded as `null` with a note, or as an inequality. Never
invent one. Duplicate encoded frames widen the uncertainty band, so say so in the note.

## 4. Write the spec

One JSON per beat, `specs/<video_id>__beatNN.json`. It is the design authority for the build
and the comparison. Required fields:

- `source`: `video_id`, `start_s`, `end_s`, `url`, `resolution`, `fps`
- `elements[]`, each with an `onset_s` key (a number or an honest `null`)
- `timebase`, `layering`, `feasibility` (`verdict`, `reason`)
- `ip`: `distinctive_assets` and `substitutions`
- the evidence frame numbers and the exact extraction command

**IP rule:** replicate structure, never assets. Timing, easing family, layout grid, type scale
and palette as an HSL family carry over. Icon glyphs, logos, characters, real screenshots and
signature motifs get substituted with your own brand equivalents, never traced. The spec
records both lists.

## 5. Build the beat

One folder per beat with `index.html`, local fonts, GSAP saved beside it and a `meta.json`
holding `"status": "draft"` and `"source_spec"`.

- **Static layout first.** Check the settled frame against `settled_bbox_pct` within 3 percent
  before animating anything.
- Expose the copy, colours and fonts as variables so the beat is reusable. Keep variable types
  simple (string, number, colour, boolean). Pass lists as pipe delimited strings.
- Render transparent overlays to WebM with alpha. Render opaque full frame scenes to MP4. The
  VP9 WebM path can corrupt opaque scenes with fixed black rectangles and smeared colour
  blocks. When you see block corruption, render the same frame to MP4 first before touching
  the CSS.

## 6. Compare against the source

Extract the render's frames at the spec onsets and put them beside the source frames:

```bash
ffmpeg -c:v libvpx-vp9 -i render.webm -vf "fps=<source_fps>" render/%04d.png
ffmpeg -i frames/beat01_0012.png -i render/0012.png -filter_complex hstack pair_0012.png
```

**Alpha trap:** ffmpeg's native VP9 decoder silently drops WebM alpha and reports `yuv420p`.
Only `-c:v libvpx-vp9` decodes the real alpha. Use it for every frame check on a WebM or you
will find missing alpha that is really there.

Flatten transparent frames over a checkerboard before judging them. An opaque background then
reads as a solid slab, which is the failure you are looking for.

**Tolerances:** onset within 0.1 s for medium or better confidence, entrance duration within
2 source frames, settled box within 3 percent, stagger order exact. Judge low confidence
elements on feel and order. One causal change per round, at most 8 rounds per beat, and stop
after 2 rounds that do not improve.

## 7. Accept

Flip `status` to `"candidate"`, record which attempt was accepted, and keep the spec and the
accepted pair sheets beside the beat as evidence. Keep the source download until that
evidence is saved.

## Gotchas worth not rediscovering

- A study brief that asks for video level stats (cuts per minute, captions yes or no) gets the
  wrong answer. Spell out the section 3 fields in any brief you hand to another agent.
- A spec whose onsets are all honestly `null` is valid. Cadence driven beats like word
  cascades often are. Pass the compare points explicitly.
- `document.fonts.ready` resolves at once if the font was never requested. It is not a
  measurement gate. Prefer layouts that need no measuring, such as a `clip-path: inset()`
  tween over a measured width tween.
- A GSAP tween on an element that also carries a CSS `transform` fights it. Use `fromTo` and
  drop the CSS transform.
- A glow in the same colour as the text floods the letterforms. Judge captions and chips at
  full resolution, not thumbnails.
- `backdrop-filter` plus `mask-image` ripples in headless Chromium. Build edge blurs as self
  contained blurred or gradient layers.
- Gradient clipped text (`background-clip: text` with a transparent colour) renders solid
  black while a CSS `filter` tween runs on it. Tween blur and opacity on an outer wrapper and
  keep the clipped text static.
- `em` spacing on an inline block resolves against the inherited size when the font size is
  set on a different element, so words render jammed together. Use flex `gap` on the line
  container instead.
