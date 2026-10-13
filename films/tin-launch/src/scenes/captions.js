// Captions: the film's voice. Screen space, FG Medium, typed word by word on the beat (docs/SHOTLIST.md).
(function () {
  const { T, BEAT, css, el, springP, clamp, caretOn } = F;
  const BAND = 96, BAND_SIZE = 102.4;

  // Every word with its bar.beat. Word lists come from docs/SHOTLIST.md's word table.
  const SPECS = [
    { id: 'hook', top: 372, size: 128, lines: [
        { words: ['Your', 'agent', 'ships', 'the', 'product.'], at: [[1, 1], [1, 1.5], [1, 2], [1, 2.5], [1, 3]] },
        { words: ['Tin', 'lets', 'it', 'run', 'the', 'marketing.'], at: [[1, 4], [1, 4.5], [2, 1], [2, 1.5], [2, 2], [2, 3]] }],
      move: { at: [2, 4], top: BAND, scale: BAND_SIZE / 128 }, out: [5, 1], caretUntil: [2, 4] },
    { id: 'forms', top: BAND, size: BAND_SIZE, lines: [
        { words: ['No', 'forms.', 'It', 'reads', 'your', 'code.'], at: [[5, 1], [5, 1.5], [5, 2], [5, 2.5], [5, 3], [5, 3.5]] }],
      out: [7, 1] },
    { id: 'plan', top: BAND, size: BAND_SIZE, lines: [
        { words: ['Tin', 'writes', 'the', 'plan.'], at: [[7, 1], [7, 1.5], [7, 2], [7, 2.5]] }],
      out: [9, 1] },
    { id: 'system', top: BAND, size: BAND_SIZE, lines: [
        { words: ['A', 'whole', 'marketing', 'system.'], at: [[9, 1], [9, 1.5], [9, 2], [9, 2.5]] },
        { words: ['60', 'workflows.'], at: [[9, 3], [9, 3.5]], quiet: true }],
      out: [10, 3] },
    { id: 'sessions', top: BAND, size: BAND_SIZE, lines: [
        { words: ['Running', 'between', 'sessions.'], at: [[10, 3], [10, 3.5], [10, 4]] }],
      out: [11, 4] },
    { id: 'review', top: BAND, size: BAND_SIZE, lines: [
        { words: ['Review', 'before', 'anything', 'ships.'], at: [[11, 4], [11, 4.5], [12, 1], [12, 1.5]] }],
      out: null },
  ];

  const caps = [];
  function build(layer) {
    for (const s of SPECS) {
      const box = el('div', 'cap', layer);
      css(box, { fontSize: s.size + 'px', lineHeight: (s.size * 1.06).toFixed(1) + 'px', top: s.top + 'px' });
      const lines = s.lines.map(l => {
        const line = el('div', 'line' + (l.quiet ? ' quiet' : ''), box);
        const words = l.words.map((w, i) => {
          const span = el('span', 'w', line);
          span.textContent = w;
          if (i < l.words.length - 1) line.appendChild(document.createTextNode(' '));
          return span;
        });
        return { line, words, at: l.at.map(([b, k]) => T(b, k)) };
      });
      const caret = el('div', 'caret', layer);
      caps.push({ s, box, lines, caret });
    }
  }

  // Measure word boxes once fonts are in (layout is static; only transforms move).
  function measure() {
    for (const c of caps) {
      for (const l of c.lines) {
        l.top = l.line.offsetTop;
        l.h = l.line.offsetHeight;
        l.ends = l.words.map(w => w.offsetLeft + w.offsetWidth);
      }
    }
  }

  // Swaps. A one-line caption is pushed out by the next one: it slides up 130 px as the next rises 130 px from
  // below into the band (constant spacing, so no overlap and no empty band). A two-line caption would overlap the
  // incoming line, so it leaves a sixteenth early instead (a short gap).
  const PUSH = 130;
  const pushes = c => c.s.lines.length === 1;
  function blockState(c, t) {
    const s = c.s;
    let dy = 0, sc = 1;
    if (s.move) {
      const u = springP(t - T(...s.move.at), 'base');
      dy = (s.move.top - s.top) * u;
      sc = 1 + (s.move.scale - 1) * u;
    }
    // The camera's life reaches the captions too: a slow push over the caption's life and a seeded drift.
    const born = c.lines[0].at[0];
    const end = s.out ? T(...s.out) : T(13, 1);
    sc *= 1 + 0.035 * F.ease.inOut(clamp((t - born) / (end - born)));
    // Rise in when the caption before this one pushes.
    const prev = caps[caps.indexOf(c) - 1];
    if (prev && pushes(prev)) dy += PUSH * (1 - springP(t - born, 'snappy'));
    let op = 1;
    if (s.out) {
      if (pushes(c)) {
        const tOut = T(...s.out);
        dy -= PUSH * springP(t - tOut, 'snappy');
        op = 1 - clamp((t - tOut) / 0.12);
      } else {
        const tOut = T(...s.out) - BEAT / 4;
        dy -= 420 * springP(t - tOut, 'snappy');
        op = 1 - clamp((t - tOut) / 0.16);
      }
    }
    return { dy, sc, op, dx: F.drift(t, 41, 3), dyd: F.drift(t, 42, 2) };
  }

  function update(t) {
    for (const c of caps) {
      const first = c.lines[0].at[0];
      const born = t >= first;
      const { dy, sc, op, dx, dyd } = blockState(c, t);
      const alive = born && op > 0.001;
      css(c.box, { display: alive ? 'block' : 'none', opacity: op.toFixed(3),
        transform: `translate(${dx.toFixed(2)}px, ${(dy + dyd).toFixed(2)}px) scale(${sc.toFixed(5)})` });
      let lastKey = -1, caretLine = null, caretIdx = -1;
      for (const l of c.lines) {
        l.words.forEach((w, i) => {
          const tw = l.at[i];
          const on = t >= tw;
          // A typed word lands whole on its beat and settles 0.06em up.
          const rise = on ? (1 - springP(t - tw, 'snappy')) * 0.06 * c.s.size : 0;
          css(w, { visibility: on && alive ? 'visible' : 'hidden', transform: `translateY(${rise.toFixed(2)}px)` });
          if (on && tw >= lastKey) { lastKey = tw; caretLine = l; caretIdx = i; }
        });
      }
      // Caret after the last typed word; hidden once the caption leaves or hands its caret on.
      const until = c.s.caretUntil ? T(...c.s.caretUntil) : (c.s.out ? T(...c.s.out) - (pushes(c) ? 0 : BEAT / 4) : Infinity);
      const showCaret = alive && caretLine && t < until && caretOn(t, lastKey);
      if (caretLine) {
        const size = c.s.size;
        const x = 120 + dx + (caretLine.ends[caretIdx] + size * 0.08) * sc;
        const y = c.s.top + dy + dyd + (caretLine.top + caretLine.h * 0.16) * sc;
        css(c.caret, { visibility: showCaret ? 'visible' : 'hidden', opacity: op.toFixed(3),
          left: x.toFixed(2) + 'px', top: y.toFixed(2) + 'px',
          width: (size * 0.075 * sc).toFixed(2) + 'px', height: (caretLine.h * 0.66 * sc).toFixed(2) + 'px' });
      } else css(c.caret, { visibility: 'hidden' });
    }
  }

  // Where the hook's caret sits on screen at the hand-off (the terminal takes it from here).
  function hookCaretAt(t) {
    const c = caps[0], l = c.lines[1];
    const { dy, sc, dx, dyd } = blockState(c, t);
    const size = c.s.size;
    return { x: 120 + dx + (l.ends[l.words.length - 1] + size * 0.08) * sc, y: c.s.top + dy + dyd + (l.top + l.h * 0.16) * sc,
      w: size * 0.075 * sc, h: l.h * 0.66 * sc };
  }

  window.Captions = { build, measure, update, hookCaretAt, SPECS };
})();
