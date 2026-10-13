# Drum and Bass Vibes (Mixkit #719)

Lily J · 1:36.00 · 87.99 BPM · 4/4

## Grid

- One beat = 0.6819 s. One bar = 2.7276 s. A 4-bar phrase = 10.910 s.
- Bar 1 starts at 0.059 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.6819. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 99% of 116 detected beats sit within 40 ms of the grid (14.3 ms RMS). Bar 1 placed by the downbeat model, agreement 97%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.06–0:10.97 | mid | 0.65 | 0.54 | 0.56 | +0.24 |
| drop | 5–32 (28) | 0:10.97–1:27.34 | peak | 0.95 | 0.98 | 0.96 | -0.00 |
| outro | 33–36 (4) | 1:27.34–1:38.25 | low | 0.27 | 0.29 | 0.24 | -0.80 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:02.79 bar 2: break, the bass drops out for 1 bar(s) and slams back in at bar 3 (0:05.51, +6.3 dB)
- 0:05.51 bar 3: riser (+22.6 dB in the highs) into bar 5
- 0:08.24 bar 4: bass in (+27.9 dB)
- 0:10.97 bar 5: bass in (+21.2 dB)
- 0:21.88 bar 9: bass in (+10.5 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:11.99 @5.2.5 (0.77), 0:19.66 @8.1.75 (0.67), 0:20.00 @8.2.25 (0.74), 0:25.62 @10.2.5 (0.80), 0:31.08 @12.2.5 (0.93), 0:36.53 @14.2.5 (0.97), 0:42.67 @16.3.5 (0.83), 0:43.02 @16.4 (1.00), 0:47.28 @18.2.25 (0.72), 0:52.74 @20.2.25 (0.75), 0:53.08 @20.2.75 (0.77), 0:54.78 @21.1.25 (0.76), 0:58.19 @22.2.25 (0.75), 1:04.49 @24.3.5 (0.86), 1:04.84 @24.4 (0.73), 1:08.93 @26.2 (0.77)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.06  intro      ████····  ███···  ███···  
  2   0:02.79  intro      █████···  ██····  ███···  break→3
  3   0:05.51  intro      ██████··  ███···  ████··  riser→5
  4   0:08.24  intro      ██████··  ████··  ████··  bass in
  5▶  0:10.97  drop       ███████·  ██████  █████·  bass in
  6   0:13.70  drop       ███████·  ██████  ██████  
  7   0:16.42  drop       ███████·  ██████  █████·  
  8   0:19.15  drop       ███████·  █████·  ██████  
  9┊  0:21.88  drop       ████████  ██████  ██████  bass in
 10   0:24.61  drop       ████████  ██████  ██████  
 11   0:27.33  drop       ████████  ██████  ██████  
 12   0:30.06  drop       ████████  ██████  ██████  
 13┊  0:32.79  drop       ████████  ██████  ██████  
 14   0:35.52  drop       ████████  ██████  ██████  
 15   0:38.24  drop       ████████  ██████  ██████  
 16   0:40.97  drop       ████████  ██████  ██████  
 17┊  0:43.70  drop       ████████  ██████  ██████  
 18   0:46.43  drop       ████████  ██████  ██████  
 19   0:49.16  drop       ████████  ██████  ██████  
 20   0:51.88  drop       ████████  ██████  ██████  
 21┊  0:54.61  drop       ████████  ██████  ██████  
 22   0:57.34  drop       ████████  ██████  ██████  
 23   1:00.06  drop       ████████  ██████  ██████  
 24   1:02.79  drop       ████████  ██████  ██████  
 25┊  1:05.52  drop       ███████·  ██████  ██████  
 26   1:08.25  drop       ████████  ██████  ██████  
 27   1:10.97  drop       ████████  ██████  ██████  
 28   1:13.70  drop       ███████·  ██████  ██████  
 29┊  1:16.43  drop       ███████·  ██████  ██████  
 30   1:19.16  drop       ████████  ██████  ██████  
 31   1:21.89  drop       ███████·  ██████  ██████  
 32   1:24.61  drop       ███████·  ██████  ██████  
 33▶  1:27.34  outro      ██████··  ██████  ████··  
 34   1:30.07  outro      ██······  █·····  ██····  
 35   1:32.80  outro      ········  ······  ······  
 36   1:35.52  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
