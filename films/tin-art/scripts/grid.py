import sys
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]; cols = int(sys.argv[2]); tw = int(sys.argv[3]); files = sys.argv[4:]
ims = [Image.open(f).convert('RGB') for f in files]
th = int(tw * ims[0].height / ims[0].width)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 6) + 6, rows * (th + 24) + 6), 'white')
d = ImageDraw.Draw(sheet)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
for i, (f, im) in enumerate(zip(files, ims)):
    r, c = divmod(i, cols); x, y = 6 + c * (tw + 6), 6 + r * (th + 24)
    sheet.paste(im.resize((tw, int(tw * im.height / im.width)), Image.LANCZOS), (x, y + 20))
    d.text((x, y + 1), f.split('/')[-1], fill='black', font=font)
sheet.save(out); print(out, sheet.size)
