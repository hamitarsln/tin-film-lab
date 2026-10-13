"""Predict flashes for a cut list from the materials' measured cell luminance (out/materials.json, scripts/strobeplan.mjs)
before rendering anything. Same rule as scripts/flashcheck.py: a change is 25% of the frame moving by 0.1 relative
luminance one way (the darker side below 0.8); a flash is a pair of opposing changes; at most 3 in any second.
  python3 scripts/planflash.py            reads out/cuts.json (scripts/editdoc.mjs) and prints changes and flashes
Shots that are not stills (TERM, DRAIN, END*) are treated as their nearest still (20 for the terminal, E for the end).
"""
import json, sys
import numpy as np
mats = {m['label']: m for m in json.load(open('out/materials.json'))}
cuts = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'out/cuts.json'))
alias = {'TERM': '20', 'DRAIN': 'E', 'END1': 'E', 'END2': 'E', 'END3': 'E'}
frames = []
for c in cuts:
    m = mats[alias.get(c['shot'], c['shot'])]
    frames += [np.array(m['cells'])] * c['holdF']
changes = []
for i in range(1, len(frames)):
    d = frames[i] - frames[i - 1]; dark = np.minimum(frames[i], frames[i - 1]) < 0.8
    up, down = ((d >= 0.1) & dark).mean(), ((d <= -0.1) & dark).mean()
    if up >= 0.25: changes.append((i, 1))
    elif down >= 0.25: changes.append((i, -1))
worst, where = 0, 0
for s in range(len(frames)):
    merged = []
    for c in [c for c in changes if s <= c[0] < s + 24]:
        if not merged or merged[-1][1] != c[1]: merged.append(c)
    if len(merged) // 2 > worst: worst, where = len(merged) // 2, s
print(f'{len(frames)} frames, {len(changes)} changes, worst window {worst} flashes at {where / 24:.2f}s ({"PASS" if worst <= 3 else "FAIL"})')
t = 0
row = []
for c in cuts:
    m = mats[alias.get(c['shot'], c['shot'])]
    row.append(f"{c['p']} {c['shot']}({m['Y']:.2f})")
print('  '.join(row))
