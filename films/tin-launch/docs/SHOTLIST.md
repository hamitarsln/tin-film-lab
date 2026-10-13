# Shot list

Gate 3, part 2. Swish Swed cut, 16 bars, 120 BPM: beat = 0.500 s, bar = 2.000 s, film bar n starts at
(n − 1) × 2.000 s. Positions are written bar.beat (9.1 = bar 9 beat 1 = 16.0 s; 7.3.5 = halfway between beats 3
and 4 of bar 7). Phrases start on bars 1, 5, 9, 13. The drop is 9.1. The code turns every cue through `T(bar, beat)`.

One continuous take on one sheet of paper. World layout (native px, before the camera):
- **Terminal** (the agent's surface, terminal blue): x 0, y 0, 1680 × 1000 until 7.1.5, then it narrows to 1412
  wide (so a 180 px band of it stays at the left of the drop framing).
- **Tin dashboard window**: x 1460, y 0, 1600 × 1000: rail 248 px + main view. Born at 7.1.5 out of the plan path.
- Captions live in screen space in the caption band (top y 96) whenever UI is on screen, with a slow push and a
  seeded drift of their own. Every UI framing keeps the UI's top edge at stage y 392, so captions never sit on UI.
  (Revised in stills rounds 1–3; see docs/REVIEW_LOG.md.)

Example data: the example project is Tin itself (dogfooding), shown as project "tin" in workspace "example", so every
value the agent fills and every title in the plan comes from refs/product/. The workspace name "example" is the
on-screen label that marks it as illustrative.

---

## Shot 1 · Hook · bars 1–2 (0.0–4.0 s)

**Words** (FG Medium 128 px, two lines, left at x 120, typed word by word with a block caret):
- C1 "Your agent ships the product." Your 1.1 · agent 1.1.5 · ships 1.2 · the 1.2.5 · product. 1.3 (done 1.0 s)
- C2 "Tin lets it run the marketing." Tin 1.4 · lets 1.4.5 · it 2.1 · run 2.1.5 · the 2.2 · marketing. 2.3 (done 3.0 s)

**UI.** Paper. The top of the terminal sits at the bottom of frame as a terminal-blue band (screen y 920–1080,
x 120–1800) with a `$` prompt and an ink caret blinking on the beat. Nothing else.

**Camera.** z 1.20 → 1.24 slow push on the terminal strip (band top at y 820), seeded drift; the caption block pushes
1.00 → 1.035 on its own.

**Music.** The sweep down on 1.1 carries the first word; words land on the kick and the off-beats.

**Grows from.** The first frame. Hook in under 2 s: by 1.0 s the full first sentence is on screen; Tin is named at 1.5 s.

## Shot 2 · One line · bars 2.4–4 (3.5–8.0 s)

**Transition 2.4 → 3.1.** On 2.4 the caption's caret stops and the terminal's caret starts blinking at the `$`
prompt (the hand-off lands on the beat; an earlier version flew the caret across and it read as a flicker) while the
camera tilts down (base spring) so the terminal's top edge rises to y 392; C1 and C2 spring up into the caption band
and settle at 102 px (scale 0.8). The captions stay (C1 + C2 read for 4–7 s in total).

**UI (terminal, SF Mono 24 px native, z 1.0).**
- 3.1 → 3.4.5 types `$ claude mcp add --transport http tin https://app.tin.computer/mcp` with a human rhythm
  (bursts per token, a pause before `--transport` and before the URL).
- 4.1 Enter (line break, the prompt line settles).
- 4.2 → 4.4 types the first prompt `› Use Tin to grow my project like a pro!`

**Camera.** F1: terminal top at screen y 360, z 1.00 → 1.03, drifting.

**Music.** Breakdown, steady kick. Enter on the bar-4 downbeat.

## Shot 3 · The agent reads the code · bars 5–6 (8.0–12.0 s)

**Words.** C1/C2 retire upward on 5.1 (pushed out by C3, 0.1 s stagger). C3 "No forms. It reads your code."
typed No 5.1 · forms. 5.1.5 · It 5.2 · reads 5.2.5 · your 5.3 · code. 5.3.5.

**UI (terminal).**
- 5.1 Enter on the prompt. The agent's reply streams 5.1 → 5.2:
  `I'll read the repository first, then help you choose a starting plan.`
- 5.2.5 → 5.4.5 Tin's own files tick past on sixteenths, dim ink, one row:
  `README.md  AGENTS.md  docs/architecture.md  docs/workflows.md  workflow_packages/  src/tin_lite/settings.py`
- 6.1 the tool call line `tin › Start here: onboard this business`
- 6.1.5, 6.2.5, 6.3.5, 6.4.5 one input per beat, name in paper-ink, value typed in ink:
  `product_url        https://tin.computer`
  `system_repository  github.com/tin-computer/tin`
  `system_docs        docs/README.md`
  `priority           organic growth`

**Camera.** Same framing, push continues to 1.05, drift. **Music.** Build: the kick thins from bar 6.

**Grows from.** The same terminal; lines append below the prompt like a real session.

## Shot 4 · Tin writes the plan · bars 7–8 (12.0–16.0 s)

**Words.** C3 retires; C4 "Tin writes the plan." Tin 7.1 · writes 7.1.5 · the 7.2 · plan. 7.2.5.

**UI.**
- 7.1 a last terminal line appears: `→ reports/GROWTH_ONBOARDING_PLAN.md` (real output path of the onboarding plan).
- 7.1.5 the path underlines; a paper-light rectangle grows out of the path's box (base spring) into the Tin
  dashboard window to the right while the terminal narrows to 1100 px. Inside the window: the rail (Tin logotype,
  project switcher "tin / example", nav System · Chat · Decisions · Files · Integrations, "Use your coding agent /
  Claude Code · Codex · API", footer) and the Markdown reader.
- Reader bar: Tin logotype · `GROWTH_ONBOARDING_PLAN.md` · `example` · spacer · **Approve**.
- The plan writes itself, one line per half-beat from 7.2: h1 "Growth onboarding plan"; h2 "Systems, ranked" (the
  lede paragraph is omitted so the plan fits a closer framing); then
  five numbered rows 7.3 · 7.3.5 · 7.4 · 7.4.5 · 8.1:
  1 Organic traffic system · Run the organic traffic system
  2 Product QA system · Walk the signup as a new user
  3 X · Draft for X
  4 Creative studio · Make a product demo video
  5 Paid ads system · Launch a Google Ads campaign
- 8.1 the cursor enters from lower right, travels on a spring, arrives on Approve at 8.3 (hover state).
- Bar 8 is the held breath: the bass is gone, the riser climbs, the camera creeps toward Approve.

**Camera.** 7.2 is an arc, not a whip: the camera pulls out to z 0.8 (the agent's terminal and Tin's window side by
side) while easing right across a bar, then pushes in to the whole reader, logo to Approve (z ≈ 1.24); bar 8 pushes
in to the plan and Approve (z ≈ 1.4), the window's top edge held at y 392. (The arc keeps screen speeds under
13 px per blur subframe; the whip doubled every word.)

**Grows from.** The path line in the terminal.

## Shot 5 · Drop: a whole marketing system · bars 9–10 (16.0–20.0 s)

**9.1 ◆ (16.000 s).** The cursor presses Approve on the slam. In the same frame:
- the camera springs back (mass with a 4% overshoot) from z ≈ 1.4 to z 0.92 on Tin's window, the agent's blue band
  at the left edge;
- each plan row's workflow name flies (snappy, on sixteenths) to its card's title while the card wipes open downward
  from its title row; the rest of the plan lifts away; the System view builds around them: h1 "System", tabs
  "My system · Add workflows · Activity", the "This week" strip, groups "Running", "Scheduled", "Available";
- the nav's System count and the project line switch to the running state.

**Words.** C4 retires on 9.1; C5 slams in with the heavy spring: "A whole marketing system." (A 9.1 · whole 9.1.5 ·
marketing 9.2 · system. 9.2.5), then a second line "60 workflows." (60 9.3 · workflows. 9.3.5). Hold to 10.3.

**UI after the drop (real formats and grouping from app.js, example values).**
- Running (one-off runs only): **Walk the signup as a new user** `qa.signup_walkthrough` · `manual` · `running`, with
  "Working on Walk the signup as a new user. Started from Claude Code at 14:32." and a progress bar.
- Scheduled: **Run the organic traffic system** `organic.traffic_system` · `mon · 09:00` · `running` (its first run, shown
  inside its own group), "Working on Audit organic visibility. Started from Claude Code at 14:32."; **Draft for X**
  `social.x_draft` · `tue, thu · 09:00` · `tue 09:00` · Skip once · Pause; **Make a product demo video**
  `creative.product_demo` · `the 1st of every month · 09:00` · `sun 09:00`.
- Available: **Launch a Google Ads campaign** `ads.launch` · `manual` · `—` · Manual run.
- Pace line: "Set up today: 4 roles. First results tue 09:00. · 4 saved workflows · 2 running · 2 runs this month ·
  next tue 09:00". This week: `mon 5 · today` "14:32 · set up by your coding agent" / "2 first runs · 2 running";
  `tue 6` and `thu 8` "09:00 · Draft for X" / "in Files"; other days "quiet"; footer "Then every week: Run the organic
  traffic system Mondays, Draft for X Tuesdays and Thursdays. And Make a product demo video on the 1st of every
  month. Next: Draft for X, tue 09:00."
- Running dots pulse on every beat; progress bars creep forward.

**10.2 (18.5 s), the session ends.** The agent's blue band at the left edge rolls up like a blind (base spring,
~0.5 s) and is gone. The dots keep pulsing.

**Camera.** Hold with a slow push 9.1 → 10.3; from 10.3 a move to the rail, "This week" and the running cards
(z 1.2, window's left edge at x 120).

## Shot 6 · Between sessions, then a decision · bars 10.3–12 (19.0–24.0 s)

**Words.** C5 retires on 10.3. C6 "Running between sessions." (Running 10.3 · between 10.3.5 · sessions. 10.4).
C6 retires on 11.4. C7 "Review before anything ships." (Review 11.4 · before 11.4.5 · anything 12.1 · ships. 12.1.5).

**UI.**
- 11.1 the Decisions count in the rail ticks to `1` (snappy pop) and its marker turns butter.
- 11.1.5 the cursor leaves the resting point and travels to the Decisions nav item; press 11.3. The main view
  switches to Decisions: h1 "Decisions", a list item (butter marker, bold) "From a useful prompt to work you can
  rely on" with `now`, and the decision card:
  header mark "R" · **From a useful prompt to work you can rely on** · `Run the organic traffic system · Just arrived`
  · Open; summary "A good skill tells an agent how to do something."; note "Approved pages reach your site through
  the delivery setting you choose: a pull request you merge, or a commit to main."; footer ☐ "Do this for future
  drafts" · Discard · **Open a pull request** · Publish now.
- 12.1 the cursor presses **Open a pull request**; the button reads `Approving` on that frame.
- 12.3 the approval becomes the colour: lime floods out of the `Approving` button's own rectangle (shot 7).

**Camera.** 11.3.5 eases over half a bar from the System framing to the Decisions list and card together (z ≈ 1.42,
window top at y 392), then a slow push.

## Shot 7 · End card · bars 13–16 (24.0–32.0 s)

**12.3 (23.0 s).** Lime floods out of the approved button's rectangle (base spring, sharp corners, analytically
motion-blurred edges, full frame by 12.4). Lime is used nowhere earlier in the film.
- 13.1 (24.0 s, the phrase start) the Tin logotype lands in ink on the lime (heavy spring, masked rise), x 120,
  150 px tall.
- 13.3 the lime contracts back into the command block (base spring), paper returns around it, and the command types
  inside the block in SF Mono 72 px on two lines: `claude mcp add --transport http tin` / `https://app.tin.computer/mcp`.
- 14.1 the tagline types under the logotype (FG Book 42 px): "Open-source marketing system, designed for coding agents."
- 14.3 "tin.computer" types (FG Medium 104 px) under the command block.
- 15.1 "Works with Claude Code, Codex and Cursor." types on the URL's baseline, right-aligned to the block.
- 15–16 hold: drift and a 1.00 → 1.03 push; the command's caret blinks on the beat; the music fades over bar 16.

---

## Sync sheet (key moment → bar.beat → seconds, all on the grid)

| Moment | Bar.beat | s |
|---|---|---|
| First word | 1.1 | 0.000 |
| Tin named | 1.4 | 1.500 |
| Camera tilts to terminal | 2.4 | 3.500 |
| Command starts / Enter | 3.1 / 4.1 | 4.000 / 6.000 |
| Prompt Enter, C3 | 5.1 | 8.000 |
| Tool call, inputs | 6.1, 6.1.5 … 6.4.5 | 10.0 … 11.75 |
| Plan path, window born, C4 | 7.1 | 12.000 |
| Cursor on Approve | 8.3 | 15.000 |
| **Approve click, System, C5** | **9.1** | **16.001** |
| Session ends (band rolls up) | 10.2 | 18.500 |
| C6 | 10.3 | 19.000 |
| Decisions count `1` | 11.1 | 20.000 |
| Click Decisions | 11.3 | 21.000 |
| C7 | 11.4 | 21.500 |
| Click "Open a pull request" | 12.1 | 22.000 |
| Lime floods out of the button | 12.3 | 23.000 |
| Logotype, end card | 13.1 | 24.001 |
| Command, URL, last line | 13.3, 14.3, 15.1 | 25.0, 27.0, 28.0 |
| Fade, hold | 16.1–end | 30.0–32.0 |

## Every on-screen word, checked

| Words | Source |
|---|---|
| Your agent ships the product. / Tin lets it run the marketing. | BRIEF one-liner ("A coding agent already ships the product; plug in Tin and the same agent starts running the marketing") |
| `claude mcp add --transport http tin https://app.tin.computer/mcp` | BRIEF facts; README Quick Start |
| Use Tin to grow my project like a pro! | BRIEF facts; README |
| I'll read the repository first, then help you choose a starting plan. | README setup conversation |
| README.md, AGENTS.md, docs/architecture.md, docs/workflows.md, workflow_packages/, src/tin_lite/settings.py, docs/README.md | Files Tin's README links to (the example project is Tin) |
| github.com/tin-computer/tin, https://tin.computer | README (clone URL, website) |
| Start here: onboard this business; product_url, system_repository, system_docs, priority | workflows.md (growth.onboarding title and inputs) |
| organic growth | README setup conversation ("If organic growth is the priority") |
| No forms. It reads your code. | BRIEF differentiator 1 ("fills Tin's onboarding plan from the codebase, so you don't fill in forms") |
| reports/GROWTH_ONBOARDING_PLAN.md | workflows.md (growth.onboarding_plan output) |
| Tin writes the plan. / Growth onboarding plan / Systems, ranked | workflows.md ("Tin writes the plan: the marketing systems ranked…") |
| Organic traffic system, Product QA system, X, Creative studio, Paid ads system | workflows.md section names |
| Run the organic traffic system, Audit organic visibility, Walk the signup as a new user, Draft for X, Make a product demo video, Launch a Google Ads campaign | BRIEF facts; workflows.md |
| organic.traffic_system, qa.signup_walkthrough, social.x_draft, creative.product_demo, ads.launch | workflows.md keys |
| Set up today: 4 roles. First results tue 09:00. · 4 saved workflows · 2 running · 2 runs this month · next tue 09:00; Then every week: … Next: Draft for X, tue 09:00.; sun 09:00 | app.js systemPaceLine, systemWeekAheadHtml, systemNextLabel formats with example values |
| Approve, System, Chat, Decisions, Files, Integrations, Use your coding agent, Claude Code · Codex · API, My system, Add workflows, Activity, Search…, This week, quiet, today, set up by your coding agent, in Files, Running, Scheduled, Available, Skip once, Pause, Manual run, No earlier run, running, manual, Working on … Started from Claude Code at …, Just arrived, Open, Discard, Open a pull request, Publish now, Do this for future drafts, Approving, Tin user, Sign out | docs/UI_REFERENCE.md (real dashboard strings and formats) |
| A whole marketing system. | BRIEF differentiator 2 |
| 60 workflows. | BRIEF facts; README line 7 |
| Running between sessions. | BRIEF differentiator 3 ("Work that continues between sessions") |
| Review before anything ships. | BRIEF differentiator 4 |
| From a useful prompt to work you can rely on (article title) / A good skill tells an agent how to do something. | README section heading and its first sentence (example draft about Tin) |
| Approved pages reach your site through the delivery setting you choose: a pull request you merge, or a commit to main. | README "Review before delivery" |
| Open-source marketing system, designed for coding agents. | BRIEF facts; README line 3 |
| tin.computer | BRIEF facts |
| Works with Claude Code, Codex and Cursor. | BRIEF facts |
| Times and dates (14:32, 09:00, mon 5, tue 6, nov 1, oct 5 – 11) and counts in UI chrome (2 first runs, 2 running, 1) | Example UI state for the "example" workspace, in the dashboard's real formats; no claims |

No customer names, logos, metrics, testimonials or quotes. No number appears outside the facts table except UI
state of the example workspace.
