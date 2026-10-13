import sys, glob, os
import numpy as np
from PIL import Image
src, fps, thr = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
files = sorted(glob.glob(os.path.join(src, 'f*.jpg')))
prev = None; diffs = []
for f in files:
    a = np.asarray(Image.open(f).convert('RGB').resize((96, 96 if 'fable' in src else 54)), dtype=np.float32)
    if prev is not None:
        # histogram-ish + pixel diff
        d = np.abs(a - prev).mean()
        diffs.append(d)
    else: diffs.append(0)
    prev = a
diffs = np.array(diffs)
cuts = [0] + [i for i in range(1, len(diffs)) if diffs[i] > thr]
print('n frames', len(files))
segs = []
for k, c in enumerate(cuts):
    e = cuts[k+1] if k+1 < len(cuts) else len(files)
    segs.append((c, e))
for c, e in segs:
    print(f'frame {c+1:4d}-{e:4d}  t={c/fps:6.3f}-{e/fps:6.3f}  hold={(e-c)/fps:5.3f}s ({e-c} fr)  diff_in={diffs[c]:.1f}')
