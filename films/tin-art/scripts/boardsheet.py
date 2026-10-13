"""Numbered contact sheet of the board: python3 scripts/boardsheet.py out/board  ->  out/board/BOARD.png (5 across)."""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
d = sys.argv[1]
stills = [s for s in json.load(open(os.path.join(d, 'stills.json'))) if s.get('sheet', True)]
cols, tw, gap, head = 5, 600, 24, 64
rows = (len(stills) + cols - 1) // cols
font_dir = os.path.join(os.path.dirname(__file__), '..', 'refs', 'brand', 'fonts')
fnum = ImageFont.truetype(os.path.join(font_dir, 'FunktionalGrotesk-Medium.ttf'), 30)
ftxt = ImageFont.truetype(os.path.join(font_dir, 'FunktionalGrotesk-Book.ttf'), 21)
sheet = Image.new('RGB', (cols * tw + (cols + 1) * gap, rows * (tw + head) + (rows + 1) * gap - gap // 2), (233, 228, 214))
dr = ImageDraw.Draw(sheet)
for i, s in enumerate(stills):
    r, c = divmod(i, cols)
    x, y = gap + c * (tw + gap), gap + r * (tw + head + gap)
    p = os.path.join(d, f"{s['label']}-{s['slug']}.png")
    if os.path.exists(p):
        sheet.paste(Image.open(p).convert('RGB').resize((tw, tw), Image.LANCZOS), (x, y + head))
    dr.text((x, y + 8), s['label'], fill=(8, 8, 8), font=fnum)
    dr.text((x + 64, y + 4), s['title'][:52], fill=(8, 8, 8), font=ftxt)
    dr.text((x + 64, y + 32), s.get('era', '')[:52], fill=(120, 113, 95), font=ftxt)
sheet.save(os.path.join(d, 'BOARD.png'))
print(os.path.join(d, 'BOARD.png'), sheet.size)
