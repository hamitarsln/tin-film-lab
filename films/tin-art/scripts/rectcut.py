"""Cut a flat rectangular object (a matchbook, a card) out of a photo by its corners, with a perspective warp.
Raw files are never edited.

  uv run --project ../.. python scripts/rectcut.py <raw> <out.png> [--crop x0,y0,x1,y1] [--dark 0.45] [--inset 4] [--corners x,y,x,y,x,y,x,y]

The object is found as the largest region darker than --dark (value 0-1) or, with --corners, given by hand
(top-left, top-right, bottom-right, bottom-left, in raw pixels). The quad is warped to an upright rectangle and
trimmed by --inset px so no background survives at the edge. Output is RGBA (opaque rectangle).
"""
import argparse
import numpy as np
import cv2
from PIL import Image


def order(pts):
    pts = np.array(pts, np.float32)
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]], np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('raw'); ap.add_argument('out')
    ap.add_argument('--crop'); ap.add_argument('--dark', type=float, default=0.45)
    ap.add_argument('--inset', type=int, default=4); ap.add_argument('--corners')
    a = ap.parse_args()
    im = np.asarray(Image.open(a.raw).convert('RGB'))
    ox = oy = 0
    if a.crop:
        v = [float(c) for c in a.crop.split(',')]
        if all(c <= 1 for c in v):
            v = [v[0] * im.shape[1], v[1] * im.shape[0], v[2] * im.shape[1], v[3] * im.shape[0]]
        x0, y0, x1, y1 = [int(round(c)) for c in v]
        im = im[y0:y1, x0:x1]; ox, oy = x0, y0
    if a.corners:
        c = [float(x) for x in a.corners.split(',')]
        quad = np.array([[c[0] - ox, c[1] - oy], [c[2] - ox, c[3] - oy], [c[4] - ox, c[5] - oy], [c[6] - ox, c[7] - oy]], np.float32)
    else:
        hsv = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
        dark = (hsv[..., 2] < a.dark * 255).astype(np.uint8)
        dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(dark, 8)
        big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
        pts = cv2.findNonZero((lab == big).astype(np.uint8))
        hull = cv2.convexHull(pts)
        approx = cv2.approxPolyDP(hull, 0.02 * cv2.arcLength(hull, True), True)
        if len(approx) != 4:
            approx = cv2.boxPoints(cv2.minAreaRect(pts))
        quad = order(approx.reshape(-1, 2))
    tl, tr, br, bl = quad
    w = int(round(max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl))))
    h = int(round(max(np.linalg.norm(bl - tl), np.linalg.norm(br - tr))))
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], np.float32)
    M = cv2.getPerspectiveTransform(quad, dst)
    warped = cv2.warpPerspective(im, M, (w, h), flags=cv2.INTER_LANCZOS4)
    k = a.inset
    warped = warped[k:h - k, k:w - k]
    rgba = np.dstack([warped, np.full(warped.shape[:2], 255, np.uint8)])
    Image.fromarray(rgba, 'RGBA').save(a.out)
    print(a.out, (w - 2 * k, h - 2 * k), 'quad (raw px):', [(round(x + ox), round(y + oy)) for x, y in quad])


if __name__ == '__main__':
    main()
