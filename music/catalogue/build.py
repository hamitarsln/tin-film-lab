"""Score analysed tracks, pick a vetting shortlist per style, cut previews around the first drop."""
import json, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np, librosa

HERE = Path(__file__).parent
FF = str(HERE.parent.parent / "bin" / "ffmpeg")
SR = 22050
PER_STYLE = 7

STYLES = [  # first match wins
    ("keynote", "Clean electronic", {"Technology", "Futuristic", "Electronica", "Synth", "Space"}),
    ("house", "Driving house", {"House", "Tech House", "Driving", "Propulsive", "EDM"}),
    ("hiphop", "Hip-hop and trap", {"Hip Hop", "Trap", "Contemporary R&B"}),
    ("cinematic", "Cinematic build", {"Cinematic", "Film Score", "Powerful", "Dramatic", "Determined", "Action"}),
    ("bright", "Bright and positive", {"Positive", "Uplifting", "Happy", "Pop", "Motivational", "Corporate Music", "Lively", "Indie Pop"}),
    ("calm", "Calm and minimal", {"Piano", "Ambient", "Atmospheric", "Reflective", "Chillout", "Relaxed", "Soft"}),
]

def first_drop(path, tempo):
    y, _ = librosa.load(path, sr=SR, mono=True)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512)) ** 2
    f = librosa.fft_frequencies(sr=SR, n_fft=2048)
    low = S[f < 150].sum(0)
    t = librosa.frames_to_time(np.arange(S.shape[1]), sr=SR, hop_length=512)
    bar = 4 * 60 / tempo
    edges = np.arange(0, len(y) / SR, bar)
    lb = np.array([10 * np.log10(low[(t >= a) & (t < a + bar)].mean() + 1e-12) for a in edges])
    for i in range(2, len(edges) - 2):
        if not 6 <= edges[i] <= 75: continue
        jump = lb[i:i + 2].mean() - lb[i - 2:i].mean()
        if jump >= 6:
            a = edges[i] - bar / 2
            win = np.arange(a, a + bar, 0.02)
            vals = np.array([10 * np.log10(low[(t >= w) & (t < w + 0.05)].mean() + 1e-12) for w in win])
            return round(float(win[int(np.argmax(np.diff(vals))) + 1]), 2), round(float(jump), 1)
    return None, 0.0

BEAT_TAGS = {"Hip Hop", "Trap", "Contemporary R&B", "House", "Tech House", "EDM"}

def style_of(tags, title):
    if any(w in title.lower() for w in ("wedding", "christmas", "new year", "holiday", "xmas", "birthday", "halloween", "love")):
        return None
    tags = set(tags)
    best = max(STYLES, key=lambda s: len(s[2] & tags))
    if not best[2] & tags: return None
    if best[0] == "calm" and tags & BEAT_TAGS: return None
    return best[0]

def score(t):
    s = 0.0
    bpm = t["bpm"]
    s += 3 if 100 <= bpm <= 135 else 1.5 if 85 <= bpm <= 150 else 0
    if t["first_drop"] is not None:
        s += min(t["first_drop_db"], 15) / 3          # contrast of the drop
        s += 1.5 if 8 <= t["first_drop"] <= 45 else 0.5  # drop where a 15-45s film can use it
    elif t["style"] == "calm":
        s += 2                                          # calm beds don't need a drop
    s += 1 if t["intro"] <= 12 else 0
    s += 1 if t["duration"] >= 75 else 0
    s += (t["steadiness"] - 0.9) * 10
    return round(s, 2)

def prep(item):
    tid, c, a = item
    bpm = a["tempo"] * 2 if a["tempo"] < 80 else a["tempo"]
    fd, fdj = first_drop(str(HERE / "mp3" / f"{tid}.mp3"), a["tempo"])
    return {**{k: c[k] for k in ("id", "title", "author", "duration", "tags")},
            "bpm": round(bpm, 1), "steadiness": a["steadiness"], "intro": a["intro"],
            "biggest_drop": a["drop"], "biggest_drop_db": a["drop_jump_db"],
            "first_drop": fd, "first_drop_db": fdj, "brightness": a["brightness"],
            "curve": a["curve"], "style": style_of(c["tags"], c["title"]),
            "source": f"https://assets.mixkit.co/music/{tid}/{tid}.mp3"}

if __name__ == "__main__":
    cands = json.loads((HERE / "candidates.json").read_text())
    an = json.loads((HERE / "analysis.json").read_text())
    items = [(k, cands[k], an[k]) for k in an]
    cache = HERE / "scored.json"
    if cache.exists():
        tracks = json.loads(cache.read_text())
        for t in tracks: t["style"] = style_of(t["tags"], t["title"])
    else:
        with ProcessPoolExecutor(7) as ex:
            tracks = list(ex.map(prep, items))
    for t in tracks: t["score"] = score(t)
    (HERE / "scored.json").write_text(json.dumps(tracks, indent=1))
    picked = []
    for key, label, _ in STYLES:
        pool = sorted((t for t in tracks if t["style"] == key), key=lambda t: -t["score"])
        picked += pool[:PER_STYLE]
    (HERE / "previews").mkdir(exist_ok=True)
    for t in picked:
        d = t["first_drop"] if t["first_drop"] is not None else (t["biggest_drop"] if t["biggest_drop"] and t["biggest_drop"] < t["duration"] - 15 else None)
        start = max(0.0, (d - 16) if d is not None else t["intro"])
        start = min(start, max(0.0, t["duration"] - 32))
        t["preview_start"], t["preview_len"] = round(start, 2), 32
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(start), "-t", "32", "-i", str(HERE / "mp3" / f"{t['id']}.mp3"),
                        "-af", "afade=t=in:d=0.4,afade=t=out:st=30.5:d=1.5", "-b:a", "128k", str(HERE / "previews" / f"{t['id']}.mp3")], check=True)
    out = {"styles": [{"key": k, "label": l} for k, l, _ in STYLES], "tracks": picked}
    (HERE / "catalogue.json").write_text(json.dumps(out, indent=1))
    print(len(picked), "picked")
    for t in picked:
        print(t["style"], t["id"], t["title"], "|", t["bpm"], "bpm drop", t["first_drop"], t["first_drop_db"], "score", t["score"])
