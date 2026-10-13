# Music

The film is cut to the music, never the other way round. Every track in `library/` is mapped so
a model can plan scenes in bars and the film code can read the beat at any frame.

## Library

`library/LIBRARY.md` lists the vetted tracks with tempo, meter, bar length, first drop, breaks
and structure. Each track folder has:

| File | For | What it holds |
|---|---|---|
| `MAP.md` | the model | grid, sections, sync points, accents, a bar-by-bar sheet |
| `map.json` | code | beats, downbeats, bars, sections, events, hits, 60 fps envelopes |
| `map.png` | the model's eyes | sections, events and per-beat high/mid/low/onset lanes |
| `check.mp3` | a human | 60 s of the track with clicks on the grid and a bell per section |

## Cut a track for a film

```bash
uv run python music/tools/cut.py music/library/1280-razor-edge films/launch/music \
  --bars 12 --land drop --at 3 --fade-bars 1
```

This takes 12 bars of Razor Edge so the drop lands on film bar 4, and writes `music.wav`,
`cue.json` (the map in film time, bars from 1, seconds from 0) and `CUE.md` (the bar sheet to plan
scenes against). The film always starts on a downbeat and ends on a bar line.

## Sync in the film

Inline `cue.json` and `tools/music.js` in the page, then drive motion from it:

```js
const M = Music(CUE);
const { bar, beat, beatPhase, section } = M.at(t);
const punch = M.pulse(t, { every: 'beat', decay: 12 });   // 1 on every beat, decays
const bass = M.env(t, 'low');                              // measured bass energy, 0..1
const sceneStart = M.time(5);                              // film seconds where bar 5 starts
```

Scenes change on phrase starts (┊ in `CUE.md`), state changes land on beats, and the biggest
visual moment lands on the drop. Never place a cut by eye in seconds.

## Rebuild

```bash
uv run python music/tools/map_track.py music/catalogue/mp3/<id>.mp3 music/library/<id>-<slug> --id <id> --title "<title>"
uv run python music/tools/index_library.py
```

`catalogue/` holds the scrape, analysis and previews used to vet the tracks. Mixkit Stock Music
Free License: social, ads and YouTube are fine without attribution. No broadcast, no remixing into
music-only tracks, no Content ID registration.
