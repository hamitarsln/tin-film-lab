// Render every material the film uses, in film order, at 2160 px, for the critique: board stills, the strobe extras,
// the terminal and the end card (src/board.html seek(n), the same draw functions the film calls at rest).
//   node scripts/filmstills.mjs <outdir>        ->  <outdir>/NN-label-slug.png, stills.json, then sheets via python
import { chromium } from '../tools/node_modules/playwright/index.mjs';
import { spawnSync } from 'node:child_process';
import { mkdirSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const outdir = resolve(process.argv[2] || 'out/film-stills');
mkdirSync(outdir, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 200, height: 200 } });
await page.goto('file://' + resolve('src/index.html') + '?render=1&w=200&h=200');
await page.waitForFunction(() => window.FILM && window.EDIT_CUTS);
const order = await page.evaluate(() => window.EDIT_CUTS.map(c => c.shot));
await page.goto('file://' + resolve('src/board.html') + '?render=1&w=200&h=200');
await page.waitForFunction(() => window.FILM && window.STILLS);
const stills = await page.evaluate(() => window.STILLS.map(s => ({ n: s.n, label: s.label, slug: s.slug, title: s.title, era: s.era || '', treatment: s.treatment || '', extra: !!s.extra })));
await browser.close();
const byLabel = Object.fromEntries(stills.map(s => [s.label, s]));
const seen = new Set(), todo = [];
for (const lab of order) {
  const key = lab === 'TERM' || lab === 'DRAIN' ? '20' : lab === 'END1' || lab === 'END2' ? 'E' : lab;
  if (seen.has(key) || !byLabel[key]) continue;
  seen.add(key); todo.push(byLabel[key]);
}
const tmp = join(outdir, '_raw'); rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp, { recursive: true });
const r = spawnSync('node', ['tools/render.mjs', 'stills', '--page', 'src/board.html', '--at', todo.map(s => s.n).join(','), '--outdir', tmp, '--w', '2160', '--h', '2160'], { stdio: 'inherit' });
if (r.status) process.exit(r.status);
const list = todo.map((s, i) => {
  const name = `${String(i + 1).padStart(2, '0')}-${s.label}-${s.slug}.png`;
  renameSync(join(tmp, `t${s.n.toFixed(3).padStart(8, '0')}.png`), join(outdir, name));
  return { ...s, file: name, order: i + 1 };
});
rmSync(tmp, { recursive: true, force: true });
writeFileSync(join(outdir, 'stills.json'), JSON.stringify(list, null, 1));
const s2 = spawnSync('python3', ['scripts/filmboard.py', outdir], { stdio: 'inherit' });
process.exit(s2.status || 0);
