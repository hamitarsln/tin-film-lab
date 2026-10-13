// Film engine: stage, bar/beat time, camera, typing, caret, cursor, DOM helpers.
// Everything here is a pure function of film time t. Static DOM is built once at load; seek(t) only sets
// properties computed from t, so any frame renders the same whether or not the frames before it were drawn.
(function (root) {
  const { spring, SPRING, clamp, lerp, rng, ease } = Motion;
  const M = Music(window.CUE);
  const Q = new URLSearchParams(location.search);
  const VW = Number(Q.get('w')) || window.innerWidth || 1920;
  const VH = Number(Q.get('h')) || window.innerHeight || 1080;
  const RENDER = Q.has('render');

  // The stage is designed at 1920×1080 and scaled to the viewport, so a 960×540 animatic matches the final.
  // layout(W, H) holds every frame-level position so a 9:16 version only has to change this function.
  const SW = 1920, SH = 1080;
  function layout(W, H) {
    const m = 120;                      // side margin
    return {
      W, H, m,
      col: (W - 2 * m - 11 * 24) / 12,  // 12-column grid, 24 px gutters
      gut: 24,
      capY: 96,                         // top of the caption band
      capH: 300,
    };
  }
  const L = layout(SW, SH);

  // Time in bars and beats. Every cue goes through this, never raw seconds.
  // Cues lead the audio by 14 ms (under one frame): a 60 fps frame with 4 blur subframes integrates the 12.5 ms
  // before its timestamp, so an event on the exact beat would only show fully one frame late. With the lead, the
  // frame that is on screen when the beat sounds already shows the whole event.
  const LEAD = 0.014;
  const T = (bar, beat = 1) => M.time(bar, beat) - LEAD;
  const BEAT = M.beat, BAR = M.bar;

  // Spring presets by name or [k, d].
  const K = p => (Array.isArray(p) ? p : SPRING[p || 'base']);
  const springP = (t, p) => spring(t, ...K(p));

  // A value built from segments. Each segment moves the value by dv starting at t0, either on a spring
  // (preset) or along an eased curve over dur (for slow pushes and drifts). Continuous by construction.
  function segs(t, v0, list) {
    let v = v0;
    for (const s of list) {
      if (t <= s.t) continue;
      const u = s.dur ? (s.fn || ease.inOut)(clamp((t - s.t) / s.dur)) : springP(t - s.t, s.p);
      v += s.dv * u;
    }
    return v;
  }
  // Keys as absolute targets: [[t, value, preset|{dur}], ...] -> segments.
  function keys(t, list) {
    const v0 = list[0][1];
    const s = [];
    for (let i = 1; i < list.length; i++) {
      const [ti, vi, p] = list[i];
      const prev = list[i - 1][1];
      if (p && typeof p === 'object' && !Array.isArray(p)) s.push({ t: ti, dv: vi - prev, dur: p.dur, fn: p.fn });
      else s.push({ t: ti, dv: vi - prev, p });
    }
    return segs(t, v0, s);
  }

  // Smooth seeded drift: a sum of slow sines with seeded phases. Never Math.random.
  function drift(t, seed, amp = 1, speed = 1) {
    const r = rng(seed);
    let v = 0;
    for (let i = 0; i < 3; i++) {
      const f = (0.07 + r() * 0.11) * speed * (i + 1), ph = r() * Math.PI * 2;
      v += Math.sin(t * f * Math.PI * 2 + ph) / (i + 1);
    }
    return v * amp / 1.83;
  }

  // Typing with a human rhythm: per-character times from a seed. Bursts inside a token, a short hesitation
  // after spaces and before punctuation-heavy tokens. Returns visible length at t.
  const typeCache = new Map();
  function typeTimes(text, t0, cps, seed) {
    const key = text + '|' + t0 + '|' + cps + '|' + seed;
    if (typeCache.has(key)) return typeCache.get(key);
    const r = rng(seed);
    const times = [];
    let tt = t0;
    for (let i = 0; i < text.length; i++) {
      times.push(tt);
      const c = text[i], n = text[i + 1] || '';
      let d = (1 / cps) * (0.55 + r() * 0.9);
      if (c === ' ') d *= 1.6 + r() * 0.8;
      if (n === '-' || n === '/' || n === ':') d *= 1.25;
      tt += d;
    }
    times.end = tt;
    typeCache.set(key, times);
    return times;
  }
  function typedLen(text, t, t0, cps = 30, seed = 7) {
    if (t < t0) return 0;
    const times = typeTimes(text, t0, cps, seed);
    let n = 0;
    while (n < times.length && times[n] <= t) n++;
    return n;
  }
  // Rescale a typing run so it ends exactly at t1 (keeps the rhythm, hits the beat).
  function typedLenFit(text, t, t0, t1, seed = 7) {
    if (t < t0) return 0;
    if (t >= t1) return text.length;
    const times = typeTimes(text, 0, 30, seed);
    const span = times[times.length - 1] || 1e-6;
    const u = (t - t0) / (t1 - t0) * span;
    let n = 0;
    while (n < times.length && times[n] <= u + 1e-9) n++;
    return n;
  }

  // Caret: solid while typing, then blinks on the beat grid (on for the first half of each beat).
  function caretOn(t, lastKey) {
    if (t - lastKey < 0.45) return true;
    return M.at(t).beatPhase < 0.5;
  }

  // DOM helpers.
  function el(tag, cls, parent, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    if (parent) parent.appendChild(e);
    return e;
  }
  function css(e, props) {
    for (const k in props) {
      const v = props[k];
      if (e.__s && e.__s[k] === v) continue;
      (e.__s || (e.__s = {}))[k] = v;
      if (k.startsWith('--')) e.style.setProperty(k, v); else e.style[k] = v;
    }
  }
  const px = v => `${v.toFixed(2)}px`;
  const show = (e, on) => css(e, { visibility: on ? 'visible' : 'hidden' });
  function text(e, s) { if (e.__t !== s) { e.__t = s; e.textContent = s; } }

  // Analytic motion blur for fast flat-colour edges. The final render averages 4 subframes a few ms apart, so a
  // hard edge moving tens of px per subframe shows four stepped ghosts. Instead, each edge ramps across the distance
  // it travelled in one subframe interval: place the element on the union of its rects at t and t − SUBDT and
  // mask each side with a linear ramp of that width. A still edge stays hard (ramp width 0).
  // The spacing comes from the renderer (render.mjs passes fps, sub and shutter); 0 for stills and sub 1 (no blur).
  const RFPS = Number(Q.get('fps')) || 60, RSUB = Number(Q.get('sub')) || 1, RSH = Number(Q.get('shutter')) || 270;
  const SUBDT = RSUB > 1 ? (RSH / 360) / ((RSUB - 1) * RFPS) : 0;
  function blurRect(e, rNow, rPrev, extra = {}) {
    const L = Math.min(rNow.x, rPrev.x), T0 = Math.min(rNow.y, rPrev.y);
    const R = Math.max(rNow.x + rNow.w, rPrev.x + rPrev.w), B = Math.max(rNow.y + rNow.h, rPrev.y + rPrev.h);
    const wl = Math.abs(rNow.x - rPrev.x), wr = Math.abs(rNow.x + rNow.w - rPrev.x - rPrev.w);
    const wt = Math.abs(rNow.y - rPrev.y), wb = Math.abs(rNow.y + rNow.h - rPrev.y - rPrev.h);
    const f = v => v.toFixed(2) + 'px';
    const mask = (wl + wr + wt + wb) < 0.5 ? 'none' :
      `linear-gradient(to right, transparent 0px, #000 ${f(wl)}, #000 calc(100% - ${f(wr)}), transparent 100%), ` +
      `linear-gradient(to bottom, transparent 0px, #000 ${f(wt)}, #000 calc(100% - ${f(wb)}), transparent 100%)`;
    css(e, { left: f(L), top: f(T0), width: f(Math.max(0, R - L)), height: f(Math.max(0, B - T0)),
      maskImage: mask, webkitMaskImage: mask, maskComposite: 'intersect', webkitMaskComposite: 'source-in', ...extra });
    return { x: L, y: T0, w: R - L, h: B - T0 };
  }

  // Camera: centre (x, y) on the paper sheet and zoom z. world = translate(stage centre) scale(z) translate(-x, -y).
  function camTransform(x, y, z, rot = 0) {
    return `translate(${SW / 2}px, ${SH / 2}px) scale(${z.toFixed(5)}) rotate(${rot.toFixed(4)}deg) translate(${(-x).toFixed(2)}px, ${(-y).toFixed(2)}px)`;
  }

  root.F = {
    M, T, LEAD, BEAT, BAR, SW, SH, VW, VH, RENDER, L, layout, K, springP, segs, keys, drift, typedLen, typedLenFit,
    typeTimes, caretOn, el, css, px, show, text, camTransform, clamp, lerp, ease, rng, SUBDT, blurRect,
  };
})(window);
