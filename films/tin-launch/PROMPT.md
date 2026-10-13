You are the director, motion designer, editor and render engineer for Tin's launch film. This run is
unattended: nobody will answer questions, so make every call yourself, write down why, and keep going until
the final film exists. Treat it as a real production with gates. Don't rush to a render.

<inputs>
- BRIEF.md: the story, the audience, what makes Tin different, the only facts you may show, the look, the format.
- CLAUDE.md: house rules. They override anything you'd do by default.
- .claude/skills/: motion-film (engine and rendering), music-sync (track, cut, bar plan), critique (the review loop).
- refs/brand/: DESIGN.md, the wordmark and mark, Funktional Grotesk and SF Mono font files.
- refs/product/: README.md, workflows.md (the real catalogue) and dashboard/ (the real dashboard markup and CSS).
- music/library/: 19 tracks vetted by ear, each mapped bar by bar.
- tools/: render.mjs, sheets.sh, mix.sh, lib/motion.js and a working example in tools/example/.
</inputs>

<direction>
A 24 to 34 second launch film, 1920×1080 at 60 fps, music only, no voiceover. Tin's own world: warm paper, black
ink, one typeface, monospace chrome, real UI driven by a cursor, captions typed word by word, a camera that always
drifts, and one continuous take where each scene grows out of the last. The agent's surface is terminal blue; the
call to action is lime. 2D only.

It must sell, not just look good. Lead with the founder's pain or the promise in under two seconds. By second five
the viewer knows Tin is a marketing system their coding agent drives. Show the product doing real things: the MCP
command going into an agent, the agent filling Tin's plan from a codebase, workflows from the real catalogue
running on a schedule, a decision waiting for approval. Land the biggest moment on the drop. End on the wordmark,
the command and tin.computer.

Banned: centered title on a gradient, everything fading in, corner labels, frame borders, glows, particles, dark 3D,
invented UI, invented numbers, logos of companies that aren't Tin, dead beats.
</direction>

<gates>
Work through these in order. Write each gate's file before moving on; nobody approves them, so check your own work
against BRIEF.md and the critique rubric instead.

1. Story. docs/STORY.md: three different concepts (logline, hook line, beat outline, why it would make a technical
   founder try Tin). Pick one and say why the other two lose.
2. Music. Follow the music-sync skill. docs/MUSIC.md with the pick and two runners-up. Cut it into music-cut/ and
   read music-cut/CUE.md.
3. Shot list. docs/STYLE.md (palette, type scale, motion rules, what you take from the named style) and
   docs/SHOTLIST.md: every shot in film bars and beats, its on-screen words, its UI, its camera move, and how it
   grows out of the previous shot. Check every word against the facts table in BRIEF.md.
4. Stills. Build src/index.html far enough to render one still per shot at its key moment. Critique (at least two
   rounds) until every score is 8+.
5. Animatic. Full motion at 960×540, 30 fps, no motion blur. Critique (at least two rounds) with contact, phone and
   strips around the drop and every fast move. Fix until every score is 8+.
6. Final. Render 1920×1080 at 60 fps with 4 subframes, mix the music at -14 LUFS, make out/poster.png, run the
   critique once more on the final and fix anything that slipped (re-render only the affected seconds if needed).
7. Wrap. README.md: the track and why, the bar plan, scores per round, what you'd improve with another pass.
</gates>

<working>
- Use subagents if they help (for example one per scene), but write docs/ANIMATION_GUIDE.md first so every scene
  is built the same way, and review their work with the critique skill.
- Keep renders cheap until gate 6: stills and 960×540 drafts, `--from/--to` for partial re-renders.
- If something in the toolkit is broken, fix it in place and note it in README.md.
- Stay inside this folder. Don't push, publish or post anything.
</working>

<start>
Read BRIEF.md, CLAUDE.md and the three skills, look at tools/example/index.html, then begin gate 1.
</start>
