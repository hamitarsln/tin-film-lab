"""Music-sync sheet for a draft: python3 scripts/syncsheet.py <video.mp4> <out.png>
Top: one thumbnail per shot at its cut time. Below: the cut's measured onset, bass and treble envelopes (music-cut/
cue.json) with a line at every cut, bar and beat numbers, and the cutting rate (cuts per second) as a step plot."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
v, out = sys.argv[1], sys.argv[2]
FF = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'bin', 'ffmpeg')
cue = json.load(open('music-cut/cue.json')); cuts = json.load(open('out/cuts.json'))
L = cue['length']; env = cue['envelope']; fps = env['fps']
Wd, pad = 3600, 60
X = lambda t: pad + (Wd - 2 * pad) * t / L
font = ImageFont.truetype('refs/brand/fonts/FunktionalGrotesk-Medium.ttf', 20)
small = ImageFont.truetype('refs/brand/fonts/FunktionalGrotesk-Book.ttf', 15)
lanes = [('onset', (60, 60, 60)), ('low', (28, 52, 92)), ('high', (220, 96, 60))]
lh, top = 150, 330
H = top + len(lanes) * (lh + 20) + 220
im = Image.new('RGB', (Wd, H), (246, 243, 235)); d = ImageDraw.Draw(im)
# thumbnails: frame at each cut, staggered in 3 rows so neighbours do not overlap
tmp = '/tmp/syncthumbs'; os.makedirs(tmp, exist_ok=True)
for i, c in enumerate(cuts):
    f = os.path.join(tmp, f'{i:03d}.png')
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', f"{(c['f'] + min(2, c['holdF'] // 2)) / 24:.4f}", '-i', v, '-frames:v', '1', '-vf', 'scale=96:96', f], check=True)
    th = Image.open(f).convert('RGB'); row = i % 3
    x = int(X(c['t'])) - 48; y = 20 + row * 100
    im.paste(th, (max(0, min(Wd - 96, x)), y)); d.line([(X(c['t']), y + 96), (X(c['t']), top)], fill=(170, 170, 170), width=1)
for k, (name, col) in enumerate(lanes):
    y0 = top + k * (lh + 20)
    vals = np.array(env[name]); n = len(vals)
    d.rectangle([pad, y0, Wd - pad, y0 + lh], outline=(200, 196, 186))
    pts = [(X(i / fps), y0 + lh - vals[i] * lh) for i in range(0, n)]
    d.line(pts, fill=col, width=2)
    d.text((8, y0 + 4), name, fill=col, font=font)
# bars and beats
for b in range(int(L / cue['bar']) + 2):
    tb = b * cue['bar']
    if tb > L: break
    d.line([(X(tb), top - 10), (X(tb), top + len(lanes) * (lh + 20))], fill=(120, 120, 120), width=2)
    d.text((X(tb) + 4, top - 30), f"bar {b + 1}", fill=(40, 40, 40), font=font)
    for q in range(1, 4):
        tq = tb + q * cue['beat']
        if tq < L: d.line([(X(tq), top), (X(tq), top + len(lanes) * (lh + 20))], fill=(215, 211, 200), width=1)
# cuts
for c in cuts:
    d.line([(X(c['t']), top), (X(c['t']), top + len(lanes) * (lh + 20))], fill=(214, 40, 90), width=2)
# cutting rate
y0 = top + len(lanes) * (lh + 20) + 20
d.text((8, y0), 'cuts/s', fill=(214, 40, 90), font=font)
mx = 9.0
for i, c in enumerate(cuts):
    rate = 24 / max(1, c['holdF'])
    x0, x1 = X(c['t']), X(c['t'] + c['holdF'] / 24)
    d.rectangle([x0, y0 + 160 - rate / mx * 150, x1, y0 + 160], fill=(214, 40, 90))
d.text((pad, y0 + 170), 'red lines: cuts; grey: bars (dark) and beats (light); envelopes measured from the music (music-cut/cue.json)', fill=(60, 60, 60), font=small)
im.save(out); print(out, im.size)
