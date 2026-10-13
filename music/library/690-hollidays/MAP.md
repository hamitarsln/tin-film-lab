# Hollidays (Mixkit #690)

Grigoriy Nuzhny · 2:06.72 · 108.00 BPM · 4/4

## Grid

- One beat = 0.5556 s. One bar = 2.2222 s. A 4-bar phrase = 8.889 s.
- Bar 1 starts at 0.049 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.5556. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 224 detected beats sit within 40 ms of the grid (17.6 ms RMS). Bar 1 placed by the downbeat model, agreement 90%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–8 (8) | 0:00.05–0:17.83 | low | 0.36 | 0.14 | 0.32 | +0.46 |
| drop | 9–24 (16) | 0:17.83–0:53.38 | peak | 0.93 | 0.96 | 0.91 | +0.26 |
| breakdown | 25–32 (8) | 0:53.38–1:11.16 | mid | 0.64 | 0.27 | 0.74 | -0.27 |
| drop | 33–48 (16) | 1:11.16–1:46.72 | peak | 0.88 | 0.90 | 0.90 | +0.02 |
| breakdown | 49–52 (4) | 1:46.72–1:55.60 | mid | 0.60 | 0.66 | 0.60 | -0.20 |
| outro | 53–57 (5) | 1:55.60–2:06.72 | low | 0.14 | 0.22 | 0.14 | -0.40 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:02.27 bar 2: bass in (+10.8 dB)
- 0:04.49 bar 3: bass in (+13.2 dB)
- 0:06.71 bar 4: break, the bass drops out for 1 bar(s) and slams back in at bar 5 (0:08.94, +15.7 dB)
- 0:11.16 bar 6: bass out (-12.3 dB)
- 0:17.83 bar 9: bass in (+23.3 dB)
- 0:55.60 bar 26: bass out (-26.4 dB)
- 1:11.16 bar 33: bass in (+12.1 dB)
- 1:13.38 bar 34: bass in (+11.3 dB)
- 2:01.06: stop, 0.64 s of near silence

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:02.27 @2.1 (1.00), 0:02.83 @2.2 (0.63), 0:09.49 @5.2 (0.63), 0:20.05 @10.1 (0.67), 0:23.94 @11.4 (0.66), 0:30.88 @14.4.5 (0.63), 0:32.83 @15.4 (0.63), 0:42.27 @20.1 (0.66), 0:42.54 @20.1.5 (0.66), 0:48.10 @22.3.5 (0.65), 0:51.43 @24.1.5 (0.66), 0:52.54 @24.3.5 (0.64), 1:13.38 @34.1 (0.69), 1:17.27 @35.4 (0.65), 1:24.49 @39.1 (0.69), 1:36.99 @44.3.5 (0.64)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.05  intro      ········  ······  ······  
  2   0:02.27  intro      ███·····  ······  ██····  bass in
  3   0:04.49  intro      ███·····  ██····  ██····  bass in
  4   0:06.71  intro      ███·····  ······  ██····  break→5
  5┊  0:08.94  intro      █████···  ███···  ███···  
  6   0:11.16  intro      ███·····  █·····  ██····  bass out
  7   0:13.38  intro      ███·····  ······  ██····  
  8   0:15.60  intro      ████····  █·····  ███···  
  9▶  0:17.83  drop       ██████··  █████·  ███···  bass in
 10   0:20.05  drop       ███████·  ██████  ██████  
 11   0:22.27  drop       ███████·  ██████  █████·  
 12   0:24.49  drop       ████████  ██████  █████·  
 13┊  0:26.71  drop       ███████·  ██████  █████·  
 14   0:28.94  drop       ███████·  ██████  ██████  
 15   0:31.16  drop       ███████·  ██████  █████·  
 16   0:33.38  drop       ████████  ██████  ██████  
 17┊  0:35.60  drop       ████████  ██████  ██████  
 18   0:37.83  drop       ███████·  ██████  ██████  
 19   0:40.05  drop       ███████·  ██████  ██████  
 20   0:42.27  drop       ████████  ██████  ██████  
 21┊  0:44.49  drop       ████████  ██████  ██████  
 22   0:46.72  drop       ████████  ██████  ██████  
 23   0:48.94  drop       ████████  ██████  ██████  
 24   0:51.16  drop       ████████  ██████  ██████  
 25▶  0:53.38  breakdown  ███████·  ██████  ██████  
 26   0:55.60  breakdown  ████····  █·····  █████·  bass out
 27   0:57.83  breakdown  █████···  █·····  ████··  
 28   1:00.05  breakdown  █████···  █·····  ████··  
 29┊  1:02.27  breakdown  █████···  █·····  ████··  
 30   1:04.49  breakdown  ████····  ······  ████··  
 31   1:06.72  breakdown  █████···  █·····  ████··  
 32   1:08.94  breakdown  █████···  ██····  ████··  
 33▶  1:11.16  drop       ██████··  ████··  ████··  bass in
 34   1:13.38  drop       ███████·  ██████  ██████  bass in
 35   1:15.60  drop       ███████·  ██████  ██████  
 36   1:17.83  drop       ████████  ██████  ██████  
 37┊  1:20.05  drop       ████████  ██████  ██████  
 38   1:22.27  drop       ████████  ██████  ██████  
 39   1:24.49  drop       ███████·  ██████  ██████  
 40   1:26.72  drop       ████████  ██████  ██████  
 41┊  1:28.94  drop       ████████  ██████  ██████  
 42   1:31.16  drop       ███████·  ██████  ██████  
 43   1:33.38  drop       ███████·  █████·  █████·  
 44   1:35.60  drop       ███████·  █████·  █████·  
 45┊  1:37.83  drop       ███████·  █████·  █████·  
 46   1:40.05  drop       ██████··  █████·  █████·  
 47   1:42.27  drop       ██████··  █████·  █████·  
 48   1:44.49  drop       ██████··  █████·  ████··  
 49▶  1:46.72  breakdown  ██████··  █████·  ████··  
 50   1:48.94  breakdown  █████···  ████··  ████··  
 51   1:51.16  breakdown  ████····  ████··  ███···  
 52   1:53.38  breakdown  ████····  ███···  ███···  
 53▶  1:55.60  outro      ███·····  ███···  ██····  
 54   1:57.83  outro      ██······  ██····  ██····  
 55   2:00.05  outro      █·······  █·····  ······  stop
 56   2:02.27  outro      ········  ······  ······  
 57┊  2:04.49  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
