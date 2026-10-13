"""Map how a track moves: beat grid, bars, phrases, sections, events and per-frame energy.

usage: python map_track.py <audio> <out_dir> --id N --title T [--fps 60]

Writes into out_dir:
  map.json    machine-readable: grid, bars, sections, events, hits, 60 fps envelopes
  MAP.md      the same, written for a model planning a film against the music
  map.png     picture of the track (energy bands, sections, downbeats, events)
  check.mp3   the track with a click on every beat, an accent on bar 1 and a bell at each section
"""
import argparse, json, math, subprocess
from pathlib import Path

import numpy as np
import librosa
import soundfile as sf

FF = str(Path(__file__).resolve().parents[2] / "bin" / "ffmpeg")
SR = 44100
HOP = 441  # 10 ms


# ---------- grid ----------

def detect_beats(path):
    from beat_this.inference import File2Beats
    f2b = File2Beats(checkpoint_path="final0", device="cpu", dbn=False)
    beats, downs = f2b(str(path))
    return np.asarray(beats, float), np.asarray(downs, float)


def refine(t0, period, n, onset, times):
    """Nudge phase (±30 ms) and period (±0.2%) to put the grid on the actual transients."""
    o = onset / (onset.max() + 1e-9)
    def score(a, p):
        g = a + p * np.arange(int(n) + 1)
        return np.interp(g, times, o).sum()
    best = (score(t0, period), t0, period)
    for dp in np.linspace(-0.002, 0.002, 41) * period:
        for da in np.arange(-0.03, 0.0301, 0.002):
            s = score(t0 + da, period + dp)
            if s > best[0]:
                best = (s, t0 + da, period + dp)
    return best[1], best[2]


def refine_phase(t0, period, n, onset, times):
    """Nudge the phase (±30 ms) onto the actual transients. The period comes from the beats."""
    o = onset / (onset.max() + 1e-9)
    g = period * np.arange(int(n) + 1)
    cands = np.arange(-0.03, 0.0301, 0.001)
    sc = [np.interp(t0 + d + g, times, o).sum() for d in cands]
    return t0 + cands[int(np.argmax(sc))]


def fit_grid(beats, downs, duration, onset=None, times=None, low_onset=None):
    """Produced music holds tempo: fit one straight grid through the detected beats and
    extend it over the whole track, so quiet intros without drums still have a grid.
    The fit maximises phase coherence, so extra eighth-note or missed detections don't drag it."""
    def coherent(bb, centre, span, step):
        best = (-1.0, centre, 0.0)
        for period in centre * (1 + np.arange(-span, span + step / 2, step)):
            z = np.exp(2j * np.pi * bb / period).mean()
            if abs(z) > best[0]:
                best = (abs(z), period, (np.angle(z) / (2 * np.pi)) * period)
        return best
    # local tempo in 20 s windows; keep only windows where detection is confident
    wins, good = [], np.zeros(len(beats), bool)
    for w0 in np.arange(0, max(beats[-1] - 10, 1), 10):
        m = (beats >= w0) & (beats < w0 + 20)
        if m.sum() < 8:
            continue
        r, per, _ = coherent(beats[m], np.median(np.diff(beats[m])), 0.05, 0.0005)
        wins.append((r, per))
        if r > 0.85:
            good |= m
    confident = [per for r, per in wins if r > 0.85]
    p_est = float(np.median(confident)) if confident else float(np.median(np.diff(beats)))
    use = beats[good] if good.sum() >= 16 else beats
    _, period, t0 = coherent(use, p_est, 0.004, 0.00002)
    t0 = t0 % period
    n = int((duration - t0) / period) + 1
    if onset is not None:
        t0 = refine_phase(t0, period, n, onset, times)
    grid = t0 + period * np.arange(0, n)
    grid = grid[grid <= duration]
    gidx = np.round((beats - t0) / period)
    resid = beats - (t0 + period * gidx)
    aligned = np.abs(resid) < 0.04
    # beats per bar from the detected downbeats (3 or 4)
    gi = np.round((downs - t0) / period).astype(int)
    steps = np.diff(gi)
    steps = steps[(steps >= 2) & (steps <= 8)]
    bpb = int(np.bincount(steps).argmax()) if len(steps) else 4
    bpb = bpb if bpb in (3, 4) else (4 if bpb in (2, 8) else 3 if bpb == 6 else 4)
    votes = np.bincount(np.mod(gi, bpb), minlength=bpb).astype(float)
    agreement = votes.max() / max(votes.sum(), 1)
    phase = int(votes.argmax())
    phase_source = "downbeats"
    if agreement < 0.6 and low_onset is not None:
        # weak downbeat detection: put bar 1 where the kick hits hardest
        kick = np.interp(grid, times[: len(low_onset)], low_onset)
        gi_grid = np.arange(len(grid))
        k = np.array([kick[np.mod(gi_grid, bpb) == ph].mean() for ph in range(bpb)])
        phase = int(k.argmax()); phase_source = "kick"
    gi_grid = np.round((grid - t0) / period).astype(int)
    is_down = np.mod(gi_grid, bpb) == np.mod(phase, bpb)
    return {
        "bpm": 60.0 / period, "period": period, "beats_per_bar": bpb,
        "beats": grid, "is_down": is_down,
        "fit_ms": float(np.sqrt(np.mean(resid[aligned] ** 2)) * 1000) if aligned.any() else 999.0,
        "aligned_share": float(aligned.mean()),
        "downbeat_agreement": float(agreement), "downbeat_source": phase_source,
        "detected_beats": len(beats),
    }


# ---------- features ----------

def band_env(S, freqs, lo, hi):
    return S[(freqs >= lo) & (freqs < hi)].sum(0)


def features(y):
    S = np.abs(librosa.stft(y, n_fft=4096, hop_length=HOP)) ** 2
    freqs = librosa.fft_frequencies(sr=SR, n_fft=4096)
    env = {
        "low": band_env(S, freqs, 20, 150),
        "mid": band_env(S, freqs, 150, 2500),
        "high": band_env(S, freqs, 4000, 16000),
    }
    env["all"] = S.sum(0)
    onset = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP)
    low_onset = librosa.onset.onset_strength(S=librosa.power_to_db(S[freqs < 150]), sr=SR, hop_length=HOP)
    times = librosa.frames_to_time(np.arange(S.shape[1]), sr=SR, hop_length=HOP)
    return env, onset, low_onset, times


def db(x):
    return 10 * np.log10(np.maximum(x, 1e-12))


# ---------- structure ----------

def bar_table(grid, env, onset, times):
    downs = grid["beats"][grid["is_down"]]
    bar_len = grid["period"] * grid["beats_per_bar"]
    # include a partial pickup bar before the first downbeat
    starts = list(downs)
    while starts[0] - bar_len > -bar_len * 0.5 and starts[0] > 0.05:
        starts.insert(0, max(0.0, starts[0] - bar_len))
    bars = []
    for i, a in enumerate(starts):
        b = starts[i + 1] if i + 1 < len(starts) else a + bar_len
        m = (times >= a) & (times < b)
        if m.sum() < 5:
            continue
        bars.append({
            "bar": len(bars) + 1, "t": round(float(a), 3), "end": round(float(b), 3),
            "all": float(db(env["all"][m].mean())), "low": float(db(env["low"][m].mean())),
            "mid": float(db(env["mid"][m].mean())), "high": float(db(env["high"][m].mean())),
            "busy": float(onset[m].mean()),
        })
    return bars


def normalise_bars(bars):
    for key in ("all", "low", "mid", "high", "busy"):
        v = np.array([b[key] for b in bars])
        lo, hi = np.percentile(v, 5), np.percentile(v, 98)
        for b, x in zip(bars, v):
            b[key + "_n"] = float(np.clip((x - lo) / max(hi - lo, 1e-6), 0, 1))
    for b in bars:
        b["energy"] = round(0.45 * b["all_n"] + 0.25 * b["low_n"] + 0.15 * b["high_n"] + 0.15 * b["busy_n"], 3)


def find_sections(bars, first_full):
    """Boundaries land on phrase starts (every 4 bars from the first full bar) where the
    music changes most between the phrase before and the phrase after."""
    X = np.array([[b["all_n"], b["low_n"], b["mid_n"], b["high_n"], b["busy_n"]] for b in bars])
    n = len(bars)
    cands = [i for i in range(first_full + 4, n - 2, 4)]
    scores = {}
    for i in cands:
        a, b = X[max(0, i - 4):i].mean(0), X[i:min(n, i + 4)].mean(0)
        scores[i] = float(np.linalg.norm(a - b))
    if not scores:
        return [0]
    vals = np.array(list(scores.values()))
    thr = max(0.12, np.median(vals) + 0.3 * vals.std())
    bounds = [0] + ([first_full] if first_full >= 2 else []) + [i for i, s in scores.items() if s >= thr]
    bounds = sorted(set(bounds))
    # merge sections shorter than 4 bars into their neighbour
    out = [bounds[0]]
    for bnd in bounds[1:]:
        if bnd - out[-1] >= 4 or out[-1] == 0 and bnd == first_full:
            out.append(bnd)
    return out


def label_sections(bars, starts):
    secs = []
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else len(bars)
        bb = bars[s:e]
        en = np.array([b["energy"] for b in bb])
        secs.append({
            "start_bar": bb[0]["bar"], "end_bar": bb[-1]["bar"], "bars": len(bb),
            "t": bb[0]["t"], "end": bb[-1]["end"],
            "energy": round(float(en.mean()), 2),
            "trend": round(float(en[-1] - en[0]), 2) if len(en) > 1 else 0.0,
            "low": round(float(np.mean([b["low_n"] for b in bb])), 2),
            "high": round(float(np.mean([b["high_n"] for b in bb])), 2),
        })
    peak = max(s["energy"] for s in secs)
    for i, s in enumerate(secs):
        prev = secs[i - 1] if i else None
        nxt = secs[i + 1] if i + 1 < len(secs) else None
        rel = s["energy"] / max(peak, 1e-6)
        if i == 0 and rel < 0.75:
            name = "intro"
        elif nxt is None and rel < 0.7:
            name = "outro"
        elif rel >= 0.85 and prev is not None and s["energy"] - prev["energy"] >= 0.12:
            name = "drop"
        elif rel >= 0.8:
            name = "main"
        elif prev is not None and prev["energy"] - s["energy"] >= 0.15:
            name = "breakdown"
        elif s["trend"] >= 0.15 or (nxt is not None and nxt["energy"] - s["energy"] >= 0.12 and s["high"] >= s["low"]):
            name = "build"
        else:
            name = "groove"
        s["name"] = name
        s["level"] = "peak" if rel >= 0.9 else "high" if rel >= 0.75 else "mid" if rel >= 0.5 else "low"
    return secs


def find_events(bars, secs, grid, env, low_onset, onset, times, duration):
    ev = []
    floor = np.percentile([b["all"] for b in bars], 50) - 30
    for i in range(1, len(bars)):
        if bars[i]["all"] < floor or i == len(bars) - 1:
            continue  # the silent tail after the song ends
        d_low = bars[i]["low"] - bars[i - 1]["low"]
        if d_low >= 6:
            ev.append({"t": bars[i]["t"], "bar": bars[i]["bar"], "type": "bass_in", "db": round(d_low, 1)})
        elif d_low <= -6:
            ev.append({"t": bars[i]["t"], "bar": bars[i]["bar"], "type": "bass_out", "db": round(d_low, 1)})
    # risers: high band climbing 2+ bars into a section start
    for s in secs[1:]:
        j = s["start_bar"] - 1
        if j >= 3:
            h = [bars[k]["high"] for k in range(j - 3, j)]
            if h[2] - h[0] >= 3 and h[1] >= h[0] - 0.5:
                ev.append({"t": bars[j - 2]["t"], "bar": bars[j - 2]["bar"], "type": "riser", "to_bar": s["start_bar"],
                           "db": round(h[2] - h[0], 1)})
    # stops: near silence for at least one beat (a gap before a drop is a classic sync point)
    allv = db(env["all"])
    ref = np.percentile(allv, 90)
    quiet = allv < ref - 25
    run, start = 0, None
    for k, q in enumerate(quiet):
        if q:
            run += 1
            start = start if start is not None else k
        else:
            if start is not None and times[k] - times[start] >= grid["period"] * 0.9 and times[start] > 0.5:
                ev.append({"t": round(float(times[start]), 3), "type": "stop", "length": round(float(times[k] - times[start]), 2)})
            run, start = 0, None
    # hits: the strongest transients, snapped to the grid when close
    beats = grid["beats"]
    peaks = librosa.util.peak_pick(onset, pre_max=10, post_max=10, pre_avg=30, post_avg=30, delta=onset.std() * 1.5, wait=20)
    strength = onset[peaks]
    order = np.argsort(-strength)[: max(12, int(duration / 4))]
    hits = []
    for p in sorted(peaks[order]):
        t = float(times[p])
        j = int(np.argmin(np.abs(beats - t)))
        snapped = abs(beats[j] - t) < 0.06
        tt = float(beats[j]) if snapped else t
        hits.append({"t": round(tt, 3), "strength": round(float(onset[p] / onset.max()), 2),
                     "on_beat": bool(snapped), "downbeat": bool(snapped and grid["is_down"][j]),
                     "pos": position(tt, bars, grid)})
    for e in ev:
        e["t"] = round(float(e["t"]), 3)
    # a bass_out followed by bass_in one bar later is a one-bar dropout: the cleanest place for a hard cut
    ev = sorted(ev, key=lambda e: e["t"])
    merged, skip = [], set()
    for i, e in enumerate(ev):
        if i in skip:
            continue
        nxt = next((k for k in range(i + 1, len(ev)) if ev[k]["type"] == "bass_in"), None)
        if e["type"] == "bass_out" and nxt is not None and ev[nxt]["bar"] - e["bar"] <= 2:
            merged.append({"t": e["t"], "bar": e["bar"], "type": "break", "bars": ev[nxt]["bar"] - e["bar"],
                           "back_in": ev[nxt]["t"], "back_in_bar": ev[nxt]["bar"], "db": ev[nxt]["db"]})
            skip.add(nxt)
        else:
            merged.append(e)
    return merged, hits


def position(t, bars, grid):
    """bar.beat with quarter-beat resolution, e.g. "10.2.5" = bar 10, beat 2 and a half."""
    b = next((x for x in reversed(bars) if x["t"] <= t + 1e-3), bars[0])
    beat = (t - b["t"]) / grid["period"] + 1
    q = round(beat * 4) / 4
    return f"{b['bar']}.{q:g}"


def envelopes(env, onset, low_onset, times, duration, fps):
    ft = np.arange(0, duration, 1 / fps)
    out = {}
    for key in ("all", "low", "mid", "high"):
        v = db(env[key])
        lo, hi = np.percentile(v, 5), np.percentile(v, 99.5)
        n = np.clip((v - lo) / max(hi - lo, 1e-6), 0, 1)
        out[key] = np.round(np.interp(ft, times, n), 3).tolist()
    for key, v in (("onset", onset), ("kick", low_onset)):
        n = np.clip(v / np.percentile(v, 99.5), 0, 1)
        out[key] = np.round(np.interp(ft, times[: len(n)], n), 3).tolist()
    return out


# ---------- writers ----------

def fmt(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def bars_glyph(x, width=8):
    full = int(round(x * width))
    return "█" * full + "·" * (width - full)


def write_md(path, meta, grid, bars, secs, events, hits):
    bpb = grid["beats_per_bar"]
    bar_len = grid["period"] * bpb
    L = []
    L.append(f"# {meta['title']} (Mixkit #{meta['id']})\n")
    L.append(f"{meta['author']} · {fmt(meta['duration'])} · {grid['bpm']:.2f} BPM · {bpb}/4\n")
    L.append("## Grid\n")
    L.append(f"- One beat = {grid['period']:.4f} s. One bar = {bar_len:.4f} s. A 4-bar phrase = {4 * bar_len:.3f} s.")
    L.append(f"- Bar 1 starts at {bars[0]['t']:.3f} s"
             + (f" (a pickup bar; the first full downbeat is bar 2 at {bars[1]['t']:.3f} s)." if bars[0]['end'] - bars[0]['t'] < bar_len * 0.9 else "."))
    L.append(f"- Beat time: t(bar, beat) = bar_start[bar] + (beat - 1) × {grid['period']:.4f}. Every bar start is listed below; use those, not arithmetic over the whole song.")
    L.append(f"- Grid fit: {grid['aligned_share']*100:.0f}% of {grid['detected_beats']} detected beats sit within 40 ms of the grid ({grid['fit_ms']:.1f} ms RMS). Bar 1 placed by {'the downbeat model' if grid['downbeat_source'] == 'downbeats' else 'the strongest kick (the downbeat model was unsure)'}, agreement {grid['downbeat_agreement']*100:.0f}%.\n")
    L.append("## Sections\n")
    L.append("| Section | Bars | Time | Level | Energy | Low | High | Trend |")
    L.append("|---|---|---|---|---|---|---|---|")
    for s in secs:
        L.append(f"| {s['name']} | {s['start_bar']}–{s['end_bar']} ({s['bars']}) | {fmt(s['t'])}–{fmt(s['end'])} | {s['level']} | {s['energy']:.2f} | {s['low']:.2f} | {s['high']:.2f} | {s['trend']:+.2f} |")
    L.append("")
    L.append("Energy, Low and High are 0–1 within this track. Low is bass and kick, High is hats, air and risers. Trend is the energy change from the section's first bar to its last.\n")
    L.append("## Sync points\n")
    if events:
        for e in events:
            if e["type"] == "riser":
                L.append(f"- {fmt(e['t'])} bar {e['bar']}: riser (+{e['db']} dB in the highs) into bar {e['to_bar']}")
            elif e["type"] == "break":
                L.append(f"- {fmt(e['t'])} bar {e['bar']}: break, the bass drops out for {e['bars']} bar(s) and slams back in at bar {e['back_in_bar']} ({fmt(e['back_in'])}, {e['db']:+} dB)")
            elif e["type"] == "stop":
                L.append(f"- {fmt(e['t'])}: stop, {e['length']} s of near silence")
            else:
                L.append(f"- {fmt(e['t'])} bar {e['bar']}: {e['type'].replace('_', ' ')} ({e['db']:+} dB)")
    else:
        L.append("- No hard bass entries or stops. The track moves by texture, so cut on phrase starts.")
    L.append("")
    L.append("Strongest hits (sharpest transients, snapped to the beat when within 60 ms):\n")
    top = sorted(hits, key=lambda h: -h["strength"])[:16]
    L.append(", ".join(f"{fmt(h['t'])} @{h['pos']} ({h['strength']:.2f})" for h in sorted(top, key=lambda h: h["t"])))
    L.append("\n@bar.beat gives each hit's place in the bar: @10.2.5 is bar 10, halfway between beats 2 and 3. Strength is 0–1.\n")
    L.append("## Bar by bar\n")
    L.append("```")
    L.append("bar   time     section    energy    low      high     events")
    sec_at = {}
    for s in secs:
        for b in range(s["start_bar"], s["end_bar"] + 1):
            sec_at[b] = s["name"]
    ev_at = {}
    for e in events:
        if "bar" in e:
            label = {"riser": f"riser→{e.get('to_bar')}", "break": f"break→{e.get('back_in_bar')}"}.get(e["type"], e["type"].replace("_", " "))
            ev_at.setdefault(e["bar"], []).append(label)
        else:
            k = next((b["bar"] for b in bars if b["t"] <= e["t"] < b["end"]), None)
            if k:
                ev_at.setdefault(k, []).append("stop")
    starts = {s["start_bar"] for s in secs}
    first_full_bar = 2 if bars[0]["end"] - bars[0]["t"] < bar_len * 0.9 else 1
    for b in bars:
        mark = "▶" if b["bar"] in starts else "┊" if (b["bar"] - first_full_bar) % 4 == 0 and b["bar"] >= first_full_bar else " "
        L.append(f"{b['bar']:>3}{mark} {fmt(b['t']):>8}  {sec_at.get(b['bar'], ''):<10} {bars_glyph(b['energy'])}  {bars_glyph(b['low_n'], 6)}  {bars_glyph(b['high_n'], 6)}  {' '.join(ev_at.get(b['bar'], []))}")
    L.append("```\n")
    L.append("▶ marks a section start and ┊ a 4-bar phrase start (counted from the first full bar). Change scenes on these; change UI states on beats inside them.\n")
    path.write_text("\n".join(L))


def draw_png(path, meta, grid, bars, secs, events, env_fps, fps, duration):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    beats = np.asarray(grid["beats"])
    edges = np.append(beats, beats[-1] + grid["period"])
    def per_beat(v, how=np.mean):
        v = np.asarray(v); idx = (edges * fps).astype(int).clip(0, len(v))
        return np.array([how(v[idx[i]:max(idx[i] + 1, idx[i + 1])]) if idx[i] < len(v) else 0 for i in range(len(beats))])
    lanes = [("high", "#e76f51"), ("mid", "#2a9d8f"), ("low", "#1d3557"), ("onset", "#6c757d")]  # onset lane: the sharpest transient in each beat
    fig, axes = plt.subplots(len(lanes) + 1, 1, figsize=(16, 5.6), dpi=110, sharex=True,
                             gridspec_kw={"height_ratios": [0.7] + [1] * len(lanes), "hspace": 0.08})
    colors = {"intro": "#d9dde3", "build": "#ffd98a", "drop": "#ff9f8f", "main": "#ffc9b9", "breakdown": "#b9cdfb",
              "groove": "#e2dcf5", "outro": "#d9dde3"}
    top = axes[0]
    for s_ in secs:
        top.axvspan(s_["t"], s_["end"], color=colors.get(s_["name"], "#eee"), lw=0)
        if s_["end"] - s_["t"] > duration * 0.04:
            top.text((s_["t"] + s_["end"]) / 2, 0.5, f"{s_['name']}\nbar {s_['start_bar']}", ha="center", va="center", fontsize=8)
    for e in events:
        c = {"bass_in": "#c1121f", "bass_out": "#457b9d", "riser": "#f4a261", "stop": "#000", "break": "#7b2cbf"}.get(e["type"], "#555")
        top.plot([e["t"]], [0.08], marker="v", color=c, ms=7)
    top.set_yticks([]); top.set_ylim(0, 1)
    top.set_title(f"{meta['title']}  ·  {grid['bpm']:.2f} BPM {grid['beats_per_bar']}/4  ·  bars = thin lines, phrases = dark lines  ·  "
                  "▼ red bass in, blue bass out, purple break, orange riser", fontsize=9, loc="left")
    first_full = 1 if bars[0]["end"] - bars[0]["t"] < grid["period"] * grid["beats_per_bar"] * 0.9 else 0
    for ax, (key, col) in zip(axes[1:], lanes):
        v = per_beat(env_fps[key], np.max if key == "onset" else np.mean)
        ax.bar(beats, v, width=grid["period"] * 0.9, align="edge", color=col, lw=0)
        ax.set_ylim(0, 1.05); ax.set_yticks([]); ax.set_ylabel(key, rotation=0, ha="right", va="center", fontsize=8)
        for i, b_ in enumerate(bars):
            ph = i >= first_full and (i - first_full) % 4 == 0
            ax.axvline(b_["t"], color="#000", lw=0.8 if ph else 0.25, alpha=0.6 if ph else 0.25)
    axes[-1].set_xlim(0, duration); axes[-1].set_xlabel("seconds")
    fig.savefig(path, bbox_inches="tight"); plt.close(fig)


def write_check(path, audio_path, grid, secs, start, length):
    y, sr = librosa.load(audio_path, sr=SR, mono=False, offset=start, duration=length)
    if y.ndim == 1:
        y = np.vstack([y, y])
    n = y.shape[1]
    click = np.zeros(n)
    def tone(f, d, amp):
        t = np.arange(int(d * SR)) / SR
        return np.sin(2 * np.pi * f * t) * np.exp(-t * 60) * amp
    for t, down in zip(grid["beats"], grid["is_down"]):
        k = int((t - start) * SR)
        if 0 <= k < n:
            s = tone(2000 if down else 1200, 0.05, 0.5 if down else 0.25)
            click[k:k + len(s)] += s[: n - k]
    for s in secs:
        k = int((s["t"] - start) * SR)
        if 0 <= k < n:
            t = np.arange(int(0.6 * SR)) / SR
            bell = (np.sin(2 * np.pi * 880 * t) + 0.5 * np.sin(2 * np.pi * 1320 * t)) * np.exp(-t * 5) * 0.35
            click[k:k + len(bell)] += bell[: n - k]
    mix = y * 0.7 + click[None, :]
    mix /= max(1.0, np.abs(mix).max())
    wav = path.with_suffix(".wav")
    sf.write(wav, mix.T, SR)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(path)], check=True)
    wav.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("out")
    ap.add_argument("--id", type=int, required=True); ap.add_argument("--title", required=True)
    ap.add_argument("--author", default=""); ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--check-length", type=float, default=60)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    y, _ = librosa.load(a.audio, sr=SR, mono=True)
    duration = len(y) / SR
    beats, downs = detect_beats(a.audio)
    env, onset, low_onset, times = features(y)
    grid = fit_grid(beats, downs, duration, onset, times, low_onset)
    bars = bar_table(grid, env, onset, times)
    normalise_bars(bars)
    first_full = 1 if bars[0]["end"] - bars[0]["t"] < grid["period"] * grid["beats_per_bar"] * 0.9 else 0
    starts = find_sections(bars, first_full)
    secs = label_sections(bars, starts)
    events, hits = find_events(bars, secs, grid, env, low_onset, onset, times, duration)
    env_fps = envelopes(env, onset, low_onset, times, duration, a.fps)
    meta = {"id": a.id, "title": a.title, "author": a.author, "duration": round(duration, 3)}
    data = {
        **meta,
        "bpm": round(grid["bpm"], 3), "beat": round(grid["period"], 5), "beats_per_bar": grid["beats_per_bar"],
        "bar": round(grid["period"] * grid["beats_per_bar"], 5),
        "grid_fit_ms": round(grid["fit_ms"], 2), "aligned_share": round(grid["aligned_share"], 3),
        "downbeat_agreement": round(grid["downbeat_agreement"], 3), "downbeat_source": grid["downbeat_source"],
        "beats": [round(float(t), 4) for t in grid["beats"]],
        "downbeats": [round(float(t), 4) for t, d in zip(grid["beats"], grid["is_down"]) if d],
        "bars": [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in b.items()
                  if k in ("bar", "t", "end", "energy", "low_n", "mid_n", "high_n", "busy_n")} for b in bars],
        "sections": secs, "events": events, "hits": hits,
        "envelope": {"fps": a.fps, **env_fps},
    }
    (out / "map.json").write_text(json.dumps(data, separators=(",", ":")))
    write_md(out / "MAP.md", meta, grid, bars, secs, events, hits)
    draw_png(out / "map.png", meta, grid, bars, secs, events, env_fps, a.fps, duration)
    # check clip: centre it on the biggest energy rise so the bell, the drop and the clicks are all audible
    rises = [(secs[i]["energy"] - secs[i - 1]["energy"], secs[i]["t"]) for i in range(1, len(secs))]
    focus = max(rises)[1] if rises else 0
    start = max(0.0, min(focus - a.check_length / 2, duration - a.check_length))
    write_check(out / "check.mp3", a.audio, grid, secs, start, a.check_length)
    data["check"] = {"start": round(start, 3), "length": a.check_length}
    (out / "map.json").write_text(json.dumps(data, separators=(",", ":")))
    data_summary = {k: data[k] for k in ("id", "title", "bpm", "beats_per_bar", "grid_fit_ms", "aligned_share", "downbeat_agreement", "downbeat_source")}
    data_summary["sections"] = [f"{s['name']}@{s['start_bar']}" for s in secs]
    data_summary["check_start"] = round(start, 2)
    print(json.dumps(data_summary))


if __name__ == "__main__":
    main()
