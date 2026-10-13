# Uplifting Bass (Mixkit #726)

Lily J · 1:36.00 · 66.99 BPM · 4/4

## Grid

- One beat = 0.8956 s. One bar = 3.5825 s. A 4-bar phrase = 14.330 s.
- Bar 1 starts at 0.057 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.8956. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 96% of 98 detected beats sit within 40 ms of the grid (11.2 ms RMS). Bar 1 placed by the downbeat model, agreement 96%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.06–0:14.39 | mid | 0.65 | 0.80 | 0.28 | +0.10 |
| drop | 5–24 (20) | 0:14.39–1:26.04 | peak | 0.97 | 0.99 | 0.97 | -0.10 |
| outro | 25–27 (3) | 1:26.04–1:36.78 | low | 0.19 | 0.16 | 0.23 | -0.56 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:07.22 bar 3: riser (+25.6 dB in the highs) into bar 5
- 0:14.39 bar 5: bass in (+12.0 dB)
- 1:26.04 bar 25: bass out (-30.1 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:20.66 @6.4 (0.86), 0:21.55 @7.1 (0.88), 0:22.45 @7.2 (0.80), 0:23.79 @7.3.5 (0.90), 0:24.24 @7.4 (0.96), 0:24.91 @7.4.75 (0.77), 0:26.03 @8.2 (1.00), 0:26.70 @8.2.75 (0.81), 0:26.93 @8.3 (0.76), 0:27.82 @8.4 (0.98), 0:28.72 @9.1 (0.90), 0:38.57 @11.4 (0.83), 0:40.36 @12.2 (0.84), 0:43.94 @13.2 (0.79), 1:14.39 @21.4 (0.83), 1:16.19 @22.2 (0.84)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.06  intro      █████···  █████·  ······  
  2   0:03.64  intro      █████···  █████·  ······  
  3   0:07.22  intro      ██████··  █████·  ███···  riser→5
  4   0:10.80  intro      ██████··  █████·  ███···  
  5▶  0:14.39  drop       ████████  ██████  ██████  bass in
  6   0:17.97  drop       ████████  ██████  ██████  
  7   0:21.55  drop       ████████  ██████  ██████  
  8   0:25.13  drop       ████████  ██████  ██████  
  9┊  0:28.72  drop       ████████  ██████  ██████  
 10   0:32.30  drop       ████████  ██████  ██████  
 11   0:35.88  drop       ████████  ██████  ██████  
 12   0:39.46  drop       ████████  ██████  ██████  
 13┊  0:43.05  drop       ████████  ██████  ██████  
 14   0:46.63  drop       ████████  ██████  ██████  
 15   0:50.21  drop       ████████  ██████  ██████  
 16   0:53.79  drop       ████████  ██████  ██████  
 17┊  0:57.38  drop       ████████  ██████  ██████  
 18   1:00.96  drop       ████████  ██████  ██████  
 19   1:04.54  drop       ████████  ██████  ██████  
 20   1:08.12  drop       ████████  ██████  ██████  
 21┊  1:11.71  drop       ████████  ██████  ██████  
 22   1:15.29  drop       ████████  ██████  ██████  
 23   1:18.87  drop       ███████·  ██████  █████·  
 24   1:22.45  drop       ███████·  ██████  ████··  
 25▶  1:26.04  outro      ████····  ███···  ████··  bass out
 26   1:29.62  outro      ········  ······  ······  
 27   1:33.20  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
