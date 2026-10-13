"""Give every prepared file the materials-skill name, <nn>-<slug>[-kk].png, and record where it came from.

  python3 scripts/finalize_cuts.py

Copies the files the board uses from their working names (t-*.png, proto/, match/, stamps/, engraved/) to
materials/cut/<label>-<slug>.png (textures) or materials/cut/<label>-<slug>-<kk>.png (object sets, in board order),
writes materials/cut/MANIFEST.json (new name -> working file, archive ids, raw files), then moves the working files to
materials/cut/work/. Object order matches the order the board lays them along the strokes.
"""
import json, os, shutil, glob

os.chdir(os.path.join(os.path.dirname(__file__), '..'))
C = 'materials/cut'

TEXTURES = {  # label-slug: (working file, ids)
    '02-wood-type': ('t-playbill.png', ['loc:2006677674']),
    '04-tin-sign': ('t-seebach.png', ['commons:181803355']),
    '05-biscuit-tin': ('t-olibet.png', ['met:910015']),
    '06-can-label': ('t-owl.png', ['loc:2022671704']),
    '07-classifieds': ('t-classifieds.png', ['loc:sn83045462-1903-09-12-p12']),
    '08-seed-catalogue': ('t-seedannual.png', ['commons:73145446']),
    '09-halftone': ('t-htcode.png', ['si:CHSDM-94743AECF1492-000001']),
    '11-painted-wall': ('t-gem.png', ['loc:2017880597']),
    '12-billboard': ('t-billboard.png', ['loc:2017809841']),
    '14-neon': ('t-lucky.png', ['loc:2023697166']),
    '15-radio-dial': ('t-dial.png', ['commons:171216726']),
    '17-television': ('t-testcard.png', ['commons:74085178']),
    '18-banner-pixels': ('t-pixels.png', ['commons:155898625']),
    'A2-alt-tin-ceiling': ('t-ceiling.png', ['commons:34525290']),
    'A3-alt-vick-seeds': ('t-vick.png', ['cma:1944.14']),
    'A4-alt-neon-donuts': ('t-sonrise.png', ['loc:2020721526']),
}
MATCH_IDS = {'superior': '77445585', 'parkvalley': '86962818', 'stahl': '77445584', 'whitespot': '52616081', 'motorramp': '59939488',
             'dutchgrille': '65169039', 'cossie': '57248427', 'schaber': '38558372', 'milkbar': '52098438', 'cloverclub': '112564666',
             'koch': '87858318', 'cormaine': '125027862'}


def tid(name):  # 'met-400581' -> 'met:400581'; 'si-CHSDM-CHD4931' -> 'si:CHSDM-CHD4931'
    a, b = name.split('-', 1)
    return f'{a}:{b}'


SETS = {
    '01-engraved-cards': [(f'engraved/engraved-trade__{n}.png', tid(n)) for n in [
        'commons-90033412', 'met-849927', 'commons-90221414', 'met-696865', 'commons-90034988', 'met-817306',
        'si-CHSDM-7DE878AC398F2-000001', 'si-CHSDM-B26CF2887A5D2-000001', 'si-CHSDM-4277FC2EF07D2-000001']],
    '03-trade-cards': [(f'proto/trade-cards__{n}.png', tid(n)) for n in [
        'met-400581', 'commons-174017081', 'met-819489', 'met-400534', 'commons-173949183', 'met-813040', 'met-400555', 'si-CHSDM-CHD4931',
        'met-819500', 'met-400593', 'commons-161317823', 'met-819487', 'met-400562', 'commons-174065314', 'met-821258', 'met-400599',
        'commons-173964931', 'met-816464', 'met-400573', 'si-CHSDM-CHD4945', 'commons-174293573', 'met-821194']],
    '10-poster-stamps': [(f'stamps/{n}.png', 'commons:' + n[3:].split('-')[0].rstrip('ab')) for n in [
        'ps-92295820', 'ps-103168123', 'ps-52773006-1', 'ps-60856928a', 'ps-70009921', 'ps-92261877', 'ps-52773006-2', 'ps-86460943',
        'ps-60856904a', 'ps-92262365', 'ps-52773006-6', 'ps-85658762', 'ps-52773006-4', 'ps-60856904b', 'ps-52773006-3', 'ps-52773006-5']],
    '13-matchbooks': [(f'match/{n}.png', 'commons:' + (n.split('-')[1] if n.startswith('flat-') else MATCH_IDS[n.replace('full-', '').split('-')[0]])) for n in [
        'superior-1', 'flat-111274882', 'parkvalley-1', 'stahl-1', 'full-whitespot', 'motorramp-1', 'flat-110403855', 'dutchgrille-a',
        'cossie-1', 'full-schaber', 'parkvalley-2', 'flat-113230970', 'stahl-2', 'full-milkbar', 'superior-2', 'motorramp-2', 'flat-104694264',
        'dutchgrille-b', 'full-cloverclub']] + [(f'proto/{n}.png', 'commons:' + MATCH_IDS[n.split('-')[1]]) for n in ['match-koch-1', 'match-cormaine', 'match-koch-2']],
    '16-punch-cards': [('proto/punch-blue.png', 'commons:8511203'), ('proto/punch-cream.png', 'commons:147324754')],
    'A1-alt-match-safes': [(f'proto/matchbooks__si-CHSDM-{n}.png', f'si:CHSDM-{n}') for n in [
        'A28BFEEEDCEA2-000001', 'CHA3710', 'CH1384', 'CHA71', 'CHA3765', 'CHA101', 'CHA3707', 'CHA32', 'CHA87', 'CHA3771', 'CHA3704', 'CHA92']],
}


def raw_for(cid):
    a, b = cid.split(':', 1)
    hits = [f for f in glob.glob('materials/raw/*') if f'__{a}-{b}.' in f or f'__{a}-{b}-orig.' in f]
    return sorted(hits)


def main():
    manifest = {}
    for name, (work, ids) in TEXTURES.items():
        src = os.path.join(C, work); dst = os.path.join(C, f'{name}.png')
        shutil.copyfile(src, dst)
        manifest[f'{name}.png'] = {'from': f'work/{work}', 'ids': ids, 'raw': [r for i in ids for r in raw_for(i)]}
    for name, items in SETS.items():
        for k, (work, cid) in enumerate(items, 1):
            src = os.path.join(C, work); dst = os.path.join(C, f'{name}-{k:02d}.png')
            shutil.copyfile(src, dst)
            manifest[f'{name}-{k:02d}.png'] = {'from': f'work/{work}', 'ids': [cid], 'raw': raw_for(cid)}
    missing_raw = [k for k, v in manifest.items() if not v['raw']]
    # move working files out of the way
    os.makedirs(os.path.join(C, 'work'), exist_ok=True)
    for p in sorted(glob.glob(os.path.join(C, 't-*.png'))) + [os.path.join(C, d) for d in ['proto', 'match', 'stamps', 'engraved']]:
        if os.path.exists(p):
            shutil.move(p, os.path.join(C, 'work', os.path.basename(p)))
    json.dump(manifest, open(os.path.join(C, 'MANIFEST.json'), 'w'), indent=1)
    print(len(manifest), 'files named; manifest at materials/cut/MANIFEST.json; missing raw:', missing_raw)
    # board order lists for stills.js
    lists = {name: [f'{name}-{k:02d}.png' for k in range(1, len(items) + 1)] for name, items in SETS.items()}
    json.dump(lists, open('/tmp/setlists.json', 'w'))


if __name__ == '__main__':
    main()
