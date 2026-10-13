# Swish Swed (Mixkit #201)

Arulo · 2:23.50 · 120.00 BPM · 4/4

## Grid

- One beat = 0.5000 s. One bar = 2.0001 s. A 4-bar phrase = 8.000 s.
- Bar 1 starts at 0.010 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.5000. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 273 detected beats sit within 40 ms of the grid (8.4 ms RMS). Bar 1 placed by the downbeat model, agreement 100%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| main | 1–12 (12) | 0:00.01–0:24.01 | peak | 0.88 | 0.98 | 0.69 | -0.02 |
| breakdown | 13–16 (4) | 0:24.01–0:32.01 | mid | 0.49 | 0.78 | 0.41 | +0.02 |
| build | 17–20 (4) | 0:32.01–0:40.01 | mid | 0.47 | 0.38 | 0.81 | -0.06 |
| drop | 21–48 (28) | 0:40.01–1:36.01 | peak | 0.87 | 0.99 | 0.69 | +0.00 |
| breakdown | 49–52 (4) | 1:36.01–1:44.01 | mid | 0.53 | 0.50 | 0.77 | -0.14 |
| drop | 53–60 (8) | 1:44.01–2:00.01 | peak | 0.87 | 0.99 | 0.71 | +0.00 |
| main | 61–68 (8) | 2:00.01–2:16.01 | peak | 0.90 | 0.99 | 0.66 | -0.06 |
| outro | 69–72 (4) | 2:16.01–2:24.01 | low | 0.03 | 0.10 | 0.00 | -0.10 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:24.01 bar 13: bass out (-10.1 dB)
- 0:32.01 bar 17: bass out (-6.6 dB)
- 0:34.01 bar 18: break, the bass drops out for 2 bar(s) and slams back in at bar 20 (0:38.01, +35.2 dB)
- 0:36.01 bar 19: break, the bass drops out for 1 bar(s) and slams back in at bar 20 (0:38.01, +35.2 dB)
- 0:40.01 bar 21: bass in (+22.3 dB)
- 1:36.01 bar 49: bass out (-8.5 dB)
- 1:38.01 bar 50: break, the bass drops out for 2 bar(s) and slams back in at bar 52 (1:42.01, +24.1 dB)
- 1:40.01 bar 51: break, the bass drops out for 1 bar(s) and slams back in at bar 52 (1:42.01, +24.1 dB)
- 1:44.01 bar 53: bass in (+22.2 dB)
- 2:16.01 bar 69: bass out (-29.7 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:05.51 @3.4 (0.92), 0:06.01 @4.1 (0.90), 0:06.51 @4.2 (0.95), 0:07.01 @4.3 (0.91), 0:07.51 @4.4 (0.98), 0:08.01 @5.1 (0.96), 0:12.51 @7.2 (0.91), 0:16.51 @9.2 (0.90), 0:17.51 @9.4 (0.97), 0:18.01 @10.1 (0.93), 0:20.51 @11.2 (0.90), 2:03.01 @62.3 (0.90), 2:06.52 @64.2 (0.96), 2:07.02 @64.3 (0.92), 2:07.52 @64.4 (1.00), 2:10.51 @66.2 (0.94)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  main       ███████·  ██████  ██████  
  2   0:02.01  main       ███████·  ██████  ████··  
  3   0:04.01  main       ███████·  ██████  ████··  
  4   0:06.01  main       ███████·  ██████  ████··  
  5┊  0:08.01  main       ███████·  ██████  █████·  
  6   0:10.01  main       ███████·  ██████  ████··  
  7   0:12.01  main       ███████·  ██████  ████··  
  8   0:14.01  main       ███████·  ██████  ████··  
  9┊  0:16.01  main       ███████·  ██████  ████··  
 10   0:18.01  main       ███████·  ██████  ████··  
 11   0:20.01  main       ███████·  ██████  ████··  
 12   0:22.01  main       ███████·  ██████  ████··  
 13▶  0:24.01  breakdown  ████····  █████·  ███···  bass out
 14   0:26.01  breakdown  ████····  █████·  ██····  
 15   0:28.01  breakdown  ████····  █████·  ██····  
 16   0:30.01  breakdown  ████····  █████·  ██····  
 17▶  0:32.01  build      █████···  ████··  ████··  bass out
 18   0:34.01  build      ███·····  ██····  ████··  break→20
 19   0:36.01  build      ███·····  ······  █████·  break→20
 20   0:38.01  build      ████····  ███···  ██████  
 21▶  0:40.01  drop       ███████·  ██████  █████·  bass in
 22   0:42.01  drop       ███████·  ██████  ████··  
 23   0:44.01  drop       ███████·  ██████  ████··  
 24   0:46.01  drop       ███████·  ██████  ████··  
 25┊  0:48.01  drop       ███████·  ██████  ████··  
 26   0:50.01  drop       ███████·  ██████  ████··  
 27   0:52.01  drop       ███████·  ██████  ████··  
 28   0:54.01  drop       ███████·  ██████  ████··  
 29┊  0:56.01  drop       ███████·  ██████  ████··  
 30   0:58.01  drop       ███████·  ██████  ████··  
 31   1:00.01  drop       ███████·  ██████  ████··  
 32   1:02.01  drop       ███████·  ██████  ████··  
 33┊  1:04.01  drop       ███████·  ██████  ████··  
 34   1:06.01  drop       ███████·  ██████  ████··  
 35   1:08.01  drop       ███████·  ██████  ████··  
 36   1:10.01  drop       ███████·  ██████  █████·  
 37┊  1:12.01  drop       ███████·  ██████  █████·  
 38   1:14.01  drop       ███████·  ██████  ████··  
 39   1:16.01  drop       ███████·  ██████  ████··  
 40   1:18.01  drop       ███████·  ██████  ████··  
 41┊  1:20.01  drop       ███████·  ██████  ████··  
 42   1:22.01  drop       ███████·  ██████  ████··  
 43   1:24.01  drop       ███████·  ██████  ████··  
 44   1:26.01  drop       ███████·  ██████  ████··  
 45┊  1:28.01  drop       ███████·  ██████  ████··  
 46   1:30.01  drop       ███████·  ██████  ████··  
 47   1:32.01  drop       ███████·  ██████  ████··  
 48   1:34.01  drop       ███████·  ██████  ████··  
 49▶  1:36.01  breakdown  ██████··  █████·  ████··  bass out
 50   1:38.01  breakdown  ████····  ███···  ████··  break→52
 51   1:40.01  breakdown  ███·····  █·····  █████·  break→52
 52   1:42.01  breakdown  ████····  ███···  ██████  
 53▶  1:44.01  drop       ███████·  ██████  █████·  bass in
 54   1:46.01  drop       ███████·  ██████  █████·  
 55   1:48.01  drop       ███████·  ██████  ████··  
 56   1:50.01  drop       ███████·  ██████  ████··  
 57┊  1:52.01  drop       ███████·  ██████  ████··  
 58   1:54.01  drop       ███████·  ██████  ████··  
 59   1:56.01  drop       ███████·  ██████  ████··  
 60   1:58.01  drop       ███████·  ██████  ████··  
 61▶  2:00.01  main       ███████·  ██████  ████··  
 62   2:02.01  main       ███████·  ██████  ████··  
 63   2:04.01  main       ███████·  ██████  ████··  
 64   2:06.02  main       ███████·  ██████  ████··  
 65┊  2:08.01  main       ███████·  ██████  ████··  
 66   2:10.01  main       ███████·  ██████  ████··  
 67   2:12.01  main       ███████·  ██████  ████··  
 68   2:14.01  main       ███████·  ██████  ████··  
 69▶  2:16.01  outro      █·······  ██····  ······  bass out
 70   2:18.01  outro      ········  ······  ······  
 71   2:20.01  outro      ········  ······  ······  
 72   2:22.01  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
