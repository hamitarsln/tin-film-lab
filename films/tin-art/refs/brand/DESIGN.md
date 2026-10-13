---
version: alpha
name: Tin Computer
description: Warm ink-on-paper workspace with a terminal-cyan agent surface; monospace chrome, Funktional Grotesk content.
colors:
  # Ink & paper foundation — web/src/app/globals.css :root (34-41)
  ink-void: "#080808"
  ink-void-hover: "#525252"
  paper: "#F5F1E6"
  paper-warm: "#ECE6D5"
  paper-pale: "#F9F7F0"
  paper-light: "#FEFDFB"
  paper-deep: "#B9AE98"
  paper-ink: "#78715F"
  # Accents — globals.css :root (43-57)
  butter: "#EBDE9A"          # decisions badge / "flat" metric / warning
  blossom: "#F3C6D5"         # "down" metric / rose
  blossom-deep: "#E4A7BC"
  hot-rose: "#E8305A"        # alert
  sky: "#A3CAD8"
  sky-deep: "#7FB1C4"
  terminal-blue: "#90D7E4"   # live agent chat surface (reserved)
  terminal-blue-deep: "#63AEBF"
  primary-green: "#66DC9D"   # "up" metric / success
  primary-green-deep: "#2FA069"
  # Hairlines — globals.css :root (59-62)
  rose-line: "#E5B8B8"
  rose-line-soft: "#EED2D4"
  line-neutral: "rgba(0,0,0,0.18)"
  line-strong: "rgba(0,0,0,0.35)"
  # Base UI — globals.css @theme (69-72)
  background: "#ffffff"
  foreground: "#1c1c1c"
  muted: "#888888"
  border: "#e5e5e5"
  # Marketing lime accent scale, OKLCH hue 120° — globals.css @theme (77-90)
  lime-pale: "oklch(0.983 0.028 120)"
  lime-subtle: "oklch(0.965 0.055 120)"
  lime-wash: "oklch(0.947 0.082 120)"
  lime-border: "oklch(0.925 0.108 120)"
  lime: "oklch(0.805 0.193 120)"
  lime-hover: "oklch(0.703 0.205 120)"
  lime-deep: "oklch(0.512 0.149 120)"
  lime-cta: "oklch(0.90 0.22 120)"
  lime-ink: "oklch(0.373 0.096 120)"
typography:
  # Funktional Grotesk, self-hosted @font-face weights 300/400/500 — globals.css (5-27)
  # families: --font-sans / --font-ui = "Funktional Grotesk", system-ui, sans-serif
  #           --font-mono = ui-monospace, SFMono-Regular, Menlo, "JetBrains Mono", monospace
  display:
    fontFamily: Funktional Grotesk
    fontSize: 22px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.015em
  ident-name:
    fontFamily: Funktional Grotesk
    fontSize: 19px
    fontWeight: 700
  body:
    fontFamily: Funktional Grotesk
    fontSize: 13.5px
    fontWeight: 400
    lineHeight: 1.58
  body-sm:
    fontFamily: Funktional Grotesk
    fontSize: 11.5px
    fontWeight: 400
  header-mono:          # UPPERCASE structural chrome (panel headers)
    fontFamily: ui-monospace
    fontSize: 11px
    fontWeight: 500
    letterSpacing: 0.14em
  metric-mono:          # status-strip / KPI cells; tabular-nums
    fontFamily: ui-monospace
    fontSize: 11px
    fontWeight: 600
    letterSpacing: 0.08em
  label-caps:           # badges / chips / eyebrows
    fontFamily: ui-monospace
    fontSize: 10px
    fontWeight: 500
    letterSpacing: 0.1em
rounded:
  none: 0px            # default chrome — sharp corners (scrollbars set to 0)
  sm: 4px              # inline code
  md: 8px              # pre blocks
  pill: 999px          # status dots / pills only
spacing:
  # Tailwind v4 defaults (4px base) elsewhere; named chrome values below
  chrome-row: 28px     # panel / header row height
  card-pad: 17px       # feed card vertical padding (20px horizontal)
  cell-pad: 5px        # metric cell vertical padding (12px horizontal)
components:
  badge-status:        # autonomy "STANDARD" pill — web/src/components/autonomy/autonomy.module.css
    backgroundColor: transparent
    textColor: "rgba(8,8,8,0.68)"
    typography: "{typography.label-caps}"
    height: 22px
    padding: 0 8px
  badge-decisions:     # yellow "N DECISIONS" chip — newsfeedColumn.module.css
    backgroundColor: "{colors.butter}"
    textColor: "{colors.ink-void}"
    typography: "{typography.label-caps}"
    height: 20px
    padding: 0 9px
  feed-card:           # nativeFeed.module.css .card
    backgroundColor: "{colors.paper-light}"
    textColor: "rgba(8,8,8,0.84)"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: 17px 20px
  filter-chip:         # nativeFeed.module.css .filterChip (active state = inverted)
    backgroundColor: "{colors.paper-light}"
    textColor: "{colors.paper-ink}"
    typography: "{typography.label-caps}"
    height: 24px
    padding: 0 10px
  avatar:              # nativeFeed.module.css .avatar
    backgroundColor: "{colors.ink-void}"
    textColor: "{colors.paper-light}"
    size: 32px
  terminal-surface:    # dashboard.module.css .terminal — the live agent panel
    backgroundColor: "{colors.terminal-blue}"
    textColor: "{colors.ink-void}"
    typography: "{typography.header-mono}"
  status-strip:        # statusStrip.module.css .strip — black bottom bar
    backgroundColor: "{colors.ink-void}"
    textColor: "{colors.paper}"
    typography: "{typography.metric-mono}"
    height: 30px
---

## Overview

Tin Computer is one product with two surfaces, both built from the same
ink-on-paper system:

- **The terminal dashboard** — a three-panel operator view. A warm `paper`
  sidebar (project identity + task pipeline), a cyan `terminal-blue` center
  panel that is the *live agent chat*, a `paper-light` workspace viewer on the
  right, and a black `ink-void` status strip pinned to the bottom carrying KPIs
  and run state.
- **The Tin Computer home feed** — a calm, single-column feed of `paper-light`
  cards on a `paper` field, where each card is something the agent did, with
  thumbs-up / thumbs-down reactions and a yellow "N DECISIONS" chip in the
  header.

The feeling is a workbench, not an app chrome: warm matte paper, near-black ink,
hairline rules instead of shadows, and a single saturated cyan that means "the
agent is live here." Type does the heavy lifting — **Funktional Grotesk** for
anything a human reads, a **monospace** stack for the structural chrome,
metrics, and labels that frame it. Nothing is glossy; nothing floats.

## Colors

**Foundation.** Two families carry almost everything: the `ink` end
(`ink-void` #080808 for text, dark strips, and 1px frames) and the `paper` end
(`paper` #F5F1E6 for fields and the sidebar, `paper-light` #FEFDFB for cards,
`paper-warm`/`paper-pale` for subtle banding, `paper-ink`/`paper-deep` for muted
labels). Body text on light cards is `rgba(8,8,8,0.84)` — ink, never pure black,
softened so it reads as paper print.

**The terminal cyan is reserved.** `terminal-blue` (#90D7E4) is the one
high-chroma surface and it means *the live agent*. Use it only for the agent
chat / terminal panel and its composer. `terminal-blue-deep` is its scrollbar /
on-cyan element shade. Don't reach for it as a generic accent.

**Accents are semantic, not decorative.** Metric and status color follows a
fixed vocabulary:

- `primary-green` (#66DC9D) — up / success / positive delta (`primary-green-deep`
  #2FA069 for text on light).
- `blossom` (#F3C6D5) — down / negative delta (`blossom-deep` for emphasis).
- `butter` (#EBDE9A) — flat / neutral, and the "decisions" chip / soft warning.
  Use `butter-deep` (#C9A227) for small marks on light — the admin fleet's
  "viewed" dot. Plain butter is ~1.2:1 on `paper`: fine as a fill behind text,
  invisible below ~12px. Don't darken past `butter-deep` chasing contrast —
  it stops reading as yellow and turns brown.
- `hot-rose` (#E8305A) — alert / destructive only.
- `sky` / `sky-deep` — informational analytics fills.

**Marketing surfaces** use the OKLCH `lime` scale (hue 120°) as their primary
accent — `lime` for buttons/dots/bars, `lime-hover` for hover, `lime-deep` for
link/chip text, the `lime-pale → lime-wash` ramp for fills, and the off-canonical
`lime-cta` for the loudest call to action. This lime system belongs to the
public/marketing site; keep it out of the app chrome, which stays on the
ink/paper/terminal palette above.

## Typography

**Funktional Grotesk** (self-hosted via `@font-face`, weights **300 Light /
400 Book / 500 Medium**) is the content face — feed copy, card authors, the
workspace prose, identity names. It is the default `--font-sans` / `--font-ui`.
The only place it goes bold (700) is the project `ident-name`.

A **monospace** stack (`ui-monospace, SFMono-Regular, Menlo, "JetBrains Mono",
monospace`) is the *chrome* face. Everything that frames content is mono:

- **`header-mono`** — panel/section headers, 11px / weight 500 / `0.14em` /
  UPPERCASE.
- **`metric-mono`** — status-strip and KPI cells, 11px / weight 600, with
  `font-variant-numeric: tabular-nums` so figures don't jitter.
- **`label-caps`** — badges, chips, eyebrows, 10px / weight 500 / `0.1em` /
  UPPERCASE.

Rule of thumb: if a human *reads* it, it's Funktional Grotesk; if it *labels* or
*measures*, it's mono, uppercase, and letter-spaced (0.08–0.14em).

## Layout

**Dashboard** is a CSS grid: `pico | terminal | viewer` over a full-width
`status-strip` footer.

- ≥1280px — three columns ≈ **3 : 4 : 4** (pico : terminal : viewer).
- 1024–1280px — tightens to **3 : 4 : 3** (viewer narrows).
- 768–1024px — the `pico` sidebar collapses into a horizontal **TopBar**;
  layout becomes terminal : viewer ≈ 4 : 5.
- <768px — **MobileShell** stacks the surfaces; a NarrowGate guards the small
  view.

Panels share a **28px chrome row** for their headers and a 1px gap, so the grid
reads as tiled cells rather than floating cards.

**Home feed** is a single centered column of cards with a **14px** gap on a
`paper` field, each card padded **17px 20px**. The column header is the same
28px mono chrome row, right-aligned to the decisions chip.

## Elevation & Depth

The system is **flat — no drop shadows.** Depth is communicated three ways:

1. **1px hairlines.** Cards and dividers use `rose-line-soft` (#EED2D4);
   neutral rules use `line-neutral`; framed tiles and badges use a solid 1px
   `ink-void` border.
2. **Inset light seams** on dark surfaces — e.g.
   `box-shadow: inset -1px 0 0 rgba(245,241,230,0.12)` separates regions of the
   black status strip with a faint paper-colored line rather than a shadow.
3. **Background banding** — `paper` vs `paper-warm` vs `paper-light` to step
   surfaces without borders.

**Motion** (dashboard tokens): `--t-ui: 200ms` for UI state, `--t-layout: 500ms`
for layout shifts, `--t-gauge: 1000ms` for gauges, all on
`--ease: cubic-bezier(0.45, 0, 0.55, 1)`. Animation is functional (caret blink,
ticker scroll, a single fade-in), never ornamental bounce.

## Shapes

Corners are **sharp** — radius `0` is the default for panels, cards, tiles, and
even scrollbars. The only rounded exceptions:

- `rounded.sm` (4px) for inline `code`, `rounded.md` (8px) for `pre` blocks.
- `rounded.pill` (999px) strictly for small **status dots** and pill indicators
  (e.g. the autonomy state dot).

Framing is done with **1px `ink-void` borders** (identity tile, badges) — a hard
edge, not a soft one.

## Components

- **`badge-status`** — the autonomy mode pill ("STANDARD"). Transparent fill,
  semi-transparent ink text, `label-caps`, 22px tall. A 7px `pill` dot encodes
  run state: `primary-green` when running, muted ink when paused.
- **`badge-decisions`** — the feed's "N DECISIONS" chip. `butter` fill, `ink-void`
  text and 1px border, `label-caps`, 20px tall — the one warm chip that pulls the
  eye to pending decisions.
- **`feed-card`** — `paper-light` fill, `rose-line-soft` 1px border, sharp
  corners, `body` type, 17×20 padding. Variants keep the same shell: the
  onboarding card tints toward `primary-green`, the stat card uses a pale
  greenish `#eef0e4`, and storyline cards add a 2px `ink-void` top border.
- **`filter-chip`** — "Needs you / All" toggle. `paper-light` + `rose-line-soft`,
  `label-caps`, `paper-ink` text; the **active** state inverts to `ink-void` fill
  with `paper-light` text.
- **`avatar`** — 32px square (sharp), `ink-void` fill, `paper-light` initials.
- **`terminal-surface`** — the live agent panel: `terminal-blue` fill, `ink-void`
  text, `header-mono` chrome. Its expandable logs invert to `ink-void` on `paper`.
- **`status-strip`** — the black footer: `ink-void` fill, `paper` text,
  `metric-mono` cells with green/rose/butter deltas, 30px collapsed (expands for
  detail). Inset paper seams divide its regions.

## Do's and Don'ts

- **Do** keep `terminal-blue` exclusive to the live agent surface — it is the
  product's "the agent is working here" signal, not a general accent.
- **Do** use the monospace stack only for chrome, metrics, and UPPERCASE labels;
  keep Funktional Grotesk for everything a person reads.
- **Do** hold the metric color vocabulary fixed: `primary-green` = up,
  `blossom` = down, `butter` = flat, `hot-rose` = alert.
- **Do** create depth with hairlines, inset seams, and paper banding.
- **Don't** add drop shadows, glows, or rounded card corners — surfaces are flat
  and sharp.
- **Don't** bring the marketing `lime` scale into the app chrome, or the
  app's `terminal-blue`/`butter` into marketing — the two accent systems stay on
  their own surfaces.
- **Don't** use pure black text on paper; use `ink-void` at ≤0.84 alpha so it
  reads as print.
