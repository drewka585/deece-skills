---
name: canvas-ui
description: Add Canvas UI creative effects (WebGL + html-in-canvas wrappers like Liquid, Glass, Shatter, Asciify, ASCII Object) to a frontend project. Use when Drew asks for a hero effect, page transition, cursor effect, "make this landing page feel premium", a 3D object render (GLB/SVG/image), or names a Canvas UI component. Covers registry setup, install commands, browser support and the graceful fallback.
---

# Canvas UI

Open-source library of 33 canvas/WebGL effect components that wrap live, interactive HTML. Framework agnostic (React, Vue, Svelte, Solid, Preact, vanilla TS). Distributed as a shadcn registry, so components are copied into the project as source, not installed as a dependency.

Site: https://canvasui.dev — Repo: https://github.com/DavidHDev/canvas-ui — License: MIT + Commons Clause (free in commercial projects, cannot resell the library itself).

## When to use

- Landing pages and client mockups that need a distinctive hero or scroll effect.
- Cursor-driven effects over real UI (Liquid, Glass, Magnify, Frost, Ripple).
- Rendering a GLB/glTF model, SVG, or image as an object (ASCII Object, Glass Object, Particle Object, Dithered Object, Liquid Object) — these are plain three.js and work in every browser.

Do not use for ordinary UI primitives (buttons, tables, forms) — that is `ui-ux-pro-max` + shadcn.

## Pick a component

Read `references/components.md` for the full table of 33 components with npm deps and one-line descriptions. Pick by effect, then append the framework suffix to the base name: `-react`, `-vue`, `-svelte`, `-solid`, `-preact`, `-vanilla`.

## Install into a project

1. Register the registry in the project's `components.json`:

```json
{
  "registries": {
    "@canvas-ui": "https://canvasui.dev/r/{name}.json"
  }
}
```

2. Add the component:

```bash
npx shadcn@latest add @canvas-ui/liquid-react
```

Source lands in `components/canvasui/` (or `src/lib/components/canvasui/` for Svelte). Any npm deps listed in the table (`three` for the object components) install automatically.

3. Wrap the content. Everything inside stays live and interactive:

```jsx
<Liquid rainbow style={{ height: 480 }}>
  <YourContent />
</Liquid>
```

All props are typed with sensible defaults, so start with no props and tune after.

## MCP server (optional, per project)

Lets the agent browse the registry and install components itself. Run inside the project, then restart Claude Code:

```bash
npx shadcn@latest mcp init --client claude
```

Then prompt with "show me the components in the @canvas-ui registry" / "add liquid from @canvas-ui to the hero". Troubleshoot with `/mcp`. This is per-project — it writes to that project's `.mcp.json`, not to the workspace root.

## Browser support — read before promising a client

- The page-wrapping effects use the experimental **html-in-canvas** API, which needs Chrome with `chrome://flags/#canvas-draw-element` enabled, or an [origin trial token](https://canvasui.dev/docs) registered for the deployed domain. canvasui.dev itself uses an origin trial, which is why it looks right in stock Chrome.
- Without support, components fall back automatically: most render a WebGL overlay version, the rest render the plain HTML. No errors either way, but **the effect Drew approves in Chrome-with-flag is not what a Safari visitor sees**. Register the origin trial for the production domain, or screenshot the fallback and show that too.
- The five object components (ASCII / Glass / Particle / Dithered / Liquid Object) are pure three.js and render identically everywhere. Prefer them when cross-browser fidelity matters.

## Framework versions

React 19, Vue 3.5, Svelte 5, Solid 1.9, Preact 10. TypeScript expected — components ship as typed source. No Tailwind requirement.

## Verification

Any page using these is visual work, so it is not done until `/test-improve` comes back clean at desktop and mobile, with the screenshots actually read. Check the fallback path too: load the page in Safari or a Chrome profile without the flag.
