---
name: motion-film
description: Build and render a launch or product film in code with a seek(t) page, springs and a headless render. Use for any film work in this folder.
---

# Motion film

## The engine
Opus writes a program, not a video. `src/index.html` paints any moment on demand through `window.seek(t)`;
`tools/render.mjs` walks time in headless Chromium and pipes frames into ffmpeg. Because nothing depends on a
clock, a fix is a one-line edit plus a re-render.

Start from `tools/example/index.html`: it shows the page contract, fonts, `Motion`, `Music` and the cue wired
together. Keep one file unless it passes ~1,500 lines; then split scenes into `src/scenes/*.js` loaded by
`<script>` tags (no modules, no bundler).

Canvas or DOM both work. DOM is easier for real UI (rebuild Tin's dashboard from `refs/product/dashboard/app.css`
class styles); canvas is easier for type and shapes. Mixing is fine: position DOM layers from `seek(t)` with inline
transforms. Never leave a CSS `transition` or `animation` on anything.

Write scenes against a layout function of (width, height), not fixed pixels, so a 9:16 cut can follow later.

## Motion that looks expensive (`tools/lib/motion.js`)
- `Motion.sp(t - t0, 'snappy' | 'base' | 'heavy' | 'playful')`: closed-form springs. Snappy for buttons and
  toggles, base for cards and the camera, heavy for big type and the logo, playful only for a mascot.
- `Motion.track(t, [[t0, v0], [t1, v1], ...])`: a value with several targets (a cursor, a container width) as a
  sum of springs. Continuous, and frame 812 renders without simulating 0–811.
- `Motion.swapAlpha(t, tIn, tOut)`: text inside a morphing box enters after the morph starts, leaves before the next.
- `Motion.typed(text, t, t0, cps)`: typing. Give keystrokes a human rhythm (vary cps per word, seeded).
- A tab indicator or highlight stretches when its leading edge uses a stiffer spring than its trailing edge.
- One continuous take: a button grows into a page, a chip becomes the next headline, a colour floods out of one
  object and back into another. Prefer that to cuts. When you do cut, cut hard on a downbeat.
- Camera: a slow push (1.00 → 1.04) per scene; the next scene starts at the zoom the last one ended on.
- Never `will-change` or CSS-scale text the camera zooms (it blurs). Scale with transforms on a parent and keep
  text crisp, or draw it on canvas at the final size.

## Story beats for a launch film
Hook in under 2 s (the pain or the promise, in five huge words) → the product appears → 2–3 moments where the
product does something real with a cursor → the payoff on the drop → the end card. Every on-screen sentence must be
true per `BRIEF.md`. A viewer who sees only the first 5 seconds should know what Tin is.

## Rendering
```bash
# stills of chosen moments (fast; use for storyboards and fixes)
node tools/render.mjs stills --page src/index.html --at 0.5,3.9,7.9 --outdir out/stills
# animatic: half size, 30 fps, no motion blur
node tools/render.mjs video --page src/index.html --w 960 --h 540 --fps 30 --sub 1 --workers 6 --out out/animatic.mp4
# a section only, to check a fix
node tools/render.mjs video --page src/index.html --from 8 --to 14 --w 960 --h 540 --fps 30 --sub 1 --out out/fix.mp4
# final: full size, 60 fps, 4 motion-blur subframes
node tools/render.mjs video --page src/index.html --fps 60 --sub 4 --workers 6 --out out/silent.mp4
tools/mix.sh out/silent.mp4 music-cut/music.wav out/tin-launch.mp4 [sfx.wav]
```
The page must read `?w=&h=` (render passes them) or lay out from `innerWidth`/`innerHeight` so the animatic at
960×540 matches the final. A final 30 s render takes several minutes; run it once, at the end.

## Deliverables
`out/tin-launch.mp4`, `out/poster.png` (the strongest single frame), `out/review/contact.png`, and `README.md`
in this folder: the track and why, the bar plan, the scores per round, and what you'd improve next.
