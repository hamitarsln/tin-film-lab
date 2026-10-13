import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
src, out, fps, step, cols, tw = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
start = int(sys.argv[7]) if len(sys.argv) > 7 else 1
end = int(sys.argv[8]) if len(sys.argv) > 8 else 10**9
files = sorted(glob.glob(os.path.join(src, 'f*.jpg')))
sel = [f for f in files if start <= int(os.path.basename(f)[1:5]) <= end][::step]
im0 = Image.open(sel[0]); th = int(tw * im0.height / im0.width)
rows = (len(sel) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 4) + 4, rows * (th + 22) + 4), 'white')
d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
except: font = ImageFont.load_default()
for i, f in enumerate(sel):
    r, c = divmod(i, cols); x, y = 4 + c * (tw + 4), 4 + r * (th + 22)
    n = int(os.path.basename(f)[1:5])
    sheet.paste(Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS), (x, y + 18))
    d.text((x, y + 1), f'#{n}  {(n-1)/fps:.3f}s', fill='black', font=font)
sheet.save(out); print(out, sheet.size, len(sel))
