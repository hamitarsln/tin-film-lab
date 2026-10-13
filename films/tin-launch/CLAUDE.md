# Motion studio rules

You are making a launch film for Tin in code. Read `BRIEF.md` first, then the skills in
`.claude/skills/`. These rules hold for every file you write here.

## Render contract
- The film is one page, `src/index.html`, that sets `window.FILM = { duration, width, height }` and
  `window.seek(t)`. `seek(t)` paints the exact frame for film time t from nothing but t.
- No CSS transitions or animations, no setTimeout, no requestAnimationFrame in render mode, no state
  carried between frames, no Math.random (use `Motion.rng(seed)`).
- Render with `node tools/render.mjs`. Never screen-record.
- Work only inside this folder. `refs/` and `music/` are read-only inputs.

## Music
- The film is cut to the music. Pick a track from `music/library/LIBRARY.md`, cut it with
  `music/tools/cut.py`, and plan every scene in bars from `CUE.md`. Never place a cut by eye in seconds.
- Scenes change on 4-bar phrase starts. UI state changes land on beats. The biggest visual moment lands
  on the drop. Read beat, section and energy at render time with `music/tools/music.js`.

## Look
- Tin's world: warm ink on paper, Funktional Grotesk, monospace chrome, sharp corners. Terminal blue is
  the agent's surface only. One accent per scene.
- Banned: a centered title on a gradient, everything fading in, corner labels and frame borders, glows on
  UI chrome, particle bursts, dark 3D, bouncy easing on type, dead beats where nothing happens.
- Something new happens every 2 to 4 seconds. Springs, not linear moves. The camera always drifts a little.
- Never draw Tin's product UI from imagination. Rebuild it from `refs/product/dashboard/` (the real markup and
  CSS) and `refs/brand/DESIGN.md`, with real workflow names and copy from `refs/product/`.

## Truth
- Every word and number on screen comes from `BRIEF.md` or `refs/product/`. No invented customers, logos,
  metrics, testimonials or quotes. Anything illustrative is labelled as an example.

## Loop before anything is final
1. Render stills or a draft, then build review sheets with `tools/sheets.sh` and LOOK at them.
2. Score 1–10: hook in the first 2 s, readability at phone size, motion quality, variety, composition,
   brand accuracy, music sync, story clarity. Log scores and the 3 worst problems in `docs/REVIEW_LOG.md`.
3. Fix the 3 worst. Repeat until every score is 8 or higher, then do the full render.
