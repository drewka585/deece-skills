---
name: test-improve
description: Verify visual/UI work in a real browser before calling it done — render at desktop and mobile, catch console errors, overflow, broken images and clipped text, look at the screenshots, fix what's wrong, and loop until clean. Use when Drew says "/test-improve", "test improve", "check it looks right", "verify the page", or before shipping ANY change to a page, component, email template, or rendered PDF/HTML.
---

# /test-improve — never ship visual work on trust

The failure this prevents: an agent edits CSS, sees no error, says "done", and the
page is broken on mobile. Nothing in a normal edit loop ever *looks* at the result.
This skill closes that loop — render it, inspect it, fix it, re-render, and only
surface the work once it actually passes.

**Rule: if a change touched anything a human will look at, it is not done until a
`visual_check` run comes back clean and you have read the screenshots.** Saying
"should look fine" is the exact failure mode this exists to kill.

## The two halves

`execution/visual_check.py` finds what a machine can prove:

- console errors and uncaught exceptions
- failed requests (4xx/5xx, broken fetches)
- horizontal overflow, with the offending selectors
- broken images
- text clipped by its own container

**You** judge what a machine can't: hierarchy, spacing, whether the headline is
too big, whether it reads right, whether it matches the brand. That means you
must actually **Read the screenshot PNGs** — the report alone is not inspection.

## Procedure

### 1. Get the thing running

Local work needs a dev server. Start it in the background, wait for it to answer,
and note the port. If the project is already deployed and the change is live, run
against the real URL instead.

Start it **detached**, or it gets reaped between tool calls:

```bash
nohup npm run dev -- -p <port> > /tmp/lane<port>.log 2>&1 & disown
```

A dead server makes the next run report a wall of ERR_CONNECTION_REFUSED and console
errors that look exactly like a broken page. Before fixing anything, read the server
log — clean 200s followed by nothing is a reaped process, not a defect.

### 2. Run the check

```bash
python3 execution/visual_check.py --url http://localhost:3000 --url http://localhost:3000/pricing
```

Defaults to desktop (1440×900) and mobile (390×844). Useful flags:

| Flag | Use |
|---|---|
| `--viewport desktop\|mobile\|both` | narrow the run — **one value, not repeatable.** `--viewport desktop --viewport mobile` runs ONLY mobile, silently, and the report looks like a complete pass. Use `--viewport both`. |
| `--full-page` | whole scroll height, not just the fold |
| `--scroll-sweep N` | N viewport frames at evenly spaced scroll positions (`<prefix>--sweep-NN.png`), each probed for horizontal overflow. **Mandatory for parallax, pinned, stacked-card or reveal-on-scroll pages**: a full-page capture flattens every scroll state into one frame and cannot show a layer that jumps or a reveal that never fires. Read the frames. Manifest routes take `"scrollSweep": N`. |
| `--flow flows/x.json` | click/fill through a real interaction. **Mandatory for tabs, filters, segmented controls and disclosures**: the gate renders a route as it loads and checks that frame, so a control that works on load and breaks on its second option passes silently. Put an `expectPresent` on the clicked control's own selected marker (`[aria-pressed="true"]`), anchored inside its container, so a click that never landed fails instead of quietly re-shooting the default state. A `--flow` file is a bare array of steps. The `{"steps": [...]}` object form belongs only inside a manifest route's `"flows"`, and passing it on the flag raises an AttributeError. Manifest routes take `"flows": [...]`. |
| `--out <dir>` | pin the output location |
| `--manifest execution/manifests/<app>.json` | run a whole app: every route, both themes, role fixtures, expected final URLs |
| `--base-url http://localhost:32NN` | point a manifest at a lane instead of its default host |
| `--only <path>` | narrow a manifest run — repeatable, but **matches the route's PATH (`/dashboard`), not its name.** A filter matching nothing produces an empty report, zero screenshots, and **exit 0** — which reads as a clean pass. Confirm the run actually shot the routes you named. |
| `--theme light\|dark\|both\|none` | force the theme and assert `<html class="dark">` actually took |
| `--expect-url <path\|re:...>` | opt-in, `--url` mode: fail if the final URL isn't this |

**For an auth-gated app, use the manifest.** A bare `--url` run follows the login
redirect, screenshots `/login`, gets a 200 and reports **clean** — the gate passes
having verified nothing. `--expect-url` turns that into a named failure, and the
manifest sets it on every route for you. Manifests also carry role fixtures whose
storage states must exist: a missing one is reported as a defect, never a skip.
Fixtures expire — re-mint the portal's with
`execution/portal_auth_state.py --base-url <url> --email <you> --out <path>`.
The storage state is **base-url-scoped**: a fixture minted against localhost and
replayed against production lands on `/login`. Re-mint per host, and let
`expectUrl` catch it when you forget.

Exit code is 1 when defects were found, 0 when clean. Report + screenshots land
in `.tmp/visual_check/<timestamp>/`.

Flow file for interactive states (modals, forms, logged-in views):

```json
[{"action": "fill", "selector": "#email", "value": "test@example.com"},
 {"action": "click", "selector": "button[type=submit]"},
 {"action": "wait", "ms": 800},
 {"action": "screenshot", "label": "after-submit"}]
```

### 3. Look at the screenshots

Read every PNG the run produced. Check the machine can't-see list:

- Does the mobile shot look like a designed mobile page or a squeezed desktop one?
- Headline size, line length, and spacing sane at both widths?
- Anything overlapping, misaligned, or touching the viewport edge?
- Do the CTAs read as CTAs?
- Empty/loading states — did you screenshot a spinner and call it a page?

Also apply Drew's standing copy rules to anything client-facing on screen:
**no em/en dashes, no semicolons**, and bare URLs rather than wrapped links.

### 4. Fix and loop — cap at 3 rounds

Fix everything found, re-run, repeat. **Stop at 3 rounds.** If it is still not
clean, stop and report what remains with the screenshot paths rather than burning
tokens grinding at it. Three rounds that converge is a fix; five that don't is a
design problem Drew needs to see.

### 5. Report

State the final run's result explicitly, with numbers:

> Clean at desktop + mobile after 2 rounds. Round 1: mobile horizontal overflow
> (`.hero-grid` +112px) and 1 broken image. Both fixed. Screenshots:
> `.tmp/visual_check/20260725-141200/`

If anything is still failing, say so plainly and do not describe the work as done.

## Scope

Run it on: web pages, dashboards, landing pages, admin views, React/Next components,
rendered HTML resources and PDF-source HTML, email templates (desktop + mobile),
and any Remotion/Hyperframes still frame that renders to HTML first.

Skip it on: pure backend/API changes, scripts, data pipelines, config. Rendering
those proves nothing.

## Chaining

- Pairs with `ui-ux-pro-max` — that skill decides how it *should* look, this one
  proves it *does*.
- Run before `/end`, not after. Unverified visual work is the worst thing to leave
  in a handoff, because the next session inherits it believing it works.
- When a defect turns out to be a repeat (same overflow bug, same breakpoint),
  that is a `/calibrate` item — write the rule into the project's docs so the next
  session avoids it instead of rediscovering it.
