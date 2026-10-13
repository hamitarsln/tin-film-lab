# Style

Gate 3, part 1. The look and the motion rules every shot follows. Tokens come from refs/brand/DESIGN.md; UI
structure and copy come from refs/product/dashboard/ (see docs/UI_REFERENCE.md).

## Two sources, one skin

The dashboard in refs/product/dashboard/ is the real app.tin.computer UI: its markup, layout, component
dimensions and copy are the ground truth for what appears on screen. Its open-source stylesheet ships Geist and
8 px card corners as defaults; hosted Tin serves the licensed brand font, and DESIGN.md is the brand's own rule
book (Funktional Grotesk, sharp corners, ink and paper, terminal blue for the agent). So the film rebuilds the
dashboard's **structure and copy** and skins it with **DESIGN.md tokens**: Funktional Grotesk for words, SF Mono
for chrome, radius 0 on panels, cards, buttons and tiles, pill radius only on status dots. Where app.css uses its
olive accent for a primary button or the active nav, the film uses DESIGN.md's inverted ink (ink-void fill,
paper-light text), the same treatment DESIGN.md gives an active filter chip. Nothing else is restyled.

## Palette

| Role | Token | Value | Where |
|---|---|---|---|
| Field | paper | #F5F1E6 | the page everything sits on |
| Cards, panels | paper-light | #FEFDFB | dashboard surfaces, the plan, cards |
| Banding | paper-warm / paper-pale | #ECE6D5 / #F9F7F0 | rail, inputs, wells |
| Muted labels | paper-ink | #78715F | mono chrome, field names |
| Ink | ink-void | #080808 at 0.84 alpha for text; solid for the wordmark, rules and inverted buttons | everything a person reads |
| Hairlines | line-neutral / rose-line-soft | rgba(0,0,0,0.18) / #EED2D4 | dividers / card borders |
| Agent surface | terminal-blue / deep | #90D7E4 / #63AEBF | the coding agent's terminal, nothing else |
| Running, success | primary-green / deep | #66DC9D / #2FA069 | run dots, "up", the approved state |
| Decisions | butter / butter-deep | #EBDE9A / #C9A227 | the decisions count, a run waiting for review |
| Call to action | lime-cta | oklch(0.90 0.22 120) | the end card's command block, nowhere earlier |

**One accent per scene:** hook, ink only (the blue strip is the agent arriving); agent and plan, terminal blue;
system, green; decision, butter; end card, lime. Never two saturated accents competing in one frame, with one
exception that is the story: on the drop the blue agent surface folds away while green runs take over.

No gradients, no shadows, no glows, no blur, no grain. Depth comes from hairlines and paper banding.

## Type

One typeface for words: **Funktional Grotesk** (Book 400, Medium 500; Light 300 for large secondary lines). One
mono for chrome and commands: **SF Mono Medium**. Sizes are at 1920×1080 in screen space; UI sizes are native
CSS px before the camera zoom.

| Use | Face | Size / leading / tracking |
|---|---|---|
| Hook captions | FG Medium | 136 px / 1.02 / −0.035em |
| Scene captions | FG Medium | 104 px / 1.02 / −0.03em |
| Caption second line (quiet) | FG Book | 104 px, ink at 0.42 alpha |
| End card logotype "Tin" | refs/brand/logotype-ink-on-transparent.png (the dashboard rail's wordmark) | 150 px tall |
| End card command | SF Mono | 72 px, two lines, on lime (≈13 px tall on a 360 px phone) |
| End card URL / tagline / agents | FG Medium / Book / Book | 104 px / 42 px / 34 px |
| Terminal text | SF Mono | 26 px native, zoomed ×1.6–2.0 in close-ups |
| Dashboard body / titles | FG Book / Medium | 14–17 px native, zoomed in close-ups |
| Header-mono / label-caps chrome | SF Mono, UPPERCASE | 11 / 10 px native, 0.14em / 0.1em tracking |

Readability floor: any word that carries the story is at least 64 px tall on screen at the moment it must be read
(≥12 px on a 360 px phone frame), and stays on screen for at least one bar (2 s). UI words that are only texture
may be smaller; the camera pushes in whenever a UI word matters (a workflow name, Approve, the count).

## Layout

- 1920×1080 stage, 120 px side margins, a 12-column grid (column 120 px, gutter 24 px).
- Captions sit top-left in the caption band (top y 96) once the UI is on screen; the UI's top edge is held at y 392
  and the UI may bleed off the bottom edge as a deliberate crop. Never centered, never framed, no corner labels.
- Tin's window is outlined by a 1 px line-strong (0.35 ink) edge, soft enough not to read as a rule in close-ups.
- The page is one continuous sheet of paper; the camera travels over it. The agent's terminal, the dashboard and
  the end card are all on that sheet.
- The page is written against `layout(W, H)` (positions from the frame size), and the stage renders identically at
  960×540 and 1920×1080.

## Motion rules

1. **Springs, not tweens.** Every move is `Motion.sp` or `Motion.track`. Snappy: buttons, chips, toggles, cursor
   presses. Base: cards, panels, camera. Heavy: big type, the wordmark, the drop pull-back. Playful is not used.
2. **Nothing fades in.** Entrances are typed (captions, commands), masked rises (a line rises out of its own
   baseline), grows from an origin (a surface grows out of a caret, a colour floods out of a button), or morphs
   (a plan row becomes a workflow card). Opacity is only used to retire something already pushed away.
3. **Captions are typed word by word**, each word landing on a beat or half-beat, rising 0.12em with a snappy spring;
   a block caret rides the end of the line. Commands type character by character with a seeded human rhythm
   (bursts per token, a short hesitation before flags and the URL).
4. **The camera always drifts.** A per-scene push of 1.00 → 1.04, a slow seeded drift of a few pixels, and the next
   scene starts at the zoom the last one ended on. Captions push (1.00 → 1.035) and drift on their own so the type
   is never frozen. Scene-to-scene moves use the base spring; the drop pull-back uses a heavy spring with a 4%
   overshoot.
5. **One continuous take.** No cuts: caption caret → agent surface → plan → workflow cards → the decision → the
   lime flood → the end card. Each element is born from the previous one.
6. **The beat is visible but small.** Running dots pulse on the beat (scale up to 1.18). Type hits on a downbeat get
   a 2% punch. Envelopes (`M.env`) only breathe the drift, never the layout.
7. **The cursor is a person.** It travels on springs, arrives a quarter-beat early, presses on the beat (0.88 scale
   for 60 ms), and the pressed control changes state on that same frame.
8. **No dead beats.** Something new every 2–4 s; holds are carried by the drift, a typing caret or pulsing dots.
9. **No CSS transitions or animations, no timers, no randomness.** All state is computed from t in `seek(t)`.

## What I take from the named style

*AI-lab launch film:* a light page, one typeface, black ink, sentences typed word by word, the product's real UI
as the star, generous white space, no gloss. The calm is in the frame, not in the music.

*Apple keynote bumper:* everything lands on the beat, one huge moment on the drop, a camera with mass that
overshoots and settles, a single colour pop at the end (lime), and the name and the way in held long enough to
read twice.
