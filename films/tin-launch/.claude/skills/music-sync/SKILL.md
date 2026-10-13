---
name: music-sync
description: Choose a track from the vetted library, cut it to the film, and sync every scene and accent to its bars and beats. Use before storyboarding and whenever timing changes.
---

# Music sync

The film is cut to the music. You plan in bars, the code reads beats, and nothing is timed by eye.

## 1. Choose the track
Read `music/library/LIBRARY.md`. Only use tracks whose grid is "solid". For each candidate, read its `MAP.md`
and look at `map.png` (lanes: high, mid, low, onset; ▼ markers for bass in/out, breaks, risers). Judge:
- tempo against the story (100–125 BPM suits a cursor-driven product film; slower tracks need fewer, bigger moves),
- a usable drop or bass entry with a build before it,
- one-bar breaks (bass drops out, slams back): the best places for a hard cut or a reveal,
- whether the texture leaves room for on-screen words.
Write the pick and two runners-up, with reasons, in `docs/MUSIC.md`.

## 2. Cut it
```bash
uv run --project ../.. python music/tools/cut.py music/library/<dir> music-cut --bars <N> --land drop --at <A> --fade-bars 1
```
- `--bars N`: film length in whole bars (bar length is in LIBRARY.md; 30 s at 120 BPM ≈ 15 bars).
- `--land drop --at A`: the drop lands on film bar A+1. Give the hook and setup A bars (usually 2–4).
  `--land bar:<song bar>` lands any song bar instead, e.g. a break's slam-back.
- Writes `music-cut/music.wav`, `music-cut/cue.json`, `music-cut/cue.js` and `music-cut/CUE.md`.
Re-cut whenever the plan changes length. Read `CUE.md` every time; it is the bar sheet in film time.

## 3. Plan in bars
`docs/SHOTLIST.md` lists every shot as film bars and beats, e.g. "Shot 3, bars 5–8: the dashboard assembles,
one card per beat from 5.1; cursor clicks Approve on 8.1". Rules:
- scene changes on phrase starts (┊ and ▶ in CUE.md),
- UI state changes, type hits and cursor clicks on beats; small things may use half beats,
- the product's biggest moment on the landing bar (◆), a hard cut or reveal on a break's slam-back,
- the end card starts on a phrase start and holds through the fade.

## 4. Read the music at render time
```html
<script src="../tools/lib/motion.js"></script>
<script src="../music/tools/music.js"></script>
<script src="../music-cut/cue.js"></script>   <!-- sets window.CUE -->
```
```js
const M = Music(CUE);
M.time(5, 1)                         // film seconds of bar 5 beat 1. Put every cue time through this.
M.at(t)                              // { bar, beat, beatPhase, barPhase, phrase, section, energy }
M.pulse(t, { every: 'beat', decay: 10 })  // 1 on each beat, decays. Subtle: scale 1 + 0.02 * pulse.
M.env(t, 'low')                      // measured bass energy 0..1; 'kick', 'high', 'onset' also exist
M.since(t, 'break')                  // seconds since the last break slam-back
```
Use the measured envelopes sparingly (a breathing background, a camera nudge on kicks). The structure comes
from bars; the envelopes add life.

## 5. Check sync
After each draft, play the cut in your head against `CUE.md`: list in `docs/REVIEW_LOG.md` where each shot's
key moment lands (bar.beat) and confirm it is on the grid. A strip of 12 frames around the drop
(`tools/sheets.sh out/animatic.mp4 out/review <drop seconds>`) must show the hit on the first frame of the bar.
