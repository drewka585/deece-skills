# DeeCe Skills

Claude Code skills built at [DeeCe Digital](https://deecedigital.com). Each one is a
process we actually run, not a demo: design and build a page, verify it in a real
browser, strip AI tells out of a draft, generate media on the cheapest capable model,
tear down and replicate motion graphics, run a YouTube episode end to end.

## Install

```
npx skills add drewka585/deece-skills
```

Or clone and copy what you want into `.claude/skills/` in your own project, or
`~/.claude/skills/` to have it everywhere.

## The skills

| Skill | What it does |
|---|---|
| [`premium-web`](skills/premium-web/SKILL.md) | Design and build a premium website, landing page or UI screen the DeeCe way: pull real references first (styles.refero.design design systems, 21st.dev components, collectui.com motion shots, the Dribbble teardown library), derive tokens from them plus the brand, pick a scroll-craft page grammar and signature move, reuse ui-library / 21st.dev components before writing, and verify by scrolling. Use when Drew says "build a website", "landing page", "make this page look better / premium / less AI", "website inspiration", "what does refero have for X", "find a component on 21st.dev", "tear down this dribbble shot", "what is on collect ui for X", or starts any new UI build. |
| [`scroll-craft`](skills/scroll-craft/SKILL.md) | Build a premium, scroll-driven interactive landing page for any business: a service company, a physical product, a food brand, a drink brand. Scroll becomes the timeline. Video scrubs frame by frame under the wheel, sections pin and advance, rails pan sideways, headlines assemble line by line, the page ground shifts colour as you travel, and the pointer moves things that are not scrolling. Interviews the human first (their vibe, their journey, one unbroken world or distinct scenes, and what assets they already own), then picks a page grammar and a signature move so no two builds share a skeleton, generates photoreal assets through kie.ai or builds from the user's own footage and photos, writes real semantic HTML on a design-system floor, and verifies the result by screenshotting its own scroll. Use for "scrollytelling", "scroll animation site", "a site where scrolling plays a video", "Apple-style landing page", "3D scroll world", "interactive landing page", "make my brand a scroll experience", "make it feel different", "this looks like a template", "a unique scroll site", or any request for a site that should feel like an experience rather than a document. |
| [`canvas-ui`](skills/canvas-ui/SKILL.md) | Add Canvas UI creative effects (WebGL + html-in-canvas wrappers like Liquid, Glass, Shatter, Asciify, ASCII Object) to a frontend project. Use when Drew asks for a hero effect, page transition, cursor effect, "make this landing page feel premium", a 3D object render (GLB/SVG/image), or names a Canvas UI component. Covers registry setup, install commands, browser support and the graceful fallback. |
| [`test-improve`](skills/test-improve/SKILL.md) | Verify visual/UI work in a real browser before calling it done — render at desktop and mobile, catch console errors, overflow, broken images and clipped text, look at the screenshots, fix what's wrong, and loop until clean. Use when Drew says "/test-improve", "test improve", "check it looks right", "verify the page", or before shipping ANY change to a page, component, email template, or rendered PDF/HTML. |
| [`no-ai-slop`](skills/no-ai-slop/SKILL.md) | Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. Use when the user wants a draft clearer, more direct, more opinionated, or less AI-sounding, or asks whether writing reads as AI. |
| [`generate`](skills/generate/SKILL.md) | Generate images and videos via AI model APIs. Routes to the cheapest capable model, quotes cost before any paid video run, and files every output flat into generations/ with a prompt log. Use when Drew says /generate, generate an image, generate a video, make a thumbnail, create a key visual, mock up a graphic, animate this, image for the deck/newsletter/landing page, or asks for a picture or clip of anything. |
| [`mg-teardown`](skills/mg-teardown/SKILL.md) | Tear down the motion graphics in a YouTube video (measure timing/easing/layout from native-fps frames) and replicate them as reusable DeeCe-branded Hyperframes beats through the spec-bound comparison gate. Use when Drew says "tear down this video's MGs", "replicate that style", or wants a new library beat derived from a real video. |
| [`video-edit-caption-pipeline`](skills/video-edit-caption-pipeline/SKILL.md) | Route DeeCe talking-head editing, audio sync, storyboard-first motion graphics, captions, and final QA. |
| [`youtube-content-pipeline`](skills/youtube-content-pipeline/SKILL.md) | Route and operate DeeCe Digital's packaging-first personal YouTube workflow from idea through verified schedule. |

## How these are meant to be used

Most of them chain. A page goes `premium-web` to pull real references and set tokens,
`scroll-craft` to give the page a grammar rather than a stack of sections, `canvas-ui`
if it needs a WebGL moment, then `test-improve` before anyone calls it done. Anything a
human will read goes through `no-ai-slop` first. Nothing visual ships until
`test-improve` is clean at desktop and mobile with the screenshots actually read.

## Updating

These are generated from a private workspace by `skills_publish.py`, which refuses to
publish anything containing a client name, a credential or a machine path. If a skill
you expect is missing, that is why.
