# PlaceIt World 02 (Mixkit #725)

Lily J · 1:36.00 · 102.00 BPM · 4/4

## Grid

- One beat = 0.5883 s. One bar = 2.3530 s. A 4-bar phrase = 9.412 s.
- Bar 1 starts at 0.059 s.
- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × 0.5883. Every bar start is listed below; use those, not arithmetic over the whole song.
- Grid fit: 100% of 154 detected beats sit within 40 ms of the grid (16.5 ms RMS). Bar 1 placed by the downbeat model, agreement 100%.

## Sections

| Section | Bars | Time | Level | Energy | Low | High | Trend |
|---|---|---|---|---|---|---|---|
| intro | 1–4 (4) | 0:00.06–0:09.47 | low | 0.33 | 0.31 | 0.28 | +0.11 |
| groove | 5–8 (4) | 0:09.47–0:18.88 | mid | 0.49 | 0.35 | 0.30 | +0.12 |
| groove | 9–16 (8) | 0:18.88–0:37.71 | high | 0.72 | 0.96 | 0.36 | -0.10 |
| drop | 17–36 (20) | 0:37.71–1:24.77 | peak | 0.94 | 0.97 | 0.93 | +0.08 |
| outro | 37–41 (5) | 1:24.77–1:36.53 | low | 0.37 | 0.37 | 0.36 | -0.95 |

Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.

## Sync points

- 0:02.41 bar 2: bass in (+10.2 dB)
- 0:04.76 bar 3: break, the bass drops out for 1 bar(s) and slams back in at bar 4 (0:07.12, +8.5 dB)
- 0:09.47 bar 5: break, the bass drops out for 1 bar(s) and slams back in at bar 6 (0:11.82, +8.1 dB)
- 0:14.18 bar 7: break, the bass drops out for 1 bar(s) and slams back in at bar 8 (0:16.53, +8.9 dB)
- 1:20.06 bar 35: riser (+3.1 dB in the highs) into bar 37
- 1:29.47 bar 39: bass out (-16.7 dB)

Strongest hits (sharpest transients, snapped to the beat when within 60 ms):

0:00.06 @1.1 (1.00), 0:28.88 @13.2 (0.52), 0:41.53 @18.3.5 (0.53), 0:50.94 @22.3.5 (0.62), 0:53.29 @23.3.5 (0.56), 0:55.06 @24.2.5 (0.54), 1:00.35 @26.3.5 (0.58), 1:04.47 @28.2.5 (0.58), 1:05.06 @28.3.5 (0.52), 1:06.53 @29.2 (0.53), 1:09.76 @30.3.5 (0.59), 1:13.88 @32.2.5 (0.59), 1:15.94 @33.2 (0.54), 1:23.29 @36.2.5 (0.59), 1:23.88 @36.3.5 (0.54), 1:25.36 @37.2 (0.58)

@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.

## Bar by bar

```
bar   time     section    energy    low      high     events
  1▶  0:00.06  intro      ██······  ······  ██····  
  2   0:02.41  intro      ███·····  ███···  █·····  bass in
  3   0:04.76  intro      ██······  █·····  ██····  break→4
  4   0:07.12  intro      ███·····  ███···  █·····  
  5▶  0:09.47  groove     ████····  █·····  ██····  break→6
  6   0:11.82  groove     ████····  ███···  █·····  
  7   0:14.18  groove     ████····  █·····  ██····  break→8
  8   0:16.53  groove     ████····  ████··  █·····  
  9▶  0:18.88  groove     ██████··  ██████  ███···  
 10   0:21.24  groove     █████···  ██████  █·····  
 11   0:23.59  groove     ██████··  ██████  ███···  
 12   0:25.94  groove     █████···  ██████  █·····  
 13┊  0:28.30  groove     ██████··  ██████  ███···  
 14   0:30.65  groove     █████···  ██████  █·····  
 15   0:33.00  groove     ██████··  ██████  ███···  
 16   0:35.35  groove     █████···  ██████  ██····  
 17▶  0:37.71  drop       ███████·  ██████  ██████  
 18   0:40.06  drop       ███████·  ██████  █████·  
 19   0:42.41  drop       ███████·  ██████  █████·  
 20   0:44.77  drop       ███████·  ██████  ██████  
 21┊  0:47.12  drop       ████████  ██████  ██████  
 22   0:49.47  drop       ████████  ██████  █████·  
 23   0:51.83  drop       ████████  ██████  ██████  
 24   0:54.18  drop       ████████  ██████  ██████  
 25┊  0:56.53  drop       ████████  ██████  ██████  
 26   0:58.88  drop       ████████  ██████  █████·  
 27   1:01.24  drop       ████████  ██████  ██████  
 28   1:03.59  drop       ████████  ██████  ██████  
 29┊  1:05.94  drop       ████████  ██████  ██████  
 30   1:08.30  drop       ███████·  ██████  █████·  
 31   1:10.65  drop       ████████  ██████  ██████  
 32   1:13.00  drop       ████████  ██████  ██████  
 33┊  1:15.36  drop       ████████  ██████  ██████  
 34   1:17.71  drop       ████████  ██████  █████·  
 35   1:20.06  drop       ███████·  ██████  ██████  riser→37
 36   1:22.42  drop       ████████  ██████  ██████  
 37▶  1:24.77  outro      ████████  ██████  ██████  
 38   1:27.12  outro      ███████·  █████·  █████·  
 39   1:29.47  outro      ········  ······  ······  bass out
 40   1:31.83  outro      ········  ······  ······  
 41┊  1:34.18  outro      ········  ······  ······  
```

▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.
