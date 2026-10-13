"""Review sheets for a film draft: python3 scripts/filmsheets.py <video.mp4> <outdir> [label]
  shots.png   one frame from the middle of every shot, in order, with its position, time and shot (the edit at a glance)
  shots-360.png  the same at 360 px (legibility on a phone)
  strip-*.png 12 consecutive frames around key moments (open, 8ths, 16ths, the stop, the drop, the drain, the loop seam)
  contact.png / phone.png from tools/sheets.sh (2 fps and 1 fps)
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
v, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
FF = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'bin', 'ffmpeg')
cuts = json.load(open('out/cuts.json'))
font = ImageFont.truetype('refs/brand/fonts/FunktionalGrotesk-Medium.ttf', 18)
tmp = os.path.join(out, '_frames'); os.makedirs(tmp, exist_ok=True)
subprocess.run([FF, '-y', '-loglevel', 'error', '-i', v, '-vsync', '0', '-vf', 'scale=1080:1080', os.path.join(tmp, 'f%04d.png')], check=True)
frames = sorted(os.listdir(tmp))
N = len(frames)
fr = lambda i: Image.open(os.path.join(tmp, frames[max(0, min(N - 1, i))])).convert('RGB')
def sheet(items, size, cols, name, label=True):
    rows = (len(items) + cols - 1) // cols
    hh = 26 if label else 0
    s = Image.new('RGB', (cols * (size + 6) + 6, rows * (size + hh + 6) + 6), (225, 221, 210)); d = ImageDraw.Draw(s)
    for k, (lab, im) in enumerate(items):
        x, y = 6 + (k % cols) * (size + 6), 6 + (k // cols) * (size + hh + 6)
        if label: d.text((x + 2, y + 3), lab, fill=(8, 8, 8), font=font)
        s.paste(im.resize((size, size), Image.LANCZOS), (x, y + hh))
    s.save(name); print(name, s.size)
items = []
for c in cuts:
    mid = c['f'] + c['holdF'] // 2
    items.append((f"{c['p']}  {c['t']:.2f}s  {c['shot']}", fr(mid)))
sheet(items, 300, 9, os.path.join(out, 'shots.png'))
sheet([(c[0].split('  ')[-1], im) for c, im in zip(items, [i for _, i in items])], 200, 9, os.path.join(out, 'shots-360.png'))
def strip(f0, name, n=12):
    sheet([(f"f{i} {i / 24:.3f}s", fr(i)) for i in range(f0, f0 + n)], 260, 6, os.path.join(out, name))
for t, nm in [(0, 'strip-open'), (7.80, 'strip-8ths'), (12.10, 'strip-16ths'), (13.60, 'strip-stop'), (15.60, 'strip-drop'), (17.60, 'strip-drain')]:
    strip(int(round(t * 24)), nm + '.png')
# the loop seam: the last 6 frames, then the first 6
sheet([(f"f{i}", fr(i)) for i in range(N - 6, N)] + [(f"f{i} (loop)", fr(i)) for i in range(0, 6)], 260, 6, os.path.join(out, 'strip-loop.png'))
subprocess.run(['bash', 'tools/sheets.sh', v, out], check=True)
for f in frames: os.remove(os.path.join(tmp, f))
os.rmdir(tmp)
