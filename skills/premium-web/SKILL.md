---
name: premium-web
description: >-
  Design and build a premium website, landing page or UI screen the DeeCe way: pull real references first (styles.refero.design design systems, 21st.dev components, collectui.com motion shots, the Dribbble teardown library), derive tokens from them plus the brand, pick a scroll-craft page grammar and signature move, reuse ui-library / 21st.dev components before writing, and verify by scrolling. Use when Drew says "build a website", "landing page", "make this page look better / premium / less AI", "website inspiration", "what does refero have for X", "find a component on 21st.dev", "tear down this dribbble shot", "what is on collect ui for X", or starts any new UI build.
---

# premium-web

The wrapper for `directives/premium_website_design.md`. Read that directive in full
before Phase 1; this file is the checklist and the commands.

## Do, in order

1. **Brief.** Product, audience, pages, brand assets, references named element by element.
2. **Pull references.** Never design from memory.
   ```bash
   python3 execution/refero_styles.py search "finance"                 # north-star lines per site
   python3 execution/refero_styles.py get <uuid> --sheet               # design.md + tokens.css + tailwind preset + preview sheet
   python3 execution/refero_styles.py similar <uuid>
   python3 execution/twentyfirst_dev.py search "hero with scroll-driven card"
   python3 execution/twentyfirst_dev.py sheet <demo_id>                # desktop + mobile screenshots of the live demo
   python3 execution/collectui.py categories --grep hero               # ~200 category slugs
   python3 execution/collectui.py list landing-page --limit 20         # curated shots, mostly video
   python3 execution/collectui.py sheet <post_id>                      # 4x4 contact sheet of the motion
   python3 execution/dribbble_teardown.py <shot url>                   # contact sheet of the shot video
   ```
   READ every sheet and screenshot. Read `directives/references/design_inspiration/README.md`
   first; four Dribbble shots and two Refero finance systems are already torn down there.
3. **Design system.** Brand tokens win; Refero + `ui-ux-pro-max` fill the rest; apply the
   scroll-craft taste floor (`.claude/skills/scroll-craft/references/taste.md`) and its
   refuse list. Write `design-system/MASTER.md` + `REFERENCES.md` in the project.
4. **Structure.** scroll-craft Step 0-2: interview -> `BRIEF.md`, ONE of eight grammars,
   feeling curve + one peak, a signature move, the fingerprint gate against
   `websites/scrollcraft/FINGERPRINTS.md`, then the act/device score.
5. **Components.** `ui-library/` first; then `twentyfirst_dev.py prompt <demo_id>
   --library` (needs `API_KEY_21ST` in `.env`, free at https://21st.dev/mcp); then
   `canvas-ui`; write last. Swap hardcoded accents for tokens.
6. **Motion.** scroll-craft engine (`data-sc-*` on real HTML) for scroll-driven pages,
   `scroll-film-studio` for a full film, reveal-on-enter for ordinary pages. Transform /
   opacity / clip-path only. User-paced, never autoplay or scroll-jack.
7. **Verify.** `/test-improve` desktop + mobile, `--scroll-sweep 10` read frame by frame,
   the scroll-craft harness for dead scroll and composited contrast, the feel check,
   a hard scroll to top and bottom, tab order. Say what a green run does not cover.
8. **File it.** New reference -> teardown README. New component -> ui-library README.
   Shipped build -> FINGERPRINTS.md row.

## Never
- Design from memory, or from adjectives.
- Ship the same six sections every AI page has (feature-card grid, 01/06 counters, scroll
  cue, gradient text, aurora purple, pill everything).
- Report visual work done without having read the screenshots.
