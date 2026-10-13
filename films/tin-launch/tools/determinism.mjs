// Check the render contract: seek(t) must paint the same pixels no matter which frames came before.
//   node tools/determinism.mjs [page] [times...]
// Seeks the times forward, then in a shuffled order, then backward, and compares the screenshots byte for byte.
import { chromium } from 'playwright';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
const { PNG } = createRequire(import.meta.url)('playwright-core/lib/utilsBundle');

const page_ = resolve(process.argv[2] || 'src/index.html');
const times = (process.argv.slice(3).length ? process.argv.slice(3) : ['0.4', '3.6', '7.9', '12.6', '16.05', '17.3', '19.2', '21.9', '24.3', '29.5']).map(Number);
const W = 960, H = 540;

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', e => errors.push(e.message));
await page.goto('file://' + page_ + `?render=1&w=${W}&h=${H}`);
await page.waitForFunction(() => typeof window.seek === 'function' && window.FILM);
const shot = async t => { await page.evaluate(async t => { await window.seek(t); }, t); return page.screenshot({ type: 'png' }); };

const orders = { forward: [...times], shuffled: [...times].sort((a, b) => ((a * 7919) % 13) - ((b * 7919) % 13)), backward: [...times].reverse() };
const shots = {};
for (const [name, list] of Object.entries(orders)) {
  shots[name] = {};
  for (const t of list) shots[name][t] = await shot(t);
}
// A real leak (state from another frame) moves whole elements; raster noise flips a few edge pixels by a few
// levels. Report both: pixels that differ and the largest channel difference.
function compare(a, b) {
  if (a.equals(b)) return { n: 0, max: 0 };
  const A = PNG.sync.read(a).data, B = PNG.sync.read(b).data;
  let n = 0, max = 0;
  for (let i = 0; i < A.length; i += 4) {
    const d = Math.max(Math.abs(A[i] - B[i]), Math.abs(A[i + 1] - B[i + 1]), Math.abs(A[i + 2] - B[i + 2]));
    if (d) { n++; if (d > max) max = d; }
  }
  return { n, max };
}
let bad = 0;
for (const t of times) {
  const r1 = compare(shots.forward[t], shots.shuffled[t]), r2 = compare(shots.forward[t], shots.backward[t]);
  const n = Math.max(r1.n, r2.n), max = Math.max(r1.max, r2.max);
  const noise = n > 0 && (max <= 6 || (max <= 12 && n < W * H * 0.001));
  if (n && !noise) bad++;
  console.log(`${t.toFixed(3).padStart(7)} s  ${!n ? 'identical' : noise ? `raster noise (${n} px, max ${max}/255)` : `DIFFERS (${n} px, max ${max}/255)`}`);
}
if (errors.length) console.log('page errors:', errors);
console.log(bad ? `${bad} frame(s) depend on history` : 'all frames are pure functions of t (up to antialiasing noise)');
await browser.close();
process.exit(bad || errors.length ? 1 : 0);
