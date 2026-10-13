"""Measure tempo, beat steadiness, drop, intro length and energy shape for each mp3."""
import json, sys
from multiprocessing import Pool
from pathlib import Path
import numpy as np, librosa

HERE = Path(__file__).parent
SR = 22050

def analyze(path):
    y, sr = librosa.load(path, sr=SR, mono=True)
    dur = len(y) / sr
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    tempo = float(np.atleast_1d(tempo)[0])
    ibi = np.diff(beats)
    steadiness = float(1 - np.std(ibi) / np.mean(ibi)) if len(ibi) > 8 else 0.0
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512)) ** 2
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    times = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=512)
    low = S[freqs < 150].sum(0)
    full = S.sum(0)
    bar = 4 * 60 / tempo if tempo > 0 else 2.0
    edges = np.arange(0, dur, bar)
    def per_bar(e):
        return np.array([10 * np.log10(e[(times >= a) & (times < a + bar)].mean() + 1e-12) for a in edges])
    lowb, fullb = per_bar(low), per_bar(full)
    # drop = biggest rise in bass energy from the previous 2 bars to the next 2 bars, after 6s
    best = (0.0, None)
    for i in range(2, len(edges) - 2):
        if edges[i] < 6 or edges[i] > dur - 10: continue
        jump = lowb[i:i + 2].mean() - lowb[i - 2:i].mean()
        if jump > best[0]: best = (float(jump), i)
    drop, jump = None, best[0]
    if best[1] is not None:
        a = edges[best[1]] - bar / 2
        win = [(t, low[(times >= t) & (times < t + 0.05)].mean()) for t in np.arange(a, a + bar, 0.02)]
        vals = np.array([10 * np.log10(v + 1e-12) for _, v in win])
        k = int(np.argmax(np.diff(vals))) + 1
        drop = float(win[k][0])
        # snap to nearest detected beat when it is close
        if len(beats):
            nb = beats[np.argmin(np.abs(beats - drop))]
            if abs(nb - drop) < 0.12: drop = float(nb)
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    peak = rms.max()
    intro = float(times[np.argmax(rms >= 0.5 * peak)])
    curve = np.interp(np.linspace(0, len(rms) - 1, 80), np.arange(len(rms)), rms) / peak
    cent = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())
    dyn = float(np.percentile(fullb, 90) - np.percentile(fullb, 20))
    return {"id": int(Path(path).stem), "tempo": round(tempo, 2), "steadiness": round(steadiness, 3),
            "drop": None if drop is None else round(drop, 2), "drop_jump_db": round(jump, 1),
            "intro": round(intro, 2), "brightness": round(cent), "dynamics_db": round(dyn, 1),
            "measured_duration": round(dur, 1), "curve": [round(float(c), 3) for c in curve]}

if __name__ == "__main__":
    files = sorted((HERE / "mp3").glob("*.mp3"))
    with Pool(8) as p:
        res = p.map(analyze, files)
    (HERE / "analysis.json").write_text(json.dumps({r["id"]: r for r in res}, indent=1))
    print(len(res))
