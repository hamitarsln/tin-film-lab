"""Refit the Tin mark's curves. refs/brand/mark.svg is a traced polygon: the n's two arches are runs of short straight
segments whose vertices sit on a 0.25-unit grid, so a curve through every vertex (src/engine.js's old smoothing)
inherits the trace's wobble, which shows on the flat black end card at 2160 px.

This fits each arch with a least-squares cubic smoothing spline (approximating the trace, not interpolating it),
with its end tangents pinned to the straight stems it meets, and converts every spline span exactly to a cubic
Bezier. Straight edges (the T, the i and every stem) are kept vertex for vertex.

  uv run --project ../.. python scripts/markfit.py      -> src/mark-fit.js (window.MARK_FIT_D) and a report
"""
import re
import numpy as np
from scipy.interpolate import splprep, splev

svg = open('refs/brand/mark.svg').read()
D = re.search(r' d="([^"]+)"', svg).group(1)
subs = [[(float(a), float(b)) for a, b in re.findall(r'(-?[\d.]+),(-?[\d.]+)', s)] for s in D.split('Z') if s.strip()]
n = max(subs, key=len)                       # the n is the long subpath
others = [s for s in subs if s is not n]


def idx(pt):
    return min(range(len(n)), key=lambda i: (n[i][0] - pt[0]) ** 2 + (n[i][1] - pt[1]) ** 2)


# The two arches, as runs of the n's vertex list (it closes from the last vertex back to the first).
# Outer: from the top of the right stem (654, 273.5), up and over, to the shoulder (481, 209.75).
# Inner: from the top of the counter's left side (482.75, 299) over to its right side (581.25, 286.5).
N = len(n)
o0, o1 = idx((654.0, 273.5)), idx((481.0, 209.75))
i0, i1 = idx((482.75, 299.0)), idx((581.25, 286.5))
outer = [n[(o0 + k) % N] for k in range((o1 - o0) % N + 1)]
# the trace leaves a 0.75-unit ledge where the arch meets the left stem (481 -> 480.25): end the arch on the stem
outer[-1] = (480.25, 209.75)
inner = [n[(i0 + k) % N] for k in range((i1 - i0) % N + 1)]


def fit(run, t_start, t_end, tol):
    """Smoothing spline through `run`, end points fixed, end tangents pinned by mirrored ghost points.
    Returns cubic Bezier segments [(p0, p1, p2, p3), ...] and the max distance from the trace."""
    P = np.array(run, float)
    # densify the trace (straight segments between vertices) so long segments weigh by their length
    dense = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        L = np.hypot(*(b - a)); m = max(1, int(L / 1.0))
        dense += [a + (b - a) * (j / m) for j in range(1, m + 1)]
    Q = np.array(dense)
    # ghost points beyond each end along the pinned tangent hold the tangent; weights pin the end points
    g0 = [Q[0] - np.array(t_start) * s for s in (3.0, 2.0, 1.0)]
    g1 = [Q[-1] + np.array(t_end) * s for s in (1.0, 2.0, 3.0)]
    X = np.vstack([g0, Q, g1])
    w = np.ones(len(X)); w[:3] = 40; w[-3:] = 40; w[3] = 200; w[-4] = 200
    u = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(X, axis=0).T))]); u /= u[-1]
    best = None
    for s in [len(X) * f for f in (0.02, 0.01, 0.005, 0.0025, 0.001)]:
        tck, _ = splprep([X[:, 0], X[:, 1]], w=w, u=u, s=s, k=3)
        uu = np.linspace(u[3], u[-4], 4000)
        cx, cy = splev(uu, tck)
        C = np.stack([cx, cy], 1)
        d = np.array([np.min(np.hypot(*(C - q).T)) for q in Q[::3]])
        best = (tck, d.max(), s)
        if d.max() <= tol:
            break
    tck, err, s = best
    # exact Bezier conversion of each knot span inside [u_start, u_end]
    t, c, k = tck
    ua, ub = u[3], u[-4]
    knots = sorted(set([ua, ub] + [x for x in t if ua < x < ub]))
    segs = []
    for a, b in zip(knots[:-1], knots[1:]):
        p0 = np.array(splev(a, tck)); p3 = np.array(splev(b, tck))
        d0 = np.array(splev(a, tck, der=1)); d1 = np.array(splev(b, tck, der=1))
        p1 = p0 + d0 * (b - a) / 3; p2 = p3 - d1 * (b - a) / 3
        segs.append((p0, p1, p2, p3))
    # snap the ends exactly onto the trace's end vertices
    segs[0] = (np.array(run[0]), segs[0][1], segs[0][2], segs[0][3])
    segs[-1] = (segs[-1][0], segs[-1][1], segs[-1][2], np.array(run[-1]))
    return segs, err, s


def unit(v):
    v = np.array(v, float); return v / np.hypot(*v)


# outer: leaves the right stem going straight up; arrives at the shoulder along the trace's last direction
outer_segs, eo, so = fit(outer, (0, -1), unit(np.subtract(outer[-1], outer[-2])), tol=0.45)
# inner: leaves the counter's left side going straight up, arrives at its right side going straight down
inner_segs, ei, si = fit(inner, (0, -1), (0, 1), tol=0.45)


def fmt(p):
    return f'{p[0]:.3f},{p[1]:.3f}'


# rebuild the n: straight vertices outside the arches, Beziers along them, in the original winding order
out = []
k = (o1) % N
pts = []
# walk the n from the outer arch's end (shoulder) all the way round to the outer arch's start
cmds = [f'M{fmt(outer[-1])}']
j = (o1 + 1) % N   # skip the trace's ledge vertex (480.25, 209.75), now the arch's own end point
while True:
    j = (j + 1) % N
    if j == i0:
        cmds.append(f'L{fmt(n[i0])}')
        for (p0, p1, p2, p3) in inner_segs:
            cmds.append(f'C{fmt(p1)} {fmt(p2)} {fmt(p3)}')
        j = i1
        continue
    if j == o0:
        cmds.append(f'L{fmt(n[o0])}')
        for (p0, p1, p2, p3) in outer_segs:
            cmds.append(f'C{fmt(p1)} {fmt(p2)} {fmt(p3)}')
        break
    cmds.append(f'L{fmt(n[j])}')
n_d = ' '.join(cmds) + ' Z'
rest = ' '.join('M' + ' L'.join(fmt(p) for p in s) + ' Z' for s in others)
d = rest + ' ' + n_d
open('src/mark-fit.js', 'w').write(
    '// Generated by scripts/markfit.py: refs/brand/mark.svg with the n\'s two arches refitted as smooth cubic\n'
    '// Beziers (least-squares smoothing spline, max deviation from the trace in the report); straight edges unchanged.\n'
    f'window.MARK_FIT_D = "{d}";\n')
print(f'outer arch: {len(outer)} trace vertices -> {len(outer_segs)} Beziers, max deviation {eo:.2f} units (s={so:.2f})')
print(f'inner arch: {len(inner)} trace vertices -> {len(inner_segs)} Beziers, max deviation {ei:.2f} units (s={si:.2f})')
print('wrote src/mark-fit.js')
