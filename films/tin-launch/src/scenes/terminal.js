// The agent's surface: a terminal-blue session where the command goes in and the agent fills Tin's plan.
// World space at (0, 0). Every line is real copy (docs/SHOTLIST.md word table).
(function () {
  const { T, BEAT, css, el, springP, keys, typedLenFit, caretOn, clamp } = F;
  const PAD = 44, LH = 40;
  const W0 = 1680, W1 = 1412, H = 1000;   // W1 leaves a blue band at the left edge of the drop framing

  const CMD = 'claude mcp add --transport http tin https://app.tin.computer/mcp';
  const PROMPT = 'Use Tin to grow my project like a pro!';
  const REPLY = "I'll read the repository first, then help you choose a starting plan.";
  const FILES = ['README.md', 'AGENTS.md', 'docs/architecture.md', 'workflow_packages/'];
  const CALL = ['tin', ' › Start here: onboard this business'];
  const INPUTS = [
    ['product_url', 'https://tin.computer'],
    ['system_repository', 'github.com/tin-computer/tin'],
    ['system_docs', 'docs/README.md'],
    ['priority', 'organic growth'],
  ];
  const PATH = 'reports/GROWTH_ONBOARDING_PLAN.md';

  // Times (bar, beat) for every line.
  const tCmd = [T(3, 1), T(3, 4.5)], tEnter1 = T(4, 1);
  const tPrompt = [T(4, 2), T(4, 4)], tEnter2 = T(5, 1);
  const tReply = [T(5, 1), T(5, 2.5)];
  const tFiles = [T(5, 2.5), T(5, 3), T(5, 3.5), T(5, 4)];
  const tCall = [T(6, 1), T(6, 1.5)];
  const tInputs = [T(6, 1.5), T(6, 2.5), T(6, 3.5), T(6, 4.5)];
  const tPath = [T(7, 1), T(7, 1.5)], tUline = T(7, 1.5);
  const tNarrow = T(7, 1.5);
  const tCollapse = T(10, 2);

  let box, content, rows = {}, caret, cw = 14.4, uline, pathSpan;
  function row(i, cls) { const r = el('div', 'tl' + (cls ? ' ' + cls : ''), content); css(r, { top: PAD + i * LH + 'px' }); return r; }
  // The session scrolls up as lines arrive (rows past the visible panel), like a real terminal.
  // A row ahead of each new line once the panel is full (rows 10, 11 and the plan path on row 13).
  const scrollAt = t => keys(t, [[0, 0], [T(6, 3.25), LH, 'snappy'], [T(6, 4.25), 2 * LH, 'snappy'], [T(6, 4.75), 4 * LH, 'base']]);

  function build(world, flyLayer) {
    box = el('div', '', world); box.id = 'terminal';
    content = el('div', '', box); css(content, { position: 'absolute', left: '0px', top: '0px', width: '100%', height: '100%' });
    rows.cmdP = row(0, 'dim'); rows.cmdP.textContent = '$';
    rows.cmd = row(0); css(rows.cmd, { left: PAD + 'px' });
    rows.pP = row(2, 'dim'); rows.pP.textContent = '›';
    rows.p = row(2);
    rows.reply = row(4);
    rows.files = FILES.map(() => row(5, 'dim'));
    rows.call = row(7);
    rows.callTin = el('span', 'strong', rows.call); rows.callRest = el('span', '', rows.call);
    rows.inputs = INPUTS.map((_, i) => {
      const r = row(8 + i);
      const n = el('span', 'dim', r), v = el('span', '', r);
      return { r, n, v };
    });
    rows.path = row(13);
    const arrow = el('span', 'dim', rows.path); arrow.textContent = '→ ';
    pathSpan = el('span', 'path', rows.path);
    uline = el('span', 'uline', pathSpan);
    caret = el('div', 'tcaret', content);
  }

  function measure() {
    const probe = el('span', 'tl', box); probe.textContent = '0'.repeat(40);
    cw = probe.offsetWidth / 40; probe.remove();
    rows.layout = {
      cmdX: PAD + 2 * cw, pX: PAD + 2 * cw,
      fileX: [], inputValX: PAD + 21 * cw,
    };
    let x = PAD;
    FILES.forEach((f, i) => { rows.layout.fileX.push(x); x += (f.length + 4) * cw; });
    rows.layout.pathX = PAD + 2 * cw;
  }

  // Terminal rect in world px at t: full width, then narrows for Tin's window. On 10.2 the session ends: the blue
  // band at the left of the frame retracts out of frame while Tin keeps running.
  function rectAt(t) {
    const w = keys(t, [[0, W0], [tNarrow, W1, 'base']]);
    const h = keys(t, [[0, H], [tCollapse, 0, 'base']]);   // the session closes like a blind rolling up
    return { x: 0, y: 0, w, h: Math.max(0, h) };
  }
  // Where the caret sits in world px (row 0 after "$ ", or row 2 after "› ").
  function caretWorld(t) {
    const L = rows.layout;
    if (t < tEnter1) {
      const n = typedLenFit(CMD, t, ...tCmd, 11);
      return { x: L.cmdX + n * cw, y: PAD + 0 * LH + 5, last: n > 0 ? Math.min(t, tCmd[1]) : T(3, 1) };
    }
    const n = typedLenFit(PROMPT, t, ...tPrompt, 23);
    return { x: L.pX + n * cw, y: PAD + 2 * LH + 5, last: n > 0 ? Math.min(t, tPrompt[1]) : tEnter1 };
  }

  function typedText(node, text, t, t0, t1, seed) { const n = typedLenFit(text, t, t0, t1, seed); F.text(node, text.slice(0, n)); return n; }

  function update(t) {
    const r = rectAt(t);
    const gone = t > tCollapse && r.h < 1;
    css(box, { display: gone ? 'none' : 'block', left: r.x.toFixed(2) + 'px', top: r.y.toFixed(2) + 'px',
      width: r.w.toFixed(2) + 'px', height: r.h.toFixed(2) + 'px', zIndex: t > tCollapse ? '5' : '1' });
    const L = rows.layout;
    css(content, { transform: `translateY(${(-scrollAt(t)).toFixed(2)}px)` });
    // Lines.
    typedText(rows.cmd, CMD, t, ...tCmd, 11); css(rows.cmd, { left: L.cmdX + 'px' });
    css(rows.pP, { visibility: t >= tEnter1 ? 'visible' : 'hidden' });
    typedText(rows.p, PROMPT, t, ...tPrompt, 23); css(rows.p, { left: L.pX + 'px' });
    // The reply streams like a model writes: fast and even.
    const nr = t < tReply[0] ? 0 : Math.round(clamp((t - tReply[0]) / (tReply[1] - tReply[0])) * REPLY.length);
    F.text(rows.reply, REPLY.slice(0, nr));
    FILES.forEach((f, i) => {
      const on = t >= tFiles[i];
      F.text(rows.files[i], f + (i < FILES.length - 1 ? '  ·' : ''));
      css(rows.files[i], { left: L.fileX[i].toFixed(2) + 'px', visibility: on ? 'visible' : 'hidden' });
    });
    const nc = t < tCall[0] ? 0 : Math.round(clamp((t - tCall[0]) / (tCall[1] - tCall[0])) * (CALL[0].length + CALL[1].length));
    F.text(rows.callTin, CALL[0].slice(0, nc)); F.text(rows.callRest, CALL[1].slice(0, Math.max(0, nc - CALL[0].length)));
    INPUTS.forEach(([name, val], i) => {
      const t0 = tInputs[i], on = t >= t0;
      F.text(rows.inputs[i].n, on ? '  ' + name.padEnd(19, ' ') : '');
      const nv = !on ? 0 : Math.round(clamp((t - t0) / (BEAT * 0.45)) * val.length);
      F.text(rows.inputs[i].v, val.slice(0, nv));
    });
    const np = t < tPath[0] ? 0 : Math.round(clamp((t - tPath[0]) / (tPath[1] - tPath[0] - 0.05)) * PATH.length);
    css(rows.path, { visibility: t >= tPath[0] ? 'visible' : 'hidden' });
    if (pathSpan.firstChild && pathSpan.firstChild.nodeType === 3) pathSpan.firstChild.nodeValue = PATH.slice(0, np);
    else pathSpan.insertBefore(document.createTextNode(PATH.slice(0, np)), uline);
    css(uline, { width: (springP(t - tUline, 'snappy') * PATH.length * cw).toFixed(2) + 'px' });

    // The caret: on 2.4 the caption's caret stops and the terminal's starts blinking at the prompt (the hand-off
    // lands on the beat; a flying caret read as a flicker), then it types from 3.1.
    const tHand = T(2, 4);
    const cwp = caretWorld(t);
    const last = t < T(3, 1) ? tHand : cwp.last;
    const showTermCaret = t >= tHand && t < tEnter2 && caretOn(t, last);
    css(caret, { visibility: showTermCaret && !gone ? 'visible' : 'hidden', left: cwp.x.toFixed(2) + 'px', top: cwp.y.toFixed(2) + 'px',
      width: (cw * 0.92).toFixed(2) + 'px' });
  }

  // The plan path's box in world px: Tin's window grows out of it.
  function pathRect(t) {
    const r = rectAt(t);
    return { x: r.x + rows.layout.pathX, y: r.y + PAD + 13 * LH - scrollAt(t), w: PATH.length * cw, h: LH };
  }

  window.Terminal = { build, measure, update, rectAt, pathRect, PAD, LH };
})();
