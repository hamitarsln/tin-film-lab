# Trap Hamza (Mixkit #267)

Arulo · 1:44.73 · 82.50 BPM · 4/4

## Grid

- One beat = 0.7273 s. One bar = 2.9091 s. A 4-bar phrase = 11.636 s.
- Bar 1 starts at 0.008 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.7273. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 99% of 128 detected beats sit within 40 ms of the grid (8.9 ms RMS). Bar 1 placed by the downbeat model, agreement 97%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| main | 1–4 (4) | 0:00.01–0:11.64 | peak | 0.89 | 0.95 | 0.88 | +0.02 |
| main | 5–32 (28) | 0:11.64–1:33.10 | peak | 0.96 | 0.98 | 0.97 | -0.19 |
| outro | 33–36 (4) | 1:33.10–1:44.74 | low | 0.07 | 0.09 | 0.06 | -0.29 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:05.83 bar 3: riser (+8.9 dB in the highs) into bar 5
- 0:11.64 bar 5: bass in (+11.5 dB)
- 0:40.74 bar 15: bass out (-7.5 dB)
- 0:52.37 bar 19: bass in (+8.8 dB)
- 1:30.19 bar 32: bass out (-14.0 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:15.28 @6.2 (1.00), 0:18.19 @7.2 (0.94), 0:19.64 @7.4 (0.77), 0:21.10 @8.2 (0.82), 0:22.55 @8.4 (0.88), 0:25.46 @9.4 (0.83), 0:38.55 @14.2 (0.82), 0:57.46 @20.4 (0.91), 1:03.28 @22.4 (0.99), 1:07.64 @24.2 (0.75), 1:13.46 @26.2 (0.87), 1:16.37 @27.2 (0.89), 1:19.28 @28.2 (0.93), 1:22.19 @29.2 (0.88), 1:25.10 @30.2 (0.79), 1:26.55 @30.4 (0.75)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  main       ███████·  ██████  █████·  
  2   0:02.92  main       ███████·  ██████  █████·  
  3   0:05.83  main       ███████·  ██████  █████·  riser→5
  4   0:08.74  main       ███████·  ██████  ██████  
  5▶  0:11.64  main       ████████  ██████  ██████  bass in
  6   0:14.55  main       ████████  ██████  ██████  
  7   0:17.46  main       ████████  ██████  ██████  
  8   0:20.37  main       ████████  ██████  ██████  
  9┊  0:23.28  main       ████████  ██████  ██████  
 10   0:26.19  main       ████████  ██████  ██████  
 11   0:29.10  main       ████████  ██████  ██████  
 12   0:32.01  main       ████████  ██████  ██████  
 13┊  0:34.92  main       ████████  ██████  ██████  
 14   0:37.83  main       ████████  ██████  ██████  
 15   0:40.74  main       ███████·  ██████  █████·  bass out
 16   0:43.65  main       ███████·  ██████  █████·  
 17┊  0:46.55  main       ███████·  ██████  █████·  
 18   0:49.46  main       ███████·  ██████  ██████  
 19   0:52.37  main       ████████  ██████  ██████  bass in
 20   0:55.28  main       ████████  ██████  ██████  
 21┊  0:58.19  main       ████████  ██████  ██████  
 22   1:01.10  main       ████████  ██████  ██████  
 23   1:04.01  main       ████████  ██████  ██████  
 24   1:06.92  main       ████████  ██████  ██████  
 25┊  1:09.83  main       ████████  ██████  ██████  
 26   1:12.74  main       ████████  ██████  ██████  
 27   1:15.64  main       ████████  ██████  ██████  
 28   1:18.55  main       ████████  ██████  ██████  
 29┊  1:21.46  main       ████████  ██████  ██████  
 30   1:24.37  main       ████████  ██████  ██████  
 31   1:27.28  main       ███████·  ██████  ██████  
 32   1:30.19  main       ██████··  █████·  █████·  bass out
 33▶  1:33.10  outro      ██······  ██····  █·····  
 34   1:36.01  outro      ········  ······  ······  
 35   1:38.92  outro      ········  ······  ······  
 36   1:41.83  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
