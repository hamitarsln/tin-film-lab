"""Flash check for a draft (WCAG 2.3.1 general flash threshold, approximated the way broadcast checks do it):
  python3 scripts/flashcheck.py <video.mp4> [--grid 8] [--plot out.png]

Every frame is reduced to a grid of cells; each cell's relative luminance is computed from linear sRGB. A transition
between two frames is a "change" when at least 25% of the frame area moves by 0.1 or more of relative luminance in the
same direction, and the darker of the two states is below 0.8. A flash is a pair of opposing changes. The film fails
when any one-second window holds more than three flashes. Prints the worst windows and every change, with film time.
"""
import argparse, os, subprocess, sys
import numpy as np
from PIL import Image

FF = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'bin', 'ffmpeg')
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--grid', type=int, default=8)
ap.add_argument('--plot'); ap.add_argument('--fps', type=float, default=24)
a = ap.parse_args()
g = a.grid
raw = subprocess.run([FF, '-loglevel', 'error', '-i', a.video, '-vf', f'scale={g * 8}:{g * 8}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                     capture_output=True, check=True).stdout
n = len(raw) // (g * 8 * g * 8 * 3)
fr = np.frombuffer(raw, np.uint8)[:n * g * 8 * g * 8 * 3].reshape(n, g * 8, g * 8, 3).astype(np.float32) / 255
lin = np.where(fr <= 0.04045, fr / 12.92, ((fr + 0.055) / 1.055) ** 2.4)
Y = lin @ np.array([0.2126, 0.7152, 0.0722], np.float32)
cells = Y.reshape(n, g, 8, g, 8).mean((2, 4))            # n x g x g
mean = Y.mean((1, 2))
changes = []                                                # (frame index of the new state, sign)
for i in range(1, n):
    d = cells[i] - cells[i - 1]
    dark = np.minimum(cells[i], cells[i - 1]) < 0.8
    up = ((d >= 0.1) & dark).mean(); down = ((d <= -0.1) & dark).mean()
    if up >= 0.25: changes.append((i, +1))
    elif down >= 0.25: changes.append((i, -1))
win = int(round(a.fps))
worst = []
for s in range(0, n):
    seq = [c for c in changes if s <= c[0] < s + win]
    merged = []
    for c in seq:
        if not merged or merged[-1][1] != c[1]: merged.append(c)
    worst.append((len(merged) // 2, s))
mx = max(worst)[0] if worst else 0
print(f'{n} frames, {len(changes)} large luminance changes, max flashes in any 1 s window: {mx}  ({"PASS" if mx <= 3 else "FAIL"}, limit 3)')
bad = sorted({s for f, s in worst if f > 3})
if bad:
    print('windows over the limit start at:', ', '.join(f'{s / a.fps:.2f}s' for s in bad[:20]), '...' if len(bad) > 20 else '')
print('changes:', ' '.join(f'{i / a.fps:.2f}{"+" if sg > 0 else "-"}' for i, sg in changes))
if a.plot:
    from PIL import ImageDraw
    W, H = 1800, 300
    im = Image.new('RGB', (W, H), (246, 243, 235)); d = ImageDraw.Draw(im)
    X = lambda i: 20 + (W - 40) * i / max(1, n - 1)
    d.line([(X(i), H - 20 - mean[i] * (H - 40)) for i in range(n)], fill=(20, 20, 20), width=2)
    for i, sg in changes:
        d.line([(X(i), 10), (X(i), H - 10)], fill=(214, 40, 90) if sg > 0 else (40, 90, 214), width=1)
    for f, s in worst:
        if f > 3: d.line([(X(s), H - 6), (X(min(n - 1, s + win)), H - 6)], fill=(214, 40, 90), width=6)
    im.save(a.plot); print(a.plot)
