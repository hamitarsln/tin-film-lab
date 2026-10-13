"""Textures where code is the honest medium, made from a real public-domain source image.

  python3 scripts/codetex.py halftone <src> <out.png> [--crop x0,y0,x1,y1] [--cell 26] [--cmyk] [--angle 45] [--seed 1]
  python3 scripts/codetex.py pixels   <src> <out.png> [--crop ...] [--px 20] [--seed 1]

Both write a 2160x2160 RGBA texture aligned to the board frame. Halftone: ink dots on transparent paper (the page
clips it with the mark). Pixels: the mark itself rasterised on a pixel grid (cells at least half inside the mark),
coloured from the source dithered to the 216-colour web palette, everything else transparent.
"""
import argparse, math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

Image.MAX_IMAGE_PIXELS = None
W = H = 2160
S = 0.7741 * W / 608
MX, MY = W / 2 - 350 * S, H / 2 - 360.875 * S


def mark_mask(scale=1):
    d = open('refs/brand/mark.svg').read()
    path = re.search(r' d="([^"]+)"', d).group(1)
    im = Image.new('L', (W * scale, H * scale), 0)
    dr = ImageDraw.Draw(im)
    polys = []
    for sub in [s for s in path.split('Z') if s.strip()]:
        nums = list(map(float, re.findall(r'[-\d.]+', sub)))
        polys.append([((MX + x * S) * scale, (MY + y * S) * scale) for x, y in zip(nums[0::2], nums[1::2])])
    # the n's counter is a separate contour inside the n polygon? No: the path's n is one outline, so fill each.
    for p in polys:
        dr.polygon(p, fill=255)
    return np.asarray(im, dtype=np.float32) / 255.0


def load(src, crop, size):
    im = Image.open(src).convert('RGB')
    if crop:
        v = [float(c) for c in crop.split(',')]
        if all(c <= 1.0 for c in v):
            v = [v[0] * im.width, v[1] * im.height, v[2] * im.width, v[3] * im.height]
        im = im.crop(tuple(int(round(c)) for c in v))
    # cover-fit to size
    k = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((max(size[0], int(im.width * k)), max(size[1], int(im.height * k))), Image.LANCZOS)
    x0, y0 = (im.width - size[0]) // 2, (im.height - size[1]) // 2
    return im.crop((x0, y0, x0 + size[0], y0 + size[1]))


def screen(gray, cell, angle, rng, gain=0.08):
    """Amplitude-modulated dots. gray: float array 0..1 (1 = paper). Returns ink coverage 0..1 (antialiased)."""
    h, w = gray.shape
    a = math.radians(angle)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx * math.cos(a) + yy * math.sin(a)) / cell
    v = (-xx * math.sin(a) + yy * math.cos(a)) / cell
    fu, fv = u - np.floor(u) - 0.5, v - np.floor(v) - 0.5
    dist = np.sqrt(fu * fu + fv * fv)  # 0 at cell centre, ~0.707 at corner
    # sample tone at the cell centre so each dot is one size (like a real screen)
    cu, cv = np.floor(u) + 0.5, np.floor(v) + 0.5
    cx = (cu * math.cos(a) - cv * math.sin(a)) * cell
    cy = (cu * math.sin(a) + cv * math.cos(a)) * cell
    cxi = np.clip(cx, 0, w - 1).astype(np.int32); cyi = np.clip(cy, 0, h - 1).astype(np.int32)
    ink = 1.0 - gray[cyi, cxi]
    ink = np.clip(ink * (1 + gain) - gain * 0.3, 0, 1)  # a little dot gain
    r = np.sqrt(ink / math.pi) * 1.02  # radius in cell units for that area
    # ragged ink edge: perturb the distance field with fine noise
    noise = rng.normal(0, 1, (h // 3 + 1, w // 3 + 1)).astype(np.float32)
    noise = np.asarray(Image.fromarray(noise).resize((w, h), Image.BILINEAR))
    dist = dist + noise * 0.018
    aa = 1.2 / cell
    cov = np.clip((r - dist) / aa + 0.5, 0, 1)
    return cov


def halftone(a):
    rng = np.random.default_rng(a.seed)
    src = load(a.src, a.crop, (W, H))
    if a.blur:
        src = src.filter(ImageFilter.GaussianBlur(a.blur))
    rgb = np.asarray(src, dtype=np.float32) / 255.0
    paper = np.array([245, 241, 230], np.float32) / 255.0
    if not a.cmyk:
        g = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
        lo, hi = np.percentile(g, 1), np.percentile(g, 99)
        g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1) ** a.gamma
        cov = screen(g, a.cell, a.angle, rng)
        ink = np.array([8, 8, 8], np.float32) / 255.0
        out = np.zeros((H, W, 4), np.float32); out[..., :3] = ink; out[..., 3] = cov * 0.94
    else:
        k = 1 - rgb.max(2)
        c = (1 - rgb[..., 0] - k) / np.maximum(1e-3, 1 - k)
        m = (1 - rgb[..., 1] - k) / np.maximum(1e-3, 1 - k)
        y = (1 - rgb[..., 2] - k) / np.maximum(1e-3, 1 - k)
        inks = {'c': (np.array([0, 158, 224]) / 255.0, c, 15), 'm': (np.array([226, 0, 122]) / 255.0, m, 75),
                'y': (np.array([255, 230, 0]) / 255.0, y, 0), 'k': (np.array([20, 20, 20]) / 255.0, k, 45)}
        # subtractive mix over paper, kept as an opaque layer; alpha marks where any ink landed
        acc = np.ones((H, W, 3), np.float32) * paper
        any_ink = np.zeros((H, W), np.float32)
        for name, (col, amt, ang) in inks.items():
            cov = screen(1 - np.clip(amt, 0, 1), a.cell, ang + a.angle - 45, rng)
            acc = acc * (1 - cov[..., None] * (1 - col[None, None, :] * 0.98))
            any_ink = np.maximum(any_ink, cov)
        out = np.zeros((H, W, 4), np.float32); out[..., :3] = acc; out[..., 3] = 1.0
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA').save(a.out)
    print(a.out)


def web_palette():
    vals = [0, 51, 102, 153, 204, 255]
    pal = [(r, g, b) for r in vals for g in vals for b in vals]
    flat = [c for p in pal for c in p] + [0] * (768 - 3 * len(pal))
    im = Image.new('P', (1, 1)); im.putpalette(flat); return im


def pixels(a):
    px = a.px
    gw, gh = W // px, H // px
    src = load(a.src, a.crop, (gw * px, gh * px)).resize((gw, gh), Image.BOX)
    q = src.quantize(palette=web_palette(), dither=Image.Dither.FLOYDSTEINBERG).convert('RGB')
    cells = np.asarray(q, dtype=np.uint8)
    # coverage of the mark per cell, measured at 4x
    m = mark_mask(1)
    cov = m[:gh * px, :gw * px].reshape(gh, px, gw, px).mean((1, 3))
    alpha = (cov >= 0.5).astype(np.uint8) * 255
    out = np.zeros((gh, gw, 4), np.uint8); out[..., :3] = cells; out[..., 3] = alpha
    big = Image.fromarray(out, 'RGBA').resize((gw * px, gh * px), Image.NEAREST)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.paste(big, (0, 0))
    canvas.save(a.out); print(a.out, 'grid', gw, 'x', gh)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('kind'); ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--crop'); ap.add_argument('--cell', type=float, default=26); ap.add_argument('--angle', type=float, default=45)
    ap.add_argument('--cmyk', action='store_true'); ap.add_argument('--px', type=int, default=20); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--blur', type=float, default=0, help='descreen: gaussian blur radius (px) on the source before screening')
    ap.add_argument('--gamma', type=float, default=1.0)
    a = ap.parse_args()
    {'halftone': halftone, 'pixels': pixels}[a.kind](a)
