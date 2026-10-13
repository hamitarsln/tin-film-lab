# Art studio rules

You are making Tin's art film in code. Read `BRIEF.md`, then the skills in `.claude/skills/`. These rules hold
for every file you write here.

## Render contract
- Stills and the film come from one page, `src/index.html`, that sets `window.FILM = { duration, width, height }`
  and `window.seek(t)`. `seek(t)` paints the exact frame for time t from nothing but t. No CSS transitions, timers,
  requestAnimationFrame in render mode, carried state or Math.random (use `Motion.rng(seed)`).
- Render with `node tools/render.mjs`. Never screen-record. Work only inside this folder; `refs/` and `music/`
  are read-only.

## Look
- One shape, many materials: the Tin mark (`refs/brand/mark.svg`) rebuilt from a different real material in
  every shot. Materials are real public-domain images (see the materials skill), never generated, never stock.
- Ground: Tin's paper (#F5F1E6) with fine grain. Ink #080808. Terminal blue #90D7E4 and lime oklch(0.90 0.22 120)
  are held back for the last beats.
- Banned: gradients, glows, particles, dark 3D, flat vector fills pretending to be materials, clip-art,
  people, modern brand logos.
- Text is almost absent: three or four words across the whole film, then the end card.

## Truth and rights
- Every image is public domain or CC0 and recorded in `materials/ASSETS.md` before it is used.

## Loop
After every board or draft, run the critique skill, log it in `docs/REVIEW_LOG.md`, and replace the weakest
materials before moving on.
