"""Legibility of the mark at phone size: python3 scripts/legibility.py <still.png> ...
Downscales each 2160 still to 360 px, then compares a 4 px band just inside the mark's edge with a 4 px band just
outside it: the mean absolute luminance difference (0-255) along the edge, and the share of edge length where that
difference is under 12 levels (where the mark has no visible edge). Higher contrast and a lower weak share read faster."""
import re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
d = open('refs/brand/mark.svg').read(); path = re.search(r' d="([^"]+)"', d).group(1)
N = 360; S = 0.7741 * N / 608; MX = N / 2 - 350 * S; MY = N / 2 - 360.875 * S
mask = Image.new('L', (N, N), 0); dr = ImageDraw.Draw(mask)
for sub in [s for s in path.split('Z') if s.strip()]:
    nums = list(map(float, re.findall(r'[-\d.]+', sub)))
    dr.polygon([(MX + x * S, MY + y * S) for x, y in zip(nums[0::2], nums[1::2])], fill=255)
m = np.asarray(mask) > 127
inner = np.asarray(mask.filter(ImageFilter.MinFilter(9))) > 127
outer = np.asarray(mask.filter(ImageFilter.MaxFilter(9))) > 127
band_in, band_out = m & ~inner, outer & ~m
# pair each inside-band pixel with the nearest outside-band pixel across the edge via local means
for f in sys.argv[1:]:
    im = Image.open(f).convert('L').resize((N, N), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float32)
    k = 7
    def local_mean(sel):
        x = np.where(sel, a, 0).astype(np.float32); w = sel.astype(np.float32)
        xs = np.asarray(Image.fromarray(x).filter(ImageFilter.BoxBlur(k))) if False else None
        from scipy.ndimage import uniform_filter
        return uniform_filter(x, k) / np.maximum(uniform_filter(w, k), 1e-6)
    mi, mo = local_mean(band_in), local_mean(band_out)
    edge = band_in | band_out
    diff = np.abs(mi - mo)[edge]
    print(f'{f.split("/")[-1]:45s} edge contrast {diff.mean():6.1f}   weak edge share {(diff < 12).mean():.2f}')
