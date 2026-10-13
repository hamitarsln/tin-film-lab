You are the director, motion designer and editor of Tin's art film. The materials board is done and reviewed
(docs/BOARD.md, out/board/, docs/REFERENCE.md, materials/). This run turns it into the finished film. It is unattended:
make every call yourself, write down why, and keep going until the final film exists.

<decisions>
The human review of the board decided these. They override BOARD.md.
- Cut 17 (TV test card), 10 (poster stamps) and 05 (biscuit tin).
- Replace 01 (engraved shop cards, too pale to open on) with A2, the pressed-tin ceiling, as a prologue: the film
  opens on the material Tin is named after, then the history runs from 02 onward.
- Rebuild 19 (search results). The mark barely reads. It must read in under half a second at 360 px, like the others,
  and still say "a page of search results" at a glance.
- Keep 18 (banner pixels) but make it say "the web, 1996" more clearly: think banner-ad dither and web-safe colour,
  not a yellow texture.
- In 13 (matchbooks), swap out the "Golden Guernsey" cover for another from the catalogue.
- Keep the mixed grounds (paper behind some stills, full-bleed with the mark cut out as paper in others).
- Words: "Your agent runs it." as BOARD.md proposes. End card as BOARD.md proposes, with the lime cursor as the only lime.
- Format: 2160×2160, 24 fps, about 20 seconds, square only for now.
</decisions>

<inputs>
- BRIEF.md, CLAUDE.md, docs/REFERENCE.md (how Fable and Opus move), docs/BOARD.md, materials/ASSETS.md and assets.json.
- src/index.html and scripts/: the board renderer. Grow it into the film; keep seek(t) pure.
- .claude/skills/: materials, critique, motion-film. Read motion-film for the render tools and the music rules below.
- music/library/LIBRARY.md: 19 vetted tracks, each mapped bar by bar (MAP.md, map.png). music/tools/cut.py cuts a
  track to whole bars and writes music-cut/CUE.md, cue.json and cue.js; music/tools/music.js reads beats at render time.
  Run it as: uv run --project ../.. python music/tools/cut.py music/library/<dir> music-cut --bars N --land drop --at A
- tools/render.mjs, tools/sheets.sh, tools/mix.sh, tools/determinism.mjs.
</inputs>

<direction>
Fable's grammar in Tin's world. The mark never moves off its spot; the material changes under it on the beat. A slow
open (the pressed tin, then the playbill, each held a beat or two, with a slow push and the grain alive), then the
history accelerates. Cuts go from every two beats, to every beat, to a strobe on half-beats or 16ths through the
twentieth century. The strobe may flash extra frames from the catalogue (other matchbooks, cards, stamps, signs,
alternate crops) between board materials, as Fable does with about 55 materials. Everything stops on the terminal:
terminal blue, the agent's log, "Your agent runs it." Then the blue drains to the ink-on-paper end card, tin.computer
with the lime cursor, and the film loops back to its first frame.

Motion is restrained: cuts on the grid, a slow push, a little drift in arranged objects, grain that changes every
frame (seeded by frame number). No transitions, no glows, no shakes, no zoom punches.
</direction>

<gates>
1. Apply the decisions. Rebuild 19 and 18, swap the matchbook, re-render those stills, and critique them.
2. Music. Pick a track from the library (solid grid only) whose shape fits a slow open, an acceleration and a stop or
   drop where the terminal lands. Write docs/MUSIC.md with the pick and two runners-up. Cut it and read CUE.md.
3. Edit plan. docs/EDIT.md: every cut as film bar.beat (and 16th where the strobe runs), which material, its
   treatment, its hold, and where the words enter. The terminal lands on the drop or the stop. The end card holds
   through the fade.
4. Animatic. The whole film at 1080×1080, 24 fps, no motion blur, with the music. Critique at least twice.
5. Final. 2160×2160, 24 fps, mixed at -14 LUFS. out/tin-art.mp4 and out/poster.png. Critique once more and fix.
6. Wrap. README.md: the track and why, the edit, the scores per round, and what you'd improve.
</gates>

<critique>
Your own scores ran generous on the last film. For every critique round, also ask a fresh subagent that has not seen
your reasoning to review the sheets cold: give it only the sheets, docs/REFERENCE.md and the critique skill's rubric,
and tell it to score as the art director comparing this with Fable 5. Log both sets of scores; the lower one counts.
Continue until both are 8 or higher on every dimension, plus music sync, rhythm (does the acceleration feel inevitable)
and loop (does the last frame lead back into the first).
</critique>

<working>
Stay inside this folder. Don't publish or post anything. Keep renders cheap until gate 5.
</working>

<start>
Read docs/BOARD.md, docs/REFERENCE.md and the decisions above, then begin gate 1.
</start>
