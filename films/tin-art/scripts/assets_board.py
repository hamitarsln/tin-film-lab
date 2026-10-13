"""Build materials/assets.json and materials/ASSETS.md from the research files and the board usage map.

  python3 scripts/assets.py

Inputs: materials/candidates/{commons,loc,museums,smithsonian}.json (every image downloaded, with rights as stated),
scripts/usage.json (which ids each still uses), out/board/stills.json (titles and eras), materials/cut/ (prepared
files). Every downloaded image is recorded; status says whether it is on the board, an alternate, or a candidate.
"""
import glob, json, os, re

ROOT = os.path.join(os.path.dirname(__file__), '..')
os.chdir(ROOT)

SOURCES = ['commons', 'loc', 'museums', 'smithsonian']
ARCHIVE_NAME = {'commons': 'Wikimedia Commons', 'loc': 'Library of Congress', 'met': 'The Met', 'cma': 'Cleveland Museum of Art',
                'si': 'Smithsonian'}
STEP_ORDER = ['engraved-trade', 'wood-type', 'trade-cards', 'pressed-tin', 'tins', 'labels', 'classifieds', 'seed-catalogue',
              'mail-order', 'halftone', 'poster-stamps', 'painted-wall', 'billboard', 'matchbooks', 'neon', 'radio-dial',
              'punch-cards', 'television']
# Prepared textures per still (objects are found by id in materials/cut/).
TEXTURE = {'02': 't-playbill.png', '04': 't-seebach.png', '05': 't-olibet.png', '06': 't-owl.png', '07': 't-classifieds.png',
           '08': 't-seedannual.png', '09': 't-htcode.png', '11': 't-gem.png', '12': 't-billboard.png', '14': 't-lucky.png',
           '15': 't-dial.png', '16': ['proto/punch-blue.png', 'proto/punch-cream.png'], '17': 't-testcard.png',
           '18': 't-pixels.png', 'A2': 't-ceiling.png', 'A3': 't-vick.png', 'A4': 't-sonrise.png'}
# Commons originals fetched again at full size after the agent was throttled to reduced copies.
ORIGINALS = {'commons:171216726': 'materials/raw/radio-dial__commons-171216726-orig.jpg',
             'commons:74085178': 'materials/raw/television__commons-74085178-orig.jpg',
             'commons:73145446': 'materials/raw/seed-catalogue__commons-73145446-orig.jpg',
             'commons:121792060': 'materials/raw/wood-type__commons-121792060-orig.jpg'}
# Matchbook cut names that do not carry the id.
MATCH_NAMES = {'77445585': 'superior', '86962818': 'parkvalley', '77445584': 'stahl', '52616081': 'whitespot',
               '59939488': 'motorramp', '65169039': 'dutchgrille', '57248427': 'cossie', '38558372': 'schaber',
               '52098438': 'milkbar', '112564666': 'cloverclub', '87858318': 'match-koch', '125027862': 'match-cormaine'}
FLAGS = {
    'commons:92295820': 'Stamp for Lech-Elektrizitätswerke (LEW). Lechwerke AG still trades as LEW; the 1910s Hohlwein design is not its current logo. Small, one of 16 stamps. Human check advised.',
    'commons:60856928': 'Vienna International Fair stamp, c. 1921, just past the 1905–1920 window.',
    'commons:111274882': 'Cover reads "Golden Guernsey", a historic milk grade mark; not a famous current brand.',
    'loc:2023697166': 'The old Lucky Motel, Las Vegas. Local, historic sign; not a famous current mark.',
    'commons:50890851': 'NOT USED: the El Cortez Hotel & Casino still operates, so its name would be a current business as the subject.',
    'loc:2017809841': 'A torn fragment "OL" of an Oldsmobile poster shows at the top edge; Oldsmobile is defunct and the fragment is not identifiable.',
    'commons:181803355': 'Fabrik Seebach, St. Ruprecht bei Villach: historic Austrian tinware factory; lettering sits above the mark.',
}


def load_candidates():
    out = []
    for src in SOURCES:
        for c in json.load(open(f'materials/candidates/{src}.json'))['candidates']:
            c = dict(c); c['found_by'] = src; out.append(c)
    return out


def token(i):
    a, b = i.split(':', 1)
    b = b.split(' ')[0]
    return b


MANIFEST = json.load(open('materials/cut/MANIFEST.json'))


def cut_files(cid, still):
    hits = sorted(f'materials/cut/{k}' for k, v in MANIFEST.items() if cid in v['ids'] and k.startswith(still + '-'))
    if hits:
        return hits
    t = token(cid)
    if still in TEXTURE:
        v = TEXTURE[still]; v = v if isinstance(v, list) else [v]
        return [f'materials/cut/{x}' for x in v]
    hits = []
    pat = [t, t.replace('CHSDM-', '')]
    if t in MATCH_NAMES:
        pat.append(MATCH_NAMES[t])
    for f in sorted(glob.glob('materials/cut/**/*.png', recursive=True)):
        name = os.path.basename(f)
        if name.startswith('t-'):
            continue
        if any(p and (f'-{p}' in name or f'_{p}' in name or name.startswith(p + '-') or name.startswith(p + '.')
                      or name.startswith('flat-' + p) or name.startswith('full-' + p) or f'ps-{p}' in name) for p in pat):
            hits.append(f)
    return hits


def main():
    cands = load_candidates()
    usage = json.load(open('scripts/usage.json'))
    stills = {s['label']: s for s in json.load(open('out/board/stills.json'))}
    used = {}
    for label, v in usage.items():
        for cid in v['ids']:
            used.setdefault(cid, []).append(label)
    records = []
    seen = set()
    for c in cands:
        if c['id'] in seen:
            continue
        seen.add(c['id'])
        labels = used.get(c['id'], [])
        status = 'board' if any(not l.startswith('A') for l in labels) else 'alternate' if labels else 'candidate'
        rec = {
            'id': c['id'], 'step': c['step'], 'status': status, 'stills': labels,
            'file': c['file'], 'file_full_size': ORIGINALS.get(c['id']),
            'title': c['title'], 'date': c['date'],
            'archive': ARCHIVE_NAME.get(c['id'].split(':')[0], c.get('archive')), 'archive_detail': c.get('archive'),
            'object_url': c['object_url'], 'image_url': c['image_url'],
            'rights_field': c['rights_field'], 'rights_as_stated': c['rights_as_stated'],
            'width': c.get('width'), 'height': c.get('height'),
            'what_it_shows': c.get('what_it_shows'), 'people_or_logos': c.get('people_or_logos'),
            'use': '; '.join(f"{l}: {usage[l]['use']}" for l in labels) or None,
            'cut_files': sorted({f for l in labels for f in cut_files(c['id'], l)}),
            'flag': FLAGS.get(c['id']),
            'found_by': c['found_by'], 'research_notes': c.get('notes'),
        }
        records.append(rec)
    made = [
        {'id': 'code:paper', 'status': 'board', 'stills': 'all', 'title': "Tin's paper #F5F1E6 with fine grain and fibres",
         'archive': 'made in code', 'file': 'src/index.html', 'use': 'Ground of every still; seeded noise (Motion.rng), ~1.7 levels of grain.'},
        {'id': 'code:halftone-screen', 'status': 'board', 'stills': ['09'], 'title': 'Halftone screen (45°, 22 px cells)',
         'archive': 'made in code from si:CHSDM-94743AECF1492-000001', 'file': 'materials/cut/09-halftone.png',
         'use': 'The 1905 print is descreened and re-screened in code so the dots hold at 2160 px. Command in scripts/README.md.'},
        {'id': 'code:web-pixels', 'status': 'board', 'stills': ['18'], 'title': 'Web-safe palette pixels (24 px grid)',
         'archive': 'made in code from commons:155898625', 'file': 'materials/cut/18-banner-pixels.png',
         'use': 'Floyd-Steinberg dither to the 216-colour web-safe palette; the mark is rasterised to the same grid.'},
        {'id': 'code:search-results', 'status': 'board', 'stills': ['19'], 'title': 'Search results page, c. 2004 (generic, example.com domains)',
         'archive': 'made in code', 'file': 'src/stills.js',
         'use': "Results set in Arial at screen colours of the time, inside the mark, framed by Tin's 1 px ink rule. No real brand or site."},
        {'id': 'code:terminal', 'status': 'board', 'stills': ['20'], 'title': "The terminal: an agent's marketing log on terminal blue #90D7E4",
         'archive': 'made in code', 'file': 'src/stills.js', 'use': 'SF Mono (refs/brand/fonts) at 0.84 ink; the reserved colour.'},
        {'id': 'code:end-card', 'status': 'board', 'stills': ['E'], 'title': 'End card: mark, hairline grid, tin.computer, lime cursor',
         'archive': 'made in code', 'file': 'src/stills.js', 'use': 'Funktional Grotesk Medium; lime-cta block cursor; grid aligned to cap and baseline.'},
    ]
    json.dump({'generated_by': 'scripts/assets.py', 'rule': 'Public domain or CC0 only; rights recorded verbatim from the archive field named.',
               'images': records, 'made_in_code': made}, open('materials/assets.json', 'w'), indent=1, ensure_ascii=False)

    # ---------- ASSETS.md ----------
    by_id = {r['id']: r for r in records}
    L = []
    L.append('# Assets\n')
    L.append('Every image downloaded for the film, with its rights as the archive states them. Generated by `scripts/assets.py` from')
    L.append('the research files in `materials/candidates/`; `materials/assets.json` has every field (image URL, size, notes, cut files).')
    L.append('Rule: public domain or CC0 only. Raw files in `materials/raw/` are never edited; prepared files are in `materials/cut/`.\n')
    L.append(f"{len(records)} images: {sum(r['status'] == 'board' for r in records)} on the board, "
             f"{sum(r['status'] == 'alternate' for r in records)} in the alternates, {sum(r['status'] == 'candidate' for r in records)} considered and not used.\n")
    L.append('## On the board\n')
    for label in [k for k in usage if not k.startswith('A')] + [k for k in usage if k.startswith('A')]:
        if label == 'A1':
            L.append('\n## Alternates\n')
        s = stills.get(label, {})
        L.append(f"### {label} · {s.get('title', usage[label]['slug'])} ({s.get('era', '')})")
        L.append(f"Use: {usage[label]['use']}\n")
        L.append('| id | title | date | archive | file (raw) | image | rights (field: as stated) |')
        L.append('|---|---|---|---|---|---|---|')
        for cid in usage[label]['ids']:
            r = by_id[cid]
            title = r['title'].replace('|', '/')[:90]
            raw = os.path.basename(r['file_full_size'] or r['file'])
            L.append(f"| [{cid}]({r['object_url']}) | {title} | {r['date']} | {r['archive']} | `{raw}` | [image]({r['image_url']}) | {r['rights_field']}: {r['rights_as_stated'][:120].replace('|', '/')} |")
        cuts = sorted({os.path.basename(f) for cid in usage[label]['ids'] for f in by_id[cid]['cut_files']})
        if cuts:
            L.append(f"\nPrepared: `{cuts[0]}`" + (f" … `{cuts[-1]}` ({len(cuts)} files)" if len(cuts) > 1 else ''))
        flags = [by_id[c]['flag'] for c in usage[label]['ids'] if by_id[c].get('flag')]
        for f in flags:
            L.append(f'\nFlag: {f}')
        L.append('')
    L.append('## Made in code\n')
    L.append('| id | what | from | use |')
    L.append('|---|---|---|---|')
    for m in made:
        L.append(f"| {m['id']} | {m['title']} | {m['archive']} | {m['use']} |")
    L.append('\n## Every candidate, by arc step\n')
    L.append('Two or more real candidates were found for every step except halftone (one real print; the dots are re-screened in')
    L.append('code, which the materials skill allows). Status: **board**, *alternate* or candidate.\n')
    steps = sorted({r['step'] for r in records}, key=lambda s: STEP_ORDER.index(s) if s in STEP_ORDER else 99)
    for st in steps:
        rs = [r for r in records if r['step'] == st]
        L.append(f'### {st} ({len(rs)})\n')
        L.append('| id | title | date | px | file (raw) | image | rights | status / use |')
        L.append('|---|---|---|---|---|---|---|---|')
        for r in sorted(rs, key=lambda r: ({'board': 0, 'alternate': 1}.get(r['status'], 2), r['id'])):
            st_ = {'board': f"**board {','.join(r['stills'])}**", 'alternate': f"*alternate {','.join(r['stills'])}*"}.get(r['status'], 'candidate, not used')
            px = f"{r['width']}×{r['height']}" if r['width'] else ''
            raw = os.path.basename(r['file_full_size'] or r['file'])
            L.append(f"| [{r['id']}]({r['object_url']}) | {r['title'].replace('|', '/')[:80]} | {str(r['date'])[:28]} | {px} | `{raw}` | [image]({r['image_url']}) | {r['rights_as_stated'][:60].replace('|', '/')} | {st_} |")
        L.append('')
    L.append('## Searched and skipped on rights (not downloaded)\n')
    L.append('- Halftone, second source (2026-10-05, after round 3): Library of Congress 2003688929 (1890 Hobbs Glass Co. advertising page)')
    L.append('  and 2003688927 (1918 Glow Thrift Lamps advertisement) are halftone prints but say "Rights status not evaluated". Skipped.')
    L.append('  Cleveland 1995.199.3 (Camera Work no. 3, CC0) is photographed as a closed bound volume, so no halftone is visible. Not usable.')
    L.append('')
    L.append('## Rejected on rights or content (not downloaded, from the research notes)\n')
    for src in SOURCES:
        g = json.load(open(f'materials/candidates/{src}.json')).get('gaps', [])
        for x in g:
            L.append(f'- ({src}) {x}')
    open('materials/ASSETS.md', 'w').write('\n'.join(L) + '\n')
    print('wrote materials/assets.json and materials/ASSETS.md:', len(records), 'images')
    nocut = [(r['id'], r['stills']) for r in records if r['status'] != 'candidate' and not r['cut_files']]
    print('board/alternate images with no cut file found:', nocut)


if __name__ == '__main__':
    main()
