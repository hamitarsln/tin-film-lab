// Measure every material at rest (src/board.html) for planning the cut: mean relative luminance, an 8x8 grid of cell
// luminance (for the flash check), the mean colour and the share of the frame that is paper. Writes out/materials.json.
//   node scripts/strobeplan.mjs
import { chromium } from '../tools/node_modules/playwright/index.mjs';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';
const { PNG } = createRequire(import.meta.url)('../tools/node_modules/playwright-core/lib/utilsBundle');

const N = 128;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: N, height: N }, deviceScaleFactor: 1 });
await page.goto('file://' + resolve('src/board.html') + `?render=1&w=${N}&h=${N}`);
await page.waitForFunction(() => window.FILM && window.STILLS, null, { timeout: 120000 });
const list = await page.evaluate(() => window.STILLS.filter(s => s.n < 300).map(s => ({ n: s.n, label: s.label, slug: s.slug, title: s.title, era: s.era || '', treatment: s.treatment || '', extra: !!s.extra })));
const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
const out = [];
for (const s of list) {
  await page.evaluate(async sn => { await window.seek(sn); }, s.n);
  const d = PNG.sync.read(await page.screenshot({ type: 'png' })).data;
  const cells = new Array(64).fill(0), cnt = new Array(64).fill(0);
  let R = 0, G = 0, Bc = 0, Y = 0, paper = 0;
  for (let i = 0, p = 0; i < d.length; i += 4, p++) {
    const y = 0.2126 * lin(d[i]) + 0.7152 * lin(d[i + 1]) + 0.0722 * lin(d[i + 2]);
    const cx = Math.floor((p % N) / (N / 8)), cy = Math.floor(Math.floor(p / N) / (N / 8));
    cells[cy * 8 + cx] += y; cnt[cy * 8 + cx]++; Y += y; R += d[i]; G += d[i + 1]; Bc += d[i + 2];
    if (Math.abs(d[i] - 245) < 10 && Math.abs(d[i + 1] - 241) < 10 && Math.abs(d[i + 2] - 230) < 12) paper++;
  }
  const np = d.length / 4;
  out.push({ ...s, Y: Y / np, cells: cells.map((v, k) => v / cnt[k]), rgb: [R / np, G / np, Bc / np], paper: paper / np });
}
await browser.close();
writeFileSync('out/materials.json', JSON.stringify(out, null, 1));
for (const o of out) console.log(`${o.label.padEnd(5)} ${o.treatment.padEnd(2)} Y ${o.Y.toFixed(2)}  paper ${o.paper.toFixed(2)}  rgb ${o.rgb.map(v => v.toFixed(0)).join(',').padEnd(12)} ${o.title.slice(0, 50)}`);
