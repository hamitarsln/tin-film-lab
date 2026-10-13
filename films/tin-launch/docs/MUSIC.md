# Music

Gate 2. Track, runners-up, the cut, and how the story sits on it.

## What the story needs from the track

Concept A (docs/STORY.md) has two halves: a setup (hook, the command, the agent filling the plan) and a payoff
(the plan becomes a running system, a decision is approved, the end card). So the track needs:
- 100–125 BPM, a steady grid: typed words, cursor clicks and UI state changes land on beats.
- Energy under the hook, so the first two seconds don't sit on a quiet pad.
- A real build where the agent works and the plan assembles, ending in a held breath (the bass gone).
- One unmistakable drop near the middle of a ~30 s cut, for the plan→system reveal.
- A steady, unbusy texture after the drop, so the system, the decision and the end card can be read.

Candidates considered: every "solid" grid track at 100–125 BPM (PlaceIt World 02, Hollidays, Blindfolded, Roses,
Funkee Monkeee, Swish Swed, House Vibez, Razor Edge, Grandpa's Twist). I read every MAP.md, looked at every
map.png, and rendered spectrograms of the exact 16-bar windows for the four strongest (I cannot listen, so the
spectrogram stands in for the ear: kick, bass, risers and melodic lines are all visible).

Dropped early: Funkee Monkeee (brass funk, only 4 intro bars, so its drop would land at 8 s), Grandpa's Twist
(blues rock, off-brand for an AI-lab film), Roses (drop at song bar 26, long build-ups that don't fit 16 bars),
Blindfolded (the build is already at 0.70 energy so the drop barely contrasts, and its first drop would land too
early), PlaceIt World 02 (102 BPM cinematic guitar; lovely but soft, and its drop at bar 17 forces a 9.4 s phrase
grid that is too slow for a cursor film), Hollidays (bar 1 is near silence, which kills the hook; its bass entry
measured ~1.7 s after the mapped bar line, so the grid there needs checking by ear).

## The pick: Swish Swed (Mixkit #201, Arulo), 120.00 BPM, 4/4

Cut: song bars 13–28 (0:24.01 onward), 16 film bars, 32.00 s, drop on film bar 9 at 16.001 s, 1-bar fade.

```bash
uv run --project ../.. python music/tools/cut.py music/library/201-swish-swed music-cut --bars 16 --land drop --at 8 --fade-bars 1
```

Why it wins:
- **The shape is the story.** Film bars 1–4 (breakdown): a four-on-the-floor kick with tonal stabs and a sweep
  down on the very first beat, energy for the hook and the command. Bars 5–8 (build): the kick thins from bar 6,
  the low end is gone by bar 7, and a noise riser climbs to bar 8: exactly the agent reading the repo, the plan
  filling, and the held breath before approval. Bar 9: the drop, the low end slamming back in on the downbeat
  (+22.3 dB; the catalogue analysis measures this as the biggest drop of every shortlisted track, 54 dB jump in
  the full song). Bars 9–16: a steady, hypnotic riff at peak energy, which suits the system running on its own.
- **The grid is exact.** 100% of beats on the grid, 8.4 ms RMS. Beat = 0.50002 s, bar = 2.00008 s. I checked the
  drop in the measured envelope: the low band goes from 0.51 to 0.99 between 39.97 s and 40.08 s of the song, on
  the bar 21 downbeat (40.011 s). The spectrogram of the cut shows the slam at 16.00 s film time.
- **Room for words.** Instrumental tech house; the breakdown and build are sparse in the mids, and the drop riff
  sits in a narrow 400–700 Hz band, leaving space for big type.
- **Phrases land where the story turns:** film bars 1, 5, 9, 13 (hook / agent at work / drop / end card).

Risk I accept: the tags read "Workout, Tech House", which is more club than Tin's calm paper world. The picture
carries the calm (paper, ink, slow camera, springs); the track carries the launch energy, which an Apple keynote
bumper needs.

## Runner-up 1: House Vibez (Mixkit #745, Lily J), 122 BPM

Cut would be song bars 25–40, drop on film bar 9 (15.74 s), 31.5 s. Warmer and more melodic than the pick: a
chord pad through the breakdown, hats building with the kick removed for bars 5–8, then a melodic drop. It loses
because its first four bars fall in energy (0.50 → 0.25), so the hook would sit on the quietest part of the cut,
and a bass pickup ~0.6 s before the drop (62.38 s in the song) blurs the "hit on the first frame of bar 9".

## Runner-up 2: Razor Edge (Mixkit #1280, Michael Ramir C.), 122 BPM, tagged "Technology"

Cut would be song bars 38–53, drop on film bar 9 (15.74 s), 31.5 s, ending on the song's real last bar. Its
breakdown keeps a driving kick for the hook, a riser on bar 7 and a one-bar break on bar 8 before the drop. It
loses because the build is only one bar long (the agent's work in bars 5–8 would have no rising tension), the
breakdown is monotone, and the drop is dense and bright across the whole spectrum, which competes with on-screen
words.

## Bar plan (film bars; details per shot in docs/SHOTLIST.md)

| Bars | Seconds | Music | Story |
|---|---|---|---|
| 1–2 | 0–4 | breakdown, kick, sweep on 1.1 | Hook: "Your agent ships the product." / "Tin lets it run the marketing." |
| 3–4 | 4–8 | breakdown, kick | The command types into the agent; Enter on a downbeat; Tin connects |
| 5–6 | 8–12 | build, kick thinning | First prompt; the agent reads the repo; the plan's fields fill on beats |
| 7–8 | 12–16 | build, bass gone, riser | The plan assembles; the cursor reaches Approve and waits (bar 8) |
| 9 ◆ | 16.001 | drop | Click lands on the slam: the plan becomes the System, camera springs back |
| 9–12 | 16–24 | drop | Workflows on schedules, the agent session folds away and runs continue; a decision arrives and is approved |
| 13–16 | 24–32 | drop, fade over bar 16 | End card: wordmark, the command, tin.computer, held through the fade |

## Sound effects

The brief allows key clicks, UI ticks and a low hit on the drop from mixkit.co. I decide on SFX at gate 6 after
the picture locks; the track's own kick already marks the beats and its drop is the hit, so the default is music
only. If added, every effect sits on a measured beat from music-cut/cue.json.
