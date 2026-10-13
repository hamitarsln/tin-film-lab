# Young Trizzy 02 (Mixkit #431)

Arulo · 1:36.97 · 70.00 BPM · 4/4

## Grid

- One beat = 0.8572 s. One bar = 3.4286 s. A 4-bar phrase = 13.715 s.
- Bar 1 starts at 0.007 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.8572. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 113 detected beats sit within 40 ms of the grid (7.1 ms RMS). Bar 1 placed by the downbeat model, agreement 100%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.01–0:13.72 | low | 0.14 | 0.21 | 0.29 | +0.33 |
| drop | 5–12 (8) | 0:13.72–0:41.15 | peak | 0.97 | 1.00 | 0.96 | +0.05 |
| breakdown | 13–16 (4) | 0:41.15–0:54.87 | low | 0.33 | 0.28 | 0.81 | +0.14 |
| drop | 17–29 (13) | 0:54.87–1:39.44 | high | 0.83 | 0.88 | 0.87 | -0.98 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:06.86 bar 3: break, the bass drops out for 1 bar(s) and slams back in at bar 4 (0:10.29, +35.1 dB)
- 0:06.86 bar 3: riser (+32.5 dB in the highs) into bar 5
- 0:13.72 bar 5: bass in (+18.9 dB)
- 0:41.15 bar 13: bass out (-33.2 dB)
- 0:44.58 bar 14: break, the bass drops out for 2 bar(s) and slams back in at bar 16 (0:51.44, +28.8 dB)
- 0:54.87 bar 17: bass in (+20.3 dB)
- 1:32.58 bar 28: bass out (-9.3 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:19.72 @6.4 (0.84), 0:26.58 @8.4 (0.93), 0:28.29 @9.2 (0.81), 0:31.72 @10.2 (0.94), 0:35.15 @11.2 (0.88), 0:40.29 @12.4 (0.90), 0:57.65 @17.4.25 (0.85), 0:59.15 @18.2 (0.91), 1:04.29 @19.4 (0.85), 1:05.15 @20.1 (0.82), 1:07.72 @20.4 (1.00), 1:11.15 @21.4 (0.92), 1:16.29 @23.2 (0.83), 1:19.72 @24.2 (0.94), 1:23.15 @25.2 (0.90), 1:28.29 @26.4 (0.83)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  intro      ········  ······  █·····  
  2   0:03.44  intro      ········  █·····  ······  
  3   0:06.86  intro      ········  ······  ██····  break→4 riser→5
  4   0:10.29  intro      ███·····  ████··  ████··  
  5▶  0:13.72  drop       ███████·  ██████  ██████  bass in
  6   0:17.15  drop       ████████  ██████  ██████  
  7   0:20.58  drop       ████████  ██████  ██████  
  8   0:24.01  drop       ████████  ██████  ██████  
  9┊  0:27.44  drop       ████████  ██████  ██████  
 10   0:30.86  drop       ████████  ██████  ██████  
 11   0:34.29  drop       ████████  ██████  ██████  
 12   0:37.72  drop       ████████  ██████  ██████  
 13▶  0:41.15  breakdown  ███·····  ██····  █████·  bass out
 14   0:44.58  breakdown  ██······  ······  █████·  break→16
 15   0:48.01  breakdown  ██······  ······  █████·  
 16   0:51.44  breakdown  ████····  ████··  █████·  
 17▶  0:54.87  drop       ████████  ██████  ██████  bass in
 18   0:58.29  drop       ████████  ██████  ██████  
 19   1:01.72  drop       ████████  ██████  ██████  
 20   1:05.15  drop       ████████  ██████  ██████  
 21┊  1:08.58  drop       ████████  ██████  ██████  
 22   1:12.01  drop       ████████  ██████  ██████  
 23   1:15.44  drop       ████████  ██████  ██████  
 24   1:18.86  drop       ███████·  ██████  ██████  
 25┊  1:22.29  drop       ████████  ██████  ██████  
 26   1:25.72  drop       ███████·  ██████  ██████  
 27   1:29.15  drop       ██████··  █████·  █████·  
 28   1:32.58  drop       ██······  ████··  ████··  bass out
 29┊  1:36.01  drop       ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
