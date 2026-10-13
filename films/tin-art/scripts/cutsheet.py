"""Check cutouts: each on paper and on charcoal. python3 scripts/cutsheet.py out.jpg files..."""
import sys
from PIL import Image, ImageDraw
out = sys.argv[1]; fs = sys.argv[2:]
tiles = []
for f in fs:
    im = Image.open(f).convert('RGBA'); im.thumbnail((290, 290))
    for bg in [(245, 241, 230, 255), (40, 40, 40, 255)]:
        t = Image.new('RGBA', (300, 316), bg); t.alpha_composite(im, ((300 - im.width) // 2, 16 + (300 - im.height) // 2))
        ImageDraw.Draw(t).text((4, 2), f.split('/')[-1][:40], fill=(255, 0, 0, 255)); tiles.append(t)
cols = 8; rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * 304, rows * 320), (255, 255, 255, 255))
for i, t in enumerate(tiles):
    r, c = divmod(i, cols); sheet.paste(t, (c * 304, r * 320))
sheet.convert('RGB').save(out, quality=88); print(out, sheet.size)
