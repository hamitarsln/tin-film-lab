# Reference breakdown: Fable 5 and Opus 5.5

Method: every frame of both films extracted with ffmpeg (`out/ref/fable/`, `out/ref/opus/`, 490 and 500 frames).
Cuts found by frame difference, hold lengths counted in frames, shape bounds, grain and grid pitch measured on
full-resolution PNGs (`out/ref/full/`). Contact sheets with timestamps are in `out/ref/sheets/`.
The brief's summary ("about 22 materials, about 0.8 s each") undersells Fable: it shows about 55 materials and
the rhythm is not even. The numbers below are measured.

## 1. How long each material holds

### Fable 5 (2160×2160, 24 fps, 20.4 s, loops)
| Section | Time | Holds (frames at 24 fps) | What happens |
|---|---|---|---|
| Withhold | 0.0–7.1 s | 24, 26, 24, 16, 12, 10, 10, 8, 6, 6, 6, 4, 6 | Macro crops of the materials while the camera pulls back. The 5 is never readable; you only see fragments of it (a floral bowl on orange at 5.6 s, flags curving at 6.9 s). Each hold is shorter than the last: 1.0 s down to 0.17 s. |
| Strobe | 7.1–12.8 s | 4, 4, 4, 2, 3, 6, 3, 6, then **3 frames (0.125 s) every cut** for 4.6 s | The full 5 at a fixed scale, a new material every 3 frames (8 a second). About 40 materials, two repeats (constellation, tarot). |
| Settle | 12.8–15.75 s | 4, 7, 18, 20, 25 | Slows down onto three long holds: green petri dish (0.75 s), flower stem (0.83 s), butterflies (1.04 s). |
| Release | 15.75–16.17 s | 10 frames of motion | The last 5's butterflies take off. One red butterfly flies at the lens, fills the frame and wipes into the title. |
| Title | 16.17–18.58 s | 58 | Title card (section 6). |
| Wordmark | 18.58–20.25 s | 40 | Wordmark card, then it dissolves into the first butterfly frame, so the film loops. |

Cuts land on the music grid: 3 frames at 24 fps is 0.125 s, a 16th note at 120 bpm.

### Opus 5.5 (1920×1080, 25 fps, 20.0 s, loops)
| Section | Time | Holds (frames at 25 fps) |
|---|---|---|
| Open | 0–3.3 s | 31, 26, 26 (1.24, 1.04, 1.04 s): Earth's limb, a beaded glass rim, a planet edge |
| Settle | 3.3–8.7 s | 11, 6, 6, then steady 13–15 (0.52–0.6 s): bread crust, sun surface, frost, blueprint, moon, leaf, coral, berries, plate rim, a painted horse jumping |
| Words | 8.7–15.96 s | 8–12 (0.32–0.48 s), then 6–8 (0.24–0.32 s), then 5 (0.2 s) just before the end |
| End | 15.96–20 s | 101 (4.04 s) end card, then the opening horizon rises again (loop) |

Both films: long holds at the start, fastest cuts just before the end card, then a long still card. Fable
strobes harder (0.125 s); Opus keeps a cut readable (0.24–0.6 s) because a word sits on top of it.

## 2. How the shape persists
In both films the shape never moves. It keeps its size and position on every material and only the material
changes. Fable uses four treatments and changes treatment almost every cut, so two neighbouring cuts never feel
the same even when their colours are close.

| Treatment | Fable examples (time) | How it is built | Share |
|---|---|---|---|
| **A. Objects along the outline** | coins 8.2, fish engravings 7.7, stamps on brown card 9.2, mushrooms 11.2, beetles 11.3, leaves on soil 11.7, autumn leaves 12.9, flags 6.9, sticky notes 10.4, butterflies 14.7 | Separate cut-out objects whose centres follow the stroke. Gaps between them are fine (coins have 30–60 px of air between them). Objects are roughly as wide as the stroke or a bit wider and turned to follow it. Only 5–25 % of the frame is covered. No drop shadows; they lie flat, as if scanned together. | ~40 % |
| **B. Texture inside the shape** | garland 7.1, navy floral textile 7.6, blueprint 10.2, constellation 10.1, petri colonies 13.1, map land 9.45 | The shape is cut from a surface and laid on plain ground. The cut edge is the shape's own edge, sharp, with no stroke or bevel. At its best the material's own edge *is* the shape: on the map at 9.45 the 5 is a coastline and the sea and graticule around it stay as ground. | ~25 % |
| **C. Texture with the shape cut out** | deer textile 7.3, blackletter page 7.4, stamp pile 8.6, tarot pile 8.7, city plan 9.6, X-ray circuit 11.4 | The material fills the whole frame edge to edge, and the shape is a flat void in it, either paper (deer, city plan) or a dark card colour (stamps: brown #644939, tarot: dark grey). Objects that touch the void are cut cleanly by the shape's edge. The densest, loudest frames in the film. | ~20 % |
| **D. One object bent into the shape** | snake 8.35, fig branch 8.4, flower stem 8.9, cyanotype seaweed 10.3, red dots on graph paper 10.8, typeset Latin text 7.9 and 9.7 | One continuous thing that is itself the line: a body, a stem, a tube, a line of type set to the outline. It is the most convincing treatment, because the shape seems to belong to the object. | ~15 % |

Opus has one treatment only: the material's real edge *is* the horizon, cropped so its curve sits on the arc.

## 3. Scale and placement
- **Fable**: the 5 is centred (bbox centre at 47–55 % x, 46–51 % y) and fills **74–88 % of the frame height**
  and 50–60 % of its width (measured on coins, snake, mushrooms, beetles, leaves, stamps, flowers). Knockout
  treatments bleed to all four edges; object treatments leave 8–12 % of air at top and bottom.
- **Opus**: the arc's crest sits at **50 % of frame height** at the centre and falls to **60–70 % at the edges**
  (it drops by 15–20 % of the frame height across the width). The material fills everything below it.
- **For Tin**: the mark is wide, not tall (608×374 in its 720 viewBox, aspect 1.63), so width sets the scale.
  The mark spans **77 % of the frame width** (1672 px at 2160, scale 2.75), which makes it 1029 px (48 %) tall and
  centred. Strokes come out about 193 px thick at that scale, and object treatments size their objects to them.

## 4. Ground and grain
- **Fable's grounds are real scanned paper**, usually the plate's own sheet: warm cream (230, 224, 213), grey-beige
  (227, 223, 221) or yellowed (220, 206, 176), with fibres and foxing. Grain is fine: the high-pass standard
  deviation of a flat patch is **0.9–1.9 levels of 255**. Some cuts drop the paper for a dark card (brown
  (100, 73, 60), charcoal (51, 50, 50), black) or the material's own colour (cyanotype blue, yellow).
- **Opus** uses flat skies above the horizon (black, teal, magenta, pale blue, cream) with heavy film grain on
  colour (**~6.3 levels**) and almost none on the black end card.
- **For Tin**, the house rule overrides both: every still sits on **Tin's paper #F5F1E6** with fine code-made grain
  of about 1.5–2.5 levels (Fable's level), seeded, plus faint low-frequency fibre mottling. The one exception
  permitted by the reference is the knockout (C), where the material covers the frame and the paper only shows
  inside the mark.

## 5. How type enters
- **Fable**: no type at all until the title card.
- **Opus**: three words in total, "There's / more to / discover", one word or pair at a time. Each enters
  **whole on a hard material cut** (no letter-by-letter typing), centred, with its **baseline resting on the
  crest of the shape**. A word holds across **4–12 material cuts** (1.7–3.5 s) and changes on a cut. Its colour
  flips with the ground (white on dark, cream on magenta, ink on paper). It grows slowly while it holds:
  "discover" goes from 30 % to 42 % of frame width over 2.6 s. Small at first: "There's" is about 6 % of frame
  width.
- **For Tin**: the same grammar. Whole words on cuts, resting on the mark's top edge (the T-bar and n-arch line at
  y ≈ 174–180 in the viewBox), in Funktional Grotesk, ink on paper.

## 6. How the end card is built
- **Fable**: the last material lifts off the shape (the butterflies fly at the lens) and the closest one wipes
  the frame. Hard cut to a **brand-colour card**: terracotta (204, 107, 87) with paper grain (~3 levels) and a
  **hairline grid at 170 px pitch (12.7 cells across 2160)**, lines only 5–8 levels darker than the ground. Its
  title is a **white serif at 64 % of frame width**, centred. A few butterflies keep flying at the edges for about
  1 s. It holds 2.4 s, then drifts up about 3 % over 6 frames and hard-cuts to the **wordmark card**: off-white
  paper (243, 242, 239) with fibre grain (~4.5 levels) and an **ochre hairline grid at 154 px pitch (14 cells)**,
  2 px lines. The wordmark is a black serif at 66 % of frame width; it rises 3 frames into place, holds 1.7 s,
  shrinks slightly, and dissolves into frame 1.
- **Opus**: the first material comes back as a low horizon glow at the bottom of a near-black frame. The product
  name sits small (20 % of frame width) at centre, then the mark plus wordmark replaces it in the same place. It
  holds 4 s, then the horizon rises into the loop.
- **For Tin**: Fable's two-card build on Tin's own surfaces. First the **Tin mark in ink on paper with a hairline
  grid**, the paper-with-grid card being the wordmark card above in Tin's colours (#F5F1E6, ink grid at
  about 0.10 alpha, 14 cells). Then **`tin.computer`** in Funktional Grotesk, the only lime is a small lime-cta
  cursor block or underline. Terminal blue stays on the terminal beat before it.

## 7. What the board copies
1. One mark, fixed at 77 % width and centred, on every still.
2. A treatment chosen per material from A–D, alternating so neighbours differ. Objects (stamps, matchbooks, trade
   cards, seed packets) get A. Surfaces (pressed tin, newsprint, halftone, billboard paper) get B or C. Things that
   are lines or grids (neon tube, punch card holes, pixels, terminal characters, wood-type letters) get D.
3. The material is never recoloured to make it fit. Edges are crisp, with no shadows, glows or outlines.
4. Tin's paper with fine grain behind everything; knockouts are the one place a material may cover the paper.
5. An end card in Fable's two-card shape, in Tin's colours, with the reserved colours only at the end.

## 8. What the board learned (rounds 1–3)
Section 7 was a starting rule. The board tested it at 2160 px and at 360 px, and changed it here:
- **D (type or lines as the mark) fails for text.** Fable's text 5 works because its strokes are about 350 px wide at
  2160. The Tin mark's strokes are about 193 px wide, which holds only one or two words per line. Search results set
  that way lost the mark at 360 px in every size tried (15–56 px). D survives only where code builds the mark itself:
  18, the mark rasterised onto a pixel grid.
- **Lit signs and dense prints work best as C, not D.** Neon (14), wood type (02), want ads (07), a tin sign (04), a
  torn billboard (12) and a CRT (17) each read instantly as a paper void in the full photograph. That matches Fable's
  stamp pile and blackletter page. Inside the mark (B), the same photos broke into colour fragments.
- **White UI on Tin's paper has no edge.** A white page on #F5F1E6 differs by under 5 L* (100 vs 95.2). The search page (19) takes
  Tin's own 1 px ink frame from DESIGN.md, the one exception to "no outlines": UI surfaces are framed in the product.
- **Object sets need 15 or more distinct objects.** Four covers or two stamps repeated read as wallpaper. With 16–22
  distinct objects (stamps, matchbooks, trade cards), ordered so neighbours differ, they read as a collection.
  Objects whose cross-section matches the stroke width, laid end to end and turned to follow the stroke, keep the
  T, i and n gaps open.
- **Studio photos of 3D objects** (match safes, with their shadows and metal glare) sit badly among flat scans.
  Flat scans belong to the same world as Tin's paper.
- **Final treatment mix (20 stills):** A (objects) 4, B (inside) 9, counting 19 and 20, C (knockout) 6, D (code-built mark) 1.
  Fable is about 40 / 25 / 20 / 15 %.
