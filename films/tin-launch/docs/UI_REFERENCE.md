# Tin dashboard: UI reference for the launch film

Source of truth: `refs/product/dashboard/` (index.html, app.css, app.js, content-plan.js, workflow-review.css,
x-posts.css, theme.js), plus `refs/brand/DESIGN.md`, `refs/product/README.md`, `refs/product/workflows.md`.
Citations are `file:line`. app.css, app.js and index.html all live in `refs/product/dashboard/`. All values are
for the **light theme** (`:root`, app.css:60-160). `{braces}` = runtime data. Numbers, times and names in "e.g."
are format illustrations, so label them as examples on screen (CLAUDE.md, Truth).

---

## 0. Read this first

1. **There are two palettes.** The open-source dashboard is warm paper with olive and orange: ink `#26231c`, page
   `#f7f5ef`, accent `#5b7328`, "needs you" orange `#f64800` (app.css:69-108). DESIGN.md describes the hosted "Tin
   Computer" surfaces: ink `#080808` on `#F5F1E6`, terminal-blue `#90D7E4` for the agent, butter for decisions,
   lime for marketing (DESIGN.md:6-45). **app.css never uses terminal-blue, butter or lime.** The dashboard's
   agent surface (`.agent-rail`) is dark ink, not cyan. The film has to choose.
2. **Corners are 4px chips, 8px cards and pill primary buttons** (app.css:157-159); DESIGN.md requires 0 except
   dots (DESIGN.md:247-257). Full list in §8.
3. **Mono chrome is lowercase, not letter-spaced** ("what it works on", "needs you", "started"). UPPERCASE 0.08em
   only appears in the unused `.rail-label` (app.css:1232-1244).
4. **Font.** Geist Sans and Geist Mono, weights 400 and 700 (app.css:1-30, 150-152). Hosted Tin injects a licensed
   stylesheet at `<!--PRIVATE_FONTS_STYLESHEET-->` (index.html:30; README.md:256; app.css:1-2), and its contents
   are not in refs. `refs/brand/fonts/` has Funktional Grotesk Light/Book/Medium and SFMono-Medium. That means
   there is **no 700 weight**, and app.css uses 700 for every bold.
5. **Not in refs, so don't invent it:** markdown-viewer.js (reader bar DOM), workflow-review.js (feedback copy, the
   "request changes" control), x-posts.js (X preview DOM, copy, publish label), content-delivery.js,
   content-draft.js, style-capture.js, output-comparison.*, billing.*, integration logo SVGs, and all server data
   (integration names and `unlocks`, decision titles and explanations, activity summaries, `system_name`).
6. **Legacy code, not reached in this build.** `workflowRunRegions()` builds the needs-you queue, "Live runs" and
   the task card, but it only replaces an existing `#workflow-run-regions` (app.js:2908-2910), which no renderer
   creates. Never called by live code: `renderRegistryWorkflows` (902) and, through it, `workflowEditor` (3482),
   `workflowDraftForm` (3508), `projectWorkflowLedger` (3586), `registryWorkflowCard` (3387); also
   `projectWorkflowCard` (3438). CSS with no renderer: `.decision-feedback` (app.css:4720), `.terminal` (4946),
   `.side-panel`, `.metric*`, `.rail-run*`, `.status-toggle`, `.live-indicator`.
7. At 1920×1080 all the desktop rules apply. The breakpoints at ≤1200, 1100, 900, 820 and 680px do not fire.

---

## 1. Light-theme tokens (app.css:60-160)

| Token | Value | Used for |
|---|---|---|
| `--paper-rail` / `--paper-bg` / `--paper-card` | `#fbf9f4` / `#f7f5ef` / `#fdfcf8` | rail / page, chat strip, reader bar / cards, inputs, secondary buttons |
| `--paper-well` / `--paper-task` / `--paper-deep` | `#efece4` / `#f2efe7` / `#eae6db` | chat input, hovers, chips / task card / deep fill |
| `--ink` / `--ink-secondary` / `--ink-muted` | `#26231c` / `#5f594c` / `#8a8375` | text tiers |
| `--accent-deep` / `--accent-hover` / `--accent-pressed` | `#5b7328` / `#4d6420` / `#42551c` | primary button, running dot, progress (`--accent` `#99af62` is defined but unused) |
| `--accent-text` | `#4f6422` | active nav, links, running state text |
| `--hot` / `--hot-hover` / `--hot-pressed` | `#f64800` / `#d94100` / `#bd3900` | needs-you dots, approval pill, reader links |
| `--bermellon-text` / `--setup-text` / `--danger` | `#be3a00` / `#b73500` / `#be2132` | Discard link / needs-setup text / delete |
| `--on-accent` / `--on-accent-strong` / `--on-hot` | `#fffdf6` / `#fff` / `#fffdf6` | text on filled buttons |
| `--well-ink` / `--well-dark` | `#26231c` / `#0f0d0b` | agent rail + toast / command `pre` |
| `--on-dark` / `-secondary` / `-muted` / `-bright` | `#f6f1e7` / `#b3aa9b` / `#857c6f` / `#fdfcf8` | text on dark |
| `--running-dot` / `--status-idle` / `--status-paused` | `#5b7328` / `#b5ac9c` / `#b7b09f` | status dots |
| `--avatar` / `--avatar-soft` | `#ddd6c8` / `#e6e1d3` | user avatar / Tin chat avatar |
| `--card-border` / `--card-hairline` | `rgb(38 35 26 / 14%)` / `/ 7%` | card edge / inner rules |
| `--paper-border` / `--paper-border-strong` | `rgb(38 35 26 / 12%)` / `/ 24%` | rules / inputs |
| `--nav-active-bg` / `--hot-wash` | `rgb(91 115 40 / 12%)` / `rgb(246 72 0 / 6%)` | active nav / needs-you wash |
| `--shadow-menu` / `--shadow-dialog` | `0 4px 16px rgb(38 35 26/10%)` / `0 24px 80px …/24%` | the only shadows (menus, dialogs) |
| `--rail` / `--chat` / `--work` | `248px` / `680px` / `1120px` | layout widths |

---

## 2. App shell (index.html:86-214)

```html
<div id="app-shell" class="app-shell">                       <!-- flex; min-height 100svh (app.css:891) -->
  <aside class="rail" aria-label="Primary navigation">
    <div class="wordmark"><img src="/assets/tin-logotype-ink.png" alt="Tin"></div>
    <div class="project-menu-shell">
      <button id="project-switcher" class="project-switcher">
        <span><strong id="project-name">{project}</strong><small id="project-summary">{workspace} · {n} running</small></span>
        <svg viewBox="0 0 10 6"><path d="M1 1l4 4 4-4"/></svg></button></div>
    <nav class="nav-list"> …5 × .nav-item… </nav>
    <div class="rail-spacer"></div>
    <div class="agent-rail" id="agent-rail"> … </div>
    <footer class="rail-footer"> … </footer>
  </aside>
  <main id="main" class="main"> …view… </main>
</div>
```

- **`.rail`** (app.css:896-909): sticky, `flex: 0 0 248px`, 100svh, flex column, gap 22px, padding `20px 14px 18px`,
  `#fbf9f4`, border-right `1px rgb(38 35 26/12%)`; `.rail-spacer` is `flex:1` (1558). **`.wordmark`** (911-923):
  padding `2px 8px`, 24px-tall image; `::before` is 37.365×24 (936), the same 1.557 ratio as
  `refs/brand/logotype-ink-on-transparent.png` (657×422, the "Tin" logotype).
- **`.project-switcher`** (959-1013): `11px 12px`, `#fdfcf8`, `1px ink/10%`, radius 8px; `strong` 13.5px/18px bold;
  `small` mono 11px/14px `#8a8375`; 1.5px chevron that rotates 180° when `.is-open`. Placeholders "Loading…" /
  "Connecting to live state" (index.html:103-104); live value `[workspace_name, "{n} running"].join(" · ")`
  (app.js:1223).
- **`.nav-item`** (1164-1225): gap 10px, padding `9px 10px`, radius 4px, `#5f594c` 14px/18px. Hover adds an ink 5%
  background. **`.is-active`**: background `rgb(91 115 40/12%)`, text `#4f6422`, 700. The SVG is 16px with no
  fill, `stroke:currentColor` 1.4px and round caps. The count **`small`** is 30px wide, right-aligned, mono
  11.5px/14px `#8a8375` 400 (it stays muted when active). **There is no badge fill.** The list gap is 2px (1158).

| View | Label | SVG children (verbatim, viewBox `0 0 16 16`) | Count |
|---|---|---|---|
| `workflows` | System (index.html:112-121) | `<circle cx="3.5" cy="8" r="1.8"/><circle cx="12.5" cy="3.5" r="1.8"/><circle cx="12.5" cy="12.5" r="1.8"/><path d="M5.2 7.2l5.6-3M5.2 8.8l5.6 3"/>` | `#workflow-count`: "—", then the running count or empty (app.js:1224-1227) |
| `chat` | Chat (122-127) | `<path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/>` | – |
| `decisions` | Decisions (128-134) | `<path d="M3 2.5h10v11H3zM5.5 6h5M5.5 9h3"/>` | `#decision-count`: waiting items or empty (app.js:1228-1229) |
| `files` | Files (135-140) | `<path d="M2 4.5h4l1.4 1.5H14v6.5H2z"/>` | – |
| `integrations` | Integrations (141-149) | four `<rect … width="4.6" height="4.6" rx="1"/>` at (2.5,2.5) (8.9,2.5) (2.5,8.9) (8.9,8.9) | – |

### 2.1 Agent rail, "Use your coding agent" (index.html:154-185; app.css:1282-1500; app.js:1233-1265, 7536-7567)

```html
<div class="agent-rail [is-open]" id="agent-rail">
  <button id="agent-rail-toggle" class="agent-rail-toggle">
    <span class="agent-rail-heading">
      <svg class="agent-rail-terminal" viewBox="0 0 14 14"><path d="M2 3l4 4-4 4M7 11h5"/></svg>
      <strong>Use your coding agent</strong>
      <svg class="agent-rail-close" viewBox="0 0 10 10"><path d="M1.5 1.5l7 7M8.5 1.5l-7 7"/></svg></span> <!-- close: open only -->
    <span class="agent-rail-summary">Claude Code · Codex · API</span></button>                    <!-- closed only -->
  <div id="agent-rail-body" class="agent-rail-body">                                              <!-- open only -->
    <p class="agent-rail-intro">Paste one line into your terminal. Every workflow here becomes a tool your agent can call.</p>
    <div class="agent-rail-tabs" role="tablist"><button aria-selected="true">Claude Code</button><button>Codex</button><button>API</button></div>
    <pre id="agent-command">{command, below}</pre>
    <div class="agent-rail-actions"><button id="copy-agent-command">Copy</button><a href="/docs">Docs →</a></div>
    <div class="agent-rail-status [is-connected]"><span class="agent-connection-dot"></span><span id="agent-last-used">not connected yet</span></div>
    <div class="agent-rail-footer">27 tools · workflows, runs, files, integrations</div>
  </div>
</div>
```

- **Box**: `#26231c`, text `#f6f1e7`, radius 4px. Closed: padding `11px 12px`, gap 4px; open: 12px, gap 10px.
  Heading 13px/16px 700; terminal icon 13px, stroke 1.5. Summary mono 11px/14px `#b3aa9b`, indented 22px. Intro
  11.5px/16px `#b3aa9b`.
- **Tabs**: `3px 8px`, radius 4px, 11px/14px `#b3aa9b`; selected `rgb(246 241 231/12%)`, `#f6f1e7`, 700.
  **`pre`**: `#0f0d0b`, radius 4px, `8px 10px 10px`, mono **9.5px/15px**, `white-space: pre`.
- **Copy**: 28px min, `6px 12px`, `#5b7328` / `#fff`, 12px/16px 700, radius 4px. "Docs →" 11.5px. **Status**: mono
  10px/12px `#857c6f`; 5px dot with 1px ring, filled `#5b7328` when `.is-connected`. **Footer**: top rule
  `rgb(246 241 231/10%)`, mono 10px/14px `#857c6f`.
- **Last used**: `last used {timeLabel} · {humanize(tool)}`, else "not connected yet" (app.js:1258-1261); example
  only: "last used 5m ago · List projects" (`list_projects`, README.md:41). **`#agent-command`** comes from
  `agentCommandFor(tab)` (app.js:1235-1250); `MCP_URL` is a server value (56-57), hosted as
  `https://app.tin.computer/mcp` (README.md:15-20):

```text
claude:  claude mcp add -t http tin https://app.tin.computer/mcp
         ⏎ # Run /mcp once to sign in. Then, in your project, say:
           # Use Tin to grow my project like a pro!
codex:   codex mcp add tin --url https://app.tin.computer/mcp
         ⏎ # A browser tab opens once to sign in. Then start Codex in
           # your project and say: Use Tin to grow my project like a pro!
api:     POST https://app.tin.computer/mcp
         Authorization: Bearer <token>
```
(⏎ = a blank line.) The rail says `-t http`; BRIEF and README say `--transport http`. After **Copy**, the `pre`
becomes `Copied. Run it, then ask your coding agent: “Use Tin to grow my project like a pro!”` for 4000ms, and the
toast reads "Command copied." (app.js:7553-7567).

### 2.2 Rail footer and main

- **`.rail-footer`** (app.css:1562-1579): gap 10px, padding `14px 8px 0`, top rule ink/10%, `#5f594c` 13px/16px.
  It holds `img.avatar` (26px circle `#ddd6c8`), "Tin user" (index.html:189), `.appearance-control` and "Sign out"
  (12px `#8a8375`). The appearance control (1591-1640) is a 26px ink/6% pill with three 20px pill buttons (pressed
  ink/10%); icons at index.html:191-207.
- **`.main`** (1851) is `flex:1` and the view container. Views (`.product-view`, 2128-2135) are
  `min(100%,1200px)`, centred, padded `30px 40px 60px`.

---

## 3. System view (`data-view="workflows"`, route `/system`), `renderWorkflows()` app.js:2034-2114

```html
<section class="product-view workspace-view system-view">          <!-- flex col, gap 22px (app.css:3388) -->
  <header class="workspace-header system-header">
    <h1>System</h1><span class="header-spacer"></span>
    <div class="search-field is-registry">
      <svg viewBox="0 0 13 13"><circle cx="5.5" cy="5.5" r="4"/><path d="M8.5 8.5L12 12"/></svg>
      <input id="workflow-search" type="search" placeholder="Search…"><button class="search-clear" hidden>✕</button></div>
  </header>
  <div class="workflow-sections system-sections">
    <button class="workflow-section is-active">My system <i></i><span>{running}</span></button>   <!-- i+span only if running -->
    <button class="workflow-section">Add workflows</button><button class="workflow-section">Activity</button>
    <span class="system-pace">{pace line}</span>
  </div>
  <div id="workflow-results" class="system-workflow-list"> week strip + groups + "Add workflows →" </div>
</section>
```

- **h1**: 32px/38px, tracking −0.03em, UA bold (app.css:2155-2160, 3399). **Search**: 240px; input 30px tall,
  padding `6px 33px`, `#fdfcf8`, border ink/22% (focus `#5b7328`), radius 4px, sans 13px; icon 13px, stroke
  `#8a8375` 1.5px (2166-2235, 3403-3423).
- **Section tabs** over a 1px ink/12% rule (2343-2348): `8px 12px 10px`, 13px/16px `#5f594c`, 2px underline;
  **active** underline and text `#26231c`, 700 (2350-2374, 3431). Running `i` is a 6px `#5b7328` dot; count mono
  11.5px `#4f6422` (3437-3448).
- **Pace line**: mono 11px/14px `#8a8375`, right-aligned (3450). `systemPaceLine()` (app.js:2130-2151):
  `{n} saved workflow(s) · {n} running · {n} runs this month · next {ddd HH:MM}` (or `nothing scheduled`); in the
  first 24h it is prefixed with `Set up today: {n} role(s). First results {ddd HH:MM}. · `. Activity tab:
  `live · {n} events · 30 days kept` (2116-2119).

### 3.1 "This week" strip, `systemWeekAheadHtml()` app.js:2570-2668 (CSS 3472-3549)

```html
<section class="system-week" aria-label="This week">
  <header><strong>This week</strong><code>{oct 5 – 11} · {Berlin}</code></header>
  <div class="system-week-days">                                       <!-- 7 equal columns, top rule -->
    <div class="system-week-day is-today"><code>{sun 5} · today</code>
      <span>{14:32} · set up by your coding agent</span><small>{3} first runs · {1 result, 2 running}</small></div>
    <div class="system-week-day"><code>{mon 6}</code><span>{09:00} · {Audit organic visibility}</span><small>in Files</small></div>
    <div class="system-week-day"><code>{tue 7}</code><span class="is-quiet">quiet</span></div>
  </div>
  <p>Then every week: {name} {Mondays}, {name} every day. Next: {name}, {mon 09:00}.</p>
</section>
```

- **Day column**: padding `12px 12px 0 0`, gap 6px; day `code` mono 11px `#8a8375`; **today** `#4f6422` 700 with
  a 7px `#5b7328` dot. Entries 13px/18px ink; "quiet" `#8a8375`; `small` and footer `p` 12.5px/17px `#5f594c`.
- **Landing text**: `in Decisions` for `content.*`, `in Files` otherwise, `last run failed; retry below` after a
  failure (2607-2610). Empty footer: `Nothing is on the calendar yet; the runs above were one-offs.` (2660). Day
  labels are en-US ("sun 5").

### 3.2 Groups and the workflow card

- **Groups.** `systemMySystemHtml()` (app.js:2538-2566) renders **"Running"**, **"Scheduled"** and **"Available"**
  (2558), then `button.system-add-workflow` "Add workflows →" (12.5px 700 `#4f6422`). Header
  `<header><strong>Running</strong><code>{count}</code></header>`: 13px bold + mono 11px `#8a8375`. Cards sit 10px
  apart, groups 14px (app.css:3551-3578, 3750-3760).
- **Empty**: `.empty-list` (1px **dashed** ink/24%, radius 8px, padding 32px) with "Your system is ready for its
  first workflow." and the secondary button "Add a workflow" (app.js:2563).

**Saved (idle) card**, `systemConfiguredCard()` app.js:2470-2497:

```html
<article class="system-workflow-card [is-failed]">
  <div class="system-card-row is-configurable" data-open-system-workflow>
    <button class="system-card-mark is-toggle"><svg viewBox="0 0 10 10"><path d="M2 3.5 5 6.5 8 3.5"/></svg></button>
    <button class="system-card-identity is-toggle"><strong>{name}</strong><code>{workflow_key}</code></button>
    <code class="system-card-every">{mon · 09:00}</code>
    <code class="system-card-state">{mon 09:00}</code>
    <span class="system-card-last">{No earlier run}</span>
    <span class="system-card-actions"><button class="system-action is-strong">Skip once</button><button class="system-action">Pause</button></span>
  </div>
</article>
```

Actions by state (app.js:2477-2486): failed → `Retry` (`.is-retry`) + `Manual run` (strong); paused → `Resume`
(strong) + `Manual run`; scheduled → `Skip once` (strong) + `Pause`; unscheduled → `Manual run` (strong).

**Running card**, `systemRunCard()` app.js:2433-2468. It replaces the saved card while a run is pending or running:

```html
<article class="system-workflow-card is-running">
  <div class="system-card-row is-configurable">                         <!-- padding-bottom 10px when running -->
    <button class="system-card-mark is-toggle"><span class="system-card-dot is-running"></span></button>
    <button class="system-card-identity is-toggle"><strong>{name}</strong><code>{workflow_key}</code></button>
    <code class="system-card-every">{schedule}</code><code class="system-card-state">{running · 2 of 5}</code>
    <span class="system-card-last">{last}</span></div>
  <div class="system-running-detail"><span>{Working on Audit organic visibility}. Started {09:00}, scheduled.</span>
    <button class="open-button">Open</button></div>
  <div class="system-progress is-indeterminate"><span></span></div>     <!-- or is-determinate + style="width:40%" -->
</article>
```

| Cell (app.css) | Size / font | Colour |
|---|---|---|
| card (3580-3587) | 1px `--card-border`, radius 8px, `overflow: clip`, background `#fdfcf8` | – |
| row (3589-3594) | flex, gap 14px, padding `14px 16px` | – |
| mark (3606-3646) | 14px slot. Chevron 10px, stroke 1.5. Running dot 7px filled; pending 7px with 1px ring; failed "×" mono 10px | `#26231c` / `#5b7328` / `#8a8375` |
| identity (3648-3688) | **420px** fixed, baseline row, gap 10px. `strong` 14.5px/18px 700; `code` mono 11px/14px | `#26231c` / `#8a8375` |
| every (3690-3701) | 130px, mono 11.5px/14px | `#5f594c` |
| state (3690-3710) | 140px, mono 11.5px/14px; running card 700 | `#5f594c`; running `#4f6422` |
| last (3712-3718) | flex 1, sans 14px/18px | `#26231c` |
| actions (3720-3748) | gap 14px, 12.5px/16px; strong and retry 700 | `#8a8375` / `#4f6422` / retry `#5f594c` |
| running detail (3762-3775) | padding `0 16px 14px 44px`, 13px/18px | `#4f6422` |
| progress (3777-3795, 3958-3961) | 3px tall, 7px side inset, radius 1.5px. Track `rgb(91 115 40/15%)`, fill `#5b7328`. Indeterminate: a 24% bar sweeping `translateX(-105%)→(430%)` over 1.8s ease-in-out, looping | – |

**Open run detail.** **Open** toggles to "Close" (app.js:2463) and renders `.system-run-detail` (padding 16px,
hairline top) with a 4-column `.system-run-facts` grid, gap 16px (app.js:2394-2423; app.css:3797-3844). Each cell
is a mono 11px muted `code` over a 12.5px/17px 700 `strong`: `started` → `{oct 5 09:00}`; `from` →
`Scheduled | From chat | From Claude Code | From Codex | From the API | Manual`; `status` → progress label; `result`
→ `{artifact title} →` or `—`. Errors render as `p.system-run-error` in `#f64800`.

### 3.3 Formatters (exact output)

| Function (app.js) | Output |
|---|---|
| `systemScheduleLabel` 2207-2214 (card "every") | `manual` · `day · 09:00` · `mon, thu · 09:00` (weekdays cut to 3 lowercase letters) · `the 1st of every month · 09:00` · `the 15th of Jan, Apr, Jul, Oct · 09:00`. **There is no "Every Monday at 09:00" format.** |
| `systemNextLabel` 2216-2222 (card "state") | `{ddd HH:MM}` via `systemDateTime` 2153-2169 (lowercase weekday + 24h, e.g. `mon 09:00`) · `paused` · `—` · `scheduling` · `program ended` · `review revision` · `revision held` |
| `systemLastLabel` 2224-2238 | `No earlier run` · `Failed after {2m 05s}, {oct 3}` · `{result summary}, {oct 3}` · `{artifact title}, {oct 3}` |
| `systemRunProgressLabel` 2253-2271 | `preparing` · `running` · `waiting` · `sending` · `finishing` · `{phase} · {2} of {5}` · `{phase} · {40}%` · `needs you` · `done` · `failed` · `paused` · `stopped` |
| `systemStartedBy` 2273-2280 | `scheduled` · `from chat` · `from Claude Code` · `from Codex` · `from the API` · `manual` |
| `systemRunningSentence` 2282-2301 | `{progress_summary or "Working on {title}."}` minus the trailing period, then `. Started {HH:MM}, scheduled.` or `. Started from Claude Code at {HH:MM}.` |
| `systemConfigurationFact` 2773-2782 | `Next run {mon 09:00}. {4} runs so far, {4} done[, {n} failed][, about {6 minutes} each].` · `Runs on demand. …` |
| `systemRunDuration` 2240 / `waitingLabel` 1165 / `timeLabel` 392 | `45s`, `2m 05s`, `1h 03m` / `now`, `5m`, `2h`, `3d` / `now`, `5m ago`, `2h ago`, locale `Oct 3` |
| content.plan result (content-plan.js:9-17) | `Roadmap saved` · `Batch prepared` · `Revision ready to review` · `No batch due` · `Program finished` |

### 3.4 Editors: saved workflow settings and template setup

**Saved workflow editor.** Clicking a row opens `systemProjectWorkflowEditor()` (app.js:2670-2730), a
`form.system-workflow-card.system-config-form`. It keeps the same row with an up-chevron
`<path d="M2 6.5 5 3.5 8 6.5"/>`, then:

```html
<div class="system-config-body">                                  <!-- flex, hairline top (app.css:3970-3987) -->
  <section><code class="system-config-kicker">what it works on</code> …inputs… <label class="system-setting"><strong>Name</strong><input class="workflow-inline-input"></label></section>
  <section class="system-config-when"><code class="system-config-kicker">when</code> …schedule rows… <p>{config fact}</p></section>  <!-- 360px -->
</div>
<footer class="system-config-footer">
  <button class="button">Save changes</button><button class="button-secondary">Manual run</button><span></span>
  <button class="button-quiet">Pause|Resume</button><button class="button-quiet is-muted">Remove</button></footer>
```

Sections: padding 16px, gap 14px; kicker mono 11px/14px `#8a8375`; `.system-setting strong` 12.5px/16px. Footer
buttons are 30px, `7px 13px`, 12.5px, **radius 4px** (overriding the pill), `.button` text `#fff` (4055-4095).

**Schedule rows**, `workflowScheduleControls()` app.js:3674-3724, with labels above controls (app.css:4015-4045):
`Runs` (`.tin-segmented` `On demand | Daily | Weekly`, plus Monthly only if the workflow allows it); `Day` (a
Monday…Sunday select, default Tuesday); for monthly, `Day` (1st…28th) and `Months` (`Every month`,
`Jan, Apr, Jul, Oct`…); `Time` (104px mono input, default `09:00`, hint `24-hour local time`); `Timezone`. Rows show
and hide via `.is-manual`, `.is-weekly` and `.is-monthly` (app.css:3198-3208).

**Template setup card.** "Set up" in Add workflows opens `systemTemplateSetupCard()` (app.js:1032-1070), a
`form.system-template-card.is-open`.
- **Header** (`.system-template-open-header`): title, description, `{key} · v{version}`, `Cancel`. **Body** grid
  `1fr 360px` (app.css:4431-4447). Left: `what it works on`, `Name`, fields, `connections` (each
  `.system-requirement` row: 8px dot, name over `Connected and ready` / `Connection required`, `Connect →`;
  4449-4489). Right: `when`, schedule rows, `Saving pins v{version}. You can change the schedule later.`
- **Footer**: `Goes to My system when you finish.` + `Set up` (secondary) + `Set up and run now` (button), both
  disabled while a connection is missing.

### 3.5 Add workflows tab, `systemAddWorkflowsHtml()` app.js:1072-1093 (CSS 4257-4421)

```html
<div class="system-template-switch"><button>Saved {n}</button><button class="is-active">All {n}</button></div>
<section class="system-template-group"><header><strong>{system_name}</strong><code>{count}</code></header>
  <div><article class="system-template-card">
    <span class="system-template-identity"><strong>{title}</strong><span class="system-template-description">{description}</span>
      <code>{key}[ · {1 workflow in My system | not set up yet}]</code></span>
    <span class="system-template-actions"><button class="system-quiet-action">Save</button>   <!-- or <span class="system-saved-mark"><i></i>Saved</span> -->
      <button class="button-secondary">Set up</button></span></article></div></section>
```

- **Card**: min-height 92px, padding `14px 16px`, radius 8px; title 14.5px/18px 700; description 13px/18px
  `#5f594c`; code mono 11px `#8a8375`. **Switch**: 30px buttons, `7px 13px`, 12.5px; active ink/8% + 700;
  container border ink/22%, radius 4px.
- **Group names** are server `system_name`, falling back to "Not in a system" (app.js:829). The workflows.md
  headings ("Start here", "Organic traffic system", "Cold outreach system", "Product QA system", "Creative studio",
  "Paid ads system", "X", "General") are the catalog grouping; an exact match with `system_name` can't be verified
  from the client. **Titles** are in workflows.md. Its "(human review)" and "(agent only)" suffixes may come from
  the doc generator, so use the bare titles as BRIEF does.

### 3.6 Activity tab and the /activity view (app.js:2121-2128, 4978-5128; CSS 5055-5296)

```html
<div class="activity-ledger"><section class="activity-day"><h2>{today · oct 5}</h2><div class="activity-day-rows">
  <div class="activity-ledger-entry"><article class="activity-ledger-row is-completed">
    <time>{09:12}</time><span class="activity-marker is-completed"></span><code class="activity-workflow">{organic.audit}</code>
    <p>{server summary}. {Scheduled}.</p><span class="activity-action"><button class="open-button">Open</button></span>
    <button class="activity-ref">{run_3f2a}</button></article></div></div></section></div>
<p class="activity-boundary">30-day activity boundary</p>
```

- **Row**: grid `44px 14px 195px 1fr max-content 70px`, gap 14px, min-height 45px, hairline top. Time mono 11.5px
  tabular `#8a8375`; workflow mono 12px `#5f594c` (needs-you: `#f64800` 700); summary 14px/20px; ref mono 10.5px.
  7px markers: completed `#5b7328`, needs-you `#f64800`, founder a 1.5px ring, failed "×".
- **Activity is not in the nav.** In System it is the third tab. The standalone view has h1 "Activity"
  (26px/32px 700), filters `All | Runs | Needs you | Your edits`, and `live · tailing runs` (mono 11px `#4f6422`,
  6px dot).

### 3.7 Legacy (styled but not reached; see §0.6)

- **`.needs-you-queue`** (CSS 2548-2738; app.js:2951-3000): `--hot-wash`, radius 8px, padding `16px 20px`. Kicker:
  a 7px `#f64800` dot, `needs you · {key} · {run_xxxx}` in mono 11.5px 700 `#be3a00`, and `waiting {2h}`. Then a
  15px/22px `p`, a "Review" hot pill and "Not now".
- **`.live-workflow-runs`** ("Live runs", `{n} active`) wrapping `.workflow-card.live-workflow-run`: background
  `rgb(87 119 37/4%)`, border `/22%`, state `running · via MCP | by schedule | via dashboard` (app.js:3360-3385;
  CSS 2509-2546).
- **`.workflow-card`**: grid `8px minmax(220px,1fr) minmax(100px,150px) minmax(160px,.9fr) auto`, min-height 66px,
  padding `13px 18px`, radius 8px (2740-2812).

---

## 4. Decisions view, `renderDecisions()` app.js:4829-4873 (CSS 4491-4915)

```html
<section class="product-view decisions-view">                          <!-- flex col, gap 22px -->
  <header class="decisions-header"><h1>Decisions</h1><code>nearest deadline {mon 09:00}</code></header>  <!-- code only if a deadline -->
  <div class="decisions-layout">                                       <!-- flex, gap 32px -->
    <div class="decision-list">                                        <!-- 380px -->
      <button class="decision-list-item is-active"><span class="activity-marker is-needs-you"></span>
        <span><strong>{title without "Review: "}</strong></span><code>{2h}</code></button></div>
    <article class="decision-detail-card">
      <header><span class="decision-workflow-mark">{D}</span>
        <span><strong>{output title}</strong><code>{Draft planned content} · {Waiting 2h | Just arrived}</code></span>
        <button class="open-button">Open</button></header>
      <div class="decision-detail-body"><p class="decision-summary">{one sentence}</p><p class="decision-note">{consequence}</p></div>
      <footer><button class="decision-discard">Discard</button><button class="decision-approval">Approve</button></footer>
    </article>
  </div>
</section>
```

- **h1**: 32px/38px, UA bold, no tracking. The code is mono 11px `#8a8375`.
- **List item**: grid `8px 1fr max-content`, gap 12px, padding `11px 10px`, radius 4px; active adds ink/4%.
  `strong` 14px/18px, 400, **700 when active**. Wait time mono 11px muted. Marker is a 7px `#f64800` dot.
- **Card**: `#fdfcf8`, 1px `--card-border`, radius 8px. Header grid `30px 1fr max-content`, `16px 22px`, hairline
  below; the mark is a 30px `rgb(91 115 40/10%)` circle with the workflow title's first letter in `#4f6422` 12px 700.
  Body `20px 22px`, gap 14px; `p` 15px/23px max 560px; notes 13px/19px `#5f594c`. Footer `14px 22px`, hairline top,
  wraps, `justify-content: flex-end`, gap 12px (4745-4813).
- **`.decision-approval`**: `#f64800` / `#fffdf6`, **pill**, padding `7px 12px` (7893-7897 overrides the `11px 14px`
  at 2625), 12.5px/16px 700. Hover `#d94100`; active `#bd3900` + translateY(1px). Blocked: ink/8% background,
  ink/35% text. **`.decision-discard`** is a 12.5px `#be3a00` text button (4816-4824).
- **Footer variants** (`decisionApprovalHtml` 4605-4633). Repository delivery: `Do this for future drafts`
  checkbox, Discard, `Open a pull request` (`.button-secondary`), `Publish now`. Adapted page: Discard + `Publish`.
  Applied revision: Discard + `Keep in Tin`. Proposal: Discard + `Approve`. Default: Discard +
  `{approval_label | Approve changes | Use documents | Approve}`. In flight: `Applying` (4905).
- **Delivery note**: `Approved drafts stay in Tin until GitHub is connected.` + link `Connect GitHub` (4707).
- **Website change card** (4764-4785): mark "W", subtitle `{Audit fix | Planned URL change | Blog index} · {kind}`,
  path and file lists as code. Note:
  `Approving lets Tin publish it: Tin merges the pull request once your repository's required checks pass. Declining keeps it off your site, and Tin won't propose it again.`
  Footer: **Decline** (discard style) + **Approve**.
- **Judgment call card** (4787-4801): mark "?", subtitle `Judgment call · {source}`. Options are `li` rows
  (`8px 10px`, 1px hairline, radius 4px); the suggested one has a `#5b7328` border and `Tin suggests`. Note:
  `Your coding agent answers this with the next website change run, and asks you when it is unsure.`
- **Empty**: `Nothing needs you.` / `When a workflow needs review or an answer, it will appear here.` + secondary
  `Open System` (4845). Min-height 280px, centred.
- **Nav count**: `decisionItems().length` as plain mono text (app.js:1228-1229). There is no butter "N DECISIONS"
  chip; that belongs to the hosted feed (DESIGN.md:101-106).

### 4.1 Feedback composer (workflow-review.css:16-23; the JS is not in refs)

`TinWorkflowReview.mount()` adds it for `content.generate`, `content.public_article`, `social.x_style`,
`style.capture` and apply-on-approval runs (app.js:4467-4500, 4870). `.review-composer`: flex column, gap 16px,
padding 24px, 1px `--paper-border`, radius 8px, `#fdfcf8`; label 17px/22px 700; `p` 13px/18px `#5f594c`; textarea
min 116px, `14px 16px`, `#efece4`, border-strong, radius 4px, 15px/24px; `.review-submit` `#5b7328` / `#fffdf6`,
`9px 14px`, 13px/18px 700, radius 4px. `.is-review-request` is an outlined 4px reader action using the undefined
`--ink-tertiary`. **The label, placeholder and button text are not in refs.** README.md:52 and :117 describe
"request changes" only as a behaviour. The toast after submitting reads
`Revising from your feedback. The previous copy remains readable.` (app.js:4496).

### 4.2 Document reader approve bar (CSS app.css:7809-7967; DOM from markdown-viewer.js, not in refs)

- **`.markdown-context-bar`**: sticky, min-height 45px, padding `14px 32px`, `#f7f5ef`, bottom rule ink/10%, gap
  14px. It holds the logo (18px), a 1×14 separator, the return link (12.5px 700 `#4f6422`), filename (mono 12px),
  reading facts (mono 11.5px muted), a spacer and the hot pill action.
- **Action labels** (app.js:3299-3309): `Approve changes` · `Publish` · `Publish now` · `Approve` · `Use documents`
  · `Approve revision` · `Approve draft`. Secondary: `Discard` or `Open a pull request` (3286-3297).
- **Reading column**: grid `150px 680px`, gap 28px, `translateX(-89px)`. Body 17px/27px; h1 40px/46px 400
  −0.04em; h2 22px/28px 700. Links and the current section are `#f64800`.

### 4.3 X post review (x-posts.css; x-posts.js not in refs, so no copy)

- **Look**: `.x-posts-reader` on `#f7f5ef`; `.x-posts-context` min-height 62px. `.x-posts-button`: `9px 12px`, 1px
  `--paper-border`, radius 4px, 13px/18px `#5f594c`; `.is-primary` `#5b7328` 700; **`.is-publish` `#f64800`** 700.
  Nav current item `#be3a00` 700. `.x-posts-account` 15px/23px with a bold name. `.x-posts-copy` is exact
  `pre-wrap` text. `.x-posts-editor`: padding 24px, radius 8px, `#fdfcf8`, label 17px/22px 700, textarea 116px
  min, 15px/24px.
- **Copy**: "Approve and publish" is **not** in refs. Safe X copy is app.js:6310 (§10) and
  `Drafts are saved in Files. Open a post, edit it, then preview and confirm before publishing.` (app.js:1000).

---

## 5. Chat ("Luna Chat", app.css:311), `renderChat()` app.js:1623-1741 (CSS 1884-2126)

```html
<section class="chat-view"><div class="chat-sheet">                     <!-- sheet: min(100%, 680px) -->
  <div class="chat-thread" id="chat-thread">                          <!-- gap 24px, padding 34px 40px 18px -->
    <div class="empty-chat"><h1>What should we move forward?</h1></div> <!-- empty state only -->
    <article class="chat-turn is-user"><p class="turn-text">{message}</p><time class="turn-time">{09:41}</time></article>
    <article class="chat-turn is-agent"><div class="tin-avatar">t</div><p class="turn-text">{reply}</p>
      <div class="run-receipt"><span class="status-dot is-running"></span>
        <code>{run_3f2a} · {organic.audit} · {running}</code><button class="open-button">Open</button></div></article>
    <article class="chat-turn is-agent"><div class="tin-avatar">t</div>
      <span class="turn-typing"><span></span><span></span><span></span></span></article>   <!-- while sending -->
  </div>
  <form class="chat-composer"><textarea class="composer-field" placeholder="Message Tin…"></textarea>
    <button class="send-button"><svg viewBox="0 0 18 18"><path d="M9 15V4M4.5 8L9 3.5 13.5 8"/></svg></button></form>
</div></section>
```

- **Layout**: `.chat-view` padding `22px 40px 0`; thread as commented above. Empty h1 32px/38px −0.02em, max 520px. User turns are right-aligned with
  120px left padding; text 17px/25px, max 560px; time mono 11px muted. Agent avatar: a 34px `#e6e1d3` circle with
  "t" at 14px 700.
- **Typing**: three 6px `#5f594c` dots at opacity .28 in a 1.15s wave, delays 0/120/240ms, peaking at opacity .82
  and −2px at 30% (1992-2029).
- **Run receipt**: `min(100%,560px)`, `12px 16px`, ink/4%, 1px `--card-border`, radius 8px, mono 11.5px `#5f594c`.
  It shows the **raw** status (`running`, `needs_input`, `succeeded`).
- **Composer**: padding `16px 36px 22px`. Field min-height 46px, `#efece4`, **radius 23px**, `13px 18px`,
  15px/20px. Send is a 46px `#5b7328` circle with an 18px arrow, stroke 1.8.
- **No terminal look or terminal blue in chat.** The only dark, terminal-like surfaces are `.agent-rail pre`
  (§2.1), `.lock-page-line` (§9) and `.toast`. "Luna" appears in the UI only as
  `Ask Luna for a {query} workflow →`, in a legacy empty-search state (app.js:906).

**One-off Codex task** (renderTask app.js:3021-3195; CSS 362-735) is a second conversational surface.
- **Header**: a sticky 54px bar with "← Workflows", `{run_xxxx}` and a status (`review changes`,
  `applying changes`, `needs you`, `finished`, otherwise humanised; 3123-3129). Eyebrow `one-off Codex task`;
  h1 `clamp(30px,4vw,42px)` 700 −0.045em.
- **Transcript**: entries `You` / `Codex` / `Tin` (meta mono 10.5px, text 16px/25px). Events are mono 10.5px with a
  5px `#5b7328` dot. `Codex is working` shows three 5px dots; their `typing-bounce` keyframes are not in app.css.
- **Composer and controls**: placeholders `Steer this task…`, `Answer Codex…`, `Request a change…`,
  `Add direction and resume…`. Buttons `Pause`, `Stop`, `Resume`, `Approve changes`.

**Onboarding (`growth.onboarding`).** No renderer in app.js or content-plan.js shows its form; workflows.md:11-12
says "agent only". Its output `reports/GROWTH_ONBOARDING_PLAN.md` would open in the Markdown reader (§4.2); the
contents are not in refs.

**Content plan (`content.plan`)** is a disclosure list inside the System card, not a table
(`systemContentProgramEditor` app.js:2732-2771; content-plan.js:136-194):

```html
<header class="content-plan-header"><strong>Upcoming work</strong><button class="system-action is-strong">Open full plan ↗</button></header>
<p class="system-config-note">{12} topics · {26} weeks</p><p class="system-config-note">Edits apply only to batches that haven't started.</p>
<div class="system-setting"><strong>Batch</strong>{tin-select: "{Oct 12, 2026} · {2} topics[ · prepared | · reserved]"}</div>
<details class="content-disclosure content-topic"><summary><strong>{topic title}</strong><span>{Ready | Verify before writing | Deferred}</span></summary>
  fields: Topic · Short brief · Action (New page | Update existing page) · Destination URL · "Intent and verification"
  actions: Move to · Defer one batch · Remove topic</details>
<button class="system-action is-strong">Add topic +</button>
<footer class="system-config-footer content-plan-actions"><button class="button">Save upcoming work</button><button class="button-quiet">Refresh program</button></footer>
<details class="content-disclosure content-revision"><summary>Ask for a revision</summary> What should change? · Applies to · Preview revision</details>
```

Topic rows: `14px 0`, hairline top, summary 12.5px/18px. Right column: `Program start`, `Duration`
(`2 weeks`…`6 months`), `Maximum pieces per batch` (`.tin-counter`, 1–3), and
`Capacity is a ceiling, not a quota. No articles are generated or published.` (content-plan.js:36-48).

---

## 6. Run, progress and "waits for you" components

| Thing | Where | Look |
|---|---|---|
| `.status-dot` | app.css:1502-1545 | 7px pill. `running`, `pending` and `provisioning` are `#5b7328` with **breathe** (opacity →.35 at 50%, 1.8s ease-in-out, loops). `succeeded`, `active` and `ready` are `#5b7328` static. `failed` and `needs_input` are `#f64800`. `paused` `#b7b09f`, `stopped` `#8a8375`, idle `#b5ac9c`. |
| Card indicators | app.js:2425-2431 | running = filled 7px dot (**not animated**), pending = 1px ring, failed `×`, idle down-chevron, open up-chevron |
| Progress bar | §3.2 | 3px; determinate width % or indeterminate sweep |
| Timers | §3.1, §3.3 | schedule cell, next cell, "This week", `Skip once` → toast `The next run will be skipped.` |
| Retries | app.js:2478, 4295-4330 | `Retry` → `Retrying` → toast `{workflow-key} is retrying.`; last cell `Failed after {2m 05s}, {oct 3}` |
| Waits for approval | §4 | rail Decisions count, the Decisions card, `in Decisions` in the week strip, status `needs you` |
| Campaign deliveries | app.js:2347-2392; CSS 3875-3944 | Facts `recipients` / `delivery` / `next` / `replies`. Pace `{09:00}–{17:00} {tz} · {90}s apart · up to {40} a day`. Rows `Initial email` / `Follow-up` with `sent {oct 5 09:12}`, `sending`, `scheduled …`, `skipped after reply`, `needs checking`, `failed`, `waiting`. Footer `Review campaign →`. |
| In-flight labels | app.js | `Starting` 3955 · `Saving` 4157 · `Skipping` 4336 · `Pausing`/`Resuming` 4394 · `Removing` 4362 · `Retrying` 4300 · `Approving` 4419 · `Applying` 4905 · `Discarding` 4447 · `Linking…` 7110 |
| Toast | app.css:6812-6835; app.js:492-500 | fixed 24px from bottom-right, max 360px, padding `11px 14px`, `#26231c` / `#fdfcf8`, 13px/18px, radius 4px. Enters from translateY(12px) + opacity 0 over 140ms. **Shown for 3200ms.** |
| Polling | app.js:6532 | 1800ms while runs are active, otherwise 5000ms |

---

## 7. Buttons, chips, toggles (light)

| Class | Box | Type | Colours | Radius | app.css |
|---|---|---|---|---|---|
| `.button` | min-height 34px, padding `8px 15px` | 12.5px/16px **700** | `#5b7328` / `#fffdf6`; hover `#4d6420`; active `#42551c` and 1px down | **pill** | 2237-2280 |
| `.button-secondary` | 34px, `8px 15px`, 1px ink/25% | 12.5px/16px 400 | `#fdfcf8` / `#26231c`; hover `#efece4`, border 35% | 4px | 2282-2296 |
| `.button-quiet` | 34px, `8px 15px` | 12.5px/16px | transparent `#5f594c` (`.is-muted` `#8a8375`) | 4px | 2331, 4093 |
| compact (card and decision footers) | 30px, `7px 13px` | 12.5px | as above | **4px** (overrides the pill) | 4068-4077, 4791-4801 |
| `.open-button` ("Open") | 26px, `4px 11px`, 1px ink/25% | 12px/16px 700 | `#fdfcf8` / `#26231c` | 4px | 2300-2329 |
| `.decision-approval`, `.markdown-context-action` | `7px 12px` | 12.5px/16px 700 | `#f64800` / `#fffdf6`; hover `#d94100` | pill | 2622-2669, 7893 |
| `.button.is-danger` ("Delete project") | as `.button` | 700 | `#be2132` / `#fff` | pill | 6675-6683 |
| `.send-button` | 46×46 | – | `#5b7328` / `#fffdf6` | pill | 2101-2126 |
| `.system-action` / `.is-strong` / `.is-retry` | text only | 12.5px/16px 400/700/700 | `#8a8375` / `#4f6422` / `#5f594c` | – | 3727-3748 |
| `.integration-connect` ("Connect") | `6px 13px` | 12px 700 | `rgb(91 115 40/12%)` / `#4f6422` | 4px | 6505-6515 |
| `.integration-disconnect` / `-done` | `7px 13px` | 12px | danger text + `/40%` border / `#f7f5ef` + ink/25% border | 4px | 6775-6795 |
| `.filter` (`.is-active`) | `6px 12px` | 12.5px (700) | transparent `#5f594c` → ink/9% `#26231c` | 4px | 2383-2400 |
| `.tin-segmented` / `.tin-segment` | 1px ink/18% border; segments min-width 48px, height **28px**, padding `0 11px`, ink/9% dividers | mono 11.5px/16px (active 700) | `#fdfcf8` `#8a8375` → active ink/9% `#26231c` | 4px | 3044-3080 |
| `.tin-select` trigger / menu / option | 30px `6px 9px`, ink/20% / 4px padding + `--shadow-menu` / 30px | mono 12.5px / 11.5px | selected option 700 with a 5px `#5b7328` marker | 4 / 4 / 3px | 3082-3196 |
| `.tin-counter` | grid `30px 54px 30px`, height 28px | mono | buttons `#5f594c` | 4px | 3210-3247 |
| `.workflow-inline-input` | 30px, `6px 9px`, ink/20% (focus `#5b7328`) | mono 12.5px (content plan uses sans) | `#fdfcf8` → `#fffefa` | 4px | 2912-2944 |
| `.appearance-control` | 26px pill, 3px pad, 20px buttons | – | ink/6%; pressed ink/10% | pill | 1591-1640 |
| `.system-template-switch` | 30px, `7px 13px` | 12.5px (active 700) | `#fdfcf8`; active ink/8% | 4px | 4264-4290 |

**Chips:** `.content-file-chip` (`#efece4`, 12.5px, radius 4px; 4244-4246) · `.system-saved-mark` (5px `#5b7328`
dot + "Saved" 12px; 4401-4412) · `.integration-badge` (24px tile, 1px ink/16%, mono 10px 700, 16px logo, radius
4px; 6357-6381) · `.decision-workflow-mark` (30px circle, §4).

---

## 8. Typography in use, and every radius

**Families**: `--sans` "Geist Sans", "Helvetica Neue", Arial, sans-serif; `--mono` "Geist Mono", "SFMono-Regular",
Consolas, monospace (app.css:150-152). The body is 400 `#26231c` on `#f7f5ef`, antialiased (857-865). Weights in
use are **400 and 700** (600 once, at 503).

| Role | Size / line-height / weight / tracking | app.css |
|---|---|---|
| View h1: System / Integrations / Files | 32/38, UA bold, −0.02em (System −0.03em) | 2155-2160, 3399, 5314 |
| View h1: Decisions / Activity | 32/38 UA bold, no tracking / 26/32 700 −0.02em | 4529, 5063 |
| Chat empty h1 / lock page h1 | 32/38 bold −0.02em / 26/32 **400** −0.01em | 1940, 8852 |
| Reader h1 / h2 / body | 40/46 400 −0.04em / 22/28 700 −0.01em / 17/27 | 7980-7994, 7959 |
| Task h1 · dialog h2 | clamp(30px,4vw,42px) 700 −0.045em lh 1.03 · 22/28 −0.02em | 439, 6560 |
| Card titles | 14.5/18 700 (system and template cards); 14/18 bold (decision, integration) | 3671, 4347, 4626, 6425 |
| Group headers | 13/16 bold + mono 11/14 count | 3561-3572 |
| Body copy | decision 15/23 · chat 17/25 · descriptions 13/18 · notes 12.5/18 | 4662, 1965, 4363, 4047 |
| Nav / switcher | 14/18 (active 700) / 13.5/18 | 1164, 979 |
| Mono labels | 11/14 standard · 11.5/14 card cells and segments · 10.5/14 small kickers · 10/12–14 agent status and footer · 9.5/15 command `pre` | passim |

**Every border-radius used** (app.css line numbers unless noted):

| Radius | Components |
|---|---|
| **0** (none set) | rail, nav strip, week strip, activity rows, section tabs, reader bar |
| **1.5px** | `.system-progress` and its fill (3782, 3789) |
| **3px** | `.tin-select-option` 3165, Markdown inline `code` 8042 |
| **4px**: shell | `.nav-item` 1171, `.agent-rail` 1288, agent tabs 1387, `pre` 1406, Copy 1450, `.toast` 6821 |
| **4px**: buttons | `.button*` base 2245, `.open-button` 2310, `.filter` 2389, `.activity-filter` 5085, compact footer buttons 4074/4778/4798, template `.button-secondary` 4395, `.integration-connect` 6509, disconnect/done 6779 |
| **4px**: controls | `.search-field input` 2195, `.workflow-inline-input` 2918, `.tin-segmented` 3049, `.tin-select-trigger` 3102, `.tin-select-menu` 3152, `.tin-counter` 3215, `.system-template-switch` 4269 |
| **4px**: small boxes | `.campaign-deliveries` 3884, `.content-file-chip` 4244, `.system-requirement` 4463, `.decision-list-item` 4562, `.judgment-options li` 4901, `.integration-badge` 6368, `.integration-setup-prompt` 6526, `.integration-project-option` 6589; workflow-review.css textarea, `.review-submit`, `.is-review-request`; x-posts.css buttons, status, textarea, select, media |
| **6px / 10px / 23px** | `.project-menu-item` 1044 / `.project-menu` 1027 / `.composer-field` 2092 |
| **8px** | `.project-switcher` 966, `.run-receipt` 2039, `.needs-you-queue` 2555, `.empty-list` 3379, `.workflow-card` 2749, `.workflow-config-form` 2820, `.system-workflow-card` 3582, `.system-template-card` 4330, `.decision-detail-card` 4608, `.integration-card` 6337, `.files-state-panel` 5453, dialog 6542, `.connect-footer` 8533, `.review-composer`, `.review-comparison`, `.x-posts-editor`/`-notes`; `.workflow-ledger-footer` is `0 0 8px 8px` (3317) |
| **50% / 999px**: dots | `.status-dot` 1507, `.agent-connection-dot` 1478, `.system-card-dot` 3630, today dot 3524, tab dot 3442, `.needs-you-dot` 2576, `.activity-marker` 5256, `.integration-state-mark` 6443, `.tin-select-marker` 3190, saved dot 4411 |
| **50% / 999px**: circles | `.avatar` 1587, `.tin-avatar` 1986, `.decision-workflow-mark` 4644, `.send-button` 2106, typing dots 2004 |
| **999px**: pills | `.appearance-control` 1598/1611, **`.button` 2254**, **`.decision-approval`/`.markdown-context-action` 2627**, `.lock-page-tabs` 8892/8899, `.lock-page-line` 8918, scrollbar thumb 843 |

---

## 9. Integrations view, `renderIntegrations()` app.js:6112-6234 (CSS 6280-6535)

```html
<section class="product-view integrations-view">
  <header class="workspace-header"><h1>Integrations</h1><span class="header-spacer"></span>
    <label class="search-field"><svg …/><input id="integration-search" placeholder="Search integrations…"></label></header>
  <div class="filters integration-filters"><button class="filter is-active">All {n}</button><button class="filter">Connected {n}</button>
    <button class="filter">Needs you {n}</button><button class="filter">Available {n}</button></div>
  <div class="integration-list">                                        <!-- gap 8px -->
    <article class="integration-card is-connected"><div class="integration-card-row">
      <span class="integration-badge [is-monochrome]"><img src="/assets/integrations/github.svg"></span>
      <span class="integration-identity"><strong class="integration-name">{name}</strong><code class="integration-key">infra.github</code></span>
      <span class="integration-state-mark is-connected"></span>
      <span class="integration-primary">{selected repo | account label}</span><span class="integration-health">ready for workflows</span>
      <button class="integration-row-action">Configure</button></div></article>
    <article class="integration-card is-available"><div class="integration-card-row">…badge…identity…
      <span class="integration-state-mark is-available"></span><span class="integration-unlocks">would unlock {unlocks · joined}</span>
      <button class="integration-connect">Connect</button></div></article>
  </div>
</section>
```

- **Card states** (6334-6347, 6437-6459). Available: transparent with a **hollow** 6px mark (1.5px ink/30% ring).
  `.is-connected`: `#fdfcf8` with a filled `#5b7328` mark. `.is-needs-setup`: border `rgb(246 72 0/28%)`, mark
  `#f64800`, text `#b73500`, action "Set up", primary `Choose a repository` / `Choose a Search property` /
  `Choose a PostHog project`. `.is-expanded`: border ink/28%.
- **Row**: min-height 48px, padding `12px 18px`, gap 12px. Identity 280px (name 14px/18px, key mono 10.5px).
  Primary mono 11.5px at 240px. Health mono 11.5px muted. Action 12px, 70px, right-aligned.
- **Health strings** (6199-6254). General: `ready for workflows`, `checked {5m ago}`, `setup required`,
  `needs you`. X: `reading only`, `ready to publish approved posts`, `reconnect required`. Custom API:
  `access verified`, `saved · not verified`. Google Ads: `accept Tin's request in Google Ads`,
  `billing missing in Google Ads`.
- **Expanded** (6322-6405): rows `Account` / `Repository` / `Access` / `Unlocks` (label 13px, 140px; value mono
  12.5px). GitHub Access: `selected repositories · Contents + Pull requests write`. X Access:
  `✓ Read your own posts · ✓ Publish posts you approve · ○ Upload media for approved posts`. Footer:
  `connected {2h ago} · via OAuth · checked {5m ago}` + `Disconnect` + `Done`.
- **Keys and logos** (app.js:6181-6189): `analytics.gsc`, `infra.github` and `infra.github_user` (GitHub is
  monochrome), `workspace.google`, `ads.google`, `payments.stripe`, `analytics.posthog`. `social.x` has **no
  logo** and falls back to the server `badge` text. `custom.api` shows "Custom API" with badge "API"
  (app.js:112-120). The SVG files are not in refs.
- **Display names are server data.** README.md:124-134 names them: Google Search Console, GitHub App, GitHub
  account, Google Workspace, Google Ads, Stripe, PostHog, X.
- **Resource dialog** (index.html:215-228; app.js:7005-7129; CSS 6536-6660): 480px wide, radius 8px,
  `--shadow-dialog`, ink/28% blurred backdrop. Title `Choose the repository for {project}`; copy
  `Tin opens pull requests and delivers approved pages here.` Radio rows are 52px with radius 4px; the selected
  row gets an accent wash and a 15px filled radio. Buttons `Later` (quiet) and `Link`; while linking, `Linking…`.
- **Agent-requested connect page** (`renderConnectRequest`, app.js:6053-6083). h1 `Connect for {project}`. Intro:
  `Your agent asked for these {2} connections. Each takes about a minute in the browser; GitHub also asks which repository.`
  The `.connect-footer` (`#efece4`, radius 8px, 14px/20px) reads
  `{1} of {2} connected. When you are done, go back to your agent and say: connected.`, or **`All connected.`**
  followed by ` Go back to your agent and say: connected.`
- **Lock page** (app.js:1269-1321; CSS 8835-8971). h1 `Set up Tin from your coding agent` (26px/32px 400,
  centred). Body: `Your coding agent already knows your repo and how you write. Connect Tin, and it will pick the workflows that fit and get the first ones running for you in a few minutes.`
  then **`Browser setup is not available yet.`** Tabs are a `#efece4` pill group ordered
  `Codex | Claude Code | API`, with 36px pill buttons; selected is `#26231c` on `#fdfcf8`, 700. The
  **`.lock-page-line`** is a 56px pill, `#141210`, text `#f6f1e7`, mono 14px/18px, with a `$` prompt in `#857c6f`
  followed by the first command line, e.g. `codex mcp add tin --url https://app.tin.computer/mcp`, and a 28px copy
  icon (app.js:1297).

---

## 10. Real UI strings safe to show (verbatim)

Each string is one backtick span (several strings themselves contain " · "). `{…}` is runtime data.

| Strings | Where | Source |
|---|---|---|
| `System` `Chat` `Decisions` `Files` `Integrations` | nav | index.html:119, 126, 132, 139, 148 |
| `Use your coding agent` `Claude Code · Codex · API` | agent rail | index.html:160, 165 |
| `Paste one line into your terminal. Every workflow here becomes a tool your agent can call.` | agent rail | index.html:168 |
| `Claude Code` `Codex` `API` `Copy` `Docs →` `not connected yet` | agent rail tabs, actions, status | index.html:170-172, 176-177, 181 |
| `27 tools · workflows, runs, files, integrations` | agent rail footer | index.html:183 |
| `Connecting to live state` `Sign out` | switcher, rail footer | index.html:104, 209 |
| `My system` `Add workflows` `Activity` `Search…` | System header | app.js:2068-2070, 2063 |
| `This week` `quiet` `today` `in Files` `in Decisions` | week strip | app.js:2664, 2639, 2640, 2609 |
| `{HH:MM} · set up by your coding agent` | week strip, first day | app.js:2626 |
| `Running` `Scheduled` `Available` `Add workflows →` | My system groups | app.js:2558, 2565 |
| `Skip once` `Pause` `Resume` `Manual run` `Retry` `Open` `Close` `No earlier run` | workflow card | app.js:2478-2486, 2463, 2225 |
| `Your system is ready for its first workflow.` `Add a workflow` | System empty | app.js:2563 |
| `Save changes` `Remove` `what it works on` `when` `connections` | editor | app.js:2722, 2726, 1054, 1060, 1057 |
| `Runs` `On demand` `Daily` `Weekly` `Monthly` `24-hour local time` | schedule rows | app.js:3700, 3694-3697, 3718 |
| `Set up` `Set up and run now` `Goes to My system when you finish.` | template setup | app.js:1066-1067, 1065 |
| `Connected and ready` `Connection required` `Connect →` | requirements | app.js:1043-1044 |
| `Save` `Saved` `Remove from saved` | template card | app.js:966, 965 |
| `Nothing has happened yet.` `live · tailing runs` `30-day activity boundary` | activity | app.js:2124, 4994, 2127 |
| `Nothing needs you.` `When a workflow needs review or an answer, it will appear here.` `Open System` | decisions empty | app.js:4845 |
| `Approve` `Discard` `Open a pull request` `Publish now` `Publish` `Keep in Tin` `Do this for future drafts` | decision footer | app.js:4628, 4596, 4622-4623, 4602, 4615, 4620 |
| `Decline` `Tin suggests` `Just arrived` `Waiting {2h}` | decision cards | app.js:4781, 4796, 4669 |
| `Approved drafts stay in Tin until GitHub is connected.` `Connect GitHub` | decision note | app.js:4707 |
| `What should we move forward?` `Message Tin…` | chat | app.js:1628, 1643 |
| `one-off Codex task` `Codex is working` `Approve changes` | task | app.js:3059, 3068, 3144 |
| `Search integrations…` `All` `Connected` `Needs you` `Available` | integrations header | app.js:6144, 6149-6152 |
| `Connect` `Configure` `Disconnect` `Done` `ready for workflows` `Publish posts you approve` | integration card | app.js:6230, 6228, 6401-6402, 6214, 6300 |
| `Drafting never posts to X. Tin publishes only the exact post you preview and confirm.` | X integration | app.js:6310 |
| `Set up Tin from your coding agent` `Browser setup is not available yet.` | lock page | app.js:1286, 1288 |
| `Workflow saved and scheduled.` `Workflow added and started.` `Changes saved.` | toasts | app.js:4093, 4092, 4242 |
| `Schedule paused.` `Schedule resumed.` `The next run will be skipped.` `Command copied.` | toasts | app.js:4403, 4347, 7561 |
| `Copied. Run it, then ask your coding agent: “Use Tin to grow my project like a pro!”` | toast and agent `pre` | app.js:1318, 7564 |
| `Draft approved. Publishing it to the repository now.` `Draft approved. GitHub PR delivery will follow; nothing is merged.` | toasts | app.js:4972-4973 |
| `Approved. Tin publishes it with the next website change run.` `Discarded. It stays in Files, and nothing was published.` | toasts | app.js:4821, 4941 |
| `Approval accepted. Applying the exact reviewed changes.` `Revising from your feedback. The previous copy remains readable.` | toasts | app.js:3250, 4496 |
| `GitHub connected with repository write access.` | toast | app.js:6963 |
