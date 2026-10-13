"""Cut objects out of raw scans for the board. Raw files are never edited; output is RGBA PNG in materials/cut/.

  uv run --project ../.. python scripts/cutout.py <raw> <out.png> [--crop x0,y0,x1,y1] [--mode rembg|flat]
         [--split N] [--min-area 0.002] [--erode 1] [--maxside 2400] [--rot deg] [--tol 28]

--crop    region of the raw image (pixels, or fractions if all values <= 1)
--mode    rembg: isnet-general-use matte (photos, objects on busy grounds)
          flat:  colour distance from the border colour (scans of cards/labels on a flat ground; crisper)
--split   keep the N largest separate objects and write <out>-1.png ... <out>-N.png (a sheet of cards)
--erode   shrink the matte by this many pixels so no background colour fringe survives
--maxside cap the long side of each output (downscale only; never upscale)
--hull    the object is convex (a card, a label, a matchbook): fill the convex hull of the largest shape, so light
          areas of the print that match the backdrop are not punched out
"""
import argparse, sys
import numpy as np
from PIL import Image
import cv2

Image.MAX_IMAGE_PIXELS = None


def load(path, crop, rot):
    im = Image.open(path)
    im = im.convert('RGB')
    if crop:
        v = [float(c) for c in crop.split(',')]
        if all(c <= 1.0 for c in v):
            v = [v[0] * im.width, v[1] * im.height, v[2] * im.width, v[3] * im.height]
        im = im.crop(tuple(int(round(c)) for c in v))
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True, fillcolor=tuple(int(c) for c in np.median(np.asarray(im)[:8].reshape(-1, 3), 0)))
    return im


def matte_rembg(im):
    from rembg import remove, new_session
    sess = new_session('isnet-general-use')
    # rembg works at ~1024 internally; run on a capped copy and upsample the matte
    k = min(1.0, 2048 / max(im.size))
    small = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS) if k < 1 else im
    m = remove(small, session=sess, only_mask=True)
    m = np.asarray(m.resize(im.size, Image.LANCZOS) if k < 1 else m, dtype=np.float32) / 255.0
    return m


def matte_flat(im, tol):
    a = np.asarray(im, dtype=np.float32)
    h, w = a.shape[:2]
    b = max(4, min(h, w) // 60)
    ring = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    bg = np.median(ring, 0)
    lab = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    bgl = cv2.cvtColor(bg.reshape(1, 1, 3).astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)[0, 0]
    d = np.sqrt(((lab - bgl) ** 2).sum(2))
    m = np.clip((d - tol * 0.6) / (tol * 0.8), 0, 1)
    # fill holes inside objects (light areas of a card that match the ground)
    hard = (m > 0.5).astype(np.uint8)
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ff = hard.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 1)
    holes = (ff == 0)
    m[holes] = 1.0
    return m


def hull_fill(m, keep=1):
    b = (m > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(b, 8)
    if n <= 1:
        return m
    order = sorted(range(1, n), key=lambda i: -stats[i, cv2.CC_STAT_AREA])[:keep]
    out = np.zeros_like(m)
    for i in order:
        pts = cv2.findNonZero((lab == i).astype(np.uint8))
        h = cv2.convexHull(pts)
        canvas = np.zeros(m.shape, np.uint8)
        cv2.fillConvexPoly(canvas, h, 255, lineType=cv2.LINE_AA)
        out = np.maximum(out, canvas.astype(np.float32) / 255.0)
    return out


def clean(m, erode):
    # sharpen the matte (kills the soft halo), then shrink it so no ground colour survives at the edge
    m = np.clip((m - 0.35) / 0.3, 0, 1)
    if erode > 0:
        m = cv2.erode(m, np.ones((2 * erode + 1, 2 * erode + 1), np.uint8))
    m = cv2.GaussianBlur(m, (3, 3), 0.7)
    return m


def decontaminate(rgb, m):
    # replace colour in the semi-transparent edge band with colour pulled in from the solid interior
    solid = (m > 0.98).astype(np.uint8)
    if solid.sum() == 0:
        return rgb
    out = rgb.astype(np.float32).copy()
    band = ((m > 0.01) & (m <= 0.98)).astype(np.uint8)
    if band.sum() == 0:
        return rgb
    filled = cv2.inpaint(rgb.astype(np.uint8), (1 - solid).astype(np.uint8) * 255, 3, cv2.INPAINT_TELEA).astype(np.float32)
    out[band == 1] = filled[band == 1]
    return out.astype(np.uint8)


def save_rgba(rgb, m, path, maxside):
    ys, xs = np.where(m > 0.02)
    if len(xs) == 0:
        print('empty matte for', path); return
    pad = 4
    x0, x1 = max(0, xs.min() - pad), min(m.shape[1], xs.max() + pad + 1)
    y0, y1 = max(0, ys.min() - pad), min(m.shape[0], ys.max() + pad + 1)
    rgba = np.dstack([rgb[y0:y1, x0:x1], (m[y0:y1, x0:x1] * 255).astype(np.uint8)])
    im = Image.fromarray(rgba, 'RGBA')
    if maxside and max(im.size) > maxside:
        k = maxside / max(im.size)
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    im.save(path)
    print(path, im.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('raw'); ap.add_argument('out')
    ap.add_argument('--crop'); ap.add_argument('--rot', type=float, default=0)
    ap.add_argument('--mode', default='rembg'); ap.add_argument('--tol', type=float, default=28)
    ap.add_argument('--split', type=int, default=0); ap.add_argument('--min-area', type=float, default=0.002)
    ap.add_argument('--erode', type=int, default=1); ap.add_argument('--maxside', type=int, default=2400)
    ap.add_argument('--hull', action='store_true')
    ap.add_argument('--band', type=float, default=0, help='with --hull: outer band (fraction of the short side) keeps the colour matte, so perforations and torn edges stay')
    a = ap.parse_args()
    im = load(a.raw, a.crop, a.rot)
    m = matte_rembg(im) if a.mode == 'rembg' else matte_flat(im, a.tol)
    if a.hull:
        hm = hull_fill(m, max(1, a.split))
        if a.band > 0:
            bp = max(2, int(a.band * min(m.shape)))
            inner = cv2.erode((hm > 0.5).astype(np.uint8), np.ones((2 * bp + 1, 2 * bp + 1), np.uint8))
            m = np.where(inner > 0, 1.0, np.minimum(hm, m)).astype(np.float32)
        else:
            m = hm
    m = clean(m, a.erode)
    rgb = decontaminate(np.asarray(im), m)
    if a.split:
        n, lab, stats, _ = cv2.connectedComponentsWithStats((m > 0.5).astype(np.uint8), 8)
        area = m.shape[0] * m.shape[1]
        comps = sorted([i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > a.min_area * area], key=lambda i: -stats[i, cv2.CC_STAT_AREA])[:a.split]
        # order left-to-right, top-to-bottom for stable names
        comps.sort(key=lambda i: (stats[i, cv2.CC_STAT_TOP] // max(1, m.shape[0] // 8), stats[i, cv2.CC_STAT_LEFT]))
        base = a.out[:-4] if a.out.endswith('.png') else a.out
        for k, i in enumerate(comps, 1):
            mk = np.where(cv2.dilate((lab == i).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0, m, 0)
            save_rgba(rgb, mk, f'{base}-{k}.png', a.maxside)
    else:
        save_rgba(rgb, m, a.out, a.maxside)


if __name__ == '__main__':
    main()
