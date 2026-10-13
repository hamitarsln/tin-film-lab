# Music

## The brief for the track
The edit needs four things from the music, in this order:
1. **A slow open**: room for the pressed tin and the playbill to hold a beat or two each, with a beat you can hear.
2. **An acceleration**: a stretch where the music itself speeds up or tightens, so cuts moving from two beats to one,
   to 8ths and then to 16ths feel pulled by the track rather than laid on top of it.
3. **A drop or a stop where the terminal lands**: one moment that is unmistakably the arrival.
4. **Room after it**: about 6 s for the terminal, the blue draining away and the end card, held through a fade.

Only "solid grid" tracks were considered (`music/library/LIBRARY.md`), which rules out R&B vibes 1, Drawing the Sky
and Dub Techno Groove. Each candidate was read from its `MAP.md` and `map.png`, then measured from `map.json` with
two checks: onset and kick strength on the beat versus off it, bar by bar (can you hear the grid where a cut lands?),
and the onset pattern on every 16th of the build bars (does the music itself accelerate?).

## Pick: House Vibez (Mixkit #745), song bars 25–35
122 BPM, 4/4, beat 0.4918 s, bar 1.967 s. 11 bars, 21.64 s. The drop lands on film bar 9 at 15.738 s.

```
uv run --project ../.. python music/tools/cut.py music/library/745-house-vibez music-cut --bars 11 --land drop --at 8 --fade-bars 1.5
```

What the 16th-note onset pattern of each bar shows (`|` strong, `:` medium, `.` weak, space quiet):

| Film bar | Song bar | Onsets per 16th | What it gives the edit |
|---|---|---|---|
| 1–4 | 25–28 | `:    . .    .  . .` … a hit on each downbeat, little else; hats out, bass slowly receding | The slow open. A cut on every downbeat (or every two beats) is audible; nothing busy competes with the first frames. |
| 5–6 | 29–30 | `| :  : :  : :  : :` … an 8th-note pulse; the riser starts (highs 0.50 → 0.64); the bass falls away | The music tightens to 8ths, exactly where the cuts go to half-beats. |
| 7 | 31 | `| |  : :  | |  : |` … the 8ths get harder; the bass is gone (0.01); highs at their highest of the build | The 16th strobe: the riser carries it. |
| 8 | 32 | `|  .   (quiet)   # .|::` … a hit on beat 1, then **near silence for two beats**, a hit on the last 16th of beat 3 and a 16th fill on beat 4 | The stop. The film settles here: two cuts, each on one of the two hits, and "Your agent" read in the silence. |
| 9 | 33 | dense, bass back at full (0.15 → 0.78) | **The drop.** The terminal lands on it with "runs it." |
| 10–11 | 34–35 | full groove, fading over the last 1.5 bars | The blue drains and the end card holds through the fade. |

Why it wins:
- It is the only candidate with a **stop and a drop back to back** (bar 32 into 33): the edit can settle onto the last
  two screens in near silence and land the terminal on the hardest hit of the cut.
- Its build accelerates by itself: whole bars, then 8ths, then harder 8ths, then a 16th fill. Every step of the
  picture's acceleration has a matching step in the music.
- The open is genuinely quiet (hats out, a hit per bar) but never beatless, so even the 1 s holds of the prologue sit
  on something audible. The drop is the biggest change in the cut (bass 0.15 → 0.78, energy 0.25 → 0.92).
- Proportions match Fable 5: 7.9 s of slow open (Fable withholds for 7.1 s), 5.9 s of build (Fable strobes for 5.7 s),
  a 2 s settle, then 5.9 s from the landing to the end (Fable's two end cards take 4.1 s, plus our terminal).
- 122 BPM: a 16th is 2.95 frames at 24 fps, so the strobe runs at Fable's three frames a cut, give or take one frame in
  twenty. 8ths are 5.9 frames, beats 11.8.
- The loop: the end fades to silence and the film restarts on song bar 25, the quietest, sparsest bar of the cut.

Costs: the drop is not much louder overall than the first bar (the open still carries some bass), so the arrival is
made by the bass and the density coming back after the stop, not by volume. 21.6 s is a little over 20 s; ten bars
(from song bar 26) would give 19.7 s but cut the open to 5.9 s, and the open is where the film earns the right to
strobe later.

## Runner-up 1: Swish Swed (Mixkit #201), song bars 13–23
120.0 BPM exactly, so a 16th is exactly 3 frames: Fable's strobe, frame for frame. Breakdown (13–16) with off-beat
hats over a steady bass, a build (17–20) where the bass drains to nothing while the highs climb, a riser bar (20) and
the drop on 21. A clean shape, but the open is a mid-energy groove rather than a quiet one (the off-beat hats run
from the first frame), the build has no stop and no fill, and its first drop bar is thin in transients (the bass
arrives before the drums), so the terminal would land on a swell rather than a hit.

## Runner-up 2: Grandpa's Twist (Mixkit #800), song bars 1–11
124 BPM. It starts from the song's own first bar, which makes the loop natural, and its drums are audible from bar 2
(a backbeat on 2 and 4, strong onsets on every beat even while the level is low), so every cut in the open would sit
on a hit. The drop on bar 9 is the biggest energy jump of all the candidates (0.28 → 0.63, bass 0.16 → 0.71). Against
it: the "build" (5–8) barely builds (highs flat at about 0.45, no riser, no change of subdivision), so the strobe
would have nothing to accelerate with; and its blues-rock twist pulls the film toward period pastiche just as the
history arrives at 2026.

## Also measured and set aside
- **Young Trizzy 02** (70 BPM): ideal shape on paper (sparse intro, riser, drop at 13.7 s), but its intro is almost
  beatless (on-beat onsets 0.07–0.12), so the open would be cut to silence.
- **Blindfolded** (110 BPM): two near-silent bars, then a strong build and drop; the silence makes the first second
  feel like a dropout.
- **Razor Edge** (122 BPM): its breakdown is a flat four-on-the-floor for seven bars with a one-bar riser; no
  acceleration until the last bar.
- **Hollidays** (108 BPM): full drums from the start, and the bass arrives a bar after the marked drop.

## Licence
Mixkit Stock Music Free License (social, ads and YouTube without attribution; no broadcast, no music-only remixes, no
Content ID). Recorded in `music-cut/cue.json`.
