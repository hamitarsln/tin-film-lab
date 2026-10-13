// Render the materials board: every still to out/board/NN-slug.png, then the numbered sheet out/board/BOARD.png.
//   node scripts/board.mjs [--only 3,7] [--outdir out/board] [--w 2160]
// Rendering goes through tools/render.mjs (stills mode), as the house rules require.
import { chromium } from '../tools/node_modules/playwright/index.mjs';
import { spawnSync } from 'node:child_process';
import { mkdirSync, renameSync, rmSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const outdir = resolve(arg('outdir', 'out/board')), W = Number(arg('w', 2160));
const page_ = resolve(arg("page", "src/board.html"));
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 400, height: 400 } });
await page.goto('file://' + page_ + '?render=1&w=400&h=400');
await page.waitForFunction(() => window.FILM && window.FILM.stills);
const stills = await page.evaluate(() => window.STILLS.map(s => ({ n: s.n, slug: s.slug, label: s.label || String(s.n).padStart(2, '0'), title: s.title || s.slug, era: s.era || '', sheet: s.sheet !== false })));
await browser.close();
const only = arg('only') ? arg('only').split(',').map(Number) : null;
const todo = stills.filter(s => only ? only.includes(s.n) : s.sheet);
const tmp = join(outdir, '_raw'); rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp, { recursive: true });
const r = spawnSync('node', ['tools/render.mjs', 'stills', '--page', 'src/board.html', '--at', todo.map(s => s.n).join(','), '--outdir', tmp, '--w', String(W), '--h', String(W)], { stdio: 'inherit' });
if (r.status) process.exit(r.status);
for (const s of todo) {
  const f = join(tmp, `t${s.n.toFixed(3).padStart(8, '0')}.png`);
  renameSync(f, join(outdir, `${s.label}-${s.slug}.png`));
}
rmSync(tmp, { recursive: true, force: true });
writeFileSync(join(outdir, 'stills.json'), JSON.stringify(todo, null, 2));
const s2 = spawnSync('python3', ['scripts/boardsheet.py', outdir], { stdio: 'inherit' });
process.exit(s2.status || 0);
