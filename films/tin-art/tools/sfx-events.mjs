// Dump the film's sound-effect events from the page itself, so every click sits on the frame that shows it.
//   node tools/sfx-events.mjs [page] > sfx/events.json
// Keys: one per character as it appears in the terminal (command, prompt), Enter on the two returns.
// Clicks: the cursor's presses.
import { chromium } from 'playwright';
import { resolve } from 'node:path';

const page_ = resolve(process.argv[2] || 'src/index.html');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 960, height: 540 } });
await page.goto('file://' + page_ + '?render=1&w=960&h=540');
await page.waitForFunction(() => typeof window.seek === 'function' && window.FILM);
const events = await page.evaluate(() => {
  const { T, typedLenFit } = F;
  const out = [];
  // The same strings, windows and seeds the terminal types with (src/scenes/terminal.js).
  const lines = [
    ['claude mcp add --transport http tin https://app.tin.computer/mcp', T(3, 1), T(3, 4.5), 11],
    ['Use Tin to grow my project like a pro!', T(4, 2), T(4, 4), 23],
  ];
  for (const [text, t0, t1, seed] of lines) {
    let prev = 0;
    for (let t = t0 - 0.002; t <= t1 + 0.002; t += 0.0005) {
      const n = typedLenFit(text, t, t0, t1, seed);
      if (n > prev) { for (let k = prev; k < n; k++) out.push({ t: +t.toFixed(4), kind: text[k] === ' ' ? 'space' : 'key' }); prev = n; }
    }
  }
  out.push({ t: +T(4, 1).toFixed(4), kind: 'enter' }, { t: +T(5, 1).toFixed(4), kind: 'enter' });
  for (const p of Cursor.PRESSES) out.push({ t: +p.toFixed(4), kind: 'click' });
  return out.sort((a, b) => a.t - b.t);
});
console.log(JSON.stringify(events));
await browser.close();
