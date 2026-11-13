# DeeCe Skills

Claude Code skills I built for my own work and still use every week. Each one is a process
I actually run, not a demo. Design and build a page, check it in a browser, strip AI tells out of a draft,
generate media on the cheapest capable model, and edit video.

## Install

```
npx skills add drewka585/deece-skills
```

Or clone the repo and copy the skills you want into `.claude/skills/` in your own project,
or into `~/.claude/skills/` to have them everywhere.

## The skills

| Skill | What it does |
|---|---|
| [`premium-web`](skills/premium-web/SKILL.md) | Design and build a premium website, landing page or UI screen the DeeCe way. |
| [`scroll-craft`](skills/scroll-craft/SKILL.md) | Build a premium, scroll-driven interactive landing page for any business. |
| [`canvas-ui`](skills/canvas-ui/SKILL.md) | Add Canvas UI creative effects (WebGL + html-in-canvas wrappers like Liquid, Glass, Shatter, Asciify, ASCII Object) to a frontend project. |
| [`test-improve`](skills/test-improve/SKILL.md) | Verify visual/UI work in a real browser before calling it done. |
| [`no-ai-slop`](skills/no-ai-slop/SKILL.md) | Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. |
| [`generate`](skills/generate/SKILL.md) | Generate images and videos via AI model APIs. |
| [`mg-teardown`](skills/mg-teardown/SKILL.md) | Tear down the motion graphics in a reference video by measuring timing, easing, stagger and layout from native frame rate frames, write each beat up as a JSON spec, then rebuild it as a reusable HTML and GSAP beat (rendered with HyperFrames or any headless browser renderer) and check the render against the source frame by frame. |
| [`editor-v1`](skills/editor-v1/SKILL.md) | Edit a talking-head recording into a 16:9 documentary-style video in the EDITOR V1 style. |

## How these are meant to be used

Most of them chain. A page goes `premium-web` to pull real references and set tokens,
`scroll-craft` to give the page a grammar rather than a stack of sections, `canvas-ui`
if it needs a WebGL moment, then `test-improve` before I call it done. Anything a person
will read goes through `no-ai-slop` first. Nothing visual ships until `test-improve` is
clean at desktop and mobile with the screenshots actually read.

## Video editing pack

Two skills for editing video with Claude Code. Both render on your own computer with free
tools.

`editor-v1` turns a talking head recording into a fast 16:9 documentary style edit. Every
line gets found footage, photos or rebuilt screens, word by word captions, a synthesised
sound kit and a music bed, all rendered from HTML with HyperFrames. After installing, run
`bash scripts/doctor.sh` from the skill folder. It sets up a private Python environment,
the renderer and GSAP, and tells you how to install anything it cannot add itself (Node,
ffmpeg, Python, Chrome). Re-run it until it prints "All set".

`mg-teardown` measures the motion graphics in a reference video frame by frame, writes
each beat up as a spec and rebuilds it as a reusable HTML animation that is checked against
the source. It needs yt-dlp and ffmpeg.

Install only the pack:

```
npx skills add drewka585/deece-skills --skill editor-v1 mg-teardown
```

## Updating

I generate these from a private workspace with a script that refuses to publish anything
containing a client name, a credential or a machine path. If a skill you expect is missing,
that is why.
