// Board stills. seek(n) paints still n. Arc order 1-20, alternates 21-24, end card 25.
// Every image here is recorded in materials/ASSETS.md; "made in code" stills say so.
(() => {
const B = window.BOARD;
const cut = p => `../materials/cut/${p}`;
// Prepared files are named <nn>-<slug>[-kk].png (materials skill); MANIFEST.json maps each to its archive ids.
const TEX = { playbill: '02-wood-type', seebach: '04-tin-sign', olibet: '05-biscuit-tin', owl: '06-can-label', classifieds: '07-classifieds',
  seedannual: '08-seed-catalogue', htcode: '09-halftone', htprint: '09-halftone-print', htnews: '09-halftone-news', gem: '11-painted-wall', billboard: '12-billboard', lucky: '14-neon',
  dial: '15-radio-dial', testcard: '17-television', pixels: '18-banner-pixels', ceiling: 'A2-alt-tin-ceiling', vick: 'A3-alt-vick-seeds',
  sonrise: 'A4-alt-neon-donuts' };
const tex = n => cut(`${TEX[n]}.png`);
const set = (name, n) => Array.from({ length: n }, (_, k) => cut(`${name}-${String(k + 1).padStart(2, '0')}.png`));

// ---------- object sets (treatment A) ----------
// Each set is numbered in the order it is laid along the strokes, hand-ordered so neighbours differ in colour and shape.
const ENGRAVED = set('01-engraved-cards', 9);
// Ordered so neighbours differ in colour (scripts: greedy max colour distance). 08 (Manhattan Watch Co.) is excluded: it has
// small drawn dock workers (no people, CLAUDE.md); 11 ("How Owl'd Are You") is excluded so the owl is not seen twice
// (06 is the Owl Brand label). 23-26 were added so the places along the strokes never repeat a card.
const byNum = (name, nums) => nums.map(k => cut(`${name}-${String(k).padStart(2, '0')}.png`));
const TRADE = byNum('03-trade-cards', [1, 18, 6, 7, 22, 13, 9, 2, 17, 25, 26, 15, 10, 4, 24, 3, 20, 14, 5, 19, 12, 23, 21, 16]);
// 01 (LEW) excluded from the film: Lechwerke AG still trades as LEW, a current company name
const STAMPS = set('10-poster-stamps', 16).filter(f => !f.endsWith('-01.png'));
// 22 (Hotel Allen) is excluded: tiny drawn pedestrians on its sidewalk. 23-28 were added (Commons, PD) so no cover repeats.
// Trade tokens (1888-97, NPM Owney collection, CC0): 'good for 5c in trade', saloon, bakery, dairy, barber tokens.
const TOKENS = set('X50-tokens', 24);
const MATCHES = byNum('13-matchbooks', [1, 26, 28, 23, 17, 21, 25, 6, 19, 10, 14, 13, 5, 7, 16, 12, 15, 11, 2, 4, 3, 27, 8, 9, 18, 20, 24]);
const PUNCH = set('16-punch-cards', 2);
const SAFES = set('A1-alt-match-safes', 12);

// ---------- treatment helpers ----------
const inside = (name, crop) => async g => B.T.inside(g, await B.img(tex(name)), crop);
const knock = (name, crop, fill) => async g => B.T.knockout(g, await B.img(tex(name)), crop, fill);
const chain = (list, opts) => async g => B.T.chain(g, await Promise.all(list.map(B.img)), opts);

// ---------- made in code: a search results page (c. 2004), framed and seen through the mark ----------
const RESULTS = [
  ['Tin Signs - Vintage Embossed Advertising Signs', 'Original embossed tin signs from 1890 to 1940. Soap, seed, coffee and feed signs, graded and photographed. Free shipping on orders over $50.', 'www.example.com/tin-signs/ - 14k'],
  ['History of Advertising: Trade Cards and Posters', 'Merchants handed out chromolithographed trade cards by the million. A short history of the card, the poster and the painted wall sign.', 'www.example.org/history/trade-cards.html - 22k'],
  ['Classified Ads - Buy, Sell and Trade Locally', 'Wanted, for sale, situations, rooms to let. Place a classified ad in minutes. Over 40,000 listings updated daily.', 'classifieds.example.net/ - 9k'],
  ['Heirloom Seed Catalog - Vegetables Since 1876', 'Order the free seed catalog. Tomatoes, beans, radishes, melons and squash, with planting guides for every zone.', 'www.example.com/seeds/catalog.html - 31k'],
  ["Matchbook Covers: A Collector's Guide", 'Hotels, cafes and night clubs gave away matchbooks with their name on the cover. Values, grading and storage.', 'www.example.org/matchcovers/ - 18k'],
  ['Neon Sign Repair and Glass Bending', 'Hand-bent neon tubing, transformers and restoration for vintage signs. Free estimates.', 'neon.example.com/ - 7k'],
  ['Punched Cards and the Census of 1890', 'How tabulating machines read holes in cards, and how the mailing list began.', 'www.example.edu/punched-cards/ - 26k'],
  ['Banner Ads That Work: 468 x 60 Tips', 'Animated GIF banners, click-through rates and the web-safe palette. Ten mistakes to avoid.', 'www.example.com/banners/tips.html - 12k'],
  ['Search Engine Marketing for Beginners', 'Keywords, sponsored links and landing pages explained. Bid on the words your customers type.', 'www.example.net/sem/guide.html - 20k'],
  ['Billboard Advertising Rates and Locations', 'Bulletins, posters and painted walls. Find a billboard near a highway in your town.', 'www.example.com/outdoor/rates.html - 15k'],
  ['Radio Advertising: How to Buy Airtime', 'Spots, jingles and drive time. A plain guide for small businesses.', 'www.example.org/radio/buy.html - 11k'],
  ['Direct Mail Lists - Rent a Mailing List', 'Targeted lists by zip code, age and interest. Postcards, letters and catalogs.', 'lists.example.com/ - 8k'],
];
// ---------- made in code: the terminal (2026) ----------
// Tin's agent surface (DESIGN.md: terminal blue is the live agent surface, ink text, monospace chrome) at full bleed:
// terminal blue edge to edge, the agent's marketing log running across the frame from the mark's cap line down, the
// mark cut out of it as paper. The band above the cap line stays clear for the words.
const LOG = [
  "09:14:02  › agent connected · project: tin · autonomy: standard · 3 channels · reading context",
  "09:14:05  › reading the product docs, the changelog and last week's report before drafting",
  "09:14:31  ✓ docs indexed · 41 pages · tone guide loaded · 6 open questions noted for review",
  "09:15:10  › drafting the launch post · plain tone · two headlines to compare · 180 words each",
  "09:16:44  › drafting replies to 6 comments on yesterday's thread · 2 need a product answer",
  "09:17:02  ✓ replies queued for your review · 2 need a decision from you · nothing sent yet",
  "09:18:20  › signups are up 14% on last week · source: tuesday's forum post · noted in report",
  "09:19:05  ✓ weekly report written to reports/week-41.md · 3 charts · 1 recommendation",
  "09:20:12  › scheduling posts for tue, thu and sat at 10:00 local · one per channel · drafts attached",
  "09:20:40  ✓ 3 posts scheduled · nothing is published without your approval · undo available",
  "09:22:03  › watching mentions · 4 new · 1 question about self-hosting · drafting an answer",
  "09:23:47  › drafting the changelog note for v0.9 · 120 words · links to the pull requests",
  "09:24:15  ✓ changelog note ready for review · suggested send time thursday 09:00",
  "09:26:31  › testing two headlines on the pricing page · 1,204 visits · 95% interval reported",
  "09:27:02  ✓ headline b kept · 6.1% vs 4.8% · test closed · result added to the weekly report",
  "09:28:40  › pricing page copy updated · opened as a pull request for your review",
  "09:29:12  › 3 new docs issues · 1 duplicate · drafting replies to the other two",
  "09:30:05  ✓ newsletter draft ready · 412 words · 2 links · waiting for your approval",
  "09:31:40  › reading 12 replies to last week's newsletter · 2 bug reports · 1 thank-you",
  "09:32:18  ✓ 2 bug reports filed with steps to reproduce · the thank-you answered",
  "09:33:51  › comparing this week against the plan · 2 goals ahead · 1 behind",
  "09:34:26  ✓ plan updated · 2 decisions waiting for you · summary sent to your inbox",
  "09:35:02  › drafting a reply to the self-hosting question · linking the docker guide",
  "09:35:40  ✓ reply drafted · waiting for your review · nothing sent without approval",
  "09:36:15  › preparing next week's calendar · 5 posts · 1 newsletter · 1 launch note",
  "09:37:02  ✓ calendar ready · open it with `tin plan` · every item can be edited or dropped",
  "09:38:44  › checking links in the launch post · 7 of 7 resolve · images under 200 kb",
  "09:39:10  ✓ launch post ready · two headlines attached · waiting for your pick",
];
// o: { scroll (log lines advanced), cursor (bool), level (frame px: above it the blue has drained away) }
function terminal(g, o = {}) {
  const k = B.W / 2160, size = 46 * k, lead = 62 * k, x0 = 64 * k;
  const [, cap] = B.toPx(0, 174);
  const lvl = o.level || 0;
  g.save();
  g.beginPath(); g.rect(0, lvl, B.W, B.H - lvl); g.clip();
  g.fillStyle = B.TERMINAL; g.fillRect(0, 0, B.W, B.H);
  g.font = `500 ${size}px "SF Mono", monospace`; g.fillStyle = 'rgba(8,8,8,0.86)'; g.textBaseline = 'alphabetic';
  const rows = Math.floor((B.H - cap - 30 * k) / lead), scroll = o.scroll || 0;
  let y = cap + 36 * k;
  for (let r = 0; r < rows - 1; r++, y += lead) g.fillText(LOG[(scroll + r) % LOG.length], x0, y);
  g.fillText('›', x0, y);
  if (o.cursor !== false) g.fillRect(x0 + size * 1.05, y - size * 0.76, size * 0.6, size * 0.98);
  g.save(); g.clip(B.markPath); B.drawPaper(g); g.restore();
  g.restore();
}
// ---------- the end card (Fable's two-card ending in Tin's colours) ----------
// The ink mark over a hairline ink grid whose lines fall on the mark's cap line and baseline; the lines sit about 7
// levels below the paper, as Fable's do (5-8), so it reads as a ground, not graph paper. Then tin.computer with a lime
// block cursor, the only lime in the film.
function grid(g, alpha = 0.03) {
  const pitch = 150 * B.W / 2160, [lx, top] = B.toPx(46, 174), [, base] = B.toPx(0, 548);
  const p = (base - top) / Math.round((base - top) / pitch);
  g.save(); g.fillStyle = `rgba(8,8,8,${alpha})`; const lw = Math.max(1, 2 * B.W / 2160);
  for (let x = lx % p; x < B.W; x += p) g.fillRect(Math.round(x - lw / 2), 0, lw, B.H);
  for (let y = top % p; y < B.H; y += p) g.fillRect(0, Math.round(y - lw / 2), B.W, lw);
  g.restore(); return p;
}
function inkMark(g) { g.fillStyle = B.INK; g.fill(B.markPath); }
function url(g, cursorOn = true) {
  const k = B.W / 2160, [, base] = B.toPx(0, 548), [, top] = B.toPx(0, 174);
  const p = (base - top) / Math.round((base - top) / (150 * k));
  const size = 150 * k; g.save(); g.font = `500 ${size}px "Funktional Grotesk"`; g.fillStyle = B.INK; g.textAlign = 'center';
  const ty = base + p * 1.5 + size * 0.36; g.fillText('tin.computer', B.W / 2, ty);
  const w = g.measureText('tin.computer').width;
  if (cursorOn) { g.fillStyle = B.LIME; g.fillRect(B.W / 2 + w / 2 + size * 0.18, ty - size * 0.74, size * 0.46, size * 0.9); }
  g.restore();
}
function endcard(g) { grid(g); inkMark(g); url(g); }
// 16: the blue 80-column card alone, cropped inside its printed area (the scan bed shows below row 977 and in the side
// margins), scaled just enough to cover the whole mark, level and centred.
async function punch(g) {
  const im = await B.img(PUNCH[0]);
  const sx = 14, sy = 8, sw = im.naturalWidth - 30, sh = 966;
  const [x0, y0] = B.toPx(46, 174), [x1, y1] = B.toPx(654, 548);
  const k = Math.max((x1 - x0) * 1.06 / sw, (y1 - y0) * 1.05 / sh) * B.motion.push;
  g.save(); g.clip(B.markPath);
  g.drawImage(im, sx, sy, sw, sh, B.W / 2 - sw * k / 2, (y0 + y1) / 2 - sh * k / 2, sw * k, sh * k);
  g.restore();
}
async function pixels(g) { g.drawImage(await B.img(tex('pixels')), 0, 0, B.W, B.H); }

// ---------- made in code: the 2004 results page laid out at frame scale ----------
// o: { scale, top (page top edge, frame px), lead, dense, fill (lines run past the frame), sponsored (right column) }
// Generic page: example.com domains, no real engine or brand. Query words are bold, as results pages of the time bolded them.
const SPONSORED = [
  ['Tin Signs at Low Prices', 'Huge selection of reproduction tin signs. Fast shipping.', 'www.example.com'],
  ['Advertise Your Business', 'Reach customers searching now. Pay only per click.', 'ads.example.net'],
  ['Antique Advertising', 'Matchbooks, trade cards, labels. Buy and sell online.', 'www.example.org'],
  ['Neon Signs Made to Order', 'Custom neon for shops and bars. Free quote today.', 'neon.example.com'],
  ['Seed Catalogs Free', 'Order 2004 garden catalogs from 40 growers.', 'seeds.example.net'],
  ['Banner Design $49', 'Animated GIF banners that get the click.', 'www.example.biz'],
];
function serpCanvas(o) {
  const c = document.createElement('canvas'); c.width = B.W; c.height = B.H; const x = c.getContext('2d');
  const k = B.W / 2160 * o.scale, F = (w, s) => `${w} ${s * k}px "Liberation Sans", Arial, sans-serif`;
  const top = o.top || 0;
  x.fillStyle = '#ffffff'; x.fillRect(0, top, B.W, B.H - top);
  // the results bar: a 1 px blue rule and a pale blue band, "Results 1 - 10 of about ..." set in it
  const barH = 30 * k;
  x.fillStyle = '#3366cc'; x.fillRect(0, top, B.W, Math.max(2, 1.4 * k));
  x.fillStyle = '#e5ecf9'; x.fillRect(0, top + 1.4 * k, B.W, barH);
  x.textBaseline = 'alphabetic'; x.fillStyle = '#000';
  x.font = F(700, 17); x.fillText('Web', 14 * k, top + 21 * k);
  x.font = F(400, 13);
  const info = 'Results 1 - 10 of about 2,140,000 for tin signs';
  x.textAlign = 'right'; x.fillText(info, B.W - 14 * k, top + 20 * k); x.textAlign = 'left';
  const Q = /^(tin|signs?|advertising|ads?|cards?|catalogs?|matchbooks?|neon|banners?)[.,:]?$/i;
  const words = (text, size, color, xx, line, bold, under, maxW) => {
    const x0 = xx;
    for (const w of text.split(' ')) {
      const isQ = bold && Q.test(w); x.font = F(isQ ? 700 : 400, size);
      const ww = x.measureText(w).width, sp = x.measureText(' ').width;
      if (maxW && xx + ww - x0 > maxW) break;
      x.fillStyle = color; x.fillText(w, xx, line);
      if (under) x.fillRect(xx, line + size * 0.14 * k, ww + sp, Math.max(1, size * 0.075 * k));
      xx += ww + sp;
    }
  };
  // main column. With o.fill every line runs on past the right edge of the frame (each result's own text, then the
  // next result's), so no line ends inside the mark and the cut-out keeps its edge everywhere.
  const colW = o.fill ? Infinity : o.sponsored ? 640 * k : B.W;
  let y = top + barH + 34 * k, i = 0;
  const lead = o.lead || (o.dense ? 1.18 : 1.3);
  const run = (parts, size, color, line, bold, under) => {
    if (!o.fill) { words(parts[0], size, color, 14 * k, line, bold, under, colW); return; }
    let text = parts.join(' '); x.font = F(400, size);
    while (x.measureText(text).width < B.W * 1.15) text += ' ' + parts.join(' ');
    words(text, size, color, 14 * k, line, bold, under, B.W * 1.2);
  };
  while (y < B.H + 40 * k) {
    const r0 = RESULTS[i % RESULTS.length], r1 = RESULTS[(i + 5) % RESULTS.length], r2 = RESULTS[(i + 3) % RESULTS.length];
    run([r0[0], '-', r2[0]], 16, '#0000cc', y, true, true); y += 16 * lead * k + 2 * k;
    run([r0[1], r2[1]], 13, '#000000', y, true, false); y += 13 * lead * k;
    run([r1[1], r0[1]], 13, '#000000', y, true, false); y += 13 * lead * k;
    run([r0[2], '-', r1[2]], 13, '#008000', y, false, false); y += (o.dense ? 22 : 28) * k;
    i++;
  }
  if (o.sponsored) {
    const sx = 690 * k;
    x.fillStyle = '#c9d7f1'; x.fillRect(sx - 14 * k, top + barH + 6 * k, Math.max(1, 1 * k), B.H);
    x.font = F(400, 11); x.fillStyle = '#666'; x.fillText('Sponsored Links', sx, top + barH + 22 * k);
    let yy = top + barH + 46 * k, j = 0;
    while (yy < B.H + 40 * k) {
      const [t, sn, u] = SPONSORED[j % SPONSORED.length];
      words(t, 14, '#0000cc', sx, yy, true, true); yy += 17 * k;
      words(sn, 12, '#000000', sx, yy, false, false, 300 * k); yy += 15 * k;
      words(u, 12, '#008000', sx, yy, false, false); yy += 30 * k;
      j++;
    }
  }
  return c;
}
let serpCache = {};
const serpOf = (key, o) => serpCache[key] || (serpCache[key] = serpCanvas(o));
// 19: the page inside the mark, framed by Tin's ink rule (DESIGN.md frames UI tiles in solid ink). A white page on
// Tin's paper has no edge of its own, so the rule carries the mark: lw = 8 px at 2160 stays over a pixel at 360 px.
// The page is set at 2.2x a 2004 page, every line running past the frame, so each stroke holds whole rows of blue
// titles, black snippets and green URLs, and the pale blue results bar runs along the tops of the strokes.
function serpInsideFramed(g, scale = 2.2, lw = 8, top = 168) {
  const pg = serpOf(`a${scale}-${top}`, { scale, lead: 1.12, top: B.toPx(0, top)[1], fill: true, dense: true });
  g.save(); g.clip(B.markPath); g.drawImage(pg, 0, 0); g.restore();
  g.save(); g.strokeStyle = '#080808'; g.lineWidth = lw * B.W / 2160; g.lineJoin = 'miter'; g.stroke(B.markPath); g.restore();
}
// 19: the page inside the mark, on Tin's deep paper (DESIGN.md paper-deep #B9AE98): the paper's own fibres, darkened,
// so the white page reads as a lit screen without an outline.
let deepPaper = null;
function drawDeepPaper(g) {
  if (!deepPaper) {
    deepPaper = document.createElement('canvas'); deepPaper.width = B.W; deepPaper.height = B.H;
    const x = deepPaper.getContext('2d'); x.drawImage(B.paper, 0, 0);
    x.globalCompositeOperation = 'multiply'; x.fillStyle = 'rgb(193,184,166)'; x.fillRect(0, 0, B.W, B.H);
  }
  g.drawImage(deepPaper, 0, 0);
}
function serpOnDeep(g, scale = 2.0) {
  drawDeepPaper(g);
  const pg = serpOf(`d${scale}`, { scale, lead: 1.08, top: B.toPx(0, 168)[1], fill: true, dense: true });
  g.save(); g.clip(B.markPath); g.drawImage(pg, 0, 0); g.restore();
}
// ---------- strobe extras ----------
// Chains (treatment A): objects end to end along each stroke, inside the silhouette. The n's arch takes objects
// across it (they turn with the curve); its right leg is a stem like the others.
const CH = (o) => Object.assign({ orient: 'long', cross: 0.96, overlap: 0.06, rotJitter: 2.5, upright: true }, o,
  { per: Object.assign({ narch: { orient: 'short', cross: 0.92, overlap: 0.48, rotJitter: 1.5 }, nright: { orient: 'long' } }, o.per || {}) });
const xt = f => cut(f);
const xin = f => async g => B.T.inside(g, await B.img(xt(f)));
const xko = f => async g => B.T.knockout(g, await B.img(xt(f)));
const EXTRAS = [
  ['X01', 'neon-nelch', 'Neon, building-materials yard', '1930s–1950s · Springfield, Ill.', 'Library of Congress (Highsmith)', 'C', [xt('X01-neon-nelch.png')], xko('X01-neon-nelch.png')],
  ['X02', 'neon-monkey', 'Neon trade sign, a monkey', '1930s–1950s', 'Smithsonian American Art Museum', 'B', [xt('X02-neon-monkey.png')], xin('X02-neon-monkey.png')],
  ['X03', 'bulbs-spectacles', "Optician's sign, bulbs", '20th century', 'Smithsonian American Art Museum', 'B', [xt('X03-bulbs-spectacles.png')], xin('X03-bulbs-spectacles.png')],
  ['X04', 'neon-parrot', 'Neon, a gasoline parrot', '1930s–1960s · Pueblo, Colo.', 'Wikimedia Commons (Highsmith)', 'B', [xt('X04-neon-parrot.png')], xin('X04-neon-parrot.png')],
  ['X05', 'oyster-can', 'Lithographed oyster can', '1935–1950 · Nanticoke, Md.', 'Smithsonian NMAAHC', 'B', [xt('X05-oyster-can.png')], xin('X05-oyster-can.png')],
  ['X06', 'dye-cabinet', 'Tin dye cabinet, instruction panel', '1900s–1920s', 'Science History Institute via Commons', 'B', [xt('X06-dye-cabinet.png')], xin('X06-dye-cabinet.png')],
  ['X07', 'label-ramrod', 'Tobacco wrap label', 'c. 1900 · Detroit', 'Cooper Hewitt', 'B', [xt('X07-label-ramrod.png')], xin('X07-label-ramrod.png')],
  ['X08', 'label-oceanic', 'Tobacco wrap label', 'c. 1900 · Detroit', 'Cooper Hewitt', 'C', [xt('X08-label-oceanic.png')], xko('X08-label-oceanic.png')],
  ['X09', 'label-union', 'Tobacco wrap label', 'c. 1900 · Detroit', 'Cooper Hewitt', 'B', [xt('X09-label-union.png')], xin('X09-label-union.png')],
  ['X10', 'wall-railway', 'Painted railway sign on brick', 'early 20th c. · Dallas', 'Library of Congress (Highsmith)', 'C', [xt('X10-wall-railway.png')], xko('X10-wall-railway.png')],
  ['X11', 'wall-salvage', 'Ghost signs, salvage yard', 'early 20th c. · Petersburg, Va.', 'Library of Congress (Highsmith)', 'C', [xt('X11-wall-salvage.png')], xko('X11-wall-salvage.png')],
  ['X12', 'label-woodcock', 'Can label, Woodcock Brand tomatoes', '1885', 'Library of Congress', 'B', [xt('X12-label-woodcock.png')], xin('X12-label-woodcock.png')],
  ['X13', 'label-seeds', 'Seed label, Northern Grown Seeds', '1887', 'Library of Congress', 'C', [xt('X13-label-seeds.png')], xko('X13-label-seeds.png')],
  ['X14', 'embossed-case', 'Embossed aluminium advertising case', 'early 1900s', 'Smithsonian NPM', 'B', [xt('X14-embossed-case.png')], xin('X14-embossed-case.png')],
  ['X15', 'neon-vacancy', 'Neon motel sign, alternate crop', '1950s · Las Vegas', 'Library of Congress (Highsmith)', 'B', [xt('X15-neon-vacancy.png')], xin('X15-neon-vacancy.png')],
  ['X16', 'tin-sign-lettering', 'Tin sign, alternate crop', '1910s–1930s · Austria', 'Wikimedia Commons', 'B', [xt('X16-tin-sign-lettering.png')], xin('X16-tin-sign-lettering.png')],
  ['X17', 'wall-dog', 'Painted wall sign, alternate crop', '1930s–1950s · Durham', 'Library of Congress (Highsmith)', 'C', [xt('X17-wall-dog.png')], xko('X17-wall-dog.png')],
  ['X18', 'billboard-layers', 'Billboard paste-up, alternate crop', '1939 · Minneapolis', 'Library of Congress (FSA)', 'B', [xt('X18-billboard-layers.png')], xin('X18-billboard-layers.png')],
  ['X19', 'radio-scale', 'Radio dial, alternate crop', '1940s', 'Wikimedia Commons', 'C', [xt('X19-radio-scale.png')], xko('X19-radio-scale.png')],
  ['X20', 'want-ads-1904', 'Want ads, another day', '1904 · Washington', 'Library of Congress (Chronicling America)', 'B', [xt('X20-want-ads-1904.png')], xin('X20-want-ads-1904.png')],
  ['X21', 'neon-donuts', 'Neon, donut shop', '1950s · Springfield, Ill.', 'Library of Congress (Highsmith)', 'C', [tex('sonrise')], knock('sonrise')],
  ['X22', 'match-safes', 'Advertising match safes', '1890s–1910s', 'Cooper Hewitt', 'A', SAFES,
    chain(SAFES, CH({ seed: 3, cross: 0.96, overlap: 0.05, rotJitter: 4, per: {} }))],
  ['X23', 'poster-stamps', 'Advertising poster stamps', '1905–1921', 'Wikimedia Commons', 'A', STAMPS,
    chain(STAMPS, CH({ seed: 11, orient: 'auto', cross: 0.96, overlap: 0.06, rotJitter: 5, pick: (n, r) => (n * 7 + 3) % 16, per: {} }))],
  ['X24', 'matchbook-pile', 'Matchbook covers, a pile', '1927–1962', 'Wikimedia Commons', 'C', MATCHES,
    async g => B.T.pile(g, await Promise.all(MATCHES.map(B.img)), { seed: 5, n: 140, size: 420, rotJitter: 30, region: [-200, -200, B.W + 200, B.H + 200], pick: (i, r) => Math.floor(r() * 22) })],
  ['X25', 'seed-lithograph', 'Seed company chromolithograph', '1870s · Rochester', 'Cleveland Museum of Art', 'C', [tex('vick')], knock('vick')],
  ['X27', 'wood-type-specimen', 'Wood-type specimen, condensed gothic', 'c. 1840 · New York', 'NYPL via Commons', 'C', [xt('X27-wood-type-specimen.png')], xko('X27-wood-type-specimen.png')],
  ['X28', 'catalogue-caps', 'Mail-order price list, caps', '1884 · New York', 'Smithsonian NMAH', 'B', [xt('X28-catalogue-caps.png')], xin('X28-catalogue-caps.png')],
  ['X29', 'neon-tropics', 'Neon, the Tropics restaurant (Route 66)', '1950 · Lincoln, Ill.', 'Library of Congress (Highsmith)', 'C', [xt('X29-neon-tropics.png')], xko('X29-neon-tropics.png')],
  ['X30', 'neon-hotel', 'Neon, HOTEL', 'mid-century · Tucson', 'Library of Congress (Highsmith)', 'C', [xt('X30-neon-hotel.png')], xko('X30-neon-hotel.png')],
  ['X31', 'bulbs-sputnik', 'Bulb sign, a sputnik', 'c. 1958 · Springfield, Ill.', 'Library of Congress (Highsmith)', 'C', [xt('X31-bulbs-sputnik.png')], xko('X31-bulbs-sputnik.png')],
  ['X32', 'neon-white-haven', 'Neon, White Haven Motor Lodge', '1957 · Overland Park, Kan.', 'Library of Congress (Highsmith)', 'C', [xt('X32-neon-white-haven.png')], xko('X32-neon-white-haven.png')],
  ['X33', 'neon-kaiser-frazer', 'Neon dealer sign, Kaiser-Frazer', '1946–1953 · Payson, Ariz.', 'Library of Congress (Highsmith)', 'B', [xt('X33-neon-kaiser-frazer.png')], xin('X33-neon-kaiser-frazer.png')],
  ['X34', 'neon-drugs', 'Neon, DRUGS / Prescriptions', 'mid-century · Cincinnati', 'Library of Congress (Highsmith)', 'C', [xt('X34-neon-drugs.png')], xko('X34-neon-drugs.png')],
  ['X35', 'bulbs-casino', 'Bulbs and neon, CASINO', 'mid-century · Las Vegas', 'Library of Congress (Highsmith)', 'B', [xt('X35-bulbs-casino.png')], xin('X35-bulbs-casino.png')],
  ['X36', 'neon-arizonan', 'Neon, the Arizonan Motel', '1951 · Tucson', 'Library of Congress (Highsmith)', 'B', [xt('X36-neon-arizonan.png')], xin('X36-neon-arizonan.png')],
  ['X40', 'postcard-diner', 'Linen postcard, a diner', '1930s–1940s · Chester, Pa.', 'Boston Public Library (Tichnor) via Commons', 'B', [xt('X40-postcard-diner.png')], xin('X40-postcard-diner.png')],
  ['X41', 'postcard-general-store', 'Linen postcard, a general store', '1930s–1940s · Rolling Hills, Calif.', 'Boston Public Library (Tichnor) via Commons', 'C', [xt('X41-postcard-general-store.png')], xko('X41-postcard-general-store.png')],
  ['X42', 'window-gas-shortage', 'Shop window, cut-paper letters: gas shortage', '1973 · Portland, Ore.', 'EPA DOCUMERICA via Commons', 'C', [xt('X42-window-gas-shortage.png')], xko('X42-window-gas-shortage.png')],
  ['X44', 'postcard-drive-in', 'Linen postcard, a drive-in theatre', '1940s · Middlesboro, Ky.', 'Boston Public Library (Tichnor) via Commons', 'C', [xt('X44-postcard-drive-in.png')], xko('X44-postcard-drive-in.png')],
  ['X50', 'trade-tokens', 'Trade tokens: good for 5c in trade', '1888–1897', 'Smithsonian National Postal Museum', 'A', TOKENS,
    chain(TOKENS, CH({ seed: 21, orient: 'long', cross: 1.18, allowOver: true, overlap: 0.02, rotJitter: 10, upright: false, per: { narch: { orient: 'long', cross: 1.12, overlap: 0.2, rotJitter: 10 } } }))],
  ['X45', 'crt-phosphor', 'Colour CRT screen, phosphor stripes', '1980s–1990s', 'Wikimedia Commons (CC0)', 'C', [xt('X45-crt-phosphor.png')], xko('X45-crt-phosphor.png')],
  ['X46', 'core-memory', 'Ferrite-core memory board', '1975', 'Wikimedia Commons', 'C', [xt('X46-core-memory.png')], xko('X46-core-memory.png')],
  ['X47', 'floppy-disk', 'Floppy disk, 3.5 inch', '1990s', 'Wikimedia Commons (CC0)', 'C', [xt('X47-floppy-disk.png')], xko('X47-floppy-disk.png')],
  ['X48', 'pressed-metal-storefront', 'Pressed-metal storefront', 'c. 1900–1909 · Cortez, Colo.', 'Library of Congress (Highsmith)', 'C', [xt('X48-pressed-metal-storefront.png')], xko('X48-pressed-metal-storefront.png')],
  ['X51', 'drive-in-tower', 'Drive-in theatre screen tower', '1940s–50s, photographed 1988', 'Library of Congress (Margolies)', 'C', [xt('X51-drive-in-tower.png')], xko('X51-drive-in-tower.png')],
  ['X52', 'maximum-purchase', 'Gas station poster: maximum purchase 10 gallons', '1973', 'EPA DOCUMERICA via Commons', 'C', [xt('X52-maximum-purchase.png')], xko('X52-maximum-purchase.png')],
  ['X54', 'trading-stamps', 'Store placard: we give trading stamps', '1972 · Texas', 'EPA DOCUMERICA via Commons', 'C', [xt('X54-trading-stamps.png')], xko('X54-trading-stamps.png')],
  ['X56', 'billboard-resort', 'Painted billboard, a Catskills resort', '1960s–70s, photographed 1977', 'Library of Congress (Margolies)', 'C', [xt('X56-billboard-resort.png')], xko('X56-billboard-resort.png')],
  ['X57', 'store-pictograms', 'Country store fascia painted with its goods', '1975 · California', 'EPA DOCUMERICA via Commons', 'C', [xt('X57-store-pictograms.png')], xko('X57-store-pictograms.png')],
  ['X58', 'auto-parts-wall', 'Painted wall sign, an auto-parts yard', '1973', 'EPA DOCUMERICA via Commons', 'B', [xt('X58-auto-parts-wall.png')], xin('X58-auto-parts-wall.png')],
  ['X60', 'ballroom-facade', 'Painted ballroom facade on Route 66', '1920s–50s, photographed 1977', 'Library of Congress (Margolies)', 'B', [xt('X60-ballroom-facade.png')], xin('X60-ballroom-facade.png')],
  ['X26', 'punch-card', 'Punched card, alone', '1960s', 'Wikimedia Commons', 'B', [PUNCH[0]],
    async g => { const im = await B.img(PUNCH[0]); g.save(); g.clip(B.markPath); const k = B.W * 1.5 / im.naturalWidth; g.translate(B.W / 2, B.H / 2); g.rotate(-90 * Math.PI / 180); g.drawImage(im, -im.naturalWidth * k / 2, -im.naturalHeight * k / 2, im.naturalWidth * k, im.naturalHeight * k); g.restore(); }],
];

// ---------- the board ----------
const S = (n, label, slug, title, era, archive, treatment, images, draw, extra = {}) => ({ n, label, slug, title, era, archive, treatment, images, draw, ...extra });
window.TIN = { terminal, LOG, grid, inkMark, url, drawDeepPaper };
window.STILLS = [
  S(1, '01', 'engraved-cards', 'Engraved shop cards (three tin-plate workers)', '1740s–1810s · London, Bath, Paris', 'British Museum via Commons, The Met, Cooper Hewitt', 'A', ENGRAVED,
    chain(ENGRAVED, CH({ seed: 9, cross: 0.98, overlap: 0.1, rotJitter: 3, per: {} }))),
  S(2, '02', 'wood-type', 'Wood-type playbill', '1843 · Hull', 'Library of Congress', 'C', [tex('playbill')], knock('playbill')),
  S(3, '03', 'trade-cards', 'Chromolithograph trade cards', '1870s–1890s', 'The Met, Commons, Cooper Hewitt', 'A', TRADE,
    chain(TRADE, CH({ seed: 7, per: { narch: { orient: 'short', cross: 0.92, overlap: 0.3, rotJitter: 1.5 } } }))),
  S(4, '04', 'tin-sign', 'Tin sign for tinned dairy ware', '1910s–1930s · Austria', 'Wikimedia Commons', 'C', [tex('seebach')], knock('seebach')),
  S(5, '05', 'biscuit-tin', 'Japanned biscuit tin', '1872–1899', 'The Met', 'B', [tex('olibet')], inside('olibet')),
  S(6, '06', 'can-label', 'Can label, Owl Brand tomatoes', '1882 · Delaware', 'Library of Congress', 'C', [tex('owl')], knock('owl')),
  S(7, '07', 'classifieds', 'Newspaper want ads', '1903 · Washington', 'Library of Congress', 'C', [tex('classifieds')], knock('classifieds')),
  S(8, '08', 'seed-catalogue', 'Seed catalogue cover: Seed Annual 1902', '1902 · St. Louis', 'USDA NAL via Commons', 'C', [tex('seedannual')], knock('seedannual')),
  // 09: a 1913 newspaper display ad printed in halftone (Wunderlich's pressed-metal interiors, Brisbane): the photograph
  // in the newspaper, its 45-degree screen real at 1:1 (10 px between dots), filling the frame with the mark cut out
  S(9, '09', 'halftone', 'Halftone newspaper ad: pressed-metal showrooms', '1913 · Brisbane', 'State Library of Queensland via Commons', 'C', [tex('htnews')], knock('htnews')),
  S(10, '10', 'poster-stamps', 'Advertising poster stamps', '1905–1921', 'Wikimedia Commons', 'A', STAMPS,
    chain(STAMPS, CH({ seed: 2, orient: 'auto', cross: 0.96, overlap: 0.06, rotJitter: 5, per: {} }))),
  S(11, '11', 'painted-wall', 'Painted wall sign', '1930s–1950s · Durham', 'Library of Congress', 'B', [tex('gem')], inside('gem')),
  S(12, '12', 'billboard', 'Billboard paste-up, torn', '1939 · Minneapolis', 'Library of Congress (FSA)', 'C', [tex('billboard')], knock('billboard')),
  S(13, '13', 'matchbooks', 'Matchbook covers', '1927–1962 · Allentown and elsewhere', 'Wikimedia Commons', 'A', MATCHES,
    chain(MATCHES, CH({ seed: 4, orient: 'long', cross: 0.96, overlap: 0.06, rotJitter: 3, per: {} }))),
  S(14, '14', 'neon', 'Neon motel sign at night', '1950s · Las Vegas', 'Library of Congress (Highsmith)', 'C', [tex('lucky')], knock('lucky')),
  S(15, '15', 'radio-dial', 'Radio tuning dial', '1940s', 'Wikimedia Commons', 'B', [tex('dial')], inside('dial')),
  S(16, '16', 'punch-cards', 'Punched cards', '1960s', 'Wikimedia Commons', 'B', PUNCH, punch),
  S(17, '17', 'television', 'Television test card on a CRT', '1964', 'Nationaal Archief via Commons', 'C', [tex('testcard')], knock('testcard')),
  S(18, '18', 'banner-pixels', 'Banner GIF: a flat colour in web-safe dither (made in code)', '1996', 'made in code (scripts/web1996.py)', 'D', [tex('pixels')], pixels),
  S(19, '19', 'search-results', 'Search results page (made in code)', '2004', 'made in code', 'B', [], g => serpInsideFramed(g, 2.2, 8)),
  S(20, '20', 'terminal', 'The terminal (made in code)', '2026', 'made in code', 'B', [], g => terminal(g)),
  S(21, 'A1', 'alt-match-safes', 'Advertising match safes', '1890s–1910s', 'Cooper Hewitt', 'A', SAFES,
    chain(SAFES, CH({ seed: 3, cross: 0.96, overlap: 0.05, rotJitter: 4, per: {} }))),
  // A2, the prologue: a salvaged pressed-steel ceiling panel (HABS) in raking daylight, so its ridges catch the light like
  // metal; it fills the frame and the mark is cut out of it as paper
  S(22, 'A2', 'alt-tin-ceiling', 'Pressed-tin ceiling panel', 'c. 1900', 'HABS, Library of Congress via Commons', 'C', [tex('ceiling')], knock('ceiling')),
  S(23, 'A3', 'alt-vick-seeds', 'Seed company chromolithograph, James Vick', '1870s · Rochester', 'Cleveland Museum of Art', 'B', [tex('vick')], inside('vick')),
  S(24, 'A4', 'alt-neon-donuts', 'Neon sign, donut shop', '1950s · Springfield, Ill.', 'Library of Congress (Highsmith)', 'C', [tex('sonrise')], knock('sonrise')),
  S(25, 'E', 'end-card', 'End card: mark, grid, tin.computer', '', 'made in code', '', [], endcard),
  // ---------- strobe extras (catalogue materials flashed between board stills; see docs/EDIT.md) ----------
  ...EXTRAS.map((x, k) => S(201 + k, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], { sheet: false, extra: true })),
];
})();
