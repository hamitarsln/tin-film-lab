"""Prepare board materials from raw downloads, from a recipe file. Raw files are never edited.

  python3 scripts/prep.py scripts/recipes.json [name ...]

Recipe entries (JSON list):
  {"name": "classifieds", "op": "tex", "src": "materials/raw/...", "out": "materials/cut/07-classifieds.png",
   "box": [x0, y0, x1, y1]  # fractions of the source (or pixels if any value > 1); the region that fills the frame
   "rot": 0, "size": 2160, "gray": false, "levels": [black, white] (optional, 0-255 stretch), "sat": 1.0}
op "tex": the box is resized to cover a size x size square (the board frame), so frame pixels map to source
pixels with no further resampling in the browser.
"""
import json, sys
import numpy as np
from PIL import Image, ImageEnhance

Image.MAX_IMAGE_PIXELS = None


def box_px(im, box):
    if all(v <= 1.0 for v in box):
        return [box[0] * im.width, box[1] * im.height, box[2] * im.width, box[3] * im.height]
    return box


def tex(r):
    im = Image.open(r['src'])
    if im.mode not in ('RGB', 'L'):
        im = im.convert('RGB')
    if r.get('rot'):
        im = im.rotate(r['rot'], resample=Image.BICUBIC, expand=False)
    x0, y0, x1, y1 = box_px(im, r['box'])
    size = r.get('size', 2160)
    # make the box square around its centre (cover), never upscale silently: warn instead
    w, h = x1 - x0, y1 - y0
    side = min(w, h)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    crop = im.crop((int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2)))
    if side < size:
        print(f"  warning: {r['name']} upscales {side:.0f}px -> {size}px ({size / side:.2f}x)")
    crop = crop.convert('L' if r.get('gray') else 'RGB').resize((size, size), Image.LANCZOS)
    if r.get('levels'):
        lo, hi = r['levels']
        a = np.asarray(crop, dtype=np.float32)
        a = np.clip((a - lo) / max(1, hi - lo), 0, 1) * 255
        crop = Image.fromarray(a.astype(np.uint8))
    if r.get('sat') and crop.mode == 'RGB':
        crop = ImageEnhance.Color(crop).enhance(r['sat'])
    crop.convert('RGBA').save(r['out'])  # materials skill: prepared files are PNG with alpha (opaque for textures)
    print(r['out'], crop.size, f'source px per frame px: {side / size:.2f}')


def main():
    recipes = json.load(open(sys.argv[1]))
    only = set(sys.argv[2:])
    for r in recipes:
        if only and r['name'] not in only:
            continue
        {'tex': tex}[r['op']](r)


if __name__ == '__main__':
    main()
