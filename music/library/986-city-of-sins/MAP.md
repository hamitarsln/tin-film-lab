# City Of Sins (Mixkit #986)

Michael Ramir C. · 2:08.00 · 89.99 BPM · 4/4

## Grid

- One beat = 0.6667 s. One bar = 2.6669 s. A 4-bar phrase = 10.668 s.
- Bar 1 starts at 0.008 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.6667. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 99% of 179 detected beats sit within 40 ms of the grid (11.6 ms RMS). Bar 1 placed by the downbeat model, agreement 98%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.01–0:10.68 | low | 0.48 | 0.30 | 0.36 | +0.16 |
| drop | 5–32 (28) | 0:10.68–1:25.35 | peak | 0.98 | 1.00 | 0.97 | +0.00 |
| breakdown | 33–36 (4) | 1:25.35–1:36.02 | mid | 0.53 | 0.32 | 0.82 | +0.11 |
| drop | 37–44 (8) | 1:36.02–1:57.35 | peak | 0.91 | 0.91 | 0.99 | -0.01 |
| outro | 45–48 (4) | 1:57.35–2:08.02 | low | 0.16 | 0.19 | 0.16 | -0.63 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:02.67 bar 2: break, the bass drops out for 1 bar(s) and slams back in at bar 3 (0:05.34, +16.3 dB)
- 0:08.01 bar 4: bass in (+14.7 dB)
- 0:10.68 bar 5: bass in (+21.0 dB)
- 1:25.35 bar 33: break, the bass drops out for 2 bar(s) and slams back in at bar 35 (1:30.68, +12.6 dB)
- 1:28.02 bar 34: break, the bass drops out for 1 bar(s) and slams back in at bar 35 (1:30.68, +12.6 dB)
- 1:33.35 bar 36: bass in (+20.2 dB)
- 1:36.02 bar 37: bass in (+14.2 dB)
- 1:57.35 bar 45: bass out (-8.3 dB)
- 1:59.06: stop, 2.92 s of near silence

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:12.68 @5.4 (0.83), 0:14.01 @6.2 (0.74), 0:18.01 @7.4 (1.00), 0:25.53 @10.3.25 (0.55), 0:39.34 @15.4 (0.68), 0:50.01 @19.4 (0.84), 1:00.68 @23.4 (0.74), 1:02.01 @24.2 (0.74), 1:07.35 @26.2 (0.51), 1:12.68 @28.2 (0.63), 1:16.68 @29.4 (0.62), 1:18.02 @30.2 (0.60), 1:22.02 @31.4 (0.61), 1:44.68 @40.2 (0.62), 1:50.02 @42.2 (0.61), 1:54.02 @43.4 (0.61)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  intro      ████····  ██····  ██····  
  2   0:02.67  intro      ███·····  ······  ██····  break→3
  3   0:05.34  intro      ████····  ██····  ██····  
  4   0:08.01  intro      █████···  ████··  ██····  bass in
  5▶  0:10.68  drop       ████████  ██████  ██████  bass in
  6   0:13.34  drop       ████████  ██████  ██████  
  7   0:16.01  drop       ████████  ██████  ██████  
  8   0:18.68  drop       ████████  ██████  ██████  
  9┊  0:21.34  drop       ████████  ██████  ██████  
 10   0:24.01  drop       ████████  ██████  ██████  
 11   0:26.68  drop       ████████  ██████  ██████  
 12   0:29.34  drop       ████████  ██████  ██████  
 13┊  0:32.01  drop       ████████  ██████  ██████  
 14   0:34.68  drop       ████████  ██████  ██████  
 15   0:37.34  drop       ████████  ██████  ██████  
 16   0:40.01  drop       ████████  ██████  ██████  
 17┊  0:42.68  drop       ████████  ██████  ██████  
 18   0:45.34  drop       ████████  ██████  ██████  
 19   0:48.01  drop       ████████  ██████  ██████  
 20   0:50.68  drop       ████████  ██████  ██████  
 21┊  0:53.35  drop       ████████  ██████  ██████  
 22   0:56.01  drop       ████████  ██████  ██████  
 23   0:58.68  drop       ████████  ██████  ██████  
 24   1:01.35  drop       ████████  ██████  ██████  
 25┊  1:04.01  drop       ████████  ██████  ██████  
 26   1:06.68  drop       ████████  ██████  ██████  
 27   1:09.35  drop       ████████  ██████  ██████  
 28   1:12.01  drop       ████████  ██████  ██████  
 29┊  1:14.68  drop       ████████  ██████  ██████  
 30   1:17.35  drop       ████████  ██████  ██████  
 31   1:20.02  drop       ████████  ██████  ██████  
 32   1:22.68  drop       ████████  ██████  ██████  
 33▶  1:25.35  breakdown  ████····  ██····  █████·  break→35
 34   1:28.02  breakdown  ███·····  ······  █████·  break→35
 35   1:30.68  breakdown  ████····  ██····  █████·  
 36   1:33.35  breakdown  █████···  ████··  █████·  bass in
 37▶  1:36.02  drop       ███████·  ██████  ██████  bass in
 38   1:38.68  drop       ███████·  █████·  ██████  
 39   1:41.35  drop       ███████·  ██████  ██████  
 40   1:44.02  drop       ███████·  █████·  ██████  
 41┊  1:46.68  drop       ███████·  ██████  ██████  
 42   1:49.35  drop       ███████·  █████·  ██████  
 43   1:52.02  drop       ███████·  ██████  ██████  
 44   1:54.68  drop       ███████·  █████·  ██████  
 45▶  1:57.35  outro      █████···  ████··  ████··  bass out stop
 46   2:00.02  outro      ········  ······  ······  
 47   2:02.69  outro      ········  ······  ······  
 48   2:05.35  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
