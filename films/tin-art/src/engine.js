// Shared engine for the board (src/board.html) and the film (src/index.html): the mark, Tin's paper and grain, the
// material treatments. Pure: everything is generated once from fixed seeds; the film sets BOARD.motion before each
// paint (local time in the shot, the push and the frame number) and nothing else carries between paints.
(() => {
const q = new URLSearchParams(location.search);
const W = Number(q.get('w')) || 2160, H = Number(q.get('h')) || 2160;
const cv = document.getElementById('c'); cv.width = W; cv.height = H;
const g = cv.getContext('2d');

// ---------- motion state (set by the film before each paint; the board leaves it at rest) ----------
const BOARD_MOTION = { u: 0, push: 1, frame: 0, drift: 0, panX: 0, panY: 0 };

// ---------- palette ----------
const PAPER = '#F5F1E6', INK = '#080808', TERMINAL = '#90D7E4', LIME = 'oklch(0.90 0.22 120)';

// ---------- the mark ----------
// refs/brand/mark.svg, viewBox 720x720. Four shapes: i stem, T, i dot, n.
const MARK_D = 'M300.50,284.00 L300.00,284.50 L300.00,547.25 L300.50,547.75 L369.50,547.75 L370.00,547.00 L370.00,284.75 L369.50,284.00 Z M46.50,180.00 L46.00,180.50 L46.25,243.75 L117.50,243.75 L118.00,244.25 L118.00,547.25 L118.50,547.75 L187.50,547.75 L188.00,547.00 L187.75,244.50 L188.50,243.75 L259.50,243.75 L260.00,243.00 L260.00,180.75 L259.50,180.00 Z M300.25,179.75 L300.00,243.25 L300.50,243.75 L369.75,243.50 L369.50,179.50 Z M608.25,185.00 L600.00,181.00 L591.50,178.00 L577.75,175.00 L567.25,174.00 L553.50,174.00 L537.75,176.00 L529.25,178.00 L522.50,180.25 L513.50,184.00 L506.25,188.00 L493.75,197.00 L490.25,200.00 L481.00,209.75 L480.25,209.75 L480.25,179.50 L479.75,179.00 L410.50,179.00 L410.00,179.50 L410.00,547.25 L410.50,547.75 L482.75,547.50 L482.75,299.00 L484.75,279.75 L487.00,270.50 L490.75,260.50 L494.25,254.00 L499.50,247.00 L507.50,239.75 L512.50,236.75 L520.75,233.75 L532.00,232.00 L541.00,232.25 L550.25,234.00 L556.75,236.75 L562.75,240.75 L568.00,246.00 L572.50,252.25 L577.00,262.00 L580.00,273.50 L581.25,286.50 L581.25,547.25 L581.75,547.75 L653.50,547.75 L654.00,547.25 L654.00,273.50 L653.75,265.50 L652.75,255.50 L650.75,244.75 L646.75,231.25 L644.75,226.25 L639.75,216.25 L638.75,215.25 L638.75,214.50 L633.50,207.00 L623.75,196.25 L617.75,191.25 Z';
// Scale from REFERENCE.md: the mark spans 77% of the frame width (608 units -> 1672 px at 2160), centred.
const S = 0.7741 * W / 608;
const MX = W / 2 - 350 * S, MY = H / 2 - 360.875 * S;
const toPx = (x, y) => [MX + x * S, MY + y * S];
// The traced path draws the n's curves as short straight segments, which facet at 2160 px. Curved runs are redrawn
// as Catmull-Rom cubics through the same vertices (the curve passes through every original point); any vertex that
// turns more than 30 degrees stays a sharp corner, so the T, the i and the stems are untouched.
function markSubpaths(d) {
  return d.split('Z').map(t => t.trim()).filter(Boolean).map(t => { const v = t.match(/-?[\d.]+/g).map(Number); const pts = []; for (let i = 0; i < v.length; i += 2) pts.push([v[i], v[i + 1]]); return pts; });
}
function smoothMarkPath(d, tf) {
  const out = new Path2D();
  for (const pts of markSubpaths(d)) {
    const n = pts.length, P = i => pts[(i + n) % n];
    const turn = i => { const a = P(i - 1), b = P(i), c = P(i + 1); const ux = b[0] - a[0], uy = b[1] - a[1], vx = c[0] - b[0], vy = c[1] - b[1];
      return Math.abs(Math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)); };
    const smooth = pts.map((_, i) => turn(i) < Math.PI / 6);
    const T = ([x, y]) => [tf.S * x + tf.MX, tf.S * y + tf.MY];
    const p0 = T(P(0)); out.moveTo(p0[0], p0[1]);
    for (let i = 0; i < n; i++) {
      const a = P(i), b = P(i + 1);
      if (smooth[i] && smooth[(i + 1) % n]) {
        // tangent direction from the neighbours, handle length a third of this segment: no overshoot where a
        // short curved segment meets a long straight stem
        const pa = P(i - 1), pb = P(i + 2), len = Math.hypot(b[0] - a[0], b[1] - a[1]);
        const unit = (u, v) => { const l = Math.hypot(v[0] - u[0], v[1] - u[1]) || 1; return [(v[0] - u[0]) / l, (v[1] - u[1]) / l]; };
        const ta = unit(pa, b), tb = unit(a, pb);
        const c1 = [a[0] + ta[0] * len / 3, a[1] + ta[1] * len / 3], c2 = [b[0] - tb[0] * len / 3, b[1] - tb[1] * len / 3];
        const [x1, y1] = T(c1), [x2, y2] = T(c2), [x3, y3] = T(b); out.bezierCurveTo(x1, y1, x2, y2, x3, y3);
      } else { const [x, y] = T(b); out.lineTo(x, y); }
    }
    out.closePath();
  }
  return out;
}
// The film uses src/mark-fit.js (scripts/markfit.py): the n's arches refitted as smooth Beziers. Its path is in viewBox
// units, so it is placed with a transform. ?mark=trace falls back to the vertex-interpolating smoothing above.
function fittedMarkPath(d) {
  const p = new Path2D(), m = new DOMMatrix([S, 0, 0, S, MX, MY]);
  p.addPath(new Path2D(d), m); return p;
}
const markPath = window.MARK_FIT_D && q.get('mark') !== 'trace' ? fittedMarkPath(window.MARK_FIT_D) : smoothMarkPath(MARK_D, { S, MX, MY });
// Stroke centrelines in viewBox units (derived from the path; see docs/REFERENCE.md). w = stroke width.
const STROKES = {
  tbar:  { pts: [[46, 212], [260, 212]], w: 64 },
  tstem: { pts: [[153, 244], [153, 548]], w: 70 },
  idot:  { pts: [[335, 211.6]], w: 70 },
  istem: { pts: [[335, 284], [335, 548]], w: 70 },
  nleft: { pts: [[446, 179], [446, 548]], w: 73 },
  narch: { pts: [[483, 222], [502, 214], [532, 205], [566, 205.5], [596.6, 223], [613.6, 253], [617.6, 285]], w: 74 },
  nright: { pts: [[617.6, 285], [617.6, 548]], w: 73 },
};
// The i's dot is a box, not a stroke: objects placed on it are fitted inside it (viewBox units).
const IDOT_BOX = { w: 70, h: 64 };
// Points spaced along a polyline, in px, with the local direction.
function along(pts, step, offset = 0) {
  const P = pts.map(([x, y]) => toPx(x, y));
  if (P.length === 1) return [{ x: P[0][0], y: P[0][1], a: 0 }];
  const segs = []; let L = 0;
  for (let i = 1; i < P.length; i++) { const l = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); segs.push([P[i - 1], P[i], l, L]); L += l; }
  const n = Math.max(1, Math.round((L - 2 * offset) / step));
  const out = [];
  for (let k = 0; k <= n; k++) {
    const s = offset + (L - 2 * offset) * (n ? k / n : 0.5);
    const sg = segs.find(z => s <= z[3] + z[2] + 1e-6) || segs[segs.length - 1];
    const u = (s - sg[3]) / sg[2];
    out.push({ x: sg[0][0] + (sg[1][0] - sg[0][0]) * u, y: sg[0][1] + (sg[1][1] - sg[0][1]) * u, a: Math.atan2(sg[1][1] - sg[0][1], sg[1][0] - sg[0][0]) });
  }
  return out;
}

// ---------- paper and grain (generated once, deterministic) ----------
function noiseCanvas(w, h, seed, fn) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const x = c.getContext('2d'); const img = x.createImageData(w, h); const r = Motion.rng(seed);
  fn(img.data, w, h, r); x.putImageData(img, 0, 0); return c;
}
// Tin's paper: #F5F1E6, fine grain (~2 levels, Fable's paper measured 0.9-1.9), soft fibre mottling.
const paper = (() => {
  const c = noiseCanvas(W, H, 1907, (d, w, h, r) => {
    const GW = 36, GH = 36, coarse = new Float32Array((GW + 2) * (GH + 2));
    for (let i = 0; i < coarse.length; i++) coarse[i] = r() * 2 - 1;
    const cs = (gx, gy) => coarse[gy * (GW + 2) + gx];
    for (let y = 0; y < h; y++) {
      const fy = y / h * GH, gy = Math.floor(fy), ty = fy - gy, sy = ty * ty * (3 - 2 * ty);
      for (let x = 0; x < w; x++) {
        const fx = x / w * GW, gx = Math.floor(fx), tx = fx - gx, sx = tx * tx * (3 - 2 * tx);
        const m = (cs(gx, gy) * (1 - sx) + cs(gx + 1, gy) * sx) * (1 - sy) + (cs(gx, gy + 1) * (1 - sx) + cs(gx + 1, gy + 1) * sx) * sy;
        const n = (r() + r() + r() - 1.5) * 3.2 + m * 1.6;
        const i = (y * w + x) * 4;
        d[i] = 245 + n; d[i + 1] = 241 + n; d[i + 2] = 230 + n * 1.1; d[i + 3] = 255;
      }
    }
  });
  // fibres: short faint strokes, a few darker, a few lighter
  const x = c.getContext('2d'); const r = Motion.rng(77);
  for (let k = 0; k < 2600; k++) {
    const px = r() * W, py = r() * H, len = (4 + r() * 14) * W / 2160, a = r() * Math.PI * 2, bend = (r() - 0.5) * 0.35;
    x.strokeStyle = r() < 0.6 ? `rgba(120,100,70,${0.014 + r() * 0.02})` : `rgba(255,255,250,${0.035 + r() * 0.04})`;
    x.lineWidth = (0.5 + r() * 0.7) * W / 2160;
    x.beginPath(); x.moveTo(px, py);
    x.quadraticCurveTo(px + Math.cos(a + bend) * len / 2, py + Math.sin(a + bend) * len / 2, px + Math.cos(a) * len, py + Math.sin(a) * len);
    x.stroke();
  }
  return c;
})();
// Shared fine grain laid over every still so all materials sit in one world (overlay blend, mid-grey noise).
const GPAD = Math.round(160 * W / 2160);
const grain = noiseCanvas(W + 2 * GPAD, H + 2 * GPAD, 4242, (d, w, h, r) => {
  for (let i = 0; i < d.length; i += 4) { const v = 128 + (r() + r() - 1) * 46; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; }
});
// The moving grain that shows on paper: a zero-mean field split into a light half (added with 'lighter') and a dark half
// (multiplied), so it lifts and darkens bright paper equally. Overlay grain alone barely touches a ground at L 95.
const MG = (() => {
  const w = W + 2 * GPAD, h = H + 2 * GPAD, r = Motion.rng(9001);
  const mk = () => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  const L = mk(), D = mk(), lx = L.getContext('2d'), dx = D.getContext('2d');
  const li = lx.createImageData(w, h), di = dx.createImageData(w, h);
  for (let i = 0; i < li.data.length; i += 4) {
    const n = (r() + r() + r() + r() - 2) * 2.6;           // std ~1.5 levels before splitting
    const up = Math.max(0, n), dn = Math.max(0, -n);
    li.data[i] = li.data[i + 1] = li.data[i + 2] = up; li.data[i + 3] = 255;
    di.data[i] = di.data[i + 1] = di.data[i + 2] = 255 - dn * 1.06; di.data[i + 3] = 255;
  }
  lx.putImageData(li, 0, 0); dx.putImageData(di, 0, 0);
  return { L, D };
})();
function drawPaper(ctx) { ctx.drawImage(paper, 0, 0); }
// Grain changes every frame: the oversized grain field is shifted by a frame-seeded offset (whole pixels, so it stays
// crisp) and mirrored on odd seeds. Frame 0 (and every board still) uses the centred field.
function drawGrain(ctx, a = 0.07, frame = 0) {
  const r = Motion.rng(frame * 7919 + 101);
  const ox = frame ? Math.floor(r() * 2 * GPAD) : GPAD, oy = frame ? Math.floor(r() * 2 * GPAD) : GPAD, flip = frame && r() < 0.5;
  // moving grain on bright grounds (paper), then the overlay grain on mid-tones
  for (const [cv, op] of [[MG.L, 'lighter'], [MG.D, 'multiply']]) {
    ctx.save(); ctx.globalCompositeOperation = op;
    if (flip) { ctx.translate(W, 0); ctx.scale(-1, 1); }
    ctx.drawImage(cv, (ox + 37) % (2 * GPAD), (oy + 53) % (2 * GPAD), W, H, 0, 0, W, H); ctx.restore();
  }
  ctx.save(); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = a;
  if (flip) { ctx.translate(W, 0); ctx.scale(-1, 1); }
  ctx.drawImage(grain, ox, oy, W, H, 0, 0, W, H); ctx.restore();
}

// ---------- images ----------
const cache = new Map();
function img(src) {
  if (!cache.has(src)) cache.set(src, new Promise((res, rej) => { const im = new Image(); im.onload = () => res(im); im.onerror = () => rej(new Error('missing ' + src)); im.src = src; }));
  return cache.get(src);
}
// Draw image region src {x,y,w,h} (fractions of the image) to cover dest rect, rotated by rot (deg) around centre.
function drawCover(ctx, im, { x = 0, y = 0, w = 1, h = 1, rot = 0, dest = [0, 0, W, H], zoom } = {}) {
  const iw = im.naturalWidth || im.width, ih = im.naturalHeight || im.height;
  const sx = x * iw, sy = y * ih, sw = w * iw, sh = h * ih;
  const [dx, dy, dw, dh] = dest; const k = Math.max(dw / sw, dh / sh) * (zoom ?? BOARD_MOTION.push);
  ctx.save(); ctx.translate(dx + dw / 2 + BOARD_MOTION.panX, dy + dh / 2 + BOARD_MOTION.panY); ctx.rotate(rot * Math.PI / 180);
  ctx.drawImage(im, sx, sy, sw, sh, -sw * k / 2, -sh * k / 2, sw * k, sh * k); ctx.restore();
}

// ---------- treatments (REFERENCE.md section 2) ----------
const T = {
  // B: texture inside the mark
  inside(ctx, im, crop) { ctx.save(); ctx.clip(markPath); drawCover(ctx, im, crop); ctx.restore(); },
  // C: texture fills the frame, the mark is a void of paper (or of a given fill)
  knockout(ctx, im, crop, voidFill) {
    drawCover(ctx, im, crop);
    ctx.save(); ctx.clip(markPath);
    if (voidFill) { ctx.fillStyle = voidFill; ctx.fillRect(0, 0, W, H); } else drawPaper(ctx);
    ctx.restore();
  },
  // A: objects along the strokes. items: [{im, s (size factor of stroke width), rot}], placement seeded.
  along(ctx, ims, o = {}) {
    const r = Motion.rng(o.seed || 1);
    const step = (o.step || 1.0) * 70 * S, jitter = (o.jitter ?? 0.12) * 70 * S, size = (o.size || 1.3) * 70 * S;
    const order = o.order || ['tbar', 'tstem', 'idot', 'istem', 'nleft', 'narch'];
    const spots = [];
    for (const k of order) for (const p of along(STROKES[k].pts, step, (o.inset ?? 0.45) * 70 * S)) spots.push({ ...p, k });
    let n = 0;
    const placed = spots.map(p => {
      const im = ims[(o.pick ? o.pick(n, r) : n) % ims.length]; n++;
      const big = Math.max(im.naturalWidth, im.naturalHeight);
      const sz = size * (1 + (r() - 0.5) * (o.sizeVar ?? 0.15));
      const follow = o.follow ? p.a + (o.followOffset || 0) : 0;
      const rot = follow + ((r() - 0.5) * 2 * (o.rotJitter ?? 12)) * Math.PI / 180;
      return { im, x: p.x + (r() - 0.5) * 2 * jitter, y: p.y + (r() - 0.5) * 2 * jitter, rot, k: sz / big, z: r() };
    });
    if (o.shuffleZ !== false) placed.sort((a, b) => a.z - b.z);
    for (const q of placed) {
      ctx.save(); ctx.translate(q.x, q.y); ctx.rotate(q.rot);
      ctx.drawImage(q.im, -q.im.naturalWidth * q.k / 2, -q.im.naturalHeight * q.k / 2, q.im.naturalWidth * q.k, q.im.naturalHeight * q.k);
      ctx.restore();
    }
    return placed.map(q => q.im.src.split('/').pop());
  },
  // C, as a pile: objects scattered (seeded) over a region until it is covered several times, then the mark is cut
  // out of the pile as a paper void. o: { seed, n, size (long side, frame px), region [x0,y0,x1,y1], rotJitter }
  pile(ctx, ims, o = {}) {
    const r = Motion.rng(o.seed || 1), [x0, y0, x1, y1] = o.region || [0, 0, W, H], n = o.n || 80;
    for (let i = 0; i < n; i++) {
      const im = ims[(o.pick ? o.pick(i, r) : i) % ims.length];
      const k = (o.size || 330) * (0.85 + r() * 0.3) / Math.max(im.naturalWidth, im.naturalHeight);
      const x = x0 + r() * (x1 - x0), y = y0 + r() * (y1 - y0), rot = (r() - 0.5) * 2 * (o.rotJitter ?? 25) * Math.PI / 180;
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
      ctx.drawImage(im, -im.naturalWidth * k / 2, -im.naturalHeight * k / 2, im.naturalWidth * k, im.naturalHeight * k); ctx.restore();
    }
    ctx.save(); ctx.clip(markPath); drawPaper(ctx); ctx.restore();
  },
  // A, chained: walk each stroke and lay objects end to end, each sized so its cross-section matches the stroke
  // (cross = factor of the stroke width), turned to follow the stroke. Keeps the T/i/n gaps open.
  // o: { seed, cross, overlap, rotJitter, offJitter, orient: 'long'|'short'|'auto', pick(n, r), strokes, dot, z }
  chain(ctx, ims, o0 = {}) {
    const r = Motion.rng(o0.seed || 1);
    // Objects stay inside the mark's silhouette: no cap extension past the stroke ends (capExt 0), a cross-section of
    // at most the stroke width (cross <= 1), and the i's dot fitted inside its own box, so the gaps between T, i and n,
    // and between the dot and its stem, stay open.
    const order = o0.strokes || ['tbar', 'tstem', 'idot', 'istem', 'nleft', 'narch', 'nright'];
    const placed = []; let n = 0;
    const pick = () => ims[(o0.pick ? o0.pick(n, r) : n) % ims.length];
    for (const key of order) {
      const o = Object.assign({}, o0, (o0.per || {})[key]);
      const st = STROKES[key], width = st.w * S * (o.allowOver ? (o.cross || 1) : Math.min(1, o.cross || 0.96));
      if (st.pts.length === 1) {   // the i dot: one object fitted inside its box
        const im = pick(); n++;
        const [x, y] = toPx(...st.pts[0]);
        const k = Math.min(IDOT_BOX.w * S / im.naturalWidth, IDOT_BOX.h * S / im.naturalHeight) * Math.min(1, o.dot || 1.0);
        placed.push({ im, x, y, rot: ((r() - 0.5) * 2 * (o.rotJitter ?? 6)) * Math.PI / 180, k, z: o.dotTop ? 2 : r(), key });
        continue;
      }
      const P = st.pts.map(([x, y]) => toPx(x, y)); const segs = []; let L = 0;
      for (let i = 1; i < P.length; i++) { const l = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); segs.push([P[i - 1], P[i], l, L]); L += l; }
      const at = s => { s = Math.max(0, Math.min(L, s)); const sg = segs.find(z => s <= z[3] + z[2] + 1e-6) || segs[segs.length - 1]; const u = (s - sg[3]) / sg[2];
        return [sg[0][0] + (sg[1][0] - sg[0][0]) * u, sg[0][1] + (sg[1][1] - sg[0][1]) * u, Math.atan2(sg[1][1] - sg[0][1], sg[1][0] - sg[0][0])]; };
      const ov = o.overlap ?? 0.12, ext = (o.capExt ?? 0) * st.w * S, total = L + 2 * ext;
      let s = -ext; const run = [];
      while (s < L + ext - 1) {
        const im = pick(); n++;
        const iw = im.naturalWidth, ih = im.naturalHeight;
        const longAlong = o.orient === 'long' ? true : o.orient === 'short' ? false : iw / ih > 1 ? true : r() < 0.5;
        const crossPx = longAlong ? Math.min(iw, ih) : Math.max(iw, ih);
        const k = width / crossPx; const len = (longAlong ? Math.max(iw, ih) : Math.min(iw, ih)) * k;
        run.push({ im, k, len, longAlong });
        s += len * (1 - ov);
      }
      // spread the run so it starts and ends flush with the stroke ends
      const used = run.reduce((a, q) => a + q.len * (1 - ov), 0) + run[run.length - 1].len * ov;
      const f = total / used; s = -ext;
      for (const q of run) {
        const c = s + (q.len / 2) * f;
        const [x, y, a] = at(c);
        const nx = -Math.sin(a), ny = Math.cos(a), off = (r() - 0.5) * 2 * (o.offJitter ?? 0.04) * st.w * S;
        const iwide = q.im.naturalWidth >= q.im.naturalHeight;
        let rot = a + (q.longAlong === iwide ? 0 : Math.PI / 2);
        if (o.upright && Math.cos(rot) < -0.01) rot += Math.PI;
        rot += ((r() - 0.5) * 2 * (o.rotJitter ?? 4)) * Math.PI / 180;
        placed.push({ im: q.im, x: x + nx * off, y: y + ny * off, rot, k: q.k, z: r(), key });
        s += q.len * (1 - ov) * f;
      }
    }
    if (o0.z !== 'order') placed.sort((a, b) => a.z - b.z);
    // the film's drift: each object slides a few px and turns a fraction of a degree over the hold, seeded per object
    const dr = Motion.rng((o0.seed || 1) * 977 + 5), du = BOARD_MOTION.drift * BOARD_MOTION.u, sp = 9 * W / 2160;
    for (const q of placed) {
      const ang = dr() * Math.PI * 2, mag = (0.5 + dr()) * sp, rv = (dr() - 0.5) * 0.012;
      ctx.save(); ctx.translate(q.x + Math.cos(ang) * mag * du, q.y + Math.sin(ang) * mag * du); ctx.rotate(q.rot + rv * du);
      ctx.drawImage(q.im, -q.im.naturalWidth * q.k / 2, -q.im.naturalHeight * q.k / 2, q.im.naturalWidth * q.k, q.im.naturalHeight * q.k);
      ctx.restore();
    }
    return placed.map(q => q.key + ':' + q.im.src.split('/').pop());
  },
};

// ---------- type set inside the mark (D: like Fable's Latin text set as a 5) ----------
// The mark rasterised on first use; spans(y0, y1) = runs of x where the whole band y0..y1 is inside the mark.
let maskRowsCache = null;
const maskRows = () => maskRowsCache || (maskRowsCache = (() => {
  const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d');
  x.fillStyle = '#000'; x.fill(markPath);
  const d = x.getImageData(0, 0, W, H).data; const rows = new Array(H);
  for (let y = 0; y < H; y++) { const r = new Uint8Array(W); for (let i = 0; i < W; i++) r[i] = d[(y * W + i) * 4 + 3] > 127 ? 1 : 0; rows[y] = r; }
  return rows;
})());
function spans(y0, y1, pad = 0) {
  const a = Math.max(0, Math.floor(y0)), b = Math.min(H - 1, Math.ceil(y1)); const out = []; let s = -1;
  for (let x = 0; x <= W; x++) {
    let ok = x < W;
    for (let y = a; ok && y <= b; y += 2) ok = maskRows()[y][x] === 1;
    if (ok && s < 0) s = x; if (!ok && s >= 0) { if (x - s > 2 * pad + 8) out.push([s + pad, x - pad]); s = -1; }
  }
  return out;
}
// Fill the mark with runs of styled words. runs: [{text, font, color, underline, gapAfter}], cycled.
function typeset(ctx, runs, { lead, size, pad = 0, ascent = 0.78, wordGap = 0.32, justify = false } = {}) {
  let ri = 0, words = [], wi = 0;
  const next = () => { while (wi >= words.length) { const r = runs[ri++ % runs.length]; words = r.text.split(/\s+/).filter(Boolean).map(word => ({ word, r })); wi = 0; } return words[wi]; };
  for (let y = 0; y + lead <= H; y += lead) {
    for (const [x0, x1] of spans(y, y + lead * 0.92, pad)) {
      let x = x0; const line = [];
      while (true) {
        const t = next(); ctx.font = t.r.font; const w = ctx.measureText(t.word).width;
        if (x + w > x1) { if (line.length === 0 && w > x1 - x0) { wi++; continue; } break; }
        line.push({ ...t, x, wid: w }); x += w + size * wordGap; wi++;
      }
      const extra = justify && line.length > 1 ? (x1 - (x - size * wordGap)) / (line.length - 1) : 0;
      line.forEach((t, k) => {
        const tx = t.x + extra * k; ctx.font = t.r.font; ctx.fillStyle = t.r.color; ctx.fillText(t.word, tx, y + lead * ascent);
        if (t.r.underline) ctx.fillRect(tx, y + lead * ascent + size * 0.12, t.wid, Math.max(1, size * 0.07));
      });
    }
  }
}
window.BOARD = { W, H, S, toPx, markPath, STROKES, along, T, img, drawCover, drawPaper, drawGrain, PAPER, INK, TERMINAL, LIME, paper, spans, typeset, motion: BOARD_MOTION, ctx: g };
})();
