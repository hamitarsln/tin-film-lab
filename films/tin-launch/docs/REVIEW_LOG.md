# Review log

Every critique round: what was reviewed, the eight scores (1–10, harsh), the three worst problems with bar.beat
or seconds, and what changed. Rubric: .claude/skills/critique/SKILL.md. Gate rule: every score 8+, with at least
two rounds on stills and two on the animatic before the final render.

Key moments checked against the grid (music-cut/CUE.md, 120 BPM, bar = 2.000 s): see docs/SHOTLIST.md "Sync sheet".

## Stills round 1 (gate 4)

Reviewed: out/stills/r1 at 1.1, 3.3, 7.6, 11.5, 15.6, 16.4, 17.8, 19.9, 21.95, 23.3, 29.0 s (one per shot at its key
moment, plus the drop in flight), 1920×1080, viewed as 960-wide sheets.

| Hook | Story | Readability | Motion | Variety | Composition | Brand | Sync |
|---|---|---|---|---|---|---|---|
| 6 | 7 | 6 | 6 | 7 | 6 | 8 | 7 |

Motion and sync are provisional from stills (springs and cue times read correctly; the animatic decides).

Three worst:
1. **The drop is small (9.1, 16.4–17.8 s).** The pull-back goes to z 0.61 to show terminal and Tin side by side,
   so the "biggest moment" is two small panels of unreadable UI on a lot of paper; mid-morph (16.4 s) the five
   flying cards overlap into a mess.
2. **The hook is static (1.1 s).** Captions live in screen space, so in the first two seconds nothing but the
   words moves; the paper between the line and the blue strip is dead and the strip reads as a bar, not a terminal.
3. **UI reads too small in the middle shots.** Reader at z 1.23 (plan rows ≈21 px), System after the drop at
   z 0.95 (titles ≈14 px), and at 11.5 s the newest terminal row is cut by the frame edge.

Also noted: in close-ups the window's 1 px ink top edge spans the whole frame and reads like a rule (21.95, 23.3 s);
the reader at 15.6 s crops the window's left edge while showing its right edge.

Changes:
1. Tin's window moves to world x 1460 (the terminal narrows to 1300); the drop now springs back to z 0.92 on the
   dashboard alone (terminal off frame), so the System builds big; cards fly in on eighths with the snappy spring.
   The session-end becomes visible: the blue terminal sweeps in from the left edge and folds into the rail's
   "Use your coding agent" box.
2. Captions get the camera's life: a slow push (1.00 → 1.035 over each caption) and a seeded drift; the hook block
   sits lower (top 344) and the terminal strip is taller (top at y 860).
3. Reader framing drops the lede paragraph so the plan fits at z ≈ 1.4 (rows ≈24 px, h1 ≈57 px); after the drop a
   new framing at z 1.2 holds the rail, the "This week" strip and the running cards for "Running between sessions";
   the terminal scrolls a row ahead of each new line. The window edge softens to line-strong (0.35 ink).

## Stills round 2 (gate 4)

Reviewed: out/stills/r2 at 1.1, 3.3, 7.6, 11.5, 15.6, 16.4, 17.8, 18.8, 19.9, 21.95, 23.3, 29.0 s, after round 1's
fixes and after correcting the example data to the app's real logic (a saved workflow's first run shows inside its
own group; "Running" holds only one-off runs; real pace line, first-runs line and weekly footer formats).

| Hook | Story | Readability | Motion | Variety | Composition | Brand | Sync |
|---|---|---|---|---|---|---|---|
| 7 | 8 | 7 | 6 | 8 | 7 | 8 | 7 |

Better: the drop now shows the System big (z 0.92), the plan is legible (z ≈ 1.4), the hook block sits in balance with
a taller terminal strip, the terminal never cuts its newest row.

Three worst:
1. **Drop morph still cluttered (16.4 s).** Whole cards fly from the plan rows and cross paths (the organic system's
   card is now in Scheduled, below the one-off Running card), so mid-flight five scaled cards stack on each other.
2. **The session end is invisible (18.8 s).** The terminal folds into the rail's agent box, but that box sits at
   window y 866, below the frame; the beat happens off screen.
3. **Edges.** The cursor rests half off the right edge after the drop (19.9 s); bar 7 crops the reader bar's Tin
   logo at the left; the terminal's right edge pokes in as an unexplained blue sliver at the drop (16.4, 17.8 s).

Changes:
1. The drop morph is now text-first: each plan row's workflow name flies (snappy, on sixteenths) to its card's title
   while the card wipes open downward from its title row (clip-path, paint-only), the rest of the plan lifts away.
   Flyers size by font-size, not transforms.
2. The sliver became the story: the terminal keeps a deliberate 180 px band at the left of the drop framing (the agent
   is still there), and on 10.2 the band rolls up like a blind (base spring, ~0.5 s) before "Running between
   sessions." types on 10.3.
3. The cursor rests over the "This week" strip; bar 7 frames the reader from its logo to Approve (z ≈ 1.24) and bar 8
   pushes in to the plan and Approve (z ≈ 1.4).
Also: tools/determinism.mjs now separates real history leaks from antialiasing noise; it caught and fixed two leaks
(hidden containers showing children through `visibility`, and the cursor's composited layer keeping a stale raster
scale, now drawn with left/top and SVG size).

## Stills round 3 (gate 4)

Reviewed: out/stills/r3 at 1.1, 3.3, 7.6, 11.5, 15.6, 16.25, 17.8, 18.65, 19.9, 21.95, 23.3, 29.0 s, plus 17.8 s at full
resolution and crops of the rail and the decision footer. Hook tightened since round 2: text block at y 372, the
camera starts at z 1.2 on the terminal strip (the `$` reads, the zoom into the terminal at 2.4 is shorter).

| Hook | Story | Readability | Motion | Variety | Composition | Brand | Sync |
|---|---|---|---|---|---|---|---|
| 8 | 8 | 8 | 8* | 8 | 8 | 8 | 8* |

\* provisional: judged from the mid-move frames (16.25 s morph, 18.65 s roll-up); the animatic decides.

What now works: the drop builds a big, legible System with names flying out of the plan into their cards; the
agent's blue band rolls up visibly before "Running between sessions."; every caption sits on paper; the UI is the
real dashboard down to its formatters (verified crisp at 1920×1080).

Three worst that remain (for the animatic to judge):
1. 23.3 s: "Nothing needs you." on an emptied view is the plainest frame of the film (it lasts one beat before the
   lime flood).
2. 16.1–16.3 s: mid-morph, flying names pass over the half-open Running card; fine if it reads as motion at speed.
3. Wide frames carry small UI microcopy (pace line, week strip): texture by design, the captions carry the meaning.

Fixed in this round: the project switcher's summary line ("example" / "example · 2 running") and the button's
in-flight label ("Approving") were stuck hidden by their build-time state; both now swap by visibility in their
shared grid cells (no width change under the cursor).

Gate 4 passes: three rounds on stills, every score 8.

## Animatic round 1 (gate 5)

Reviewed: out/animatic.mp4 (960×540, 30 fps, no blur; with music: out/animatic-music.mp4). Sheets in out/review/a1:
contact, phone, strips at 3.5, 12.25, 15.95, 16.1, 18.5, 19.0, 21.0, 22.0, 24.0, 25.0 s.

Sync check (key moment → bar.beat, read off the frames): first word 1.1 (frame 0); Tin 1.4; tilt 2.4; command 3.1,
Enter 4.1; prompt Enter + "No forms" 5.1; tool call 6.1; plan path 7.1; cursor on Approve 8.3; **Approve + "A" +
System on 9.1 (frame 480 = 16.000 s shows the click, the caption word and the header)**; band rolls up 10.2;
"Running" 10.3; count 11.1; click Decisions 11.3 (frame 630); click PR 12.1 (frame 660); flood 13.1; command 13.3.
All on the grid (cues lead the audio by 14 ms by design).

| Hook | Story | Readability | Motion | Variety | Composition | Brand | Sync |
|---|---|---|---|---|---|---|---|
| 8 | 8 | 8 | 6 | 8 | 8 | 8 | 7 |

Three worst:
1. **12.25 s, Tin's window never visibly grows out of the plan path.** The growing frame only clips the dashboard at
   its final position, so nothing shows until the aperture reaches x 1460; the "grows out of" link is lost.
2. **16.0–16.15 s, the drop hit is soft and muddy.** The camera spring needs three frames to get going (≈33% at
   0.1 s), and for four frames the fading plan text overlaps the incoming System header.
3. **24.0 s, the lime flood starts from nothing.** The decision card has already resolved, so the flood erupts as a
   tiny square from empty paper and the heavy spring accelerates late, behind its beat.

Also found: "Open a pull request" floating over the still-hidden card at 21.0–21.3 s (a child set to
`visibility: visible` shows through a hidden parent; every "on" state is now `''`, inherit); an empty caption band
for an eighth note between captions (seen on the phone sheet at ~21.3 s).

Changes:
1. Tin's growing frame has its own paper fill and line-strong edge: a paper sheet unfolds out of the path line and
   becomes the window, the dashboard appearing inside it as it lands.
2. Drop: the camera springs back on [240, 24] (≈53% of the move in 0.1 s, 3% overshoot); the plan's chrome cuts hard
   on the downbeat while the workflow names fly (no fading text under the new view).
3. The approval becomes the colour: the card stays in its "Approving" state and on 12.3 the lime floods out of that
   button's own rectangle (base spring, full frame by 12.4); the logotype lands on the phrase start 13.1, the lime
   contracts into the command on 13.3.
4. Captions now leave a sixteenth before the next one types (clear of the band, no empty gap).

## Animatic round 2 (gate 5)

Reviewed: out/animatic.mp4 after round 1's fixes and the caption push swap. Sheets in out/review/a2: contact,
phone, strips at 7.95, 15.95, 16.1, 18.95, 21.4, 22.95 s (plus an intermediate pass at 3.5, 12.3, 18.5, 21.0, 22.9,
23.3, 25.0 s before the push swap). tools/determinism.mjs: all frames pure functions of t.

Sync check (frame numbers at 30 fps; cues lead the audio by 14 ms): words on 1.1–2.3 (frames 0–90); tilt 2.4
(105); command 3.1 (120) → Enter 4.1 (180); prompt Enter, reply, "No forms" 5.1 (240); tool call 6.1 (300); plan path
7.1 (360), the window unfolding from it 7.1.5 (367); cursor on Approve 8.2–8.3 (435–450); **drop 9.1 (480): click,
"A", System skeleton and flyers on the first frame of the bar, camera 53% out by frame 483**; "60" 9.3 (510); band
rolls up 10.2 (555); "Running" + camera 10.3 (570); count 11.1 (600); click Decisions 11.3 (630); "Review" 11.4
(645); click PR 12.1 (660); flood out of the button 12.3 (690); logotype 13.1 (720); lime into the command 13.3
(750); tagline 14.1, URL 14.3, agents 15.1; hold and fade 16 (900–960). Every key moment sits on a beat; the end card
starts on the phrase start (13.1) and holds through the fade.

| Hook | Story | Readability | Motion | Variety | Composition | Brand | Sync |
|---|---|---|---|---|---|---|---|
| 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |

What changed the scores: the paper sheet visibly unfolds out of the plan path (12.3 s); the drop cuts the plan's
chrome on the downbeat while the names fly and the camera snaps back (no fading text under the new view); the
lime floods out of the approved button; one-line captions push each other (no empty band, no overlap); the stray
label through the hidden card is gone.

Three worst that remain (minor, carried to the final review):
1. 3.5 s: the caret's drop from the caption into the terminal is a small, quick mark; it may read as a flicker
   rather than a hand-off at phone size.
2. 16.0–16.2 s: the flying names cross paths over the half-open cards for a few frames (reads as motion at speed).
3. 29–32 s: the end card's last three seconds hold with only the caret and the drift (by design: the music fades).

Gate 5 passes: two rounds on the animatic, every score 8.

## Final review (gate 6)

Reviewed: out/tin-launch.mp4 (1920×1080, 60 fps, 4 subframes, 32.00 s, AAC 48 kHz) and out/silent.mp4. Sheets in
out/review/final (contact copied to out/review/contact.png): contact, phone, strips at 3.55, 12.8, 15.98, 16.05,
18.6, 21.4, 23.05, 25.05 s, plus full-resolution frames at 3.6, 12.8, 16.05, 21.4, 23.1, 25.1 s.

First final pass (270° shutter, the toolkit default) failed the strips:
1. **Stepped ghosts on fast flat-colour edges.** The lime flood (23.05 s) and its contraction (25.05 s) and the
   unfolding paper sheet (12.35 s) showed four hard copies of their edges (four subframes ≈ 27–40 px apart).
2. **Whole-frame doubling in fast camera moves.** The whip from the terminal to the reader (12.5 s, ≈46 px per
   subframe) and the move to Decisions (21.3 s, ≈15 px) split every word into four offset copies.
3. **The caret's flight into the terminal (3.55 s) read as four ghost bars**, and the cursor travelled as four
   separate arrows.
Also: tools/mix.sh's single-pass loudnorm delivered −12.7 LUFS / −0.2 dBTP and squeezed the loudness range from
7.6 to 3.2 LU, flattening the drop.

Fixes, then a full re-render (the camera changes touch most of the film, so no splicing):
1. Fast flat edges get analytic motion blur (F.blurRect: each edge ramps across the distance it travelled in one
   subframe interval); smooth, no steps.
2. render.mjs gained `--shutter` (default 270 = old behaviour); the final uses 4 subframes over a 180° shutter, half
   the gap between samples. Bar 7's whip became an arc (pull out to the agent and Tin side by side, then in) and the
   Decisions move eases over a bar's half. Peak motion is now ≤13 px per subframe anywhere in the film (measured at
   the frame corners), 4 px at the Decisions move.
3. The caret flight is cut: the caption's caret stops on 2.4 and the terminal's starts on the same beat. The cursor
   draws three fading trail copies in proportion to its speed (none when still).
4. mix.sh is now two-pass: one linear gain plus a gentle peak limiter at 4× oversampling, verified:
   **−14.1 LUFS integrated, −1.4 dBTP, LRA 7.2 LU** (the build-to-drop dynamics survive).

Second final pass (delivered file):

| Hook | Story | Readability | Motion | Variety | Composition | Brand | Sync |
|---|---|---|---|---|---|---|---|
| 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |

Sync verified on the delivered frames: the click, "A", the System skeleton and the flying names are all on frame 960
(16.000 s, the first frame of bar 9); the flood leaves the button on 12.3 (frame 1380); the logotype lands on 13.1
(frame 1440); the end card holds through the fade over bar 16. Typing and click sounds come from the page's own
event times (sfx/events.json).

What remains (accepted): the end card's last ~3 s are a hold (caret, drift, fading music) by design; UI microcopy
is texture at phone size (the captions carry the meaning); the cursor's fast travel shows a stylised trail rather
than a true smear.
