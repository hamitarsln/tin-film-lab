// Tin dashboard window for the film: a static rebuild of the real dashboard in refs/product/dashboard
// (index.html shell, app.js renderers, app.css layout), skinned with DESIGN.md tokens (src/ui/dashboard.css).
//
//   const dash = Dashboard(container, { assetBase: '../' });   // assetBase: path from the page to the film root
//   dash.root          the .tin-dash window, 1600 x 1000 native px
//   dash.el            named elements the film animates (arrays where noted)
//   dash.rect(target)  {x, y, w, h} in window-local px (from root's outer top-left), read from the offset chain,
//                      so CSS transforms are ignored. target: an element, an el key, or a dotted path such as
//                      'cards.0', 'planRows.4', 'groups.running'.
//
// Built once. No timers, transitions or randomness: everything that moves is written by the film from seek(t).
// Initial state: the Markdown reader is visible; System and Decisions views are visibility: hidden. Things that
// are "not yet born" inside a view (count chip, running summary, "Approving", the empty state) are hidden too.
// Every string below comes from refs/product (see docs/UI_REFERENCE.md) or docs/SHOTLIST.md's word table.
(function (global) {
  'use strict';

  const LOGO = 'refs/brand/logotype-ink-on-transparent.png';

  // Rail navigation, icons verbatim from index.html:112-149.
  const NAV = [
    { label: 'System', view: 'workflows',
      icon: '<circle cx="3.5" cy="8" r="1.8"/><circle cx="12.5" cy="3.5" r="1.8"/><circle cx="12.5" cy="12.5" r="1.8"/><path d="M5.2 7.2l5.6-3M5.2 8.8l5.6 3"/>' },
    { label: 'Chat', view: 'chat', icon: '<path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/>' },
    { label: 'Decisions', view: 'decisions', icon: '<path d="M3 2.5h10v11H3zM5.5 6h5M5.5 9h3"/>' },
    { label: 'Files', view: 'files', icon: '<path d="M2 4.5h4l1.4 1.5H14v6.5H2z"/>' },
    { label: 'Integrations', view: 'integrations',
      icon: '<rect x="2.5" y="2.5" width="4.6" height="4.6" rx="1"/><rect x="8.9" y="2.5" width="4.6" height="4.6" rx="1"/><rect x="2.5" y="8.9" width="4.6" height="4.6" rx="1"/><rect x="8.9" y="8.9" width="4.6" height="4.6" rx="1"/>' },
  ];

  // Appearance control, index.html:191-207. "system" is the default preference (theme.js), so it is pressed.
  const APPEARANCE = [
    { cls: 'appearance-system', pressed: true,
      icon: '<circle cx="5.5" cy="5.5" r="4.5"/><path d="M5.5 1 A4.5 4.5 0 0 0 5.5 10 Z"/>' },
    { cls: '', pressed: false,
      icon: '<circle cx="5.5" cy="5.5" r="2.35"/><path d="M5.5.5v1.4m0 7.2v1.4M.5 5.5h1.4m7.2 0h1.4M2 2l1 1m5 5 1 1m0-7-1 1M3 8 2 9"/>' },
    { cls: 'appearance-moon', pressed: false,
      icon: '<path d="M8.9 7.7A4.3 4.3 0 0 1 3.3 2.1 4.35 4.35 0 1 0 8.9 7.7Z"/>' },
  ];

  // The plan's ranked systems (SHOTLIST shot 4); row i becomes card i on the drop.
  const PLAN = [
    ['Organic traffic system', 'Run the organic traffic system'],
    ['Product QA system', 'Walk the signup as a new user'],
    ['X', 'Draft for X'],
    ['Creative studio', 'Make a product demo video'],
    ['Paid ads system', 'Launch a Google Ads campaign'],
  ];
  const TOC = ['Systems, ranked', 'Usable in Tin today', 'Proposed scope', 'What Tin would run'];

  // My system cards, in plan order (app.js systemRunCard / systemConfiguredCard, example values).
  const CARDS = [
    // A saved workflow's first run shows as a running card inside its own group (app.js systemGroupEntries);
    // "Running" holds only one-off runs (systemMySystemHtml).
    { group: 'scheduled', run: true, name: 'Run the organic traffic system', key: 'organic.traffic_system', every: 'mon · 09:00',
      state: 'running', last: 'No earlier run', progress: 30,
      detail: 'Working on Audit organic visibility. Started from Claude Code at 14:32.' },
    { group: 'running', run: true, name: 'Walk the signup as a new user', key: 'qa.signup_walkthrough', every: 'manual',
      state: 'running', last: 'No earlier run', progress: 15,
      detail: 'Working on Walk the signup as a new user. Started from Claude Code at 14:32.' },
    { group: 'scheduled', name: 'Draft for X', key: 'social.x_draft', every: 'tue, thu · 09:00',
      state: 'tue 09:00', last: 'No earlier run', actions: [['Skip once', true], ['Pause', false]] },
    { group: 'scheduled', name: 'Make a product demo video', key: 'creative.product_demo',
      every: 'the 1st of every month · 09:00', state: 'sun 09:00', last: 'No earlier run',
      actions: [['Skip once', true], ['Pause', false]] },
    { group: 'available', name: 'Launch a Google Ads campaign', key: 'ads.launch', every: 'manual',
      state: '—', last: 'No earlier run', actions: [['Manual run', true]] },
  ];
  const GROUPS = [['running', 'Running'], ['scheduled', 'Scheduled'], ['available', 'Available']];

  // This week (app.js systemWeekAheadHtml), from today, mon 5.
  const WEEK = [
    { day: 'mon 5 · today', today: true, entry: '14:32 · set up by your coding agent', note: '2 first runs · 2 running' },
    { day: 'tue 6', entry: '09:00 · Draft for X', note: 'in Files' },
    { day: 'wed 7' },
    { day: 'thu 8', entry: '09:00 · Draft for X', note: 'in Files' },
    { day: 'fri 9' },
    { day: 'sat 10' },
    { day: 'sun 11' },
  ];

  function h(tag, cls, parent, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (tag === 'button') e.type = 'button';
    if (parent) parent.appendChild(e);
    return e;
  }

  function svg(parent, cls, viewBox, inner) {
    parent.insertAdjacentHTML('beforeend',
      `<svg${cls ? ` class="${cls}"` : ''} aria-hidden="true" viewBox="${viewBox}">${inner}</svg>`);
    return parent.lastElementChild;
  }

  function hide(e) {
    e.style.visibility = 'hidden';
    return e;
  }

  function Dashboard(container, opts) {
    const base = (opts && opts.assetBase != null) ? opts.assetBase : '../';
    const el = {};

    const root = h('div', 'tin-dash', container);

    // ------------------------------------------------------------------ rail (index.html:87-212)
    const rail = el.rail = h('aside', 'rail', root);
    rail.setAttribute('aria-label', 'Primary navigation');

    const wordmark = el.wordmark = h('div', 'wordmark', rail);
    const logo = h('img', null, wordmark);
    logo.src = base + LOGO;
    logo.alt = 'Tin';

    const shell = h('div', 'project-menu-shell', rail);
    const switcher = el.projectSwitcher = h('button', 'project-switcher', shell);
    const switcherText = h('span', null, switcher);
    el.projectName = h('strong', null, switcherText, 'tin');
    const summary = h('small', null, switcherText);
    el.projectSummaryIdle = h('span', null, summary, 'example');
    el.projectSummaryRunning = hide(h('span', null, summary, 'example · 2 running'));
    svg(switcher, null, '0 0 10 6', '<path d="M1 1l4 4 4-4"/>');

    const navList = h('nav', 'nav-list', rail);
    el.nav = NAV.map((item, i) => {
      const b = h('button', 'nav-item' + (i === 0 ? ' is-active' : ''), navList);
      b.dataset.view = item.view;
      svg(b, null, '0 0 16 16', item.icon);
      h('span', null, b, item.label);
      return b;
    });
    [el.navSystem, el.navChat, el.navDecisions, el.navFiles, el.navIntegrations] = el.nav;
    el.systemCount = h('small', null, el.navSystem);            // "#workflow-count": empty until runs start
    const decisionSlot = h('small', null, el.navDecisions);      // "#decision-count" slot (30 px, right-aligned)
    el.decisionCount = hide(h('span', 'decisions-chip', decisionSlot, '1'));

    h('div', 'rail-spacer', rail);

    const agent = el.agentRail = h('div', 'agent-rail', rail);
    const toggle = h('button', 'agent-rail-toggle', agent);
    const heading = h('span', 'agent-rail-heading', toggle);
    svg(heading, 'agent-rail-terminal', '0 0 14 14', '<path d="M2 3l4 4-4 4M7 11h5"/>');
    h('strong', null, heading, 'Use your coding agent');
    h('span', 'agent-rail-summary', toggle, 'Claude Code · Codex · API');

    const footer = el.railFooter = h('footer', 'rail-footer', rail);
    h('span', 'avatar', footer, 'T');
    h('span', null, footer, 'Tin user');
    const appearance = h('div', 'appearance-control', footer);
    appearance.setAttribute('role', 'group');
    for (const a of APPEARANCE) {
      const b = h('button', null, appearance);
      b.setAttribute('aria-pressed', String(a.pressed));
      svg(b, a.cls, '0 0 11 11', a.icon);
    }
    h('button', 'rail-sign-out', footer, 'Sign out');

    // ------------------------------------------------------------------ main
    const main = el.main = h('main', 'main', root);

    // ------------------------------------------------------------------ Markdown reader (app.css 7809-8128)
    const reader = el.viewReader = h('section', 'dash-view markdown-viewer is-in-app', main);
    const bar = el.readerBar = h('div', 'markdown-context-bar', reader);
    const readerLogo = el.readerLogo = h('span', 'markdown-logo', bar);
    const readerImg = h('img', null, readerLogo);
    readerImg.src = base + LOGO;
    readerImg.alt = 'Tin';
    h('span', 'markdown-context-separator', bar);
    el.readerFilename = h('code', 'markdown-filename', bar, 'GROWTH_ONBOARDING_PLAN.md');
    el.readerFacts = h('code', 'markdown-reading-facts', bar, 'example');
    h('span', 'markdown-context-spacer', bar);
    el.approve = h('button', 'markdown-context-action', bar, 'Approve');

    const readerBody = h('div', 'markdown-viewer-body', reader);
    const layout = el.readerLayout = h('div', 'markdown-reader-layout', readerBody);
    const toc = el.toc = h('nav', 'markdown-section-map', layout);
    const tocInner = h('div', 'markdown-section-map-inner', toc);
    el.tocLinks = TOC.map((label, i) => h('button', 'markdown-section-link' + (i === 0 ? ' is-current' : ''), tocInner, label));

    const doc = el.planDoc = h('article', 'markdown-document', layout);
    el.planTitle = h('h1', null, doc, 'Growth onboarding plan');
    el.planLede = h('p', null, doc,
      'The marketing systems ranked for this business, which are usable in Tin today, a proposed scope, and what Tin would run system by system.');
    el.planH2 = h('h2', null, doc, 'Systems, ranked');
    const list = el.planList = h('ol', null, doc);
    el.planNums = [];
    el.planSystems = [];
    el.planWorkflows = [];
    el.planRows = PLAN.map(([system, workflow], i) => {
      const li = h('li', 'plan-row', list);
      el.planNums.push(h('span', 'num', li, String(i + 1)));
      const line = h('span', 'line', li);
      el.planSystems.push(h('span', 'sys', line, system));
      h('span', 'sep', line, ' · ');
      el.planWorkflows.push(h('span', 'wf', line, workflow));
      return li;
    });

    // ------------------------------------------------------------------ System (app.js renderWorkflows 2034-2114)
    const systemWrap = el.viewSystem = hide(h('div', 'dash-view', main));
    const system = el.systemPage = h('section', 'product-view workspace-view system-view', systemWrap);

    const sysHeader = el.systemHeader = h('header', 'workspace-header system-header', system);
    el.systemTitle = h('h1', null, sysHeader, 'System');
    h('span', 'header-spacer', sysHeader);
    const search = el.searchField = h('div', 'search-field is-registry', sysHeader);
    svg(search, null, '0 0 13 13', '<circle cx="5.5" cy="5.5" r="4"/><path d="M8.5 8.5L12 12"/>');
    const searchInput = h('span', 'search-input', search);
    h('span', 'search-placeholder', searchInput, 'Search…');

    const tabs = el.systemTabs = h('div', 'workflow-sections system-sections', system);
    const tabMine = h('button', 'workflow-section is-active', tabs, 'My system');
    el.tabDot = h('i', null, tabMine);
    el.tabCount = h('span', 'tab-count', tabMine, '2');
    h('button', 'workflow-section', tabs, 'Add workflows');
    h('button', 'workflow-section', tabs, 'Activity');
    el.tabs = [...tabs.querySelectorAll('.workflow-section')];
    el.pace = h('span', 'system-pace', tabs, 'Set up today: 4 roles. First results tue 09:00. · 4 saved workflows · 2 running · 2 runs this month · next tue 09:00');

    const results = el.systemList = h('div', 'system-workflow-list', system);

    const week = el.week = h('section', 'system-week', results);
    week.setAttribute('aria-label', 'This week');
    const weekHeader = h('header', null, week);
    h('strong', null, weekHeader, 'This week');
    h('code', null, weekHeader, 'oct 5 – 11');
    const days = h('div', 'system-week-days', week);
    el.weekDays = WEEK.map((d) => {
      const col = h('div', 'system-week-day' + (d.today ? ' is-today' : ''), days);
      h('code', null, col, d.day);
      if (d.entry) {
        h('span', null, col, d.entry);
        h('small', null, col, d.note);
      } else {
        h('span', 'is-quiet', col, 'quiet');
      }
      return col;
    });
    el.weekFooter = h('p', null, week,
      'Then every week: Run the organic traffic system Mondays, Draft for X Tuesdays and Thursdays. And Make a product demo video on the 1st of every month. Next: Draft for X, tue 09:00.');

    el.groups = {};
    const groupBodies = {};
    for (const [key, title] of GROUPS) {
      const group = el.groups[key] = h('section', 'system-workflow-group', results);
      const gh = h('header', null, group);
      h('strong', null, gh, title);
      h('code', null, gh, String(CARDS.filter((c) => c.group === key).length));
      groupBodies[key] = h('div', null, group);
    }

    el.cards = [];
    el.cardRows = [];
    el.cardTitles = [];
    el.cardDots = [];
    el.progress = [];
    for (const c of CARDS) {
      const running = !!c.run;
      const card = h('article', 'system-workflow-card' + (running ? ' is-running' : ''), groupBodies[c.group]);
      const row = h('div', 'system-card-row is-configurable', card);
      const mark = h('button', 'system-card-mark is-toggle', row);
      if (running) el.cardDots.push(h('span', 'system-card-dot is-running', mark));
      else svg(mark, null, '0 0 10 10', '<path d="M2 3.5 5 6.5 8 3.5"/>');
      const identity = h('button', 'system-card-identity is-toggle', row);
      el.cardTitles.push(h('strong', null, identity, c.name));
      h('code', null, identity, c.key);
      h('code', 'system-card-every', row, c.every);
      h('code', 'system-card-state', row, c.state);
      h('span', 'system-card-last', row, c.last);
      if (c.actions) {
        const actions = h('span', 'system-card-actions', row);
        for (const [label, strong] of c.actions) h('button', 'system-action' + (strong ? ' is-strong' : ''), actions, label);
      }
      if (running) {
        const detail = h('div', 'system-running-detail', card);
        h('span', null, detail, c.detail);
        h('button', 'open-button', detail, 'Open');
        const progress = h('div', 'system-progress is-determinate', card);
        const fill = h('span', null, progress);
        fill.style.width = c.progress + '%';
        el.progress.push(fill);
      }
      el.cards.push(card);
      el.cardRows.push(row);
    }
    el.addWorkflows = h('button', 'system-add-workflow', results, 'Add workflows →');

    // ------------------------------------------------------------------ Decisions (app.js renderDecisions 4829-4873)
    const decWrap = el.viewDecisions = hide(h('div', 'dash-view', main));
    const decisions = el.decisionsPage = h('section', 'product-view decisions-view', decWrap);
    el.decHeader = h('header', 'decisions-header', decisions);
    h('h1', null, el.decHeader, 'Decisions');

    const decLayout = el.decLayout = h('div', 'decisions-layout', decisions);
    const decList = el.decList = h('div', 'decision-list', decLayout);
    const item = el.decItem = h('button', 'decision-list-item is-active', decList);
    el.decMarker = h('span', 'activity-marker is-needs-you', item);
    h('strong', null, h('span', null, item), 'From a useful prompt to work you can rely on');
    h('code', null, item, 'now');

    const card = el.decCard = h('article', 'decision-detail-card', decLayout);
    const cardHeader = h('header', null, card);
    h('span', 'decision-workflow-mark', cardHeader, 'R');
    const cardTitle = h('span', null, cardHeader);
    el.decTitle = h('strong', null, cardTitle, 'From a useful prompt to work you can rely on');
    h('code', null, cardTitle, 'Run the organic traffic system · Just arrived');
    h('button', 'open-button', cardHeader, 'Open');
    const cardBody = h('div', 'decision-detail-body', card);
    h('p', 'decision-summary', cardBody, 'A good skill tells an agent how to do something.');
    h('p', 'decision-note', cardBody,
      'Approved pages reach your site through the delivery setting you choose: a pull request you merge, or a commit to main.');
    const cardFooter = el.decFooter = h('footer', null, card);
    const remember = h('label', 'decision-remember', cardFooter);
    el.decCheckbox = h('span', 'decision-check', remember);
    remember.appendChild(document.createTextNode('Do this for future drafts'));
    el.discardButton = h('button', 'decision-discard', cardFooter, 'Discard');
    const pr = el.prButton = h('button', 'button-secondary pr-button', cardFooter);
    el.prButtonLabel = h('span', null, pr, 'Open a pull request');
    el.prButtonBusy = hide(h('span', null, pr, 'Approving'));
    el.publishButton = h('button', 'decision-approval', cardFooter, 'Publish now');

    const empty = el.decEmpty = hide(h('div', 'decisions-empty', decLayout));
    h('strong', null, empty, 'Nothing needs you.');
    h('span', null, empty, 'When a workflow needs review or an answer, it will appear here.');
    el.openSystemButton = h('button', 'button-secondary', empty, 'Open System');

    // ------------------------------------------------------------------ geometry
    function resolve(target) {
      if (target && target.nodeType === 1) return target;
      if (typeof target !== 'string') return null;
      let v = el;
      for (const part of target.split('.')) v = v == null ? v : v[part];
      return v && v.nodeType === 1 ? v : null;
    }

    function rect(target) {
      const e = resolve(target);
      if (!e) throw new Error(`Dashboard.rect: no element for ${target}`);
      if (e === root) return { x: 0, y: 0, w: root.offsetWidth, h: root.offsetHeight };
      let x = 0, y = 0, n = e;
      while (n && n !== root) {
        x += n.offsetLeft;
        y += n.offsetTop;
        const p = n.offsetParent;
        if (!p || !root.contains(p)) throw new Error(`Dashboard.rect: ${target} is not laid out inside the window`);
        x += p.clientLeft;    // offsets are measured from the parent's padding edge; add its border
        y += p.clientTop;
        n = p;
      }
      return { x, y, w: e.offsetWidth, h: e.offsetHeight };
    }

    return { root, el, rect };
  }

  global.Dashboard = Dashboard;
})(window);
