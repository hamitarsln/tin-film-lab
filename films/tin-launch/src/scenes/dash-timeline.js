// Tin's window on the sheet (bars 7–13). Static DOM from src/ui/dashboard.js; this file only moves it in time.
(function () {
  const { T, BEAT, M, css, el, springP, clamp, keys } = F;
  const WIN = { x: 1460, y: 0, w: 1600, h: 1000 };
  const tBorn = T(7, 1.5), tDrop = T(9, 1);
  let frame, inner, D, E, R = {};

  function build(world, assetBase) {
    frame = el('div', '', world); frame.id = 'dashFrame';
    inner = el('div', '', frame); inner.id = 'dashInner';
    D = Dashboard(inner, { assetBase });
    E = D.el;
    // On the drop each plan row's workflow name flies to its card's title (the plan becomes the system).
    flyers = E.cardTitles.map(n => {
      const f = el('span', 'dash-flyer', D.root);
      f.textContent = n.textContent;
      return f;
    });
  }
  let flyers = [];

  const cls = (node, name, on) => { if (node && node.classList.contains(name) !== on) node.classList.toggle(name, on); };
  const local = n => (typeof n === 'string' ? D.rect(n) : D.rect(n));

  function measure() {
    // The film omits the plan's lede so the ranked rows fit a closer framing (round 1, readability).
    if (E.planLede) E.planLede.style.display = 'none';
    // Window-local rects of everything we aim at or morph between, measured once (layout is static).
    for (const k of ['approve', 'navDecisions', 'navSystem', 'prButton', 'decCard', 'decList', 'decHeader', 'agentRail', 'decisionCount', 'planTitle', 'toc'])
      R[k] = local(k);
    R.rows = E.planRows.map(n => local(n));
    R.cards = E.cards.map(n => local(n));
    R.wf = E.planWorkflows.map(n => local(n));
    R.titles = E.cardTitles.map(n => local(n));
    R.cardRows = E.cardRows.map(n => local(n));
    R.logo = local('readerLogo');
    R.week = local('week');
    R.readerDoc = { x: R.planTitle.x, y: R.planTitle.y, w: 680, h: 400 };
  }
  const windowRect = () => ({ ...WIN });
  function worldRect(name) {
    const r = name === 'readerDoc' ? R.readerDoc : name === 'lastRow' ? R.rows[R.rows.length - 1] : (R[name] || local(name));
    return { x: WIN.x + r.x, y: WIN.y + r.y, w: r.w, h: r.h };
  }

  // Appear on a beat: visibility on, settle 10 px up with a snappy spring (UI building itself, never a fade).
  function appear(node, t, t0, dy = 10) {
    const on = t >= t0;
    css(node, { visibility: on ? '' : 'hidden', opacity: '1', transform: `translateY(${(on ? (1 - springP(t - t0, 'snappy')) * dy : dy).toFixed(2)}px)` });
  }
  // Leave: move up and retire (only things already moving may fade).
  function leave(node, t, t0, dy = -40) {
    if (t < t0) return false;
    const u = springP(t - t0, 'snappy');
    css(node, { transform: `translateY(${(dy * u).toFixed(2)}px)`, opacity: (1 - clamp((t - t0) / 0.14)).toFixed(3),
      visibility: t - t0 > 0.16 ? 'hidden' : '' });
    return true;
  }

  function update(t) {
    // The window grows out of the plan path in the terminal (base spring), clipping the dashboard inside it.
    const born = t >= tBorn;
    const frameAt = tt => {
      if (tt < tBorn) return Terminal.pathRect(tBorn);
      const p = Terminal.pathRect(tBorn);
      const u = springP(tt - tBorn, 'base');
      return { x: p.x + (WIN.x - p.x) * u, y: p.y + (WIN.y - p.y) * u, w: p.w + (WIN.w - p.w) * u, h: p.h + (WIN.h - p.h) * u };
    };
    // Containers hide with display (a child's explicit visibility would show through a hidden parent).
    // The unfolding sheet's edges carry their own motion blur (F.blurRect), in world px.
    css(frame, { display: born ? 'block' : 'none', visibility: '', zIndex: '3' });
    const fr = born ? F.blurRect(frame, frameAt(t), frameAt(t - F.SUBDT)) : WIN;
    // The frame's own 1 px edge sits on the window's edge once landed (inner offset by the border).
    css(inner, { left: (WIN.x - fr.x - 1).toFixed(2) + 'px', top: (WIN.y - fr.y - 1).toFixed(2) + 'px' });
    if (!born) return;

    const dropped = t >= tDrop;
    const tDec = T(11, 3);
    const inDecisions = t >= tDec;

    // Reader: the plan writes itself, line by line, from 7.2.
    // On the downbeat the plan's chrome cuts hard; only the workflow names travel on (the flyers).
    css(E.viewReader, { visibility: '', display: dropped ? 'none' : '' });
    const readerParts = [[E.readerBar, T(7, 2)], [E.toc, T(7, 2)], [E.planTitle, T(7, 2)], [E.planLede, T(7, 2.5)], [E.planH2, T(7, 2.5)]];
    for (const [n, t0] of readerParts) appear(n, t, t0);
    const rowT = [T(7, 3), T(7, 3.5), T(7, 4), T(7, 4.5), T(8, 1)];
    E.planRows.forEach((n, i) => appear(n, t, rowT[i], 8));
    cls(E.approve, 'is-hover', t >= T(8, 2.5) && t < tDrop + 0.11);
    cls(E.approve, 'is-pressed', Cursor.isPressed(t, tDrop));

    // System: builds around the plan rows on the drop. Rows fly into cards, staggered by sixteenths.
    css(E.viewSystem, { visibility: '', display: dropped && !inDecisions ? '' : 'none' });
    if (dropped) {
      appear(E.systemHeader, t, tDrop, 14);
      appear(E.systemTabs, t, tDrop + BEAT / 4, 14);
      appear(E.week, t, tDrop + BEAT / 2, 14);
      E.weekDays.forEach((d, i) => appear(d, t, tDrop + BEAT / 2 + (i * BEAT) / 8, 10));
      const g = E.groups;
      appear(g.running, t, tDrop, 0); appear(g.scheduled, t, tDrop, 0); appear(g.available, t, tDrop, 0);
      // Each card wipes open downward from its title row as its flyer lands, on sixteenths.
      E.cards.forEach((c, i) => {
        const t0 = tDrop + (i * BEAT) / 4;
        const tOpen = t0 + 0.1, tLand = t0 + 0.26;
        const h = R.cards[i].h, top = R.cardRows[i].h;
        const u = springP(t - tOpen, 'base');
        const cut = t < tOpen ? h : (h - top) * (1 - u);
        css(c, { visibility: t >= tOpen ? '' : 'hidden', transform: 'none', clipPath: `inset(0px 0px ${cut.toFixed(2)}px 0px)` });
        css(E.cardTitles[i], { visibility: t >= tLand ? '' : 'hidden' });
      });
      flyers.forEach((f, i) => {
        const t0 = tDrop + (i * BEAT) / 4, tLand = t0 + 0.26;
        const a = R.wf[i], b = R.titles[i];
        const u = springP(t - t0, 'snappy');
        const s0 = 17 / 14.5, sc = s0 + (1 - s0) * u;
        // Size by font-size (a paint property), not a transform: small layers with a changing scale keep stale rasters.
        css(f, { display: t < tLand ? 'block' : 'none', left: (a.x + (b.x - a.x) * u).toFixed(2) + 'px',
          top: (a.y + (b.y - a.y) * u).toFixed(2) + 'px', fontSize: (14.5 * sc).toFixed(3) + 'px', lineHeight: (18 * sc).toFixed(3) + 'px' });
      });
      // Running dots breathe on the beat; progress creeps forward.
      const pulse = M.pulse(t, { every: 'beat', decay: 9 });
      (E.cardDots || []).forEach(d => css(d, { transform: `scale(${(1 + 0.22 * pulse).toFixed(4)})` }));
      if (E.tabDot) css(E.tabDot, { transform: `scale(${(1 + 0.22 * pulse).toFixed(4)})` });
      const prog = [[0.30, 0.62], [0.15, 0.48]];
      (E.progress || []).forEach((p, i) => {
        const [a, b] = prog[i] || [0.2, 0.5];
        css(p, { width: ((a + (b - a) * F.ease.inOut(clamp((t - tDrop) / 8))) * 100).toFixed(2) + '%' });
      });
    }
    if (!dropped) flyers.forEach(f => css(f, { display: 'none' }));
    // Rail state follows the system.
    // Stacked in one grid cell (no layout shift): swap by visibility; the rail is never hidden.
    css(E.projectSummaryIdle, { visibility: dropped ? 'hidden' : '' });
    css(E.projectSummaryRunning, { visibility: dropped ? '' : 'hidden' });
    F.text(E.systemCount, t >= tDrop + BEAT ? '2' : '');

    // Decisions: the count ticks to 1 on 11.1; the cursor clicks Decisions on 11.3.
    // The decision stays in its "Approving" state; on 12.3 the lime floods out of that button (EndCard).
    const tCount = T(11, 1), tResolve = Infinity;
    const countOn = t >= tCount && t < tResolve;
    const cpop = springP(t - tCount, 'snappy');
    css(E.decisionCount, { visibility: countOn ? '' : 'hidden', transform: `scale(${(0.55 + 0.45 * cpop).toFixed(4)})` });
    cls(E.navSystem, 'is-active', !inDecisions);
    cls(E.navDecisions, 'is-active', inDecisions);
    cls(E.navDecisions, 'is-hover', t >= T(11, 2.5) && t < tDec);
    css(E.viewDecisions, { visibility: '', display: inDecisions ? '' : 'none' });
    if (inDecisions) {
      appear(E.decHeader || E.viewDecisions.firstElementChild, t, tDec, 12);
      if (!leave(E.decItem, t, tResolve)) appear(E.decItem, t, tDec + BEAT / 4, 12);
      if (!leave(E.decCard, t, tResolve, -60)) appear(E.decCard, t, tDec + BEAT / 2, 18);
      appear(E.decEmpty, t, tResolve + BEAT / 2, 12);
      const tPress = T(12, 1);
      cls(E.prButton, 'is-hover', t >= T(11, 4.5) && t < tPress);
      cls(E.prButton, 'is-pressed', Cursor.isPressed(t, tPress));
      const busy = t >= tPress;
      // Stacked in one grid cell so the button keeps its width; the decisions view hides with display.
      css(E.prButtonLabel, { visibility: busy ? 'hidden' : '' });
      css(E.prButtonBusy, { visibility: busy ? '' : 'hidden' });
    } else {
      css(E.decEmpty, { visibility: 'hidden' });
    }
  }

  window.DashTimeline = { build, measure, update, worldRect, windowRect, get el() { return E; }, get dash() { return D; } };
})();
