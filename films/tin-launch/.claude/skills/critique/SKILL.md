---
name: critique
description: Make the film watch its own frames. Render review sheets, score them harshly, fix the three worst problems, repeat. Use after every stills pass, animatic and final.
---

# Critique loop

You can read images. Looking at your own frames is the single habit that separates good films from "a bit mid".
Be a harsh motion director, not a proud author.

## Sheets
```bash
tools/sheets.sh out/animatic.mp4 out/review/r<N> <seconds of fast moves...>
```
- `contact.png`: 2 frames per second. Pacing, variety, composition, dead stretches.
- `phone.png`: 1 frame per second at 360 px wide. Can every word be read on a phone?
- `strip-<t>.png`: 12 consecutive frames around a fast move. Pops, overlaps, ghosting, text blurring mid-move.
For stills, open the PNGs from `out/stills/` directly.

Open every sheet and look properly before scoring.

## Score 1–10
| Dimension | 8 means |
|---|---|
| Hook | the first 2 s stop a scroll and say what this is about |
| Story clarity | someone who sees it once can say what Tin is and how to try it |
| Readability | every word readable at 360 px wide, on screen long enough to read twice |
| Motion quality | springs with mass, no linear slides, no pops, nothing jitters |
| Variety | something new every 2–4 s, no two scenes built the same way |
| Composition | deliberate layout, no corner labels or borders, nothing crowding an edge |
| Brand accuracy | looks like Tin's own product and site, real UI, real copy |
| Music sync | every key moment on a beat, the biggest moment on the drop, the end card holds through the fade |

## Hunt for
Text overlapping during swaps, anything sliding instead of springing, a centered title on a gradient, everything
fading in, glows, blurry scaled text, a dead beat with nothing happening, UI that looks invented, a number or claim
not in BRIEF.md, a word on screen for under 1 s, a cut that misses the downbeat.

## Log
Append to `docs/REVIEW_LOG.md` for each round: the round, what was reviewed, the eight scores, the three worst
problems with timestamps or bar.beat, and what you changed. Then fix the three worst, re-render only what changed
(stills or `--from/--to`), and go again. Stop when every score is 8 or higher, with at least two rounds on stills
and two on the animatic.
