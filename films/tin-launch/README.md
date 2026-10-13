# Tin launch film

A 32-second launch film for Tin, made in code: one page (`src/index.html`) paints any frame from film time alone,
and `tools/render.mjs` walks it in headless Chromium. 1920×1080, 60 fps, 4 motion-blur subframes (180° shutter),
music plus subtle key and mouse clicks, mixed to −14.1 LUFS integrated, −1.4 dBTP.

| Deliverable | File |
|---|---|
| The film | `out/tin-launch.mp4` |
| Poster (strongest single frame, 17.9 s) | `out/poster.png` |
| Final review sheet | `out/review/contact.png` (plus `out/review/final/`) |
| Silent picture / music cut / effects stem | `out/silent.mp4`, `music-cut/music.wav`, `sfx/sfx.wav` |
| Gates | `docs/STORY.md`, `docs/MUSIC.md`, `docs/STYLE.md`, `docs/SHOTLIST.md`, `docs/ANIMATION_GUIDE.md`, `docs/UI_REFERENCE.md`, `docs/REVIEW_LOG.md` |

## The film in one line

*Your agent ships the product. Tin lets it run the marketing.* One continuous take on one sheet of paper: the
caption hands its caret to the agent's terminal-blue session on the beat; the MCP command goes in; the agent reads Tin's own
repository and fills the onboarding inputs; the plan path unfolds into Tin's real dashboard, where Tin writes the
plan; on the drop the plan's workflow names fly into a running System; the agent's session rolls up while the work
keeps going; a draft waits in Decisions and is approved as a pull request; the approval floods into lime and becomes
the call to action: the Tin logotype, `claude mcp add --transport http tin https://app.tin.computer/mcp`,
tin.computer.

Every word on screen comes from BRIEF.md or refs/product/ (checked line by line in docs/SHOTLIST.md). The example
project is Tin itself, shown in a workspace named "example", so every filled value and title is real copy; times,
dates and counts in the UI are example state in the dashboard's own formats.

## The track and why

**Swish Swed** (Mixkit #201, Arulo), 120 BPM, song bars 13–28, 16 bars = 32.00 s, drop on film bar 9 (16.0 s).
```bash
uv run --project ../.. python music/tools/cut.py music/library/201-swish-swed music-cut --bars 16 --land drop --at 8 --fade-bars 1
```
Its shape is the story: a kick-driven breakdown under the hook and the command (bars 1–4), a build where the kick
thins and the bass disappears under a riser while the agent works and the plan is written (bars 5–8, bar 8 is the held
breath with the cursor on Approve), and the biggest measured drop in the shortlist (+22 dB bass on the bar-21
downbeat, checked in the envelope and a spectrogram) for the plan becoming a system. A steady riff after the drop
leaves room for type. Runners-up: House Vibez (warmer, but its hook bars are the quietest of the cut) and Razor Edge
(a one-bar build only). Full reasoning in docs/MUSIC.md. I can't listen, so tracks were judged from the maps,
envelopes and spectrograms of the exact windows.

## Bar plan

| Bars | s | Music | Picture | Words |
|---|---|---|---|---|
| 1–2 | 0–4 | breakdown, sweep on 1.1 | paper, the terminal's blue strip | Your agent ships the product. / Tin lets it run the marketing. |
| 2.4–4 | 3.5–8 | breakdown | camera tilts into the terminal, its caret takes over on 2.4; the MCP command; Enter on 4.1; the first prompt | (captions hold) |
| 5–6 | 8–12 | build, kick thins | the agent's reply, Tin's files, `tin › Start here: onboard this business`, four inputs, one per beat | No forms. It reads your code. |
| 7–8 | 12–16 | build, bass gone, riser | the plan path unfolds into Tin's window; the camera arcs out (agent and Tin side by side) and into the reader; the plan writes itself; the cursor waits on Approve | Tin writes the plan. |
| 9 ◆ | 16.0 | **drop** | click; camera snaps back; names fly into System cards | A whole marketing system. / 60 workflows. |
| 10 | 18–20 | drop | the agent's band rolls up (10.2); camera to rail + This week | Running between sessions. |
| 11–12 | 20–24 | drop | Decisions count ticks (11.1), click Decisions (11.3), click "Open a pull request" (12.1), lime floods out of it (12.3) | Review before anything ships. |
| 13–16 | 24–32 | drop, fade over bar 16 | logotype lands (13.1), lime contracts into the command (13.3), tagline, tin.computer, agents; hold | Open-source marketing system, designed for coding agents. / tin.computer / Works with Claude Code, Codex and Cursor. |

Cues are written as `T(bar, beat)` and lead the audio by 14 ms (under one frame) so each event is fully on the frame
that is on screen when its beat sounds (the renderer's blur subframes integrate the few ms before each frame).

## Scores per round

Rubric: hook, story clarity, readability, motion, variety, composition, brand accuracy, music sync (1–10).
Details, worst problems and fixes for every round: docs/REVIEW_LOG.md.

| Round | Hook | Story | Read | Motion | Variety | Comp | Brand | Sync |
|---|---|---|---|---|---|---|---|---|
| Stills 1 | 6 | 7 | 6 | 6 | 7 | 6 | 8 | 7 |
| Stills 2 | 7 | 8 | 7 | 6 | 8 | 7 | 8 | 7 |
| Stills 3 | 8 | 8 | 8 | 8* | 8 | 8 | 8 | 8* |
| Animatic 1 | 8 | 8 | 8 | 6 | 8 | 8 | 8 | 7 |
| Animatic 2 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Final, pass 1 | 8 | 8 | 8 | 6 | 8 | 8 | 8 | 8 |
| Final, delivered | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |

\* provisional from mid-move frames. Final pass 1 failed on stepped motion-blur ghosts and an off-target mix;
fixed and re-rendered in full (docs/REVIEW_LOG.md, "Final review").

## How it's built

- `src/engine.js`: time in bars (`T`), springs as sums of segments (`keys`), seeded drift, human typing rhythm,
  caret, DOM helpers. `src/scenes/*.js`: captions, terminal, dashboard timeline, cursor, camera, end card.
  `src/ui/dashboard.{js,css}`: Tin's real dashboard rebuilt from refs/product/dashboard (structure, sizes, copy,
  formatters) and skinned with DESIGN.md tokens (Funktional Grotesk, sharp corners, ink and paper, terminal blue
  only on the agent, butter for decisions, green for running, lime only at the end).
- `docs/ANIMATION_GUIDE.md` is the contract every piece follows (one subagent inventoried the real UI into
  docs/UI_REFERENCE.md, another built the dashboard component against that guide; I reviewed both with the
  critique loop).

```bash
node tools/render.mjs stills --page src/index.html --at 3.3,17.9,29.5 --outdir out/stills/check
node tools/render.mjs video --page src/index.html --w 960 --h 540 --fps 30 --sub 1 --workers 6 --out out/animatic.mp4
node tools/render.mjs video --page src/index.html --fps 60 --sub 4 --shutter 180 --workers 6 --out out/silent.mp4
node tools/sfx-events.mjs src/index.html > sfx/events.json && python3 tools/sfx.py --key-db -16 --enter-db -13 --click-db -10
tools/mix.sh out/silent.mp4 music-cut/music.wav out/tin-launch.mp4 sfx/sfx.wav
node tools/determinism.mjs src/index.html   # proves seek(t) is a pure function of t
```

## Toolkit notes

Fixed in place:
- **`tools/mix.sh` missed its target.** Its single-pass dynamic `loudnorm` delivered −12.7 LUFS and −0.2 dBTP on this
  32 s film and squeezed the loudness range from 7.6 to 3.2 LU, which flattened the build-to-drop contrast. It is now
  two-pass: measure, apply one linear gain plus a gentle peak limiter run at 4× the sample rate, verify and correct
  once. Result: −14.1 LUFS integrated, −1.4 dBTP, LRA 7.2 LU.
- **`tools/render.mjs` gained `--shutter`.** Subframes were always spread over 270° of the frame interval; with 4
  subframes, fast moves showed four separate copies. `--shutter 180` (used for the final, still 4 subframes) halves
  the gap; the default stays 270 so old commands render identically. render.mjs now also passes `fps`, `sub` and
  `shutter` to the page, so the page can add analytic motion blur that matches the real subframe spacing.

Added and noted:
- **Added** `tools/determinism.mjs`: seeks the same times in three orders and compares pixels (reports raster
  noise separately from real leaks). It caught two real history leaks during the build: a hidden container whose
  child had `visibility: visible` (it shows through the parent), and a small composited layer (the cursor) keeping a
  stale raster scale after its transform changed. Both rules are now in docs/ANIMATION_GUIDE.md.
- **Added** `tools/stillsheet.py` (tile stills into a labelled sheet), `tools/sfx-events.mjs` and `tools/sfx.py`
  (an effects stem whose every click comes from the page's own typing and press times).
- **Behaviour:** `render.mjs` places blur subframes in the interval *before* each frame time, so an event exactly on a
  beat first shows one frame late; the film compensates with a 14 ms cue lead (`F.LEAD` in src/engine.js).
- **In the film, not the toolkit:** fast flat-colour edges (the lime flood, the unfolding sheet) draw their own
  motion blur (`F.blurRect`, a ramp across the distance each edge moves in one subframe), and the cursor draws
  speed-scaled trail copies, so 4 subframes never show stepped ghosts.

## Sound

Music: Swish Swed, Mixkit Stock Music Free License. Effects: Mixkit SFX (free licence, no attribution): "Hard single
key press in a laptop" (#2542), "Single key type" (#2533), "Classic click" (#1117). Only about one keystroke in four
is voiced (the screen types ~36 characters a second, which would sound like a machine gun), set ~14 LU under the
music; mouse clicks sit on the three presses about 7 dB under the music's peaks. Nothing is synthesized. No hit was
added on the drop: the track's own slam is the hit.

## What I'd improve with another pass

1. **Hear it.** I judged the track from maps, envelopes and spectrograms and set the effects by loudness
   measurements, not by ear. A listening pass on the mix (are the key clicks too clean or too quiet against the
   breakdown's kick?) is the first thing I'd do.
2. **Make "60" visible in the product, not just the caption.** A half-bar beat on the System's "Add workflows" tab,
   the catalogue grouped by area, before it collapses to "My system", would prove the number with real UI.
3. **Choreograph the flying names.** At the drop the organic system's name crosses the one-off run's name because
   the app puts saved workflows' runs inside "Scheduled"; ordering the plan to match the System's groups (or arcing
   the paths) would remove the crossing.
4. **The agent's terminal is a stylised surface.** It uses DESIGN.md's terminal blue and only real strings, but it is
   not Claude Code's real interface (no reference for it was in refs/). With a real session capture in refs it could
   be exact, including the MCP authentication step the cut compresses away.
5. **A 9:16 cut.** The page lays out from a `layout(W, H)` function and captions are screen-space, but the camera
   framings assume 16:9; a vertical version needs its own framings (the caption band on top works as is).
6. **More life in the last three seconds.** The end card holds on drift and a blinking caret while the music fades;
   a quieter secondary beat (the command's caret blinking in time, a hairline under tin.computer drawing on the
   last downbeat) could carry it without breaking the hold.
7. **Phone-first UI moments.** The UI is legible at 1080p but texture on a phone; one or two tighter push-ins (the
   "set up by your coding agent" line, the "Open a pull request" button) would let a phone viewer read the proof,
   not only the captions.
