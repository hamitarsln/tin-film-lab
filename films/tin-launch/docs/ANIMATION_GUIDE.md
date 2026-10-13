# Animation guide

How every part of the film is built, so pieces written by different hands fit together. Read with
docs/STYLE.md (look, motion rules), docs/SHOTLIST.md (what happens when) and docs/UI_REFERENCE.md (the real
dashboard).

## Files

```
src/index.html          stage, fonts, tokens, script order. No logic beyond wiring.
src/engine.js           F: time (T), springs (segs/keys), drift, typing, caret, DOM helpers, camera transform.
src/ui/dashboard.css    the Tin dashboard skin: real structure from app.css, DESIGN.md tokens.
src/ui/dashboard.js     window.Dashboard(container) -> static DOM + named element map + rect().
src/scenes/*.js         one file per concern: captions, terminal, dashboard timeline, cursor, camera, end card.
src/main.js             builds everything once, then window.seek(t) calls each scene's update(t) in order.
```

Scripts load in that order with plain `<script>` tags (no modules, no bundler): motion.js, music.js, cue.js,
engine.js, ui/dashboard.js, scenes/*.js, main.js.

## The contract

- `seek(t)` paints the exact frame for film time t from t alone. Static DOM is built once at load. Per frame you
  may only set properties computed from t. Never read a value you wrote on a previous frame.
- No CSS `transition`, `animation`, `@keyframes`, `will-change`, `setTimeout`, `setInterval`,
  `requestAnimationFrame` (render mode), `Math.random`, `Date`. Use `F.rng(seed)` for noise.
- Every animated property is written on every call of `update(t)` (use `F.css`, which skips unchanged values, so it
  is cheap). An element that is "not yet born" is hidden, not removed.
- **Hide containers with `display: none`, never `visibility: hidden`.** A child whose `visibility: visible` was set
  on a later frame shows straight through a hidden parent, so the frame would depend on history.
  `tools/determinism.mjs` seeks the same times in three orders and fails if any pixel differs; run it after every
  structural change.
- Anything that can `leave()` (opacity, transform) must have every one of those properties re-set by `appear()`.
- **The "on" state of `visibility` is `''` (inherit), never `'visible'`.** An explicit `visible` on a child shows it
  through any hidden ancestor (the animatic caught a button label floating over its still-hidden card).
- Times come from the music: `F.T(bar, beat)` only. Never a literal second in scene code. Half beats are
  `F.T(7, 3.5)`.

## Spaces

- **Stage**: 1920×1080 design px, scaled to the viewport by index.html. Screen-space layers (captions, end card,
  flood) are positioned in stage px.
- **World**: one sheet of paper under the camera. The terminal and the dashboard window live here, in native px.
  The camera writes one transform on `#world`: `F.camTransform(x, y, z)` (centre of view in world px, zoom).
- **Window-local**: dashboard elements are positioned by CSS inside the 1600×1000 window. `dash.rect(name)` returns
  the element's box in window-local px measured at build time (offset chain, transforms ignored), so scene code can
  aim the camera and the cursor at real controls: world = window origin + local.

## Springs and easing

| Preset | Use |
|---|---|
| `snappy` [320, 30] | buttons, chips, counts, cursor presses, a word's settle |
| `base` [170, 26] | panels, cards, morphs, camera moves, the cursor's travel |
| `heavy` [90, 19] | big type, the logotype, the drop pull-back, the lime flood |

- A property with several targets: `F.keys(t, [[t0, v0], [t1, v1, 'base'], [t2, v2, {dur: 4}]])`. A key with a
  preset springs; a key with `{dur}` eases (inOut) and is only for slow pushes and drifts.
- Stagger lists by sixteenths (`F.BEAT / 4`) or eighths, never by arbitrary seconds.
- Overshoot is welcome on panels and the camera, never on body text: words settle with `snappy` (critically
  damped enough that type does not wobble).

## Entrances and exits

- Words: typed. A caption word appears whole on its beat and settles 0.06em upward with `snappy`; a block caret
  rides the end of the line. Never fade a word in.
- Commands and terminal lines: `F.typedLen` / `F.typedLenFit` with a seed per line. The caret is solid while keys are
  arriving and blinks on the beat grid after (`F.caretOn`).
- Panels and windows: grow out of an origin rect (clip or size spring), or morph from the element they come from.
- Cards and rows: rise from their own baseline under a mask, or fly from a source rect (FLIP with a spring).
- Exits: pushed out by the next element (move with a spring) or masked away. Opacity may only reach 0 on something
  already moving out.
- Colour changes (a count turning butter, a dot turning green) switch on the beat, no cross-fade longer than 0.08 s.

## The cursor

An arrow drawn as inline SVG (ink fill, paper-light 1.5 px outline), 26 px tall at native scale, living in world
space so it sticks to UI under camera moves. Travel uses `F.keys` with `base` per axis and arrives a quarter beat
before the click. A press is 0.88 scale for 0.06 s then `snappy` back; the pressed control shows its active state
from the press frame. Hover states turn on when the cursor arrives.

## Camera

`#world` gets one transform per frame from the camera scene: centre x, y and zoom z, each built with `F.keys` from
the framings in SHOTLIST.md, plus `F.drift` (a few px, a few thousandths of zoom) and a slow push per shot. Every UI
framing keeps the UI's top edge at or below stage y 360 (zoom z, window top at world y 0 → centre y = 180 / z + top),
so the caption band is always paper.

## Captions

Screen space, FG Medium, ink at 0.84 alpha, left edge x 120. One caption block = one or two lines, each line a list
of words with a `T(bar, beat)` per word. Hook size 128 px; band size 102 px. Captions never overlap UI and never sit
on a coloured surface.

## Colour and type tokens

Defined once as CSS variables in index.html (`--paper`, `--paper-light`, `--paper-warm`, `--paper-pale`,
`--paper-ink`, `--ink`, `--ink-84`, `--line`, `--rose-soft`, `--terminal`, `--terminal-deep`, `--green`,
`--green-deep`, `--butter`, `--butter-deep`, `--lime`). Fonts: `"FG"` (300/400/500) and `"SFM"` (500). Nothing uses a
colour or a font outside these.

## Checklist for any piece before it is merged

1. Renders the same frame at any t without having rendered the frames before it.
2. Every time is `F.T(...)`; every move is a named spring or an eased drift.
3. No fades in; no CSS animation; no randomness.
4. Every string is in SHOTLIST.md's word table.
5. Looks right at 960×540 and 1920×1080 (same layout, crisp text).
