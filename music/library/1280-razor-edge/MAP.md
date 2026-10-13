# Razor Edge (Mixkit #1280)

Michael Ramir C. · 1:44.02 · 122.01 BPM · 4/4

## Grid

- One beat = 0.4918 s. One bar = 1.9671 s. A 4-bar phrase = 7.868 s.
- Bar 1 starts at 0.000 s (a pickup bar; the first full downbeat is bar 2 at 1.001 s).
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.4918. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 209 detected beats sit within 40 ms of the grid (7.2 ms RMS). Bar 1 placed by the downbeat model, agreement 100%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–5 (5) | 0:00.00–0:08.87 | low | 0.13 | 0.04 | 0.30 | +0.36 |
| drop | 6–37 (32) | 0:08.87–1:11.82 | peak | 0.80 | 0.84 | 0.85 | -0.19 |
| breakdown | 38–45 (8) | 1:11.82–1:27.55 | mid | 0.60 | 0.83 | 0.16 | -0.12 |
| drop | 46–54 (9) | 1:27.55–1:45.26 | peak | 0.81 | 0.89 | 0.73 | -0.93 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:01.00 bar 2: bass in (+18.8 dB)
- 0:04.93 bar 4: riser (+22.1 dB in the highs) into bar 6
- 0:08.87 bar 6: bass in (+14.7 dB)
- 0:30.51 bar 17: break, the bass drops out for 1 bar(s) and slams back in at bar 18 (0:32.48, +9.9 dB)
- 0:54.11 bar 29: break, the bass drops out for 1 bar(s) and slams back in at bar 30 (0:56.08, +8.6 dB)
- 1:23.62 bar 44: riser (+20.6 dB in the highs) into bar 46
- 1:25.59 bar 45: break, the bass drops out for 1 bar(s) and slams back in at bar 46 (1:27.55, +12.9 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:01.00 @2.1 (0.80), 0:18.21 @10.4 (0.85), 0:23.13 @13.2 (0.79), 0:26.08 @14.4 (0.80), 0:27.07 @15.2 (0.81), 0:30.02 @16.4 (0.78), 0:41.33 @22.3 (0.77), 0:43.29 @23.3 (0.88), 0:43.79 @23.4 (0.82), 0:45.26 @24.3 (1.00), 0:46.74 @25.2 (0.87), 0:48.21 @26.1 (0.81), 0:49.20 @26.3 (0.82), 0:55.10 @29.3 (0.80), 0:56.08 @30.1 (0.78), 1:25.59 @45.1 (0.77)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.00  intro      ········  ······  ······  
  2┊  0:01.00  intro      █·······  ······  █·····  bass in
  3   0:02.97  intro      ········  ······  ······  
  4   0:04.93  intro      █·······  ······  ██····  riser→6
  5   0:06.90  intro      ███·····  █·····  ██████  
  6▶  0:08.87  drop       ███████·  █████·  █████·  bass in
  7   0:10.84  drop       ██████··  █████·  █████·  
  8   0:12.80  drop       ██████··  █████·  █████·  
  9   0:14.77  drop       ██████··  █████·  █████·  
 10┊  0:16.74  drop       ██████··  █████·  █████·  
 11   0:18.70  drop       ██████··  █████·  █████·  
 12   0:20.67  drop       ██████··  █████·  █████·  
 13   0:22.64  drop       ██████··  █████·  █████·  
 14┊  0:24.61  drop       ██████··  █████·  █████·  
 15   0:26.57  drop       ██████··  █████·  █████·  
 16   0:28.54  drop       ██████··  █████·  █████·  
 17   0:30.51  drop       ████····  ███···  ██████  break→18
 18┊  0:32.48  drop       ███████·  ██████  █████·  
 19   0:34.44  drop       ███████·  ██████  █████·  
 20   0:36.41  drop       ███████·  ██████  █████·  
 21   0:38.38  drop       ███████·  ██████  █████·  
 22┊  0:40.34  drop       ██████··  █████·  █████·  
 23   0:42.31  drop       ██████··  █████·  █████·  
 24   0:44.28  drop       ███████·  █████·  █████·  
 25   0:46.24  drop       ██████··  █████·  █████·  
 26┊  0:48.21  drop       ██████··  █████·  █████·  
 27   0:50.18  drop       ██████··  █████·  █████·  
 28   0:52.15  drop       ███████·  █████·  █████·  
 29   0:54.11  drop       ████····  ███···  ██████  break→30
 30┊  0:56.08  drop       ███████·  ██████  █████·  
 31   0:58.05  drop       ███████·  ██████  █████·  
 32   1:00.01  drop       ███████·  ██████  █████·  
 33   1:01.98  drop       ███████·  ██████  ██████  
 34┊  1:03.95  drop       ███████·  ██████  █████·  
 35   1:05.92  drop       ███████·  ██████  █████·  
 36   1:07.88  drop       ███████·  ██████  █████·  
 37   1:09.85  drop       █████···  ████··  █████·  
 38▶  1:11.82  breakdown  █████···  █████·  ······  
 39   1:13.78  breakdown  █████···  █████·  ······  
 40   1:15.75  breakdown  █████···  █████·  ······  
 41   1:17.72  breakdown  █████···  █████·  ······  
 42┊  1:19.69  breakdown  █████···  █████·  ······  
 43   1:21.65  breakdown  █████···  █████·  ······  
 44   1:23.62  breakdown  █████···  █████·  ██····  riser→46
 45   1:25.59  breakdown  ████····  ██····  ██████  break→46
 46▶  1:27.55  drop       ███████·  ██████  █████·  
 47   1:29.52  drop       ███████·  ██████  █████·  
 48   1:31.49  drop       ███████·  ██████  █████·  
 49   1:33.45  drop       ███████·  ██████  █████·  
 50┊  1:35.42  drop       ███████·  ██████  █████·  
 51   1:37.39  drop       ███████·  ██████  █████·  
 52   1:39.36  drop       ███████·  ██████  █████·  
 53   1:41.32  drop       ███████·  ██████  █████·  
 54┊  1:43.29  drop       ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
