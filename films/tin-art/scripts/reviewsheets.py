"""Review sheets for the critique: phone (360 px), mid (720 px, 3 across) and 1:1 detail crops.
  python3 scripts/reviewsheets.py out/board out/review/r1"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
d, pre = sys.argv[1], sys.argv[2]
stills = json.load(open(os.path.join(d, 'stills.json')))
fdir = os.path.join(os.path.dirname(__file__), '..', 'refs', 'brand', 'fonts')
font = ImageFont.truetype(os.path.join(fdir, 'FunktionalGrotesk-Medium.ttf'), 22)
ims = []
for s in stills:
    p = os.path.join(d, f"{s['label']}-{s['slug']}.png")
    ims.append((s, Image.open(p).convert('RGB')))
def sheet(tiles, cols, tw, th, name, label=True):
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new('RGB', (cols * (tw + 8) + 8, rows * (th + (30 if label else 0) + 8) + 8), (220, 216, 204))
    dr = ImageDraw.Draw(out)
    for i, (s, t) in enumerate(tiles):
        r, c = divmod(i, cols); x = 8 + c * (tw + 8); y = 8 + r * (th + (30 if label else 0) + 8)
        if label: dr.text((x, y + 2), f"{s['label']}  {s['slug']}", fill=(8, 8, 8), font=font)
        out.paste(t, (x, y + (30 if label else 0)))
    out.save(name); print(name, out.size)
# phone: 360 px
sheet([(s, im.resize((360, 360), Image.LANCZOS)) for s, im in ims], 5, 360, 360, pre + '-phone.png')
# mid: 640 px, 3 across, in chunks of 9
for k in range(0, len(ims), 9):
    sheet([(s, im.resize((640, 640), Image.LANCZOS)) for s, im in ims[k:k + 9]], 3, 640, 640, pre + f'-mid{k // 9 + 1}.png')
# 1:1 detail: crop around the T-bar/stem junction and the n arch (frame px at 2160)
boxes = [(330, 560, 730, 960), (1380, 520, 1780, 920)]
tiles = []
for s, im in ims:
    for b in boxes: tiles.append((s, im.crop(b)))
for k in range(0, len(tiles), 20):
    sheet(tiles[k:k + 20], 4, 400, 400, pre + f'-detail{k // 20 + 1}.png')
