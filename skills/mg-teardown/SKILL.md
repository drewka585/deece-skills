---
name: mg-teardown
description: Tear down the motion graphics in a YouTube video (measure timing/easing/layout from native-fps frames) and replicate them as reusable DeeCe-branded Hyperframes beats through the spec-bound comparison gate. Use when Drew says "tear down this video's MGs", "replicate that style", or wants a new library beat derived from a real video.
---

# MG Teardown

Follow **`directives/mg_teardown.md`** — it is the SOP and carries every earned gotcha. This
skill is the entry point, not a substitute for reading it.

## Invocation

`/mg-teardown <youtube_url> [timestamps or "whole video"] [notes]`

## The short loop (details + tolerances in the directive)

1. **Download verified**: `execution/mg_reference_study.py "<url>" --times 0` — aborts on <720p;
   read the measured fps from `info.json` (23.976 is common; never assume 30).
2. **Locate + select** beats (reusability, type diversity, feasibility gate). Log all beats,
   rejects with reasons.
3. **Measure** from native-fps ffmpeg frame runs; Claude reads frames; easing named from
   %-at-25/50/75; unresolvable numbers recorded as `null`/inequality, never invented.
4. **Spec** per beat → `.tmp/mg_teardown/specs/` (schema enforced by `mg_beat_compare.py`'s
   validator: `source{video_id,start_s,end_s}`, every element has an `onset_s` key). Record the
   IP substitution list — distinctive assets swapped for DeeCe equivalents, never traced.
5. **Build** via Sonnet builders: own folder, `"status": "draft"`, vendored GSAP, static layout
   check before motion, render ONLY via `execution/hyperframes_render_beat.py`.
6. **Compare**: `execution/mg_beat_compare.py --spec <spec> --render <webm> --out-dir ...` —
   spec-bound attempts, real alpha gate. Builders self-iterate (≤8 rounds, one causal change
   each); the MAIN SESSION alone accepts.
7. **Accept**: flip meta to `"candidate"`, README Candidates row, commit spec + manifest + pair
   sheets to `directives/references/mg_teardown/`, demo-render at `--quality high`. Keep source
   MP4s until that commit lands.

## Hard rules

- Never pass `durationSeconds` in `--variables`; never call raw `hyperframes render`.
- WebM alpha only reads truly via `-c:v libvpx-vp9` decode.
- No array composition variables — pipe-delimited strings.
- Max 6 beats built per batch; halt and ask Drew if 2 beats exhaust their round caps.
- Drew signs off before any candidate is promoted to the library Inventory.
