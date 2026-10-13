"""Tile stills into one review sheet with their timestamps: python3 tools/stillsheet.py <dir> <out.png> [cols] [width]"""
import sys, glob, os
from PIL import Image, ImageDraw
d, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 2
w = int(sys.argv[4]) if len(sys.argv) > 4 else 960
files = sorted(glob.glob(os.path.join(d, 't*.png')))
ims = [Image.open(f).convert('RGB') for f in files]
h = int(w * 9 / 16)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w + (cols + 1) * 8, rows * (h + 26) + 8), 'white')
dr = ImageDraw.Draw(sheet)
for i, (f, im) in enumerate(zip(files, ims)):
    r, c = divmod(i, cols)
    x, y = 8 + c * (w + 8), 8 + r * (h + 26)
    sheet.paste(im.resize((w, h), Image.LANCZOS), (x, y + 18))
    dr.text((x, y + 2), os.path.basename(f)[1:-4].lstrip('0') + ' s', fill='black')
sheet.save(out)
print(out, sheet.size)
