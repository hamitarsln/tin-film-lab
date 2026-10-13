// Write docs/EDIT.md from the cut list the film actually uses (window.EDIT_CUTS in src/film.js), so the plan and the
// film can never disagree.   node scripts/editdoc.mjs
import { chromium } from '../tools/node_modules/playwright/index.mjs';
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 200, height: 200 } });
await page.goto('file://' + resolve('src/index.html') + '?render=1&w=200&h=200');
await page.waitForFunction(() => window.FILM && window.EDIT_CUTS);
const data = await page.evaluate(() => ({
  cuts: window.EDIT_CUTS.map(c => ({ p: c.p, shot: c.shot, note: c.note, t: c.t, f: c.f, holdF: c.holdF,
    title: c.still ? c.still.title : '', era: c.still ? c.still.era : '', treatment: c.still ? c.still.treatment : '',
    extra: c.still ? !!c.still.extra : false, archive: c.still ? c.still.archive : '' })),
  cue: { bpm: window.CUE.bpm, beat: window.CUE.beat, bar: window.CUE.bar, length: window.CUE.length },
  words: window.EDIT_WORDS,
}));
await browser.close();

const { cuts, cue, words } = data;
const sixteenth = cue.beat / 4;
const holdName = c => {
  const n = Math.round((c.holdF / 24) / sixteenth);
  if (n % 16 === 0) return `${n / 16} bar${n > 16 ? 's' : ''}`;
  if (n % 4 === 0) return `${n / 4} beat${n > 4 ? 's' : ''}`;
  if (n === 2) return '8th';
  if (n === 1) return '16th';
  return `${n} 16ths`;
};
const TREAT = { A: 'A, objects along the strokes', B: 'B, inside the mark', C: 'C, mark cut out as paper', D: 'D, the mark in pixels' };
const special = {
  TERM: ['The terminal: an agent\'s marketing log on terminal blue, full bleed', '2026', 'C, mark cut out as paper'],
  DRAIN: ['The blue drains down the frame, uncovering the end card', '', 'end card'],
  END3: ['The pressed tin inside the ink mark (the loop turns it inside out)', '', 'B, inside the mark'],
  END1: ['End card 1: the ink mark on paper over a hairline grid', '', 'end card'],
  END2: ['End card 2: tin.computer and the lime cursor', '', 'end card'],
};
const motion = c => {
  if (c.shot === 'TERM') return 'idle until 8.3.4 (cursor blinks on the beat), then a new log line every 8th';
  if (c.shot === 'DRAIN') return 'the blue lowers down the frame, eased, over one beat';
  if (c.shot === 'END3') return 'still';
  if (c.shot === 'END2') return 'lime cursor blinks every other beat';
  if (c.shot === 'END1') return 'still';
  if (c.shot === '18') return 'still (the GIF and its cursor)';
  if (c.shot === '19') return 'still';
  if (c.holdF >= Math.round(cue.beat * 24) - 1) return c.treatment === 'A' ? 'objects drift' : c.treatment === 'D' ? 'still' : 'push +4.5%/s, slow drift';
  return 'still (too short to move)';
};
const rows = cuts.map((c, i) => {
  const [title, era, tr] = special[c.shot] || [c.title, c.era, TREAT[c.treatment] || c.treatment];
  const src = c.extra ? 'extra' : special[c.shot] ? '' : 'board';
  return `| ${i + 1} | ${c.p} | ${c.t.toFixed(3)} | ${c.f} | ${c.shot} | ${title}${era ? ` (${era})` : ''} | ${src} | ${tr} | ${holdName(c)} (${c.holdF} f) | ${motion(c)} | ${c.note || ''} |`;
});
const board = cuts.filter(c => c.title && !c.extra).length, extras = cuts.filter(c => c.extra).length;
const md = `# Edit plan

Generated from \`src/film.js\` by \`node scripts/editdoc.mjs\`; the film renders exactly this list.

House Vibez (Mixkit #745), song bars 25–35, cut with \`music/tools/cut.py\` (docs/MUSIC.md). ${cue.bpm.toFixed(2)} BPM,
beat ${cue.beat.toFixed(5)} s, bar ${cue.bar.toFixed(5)} s, ${cue.length.toFixed(2)} s, 24 fps. Positions are film
bar.beat.16th from 1.1.1; times are film seconds; frames are 24 fps and each cut is snapped to the nearest frame (at
most 21 ms from the grid). A hold is the time to the next cut.

## Shape
The acceleration copies Fable's withhold, measured in docs/REFERENCE.md (holds of 24, then 12, 6 and 3 frames), and
puts each step on a step of the music.

| Film bars | Music | Cutting | Materials |
|---|---|---|---|
| 1–2 | Breakdown: a hit on each downbeat, hats out, the bass slowly receding | Every two beats (0.98 s, 24 frames), each material pushed in slowly | The pressed tin (prologue), then 1843 to 1882 |
| 3–4 | The same, the riser beginning | Every beat (0.49 s, 12 frames) | 1902 to 1939 |
| 5–6 | An 8th-note pulse; the bass falls away | Every 8th (0.25 s, 6 frames): board stills with catalogue extras between them | 1900s ephemera to the 1940s radio, the first neon |
| 7 | The bass is gone, the riser peaks | Every 16th (3 frames) | The roadside at night, the 1950s and 60s, ending on punched cards |
| 8 | **The stop**: a hit, near silence, a hit on 8.3.4, a 16th fill | Two holds, each on a hit; "Your agent" read in the silence | 1996 banner, 2004 search page |
| 9 | **The drop** | One bar on the terminal; "runs it." | 2026 |
| 10–11 | The groove, fading out over the last 1.5 bars | The blue drains (one beat), the grid card, then tin.computer through the fade | End card |

${cuts.length} shots: ${board} board stills, ${extras} catalogue extras, the terminal and the end card states. The film
loops: the last frame (end card) cuts to the first (the pressed tin), the mark in the same place.

## Every cut
| # | Pos | Time (s) | Frame | Shot | Material | Source | Treatment | Hold | Motion | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
${rows.join('\n')}

## Words
${words.map(w => `- **"${w.text}"** from ${w.from} (${w.t.toFixed(3)} s) to ${w.to} (${w.tEnd.toFixed(3)} s).`).join('\n')}
- Both sit on the terminal: "Your agent" over the idle terminal through the near-silence, "runs it." from the hit at
  8.3.4, when the log starts to run. Funktional Grotesk Medium, ink, 150 px at 2160, centred on the mark with the
  baseline resting just above its top edge (Opus's grammar). No typing, no fades.

## Motion
- The mark never moves. Materials held a beat or longer are pushed in at 3% a second about the frame centre (the mark
  stays put, the material moves under it); arranged objects drift a few pixels and a fraction of a degree instead.
- Strobe frames (8ths and 16ths) are still: there is nothing to see in three frames but the material.
- Grain changes every frame (a grain field shifted and mirrored by a frame-seeded offset); the paper itself is fixed.
- No transitions: every change is a hard cut on the grid. The one progressive change is the drain, which the brief
  asks for, and it takes one beat.
`;
writeFileSync('docs/EDIT.md', md);
writeFileSync('out/cuts.json', JSON.stringify(cuts, null, 1));
console.log('docs/EDIT.md', cuts.length, 'cuts');
