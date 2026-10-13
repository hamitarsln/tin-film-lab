You are the art director and designer for Tin's art film. This is the pilot: build the materials board and stop.
No motion and no music yet. The run is unattended, so make every call yourself, write down why, and finish the
board; a human reviews it afterwards and cuts the weak materials.

<inputs>
- BRIEF.md: the idea, the arc of materials, the references, the format.
- CLAUDE.md: house rules.
- .claude/skills/: materials (sources, rights, cutouts), critique (the art rubric), motion-film (the page contract
  and render tools).
- refs/films/fable-5.mp4 and opus-5-5.mp4: the style references.
- refs/brand/mark.svg: the Tin mark as a vector path (viewBox 720×720, four shapes: T, i dot, i stem, n).
- tools/: render.mjs (stills mode), sheets.sh, lib/motion.js.
</inputs>

<gates>
1. Reference breakdown. Extract frames from both films with ffmpeg (several per second) and study them. Write
   docs/REFERENCE.md: how long each material holds, how the shape persists (arranged objects along its outline,
   texture inside it, or texture with the shape cut out), scale and placement, ground and grain, how type enters,
   how the end card is built. Be specific; this is what the board copies.
2. Material research. For each step of the arc in BRIEF.md, find at least two real candidates in the open-access
   archives and choose the best. Aim for 20 materials in arc order, plus 4 alternates. Record everything in
   materials/ASSETS.md and materials/assets.json per the materials skill.
3. Board. Build src/index.html so seek(i) paints still i: the Tin mark made from material i on Tin's paper,
   2160×2160, in the treatment REFERENCE.md says suits that material. Render every still to out/board/ and a single
   sheet out/board/BOARD.png (5 across, numbered). Run the critique skill at least twice; replace the weakest
   materials each round.
4. Hand-off. docs/BOARD.md: one line per still (number, material, era, archive, why it earns its place, its score),
   the alternates, which you would cut, and the words and end card you recommend. Then stop.
</gates>

<working>
- Use subagents to search archives in parallel if it helps; keep rights checks strict.
- Download at the largest size offered. Go slowly with each archive and back off on 429.
- Stay inside this folder. Don't publish or post anything.
</working>

<start>
Read BRIEF.md, CLAUDE.md and the skills, then begin gate 1.
</start>
