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
    """The film's catalogue. The board's usage (scripts/usage.json) is kept as history; the film's usage is
    scripts/usage-film.json (label -> archive ids), in the order the labels first appear in src/film.js (out/cuts.json)."""
    srcs = SOURCES + [x for x in ('film-matchbooks', 'round5', 'neon2', 'objects2', 'surfaces2', 'infoage', 'roadside') if os.path.exists(f'materials/candidates/{x}.json')]
    cands = []
    for src in srcs:
        for c in json.load(open(f'materials/candidates/{src}.json'))['candidates']:
            c = dict(c); c['found_by'] = src; cands.append(c)
    board_usage = json.load(open('scripts/usage.json'))
    film_usage = json.load(open('scripts/usage-film.json'))
    cuts = json.load(open('out/cuts.json'))
    order = []
    for c in cuts:
        if c['shot'] in film_usage and c['shot'] not in order:
            order.append(c['shot'])
    titles = {c['shot']: (c.get('title') or '', c.get('era') or '', c.get('treatment') or '', c.get('extra')) for c in cuts}
    in_film, in_board = {}, {}
    missing_labels = [c['shot'] for c in cuts if c.get('title') and c['shot'] not in film_usage]
    if missing_labels:
        raise SystemExit(f'shots with no usage record (scripts/usage-film.json): {missing_labels}')
    for label in order:
        for cid in film_usage[label]['ids']:
            in_film.setdefault(cid, []).append(label)
    for label, v in board_usage.items():
        for cid in v['ids']:
            in_board.setdefault(cid, []).append(label)
    records, seen = [], set()
    for c in cands:
        if c['id'] in seen:
            continue
        seen.add(c['id'])
        fl, bl = in_film.get(c['id'], []), in_board.get(c['id'], [])
        status = 'film' if fl else 'board only' if bl else 'candidate'
        cut = sorted(f'materials/cut/{k}' for k, v in MANIFEST.items() if c['id'] in v['ids'])
        if not cut:
            cut = sorted({f for l in bl for f in cut_files(c['id'], l)})
        rec = {
            'id': c['id'], 'step': c['step'], 'status': status, 'film_shots': fl, 'board_stills': bl,
            'file': c['file'], 'file_full_size': ORIGINALS.get(c['id']),
            'title': c['title'], 'date': c['date'],
            'archive': ARCHIVE_NAME.get(c['id'].split(':')[0], c.get('archive')), 'archive_detail': c.get('archive'),
            'object_url': c['object_url'], 'image_url': c['image_url'],
            'rights_field': c['rights_field'], 'rights_as_stated': c['rights_as_stated'],
            'width': c.get('width'), 'height': c.get('height'),
            'what_it_shows': c.get('what_it_shows'), 'people_or_logos': c.get('people_or_logos'),
            'use': '; '.join(f"{l}: {film_usage[l]['use']}" for l in fl) or None,
            'cut_files': cut, 'flag': FLAGS.get(c['id']),
            'found_by': c['found_by'], 'research_notes': c.get('notes'),
        }
        records.append(rec)
    made = json.load(open('scripts/made-in-code.json'))
    json.dump({'generated_by': 'scripts/assets.py', 'rule': 'Public domain or CC0 only; rights recorded verbatim from the archive field named.',
               'images': records, 'made_in_code': made}, open('materials/assets.json', 'w'), indent=1, ensure_ascii=False)
    by_id = {r['id']: r for r in records}
    missing = [(l, cid) for l in order for cid in film_usage[l]['ids'] if cid not in by_id]
    if missing:
        raise SystemExit(f'film uses ids with no catalogue record: {missing}')
    L = ['# Assets\n']
    L.append('Every image downloaded for the film and its board, with its rights as the archive states them. Generated by')
    L.append('`scripts/assets.py` from the research files in `materials/candidates/`, the film\'s usage (`scripts/usage-film.json`) and')
    L.append('`materials/cut/MANIFEST.json`; `materials/assets.json` has every field. Rule: public domain or CC0 only. Raw files in')
    L.append('`materials/raw/` are never edited; prepared files are in `materials/cut/`.\n')
    n = lambda st: sum(r['status'] == st for r in records)
    L.append(f"{len(records)} images: {n('film')} in the film, {n('board only')} used on the board only (cut by the review), {n('candidate')} considered and not used.\n")
    L.append('## In the film, in order of first appearance\n')
    L.append('Labels are those of `src/stills.js`: 02–20 board stills, A2 the prologue, X01–X36 strobe extras (see docs/EDIT.md).\n')
    for label in order:
        t = titles.get(label, ('', '', '', False))
        L.append(f"### {label} · {t[0]}{f' ({t[1]})' if t[1] else ''}{' · strobe extra' if t[3] else ''}")
        L.append(f"Use: {film_usage[label]['use']}\n")
        L.append('| id | title | date | archive | file (raw) | image | rights (field: as stated) |')
        L.append('|---|---|---|---|---|---|---|')
        for cid in film_usage[label]['ids']:
            r = by_id[cid]
            raw = os.path.basename(r['file_full_size'] or r['file'])
            L.append(f"| [{cid}]({r['object_url']}) | {r['title'].replace('|', '/')[:90]} | {r['date']} | {r['archive']} | `{raw}` | [image]({r['image_url']}) | {r['rights_field']}: {str(r['rights_as_stated'])[:120].replace('|', '/')} |")
        cutn = sorted({os.path.basename(f) for cid in film_usage[label]['ids'] for f in by_id[cid]['cut_files']})
        if cutn:
            L.append(f"\nPrepared: `{cutn[0]}`" + (f" … `{cutn[-1]}` ({len(cutn)} files)" if len(cutn) > 1 else ''))
        for cid in film_usage[label]['ids']:
            if by_id[cid].get('flag'):
                L.append(f"\nFlag: {by_id[cid]['flag']}")
        L.append('')
    L.append('## Made in code\n')
    L.append('| id | what | from | use |')
    L.append('|---|---|---|---|')
    for m in made:
        L.append(f"| {m['id']} | {m['title']} | {m['archive']} | {m['use']} |")
    L.append('\n## Excluded after the board\n')
    for x in EXCLUDED:
        L.append(f'- {x}')
    L.append('\n## Every candidate, by arc step\n')
    L.append('Status: **film** (with the shots that use it), board only, or candidate (not used).\n')
    steps = sorted({r['step'] for r in records}, key=lambda s: STEP_ORDER.index(s) if s in STEP_ORDER else 99)
    for st in steps:
        rs = [r for r in records if r['step'] == st]
        L.append(f'### {st} ({len(rs)})\n')
        L.append('| id | title | date | px | file (raw) | image | rights | status |')
        L.append('|---|---|---|---|---|---|---|---|')
        for r in sorted(rs, key=lambda r: ({'film': 0, 'board only': 1}.get(r['status'], 2), r['id'])):
            st_ = {'film': f"**film {','.join(r['film_shots'])}**", 'board only': f"board only ({','.join(r['board_stills'])})"}.get(r['status'], 'candidate, not used')
            px = f"{r['width']}×{r['height']}" if r['width'] else ''
            raw = os.path.basename(r['file_full_size'] or r['file'])
            L.append(f"| [{r['id']}]({r['object_url']}) | {r['title'].replace('|', '/')[:80]} | {str(r['date'])[:28]} | {px} | `{raw}` | [image]({r['image_url']}) | {str(r['rights_as_stated'])[:60].replace('|', '/')} | {st_} |")
        L.append('')
    L.append('## Searched and skipped (not downloaded)\n')
    L.append('- Halftone, second source (2026-10-05, after the board): Library of Congress 2003688929 (1890 Hobbs Glass Co. advertising page)')
    L.append('  and 2003688927 (1918 Glow Thrift Lamps advertisement) are halftone prints but say "Rights status not evaluated". Skipped.')
    L.append('  Cleveland 1995.199.3 (Camera Work no. 3, CC0) is photographed as a closed bound volume, so no halftone is visible. Not usable.')
    for src in srcs:
        for x in json.load(open(f'materials/candidates/{src}.json')).get('gaps', []):
            L.append(f'- ({src}) {x}')
    open('materials/ASSETS.md', 'w').write('\n'.join(L) + '\n')
    print('wrote materials/assets.json and materials/ASSETS.md:', len(records), 'images,', n('film'), 'in the film')
    nocut = [(r['id'], r['film_shots']) for r in records if r['status'] == 'film' and not r['cut_files']]
    print('film images with no prepared file found:', nocut)


EXCLUDED = [
    'commons:111274882 (Freeman\'s Dairy, "Golden Guernsey" cover): swapped out of 13 by the human review; replaced by commons:63785956.',
    'si:CHSDM-CHD4931 (Manhattan Watch Co. trade card): small drawn dock workers on the card (no people). Removed from 03.',
    'commons:87858318, Hotel Allen front (the Koch Bros back stays): tiny drawn pedestrians on the sidewalk. Removed from 13.',
    'commons:92295820 (LEW poster stamp): Lechwerke AG still trades as LEW. Removed from the stamps the film flashes (X23).',
    'Board stills 01 (engraved shop cards), 05 (biscuit tin), 10 (poster stamps as a still) and 17 (TV test card): cut by the human review.',
]


if __name__ == '__main__':
    main()
