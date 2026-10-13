// End card (bars 13–16): lime floods out of the approval, then contracts into the command block on paper.
// Logotype, command, tin.computer, held through the fade. Lime appears nowhere earlier.
(function () {
  const { T, BEAT, BAR, css, el, springP, typedLenFit, caretOn, segs, clamp, drift } = F;
  const HEAVY = 'heavy';
  const LOGO_H = 150, LOGO_W = 150 * 657 / 422;
  const CMD1 = 'claude mcp add --transport http tin', CMD2 = 'https://app.tin.computer/mcp';
  const MONO = 72, MONO_LH = 92, PADX = 36, PADY = 30;
  const TAG = ['Open-source', 'marketing', 'system,', 'designed', 'for', 'coding', 'agents.'];
  const AGENTS = ['Works', 'with', 'Claude', 'Code,', 'Codex', 'and', 'Cursor.'];
  const Y = { logo: 176, tag: 354, cmd: 452, url: 762, agents: 814 };

  const tFlood = T(12, 3), tLogo = T(13, 1), tShrink = T(13, 3);
  const tCmd = [T(13, 3.5), T(14, 1)], tTag = T(14, 1), tUrl = [T(14, 3), T(14, 4)], tAgents = T(15, 1);

  let wrap, bg, flood, logo, cmd1, cmd2, caret, tag, url, agents, cmdBox, cw;
  function words(parent, list, cls, size) {
    const box = el('div', 'end-text ' + (cls || ''), parent);
    css(box, { fontSize: size + 'px' });
    const ws = list.map((w, i) => { const s = el('span', 'w', box); s.textContent = w; if (i < list.length - 1) box.appendChild(document.createTextNode(' ')); return s; });
    return { box, ws };
  }

  function build(layer, assetBase) {
    wrap = el('div', '', layer); wrap.id = 'endwrap';
    bg = el('div', '', wrap); bg.id = 'endbg';
    flood = el('div', '', wrap); flood.id = 'floodRect';
    logo = el('div', 'end-logo', wrap);
    const img = el('img', '', logo); img.src = assetBase + 'refs/brand/logotype-ink-on-transparent.png'; img.alt = 'Tin';
    css(logo, { left: '120px', top: Y.logo + 'px', width: LOGO_W.toFixed(1) + 'px', height: LOGO_H + 'px' });
    tag = words(wrap, TAG, '', 42); css(tag.box, { top: Y.tag + 'px', fontWeight: '400', letterSpacing: '-0.01em' });
    cmd1 = el('div', 'end-cmd', wrap); cmd2 = el('div', 'end-cmd', wrap);
    caret = el('div', 'caret', wrap);
    url = el('div', 'end-text', wrap); css(url, { top: Y.url + 'px', fontSize: '104px', lineHeight: '1', fontWeight: '500', letterSpacing: '-0.035em', color: 'var(--ink)' });
    agents = words(wrap, AGENTS, '', 34); css(agents.box, { top: Y.agents + 'px', lineHeight: '1', fontWeight: '400', color: 'var(--ink-64)', left: 'auto', textAlign: 'right' });
    for (const c of [cmd1, cmd2]) css(c, { fontSize: MONO + 'px', lineHeight: MONO_LH + 'px' });
  }

  function measure() {
    const probe = el('span', 'end-cmd', wrap); css(probe, { fontSize: MONO + 'px' }); probe.textContent = '0'.repeat(20);
    cw = probe.offsetWidth / 20; probe.remove();
    const w = Math.max(CMD1.length, CMD2.length) * cw + 2 * PADX;
    cmdBox = { x: 120, y: Y.cmd, w, h: 2 * MONO_LH + 2 * PADY };
    // The agent line sits on the URL's baseline, right-aligned to the command block.
    css(agents.box, { right: (1920 - (120 + w)).toFixed(1) + 'px' });
    css(cmd1, { left: 120 + PADX + 'px', top: Y.cmd + PADY + 'px' });
    css(cmd2, { left: 120 + PADX + 'px', top: Y.cmd + PADY + MONO_LH + 'px' });
  }

  // The flood rect: out of the approved button's own rectangle to the full frame, then back into the command block.
  function floodRect(t) {
    const b = DashTimeline.worldRect('prButton');
    const p0 = Camera.toScreen(b.x, b.y, tFlood), p1 = Camera.toScreen(b.x + b.w, b.y + b.h, tFlood);
    const r0 = { x: p0.x, y: p0.y, w: p1.x - p0.x, h: p1.y - p0.y };
    const r1 = { x: -40, y: -40, w: 2000, h: 1160 };
    const r2 = cmdBox;
    const u1 = springP(t - tFlood, 'base'), u2 = springP(t - tShrink, 'base');
    const k = (a, b, c) => a + (b - a) * u1 + (c - b) * u2;
    return { x: k(r0.x, r1.x, r2.x), y: k(r0.y, r1.y, r2.y), w: k(r0.w, r1.w, r2.w), h: k(r0.h, r1.h, r2.h) };
  }

  function typedWords(list, t, t0, step) {
    list.ws.forEach((w, i) => {
      const tw = t0 + i * step;
      const on = t >= tw;
      css(w, { visibility: on ? 'visible' : 'hidden', transform: `translateY(${(on ? (1 - springP(t - tw, 'snappy')) * 3 : 0).toFixed(2)}px)` });
    });
  }

  function update(t) {
    const on = t >= tFlood;
    css(wrap, { display: on ? 'block' : 'none' });
    if (!on) return;
    // The card itself drifts and pushes a little, like the rest of the take.
    const push = 1 + 0.03 * F.ease.inOut(clamp((t - tShrink) / (T(17, 1) - tShrink)));
    css(wrap, { transform: `translate(${(drift(t, 31, 5)).toFixed(2)}px, ${(drift(t, 32, 3)).toFixed(2)}px) scale(${push.toFixed(5)})` });
    // Paper replaces the world once lime covers the frame.
    css(bg, { visibility: t >= tLogo ? 'visible' : 'hidden' });
    // The flood's edges carry their own motion blur (see F.blurRect): no stepped ghosts at 4 subframes.
    F.blurRect(flood, floodRect(t), floodRect(t - F.SUBDT), { visibility: 'visible' });
    // Logotype lands with mass: a masked rise.
    const ul = springP(t - tLogo, HEAVY);
    const img = logo.firstChild;
    css(logo, { visibility: t >= tLogo ? 'visible' : 'hidden' });
    css(img, { transform: `translateY(${((1 - ul) * LOGO_H * 1.02).toFixed(2)}px)` });
    // The command types inside the block.
    const total = CMD1.length + CMD2.length;
    const n = typedLenFit(CMD1 + CMD2, t, tCmd[0], tCmd[1], 41);
    F.text(cmd1, CMD1.slice(0, Math.min(n, CMD1.length)));
    F.text(cmd2, CMD2.slice(0, Math.max(0, n - CMD1.length)));
    const onLine2 = n > CMD1.length || n === total;
    const cx = 120 + PADX + (onLine2 ? n - CMD1.length : n) * cw + 4;
    const cy = Y.cmd + PADY + (onLine2 ? MONO_LH : 0) + 12;
    const lastKey = Math.min(t, tCmd[1]);
    css(caret, { visibility: t >= tCmd[0] && caretOn(t, lastKey) ? 'visible' : 'hidden', left: cx.toFixed(2) + 'px', top: cy.toFixed(2) + 'px',
      width: (cw * 0.9).toFixed(2) + 'px', height: '70px' });
    typedWords(tag, t, tTag, BEAT / 4);
    const nu = typedLenFit('tin.computer', t, tUrl[0], tUrl[1], 53);
    F.text(url, 'tin.computer'.slice(0, nu));
    typedWords(agents, t, tAgents, BEAT / 4);
  }

  window.EndCard = { build, measure, update };
})();
