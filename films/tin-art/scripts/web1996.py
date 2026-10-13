"""Still 18, the web in 1996, made in code: the Tin mark snapped to a pixel grid as a banner-ad GIF.

  python3 scripts/web1996.py banner <out.png> [--px 20] [--shift 0] [--no-cursor]
  python3 scripts/web1996.py preview <out.png> <texture.png> ...   (composites on paper; 750 and 360 px sheets)

What makes it 1996 rather than "pixel art":
- Web-safe colour. Every pixel is one of the 216 browser-safe colours (channels 0, 51, 102, 153, 204, 255). Banner GIFs
  were squeezed to a handful of those to stay under the ad networks' file-size limits, so the blend is drawn from five
  hot web-safe colours only.
- Banner-ad dither. The blend is an ordered (Bayer 4x4) dither between neighbouring palette colours, the cross-hatch a
  limited palette left on every gradient and photo of the time.
- The button. The mark has the raised bevel of a 1996 GIF button (white light edge, dark grey and black shadow edge,
  all on the pixel grid, no anti-aliasing).
- The link. The pointing-hand cursor of a 1996 browser rests on the n: this is something to click.

Writes a 2160x2160 RGBA texture aligned to the film frame (transparent off the mark and the cursor). --shift N moves
the blend N cells along its axis, so an animated-GIF frame can be made for motion.
"""
import argparse, math, re
import numpy as np
from PIL import Image, ImageDraw

W = H = 2160
S = 0.7741 * W / 608
MX, MY = W / 2 - 350 * S, H / 2 - 360.875 * S
BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16
# Five hot web-safe colours, in blend order: magenta, rose, red-orange, orange, yellow. Neighbours sit far apart in
# the colour cube, so every dithered seam between them shows as a cross-hatch, as it did in a 16-colour banner GIF.
BANNER = [(255, 0, 255), (255, 0, 102), (255, 51, 0), (255, 153, 0), (255, 255, 0)]
LIGHT, SHADE, BLACK = (255, 255, 255), (102, 102, 102), (0, 0, 0)
# 1-bit pointing-hand link cursor: 1 = black outline, 2 = white fill.
HAND = [
    "....11..........",
    "...1221.........",
    "...1221.........",
    "...1221.........",
    "...1221111......",
    "...12212211111..",
    "11.122122122121.",
    "1211222222221221",
    "1221222222222221",
    ".122222222222221",
    "..12222222222221",
    "..1222222222221.",
    "...122222222221.",
    "...12222222221..",
    "....1222222221..",
    "....1111111111..",
]


def mark_paths():
    """The mark as polygons in viewBox units: src/mark-fit.js (the traced mark with the n's arches refitted as smooth
    Beziers, scripts/markfit.py), with every Bezier flattened to 64 segments."""
    js = open('src/mark-fit.js').read()
    d = re.search(r'MARK_FIT_D = "([^"]+)"', js).group(1)
    polys, cur = [], []
    for cmd, args in re.findall(r'([MLCZ])([^MLCZ]*)', d):
        v = [float(x) for x in re.findall(r'-?[\d.]+', args)]
        if cmd == 'M':
            if cur: polys.append(cur)
            cur = [(v[0], v[1])]
        elif cmd == 'L':
            cur.append((v[0], v[1]))
        elif cmd == 'C':
            p0 = cur[-1]; p1, p2, p3 = (v[0], v[1]), (v[2], v[3]), (v[4], v[5])
            for k in range(1, 65):
                t = k / 64; u = 1 - t
                cur.append((u**3 * p0[0] + 3*u*u*t * p1[0] + 3*u*t*t * p2[0] + t**3 * p3[0],
                            u**3 * p0[1] + 3*u*u*t * p1[1] + 3*u*t*t * p2[1] + t**3 * p3[1]))
        elif cmd == 'Z':
            if cur: polys.append(cur); cur = []
    if cur: polys.append(cur)
    return polys


def mark_mask(scale=4):
    """The mark rasterised at `scale` x the frame (2160) for accurate cell coverage, returned at frame size."""
    im = Image.new('L', (W * scale, H * scale), 0)
    dr = ImageDraw.Draw(im)
    for poly in mark_paths():
        dr.polygon([((MX + x * S) * scale, (MY + y * S) * scale) for x, y in poly], fill=255)
    a = np.asarray(im, dtype=np.float32) / 255.0
    return a.reshape(H, scale, W, scale).mean((1, 3))


def cells_of_mark(px):
    """A cell belongs to the mark when at least half of it is inside the vector mark."""
    gw, gh = W // px, H // px
    m = mark_mask()[:gh * px, :gw * px]
    return m.reshape(gh, px, gw, px).mean((1, 3)) >= 0.5


def blend(gh, gw, palette, angle, shift):
    """Ordered dither of a straight blend through `palette`: each cell picks one of the two neighbouring colours by
    the Bayer threshold, so the blend reads as cross-hatched bands, never as a smooth gradient."""
    yy, xx = np.mgrid[0:gh, 0:gw].astype(np.float32)
    a = math.radians(angle)
    u = xx * math.cos(a) + yy * math.sin(a) + shift
    u = (u - u.min()) / (u.max() - u.min())
    p = u * (len(palette) - 1)
    base = np.clip(np.floor(p).astype(int), 0, len(palette) - 2)
    t = np.tile(BAYER4, (gh // 4 + 1, gw // 4 + 1))[:gh, :gw]
    idx = base + ((p - base) > t)
    return np.array(palette, np.uint8)[np.clip(idx, 0, len(palette) - 1)]


def bevel(cells, inside):
    """Raised 1996 button edge on the mark's own outline: light on the top and left edge cells, black on the bottom
    and right edge cells, dark grey one cell further in."""
    def shifted(dy, dx):
        s = np.zeros_like(inside)
        ys = slice(max(0, -dy), inside.shape[0] - max(0, dy)); yd = slice(max(0, dy), inside.shape[0] - max(0, -dy))
        xs = slice(max(0, -dx), inside.shape[1] - max(0, dx)); xd = slice(max(0, dx), inside.shape[1] - max(0, -dx))
        s[yd, xd] = inside[ys, xs]
        return s
    top = inside & (~shifted(1, 0) | ~shifted(0, 1))
    bottom = inside & (~shifted(-1, 0) | ~shifted(0, -1))
    bottom2 = inside & ~bottom & (~shifted(-2, 0) | ~shifted(0, -2))
    out = cells.copy()
    out[bottom2] = SHADE
    out[bottom] = BLACK
    out[top & ~bottom] = LIGHT
    return out


def checker(gh, gw, c1, c2, level=0.5):
    """A flat colour that is not in the web palette, as a GIF showed it: two web-safe colours in a Bayer pattern."""
    t = np.tile(BAYER4, (gh // 4 + 1, gw // 4 + 1))[:gh, :gw]
    out = np.zeros((gh, gw, 3), np.uint8); out[:] = c1; out[t < level] = c2
    return out


def bands(gh, gw, palette, band, angle, seam=0.5):
    """Flat bands of web-safe colour (no blend), each seam a short ordered-dither step between neighbours: how a
    designer limited to the web palette drew a banner background."""
    yy, xx = np.mgrid[0:gh, 0:gw].astype(np.float32)
    a = math.radians(angle)
    u = xx * math.cos(a) + yy * math.sin(a); u = u - u.min()
    k = np.floor(u / band).astype(int); f = (u - k * band) / band
    t = np.tile(BAYER4, (gh // 4 + 1, gw // 4 + 1))[:gh, :gw]
    nxt = np.minimum(k + 1, len(palette) - 1); k = np.minimum(k, len(palette) - 1)
    # the last `seam` of each band dithers into the next colour, 25/50/75%
    w = np.clip((f - (1 - seam)) / seam, 0, 1)
    pick = np.where(w > t, nxt, k)
    return np.array(palette, np.uint8)[pick]


def shadow(cells, inside, color=(0, 0, 0)):
    """Hard one-cell drop shadow down and to the right, outside the mark (the GIF text shadow of the time)."""
    sh = np.zeros_like(inside); sh[1:, 1:] = inside[:-1, :-1]
    ring = sh & ~inside
    return ring


def banner2(a):
    px = a.px
    inside = cells_of_mark(px)
    gh, gw = inside.shape
    if a.fill == 'checker':
        cells = checker(gh, gw, (255, 0, 0), (255, 204, 0), 0.5)
    elif a.fill == 'bands':
        cells = bands(gh, gw, [(255, 0, 153), (255, 0, 51), (255, 102, 0), (255, 204, 0)], band=a.band, angle=90, seam=0.45)
    elif a.fill == 'bands-h':
        cells = bands(gh, gw, [(255, 0, 153), (255, 0, 51), (255, 102, 0), (255, 204, 0)], band=a.band, angle=0, seam=0.45)
    rgba = np.zeros((gh, gw, 4), np.uint8)
    rgba[..., :3] = cells; rgba[..., 3] = inside * 255
    if a.shadow:
        ring = shadow(cells, inside)
        rgba[ring] = (0, 0, 0, 255)
    used = {tuple(c) for c in rgba[rgba[..., 3] > 0][:, :3]}
    assert all(v % 51 == 0 for c in used for v in c), 'non web-safe colour'
    big = Image.fromarray(rgba, 'RGBA').resize((gw * px, gh * px), Image.NEAREST)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.paste(big, (0, 0))
    canvas.save(a.out)
    print(a.out, f'grid {gw}x{gh}, {len(used)} web-safe colours')


def banner(a):
    px = a.px
    inside = cells_of_mark(px)
    gh, gw = inside.shape
    cells = bevel(blend(gh, gw, BANNER, 70, a.shift), inside)
    rgba = np.zeros((gh, gw, 4), np.uint8)
    rgba[..., :3] = cells; rgba[..., 3] = inside * 255
    if not a.no_cursor:
        ys, xs = np.where(inside)
        # fingertip on the right edge of the n's right stem, a little below the middle of the mark
        cx = xs.max() - 6
        cy = int(ys.min() + (ys.max() - ys.min()) * 0.56)
        for j, row in enumerate(HAND):
            for i, ch in enumerate(row):
                if ch != '.':
                    rgba[cy + j, cx + i] = (*BLACK, 255) if ch == '1' else (*LIGHT, 255)
    used = {tuple(c) for c in rgba[rgba[..., 3] > 0][:, :3]}
    assert all(v % 51 == 0 for c in used for v in c), 'non web-safe colour'
    big = Image.fromarray(rgba, 'RGBA').resize((gw * px, gh * px), Image.NEAREST)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.paste(big, (0, 0))
    canvas.save(a.out)
    print(a.out, f'grid {gw}x{gh}, {len(used)} web-safe colours')


def preview(out, textures):
    rng = np.random.default_rng(3)
    base = np.zeros((H, W, 4), np.float32); base[..., :3] = (245, 241, 230); base[..., 3] = 255
    base[..., :3] += rng.normal(0, 2.0, (H, W))[..., None]
    paper = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGBA')
    tiles = []
    for t in textures:
        im = paper.copy(); im.alpha_composite(Image.open(t).convert('RGBA')); tiles.append(im.convert('RGB'))
    big = Image.new('RGB', (len(tiles) * 760 + 10, 760), 'white')
    small = Image.new('RGB', (len(tiles) * 370 + 10, 370), 'white')
    for i, im in enumerate(tiles):
        big.paste(im.resize((750, 750), Image.LANCZOS), (10 + i * 760, 5))
        small.paste(im.resize((360, 360), Image.LANCZOS), (10 + i * 370, 5))
    big.save(out.replace('.png', '-750.png')); small.save(out.replace('.png', '-360.png'))
    print(out.replace('.png', '-750.png'), out.replace('.png', '-360.png'))


if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'preview':
        preview(sys.argv[2], sys.argv[3:]); raise SystemExit
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['banner', 'banner2']); ap.add_argument('out')
    ap.add_argument('--fill', default='bands'); ap.add_argument('--band', type=float, default=14); ap.add_argument('--shadow', action='store_true')
    ap.add_argument('--px', type=int, default=20); ap.add_argument('--shift', type=float, default=0)
    ap.add_argument('--no-cursor', action='store_true')
    a = ap.parse_args()
    (banner2 if a.kind == 'banner2' else banner)(a)
