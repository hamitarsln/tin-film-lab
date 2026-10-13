// The cursor is a person: springs between targets, arrives early, presses on the beat (docs/ANIMATION_GUIDE.md).
// Its path is in world px (so it sticks to UI under camera moves); it's drawn in screen space at a constant size.
(function () {
  const { T, BEAT, css, el, keys, springP, clamp } = F;
  let node, K = null;
  const PRESSES = [];            // [time] of each click

  const ARROW = '<svg viewBox="0 0 40 40" width="40" height="40" style="position:absolute;left:0;top:0"><path d="M6 4 L6 31 L13 24.5 L17.8 35 L22.6 32.8 L17.9 22.6 L27 22.6 Z" fill="#080808" stroke="#FEFDFB" stroke-width="2" stroke-linejoin="round"/></svg>';
  let trails = [];
  function build(layer) {
    // Three trail copies fill the gaps between the final render's 4 blur subframes when the hand moves fast;
    // they sit exactly under the cursor (and vanish) when it is still.
    trails = [3, 2, 1].map(() => { const n = el('div', '', layer); n.className = 'cursor-trail'; n.innerHTML = ARROW; return n; });
    node = el('div', '', layer); node.id = 'cursor';
    node.innerHTML = ARROW;
  }

  const centre = r => ({ x: r.x + r.w * 0.5, y: r.y + r.h * 0.58 });

  function measure() {
    const D = DashTimeline;
    const ap = centre(D.worldRect('approve'));
    const nav = centre(D.worldRect('navDecisions'));
    const pr = centre(D.worldRect('prButton'));
    const enter = { x: ap.x + 260, y: ap.y + 520 };
    // After the drop the hand rests over the "This week" strip, inside the between-sessions framing.
    const wk = D.worldRect('week');
    const rest1 = { x: wk.x + wk.w * 0.72, y: wk.y + wk.h * 0.55 };
    const rest2 = { x: pr.x + 60, y: pr.y + 90 };
    // Travel keys land a quarter beat before each press.
    K = {
      x: [[0, enter.x], [T(8, 1), ap.x, 'base'], [T(9, 1.5), rest1.x, 'base'], [T(11, 1.5), nav.x, 'base'],
          [T(11, 3.5), pr.x, 'base'], [T(12, 2), rest2.x, 'base']],
      y: [[0, enter.y], [T(8, 1), ap.y, 'base'], [T(9, 1.5), rest1.y, 'base'], [T(11, 1.5), nav.y, 'base'],
          [T(11, 3.5), pr.y, 'base'], [T(12, 2), rest2.y, 'base']],
    };
    PRESSES.length = 0;
    PRESSES.push(T(9, 1), T(11, 3), T(12, 1));
  }

  // Press: 0.88 for 0.06 s, then a snappy return.
  function pressScale(t) {
    let s = 1;
    for (const p of PRESSES) {
      if (t >= p && t < p + 0.06) s = Math.min(s, 0.88);
      else if (t >= p + 0.06) s = Math.min(s, 1 - 0.12 * (1 - springP(t - p - 0.06, 'snappy')));
    }
    return s;
  }
  const isPressed = (t, p) => t >= p && t < p + 0.11;

  function screenAt(t) { return Camera.toScreen(keys(t, K.x), keys(t, K.y), t); }
  function update(t) {
    const born = t >= T(8, 1) - 0.02, gone = t >= T(13, 1.5);
    const p = screenAt(t);
    const s = pressScale(t);
    // Trail copies at t − k·SUBDT/4, fading with speed (px per subframe interval).
    const back = screenAt(t - F.SUBDT);
    const speed = F.SUBDT ? Math.hypot(p.x - back.x, p.y - back.y) : 0;
    const a = clamp((speed - 3) / 12) * 0.42;
    trails.forEach((n, i) => {
      const k = 3 - i;                        // 3, 2, 1 quarter-intervals back
      const q = screenAt(t - (k * F.SUBDT) / 4);
      css(n, { visibility: born && !gone && a > 0.01 ? 'visible' : 'hidden', opacity: a.toFixed(3),
        left: (q.x - 6).toFixed(2) + 'px', top: (q.y - 4).toFixed(2) + 'px' });
    });
    // Position and press scale are paint properties (left/top, the SVG's size), not a CSS transform: a small
    // composited layer with a changing transform can keep a stale raster scale and differ with history.
    const size = 40 * s;
    css(node, { visibility: born && !gone ? 'visible' : 'hidden', left: (p.x - 6 * s).toFixed(2) + 'px', top: (p.y - 4 * s).toFixed(2) + 'px' });
    const svg = node.firstChild;
    if (svg.__s !== size) { svg.__s = size; svg.setAttribute('width', size.toFixed(2)); svg.setAttribute('height', size.toFixed(2)); }
  }

  window.Cursor = { build, measure, update, isPressed, PRESSES, worldAt: t => ({ x: keys(t, K.x), y: keys(t, K.y) }) };
})();
