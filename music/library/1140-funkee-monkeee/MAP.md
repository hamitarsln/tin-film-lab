# Funkee Monkeee (Mixkit #1140)

Michael Ramir C. · 1:38.08 · 120.00 BPM · 4/4

## Grid

- One beat = 0.5000 s. One bar = 2.0000 s. A 4-bar phrase = 8.000 s.
- Bar 1 starts at 0.012 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.5000. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 192 detected beats sit within 40 ms of the grid (12.3 ms RMS). Bar 1 placed by the downbeat model, agreement 98%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.01–0:08.01 | low | 0.35 | 0.36 | 0.15 | +0.43 |
| drop | 5–20 (16) | 0:08.01–0:40.01 | peak | 0.83 | 0.95 | 0.94 | -0.03 |
| main | 21–36 (16) | 0:40.01–1:12.01 | peak | 0.84 | 0.94 | 0.94 | +0.01 |
| breakdown | 37–50 (14) | 1:12.01–1:40.01 | high | 0.67 | 0.81 | 0.82 | -0.80 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:02.01 bar 2: bass in (+6.1 dB)
- 0:04.01 bar 3: bass in (+8.8 dB)
- 1:36.01 bar 49: bass out (-45.8 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:00.76 @1.2.5 (0.71), 0:01.01 @1.3 (0.83), 0:01.26 @1.3.5 (0.75), 0:01.51 @1.4 (1.00), 0:01.76 @1.4.5 (0.76), 0:02.01 @2.1 (0.72), 0:02.26 @2.1.5 (0.96), 0:02.76 @2.2.5 (0.74), 0:03.26 @2.3.5 (0.79), 0:11.25 @6.3.5 (0.69), 0:22.76 @12.2.5 (0.70), 0:28.76 @15.2.5 (0.71), 0:43.76 @22.4.5 (0.70), 0:52.76 @27.2.5 (0.75), 0:54.76 @28.2.5 (0.79), 1:08.76 @35.2.5 (0.73)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  intro      █·······  ······  ······  
  2   0:02.01  intro      ██······  █·····  █·····  bass in
  3   0:04.01  intro      ████····  ███···  █·····  bass in
  4   0:06.01  intro      █████···  ████··  ██····  
  5▶  0:08.01  drop       ███████·  ██████  ██████  
  6   0:10.01  drop       ███████·  ██████  ██████  
  7   0:12.01  drop       ███████·  ██████  ██████  
  8   0:14.01  drop       ███████·  ██████  ██████  
  9┊  0:16.01  drop       ██████··  █████·  ██████  
 10   0:18.01  drop       ███████·  ██████  ██████  
 11   0:20.01  drop       ██████··  █████·  ██████  
 12   0:22.01  drop       ██████··  ██████  ██████  
 13┊  0:24.01  drop       ███████·  ██████  ██████  
 14   0:26.01  drop       ███████·  ██████  ██████  
 15   0:28.01  drop       ███████·  ██████  ██████  
 16   0:30.01  drop       ███████·  ██████  ██████  
 17┊  0:32.01  drop       ███████·  ██████  ██████  
 18   0:34.01  drop       ███████·  ██████  ██████  
 19   0:36.01  drop       ██████··  ██████  ██████  
 20   0:38.01  drop       ██████··  ██████  ██████  
 21▶  0:40.01  main       ██████··  █████·  ██████  
 22   0:42.01  main       ███████·  ██████  ██████  
 23   0:44.01  main       ██████··  █████·  █████·  
 24   0:46.01  main       ███████·  ██████  ██████  
 25┊  0:48.01  main       ███████·  ██████  ██████  
 26   0:50.01  main       ███████·  ██████  ██████  
 27   0:52.01  main       ██████··  █████·  ██████  
 28   0:54.01  main       ███████·  ██████  ██████  
 29┊  0:56.01  main       ███████·  ██████  ██████  
 30   0:58.01  main       ███████·  ██████  ██████  
 31   1:00.01  main       ███████·  ██████  ██████  
 32   1:02.01  main       ███████·  ██████  ██████  
 33┊  1:04.01  main       ███████·  █████·  ██████  
 34   1:06.01  main       ███████·  ██████  ██████  
 35   1:08.01  main       ███████·  █████·  ██████  
 36   1:10.01  main       ███████·  ██████  ██████  
 37▶  1:12.01  breakdown  ██████··  ██████  ██████  
 38   1:14.01  breakdown  ██████··  ██████  ██████  
 39   1:16.01  breakdown  ██████··  ██████  ██████  
 40   1:18.01  breakdown  ███████·  ██████  ██████  
 41┊  1:20.01  breakdown  ██████··  ██████  ██████  
 42   1:22.01  breakdown  ██████··  ██████  ██████  
 43   1:24.01  breakdown  ██████··  ██████  ██████  
 44   1:26.01  breakdown  ██████··  ██████  ██████  
 45┊  1:28.01  breakdown  ██████··  ██████  ██████  
 46   1:30.01  breakdown  ██████··  ██████  ██████  
 47   1:32.01  breakdown  ██████··  ██████  ██████  
 48   1:34.01  breakdown  ██████··  ██████  █████·  
 49┊  1:36.01  breakdown  ········  ······  ······  bass out
 50   1:38.01  breakdown  ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
