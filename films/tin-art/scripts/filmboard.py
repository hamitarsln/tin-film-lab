"""Sheets of the film's materials in film order: python3 scripts/filmboard.py <dir>  (dir from scripts/filmstills.mjs)
  board.png       board stills and the end card, 5 across at 600 px, numbered, with title and era
  extras.png      the strobe extras, 7 across at 300 px
  phone.png       every material at 360 px (legibility on a phone)
  detail-*.png    1:1 crops at 2160 px of the T junction and the n's arch, board stills only
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]
st = json.load(open(os.path.join(d, 'stills.json')))
fd = os.path.join(os.path.dirname(__file__), '..', 'refs', 'brand', 'fonts')
fnum = ImageFont.truetype(os.path.join(fd, 'FunktionalGrotesk-Medium.ttf'), 28)
ftxt = ImageFont.truetype(os.path.join(fd, 'FunktionalGrotesk-Book.ttf'), 20)
open_ = lambda s: Image.open(os.path.join(d, s['file'])).convert('RGB')
board = [s for s in st if not s['extra']]
extras = [s for s in st if s['extra']]


def sheet(items, cols, tw, name, head=64, big=True):
    rows = (len(items) + cols - 1) // cols; gap = 20
    out = Image.new('RGB', (cols * tw + (cols + 1) * gap, rows * (tw + head) + (rows + 1) * gap), (233, 228, 214))
    dr = ImageDraw.Draw(out)
    for i, s in enumerate(items):
        r, c = divmod(i, cols); x, y = gap + c * (tw + gap), gap + r * (tw + head + gap)
        out.paste(open_(s).resize((tw, tw), Image.LANCZOS), (x, y + head))
        dr.text((x, y + 6), s['label'], fill=(8, 8, 8), font=fnum)
        dr.text((x + 70, y + 2), s['title'][:46 if big else 24], fill=(8, 8, 8), font=ftxt)
        dr.text((x + 70, y + 30), (s['era'] + (f"  ·  {s['treatment']}" if s['treatment'] else ''))[:46 if big else 24], fill=(120, 113, 95), font=ftxt)
    out.save(os.path.join(d, name)); print(os.path.join(d, name), out.size)


sheet(board, 5, 600, 'board.png')
sheet(extras, 7, 300, 'extras.png', big=False)
sheet(st, 8, 360, 'phone.png', head=40, big=False)
boxes = [(330, 560, 730, 960), (1380, 520, 1780, 920)]
tiles = []
for s in board:
    im = open_(s)
    for b in boxes:
        tiles.append((s, im.crop(b)))
per = 6
for k in range(0, len(tiles), per * 3):
    chunk = tiles[k:k + per * 3]
    rows = (len(chunk) + per - 1) // per
    out = Image.new('RGB', (per * 408 + 8, rows * 438 + 8), (233, 228, 214)); dr = ImageDraw.Draw(out)
    for i, (s, t) in enumerate(chunk):
        r, c = divmod(i, per); x, y = 8 + c * 408, 8 + r * 438
        dr.text((x, y + 4), s['label'], fill=(8, 8, 8), font=ftxt); out.paste(t, (x, y + 30))
    name = os.path.join(d, f'detail-{k // (per * 3) + 1}.png'); out.save(name); print(name, out.size)
