# Don't Look Back (Mixkit #488)

Diego Nava · 1:41.55 · 65.00 BPM · 4/4

## Grid

- One beat = 0.9231 s. One bar = 3.6924 s. A 4-bar phrase = 14.769 s.
- Bar 1 starts at 0.014 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.9231. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 99% of 110 detected beats sit within 40 ms of the grid (10.8 ms RMS). Bar 1 placed by the downbeat model, agreement 90%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–8 (8) | 0:00.01–0:29.55 | mid | 0.64 | 0.51 | 0.84 | +0.05 |
| drop | 9–24 (16) | 0:29.55–1:28.63 | peak | 0.95 | 0.98 | 0.93 | -0.00 |
| outro | 25–28 (4) | 1:28.63–1:43.40 | low | 0.20 | 0.13 | 0.27 | -0.46 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:29.55 bar 9: bass in (+17.0 dB)
- 1:28.63 bar 25: bass out (-25.7 dB)
- 1:32.32 bar 26: bass out (-7.0 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:02.78 @1.4 (0.86), 0:06.47 @2.4 (0.85), 0:21.25 @6.4 (0.86), 0:32.32 @9.4 (0.90), 0:47.09 @13.4 (0.93), 0:50.78 @14.4 (0.83), 1:01.86 @17.4 (0.98), 1:05.55 @18.4 (0.91), 1:07.40 @19.2 (0.86), 1:11.09 @20.2 (0.85), 1:12.94 @20.4 (0.87), 1:16.63 @21.4 (0.96), 1:20.32 @22.4 (1.00), 1:22.17 @23.2 (0.87), 1:24.02 @23.4 (0.87), 1:25.86 @24.2 (0.83)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.01  intro      █████···  ███···  █████·  
  2   0:03.71  intro      █████···  ███···  █████·  
  3   0:07.40  intro      █████···  ███···  █████·  
  4   0:11.09  intro      █████···  ███···  █████·  
  5┊  0:14.78  intro      █████···  ███···  █████·  
  6   0:18.48  intro      █████···  ███···  █████·  
  7   0:22.17  intro      █████···  ███···  █████·  
  8   0:25.86  intro      █████···  ████··  █████·  
  9▶  0:29.55  drop       ████████  ██████  ██████  bass in
 10   0:33.24  drop       ████████  ██████  █████·  
 11   0:36.94  drop       ███████·  ██████  █████·  
 12   0:40.63  drop       ███████·  ██████  █████·  
 13┊  0:44.32  drop       ████████  ██████  █████·  
 14   0:48.02  drop       ████████  ██████  █████·  
 15   0:51.71  drop       ███████·  ██████  █████·  
 16   0:55.40  drop       ███████·  ██████  █████·  
 17┊  0:59.09  drop       ████████  ██████  ██████  
 18   1:02.78  drop       ████████  ██████  ██████  
 19   1:06.48  drop       ████████  ██████  ██████  
 20   1:10.17  drop       ████████  ██████  ██████  
 21┊  1:13.86  drop       ████████  ██████  ██████  
 22   1:17.55  drop       ████████  ██████  ██████  
 23   1:21.25  drop       ████████  ██████  ██████  
 24   1:24.94  drop       ████████  ██████  ██████  
 25▶  1:28.63  outro      ████····  ██····  ███···  bass out
 26   1:32.32  outro      ███·····  █·····  ███···  bass out
 27   1:36.02  outro      ········  ······  ······  
 28   1:39.71  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
