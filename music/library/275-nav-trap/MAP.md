# Nav Trap (Mixkit #275)

Arulo · 1:44.58 · 70.00 BPM · 4/4

## Grid

- One beat = 0.8572 s. One bar = 3.4287 s. A 4-bar phrase = 13.715 s.
- Bar 1 starts at 0.010 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.8572. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 122 detected beats sit within 40 ms of the grid (7.4 ms RMS). Bar 1 placed by the downbeat model, agreement 78%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.01–0:13.72 | low | 0.06 | 0.03 | 0.10 | +0.12 |
| build | 5–8 (4) | 0:13.72–0:27.44 | low | 0.33 | 0.19 | 0.68 | +0.12 |
| drop | 9–28 (20) | 0:27.44–1:36.01 | peak | 0.93 | 0.97 | 0.94 | +0.01 |
| outro | 29–31 (3) | 1:36.01–1:46.30 | low | 0.42 | 0.53 | 0.50 | -0.83 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:00.54: stop, 1.17 s of near silence
- 0:02.00: stop, 1.42 s of near silence
- 0:03.91: stop, 1.22 s of near silence
- 0:07.40: stop, 1.16 s of near silence
- 0:08.98: stop, 1.3 s of near silence
- 0:10.61: stop, 1.38 s of near silence
- 0:24.01 bar 8: bass in (+23.5 dB)
- 0:27.44 bar 9: bass in (+25.1 dB)
- 1:39.44 bar 30: bass out (-11.1 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:14.58 @5.2 (0.88), 0:23.15 @7.4 (0.91), 0:31.73 @10.2 (0.87), 0:35.15 @11.2 (0.95), 0:38.58 @12.2 (0.89), 0:59.15 @18.2 (1.00), 1:02.58 @19.2 (0.90), 1:07.73 @20.4 (0.87), 1:10.30 @21.3 (0.93), 1:12.01 @22.1 (0.86), 1:14.58 @22.4 (0.90), 1:16.94 @23.2.75 (0.85), 1:18.87 @24.1 (0.85), 1:19.73 @24.2 (0.91), 1:23.16 @25.2 (0.93), 1:26.58 @26.2 (0.85)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  intro      ········  ······  ······  stop stop
  2   0:03.44  intro      █·······  ······  █·····  stop
  3   0:06.87  intro      ········  ······  ······  stop stop
  4   0:10.30  intro      █·······  ······  █·····  stop
  5▶  0:13.72  build      ██······  ······  ████··  
  6   0:17.15  build      ██······  █·····  ████··  
  7   0:20.58  build      ██······  ······  ████··  
  8   0:24.01  build      ███·····  ███···  ████··  bass in
  9▶  0:27.44  drop       ████████  ██████  ██████  bass in
 10   0:30.87  drop       ████████  ██████  ██████  
 11   0:34.30  drop       ████████  ██████  ██████  
 12   0:37.73  drop       ████████  ██████  ██████  
 13┊  0:41.15  drop       ███████·  ██████  ██████  
 14   0:44.58  drop       ████████  ██████  ██████  
 15   0:48.01  drop       ████████  ██████  ██████  
 16   0:51.44  drop       ████████  ██████  ██████  
 17┊  0:54.87  drop       ██████··  ██████  ████··  
 18   0:58.30  drop       ██████··  ██████  ████··  
 19   1:01.73  drop       ██████··  ██████  ████··  
 20   1:05.16  drop       ██████··  ██████  ████··  
 21┊  1:08.58  drop       ████████  ██████  ██████  
 22   1:12.01  drop       ████████  ██████  ██████  
 23   1:15.44  drop       ████████  ██████  ██████  
 24   1:18.87  drop       ██████··  █████·  ██████  
 25┊  1:22.30  drop       ████████  ██████  ██████  
 26   1:25.73  drop       ████████  ██████  ██████  
 27   1:29.16  drop       ████████  ██████  ██████  
 28   1:32.58  drop       ████████  ██████  ██████  
 29▶  1:36.01  outro      ███████·  █████·  █████·  
 30   1:39.44  outro      ███·····  ████··  ███···  bass out
 31   1:42.87  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
