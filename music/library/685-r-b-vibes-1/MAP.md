# R&B vibes 1 (Mixkit #685)

Grigoriy Nuzhny · 3:01.39 · 90.00 BPM · 4/4

## Grid

- One beat = 0.6667 s. One bar = 2.6666 s. A 4-bar phrase = 10.666 s.
- Bar 1 starts at 0.042 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.6667. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 87% of 313 detected beats sit within 40 ms of the grid (13.9 ms RMS). Bar 1 placed by the downbeat model, agreement 99%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.04–0:10.71 | low | 0.23 | 0.15 | 0.20 | +0.45 |
| drop | 5–36 (32) | 0:10.71–1:36.04 | peak | 0.92 | 0.97 | 0.96 | +0.06 |
| breakdown | 37–44 (8) | 1:36.04–1:57.37 | high | 0.72 | 0.91 | 0.50 | +0.01 |
| drop | 45–60 (16) | 1:57.37–2:40.04 | peak | 0.87 | 0.94 | 0.90 | -0.19 |
| breakdown | 61–64 (4) | 2:40.04–2:50.71 | low | 0.39 | 0.70 | 0.20 | -0.28 |
| outro | 65–68 (4) | 2:50.71–3:01.37 | low | 0.07 | 0.29 | 0.00 | -0.14 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:05.38 bar 3: riser (+6.9 dB in the highs) into bar 5
- 0:08.04 bar 4: bass in (+33.2 dB)
- 0:10.71 bar 5: bass in (+12.3 dB)
- 2:53.52: stop, 0.67 s of near silence
- 2:54.50: stop, 1.46 s of near silence
- 2:56.15: stop, 0.88 s of near silence

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:27.37 @11.2 (0.74), 0:30.87 @12.3.25 (0.78), 0:54.04 @21.2 (0.76), 0:55.37 @21.4 (0.84), 0:56.71 @22.2 (0.81), 0:59.37 @23.2 (0.88), 1:00.71 @23.4 (0.77), 1:02.04 @24.2 (0.77), 1:04.71 @25.2 (0.93), 1:07.37 @26.2 (0.94), 1:08.71 @26.4 (0.83), 1:10.04 @27.2 (0.76), 1:10.87 @27.3.25 (0.82), 1:12.71 @28.2 (0.78), 1:26.87 @33.3.25 (0.78), 2:11.37 @50.2 (0.81)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.04  intro      ········  ······  ······  
  2   0:02.71  intro      █·······  ······  █·····  
  3   0:05.38  intro      ██······  ······  █·····  riser→5
  4   0:08.04  intro      ████····  ████··  ███···  bass in
  5▶  0:10.71  drop       ███████·  ██████  ██████  bass in
  6   0:13.38  drop       ████████  ██████  ██████  
  7   0:16.04  drop       ███████·  ██████  ██████  
  8   0:18.71  drop       ████████  ██████  ██████  
  9┊  0:21.37  drop       ███████·  ██████  ██████  
 10   0:24.04  drop       ████████  ██████  ██████  
 11   0:26.71  drop       ████████  ██████  ██████  
 12   0:29.37  drop       ████████  ██████  ██████  
 13┊  0:32.04  drop       ███████·  ██████  █████·  
 14   0:34.71  drop       ███████·  ██████  █████·  
 15   0:37.37  drop       ███████·  ██████  █████·  
 16   0:40.04  drop       ███████·  ██████  ██████  
 17┊  0:42.71  drop       ███████·  █████·  █████·  
 18   0:45.37  drop       ███████·  ██████  █████·  
 19   0:48.04  drop       ███████·  ██████  █████·  
 20   0:50.71  drop       ███████·  ██████  █████·  
 21┊  0:53.37  drop       ███████·  ██████  ██████  
 22   0:56.04  drop       ████████  ██████  ██████  
 23   0:58.71  drop       ███████·  ██████  ██████  
 24   1:01.37  drop       ████████  ██████  ██████  
 25┊  1:04.04  drop       ████████  ██████  ██████  
 26   1:06.71  drop       ████████  ██████  ██████  
 27   1:09.37  drop       ████████  ██████  ██████  
 28   1:12.04  drop       ████████  ██████  ██████  
 29┊  1:14.71  drop       ███████·  ██████  ██████  
 30   1:17.37  drop       ████████  ██████  ██████  
 31   1:20.04  drop       ███████·  ██████  ██████  
 32   1:22.71  drop       ████████  ██████  ██████  
 33┊  1:25.37  drop       ████████  ██████  ██████  
 34   1:28.04  drop       ████████  ██████  ██████  
 35   1:30.71  drop       ████████  ██████  ██████  
 36   1:33.37  drop       ████████  ██████  ██████  
 37▶  1:36.04  breakdown  ██████··  █████·  ████··  
 38   1:38.71  breakdown  █████···  █████·  ███···  
 39   1:41.37  breakdown  ██████··  ██████  ███···  
 40   1:44.04  breakdown  ██████··  ██████  ███···  
 41┊  1:46.71  breakdown  ██████··  █████·  ███···  
 42   1:49.37  breakdown  ██████··  █████·  ███···  
 43   1:52.04  breakdown  ██████··  █████·  ███···  
 44   1:54.71  breakdown  ██████··  ██████  ███···  
 45▶  1:57.37  drop       ███████·  ██████  ██████  
 46   2:00.04  drop       ████████  ██████  ██████  
 47   2:02.71  drop       ███████·  ██████  ██████  
 48   2:05.37  drop       ███████·  ██████  ██████  
 49┊  2:08.04  drop       ████████  ██████  ██████  
 50   2:10.71  drop       ████████  ██████  ██████  
 51   2:13.37  drop       ████████  ██████  ██████  
 52   2:16.04  drop       ████████  ██████  ██████  
 53┊  2:18.71  drop       ███████·  ██████  █████·  
 54   2:21.37  drop       ███████·  ██████  █████·  
 55   2:24.04  drop       ███████·  ██████  █████·  
 56   2:26.71  drop       ███████·  ██████  █████·  
 57┊  2:29.37  drop       ██████··  █████·  █████·  
 58   2:32.04  drop       ██████··  █████·  █████·  
 59   2:34.71  drop       ██████··  █████·  ████··  
 60   2:37.37  drop       ██████··  █████·  ████··  
 61▶  2:40.04  breakdown  ████····  █████·  ███···  
 62   2:42.71  breakdown  ███·····  ████··  █·····  
 63   2:45.37  breakdown  ███·····  ████··  █·····  
 64   2:48.04  breakdown  ██······  ████··  ······  
 65▶  2:50.71  outro      █·······  ███···  ······  
 66   2:53.37  outro      █·······  ██····  ······  stop stop
 67   2:56.04  outro      ········  █·····  ······  stop
 68   2:58.71  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
